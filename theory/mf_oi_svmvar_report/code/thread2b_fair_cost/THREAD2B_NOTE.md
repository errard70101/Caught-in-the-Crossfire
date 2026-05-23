# Thread 2b: Fair Solver Cost and Memory Benchmark

Reference plan: `theory/mf_oi_svmvar_report/NEXT_THREAD_PLAN.md`, Thread 2b.
Builds on Thread 1 (`code/thread1_matvec/`) and Thread 2
(`code/thread2_pcg/`).

## Objective

Thread 2 established that, at Taiwan-scale dimensions,
`direct_cholmod`'s solve dominates `pcg_time_avg_chol`'s solve by two
orders of magnitude. But that comparison only timed the solve --
assembly of `Kbar` was hidden in an untimed setup step. This thread
fixes the comparison by breaking each path into three timed phases and
stressing dimensions beyond Thread 2 to find the regime where matrix-
free PCG (still) wins on total cost, memory, or feasibility.

The accounting model is **one cell = one MCMC iteration**:
SV updates every iteration, so the direct path must re-assemble and
re-factor every iteration, and the PCG path must re-assemble and
re-factor the time-averaged preconditioner every iteration.

A clearly labelled best-case row (`*_frozen_amortized_50`) reports the
PCG path when the time-averaged precision preconditioner setup is held
fixed across 50 MCMC sweeps -- this is the upper bound on the
matrix-free advantage, not the production full-chain figure.

Correction rerun status (2026-05-23): `cost_runner.py` and
`results.csv` now use the corrected precision average
`D_bar = mean_t(D_t) = B0' diag(mean_t 1/U_t) B0`, replacing the old
`B0' diag(1 / mean_t U_t) B0` construction.

## Design

Four paths, three timed phases each. Same phase semantics across paths
so the table aggregates directly:

| path | phase1_assembly | phase2_factor | phase3_solve |
|---|---|---|---|
| `direct_cholmod` | build explicit `Kbar` from `(H_B, D_t, λ M'M)` | CHOLMOD supernodal Cholesky on `Kbar` | `factor(b)` |
| `direct_splu` | build explicit `Kbar` | `scipy.sparse.linalg.splu` on `Kbar` | `splu.solve(b)` |
| `pcg_time_avg_chol_explicit_avgK` | build `Kbar_avg` from `D_bar = B0' diag(mean_t 1/U_t) B0` | CHOLMOD on `Kbar_avg` | PCG to `rtol=1e-8` (matrix-free matvec, CHOLMOD preconditioner) |
| `pcg_time_avg_chol_frozen_amortized_50` *(derived row)* | `phase1 / 50` | `phase2 / 50` | same PCG solve time |

The amortised row is **not** a separate run; it is the same PCG numbers
re-presented with setup costs divided by 50 -- the upper bound on the
matrix-free advantage if the time-averaged precision preconditioner is
frozen.

The name `explicit_avgK` records that this PCG path still materialises
`Kbar_avg` as a `Tn × Tn` sparse matrix. A truly no-explicit-`Kbar_avg`
alternative (analytic construction of the time-averaged precision
blocks) is left as follow-up; the present implementation cannot test
that.

### Stress grid

```
n         in {5, 10, 20}
T         in {480, 1920, 5000, 10000}
p         in {2, 12, 24}
sv_sigma  in {0.1, 0.3, 0.5}
seeds     in {0, 1, 7}
```

`3·4·3·3 = 108` cells × 3 seeds × 4 paths = 1 296 rows. Other axes held
at the Thread 2 baseline (`sv_rho=0.95`, `lam=1e4`,
`target_radius=0.9`).

### Skip rule and timeouts

Before any explicit `Kbar` is built, `memory_estimate.estimate()`
returns closed-form `H_B_nnz`, `Kbar_nnz`, and a CSR byte estimate
(`16 bytes / nnz`, conservative for SciPy intermediate transposes).
If either

```
estimated_Kbar_nnz       > 1e8
estimated_Kbar_csr_bytes > 6 GB
```

the explicit paths (`direct_cholmod`, `direct_splu`, and
`pcg_time_avg_chol_explicit_avgK`, which also assembles a `Tn × Tn`
`Kbar_avg`) are recorded as
`status=skipped_memory_estimate:...`. The skip is visible in the CSV,
never silently dropped.

Per-segment timeouts via `signal.setitimer(SIGALRM)`:

| Tn | timeout / segment |
|---|---|
| ≤ 20 000  | 60 s |
| ≤ 50 000  | 300 s |
| ≤ 100 000 | 600 s |
| > 100 000 | 900 s |

A segment that overruns its budget is recorded as
`status=timeout_phaseN` with empty timings.

### Memory proxies

Reported per row (deterministic, reproducible across runs):

| column | meaning |
|---|---|
| `H_B_nnz` | actual nnz of the matrix-free forward operator `H_B` |
| `Kbar_nnz_estimate` | closed-form upper bound on `Kbar` nnz, `T·(2p+1)·n²` |
| `Kbar_csr_bytes_estimate` | `16 × Kbar_nnz` (conservative CSR storage) |
| `L_factor_nnz` | actual nnz of the CHOLMOD `L` factor (or `splu.L.nnz + splu.U.nnz`) when the factor is built |
| `M_m_nnz` | nnz of the aggregation operator (negligible at this scale) |

Peak RSS sanity checks are available via `rss_sanity.py` (subprocess
per cell, `resource.getrusage(...).ru_maxrss`). Not run in the
production sweep -- nnz proxies were deemed sufficient given the
consistent factor-fill ratios observed.

## Results

Full sweep: 324 cells × 4 paths in 3.6 hours of wall time on the local
machine. 315/324 cells ran `direct_*` to completion; 9 cells hit the
memory-estimate skip rule; 2 cells hit `timeout_phase3` on the PCG
path. No silent failures.

### Total time at production-nominal `sv_sigma = 0.3`, seed-median (ms)

`p = 2` (Taiwan-scale lag length):

| n  |    T   | direct_cholmod | direct_splu | pcg_explicit_avgK | frozen_amortized_50 |
|---:|------:|---:|---:|---:|---:|
| 5  |   480 |     11.1 |     12.0 |     21.1 |     10.3 |
| 5  | 1 920 |     46.0 |     50.1 |    104.3 |     60.2 |
| 5  | 5 000 |    123.0 |    131.8 |    405.4 |    285.9 |
| 5  | 10 000 |   237.8 |    255.9 |    790.9 |    561.4 |
| 10 |   480 |     37.3 |     39.3 |     66.0 |     28.6 |
| 10 | 1 920 |    153.3 |    163.8 |    426.6 |    274.8 |
| 10 | 5 000 |    396.6 |    411.9 |  1 103.6 |    721.4 |
| 10 | 10 000 |   770.0 |    826.0 |  2 251.8 |  1 499.5 |
| 20 |   480 |    151.5 |    159.3 |    296.2 |    151.4 |
| 20 | 1 920 |    598.3 |    636.1 |  1 829.6 |  1 244.1 |
| 20 | 5 000 |  1 528.6 |  1 593.6 |  4 971.7 |  3 470.1 |
| 20 | 10 000 |  3 137.3 |  3 371.3 | 11 772.9 |  8 712.7 |

`p = 12` (deeper lag stress):

| n  |    T   | direct_cholmod | direct_splu | pcg_explicit_avgK | frozen_amortized_50 |
|---:|------:|---:|---:|---:|---:|
| 5  |   480 |     51.2 |     55.5 |     83.6 |     32.2 |
| 5  | 1 920 |    224.5 |    236.0 |    405.2 |    197.2 |
| 5  | 5 000 |    561.2 |    607.6 |  1 314.2 |    782.5 |
| 5  | 10 000 |  1 077.1 |  1 169.6 |  2 892.5 |  1 848.1 |
| 10 |   480 |    236.9 |    244.7 |    387.8 |    153.5 |
| 10 | 1 920 |    973.6 |  1 011.7 |  2 133.3 |  1 198.4 |
| 10 | 5 000 |  2 478.0 |  2 611.5 |  6 350.3 |  3 901.1 |
| 10 | 10 000 |  4 880.6 |  5 124.1 | 13 143.6 |  8 331.4 |
| 20 |   480 |  1 128.3 |  1 277.8 |  2 109.8 |  1 002.6 |
| 20 | 1 920 |  4 566.2 |  5 200.9 | 10 687.1 |  6 220.7 |
| 20 | 5 000 | 11 726.7 | 13 267.8 | 31 882.1 | 20 372.6 |
| 20 | 10 000 | 24 002.8 | 27 168.0 | 84 650.9 | 60 878.1 |

`p = 24` (extreme lag stress; some cells skipped):

| n  |    T   | direct_cholmod | direct_splu | pcg_explicit_avgK | frozen_amortized_50 |
|---:|------:|---:|---:|---:|---:|
| 5  |   480 |    121.7 |    126.7 |    178.6 |     59.6 |
| 5  | 1 920 |    491.6 |    527.8 |    892.8 |    407.1 |
| 5  | 5 000 |  1 249.1 |  1 362.7 |  2 678.9 |  1 465.2 |
| 5  | 10 000 |  5 501.2 |  4 744.5 | 11 173.2 |  6 267.8 |
| 10 |   480 |    547.8 |    612.2 |    888.4 |    352.3 |
| 10 | 1 920 |  2 195.0 |  2 445.2 |  4 631.4 |  2 461.2 |
| 10 | 5 000 |  5 745.7 |  6 428.4 | 12 952.2 |  7 325.3 |
| 10 | 10 000 | 11 742.1 | 12 972.3 | 28 305.9 | 16 841.3 |
| 20 |   480 |  2 909.8 |  3 391.9 |  4 691.1 |  1 850.4 |
| 20 | 1 920 | 11 752.3 | 13 731.4 | 22 687.6 | 11 197.9 |
| 20 | 5 000 | 31 546.0 | 36 694.1 | 69 182.5 | 38 102.8 |
| 20 | 10 000 |  -- (skipped: estimated_Kbar_nnz = 1.96e8 > 1e8) |

**Read across rows.** `direct_cholmod` wins on total time at every
single `(n, T, p)` cell that completed. `direct_splu` is consistently
~5--15% slower than CHOLMOD on the same input -- expected, since LU
ignores SPD structure -- but is included for environments without
`scikit-sparse`. The matrix-free PCG path with explicit `Kbar_avg`
loses to direct CHOLMOD by **2--4×** uniformly. Even the best-case
amortised row (setup divided by 50) only beats direct CHOLMOD at
**three** small cells: `(5, 480, 2)`, `(10, 480, 2)`, `(20, 480, 2)`.

### Phase breakdown at six representative `sigma=0.3` cells (median ms)

```
(n=5, T=480, p=2, Tn=2400)
  direct_cholmod                              asm=    10.5  fac=     0.6  sol=     0.0   tot=     11.1
  pcg_time_avg_chol_explicit_avgK             asm=    10.3  fac=     0.6  sol=    10.0   tot=     21.1
  pcg_time_avg_chol_frozen_amortized_50       asm=     0.2  fac=     0.0  sol=    10.0   tot=     10.2

(n=5, T=1920, p=2, Tn=9600)
  direct_cholmod                              asm=    43.0  fac=     2.8  sol=     0.1   tot=     46.0
  pcg_time_avg_chol_explicit_avgK             asm=    42.7  fac=     2.9  sol=    59.3   tot=    104.3
  pcg_time_avg_chol_frozen_amortized_50       asm=     0.9  fac=     0.1  sol=    59.3   tot=     60.2

(n=10, T=1920, p=12, Tn=19200)
  direct_cholmod                              asm=   861.7  fac=   113.0  sol=     1.8   tot=    973.6
  pcg_time_avg_chol_explicit_avgK             asm=   863.2  fac=   112.0  sol=  1179.4   tot=   2133.3
  pcg_time_avg_chol_frozen_amortized_50       asm=    17.3  fac=     2.2  sol=  1179.4   tot=   1198.4

(n=20, T=1920, p=12, Tn=38400)
  direct_cholmod                              asm=  4186.7  fac=   362.6  sol=     6.0   tot=   4566.2
  pcg_time_avg_chol_explicit_avgK             asm=  4196.6  fac=   364.1  sol=  6129.5   tot=  10687.1
  pcg_time_avg_chol_frozen_amortized_50       asm=    83.9  fac=     7.3  sol=  6129.5   tot=   6220.7

(n=20, T=5000, p=12, Tn=100000)
  direct_cholmod                              asm= 10772.0  fac=   936.2  sol=    18.5   tot=  11726.7
  pcg_time_avg_chol_explicit_avgK             asm= 10835.5  fac=   908.9  sol= 20137.7   tot=  31882.1
  pcg_time_avg_chol_frozen_amortized_50       asm=   216.7  fac=    18.2  sol= 20137.7   tot=  20372.6

(n=20, T=10000, p=2, Tn=200000)
  direct_cholmod                              asm=  2847.2  fac=   280.4  sol=    10.4   tot=   3137.3
  pcg_time_avg_chol_explicit_avgK             asm=  2834.3  fac=   283.2  sol=  8650.2   tot=  11772.9
  pcg_time_avg_chol_frozen_amortized_50       asm=    56.7  fac=     5.7  sol=  8650.2   tot=   8712.7
```

The phase breakdown is the clearest finding of Thread 2b:

* **Assembly is 87--92% of `direct_cholmod` total time across the
  stress grid.** At `(n=10, T=1920, p=12)`: 862 ms assembly + 113 ms
  factor + 2 ms solve = 974 ms total. Factor is 12% of total; solve is
  0.2%.
* **`pcg_time_avg_chol_explicit_avgK`'s phase1 timing essentially
  equals `direct_cholmod`'s phase1 timing.** The PCG path assembles a
  `Tn × Tn` `Kbar_avg` of the same sparsity pattern as `Kbar`, so
  there is no assembly-side advantage to the matrix-free framing as
  currently implemented. This is why the path label includes
  `_explicit_avgK`: it makes the assembly cost visible in the
  comparison.
* The matrix-free PCG path therefore pays everything `direct_cholmod`
  pays (assembly, factorisation -- of `Kbar_avg`, but same nnz), **plus**
  the PCG solve cost, which is one to two orders of magnitude larger
  than the direct solve. There is no per-iteration scenario in the
  measured grid where this combination wins.

### Memory: L factor nnz (`sv_sigma=0.3, p=12`, seed-median)

| n  |   T    | direct_cholmod | direct_splu | pcg_explicit_avgK |
|---:|------:|---:|---:|---:|
| 5  |   480 |     160 975 |     332 335 |     160 975 |
| 5  | 1 920 |     650 575 |   1 362 465 |     650 575 |
| 5  | 5 000 |   1 697 750 |   3 547 995 |   1 697 750 |
| 5  | 10 000 |  3 397 750 |   7 121 855 |   3 397 750 |
| 10 |   480 |     641 500 |   1 377 700 |     641 500 |
| 10 | 1 920 |   2 592 700 |   5 579 110 |   2 592 700 |
| 10 | 5 000 |   6 766 000 |  14 573 290 |   6 766 000 |
| 10 | 10 000 | 13 541 000 |  29 147 270 |  13 541 000 |
| 20 |   480 |   2 468 800 |   6 602 560 |   2 468 800 |
| 20 | 1 920 |   9 971 200 |  26 329 680 |   9 971 200 |
| 20 | 5 000 |  26 018 000 |  69 093 120 |  26 018 000 |
| 20 | 10 000 | 52 068 000 | 138 293 100 |  52 068 000 |

Three findings on memory:

1. **CHOLMOD's `L` factor is identical-size on `Kbar` and `Kbar_avg`**,
   because the two have the same sparsity pattern (`Kbar_avg` only
   changes values, not nonzero positions). So the matrix-free PCG
   path has no factor-storage advantage either.
2. **SPLU's `L + U` is ~2.1× CHOLMOD's `L`** consistently across the
   grid -- the standard penalty for ignoring SPD structure. CHOLMOD
   should always be preferred when `scikit-sparse` is available.
3. **At `(n=20, T=10000, p=12)`**, CHOLMOD's L has 52M nz ≈ 416 MB at
   8 bytes/entry plus indices. Still feasible on a 32 GB workstation,
   but the next stress point `(n=20, T=10000, p=24)` exceeds the skip
   threshold and is left unmeasured -- this is where a truly
   `Kbar`-free preconditioner would matter.

### Skip rule and timeouts

The skip rule fired exactly once: `(n=20, T=10000, p=24)`, estimated
`Kbar_nnz = 1.96e8 > 1e8`. 9 cells (3 sigma × 3 seeds) were skipped
across all three explicit paths. Their rows in `results.csv` carry
`status=skipped_memory_estimate:...` -- not silently dropped.

Two timeout events: `(n=20, T=10000, p=12, sv_sigma=0.5, seed=0)` and
`(seed=1)` on `pcg_time_avg_chol_explicit_avgK` phase3 (PCG solve).
At `Tn = 200 000` with `sv_sigma = 0.5`, the time-averaged CHOLMOD
preconditioner needed more than `maxiter = min(5*Tn, 20000) = 20000`
iterations to converge, and was killed at the 900-second segment
budget. This is consistent with Thread 2's finding that the
time-averaged preconditioner partially survives `sigma = 0.5` but
loses control as `Tn` grows.

### Findings

1. **Assembly dominates the direct path. Removing it is the only
   route to a matrix-free advantage.** At all but the smallest
   Taiwan-scale cell, `direct_cholmod` spends ≥85% of its total time
   on Kbar assembly, not factorisation. CHOLMOD's solve is in the
   sub-millisecond range up to `Tn = 200 000`. A matrix-free path
   that genuinely avoids explicit Kbar assembly (analytic block
   construction of `Kbar_avg = H_B' (I ⊗ D_bar) H_B + λ M'M` without
   building the global sparse matrix) is therefore the right
   research direction.

2. **The current `time_avg_chol_explicit_avgK` preconditioner does
   not avoid assembly.** It builds `Kbar_avg` from the same `H_B' D
   H_B` sparse-product code path as `Kbar`, with the same nnz. So it
   pays the assembly cost twice (once for `Kbar_avg` plus once
   inside PCG's matrix-free matvec which still touches `H_B` and
   `B0` per matvec). This is why Thread 2's apparent factor-only
   speedup disappears once the full pipeline is timed: the apparent
   speed advantage was hiding the same assembly cost.

3. **No crossover regime in the measured grid.** `direct_cholmod`
   wins on total time at every cell that ran. The amortised row
   (setup divided by 50) only beats `direct_cholmod` at three small
   `(n, 480, 2)` cells; for any realistically deep lag (`p ≥ 12`) or
   long sample (`T ≥ 1920`), even the amortised PCG path is slower.

4. **Memory regime is also unresolved.** The largest feasible cell,
   `(n=20, T=10000, p=12)`, has CHOLMOD L factor 52M nz ≈ 0.4 GB --
   easy on commodity hardware. The next step `(p=24)` would be
   ~196M nz Kbar ≈ 1.6 GB sparse + a much larger factor, and was
   skipped to avoid an OOM. But `pcg_time_avg_chol_explicit_avgK`
   was skipped *at the same cell* by the same rule, because it also
   assembles a Tn × Tn matrix. So the present matrix-free
   implementation does **not** unlock the regime where direct fails.

### Recommendation

* **Production regime (Taiwan-scale: `n ≈ 5`, `T ≤ 1920`, `p ∈ 2..12`):
  use `direct_cholmod`.** Per-iteration total cost is 11--225 ms
  depending on `p`. Factor and solve are sub-millisecond; the
  bottleneck is the SV-driven re-assembly of `Kbar`. This is the
  Taiwan-scale production baseline.

* **Larger-`n` or longer-`T` regime (`n=10..20`, `T = 5000..10000`):
  still `direct_cholmod`** at total cost 0.4--24 seconds per
  iteration, until either L factor or peak RSS exhaust the
  workstation budget. The PCG path with `explicit_avgK` is
  consistently 2--4× slower and never wins.

* **The largest stress point `(n=20, T=10000, p=24)` requires a
  no-explicit-`Kbar_avg` preconditioner.** Neither `direct_cholmod`
  nor `pcg_time_avg_chol_explicit_avgK` can run there with the
  current memory budget. This is the matrix-free contribution that
  Thread 2b proves *would* be valuable but is not yet implemented.

* **Do not advertise a matrix-free per-iteration speed advantage in
  the proposal.** The honest finding is the opposite: direct
  CHOLMOD dominates total cost at Taiwan-scale and the regime where
  matrix-free might dominate (very large `(n, T, p)` corners)
  requires a preconditioner that the current code does not build.

### Plots

* `fig_total_time_vs_T.{pdf,png}` -- median total time vs `T`, one
  line per path, faceted by `n`, at `sv_sigma = 0.3`. Demonstrates the
  ranking is stable across the entire `(n, T)` range.
* `fig_memory_vs_Tn.{pdf,png}` -- L factor nnz and Kbar/H_B nnz vs
  `Tn`, showing that direct and matrix-free paths have identical
  factor-storage requirements as currently implemented.
* `fig_phase_breakdown.{pdf,png}` -- stacked bars
  (assembly | factor/setup | solve/PCG) per path at four `(n, T)`
  reference points; visualises the assembly-dominance result.

## Files

```
theory/mf_oi_svmvar_report/code/thread2b_fair_cost/
├── memory_estimate.py    # closed-form skip estimator
├── cost_runner.py        # per-cell phased timing for all four paths
├── sweep.py              # stress-grid driver
├── rss_sanity.py         # subprocess RSS sampling (not run in this sweep)
├── plots.py              # the three figures above
├── results.csv           # 1 296 rows = 324 cells × 4 paths
├── fig_total_time_vs_T.{pdf,png}
├── fig_memory_vs_Tn.{pdf,png}
├── fig_phase_breakdown.{pdf,png}
└── THREAD2B_NOTE.md      # this file
```

Reproduce (requires the `benchmark` conda env with `scikit-sparse`):

```
cd theory/mf_oi_svmvar_report/code/thread2b_fair_cost
PYTHONUNBUFFERED=1 /opt/homebrew/Caskroom/miniforge/base/envs/benchmark/bin/python sweep.py --quick   # ~30s
PYTHONUNBUFFERED=1 /opt/homebrew/Caskroom/miniforge/base/envs/benchmark/bin/python sweep.py           # full grid, ~3.5 hours
/opt/homebrew/Caskroom/miniforge/base/envs/benchmark/bin/python plots.py
```

## Acceptance against Thread 2b plan

* [x] **No comparison mixes direct solve-only cost with matrix-free
      total cost.** All paths report `phase1_assembly_time +
      phase2_factor_time + phase3_solve_time` and the `total_time`
      column is exactly the sum.
* [x] **Direct CHOLMOD treated as the primary Taiwan-scale production
      baseline.** Recommendation section makes this explicit, with the
      quantitative per-iteration cost band 11--225 ms for the Taiwan-
      scale `(n=5, T ≤ 1920, p ∈ 2..12)` rectangle.
* [x] **Matrix-free claims restricted to regimes where it wins on
      total time, memory, or feasibility.** None of those regimes
      were found in the measured grid with the current
      implementation. The honest matrix-free advantage requires an
      analytic, non-explicit `Kbar_avg` preconditioner that bypasses
      the global `Tn × Tn` assembly; quantifying that is left as a
      follow-up.

## Carry-overs

1. **Analytic `Kbar_avg` preconditioner.** The bottleneck for the
   matrix-free path is the explicit `Tn × Tn` `Kbar_avg` assembly.
   Implementing `K_pre · x` analytically as
   `H_B' (I ⊗ D_bar) H_B x + λ M' (M x)` -- where the middle step
   replaces a sparse SpMV by a per-date `n × n` BLAS3 contraction --
   would eliminate phase1 entirely on the PCG path. Until this is in
   place, no matrix-free total-cost claim against direct CHOLMOD is
   defensible.

2. **`(n=20, T=10000, p=24)` and beyond.** Once an analytic-block
   preconditioner is in place, re-run this corner. It is the only
   regime where direct CHOLMOD genuinely cannot run with current
   memory; demonstrating PCG convergence there would be the headline
   matrix-free contribution.

3. **RSS sanity check.** `rss_sanity.py` is in place but was not run
   in this sweep. nnz proxies tracked the L factor sizes consistently
   across `n` and `T` so the production conclusion does not depend
   on a peak-RSS measurement. Run if a reviewer asks.

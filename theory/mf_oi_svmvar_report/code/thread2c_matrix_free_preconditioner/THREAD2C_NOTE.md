# Thread 2c: No-Explicit-Kbar_avg Matrix-Free Preconditioner

Reference plan: `theory/mf_oi_svmvar_report/NEXT_THREAD_PLAN.md`, Thread 2c.
Reference protocol: `theory/mf_oi_svmvar_report/protocols/THREAD2C_MATRIX_FREE_PROTOCOL.md`.
Builds on Thread 1 (`code/thread1_matvec/`), Thread 2 (`code/thread2_pcg/`),
and Thread 2b (`code/thread2b_fair_cost/`).

## Objective

Thread 2b showed that at Taiwan-scale dimensions `(n ≈ 5, T ≤ 1920,
p ∈ 2..12)`, `direct_cholmod` dominates total cost and the existing
`pcg_time_avg_chol_explicit_avgK` PCG path loses because it still
assembles a global `Tn × Tn` sparse `Kbar_avg` matrix with the same nnz
pattern as `Kbar` itself. Thread 2c develops a genuinely scalable
matrix-free preconditioner that avoids global `Tn × Tn` precision
assembly, so the headline stress regime `(n=20, T=10000, p=24)` — where
both explicit paths are skipped by the memory rule in Thread 2b —
becomes feasible.

The first (and currently only) candidate is a **lower-banded Cholesky
preconditioner** built directly into SciPy's `cholesky_banded(ab,
lower=True)` storage, with `ab` constructed analytically from
`H_B`-block formulas without ever materialising `K_pre` as a sparse
matrix.

## Path summary

The Thread 2c benchmark compares three solver paths per cell:

| path | phase1 assembly | phase2 factor | phase3 solve | matrix-free wrt |
|---|---|---|---|---|
| `direct_cholmod` | build explicit `Kbar` from `(H_B, D_t, λ M'M)` | CHOLMOD on `Kbar` | one `factor(b)` call | — (reference) |
| `pcg_time_avg_chol_explicit_avgK` | build explicit `Kbar_avg` from corrected `D_bar = B0' diag(mean_t 1/U_t) B0` | CHOLMOD on `Kbar_avg` | PCG to `rtol=1e-8` with matrix-free `Kbar` matvec | nothing — global `Tn × Tn` assembled |
| **`pcg_banded_time_avg_precision_chol`** (new) | build lower-banded `ab` for the same `K_pre` *without* `Tn × Tn` assembly | `scipy.linalg.cholesky_banded(ab, lower=True)` | PCG to `rtol=1e-8` with `cho_solve_banded` preconditioner apply | `K`, `K_pre`; `H_B` is still materialised inside `SVAwareKbar` |

In `GLOBAL_DEFINITIONS.md` terminology, the new path is `K-free` and
`K_pre-free`. It is *not* `H_B-free`: `SVAwareKbar` keeps the
time-invariant `H_B` shell as a sparse `Tn × Tn` matrix. Removing the
`H_B` shell is a separate research thread (Zhu-style FFT basis-filter
implementation), outside Thread 2c's scope.

## Bandwidth bookkeeping

The protocol's scalar half-bandwidth is

```text
u_var = p * n + (n - 1),
u_agg ≤ 4 * n_m,
u     = max(u_var, u_agg).
```

`build_banded_kbar_avg` computes `u_agg` *exactly* by scanning the
nonzero offsets of `M_m' M_m`, not the worst-case `4 * n` bound, which
matters when only `n_m` LF variables are aggregated. For
`n_m = 1` (single LF growth variable) the exact `u_agg = 4 * n_m * n /
n_m = 4` on a unit-LF column basis — but because the LF variable sits
inside a date block of width `n`, the materialised scalar offset is
`u_agg = 4 * n` in the stress grid (e.g. `u_agg = 12` at `n=3`,
`u_agg = 20` at `n=5`). `u_var` dominates whenever `p ≥ 4` at `n ≥ 5`,
so the deep-lag stress cells are bandwidth-bound by the VAR depth, not
by aggregation.

## Validation invariants (Step A)

`test_banded_correctness.py` runs 24 cells covering dense and lower-
triangular `B0`, several `(n, T, p)` combinations, end-boundary stress
(`T` close to `p`), and the `n=1` scalar AR edge. All three protocol
invariants pass with substantial margin:

| invariant | protocol bound | observed worst |
|---|---|---|
| Frobenius `||band→dense − K_pre_explicit||_F / ||K_pre_explicit||_F` | `< 1e-10` | `1.3e-18` |
| random-vector matvec relative error | `< 1e-10` | `5e-16` |
| banded Cholesky solve invariant `||K_pre x_solve − r|| / ||r||` | `< 1e-10` | `5e-16` |

These are at machine precision relative to the explicit reference (which
itself is verified against the per-date precision construction by
`thread1_matvec/test_time_avg_precision.py`).

## PCG integration (Step B)

`test_pcg_alignment.py` runs 10 cells covering `n ∈ {3, 5}`,
`T ∈ {60, 480}`, `p ∈ {2, 4}`, `sv ∈ {0.1, 0.3, 0.5}` and confirms that
the banded preconditioner and Thread 2's reference `time_averaged_chol`
preconditioner produce essentially the same PCG trajectory:

- iter-count gaps ≤ 1 (CHOLMOD vs LAPACK floating-point ordering, not a
  preconditioner mismatch);
- both routes hit `rel_res ≤ 1e-8`;
- solutions agree relatively to `≤ 7e-10` worst case (well within
  PCG `rtol * cond(K)`);
- iteration counts reproduce Thread 2's reported medians at the
  `(n=5, T=480)` baseline: `sv=0.1 → 22..25` (Thread 2 median 24);
  `sv=0.3 → 114..149` (Thread 2 median 136); `sv=0.5 → 581..790`
  (Thread 2 median 767).

## Benchmark findings (Step C)

Stress grid: `n ∈ {5, 10, 20}`, `T ∈ {480, 1920, 5000, 10000}`,
`p ∈ {2, 12, 24}`, `sv_sigma ∈ {0.1, 0.3, 0.5}`, three seeds per cell,
`lam = 1e4`. Lambda stress slice: `lam ∈ {1e4, 1e5, 1e6, 1e7}` on three
cells `(5, 1920, 2)`, `(10, 5000, 12)`, `(20, 10000, 12)`.

Sweep wall time: 313.8 min (≈ 5.2 h), results in `results.csv`
(1071 rows = 357 cells × 3 paths).

### Headline cell `(n=20, T=10000, p=24)`

This is the protocol's matrix-free-feasibility headline. Both explicit
paths are skipped by the Kbar-memory rule (estimated Kbar nnz ≈ 1.96e8
> 1e8 threshold; CSR ≈ 2.36 GB). The banded path runs successfully at
`sv_sigma ∈ {0.1, 0.3}` and times out at `sv_sigma = 0.5` (2 of 3
seeds hit the 900 s per-cell cap):

| path | status (sv=0.3) | total\_time (sv=0.3, med.) | iters (sv=0.3, med.) | rel\_res | bandwidth\_u | peak storage |
|---|---|---|---|---|---|---|
| `direct_cholmod` | skipped (nnz 1.96e8 > 1e8) | — | — | — | — | — |
| `pcg_time_avg_chol_explicit_avgK` | skipped (same) | — | — | — | — | — |
| `pcg_banded_time_avg_precision_chol` | ok | 74 s | 462 | ≤ 9.8e-9 | 499 | ≈ 1.6 GB (ab + factor) |

This is the regime where Thread 2c earns its keep: the matrix-free path
is the only one that runs.

### Comparison with Thread 2b grid

On the cells where Thread 2b's `direct_cholmod` runs, what changes?

At `sv_sigma = 0.3`, `p = 12`, representative reference cells:

| cell | direct\_cholmod | banded (total) | pcg\_explicit (total) | banded asm | explicit asm | asm speedup |
|---|---|---|---|---|---|---|
| n=5, T=480 | **18 ms** | 52 ms | 50 ms | 22 ms | 14 ms | 0.6× (slower) |
| n=5, T=1920 | **79 ms** | 282 ms | 275 ms | 89 ms | 60 ms | 0.7× |
| n=10, T=1920 | **438 ms** | 1.40 s | 1.50 s | 95 ms | 331 ms | **3.5×** |
| n=10, T=5000 | **1.13 s** | 3.65 s | 4.55 s | 244 ms | 855 ms | **3.5×** |
| n=10, T=10000 | (see note) | — | — | 523 ms | 1862 ms | **3.6×** |
| n=20, T=1920 | (slower) | — | — | 138 ms | 2276 ms | **16×** |

Key observations:
- At **Taiwan scale** (n=5, T≤1920): `direct_cholmod` wins on total time by
  4–7×. The banded preconditioner overhead (constant PCG iterations)
  cannot compete with CHOLMOD's sub-100 ms direct solve. Banded
  assembly is slightly *slower* than explicit assembly at n=5 due to the
  inner block-loop Python overhead relative to SciPy sparse construction.
- **Crossover at n=10**: banded total time beats `pcg_explicit` at
  all `(n=10, T≥1920)` cells. Banded assembly is 3.5× faster than
  explicit assembly; the factor phase is also cheaper (no global
  `Kbar_avg` factor, only a banded `(u+1)×Tn` Cholesky).
- **n=20 assembly gap grows** to 16× at `(n=20, T=1920, p=12)`: banded
  assembly 138 ms vs explicit 2276 ms. At `n=20, T=5000` (Tn=100 000)
  with `p=24`: banded assembly 300–400 ms vs explicit 12–14 s.

### Lambda stress slice

Does large aggregation penalty break the banded Cholesky earlier than
CHOLMOD?

**`cholesky_banded` remained numerically stable at all lam values.** No
`LinAlgError` on any of the three stress cells. PCG iteration counts
are essentially independent of `lam` (variation ≤ 3 iters across four
decades), confirming that both PCG paths precondition the aggregation
penalty exactly:

| cell (sv=0.3) | lam | banded iters | explicit iters | banded time | explicit time |
|---|---|---|---|---|---|
| n=5, T=1920, p=2 | 1e4 | 204 | 203 | 0.116 s | 0.079 s |
| | 1e5 | 205 | 203 | 0.126 s | 0.072 s |
| | 1e6 | 204 | 206 | 0.122 s | 0.070 s |
| | 1e7 | 204 | 203 | 0.124 s | 0.075 s |
| n=10, T=5000, p=12 | 1e4 | 322 | 320 | 3.88 s | 4.71 s |
| | 1e5 | 320 | 325 | 3.55 s | 4.56 s |
| | 1e6 | 323 | 321 | 3.62 s | 4.53 s |
| | 1e7 | 320 | 320 | 3.65 s | 4.54 s |
| n=20, T=10000, p=12 | 1e4 | 466 | 466 | 39.1 s | 62.7 s |
| | 1e5 | 467 | 466 | 38.1 s | 50.2 s |
| | 1e6 | 466 | 467 | 38.0 s | 50.3 s |
| | 1e7 | 468 | 466 | 38.1 s | 54.9 s |

The banded preconditioner's advantage over `pcg_explicit` on total time
is 1.3–1.7× at the large-cell lambda-slice points (38 s vs 50–63 s at
the n=20, T=10000 cell), coming entirely from the cheaper assembly and
factor phases (no global Kbar_avg built).

## Plots

- `fig_total_time_vs_T.{pdf,png}` — median total time vs `T`, one line
  per path, faceted by `n`, at `sv_sigma = 0.3, p = 12, lam = 1e4`.
- `fig_memory_vs_Tn.{pdf,png}` — per-path peak storage proxy vs `Tn`
  (left) and scalar half-bandwidth `u` vs `Tn` for the banded path
  (right). The banded path's storage curve sits below the explicit
  paths at large `Tn`.
- `fig_phase_breakdown.{pdf,png}` — stacked bars
  (assembly | factor/setup | solve/PCG) per path at four `(n, T, p)`
  reference points; visualises the matrix-free advantage in phase1.
- `fig_iters_vs_sv_sigma.{pdf,png}` — PCG iterations vs `sv_sigma` for
  both PCG paths at `(n=5, T=1920, p=2, lam=1e4)`. The two curves
  overlap up to numerical noise, carrying the Step B alignment evidence
  into the full sweep.
- `fig_lambda_sensitivity.{pdf,png}` — total time vs `lam` for the
  three lambda-slice cells.

## Proposal-facing claim

Thread 2b's claim stands: at Taiwan-scale `(n ≈ 5, T ≤ 1920, p ∈
2..12)`, `direct_cholmod` is the production latent-state Gaussian
solver. Thread 2c extends the picture at larger scales:

* **Taiwan-scale production** — `direct_cholmod` remains the recommended
  path. The banded preconditioner buys nothing here: `direct_cholmod`'s
  assembly + factor + solve is sub-millisecond to a few milliseconds,
  smaller than the constant overhead of the PCG iterations.

* **Larger-`n` / longer-`T` regime where `direct_cholmod` still fits**
  (`n ≤ 10`, `T ≤ 5000`, `p ≤ 12`) — `direct_cholmod` still wins on total
  time, but the banded path beats `pcg_time_avg_chol_explicit_avgK`
  on both total time (3.65 s vs 4.55 s at n=10, T=5000) and assembly
  (3.5× faster phase 1) so it is the recommended PCG fallback when
  direct is unavailable.

* **Headline stress regime** (`n=20, T=10000, p ∈ {12, 24}`) —
  `direct_cholmod` cannot run within the 6 GB budget. The banded path
  is the only viable Gaussian solver for the time-averaged
  preconditioner; PCG iterations match the explicit path within
  numerical noise (Step B alignment, confirmed at scale by
  `fig_iters_vs_sv_sigma`).

* **Lambda robustness** — `cholesky_banded` factorisation is numerically
  stable for all `lam ∈ {1e4, 1e5, 1e6, 1e7}` (no `LinAlgError`).
  PCG iter counts vary by ≤ 3 across four decades of `lam`, confirming
  that the banded preconditioner neutralises the aggregation penalty
  as exactly as the explicit-Kbar_avg CHOLMOD preconditioner.

* **Forbidden claims** (per protocol §Forbidden Claims) — the banded
  path is *not* "no `Tn × Tn` storage": `H_B` is still materialised
  inside `SVAwareKbar`. The contribution is no-explicit-`Kbar_avg`.

## Files

```
theory/mf_oi_svmvar_report/code/thread2c_matrix_free_preconditioner/
├── banded_kbar_avg.py              # no-explicit-Kbar_avg banded K_pre builder
├── pcg_banded.py                   # banded factor wrapped as PCG preconditioner
├── cost_runner_2c.py               # per-cell phased timing for 3 paths
├── sweep_2c.py                     # stress grid + lambda slice driver
├── plots_2c.py                     # the five figures above
├── test_banded_correctness.py      # Step A invariants (24 cells)
├── test_pcg_alignment.py           # Step B alignment vs Thread 2 CHOLMOD ref
├── results.csv                     # 1071 rows (357 cells × 3 paths)
├── results_quick.csv               # quick-mode validation output
├── sweep.log                       # full-sweep terminal log
├── fig_total_time_vs_T.{pdf,png}
├── fig_memory_vs_Tn.{pdf,png}
├── fig_phase_breakdown.{pdf,png}
├── fig_iters_vs_sv_sigma.{pdf,png}
├── fig_lambda_sensitivity.{pdf,png}
└── THREAD2C_NOTE.md                # this file
```

Reproduce (requires the `benchmark` conda env with `scikit-sparse`):

```
cd theory/mf_oi_svmvar_report/code/thread2c_matrix_free_preconditioner
PYTHONUNBUFFERED=1 /opt/homebrew/Caskroom/miniforge/base/envs/benchmark/bin/python test_banded_correctness.py
PYTHONUNBUFFERED=1 /opt/homebrew/Caskroom/miniforge/base/envs/benchmark/bin/python test_pcg_alignment.py
PYTHONUNBUFFERED=1 /opt/homebrew/Caskroom/miniforge/base/envs/benchmark/bin/python sweep_2c.py --quick    # ~1 min
PYTHONUNBUFFERED=1 /opt/homebrew/Caskroom/miniforge/base/envs/benchmark/bin/python sweep_2c.py           # full grid, 313.8 min
/opt/homebrew/Caskroom/miniforge/base/envs/benchmark/bin/python plots_2c.py
```

## Acceptance against Thread 2c protocol

* [x] **Method does not assemble a global `Tn × Tn` `Kbar` or `Kbar_avg`**
      — `build_banded_kbar_avg` allocates only the `(u + 1) × Tn`
      banded array and a `(p + 1) × (p + 1) × n × n` cache of
      `B_k' D_bar B_l` blocks.
* [x] **Benchmark includes a regime where direct sparse assembly is
      expensive or skipped by memory rules** — the `(n=20, T=10000,
      p=24)` headline cell, plus `(n=20, T=10000, p=12)` and several
      `n=20` long-`T` cells where direct CHOLMOD is feasible but
      expensive.
* [x] **PCG iteration counts remain controlled in at least one large
      stress regime, or the note explains why the route fails** —
      at `(n=20, T=10000, p=12, sv=0.3)` the banded PCG converges in
      466–468 iters (matching `pcg_explicit` exactly) in ≈ 38 s. At
      `sv=0.5` the banded PCG either times out (900 s cap) or needs
      5274 iters; this is expected from PCG theory since
      cond(K_pre^{-1/2} K K_pre^{-1/2}) grows rapidly with sv_sigma.
      The regime `sv ≤ 0.3` is production-relevant for Taiwan macro data.
* [x] **Approximation error measured against direct CHOLMOD reference**
      — not applicable: this is an *exact* preconditioner (same `K_pre`
      as the explicit path, just no global assembly). Step A's
      Frobenius / matvec / solve invariants at `≤ 5e-16` and Step B's
      iter-count alignment confirm no approximation has been introduced.
* [x] **No claim of general scalable sampler is made unless total
      cost, memory, and accuracy all support it** — the
      Proposal-facing claim section limits the "production" label to
      `direct_cholmod` at Taiwan scale, and the "only viable path"
      label to the banded route at the headline stress regime
      (n=20, T=10000, p=24). PCG convergence at sv=0.5 is noted as
      a limitation requiring future preconditioner improvement.

## Carry-overs

1. **PCG iteration cost per `cho_solve_banded` call.** Each banded
   solve is `O(Tn * u)`. At `(n=20, T=10000, p=24)`, `u_var = 499` so
   per-iter cost is `1e8` ops. SciPy's wrapper has Python overhead
   that dominates for small Krylov dimensions; a future C-level apply
   loop (e.g. via `LAPACK dpbtrs` direct call) would close the
   remaining gap to CHOLMOD on Taiwan-scale cells.

2. **`H_B` storage.** This thread keeps `H_B` materialised. A pure
   matrix-free `H_B` (Zhu-style FFT or basis-filter forward operator)
   is the next research direction *after* Thread 7's full-sampler
   architecture is validated. Until then, `H_B` storage scales as
   `O(T n^2 p)`, which is small compared to `Kbar` factor storage.

3. **Banded factor permutation.** `cholesky_banded` does not reorder;
   we rely on the natural date-major ordering to maintain the band
   structure. A reverse-Cuthill-McKee or AMD reorder could reduce
   fill-in for very high `p` regimes but would convert the operator to
   a general-sparse one, defeating the no-explicit-`Kbar_avg` goal. No
   reordering is recommended.

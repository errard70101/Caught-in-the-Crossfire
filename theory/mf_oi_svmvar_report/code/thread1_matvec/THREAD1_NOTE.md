# Thread 1: SV-Aware Matrix-Free Matvec — Proof of Concept

Reference plan: `theory/mf_oi_svmvar_report/NEXT_THREAD_PLAN.md`, Thread 1.

## Objective

Implement and validate the SV-aware precision product

```
Kbar x  =  A' D A x  +  lambda M_m' M_m x,
A = H_B S^m,
D = blockdiag(D_1, ..., D_T),  D_t = B0' diag(1/U_t) B0,
```

both as an **explicit** sparse `Kbar @ x` (ground truth) and as a
**matrix-free** product that never assembles the SV-dependent precision
`Kbar` (although the time-invariant VAR shell `H_B` *is* materialised
as a sparse banded Tn × Tn matrix). The matvec is shown to match the
explicit product at machine precision.

## What "matrix-free" means here, precisely

The matrix-free path in `kbar_matfree.py` does **not** form the
`Tn × Tn` precision `Kbar = A'DA + λM'M`. It does, however, build
`H_B` once as a sparse banded `Tn × Tn` CSR. This is the correct
framing of the engineering claim:

- `H_B` depends only on the VAR coefficients. Under a typical Gibbs
  step those change far less often than the SV path; `H_B` is
  amortised across SV updates.
- `D = blockdiag(D_t)` and the product `A'DA` are **never** assembled.
  An SV update only refreshes the local `(T, n)` array `U_inv`. The
  matvec uses two dense `(T, n) @ (n, n)` products to apply the
  per-date `D_t`.
- The aggregation term `λ M_m' M_m` is held only via `M_m` and
  `M_m.T` (small, at most 5 nonzeros per row of `M_m`).

What this does *not* claim:

- It does not claim that no `Tn × Tn` matrix exists in memory; `H_B`
  is `Tn × Tn`.
- It does not claim a uniform per-matvec speedup over explicit `Kbar @ x`
  in isolation -- once `Kbar` exists, SpMV against it is competitive
  with the matrix-free decomposition for small `Tn`.

The downstream PCG / solver story is treated in Thread 2 / 2b / 3.

## Construction

| Object | Construction | Notes |
|---|---|---|
| `H_B`  | Banded `Tn × Tn` sparse (`scipy.sparse.csr_matrix`). Diagonal blocks `I_n`, sub-diagonal blocks `-B_i` for lag `i = 1..p`. Lags that fall before `t=1` are truncated (initial conditions absorbed in `c_B`). | bandwidth `p*n`; nnz `O(T p n^2)` |
| `B_1, ..., B_p` | Independent Gaussian entries, jointly rescaled so the companion matrix spectral radius equals a target (default `0.9`). | guarantees stationarity for the PoC DGP |
| `B0` | Lower triangular, unit diagonal, Gaussian off-diagonals (scale `0.3`). | matches DHK structural normalisation |
| `U_t` | Diagonal of `exp(h_{i,t})`, with each `h_{i,t}` an independent AR(1): `h_{i,t} = mu + rho (h_{i,t-1} - mu) + sigma * eta`. | The per-variable `h_{i,t}` here is a PoC log-variance path, distinct from the common volatility factor `h_t` in main.tex eq (1). `sv_sigma` is tunable for Thread 2. |
| `S^m` | `I_{Tn}` in this PoC (all entries treated as latent). | observed-entry embedding deferred to a later PoC |
| `M_m` | Mariano–Murasawa monthly→quarterly growth weights `(1/3, 2/3, 1, 2/3, 1/3)` placed on the chosen low-frequency variable index, for each quarter whose end-month lies in `[6, T]`. | at most 5 nonzeros per row |
| `lambda` | Soft-aggregation penalty, default `1e4`. | sensitivity study is Thread 4 |

### Initial-condition handling

Rows 0..p-1 of `H_B` carry fewer off-diagonal entries than interior
rows because lags before `t=0` are truncated. The quadratic form
`x' H_B' D H_B x` therefore evaluates the VAR residual energy at
boundary dates using only the available lags, which is mathematically
a truncated-lag prior on `(y_0, …, y_{p-1})`. The explicit and
matrix-free products agree on this convention to machine precision.
Modellers attaching this operator to a real MCMC should know that
posterior calibration of boundary dates differs from interior dates;
the standard fix (condition on observed pre-sample, fold into `c_B`)
is intentionally not done in the PoC.

The **explicit** path builds `D` as `scipy.sparse.block_diag(D_t)` and
forms `Kbar = H_B' D H_B + lambda * M_m' M_m`. A cheap SPD sanity
check (`assert_spd_small`) catches symmetry or definiteness errors
during future extensions. For `Tn <= 400` it runs a relative-Frobenius
symmetry check and a dense Cholesky on the symmetrised matrix; above
that it falls back to a sparse relative-skew check plus five random
`x' K x > 0` probes. Both branches use relative tolerances so the
check does not spuriously fail under large `lambda`.

The **matrix-free** path applies, per matvec:

1. `w  = H_B @ x`                                     (forward, sparse `nnz O(T p n^2)`)
2. for each date `t`: `u_t = B0' (diag(1/U_t) (B0 w_t))`  (local `n × n` block, total `O(T n^2)`)
3. `z  = H_B.T @ u`                                   (adjoint; `H_B.T` is a free CSC view)
4. `z += lambda * M_m' (M_m x)`                       (aggregation penalty)

The SV update only touches the small dense `(T, n)` array `U_inv`,
never the global precision. `H_B.T` is *not* cached as a separate
CSR -- `scipy.sparse.csr_matrix.T` returns a CSC view of the same
data, so allocating a transposed CSR would double sparse storage for
no measured speed gain.

## Equivalence Results

Test sweep (`test_equivalence.py`): 5 configurations × 4 seeds × 20
random vectors per config. Tolerance: `1e-10`.

| (n, T, p, λ, σ_SV)         | seeds | max relative error |
|----------------------------|-------|--------------------|
| (3, 20, 1, 1e2, 0.1)       | 0,1,7,42 | 4.2e-16 |
| (3, 20, 2, 1e4, 0.3)       | 0,1,7,42 | 4.2e-16 |
| (5, 30, 2, 1e4, 0.5)       | 0,1,7,42 | 3.9e-16 |
| (5, 60, 3, 1e6, 0.8)       | 0,1,7,42 | 3.3e-16 |
| (7, 45, 4, 1e4, 0.3)       | 0,1,7,42 | 4.6e-16 |

**All cases: max relative error ≈ 3–5 × 10⁻¹⁶ (machine precision).**
Acceptance criterion satisfied with six orders of magnitude margin.
The SPD sanity check passes for all small cases.

## Regression after time-average correction

A separate test (`test_time_avg_precision.py`) validates the
*time-averaged* precision block used by the Thread 2 / 2b preconditioner:

```
D_bar  =  mean_t( D_t )  =  B0' diag( mean_t(1/U_t) ) B0,
```

NOT the naive `B0' diag(1 / mean_t(U_t)) B0`. The two differ for any
non-degenerate SV by Jensen's inequality applied to `u -> 1/u`. The
test asserts:

- per-date mean of `D_t` equals `B0' diag(mean(1/U_t)) B0` to ~1e-16;
- `_build_time_averaged_kbar` (in `thread2_pcg/preconditioners.py`,
  now corrected) matches an independently-built reference to ~1e-19
  Frobenius / ~1e-17 random-vector matvec;
- the old `1/mean(U_t)` construction differs from the corrected
  `mean(1/U_t)` form by 18–27% at `sv_sigma = 0.3` and 42–52% at
  `sv_sigma = 0.5` in the `D_bar` block, documenting the size of the
  Thread 2 / 2b correction.

**Important:** Thread 1's actual `SVAwareKbar` operator is unchanged
and continues to apply the per-date `D_t = B0' diag(1/U_t) B0`. The
equivalence test still passes at machine precision. The time-average
correction lives entirely in the preconditioner builder used by
Threads 2, 2b, and 3; it does not alter any conclusion in this thread.

## Runtime and Memory

### Per-matvec only (`bench_scaling.py`, excerpt)

| n | T | p | Tn | matrix-free (ms) | explicit (ms) | H_B nnz | Kbar nnz | mf MB | explicit MB |
|---|---|---|----|------------------|---------------|---------|----------|-------|-------------|
| 3 |  120 | 2 |   360 | 0.012 | 0.003 |  2 493 |   5 580 |  0.04 |  0.07 |
| 3 |  960 | 2 |  2880 | 0.042 | 0.022 | 20 133 |  45 060 |  0.31 |  0.55 |
| 5 |  960 | 2 |  4800 | 0.070 | 0.045 | 52 725 | 121 764 |  0.73 |  1.48 |
| 5 |  240 | 6 |  1200 | 0.037 | 0.032 | 36 675 |  76 950 |  0.46 |  0.93 |

The matrix-free path holds roughly nnz(H_B) of sparse storage; the
explicit path holds nnz(Kbar) ≈ 2 nnz(H_B). The naive 2× ratio
observable in the small table above is not a uniform "50% saving" --
it reflects the specific product structure `A' D A`, where `D` is
block-diagonal so the product `H_B' D H_B` has roughly the same
sparsity pattern as `H_B' H_B`. Real savings show up further
downstream when `D` would need to be assembled and re-assembled
every SV update on the explicit path.

### Amortised per-PCG-iteration (`bench_amortised.py`) — SUPERSEDED

The original Thread 1 amortised benchmark compared

```
cost_explicit  = assemble_Kbar + iter_PCG * ex_matvec
cost_matfree   =                 iter_PCG * mf_matvec
```

and reported a 4–8× advantage for the matrix-free path at `iter_PCG = 50`.
**Both terms are wrong for the comparison that actually matters** in an
MCMC step:

- The real explicit baseline is `assemble + factor + back-solve` (direct
  CHOLMOD), not `assemble + iter_PCG SpMVs`. CHOLMOD performs one
  back-solve per draw, not `iter_PCG` matvecs.
- The hard-coded `iter_PCG = 50` is contradicted by Thread 2: measured
  PCG iteration counts range from ~7 (sv=0.1) to >1000 under high SV
  dispersion with lightweight preconditioning.

Thread 2b's phase-separated benchmark replaces this comparison and
finds the opposite: direct CHOLMOD wins on total time at every
Taiwan-scale grid cell. The `bench_amortised.py` script is retained
only for reproducibility of older table references; its conclusions
are not load-bearing.

## What This PoC Does Not Yet Verify

- **PCG behaviour**: matvec ≠ solve. Whether `iter_PCG` is stable as SV
  dispersion or `lambda` grows is Thread 2.
- **Basis-filter forward operator**: `H_B` is built as a sparse banded
  matrix, not as a parametric-lag FFT filter. The matvec equivalence
  result is therefore conservative w.r.t. the operator in the report.
- **Observed embedding**: `S^m = I`. Reinstating `S^o, S^m` and `c_B`
  is a small extension before any real MCMC.
- **Basis-filter stress path**: `build_H_B` has been vectorised via bulk
  COO construction (`np.meshgrid` + `np.tile` per lag), so the Thread 2c
  stress cells (n=20, T=10000, p=24) are no longer blocked by sequential
  Python iteration. What is still untested at that scale is the
  *basis-filter* forward operator referenced in main.tex eq (12); the
  current path materialises sparse `H_B` rather than applying a parametric
  lag-filter on the fly. Validating an FFT or block-Toeplitz forward op
  is Thread 2c (or a later thread) work, not Thread 1.
- **Identification**: this is purely a numerical-operator test, with
  no statement about `B0` recoverability (Thread 6).

## Files

```
theory/mf_oi_svmvar_report/code/thread1_matvec/
├── dgp.py                       # H_B, B0, U_t, M_m construction
├── kbar_explicit.py             # ground-truth sparse Kbar assembly + matvec + SPD sanity check
├── kbar_matfree.py              # SV-aware matrix-free operator (LinearOperator)
├── test_equivalence.py          # acceptance test, rel err < 1e-10
├── test_time_avg_precision.py   # regression test for the corrected D_bar in Thread 2/2b
├── bench_scaling.py             # per-matvec runtime / memory sweep
├── bench_amortised.py           # SUPERSEDED -- see Thread 2b for the fair-cost benchmark
└── THREAD1_NOTE.md              # this file
```

Reproduce: `cd theory/mf_oi_svmvar_report/code/thread1_matvec && python3 test_equivalence.py && python3 test_time_avg_precision.py`.

## Verdict

Thread 1 acceptance criteria are met:

- [x] **Relative matvec error below `1e-10` in small test cases.**
      Measured at machine precision (~`3e-16`) across all 20
      configurations, unchanged after the H_BT-removal, `build_H_B`
      COO vectorisation, and SPD-check upgrade (large-`Tn` branch
      now runs a relative sparse symmetry check plus random PSD
      probes instead of no-op).
- [x] **Time-averaged precision block correctness.** The corrected
      `mean(1/U_t)` builder matches the per-date-mean reference to
      ~1e-19 Frobenius. The old `1/mean(U_t)` construction is
      documented to differ by 18–52% under realistic SV.
- [x] **Runtime and memory reported for increasing T.**
      `bench_scaling.py` is current. `bench_amortised.py` is retained
      but flagged as superseded by Thread 2b.

The unblocked next step remains **Thread 4 (lambda sensitivity)** under
the corrected preconditioner.

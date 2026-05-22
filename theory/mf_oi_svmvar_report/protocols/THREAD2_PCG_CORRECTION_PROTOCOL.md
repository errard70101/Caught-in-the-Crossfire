# Thread 2 Protocol: Corrected PCG / Preconditioner Rerun

Reference implementation: `code/thread2_pcg/`.

## Formal Target

Solve

```text
K x = b,
K = H_B' blockdiag(D_t) H_B + lambda M' M,
D_t = B0' diag(1 / U_t) B0,
```

with PCG using a matrix-free `K` matvec and compare preconditioners.

The corrected time-averaged precision preconditioner is

```text
D_bar = mean_t(D_t) = B0' diag(mean_t(1 / U_t)) B0,
K_pre = H_B' (I_T kron D_bar) H_B + lambda M' M.
```

## Preconditioners

Primary lightweight preconditioners:

- `none`
- scalar Jacobi
- date block-Jacobi

Strong diagnostic preconditioners:

- corrected `time_averaged_lu`
- corrected `time_averaged_chol`

Any legacy preconditioner using `1 / mean(U_t)` must be renamed explicitly, for example `time_avg_volatility_chol`, and cannot be reported as time-averaged precision.

## Algorithm

For each cell:

1. Generate DGP with fixed seed.
2. Build matrix-free `K` operator.
3. Build explicit `K` only for lightweight preconditioner setup and direct baselines.
4. Build corrected `K_pre` using `D_bar = mean_t(D_t)`.
5. Run `scipy.sparse.linalg.cg` with:

```text
rtol = 1e-8
atol = 0
maxiter = min(5 * Tn, 20000)
```

6. Count iterations using a callback.
7. Report relative residual against the actual `K`, not against `K_pre`.

## Reduced Correction Grid

The first correction rerun should not repeat the full old sweep. Use:

```text
n = 5
T = 480
p = 2
lambda = 1e4
target_radius = 0.9
sv_rho = 0.95
sv_sigma in {0.1, 0.3, 0.5, 0.8, 1.2}
seeds in {0, 1, 7}
```

Optional comparison:

- include legacy `1 / mean(U_t)` preconditioner only if it is clearly labeled as legacy.

## Validation Invariants

Corrected `K_pre` small-case invariant:

```text
||K_pre_exp x - K_pre_builder x|| / ||K_pre_exp x|| < 1e-10.
```

PCG solve invariant:

```text
||b - K x_pcg|| / ||b|| <= 1e-8 up to normal solver tolerance.
```

## Benchmark Accounting

Report:

```text
setup_time,
solve_time,
iters,
hit_maxiter,
relative_residual,
matvec_time_mean,
direct_cholmod_setup_time,
direct_cholmod_solve_time.
```

Thread 2 may report direct solve timings, but final total-cost claims belong to Thread 2b.

## Expected Outputs

- A correction CSV, for example `results_time_avg_precision_correction.csv`.
- A correction note, for example `THREAD2_TIME_AVG_PRECISION_CORRECTION.md`.
- A direct statement of whether corrected `D_bar` changes the previous preconditioner ranking.

## Forbidden Claims

Do not claim:

- old Thread 2 iteration counts are final after the correction;
- `time_averaged_chol` uses time-averaged precision unless it uses `mean_t(D_t)`;
- a PCG iteration improvement alone proves production competitiveness.


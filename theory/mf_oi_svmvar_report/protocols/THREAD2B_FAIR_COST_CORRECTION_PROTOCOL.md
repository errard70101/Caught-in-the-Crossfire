# Thread 2b Protocol: Corrected Fair-Cost Rerun

Reference implementation: `code/thread2b_fair_cost/`.

## Formal Target

Re-evaluate fair total cost after correcting the time-averaged precision preconditioner:

```text
D_bar = mean_t(D_t),
K_pre = H_B' (I_T kron D_bar) H_B + lambda M' M.
```

Direct CHOLMOD rows from the original Thread 2b remain valid because they use the actual `K`. PCG rows using `K_pre` must be rerun.

## Paths

Required paths:

- `direct_cholmod`: explicit `K` assembly + CHOLMOD factor + solve.
- corrected `pcg_time_avg_precision_chol_explicit_avgK`: explicit corrected `K_pre` assembly + CHOLMOD factor + PCG solve using actual matrix-free `K`.

Optional paths:

- `direct_splu`.
- legacy `pcg_time_avg_volatility_chol_explicit_avgK`, clearly labeled.
- amortized best-case derived row, clearly labeled and never treated as production.

## Reduced Rerun Grid

Run representative cells before any full rerun:

```text
(n=5,  T=480,   p=2,  sv_sigma=0.3)
(n=5,  T=1920,  p=2,  sv_sigma=0.3)
(n=10, T=5000,  p=12, sv_sigma=0.3)
(n=20, T=10000, p=12, sv_sigma=0.3)
(n=20, T=10000, p=12, sv_sigma=0.5)  optional but recommended
seeds in {0, 1, 7}
```

Use the same `lambda=1e4`, `target_radius=0.9`, and `sv_rho=0.95` as Thread 2b unless explicitly varied.

## Algorithm

For each cell and path:

1. Build DGP.
2. Build actual matrix-free `K` operator.
3. For direct path, assemble actual `K`, factor, solve.
4. For PCG path, assemble corrected `K_pre`, factor, solve actual `K x = b` with PCG.
5. Record status even on skip, timeout, or failure.

## Validation Invariants

All successful rows must satisfy:

```text
total_time = phase1_assembly_time + phase2_factor_time + phase3_solve_time.
```

Direct residual:

```text
||b - K x_direct|| / ||b|| near direct numerical precision.
```

PCG residual:

```text
||b - K x_pcg|| / ||b|| <= 1e-8 unless status indicates hit_maxiter or timeout.
```

Failure accounting:

- no failed cell may disappear from the CSV;
- emit `status=cell_failed:<reason>` rows if a cell-level exception occurs.

## Memory Accounting

Report:

```text
H_B_nnz,
K_nnz_estimate,
K_pre_nnz_estimate,
K_csr_bytes_estimate,
L_factor_nnz,
M_nnz,
whether H_B.T is copied.
```

If corrected `K_pre` has the same sparsity pattern as old `Kbar_avg`, state this explicitly.

## Expected Outputs

- `results_time_avg_precision_correction.csv`.
- `THREAD2B_TIME_AVG_PRECISION_CORRECTION.md`.
- A table comparing original PCG rows and corrected PCG rows for the reduced grid.
- A conclusion stating whether direct CHOLMOD remains dominant after the correction.

## Forbidden Claims

Do not claim:

- matrix-free wins if setup/factorization is omitted;
- corrected PCG changes production recommendation before fair total cost is measured;
- skipped or timed-out rows are evidence of success.


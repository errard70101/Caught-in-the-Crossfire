# Thread 2c Protocol: No-Explicit-Kbar Matrix-Free Preconditioner

This protocol must be reviewed before Thread 2c implementation begins.

## Objective

Develop and benchmark a scalable preconditioner or sampler path that avoids explicit global `Tn x Tn` assembly of both:

```text
K      = H_B' blockdiag(D_t) H_B + lambda M' M,
K_pre  = H_B' (I_T kron D_bar) H_B + lambda M' M.
```

The method must use the corrected time-averaged precision block:

```text
D_bar = mean_t(D_t) = B0' diag(mean_t 1/U_t) B0.
```

## Solver Choice Under Review

The first candidate is a structured banded Cholesky preconditioner using SciPy banded storage and solves.

This is acceptable as Thread 2c's first route if the implementation satisfies all invariants below.

## Banded Structure

Ignoring aggregation, `K_pre` is block-banded with block half-bandwidth `p`. Since each block is dense `n x n`, the scalar half-bandwidth is

```text
u_var = p * n + (n - 1).
```

The aggregation penalty `M' M` may increase bandwidth. For Mariano-Murasawa 5-month aggregation on one variable,

```text
u_agg <= 4 * n.
```

This is a conservative whole-system bound. If only `n_m` macro variables are
subject to Mariano-Murasawa aggregation and the storage builder can track their
positions, the tighter bound is

```text
u_agg <= 4 * n_m.
```

Using `4 * n` is correct but may over-allocate banded storage.

The scalar half-bandwidth used for banded storage must be

```text
u = max(u_var, u_agg).
```

Do not use `p*n + 1` as the bandwidth.

## Candidate Algorithm: Banded Time-Averaged Precision

1. Compute `D_bar = B0' diag(mean_t 1/U_t) B0`.
2. Derive block offsets for

```text
K_pre = H_B' (I_T kron D_bar) H_B + lambda M' M.
```

3. Construct the banded array `ab` in SciPy lower-band convention for
   `scipy.linalg.cholesky_banded(..., lower=True)`:

```text
ab[i - j, j] = K_pre[i, j] for i >= j and i - j <= u.
```

The code and tests must use this lower-band convention throughout. Do not
switch conventions between construction, factorization, solve, and CSV
diagnostics.

4. Include boundary corrections for the first `p` dates induced by truncated
   lag equations in `H_B`. End-of-sample dates do not require special bandwidth
   handling because the VAR residual operator is lower-block-triangular with
   pre-sample truncation only at the start.
5. Add `lambda M' M` into the same banded array. Before writing aggregation
   terms into `ab`, compute the actual nonzero pattern of `M' M` and assert that
   every scalar column offset is at most `u_agg`. If any aggregation term falls
   outside the chosen bandwidth, the test must fail rather than silently
   dropping it.
6. Factor with `cholesky_banded`.
7. Apply the preconditioner with `cho_solve_banded` inside PCG.

`K_pre` depends on `B0` through `D_bar` and on the current volatility paths
through `mean_t 1/U_t`. In a full sampler, the banded preconditioner setup can
be amortized across PCG iterations within one latent-path sweep only. It cannot
be amortized across MCMC sweeps after `B0` or any volatility path is updated.

## Alternative Routes

Acceptable alternatives, if banded Cholesky fails:

- block-banded custom Cholesky;
- state-space / Kalman simulation smoother for the same Gaussian draw;
- FFT or block-Toeplitz approximation only if approximation error is measured against direct CHOLMOD and explicitly labeled approximate.

## Validation Invariants

Small-case banded construction:

```text
||K_pre_dense_from_banded - K_pre_explicit.toarray()||_F
/ ||K_pre_explicit.toarray()||_F < 1e-10.
```

Random-vector preconditioner invariant:

```text
||K_pre_banded x - K_pre_explicit x|| / ||K_pre_explicit x|| < 1e-10.
```

Solve invariant:

```text
||K_pre x_banded_solve - r|| / ||r|| < 1e-10
```

for small and medium cases where explicit `K_pre` can be built.

PCG invariant:

```text
||b - K x_pcg|| / ||b|| <= 1e-8
```

unless status is `hit_maxiter` or timeout.

Numerical factorization invariant:

- `cholesky_banded` failure must be reported as a solver failure, not silently repaired.
- If diagonal jitter, ridge regularization, rescaling, or an approximate solve is introduced, the method must be renamed or explicitly labeled approximate.
- The perturbation must be reported, and accuracy must be rechecked against direct CHOLMOD.

## Benchmark Grid

Start with small correctness cells:

```text
(n=3, T=20, p=2, sv_sigma=0.3)
(n=5, T=30, p=3, sv_sigma=0.5)
```

Then reduced stress cells:

```text
n in {10, 20}
T in {5000, 10000}
p in {12, 24}
sv_sigma in {0.1, 0.3, 0.5}
lambda in {1e4}
seeds in {0, 1, 7}
```

The headline feasibility cell is:

```text
n=20, T=10000, p=24.
```

This headline cell is a memory-feasibility test, not an unconditional
requirement that the banded route succeed on every machine. For `n=20`,
`T=10000`, and `p=24`, the VAR scalar half-bandwidth is
`u_var = p*n + (n-1) = 499`, so lower-banded storage alone is approximately
`Tn * (u+1) * 8 bytes = 200000 * 500 * 8`, about 800 MB before factor storage,
temporary arrays, and Python overhead. If pre-flight memory accounting predicts
that this cell exceeds the configured memory budget, report
`status=skipped_memory_estimate` and do not count it as a numerical
factorization failure. If the cell is attempted and `cholesky_banded` fails,
report it as a banded-route solver failure.

Lambda stress slice:

```text
lambda in {1e4, 1e5, 1e6, 1e7}
cells:
  (n=5,  T=1920,  p=2,  sv_sigma=0.3)
  (n=10, T=5000,  p=12, sv_sigma=0.3)
  (n=20, T=10000, p=12, sv_sigma=0.3)
```

This slice tests whether high aggregation penalties break the banded solver earlier than CHOLMOD. If Thread 4 later recommends a lambda outside this slice, extend the slice before making scalable-solver claims.

## Benchmark Accounting

Compare at least:

- `direct_cholmod`, when feasible;
- corrected `pcg_time_avg_precision_chol_explicit_avgK`;
- new `pcg_banded_time_avg_precision_chol`.

Report:

```text
structured_setup_time,
banded_factor_time,
pcg_solve_time,
total_time,
iters,
relative_residual,
bandwidth_u,
lambda,
banded_storage_bytes,
H_B_storage_bytes,
whether H_B is materialized,
whether K_pre is materialized.
```

If the method still materializes `H_B`, say so. The contribution is no-explicit-`K_pre`, not necessarily no-`H_B`.
For full-sampler cost projections, count `structured_setup_time` and
`banded_factor_time` once per latent-path sweep whenever `B0` or volatility has
changed; do not amortize those costs across the full MCMC chain.

## Expected Outputs

- `code/thread2c_matrix_free_preconditioner/`
- `THREAD2C_NOTE.md`
- correctness CSV or test logs;
- benchmark CSV;
- total-time and memory plots;
- explicit proposal-facing claim stating where the method wins, loses, or remains unresolved.

## Review Gate Before Implementation

Before coding, reviewer must approve:

1. `D_bar` definition.
2. lower-band storage convention for `cholesky_banded(..., lower=True)`.
3. scalar bandwidth formula.
4. aggregation penalty handling.
5. boundary correction strategy.
6. benchmark cells.
7. what counts as a successful matrix-free claim.
8. lambda stress slice and failure handling for banded Cholesky breakdown.

## Forbidden Claims

Do not claim:

- no `Tn x Tn` matrix is stored if `H_B` is stored;
- the method is exact if it uses an approximation without error diagnostics;
- a total-cost advantage if setup/factorization is excluded;
- high-SV readiness if `sv_sigma=0.5` hits maxiter or times out.
- lambda robustness if only `lambda=1e4` was tested.

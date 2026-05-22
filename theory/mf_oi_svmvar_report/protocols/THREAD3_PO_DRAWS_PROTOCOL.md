# Thread 3 Protocol: Perturbation-Optimisation Gaussian Draws

Reference implementation: `code/thread3_po_draws/`.

## Formal Target

Draw from

```text
y | rest ~ N(K^{-1} h, K^{-1}),
K = H_B' blockdiag(D_t) H_B + lambda M' M,
h = lambda M' y_L.
```

Direct CHOLMOD is the gold-standard reference draw. PCG draws are diagnostic only until scalable preconditioning is established.

This RHS is intentionally the controlled Gaussian test RHS. In production,
where only missing entries are sampled, the latent-path RHS must be

```text
A' D r + lambda M_m' y_tilde^L,
```

with `r` carrying intercept, volatility-in-mean, and observed high-frequency
contributions. Thread 7 must restore this term before composing the full sampler.

## Perturbation-Optimisation Algorithm

For each draw:

1. Sample `eta_t ~ N(0, I_n)` independently for `t = 1..T`.
2. Construct `s_t = B0' diag(1 / sqrt(U_t)) eta_t`, so `s ~ N(0, blockdiag(D_t))`.
3. Sample `zeta ~ N(0, I_m)`, where `m` is the number of aggregation rows.
4. Construct

```text
v = h + H_B' s + sqrt(lambda) M' zeta.
```

Then

```text
v ~ N(h, K).
```

5. Solve `K y_draw = v`.
6. Then `y_draw ~ N(K^{-1} h, K^{-1})`.

Direct path:

```text
assemble K -> CHOLMOD factor -> factor(v).
```

PCG diagnostic path:

```text
matrix-free K matvec + corrected time-averaged precision preconditioner.
```

## Corrected PCG Dependency

Any PCG diagnostic rerun must use the corrected preconditioner:

```text
D_bar = mean_t(D_t) = B0' diag(mean_t 1/U_t) B0.
```

Old `1 / mean(U_t)` PCG diagnostics are superseded.

## Validation Invariants

Small cases with dense or selected exact summaries:

```text
mu = K^{-1} h,
Var(c_j' y) = c_j' K^{-1} c_j.
```

For scalar functionals:

```text
|sample_mean(c_j' y) - c_j' mu| <= 2 * MCSE_j
sample_var(c_j' y) matches c_j' K^{-1} c_j within sampling error.
```

Direct-vs-PCG paired-noise diagnostic:

```text
||y_pcg - y_direct|| / ||y_direct|| is consistent with PCG residual and conditioning.
```

Distribution diagnostic:

- KS tests on selected functionals should not show systematic rejection beyond multiple-testing expectations.
- Tolerance sensitivity should show PCG numerical error below Monte Carlo error.

## Reduced Correction Rerun

After correcting `D_bar`, rerun only diagnostic cells first:

```text
scales:
  small:  n=3, T=40,  p=2
  taiwan: n=5, T=480, p=2
sv_sigma in {0.1, 0.3}
rtol in {1e-6, 1e-8, 1e-10} for sv_sigma=0.3
```

Use the same direct draw reference. The direct CHOLMOD distribution result need not be recomputed if no direct code changed, but rerunning it in the same script is acceptable for reproducibility.

## Benchmark Accounting

For PCG diagnostics report:

```text
preconditioner_setup_time,
iters_mean,
iters_max,
relative_residual_mean,
relative_residual_max,
direct_solve_time_mean,
pcg_solve_time_mean.
```

Do not interpret draw-level PCG solve time without Thread 2b-style setup accounting.

## Expected Outputs

- Updated or correction-labeled `po_moments` CSV.
- Updated or correction-labeled `po_functionals` CSV.
- Updated or correction-labeled `pcg_tolerance` CSV.
- `THREAD3_TIME_AVG_PRECISION_CORRECTION.md` or an amended note section.

## Forbidden Claims

Do not claim:

- PCG is production-ready from Thread 3 alone;
- old PCG tolerance results remain final after correcting `D_bar`;
- matching a few functionals proves high-SV or large-scale PCG validity.

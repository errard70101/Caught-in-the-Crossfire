# Thread 4 Protocol: Lambda Sensitivity and Exact Aggregation Limit

## Objective

Choose a finite soft-aggregation penalty `lambda` that makes the latent high-frequency path sufficiently consistent with observed low-frequency aggregates without creating avoidable conditioning, solver, or posterior-distortion problems.

Thread 4 is not a solver-ranking thread. It studies the statistical and numerical effect of

```text
K(lambda) = H_B' blockdiag(D_t) H_B + lambda M' M,
h(lambda) = lambda M' y_L.
```

## Formal Target

For each `lambda`, the target Gaussian posterior is

```text
y | rest, lambda ~ N(mu_lambda, K(lambda)^{-1}),
mu_lambda = K(lambda)^{-1} h(lambda).
```

The aggregation residual is

```text
r_agg(lambda) = M mu_lambda - y_L.
```

If posterior draws are available, also track draw-level residuals:

```text
M y_draw - y_L.
```

## Lambda Grid

Start with:

```text
lambda in {1e2, 1e3, 1e4, 1e5, 1e6, 1e7}
```

Extend only if:

- aggregation residual is not yet stable at `1e7`; or
- conditioning or direct CHOLMOD failures appear before the residual stabilizes.

## Algorithm

For each DGP cell and `lambda`:

1. Build `K(lambda)` and `h(lambda)`.
2. Solve for `mu_lambda` using direct CHOLMOD where feasible.
3. Compute aggregation residual norms.
4. Compute posterior variance summaries for selected functionals.
5. Record solver diagnostics:
   - direct CHOLMOD assembly time;
   - factor time;
   - solve time;
   - residual;
   - any numerical failure.
6. Optionally run corrected time-averaged precision PCG diagnostics only in regimes where Thread 2 correction shows controlled convergence.

## Diagnostics

Aggregation residual:

```text
||M mu_lambda - y_L||_2 / max(||y_L||_2, 1e-300)
||M mu_lambda - y_L||_inf
```

Posterior stability:

```text
||mu_lambda - mu_lambda_ref||_2 / max(||mu_lambda_ref||_2, 1e-300)
```

where `lambda_ref` is the largest numerically stable `lambda` in the grid.

Variance stability for selected functionals `c_j`:

```text
|c_j' K(lambda)^{-1} c_j - c_j' K(lambda_ref)^{-1} c_j|
/ max(c_j' K(lambda_ref)^{-1} c_j, 1e-300).
```

Conditioning proxies:

- direct CHOLMOD factor success/failure;
- direct residual;
- factor time growth;
- optional Lanczos/eigenvalue proxy on small cases only;
- corrected PCG iteration count if PCG is exercised.

## Solver-Specific Stability Gate

Thread 4's lambda recommendation must distinguish statistical adequacy from solver-specific numerical stability.

At minimum, report lambda stability for:

- direct CHOLMOD on explicit `K(lambda)`;
- corrected explicit `K_pre(lambda)` PCG if Thread 2 correction shows controlled convergence;
- Thread 2c banded Cholesky if Thread 2c has been implemented.

CHOLMOD success does not imply `scipy.linalg.cholesky_banded` success. If Thread 2c's banded solver fails at a lambda value that CHOLMOD handles, the recommended lambda range for scalable matrix-free use must be narrower or the banded route must be labeled numerically unstable at that lambda.

If any solver adds diagonal jitter, ridge regularization, pivoting, or rescaling beyond algebraic equivalence, the output must label the method as modified or approximate and report the perturbation size.

## Validation Invariants

For every successful direct solve:

```text
||h(lambda) - K(lambda) mu_lambda|| / ||h(lambda)|| near direct numerical precision.
```

Aggregation residual should be monotone weakly decreasing in broad terms as `lambda` rises; small non-monotonicity from numerical error must be investigated.

Posterior summaries should stabilize over a finite lambda interval before recommending a default.

## Recommended Output

- `code/thread4_lambda_sensitivity/`
- `THREAD4_NOTE.md`
- `lambda_sensitivity.csv`
- plot of aggregation residual vs `lambda`;
- plot/table of posterior summary changes vs `lambda`;
- table of direct CHOLMOD and optional corrected-PCG diagnostics.

## Acceptance Criteria

- A finite recommended lambda range is documented.
- The recommendation is based on aggregation residual, posterior stability, and solver stability.
- The recommendation separates direct-CHOLMOD-safe lambda values from Thread-2c-banded-safe lambda values once the banded route exists.
- Direct CHOLMOD remains the primary reference unless Thread 2c supplies a validated scalable alternative.
- If no finite stable range is found, the note must say so and identify whether the problem is statistical residual, conditioning, or solver failure.

## Forbidden Claims

Do not claim:

- "`lambda` should be large" without a finite rule;
- exact aggregation is achieved unless the residual is numerically measured;
- PCG lambda behavior is relevant unless the corrected preconditioner is used;
- lambda sensitivity can be skipped because Thread 1-3 used `lambda=1e4`.
- a lambda value is safe for all solvers because it is safe for CHOLMOD.

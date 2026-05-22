# Thread 5 Protocol: Parametric Lag Stability Screening

## Objective

Make the basis-lag restriction operational while controlling stationarity and rejection rates.

This protocol covers two distinct experiments: prior or proposal draws used to
measure stationarity rejection risk, and the production SUR posterior update for
`Gamma_k` used inside the MCMC.

The model uses

```text
B_j = sum_{k=1}^K Gamma_k phi_k(j / p),  j = 1, ..., p,
```

instead of unrestricted lag matrices.

## Formal Target

Given basis functions `phi_k` and coefficient matrices `Gamma_k`, construct the VAR companion matrix

```text
C =
[ B_1 B_2 ... B_p ]
[ I   0   ... 0   ]
[ 0   I   ... 0   ]
[ ...             ].
```

The stationarity condition is

```text
rho(C) < 1,
```

where `rho(C)` is the spectral radius.

## SUR Posterior Update

Thread 5 is not only a reconstruction and stationarity-screening thread. It
must also define the conditional posterior update for the basis coefficients
used by the full sampler.

Given a sampled high-frequency path, common volatilities, and `B0`, define

```text
y_t_dagger = y_t* - b0 - sum_{j=0}^q A_j h_{t-j},
z_t        = (z_{1,t}', ..., z_{K,t}')',
z_{k,t}    = sum_{j=1}^p phi_k(j / p) y_{t-j}*.
```

Stack the coefficient matrices as

```text
G     = [Gamma_1 ... Gamma_K]              in R^{n x K n}
gamma = vec(G)
X_t   = z_t' kron I_n.
```

The conditional equation is

```text
y_t_dagger = X_t gamma + e_t,
e_t ~ N(0, Sigma_t),
Sigma_t^{-1} = D_t = B0' U_t^{-1} B0.
```

For a Gaussian prior `gamma ~ N(m0, Q0^{-1})`, the Gaussian conditional
posterior has precision and linear term

```text
Q_gamma = Q0 + sum_t X_t' D_t X_t,
q_gamma = Q0 m0 + sum_t X_t' D_t y_t_dagger,
gamma | rest ~ N(Q_gamma^{-1} q_gamma, Q_gamma^{-1}),
```

before applying the stationarity truncation. Minnesota priors enter through
`m0` and `Q0`. Horseshoe priors enter conditionally as a Gaussian prior with
draw-specific local and global shrinkage scales; those scales must be updated in
a separate shrinkage-hyperparameter step conditional on the current accepted
`gamma`.

Time-varying covariance handling:

- use `D_t = B0' U_t^{-1} B0` date by date in both `Q_gamma` and `q_gamma`;
- do not replace `D_t` by a time average in the posterior update unless the
  method is explicitly labeled approximate;
- drop or condition on pre-sample rows consistently with the latent-path
  boundary convention.

Required draw order for an exact rejection implementation:

1. Draw `gamma_candidate` from the Gaussian conditional implied by the current
   shrinkage scales.
2. Reconstruct `B_1, ..., B_p`.
3. Build the companion matrix and screen `rho(C) < rho_max`.
4. If the candidate passes, commit `gamma_candidate`; otherwise retain the
   previous accepted `gamma` and count a stationarity rejection.
5. Update shrinkage hyperparameters conditional on the current accepted
   `gamma`, using the chosen Minnesota or Horseshoe hierarchy.

If rejection rates hit the fallback triggers below, do not continue with plain
rejection as if it were a validated MCMC kernel. Switch to a documented
constrained proposal or explicitly record that Thread 7 cannot proceed with the
current lag update.

Preconditioning or factorization design for `Q_gamma` must be reported. For the
small Thread 7 synthetic DGP, dense or sparse Cholesky is acceptable. For larger
systems, any PCG or blocked SUR implementation must include a residual check for
the `Q_gamma` solve and must preserve the exact `D_t` weights.

At DHK-style stress dimensions such as `n=23` and `K=5`, the Gaussian SUR block
has dimension `n^2 K = 2645`, which is still plausibly dense-Cholesky territory.
Treat PCG or blocked SUR as an escape route for materially larger empirical
systems, not as a required bottleneck workaround at the protocol DGP scales.

## Basis Candidates

Required:

- normalized Legendre basis;
- normalized Almon polynomial basis;
- exponential decay basis.

Optional:

- B-spline basis, only if implementation cost is small.

Every basis must document:

- domain of `j / p`;
- normalization convention;
- whether an intercept/level basis is included;
- scaling of `Gamma_k`.

## Algorithm

For each basis and prior scale:

1. Draw `Gamma_k` from the proposed prior or screening distribution.
2. Construct `B_1, ..., B_p`.
3. Build the companion matrix.
4. Compute spectral radius.
5. Record accept/reject under `rho(C) < rho_max`, where default `rho_max = 0.99`.
6. Record distance-to-boundary statistics.

## Rejection-Rate Trap and Fallback Gate

Stationarity screening by rejection is a diagnostic, not automatically a viable MCMC strategy. In high-dimensional VARs, rejection rates can approach 100% if the unconstrained posterior places mass near or outside the stationarity boundary.

If rejection rates are high, do not simply shrink the prior until acceptance looks acceptable. Prior shrinkage can create a prior-driven stationary model that no longer reflects the data.

Fallbacks to consider and document before full MCMC:

- stationarity-preserving parameterization;
- Waggoner-Zha-style constrained proposal or accept/reject correction;
- local proposals that respect the companion-radius boundary;
- explicit decision to use a tighter prior, with prior-bias diagnostics.

Trigger conditions requiring a fallback note:

```text
rejection_rate > 0.80 for any production-relevant basis/prior cell,
or rejection_rate > 0.50 near the prior scale needed for data fit,
or accepted draws concentrate near rho(C) >= 0.98.
```

## Prior Scale Grid

Start with:

```text
Gamma_scale in {0.02, 0.05, 0.1, 0.2, 0.5}
n in {5, 10}
p in {12, 24}
K_basis in {3, 5}
draws >= 1000 per cell where feasible.
```

## Validation Invariants

Reconstruction invariant:

```text
B_j shape = (n, n) for all j,
number of B_j = p.
```

Companion invariant:

```text
C shape = (n*p, n*p).
```

Stationarity invariant:

```text
accepted iff max(abs(eigvals(C))) < rho_max.
```

Numerical reproducibility:

- fixed seeds must reproduce rejection rates;
- basis matrices should be saved or deterministically reconstructed.

## Diagnostics

Report:

- rejection rate;
- median and 95th percentile of `rho(C)`;
- distribution of accepted `rho(C)`;
- unconstrained draw distribution of `rho(C)`;
- prior-bias diagnostic when shrinking prior scale changes acceptance materially;
- runtime for screening;
- examples of accepted and rejected lag profiles.

## Recommended Output

- `code/thread5_lag_stability/`
- `THREAD5_NOTE.md`
- `lag_stability_screening.csv`
- plot of rejection rate by basis and prior scale;
- recommended basis and prior scaling.

## Acceptance Criteria

- Automated stationarity check exists and is tested.
- At least one basis/prior-scale combination has manageable rejection rates, target below 50% for initial implementation unless a more efficient sampler is planned.
- Recommended prior scale keeps `rho(C)` away from one enough to avoid pathological latent-state conditioning in Threads 1-4.
- If rejection is high, the note proposes a constrained-sampling fallback or explicitly documents the prior-bias tradeoff.
- The note states whether basis-lag restriction changes any Thread 1-4 solver assumptions.

## Forbidden Claims

Do not claim:

- a basis is stationarity-safe without companion screening;
- low rejection at `n=5` implies low rejection at larger `n`;
- stationarity screening solves identification of `B0`;
- prior scale is final without checking interaction with lambda and latent-state conditioning.
- lowering prior variance is harmless because it improves rejection rates.

# Thread SV/Classification Protocol: Volatility and State Updates

This protocol fills the posterior-simulation gap between the latent path, VAR
coefficient, and `B0` blocks. It covers the high-frequency updates for common
log volatilities, idiosyncratic volatilities, and Markov classification paths.

## Objective

Specify the standalone block required by `main.tex` Step 4 before Thread 7 can
compose a full synthetic MCMC. The implementation may inherit the DHK band-sparse
Acceptance-Rejection Metropolis-Hastings logic, but it must still pass
mixed-frequency-specific validation after conditioning on a sampled high-frequency
path.

## Conditional Target

Given a sampled full high-frequency path `y*`, current lag coefficients, `B0`,
volatility-in-mean coefficients, and classification states, compute structural
innovations

```text
eps_t = B0 (y_t* - b0 - sum_{j=1}^p B_j y_{t-j}* - sum_{j=0}^q A_j h_{t-j}).
```

The volatility block targets the conditional posterior for:

```text
h_t              common macro and financial log-volatility factors,
omega_{i,t}      idiosyncratic log-volatility components,
s_{i,t}          Markov classification state for unclassified variable i.
```

The production target is the DHK high-frequency conditional likelihood operated
on `eps_t`, with the sampled `y*` treated as observed for this block.

## Algorithmic Requirements

Common and idiosyncratic volatility update:

1. Build the band-sparse conditional log posterior for the relevant volatility
   path, including the volatility-in-mean terms used in the current model.
2. Use the DHK/CHKP ARMH update or an explicitly documented equivalent.
3. Preserve the same time indexing, lag truncation, and normalization used by
   the `B0` and lag-coefficient blocks.
4. Recompute `U_t` and therefore `D_t = B0' U_t^{-1} B0` after accepted
   volatility moves.

Classification update:

1. For each unclassified variable, define the two-state Markov transition
   matrix and the state-dependent loading on macro versus financial uncertainty.
2. Sample the full state path with forward-filtering/backward-sampling or an
   equivalent exact finite-state smoother.
3. Record posterior classification probabilities

```text
pi_{i,t} = Pr(s_{i,t} = macro | data)
```

   from retained MCMC draws.
4. If classification states are not included in a synthetic DGP, Thread 7 must
   state that the block is intentionally disabled and must not claim validation
   of classification probabilities.

## Standalone Tests

Synthetic volatility recovery:

- simulate `eps_t` from known volatility paths with fixed `B0` and fixed lag
  coefficients;
- run only the volatility block;
- verify posterior means and intervals for selected `h_t` and `omega_{i,t}`
  against the known paths in an easy signal-to-noise setting.

Classification recovery:

- simulate at least one unclassified variable with known two-state Markov path;
- run only the classification smoother conditional on known volatility factors;
- verify that state probabilities are high in persistent, well-separated
  regimes and uncertain near deliberately ambiguous regimes.

Integration smoke test:

- update `U_t` from a volatility draw;
- rebuild `D_t`;
- verify that the latent-path precision in Thread 1/3 accepts the updated `D_t`
  without dimension or positive-definiteness failures.

## Required Diagnostics

Report:

- ARMH proposal scale and acceptance rate for each volatility block;
- effective sample size for selected `h_t` and idiosyncratic volatility
  functionals;
- autocorrelation for common volatility factors;
- classification switching frequency by variable;
- posterior distribution of Markov transition probabilities, if sampled;
- fraction of draws in which a variable is classified macro or financial;
- failures caused by non-positive variance, invalid transition probabilities,
  or incompatible block dimensions.

Minimum diagnostic thresholds for an easy synthetic DGP:

```text
ARMH acceptance rate should be reported and investigated if below 0.15 or above 0.70.
ESS for selected h_t functionals should be nonzero and large enough for interval checks.
Classification paths should show nondegenerate switching unless the DGP is intentionally absorbing.
```

These thresholds are debugging gates, not universal empirical convergence
claims.

## Acceptance Criteria

- A standalone volatility update runs on a known synthetic DGP.
- `U_t` remains diagonal with strictly positive entries after every accepted
  update.
- Rebuilt `D_t = B0' U_t^{-1} B0` is symmetric positive definite in every tested
  date block.
- ARMH acceptance rates, ESS, and trace diagnostics are reported.
- Classification FFBS, when enabled, recovers easy state paths and reports
  switching frequencies.
- Thread 7 lists this protocol as a prerequisite before enabling SV or
  classification blocks in a full synthetic sampler.

## Forbidden Claims

Do not claim:

- the full MCMC validates Step 4 if this standalone block has not passed;
- DHK inheritance alone validates the mixed-frequency implementation;
- classification probabilities are meaningful if the classification block was
  disabled in the synthetic DGP;
- volatility mixing is adequate from acceptance rates alone.

# Thread 7 Protocol: Full MCMC Architecture Gate

Thread 7 is intentionally a gate-level protocol until Threads 1-6 and any
enabled SV/classification block have passed.

## Objective

Assemble a minimal block-Gibbs architecture for a synthetic MF-OI-SVMVAR only after the component protocols are satisfied.

Thread 7 is not an empirical Taiwan application. It is an architecture and recovery test on a small known DGP.

## Prerequisites

Thread 7 cannot start until:

- Thread 1 matvec protocol passes.
- Thread 2 corrected PCG rerun is reviewed.
- Thread 2b corrected fair-cost rerun is reviewed.
- Thread 3 PO draw protocol passes under corrected preconditioner diagnostics.
- Thread 4 recommends a finite lambda range or documents why none is available.
- Thread 5 recommends a basis-lag and stationarity screening rule.
- Thread 6 supplies at least a conditional `B0` diagnostic and a mixed-frequency identification caveat.
- `THREAD_SV_CLASSIFICATION_PROTOCOL.md` passes for any SV or classification
  block enabled in the synthetic sampler.

If any prerequisite fails, Thread 7 must be scoped down or postponed.

## Candidate Blocks

Minimal synthetic sampler:

1. Latent high-frequency path update using Thread 3 direct CHOLMOD reference path, or a Thread 2c method only if it passed.
2. VAR lag/basis coefficient update under Thread 5 stationarity screening.
3. `B0` update using DHK-style conditional logic given latent path, with proper priors.
4. SV update under `THREAD_SV_CLASSIFICATION_PROTOCOL.md`.
5. Classification/block update under `THREAD_SV_CLASSIFICATION_PROTOCOL.md`, if included in the synthetic DGP.

Each block must have a standalone test before full composition.

## Architecture Invariants

Dimension invariant:

```text
all blocks consume and return consistently stacked date-major y.
```

Stationarity invariant:

```text
all accepted VAR draws satisfy rho(C) < rho_max.
```

Latent-state invariant:

```text
latent update targets the Gaussian conditional defined in Global Definitions.
```

Thread 2c cost invariant:

```text
if a Thread 2c preconditioner is used, rebuild its setup after every accepted
B0 or volatility-path update that changes D_bar.
```

Thread 2c setup and factorization costs may be amortized across PCG iterations
inside one latent-path sweep, but not across the full MCMC chain.

Production RHS invariant:

```text
the full mixed-frequency latent update must include A' D r
plus lambda M_m' y_tilde^L.
```

Thread 3's controlled test RHS keeps only the aggregation-side data term. Thread
7 must restore the intercept, volatility-in-mean, and observed-high-frequency
contributions in `r` before claiming production architectural consistency.

`B0` normalization invariant:

```text
B0 normalization is fixed and used consistently in simulation, update, and recovery metrics.
```

Reproducibility invariant:

```text
fixed random seed reproduces all synthetic recovery summaries.
```

## Synthetic DGP

DHK reference:

The synthetic DGP ladder should be explicitly modeled on DHK's simulation study
in Section 3, Table 1, and Figures 1-3 of
`references/davidson-hou-koop-investigating-economic-uncertainty-using-stochastic-volatility-in-mean-vars-the-importance-of-model-size-order-invariance-and-classification-2025.pdf`.
DHK's key design choice is to simulate from a large order-invariant model with
time-varying classification, then estimate competing models that remove OI,
remove variables, or remove correct classification. Thread 7 should preserve
that comparison logic while adding mixed-frequency aggregation.

Start small:

```text
n = 3
T <= 240
p in {2, 4}
known B0
known basis-lag coefficients
controlled SV process
mixed-frequency observation through M.
```

Scale only after recovery and timing are understood.

Scale-up ladder:

1. Small smoke DGP: `n in {3, 6}`, `T <= 240`, dense unit-diagonal `B0`, one
   aggregated macro variable, and at most one unclassified variable.
2. Medium MF-OI DGP: `n in {10, 12}`, `T in {240, 480}`, dense `B0`, macro and
   financial blocks, and one unclassified variable that switches classification
   in the middle of the sample.
3. DHK-style stress DGP: `n = 23`, `T = 600`, with macro, financial, and three
   unclassified variables following the DHK pattern: one fixed macro, one fixed
   financial, and one temporarily switching state.

For each scale where feasible, compare:

- correctly specified `MF-OI-TVC`;
- order-dependent `MF-triangular-TVC`;
- omitted-variable `MF-OI-small`;
- fixed-classification `MF-OI-fixed-classification`;
- high-frequency oracle `HF-oracle-OI-TVC` when the computational budget allows.

## Diagnostics

Report:

- trace plots for key scalar parameters;
- posterior mean and interval for selected `B_j`, `Gamma_k`, `B0` entries;
- latent path recovery diagnostics;
- SV recovery diagnostics;
- stationarity rejection rate;
- per-block runtime;
- effective sample size where meaningful;
- `B0` block autocorrelation and effective sample size;
- split-R-hat across multiple chains for selected `B0` entries;
- chain-specific modes or label/normalization switching diagnostics;
- acceptance/rejection diagnostics for stationarity-constrained lag updates.

## Mixing Gate

Thread 7 must treat poor `B0` mixing as a model/identification warning, not just an MCMC tuning nuisance.

Minimum mixing diagnostics:

```text
multiple chains >= 4 where feasible;
ESS for selected B0 entries;
lag autocorrelation for selected B0 entries;
split-R-hat for selected B0 entries;
visual trace comparison across chains.
```

If `B0` ESS is poor or chains occupy different modes, the sampler is not considered validated even if each conditional block is mathematically correct.

If poor mixing aligns with Thread 6 weak-ID diagnostics, the conclusion should be weak marginal identification rather than merely "needs more MCMC iterations."

## Acceptance Criteria

- Each block passes standalone tests.
- Full sampler runs on a small synthetic DGP without dimension or stability failures.
- Synthetic parameters are recovered within documented Monte Carlo uncertainty for at least one easy DGP.
- Runtime bottleneck is identified quantitatively.
- `B0` mixing diagnostics are acceptable in the easy DGP, or poor mixing is explicitly traced to weak identification and reported as a failure/limitation.
- Any failed block is isolated and reported.

## Forbidden Claims

Do not claim:

- empirical readiness from a small synthetic DGP;
- full MF-OI-SVMVAR validity if any prerequisite protocol is unresolved;
- `B0` marginal identification from conditional update mechanics alone;
- Thread 2c scalability unless the Thread 2c protocol has passed.
- full sampler convergence from blockwise correctness alone.

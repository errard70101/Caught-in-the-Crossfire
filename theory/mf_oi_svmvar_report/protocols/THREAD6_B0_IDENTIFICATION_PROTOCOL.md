# Thread 6 Protocol: B0 Identification Diagnostics

## Objective

Diagnose whether the order-invariant heteroskedastic identification argument for `B0` remains credible in the latent mixed-frequency likelihood.

Thread 6 must separate:

1. conditional identification given a high-frequency latent path `y*`;
2. marginal identification after integrating over latent paths subject to mixed-frequency aggregation.

## Formal Statements

Conditional statement:

```text
Given y*, and under DHK-style heteroskedastic rank conditions,
B0 is identified up to the normalizations used by the OI-SVMVAR.
```

Marginal mixed-frequency statement:

```text
Identification after integrating over y* is not automatic.
It requires diagnostic or formal evidence that latent-path uncertainty
does not destroy the relevant rank variation.
```

No protocol may collapse these two statements.

## Diagnostic Targets

For simulated or posterior latent paths:

1. Compute residuals implied by candidate VAR dynamics.
2. Estimate or recover volatility-state variation.
3. Form the DHK / heteroskedastic rank diagnostic relevant to `B0`.
4. Track the diagnostic across:
   - latent path draws;
   - lambda values;
   - SV dispersion;
   - sample length;
   - known-DGP recovery cases.

The exact rank matrix must be specified in the Thread 6 note before implementation. If multiple plausible diagnostics exist, list them and choose one primary diagnostic.

## Marginal Weak-Identification and Mixing Risk

Passing a conditional rank diagnostic for each sampled `y*` is not sufficient. If mixed-frequency aggregation leaves large uncertainty about `y*`, the marginal posterior for `B0` may be flat, weakly identified, or multimodal even when conditional identification holds.

Thread 6 must therefore add diagnostics for marginal weakness:

- variation of the rank diagnostic across latent-path draws;
- curvature or concentration of the `B0` objective/posterior surrogate across latent draws;
- sensitivity of `B0` recovery to lambda;
- multimodality checks in controlled recovery experiments;
- posterior interval width or dispersion for normalized `B0` entries.

These diagnostics feed directly into Thread 7's MCMC mixing gate.

## Monte Carlo Recovery Design

Reference design:

Use DHK's simulation study as the observed-frequency template:
`references/davidson-hou-koop-investigating-economic-uncertainty-using-stochastic-volatility-in-mean-vars-the-importance-of-model-size-order-invariance-and-classification-2025.pdf`.
The relevant anchors are Section 3, Table 1, and Figures 1-3. DHK simulate a
large OI-SVMVAR with time-varying classification and then compare correctly
specified OI/TVC estimates against order-dependent and small-model alternatives.
Thread 6 should adapt this logic to the mixed-frequency setting rather than
inventing an unrelated Monte Carlo.

Minimum design:

```text
n in {3, 5}
T in {240, 480}
sv_sigma in {0.1, 0.3, 0.5}
lambda in recommended range from Thread 4
known B0
known or controlled VAR coefficients
latent path either observed or drawn from Thread 3 reference sampler.
```

Compare:

- observed high-frequency benchmark;
- mixed-frequency latent reconstruction with direct CHOLMOD draws;
- sensitivity to lambda.

DHK-inspired comparison ladder:

1. `HF-oracle-OI-TVC`: all high-frequency paths observed; dense unit-diagonal
   `B0`; time-varying classification enabled. This isolates the observed-frequency
   DHK identification benchmark.
2. `MF-OI-TVC`: same DGP, but macro variables are observed only through
   mixed-frequency aggregation. This measures latent-path degradation.
3. `MF-triangular-TVC`: same mixed-frequency DGP, but estimated with a
   lower-triangular/order-dependent `B0`. This isolates order-dependence bias.
4. `MF-OI-small`: omit relevant variables while keeping dense `B0`. This mirrors
   DHK's model-size experiment and measures omitted-variable bias.
5. `MF-OI-fixed-classification`: hold unclassified variables in fixed blocks.
   This measures classification misspecification.

The true DGP should use a dense unit-diagonal `B0`, because DHK's simulation
shows that triangular restrictions can severely distort uncertainty estimates
and impulse responses when the true impact matrix is unrestricted.

## Validation Invariants

Conditional diagnostic:

```text
rank_condition(y*) passes for observed/simulated high-frequency paths
under the known-DGP settings where identification should hold.
```

Latent sensitivity:

```text
rank_condition(y*_draw) is stable across posterior draws
within documented tolerance or uncertainty bands.
```

Weak-ID diagnostic:

```text
B0 diagnostic dispersion across y*_draw is reported,
and flat/multimodal cases are flagged rather than averaged away.
```

Recovery:

```text
distance(B0_hat, B0_true)
```

must be measured under the same normalization. The metric and normalization must be stated before reporting results.

## Required Outputs

- `THREAD6_NOTE.md`
- explicit definition of the rank diagnostic;
- Monte Carlo recovery design;
- diagnostic CSVs;
- plots of rank diagnostic across lambda and latent draws;
- weak-identification / posterior-flatness diagnostics for `B0`;
- list of assumptions needed for a formal identification lemma.

## Acceptance Criteria

- The note clearly states what is proved, what is diagnosed, and what remains open.
- Conditional identification is not presented as marginal mixed-frequency identification.
- A rank or recovery diagnostic is implemented on at least one controlled known-DGP case.
- The note states expected implications for Thread 7 mixing, including whether `B0` ESS/autocorrelation problems are likely.
- Failure cases are reported, not hidden.

## Forbidden Claims

Do not claim:

- high-frequency latent modeling automatically identifies `B0`;
- DHK's observed-frequency proof directly covers the integrated mixed-frequency likelihood;
- posterior draws with one lambda value establish identification;
- numerical recovery is a formal proof.
- conditional rank success guarantees good marginal MCMC mixing.

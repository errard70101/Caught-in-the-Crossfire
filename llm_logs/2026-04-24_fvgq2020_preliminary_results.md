# FVGQ 2020 Preliminary Simulated BCA - Results Memo

**Date:** 2026-04-24
**Spec:** `docs/superpowers/specs/2026-04-24-fvgq2020-preliminary-simulated-bca-design.md`
**Plan:** `docs/superpowers/plans/2026-04-24-fvgq2020-preliminary-simulated-bca.md`
**Code:** `code/bca_uncertainty_simulation/fvgq2020_preliminary/`

## Purpose

This memo summarizes the preliminary simulated-BCA exercise driven by the
Fernandez-Villaverde and Guerron-Quintana (2020, RED) two-agent DSGE model.
The goal is to obtain concrete wedge signatures of uncertainty shocks
(`uA` for TFP stochastic volatility and `ue` for collateral-LTV stochastic
volatility) before investing in the Section 7 representative-agent
LWZ+CGK hybrid.

## Methodology update: Inside-Dynare wedges (2026-04-25)

The wedge extraction pipeline has been migrated from a MATLAB-side algebraic
fixed-point approximation to **Inside-Dynare wedge extraction**. The solve-only
Dynare file now exports four auxiliary accounting observables:

- `wedge_A` → `log_A`
- `wedge_G` → `G_share`
- `wedge_l` → `tau_l`
- `wedge_x` → `tau_x`

The investment wedge is now pinned down by the CKM Euler accounting identity
inside Dynare, including the `wedge_x(+1)` forward expectation term. This makes
the wedge series true DGP observables rather than ex post fixed-point estimates
constructed from a finite simulated path. The likelihood/Kalman smoother remains
as the econometrician-facing recovery exercise and is now initialized from
`[wedge_A, wedge_l, wedge_x]`, with `G_share` copied from `wedge_G`.

The numerical tables below were produced before this migration and should be
treated as superseded once `run_fvgq2020_simulation`, `run_bca_analysis`, and
`plot_bca_responses` are rerun under the Inside-Dynare pipeline.

## Setup recap

- **DGP:** FVGQ (2020) model unchanged; baseline `higherphi = 0`; third-order
  perturbation with Dynare 6.2 native pruning.
- **Agents:** 6% entrepreneurs and 94% workers; this is a segmented two-agent
  economy, not a Krusell-Smith heterogeneous-agent setup.
- **Uncertainty shocks:** `uA` (macro uncertainty target) and `ue`
  (financial uncertainty target).
- **Warm-up:** `T_wu = 50,000` from DSS to SSS; convergence tail norm
  `0.000000e+00`, DSS-to-SSS gap norm `4.137892e-01`.
- **Experiment 1:** `T = 20,000` ergodic path; LP of each wedge on `(uA, ue)`
  with controls for level shocks, preference SV, lagged SV states, and lagged
  wedges.
- **Experiment 2:** `N = 1,000` antithetic pairs, horizon `H = 60`, run
  separately for `ue` and `uA`.
- **CKM prototype:** `alpha = 0.36`, `beta = 0.994`, `delta = 0.01625`,
  `gamma = 2`, `nu = 1`, `chi` matched to FVGQ steady-state labor.
- **Tripwire:** recovered `G/Y` is numerically zero (`max |G_share| = 8.403e-15`).

## Headline numbers

### LP peak responses (Experiment 1)

| Wedge | Macro peak (horizon) | Financial peak (horizon) |
|-------|----------------------|--------------------------|
| log A | `1.032677e-03` at `h=15` | `1.041233e-03` at `h=25` |
| G/Y | `6.992795e-17` at `h=5` | `-7.057125e-17` at `h=46` |
| tau_l | `-1.041823e-03` at `h=53` | `9.012600e-04` at `h=15` |
| tau_x | `-1.641801e-03` at `h=40` | `1.886355e-03` at `h=32` |

### GIRF peak responses (Experiment 2)

| Wedge | Macro peak [5-95%] | Financial peak [5-95%] |
|-------|---------------------|------------------------|
| log A | `-7.764880e-04` at `h=6` [`-1.404255e-02`, `1.155922e-02`] | `3.129173e-04` at `h=4` [`-5.009080e-03`, `5.725260e-03`] |
| G/Y | `-1.465494e-17` at `h=42` [`-2.498002e-16`, `2.220446e-16`] | `1.298267e-17` at `h=26` [`-2.220446e-16`, `2.498002e-16`] |
| tau_l | `6.035144e-04` at `h=0` [`-9.392123e-03`, `1.014368e-02`] | `-2.394785e-04` at `h=6` [`-3.446721e-03`, `2.963584e-03`] |
| tau_x | `4.811966e-04` at `h=0` [`-1.642952e-02`, `1.972241e-02`] | `-3.460759e-05` at `h=24` [`-5.619120e-04`, `4.931024e-04`] |

Figures:

- `code/bca_uncertainty_simulation/fvgq2020_preliminary/output/bca_lp_fin.png`
- `code/bca_uncertainty_simulation/fvgq2020_preliminary/output/bca_lp_macro.png`
- `code/bca_uncertainty_simulation/fvgq2020_preliminary/output/bca_girf_fin.png`
- `code/bca_uncertainty_simulation/fvgq2020_preliminary/output/bca_girf_macro.png`

## Initial read

1. **LP says the investment wedge is the main financial absorber.** In the
   ergodic-sample LP, `ue` loads most strongly on `tau_x`
   (`1.886355e-03` at `h=32`), with `tau_l` second
   (`9.012600e-04` at `h=15`). This is directionally consistent with a
   collateral or investment-distortion narrative.
2. **The pairwise GIRF is much weaker than the LP for `ue`.** The financial
   GIRF mean for `tau_x` is tiny (`-3.460759e-05` at `h=24`) and the band
   comfortably straddles zero. That LP-GIRF gap is itself evidence that the
   uncertainty-to-wedge mapping is highly nonlinear or state-dependent.
3. **Segmentation alone may already contaminate labor accounting.** Even though
   the strongest financial LP loading is on `tau_x`, `tau_l` is not negligible.
   That keeps open the interpretation that the two-agent consumption split
   leaks into what CKM reads as a labor wedge.
4. **Macro uncertainty is not a pure efficiency-wedge story either.** `uA`
   moves `log_A`, but also shows material LP responses in `tau_l` and `tau_x`,
   which suggests the accounting translation is redistributing uncertainty
   across multiple wedges rather than preserving a one-wedge mapping.

## Three questions for scholars

1. **Which wedge really absorbs `ue`?** Should we treat the LP result
   (`tau_x` strongest) or the GIRF result (financial effects near zero in the
   mean, with wide bands) as the more relevant object for the Section 7 design?
2. **How should we interpret the LP-GIRF disagreement?** Is the gap best read
   as higher-order nonlinearity in the accounting translation, or as evidence
   that the ergodic LP averages across states that the pairwise GIRF holds fixed?
3. **Does Section 7 need an additional labor channel?** If `tau_l` already
   appears here without working-capital frictions, Section 7 may amplify an
   existing labor-wedge signature rather than create one from scratch.

## Caveats

- The current code now compares True DGP (Inside-Dynare) wedges against the
  likelihood/Kalman recovery. Re-run the simulation and analysis after this
  migration before quoting the headline numbers above.
- FVGQ calibration is a U.S. business-cycle calibration; no Taiwan calibration
  is attempted here.
- The DGP contains capital utilization, but the prototype accounting system
  deliberately does not. Some recovered wedge movement is therefore an
  accounting projection of utilization.

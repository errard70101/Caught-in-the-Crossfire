# FVGQ 2020 Preliminary - Implementation Notes

## Source

`replicationRED.mod` was vendored from the RED code archive on 2026-04-24:

https://red-files-public.s3.amazonaws.com/codes/20/20-250/replicationRED.mod

Reference paper:

Fernandez-Villaverde, J., and Guerron-Quintana, P. (2020). "Uncertainty
Shocks and Business Cycle Research." *Review of Economic Dynamics*, 37,
118-166.

## Solve-only adaptation

The original RED file mixes the model definition with MATLAB-side postprocessing
that depends on an external pruning toolbox. The local
`dynare/fvgq2020_solveonly.mod` removes that postprocessing and relies on
Dynare 6.2 native `pruning` plus MATLAB-side `simult_` calls.

Relative to `replicationRED_vendored.mod`, the solve-only adaptation:

1. Removes the inline `addpath(...)` call to the external pruning toolbox.
2. Removes the MATLAB block after the original `stoch_simul` calls.
3. Replaces the solve block with a Dynare 6.2 native
   `stoch_simul(order=3, pruning, k_order_solver, periods=0, irf=0, ...)`.
4. Replaces `resid(1)` with `resid;` for Dynare 6.x syntax.
5. Adds `set_dynare_seed(20260424);` for reproducible solving.

No economic equations, state definitions, `initval` values, or parameter values
are changed. Baseline `@#define higherphi = 0` is preserved.

## Variable mapping to CKM inputs

| CKM input | FVGQ expression | Comment |
|-----------|-----------------|---------|
| `Y_t` | `y` | Aggregate output |
| `C_t` | `cspt` | `ifrac * ce + (1 - ifrac) * cw` |
| `I_t` | `ifrac * ivst` | Aggregate investment |
| `L_t` | `labor` | Aggregate hours |
| `K_t` | `k` | Aggregate capital |

The uncertainty shocks of interest are:

- `uA`: TFP stochastic-volatility innovation.
- `ue`: collateral-LTV stochastic-volatility innovation.

Ambient noise sources retained in simulation but not targeted for identification:

- `ud`: preference stochastic-volatility innovation.
- `ethet`, `eA`, `ed`: level shocks.

## Calibration provenance

The preliminary pipeline uses the exact FVGQ calibration in the vendored RED
file. The CKM prototype later maps those aggregates into a representative-agent
accounting system with:

- `alpha = 0.36`
- `beta = 0.994`
- `delta = 0.01625`
- `gamma = 2`
- `nu = 1`
- `chi` matched to FVGQ steady-state labor

This is a provisional accounting translation layer, not a Taiwan calibration.

## 2026-04-25 — LP/GIRF reporting and sensitivity additions

Following a design review of the preliminary results (see
`llm_logs/2026-04-25_lp_girf_design_diagnostic.md`), three additions were
made to the analysis layer **without re-running the simulation**:

1. **GIRF mean-precision band (revised same day)**: `run_bca_analysis.m`
   now also stores `se_mean = std(diffs)/sqrt(N)` and `ci_lo_mean /
   ci_hi_mean` (mean ± 1.96·SE) for every GIRF struct. The 5–95%
   pair-dispersion band is **omitted** from the plotted figures
   (`bca_girf_*.png`, `bca_girf_*_likelihood.png`, `bca_girf_compare_*.png`)
   because at the typical 26× width ratio it visually drowns out the mean
   line and conflates state-dependence with estimation precision. The
   q05/q95 dispersion data are still retained in `wedges_girf.mat` /
   `wedges_girf_likelihood.mat` for future regime-conditional analysis.

2. **DGP-precision LP figures**: `bca_lp_<ts>_dgp.png` plots the
   fixed-point LP with HAC SE on the full T=20000 ergodic path, providing
   a population-precision counterpart to the empirical-relevance T=400 MC
   bands in `bca_lp_<ts>_fixed.png`.

3. **Sensitivity LP without SV-state controls**: the contemporaneous SV
   states (`sigAt`, `sigdt`, `siget`) are mediators of the (uA, ue)
   shocks (by construction: `sigAt = rho*sigAt(-1) + scale*uA`).
   Including them as controls partials away the very channel of interest.
   New outputs: `lp_results_no_svctrl.mat`,
   `lp_results_likelihood_no_svctrl.mat`,
   `lp_no_svctrl_peak_comparison.csv`, and figure
   `bca_lp_<ts>_no_svctrl.png` overlays baseline vs. sensitivity.

Items 4-6 (larger SV shock size, standard GIRF differencing instead of
antithetic ±epsilon, regime-conditional GIRF) are listed as future work
in the same diagnostic memo.

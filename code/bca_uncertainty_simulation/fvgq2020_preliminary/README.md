# FVGQ 2020 Preliminary Simulated BCA

This subfolder hosts a preliminary simulated-BCA exercise driven by the
off-the-shelf DSGE model from Fernandez-Villaverde and Guerron-Quintana
(2020, *Review of Economic Dynamics*, "Uncertainty Shocks and Business
Cycle Research").

## Relation to the parent scaffold

This folder is intentionally isolated from the parent
`code/bca_uncertainty_simulation/` scaffold. The parent scaffold remains the
long-run Section 7 target. This preliminary exercise instead uses the FVGQ
two-agent entrepreneur-worker model to generate discussion-ready wedge
signatures before committing to the custom Section 7 implementation.

Authoritative design documents:

- `docs/superpowers/specs/2026-04-24-fvgq2020-preliminary-simulated-bca-design.md`
- `docs/superpowers/plans/2026-04-24-fvgq2020-preliminary-simulated-bca.md`

## Layout

- `dynare/replicationRED_vendored.mod`: unmodified copy of the RED archive
  replication file.
- `dynare/fvgq2020_solveonly.mod`: Dynare 6.2 solve-only adaptation that
  produces `oo_.dr` for MATLAB-driven simulation via `simult_`.
- `dynare/ckm_three_wedge_likelihood.mod`: linearized CKM-style prototype used
  for Kalman smoothing of `{z, tau_l, tau_x}`.
- `matlab/setup_paths.m`: Dynare path helper.
- `matlab/run_fvgq2020_simulation.m`: solve + warm-up + Experiment 1 + Experiment 2.
- `matlab/estimate_ckm_wedges.m`: four-wedge CKM extractor.
- `matlab/estimate_ckm_wedges_likelihood.m`: first-pass full-likelihood CKM
  smoother for Experiment 1.
- `matlab/local_projection.m`: local-projection helper.
- `matlab/monte_carlo_lp_bands.m`: repeated-simulation LP helper returning
  median responses and empirical 95% Monte Carlo bands.
- `matlab/run_bca_analysis.m`: CKM + LP + GIRF analysis driver plus CKM-style
  reporting-series export.
- `matlab/plot_bca_responses.m`: LP/GIRF plotting with explicit units plus
  CKM-style measured-wedge figures.
- `matlab/sanity_checks.m`: post-run invariants.

Generated output lives under `output/` and is ignored by git.

Additional likelihood outputs:

- `wedges_exp1_proxy.csv`
- `wedges_exp1_likelihood.csv`
- `wedges_exp1_report.csv`
- `wedges_exp1_likelihood_report.csv`
- `ckm_likelihood_exp1.mat`
- `lp_results_likelihood.mat`
- `lp_interval_comparison.csv`
- `lp_results_mc_fixed.mat`
- `lp_results_mc_fixed_summary.csv`
- `bca_lp_macro.png`, `bca_lp_fin.png` (main LP figures, now mapped to likelihood)
- `bca_lp_macro_fixed.png`, `bca_lp_fin_fixed.png`
- `bca_lp_macro_likelihood.png`, `bca_lp_fin_likelihood.png`
- `bca_lp_compare_macro.png`, `bca_lp_compare_fin.png`
- `bca_measured_wedges_fixed.png`
- `bca_measured_wedges_likelihood.png`
- `bca_wedges_exp1_compare.png`

## Run

From MATLAB:

```matlab
addpath('code/bca_uncertainty_simulation/fvgq2020_preliminary/matlab');
setup_paths;
run_fvgq2020_simulation;
run_bca_analysis;
plot_bca_responses;
sanity_checks;
```

Headless:

```bash
/Applications/MATLAB_R2025b.app/bin/matlab -batch \
  "addpath('code/bca_uncertainty_simulation/fvgq2020_preliminary/matlab'); \
   setup_paths; run_fvgq2020_simulation; run_bca_analysis; \
   plot_bca_responses; sanity_checks"
```

## LP figure convention

All LP figures use **transformed CKM-style log wedges** as dependent variables:

- `log_efficiency_wedge = log(A)`
- `log_labor_wedge = log(1 - tau_l)`
- `log_investment_wedge = log(1 / (1 + tau_x))`

The main exported LP figures, `bca_lp_macro.png` and `bca_lp_fin.png`, now show
the **likelihood-smoothed** responses. The fixed-point Monte Carlo versions are
still exported separately as `bca_lp_macro_fixed.png` and
`bca_lp_fin_fixed.png`.

The fixed-point LP figures use **Monte Carlo median responses and empirical
95% bands** computed from repeated simulated samples with:

- `B = 10000` repetitions
- `T = 400` periods per repetition

The older single-sample HAC/Newey-West LP output is still saved for reference
and for the likelihood-smoothed comparison figures.

## GIRF figure convention

The main GIRF figures now use **pair-level transformed wedge differences** for:

- `log_efficiency_wedge = log(A)`
- `log_labor_wedge = log(1 - tau_l)`
- `log_investment_wedge = log(1 / (1 + tau_x))`

The lower-right GIRF panel remains the raw `G/Y` resource residual as a
diagnostic because it does not have a CKM-style log transform analogue.
Raw GIRF outputs are still preserved in the saved `.mat` files.

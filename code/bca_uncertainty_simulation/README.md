# BCA Uncertainty Simulation

This folder is the executable scaffold for translating a TFP uncertainty shock
into CKM-style BCA wedges by simulation.

The maintained interpretation is:

1. The true data-generating model is a simple representative-agent RBC model.
2. The only structural second-moment shock is TFP uncertainty.
3. Synthetic data are generated from the true model.
4. CKM-style BCA is then used as a coordinate system to estimate which wedges
   represent the uncertainty shock.

This is not framed as "BCA misclassifies uncertainty." The point is that a
clean CKM wedge-equivalence theorem is hard to derive analytically for a
third-order uncertainty shock, so the wedge representation is obtained
operationally from simulated data.

The authoritative specification for the simulation design lives in
`theory/nk_uncertainty_bca/sections/07_simulation_based_bca.tex`.

## Files

- `dynare/ra_rbc_tfp_uncertainty.mod`: simple CRRA RBC model with TFP
  stochastic volatility. Solve-only (`periods=0, irf=0`); simulation is driven
  from MATLAB via `simult_`.
- `matlab/run_simulation.m`: three-phase pipeline -- Dynare solve, shared
  warm-up to SSS, Experiment 1 (ergodic sample), Experiment 2 (antithetic
  GIRF panel).
- `matlab/recover_direct_wedges_debug.m`: direct wedge recovery for debugging
  and sanity checks only. This is not the final CKM estimator.
- `matlab/estimate_ckm_wedges_skeleton.m`: explicit scaffold for the CKM-style
  state-space estimator.
- `matlab/plot_wedge_responses.m`: produces (A) debug wedge time series from
  Experiment 1 and (B) GIRF mean plus 5-95% cross-sectional band plots from
  Experiment 2.

Generated output goes to `output/` and is ignored by git:

- `experiment1_sample.csv`: T = 20,000 period ergodic sample (endogenous
  variables plus the driving `eps_a`, `eps_v` innovations).
- `experiment2_paths.mat`: `paths_base`, `paths_shock` arrays of shape
  `N x H x n_obs`, plus `var_names`, `v_idx`, `N`, `H`.
- `parameters.csv`: parameter dump from `M_.params`.
- `warmup_diagnostics.csv`: SSS-vs-DSS gap, tail-difference norm, and
  per-variable `SSS - DSS` entries.
- `simulated_workspace.mat`: consolidated MATLAB workspace (`M_`, `oo_`,
  `options_`, `sss_state`, experiment outputs, params).
- `exp1_debug_wedge_series.png`, `exp2_girf_bands.png`: plots.

## Model

The TFP process is written as

```text
a_t = rho_a a_{t-1} + sigma_a exp(v_t) eps_a,t
v_t = rho_v v_{t-1} + sigma_v eps_v,t
```

where `v_t` is the log-volatility state relative to its baseline level. This is
the same stochastic-volatility timing used in the dissertation code, with the
baseline TFP innovation scale written separately as `sigma_a`.

## Experimental design

See `theory/nk_uncertainty_bca/sections/07_simulation_based_bca.tex` for the
authoritative specification. The pipeline has three phases:

1. **Shared warm-up to SSS.** Starting from the deterministic steady state,
   iterate the third-order pruned policy functions forward for
   `T_wu = 50,000` periods with all innovations set to zero. The terminal
   state is the numerical stochastic steady state (SSS). Convergence is
   verified against the state 1,000 periods earlier.
2. **Experiment 1: ergodic sample.** From SSS, simulate one path of length
   `T = 20,000` with iid standard-normal innovations. This feeds local
   projections of BCA wedges on `eps_v`.
3. **Experiment 2: antithetic GIRF panel.** From SSS, generate `N = 1,000`
   innovation sequences of length `H = 60`. For each sequence, run two
   matched paths that differ only in the period-1 `eps_v` realisation
   (0 for baseline, 1 for shocked). Cross-path differences averaged across
   `N` deliver the GIRF; 5-95% quantiles deliver cross-sectional bands.

Both experiments seed RNGs deterministically so that rerunning the pipeline
reproduces identical output.

## Run

### Local environment (this machine)

- MATLAB: `/Applications/MATLAB_R2025b.app/bin/matlab` (R2025b; R2024b also
  installed).
- Dynare: `/Applications/Dynare/6.2-arm64/` (6.2, Apple Silicon build). The
  MATLAB interface lives in `/Applications/Dynare/6.2-arm64/matlab`.

From MATLAB:

```matlab
addpath('/Applications/Dynare/6.2-arm64/matlab');
cd(fullfile(getenv('HOME'), ...
   'Documents/GitHub/Caught-in-the-Crossfire/code/bca_uncertainty_simulation/matlab'));
run_simulation
plot_wedge_responses
```

Or headless from the shell:

```bash
/Applications/MATLAB_R2025b.app/bin/matlab -batch \
  "addpath('/Applications/Dynare/6.2-arm64/matlab'); \
   cd('code/bca_uncertainty_simulation/matlab'); run_simulation"
```

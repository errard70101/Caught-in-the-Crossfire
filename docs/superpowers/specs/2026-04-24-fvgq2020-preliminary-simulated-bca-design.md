# Design Spec: FVGQ 2020 Preliminary Simulated BCA

**Date**: 2026-04-24
**Status**: Brainstorming complete, awaiting user review before writing implementation plan
**Project**: Caught in the Crossfire — Year 2 theoretical module
**Related**:
- `theory/rbc_uncertainty_bca/sections/07_simulation_based_bca.tex` (long-term target, unchanged by this spec)
- `code/bca_uncertainty_simulation/` (existing scaffold for §7, unchanged by this spec)
- `llm_logs/2026-04-24_simulated_bca_vs_dsge_irf.md` (narrative rationale)
- External plan: `/Users/linshih-yang/.gemini/tmp/caught-in-the-crossfire/e19260f7-ddd0-4fe5-a83f-3089a0808e01/plans/2026-04-24-fvgq2020-preliminary-bca-plan.md`

## 1. Objective

Produce a **preliminary set of simulated Business Cycle Accounting (BCA) results** using the off-the-shelf DSGE model from Fernández-Villaverde and Guerrón-Quintana (2020, *Review of Economic Dynamics*, "Uncertainty Shocks and Business Cycle Research") — hereafter FVGQ (2020) — in order to generate a concrete artifact that can be circulated to scholars for feedback **before** investing weeks developing the custom representative-agent hybrid model described in `theory/rbc_uncertainty_bca/sections/07_simulation_based_bca.tex` (hereafter §7).

The goal is velocity, not completeness. Any substantive model change (extension to working-capital friction, Taiwan calibration, open-economy block) waits on scholar feedback.

## 2. Scope and Non-Goals

**In scope**:
- Acquire and adapt the RED replication package for FVGQ (2020).
- Drive Experiments 1 (ergodic sample + local projections) and 2 (antithetic-pairs GIRF) over both `uA` (TFP SV) and `ue` (collateral SV) shocks, mirroring §7's two-experiment design.
- Estimate the four canonical CKM (2007) wedges — efficiency `A`, government `G/Y`, labor `τ_ℓ`, investment `τ_x` — on the simulated aggregates `(Y, C, I, L, K)`.
- Produce figures and a short memo for scholar discussion.

**Not in scope (explicit)**:
- Modifying §7 or the existing `code/bca_uncertainty_simulation/` scaffold in any way.
- Changing FVGQ's economic structure or calibration values.
- Taiwan data or open-economy extensions.
- Working-capital friction (φ process from CGK 2024).
- Shocking preference SV (`ud`); it stays as an ambient noise source but is not an identification target.
- Anything that would delay the preliminary memo beyond ~5 working days.

## 3. Narrative Correction (Required Before Writing Memo)

The FVGQ (2020) Section 5 model — confirmed by reading `replicationRED.mod` from the RED code archive — is a **two-agent** framework: 6% representative entrepreneurs + 94% representative workers, no Krusell–Smith distribution dynamics. Entrepreneurs face a stochastic-LTV collateral constraint; workers supply labor frictionlessly.

This requires **narrative correction** across project documents (to be applied in a follow-up pass, not in this spec's implementation):

- **Old framing** (in `llm_logs/2026-04-24_simulated_bca_vs_dsge_irf.md` Insight 3): "micro-level heterogeneous financial friction, when aggregated into macroeconomic data, gets misattributed…"
- **New framing**: "a **financially-segmented two-agent economy** — entrepreneurs bound by the collateral constraint, workers consuming out of wages — projects its segmentation gap `C_t = 0.06·c^e_t + 0.94·c^w_t` onto the CKM single-representative-agent prototype, where the gap surfaces as specific wedge signatures."

This framing is actually *more coherent* with §7 (which is also a representative/unified-agent structure), and preserves the three insights in the rationale log with only terminological edits.

## 4. Folder Layout

```
code/bca_uncertainty_simulation/
├── (existing) dynare/, matlab/, output/, README.md    ← §7 long-term target, UNCHANGED
└── fvgq2020_preliminary/                              ← NEW
    ├── README.md                                      ← Purpose, relation to §7, run instructions
    ├── NOTES.md                                       ← Calibration provenance, deviations from FVGQ original
    ├── dynare/
    │   ├── replicationRED_vendored.mod                ← Unmodified copy from RED archive
    │   └── fvgq2020_solveonly.mod                     ← Our adapted solve-only version
    ├── matlab/
    │   ├── setup_paths.m                              ← Dynare 6.2 path (no external pruning toolbox needed)
    │   ├── run_fvgq2020_simulation.m                  ← Phase 1–3 driver, parallels existing run_simulation.m
    │   ├── estimate_ckm_wedges.m                      ← Four-wedge CKM estimator
    │   ├── local_projection.m                         ← Experiment 1 LP helper
    │   └── plot_bca_responses.m                       ← LP + GIRF figures with bands
    └── output/                                        ← .gitignore'd
        ├── experiment1_sample.csv
        ├── experiment2_paths.mat
        ├── parameters.csv
        ├── warmup_diagnostics.csv
        ├── wedges_lp.csv
        ├── wedges_girf.mat
        └── *.png
```

Principle: mirror the existing §7 scaffold's file naming and three-phase structure as closely as possible so code review can proceed by analogy.

## 5. `.mod` File Adaptation

`replicationRED.mod` from the RED archive mixes model definition with MATLAB-side IRF construction (~80 lines of post-`stoch_simul` scripting) and relies on the Andreasen–Fernández-Villaverde–Rubio-Ramírez pruning toolbox. We adapt it to match the solve-only philosophy of the existing scaffold:

1. **Vendor unchanged copy** as `dynare/replicationRED_vendored.mod` for provenance.
2. **Create `dynare/fvgq2020_solveonly.mod`**, derived by:
   - Removing `addpath(...)` line (Dynare 6.2 does not accept path manipulation inside `.mod` files; paths are set in `setup_paths.m` instead).
   - Removing all MATLAB commands after `stoch_simul` (the `outDynare = RunDynarePruning(...)` block and IRF matrix construction, approximately lines 162–240 of the original).
   - Replacing the solve block with Dynare 6.2 native:
     ```
     stoch_simul(order=3, pruning, periods=0, irf=0, k_order_solver,
                 nomoments, noprint);
     ```
     This produces only `oo_.dr`. Experiments 1/2 call `simult_(M_, options_, y0, oo_.dr, ex, 3)` from MATLAB, identical to the pattern in the existing `run_simulation.m`.
   - Keeping `@#define higherphi = 0` as the baseline.
   - Preserving all model equations, parameter values, and `initval` block unchanged.
3. **Dynare 6.2 syntax review** — expected compatibility with low risk, but confirm:
   - `steady(solve_algo=3)` (supported).
   - `resid(1)` may need to become `resid;` in 6.2 — fix if so.
   - `@#if / @#endif` preprocessor directives (supported).
   - `var`, `varexo`, `parameters`, `shocks`, `model;` blocks (unchanged syntax).

**No external pruning toolbox is installed**: `stoch_simul(..., pruning)` + `simult_` with `iorder=3` natively support third-order pruning via `k_order_simul` (confirmed against `/Applications/Dynare/6.2-arm64/matlab/stochastic_solver/simult_.m` line 46 onward).

## 6. Experiment Design

Aligned 1:1 with §7 experimental structure, substituting FVGQ shock names:

| §7 concept | FVGQ shock | Role |
|------------|-----------|------|
| ε_{VA,t} (Macro uncertainty) | `uA` | TFP SV innovation — targeted |
| ε_{VF,t} (Financial uncertainty) | `ue` | Collateral-LTV SV innovation — targeted |
| — | `ud` | Preference SV — ambient noise only |
| — | `eA`, `ed`, `ethet` | Level shocks — ambient noise only |

### 6.1 Shared warm-up

Start from the deterministic steady state. Iterate pruned third-order policy functions forward for `T_wu = 50,000` periods with all six innovations set to zero. Record the terminal state as the numerical Stochastic Steady State (SSS). Verify convergence by comparing the state at `T_wu` against the state at `T_wu - 1,000`.

### 6.2 Experiment 1 (ergodic sample + local projections)

From SSS, simulate one path of length `T = 20,000` with all six innovations drawn iid N(0,1). Apply the CKM estimator (§7) to the aggregate series `(Y, C, I, L, K)`, recovering `{ŝ_t}_{t=1}^T` where `s_t = (log A_t, G_t/Y_t, τ_{ℓ,t}, τ_{x,t})'`.

Estimate local projections for `j ∈ {A, G, ℓ, x}` and horizons `h ∈ {0, 1, …, H}` with `H = 60` (matched to the GIRF horizon in §6.3 for clean cross-validation):

```
ŝ_{j,t+h} = α_{j,h} + β^macro_{j,h} · uA_t + β^fin_{j,h} · ue_t + Γ'_{j,h} · Z_t + u_{j,t+h}
```

where `Z_t` includes level shocks `{eA, ed, ethet}`, lagged SV states `{sigAt, siget, sigdt}`, and lagged wedges.

### 6.3 Experiment 2 (antithetic-pairs GIRF)

From SSS, draw `N = 1,000` innovation sequences of length `H = 60`. For each shock of interest, build two matched paths differing only in `ε_0`:

- **Financial GIRF**: baseline `ue_0 = 0` vs. shocked `ue_0 = 1`; all other innovations identical within the pair.
- **Macro GIRF**: baseline `uA_0 = 0` vs. shocked `uA_0 = 1`; analogous.

For each wedge `j`:

```
GIRF^fin_{j,h} = (1/N) Σ_i [ ŝ^{(i), shock}_{j,h} - ŝ^{(i), base}_{j,h} ]
```

Cross-sectional 5–95% bands come from the within-pair difference distribution.

### 6.4 Cross-validation

Compare `β_{j,h}` (LP, first-order projection) against `GIRF_{j,h}` (nonlinear pair differencing). Disagreement quantifies higher-order nonlinearity in the uncertainty-to-wedge mapping — this is Insight 1 from the rationale log.

## 7. CKM Wedge Estimation Details

### 7.1 Aggregate inputs

| Wedge input | FVGQ variable | Notes |
|-------------|---------------|-------|
| `Y_t` | `y` | Aggregate output |
| `C_t` | `cspt` (= `ifrac·ce + (1-ifrac)·cw`) | Population-weighted consumption |
| `I_t` | `ifrac · ivst` | **Critical**: `ivst` is per-entrepreneur; resource constraint (`replicationRED.mod` line 66) shows aggregate investment = `ifrac · ivst` |
| `L_t` | `labor` | Already aggregate (per-worker hours × worker mass absorbed into equations) |
| `K_t` | `k` | Aggregate capital |

Utilization `utilt` is **deliberately not fed** to the CKM estimator: CKM (2007) prototype has no utilization margin, so letting that contribution spill into the wedges is one channel of Insight 1.

### 7.2 Estimator

Reuse the VAR(1) state-space form from `estimate_ckm_wedges_skeleton.m`:

```
s_{t+1} = P_0 + P · s_t + ε_{t+1}
s_t = (log A_t, G_t/Y_t, τ_{ℓ,t}, τ_{x,t})'
```

### 7.3 Tripwire diagnostic

FVGQ has no government sector, so the resource identity gives `Y = C + I`. The recovered `Ĝ_t/Y_t` series should be numerically near zero. Any material departure signals an aggregation error — most likely the `ifrac` multiplier on `ivst`. This is a **mandatory sanity check** before interpreting `τ_ℓ` or `τ_x`.

## 8. Deliverables and Timeline

| # | Deliverable | Content | Work days |
|---|------------|---------|-----------|
| D1 | Pipeline runs | `run_fvgq2020_simulation.m` produces `experiment1_sample.csv` and `experiment2_paths.mat`; warm-up convergence verified | 1 |
| D2 | CKM wedges recovered | Four-wedge series from Experiment 1 sample; `Ĝ_t/Y_t` near zero confirmed | 1 |
| D3 | Experiment 1 LP results | `β^macro_{j,h}` and `β^fin_{j,h}` with 95% CIs, table + figures | 1 |
| D4 | Experiment 2 GIRF results | `GIRF^fin_{j,h}` and `GIRF^macro_{j,h}` with 5–95% bands, by shock × wedge | 1 |
| D5 | Scholar-discussion memo | `llm_logs/YYYY-MM-DD_fvgq2020_preliminary_results.md` addressing: (a) which wedge absorbs `ue`? (b) how large is LP–GIRF disagreement? (c) do results support §7 direction? | 1 |

**Total**: 4–5 working days (excludes scholar-feedback iteration).

## 9. Dependencies

- **MATLAB**: R2024b or R2025b (both installed locally at `/Applications/MATLAB_R2024b.app` / `/Applications/MATLAB_R2025b.app`).
- **Dynare**: 6.2-arm64 at `/Applications/Dynare/6.2-arm64/` (native `pruning` support confirmed).
- **No external pruning toolbox** required.
- **FVGQ replication files** already downloaded to `/tmp/fvgq2020/`; will be vendored into `fvgq2020_preliminary/dynare/`.

## 10. Risks and Mitigations

| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| Dynare 6.2 syntax drift from 4.5 breaks `.mod` compile | Low-medium | Run `dynare fvgq2020_solveonly.mod` early in D1; fix line by line (expected only `resid` syntax). |
| FVGQ SSS far from DSS causes `simult_` to explode under heavy pruning | Low | Existing `run_simulation.m` already solved this; reuse warm-up convergence check. |
| `ifrac` misapplied to `ivst` breaks resource identity | Medium | `Ĝ_t/Y_t` tripwire (§7.3) catches this before memo stage. |
| Preference SV `ud` contaminates LP identification | Low | Include lagged SV states `{sigAt, sigdt, siget}` in `Z_t` as controls. |
| Results contradict §7 direction (e.g., only `τ_x` moves, not `τ_ℓ`) | Unknown — this *is* the research output | The contradiction itself is a scholar-discussion item, not a failure. |

## 11. Post-Preliminary Branch Points

Once scholars feed back, the paths forward are:

- **(A)** If FVGQ-based signature is clear and well-received → proceed with §7's RA+LWZ/CGK implementation to refine and extend.
- **(B)** If scholars request a different DGP → revise §7, rerun against preliminary as benchmark.
- **(C)** If the BCA translation itself is challenged (e.g., CKM assumptions invalidated by uncertainty shocks) → pivot to Insight-1-focused narrative (nonlinear-distortion diagnostic) and reconsider §7 scope.

This spec does not commit to any of (A)/(B)/(C); the purpose is to enable the decision, not pre-judge it.

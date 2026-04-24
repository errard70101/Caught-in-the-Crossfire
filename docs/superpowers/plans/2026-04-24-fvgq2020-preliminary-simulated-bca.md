# FVGQ 2020 Preliminary Simulated BCA Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce a preliminary set of simulated Business Cycle Accounting (BCA) results by driving the FVGQ (2020, *Review of Economic Dynamics*) DSGE model, adapted to Dynare 6.2 native pruning, through a three-phase simulation pipeline and a four-wedge CKM (2007) extraction — delivering a scholar-discussion memo within ~5 working days.

**Architecture:** A new isolated subfolder `code/bca_uncertainty_simulation/fvgq2020_preliminary/` with its own `.mod` file, MATLAB driver, CKM estimator, local-projection helper, and plotting module. Mirrors the existing §7 scaffold's file layout and `simult_`-based `(solve → warm-up → Experiment 1 → Experiment 2)` pipeline 1:1 so review can proceed by analogy. The existing scaffold and `theory/nk_uncertainty_bca/sections/07_simulation_based_bca.tex` are not modified.

**Tech Stack:** MATLAB R2024b/R2025b · Dynare 6.2-arm64 (native `pruning` + `simult_` for order=3) · No external pruning toolbox.

**Spec:** [`docs/superpowers/specs/2026-04-24-fvgq2020-preliminary-simulated-bca-design.md`](../specs/2026-04-24-fvgq2020-preliminary-simulated-bca-design.md)

---

## Overall File Map

| Path | Create / Modify | Role |
|------|-----------------|------|
| `.gitignore` | Modify | Ignore `code/bca_uncertainty_simulation/fvgq2020_preliminary/output/` |
| `code/bca_uncertainty_simulation/fvgq2020_preliminary/README.md` | Create | Purpose + run instructions |
| `code/bca_uncertainty_simulation/fvgq2020_preliminary/NOTES.md` | Create | Calibration provenance + deviations from RED archive |
| `code/bca_uncertainty_simulation/fvgq2020_preliminary/dynare/replicationRED_vendored.mod` | Create | Unmodified copy of RED archive `.mod` |
| `code/bca_uncertainty_simulation/fvgq2020_preliminary/dynare/fvgq2020_solveonly.mod` | Create | Adapted solve-only `.mod` for Dynare 6.2 |
| `code/bca_uncertainty_simulation/fvgq2020_preliminary/matlab/setup_paths.m` | Create | Add Dynare to MATLAB path |
| `code/bca_uncertainty_simulation/fvgq2020_preliminary/matlab/run_fvgq2020_simulation.m` | Create | Three-phase driver (solve + warm-up + Exp1 + Exp2) |
| `code/bca_uncertainty_simulation/fvgq2020_preliminary/matlab/estimate_ckm_wedges.m` | Create | Four-wedge CKM estimator |
| `code/bca_uncertainty_simulation/fvgq2020_preliminary/matlab/local_projection.m` | Create | Experiment 1 LP estimator |
| `code/bca_uncertainty_simulation/fvgq2020_preliminary/matlab/run_bca_analysis.m` | Create | Apply CKM + LP + GIRF to simulation outputs |
| `code/bca_uncertainty_simulation/fvgq2020_preliminary/matlab/plot_bca_responses.m` | Create | LP and GIRF figures |
| `code/bca_uncertainty_simulation/fvgq2020_preliminary/matlab/sanity_checks.m` | Create | Resource identity + SSS convergence assertions |
| `code/bca_uncertainty_simulation/fvgq2020_preliminary/output/*` | Generated | CSV/MAT/PNG outputs (gitignored) |
| `llm_logs/2026-04-XX_fvgq2020_preliminary_results.md` | Create (last task) | Scholar-discussion memo |

**Non-goals (from spec §2):** no modification of `code/bca_uncertainty_simulation/{dynare,matlab}/*` or `theory/nk_uncertainty_bca/sections/07_simulation_based_bca.tex`, no change to FVGQ's economic structure or parameter values, no Taiwan data, no working-capital friction.

---

## Task 1: Scaffold folder and vendor RED replication file

**Files:**
- Create: `code/bca_uncertainty_simulation/fvgq2020_preliminary/README.md`
- Create: `code/bca_uncertainty_simulation/fvgq2020_preliminary/NOTES.md`
- Create: `code/bca_uncertainty_simulation/fvgq2020_preliminary/dynare/replicationRED_vendored.mod`
- Create: `code/bca_uncertainty_simulation/fvgq2020_preliminary/matlab/.gitkeep`
- Create: `code/bca_uncertainty_simulation/fvgq2020_preliminary/output/.gitkeep`
- Modify: `.gitignore`

- [ ] **Step 1.1: Create subfolder tree**

```bash
mkdir -p code/bca_uncertainty_simulation/fvgq2020_preliminary/dynare
mkdir -p code/bca_uncertainty_simulation/fvgq2020_preliminary/matlab
mkdir -p code/bca_uncertainty_simulation/fvgq2020_preliminary/output
touch code/bca_uncertainty_simulation/fvgq2020_preliminary/matlab/.gitkeep
touch code/bca_uncertainty_simulation/fvgq2020_preliminary/output/.gitkeep
```

- [ ] **Step 1.2: Vendor the RED archive `.mod` file (already downloaded to `/tmp/fvgq2020/`)**

```bash
cp /tmp/fvgq2020/replicationRED.mod \
   code/bca_uncertainty_simulation/fvgq2020_preliminary/dynare/replicationRED_vendored.mod
```

If `/tmp/fvgq2020/replicationRED.mod` no longer exists, re-download:

```bash
mkdir -p /tmp/fvgq2020
curl -sL "https://red-files-public.s3.amazonaws.com/codes/20/20-250/replicationRED.mod" \
  -o code/bca_uncertainty_simulation/fvgq2020_preliminary/dynare/replicationRED_vendored.mod
```

Verify file is 240 lines (from RED archive):

```bash
wc -l code/bca_uncertainty_simulation/fvgq2020_preliminary/dynare/replicationRED_vendored.mod
```

Expected: `240 code/bca_uncertainty_simulation/fvgq2020_preliminary/dynare/replicationRED_vendored.mod`

- [ ] **Step 1.3: Write README.md**

File: `code/bca_uncertainty_simulation/fvgq2020_preliminary/README.md`

```markdown
# FVGQ 2020 Preliminary Simulated BCA

A parallel, preliminary BCA simulation driven by the off-the-shelf model from
Fernández-Villaverde & Guerrón-Quintana (2020, *Review of Economic Dynamics*,
"Uncertainty Shocks and Business Cycle Research").

## Relation to parent scaffold

This subfolder is **independent** of the parent `code/bca_uncertainty_simulation/`
scaffold. The parent is the long-term §7 target (representative-agent RBC with
unified collateral constraint, Liu–Wang–Zha 2013 + Chatterjee–Gunawan–Kohn 2024).
This preliminary uses FVGQ's off-the-shelf two-agent entrepreneur-worker model
to produce discussion-ready simulated BCA results before committing to the §7
implementation effort.

Authoritative spec:
`docs/superpowers/specs/2026-04-24-fvgq2020-preliminary-simulated-bca-design.md`.

## Files

- `dynare/replicationRED_vendored.mod`: unmodified copy of the RED archive
  replication file (https://red-files-public.s3.amazonaws.com/codes/20/20-250/).
- `dynare/fvgq2020_solveonly.mod`: adapted version that only produces the
  decision rule (`oo_.dr`); Experiments 1/2 run from MATLAB via `simult_`.
- `matlab/setup_paths.m`: one-shot MATLAB path setup.
- `matlab/run_fvgq2020_simulation.m`: three-phase pipeline.
- `matlab/estimate_ckm_wedges.m`: four-wedge CKM (2007) extractor.
- `matlab/local_projection.m`: Experiment 1 LP helper.
- `matlab/run_bca_analysis.m`: CKM + LP + GIRF driver.
- `matlab/plot_bca_responses.m`: figures.
- `matlab/sanity_checks.m`: resource-identity and convergence assertions.

Generated output lives in `output/` (gitignored):

- `experiment1_sample.csv`
- `experiment2_paths.mat`
- `parameters.csv`
- `warmup_diagnostics.csv`
- `wedges_exp1.csv`, `wedges_girf.mat`
- `lp_results.mat`
- `bca_lp_*.png`, `bca_girf_*.png`

## Run

From MATLAB:

```matlab
addpath('code/bca_uncertainty_simulation/fvgq2020_preliminary/matlab');
setup_paths;
run_fvgq2020_simulation;
run_bca_analysis;
plot_bca_responses;
```

Or headless:

```bash
/Applications/MATLAB_R2025b.app/bin/matlab -batch \
  "addpath('code/bca_uncertainty_simulation/fvgq2020_preliminary/matlab'); \
   setup_paths; run_fvgq2020_simulation; run_bca_analysis; plot_bca_responses"
```
```

- [ ] **Step 1.4: Write NOTES.md**

File: `code/bca_uncertainty_simulation/fvgq2020_preliminary/NOTES.md`

```markdown
# FVGQ 2020 Preliminary — Implementation Notes

## Source

`replicationRED.mod` retrieved 2026-04-24 from:
https://red-files-public.s3.amazonaws.com/codes/20/20-250/replicationRED.mod
(RED code archive 20-250.)

Original paper:
Fernández-Villaverde, J., & Guerrón-Quintana, P. (2020). "Uncertainty shocks
and business cycle research." *Review of Economic Dynamics*, 37, 118–166.

## Deviations from the original `.mod`

The original file mixes model definition with ~80 lines of MATLAB post-
processing that depends on the Andreasen–Fernández-Villaverde–Rubio-Ramírez
pruning toolbox. Our `fvgq2020_solveonly.mod` strips post-processing and
relies on Dynare 6.2's native `pruning` option, which is evaluated inside
`simult_` via `k_order_simul` (see
`/Applications/Dynare/6.2-arm64/matlab/stochastic_solver/simult_.m:46`).

Specific edits relative to `replicationRED_vendored.mod`:

1. Removed the inline `addpath(...)` to the external pruning toolbox (line 10).
2. Removed all MATLAB commands after the `stoch_simul(order=3)` line
   (approx. lines 162–240), which build IRFs and `yirf` matrices.
3. Replaced the `stoch_simul(order = 3, irf = 0)` call with:
   `stoch_simul(order=3, pruning, k_order_solver, periods=0, irf=0, nograph, noprint, nomoments, nofunctions, nocorr);`
4. Replaced `resid(1)` with `resid;` (Dynare 6.x syntax).
5. Added `set_dynare_seed(20260424);` to mirror the parent scaffold.

No economic-structural or parameter changes were made. The baseline
(`@#define higherphi = 0`) configuration is used.

## Variable and shock mapping

Aggregate inputs to CKM estimator (derived in `run_fvgq2020_simulation.m`):

| CKM input | FVGQ expression | Comment |
|-----------|-----------------|---------|
| `Y_t` | `y` | Aggregate output |
| `C_t` | `cspt` | = `ifrac*ce + (1-ifrac)*cw` |
| `I_t` | `ifrac * ivst` | Aggregate investment (resource constraint line 66) |
| `L_t` | `labor` | Aggregate hours |
| `K_t` | `k` | Aggregate capital |

Uncertainty innovations of interest:

- `uA` = TFP stochastic-volatility innovation (Macro uncertainty target)
- `ue` = collateral-LTV stochastic-volatility innovation (Financial uncertainty target)
- `ud` = preference stochastic-volatility innovation (ambient noise only)
- `eA`, `ed`, `ethet` = level shocks (ambient noise only)

## Calibration: unchanged from RED archive

| Parameter | Value | Parameter | Value |
|-----------|-------|-----------|-------|
| `beta` | 0.994 | `rhothet` | 0.95 |
| `ifrac` | 0.06 | `rhoA` | 0.95 |
| `alpha` | 0.36 | `rhod` | 0.95 |
| `delt0` | 0.01625 | `rhosigA` | 0.75 |
| `ssPhi` | 0.09539948 | `rhosigd` | 0.75 |
| `delt1` | 0.01309569 | `rhosige` | 0.75 |
| `rho` | 2 | `sigA` | log(0.007) |
| `eta` | 1.524829 | `sigd` | log(0.13/4) |
| `gss` | 1.00 | `sige` | log(0.033/4) |
```

- [ ] **Step 1.5: Add `.gitignore` entry for output folder**

Modify `.gitignore` — append to the end:

```
# FVGQ 2020 preliminary simulation outputs
code/bca_uncertainty_simulation/fvgq2020_preliminary/output/**
!code/bca_uncertainty_simulation/fvgq2020_preliminary/output/.gitkeep
```

- [ ] **Step 1.6: Verify folder structure**

Run:

```bash
find code/bca_uncertainty_simulation/fvgq2020_preliminary -type f | sort
```

Expected output (exactly these six files):

```
code/bca_uncertainty_simulation/fvgq2020_preliminary/NOTES.md
code/bca_uncertainty_simulation/fvgq2020_preliminary/README.md
code/bca_uncertainty_simulation/fvgq2020_preliminary/dynare/replicationRED_vendored.mod
code/bca_uncertainty_simulation/fvgq2020_preliminary/matlab/.gitkeep
code/bca_uncertainty_simulation/fvgq2020_preliminary/output/.gitkeep
```

(Five files; the `find` command above also shows `.gitkeep` entries.)

- [ ] **Step 1.7: Commit**

```bash
git add .gitignore code/bca_uncertainty_simulation/fvgq2020_preliminary/
git commit -m "$(cat <<'EOF'
feat(bca-sim): scaffold FVGQ 2020 preliminary subfolder

Creates isolated subfolder under code/bca_uncertainty_simulation/ for the
FVGQ (2020, RED) preliminary simulated BCA exercise. Vendors the RED archive
replication file (replicationRED_vendored.mod, unchanged from source),
documents the provenance and planned adaptations in NOTES.md, and provides
a run README. Output folder is gitignored with a .gitkeep placeholder.

Does not touch parent code/bca_uncertainty_simulation/ or §7.

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>
EOF
)"
```

---

## Task 2: Write adapted `fvgq2020_solveonly.mod`

**Files:**
- Create: `code/bca_uncertainty_simulation/fvgq2020_preliminary/dynare/fvgq2020_solveonly.mod`

**Goal:** A Dynare 6.2-compatible solve-only `.mod` that produces `oo_.dr` via third-order pruning, with all model structure and calibration identical to `replicationRED_vendored.mod`.

- [ ] **Step 2.1: Create `fvgq2020_solveonly.mod`**

File content (complete, starts from scratch to avoid line-range confusion):

```text
// FVGQ 2020 preliminary -- solve-only adaptation for Dynare 6.2.
//
// Source: replicationRED.mod from RED code archive 20-250.
// Adaptations (see NOTES.md for rationale):
//   * Removed external pruning-toolbox addpath (line 10 of source).
//   * Removed post-stoch_simul MATLAB block (lines 162-240 of source).
//   * Replaced stoch_simul call with Dynare 6.2 native pruning.
//   * Replaced resid(1) with resid; for Dynare 6.x syntax.
//   * Added set_dynare_seed(20260424) to match parent scaffold.
//
// Model structure and calibration are unchanged from the source.

@#define higherphi = 0

var ce cw ivst q k labor y cspt phi utilt delt deltp demt lambdat At sigAt sigdt thetat siget;
varexo ethet eA ed uA ud ue;

parameters beta ifrac alpha delt0 delt1 delt2 ssPhi theta rho eta gss
           rhothet rhoA rhod sigA sigd sige rhosigA rhosigd rhosige
           metaA metad metae;

beta = 0.994;
ifrac = 0.06;
alpha = 0.36;
delt0 = 0.01625;

@#if higherphi == 0
ssPhi = 0.09539948379;
delt1 = 0.01309569021;
delt2 = 0.33*delt1;
@#else
ssPhi = 0.2;
delt1 = 0.02052077068;
delt2 = 0.33*delt1;
@#endif

theta = ssPhi;
rho = 2;
eta = 1.524829433;
gss = 1.00;

rhothet = 0.95;
rhoA  = 0.95;
sigA  = log(0.007);
sige  = log(0.033/4);
rhod  = 0.95;
sigd  = log(0.13/4);
rhosigA = 0.75;
rhosigd = 0.75;
rhosige = 0.75;
metaA = (log(2)/(1-rhosigA^2)^0.5);
metad = (log(2)/(1-rhosigd^2)^0.5);
metae = (log(2)/(1-rhosige^2)^0.5);

model;

((ce))^(-rho) = (1 + ((q)-1)/(1-thetat*(q)))*((cw))^(-rho)*(1-(labor))^(eta*(1-rho));

eta*(cw)/(1-(labor)) = (1-alpha)*((y))/((1-ifrac)*(labor));

(q) = beta*demt(+1)/demt*(gss*(cw(+1))/(cw))^(-rho)*((1-(labor(+1)))/(1-(labor)))^(eta*(1-rho))
        *(alpha*((y(+1)))/(utilt(+1)*k) + (q(+1))*(1-delt)
        + ifrac*(((q(+1))-1)/(1-thetat(+1)*(q(+1))))*( alpha*((y(+1)))/(utilt(+1)*k) + (q(+1))*(1-delt)*(phi(+1)) ) );

(ce) + (1 - thetat*(q))*(ivst) = alpha*(y) + (q)*(phi)*(1-delt)*(k(-1));

(y) = (At)*((utilt*k(-1)))^alpha*((1-ifrac)*(labor))^(1-alpha);

(y) = ifrac*(ce) + (1 - ifrac)*(cw) + ifrac*(ivst);

(k) = (1 - delt)*(k(-1)) + ifrac*(ivst);

phi = ssPhi;

thetat = (1-rhothet)*(theta) + rhothet*thetat(-1) + exp(siget)*ethet;

At = (1 - rhoA) + rhoA*At(-1) + exp(sigAt)*eA;

demt = 1 - rhod + rhod*demt(-1) + exp(sigdt)*ed;

(sigAt) = (1-rhosigA)*(sigA) + rhosigA*(sigAt(-1)) + (1-rhosigA^2)^(0.5)*metaA*uA;

(sigdt) = (1-rhosigd)*(sigd) + rhosigd*(sigdt(-1)) + (1-rhosigd^2)^(0.5)*metad*ud;

(siget) = (1-rhosige)*(sige) + rhosige*(siget(-1)) + (1-rhosige^2)^(0.5)*metae*ue;

(cspt) = ifrac*(ce) + (1-ifrac)*(cw);

alpha*(y)/(utilt*k(-1)) - (q)*deltp + ((q)-1)/(1-thetat*(q))*ifrac*(alpha*(y)/(utilt*k(-1)) - phi*(q)*deltp) = 0;

delt = delt0 + delt1*(utilt - 1) + delt2/2*(utilt - 1)^2;

deltp = delt1 + delt2*(utilt - 1);

(lambdat) = ((q) - 1)/(1 - (q)*theta);

end;

shocks;
var ethet = 1;
var eA = 1;
var ed = 1;
var uA = 1;
var ud = 1;
var ue = 1;
end;

initval;
@#if higherphi == 0
ce = 0.5913719745;
cw = 1.101401063;
ivst = 5.087186128;
k = 18.78345647;
q = 2.26297;
y = 1.422989127;
labor = 0.3546099291;
phi = ssPhi;
cspt = 1.070799318;
utilt = 1;
delt = delt0;
deltp = delt1;
demt = 1;
lambdat = ((1.568268059) - 1)/(1-(1.568268059)*theta);
At = 1;
thetat = theta;
sigAt = sigA;
sigdt = sigd;
siget = sige;
@#else
ce = 0.8202039838;
cw = 1.250189404;
ivst = 7.08561785087176;
k = 26.16228137;
q = 1.113859944;
y = 1.649527351;
labor = 0.3707267006;
phi = ssPhi;
cspt = 1.224390278;
utilt = 1;
delt = delt0;
deltp = delt1;
demt = 1;
lambdat = ((1.113859944) - 1)/(1-(1.113859944)*theta);
At = 1;
thetat = theta;
sigAt = sigA;
sigdt = sigd;
siget = sige;
@#endif
end;

resid;
steady(solve_algo=3);
check;

set_dynare_seed(20260424);

stoch_simul(order=3, pruning, k_order_solver, periods=0, irf=0,
            nograph, noprint, nomoments, nofunctions, nocorr);
```

- [ ] **Step 2.2: Compile the `.mod` standalone to catch syntax errors early**

Run (from repo root):

```bash
cd code/bca_uncertainty_simulation/fvgq2020_preliminary/dynare && \
/Applications/MATLAB_R2025b.app/bin/matlab -batch \
  "addpath('/Applications/Dynare/6.2-arm64/matlab'); \
   dynare fvgq2020_solveonly.mod noclearall"
```

Expected (final lines):

```
Starting Dynare (version ...).
Calling Dynare with 'fvgq2020_solveonly.mod'
...
STEADY-STATE RESULTS:
...
MODEL SUMMARY
Number of variables:         20
Number of stochastic shocks: 6
...
```

No error messages. `stoch_simul` with `order=3` and `pruning` must complete.

- [ ] **Step 2.3: If compile fails — debug loop**

Most likely failure modes and fixes:

1. `resid;` syntax error on Dynare 6.2 → try `resid(1);` (old syntax kept)
2. `steady(solve_algo=3)` issue → try `steady;` without `solve_algo` option
3. `@#if` conditional directive not parsed → replace the `@#if/@#else/@#endif` blocks with the `higherphi == 0` branch written out directly (drop the preprocessor; keep alt values in a comment).
4. `check;` failing with indeterminacy → remove `check;` for now (not required for `simult_` to work).

Re-run Step 2.2 after each fix until clean compile.

- [ ] **Step 2.4: Verify decision rule produces expected state ordering**

From the MATLAB session opened by the compile above (or a fresh session after `dynare fvgq2020_solveonly.mod noclearall`):

```matlab
disp(M_.endo_names');
disp(M_.exo_names');
disp(size(oo_.dr.ghx));
disp(size(oo_.dr.ghu));
```

Expected:

- `M_.endo_names` contains the 20 variables declared in `var` (may be more if Dynare introduces auxiliary variables; that is fine).
- `M_.exo_names` contains exactly: `ethet`, `eA`, `ed`, `uA`, `ud`, `ue`.
- `oo_.dr.ghx` and `oo_.dr.ghu` are non-empty.
- For order=3 with pruning: `oo_.dr.g_1`, `oo_.dr.g_2`, `oo_.dr.g_3` exist (used internally by `simult_`).

- [ ] **Step 2.5: Commit**

```bash
git add code/bca_uncertainty_simulation/fvgq2020_preliminary/dynare/fvgq2020_solveonly.mod
git commit -m "$(cat <<'EOF'
feat(bca-sim): add Dynare 6.2-compatible FVGQ solve-only .mod

Adapts FVGQ (2020, RED) replicationRED.mod for use with Dynare 6.2 native
pruning, stripping the Andreasen toolbox addpath and the 80 lines of post-
stoch_simul IRF construction. Model equations, calibration values, and
initval block are 1:1 with the source. Solve block uses:
  stoch_simul(order=3, pruning, k_order_solver, periods=0, irf=0, ...)
so that simult_ can drive Experiments 1/2 from MATLAB.

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>
EOF
)"
```

---

## Task 3: `setup_paths.m`

**Files:**
- Create: `code/bca_uncertainty_simulation/fvgq2020_preliminary/matlab/setup_paths.m`

- [ ] **Step 3.1: Write `setup_paths.m`**

```matlab
% setup_paths.m -- one-shot MATLAB path setup for FVGQ preliminary pipeline.
%
% Adds Dynare 6.2 to the path and changes the working directory context
% does NOT change cwd; that is the caller's responsibility.

function setup_paths()
    dynare_dir = '/Applications/Dynare/6.2-arm64/matlab';
    if ~isfolder(dynare_dir)
        error('setup_paths:dynare_missing', ...
              'Dynare 6.2 not found at %s. Update setup_paths.m if installed elsewhere.', ...
              dynare_dir);
    end
    if exist('dynare', 'file') ~= 2
        addpath(dynare_dir);
        fprintf('Added Dynare to path: %s\n', dynare_dir);
    else
        fprintf('Dynare already on path.\n');
    end

    this_file = mfilename('fullpath');
    fvgq_matlab_dir = fileparts(this_file);
    if exist(fullfile(fvgq_matlab_dir, 'run_fvgq2020_simulation.m'), 'file') == 2
        addpath(fvgq_matlab_dir);
    end
end
```

- [ ] **Step 3.2: Smoke-test `setup_paths`**

```bash
/Applications/MATLAB_R2025b.app/bin/matlab -batch \
  "addpath('code/bca_uncertainty_simulation/fvgq2020_preliminary/matlab'); \
   setup_paths; \
   assert(exist('dynare','file')==2, 'Dynare not on path'); \
   disp('setup_paths OK')"
```

Expected: `Added Dynare to path: /Applications/Dynare/6.2-arm64/matlab` and `setup_paths OK`.

- [ ] **Step 3.3: Commit**

```bash
git add code/bca_uncertainty_simulation/fvgq2020_preliminary/matlab/setup_paths.m
git commit -m "feat(bca-sim): add setup_paths helper for FVGQ preliminary

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

## Task 4: `run_fvgq2020_simulation.m` — Phase 0 (solve) and Phase 1 (warm-up)

**Files:**
- Create: `code/bca_uncertainty_simulation/fvgq2020_preliminary/matlab/run_fvgq2020_simulation.m`

This task builds the driver incrementally. Phases 2 and 3 are added in later tasks.

- [ ] **Step 4.1: Write the Phase 0 + Phase 1 skeleton**

```matlab
% run_fvgq2020_simulation.m
%
% Three-phase pipeline for the FVGQ (2020, RED) preliminary simulated BCA.
%
% Phase 0: solve fvgq2020_solveonly.mod with Dynare (order=3, pruning).
% Phase 1: shared warm-up from DSS to SSS (T_wu = 50000, zero innovations).
% Phase 2: Experiment 1 -- one long ergodic path of length T_exp1 = 20000.
% Phase 3: Experiment 2 -- N antithetic pairs of length H, for financial
%          and macro uncertainty GIRFs.
%
% Requirements:
%   MATLAB + Dynare 6.2 on the path (call setup_paths first).

clear;
clc;

this_file = mfilename('fullpath');
matlab_dir = fileparts(this_file);
root_dir = fileparts(matlab_dir);
dynare_dir = fullfile(root_dir, 'dynare');
output_dir = fullfile(root_dir, 'output');

if ~exist(output_dir, 'dir')
    mkdir(output_dir);
end

if exist('dynare', 'file') ~= 2
    error(['Dynare is not on the MATLAB path. Run setup_paths first, then ', ...
           'rerun run_fvgq2020_simulation.']);
end

old_dir = pwd;
cleanup = onCleanup(@() cd(old_dir));

% --- Phase 0: solve ------------------------------------------------------
cd(dynare_dir);
dynare fvgq2020_solveonly.mod noclearall;
cd(old_dir);

endo_names = dynare_names_to_cell(M_.endo_names);
endo_names = cellfun(@strtrim, endo_names, 'UniformOutput', false);
var_names = matlab.lang.makeValidName(endo_names);

exo_names = dynare_names_to_cell(M_.exo_names);
exo_names = cellfun(@strtrim, exo_names, 'UniformOutput', false);
exo_var_names = matlab.lang.makeValidName(exo_names);

% Shock indices needed by Experiment 2.
uA_idx = find(strcmp(exo_names, 'uA'));
ue_idx = find(strcmp(exo_names, 'ue'));
if isempty(uA_idx) || isempty(ue_idx)
    error('Could not locate uA / ue in M_.exo_names.');
end

% Endogenous-variable indices needed by CKM.
y_idx     = find(strcmp(endo_names, 'y'));
cspt_idx  = find(strcmp(endo_names, 'cspt'));
ivst_idx  = find(strcmp(endo_names, 'ivst'));
labor_idx = find(strcmp(endo_names, 'labor'));
k_idx     = find(strcmp(endo_names, 'k'));
if any(cellfun(@isempty, {y_idx, cspt_idx, ivst_idx, labor_idx, k_idx}))
    error('Could not locate y/cspt/ivst/labor/k in M_.endo_names.');
end

params = dynare_params_to_struct(M_);

% --- Phase 1: warm-up to SSS ---------------------------------------------
T_wu = 50000;
[sss_state, warmup_diag] = run_warmup(M_, options_, oo_, T_wu, endo_names);

fprintf('Phase 1 SSS gap norm = %.4e; tail-diff = %.4e\n', ...
        warmup_diag.value(strcmp(warmup_diag.name, 'sss_dss_gap_norm')), ...
        warmup_diag.value(strcmp(warmup_diag.name, 'sss_tail_diff_norm')));

% --- Phase 2: Experiment 1 -----------------------------------------------
% (Added in Task 5)

% --- Phase 3: Experiment 2 -----------------------------------------------
% (Added in Task 6)

% --- Outputs -------------------------------------------------------------
param_names = fieldnames(params);
param_values = cellfun(@(name) params.(name), param_names);
param_table = table(param_names, param_values, ...
    'VariableNames', {'name', 'value'});

writetable(param_table, fullfile(output_dir, 'parameters.csv'));
writetable(warmup_diag, fullfile(output_dir, 'warmup_diagnostics.csv'));

fprintf('Wrote parameters and warmup diagnostics to %s\n', output_dir);

% =========================================================================
% Helpers
% =========================================================================
function [sss_state, diag_tbl] = run_warmup(M_, options_, oo_, T_wu, endo_names)
    ex_warmup = zeros(T_wu, M_.exo_nbr);
    path_wu = simult_(M_, options_, oo_.dr.ys, oo_.dr, ex_warmup, 3);
    sss_state = path_wu(:, end);

    tail_diff_norm = norm(path_wu(:, end) - path_wu(:, end - 1000));
    sss_dss_gap = sss_state - oo_.dr.ys;
    gap_norm = norm(sss_dss_gap);

    names = {'sss_dss_gap_norm'; 'sss_tail_diff_norm'};
    values = [gap_norm; tail_diff_norm];
    for ii = 1:numel(endo_names)
        names{end + 1, 1} = sprintf('sss_minus_dss_%s', endo_names{ii}); %#ok<AGROW>
        values(end + 1, 1) = sss_dss_gap(ii); %#ok<AGROW>
    end
    diag_tbl = table(names, values, 'VariableNames', {'name', 'value'});
end

function names = dynare_names_to_cell(raw_names)
    if iscell(raw_names)
        names = raw_names(:);
    elseif isstring(raw_names)
        names = cellstr(raw_names(:));
    else
        names = cellstr(raw_names);
    end
end

function params = dynare_params_to_struct(M_)
    raw_names = dynare_names_to_cell(M_.param_names);
    params = struct();
    for ii = 1:numel(raw_names)
        field = matlab.lang.makeValidName(strtrim(raw_names{ii}));
        params.(field) = M_.params(ii);
    end
end
```

- [ ] **Step 4.2: Run Phase 0 + Phase 1 end-to-end**

```bash
cd /Users/linshih-yang/Documents/GitHub/Caught-in-the-Crossfire && \
/Applications/MATLAB_R2025b.app/bin/matlab -batch \
  "addpath('code/bca_uncertainty_simulation/fvgq2020_preliminary/matlab'); \
   setup_paths; run_fvgq2020_simulation"
```

Expected final lines:

```
Phase 1 SSS gap norm = <small, e.g. 1e-3 to 1e-1>; tail-diff = <very small, e.g. < 1e-8>
Wrote parameters and warmup diagnostics to .../fvgq2020_preliminary/output
```

- [ ] **Step 4.3: Inspect `warmup_diagnostics.csv`**

```bash
head -30 code/bca_uncertainty_simulation/fvgq2020_preliminary/output/warmup_diagnostics.csv
```

Expected: two header rows (`sss_dss_gap_norm`, `sss_tail_diff_norm`) plus one row per endogenous variable with its SSS–DSS gap. The `sss_tail_diff_norm` must be < 1e-6 (convergence criterion).

If `tail_diff_norm > 1e-6`, increase `T_wu` to 100000 and rerun.

- [ ] **Step 4.4: Commit**

```bash
git add code/bca_uncertainty_simulation/fvgq2020_preliminary/matlab/run_fvgq2020_simulation.m
git commit -m "feat(bca-sim): FVGQ driver Phase 0 (solve) + Phase 1 (SSS warm-up)

Mirrors parent scaffold's run_simulation.m structure. Uses Dynare 6.2 native
pruning via simult_. Warm-up runs 50,000 periods with zero innovations from
DSS; verifies convergence against state at T_wu - 1,000.

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

## Task 5: `run_fvgq2020_simulation.m` — Phase 2 (Experiment 1)

**Files:**
- Modify: `code/bca_uncertainty_simulation/fvgq2020_preliminary/matlab/run_fvgq2020_simulation.m`

- [ ] **Step 5.1: Add Experiment 1 invocation in main body**

Replace the placeholder line `% (Added in Task 5)` under `% --- Phase 2: Experiment 1 -----------------------------------------------` with:

```matlab
T_exp1 = 20000;
exp1_table = run_experiment1(M_, options_, oo_, sss_state, T_exp1, ...
                             var_names, exo_var_names);
writetable(exp1_table, fullfile(output_dir, 'experiment1_sample.csv'));
fprintf('Phase 2: wrote %d rows to experiment1_sample.csv\n', height(exp1_table));
```

- [ ] **Step 5.2: Add `run_experiment1` helper at the bottom of the file**

Append to the `% Helpers` section (between `run_warmup` and `dynare_names_to_cell`):

```matlab
function tbl = run_experiment1(M_, options_, oo_, sss_state, T_exp1, ...
                                var_names, exo_var_names)
    rng(20260424, 'twister');
    ex_exp1 = randn(T_exp1, M_.exo_nbr);
    path_exp1 = simult_(M_, options_, sss_state, oo_.dr, ex_exp1, 3);
    % Drop column 1 (initial state). Keep T_exp1 observations.
    sim_matrix = path_exp1(:, 2:end)';
    tbl = array2table(sim_matrix, 'VariableNames', var_names);
    tbl.t = (1:height(tbl))';
    eps_tbl = array2table(ex_exp1, 'VariableNames', exo_var_names);
    tbl = [tbl, eps_tbl];
    tbl = movevars(tbl, 't', 'Before', 1);
end
```

- [ ] **Step 5.3: Rerun the driver**

```bash
/Applications/MATLAB_R2025b.app/bin/matlab -batch \
  "addpath('code/bca_uncertainty_simulation/fvgq2020_preliminary/matlab'); \
   setup_paths; run_fvgq2020_simulation"
```

Expected final lines (order):

```
Phase 1 SSS gap norm = ...; tail-diff = ...
Phase 2: wrote 20000 rows to experiment1_sample.csv
Wrote parameters and warmup diagnostics to .../output
```

- [ ] **Step 5.4: Verify sample structure**

```bash
head -2 code/bca_uncertainty_simulation/fvgq2020_preliminary/output/experiment1_sample.csv
wc -l code/bca_uncertainty_simulation/fvgq2020_preliminary/output/experiment1_sample.csv
```

Expected:
- First line (header) contains columns: `t,ce,cw,ivst,q,k,labor,y,cspt,phi,utilt,delt,deltp,demt,lambdat,At,sigAt,sigdt,thetat,siget,ethet,eA,ed,uA,ud,ue` (order may vary).
- Total 20,001 lines (header + 20,000 data rows).

- [ ] **Step 5.5: Sanity check — resource identity on sample**

From MATLAB:

```matlab
T = readtable('code/bca_uncertainty_simulation/fvgq2020_preliminary/output/experiment1_sample.csv');
resid_identity = T.y - T.cspt - 0.06 * T.ivst;   % ifrac = 0.06
fprintf('Max |Y - C - I| in sample = %.3e\n', max(abs(resid_identity)));
assert(max(abs(resid_identity)) < 1e-6, 'Resource identity violated — check ifrac.');
```

Expected: `Max |Y - C - I| in sample = < 1e-8` (numerical residuals from simulation only).

- [ ] **Step 5.6: Commit**

```bash
git add code/bca_uncertainty_simulation/fvgq2020_preliminary/matlab/run_fvgq2020_simulation.m
git commit -m "feat(bca-sim): FVGQ driver Phase 2 (Experiment 1 ergodic sample)

Generates T=20,000 period path from SSS with all six innovations iid N(0,1).
Writes experiment1_sample.csv with 26 columns (20 endogenous + 6 innovations +
t). Seed 20260424 matches parent scaffold.

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

## Task 6: `run_fvgq2020_simulation.m` — Phase 3 (Experiment 2)

**Files:**
- Modify: `code/bca_uncertainty_simulation/fvgq2020_preliminary/matlab/run_fvgq2020_simulation.m`

- [ ] **Step 6.1: Add Experiment 2 invocation in main body**

Replace `% (Added in Task 6)` under `% --- Phase 3: Experiment 2 -----------------------------------------------` with:

```matlab
N = 1000;
H = 60;

[paths_base_fin, paths_shock_fin] = run_experiment2(M_, options_, oo_, sss_state, ...
                                                   N, H, ue_idx, 'fin');
[paths_base_macro, paths_shock_macro] = run_experiment2(M_, options_, oo_, sss_state, ...
                                                       N, H, uA_idx, 'macro');

exp2_path = fullfile(output_dir, 'experiment2_paths.mat');
save(exp2_path, ...
     'paths_base_fin', 'paths_shock_fin', ...
     'paths_base_macro', 'paths_shock_macro', ...
     'var_names', 'exo_var_names', ...
     'uA_idx', 'ue_idx', 'N', 'H', '-v7.3');
fprintf('Phase 3: wrote %d financial pairs + %d macro pairs to %s\n', ...
        N, N, exp2_path);

workspace_path = fullfile(output_dir, 'simulated_workspace.mat');
save(workspace_path, 'M_', 'oo_', 'options_', 'sss_state', ...
     'exp1_table', 'paths_base_fin', 'paths_shock_fin', ...
     'paths_base_macro', 'paths_shock_macro', 'params', ...
     'var_names', 'exo_var_names', 'uA_idx', 'ue_idx', ...
     'y_idx', 'cspt_idx', 'ivst_idx', 'labor_idx', 'k_idx', ...
     'warmup_diag', '-v7.3');
fprintf('Wrote consolidated workspace to %s\n', workspace_path);
```

- [ ] **Step 6.2: Add `run_experiment2` helper**

Append to the `% Helpers` section after `run_experiment1`:

```matlab
function [paths_base, paths_shock] = run_experiment2(M_, options_, oo_, ...
                                                     sss_state, N, H, ...
                                                     shock_idx, tag)
    n_obs = M_.endo_nbr;
    paths_base = zeros(N, H, n_obs);
    paths_shock = zeros(N, H, n_obs);

    tag_offset = tag_to_offset(tag);
    for i = 1:N
        rng(20260424 + tag_offset + i, 'twister');
        ex_i = randn(H, M_.exo_nbr);

        ex_base = ex_i;  ex_base(1, shock_idx) = 0;
        ex_shock = ex_i; ex_shock(1, shock_idx) = 1;

        path_base = simult_(M_, options_, sss_state, oo_.dr, ex_base, 3);
        path_shock = simult_(M_, options_, sss_state, oo_.dr, ex_shock, 3);

        paths_base(i, :, :) = path_base(:, 2:end)';
        paths_shock(i, :, :) = path_shock(:, 2:end)';
    end
    fprintf('  Experiment 2 (%s): generated %d pairs x H=%d\n', tag, N, H);
end

function offset = tag_to_offset(tag)
    % Separate RNG streams between fin and macro experiments so that
    % within-pair antithesis is preserved but cross-tag comparisons are
    % independent.
    switch lower(tag)
        case 'fin'
            offset = 0;
        case 'macro'
            offset = 1000000;
        otherwise
            error('run_experiment2:bad_tag', 'Unknown tag: %s', tag);
    end
end
```

- [ ] **Step 6.3: Rerun full driver**

```bash
/Applications/MATLAB_R2025b.app/bin/matlab -batch \
  "addpath('code/bca_uncertainty_simulation/fvgq2020_preliminary/matlab'); \
   setup_paths; tic; run_fvgq2020_simulation; toc"
```

Expected final lines:

```
Phase 1 SSS gap norm = ...; tail-diff = ...
Phase 2: wrote 20000 rows to experiment1_sample.csv
  Experiment 2 (fin): generated 1000 pairs x H=60
  Experiment 2 (macro): generated 1000 pairs x H=60
Phase 3: wrote 1000 financial pairs + 1000 macro pairs to .../output/experiment2_paths.mat
Wrote consolidated workspace to .../output/simulated_workspace.mat
Elapsed time is <100-300> seconds.
```

- [ ] **Step 6.4: Verify Experiment 2 output shape**

From MATLAB:

```matlab
S = load('code/bca_uncertainty_simulation/fvgq2020_preliminary/output/experiment2_paths.mat');
assert(isequal(size(S.paths_base_fin),   [1000, 60, numel(S.var_names)]));
assert(isequal(size(S.paths_shock_fin),  [1000, 60, numel(S.var_names)]));
assert(isequal(size(S.paths_base_macro), [1000, 60, numel(S.var_names)]));
diff_fin_at_t1 = squeeze(S.paths_shock_fin(1,1,:) - S.paths_base_fin(1,1,:));
fprintf('Max |shock - base| at h=1 (fin pair 1) = %.4e\n', max(abs(diff_fin_at_t1)));
disp('Experiment 2 shape OK');
```

Expected: no errors; `Max |shock - base|` is **non-zero** (confirms shock at t=0 propagates to t=1).

- [ ] **Step 6.5: Commit**

```bash
git add code/bca_uncertainty_simulation/fvgq2020_preliminary/matlab/run_fvgq2020_simulation.m
git commit -m "feat(bca-sim): FVGQ driver Phase 3 (Experiment 2 antithetic GIRF panel)

Generates N=1,000 antithetic innovation pairs of length H=60 for both
financial (ue) and macro (uA) uncertainty shocks. Within each pair, all
innovations are identical except the period-1 targeted shock (0 vs. 1).
Separate RNG offsets keep fin and macro streams independent.

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

## Task 7: `estimate_ckm_wedges.m`

**Files:**
- Create: `code/bca_uncertainty_simulation/fvgq2020_preliminary/matlab/estimate_ckm_wedges.m`

**Algorithm:** Given `(Y, C, I, L, K)` and structural parameters `(α, β, δ, γ, χ, ν)`, back out the four wedges via static identities and a fixed-point iteration for `τ_x`:

1. `A_t = Y_t / (K_{t-1}^α · L_t^{1-α})` (timing: CKM uses `K_{t-1}` for production).
2. `G_t/Y_t = 1 - C_t/Y_t - I_t/Y_t` (should be ≈ 0 in FVGQ).
3. `τ_ℓ,t = 1 - χ · L_t^{ν+1} · C_t^γ / ((1-α) · Y_t)`.
4. Investment wedge `τ_x,t` via realized-value fixed point (see Step 7.1 inline comments).

**Structural parameters** (taken from the FVGQ calibration; `χ` is set to match a target steady-state labor of 0.3546, which is the FVGQ SSS labor value):

| Symbol | Value | Source |
|--------|-------|--------|
| `α` | 0.36 | FVGQ `alpha` |
| `β` | 0.994 | FVGQ `beta` |
| `δ` | 0.01625 | FVGQ `delt0` (utilization turned off for CKM prototype) |
| `γ` | 2 | FVGQ `rho` (CRRA coefficient) |
| `ν` | 1 | Standard Frisch elasticity for CKM prototype |
| `χ` | computed to match FVGQ SSS labor | See code |

- [ ] **Step 7.1: Write `estimate_ckm_wedges.m`**

```matlab
function wedges = estimate_ckm_wedges(Y, C, I, L, K, prototype_params)
%ESTIMATE_CKM_WEDGES Back out the four canonical CKM (2007) wedges from
%aggregate simulated data using a prototype frictionless RBC economy.
%
% INPUTS
%   Y, C, I, L, K : T x 1 column vectors (level aggregates)
%   prototype_params : struct with fields
%       alpha, beta, delta, gamma, nu, chi
%
% OUTPUT
%   wedges : table with columns t, log_A, G_share, tau_l, tau_x
%
% METHOD
%   A_t       = Y_t / ( K_{t-1}^alpha * L_t^(1-alpha) )
%   G_t/Y_t   = 1 - C_t/Y_t - I_t/Y_t
%   tau_l_t   = 1 - chi * L_t^(nu+1) * C_t^gamma / ( (1-alpha) * Y_t )
%   tau_x_t   = realized-value fixed point of the Euler equation:
%                 u_c(C_t) * (1 + tau_x_t) =
%                     beta * u_c(C_{t+1}) * (alpha Y_{t+1}/K_t +
%                                            (1-delta)*(1 + tau_x_{t+1}))
%               Initialize tau_x = 0; iterate 5 times; terminal wedge
%               uses forward-filled last value.

    T = numel(Y);
    if numel(C) ~= T || numel(I) ~= T || numel(L) ~= T || numel(K) ~= T
        error('estimate_ckm_wedges:size_mismatch', ...
              'Y, C, I, L, K must all have length T = %d', T);
    end

    alpha = prototype_params.alpha;
    beta  = prototype_params.beta;
    delta = prototype_params.delta;
    gamma = prototype_params.gamma;
    nu    = prototype_params.nu;
    chi   = prototype_params.chi;

    % Lagged capital K_{t-1}. Assume K is given as end-of-period stock, so
    % production at period t uses K(t-1) with K(0) unobserved; pad by
    % replicating the first observation. The first observation's A_t is
    % therefore slightly biased and should be treated as a burn-in.
    K_lag = [K(1); K(1:T-1)];

    % Wedge 1: TFP (log_A)
    log_A = log(Y) - alpha * log(K_lag) - (1 - alpha) * log(L);

    % Wedge 2: G_share (should be ~ 0 in FVGQ data)
    G_share = 1 - C ./ Y - I ./ Y;

    % Wedge 3: tau_l from labor FOC
    tau_l = 1 - chi * L.^(nu + 1) .* C.^gamma ./ ((1 - alpha) * Y);

    % Wedge 4: tau_x via realized-value fixed point
    tau_x = zeros(T, 1);
    MPK_next = alpha * [Y(2:T); Y(T)] ./ K;    % alpha * Y_{t+1} / K_t, last row forward-filled
    uc      = C.^(-gamma);
    uc_next = [uc(2:T); uc(T)];
    for iter = 1:5
        tau_x_next = [tau_x(2:T); tau_x(T)];
        rhs = beta * uc_next .* (MPK_next + (1 - delta) * (1 + tau_x_next));
        tau_x = rhs ./ uc - 1;
    end

    wedges = table((1:T)', log_A, G_share, tau_l, tau_x, ...
        'VariableNames', {'t', 'log_A', 'G_share', 'tau_l', 'tau_x'});
end
```

- [ ] **Step 7.2: Unit-test `estimate_ckm_wedges` against a degenerate case**

From MATLAB:

```matlab
addpath('code/bca_uncertainty_simulation/fvgq2020_preliminary/matlab');

% Construct deterministic Solow-like data where A_t = 1, no wedges expected.
T = 200;
alpha = 0.36; beta = 0.994; delta = 0.01625; gamma = 2; nu = 1;
rk = 1/beta - 1 + delta;
k_over_l = (alpha/rk)^(1/(1-alpha));
y_over_l = k_over_l^alpha;
x_over_l = delta * k_over_l;
c_over_l = y_over_l - x_over_l;
L = 0.35 * ones(T,1);
K = k_over_l * L;
Y = y_over_l * L;
I = x_over_l * L;
C = c_over_l * L;
chi = (1-alpha) * y_over_l / (L(1)^(nu+gamma) * c_over_l^gamma);

pp = struct('alpha',alpha,'beta',beta,'delta',delta, ...
            'gamma',gamma,'nu',nu,'chi',chi);
W = estimate_ckm_wedges(Y, C, I, L, K, pp);

fprintf('log_A max abs = %.3e (expected ~0)\n', max(abs(W.log_A(2:end))));
fprintf('G_share max abs = %.3e (expected ~0)\n', max(abs(W.G_share)));
fprintf('tau_l max abs = %.3e (expected ~0)\n', max(abs(W.tau_l)));
fprintf('tau_x max abs = %.3e (expected ~0)\n', max(abs(W.tau_x(1:end-1))));

assert(max(abs(W.log_A(2:end))) < 1e-10);
assert(max(abs(W.G_share)) < 1e-10);
assert(max(abs(W.tau_l)) < 1e-8);
assert(max(abs(W.tau_x(1:end-1))) < 1e-6);
disp('Degenerate-case sanity check passed');
```

Expected: all four `max abs` values near machine epsilon; `Degenerate-case sanity check passed` prints.

- [ ] **Step 7.3: Commit**

```bash
git add code/bca_uncertainty_simulation/fvgq2020_preliminary/matlab/estimate_ckm_wedges.m
git commit -m "feat(bca-sim): add four-wedge CKM estimator

Implements CKM (2007) wedge extraction for simulated aggregates (Y,C,I,L,K):
TFP and G/Y via static identities, tau_l via labor FOC inversion, tau_x via
5-iteration realized-value fixed point on the prototype Euler equation.
Verified against a steady-state Solow benchmark where all four wedges
collapse to numerical zero.

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

## Task 8: `local_projection.m`

**Files:**
- Create: `code/bca_uncertainty_simulation/fvgq2020_preliminary/matlab/local_projection.m`

- [ ] **Step 8.1: Write `local_projection.m`**

```matlab
function lp = local_projection(y, shocks, controls, H)
%LOCAL_PROJECTION Estimate Jordà-style local projections of y on a set of
%shocks and controls.
%
% INPUTS
%   y        : T x 1 outcome series
%   shocks   : T x K matrix of shock regressors (columns are different shocks)
%   controls : T x M matrix of control regressors (can be empty)
%   H        : maximum horizon (h = 0, 1, ..., H)
%
% OUTPUT
%   lp : struct with fields
%       beta : (H+1) x K matrix of shock coefficients across horizons
%       se   : (H+1) x K matrix of Newey-West standard errors
%       ci_lo, ci_hi : 95% CIs
%       horizons : 0..H vector

    [T, K] = size(shocks);
    M = size(controls, 2);

    lp.horizons = (0:H)';
    lp.beta = nan(H+1, K);
    lp.se   = nan(H+1, K);

    for hh = 0:H
        y_h = y(1+hh:T);
        X_shocks = shocks(1:T-hh, :);
        X_controls = controls(1:T-hh, :);
        X = [ones(T-hh, 1), X_shocks, X_controls];

        b = X \ y_h;
        res = y_h - X * b;
        n = size(X, 1);
        k_reg = size(X, 2);

        % Newey-West with lag = hh (standard for LP).
        L = max(hh, 1);
        XX = X' * X;
        S = (X .* res)' * (X .* res);
        for ll = 1:L
            w = 1 - ll/(L+1);
            Xl = X(1:end-ll, :) .* res(1:end-ll);
            Xr = X(1+ll:end, :) .* res(1+ll:end);
            Gamma = Xl' * Xr;
            S = S + w * (Gamma + Gamma');
        end
        V = XX \ S / XX;
        se_b = sqrt(diag(V));

        lp.beta(hh+1, :) = b(2:K+1)';
        lp.se(hh+1, :)   = se_b(2:K+1)';
    end
    lp.ci_lo = lp.beta - 1.96 * lp.se;
    lp.ci_hi = lp.beta + 1.96 * lp.se;
end
```

- [ ] **Step 8.2: Unit-test `local_projection` on a simple AR(1)-with-shock DGP**

From MATLAB:

```matlab
addpath('code/bca_uncertainty_simulation/fvgq2020_preliminary/matlab');

rng(42, 'twister');
T = 5000;
rho = 0.8;
u = randn(T,1);
shock = randn(T,1);
y = zeros(T,1);
for t = 2:T
    y(t) = rho * y(t-1) + 0.5 * shock(t) + 0.1 * u(t);
end

lp = local_projection(y, shock, zeros(T,0), 10);
fprintf('LP beta at h=0: %.3f (expected ~0.50)\n', lp.beta(1));
fprintf('LP beta at h=5: %.3f (expected ~%.3f)\n', lp.beta(6), 0.5 * rho^5);
assert(abs(lp.beta(1) - 0.5) < 0.05);
assert(abs(lp.beta(6) - 0.5 * rho^5) < 0.05);
disp('LP sanity check passed');
```

Expected: `beta(1) ≈ 0.50`, `beta(6) ≈ 0.164`, assertion passes.

- [ ] **Step 8.3: Commit**

```bash
git add code/bca_uncertainty_simulation/fvgq2020_preliminary/matlab/local_projection.m
git commit -m "feat(bca-sim): add Jordà local-projection estimator

Newey-West HAC standard errors with lag = horizon. Supports multiple shock
regressors simultaneously (e.g., orthogonal Macro and Financial uncertainty
innovations estimated in one LP). Verified against AR(1) ground truth.

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

## Task 9: `run_bca_analysis.m` — apply CKM + LP + GIRF

**Files:**
- Create: `code/bca_uncertainty_simulation/fvgq2020_preliminary/matlab/run_bca_analysis.m`

- [ ] **Step 9.1: Write `run_bca_analysis.m`**

```matlab
% run_bca_analysis.m
%
% Second-stage driver. Requires run_fvgq2020_simulation to have produced
% output/experiment1_sample.csv and output/experiment2_paths.mat.
%
% Steps:
%   A. Load Experiment 1 sample; run CKM; run LP on (uA, ue).
%   B. Load Experiment 2 paths; run CKM on each path pair; compute GIRF.
%   C. Save wedges_exp1.csv, lp_results.mat, wedges_girf.mat.

clear;
clc;

this_file = mfilename('fullpath');
matlab_dir = fileparts(this_file);
root_dir = fileparts(matlab_dir);
output_dir = fullfile(root_dir, 'output');

addpath(matlab_dir);

% ---- Prototype CKM parameters (from FVGQ calibration) ------------------
pp.alpha = 0.36;
pp.beta  = 0.994;
pp.delta = 0.01625;
pp.gamma = 2;
pp.nu    = 1;
% Chi is calibrated to the FVGQ steady-state labor of 0.3546099291 given
% the corresponding C/Y at the SSS. We match the labor FOC in steady state:
%   chi = (1-alpha) * y_ss / (l_ss^(nu+1) * c_ss^gamma)
% Pulling SSS values from FVGQ initval (higherphi=0):
l_ss = 0.3546099291;
y_ss = 1.422989127;
c_ss = 1.070799318;
pp.chi = (1 - pp.alpha) * y_ss / (l_ss^(pp.nu + 1) * c_ss^pp.gamma);

fprintf('Prototype chi = %.6f\n', pp.chi);

% ---- A. Experiment 1: CKM + LP ----------------------------------------
exp1_csv = fullfile(output_dir, 'experiment1_sample.csv');
T = readtable(exp1_csv);

Y = T.y;
C = T.cspt;
I = 0.06 * T.ivst;       % ifrac = 0.06
L = T.labor;
K = T.k;

wedges = estimate_ckm_wedges(Y, C, I, L, K, pp);
fprintf('CKM on Exp1: max |G_share| = %.3e (tripwire: should be near 0)\n', ...
        max(abs(wedges.G_share)));
writetable(wedges, fullfile(output_dir, 'wedges_exp1.csv'));

% LP: regress each wedge at horizon h on (uA, ue) with controls.
wedge_names = {'log_A', 'G_share', 'tau_l', 'tau_x'};
shocks = [T.uA, T.ue];
controls = [T.eA, T.ed, T.ethet, T.ud, T.sigAt, T.sigdt, T.siget];
H_lp = 60;

lp_results = struct();
for j = 1:numel(wedge_names)
    lp = local_projection(wedges.(wedge_names{j}), shocks, controls, H_lp);
    lp_results.(wedge_names{j}) = lp;
end
save(fullfile(output_dir, 'lp_results.mat'), 'lp_results', 'wedge_names', ...
     'H_lp', '-v7.3');
fprintf('LP on Exp1: saved %s\n', fullfile(output_dir, 'lp_results.mat'));

% ---- B. Experiment 2: CKM on pairs + GIRF -----------------------------
S = load(fullfile(output_dir, 'experiment2_paths.mat'));
var_names = S.var_names;
y_idx_v   = find(strcmp(var_names, 'y'));
cspt_idx_v  = find(strcmp(var_names, 'cspt'));
ivst_idx_v  = find(strcmp(var_names, 'ivst'));
labor_idx_v = find(strcmp(var_names, 'labor'));
k_idx_v     = find(strcmp(var_names, 'k'));

girf = struct();
for tag = {'fin', 'macro'}
    tag_str = tag{1};
    pb = S.(['paths_base_' tag_str]);
    ps = S.(['paths_shock_' tag_str]);
    [Npairs, Hpairs, ~] = size(pb);

    gird_wedges_base  = zeros(Npairs, Hpairs, numel(wedge_names));
    gird_wedges_shock = zeros(Npairs, Hpairs, numel(wedge_names));
    for i = 1:Npairs
        wb = wedges_from_path(squeeze(pb(i, :, :)), ...
                              y_idx_v, cspt_idx_v, ivst_idx_v, ...
                              labor_idx_v, k_idx_v, pp);
        ws = wedges_from_path(squeeze(ps(i, :, :)), ...
                              y_idx_v, cspt_idx_v, ivst_idx_v, ...
                              labor_idx_v, k_idx_v, pp);
        for j = 1:numel(wedge_names)
            gird_wedges_base(i, :, j)  = wb.(wedge_names{j});
            gird_wedges_shock(i, :, j) = ws.(wedge_names{j});
        end
    end

    diff_wedges = gird_wedges_shock - gird_wedges_base;
    girf.(tag_str).mean     = squeeze(mean(diff_wedges, 1));          % H x 4
    girf.(tag_str).q05      = squeeze(quantile(diff_wedges, 0.05, 1));
    girf.(tag_str).q95      = squeeze(quantile(diff_wedges, 0.95, 1));
    girf.(tag_str).wedges_base  = gird_wedges_base;
    girf.(tag_str).wedges_shock = gird_wedges_shock;
    fprintf('GIRF (%s): %d pairs x H=%d x %d wedges computed\n', ...
            tag_str, Npairs, Hpairs, numel(wedge_names));
end

save(fullfile(output_dir, 'wedges_girf.mat'), 'girf', 'wedge_names', '-v7.3');
fprintf('GIRF: saved %s\n', fullfile(output_dir, 'wedges_girf.mat'));

% =========================================================================
% Helpers
% =========================================================================
function wedges = wedges_from_path(path_rows, y_idx, cspt_idx, ivst_idx, ...
                                    labor_idx, k_idx, pp)
    % path_rows is H x n_obs (one pair's simulated path).
    Y = path_rows(:, y_idx);
    C = path_rows(:, cspt_idx);
    I = 0.06 * path_rows(:, ivst_idx);
    L = path_rows(:, labor_idx);
    K = path_rows(:, k_idx);
    wedges = estimate_ckm_wedges(Y, C, I, L, K, pp);
end
```

- [ ] **Step 9.2: Run the analysis**

```bash
/Applications/MATLAB_R2025b.app/bin/matlab -batch \
  "addpath('code/bca_uncertainty_simulation/fvgq2020_preliminary/matlab'); \
   setup_paths; run_bca_analysis"
```

Expected final lines:

```
Prototype chi = <numeric>
CKM on Exp1: max |G_share| = <near 0, e.g. < 1e-6>
LP on Exp1: saved .../output/lp_results.mat
GIRF (fin): 1000 pairs x H=60 x 4 wedges computed
GIRF (macro): 1000 pairs x H=60 x 4 wedges computed
GIRF: saved .../output/wedges_girf.mat
```

- [ ] **Step 9.3: Tripwire — assert G/Y is numerically zero**

From MATLAB:

```matlab
W = readtable('code/bca_uncertainty_simulation/fvgq2020_preliminary/output/wedges_exp1.csv');
fprintf('mean(G_share) = %.3e,  max|G_share| = %.3e\n', ...
        mean(W.G_share), max(abs(W.G_share)));
assert(max(abs(W.G_share)) < 1e-6, ...
       'Tripwire: G/Y is not near zero — aggregation error suspected.');
disp('Tripwire passed');
```

If this fails, the most likely cause is the `ifrac` multiplier on `ivst` — check that `I = 0.06 * T.ivst` in both `run_bca_analysis.m` main body and `wedges_from_path` helper.

- [ ] **Step 9.4: Commit**

```bash
git add code/bca_uncertainty_simulation/fvgq2020_preliminary/matlab/run_bca_analysis.m
git commit -m "feat(bca-sim): CKM + LP + GIRF analysis driver for FVGQ preliminary

Loads Experiment 1 sample and Experiment 2 pair arrays, applies CKM wedge
extraction with FVGQ-calibrated prototype parameters (alpha=0.36, beta=0.994,
delta=0.01625, gamma=2, nu=1, chi matched to SSS). Regresses wedges on
(uA, ue) with seven controls via local projection at horizons 0-60. Computes
GIRF by wedge and shock type across 1,000 antithetic pairs with 5-95%
cross-sectional bands.

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

## Task 10: `plot_bca_responses.m`

**Files:**
- Create: `code/bca_uncertainty_simulation/fvgq2020_preliminary/matlab/plot_bca_responses.m`

- [ ] **Step 10.1: Write `plot_bca_responses.m`**

```matlab
% plot_bca_responses.m
%
% Consumes output/lp_results.mat and output/wedges_girf.mat; produces:
%   bca_lp_fin.png    -- LP response of each wedge to ue (financial SV)
%   bca_lp_macro.png  -- LP response of each wedge to uA (TFP SV)
%   bca_girf_fin.png  -- GIRF of each wedge to ue with 5-95% band
%   bca_girf_macro.png-- GIRF of each wedge to uA with 5-95% band

clear;
clc;

this_file = mfilename('fullpath');
matlab_dir = fileparts(this_file);
root_dir = fileparts(matlab_dir);
output_dir = fullfile(root_dir, 'output');

LP = load(fullfile(output_dir, 'lp_results.mat'));
G  = load(fullfile(output_dir, 'wedges_girf.mat'));

wedge_names = LP.wedge_names;
wedge_titles = {'log A (efficiency)', 'G/Y (resource)', '\tau_\ell (labor)', '\tau_x (investment)'};
H_lp = LP.H_lp;

% ---- LP plots ----------------------------------------------------------
for shock_tag = {'macro', 'fin'}
    ts = shock_tag{1};
    shock_col = strcmp({'macro','fin'}, ts);
    fig = figure('Visible','off','Position',[100 100 900 700]);
    for j = 1:numel(wedge_names)
        subplot(2,2,j);
        lp = LP.lp_results.(wedge_names{j});
        h = lp.horizons;
        b = lp.beta(:, shock_col);
        lo = lp.ci_lo(:, shock_col);
        hi = lp.ci_hi(:, shock_col);
        fill([h; flipud(h)], [hi; flipud(lo)], [0.8 0.85 0.95], ...
             'EdgeColor','none'); hold on;
        plot(h, b, 'b-', 'LineWidth', 1.5);
        plot(h, zeros(size(h)), 'k:');
        title(wedge_titles{j});
        xlabel('horizon');
        ylabel('LP coefficient');
        grid on;
    end
    sgtitle(sprintf('LP: wedge response to %s uncertainty shock', ts));
    saveas(fig, fullfile(output_dir, sprintf('bca_lp_%s.png', ts)));
    close(fig);
end

% ---- GIRF plots --------------------------------------------------------
for shock_tag = {'macro', 'fin'}
    ts = shock_tag{1};
    fig = figure('Visible','off','Position',[100 100 900 700]);
    gd = G.girf.(ts);
    H_g = size(gd.mean, 1);
    h = (0:H_g-1)';
    for j = 1:numel(wedge_names)
        subplot(2,2,j);
        fill([h; flipud(h)], [gd.q95(:,j); flipud(gd.q05(:,j))], ...
             [0.95 0.85 0.8], 'EdgeColor','none'); hold on;
        plot(h, gd.mean(:,j), 'r-', 'LineWidth', 1.5);
        plot(h, zeros(size(h)), 'k:');
        title(wedge_titles{j});
        xlabel('horizon');
        ylabel('GIRF');
        grid on;
    end
    sgtitle(sprintf('GIRF: wedge response to %s uncertainty shock', ts));
    saveas(fig, fullfile(output_dir, sprintf('bca_girf_%s.png', ts)));
    close(fig);
end

fprintf('Wrote LP and GIRF figures to %s\n', output_dir);
```

- [ ] **Step 10.2: Run plotting**

```bash
/Applications/MATLAB_R2025b.app/bin/matlab -batch \
  "addpath('code/bca_uncertainty_simulation/fvgq2020_preliminary/matlab'); \
   plot_bca_responses"
```

Expected: `Wrote LP and GIRF figures to .../output`

- [ ] **Step 10.3: Verify figures exist**

```bash
ls -la code/bca_uncertainty_simulation/fvgq2020_preliminary/output/*.png
```

Expected: four PNGs — `bca_lp_fin.png`, `bca_lp_macro.png`, `bca_girf_fin.png`, `bca_girf_macro.png`, each >20KB.

- [ ] **Step 10.4: Commit**

```bash
git add code/bca_uncertainty_simulation/fvgq2020_preliminary/matlab/plot_bca_responses.m
git commit -m "feat(bca-sim): LP and GIRF plotting for FVGQ preliminary

2x2 subplot grids per shock type (fin, macro) showing the response of each
of the four CKM wedges. LP plots show point estimates with 95% Newey-West
CIs; GIRF plots show cross-pair mean with 5-95% bands across N=1,000 pairs.

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

## Task 11: `sanity_checks.m`

**Files:**
- Create: `code/bca_uncertainty_simulation/fvgq2020_preliminary/matlab/sanity_checks.m`

Consolidates the ad-hoc asserts used in Steps 5.5, 6.4, 9.3 into one reusable checker, invoked after the full pipeline runs.

- [ ] **Step 11.1: Write `sanity_checks.m`**

```matlab
% sanity_checks.m
%
% Asserts invariants over the full output/ folder. Call after
% run_fvgq2020_simulation + run_bca_analysis.

clear;
clc;

this_file = mfilename('fullpath');
matlab_dir = fileparts(this_file);
root_dir = fileparts(matlab_dir);
output_dir = fullfile(root_dir, 'output');

fail_count = 0;

% Check 1: warmup tail convergence.
WU = readtable(fullfile(output_dir, 'warmup_diagnostics.csv'));
tail_diff = WU.value(strcmp(WU.name, 'sss_tail_diff_norm'));
if tail_diff > 1e-6
    fprintf('[FAIL] SSS tail-diff norm %.3e exceeds 1e-6\n', tail_diff);
    fail_count = fail_count + 1;
else
    fprintf('[PASS] SSS tail-diff norm %.3e\n', tail_diff);
end

% Check 2: Experiment 1 resource identity.
T1 = readtable(fullfile(output_dir, 'experiment1_sample.csv'));
resid1 = T1.y - T1.cspt - 0.06 * T1.ivst;
if max(abs(resid1)) > 1e-6
    fprintf('[FAIL] Exp1 resource identity max |Y-C-I| = %.3e\n', max(abs(resid1)));
    fail_count = fail_count + 1;
else
    fprintf('[PASS] Exp1 resource identity max |Y-C-I| = %.3e\n', max(abs(resid1)));
end

% Check 3: Experiment 2 shapes and non-zero shock.
S = load(fullfile(output_dir, 'experiment2_paths.mat'));
expected_shape = [S.N, S.H, numel(S.var_names)];
for tag = {'fin', 'macro'}
    pb = S.(['paths_base_' tag{1}]);
    ps = S.(['paths_shock_' tag{1}]);
    if ~isequal(size(pb), expected_shape) || ~isequal(size(ps), expected_shape)
        fprintf('[FAIL] Exp2 (%s) shape mismatch: got %s, expected %s\n', ...
                tag{1}, mat2str(size(pb)), mat2str(expected_shape));
        fail_count = fail_count + 1;
    else
        diff_max = max(abs(squeeze(ps(1,1,:) - pb(1,1,:))));
        if diff_max < 1e-8
            fprintf('[FAIL] Exp2 (%s) no shock propagation at h=1 (diff=%.3e)\n', ...
                    tag{1}, diff_max);
            fail_count = fail_count + 1;
        else
            fprintf('[PASS] Exp2 (%s) shape OK, h=1 diff %.3e\n', tag{1}, diff_max);
        end
    end
end

% Check 4: G/Y tripwire on recovered wedges.
W = readtable(fullfile(output_dir, 'wedges_exp1.csv'));
if max(abs(W.G_share)) > 1e-6
    fprintf('[FAIL] Wedge G_share max |.| = %.3e (tripwire)\n', max(abs(W.G_share)));
    fail_count = fail_count + 1;
else
    fprintf('[PASS] Wedge G_share max |.| = %.3e\n', max(abs(W.G_share)));
end

if fail_count > 0
    error('sanity_checks: %d check(s) failed.', fail_count);
else
    fprintf('\nAll %d sanity checks passed.\n', 4 + 1);  % 4 named + 2 sub-checks on Exp2
end
```

- [ ] **Step 11.2: Run sanity checks**

```bash
/Applications/MATLAB_R2025b.app/bin/matlab -batch \
  "addpath('code/bca_uncertainty_simulation/fvgq2020_preliminary/matlab'); \
   sanity_checks"
```

Expected: every line starts with `[PASS]`; final line `All 5 sanity checks passed.`

If any `[FAIL]` appears, stop and debug before the memo task — the failure is one of: aggregation (ifrac), warmup length, or RNG streams.

- [ ] **Step 11.3: Commit**

```bash
git add code/bca_uncertainty_simulation/fvgq2020_preliminary/matlab/sanity_checks.m
git commit -m "feat(bca-sim): consolidated sanity-checks script

Asserts SSS tail convergence, Exp1 resource identity, Exp2 shape and shock
propagation, and wedge G/Y tripwire. One-stop validation for the whole
FVGQ preliminary pipeline.

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

## Task 12: Scholar-discussion memo

**Files:**
- Create: `llm_logs/<today>_fvgq2020_preliminary_results.md` (where `<today>` is the date on which this task is performed, in `YYYY-MM-DD` form)

- [ ] **Step 12.1: Gather summary statistics from outputs**

From MATLAB:

```matlab
LP = load('code/bca_uncertainty_simulation/fvgq2020_preliminary/output/lp_results.mat');
G  = load('code/bca_uncertainty_simulation/fvgq2020_preliminary/output/wedges_girf.mat');

% LP: peak response of each wedge to each shock (macro=col1, fin=col2).
for j = 1:numel(LP.wedge_names)
    lp = LP.lp_results.(LP.wedge_names{j});
    [~, hmax_macro] = max(abs(lp.beta(:,1)));
    [~, hmax_fin]   = max(abs(lp.beta(:,2)));
    fprintf('%s: peak LP-macro %.3e at h=%d | peak LP-fin %.3e at h=%d\n', ...
            LP.wedge_names{j}, lp.beta(hmax_macro,1), hmax_macro-1, ...
            lp.beta(hmax_fin,2), hmax_fin-1);
end

% GIRF: peak response per wedge per shock.
for tag = {'macro', 'fin'}
    gd = G.girf.(tag{1});
    fprintf('\nGIRF (%s):\n', tag{1});
    for j = 1:numel(LP.wedge_names)
        [~, hmax] = max(abs(gd.mean(:,j)));
        fprintf('  %s: peak %.3e at h=%d (band [%.3e, %.3e])\n', ...
                LP.wedge_names{j}, gd.mean(hmax,j), hmax-1, ...
                gd.q05(hmax,j), gd.q95(hmax,j));
    end
end
```

Copy the printed output into the memo below.

- [ ] **Step 12.2: Write the memo**

File: `llm_logs/<today>_fvgq2020_preliminary_results.md` — the engineer should substitute `<today>` with the current date (e.g., `2026-04-28`).

Template (fill in `<...>` placeholders with actual values from Step 12.1):

```markdown
# FVGQ 2020 Preliminary Simulated BCA — Results Memo

**Date:** <YYYY-MM-DD>
**Spec:** `docs/superpowers/specs/2026-04-24-fvgq2020-preliminary-simulated-bca-design.md`
**Plan:** `docs/superpowers/plans/2026-04-24-fvgq2020-preliminary-simulated-bca.md`
**Code:** `code/bca_uncertainty_simulation/fvgq2020_preliminary/`

## Purpose

This memo summarizes the preliminary simulated-BCA exercise driven by the
Fernández-Villaverde & Guerrón-Quintana (2020, RED) two-agent DSGE model.
The goal is to obtain concrete wedge signatures of uncertainty shocks
(macro `uA` and financial `ue`) for scholar discussion, prior to developing
the §7 representative-agent LWZ+CGK hybrid.

## Setup recap

- **DGP:** FVGQ (2020) model unchanged; baseline `higherphi = 0`; third-order
  perturbation with Dynare 6.2 native pruning.
- **Agents:** 6% entrepreneurs + 94% workers (two-agent, not heterogeneous —
  no Krusell-Smith distribution dynamics).
- **Uncertainty shocks:** `uA` (TFP SV) and `ue` (collateral LTV SV).
- **Warm-up:** T_wu = 50,000 from DSS to SSS (convergence norm <value>).
- **Experiment 1:** T = 20,000 ergodic path, LP of each wedge on (uA, ue)
  with controls for level shocks, preference SV, and lagged SV states.
- **Experiment 2:** N = 1,000 antithetic pairs, horizon H = 60, separately
  for `ue` and `uA`.
- **CKM prototype:** α=0.36, β=0.994, δ=0.01625, γ=2, ν=1, χ matched to
  FVGQ SSS labor.

## Headline numbers

### LP peak responses (Experiment 1)

| Wedge | Macro peak (horizon) | Financial peak (horizon) |
|-------|---------------------|-------------------------|
| log A | <value> at h=<int> | <value> at h=<int> |
| G/Y | <value> at h=<int> | <value> at h=<int> |
| τ_ℓ | <value> at h=<int> | <value> at h=<int> |
| τ_x | <value> at h=<int> | <value> at h=<int> |

### GIRF peak responses (Experiment 2)

| Wedge | Macro peak [5-95%] | Financial peak [5-95%] |
|-------|---------------------|--------------------------|
| log A | <value> [<lo>, <hi>] | <value> [<lo>, <hi>] |
| G/Y | <value> [<lo>, <hi>] | <value> [<lo>, <hi>] |
| τ_ℓ | <value> [<lo>, <hi>] | <value> [<lo>, <hi>] |
| τ_x | <value> [<lo>, <hi>] | <value> [<lo>, <hi>] |

Figures:
- `.../output/bca_lp_fin.png`, `.../output/bca_lp_macro.png`
- `.../output/bca_girf_fin.png`, `.../output/bca_girf_macro.png`

## Three questions for scholars

1. **Which wedge absorbs `ue`?** If τ_x is the only mover, FVGQ translates
   its financial uncertainty into a narrow investment-wedge story —
   consistent with Christiano-Motto-Rostagno-style expectations. If τ_ℓ
   also moves materially, the two-agent segmentation (entrepreneurs
   collateral-constrained vs. workers consuming out of wages) is leaking
   into what CKM reads as a labor-market friction.

2. **How large is the LP vs. GIRF disagreement?** Under linearity and
   ergodicity these should agree. Any wedge where LP and GIRF differ
   substantially is evidence of higher-order nonlinearity in the
   uncertainty-to-wedge transmission — exactly the Insight 1 narrative
   from the 2026-04-24 rationale log.

3. **Do the results support the §7 direction (RA + unified LTV/working-
   capital)?** If FVGQ preliminary already makes τ_ℓ move via segmentation
   alone, the LWZ+CGK refinement in §7 is amplifying rather than creating
   the labor-wedge channel. If τ_ℓ is muted here, §7's working-capital
   channel becomes the *necessary* additional mechanism.

## Caveats (preliminary)

- CKM wedge extraction uses a 5-iteration realized-value fixed point for
  τ_x, not the full CKM (2007) Kalman likelihood estimator. Re-do with
  full CKM before any external claim.
- FVGQ parameters are from their U.S. business-cycle calibration;
  Taiwan-relevant recalibration is out of scope for preliminary.
- Capital utilization margin is present in the DGP but ignored by the
  prototype — some of what CKM attributes to wedges is actually utilization.
```

- [ ] **Step 12.3: Commit**

```bash
MEMO_DATE=$(date +%Y-%m-%d)
git add "llm_logs/${MEMO_DATE}_fvgq2020_preliminary_results.md"
git commit -m "docs: FVGQ 2020 preliminary simulated BCA results memo

Summarizes LP and GIRF wedge signatures for (uA, ue) shocks, poses three
discussion questions for scholars (which wedge absorbs ue, LP-GIRF gap,
§7 implications), flags preliminary caveats (simplified tau_x extraction,
ignored utilization).

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

## Self-Review Checklist

- [x] **Spec coverage:** Every spec section maps to at least one task.
  - Spec §1 Objective → whole plan
  - Spec §2 Scope → Task 1 (folder isolation), NOTES.md documents non-goals
  - Spec §3 Narrative correction → documented in NOTES.md + memo (not code)
  - Spec §4 Folder layout → Task 1
  - Spec §5 .mod adaptation → Task 2
  - Spec §6 Experiment design → Tasks 4-6
  - Spec §7 CKM details → Tasks 7, 9
  - Spec §8 Deliverables → Tasks 4-12 map 1:1 to D1-D5
  - Spec §9 Dependencies → Task 3 (setup_paths)
  - Spec §10 Risks → Task 2 Step 2.3 (Dynare syntax), Task 11 (tripwires)
  - Spec §11 Branch points → memo discussion section
- [x] **Placeholder scan:** No "TBD"/"TODO"/"implement later". One `<today>` in Task 12 is explicitly defined as the current date at execution time. Memo template has `<value>` placeholders that Step 12.1 produces concrete numbers for.
- [x] **Type consistency:** `var_names` in run_fvgq2020_simulation.m is reused by run_bca_analysis.m via load; wedge column names `log_A, G_share, tau_l, tau_x` match across estimator, LP, GIRF, plotting, and sanity_checks. FVGQ variable names (`y, cspt, ivst, labor, k`) are consistent everywhere.

---

## Execution Options

**Plan complete and saved to `docs/superpowers/plans/2026-04-24-fvgq2020-preliminary-simulated-bca.md`.**

Two execution options:

1. **Subagent-Driven (recommended)** — dispatch a fresh subagent per task, review between tasks, fast iteration.
2. **Inline Execution** — execute tasks in this session using `superpowers:executing-plans`, batch execution with checkpoints.

Which approach?

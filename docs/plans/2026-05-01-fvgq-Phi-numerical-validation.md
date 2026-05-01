# FVGQ 2020 $\Phi(\Omega_t)$ Closed-Form: Numerical Validation

**Date:** 2026-05-01
**Companion to:** `2026-05-01-fvgq-Phi-closed-form.md`
**Source artifacts:** `code/bca_uncertainty_simulation/fvgq2020_preliminary/output/simulated_workspace.mat`
**Method:** Read pruned third-order policy matrices (`oo_.dr.gh*`) directly via `h5py`; MATLAB MCP was unresponsive in this session.

---

## 1. Five extracted coefficients

Variables used: $c \equiv$ `cspt` (composite per-capita consumption, the BCA-relevant aggregate);
$r^k \equiv \log(\alpha y_{t+1}/(u_{t+1} k_t) + (1-\delta))$, constructed as `share × (log y − log util)`
with `share = R^k_ss/(R^k_ss + 1 − δ) ≈ 0.0270`. All policy coefficients converted to **log-deviations** by dividing by SS.

The SV state in FVGQ is `sigAt = log σ_A,t` (and `siget = log σ_e,t`). Using
$\sigma_{A,t}^2 = \exp(2\,\mathrm{sigAt})$ so $\mathrm{d}\sigma_A^2/\mathrm{d}\,\mathrm{sigAt} = 2\sigma_{A,\mathrm{ss}}^2$,
the conditional variance/covariance derivatives are mapped as

$$a_{cc,X} = \frac{\partial \mathrm{Var}_t(\hat c_{t+1})}{\partial \sigma_{X,t}^2}\bigg|_\text{ss},\quad
a_{cR,X} = \frac{\partial \mathrm{Cov}_t(\hat c_{t+1},\hat r^k_{t+1})}{\partial \sigma_{X,t}^2}\bigg|_\text{ss}.$$

Computed from $\mathrm{ghu}$ and $\mathrm{ghxu}$ (since FVGQ has SV-in-mean **inside the model equations** as `exp(sigAt)·eA`, the relevant SV-loading lives in `ghxu[c, sigAt, eA]` rather than in `ghuss`/`ghs2`):

| Coefficient | Value |
|---|---|
| $a_{cc,A}$ | $4.844\times 10^{-1}$ |
| $a_{cc,e}$ | $4.115\times 10^{-4}$ |
| $a_{cR,A}$ | $1.886\times 10^{-2}$ |
| $a_{cR,e}$ | $-1.786\times 10^{-4}$ |
| $\nu_\theta$ | $\mathbf{0}$ (see §3 caveat) |

**Sanity check on the SV multiplier:** $\mathrm{ghxu}[c, \mathrm{sigAt}, eA]\, /\, \mathrm{ghu}[c, eA] = 0.7500$ exactly, equal to $\rho_{\sigma_A}$. This is the correct propagation of `sigAt_t` to the conditional std of $\mathrm{eA}\cdot\exp(\mathrm{sigAt}_{t+1})$ through the AR(1) of `sigAt`. The same ratio holds for the `(siget, ethet)` channel — a strong consistency check.

## 2. $\kappa_x$ and comparison with LP

**Calibration as in the .mod file** (note differences from §4 of the closed-form doc):
- $\bar\theta = \mathrm{ssPhi} = 0.0954$ — **NOT** 0.20 as written in the closed-form doc §4. The .mod uses `ssPhi = 0.09539948379`. This affects $1-\bar\theta(1-\delta) = 0.906$ and the collateral coefficient.
- $\rho_{\sigma_A} = \rho_{\sigma_e} = 0.75$ — **NOT** 0.95 as written in §4. This is the largest single difference: with $\omega_\tau = 0.973$, the amplification factor changes from $1/(1-0.973\times 0.95)=13.2$ to $1/(1-0.973\times 0.75)=3.7$.
- $\bar R^k = \alpha y_\mathrm{ss}/k_\mathrm{ss} = 0.0273$.
- $\beta\bar R\bar\theta(1-\delta) = 0.0938$ (about half of doc §4's 0.197 because $\bar\theta$ is half).

**Resulting $\phi$ and $\kappa$:**

| Quantity | Value |
|---|---|
| $\phi_A$ (precaution + risk-premium) | $+8.40\times 10^{-1}$ (precaution dominates) |
| $\phi_e$ (precaution + RP + collateral) | $+1.10\times 10^{-3}$ (collateral $=0$ at this stage) |
| $1 - \omega_\tau \rho_{\sigma}$ | $0.270$ (amplification $\approx 3.7\times$) |
| $\kappa_{x,A}$ | $+1.554$ |
| $\kappa_{x,e}$ | $+2.04\times 10^{-3}$ |

**Translating to LP-comparable units.** A unit `uA` shock raises $\mathrm{sigAt}$ by $\sqrt{1-\rho^2}\,m_{\eta,A}=0.6931$, raising $\sigma_A^2$ by $\Delta\sigma_A^2 = 2\sigma_{A,\mathrm{ss}}^2\cdot 0.6931 = 6.79\times 10^{-5}$. Similarly $\Delta\sigma_e^2 = 9.44\times 10^{-5}$ per unit `ue`.

**Predicted impact response (h=0) of $\hat\tau_x$:**
- $uA \to \hat\tau_x:\ \kappa_{x,A}\Delta\sigma_A^2 = +1.06\times 10^{-4}$
- $ue \to \hat\tau_x:\ \kappa_{x,e}\Delta\sigma_e^2 = +1.93\times 10^{-7}$

**LP measured peaks** (from `2026-04-24_fvgq2020_preliminary_results.md`):
- $uA \to \hat\tau_x:\ -1.642\times 10^{-3}$ at $h=40$
- $ue \to \hat\tau_x:\ +1.886\times 10^{-3}$ at $h=32$

| Channel | Sign predicted | Sign LP | Magnitude ratio (pred/LP, abs) |
|---|---|---|---|
| `uA → τ_x` | **+** | **−** | 0.06 (sign mismatch) |
| `ue → τ_x` | **+** | **+** | 0.0001 (off by ~10 000×) |

Neither channel passes the "within 50 %" magnitude criterion. Sign matches only on `ue`.

## 3. Issues encountered

1. **`ν_θ` could not be extracted at first order.** In FVGQ's mod file, neither `ghx[cspt, siget]` nor `ghxx[cspt, siget, siget]` is non-zero at the saved precision. `siget` (log $\sigma_e$) does not enter the policy function for `cspt` at first order — it only feeds in through the conditional variance of `ethet`. Hence the collateral term $\beta\bar R\bar\theta(1-\delta)\nu_\theta\sigma_{e,t}^2$ in the closed-form is empirically zero at this approximation order. Capturing it requires either (a) reading `ghxxx`/`ghxss` and a careful chain-rule expansion, or (b) Monte Carlo: simulate the pruned policy at perturbed `siget_t` and regress mean log $\lambda_t$ on $\sigma_e^2$. I recommend option (b) as the cleanest fix.

2. **Calibration gap between closed-form doc §4 and .mod.** The doc uses $\bar\theta=0.20,\rho_\sigma=0.95$; the simulation uses $\bar\theta=0.0954,\rho_\sigma=0.75$. The $0.0654 \to 0.270$ jump in the denominator $1-\omega_\tau\rho_\sigma$ alone reduces predicted $\kappa$ magnitudes by ~4×. The doc should be updated to the .mod values, or the .mod should be re-run with the doc's calibration to test that flavor.

3. **MATLAB MCP unresponsive.** All `mcp__MATLAB__*` calls timed out. Fell back to Python `h5py` reading the v7.3 .mat file directly. This works for first- and second-order matrices but makes deeper extractions (third-order chain rules, simulation) more painful. Recommend retrying MATLAB later for the Monte Carlo step.

4. **`r^k` proxy.** No direct `r_k` variable in the model; constructed as `share × (log y − log util)` with `share = R^k_ss/(R^k_ss+1-δ) = 0.0270`. The smallness of this share (because $R^k$ is monthly-ish and $1-\delta$ is huge) makes $a_{cR,*}$ small relative to $a_{cc,*}$, so $\Phi$ is dominated by the precaution term — that's why $\phi_A$ comes out unambiguously positive.

5. **`cspt` is composite consumption** ($\xi c_E + (1-\xi)c_W$), not entrepreneur consumption. The closed-form doc §6 flags that two-agent aggregation introduces a risk-sharing term. With composite consumption, $a_{cc}$ already nets across the two agents, so the predicted sign should be interpreted accordingly.

6. **Sign mismatch on `uA`.** The closed-form predicts $\kappa_{x,A}>0$ (precaution > risk premium). LP shows negative. Possible explanations (in order of likelihood given the data):
   - The actual LP peak is at $h=40$, far past the shock; the IRF likely crosses zero. The h=0 prediction may agree in sign with the LP **at h=0**, with the negative peak emerging from CKM's slow accumulator $\omega_\tau$ wedge dynamics. Suggested next step: extract LP IRF at $h=0$ and at the zero-crossing rather than just the peak.
   - The two-agent risk-sharing term §6 may flip the sign — entrepreneurs disproportionately bear macro uncertainty, and the composite `cspt` averages them.
   - The `r^k` proxy is too noisy; using `q` directly (Tobin's q) might give different `a_{cR}`.

## 4. Recommended next steps

1. **Run a Monte Carlo simulation** on the pruned solution with `siget_t` perturbed at fixed grid values; regress simulated mean log `cspt` on `siget` to extract a non-trivial $\nu_\theta$.
2. **Reconcile the calibration** between the closed-form doc and the .mod (decide canonical values for $\bar\theta$ and $\rho_\sigma$).
3. **Compute LP IRF at $h=0$ and at the zero-crossing**, not just the peak, before declaring sign mismatch.
4. **Re-run with $r^k = \log q + \mathrm{const}$** as an alternative proxy and check robustness of $a_{cR,*}$.
5. **Verify the SV-loading interpretation** of `ghxu[*, sigAt, eA] / ghu[*, eA] = ρ_sigA` analytically — this confirmed pattern is the cleanest empirical anchor for the closed-form derivation.

## 5. Bottom line

- $a_{cc}$ and $a_{cR}$ extracted cleanly; the SV multiplier checks out exactly at $\rho_\sigma = 0.75$.
- $\nu_\theta = 0$ at the first-order/quadratic-in-state extraction used here; need MC.
- Predicted $\kappa_{x,A}$ sign disagrees with LP peak (but maybe agrees at $h=0$).
- Predicted magnitudes are 16× too small (`uA`) and 10⁴× too small (`ue`), driven primarily by the missing $\nu_\theta$ for `ue` and by the calibration/persistence gap for `uA`.
- The closed-form is **structurally correct** (SV-loading pattern matches Dynare exactly), but the calibration in the doc and the missing $\nu_\theta$ both need to be repaired before the numerical comparison is fair.

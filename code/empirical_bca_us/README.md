# Empirical BCA for U.S. Data (Spin-off Research)

This module extracts impulse response functions (IRFs) from pre-estimated U.S. Bayesian SVARs and transforms them into "Empirical Wedges" using the Business Cycle Accounting (BCA) prototype model.

## Purpose

The empirical wedge signatures generated here serve as the **ground-truth target** for structural model selection. By demonstrating that U.S. data exhibits severe deterioration in both labor and investment wedges following an uncertainty shock, we provide a robust benchmark against which theoretical models (e.g., FVGQ 2020 vs. LWZ+CGK) can be evaluated.

## ⚠️ Important Caveats

1. **Investment Variable:** The 22-variable `SVMVAR_AddingHousingPrice` specification uses actual real gross private domestic investment (`GPDIC1`) as variable 3. Durable goods new orders (`AMDMNOx`) remains in the system as variable 14.
2. **IRF Script Matching:** Post-estimation IRFs should use `estimate_IRF_3SV_AddingHousingPrice.m`, whose `tcode` and labels match the 22-variable ordering.
3. **COVID Outlier:** Results including data from 2020 onwards (Full Sample) show highly distorted labor responses due to the massive COVID-19 lockdown outliers. For structural transmission analysis, the **Pre-COVID (1959-2019)** results are highly recommended.

## Workflow & Core Scripts

All paths and external drive locations are centralized in `matlab/get_project_config.m`.

### 1. Generating 2019 Results (Recommended)
- **Step 1:** Run `matlab/run_2019_svar_estimation.m` to re-estimate the SVAR on a sample truncated at 2019:Q4. This generates `data/est_result_2019.mat`.
- **Step 2:** Run `matlab/batch_compute_wedges_2019.m` to perform the BCA transformation on the 25,000 MCMC draws.
- **Step 3:** Run `matlab/plot_empirical_wedges_2019.m` to generate the final figures with 68% credible intervals.

### 2. Generating Full Sample Results
- Run `matlab/batch_compute_wedges_full.m` followed by `matlab/plot_empirical_wedges_ci.m`.

## Credible Intervals
Following Sims and Zha (1999) and standard Bayesian SVAR conventions, we report the **68% Bayesian Credible Interval** (16th and 84th percentiles of the posterior distribution) rather than the standard error of the mean. This correctly reflects parameter uncertainty rather than numerical MCMC error.

## Directory Structure
- `data/`: Extracted MCMC results (Git-ignored).
- `matlab/`: Core processing and plotting scripts.
- `matlab/utils/`: Shared helper for CKM wedge identities.
- `output/`: Final PNG figures and CSV tables (Git-ignored).

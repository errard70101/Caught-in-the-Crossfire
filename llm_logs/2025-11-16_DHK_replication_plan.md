# DHK (2025) Paper Replication Plan

**Date**: 2025-11-16
**Model**: Claude Sonnet 4.5
**Purpose**: Comprehensive plan to replicate "Investigating Economic Uncertainty Using Stochastic Volatility in Mean VARs: The Importance of Model Size, Order-Invariance and Classification"

---

## Executive Summary

This document provides a modular, step-by-step plan to replicate the DHK (2025) paper. The replication will be structured into **8 major modules**, each with specific tasks and deliverables.

**Key Objectives:**
1. Implement the Order-Invariant SVMVAR (OI-SVMVAR) model
2. Develop the novel MCMC algorithm with time-varying classification
3. Replicate the simulation study (Section 3 of paper)
4. Replicate the empirical application with US data (Section 4 of paper)
5. Generate all figures and tables from the paper
6. Create reusable, well-documented code for Taiwan application

**Estimated Timeline**: 3-4 months for full replication

---

## Module Overview

| Module | Purpose | Priority | Complexity | Est. Time |
|--------|---------|----------|------------|-----------|
| M1: Data Collection | Get US data from FRED-MD | P1 | Low | 1 week |
| M2: Model Specification | Implement OI-SVMVAR equations | P1 | Medium | 2 weeks |
| M3: MCMC Algorithm | Novel sampler implementation | P1 | High | 4 weeks |
| M4: Simulation Study | Validate algorithm | P2 | Medium | 2 weeks |
| M5: Empirical Application | Run models on US data | P2 | Medium | 2 weeks |
| M6: Analysis Tools | IRFs, FEVDs, decompositions | P2 | Medium | 2 weeks |
| M7: Visualization | Replicate all figures | P3 | Low | 1 week |
| M8: Documentation | Code docs and user guide | P3 | Low | 1 week |

**Critical Path**: M1 → M2 → M3 → M4 → M5 → M6 → M7

---

## Detailed Module Breakdown

## Module 1: Data Collection and Processing

### M1.1: Obtain FRED-MD Dataset
**Files**: `code/data_processing/01_download_fredmd.R` or `.py`

**Tasks:**
1. Download FRED-MD dataset (monthly, 1960-2021)
2. Extract the 43 variables used in the paper (see Online Appendix B)
3. Apply transformations (log, first difference, etc.)
4. Handle missing values
5. Standardize data (zero mean, unit variance)

**Key Variables** (from paper):
- **Macro variables (18)**: Industrial production, employment, prices, orders, etc.
- **Financial variables (12)**: S&P 500, interest rates, credit spread, etc.
- **Unclassified (13)**: Federal funds rate, S&P 500 returns, credit spread, monetary aggregates, exchange rates

**Outputs:**
- `data/processed/fredmd_raw.csv` - Raw FRED-MD data
- `data/processed/fredmd_transformed.csv` - After transformations
- `data/processed/fredmd_standardized.csv` - Standardized for estimation
- `data/processed/variable_classification.csv` - Classification scheme

**Data Appendix Reference**: Online Appendix B contains full variable list

---

### M1.2: Create Smaller Dataset for Testing
**Files**: `code/data_processing/02_create_test_data.R`

**Tasks:**
1. Create 6-variable subset for quick testing
2. Create 30-variable dataset (CCM baseline)
3. Save in multiple formats (.csv, .RData, .mat)

**Outputs:**
- `data/processed/test_6var.csv`
- `data/processed/ccm_30var.csv`
- `data/processed/oi_tvc_43var.csv`

---

## Module 2: Model Specification

### M2.1: Core Model Equations
**Files**: `code/DHK_original/model/svmvar_equations.R`

**Tasks:**
1. Implement Equation (1): VAR with SV in mean
   - `yt = Σ Bi*yt-i + Σ Aj*ht-j + B0^(-1)*εt`
2. Implement Equations (3)-(5): Volatility decomposition
   - Macro: `ωm_i,t = ηm_i,t + hm,t`
   - Financial: `ωf_i,t = ηf_i,t + hf,t`
   - Unclassified: `ωu_i,t = ηu_i,t + hs_i,t,t` (depends on indicator si,t)
3. Implement Equation (6): Common volatility dynamics
   - `ht = Σ Φi*ht-i + Σ Ψj*yt-j + εh`
4. Implement Equation (7): Idiosyncratic volatilities
   - `ηk_i,t = μk,i + ρk,i*ηk_i,t-1 + εk_i,t`

**Key Features:**
- B0 is **unrestricted** (not lower triangular) → order-invariant
- Diagonal of B0 restricted to 1 → point-identified
- Time-varying classification via Markov-switching si,t

**Outputs:**
- Model structure object
- Prior specification functions
- Log-posterior functions

---

### M2.2: Prior Specification
**Files**: `code/DHK_original/model/priors.R`

**Tasks:**
1. Implement Horseshoe prior for B0 (sparsity)
2. Minnesota-style priors for VAR coefficients
3. Priors for volatility parameters
4. Markov transition probabilities

**Reference**: Online Appendix A1

---

## Module 3: MCMC Algorithm Implementation

This is the **most complex** module. The paper develops a novel algorithm.

### M3.1: Sampling B0 (Order-Invariant)
**Files**: `code/DHK_original/mcmc/sample_B0.R`

**Tasks:**
1. Implement parameter transformation (Equation 14-15)
2. Sample w1 from absolute normal (Proposition 1)
3. Sample w_-1 from Gaussian conditional
4. Transform back to b0,i

**Key Innovation**: This is the novel contribution that allows order-invariance while maintaining point-identification

**Reference**: Section 2.2, Equations (8)-(18), Proposition 1

---

### M3.2: Sampling Log-Volatilities
**Files**: `code/DHK_original/mcmc/sample_volatilities.R`

**Tasks:**
1. Implement CHKP (2023) efficient sampler
2. Use band and sparse matrix algorithms
3. Independent Acceptance-Rejection Metropolis-Hastings step
4. Sample all log-volatilities in single block

**Reference**: Cross et al. (2023) CHKP algorithm

**Note**: This step is computationally intensive (~30 hours for 43-variable model)

---

### M3.3: Sampling Classification Indicators
**Files**: `code/DHK_original/mcmc/sample_classification.R`

**Tasks:**
1. Given h1,...,hT, sample si,1,...,si,T for each unclassified variable
2. Use Chib (1996) algorithm for Markov-switching
3. Sample Markov transition probabilities (pi_m,m, pi_m,f, pi_f,m, pi_f,f)

**Key Feature**: Time-varying classification allows variables to switch between macro/financial blocks

**Reference**: Section 2.2, Equation (5)

---

### M3.4: Sampling VAR Coefficients
**Files**: `code/DHK_original/mcmc/sample_var_coefs.R`

**Tasks:**
1. Sample B1,...,Bp (VAR coefficients)
2. Sample A0,...,Aq (volatility-in-mean coefficients)
3. Use conditional posterior with Minnesota prior

---

### M3.5: Sampling Volatility Dynamics
**Files**: `code/DHK_original/mcmc/sample_h_dynamics.R`

**Tasks:**
1. Sample Φ1,...,Φph (VAR coefficients for ht)
2. Sample Ψ1,...,Ψpy (coefficients linking yt to ht)
3. Sample Σh (covariance matrix)

**Reference**: Equation (6)

---

### M3.6: Sampling Idiosyncratic Volatilities
**Files**: `code/DHK_original/mcmc/sample_idiosyncratic.R`

**Tasks:**
1. Sample μk,i, ρk,i, σ²k,i for each variable
2. Use auxiliary mixture sampler (Kim, Shephard, Chib 1998)

**Reference**: Equation (7)

---

### M3.7: Main MCMC Loop
**Files**: `code/DHK_original/mcmc/mcmc_main.R`

**Tasks:**
1. Initialize all parameters
2. Run MCMC for M iterations
3. Implement convergence diagnostics
4. Save draws efficiently
5. Monitor acceptance rates

**Pseudo-code:**
```r
for (m in 1:M) {
  # 1. Sample B0 (novel algorithm)
  B0 <- sample_B0(...)

  # 2. Sample classification indicators
  class_indicators <- sample_classification(...)

  # 3. Transform model based on classification
  # (reorder equations so unclassified variables
  #  are grouped with appropriate block)

  # 4. Sample log-volatilities (CHKP algorithm)
  h <- sample_volatilities(...)

  # 5. Sample VAR coefficients
  B_coefs <- sample_var_coefs(...)
  A_coefs <- sample_volatility_in_mean_coefs(...)

  # 6. Sample volatility dynamics
  Phi <- sample_h_var_coefs(...)
  Psi <- sample_h_y_coefs(...)
  Sigma_h <- sample_h_covariance(...)

  # 7. Sample idiosyncratic volatilities
  eta_params <- sample_idiosyncratic(...)

  # Save draws
  save_draws(m, ...)
}
```

**Computational Notes:**
- 30-variable model: ~10 hours per run (15,000 draws)
- 43-variable model: ~30 hours per run
- Requires high-performance computing or optimized code

---

## Module 4: Simulation Study

**Purpose**: Replicate Section 3 of the paper to validate algorithm

### M4.1: Generate Synthetic Data
**Files**: `code/DHK_original/simulation/01_generate_data.R`

**Tasks:**
1. Set up 23-variable DGP (Data Generating Process)
   - nm = 10 macro variables
   - nf = 10 financial variables
   - nu = 3 unclassified variables
2. Generate true parameters:
   - B0: full nonzero matrix (diagonal = 1, off-diagonal ~ N(0, 0.2))
   - B1: diagonal ~ U(0,0.6), off-diagonal ~ U(-0.2,0.2)
   - Bi, i>1: ~ N(0, 0.12/i²)
3. Set classification:
   - s1,t = m (always macro)
   - s3,t = f (always financial)
   - s2,t = f for t=1-200, 401-600; s2,t = m for t=201-400
4. Generate T=600 observations

**Reference**: Section 3.1

**Outputs:**
- `results/simulation/true_parameters.RData`
- `results/simulation/simulated_data.csv`

---

### M4.2: Estimate Four Models
**Files**: `code/DHK_original/simulation/02_estimate_models.R`

**Models** (Table 1):
1. **CCM-6**: 6 variables, lower triangular B0
2. **OI-6**: 6 variables, unrestricted B0 (order-invariant)
3. **CCM-TVC-23**: 23 variables, time-varying classification, lower triangular B0
4. **OI-TVC-23**: 23 variables, time-varying classification, unrestricted B0 (TRUE MODEL)

**Tasks:**
- Run MCMC for each model (15,000 draws, 5,000 burn-in)
- Save posterior draws
- Compute convergence diagnostics

**Outputs:**
- `results/simulation/CCM_6_posterior.RData`
- `results/simulation/OI_6_posterior.RData`
- `results/simulation/CCM_TVC_23_posterior.RData`
- `results/simulation/OI_TVC_23_posterior.RData`

---

### M4.3: Generate Simulation Figures
**Files**: `code/DHK_original/simulation/03_simulation_figures.R`

**Figure 1**: Uncertainty estimates (e^(0.5*hm,t) and e^(0.5*hf,t))
- Compare all 4 models vs. true values
- Show OI-TVC-23 recovers truth; others deviate

**Figure 2**: Impulse responses (6 common variables)
- One SD macro uncertainty shock (top panel)
- One SD financial uncertainty shock (bottom panel)
- Plot posterior medians + 70% credible intervals
- Compare all 4 models vs. true responses

**Figure 3**: Classification probabilities
- Plot p(si,t = m | y) for 3 unclassified variables
- Show algorithm correctly detects constant and time-varying classification

**Outputs:**
- `figures/simulation/figure1_uncertainty_estimates.pdf`
- `figures/simulation/figure2_impulse_responses.pdf`
- `figures/simulation/figure3_classification.pdf`

---

## Module 5: Empirical Application (US Data)

**Purpose**: Replicate Section 4 of the paper

### M5.1: Estimate Six Models
**Files**: `code/DHK_original/empirical/01_estimate_models.R`

**Models** (Table 2):
1. **CCM-30**: 30 variables, lower triangular, pre-classified
2. **OI-30**: 30 variables, unrestricted B0, pre-classified
3. **CCM-TVC-43**: 43 variables, lower triangular, time-varying classification
4. **OI-TVC-43**: 43 variables, unrestricted B0, time-varying classification (MAIN MODEL)
5. **CCM-TVC-RO-43**: Same as #3 but reversed variable ordering
6. **OI-TVC-RO-43**: Same as #4 but reversed variable ordering

**Computational Requirements:**
- CCM-30, OI-30: ~10 hours each
- CCM-TVC-43, OI-TVC-43: ~30 hours each
- Total: ~100 hours of computation

**Strategy**: Run models in parallel if possible; otherwise sequential

**Outputs:**
- `results/empirical/CCM_30_posterior.RData`
- `results/empirical/OI_30_posterior.RData`
- ... (6 total)

---

### M5.2: Variable Classification
**Files**: `code/DHK_original/empirical/02_classify_variables.R`

**Classification Scheme:**

**Macro (18 variables):**
- PAYEMS, INDPRO, CUMFNS, MANEMP, UNRATE, PPI, CES0600000007, HOUST
- PERMITNFS, AMDMNO, W875RX1, NAPM, FEDFUNDS (wait, FFR is unclassified in 43-var!)
- Need to check Online Appendix B carefully

**Financial (12 variables):**
- S&P 500, TB3MS, GS10, BAA10Y, EXSZUS, EXUSUKx
- Check appendix for full list

**Unclassified (13 variables in 43-var model):**
- Federal Funds Rate (FEDFUNDS)
- S&P 500 (S&P 500)
- Credit Spread (BAA10Y)
- M1REAL, M2REAL, CONSUMER, BUSLOANS, NONREVSL
- RHPI, GS10TB3Mx, TB3SMFFM, AAA FFM, EXSZUSx, EXUSUKx, EXCAUSx

**Reference**: Online Appendix B (Data Appendix)

---

## Module 6: Analysis Tools

### M6.1: Impulse Response Functions
**Files**: `code/DHK_original/analysis/01_compute_irfs.R`

**Tasks:**
1. Compute IRFs to macro uncertainty shock (εh_m,t)
2. Compute IRFs to financial uncertainty shock (εh_f,t)
3. Identification: Lower triangular L matrix
   - Macro uncertainty affects financial contemporaneously
   - Financial affects macro with lag
4. Compute cumulated IRFs (rescale using standardization)
5. Compute posterior medians and credible intervals

**Reference**: Figure 5, Figure 6, Figure 8

**Outputs:**
- `results/analysis/irfs_macro_shock.RData`
- `results/analysis/irfs_financial_shock.RData`

---

### M6.2: Forecast Error Variance Decomposition
**Files**: `code/DHK_original/analysis/02_compute_fevd.R`

**Tasks:**
1. Decompose variance of each variable into:
   - Contribution from macro uncertainty shock
   - Contribution from financial uncertainty shock
   - Contribution from VAR shocks
2. Compute at different horizons (h=1,6,12,24,36,48 months)
3. Report posterior medians

**Reference**: Online Appendix C2, Figure 15

**Outputs:**
- `results/analysis/fevd.csv`
- `tables/fevd_table.tex`

---

### M6.3: Historical Decomposition
**Files**: `code/DHK_original/analysis/03_historical_decomp.R`

**Tasks:**
1. Decompose historical variation in each variable
2. Attribute to different shocks over time
3. Focus on key variables (industrial production, unemployment)

**Reference**: Online Appendix C2, Figure 14

**Outputs:**
- `results/analysis/historical_decomp.RData`

---

### M6.4: Classification Analysis
**Files**: `code/DHK_original/analysis/04_analyze_classification.R`

**Tasks:**
1. Extract posterior probabilities p(si,t = m | y)
2. Determine classification at each time point
3. Identify regime switches
4. Match with known crisis periods (2008, 2020, etc.)

**Reference**: Figure 9

**Outputs:**
- `results/analysis/classification_probabilities.csv`
- `results/analysis/regime_switches.csv`

---

## Module 7: Visualization

### M7.1: Main Paper Figures
**Files**: `code/DHK_original/visualization/`

**Figure 1**: Simulation uncertainty estimates (OI-6 vs CCM-6, OI-TVC-23 vs CCM-TVC-23)
**Figure 2**: Simulation IRFs (all 4 models)
**Figure 3**: Simulation classification probabilities
**Figure 4**: Empirical uncertainty estimates (model size comparison)
**Figure 5**: Empirical IRFs (OI-30 vs OI-TVC-43)
**Figure 6**: Empirical IRFs (OI-30 vs CCM-30)
**Figure 7**: Empirical uncertainty estimates (order dependence)
**Figure 8**: Empirical IRFs (CCM-TVC-43 vs CCM-30)
**Figure 9**: Empirical time-varying classification

**Tasks:**
- Replicate exact formatting, colors, layout
- Use ggplot2 (R) or matplotlib (Python)
- Save as high-resolution PDF

**Outputs:**
- `figures/main/figure_1.pdf` through `figure_9.pdf`

---

### M7.2: Supplementary Figures
**Files**: `code/DHK_original/visualization/supplementary_figures.R`

**Online Appendix Figures:**
- Figure 11: Differences in responses (OI-TVC-43 vs OI-30)
- Figure 12: Differences in responses (CCM-30 vs OI-30)
- Figure 13: Differences in responses (CCM-TVC-43 vs OI-TVC-43)
- Figure 14: Historical decompositions
- Figure 15: FEVDs
- Figure 16-18: Additional robustness checks

**Outputs:**
- `figures/supplementary/figure_11.pdf` through `figure_18.pdf`

---

## Module 8: Documentation and Validation

### M8.1: Code Documentation
**Files**: `code/DHK_original/README.md`

**Tasks:**
1. Document each function with:
   - Purpose
   - Inputs/outputs
   - Mathematical equation reference
   - Example usage
2. Create master README for DHK replication
3. Document computational requirements

---

### M8.2: Validation and Testing
**Files**: `code/DHK_original/tests/`

**Tasks:**
1. Unit tests for each MCMC step
2. Integration tests for full model
3. Compare results with published figures
4. Document any discrepancies

**Outputs:**
- `code/DHK_original/tests/test_suite.R`
- `docs/validation_report.md`

---

### M8.3: User Guide
**Files**: `docs/DHK_replication_guide.md`

**Contents:**
1. How to run simulation study
2. How to run empirical application
3. How to modify for Taiwan data
4. Computational tips and tricks
5. Troubleshooting common errors

---

## Folder Structure for Replication

```
code/DHK_original/
├── README.md                           # Main documentation
├── data_processing/
│   ├── 01_download_fredmd.R
│   ├── 02_transform_data.R
│   ├── 03_standardize_data.R
│   └── 04_create_subsets.R
├── model/
│   ├── svmvar_equations.R             # Equations (1)-(7)
│   ├── priors.R                        # Prior specifications
│   └── utilities.R                     # Helper functions
├── mcmc/
│   ├── mcmc_main.R                     # Main MCMC loop
│   ├── sample_B0.R                     # Novel B0 sampler
│   ├── sample_volatilities.R           # CHKP algorithm
│   ├── sample_classification.R         # Time-varying classification
│   ├── sample_var_coefs.R              # VAR coefficients
│   ├── sample_h_dynamics.R             # Volatility dynamics
│   ├── sample_idiosyncratic.R          # Idiosyncratic volatilities
│   └── diagnostics.R                   # Convergence checks
├── simulation/
│   ├── 01_generate_data.R
│   ├── 02_estimate_models.R
│   ├── 03_simulation_figures.R
│   └── 04_simulation_tables.R
├── empirical/
│   ├── 01_estimate_models.R
│   ├── 02_classify_variables.R
│   └── 03_robustness_checks.R
├── analysis/
│   ├── 01_compute_irfs.R
│   ├── 02_compute_fevd.R
│   ├── 03_historical_decomp.R
│   └── 04_analyze_classification.R
├── visualization/
│   ├── main_figures.R
│   ├── supplementary_figures.R
│   └── plotting_utilities.R
└── tests/
    ├── test_mcmc_steps.R
    ├── test_model_equations.R
    └── test_suite.R

data/processed/
├── fredmd_raw.csv
├── fredmd_transformed.csv
├── fredmd_standardized.csv
├── variable_classification.csv
├── test_6var.csv
├── ccm_30var.csv
└── oi_tvc_43var.csv

results/
├── simulation/
│   ├── true_parameters.RData
│   ├── simulated_data.csv
│   ├── CCM_6_posterior.RData
│   ├── OI_6_posterior.RData
│   ├── CCM_TVC_23_posterior.RData
│   └── OI_TVC_23_posterior.RData
├── empirical/
│   ├── CCM_30_posterior.RData
│   ├── OI_30_posterior.RData
│   ├── CCM_TVC_43_posterior.RData
│   ├── OI_TVC_43_posterior.RData
│   ├── CCM_TVC_RO_43_posterior.RData
│   └── OI_TVC_RO_43_posterior.RData
└── analysis/
    ├── irfs_macro_shock.RData
    ├── irfs_financial_shock.RData
    ├── fevd.csv
    ├── historical_decomp.RData
    └── classification_probabilities.csv

figures/
├── main/
│   ├── figure_1.pdf (through figure_9.pdf)
└── supplementary/
    └── figure_11.pdf (through figure_18.pdf)

docs/
├── DHK_replication_guide.md
├── validation_report.md
├── computational_notes.md
└── taiwan_adaptation_guide.md
```

---

## Implementation Priorities and Phases

### Phase 1: Foundation (Weeks 1-2)
- **M1**: Data collection and processing
- **M2.1**: Core model equations
- Test with simple examples

### Phase 2: Core Algorithm (Weeks 3-6)
- **M3**: Full MCMC implementation
- **M2.2**: Priors
- Test on small synthetic data

### Phase 3: Validation (Weeks 7-8)
- **M4**: Complete simulation study
- Verify algorithm recovers true parameters
- Debug and optimize

### Phase 4: Application (Weeks 9-11)
- **M5**: Empirical application
- **M6**: Analysis tools
- Run all 6 models

### Phase 5: Finalization (Weeks 12-13)
- **M7**: All visualizations
- **M8**: Documentation
- Comparison with published results

---

## Programming Language Recommendations

### Option 1: R (Recommended)
**Pros:**
- Excellent for Bayesian econometrics
- MCMC packages: `MCMCpack`, `coda`
- Matrix operations: `Matrix`, `spam` (for sparse/band matrices)
- Visualization: `ggplot2`
- Most econometrics replication code is in R

**Cons:**
- Slower than compiled languages for large loops

**Recommended packages:**
```r
install.packages(c(
  "Matrix",        # Sparse/band matrices
  "spam",          # Sparse matrices
  "MCMCpack",      # MCMC utilities
  "coda",          # Convergence diagnostics
  "mvtnorm",       # Multivariate normal
  "ggplot2",       # Visualization
  "readxl",        # Data import
  "dplyr",         # Data manipulation
  "tidyr"          # Data tidying
))
```

### Option 2: MATLAB
**Pros:**
- Fast matrix operations
- Many VAR toolboxes available
- May be what DHK authors used

**Cons:**
- Expensive license
- Less flexible than R for data manipulation

### Option 3: Python
**Pros:**
- Free and open-source
- NumPy/SciPy for numerical computing
- Good for integration with Taiwan project

**Cons:**
- Fewer Bayesian econometrics packages
- Requires more custom code

**Recommendation**: Start with R for replication, then port to Python for Taiwan application if needed.

---

## Computational Considerations

### Hardware Requirements
- **RAM**: Minimum 16 GB, recommended 32 GB for 43-variable model
- **CPU**: Multi-core processor (algorithm is single-threaded but can run multiple chains)
- **Storage**: ~50 GB for all results
- **Time**: Plan for 100+ hours of computation

### Optimization Strategies
1. **Start small**: Test on 6-variable model first
2. **Use sparse matrices**: Critical for large models
3. **Parallelize chains**: Run multiple MCMC chains in parallel
4. **Save selectively**: Don't save every parameter at every iteration
5. **Monitor convergence**: Use Geweke, Gelman-Rubin diagnostics

### HPC Considerations
If running on cluster:
- Submit separate jobs for each model
- Use job arrays for multiple chains
- Save intermediate results
- Use checkpointing for long runs

---

## Key Technical Challenges

### Challenge 1: Sampling B0
**Difficulty**: High
**Why**: Novel algorithm not implemented anywhere else
**Solution**: Study Section 2.2 and Proposition 1 carefully; implement step-by-step

### Challenge 2: Sampling Log-Volatilities
**Difficulty**: High
**Why**: Requires CHKP (2023) algorithm with band matrices
**Solution**: Study CHKP paper; use sparse matrix packages; test on small examples

### Challenge 3: Time-Varying Classification
**Difficulty**: Medium
**Why**: Markov-switching requires careful indexing
**Solution**: Use Chib (1996) filter; test on simple 2-state example first

### Challenge 4: Computational Speed
**Difficulty**: Medium-High
**Why**: 43-variable model takes 30 hours
**Solution**: Optimize matrix operations; use compiled code where possible; parallelize

### Challenge 5: Convergence Diagnostics
**Difficulty**: Medium
**Why**: High-dimensional parameter space
**Solution**: Monitor key parameters; use thinning; run long chains

---

## Success Criteria

### Minimal Success
- [ ] Algorithm runs without errors
- [ ] Recovers truth in simulation study
- [ ] Generates uncertainty estimates for US data

### Target Success (Full Replication)
- [ ] All simulation figures match paper (Figures 1-3)
- [ ] All empirical figures match paper (Figures 4-9)
- [ ] All results qualitatively consistent with paper
- [ ] Documented, reusable code

### Stretch Goals
- [ ] Numerical results match paper to 2 decimal places
- [ ] Faster implementation than paper (through optimization)
- [ ] Extended to Taiwan data
- [ ] Robustness checks beyond paper

---

## Relationship to Taiwan Project

This DHK replication serves as **Phase 2.1** of the Taiwan project:

**Phase 0**: Literature review ✅ (Completed)
**Phase 1**: Data collection (In progress)
**Phase 2.1**: DHK replication (This plan) ← **WE ARE HERE**
**Phase 2.2**: Taiwan model adaptation
**Phase 3**: Taiwan estimation
**Phase 4**: Taiwan analysis
**Phase 5**: Writing

**Key Differences for Taiwan Application:**
1. **Variables**: Taiwan macro/financial + US/China/global (external)
2. **Classification**: External variables → unclassified
3. **Sample**: 1990-2025 (Taiwan data availability)
4. **Research question**: Transmission channels, not uncertainty dominance

---

## Next Steps

### Immediate Actions (This Week)
1. ✅ Review this plan with user
2. ⬜ Decide on programming language (recommend R)
3. ⬜ Contact DHK authors for replication code (Task-006 in ACTIVE_TASKS.md)
4. ⬜ Download FRED-MD data (M1.1)
5. ⬜ Set up development environment

### Week 1-2
- Complete M1 (Data collection)
- Begin M2.1 (Model equations)
- Study CHKP (2023) paper for algorithm details

### Week 3-4
- Continue M3 (MCMC algorithm)
- Test on synthetic data
- Debug

---

## References for Implementation

### Primary Reference
- Davidson, Hou, Koop (2025) - Main paper + Online Appendix

### MCMC Algorithm
- Cross et al. (2023) "Large Stochastic Volatility in Mean VARs" - CHKP algorithm
- Chib (1996) - Markov-switching sampler
- Kim, Shephard, Chib (1998) - SV sampler

### Order-Invariance
- Chan, Koop, Yu (2024) - Order-invariant VARs
- Bertsche & Braun (2022) - Identification by heteroskedasticity

### Priors
- Villani (2009) - Absolute normal mixture approximation

### Matrix Computation
- Golub & Van Loan - Matrix Computations (for band matrices)

---

## Questions for User

1. **Language preference**: R, MATLAB, or Python?
2. **Timeline**: Is 3-4 months acceptable, or need faster results?
3. **Computing resources**: Do you have access to HPC cluster?
4. **Priority**: Full replication first, or jump to Taiwan application?
5. **Collaboration**: Will you be running code, or should I provide complete documentation?

---

## Conclusion

This plan provides a comprehensive roadmap for replicating DHK (2025). The modular structure allows for:
- **Incremental progress**: Each module can be completed independently
- **Testing**: Validate at each stage before proceeding
- **Reusability**: Code can be adapted for Taiwan application
- **Collaboration**: Clear task assignments for team members or AI assistance

The critical path is M1 → M2 → M3, with M4 serving as essential validation before moving to empirical work.

**Estimated effort**: 300-400 hours of focused work for complete replication.

**Timeline**: 3-4 months working steadily, or 1-2 months with dedicated effort and HPC resources.

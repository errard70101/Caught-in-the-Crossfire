# DHK (2025) Replication Code

This directory contains code for replicating:

**"Investigating Economic Uncertainty Using Stochastic Volatility in Mean VARs: The Importance of Model Size, Order-Invariance and Classification"**

by Davidson, Hou, and Koop (2025), *Journal of Business & Economic Statistics*

---

## Quick Start

### For R Users

```r
# 1. Install required packages
source("setup/install_packages.R")

# 2. Download FRED-MD data
source("data_processing/01_download_fredmd.R")

# 3. Run simulation study
source("simulation/run_all_simulations.R")

# 4. Run empirical application
source("empirical/run_all_empirical.R")
```

### For Python Users

```python
# Coming soon...
```

---

## What This Replication Includes

### ✅ Full Replication
- **Simulation Study** (Section 3): 4 models, 23 variables, T=600
- **Empirical Application** (Section 4): 6 models, 30-43 variables, US data 1960-2021
- **All Figures**: Figures 1-9 (main paper) + supplementary figures
- **All Tables**: Convergence diagnostics, FEVD tables

### 🔬 Novel Methodology Implemented
1. **Order-Invariant B0 Sampling** - New parameter transformation algorithm
2. **Time-Varying Classification** - Markov-switching for unclassified variables
3. **Efficient Volatility Sampling** - CHKP (2023) algorithm with sparse matrices
4. **Large-Scale Estimation** - 43 variables, ~30 hours computation time

---

## Directory Structure

```
DHK_original/
├── README.md                    # This file
├── MODULE_INSTRUCTIONS.md       # Detailed technical instructions
│
├── data_processing/             # Module 1
│   ├── 01_download_fredmd.R     # Get FRED-MD dataset
│   ├── 02_transform_data.R      # Apply transformations
│   ├── 03_standardize_data.R    # Standardize (zero mean, unit var)
│   └── 04_create_subsets.R      # Create 6/30/43 variable datasets
│
├── model/                       # Module 2
│   ├── svmvar_equations.R       # Equations (1)-(7)
│   ├── priors.R                 # Prior specifications
│   └── utilities.R              # Helper functions
│
├── mcmc/                        # Module 3 - CORE ALGORITHMS
│   ├── mcmc_main.R              # Main MCMC loop
│   ├── sample_B0.R              # ⭐ Novel order-invariant B0 sampler
│   ├── sample_volatilities.R    # ⭐ CHKP algorithm
│   ├── sample_classification.R  # ⭐ Time-varying classification
│   ├── sample_var_coefs.R       # VAR coefficients
│   ├── sample_h_dynamics.R      # Volatility dynamics
│   ├── sample_idiosyncratic.R   # Idiosyncratic volatilities
│   └── diagnostics.R            # Convergence checks
│
├── simulation/                  # Module 4
│   ├── 01_generate_data.R       # DGP for simulation
│   ├── 02_estimate_models.R     # Estimate 4 models
│   ├── 03_simulation_figures.R  # Figures 1-3
│   └── run_all_simulations.R    # Master script
│
├── empirical/                   # Module 5
│   ├── 01_estimate_models.R     # Estimate 6 models (30/43 vars)
│   ├── 02_classify_variables.R  # Variable classification
│   ├── run_all_empirical.R      # Master script
│   └── config_empirical.R       # Model specifications
│
├── analysis/                    # Module 6
│   ├── 01_compute_irfs.R        # Impulse response functions
│   ├── 02_compute_fevd.R        # Variance decompositions
│   ├── 03_historical_decomp.R   # Historical decompositions
│   └── 04_analyze_classification.R  # Time-varying classification
│
├── visualization/               # Module 7
│   ├── main_figures.R           # Figures 1-9
│   ├── supplementary_figures.R  # Appendix figures
│   └── plotting_utilities.R     # Helper functions
│
├── tests/                       # Module 8
│   ├── test_mcmc_steps.R        # Unit tests for MCMC
│   ├── test_model_equations.R   # Verify equations
│   └── test_suite.R             # Run all tests
│
└── setup/
    ├── install_packages.R       # Install dependencies
    └── config.R                 # Global configuration
```

---

## Key Technical Features

### 1. Order-Invariant B0 Estimation
**Problem**: Traditional VAR models use Cholesky decomposition → results depend on variable ordering

**Solution** (DHK innovation):
- B0 is **unrestricted** (diagonal = 1, off-diagonal free)
- Point-identified (not set-identified)
- Novel MCMC sampler using parameter transformation
- Results invariant to variable ordering

**Implementation**: `mcmc/sample_B0.R`

### 2. Time-Varying Classification
**Problem**: Should FFR, S&P 500, credit spread be "macro" or "financial"?

**Solution**:
- Let data decide via time-varying classification
- Variables can switch between macro/financial blocks
- Uses Markov-switching (Chib 1996)

**Implementation**: `mcmc/sample_classification.R`

### 3. Efficient Large-Scale Estimation
**Problem**: 43-variable SVMVAR is computationally prohibitive

**Solution**:
- Use CHKP (2023) algorithm
- Exploit band/sparse matrix structure
- Sample all volatilities in single block
- Still takes ~30 hours per model!

**Implementation**: `mcmc/sample_volatilities.R`

---

## Computational Requirements

### Hardware
- **RAM**: Minimum 16 GB, recommended 32 GB
- **CPU**: Multi-core (can run multiple chains in parallel)
- **Storage**: ~50 GB for all results
- **Time**:
  - Simulation study: ~10 hours
  - 30-variable models: ~10 hours each
  - 43-variable models: ~30 hours each
  - **Total**: ~120 hours

### Software
**R** (recommended):
```r
# Required packages
install.packages(c(
  "Matrix",      # Sparse matrices
  "spam",        # Band matrices (critical for speed!)
  "mvtnorm",     # Multivariate normal
  "MCMCpack",    # MCMC utilities
  "coda",        # Diagnostics
  "ggplot2",     # Visualization
  "dplyr", "tidyr"  # Data manipulation
))
```

**MATLAB** (alternative):
- Optimization Toolbox
- Statistics Toolbox
- Econometrics Toolbox

**Python** (future):
- NumPy, SciPy, pandas
- PyMC or Stan (for MCMC)

---

## Running the Replication

### Step 1: Data Collection (1 hour)
```r
source("data_processing/01_download_fredmd.R")
source("data_processing/02_transform_data.R")
source("data_processing/03_standardize_data.R")
```

**Output**: `data/processed/fredmd_standardized.csv`

### Step 2: Simulation Study (10 hours)
```r
source("simulation/run_all_simulations.R")
```

**Output**:
- `results/simulation/CCM_6_posterior.RData`
- `results/simulation/OI_TVC_23_posterior.RData` (and 2 others)
- `figures/simulation/figure_1.pdf` (and 2 others)

### Step 3: Empirical Application (110 hours)
```r
# Run all 6 models (will take ~5 days on single machine!)
source("empirical/run_all_empirical.R")

# OR run models individually
source("empirical/01_estimate_models.R")  # Customize which model
```

**Output**:
- `results/empirical/OI_TVC_43_posterior.RData` (and 5 others)

### Step 4: Analysis & Figures (2 hours)
```r
source("analysis/01_compute_irfs.R")
source("analysis/02_compute_fevd.R")
source("visualization/main_figures.R")
```

**Output**:
- `figures/main/figure_4.pdf` through `figure_9.pdf`

---

## Validation

### How to Check if Replication is Correct

1. **Simulation Study**:
   - [ ] Figure 1: OI-TVC-23 uncertainty tracks true values
   - [ ] Figure 2: OI-TVC-23 IRFs match true responses
   - [ ] Figure 3: Classification probabilities correct

2. **Empirical Application**:
   - [ ] Figure 4: Uncertainty spikes during 2008, 2020
   - [ ] Figure 5: OI-TVC-43 shows financial uncertainty matters
   - [ ] Figure 7: Order-dependence clearly visible
   - [ ] Figure 9: Classification changes during crises

3. **Numerical Checks**:
   - [ ] Acceptance rates: B0 (30-50%), volatilities (20-40%)
   - [ ] Convergence: Geweke < 2, Gelman-Rubin < 1.1
   - [ ] Posterior medians within credible intervals

---

## Troubleshooting

### Common Issues

**1. Memory error during volatility sampling**
```r
# Solution: Use sparse matrices
library(spam)
# Ensure sample_volatilities.R uses spam package
```

**2. MCMC not converging**
```r
# Solution: Run longer chains
mcmc_spec$n_iter <- 30000  # Instead of 15000
mcmc_spec$burn_in <- 10000  # Instead of 5000
```

**3. B0 sampling very slow**
```r
# Solution: Tune proposal variance
# In sample_B0.R, adjust tuning parameter
```

**4. Code crashes on large model (43 vars)**
```r
# Solution: Reduce memory usage
# Save only thinned draws
mcmc_spec$thin <- 5  # Save every 5th draw
```

---

## Adapting for Taiwan Application

This replication serves as foundation for Taiwan project. Key modifications needed:

### Data Changes
```r
# Replace US variables with:
- Taiwan macro: IPI, CPI, unemployment, exports
- Taiwan financial: TAIEX, interest rates, TWD/USD
- External (unclassified): US, China, global variables
```

### Model Changes
```r
# Keep same structure, but:
- nm: Taiwan macro variables
- nf: Taiwan financial variables
- nu: US + China + global variables (unclassified!)

# Classification probabilities reveal transmission channels!
```

### Analysis Changes
```r
# Focus on:
- Which channel (macro vs financial) do external shocks use?
- How does transmission change over time?
- Policy implications for Central Bank of China (Taiwan)
```

See `docs/taiwan_adaptation_guide.md` for details.

---

## Citation

If you use this code, please cite:

```
@article{davidson2025investigating,
  title={Investigating Economic Uncertainty Using Stochastic Volatility in Mean VARs: The Importance of Model Size, Order-Invariance and Classification},
  author={Davidson, Sharada Nia and Hou, Chenghan and Koop, Gary},
  journal={Journal of Business \& Economic Statistics},
  year={2025},
  publisher={Taylor \& Francis}
}
```

---

## Documentation

- **Overview**: This file (README.md)
- **Technical Details**: `MODULE_INSTRUCTIONS.md`
- **Full Plan**: `../../llm_logs/2025-11-16_DHK_replication_plan.md`
- **Original Paper**: `../../references/Investigating Economic Uncertain.pdf`

---

## Status

| Module | Status | Priority |
|--------|--------|----------|
| M1: Data | ⬜ Not started | P1 |
| M2: Model | ⬜ Not started | P1 |
| M3: MCMC | ⬜ Not started | P1 |
| M4: Simulation | ⬜ Not started | P2 |
| M5: Empirical | ⬜ Not started | P2 |
| M6: Analysis | ⬜ Not started | P2 |
| M7: Visualization | ⬜ Not started | P3 |
| M8: Documentation | ⬜ Not started | P3 |

**Next steps**:
1. Review plan with team
2. Download FRED-MD data (M1)
3. Implement model equations (M2)

---

## Contact

For questions or issues:
- Check `MODULE_INSTRUCTIONS.md` for technical details
- See simulation tests in `tests/` directory
- Refer to original paper and online appendix

**Last updated**: 2025-11-16

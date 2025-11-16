# Model Specification for DHK (2025) Replication

This directory contains the core model equations and specifications for the Order-Invariant Stochastic Volatility in Mean VAR (OI-SVMVAR) model.

## Overview

The OI-SVMVAR model combines:
1. **VAR structure** with volatility-in-mean effects
2. **Stochastic volatility** decomposed into common and idiosyncratic components
3. **Time-varying classification** allowing variables to switch between macro/financial blocks
4. **Order-invariance** via novel parameter transformation (key innovation!)

## Files

### `svmvar_equations.py`
**Core model equations (DHK Section 2.1)**

Implements Equations (1)-(7) from the paper:

1. **VAR with Volatility-in-Mean** (Equation 1)
   ```
   y_t = Σ B_i*y_{t-i} + Σ A_j*h_{t-j} + B0^{-1}*ε_t
   ```

2. **Covariance Structure** (Equation 2)
   ```
   Σ_t = B0^{-1} * U_t * (B0^{-1})'
   U_t = diag(Ω_m,t, Ω_u,t, Ω_f,t)
   ```

3. **Volatility Decomposition** (Equations 3-5)
   ```
   ω_m,i,t = η_m,i,t + h_m,t    (macro variables)
   ω_f,i,t = η_f,i,t + h_f,t    (financial variables)
   ω_u,i,t = η_u,i,t + h_{s_i,t},t  (unclassified - depends on state!)
   ```

4. **Common Volatility Dynamics** (Equation 6)
   ```
   h_t = Σ Φ_i*h_{t-i} + Σ Ψ_j*y_{t-j} + ε_h
   ```

5. **Idiosyncratic Volatility** (Equation 7)
   ```
   η_t = μ + ρ(η_{t-1} - μ) + σ*ε_t
   ```

**Key Functions:**
- `create_lags()` - Create lagged matrices for VAR
- `compute_var_mean()` - Conditional mean of y_t
- `decompose_volatility()` - Split volatility into common + idiosyncratic
- `compute_h_mean()` - Dynamics of common volatility
- `simulate_idiosyncratic_volatility()` - AR(1) for idiosyncratic components
- `log_likelihood_contribution()` - Log-likelihood for MCMC

**Tests:** Comprehensive unit tests included in `if __name__ == "__main__"` block

---

### `priors.py`
**Bayesian prior specifications (DHK Section 3.2)**

**Classes:**
- `PriorConfig`: Dataclass for prior hyperparameters
- `PriorDistributions`: Compute prior distributions for all parameters

**Prior Types:**

1. **Minnesota Prior** (VAR coefficients B)
   - Random walk prior: first own lag = 1, others → 0
   - Lag decay: variance ∝ 1/k^λ₁
   - Cross-variable shrinkage via λ₂

2. **Volatility-in-Mean Prior** (A coefficients)
   - Default: no volatility-in-mean effect (tight prior at 0)
   - Allows data to determine if h_t affects y_t

3. **B0 Prior** (contemporaneous effects)
   - Normal prior: N(0, σ²I)
   - Used in parameter transformation algorithm

4. **h Equation Prior**
   - AR coefficients Φ: persistent but stationary
   - y coefficients Ψ: weakly informative (y doesn't affect h by default)

5. **η AR(1) Prior**
   - μ: Normal prior (unconditional mean)
   - ρ: Normal prior centered at 0.8 (persistent)
   - σ²: Inverse Gamma prior

6. **Classification Transition Prior**
   - High persistence (p_stay = 0.95)
   - Rare regime switches

**Usage:**
```python
from priors import get_default_priors

# Get all priors with default hyperparameters
priors = get_default_priors(n=43, nm=18, nf=12, nu=13,
                           p=6, q=2, ph=2, py=1,
                           sigma_ols=residual_sds)
```

---

### `utilities.py`
**Helper functions for model operations**

**Matrix Operations:**
- `check_positive_definite()` - Verify covariance matrices
- `nearest_positive_definite()` - Fix numerical errors
- `vec()`, `unvec()` - Vectorization operations
- `kron_prod()` - Kronecker product

**VAR-Specific:**
- `companion_matrix()` - VAR(p) → VAR(1) companion form
- `check_stationarity()` - Test eigenvalues < 1
- `impulse_response()` - Compute IRFs
- `ols_var()` - OLS for initialization

**Volatility:**
- `exp_transform()` - Numerically stable exp(x)
- `log_transform()` - Safe log(x)
- `construct_volatility_matrix()` - Build Ω_t

**Data Preparation:**
- `standardize_data()` - Z-score or min-max scaling
- `inverse_standardize()` - Transform back
- `create_var_data_matrix()` - Y, X for VAR estimation

**MCMC Diagnostics:**
- `autocorrelation()` - ACF for convergence checks
- `geweke_diagnostic()` - Geweke Z-score
- `effective_sample_size()` - ESS accounting for autocorrelation
- `format_parameter_summary()` - Summary tables

**Usage:**
```python
from utilities import ols_var, check_stationarity, geweke_diagnostic

# Initialize with OLS
B_ols, resid, Sigma = ols_var(y, p=6)

# Check stationarity
is_stationary, max_eig = check_stationarity(B_ols[:, :-1], p=6)

# MCMC diagnostics
z_score = geweke_diagnostic(mcmc_chain)
```

---

## Model Dimensions

For the **43-variable DHK model**:

```python
n = 43      # Total variables
nm = 18     # Macro variables (clearly real economy)
nf = 12     # Financial variables (clearly financial markets)
nu = 13     # Unclassified (ambiguous or external shocks)

p = 6       # VAR lags
q = 2       # Volatility-in-mean lags (h_{t-1}, h_{t-2} in y equation)
ph = 2      # h lags in h equation
py = 1      # y lags in h equation
```

**Parameter counts:**
- B coefficients: n × (n×p) = 43 × 258 = 11,094
- A coefficients: n × (2×q) = 43 × 4 = 172
- B0 parameters: n×(n-1)/2 = 903 (lower triangular)
- Φ, Ψ: 2×4 + 2×43 = 94
- η parameters: 3×n = 129 (μ, ρ, σ for each variable)
- Classification states: nu × T = 13 × T time-varying states

**Total parameters: ~12,392 + time-varying classifications**

This is why MCMC is required—maximum likelihood would be infeasible!

---

## Key Innovations in DHK (2025)

### 1. Order-Invariance
**Problem:** Traditional large VARs suffer from ordering dependence. Changing variable order changes results!

**Solution:** Parameter transformation for B0 sampler
- Transform B0 to unconstrained space
- Sample transformed parameters
- Transform back to B0

**Implementation:** Will be in `mcmc/b0_sampler.py` (Module 3)

### 2. Time-Varying Classification
**Problem:** Is S&P 500 a macro variable or financial variable? Depends on economic regime!

**Solution:** Markov-switching classification
- s_{i,t} ∈ {macro, financial} for each unclassified variable i
- Transition probabilities estimated via MCMC
- Different volatility loadings in different states

**Implementation:** `decompose_volatility()` in `svmvar_equations.py` handles this

### 3. Large-Scale Estimation
**Problem:** Small VARs (~6 variables) produce biased uncertainty estimates

**Solution:**
- 43-variable model captures interactions
- Minnesota priors prevent overfitting
- Sparse matrix algorithms for speed

---

## Model Validation Checklist

Before running MCMC on real data, verify:

- [ ] **Stationarity**: All VAR coefficients satisfy eigenvalue condition
- [ ] **Positive Definiteness**: All covariance matrices are PD
- [ ] **Identification**: B0 transformation is invertible
- [ ] **Prior Sensitivity**: Results stable to prior hyperparameters
- [ ] **Classification**: Transition probabilities > 0.9 (persistent regimes)

---

## Next Steps

**Module 3: MCMC Algorithm** (`code/DHK_original/mcmc/`)

Will implement:
1. **Parameter Samplers:**
   - `b0_sampler.py` - Novel transformation algorithm
   - `var_sampler.py` - B, A coefficients (Gibbs)
   - `volatility_sampler.py` - h_t via precision sampler
   - `idiosyncratic_sampler.py` - η_t AR(1) parameters
   - `classification_sampler.py` - s_{i,t} states

2. **Main MCMC Loop:**
   - `mcmc_main.py` - Coordinate samplers
   - Burn-in, thinning, convergence diagnostics
   - Save draws for posterior analysis

**Estimated Implementation Time:** 4 weeks (this is the hardest module!)

---

## References

- Davidson, Hou, Koop (2025): "Investigating Economic Uncertainty Using Stochastic Volatility in Mean VARs"
- Chan, Koop, Yu (2024): "Order-Invariant Bayesian Vector Autoregressions"
- Carriero, Clark, Marcellino (2022): "Large Bayesian VARs"

---

## Testing

Run tests for all modules:

```bash
# Test model equations
python svmvar_equations.py

# Test priors
python priors.py

# Test utilities
python utilities.py
```

All tests should pass before proceeding to Module 3.

---

**Status:** Module 2 Complete ✓

**Next:** Module 3 - MCMC Algorithm (Critical Path!)

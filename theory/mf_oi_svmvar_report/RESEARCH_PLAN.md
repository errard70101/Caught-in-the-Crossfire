# Research Plan: Mixed-Frequency Order-Invariant SVMVAR (MF-OI-SVMVAR)

## Current Note

For immediate technical work, use `NEXT_THREAD_PLAN.md`. This older roadmap predates the referee review and should not be read as validating `O(Tn)` compute or automatic latent-frequency identification of `B0`. The current priority is to validate the SV-aware matrix-free sampler, preconditioning, lambda sensitivity, and identification diagnostics in separate threads.

## 🎯 Project Overview
This project extends the Order-Invariant Stochastic Volatility in Mean VAR (OI-SVMVAR) proposed by Davidson, Hou, and Koop (2025) to a mixed-frequency setting. By incorporating a latent high-frequency state-space and leveraging precision-based sampling, we aim to eliminate temporal aggregation bias and enable the real-time nowcasting of uncertainty impacts, without falling into the MCMC curse of dimensionality.

## 🧭 Methodological Philosophy (Inspired by DHK 2025)
To ensure computational feasibility and align with the publication standards of top-tier journals (e.g., *JBES*), we adopt a **Finite-Sample Bayesian Regularization** approach:
- **No Asymptotic Proofs:** We will *not* attempt to prove large-sample properties like Posterior Consistency or the Bernstein-von Mises theorem.
- **Proper Priors:** We strictly use *Proper Priors* (e.g., Gaussian, Horseshoe) for all parameters to mathematically guarantee Posterior Propriety without complex proofs.
- **Simulation-Based Validation:** The validity and efficiency of the algorithm will be proven through rigorous Monte Carlo simulations rather than theoretical limits.

## 🗺️ Three-Year Execution Roadmap

### Year 1: Methodology & Algorithm (Theory Core)
1. **Latent State-Space Formulation:** Formally define the observation equations linking quarterly data to the latent monthly OI-SVMVAR process.
2. **Point Identification of $\mathbf{B}_0$:** Adapt the Lütkepohl and Woźniak (2020) conditions to prove that $\mathbf{B}_0$ is strictly point-identified in the mixed-frequency setting, relying on the heteroskedasticity of the high-frequency latent common volatilities.
3. **Precision-Based MCMC Sampler:** Derive the joint conditional posterior for the latent high-frequency states and demonstrate its band-sparse structure to achieve $\mathcal{O}(Tn)$ computational complexity (Chan and Jeliazkov, 2009).

### Year 2: Simulation & Code Optimization
1. **Algorithm Implementation:** Write highly optimized, vectorized MATLAB code for the precision-based MCMC sampler.
2. **Monte Carlo Simulations:** Design DGPs to evaluate the finite-sample performance, convergence, and computational speed of the MF-OI-SVMVAR against standard baselines.

### Year 3: Empirical Application & Policy
1. **Data Construction:** Build a large mixed-frequency dataset (e.g., 40+ variables) incorporating daily/weekly financial condition indices and quarterly macroeconomic fundamentals.
2. **Empirical Analysis:** Estimate the asymmetric real effects of global/US macro vs. financial uncertainty shocks on a small open economy (e.g., Taiwan).
3. **Paper Writing:** Finalize the manuscript for submission to *JBES* or *Journal of Econometrics*.

---
*Note: This document serves as the internal compass for the project. The formal mathematical proofs and reports are maintained in `main.tex`.*

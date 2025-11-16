#!/usr/bin/env python3
"""
Prior Specifications for OI-SVMVAR Model

Purpose: Define Bayesian priors for all model parameters in DHK (2025) replication
Reference: DHK (2025) - Section 3.2, Online Appendix C
Author: Claude Code
Date: 2025-11-16

Prior Structure:
--------------
1. VAR coefficients (B, A): Minnesota-style priors
2. Contemporaneous matrix (B0): Reduced-form identification
3. Volatility parameters (h): Initial conditions and dynamics
4. Idiosyncratic volatilities (η): AR(1) parameters
5. Classification probabilities: Markov-switching priors
"""

import numpy as np
from dataclasses import dataclass
from typing import Tuple, Optional


@dataclass
class PriorConfig:
    """
    Configuration for prior hyperparameters

    Attributes
    ----------
    # Minnesota prior for VAR coefficients
    lambda_0 : float
        Overall tightness (default: 0.2)
    lambda_1 : float
        Lag decay (default: 1.0)
    lambda_2 : float
        Cross-variable shrinkage (default: 0.5)
    lambda_3 : float
        Constant term variance (default: 100.0)

    # Volatility-in-mean coefficients
    lambda_h : float
        Tightness for A coefficients (default: 0.1)

    # B0 prior (contemporaneous effects)
    b0_mean : float
        Prior mean for off-diagonal elements (default: 0.0)
    b0_std : float
        Prior std for off-diagonal elements (default: 1.0)

    # Common volatility h dynamics
    phi_mean : float
        Prior mean for Φ (AR coefficients in h equation)
    phi_std : float
        Prior std for Φ
    psi_mean : float
        Prior mean for Ψ (y coefficients in h equation)
    psi_std : float
        Prior std for Ψ

    # Idiosyncratic volatility η ~ AR(1)
    mu_eta_mean : float
        Prior mean for μ_η (intercept)
    mu_eta_std : float
        Prior std for μ_η
    rho_eta_mean : float
        Prior mean for ρ_η (AR coefficient)
    rho_eta_std : float
        Prior std for ρ_η
    sigma_eta_shape : float
        Inverse Gamma shape for σ_η²
    sigma_eta_scale : float
        Inverse Gamma scale for σ_η²

    # Classification transition probabilities
    p_stay_macro : float
        Prior prob of staying in macro classification (default: 0.95)
    p_stay_financial : float
        Prior prob of staying in financial classification (default: 0.95)
    """

    # Minnesota prior
    lambda_0: float = 0.2
    lambda_1: float = 1.0
    lambda_2: float = 0.5
    lambda_3: float = 100.0

    # Volatility-in-mean
    lambda_h: float = 0.1

    # B0 prior
    b0_mean: float = 0.0
    b0_std: float = 1.0

    # h equation priors
    phi_mean: float = 0.5
    phi_std: float = 0.2
    psi_mean: float = 0.0
    psi_std: float = 0.1

    # η AR(1) priors
    mu_eta_mean: float = 0.0
    mu_eta_std: float = 1.0
    rho_eta_mean: float = 0.8
    rho_eta_std: float = 0.1
    sigma_eta_shape: float = 3.0
    sigma_eta_scale: float = 0.1

    # Classification priors
    p_stay_macro: float = 0.95
    p_stay_financial: float = 0.95


class PriorDistributions:
    """
    Prior distributions for OI-SVMVAR model parameters
    """

    def __init__(self, config: PriorConfig, n: int, nm: int, nf: int, nu: int, p: int, q: int):
        """
        Initialize prior distributions

        Parameters
        ----------
        config : PriorConfig
            Prior hyperparameters
        n : int
            Total number of variables
        nm : int
            Number of macro variables
        nf : int
            Number of financial variables
        nu : int
            Number of unclassified variables
        p : int
            VAR lags
        q : int
            Volatility-in-mean lags
        """
        self.config = config
        self.n = n
        self.nm = nm
        self.nf = nf
        self.nu = nu
        self.p = p
        self.q = q

    def minnesota_prior_var(self, sigma_ols: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Minnesota prior for VAR coefficients B

        Prior: vec(B) ~ N(vec(B_prior), V_prior)

        Parameters
        ----------
        sigma_ols : np.ndarray, shape (n,)
            OLS residual standard deviations for scaling

        Returns
        -------
        B_prior : np.ndarray, shape (n, n*p)
            Prior mean (random walk: first own lag = 1, others = 0)
        V_prior : np.ndarray, shape (n*p, n*p)
            Prior variance (diagonal)
        """
        # Prior mean: random walk (only first own lag = 1)
        B_prior = np.zeros((self.n, self.n * self.p))
        for i in range(self.n):
            B_prior[i, i] = 1.0  # First own lag coefficient = 1

        # Prior variance (diagonal matrix)
        V_prior = np.zeros((self.n * self.p, self.n * self.p))

        for lag in range(1, self.p + 1):
            for i in range(self.n):
                for j in range(self.n):
                    idx = (lag - 1) * self.n + j

                    if i == j:  # Own lag
                        variance = (self.config.lambda_0 / lag ** self.config.lambda_1) ** 2
                    else:  # Cross-variable lag
                        variance = (
                            self.config.lambda_0 * self.config.lambda_2 *
                            sigma_ols[i] / (sigma_ols[j] * lag ** self.config.lambda_1)
                        ) ** 2

                    V_prior[idx, idx] = variance

        return B_prior, V_prior

    def volatility_in_mean_prior(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Prior for volatility-in-mean coefficients A

        Prior: vec(A) ~ N(0, V_A)

        Returns
        -------
        A_prior : np.ndarray, shape (n, 2*q)
            Prior mean (zeros - no volatility-in-mean by default)
        V_A : np.ndarray, shape (2*q, 2*q)
            Prior variance (diagonal, tight prior)
        """
        # Prior mean: zeros
        A_prior = np.zeros((self.n, 2 * self.q))

        # Prior variance: diagonal with tight prior
        V_A = np.eye(2 * self.q) * self.config.lambda_h ** 2

        return A_prior, V_A

    def b0_prior(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Prior for contemporaneous matrix B0

        Note: B0 is lower triangular in standard Cholesky VAR
        In DHK's order-invariant approach, we use parameter transformation

        Returns
        -------
        b0_mean : np.ndarray, shape (n*(n-1)/2,)
            Prior mean for lower triangular off-diagonal elements
        b0_var : np.ndarray, shape (n*(n-1)/2,)
            Prior variance (diagonal)
        """
        n_b0_params = self.n * (self.n - 1) // 2

        # Prior: N(0, σ²I) for off-diagonal elements
        b0_mean = np.ones(n_b0_params) * self.config.b0_mean
        b0_var = np.ones(n_b0_params) * self.config.b0_std ** 2

        return b0_mean, b0_var

    def h_equation_prior(self, ph: int, py: int) -> dict:
        """
        Prior for common volatility h equation (Equation 6)

        h_t = Σ Φ_i * h_{t-i} + Σ Ψ_j * y_{t-j} + ε_h

        Parameters
        ----------
        ph : int
            Number of lags of h in h equation
        py : int
            Number of lags of y in h equation

        Returns
        -------
        dict
            Dictionary with keys: 'Phi_mean', 'Phi_var', 'Psi_mean', 'Psi_var', 'Sigma_h'
        """
        # Φ coefficients (AR part for h)
        Phi_mean = np.ones((2, 2 * ph)) * self.config.phi_mean
        Phi_var = np.ones((2, 2 * ph)) * self.config.phi_std ** 2

        # Ψ coefficients (y lags in h equation)
        Psi_mean = np.zeros((2, self.n * py))  # Prior: y doesn't affect h
        Psi_var = np.ones((2, self.n * py)) * self.config.psi_std ** 2

        # Innovation variance Σ_h (2x2 covariance matrix)
        # Prior: inverse Wishart (conjugate prior)
        Sigma_h_df = 5  # Degrees of freedom
        Sigma_h_scale = np.eye(2) * 0.1  # Scale matrix

        return {
            'Phi_mean': Phi_mean,
            'Phi_var': Phi_var,
            'Psi_mean': Psi_mean,
            'Psi_var': Psi_var,
            'Sigma_h_df': Sigma_h_df,
            'Sigma_h_scale': Sigma_h_scale
        }

    def eta_ar1_prior(self) -> dict:
        """
        Prior for idiosyncratic volatility AR(1) parameters (Equation 7)

        η_t = μ + ρ(η_{t-1} - μ) + σ * ε_t

        Returns
        -------
        dict
            Dictionary with keys: 'mu_mean', 'mu_var', 'rho_mean', 'rho_var',
            'sigma_shape', 'sigma_scale'
        """
        return {
            'mu_mean': self.config.mu_eta_mean,
            'mu_var': self.config.mu_eta_std ** 2,
            'rho_mean': self.config.rho_eta_mean,
            'rho_var': self.config.rho_eta_std ** 2,
            'sigma_shape': self.config.sigma_eta_shape,  # Inverse Gamma
            'sigma_scale': self.config.sigma_eta_scale
        }

    def classification_transition_prior(self) -> np.ndarray:
        """
        Prior for classification transition matrix (Markov-switching)

        P = [[p_MM, 1-p_MM],
             [1-p_FF, p_FF]]

        where p_MM = prob(macro→macro), p_FF = prob(financial→financial)

        Returns
        -------
        transition_prior : np.ndarray, shape (2, 2)
            Prior transition matrix
        """
        p_MM = self.config.p_stay_macro
        p_FF = self.config.p_stay_financial

        transition_prior = np.array([
            [p_MM, 1 - p_MM],
            [1 - p_FF, p_FF]
        ])

        return transition_prior

    def initial_h_prior(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Prior for initial common volatility h_0

        Returns
        -------
        h0_mean : np.ndarray, shape (2,)
            Prior mean for h_0
        h0_var : np.ndarray, shape (2, 2)
            Prior covariance for h_0
        """
        h0_mean = np.zeros(2)
        h0_var = np.eye(2) * 1.0  # Diffuse prior

        return h0_mean, h0_var

    def get_all_priors(self, sigma_ols: np.ndarray, ph: int, py: int) -> dict:
        """
        Get all prior specifications in a single dictionary

        Parameters
        ----------
        sigma_ols : np.ndarray, shape (n,)
            OLS residual standard deviations
        ph : int
            h lags in h equation
        py : int
            y lags in h equation

        Returns
        -------
        dict
            Complete prior specification
        """
        B_prior, V_B = self.minnesota_prior_var(sigma_ols)
        A_prior, V_A = self.volatility_in_mean_prior()
        b0_mean, b0_var = self.b0_prior()
        h_prior = self.h_equation_prior(ph, py)
        eta_prior = self.eta_ar1_prior()
        trans_prior = self.classification_transition_prior()
        h0_mean, h0_var = self.initial_h_prior()

        return {
            'B': {'mean': B_prior, 'var': V_B},
            'A': {'mean': A_prior, 'var': V_A},
            'B0': {'mean': b0_mean, 'var': b0_var},
            'h_equation': h_prior,
            'eta_ar1': eta_prior,
            'classification_transition': trans_prior,
            'h0': {'mean': h0_mean, 'var': h0_var}
        }


def get_default_priors(n: int, nm: int, nf: int, nu: int, p: int, q: int,
                       ph: int, py: int, sigma_ols: np.ndarray) -> dict:
    """
    Convenience function to get default prior specifications

    Parameters
    ----------
    n : int
        Total number of variables
    nm : int
        Number of macro variables
    nf : int
        Number of financial variables
    nu : int
        Number of unclassified variables
    p : int
        VAR lags
    q : int
        Volatility-in-mean lags
    ph : int
        h lags in h equation
    py : int
        y lags in h equation
    sigma_ols : np.ndarray, shape (n,)
        OLS residual standard deviations

    Returns
    -------
    dict
        Complete prior specification with default hyperparameters
    """
    config = PriorConfig()
    priors = PriorDistributions(config, n, nm, nf, nu, p, q)
    return priors.get_all_priors(sigma_ols, ph, py)


# ============================================================================
# Example Usage
# ============================================================================

if __name__ == "__main__":
    """Example: Set up priors for 43-variable DHK model"""

    # Model dimensions
    n = 43      # Total variables
    nm = 18     # Macro variables
    nf = 12     # Financial variables
    nu = 13     # Unclassified variables
    p = 6       # VAR lags
    q = 2       # Volatility-in-mean lags
    ph = 2      # h lags in h equation
    py = 1      # y lags in h equation

    # OLS residual std (placeholder - would come from data)
    sigma_ols = np.ones(n) * 0.5

    # Get all priors
    priors = get_default_priors(n, nm, nf, nu, p, q, ph, py, sigma_ols)

    # Display prior dimensions
    print("="*70)
    print("DHK (2025) OI-SVMVAR Prior Specifications")
    print("="*70)

    print("\n1. VAR Coefficients (B):")
    print(f"   Shape: {priors['B']['mean'].shape}")
    print(f"   Prior mean (first own lag): {priors['B']['mean'][0, 0]}")

    print("\n2. Volatility-in-Mean Coefficients (A):")
    print(f"   Shape: {priors['A']['mean'].shape}")
    print(f"   Prior variance: {priors['A']['var'][0, 0]}")

    print("\n3. Contemporaneous Matrix (B0):")
    print(f"   Number of parameters: {len(priors['B0']['mean'])}")
    print(f"   Prior mean: {priors['B0']['mean'][0]}")

    print("\n4. Common Volatility h Equation:")
    print(f"   Φ (AR coefficients): {priors['h_equation']['Phi_mean'].shape}")
    print(f"   Ψ (y coefficients): {priors['h_equation']['Psi_mean'].shape}")

    print("\n5. Idiosyncratic Volatility η AR(1):")
    print(f"   μ prior mean: {priors['eta_ar1']['mu_mean']}")
    print(f"   ρ prior mean: {priors['eta_ar1']['rho_mean']}")

    print("\n6. Classification Transition Matrix:")
    print(f"   P(macro→macro): {priors['classification_transition'][0, 0]}")
    print(f"   P(financial→financial): {priors['classification_transition'][1, 1]}")

    print("\n✓ Prior setup complete!")
    print("="*70)

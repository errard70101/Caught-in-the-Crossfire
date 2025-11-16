#!/usr/bin/env python3
"""
OI-SVMVAR Model Equations

Purpose: Implement core equations (1)-(7) from DHK (2025)
Reference: Davidson, Hou, Koop (2025) Section 2.1
Author: Claude Code
Date: 2025-11-16

Equations implemented:
    (1) VAR with SV in mean: yt = Σ Bi*yt-i + Σ Aj*ht-j + B0^(-1)*εt
    (2) Covariance structure: Ut = diag(Ωm,t, Ωu,t, Ωf,t)
    (3-5) Volatility decomposition (macro, financial, unclassified)
    (6) Common volatility dynamics: ht = Σ Φi*ht-i + Σ Ψj*yt-j + εh
    (7) Idiosyncratic volatilities: AR(1) processes
"""

import numpy as np
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass


@dataclass
class SVMVARConfig:
    """Configuration for OI-SVMVAR model"""
    n: int              # Total number of variables
    nm: int             # Number of macro variables
    nf: int             # Number of financial variables
    nu: int             # Number of unclassified variables
    p: int = 6          # VAR lags (default: 6)
    q: int = 2          # Volatility-in-mean lags (default: 2)
    ph: int = 2         # h VAR lags (default: 2)
    py: int = 1         # y in h equation lags (default: 1)

    def __post_init__(self):
        """Validate configuration"""
        assert self.n == self.nm + self.nf + self.nu, \
            f"n ({self.n}) != nm + nf + nu ({self.nm + self.nf + self.nu})"
        assert self.p > 0, "VAR lag order must be positive"
        assert self.q >= 0, "Volatility-in-mean lag order must be non-negative"


def create_lags(y: np.ndarray, p: int) -> np.ndarray:
    """
    Create lagged matrices for VAR

    Parameters
    ----------
    y : np.ndarray
        Data matrix (T x n)
    p : int
        Number of lags

    Returns
    -------
    np.ndarray
        Lagged matrices (T x n x p)
        y_lags[t, :, i] contains y[t-i-1, :]
    """
    T, n = y.shape
    y_lags = np.zeros((T, n, p))

    for lag in range(p):
        # lag=0 means t-1, lag=1 means t-2, etc.
        y_lags[(lag+1):, :, lag] = y[:(T-lag-1), :]

    return y_lags


def compute_var_mean(
    y: np.ndarray,
    ht: np.ndarray,
    B_coefs: List[np.ndarray],
    A_coefs: List[np.ndarray],
    config: SVMVARConfig
) -> np.ndarray:
    """
    Compute conditional mean of VAR

    Equation (1): yt = Σ(i=1 to p) Bi*yt-i + Σ(j=0 to q) Aj*ht-j + B0^(-1)*εt

    Parameters
    ----------
    y : np.ndarray
        Data matrix (T x n)
    ht : np.ndarray
        Common log-volatilities (T x 2) - [hm,t, hf,t]
    B_coefs : List[np.ndarray]
        VAR coefficient matrices [B1, B2, ..., Bp], each (n x n)
    A_coefs : List[np.ndarray]
        Volatility-in-mean matrices [A0, A1, ..., Aq], each (n x 2)
    config : SVMVARConfig
        Model configuration

    Returns
    -------
    np.ndarray
        Conditional mean (T x n)
    """
    T, n = y.shape
    p, q = config.p, config.q

    # Initialize mean
    mu = np.zeros((T, n))

    # Create lags
    y_lags = create_lags(y, p)
    h_lags = create_lags(ht, q + 1)  # q+1 for contemporaneous

    # Compute VAR term and volatility-in-mean term
    for t in range(max(p, q), T):
        # VAR term: Σ Bi * yt-i
        for i in range(p):
            mu[t, :] += B_coefs[i] @ y_lags[t, :, i]

        # Volatility-in-mean term: Σ Aj * ht-j
        for j in range(q + 1):
            if t - j >= 0:
                mu[t, :] += A_coefs[j] @ ht[t - j, :]

    return mu


def compute_covariance_matrix(
    omega_m: np.ndarray,
    omega_u: np.ndarray,
    omega_f: np.ndarray
) -> np.ndarray:
    """
    Compute covariance matrix Ut

    Equation (2): Ut = diag(Ωm,t, Ωu,t, Ωf,t)
    where Ωk,t = diag(exp(ωk_1,t), ..., exp(ωk_nk,t))

    Parameters
    ----------
    omega_m : np.ndarray
        Log-volatilities for macro variables (T x nm)
    omega_u : np.ndarray
        Log-volatilities for unclassified variables (T x nu)
    omega_f : np.ndarray
        Log-volatilities for financial variables (T x nf)

    Returns
    -------
    np.ndarray
        Covariance matrix at each time t (T x n x n)
        Actually returns only diagonals for efficiency: (T x n)
    """
    # For computational efficiency, return diagonals only
    # Full matrix can be constructed when needed

    # Exponentiate to get variances
    Omega_m = np.exp(omega_m)  # (T x nm)
    Omega_u = np.exp(omega_u)  # (T x nu)
    Omega_f = np.exp(omega_f)  # (T x nf)

    # Concatenate
    Omega_t = np.concatenate([Omega_m, Omega_u, Omega_f], axis=1)  # (T x n)

    return Omega_t


def decompose_volatility(
    eta_m: np.ndarray,
    eta_f: np.ndarray,
    eta_u: np.ndarray,
    h_m: np.ndarray,
    h_f: np.ndarray,
    class_indicators: np.ndarray
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Decompose log-volatilities into idiosyncratic and common components

    Equations (3-5):
        ωm_i,t = ηm_i,t + hm,t  (macro)
        ωf_i,t = ηf_i,t + hf,t  (financial)
        ωu_i,t = ηu_i,t + hs_i,t,t  (unclassified, time-varying)

    Parameters
    ----------
    eta_m : np.ndarray
        Idiosyncratic log-volatilities for macro (T x nm)
    eta_f : np.ndarray
        Idiosyncratic log-volatilities for financial (T x nf)
    eta_u : np.ndarray
        Idiosyncratic log-volatilities for unclassified (T x nu)
    h_m : np.ndarray
        Common macro log-volatility (T,)
    h_f : np.ndarray
        Common financial log-volatility (T,)
    class_indicators : np.ndarray
        Classification for unclassified variables (nu x T)
        class_indicators[i, t] = 0 (macro) or 1 (financial)

    Returns
    -------
    Tuple[np.ndarray, np.ndarray, np.ndarray]
        (omega_m, omega_u, omega_f) - total log-volatilities
    """
    T = len(h_m)
    nm, nf, nu = eta_m.shape[1], eta_f.shape[1], eta_u.shape[1]

    # Macro volatilities: ωm_i,t = ηm_i,t + hm,t
    omega_m = eta_m + h_m[:, np.newaxis]  # Broadcasting

    # Financial volatilities: ωf_i,t = ηf_i,t + hf,t
    omega_f = eta_f + h_f[:, np.newaxis]

    # Unclassified volatilities (TIME-VARYING classification!)
    omega_u = np.zeros((T, nu))

    for i in range(nu):
        for t in range(T):
            if class_indicators[i, t] == 0:  # Classified as macro at time t
                omega_u[t, i] = eta_u[t, i] + h_m[t]
            else:  # Classified as financial at time t
                omega_u[t, i] = eta_u[t, i] + h_f[t]

    return omega_m, omega_u, omega_f


def compute_h_mean(
    ht: np.ndarray,
    yt: np.ndarray,
    Phi_coefs: List[np.ndarray],
    Psi_coefs: List[np.ndarray],
    ph: int,
    py: int
) -> np.ndarray:
    """
    Compute conditional mean of common log-volatilities

    Equation (6): ht = Σ(i=1 to ph) Φi*ht-i + Σ(j=1 to py) Ψj*yt-j + εh

    Parameters
    ----------
    ht : np.ndarray
        Common log-volatilities (T x 2)
    yt : np.ndarray
        Data matrix (T x n)
    Phi_coefs : List[np.ndarray]
        Autoregressive coefficients [Φ1, ..., Φph], each (2 x 2)
    Psi_coefs : List[np.ndarray]
        Link to observables [Ψ1, ..., Ψpy], each (2 x n)
    ph : int
        Number of lags for ht
    py : int
        Number of lags for yt

    Returns
    -------
    np.ndarray
        Conditional mean of ht (T x 2)
    """
    T = ht.shape[0]

    # Initialize mean
    h_mean = np.zeros((T, 2))

    # Create lags
    h_lags = create_lags(ht, ph)
    y_lags = create_lags(yt, py)

    # Compute mean
    for t in range(max(ph, py), T):
        # Autoregressive term: Σ Φi * ht-i
        for i in range(ph):
            h_mean[t, :] += Phi_coefs[i] @ h_lags[t, :, i]

        # Link to observables: Σ Ψj * yt-j
        for j in range(py):
            h_mean[t, :] += Psi_coefs[j] @ y_lags[t, :, j]

    return h_mean


def simulate_idiosyncratic_volatility(
    T: int,
    mu: float,
    rho: float,
    sigma: float,
    eta_0: Optional[float] = None
) -> np.ndarray:
    """
    Simulate idiosyncratic log-volatility following AR(1)

    Equation (7): ηk_i,t = μk,i + ρk,i * ηk_i,t-1 + εk_i,t
    where εk_i,t ~ N(0, σ²k,i)

    Parameters
    ----------
    T : int
        Number of time periods
    mu : float
        Intercept
    rho : float
        AR(1) coefficient (|rho| < 1 for stationarity)
    sigma : float
        Standard deviation of innovations
    eta_0 : float, optional
        Initial value. If None, draw from stationary distribution

    Returns
    -------
    np.ndarray
        Simulated idiosyncratic volatility (T,)
    """
    assert abs(rho) < 1, f"AR(1) coefficient must satisfy |rho| < 1, got {rho}"

    eta = np.zeros(T)

    # Initialize from stationary distribution
    if eta_0 is None:
        # Stationary distribution: N(0, σ² / (1 - ρ²))
        eta[0] = np.random.normal(0, sigma / np.sqrt(1 - rho**2))
    else:
        eta[0] = eta_0

    # Simulate AR(1) process
    for t in range(1, T):
        epsilon_t = np.random.normal(0, sigma)
        eta[t] = mu + rho * eta[t-1] + epsilon_t

    return eta


def log_likelihood_contribution(
    y_t: np.ndarray,
    mu_t: np.ndarray,
    B0_inv: np.ndarray,
    Omega_t: np.ndarray
) -> float:
    """
    Compute log-likelihood contribution at time t

    log p(yt | θ) = -n/2 * log(2π) - 1/2 * log|Ut|
                    + log|det(B0)| - 1/2 * εt' * Ut^(-1) * εt

    where εt = B0 * (yt - μt)

    Parameters
    ----------
    y_t : np.ndarray
        Observed data at time t (n,)
    mu_t : np.ndarray
        Conditional mean at time t (n,)
    B0_inv : np.ndarray
        Inverse of impact matrix B0 (n x n)
    Omega_t : np.ndarray
        Diagonal variances at time t (n,)

    Returns
    -------
    float
        Log-likelihood contribution
    """
    n = len(y_t)

    # Reduced-form errors: yt - μt
    resid = y_t - mu_t

    # Structural errors: εt = B0 * (yt - μt) = B0 * B0^(-1) * εt
    # Actually: yt - μt = B0^(-1) * εt, so εt = B0 * (yt - μt)
    B0 = np.linalg.inv(B0_inv)
    epsilon_t = B0 @ resid

    # Log-likelihood
    log_det_Omega = np.sum(np.log(Omega_t))  # log|Ut| for diagonal matrix
    log_det_B0 = np.linalg.slogdet(B0)[1]

    # Mahalanobis distance: εt' * Ut^(-1) * εt
    # For diagonal Ut: Σ (εt,i² / Ωt,i)
    mahalanobis = np.sum(epsilon_t**2 / Omega_t)

    log_like = -n/2 * np.log(2 * np.pi) - 0.5 * log_det_Omega \
               + log_det_B0 - 0.5 * mahalanobis

    return log_like


# ============================================================================
# Testing and example usage
# ============================================================================

def test_create_lags():
    """Test lag creation"""
    print("Testing create_lags()...")

    # Simple test data
    T, n, p = 10, 3, 2
    y = np.random.randn(T, n)

    y_lags = create_lags(y, p)

    # Check dimensions
    assert y_lags.shape == (T, n, p), f"Expected shape {(T, n, p)}, got {y_lags.shape}"

    # Check correctness
    # y_lags[t, :, 0] should equal y[t-1, :]
    for t in range(1, T):
        assert np.allclose(y_lags[t, :, 0], y[t-1, :]), \
            f"Lag 0 mismatch at t={t}"

    # y_lags[t, :, 1] should equal y[t-2, :]
    for t in range(2, T):
        assert np.allclose(y_lags[t, :, 1], y[t-2, :]), \
            f"Lag 1 mismatch at t={t}"

    print("✓ create_lags() passed all tests\n")


def test_decompose_volatility():
    """Test volatility decomposition"""
    print("Testing decompose_volatility()...")

    T, nm, nf, nu = 100, 3, 2, 2

    # Simulate idiosyncratic components
    eta_m = np.random.randn(T, nm) * 0.1
    eta_f = np.random.randn(T, nf) * 0.1
    eta_u = np.random.randn(T, nu) * 0.1

    # Simulate common factors
    h_m = np.random.randn(T) * 0.5
    h_f = np.random.randn(T) * 0.5

    # Classification: first unclassified always macro, second switches
    class_indicators = np.zeros((nu, T), dtype=int)
    class_indicators[0, :] = 0  # Always macro
    class_indicators[1, :50] = 1  # Financial first half
    class_indicators[1, 50:] = 0  # Macro second half

    # Decompose
    omega_m, omega_u, omega_f = decompose_volatility(
        eta_m, eta_f, eta_u, h_m, h_f, class_indicators
    )

    # Check dimensions
    assert omega_m.shape == (T, nm)
    assert omega_u.shape == (T, nu)
    assert omega_f.shape == (T, nf)

    # Check correctness for macro
    assert np.allclose(omega_m, eta_m + h_m[:, np.newaxis])

    # Check correctness for unclassified (first variable - always macro)
    assert np.allclose(omega_u[:, 0], eta_u[:, 0] + h_m)

    # Check time-varying classification (second variable)
    assert np.allclose(omega_u[:50, 1], eta_u[:50, 1] + h_f[:50])  # Financial
    assert np.allclose(omega_u[50:, 1], eta_u[50:, 1] + h_m[50:])  # Macro

    print("✓ decompose_volatility() passed all tests\n")


def test_simulate_idiosyncratic():
    """Test AR(1) simulation"""
    print("Testing simulate_idiosyncratic_volatility()...")

    T = 10000
    mu, rho, sigma = 0.1, 0.9, 0.2

    eta = simulate_idiosyncratic_volatility(T, mu, rho, sigma)

    # Check stationarity
    assert abs(eta.mean() - mu/(1-rho)) < 0.05, "Mean not close to theoretical"

    # Check variance (approximately)
    theoretical_var = sigma**2 / (1 - rho**2)
    assert abs(eta.var() - theoretical_var) < 0.05, "Variance not close to theoretical"

    print(f"  Sample mean: {eta.mean():.4f} (theoretical: {mu/(1-rho):.4f})")
    print(f"  Sample var:  {eta.var():.4f} (theoretical: {theoretical_var:.4f})")
    print("✓ simulate_idiosyncratic_volatility() passed all tests\n")


if __name__ == "__main__":
    print("="*70)
    print("DHK (2025) Replication - Module 2: Model Equations")
    print("Testing core functions")
    print("="*70 + "\n")

    # Run tests
    test_create_lags()
    test_decompose_volatility()
    test_simulate_idiosyncratic()

    print("="*70)
    print("✓ All tests passed!")
    print("="*70)

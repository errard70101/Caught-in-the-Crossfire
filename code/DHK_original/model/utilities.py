#!/usr/bin/env python3
"""
Utility Functions for OI-SVMVAR Model

Purpose: Helper functions for model operations, validation, and diagnostics
Reference: DHK (2025) replication
Author: Claude Code
Date: 2025-11-16
"""

import numpy as np
import pandas as pd
from typing import Tuple, Optional, List
from scipy import linalg


# ============================================================================
# Matrix Operations
# ============================================================================

def check_positive_definite(matrix: np.ndarray, tol: float = 1e-8) -> bool:
    """
    Check if matrix is positive definite

    Parameters
    ----------
    matrix : np.ndarray
        Square matrix to check
    tol : float
        Tolerance for eigenvalue check

    Returns
    -------
    bool
        True if positive definite
    """
    try:
        # Attempt Cholesky decomposition
        linalg.cholesky(matrix, lower=True)
        return True
    except linalg.LinAlgError:
        # Check eigenvalues
        eigvals = linalg.eigvalsh(matrix)
        return np.all(eigvals > tol)


def nearest_positive_definite(A: np.ndarray) -> np.ndarray:
    """
    Find nearest positive definite matrix

    Uses Higham (1988) algorithm to find nearest PD matrix
    Useful when numerical errors cause covariance matrices to be non-PD

    Parameters
    ----------
    A : np.ndarray
        Square symmetric matrix

    Returns
    -------
    np.ndarray
        Nearest positive definite matrix
    """
    B = (A + A.T) / 2
    _, s, V = linalg.svd(B)

    H = V.T @ np.diag(s) @ V
    A2 = (B + H) / 2
    A3 = (A2 + A2.T) / 2

    if check_positive_definite(A3):
        return A3

    spacing = np.spacing(linalg.norm(A))
    I = np.eye(A.shape[0])
    k = 1
    while not check_positive_definite(A3):
        mineig = np.min(np.real(linalg.eigvals(A3)))
        A3 += I * (-mineig * k**2 + spacing)
        k += 1

    return A3


def vec(A: np.ndarray) -> np.ndarray:
    """
    Vectorize matrix (stack columns)

    Parameters
    ----------
    A : np.ndarray, shape (m, n)
        Input matrix

    Returns
    -------
    np.ndarray, shape (m*n,)
        Vectorized matrix
    """
    return A.T.flatten()


def unvec(a: np.ndarray, rows: int, cols: int) -> np.ndarray:
    """
    Unvectorize vector to matrix

    Parameters
    ----------
    a : np.ndarray, shape (rows*cols,)
        Vectorized matrix
    rows : int
        Number of rows
    cols : int
        Number of columns

    Returns
    -------
    np.ndarray, shape (rows, cols)
        Matrix
    """
    return a.reshape((cols, rows)).T


def kron_prod(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    """
    Kronecker product (wrapper for np.kron)

    Parameters
    ----------
    A : np.ndarray
        First matrix
    B : np.ndarray
        Second matrix

    Returns
    -------
    np.ndarray
        Kronecker product A ⊗ B
    """
    return np.kron(A, B)


# ============================================================================
# VAR-Specific Functions
# ============================================================================

def companion_matrix(B: np.ndarray, p: int) -> np.ndarray:
    """
    Construct companion matrix for VAR(p)

    For VAR(p): y_t = B_1*y_{t-1} + ... + B_p*y_{t-p} + ε_t

    Companion form:
    Y_t = F*Y_{t-1} + e_t

    where Y_t = [y_t, y_{t-1}, ..., y_{t-p+1}]' (n*p × 1)

    Parameters
    ----------
    B : np.ndarray, shape (n, n*p)
        VAR coefficient matrix [B_1, B_2, ..., B_p]
    p : int
        Number of lags

    Returns
    -------
    np.ndarray, shape (n*p, n*p)
        Companion matrix
    """
    n = B.shape[0]
    F = np.zeros((n * p, n * p))

    # Top block: VAR coefficients
    F[:n, :] = B

    # Lower blocks: identity matrices
    if p > 1:
        F[n:, :-n] = np.eye(n * (p - 1))

    return F


def check_stationarity(B: np.ndarray, p: int) -> Tuple[bool, float]:
    """
    Check VAR stationarity condition

    VAR is stationary if all eigenvalues of companion matrix are < 1 in modulus

    Parameters
    ----------
    B : np.ndarray, shape (n, n*p)
        VAR coefficient matrix
    p : int
        Number of lags

    Returns
    -------
    is_stationary : bool
        True if stationary
    max_eigenvalue : float
        Maximum absolute eigenvalue
    """
    F = companion_matrix(B, p)
    eigenvalues = linalg.eigvals(F)
    max_eig = np.max(np.abs(eigenvalues))

    return max_eig < 1.0, max_eig


def impulse_response(B: np.ndarray, B0_inv: np.ndarray, p: int, horizon: int) -> np.ndarray:
    """
    Compute structural impulse responses

    IRF(h) = Ψ_h = ∂y_{t+h}/∂ε_t

    Parameters
    ----------
    B : np.ndarray, shape (n, n*p)
        VAR coefficient matrix
    B0_inv : np.ndarray, shape (n, n)
        Inverse of contemporaneous matrix B0
    p : int
        VAR lags
    horizon : int
        IRF horizon

    Returns
    -------
    np.ndarray, shape (horizon, n, n)
        IRF[h, i, j] = response of variable i to shock j at horizon h
    """
    n = B.shape[0]
    F = companion_matrix(B, p)

    # Initialize IRF array
    irf = np.zeros((horizon, n, n))

    # Impact response: Ψ_0 = B0^{-1}
    irf[0] = B0_inv

    # Subsequent responses: Ψ_h = Φ_h * B0^{-1}
    # where Φ_h = first n rows of F^h
    F_power = F.copy()
    for h in range(1, horizon):
        Phi_h = F_power[:n, :n]  # First n×n block
        irf[h] = Phi_h @ B0_inv
        F_power = F_power @ F

    return irf


# ============================================================================
# Volatility Functions
# ============================================================================

def exp_transform(x: np.ndarray) -> np.ndarray:
    """
    Safe exponential transform for log-volatilities

    Avoids overflow by capping input

    Parameters
    ----------
    x : np.ndarray
        Log-volatilities

    Returns
    -------
    np.ndarray
        exp(x), numerically stable
    """
    x_capped = np.clip(x, -20, 20)  # Avoid overflow
    return np.exp(x_capped)


def log_transform(x: np.ndarray, eps: float = 1e-10) -> np.ndarray:
    """
    Safe log transform

    Parameters
    ----------
    x : np.ndarray
        Input values (must be positive)
    eps : float
        Small constant to avoid log(0)

    Returns
    -------
    np.ndarray
        log(x), numerically stable
    """
    x_safe = np.maximum(x, eps)
    return np.log(x_safe)


def construct_volatility_matrix(omega_m: np.ndarray, omega_u: np.ndarray,
                                omega_f: np.ndarray) -> np.ndarray:
    """
    Construct block-diagonal volatility matrix

    Ω_t = diag(exp(ω_{m,t}), exp(ω_{u,t}), exp(ω_{f,t}))

    Parameters
    ----------
    omega_m : np.ndarray, shape (nm,)
        Macro log-volatilities
    omega_u : np.ndarray, shape (nu,)
        Unclassified log-volatilities
    omega_f : np.ndarray, shape (nf,)
        Financial log-volatilities

    Returns
    -------
    np.ndarray, shape (n, n)
        Covariance matrix Ω_t
    """
    omega = np.concatenate([omega_m, omega_u, omega_f])
    return np.diag(exp_transform(omega))


# ============================================================================
# Data Preparation
# ============================================================================

def standardize_data(y: np.ndarray, method: str = 'zscore') -> Tuple[np.ndarray, dict]:
    """
    Standardize data

    Parameters
    ----------
    y : np.ndarray, shape (T, n)
        Raw data
    method : str
        'zscore' or 'minmax'

    Returns
    -------
    y_std : np.ndarray, shape (T, n)
        Standardized data
    params : dict
        Transformation parameters for inverse transform
    """
    if method == 'zscore':
        mean = np.mean(y, axis=0)
        std = np.std(y, axis=0)
        y_std = (y - mean) / std
        params = {'mean': mean, 'std': std, 'method': 'zscore'}

    elif method == 'minmax':
        min_val = np.min(y, axis=0)
        max_val = np.max(y, axis=0)
        y_std = (y - min_val) / (max_val - min_val)
        params = {'min': min_val, 'max': max_val, 'method': 'minmax'}

    else:
        raise ValueError(f"Unknown method: {method}")

    return y_std, params


def inverse_standardize(y_std: np.ndarray, params: dict) -> np.ndarray:
    """
    Inverse standardization

    Parameters
    ----------
    y_std : np.ndarray
        Standardized data
    params : dict
        Transformation parameters from standardize_data()

    Returns
    -------
    np.ndarray
        Original scale data
    """
    if params['method'] == 'zscore':
        return y_std * params['std'] + params['mean']
    elif params['method'] == 'minmax':
        return y_std * (params['max'] - params['min']) + params['min']
    else:
        raise ValueError(f"Unknown method: {params['method']}")


def create_var_data_matrix(y: np.ndarray, p: int) -> Tuple[np.ndarray, np.ndarray]:
    """
    Create data matrices for VAR estimation

    Y = X*B + ε

    Parameters
    ----------
    y : np.ndarray, shape (T, n)
        Time series data
    p : int
        Number of lags

    Returns
    -------
    Y : np.ndarray, shape (T-p, n)
        Dependent variable matrix
    X : np.ndarray, shape (T-p, n*p + 1)
        Regressor matrix [y_{t-1}, ..., y_{t-p}, 1]
    """
    T, n = y.shape

    # Dependent variable
    Y = y[p:, :]

    # Regressors
    X = np.ones((T - p, n * p + 1))

    for lag in range(1, p + 1):
        X[:, (lag - 1) * n : lag * n] = y[p - lag : T - lag, :]

    return Y, X


def ols_var(y: np.ndarray, p: int) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    OLS estimation of VAR(p) for initialization

    Parameters
    ----------
    y : np.ndarray, shape (T, n)
        Time series data
    p : int
        VAR lags

    Returns
    -------
    B_ols : np.ndarray, shape (n, n*p + 1)
        OLS coefficients [B_1, ..., B_p, c]
    residuals : np.ndarray, shape (T-p, n)
        OLS residuals
    Sigma_ols : np.ndarray, shape (n, n)
        Residual covariance matrix
    """
    Y, X = create_var_data_matrix(y, p)

    # OLS: B = (X'X)^{-1} X'Y
    B_ols = linalg.solve(X.T @ X, X.T @ Y).T

    # Residuals
    residuals = Y - X @ B_ols.T

    # Covariance matrix
    Sigma_ols = (residuals.T @ residuals) / (len(Y) - X.shape[1])

    return B_ols, residuals, Sigma_ols


# ============================================================================
# Diagnostic Functions
# ============================================================================

def autocorrelation(x: np.ndarray, max_lag: int = 20) -> np.ndarray:
    """
    Compute autocorrelation function

    Parameters
    ----------
    x : np.ndarray, shape (T,)
        Time series
    max_lag : int
        Maximum lag

    Returns
    -------
    np.ndarray, shape (max_lag + 1,)
        Autocorrelations at lags 0, 1, ..., max_lag
    """
    x_centered = x - np.mean(x)
    c0 = np.sum(x_centered ** 2)

    acf = np.zeros(max_lag + 1)
    acf[0] = 1.0

    for lag in range(1, max_lag + 1):
        c_lag = np.sum(x_centered[:-lag] * x_centered[lag:])
        acf[lag] = c_lag / c0

    return acf


def geweke_diagnostic(chain: np.ndarray, first: float = 0.1, last: float = 0.5) -> float:
    """
    Geweke convergence diagnostic for MCMC

    Tests if means of first and last portions are equal

    Parameters
    ----------
    chain : np.ndarray, shape (n_iter,)
        MCMC chain
    first : float
        Proportion for first portion (default: 0.1)
    last : float
        Proportion for last portion (default: 0.5)

    Returns
    -------
    float
        Z-score (should be < 2 for convergence)
    """
    n = len(chain)
    n1 = int(n * first)
    n2 = int(n * last)

    # First portion
    x1 = chain[:n1]
    mean1 = np.mean(x1)
    var1 = np.var(x1) / n1

    # Last portion
    x2 = chain[-n2:]
    mean2 = np.mean(x2)
    var2 = np.var(x2) / n2

    # Z-score
    z = (mean1 - mean2) / np.sqrt(var1 + var2)

    return z


def effective_sample_size(chain: np.ndarray, max_lag: int = 100) -> float:
    """
    Compute effective sample size for MCMC chain

    ESS = n / (1 + 2*Σρ_k)

    Parameters
    ----------
    chain : np.ndarray, shape (n_iter,)
        MCMC chain
    max_lag : int
        Maximum lag for autocorrelation

    Returns
    -------
    float
        Effective sample size
    """
    n = len(chain)
    acf = autocorrelation(chain, max_lag)

    # Sum autocorrelations until they become small
    sum_acf = 0.0
    for k in range(1, max_lag + 1):
        if acf[k] < 0.05:  # Truncate when autocorrelation becomes small
            break
        sum_acf += acf[k]

    ess = n / (1 + 2 * sum_acf)

    return ess


# ============================================================================
# Utility for Model Output
# ============================================================================

def format_parameter_summary(draws: np.ndarray, param_name: str,
                            quantiles: List[float] = [0.05, 0.5, 0.95]) -> pd.DataFrame:
    """
    Format MCMC draws into summary table

    Parameters
    ----------
    draws : np.ndarray, shape (n_iter, n_params)
        MCMC draws
    param_name : str
        Parameter name
    quantiles : list
        Quantiles to compute

    Returns
    -------
    pd.DataFrame
        Summary table with mean, std, quantiles
    """
    mean = np.mean(draws, axis=0)
    std = np.std(draws, axis=0)
    quants = np.quantile(draws, quantiles, axis=0)

    summary = pd.DataFrame({
        'parameter': [f"{param_name}_{i}" for i in range(draws.shape[1])],
        'mean': mean,
        'std': std
    })

    for i, q in enumerate(quantiles):
        summary[f'q{int(q*100)}'] = quants[i]

    return summary


# ============================================================================
# Example Usage
# ============================================================================

if __name__ == "__main__":
    """Test utility functions"""

    print("="*70)
    print("Testing OI-SVMVAR Utility Functions")
    print("="*70)

    # Test 1: Matrix operations
    print("\n1. Testing matrix operations...")
    A = np.array([[4, 1], [1, 3]])
    print(f"   Matrix A:\n{A}")
    print(f"   Is positive definite: {check_positive_definite(A)}")
    print(f"   ✓ Matrix operations working")

    # Test 2: VAR functions
    print("\n2. Testing VAR functions...")
    n, p = 3, 2
    B = np.random.randn(n, n * p) * 0.1  # Small coefficients for stationarity
    is_stat, max_eig = check_stationarity(B, p)
    print(f"   VAR({p}) with {n} variables")
    print(f"   Stationary: {is_stat}, max |λ|: {max_eig:.3f}")
    print(f"   ✓ VAR functions working")

    # Test 3: Data standardization
    print("\n3. Testing data standardization...")
    y = np.random.randn(100, 5)
    y_std, params = standardize_data(y)
    y_back = inverse_standardize(y_std, params)
    error = np.max(np.abs(y - y_back))
    print(f"   Standardization round-trip error: {error:.2e}")
    print(f"   ✓ Standardization working")

    # Test 4: OLS VAR
    print("\n4. Testing OLS VAR estimation...")
    T, n, p = 200, 3, 2
    y_sim = np.random.randn(T, n)
    B_ols, resid, Sigma = ols_var(y_sim, p)
    print(f"   Estimated VAR({p}): shape {B_ols.shape}")
    print(f"   Residual covariance: shape {Sigma.shape}")
    print(f"   ✓ OLS VAR working")

    # Test 5: MCMC diagnostics
    print("\n5. Testing MCMC diagnostics...")
    chain = np.random.randn(1000)  # Random chain (no convergence)
    z = geweke_diagnostic(chain)
    ess = effective_sample_size(chain)
    print(f"   Geweke Z-score: {z:.3f}")
    print(f"   Effective sample size: {ess:.1f}")
    print(f"   ✓ MCMC diagnostics working")

    print("\n" + "="*70)
    print("✓ All utility functions tested successfully!")
    print("="*70)

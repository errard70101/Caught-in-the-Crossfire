"""Data-generating process utilities for the Thread 1 matvec proof-of-concept.

Implements the building blocks of the SV-aware latent-state precision

    Kbar = A' D A  +  lambda M_m' M_m,
    A    = H_B S^m  (with S^m = I in this PoC),
    D    = blockdiag(D_1, ..., D_T),  D_t = B0' U_t^{-1} B0,

following the report at theory/mf_oi_svmvar_report/main.tex.

All operators that are O(Tn) in nnz are returned as scipy.sparse matrices.
H_B is banded with bandwidth p*n; M_m has at most 5 nonzeros per row for
Mariano-Murasawa growth aggregation.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import scipy.sparse as sp


@dataclass
class DGP:
    """Container for a single PoC draw of model primitives."""

    n: int
    T: int
    p: int
    B_list: list[np.ndarray]
    B0: np.ndarray
    U: np.ndarray
    M_m: sp.csr_matrix
    lam: float
    seed: int

    @property
    def Tn(self) -> int:
        return self.T * self.n


def _stable_var_coefs(n: int, p: int, target_radius: float, rng: np.random.Generator) -> list[np.ndarray]:
    """Draw VAR(p) coefficients with companion spectral radius below target_radius.

    Approach: independent Gaussian entries, then rescale all B_i jointly until
    the companion matrix has spectral radius equal to target_radius.
    """
    raw = [rng.standard_normal((n, n)) / (p * np.sqrt(n)) for _ in range(p)]
    comp = _companion(raw)
    rho = max(abs(np.linalg.eigvals(comp)))
    if rho == 0.0:
        return raw
    scale = target_radius / rho
    return [scale * B for B in raw]


def _companion(B_list: list[np.ndarray]) -> np.ndarray:
    n = B_list[0].shape[0]
    p = len(B_list)
    top = np.hstack(B_list)
    if p == 1:
        return top
    bottom = np.hstack([np.eye(n * (p - 1)), np.zeros((n * (p - 1), n))])
    return np.vstack([top, bottom])


def build_H_B(B_list: list[np.ndarray], T: int) -> sp.csr_matrix:
    """Banded Tn x Tn sparse H_B with identity on the diagonal and -B_i on
    the i-th sub-diagonal block (i = 1..p). Lags that fall before t=1 are
    truncated, which matches absorbing initial conditions into c_B.

    Initial-condition handling
    --------------------------
    The first ``p`` dates (rows 0..p-1) have *fewer* off-diagonal entries
    than interior rows: row t carries -B_k blocks only for k <= t. So the
    quadratic form x' H_B' D H_B x evaluates the VAR residual energy at
    dates 0..p-1 using only the available lags, which is mathematically a
    truncated-lag prior on (y_0, ..., y_{p-1}). The matvec is internally
    consistent (explicit and matrix-free agree to machine precision), but
    posterior calibration of those boundary dates differs from interior
    dates -- worth flagging when this operator is plugged into a real
    MCMC. The standard fix is to pre-condition on observed pre-sample
    values and reabsorb them into a constant term c_B, which is *not*
    done in this PoC (S^o is left implicit).

    Vectorised via bulk COO construction (block-diagonal eye plus
    np.tile/np.repeat patterns for each lag) to handle stress dimensions.
    """
    n = B_list[0].shape[0]
    p = len(B_list)
    Tn = T * n

    # 1. Diagonal part: identity matrix blocks
    diag_rows = np.arange(Tn)
    diag_cols = np.arange(Tn)
    diag_data = np.ones(Tn)

    all_rows = [diag_rows]
    all_cols = [diag_cols]
    all_data = [diag_data]

    # Pre-generate block templates
    r_block, c_block = np.meshgrid(np.arange(n), np.arange(n), indexing='ij')
    r_block = r_block.flatten()
    c_block = c_block.flatten()

    # 2. Sub-diagonal blocks for each lag k
    for k in range(1, p + 1):
        if k >= T:
            continue
        Bk = B_list[k - 1]
        num_blocks = T - k
        
        offsets = np.arange(k, T)
        row_offsets = offsets * n
        col_offsets = (offsets - k) * n
        
        r_k = (row_offsets[:, None] + r_block[None, :]).flatten()
        c_k = (col_offsets[:, None] + c_block[None, :]).flatten()
        data_k = np.tile((-Bk).flatten(), num_blocks)
        
        all_rows.append(r_k)
        all_cols.append(c_k)
        all_data.append(data_k)

    # Concatenate all parts
    rows = np.concatenate(all_rows)
    cols = np.concatenate(all_cols)
    data = np.concatenate(all_data)

    return sp.csr_matrix((data, (rows, cols)), shape=(Tn, Tn))


def simulate_log_variance(n: int, T: int, mu: np.ndarray, rho: float, sigma: float, rng: np.random.Generator) -> np.ndarray:
    """Simulate independent AR(1) log-variances h_{i,t} per variable.
    Here h denotes log-variance, not log-volatility.

    Returns U of shape (T, n) holding diag(U_t) = exp(h_t).
    """
    h = np.empty((T, n))
    h[0] = mu
    for t in range(1, T):
        h[t] = mu + rho * (h[t - 1] - mu) + sigma * rng.standard_normal(n)
    return np.exp(h)


def build_B0(n: int, rng: np.random.Generator, off_diag_scale: float = 0.3) -> np.ndarray:
    """Lower-triangular B0 with unit diagonal and Gaussian off-diagonals."""
    B0 = np.eye(n)
    for i in range(1, n):
        for j in range(i):
            B0[i, j] = off_diag_scale * rng.standard_normal()
    return B0


def build_M_m_growth(T: int, n: int, lf_indices: list[int], start_quarter: int = 2) -> sp.csr_matrix:
    """Mariano-Murasawa monthly->quarterly growth-rate aggregation.

    For each low-frequency variable index i in lf_indices, and each quarter
    q whose end-month tau = 3*q is in [3*start_quarter, T], place a row with
    weights (1/3, 2/3, 1, 2/3, 1/3) at months (tau-4, ..., tau) for variable i.

    Rows are stacked variable-major: all quarters of lf_indices[0] first, etc.
    """
    weights = np.array([1.0 / 3, 2.0 / 3, 1.0, 2.0 / 3, 1.0 / 3])
    rows: list[int] = []
    cols: list[int] = []
    data: list[float] = []
    row_idx = 0
    for i in lf_indices:
        for q in range(start_quarter, T // 3 + 1):
            tau = 3 * q  # 1-based end month
            for k, w in enumerate(weights):
                month = tau - 4 + k  # 1-based
                if 1 <= month <= T:
                    t = month - 1  # 0-based
                    rows.append(row_idx)
                    cols.append(t * n + i)
                    data.append(w)
            row_idx += 1
    num_rows = row_idx
    return sp.csr_matrix((data, (rows, cols)), shape=(num_rows, T * n))


def sample_dgp(n: int, T: int, p: int, *, seed: int = 0, target_radius: float = 0.9,
               sv_mu: float = -1.0, sv_rho: float = 0.95, sv_sigma: float = 0.3,
               lam: float = 1e4, lf_indices: list[int] | None = None) -> DGP:
    """Sample a full DGP draw for the matvec PoC."""
    rng = np.random.default_rng(seed)
    B_list = _stable_var_coefs(n, p, target_radius, rng)
    B0 = build_B0(n, rng)
    mu = sv_mu * np.ones(n)
    U = simulate_log_variance(n, T, mu, sv_rho, sv_sigma, rng)
    if lf_indices is None:
        lf_indices = [0]
    M_m = build_M_m_growth(T, n, lf_indices)
    return DGP(n=n, T=T, p=p, B_list=B_list, B0=B0, U=U, M_m=M_m, lam=lam, seed=seed)


if __name__ == "__main__":
    dgp = sample_dgp(n=3, T=20, p=2, seed=42)
    print(f"n={dgp.n}, T={dgp.T}, p={dgp.p}, Tn={dgp.Tn}")
    H_B = build_H_B(dgp.B_list, dgp.T)
    print(f"H_B shape={H_B.shape}, nnz={H_B.nnz}")
    print(f"M_m shape={dgp.M_m.shape}, nnz={dgp.M_m.nnz}")
    print(f"companion radius={max(abs(np.linalg.eigvals(_companion(dgp.B_list)))):.4f}")

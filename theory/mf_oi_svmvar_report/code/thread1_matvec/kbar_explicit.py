"""Explicit (ground-truth) assembly of Kbar = A' D A + lambda M_m' M_m.

Used only for verification against the matrix-free product in
``kbar_matfree.py``. Forms the full Tn x Tn precision once and exposes a
matvec.
"""

from __future__ import annotations

import numpy as np
import scipy.sparse as sp

from dgp import DGP, build_H_B


def build_D_block_diag(B0: np.ndarray, U: np.ndarray) -> sp.csr_matrix:
    """Assemble D = blockdiag(D_1, ..., D_T) with D_t = B0' diag(1/U_t) B0.

    Parameters
    ----------
    B0 : (n, n) structural impact matrix with unit diagonal. The production
         OI target is general dense; lower-triangular inputs are legacy test
         cases only.
    U  : (T, n) array of diagonal entries of U_t (volatilities, *not* log-vols).
    """
    T, n = U.shape
    blocks = []
    B0T = B0.T
    for t in range(T):
        Dt = B0T @ np.diag(1.0 / U[t]) @ B0
        blocks.append(Dt)
    return sp.block_diag(blocks, format="csr")


def build_Kbar_explicit(dgp: DGP) -> sp.csr_matrix:
    """Form Kbar densely in sparse format for verification."""
    H_B = build_H_B(dgp.B_list, dgp.T)
    # A = H_B S^m, with S^m = I in this PoC
    A = H_B
    D = build_D_block_diag(dgp.B0, dgp.U)
    AtDA = (A.T @ D @ A).tocsr()
    MtM = (dgp.M_m.T @ dgp.M_m).tocsr()
    return (AtDA + dgp.lam * MtM).tocsr()


def assert_spd_small(Kbar: sp.csr_matrix, max_dim: int = 400) -> None:
    """Cheap SPD sanity check for Kbar.

    Uses dense Cholesky for small matrices (dimension <= max_dim).
    For larger matrices, runs a cheap sparse symmetry check and a randomized
    positive-definiteness check (x' K x > 0 for random vectors x).

    Raises ``AssertionError`` if symmetry or positive-definiteness checks fail.
    """
    if Kbar.shape[0] > max_dim:
        # 1. Cheap sparse symmetry check using a relative tolerance. Sparse
        #    matmul accumulates ~eps * nnz_per_row * max_entry of skew, which
        #    scales with lambda; an absolute 1e-10 would spuriously fail at
        #    large lambda. Use the matrix scale as the reference instead.
        diff = Kbar - Kbar.T
        if diff.nnz > 0:
            max_diff = float(np.abs(diff.data).max())
            scale = float(np.abs(Kbar.data).max()) if Kbar.nnz > 0 else 1.0
            rel_skew = max_diff / max(scale, 1e-300)
            assert rel_skew < 1e-10, (
                f"Kbar not symmetric (sparse check): "
                f"max|K - K.T| = {max_diff:.2e}, "
                f"max|K| = {scale:.2e}, rel = {rel_skew:.2e}"
            )
        # 2. Randomized PSD check: x' Kbar x > 0 for 5 random standard normal vectors
        rng = np.random.default_rng(0)
        for i in range(5):
            x = rng.standard_normal(Kbar.shape[0])
            quad = float(x @ (Kbar @ x))
            assert quad > 0.0, (
                f"Kbar is not positive definite (randomized check index {i}): x' Kbar x = {quad:.4e} <= 0"
            )
        return

    K = Kbar.toarray()
    rel_sym = float(np.linalg.norm(K - K.T) / max(np.linalg.norm(K), 1e-300))
    assert rel_sym < 1e-10, (
        f"Kbar not symmetric: ||K - K.T||_F / ||K||_F = {rel_sym:.2e}"
    )
    # Symmetrise before Cholesky -- sparse matmul leaves O(eps) skew that
    # would otherwise spuriously fail the SPD check.
    Ks = 0.5 * (K + K.T)
    try:
        np.linalg.cholesky(Ks)
    except np.linalg.LinAlgError as e:
        raise AssertionError(f"Kbar not SPD: {e}") from e


def explicit_matvec(Kbar: sp.csr_matrix, x: np.ndarray) -> np.ndarray:
    return Kbar @ x


if __name__ == "__main__":
    from dgp import sample_dgp

    dgp = sample_dgp(n=3, T=20, p=2, seed=42, lam=1e4)
    Kbar = build_Kbar_explicit(dgp)
    print(f"Kbar shape={Kbar.shape}, nnz={Kbar.nnz}")
    print(f"Kbar symmetric? max|K - K.T| = {abs(Kbar - Kbar.T).max():.2e}")
    # PSD spot check
    rng = np.random.default_rng(0)
    x = rng.standard_normal(dgp.Tn)
    quad = float(x @ (Kbar @ x))
    print(f"x' Kbar x = {quad:.4f} (should be > 0)")

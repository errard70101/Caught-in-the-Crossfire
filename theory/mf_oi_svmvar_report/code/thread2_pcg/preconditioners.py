"""Preconditioners for the SV-aware MF-OI-SVMVAR latent-state precision.

This module exposes five preconditioners for ``Kbar = A' D A + lambda M' M``:

    * ``none``                        -- no preconditioning (identity)
    * ``jacobi``                      -- scalar diagonal Jacobi
    * ``block_jacobi``                -- block-Jacobi by date (n x n blocks)
    * ``time_averaged_lu``            -- strong preconditioner: replace U_t
                                         by its time average, factor the
                                         resulting time-invariant Kbar once
                                         with sparse LU, reuse.
    * ``time_averaged_chol``          -- same as ``time_averaged_lu`` but
                                         uses CHOLMOD (via ``scikit-sparse``)
                                         to exploit SPD structure.

Design notes
------------

* matvec at PCG time is supplied by the matrix-free ``SVAwareKbar`` operator
  in ``thread1_matvec/kbar_matfree.py``. None of the preconditioners alters
  that.
* For ``jacobi`` and ``block_jacobi`` we extract diagonal entries / blocks
  from the explicit ``Kbar``. As discussed in ``THREAD2_NOTE.md``, this is
  a one-off setup cost that is acceptable for a go/no-go benchmark; a
  production sampler would derive the (t,t) block analytically without
  forming Kbar.
* ``time_averaged_lu`` builds a *different* Kbar where ``U`` is replaced by
  its row-mean (a time-invariant approximation), so the resulting precision
  is block-Toeplitz plus the unchanged aggregation term. A single sparse
  LU factorisation is reused for every PCG iteration.

All preconditioners are returned as ``scipy.sparse.linalg.LinearOperator``
so they can be passed directly to ``scipy.sparse.linalg.cg`` via ``M=``.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Allow imports from sibling thread1 directory.
_THIS_DIR = Path(__file__).resolve().parent
_THREAD1_DIR = _THIS_DIR.parent / "thread1_matvec"
if str(_THREAD1_DIR) not in sys.path:
    sys.path.insert(0, str(_THREAD1_DIR))

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

from dgp import DGP, build_H_B  # type: ignore
from kbar_explicit import build_Kbar_explicit  # type: ignore


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _identity_op(Tn: int) -> spla.LinearOperator:
    return spla.LinearOperator(
        shape=(Tn, Tn), matvec=lambda x: x, rmatvec=lambda x: x, dtype=np.float64
    )


# ---------------------------------------------------------------------------
# Jacobi (scalar diagonal)
# ---------------------------------------------------------------------------


def build_jacobi(Kbar: sp.csr_matrix) -> spla.LinearOperator:
    """Return M^{-1} = diag(1 / diag(Kbar))."""
    d = Kbar.diagonal()
    if np.any(d <= 0.0):
        raise ValueError("Jacobi preconditioner requires positive diagonal entries.")
    inv = 1.0 / d
    return spla.LinearOperator(
        shape=Kbar.shape,
        matvec=lambda x: inv * x,
        rmatvec=lambda x: inv * x,
        dtype=np.float64,
    )


# ---------------------------------------------------------------------------
# Block-Jacobi by date
# ---------------------------------------------------------------------------


def _extract_diag_blocks(Kbar: sp.csr_matrix, T: int, n: int) -> np.ndarray:
    """Return an array ``(T, n, n)`` of the n x n diagonal blocks of Kbar."""
    K = Kbar.tocsr()
    out = np.empty((T, n, n), dtype=np.float64)
    for t in range(T):
        sl = slice(t * n, (t + 1) * n)
        out[t] = K[sl, :][:, sl].toarray()
    return out


def build_block_jacobi(Kbar: sp.csr_matrix, T: int, n: int) -> spla.LinearOperator:
    """Block-Jacobi by date: factor each (t,t) block and apply per-block.

    The setup cost is ``T`` n x n inversions (LAPACK batched) plus block
    extraction. PCG application is a single ``np.linalg.solve`` on the
    pre-computed inverse stack, vectorised across dates -- so the apply
    cost is dominated by BLAS, not Python overhead.
    """
    blocks = _extract_diag_blocks(Kbar, T, n)
    # Pre-invert each block once. For small n this is cheap and turns the
    # apply into a single batched matvec. The blocks here are SPD by
    # construction (sum of B_k' D_{t+k} B_k + lambda M_m'M_m diagonal
    # contribution + D_t itself), so inversion is well-defined; we use a
    # batched solve against the identity which is numerically equivalent.
    eye = np.broadcast_to(np.eye(n), (T, n, n))
    inv_blocks = np.linalg.solve(blocks, eye)  # (T, n, n)
    Tn = T * n

    def apply(x: np.ndarray) -> np.ndarray:
        X = x.reshape(T, n)
        # y_t = inv_blocks[t] @ x_t  ==  einsum('tij,tj->ti', inv_blocks, X)
        Y = np.einsum("tij,tj->ti", inv_blocks, X, optimize=True)
        return Y.reshape(Tn)

    return spla.LinearOperator(
        shape=(Tn, Tn), matvec=apply, rmatvec=apply, dtype=np.float64
    )


# ---------------------------------------------------------------------------
# Time-averaged sparse LU preconditioner ("strong" preconditioner upper bound)
# ---------------------------------------------------------------------------


def _build_time_averaged_kbar(dgp: DGP) -> sp.csc_matrix:
    """Assemble Kbar with the time-averaged precision block.

    The correct time-average of the per-date precision blocks is

        D_bar  =  mean_t( D_t )
              =  mean_t( B0' diag(1/U_t) B0 )
              =  B0' diag( mean_t(1/U_t) ) B0,

    NOT the naive ``B0' diag(1 / mean_t(U_t)) B0``. The two differ for
    any non-degenerate SV by Jensen's inequality on the convex function
    ``u -> 1/u``. We implement the correct form by passing a fake
    constant ``U_t = U_avg_proxy`` where
    ``1 / U_avg_proxy = mean_t(1 / U_t)``, so that
    ``build_D_block_diag`` (which inverts U coordinatewise) reproduces
    ``mean_t(1/U_t)`` exactly.
    """
    n, T = dgp.n, dgp.T
    inv_U_mean = (1.0 / dgp.U).mean(axis=0)  # (n,)
    U_avg_proxy = np.broadcast_to(1.0 / inv_U_mean, (T, n)).copy()
    dgp_avg = DGP(
        n=n, T=T, p=dgp.p,
        B_list=dgp.B_list, B0=dgp.B0, U=U_avg_proxy,
        M_m=dgp.M_m, lam=dgp.lam, seed=dgp.seed,
    )
    return build_Kbar_explicit(dgp_avg).tocsc()


def build_time_averaged_lu(dgp: DGP) -> tuple[spla.LinearOperator, float]:
    """Strong preconditioner via sparse LU on the time-averaged Kbar."""
    Kbar_avg = _build_time_averaged_kbar(dgp)
    solver = spla.splu(Kbar_avg)
    Tn = dgp.T * dgp.n
    op = spla.LinearOperator(
        shape=(Tn, Tn),
        matvec=lambda x: solver.solve(x),
        rmatvec=lambda x: solver.solve(x),
        dtype=np.float64,
    )
    return op, float("nan")


def build_time_averaged_chol(dgp: DGP) -> tuple[spla.LinearOperator, float]:
    """Strong preconditioner via CHOLMOD on the time-averaged Kbar.

    Uses ``sksparse.cholmod.cholesky`` (supernodal sparse Cholesky). This
    is the apples-to-apples replacement for the ``splu`` factor when
    ``scikit-sparse`` is available.
    """
    from sksparse.cholmod import cholesky as cholmod_cholesky  # type: ignore

    Kbar_avg = _build_time_averaged_kbar(dgp)
    factor = cholmod_cholesky(Kbar_avg)
    Tn = dgp.T * dgp.n
    op = spla.LinearOperator(
        shape=(Tn, Tn),
        matvec=lambda x: factor(x),
        rmatvec=lambda x: factor(x),
        dtype=np.float64,
    )
    return op, float("nan")


# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------


def make_preconditioner(
    name: str, Kbar: sp.csr_matrix, dgp: DGP
) -> tuple[spla.LinearOperator | None, dict]:
    """Construct a preconditioner by name.

    Returns
    -------
    M : LinearOperator | None
        ``None`` if ``name == 'none'``; ``scipy.sparse.linalg.cg`` treats
        ``M=None`` as the identity preconditioner.
    info : dict
        Auxiliary information (e.g. ``cond_proxy`` for ``time_averaged_lu``).
    """
    if name == "none":
        return None, {}
    if name == "jacobi":
        return build_jacobi(Kbar), {}
    if name == "block_jacobi":
        return build_block_jacobi(Kbar, dgp.T, dgp.n), {}
    if name == "time_averaged_lu":
        op, cond_proxy = build_time_averaged_lu(dgp)
        return op, {"cond_proxy": cond_proxy}
    if name == "time_averaged_chol":
        op, cond_proxy = build_time_averaged_chol(dgp)
        return op, {"cond_proxy": cond_proxy}
    raise ValueError(f"unknown preconditioner: {name!r}")


PRECONDITIONER_NAMES = [
    "none", "jacobi", "block_jacobi", "time_averaged_lu", "time_averaged_chol"
]


if __name__ == "__main__":
    from dgp import sample_dgp  # type: ignore

    dgp = sample_dgp(n=4, T=30, p=2, seed=42, lam=1e4)
    Kbar = build_Kbar_explicit(dgp)
    for name in PRECONDITIONER_NAMES:
        M, info = make_preconditioner(name, Kbar, dgp)
        if M is None:
            print(f"{name:18s}: identity (no preconditioning)")
            continue
        rng = np.random.default_rng(0)
        x = rng.standard_normal(dgp.Tn)
        y = M @ x
        print(f"{name:18s}: ||M^-1 x|| / ||x|| = {np.linalg.norm(y) / np.linalg.norm(x):.3e}  info={info}")

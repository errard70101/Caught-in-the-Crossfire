"""Banded time-averaged precision K_pre for Thread 2c.

Builds the SciPy lower-band storage of the time-averaged preconditioner

    K_pre = H_B' (I_T kron D_bar) H_B + lambda M_m' M_m,
    D_bar = B0' diag(mean_t 1/U_t) B0,

WITHOUT materialising the global ``Tn x Tn`` sparse matrix. This is the
matrix-free contribution of Thread 2c: only an ``(u+1) x Tn`` banded
array is allocated, where ``u`` is the scalar half-bandwidth.

Storage convention (SciPy lower-band, used by
``scipy.linalg.cholesky_banded(ab, lower=True)``):

    ab[i - j, j] == K_pre[i, j]   for  i >= j  and  i - j <= u.

The code, tests, factorisation, solve, and CSV diagnostics in this
thread use the lower convention end-to-end. Do not switch conventions.

Bandwidth formula (from THREAD2C_MATRIX_FREE_PROTOCOL.md):

    u_var = p * n + (n - 1),
    u_agg = exact scalar half-bandwidth of M_m' M_m  (<= 4 * n_m),
    u     = max(u_var, u_agg).

``u_agg`` is computed directly from ``M_m`` rather than using the
conservative ``4 * n`` bound; for Mariano-Murasawa aggregation on
``n_m << n`` macro variables this materially reduces banded storage.

Block formulas (derived from K_pre = sum_r H_B[r,:]' D_bar H_B[r,:]):

* Diagonal block K_pre[s, s]:

    K_pre[s, s] = D_bar + sum_{k=1}^{J} B_k' D_bar B_k,
    J = min(p, T - 1 - s).

* Sub-diagonal block K_pre[s+delta, s], delta = 1..p:

    K_pre[s+delta, s] = -D_bar B_delta
                       + sum_{k=1}^{J} B_k' D_bar B_{delta+k},
    J = min(p - delta, T - 1 - s - delta).

Boundary handling: ``J`` truncates the sum at late dates (``s + p > T-1``).
Early dates do not need a separate correction because columns ``s < p``
still receive contributions from every available H_B row that hits
column ``s``. This is verified by the random-vector matvec invariant in
``test_banded_correctness.py``.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import scipy.sparse as sp

_THIS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_THIS_DIR.parent / "thread1_matvec"))

from dgp import DGP  # type: ignore  # noqa: E402


@dataclass
class BandedKbarAvg:
    """Lower-band storage of K_pre with bookkeeping for diagnostics."""

    ab: np.ndarray  # shape (u + 1, Tn), float64
    u: int
    u_var: int
    u_agg: int
    n: int
    T: int
    p: int

    @property
    def Tn(self) -> int:
        return self.T * self.n

    @property
    def storage_bytes(self) -> int:
        return int(self.ab.nbytes)


def compute_D_bar(B0: np.ndarray, U: np.ndarray) -> np.ndarray:
    """``D_bar = B0' diag(mean_t 1/U_t) B0`` (corrected precision average)."""
    inv_U_mean = (1.0 / U).mean(axis=0)
    return B0.T @ np.diag(inv_U_mean) @ B0


def compute_u_agg(M_m: sp.spmatrix) -> int:
    """Exact scalar half-bandwidth of ``M_m' M_m``.

    Tighter than the protocol's worst-case ``4 * n`` bound. Returns 0 if
    ``M_m`` is empty (no aggregation rows).
    """
    if M_m.shape[0] == 0 or M_m.nnz == 0:
        return 0
    MtM = (M_m.T @ M_m).tocoo()
    MtM.sum_duplicates()
    if MtM.nnz == 0:
        return 0
    offsets = np.abs(MtM.row - MtM.col)
    return int(offsets.max())


def build_banded_kbar_avg(dgp: DGP) -> BandedKbarAvg:
    """Build banded ``K_pre`` without global ``Tn x Tn`` assembly.

    Returns a ``BandedKbarAvg`` whose ``.ab`` is suitable for direct
    passage to ``scipy.linalg.cholesky_banded(ab, lower=True)`` and
    ``scipy.linalg.cho_solve_banded((c, True), b)``.

    Implementation invariants:

    * Never builds the dense or sparse global ``K_pre``.
    * Builds at most an ``(u + 1) x Tn`` banded array and the small
      ``(p + 1) x (p + 1)`` cache of ``B_k' D_bar B_l`` blocks.
    * Asserts that every nonzero of ``lambda M_m' M_m`` lies within
      ``u_agg``; failure indicates a bandwidth bug, not data.
    """
    n, T, p = dgp.n, dgp.T, dgp.p
    Tn = T * n
    B_list = dgp.B_list
    lam = dgp.lam
    M_m = dgp.M_m

    # 1. Time-averaged precision block (n x n).
    D_bar = compute_D_bar(dgp.B0, dgp.U)

    # 2. Bandwidths.
    u_var = p * n + (n - 1)
    u_agg = compute_u_agg(M_m)
    u = max(u_var, u_agg)

    # 3. Banded storage allocation.
    ab = np.zeros((u + 1, Tn), dtype=np.float64)

    # 4. Cache B_k' D_bar B_l for k, l in {0, 1, ..., p}, where B_0 := I.
    #    BtDB[k, l] = B_k' D_bar B_l. Reused by every block formula below.
    B_ext = [np.eye(n)] + list(B_list)  # length p + 1
    BtDB = np.empty((p + 1, p + 1, n, n), dtype=np.float64)
    for k in range(p + 1):
        for l in range(p + 1):
            BtDB[k, l] = B_ext[k].T @ D_bar @ B_ext[l]

    # Index helpers for vectorised block placement into ab.
    i_grid, j_grid = np.meshgrid(np.arange(n), np.arange(n), indexing="ij")
    i_lt, j_lt = np.tril_indices(n)  # lower triangle (incl. diagonal) of an n x n block

    # 5. Diagonal blocks: K_pre[s, s] = D_bar + sum_{k=1..J} B_k' D_bar B_k.
    #    Place only the lower triangle of each diagonal block (incl. diag).
    for s in range(T):
        J = min(p, T - 1 - s)
        block = BtDB[0, 0].copy()  # D_bar
        for k in range(1, J + 1):
            block += BtDB[k, k]
        # Diagonal block sits at scalar rows/cols [s*n, (s+1)*n).
        # ab[(s*n + i) - (s*n + j), s*n + j] = ab[i - j, s*n + j] = block[i, j].
        ab[i_lt - j_lt, s * n + j_lt] = block[i_lt, j_lt]

    # 6. Sub-diagonal blocks: K_pre[s+delta, s] for delta = 1..p,
    #    s = 0..T-1-delta.
    #    Block formula:
    #      K_pre[s+delta, s] = -D_bar B_delta
    #                          + sum_{k=1..J} B_k' D_bar B_{delta+k},
    #      J = min(p - delta, T - 1 - s - delta).
    #    All (i, j) entries of a sub-diagonal block are in the lower
    #    triangle of the global matrix (delta*n + i - j > 0 for delta >= 1).
    for delta in range(1, p + 1):
        s_max = T - 1 - delta  # last valid s such that s + delta <= T - 1
        if s_max < 0:
            continue
        for s in range(0, s_max + 1):
            J = min(p - delta, T - 1 - s - delta)
            block = -BtDB[0, delta]  # -D_bar @ B_delta
            for k in range(1, J + 1):
                block = block + BtDB[k, delta + k]
            # Place full block at scalar rows [(s+delta)*n, (s+delta+1)*n),
            # cols [s*n, (s+1)*n):
            # ab[(s+delta)*n + i - (s*n + j), s*n + j]
            #   = ab[delta*n + i - j, s*n + j] = block[i, j].
            ab_rows = delta * n + i_grid - j_grid
            ab_cols = s * n + j_grid
            ab[ab_rows.ravel(), ab_cols.ravel()] = block.ravel()

    # 7. Add lambda * M_m' M_m into the lower band, with bandwidth assert.
    if M_m.shape[0] > 0 and M_m.nnz > 0:
        MtM = (M_m.T @ M_m).tocoo()
        MtM.sum_duplicates()
        if MtM.nnz > 0:
            mask = MtM.row >= MtM.col  # lower triangle (incl. diagonal)
            i_arr = MtM.row[mask]
            j_arr = MtM.col[mask]
            vals = lam * MtM.data[mask]
            offsets = (i_arr - j_arr).astype(np.intp)
            if offsets.size > 0:
                max_offset = int(offsets.max())
                assert max_offset <= u_agg, (
                    f"M_m' M_m has scalar offset {max_offset} > u_agg = "
                    f"{u_agg}; banded storage would silently truncate it"
                )
                # np.add.at accumulates safely even if (offsets, j_arr) has
                # repeats (e.g., from a non-canonical sparse intermediate).
                np.add.at(ab, (offsets, j_arr.astype(np.intp)), vals)

    return BandedKbarAvg(ab=ab, u=u, u_var=u_var, u_agg=u_agg, n=n, T=T, p=p)


def banded_to_dense(banded: BandedKbarAvg) -> np.ndarray:
    """Reconstruct the full symmetric dense matrix from lower-band storage.

    Used only for correctness tests against ``_build_time_averaged_kbar``.
    The production path never calls this function (it would defeat the
    no-explicit-``Kbar_avg`` invariant).
    """
    Tn = banded.Tn
    u = banded.u
    ab = banded.ab
    K = np.zeros((Tn, Tn), dtype=np.float64)
    for k in range(u + 1):
        # k-th sub-diagonal: ab[k, j] = K[j + k, j] for j in [0, Tn - k).
        for j in range(Tn - k):
            v = ab[k, j]
            K[j + k, j] = v
            if k > 0:
                K[j, j + k] = v
    return K


if __name__ == "__main__":
    from dgp import sample_dgp  # type: ignore

    sys.path.insert(0, str(_THIS_DIR.parent / "thread2_pcg"))
    from preconditioners import _build_time_averaged_kbar  # type: ignore

    dgp = sample_dgp(n=3, T=20, p=2, seed=42, lam=1e4)
    banded = build_banded_kbar_avg(dgp)
    print(f"DGP: n={dgp.n}, T={dgp.T}, p={dgp.p}, Tn={dgp.Tn}")
    print(f"Bandwidths: u_var={banded.u_var}, u_agg={banded.u_agg}, u={banded.u}")
    print(f"ab.shape={banded.ab.shape}, bytes={banded.storage_bytes:,}")

    K_ref = _build_time_averaged_kbar(dgp).toarray()
    K_dense = banded_to_dense(banded)
    fro_err = float(
        np.linalg.norm(K_dense - K_ref, "fro")
        / max(np.linalg.norm(K_ref, "fro"), 1e-300)
    )
    print(f"||banded - explicit||_F / ||explicit||_F = {fro_err:.2e}")

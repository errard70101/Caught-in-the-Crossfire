"""Matrix-free SV-aware precision product for the MF-OI-SVMVAR latent path.

Applies

    Kbar x  =  A' D A x  +  lambda M_m' M_m x,

with A = H_B (S^m = I in this PoC) and D = blockdiag(D_t),
D_t = B0' diag(1/U_t) B0, without ever forming the Tn x Tn precision.

Algorithm (per matvec):

    1. w = H_B x                                       (forward VAR)
    2. for t in 1..T:  u_t = D_t w_t                   (local SV block)
    3. z = H_B' u                                      (adjoint VAR)
    4. y = z + lambda * M_m' (M_m x)                   (aggregation penalty)

Step 1 and 3 use the sparse banded H_B; step 2 is implemented as two dense
n-vector products per date (B0 then diagonal scale then B0'), so the local
cost is O(T n^2). No FFT yet -- a basis-filter-based forward operator is a
later concern; the present PoC verifies the operator structure first.
"""

from __future__ import annotations

import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import LinearOperator

from dgp import DGP, build_H_B


class SVAwareKbar:
    """Matrix-free Kbar operator with cached H_B and M_m."""

    def __init__(self, dgp: DGP):
        self.n = dgp.n
        self.T = dgp.T
        self.Tn = dgp.Tn
        self.B0 = dgp.B0
        self.U_inv = 1.0 / dgp.U  # (T, n)
        self.M_m = dgp.M_m.tocsr()
        self.M_mT = self.M_m.T.tocsr()
        self.lam = dgp.lam
        # H_B kept sparse; basis-filter forward op is a later Thread.
        # NOTE: we do NOT cache H_B.T as a separate CSR. ``self.H_B.T`` is
        # a free CSC view of the same data; scipy executes ``H_B.T @ u``
        # as a CSC matvec without copying. Caching a transposed CSR would
        # double sparse storage for no measured speed gain.
        self.H_B = build_H_B(dgp.B_list, dgp.T).tocsr()

    def _apply_D(self, w_flat: np.ndarray) -> np.ndarray:
        """Apply block-diagonal D to a stacked Tn vector w.

        For each date t: u_t = B0' (diag(1/U_t) (B0 w_t)).

        Order-invariant target
        ----------------------
        Production `B0` is a general dense matrix under the DHK-style
        order-invariant target. Lower-triangular `B0` can be used in controlled
        legacy DGPs, but this operator must not rely on a triangular zero
        pattern. Dense multiplication is therefore the baseline path.
        """
        W = w_flat.reshape(self.T, self.n)
        # B0 w_t for all t simultaneously: shape (T, n)
        BW = W @ self.B0.T  # because (B0 w_t)_i = sum_j B0[i,j] w_t[j]
        # diag(1/U_t) scale, elementwise
        BW *= self.U_inv
        # B0' (.) for all t: (B0' v_t)_j = sum_i B0[i,j] v_t[i] => v @ B0
        out = BW @ self.B0
        return out.reshape(self.Tn)

    def matvec(self, x: np.ndarray) -> np.ndarray:
        # 1. forward VAR
        w = self.H_B @ x
        # 2. local SV block per date
        u = self._apply_D(w)
        # 3. adjoint VAR -- H_B.T returns a CSC view, no copy.
        z = self.H_B.T @ u
        # 4. aggregation penalty
        if self.M_m.shape[0] > 0:
            y_agg = self.M_m @ x
            z = z + self.lam * (self.M_mT @ y_agg)
        return z

    def as_linear_operator(self) -> LinearOperator:
        return LinearOperator(
            shape=(self.Tn, self.Tn),
            matvec=self.matvec,
            rmatvec=self.matvec,  # symmetric
            dtype=np.float64,
        )


if __name__ == "__main__":
    from dgp import sample_dgp
    from kbar_explicit import build_Kbar_explicit

    dgp = sample_dgp(n=3, T=20, p=2, seed=42, lam=1e4)
    op = SVAwareKbar(dgp)
    Kbar_ex = build_Kbar_explicit(dgp)
    rng = np.random.default_rng(0)
    x = rng.standard_normal(dgp.Tn)
    y_ex = Kbar_ex @ x
    y_mf = op.matvec(x)
    err = np.linalg.norm(y_ex - y_mf) / np.linalg.norm(y_ex)
    print(f"single-vector relative error = {err:.3e}")

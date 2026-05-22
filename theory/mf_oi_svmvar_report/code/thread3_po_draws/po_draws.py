"""Perturbation-optimisation Gaussian draws for the SV-aware MF latent state.

Target conditional posterior (cf. Thread 1/2 controlled DGP):

    y* | rest  ~  N(K^{-1} h,  K^{-1}),
    K          =  A' D A  +  lambda * M_m' M_m,
    D          =  blockdiag(D_t),  D_t = B0' diag(1/U_t) B0,
    h          =  lambda * M_m' y_L   (synthetic data h is supplied).

Perturbation-optimisation (PO) recipe (Papandreou-Yuille / Bhattacharya 2016):

    1. eta_t  ~  N(0, I_n)              for t = 1..T
       s_t    =  B0' diag(1/sqrt(U_t)) eta_t          (so Cov(s_t) = D_t)
       s      =  stack(s_t)            ==>  s ~ N(0, D)
    2. zeta   ~  N(0, I_{n_L})
       q      =  sqrt(lambda) M_m' zeta              (so Cov(q) = lambda M_m'M_m)
    3. v      =  h + A' s + q                        (then v ~ N(h, K))
    4. solve  K y = v                                ==>  y ~ N(K^{-1} h, K^{-1}).

Two concrete solvers are provided:

* ``po_draw_direct`` -- uses a single CHOLMOD factor of the exact K
  (production reference per Thread 2b).
* ``po_draw_pcg`` -- uses the matrix-free Kbar matvec from Thread 1
  with the ``time_averaged_chol`` preconditioner from Thread 2 (the only
  PCG variant that survived Thread 2 at moderate SV dispersion). All
  other lightweight preconditioners are intentionally excluded.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path
from time import perf_counter
from typing import Optional

# Allow imports from sibling thread directories.
_THIS_DIR = Path(__file__).resolve().parent
_THREAD1_DIR = _THIS_DIR.parent / "thread1_matvec"
_THREAD2_DIR = _THIS_DIR.parent / "thread2_pcg"
for _p in (_THREAD1_DIR, _THREAD2_DIR):
    sp_str = str(_p)
    if sp_str not in sys.path:
        sys.path.insert(0, sp_str)

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

from dgp import DGP, build_H_B  # type: ignore
from kbar_explicit import build_Kbar_explicit  # type: ignore
from kbar_matfree import SVAwareKbar  # type: ignore
from preconditioners import build_time_averaged_chol  # type: ignore


# ---------------------------------------------------------------------------
# Noise construction shared by both draw routines
# ---------------------------------------------------------------------------


def _build_perturbation_rhs(
    dgp: DGP,
    h: np.ndarray,
    H_B: sp.csr_matrix,
    rng: np.random.Generator,
) -> np.ndarray:
    """Construct v = h + A' s + sqrt(lambda) M' zeta, with v ~ N(h, K)."""
    T, n = dgp.T, dgp.n
    Tn = T * n
    if h.shape != (Tn,):
        raise ValueError(f"h has shape {h.shape}, expected ({Tn},).")

    # Step 1: s ~ N(0, D), with D = blockdiag(B0' diag(1/U_t) B0).
    eta = rng.standard_normal((T, n))
    # B0' diag(1/sqrt(U_t)) eta_t == B0' (eta_t / sqrt(U_t)) elementwise per t
    inv_sqrt_U = 1.0 / np.sqrt(dgp.U)  # (T, n)
    scaled = eta * inv_sqrt_U  # (T, n)
    # (B0' v_t)_j = sum_i B0[i, j] v_t[i]  ==  scaled @ B0
    s = scaled @ dgp.B0  # (T, n)
    s = s.reshape(Tn)

    # A' s = H_B' s in the PoC (S^m = I).
    AtS = H_B.T @ s

    # Step 2: zeta ~ N(0, I_{n_L}), q = sqrt(lambda) M' zeta.
    n_L = dgp.M_m.shape[0]
    if n_L > 0 and dgp.lam > 0.0:
        zeta = rng.standard_normal(n_L)
        q = np.sqrt(dgp.lam) * (dgp.M_m.T @ zeta)
    else:
        q = np.zeros(Tn)

    return h + AtS + q


# ---------------------------------------------------------------------------
# Direct CHOLMOD PO draw (production accuracy reference)
# ---------------------------------------------------------------------------


@dataclass
class DirectPOContext:
    """Cached CHOLMOD factor + sparse operators for repeated PO draws.

    Build once per parameter sweep; ``draw()`` then costs one RHS
    construction (Thread 1's O(Tn) operators) plus one CHOLMOD back-solve.
    """

    dgp: DGP
    Kbar: sp.csc_matrix
    factor: object  # sksparse.cholmod.Factor
    H_B: sp.csr_matrix
    setup_time_assembly: float
    setup_time_factor: float

    def draw(self, h: np.ndarray, rng: np.random.Generator) -> tuple[np.ndarray, float]:
        """Return one PO draw and the solve time."""
        v = _build_perturbation_rhs(self.dgp, h, self.H_B, rng)
        t0 = perf_counter()
        y = self.factor(v)
        return y, perf_counter() - t0

    def solve_mean(self, h: np.ndarray) -> np.ndarray:
        """Return the exact posterior mean K^{-1} h (no perturbation)."""
        return self.factor(h)


def build_direct_context(dgp: DGP) -> DirectPOContext:
    """Assemble Kbar explicitly and factor it with CHOLMOD."""
    from sksparse.cholmod import cholesky as cholmod_cholesky  # type: ignore

    t0 = perf_counter()
    Kbar = build_Kbar_explicit(dgp).tocsc()
    t_assemble = perf_counter() - t0

    t0 = perf_counter()
    factor = cholmod_cholesky(Kbar)
    t_factor = perf_counter() - t0

    H_B = build_H_B(dgp.B_list, dgp.T).tocsr()
    return DirectPOContext(
        dgp=dgp,
        Kbar=Kbar,
        factor=factor,
        H_B=H_B,
        setup_time_assembly=t_assemble,
        setup_time_factor=t_factor,
    )


# ---------------------------------------------------------------------------
# Matrix-free PCG PO draw (diagnostic only)
# ---------------------------------------------------------------------------


@dataclass
class PCGPODrawResult:
    y: np.ndarray
    iters: int
    relative_residual: float
    solve_time: float
    status: int


@dataclass
class PCGPOContext:
    """Cached matrix-free K matvec + CHOLMOD-on-time-averaged preconditioner."""

    dgp: DGP
    op_K: spla.LinearOperator
    op_M: spla.LinearOperator
    H_B: sp.csr_matrix
    rtol: float
    maxiter: int
    setup_time_precond: float

    def draw(self, h: np.ndarray, rng: np.random.Generator) -> PCGPODrawResult:
        v = _build_perturbation_rhs(self.dgp, h, self.H_B, rng)
        iters = 0

        def _cb(_xk: np.ndarray) -> None:
            nonlocal iters
            iters += 1

        t0 = perf_counter()
        y, info = spla.cg(
            self.op_K, v, M=self.op_M, rtol=self.rtol, atol=0.0,
            maxiter=self.maxiter, callback=_cb,
        )
        solve_time = perf_counter() - t0
        r = v - self.op_K @ y
        rel = float(np.linalg.norm(r) / max(np.linalg.norm(v), 1e-300))
        return PCGPODrawResult(
            y=y, iters=iters, relative_residual=rel,
            solve_time=solve_time, status=int(info),
        )


def build_pcg_context(
    dgp: DGP, *, rtol: float = 1e-8, maxiter: Optional[int] = None,
) -> PCGPOContext:
    """Build matrix-free K and the time_averaged_chol preconditioner."""
    op_K = SVAwareKbar(dgp).as_linear_operator()

    t0 = perf_counter()
    op_M, _info = build_time_averaged_chol(dgp)
    t_pc = perf_counter() - t0

    H_B = build_H_B(dgp.B_list, dgp.T).tocsr()
    if maxiter is None:
        maxiter = min(5 * dgp.Tn, 20000)
    return PCGPOContext(
        dgp=dgp, op_K=op_K, op_M=op_M, H_B=H_B,
        rtol=rtol, maxiter=maxiter, setup_time_precond=t_pc,
    )


# ---------------------------------------------------------------------------
# Self-check
# ---------------------------------------------------------------------------


if __name__ == "__main__":
    from dgp import sample_dgp  # type: ignore

    dgp = sample_dgp(n=4, T=30, p=2, seed=42, lam=1e4, sv_sigma=0.1)
    ctx = build_direct_context(dgp)
    print(
        f"direct setup: assembly={ctx.setup_time_assembly*1e3:.2f} ms, "
        f"factor={ctx.setup_time_factor*1e3:.2f} ms"
    )
    rng = np.random.default_rng(0)
    n_L = dgp.M_m.shape[0]
    y_L = rng.standard_normal(n_L)
    h = dgp.lam * (dgp.M_m.T @ y_L)
    mu = ctx.solve_mean(h)
    print(f"||mu||_inf = {np.abs(mu).max():.4f}")
    rng_d = np.random.default_rng(123)
    y, t_solve = ctx.draw(h, rng_d)
    print(f"direct draw solve_time={t_solve*1e3:.2f} ms, ||y - mu||={np.linalg.norm(y - mu):.4f}")

    pctx = build_pcg_context(dgp, rtol=1e-8)
    print(f"PCG setup (precond only): {pctx.setup_time_precond*1e3:.2f} ms")
    rng_p = np.random.default_rng(123)
    pres = pctx.draw(h, rng_p)
    print(
        f"PCG draw: iters={pres.iters}, rel_res={pres.relative_residual:.2e}, "
        f"time={pres.solve_time*1e3:.2f} ms"
    )
    # Same noise seed gives same RHS v; direct and PCG y should match within PCG rtol.
    diff = np.linalg.norm(pres.y - y) / max(np.linalg.norm(y), 1e-300)
    print(f"||y_pcg - y_direct|| / ||y_direct|| = {diff:.2e}  (should be ~rtol on K's condition)")

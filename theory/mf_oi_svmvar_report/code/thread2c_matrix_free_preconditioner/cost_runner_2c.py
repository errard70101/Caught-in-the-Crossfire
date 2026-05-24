"""Phased-cost runner for Thread 2c.

For one ``(n, T, p, sv_sigma, seed, lam)`` cell, run three solver paths
and time each phase separately. Phase labels are uniform across paths
so the output CSV can be aggregated and plotted directly.

Paths
-----

``direct_cholmod``  (reference)
    phase1_assembly  -- build explicit ``Kbar`` from ``(H_B, D_t, lambda M' M)``
    phase2_factor    -- CHOLMOD supernodal Cholesky on ``Kbar``
    phase3_solve     -- single ``factor(b)`` call

``pcg_time_avg_chol_explicit_avgK``  (Thread 2b reference)
    phase1_assembly  -- build ``Kbar_avg`` from the corrected precision average
                        ``D_bar = B0' diag(mean_t 1/U_t) B0`` (full ``Tn x Tn`` sparse)
    phase2_factor    -- CHOLMOD on ``Kbar_avg`` (preconditioner setup)
    phase3_solve     -- PCG to ``rtol=1e-8`` with matrix-free ``Kbar`` matvec
                        and CHOLMOD(``Kbar_avg``) preconditioner apply

``pcg_banded_time_avg_precision_chol``  (NEW Thread 2c)
    phase1_assembly  -- build lower-banded ``ab`` array for the same ``K_pre``
                        WITHOUT global ``Tn x Tn`` assembly (no-explicit-``Kbar_avg``)
    phase2_factor    -- ``scipy.linalg.cholesky_banded(ab, lower=True)``
    phase3_solve     -- PCG to ``rtol=1e-8`` with matrix-free ``Kbar`` matvec
                        and ``cho_solve_banded`` preconditioner apply

Skip rules
----------
Two separate budgets are tracked:

* ``estimate_explicit(...)`` (Thread 2b's existing ``memory_estimate.estimate``):
  if explicit ``Kbar`` exceeds the byte/nnz budget, both
  ``direct_cholmod`` and ``pcg_time_avg_chol_explicit_avgK`` are emitted
  with ``status='skipped_memory_estimate'``.

* ``estimate_banded(...)`` (new local helper):
  if the banded ``ab`` plus its Cholesky factor exceed the byte budget,
  ``pcg_banded_time_avg_precision_chol`` is emitted with
  ``status='skipped_memory_estimate'``. This is the only headline-cell
  feasibility gate for the matrix-free path.

These budgets are independent on purpose: the headline ``(n=20, T=10000,
p=24)`` cell is meant to demonstrate the regime where the explicit path
is skipped but the banded path is not. Sharing one budget would defeat
the entire point of the thread.

Per-segment timeout
-------------------
Each phase is guarded by ``signal.setitimer`` and reported as
``status='timeout_phaseN'`` on expiry.
"""

from __future__ import annotations

import signal
import sys
from contextlib import contextmanager
from dataclasses import dataclass, asdict
from pathlib import Path
from time import perf_counter
from typing import Optional

import numpy as np
import scipy.linalg as sla
import scipy.sparse as sp
import scipy.sparse.linalg as spla

# Sibling thread directories.
_THIS_DIR = Path(__file__).resolve().parent
_THREAD1_DIR = _THIS_DIR.parent / "thread1_matvec"
_THREAD2_DIR = _THIS_DIR.parent / "thread2_pcg"
_THREAD2B_DIR = _THIS_DIR.parent / "thread2b_fair_cost"
for d in (_THIS_DIR, _THREAD1_DIR, _THREAD2_DIR, _THREAD2B_DIR):
    if str(d) not in sys.path:
        sys.path.insert(0, str(d))

from dgp import DGP, sample_dgp  # type: ignore  # noqa: E402
from kbar_explicit import build_Kbar_explicit  # type: ignore  # noqa: E402
from kbar_matfree import SVAwareKbar  # type: ignore  # noqa: E402
from pcg_runner import run_pcg  # type: ignore  # noqa: E402
from memory_estimate import (  # type: ignore  # noqa: E402
    estimate as estimate_explicit,
)

from banded_kbar_avg import build_banded_kbar_avg  # noqa: E402


# ---------------------------------------------------------------------------
# Banded memory budget
# ---------------------------------------------------------------------------


_DEFAULT_MAX_BYTES_EXPLICIT = 6.0 * 1024**3   # matches Thread 2b
_DEFAULT_MAX_NNZ_EXPLICIT = 1e8
_DEFAULT_MAX_BYTES_BANDED = 6.0 * 1024**3     # ab + factor combined


@dataclass(frozen=True)
class BandedMemoryEstimate:
    n: int
    T: int
    p: int
    Tn: int
    u_var: int
    u_agg_upper: int           # 4 * n_m upper bound; tight value known only after building M_m
    u_upper: int               # max(u_var, u_agg_upper)
    ab_bytes: int              # (u_upper + 1) * Tn * 8
    factor_bytes_upper: int    # same shape as ab, conservative
    banded_total_bytes: int    # ab + factor
    skip_banded: bool
    skip_reason: str


def estimate_banded(
    n: int,
    T: int,
    p: int,
    *,
    n_m: int = 1,
    max_bytes: float = _DEFAULT_MAX_BYTES_BANDED,
) -> BandedMemoryEstimate:
    """Pre-flight banded storage estimate.

    ``n_m`` is the count of low-frequency variables subject to
    Mariano-Murasawa aggregation (defaults to 1 -- the production
    ``sample_dgp`` convention). The tight bound ``u_agg <= 4 * n_m``
    from the protocol is used. The exact ``u_agg`` from ``M_m'M_m`` is
    only known after building ``M_m``, but the bound is already safe
    for skip decisions; ``build_banded_kbar_avg`` itself asserts that
    no nonzero exceeds the bandwidth it actually allocates.
    """
    Tn = T * n
    u_var = p * n + (n - 1)
    u_agg_upper = 4 * n_m
    u_upper = max(u_var, u_agg_upper)
    ab_bytes = (u_upper + 1) * Tn * 8
    factor_bytes_upper = ab_bytes  # cholesky_banded returns the same shape
    total = ab_bytes + factor_bytes_upper

    skip = total > max_bytes
    reason = (
        f"estimated banded ab+factor = {total / 1024**3:.2f} GB > "
        f"{max_bytes / 1024**3:.2f} GB"
        if skip
        else ""
    )
    return BandedMemoryEstimate(
        n=n, T=T, p=p, Tn=Tn,
        u_var=u_var, u_agg_upper=u_agg_upper, u_upper=u_upper,
        ab_bytes=ab_bytes, factor_bytes_upper=factor_bytes_upper,
        banded_total_bytes=total,
        skip_banded=skip, skip_reason=reason,
    )


# ---------------------------------------------------------------------------
# Timeout helper (re-implemented locally so we don't depend on Thread 2b)
# ---------------------------------------------------------------------------


class SegmentTimeout(Exception):
    pass


@contextmanager
def segment_timeout(seconds: Optional[float]):
    if seconds is None or seconds <= 0:
        yield
        return

    def _handler(signum, frame):  # noqa: ARG001
        raise SegmentTimeout(f"segment exceeded {seconds:.1f}s")

    old = signal.signal(signal.SIGALRM, _handler)
    signal.setitimer(signal.ITIMER_REAL, float(seconds))
    try:
        yield
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0.0)
        signal.signal(signal.SIGALRM, old)


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------


def _build_kbar_explicit_timed(dgp: DGP) -> tuple[sp.csr_matrix, float]:
    t0 = perf_counter()
    Kbar = build_Kbar_explicit(dgp)
    return Kbar, perf_counter() - t0


def _build_kbar_avg(dgp: DGP) -> sp.csr_matrix:
    """Time-invariant ``Kbar_avg`` using ``D_bar = B0' diag(mean_t 1/U_t) B0``.

    Matches the corrected ``thread2b_fair_cost/cost_runner._build_kbar_avg``.
    """
    n, T = dgp.n, dgp.T
    inv_U_mean = (1.0 / dgp.U).mean(axis=0)
    U_avg = np.broadcast_to(1.0 / inv_U_mean, (T, n)).copy()
    dgp_avg = DGP(
        n=n, T=T, p=dgp.p,
        B_list=dgp.B_list, B0=dgp.B0, U=U_avg,
        M_m=dgp.M_m, lam=dgp.lam, seed=dgp.seed,
    )
    return build_Kbar_explicit(dgp_avg)


def _cholmod_nnz(factor) -> int:
    try:
        return int(factor.L().nnz)
    except Exception:
        return -1


# ---------------------------------------------------------------------------
# Per-path runners
# ---------------------------------------------------------------------------


@dataclass
class PathResult:
    path: str
    status: str
    phase1_assembly_time: float
    phase2_factor_time: float
    phase3_solve_time: float
    total_time: float
    iters: int
    hit_maxiter: int
    relative_residual: float
    L_factor_nnz: int
    bandwidth_u: int             # banded path only; -1 for explicit paths
    banded_ab_bytes: int         # banded path only; -1 for explicit paths
    banded_factor_bytes: int     # banded path only; -1 for explicit paths


_EMPTY = {
    "phase1_assembly_time": float("nan"),
    "phase2_factor_time": float("nan"),
    "phase3_solve_time": float("nan"),
    "total_time": float("nan"),
    "iters": 0,
    "hit_maxiter": 0,
    "relative_residual": float("nan"),
    "L_factor_nnz": -1,
    "bandwidth_u": -1,
    "banded_ab_bytes": -1,
    "banded_factor_bytes": -1,
}


def _result_skipped(path: str, reason: str) -> PathResult:
    return PathResult(path=path, status=f"skipped_memory_estimate:{reason}", **_EMPTY)


def _result_timeout(path: str, phase: str) -> PathResult:
    return PathResult(path=path, status=f"timeout_{phase}", **_EMPTY)


def _run_direct_cholmod(
    dgp: DGP, op: spla.LinearOperator, b: np.ndarray,
    *, timeout_s: Optional[float], skip: bool, skip_reason: str,
) -> PathResult:
    path = "direct_cholmod"
    if skip:
        return _result_skipped(path, skip_reason)
    try:
        from sksparse.cholmod import cholesky as cholmod_cholesky  # type: ignore
    except ImportError:
        return PathResult(path=path, status="cholmod_unavailable", **_EMPTY)

    try:
        with segment_timeout(timeout_s):
            Kbar, t_asm = _build_kbar_explicit_timed(dgp)
    except SegmentTimeout:
        return _result_timeout(path, "phase1")

    Kbar_csc = Kbar.tocsc()

    try:
        with segment_timeout(timeout_s):
            t0 = perf_counter()
            factor = cholmod_cholesky(Kbar_csc)
            t_factor = perf_counter() - t0
    except SegmentTimeout:
        return _result_timeout(path, "phase2")

    try:
        with segment_timeout(timeout_s):
            t0 = perf_counter()
            x = factor(b)
            t_solve = perf_counter() - t0
    except SegmentTimeout:
        return _result_timeout(path, "phase3")

    r = b - (op @ x)
    rel = float(np.linalg.norm(r) / max(np.linalg.norm(b), 1e-300))
    L_nnz = _cholmod_nnz(factor)
    return PathResult(
        path=path, status="ok",
        phase1_assembly_time=t_asm,
        phase2_factor_time=t_factor,
        phase3_solve_time=t_solve,
        total_time=t_asm + t_factor + t_solve,
        iters=0, hit_maxiter=0, relative_residual=rel,
        L_factor_nnz=L_nnz,
        bandwidth_u=-1, banded_ab_bytes=-1, banded_factor_bytes=-1,
    )


def _run_pcg_explicit_chol(
    dgp: DGP, op: spla.LinearOperator, b: np.ndarray,
    *, timeout_s: Optional[float], skip: bool, skip_reason: str,
) -> PathResult:
    path = "pcg_time_avg_chol_explicit_avgK"
    if skip:
        return _result_skipped(path, skip_reason)
    try:
        from sksparse.cholmod import cholesky as cholmod_cholesky  # type: ignore
    except ImportError:
        return PathResult(path=path, status="cholmod_unavailable", **_EMPTY)

    try:
        with segment_timeout(timeout_s):
            t0 = perf_counter()
            Kbar_avg = _build_kbar_avg(dgp)
            t_asm = perf_counter() - t0
    except SegmentTimeout:
        return _result_timeout(path, "phase1")

    Kbar_avg_csc = Kbar_avg.tocsc()

    try:
        with segment_timeout(timeout_s):
            t0 = perf_counter()
            factor = cholmod_cholesky(Kbar_avg_csc)
            t_factor = perf_counter() - t0
    except SegmentTimeout:
        return _result_timeout(path, "phase2")

    Tn = dgp.T * dgp.n
    M = spla.LinearOperator(
        shape=(Tn, Tn),
        matvec=lambda x: factor(x),
        rmatvec=lambda x: factor(x),
        dtype=np.float64,
    )

    try:
        with segment_timeout(timeout_s):
            res = run_pcg(op, b, M=M)
    except SegmentTimeout:
        return _result_timeout(path, "phase3")

    L_nnz = _cholmod_nnz(factor)
    return PathResult(
        path=path,
        status="ok" if not res.hit_maxiter else "hit_maxiter",
        phase1_assembly_time=t_asm,
        phase2_factor_time=t_factor,
        phase3_solve_time=res.solve_time,
        total_time=t_asm + t_factor + res.solve_time,
        iters=res.iters,
        hit_maxiter=int(res.hit_maxiter),
        relative_residual=res.relative_residual,
        L_factor_nnz=L_nnz,
        bandwidth_u=-1, banded_ab_bytes=-1, banded_factor_bytes=-1,
    )


def _run_pcg_banded(
    dgp: DGP, op: spla.LinearOperator, b: np.ndarray,
    *, timeout_s: Optional[float], skip: bool, skip_reason: str,
) -> PathResult:
    path = "pcg_banded_time_avg_precision_chol"
    if skip:
        return _result_skipped(path, skip_reason)

    # Phase 1: build banded ab (no global Tn x Tn assembly).
    try:
        with segment_timeout(timeout_s):
            t0 = perf_counter()
            banded = build_banded_kbar_avg(dgp)
            t_asm = perf_counter() - t0
    except SegmentTimeout:
        return _result_timeout(path, "phase1")

    # Phase 2: lower-band Cholesky factor.
    try:
        with segment_timeout(timeout_s):
            t0 = perf_counter()
            c = sla.cholesky_banded(banded.ab, lower=True)
            t_factor = perf_counter() - t0
    except SegmentTimeout:
        return _result_timeout(path, "phase2")
    except sla.LinAlgError as e:
        return PathResult(
            path=path, status=f"banded_factor_error:{type(e).__name__}", **_EMPTY,
        )

    Tn = dgp.T * dgp.n
    M = spla.LinearOperator(
        shape=(Tn, Tn),
        matvec=lambda x: sla.cho_solve_banded((c, True), x),
        rmatvec=lambda x: sla.cho_solve_banded((c, True), x),
        dtype=np.float64,
    )

    # Phase 3: PCG solve.
    try:
        with segment_timeout(timeout_s):
            res = run_pcg(op, b, M=M)
    except SegmentTimeout:
        return _result_timeout(path, "phase3")

    return PathResult(
        path=path,
        status="ok" if not res.hit_maxiter else "hit_maxiter",
        phase1_assembly_time=t_asm,
        phase2_factor_time=t_factor,
        phase3_solve_time=res.solve_time,
        total_time=t_asm + t_factor + res.solve_time,
        iters=res.iters,
        hit_maxiter=int(res.hit_maxiter),
        relative_residual=res.relative_residual,
        L_factor_nnz=-1,  # banded factor has dense (u+1)*Tn footprint, not nnz-like
        bandwidth_u=banded.u,
        banded_ab_bytes=banded.storage_bytes,
        banded_factor_bytes=int(c.nbytes),
    )


# ---------------------------------------------------------------------------
# Cell driver
# ---------------------------------------------------------------------------


def run_cell(
    *,
    n: int,
    T: int,
    p: int,
    sv_sigma: float,
    seed: int,
    sv_rho: float = 0.95,
    lam: float = 1e4,
    target_radius: float = 0.9,
    timeout_s: Optional[float] = 900.0,
    max_bytes_explicit: float = _DEFAULT_MAX_BYTES_EXPLICIT,
    max_nnz_explicit: float = _DEFAULT_MAX_NNZ_EXPLICIT,
    max_bytes_banded: float = _DEFAULT_MAX_BYTES_BANDED,
) -> list[dict]:
    """Run all three paths on one cell. Returns CSV-ready dicts."""
    est_ex = estimate_explicit(n, T, p, max_bytes=max_bytes_explicit,
                                max_nnz=max_nnz_explicit)
    est_band = estimate_banded(n, T, p, max_bytes=max_bytes_banded)

    dgp = sample_dgp(
        n=n, T=T, p=p, seed=seed,
        target_radius=target_radius,
        sv_sigma=sv_sigma, sv_rho=sv_rho,
        lam=lam,
    )
    matfree = SVAwareKbar(dgp)
    op = matfree.as_linear_operator()
    rng = np.random.default_rng(seed + 1_000_003)
    b = rng.standard_normal(dgp.Tn)

    H_B_nnz = int(matfree.H_B.nnz)
    M_m_nnz = int(dgp.M_m.nnz)

    rows: list[PathResult] = []
    rows.append(_run_direct_cholmod(
        dgp, op, b, timeout_s=timeout_s,
        skip=est_ex.skip_direct, skip_reason=est_ex.skip_reason,
    ))
    rows.append(_run_pcg_explicit_chol(
        dgp, op, b, timeout_s=timeout_s,
        skip=est_ex.skip_direct, skip_reason=est_ex.skip_reason,
    ))
    rows.append(_run_pcg_banded(
        dgp, op, b, timeout_s=timeout_s,
        skip=est_band.skip_banded, skip_reason=est_band.skip_reason,
    ))

    out: list[dict] = []
    for r in rows:
        d = asdict(r)
        d.update({
            "n": n, "T": T, "p": p, "Tn": dgp.Tn,
            "sv_sigma": sv_sigma, "sv_rho": sv_rho,
            "lam": lam, "target_radius": target_radius, "seed": seed,
            "H_B_nnz": H_B_nnz,
            "Kbar_nnz_estimate": est_ex.Kbar_nnz,
            "Kbar_csr_bytes_estimate": est_ex.Kbar_csr_bytes,
            "M_m_nnz": M_m_nnz,
            "skip_direct": int(est_ex.skip_direct),
            "banded_total_bytes_estimate": est_band.banded_total_bytes,
            "skip_banded": int(est_band.skip_banded),
        })
        out.append(d)
    return out


if __name__ == "__main__":
    # Smoke test.
    rows = run_cell(n=5, T=480, p=2, sv_sigma=0.3, seed=0)
    print(f"{'path':40s} {'status':22s} "
          f"{'asm_ms':>10s} {'fac_ms':>10s} {'sol_ms':>10s} "
          f"{'tot_ms':>11s} {'iters':>6s} {'rel_res':>10s} {'u':>5s}")
    for r in rows:
        print(
            f"{r['path']:40s} {r['status']:22s} "
            f"{r['phase1_assembly_time']*1e3:>10.2f} "
            f"{r['phase2_factor_time']*1e3:>10.2f} "
            f"{r['phase3_solve_time']*1e3:>10.2f} "
            f"{r['total_time']*1e3:>11.2f} "
            f"{r['iters']:>6d} {r['relative_residual']:>10.2e} "
            f"{r['bandwidth_u']:>5d}"
        )

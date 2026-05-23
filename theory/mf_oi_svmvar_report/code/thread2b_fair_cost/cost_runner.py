"""Phased-cost runner for Thread 2b.

For a single ``(dgp, b)`` cell, run each of four solver paths and time
each phase separately. Phase labels are uniform across paths so the
output table can be aggregated and plotted directly.

Paths
-----

``direct_cholmod``
    phase1_assembly  -- build explicit Kbar from (H_B, D_t, lambda M' M)
    phase2_factor    -- CHOLMOD supernodal Cholesky on Kbar
    phase3_solve     -- single ``factor(b)`` call

``direct_splu``
    phase1_assembly  -- build explicit Kbar (same as above)
    phase2_factor    -- ``scipy.sparse.linalg.splu`` on Kbar
    phase3_solve     -- single ``splu.solve(b)`` call

``pcg_time_avg_chol_explicit_avgK``
    phase1_assembly  -- build Kbar_avg from the corrected
                        D_bar = B0' diag(mean_t 1/U_t) B0 precision
                        average (explicit Tn x Tn sparse)
    phase2_factor    -- CHOLMOD on Kbar_avg (preconditioner setup)
    phase3_solve     -- PCG to rtol=1e-8 using matrix-free Kbar matvec
                       and CHOLMOD(Kbar_avg) preconditioner apply

    The name records that this path still materialises Kbar_avg
    explicitly. A truly no-explicit-Kbar alternative (analytic
    construction of the time-averaged precision blocks) is left as
    follow-up; the same memory skip rule applies here.

``pcg_time_avg_chol_frozen_amortized_50`` (derived; not run separately)
    Same numbers as the PCG path but with phase1 and phase2 divided
    by 50. Reports a best-case derived cost if the time-averaged
    precision preconditioner setup were held fixed across 50 MCMC
    sweeps. Labelled clearly so it cannot be misread as the production
    full-chain figure.

Skip rule
---------
``estimate()`` from ``memory_estimate`` is called per cell. If the
estimated Kbar exceeds the memory budget, rows for all three explicit
paths (``direct_cholmod``, ``direct_splu``, and
``pcg_time_avg_chol_explicit_avgK`` -- which builds a full Tn x Tn
Kbar_avg) are emitted with ``status='skipped_memory_estimate'`` and
empty timings. The derived ``frozen_amortized_50`` row inherits the
skip status from the PCG row.

Per-segment timeout
-------------------
Each phase is guarded by ``signal.alarm(timeout_s)``. If the alarm
fires inside Python code the segment is recorded with
``status='timeout_phaseN'``. (CHOLMOD / LU calls return to Python only
at completion, so a stuck factorisation may exceed the wall budget by
some seconds before the timeout is delivered. Setting the alarm before
the call is still the right safety net.)
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
import scipy.sparse as sp
import scipy.sparse.linalg as spla

# Imports from sibling thread1/thread2 directories.
_THIS_DIR = Path(__file__).resolve().parent
_THREAD1_DIR = _THIS_DIR.parent / "thread1_matvec"
_THREAD2_DIR = _THIS_DIR.parent / "thread2_pcg"
for d in (_THREAD1_DIR, _THREAD2_DIR):
    if str(d) not in sys.path:
        sys.path.insert(0, str(d))

from dgp import DGP, sample_dgp, build_H_B  # type: ignore
from kbar_explicit import build_Kbar_explicit, build_D_block_diag  # type: ignore
from kbar_matfree import SVAwareKbar  # type: ignore
from pcg_runner import run_pcg  # type: ignore

from memory_estimate import estimate, MemoryEstimate


# ---------------------------------------------------------------------------
# Timeout helper
# ---------------------------------------------------------------------------


class SegmentTimeout(Exception):
    pass


@contextmanager
def segment_timeout(seconds: Optional[float]):
    """Raise ``SegmentTimeout`` if a code block exceeds ``seconds``.

    Only effective when called from the main thread on POSIX. Pass
    ``None`` to disable.
    """
    if seconds is None or seconds <= 0:
        yield
        return

    def _handler(signum, frame):  # noqa: ARG001
        raise SegmentTimeout(f"segment exceeded {seconds:.1f}s")

    old = signal.signal(signal.SIGALRM, _handler)
    # signal.setitimer supports sub-second precision; signal.alarm does not.
    signal.setitimer(signal.ITIMER_REAL, float(seconds))
    try:
        yield
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0.0)
        signal.signal(signal.SIGALRM, old)


# ---------------------------------------------------------------------------
# Path-specific assemblers
# ---------------------------------------------------------------------------


def _build_kbar_explicit_timed(dgp: DGP) -> tuple[sp.csr_matrix, float]:
    t0 = perf_counter()
    Kbar = build_Kbar_explicit(dgp)
    return Kbar, perf_counter() - t0


def _build_kbar_avg(dgp: DGP) -> sp.csr_matrix:
    """Time-invariant Kbar using D_bar = B0' diag(mean_t 1/U_t) B0."""
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
    """Return nnz of the L factor from a CHOLMOD Factor object.

    Uses ``factor.L()`` to materialise L as a SciPy sparse matrix and
    counts entries. This is O(L nnz) memory and time, so the caller
    should be ready for that cost on the largest cells; we report it
    once per cell.
    """
    try:
        L = factor.L()
        return int(L.nnz)
    except Exception:
        return -1


def _splu_nnz(splu) -> int:
    try:
        return int(splu.L.nnz + splu.U.nnz)
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


_EMPTY = {
    "phase1_assembly_time": float("nan"),
    "phase2_factor_time": float("nan"),
    "phase3_solve_time": float("nan"),
    "total_time": float("nan"),
    "iters": 0,
    "hit_maxiter": 0,
    "relative_residual": float("nan"),
    "L_factor_nnz": -1,
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
    )


def _run_direct_splu(
    dgp: DGP, op: spla.LinearOperator, b: np.ndarray,
    *, timeout_s: Optional[float], skip: bool, skip_reason: str,
) -> PathResult:
    path = "direct_splu"
    if skip:
        return _result_skipped(path, skip_reason)

    try:
        with segment_timeout(timeout_s):
            Kbar, t_asm = _build_kbar_explicit_timed(dgp)
    except SegmentTimeout:
        return _result_timeout(path, "phase1")

    Kbar_csc = Kbar.tocsc()

    try:
        with segment_timeout(timeout_s):
            t0 = perf_counter()
            splu = spla.splu(Kbar_csc)
            t_factor = perf_counter() - t0
    except SegmentTimeout:
        return _result_timeout(path, "phase2")

    try:
        with segment_timeout(timeout_s):
            t0 = perf_counter()
            x = splu.solve(b)
            t_solve = perf_counter() - t0
    except SegmentTimeout:
        return _result_timeout(path, "phase3")

    r = b - (op @ x)
    rel = float(np.linalg.norm(r) / max(np.linalg.norm(b), 1e-300))
    L_nnz = _splu_nnz(splu)

    return PathResult(
        path=path, status="ok",
        phase1_assembly_time=t_asm,
        phase2_factor_time=t_factor,
        phase3_solve_time=t_solve,
        total_time=t_asm + t_factor + t_solve,
        iters=0, hit_maxiter=0, relative_residual=rel,
        L_factor_nnz=L_nnz,
    )


def _run_pcg_time_avg_chol(
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
        path=path, status="ok" if not res.hit_maxiter else "hit_maxiter",
        phase1_assembly_time=t_asm,
        phase2_factor_time=t_factor,
        phase3_solve_time=res.solve_time,
        total_time=t_asm + t_factor + res.solve_time,
        iters=res.iters,
        hit_maxiter=int(res.hit_maxiter),
        relative_residual=res.relative_residual,
        L_factor_nnz=L_nnz,
    )


def _derive_frozen_amortized(pcg_row: PathResult, k: int = 50) -> PathResult:
    """Best-case row: amortise setup costs over ``k`` MCMC sweeps."""
    if pcg_row.status not in ("ok", "hit_maxiter"):
        return PathResult(
            path=f"pcg_time_avg_chol_frozen_amortized_{k}",
            status="derived_from_failed_pcg", **_EMPTY,
        )
    p1 = pcg_row.phase1_assembly_time / k
    p2 = pcg_row.phase2_factor_time / k
    p3 = pcg_row.phase3_solve_time
    return PathResult(
        path=f"pcg_time_avg_chol_frozen_amortized_{k}",
        status="derived_best_case",
        phase1_assembly_time=p1,
        phase2_factor_time=p2,
        phase3_solve_time=p3,
        total_time=p1 + p2 + p3,
        iters=pcg_row.iters,
        hit_maxiter=pcg_row.hit_maxiter,
        relative_residual=pcg_row.relative_residual,
        L_factor_nnz=pcg_row.L_factor_nnz,
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
    timeout_s: Optional[float] = 300.0,
    max_bytes: float = 6.0 * 1024**3,
    max_nnz: float = 1e8,
    amortize_k: int = 50,
) -> list[dict]:
    """Run all four paths on one ``(n, T, p, sv_sigma, seed)`` cell.

    Returns a list of dicts ready for CSV writing. Even when the direct
    paths are skipped, their rows are emitted with ``status`` indicating
    the reason -- never silently dropped.
    """
    est = estimate(n, T, p, max_bytes=max_bytes, max_nnz=max_nnz)

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

    # Static memory proxies that do not depend on a particular path.
    H_B_nnz = int(matfree.H_B.nnz)
    M_m_nnz = int(dgp.M_m.nnz)

    rows: list[PathResult] = []

    rows.append(_run_direct_cholmod(
        dgp, op, b, timeout_s=timeout_s,
        skip=est.skip_direct, skip_reason=est.skip_reason,
    ))
    rows.append(_run_direct_splu(
        dgp, op, b, timeout_s=timeout_s,
        skip=est.skip_direct, skip_reason=est.skip_reason,
    ))

    pcg_row = _run_pcg_time_avg_chol(
        dgp, op, b, timeout_s=timeout_s,
        skip=est.skip_direct, skip_reason=est.skip_reason,
    )
    rows.append(pcg_row)
    rows.append(_derive_frozen_amortized(pcg_row, k=amortize_k))

    # Decorate with shared cell-level fields.
    out: list[dict] = []
    for r in rows:
        d = asdict(r)
        d.update({
            "n": n, "T": T, "p": p, "Tn": dgp.Tn,
            "sv_sigma": sv_sigma, "sv_rho": sv_rho,
            "lam": lam, "target_radius": target_radius, "seed": seed,
            "H_B_nnz": H_B_nnz,
            "Kbar_nnz_estimate": est.Kbar_nnz,
            "Kbar_csr_bytes_estimate": est.Kbar_csr_bytes,
            "M_m_nnz": M_m_nnz,
            "skip_direct": int(est.skip_direct),
        })
        out.append(d)
    return out


if __name__ == "__main__":
    rows = run_cell(n=5, T=480, p=2, sv_sigma=0.3, seed=0)
    for r in rows:
        print(
            f"{r['path']:42s} status={r['status']:18s} "
            f"asm={r['phase1_assembly_time']*1e3:7.1f}ms "
            f"fac={r['phase2_factor_time']*1e3:7.1f}ms "
            f"sol={r['phase3_solve_time']*1e3:7.1f}ms "
            f"tot={r['total_time']*1e3:8.1f}ms "
            f"iters={r['iters']:5d} rel={r['relative_residual']:.1e}"
        )

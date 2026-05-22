"""Thin wrapper around scipy.sparse.linalg.cg for the Thread 2 benchmark.

Exposes a single function ``run_pcg`` that solves ``Kbar x = b`` with
optional preconditioning and returns timing + convergence diagnostics.
"""

from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter
from typing import Optional

import numpy as np
import scipy.sparse.linalg as spla


@dataclass
class PCGResult:
    iters: int
    status: int  # 0 success, >0 maxiter, <0 breakdown
    relative_residual: float
    solve_time: float
    hit_maxiter: bool


def run_pcg(
    A: spla.LinearOperator,
    b: np.ndarray,
    M: Optional[spla.LinearOperator] = None,
    *,
    rtol: float = 1e-8,
    maxiter: Optional[int] = None,
    x0: Optional[np.ndarray] = None,
) -> PCGResult:
    """Solve A x = b with PCG and record diagnostics.

    Parameters
    ----------
    A : LinearOperator
        SPD precision matvec (e.g. ``SVAwareKbar.as_linear_operator()``).
    b : ndarray
        Right-hand side.
    M : LinearOperator | None
        Preconditioner. ``None`` is treated as identity by scipy's cg.
    rtol : float
        Relative residual tolerance.
    maxiter : int | None
        Hard cap; defaults to ``min(5 * len(b), 20000)``.

    Returns
    -------
    PCGResult with iteration count, convergence status, residual norm
    ratio, wallclock, and a ``hit_maxiter`` flag.
    """
    n = b.size
    if maxiter is None:
        maxiter = min(5 * n, 20000)

    iters = 0

    def callback(_xk: np.ndarray) -> None:
        nonlocal iters
        iters += 1

    t0 = perf_counter()
    x, info = spla.cg(
        A, b, M=M, rtol=rtol, atol=0.0, maxiter=maxiter, x0=x0, callback=callback
    )
    solve_time = perf_counter() - t0

    r = b - (A @ x)
    rel = float(np.linalg.norm(r) / max(np.linalg.norm(b), 1e-300))

    return PCGResult(
        iters=iters,
        status=int(info),
        relative_residual=rel,
        solve_time=solve_time,
        hit_maxiter=(info > 0 or iters >= maxiter),
    )


if __name__ == "__main__":
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "thread1_matvec"))
    from dgp import sample_dgp  # type: ignore
    from kbar_explicit import build_Kbar_explicit  # type: ignore
    from kbar_matfree import SVAwareKbar  # type: ignore

    from preconditioners import make_preconditioner, PRECONDITIONER_NAMES

    dgp = sample_dgp(n=4, T=60, p=2, seed=42, lam=1e4)
    op = SVAwareKbar(dgp).as_linear_operator()
    Kbar = build_Kbar_explicit(dgp)
    rng = np.random.default_rng(1)
    b = rng.standard_normal(dgp.Tn)

    print(f"problem: n={dgp.n}, T={dgp.T}, p={dgp.p}, Tn={dgp.Tn}, lam={dgp.lam}")
    for name in PRECONDITIONER_NAMES:
        M, _ = make_preconditioner(name, Kbar, dgp)
        res = run_pcg(op, b, M=M)
        print(
            f"  {name:18s}: iters={res.iters:5d}  rel_res={res.relative_residual:.2e}  "
            f"time={res.solve_time * 1000:7.2f} ms  status={res.status}  hit_max={res.hit_maxiter}"
        )

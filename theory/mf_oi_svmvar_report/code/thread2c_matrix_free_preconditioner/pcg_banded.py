"""Banded time-averaged precision preconditioner for Thread 2c PCG.

Wraps the lower-banded Cholesky factor of ``K_pre`` produced by
``banded_kbar_avg.build_banded_kbar_avg`` into a
``scipy.sparse.linalg.LinearOperator`` that applies ``M @ x = K_pre^{-1} x``
via ``scipy.linalg.cho_solve_banded((c, True), x)``.

In ``GLOBAL_DEFINITIONS.md`` terms this path is:

* ``K-free``    -- ``K`` is applied matrix-free through
                   ``thread1_matvec.kbar_matfree.SVAwareKbar``;
* ``K_pre-free``-- ``K_pre`` is never assembled as a global ``Tn x Tn`` sparse
                   matrix; only the ``(u + 1) x Tn`` banded array is built;
* ``H_B`` is still materialised inside ``SVAwareKbar`` (the matrix-free claim
  here is about ``K`` and ``K_pre``, not about ``H_B``).

This module owns only the preconditioner construction. Solver-level
phased timing (assembly + factor + PCG-solve) is the responsibility of
the Thread 2c Step C ``cost_runner``; this module exposes the
underlying ``setup_band_time`` and ``factor_time`` so that ``cost_runner``
can attribute them correctly.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path
from time import perf_counter

import numpy as np
import scipy.linalg as sla
from scipy.sparse.linalg import LinearOperator

_THIS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_THIS_DIR.parent / "thread1_matvec"))

from dgp import DGP  # type: ignore  # noqa: E402

from banded_kbar_avg import (  # noqa: E402
    BandedKbarAvg,
    build_banded_kbar_avg,
)


@dataclass
class BandedPreconditioner:
    """Bundle of the banded preconditioner LinearOperator and bookkeeping."""

    op: LinearOperator
    banded: BandedKbarAvg
    cho_factor: np.ndarray  # output of cholesky_banded(ab, lower=True)
    setup_band_time: float
    factor_time: float

    @property
    def setup_total_time(self) -> float:
        return self.setup_band_time + self.factor_time

    @property
    def banded_storage_bytes(self) -> int:
        return self.banded.storage_bytes

    @property
    def factor_storage_bytes(self) -> int:
        return int(self.cho_factor.nbytes)


def build_banded_preconditioner(dgp: DGP) -> BandedPreconditioner:
    """Build the no-explicit-``Kbar_avg`` banded preconditioner.

    Returns a ``BandedPreconditioner`` whose ``.op`` is suitable for the
    ``M=`` argument of ``scipy.sparse.linalg.cg``. ``M @ x`` applies
    ``K_pre^{-1} x`` via ``scipy.linalg.cho_solve_banded((c, True), x)``.
    """
    t0 = perf_counter()
    banded = build_banded_kbar_avg(dgp)
    setup_band_time = perf_counter() - t0

    t1 = perf_counter()
    c = sla.cholesky_banded(banded.ab, lower=True)
    factor_time = perf_counter() - t1

    Tn = banded.Tn

    def _solve(x: np.ndarray) -> np.ndarray:
        return sla.cho_solve_banded((c, True), x)

    op = LinearOperator(
        shape=(Tn, Tn),
        matvec=_solve,
        rmatvec=_solve,  # K_pre symmetric => K_pre^{-1} symmetric
        dtype=np.float64,
    )

    return BandedPreconditioner(
        op=op,
        banded=banded,
        cho_factor=c,
        setup_band_time=setup_band_time,
        factor_time=factor_time,
    )


if __name__ == "__main__":
    from dgp import sample_dgp  # type: ignore

    dgp = sample_dgp(n=5, T=120, p=2, seed=42, lam=1e4)
    pre = build_banded_preconditioner(dgp)
    print(
        f"DGP: n={dgp.n}, T={dgp.T}, p={dgp.p}, Tn={dgp.Tn}, "
        f"sv_sigma={0.3}, lam={dgp.lam:.0e}"
    )
    print(
        f"Bandwidths: u_var={pre.banded.u_var}, "
        f"u_agg={pre.banded.u_agg}, u={pre.banded.u}"
    )
    print(
        f"setup: build_band={pre.setup_band_time * 1000:.2f} ms, "
        f"cholesky_banded={pre.factor_time * 1000:.2f} ms, "
        f"total={pre.setup_total_time * 1000:.2f} ms"
    )
    print(
        f"storage: banded_ab={pre.banded_storage_bytes:,} B, "
        f"factor={pre.factor_storage_bytes:,} B"
    )

    rng = np.random.default_rng(0)
    b = rng.standard_normal(dgp.Tn)
    x = pre.op @ b
    print(f"sample apply: ||M b||={np.linalg.norm(x):.3e}")

"""Correctness tests for the banded ``K_pre`` builder.

Validates the four Thread 2c invariants stated in
``protocols/THREAD2C_MATRIX_FREE_PROTOCOL.md`` and
``protocols/GLOBAL_DEFINITIONS.md`` (Preconditioner invariant + Solve
invariant), on a small-but-varied case grid:

  (I)   Frobenius:
        ``||banded->dense - K_pre_explicit||_F / ||K_pre_explicit||_F < 1e-10``

  (II)  Random-vector matvec invariant:
        ``||(banded->dense) x - K_pre_explicit x|| / ||K_pre_explicit x|| < 1e-10``

  (III) Banded Cholesky solve invariant:
        ``||K_pre_explicit x_solve - r|| / ||r|| < 1e-10``
        where ``x_solve = cho_solve_banded((cholesky_banded(ab, lower=True),
        True), r)``. This both exercises the full
        construction -> factorise -> solve pipeline and catches any silent
        bandwidth truncation.

  (IV)  Bandwidth invariant (implicit): ``build_banded_kbar_avg`` asserts
        that every nonzero of ``lambda M_m' M_m`` falls inside ``u_agg``.
        Running on the cases below exercises that assert without it firing,
        which is the desired outcome.

The reference ``K_pre_explicit`` is the *corrected*
``_build_time_averaged_kbar`` from ``thread2_pcg/preconditioners.py``,
which is itself verified by ``thread1_matvec/test_time_avg_precision.py``
against an independent per-date construction. So passing here transitively
certifies the banded route against the protocol's ``D_bar`` definition.

Run:
    python test_banded_correctness.py
Exit 0 on PASS, 1 on FAIL.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import scipy.linalg as sla

_THIS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_THIS_DIR))
sys.path.insert(0, str(_THIS_DIR.parent / "thread1_matvec"))
sys.path.insert(0, str(_THIS_DIR.parent / "thread2_pcg"))

from dgp import sample_dgp  # type: ignore  # noqa: E402
from preconditioners import _build_time_averaged_kbar  # type: ignore  # noqa: E402

from banded_kbar_avg import (  # noqa: E402
    build_banded_kbar_avg,
    banded_to_dense,
)


TOL = 1e-10


# Case grid: cover dense and lower-triangular B0, varying (n, T, p, sv, lam),
# include T close to p (end-boundary truncation), and a scalar AR(1) edge.
CASES = [
    # Baseline-ish small case.
    dict(n=3, T=20, p=2, sv_sigma=0.3, lam=1e4, b0_structure="dense"),
    # Moderate, deeper lag.
    dict(n=5, T=30, p=3, sv_sigma=0.5, lam=1e4, b0_structure="dense"),
    # Higher SV + large lambda.
    dict(n=5, T=60, p=4, sv_sigma=0.5, lam=1e6, b0_structure="dense"),
    # Legacy lower-triangular B0 must still work.
    dict(n=5, T=30, p=3, sv_sigma=0.5, lam=1e4, b0_structure="lower_triangular"),
    # End-boundary stress: T just barely > p.
    dict(n=3, T=5, p=4, sv_sigma=0.3, lam=1e4, b0_structure="dense"),
    # Very small T (degenerate end boundary).
    dict(n=2, T=3, p=2, sv_sigma=0.1, lam=1e2, b0_structure="dense"),
    # Scalar AR(1) edge.
    dict(n=1, T=20, p=1, sv_sigma=0.3, lam=1e3, b0_structure="dense"),
    # n=1, p=2 (small but multiple lags).
    dict(n=1, T=20, p=2, sv_sigma=0.3, lam=1e3, b0_structure="dense"),
]
SEEDS = (0, 1, 7)


def _run_case(case: dict, seed: int) -> dict:
    dgp = sample_dgp(seed=seed, **case)
    banded = build_banded_kbar_avg(dgp)

    K_ref = _build_time_averaged_kbar(dgp).toarray()
    K_dense_from_banded = banded_to_dense(banded)
    ref_fro = float(np.linalg.norm(K_ref, "fro"))
    ref_fro_safe = max(ref_fro, 1e-300)

    # (I) Frobenius.
    err_fro = float(
        np.linalg.norm(K_dense_from_banded - K_ref, "fro") / ref_fro_safe
    )

    # (II) Random-vector matvec.
    rng = np.random.default_rng(seed + 101)
    worst_mv = 0.0
    for _ in range(20):
        x = rng.standard_normal(dgp.Tn)
        y_ref = K_ref @ x
        y_band = K_dense_from_banded @ x
        denom = max(float(np.linalg.norm(y_ref)), 1e-300)
        rel = float(np.linalg.norm(y_band - y_ref) / denom)
        if rel > worst_mv:
            worst_mv = rel

    # (III) Banded Cholesky solve. Construct a true x, form r = K_ref @ x,
    #       solve via banded factor, recover x, and check K_ref @ x_solve = r
    #       within tolerance. Doing the residual check against K_ref (rather
    #       than against x itself) avoids inflating the apparent error by
    #       cond(K_ref) when x has small components in stiff directions.
    try:
        c = sla.cholesky_banded(banded.ab, lower=True)
        chol_status = "ok"
        x_true = rng.standard_normal(dgp.Tn)
        r = K_ref @ x_true
        x_solve = sla.cho_solve_banded((c, True), r)
        solve_err = float(
            np.linalg.norm(K_ref @ x_solve - r)
            / max(float(np.linalg.norm(r)), 1e-300)
        )
    except (sla.LinAlgError, ValueError) as e:
        chol_status = f"fail: {type(e).__name__}: {e}"
        solve_err = float("inf")

    return dict(
        err_fro=err_fro,
        err_mv=worst_mv,
        solve_err=solve_err,
        chol_status=chol_status,
        u_var=banded.u_var,
        u_agg=banded.u_agg,
        u=banded.u,
        Tn=dgp.Tn,
    )


def main() -> int:
    header = (
        f"{'case':<66} {'seed':>4} "
        f"{'u_var':>6} {'u_agg':>6} {'u':>5} "
        f"{'err_fro':>10} {'err_mv':>10} {'solve_err':>10}  status"
    )
    print(header)
    print("-" * len(header))
    fail = False
    for c in CASES:
        for s in SEEDS:
            r = _run_case(c, s)
            ok = (
                r["err_fro"] < TOL
                and r["err_mv"] < TOL
                and r["solve_err"] < TOL
                and r["chol_status"] == "ok"
            )
            if not ok:
                fail = True
            tag = (
                f"n={c['n']} T={c['T']} p={c['p']} sv={c['sv_sigma']} "
                f"lam={c['lam']:.0e} B0={c['b0_structure']}"
            )
            note = "OK" if ok else f"FAIL ({r['chol_status']})"
            print(
                f"{tag:<66} {s:>4} "
                f"{r['u_var']:>6} {r['u_agg']:>6} {r['u']:>5} "
                f"{r['err_fro']:>10.2e} {r['err_mv']:>10.2e} "
                f"{r['solve_err']:>10.2e}  {note}"
            )
    print("-" * len(header))
    if fail:
        print(f"FAIL: at least one case violated TOL = {TOL:.0e}")
        return 1
    print(f"PASS: all cases satisfy err_fro, err_mv, solve_err < {TOL:.0e}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

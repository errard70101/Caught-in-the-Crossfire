"""Regression test for the corrected time-averaged precision block.

Thread 2/2b/3's ``time_averaged_chol`` preconditioner previously built

    D_bar_wrong = B0' diag(1 / mean_t(U_t)) B0,

which is *not* the time-average of the per-date precision. The correct
construction is

    D_bar = mean_t(D_t)
          = mean_t( B0' diag(1/U_t) B0 )
          = B0' diag( mean_t(1/U_t) ) B0.

This test verifies three claims:

    (A) ``D_bar`` computed via the per-date mean equals
        ``B0' diag(mean(1/U_t)) B0`` to machine precision.
    (B) The corrected ``Kbar_avg_precision`` assembled by
        ``thread2_pcg.preconditioners._build_time_averaged_kbar``
        matches the independently-built reference within < 1e-10
        (relative Frobenius and random-vector matvec).
    (C) For ``sv_sigma > 0``, the old ``D_bar_wrong`` and the corrected
        ``D_bar`` differ by a non-negligible amount, documenting the
        Thread 2/2b preconditioner correction.

Thread 1's actual ``SVAwareKbar`` is NOT exercised here -- that is the
job of ``test_equivalence.py``. This file only validates the
time-averaged block used by the preconditioner.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import scipy.sparse as sp

_THIS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_THIS_DIR))
sys.path.insert(0, str(_THIS_DIR.parent / "thread2_pcg"))

from dgp import sample_dgp  # type: ignore
from kbar_explicit import build_D_block_diag, build_Kbar_explicit  # type: ignore
from preconditioners import _build_time_averaged_kbar  # type: ignore


TOL_EQ = 1e-10
TOL_DIFFER = 1e-4  # minimum |D_bar_wrong - D_bar| / |D_bar| we expect for sv >= 0.3


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _D_bar_per_date(B0: np.ndarray, U: np.ndarray) -> np.ndarray:
    """D_bar = mean_t( B0' diag(1/U_t) B0 ).  Reference, never simplified."""
    T, n = U.shape
    acc = np.zeros((n, n))
    for t in range(T):
        acc += B0.T @ np.diag(1.0 / U[t]) @ B0
    return acc / T


def _D_bar_closed_form(B0: np.ndarray, U: np.ndarray) -> np.ndarray:
    """D_bar via the simplification B0' diag(mean(1/U_t)) B0."""
    inv_U_mean = (1.0 / U).mean(axis=0)
    return B0.T @ np.diag(inv_U_mean) @ B0


def _D_bar_wrong(B0: np.ndarray, U: np.ndarray) -> np.ndarray:
    """Old (incorrect) construction: B0' diag(1 / mean(U_t)) B0."""
    U_mean = U.mean(axis=0)
    return B0.T @ np.diag(1.0 / U_mean) @ B0


def _reference_kbar_avg(dgp, D_bar: np.ndarray) -> sp.csc_matrix:
    """Build Kbar_avg = H_B' (I_T kron D_bar) H_B + lam M'M from D_bar."""
    from dgp import build_H_B  # type: ignore

    H_B = build_H_B(dgp.B_list, dgp.T).tocsr()
    D_block = sp.block_diag([sp.csr_matrix(D_bar)] * dgp.T, format="csr")
    AtDA = (H_B.T @ D_block @ H_B).tocsr()
    MtM = (dgp.M_m.T @ dgp.M_m).tocsr()
    return (AtDA + dgp.lam * MtM).tocsc()


# ---------------------------------------------------------------------------
# Test cases
# ---------------------------------------------------------------------------


CASES = [
    dict(n=3, T=20, p=2, sv_sigma=0.3, lam=1e4, b0_structure="dense"),
    dict(n=5, T=30, p=3, sv_sigma=0.5, lam=1e4, b0_structure="dense"),
    dict(n=5, T=30, p=3, sv_sigma=0.5, lam=1e4, b0_structure="lower_triangular"),
]
SEEDS = (0, 1, 7)


def run_case(case: dict, seed: int) -> dict:
    dgp = sample_dgp(seed=seed, **case)

    # (A) per-date mean == B0' diag(mean(1/U_t)) B0
    D_bar_iter = _D_bar_per_date(dgp.B0, dgp.U)
    D_bar_cf = _D_bar_closed_form(dgp.B0, dgp.U)
    err_A = np.linalg.norm(D_bar_iter - D_bar_cf) / max(np.linalg.norm(D_bar_iter), 1e-300)

    # (B) corrected preconditioner builder matches the reference
    Kbar_avg_ref = _reference_kbar_avg(dgp, D_bar_iter)
    Kbar_avg_pre = _build_time_averaged_kbar(dgp)
    diff_fro = sp.linalg.norm(Kbar_avg_pre - Kbar_avg_ref)
    ref_fro = sp.linalg.norm(Kbar_avg_ref)
    err_B_fro = float(diff_fro / max(ref_fro, 1e-300))
    rng = np.random.default_rng(seed + 101)
    worst_mv = 0.0
    for _ in range(20):
        x = rng.standard_normal(Kbar_avg_ref.shape[0])
        y_ref = Kbar_avg_ref @ x
        y_pre = Kbar_avg_pre @ x
        rel = float(np.linalg.norm(y_ref - y_pre) / max(np.linalg.norm(y_ref), 1e-300))
        if rel > worst_mv:
            worst_mv = rel

    # (C) old construction differs from corrected under SV
    D_bar_old = _D_bar_wrong(dgp.B0, dgp.U)
    rel_diff_old = float(
        np.linalg.norm(D_bar_old - D_bar_iter) / max(np.linalg.norm(D_bar_iter), 1e-300)
    )

    return dict(err_A=err_A, err_B_fro=err_B_fro, err_B_mv=worst_mv, rel_diff_old=rel_diff_old)


def main() -> int:
    print(f"{'case':<62} {'seed':>4} {'err_A':>10} {'err_B_fro':>12} {'err_B_mv':>11} {'|old-new|':>11}  status")
    print("-" * 122)
    fail = False
    for c in CASES:
        for s in SEEDS:
            r = run_case(c, s)
            ok = (r["err_A"] < TOL_EQ
                  and r["err_B_fro"] < TOL_EQ
                  and r["err_B_mv"] < TOL_EQ
                  and r["rel_diff_old"] > TOL_DIFFER)
            if not ok:
                fail = True
            tag = f"n={c['n']} T={c['T']} p={c['p']} sv={c['sv_sigma']} B0={c['b0_structure']}"
            print(
                f"{tag:<62} {s:>4} "
                f"{r['err_A']:>10.2e} {r['err_B_fro']:>12.2e} {r['err_B_mv']:>11.2e} "
                f"{r['rel_diff_old']:>11.2e}  {'OK' if ok else 'FAIL'}"
            )
    print("-" * 122)
    if fail:
        print(f"FAIL: at least one case violated TOL_EQ={TOL_EQ:.0e} "
              f"or TOL_DIFFER={TOL_DIFFER:.0e}")
        return 1
    print(f"PASS: corrected D_bar matches per-date mean to < {TOL_EQ:.0e}; "
          f"old != new by > {TOL_DIFFER:.0e}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Step B: PCG-alignment check for the new banded preconditioner.

The new banded preconditioner from ``pcg_banded.build_banded_preconditioner``
and Thread 2's reference ``time_averaged_chol`` from
``thread2_pcg.preconditioners.build_time_averaged_chol`` apply the *same*
mathematical inverse

    M = K_pre^{-1},   K_pre = H_B' (I_T kron D_bar) H_B + lambda M_m' M_m,

via different solver libraries (SciPy lower-banded LAPACK vs CHOLMOD
supernodal sparse Cholesky). With matched right-hand side, ``x0 = 0``,
and the same PCG tolerance, the two preconditioned-CG trajectories must
therefore agree up to numerical noise:

* iteration counts within a small gap (``ITER_GAP_MAX``);
* both converge to the same target residual ``rel_res <= RTOL_PCG``;
* solutions agree relatively to ``SOLUTION_REL_MAX`` (set by PCG
  tolerance times the conditioning of ``K``, not by the preconditioner
  identity).

This certifies the *integration* of the banded factor into the PCG
pipeline; it does NOT yet do total-cost benchmarking. Total-cost
benchmark accounting is the responsibility of Thread 2c Step C.

Run:
    python test_pcg_alignment.py
Exit 0 on PASS, 1 on FAIL.
"""

from __future__ import annotations

import sys
from pathlib import Path
from time import perf_counter

import numpy as np
import scipy.sparse.linalg as spla

_THIS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_THIS_DIR))
sys.path.insert(0, str(_THIS_DIR.parent / "thread1_matvec"))
sys.path.insert(0, str(_THIS_DIR.parent / "thread2_pcg"))

from dgp import sample_dgp  # type: ignore  # noqa: E402
from kbar_matfree import SVAwareKbar  # type: ignore  # noqa: E402
from preconditioners import build_time_averaged_chol  # type: ignore  # noqa: E402

from pcg_banded import build_banded_preconditioner  # noqa: E402


RTOL_PCG = 1e-8
ITER_GAP_MAX = 2            # numerical noise tolerance on iter count
SOLUTION_REL_MAX = 1e-5     # ~ rtol * cond(K) ballpark


CASES = [
    # Sanity: tiny, very fast.
    dict(n=3, T=60,  p=2, sv_sigma=0.3, lam=1e4, b0_structure="dense"),
    # Easier SV regime; Thread 2 medians at this cell: ~24 iters.
    dict(n=5, T=480, p=2, sv_sigma=0.1, lam=1e4, b0_structure="dense"),
    # Thread 2 baseline; medians at this cell: ~136 iters.
    dict(n=5, T=480, p=2, sv_sigma=0.3, lam=1e4, b0_structure="dense"),
    # Deeper lag.
    dict(n=5, T=480, p=4, sv_sigma=0.3, lam=1e4, b0_structure="dense"),
    # Higher SV; Thread 2 medians at this cell: ~767 iters.
    dict(n=5, T=480, p=2, sv_sigma=0.5, lam=1e4, b0_structure="dense"),
]
SEEDS = (0, 1)


def _solve_with_callback(A_op, M_op, b, rtol):
    """Run scipy.cg, return (x, iters, rel_residual, info, solve_time)."""
    iters = [0]

    def cb(_xk):
        iters[0] += 1

    t0 = perf_counter()
    x, info = spla.cg(
        A_op,
        b,
        M=M_op,
        rtol=rtol,
        atol=0.0,
        maxiter=min(5 * b.size, 20000),
        callback=cb,
    )
    solve_time = perf_counter() - t0
    rel = float(
        np.linalg.norm(b - (A_op @ x))
        / max(float(np.linalg.norm(b)), 1e-300)
    )
    return x, iters[0], rel, int(info), solve_time


def _run_pair(case: dict, seed: int) -> dict:
    dgp = sample_dgp(seed=seed, **case)
    A_op = SVAwareKbar(dgp).as_linear_operator()

    rng = np.random.default_rng(seed + 1000)
    b = rng.standard_normal(dgp.Tn)

    # --- reference: CHOLMOD on explicit Kbar_avg ---
    M_chol, _ = build_time_averaged_chol(dgp)
    x_c, it_c, rel_c, info_c, t_c = _solve_with_callback(
        A_op, M_chol, b, RTOL_PCG
    )

    # --- new: banded LAPACK on Kbar_avg without global assembly ---
    pre = build_banded_preconditioner(dgp)
    x_b, it_b, rel_b, info_b, t_b = _solve_with_callback(
        A_op, pre.op, b, RTOL_PCG
    )

    x_ref_norm = max(float(np.linalg.norm(x_c)), 1e-300)
    sol_rel = float(np.linalg.norm(x_b - x_c) / x_ref_norm)

    return dict(
        Tn=dgp.Tn,
        u=pre.banded.u,
        iter_chol=it_c,
        iter_band=it_b,
        rel_res_chol=rel_c,
        rel_res_band=rel_b,
        info_chol=info_c,
        info_band=info_b,
        solve_ms_chol=t_c * 1000,
        solve_ms_band=t_b * 1000,
        sol_rel_diff=sol_rel,
    )


def main() -> int:
    header = (
        f"{'case':<60} {'seed':>4} {'Tn':>5} {'u':>4} "
        f"{'it_c':>6} {'it_b':>6} "
        f"{'rel_c':>10} {'rel_b':>10} "
        f"{'sol_rel':>10}  status"
    )
    print(header)
    print("-" * len(header))
    fail = False
    for c in CASES:
        for s in SEEDS:
            r = _run_pair(c, s)
            iter_gap_ok = abs(r["iter_band"] - r["iter_chol"]) <= ITER_GAP_MAX
            rel_ok = (
                r["rel_res_chol"] <= RTOL_PCG
                and r["rel_res_band"] <= RTOL_PCG
            )
            sol_ok = r["sol_rel_diff"] <= SOLUTION_REL_MAX
            info_ok = r["info_chol"] == 0 and r["info_band"] == 0
            ok = iter_gap_ok and rel_ok and sol_ok and info_ok
            if not ok:
                fail = True
                tag_bits = []
                if not iter_gap_ok:
                    tag_bits.append(
                        f"iter_gap={abs(r['iter_band'] - r['iter_chol'])}"
                    )
                if not rel_ok:
                    tag_bits.append("rel_res")
                if not sol_ok:
                    tag_bits.append(f"sol_rel={r['sol_rel_diff']:.1e}")
                if not info_ok:
                    tag_bits.append(
                        f"info=({r['info_chol']},{r['info_band']})"
                    )
                status = "FAIL: " + ",".join(tag_bits)
            else:
                status = "OK"

            tag = (
                f"n={c['n']} T={c['T']} p={c['p']} "
                f"sv={c['sv_sigma']} B0={c['b0_structure']}"
            )
            print(
                f"{tag:<60} {s:>4} {r['Tn']:>5} {r['u']:>4} "
                f"{r['iter_chol']:>6d} {r['iter_band']:>6d} "
                f"{r['rel_res_chol']:>10.2e} {r['rel_res_band']:>10.2e} "
                f"{r['sol_rel_diff']:>10.2e}  {status}"
            )

    print("-" * len(header))
    if fail:
        print(
            "FAIL: at least one case violated iter-gap, rel_res, "
            "solution-diff, or info==0."
        )
        return 1
    print(
        f"PASS: all cases agree within iter_gap <= {ITER_GAP_MAX}, "
        f"rel_res <= {RTOL_PCG:.0e}, sol_rel <= {SOLUTION_REL_MAX:.0e}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

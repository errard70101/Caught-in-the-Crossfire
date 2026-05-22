"""Equivalence test: explicit Kbar vs matrix-free Kbar.

Acceptance criterion (NEXT_THREAD_PLAN.md):
    relative matvec error < 1e-10 in small test cases.

We sweep a few (n, T, p, lambda, SV dispersion) configurations and several
random vectors per config.
"""

from __future__ import annotations

import numpy as np

from dgp import sample_dgp
from kbar_explicit import assert_spd_small, build_Kbar_explicit
from kbar_matfree import SVAwareKbar


TOL = 1e-10


def run_case(
    *,
    n: int,
    T: int,
    p: int,
    lam: float,
    sv_sigma: float,
    b0_structure: str,
    seed: int,
    n_vecs: int = 20,
) -> float:
    dgp = sample_dgp(
        n=n, T=T, p=p, seed=seed, sv_sigma=sv_sigma, lam=lam,
        b0_structure=b0_structure,
    )
    Kbar = build_Kbar_explicit(dgp)
    assert_spd_small(Kbar)  # cheap symmetry + dense Cholesky for small dims
    op = SVAwareKbar(dgp)
    rng = np.random.default_rng(seed + 1)
    worst = 0.0
    for _ in range(n_vecs):
        x = rng.standard_normal(dgp.Tn)
        y_ex = Kbar @ x
        y_mf = op.matvec(x)
        rel = np.linalg.norm(y_ex - y_mf) / max(np.linalg.norm(y_ex), 1e-300)
        if rel > worst:
            worst = rel
    return worst


def main() -> int:
    cases = [
        dict(n=3, T=20, p=1, lam=1e2, sv_sigma=0.1, b0_structure="dense"),
        dict(n=3, T=20, p=2, lam=1e4, sv_sigma=0.3, b0_structure="lower_triangular"),
        dict(n=5, T=30, p=2, lam=1e4, sv_sigma=0.5, b0_structure="dense"),
        dict(n=5, T=60, p=3, lam=1e6, sv_sigma=0.8, b0_structure="dense"),
        dict(n=7, T=45, p=4, lam=1e4, sv_sigma=0.3, b0_structure="dense"),
    ]
    seeds = [0, 1, 7, 42]

    fail = False
    print(f"{'case':<70} {'seed':>4} {'max_rel_err':>14}")
    print("-" * 92)
    for c in cases:
        for s in seeds:
            worst = run_case(seed=s, **c)
            status = "OK" if worst < TOL else "FAIL"
            tag = (
                f"n={c['n']} T={c['T']} p={c['p']} "
                f"lam={c['lam']:.0e} sv={c['sv_sigma']} B0={c['b0_structure']}"
            )
            print(f"{tag:<70} {s:>4} {worst:>14.3e}  {status}")
            if worst >= TOL:
                fail = True

    print("-" * 92)
    if fail:
        print(f"FAIL: some cases exceeded tolerance {TOL:.0e}")
        return 1
    print(f"PASS: all cases below tolerance {TOL:.0e}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

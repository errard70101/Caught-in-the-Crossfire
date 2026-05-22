"""Thread 2 benchmark sweep.

Runs PCG with four preconditioners (``none``, ``jacobi``, ``block_jacobi``,
``time_averaged_lu``) plus a sparse direct LU baseline on the SV-aware
matrix-free precision. Five one-at-a-time axes are scanned around a fixed
baseline, mirroring the design in ``NEXT_THREAD_PLAN.md`` Thread 2.

Axes scanned (others held at baseline):

    T              in {120, 240, 480, 960, 1920}
    sv_sigma       in {0.05, 0.1, 0.3, 0.5, 0.8, 1.2}
    lam            in {1e2, 1e3, 1e4, 1e5, 1e6}
    target_radius  in {0.5, 0.7, 0.9, 0.97, 0.99}
    p              in {1, 2, 4, 8, 12}

Baseline: ``n=5, T=480, p=2, sv_sigma=0.3, sv_rho=0.95, lam=1e4,
target_radius=0.9`` with 3 seeds.

Output CSV columns:

    axis, axis_value, n, T, p, sv_sigma, sv_rho, lam, target_radius,
    seed, preconditioner, iters, status, hit_maxiter, relative_residual,
    setup_time, solve_time, matvec_time_mean, cond_proxy

A ``--quick`` flag reduces every axis to two points and uses a single seed,
which is what you want for iteration during development.
"""

from __future__ import annotations

import argparse
import csv
import sys
from dataclasses import dataclass, replace
from pathlib import Path
from time import perf_counter

import numpy as np
import scipy.sparse.linalg as spla

# Add thread1 to path.
_THIS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_THIS_DIR.parent / "thread1_matvec"))

from dgp import sample_dgp  # type: ignore
from kbar_explicit import build_Kbar_explicit  # type: ignore
from kbar_matfree import SVAwareKbar  # type: ignore

from pcg_runner import run_pcg
from preconditioners import make_preconditioner, PRECONDITIONER_NAMES


# ---------------------------------------------------------------------------
# Baseline + axes
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Config:
    n: int = 5
    T: int = 480
    p: int = 2
    sv_sigma: float = 0.3
    sv_rho: float = 0.95
    lam: float = 1e4
    target_radius: float = 0.9


BASELINE = Config()

AXES = {
    "T": [120, 240, 480, 960, 1920],
    "sv_sigma": [0.05, 0.1, 0.3, 0.5, 0.8, 1.2],
    "lam": [1e2, 1e3, 1e4, 1e5, 1e6],
    "target_radius": [0.5, 0.7, 0.9, 0.97, 0.99],
    "p": [1, 2, 4, 8, 12],
}
AXES_QUICK = {
    "T": [120, 240],
    "sv_sigma": [0.1, 0.8],
    "lam": [1e2, 1e6],
    "target_radius": [0.7, 0.97],
    "p": [1, 4],
}


# ---------------------------------------------------------------------------
# Per-cell evaluation
# ---------------------------------------------------------------------------


def estimate_matvec_time(op: spla.LinearOperator, n_vec: int, n_calls: int = 5) -> float:
    """Median time per matvec across ``n_calls`` runs."""
    rng = np.random.default_rng(123)
    times = []
    for _ in range(n_calls):
        x = rng.standard_normal(n_vec)
        t0 = perf_counter()
        op.matvec(x) if hasattr(op, "matvec") else op @ x
        times.append(perf_counter() - t0)
    return float(np.median(times))


def evaluate_cell(cfg: Config, seed: int) -> list[dict]:
    """Run all preconditioners on a single (config, seed) cell."""
    dgp = sample_dgp(
        n=cfg.n,
        T=cfg.T,
        p=cfg.p,
        seed=seed,
        target_radius=cfg.target_radius,
        sv_sigma=cfg.sv_sigma,
        sv_rho=cfg.sv_rho,
        lam=cfg.lam,
    )
    op = SVAwareKbar(dgp).as_linear_operator()
    Kbar = build_Kbar_explicit(dgp)
    rng = np.random.default_rng(seed + 1_000_003)
    b = rng.standard_normal(dgp.Tn)

    matvec_t = estimate_matvec_time(op, dgp.Tn)

    rows: list[dict] = []
    for name in PRECONDITIONER_NAMES:
        t0 = perf_counter()
        M, info = make_preconditioner(name, Kbar, dgp)
        setup_time = perf_counter() - t0
        res = run_pcg(op, b, M=M)
        rows.append(
            {
                "preconditioner": name,
                "iters": res.iters,
                "status": res.status,
                "hit_maxiter": int(res.hit_maxiter),
                "relative_residual": res.relative_residual,
                "setup_time": setup_time,
                "solve_time": res.solve_time,
                "matvec_time_mean": matvec_t,
                "cond_proxy": info.get("cond_proxy", float("nan")),
            }
        )

    # Sparse direct LU baseline (scipy splu).
    t0 = perf_counter()
    splu = spla.splu(Kbar.tocsc())
    lu_setup = perf_counter() - t0
    t0 = perf_counter()
    x_direct = splu.solve(b)
    lu_solve_t = perf_counter() - t0
    r = b - (op @ x_direct)
    rel = float(np.linalg.norm(r) / max(np.linalg.norm(b), 1e-300))
    rows.append(
        {
            "preconditioner": "direct_splu",
            "iters": 0,
            "status": 0,
            "hit_maxiter": 0,
            "relative_residual": rel,
            "setup_time": lu_setup,
            "solve_time": lu_solve_t,
            "matvec_time_mean": matvec_t,
            "cond_proxy": float("nan"),
        }
    )

    # Sparse direct Cholesky baseline (CHOLMOD via scikit-sparse).
    try:
        from sksparse.cholmod import cholesky as cholmod_cholesky  # type: ignore

        t0 = perf_counter()
        factor = cholmod_cholesky(Kbar.tocsc())
        chol_setup = perf_counter() - t0
        t0 = perf_counter()
        x_direct = factor(b)
        chol_solve_t = perf_counter() - t0
        r = b - (op @ x_direct)
        rel = float(np.linalg.norm(r) / max(np.linalg.norm(b), 1e-300))
        rows.append(
            {
                "preconditioner": "direct_cholmod",
                "iters": 0,
                "status": 0,
                "hit_maxiter": 0,
                "relative_residual": rel,
                "setup_time": chol_setup,
                "solve_time": chol_solve_t,
                "matvec_time_mean": matvec_t,
                "cond_proxy": float("nan"),
            }
        )
    except ImportError:
        pass

    # Decorate with cfg fields and seed.
    for row in rows:
        row.update(
            {
                "n": cfg.n,
                "T": cfg.T,
                "p": cfg.p,
                "sv_sigma": cfg.sv_sigma,
                "sv_rho": cfg.sv_rho,
                "lam": cfg.lam,
                "target_radius": cfg.target_radius,
                "seed": seed,
            }
        )
    return rows


# ---------------------------------------------------------------------------
# Sweep driver
# ---------------------------------------------------------------------------


def sweep(out_path: Path, quick: bool = False, seeds: list[int] | None = None) -> None:
    axes = AXES_QUICK if quick else AXES
    if seeds is None:
        seeds = [0] if quick else [0, 1, 7]

    field_order = [
        "axis", "axis_value",
        "n", "T", "p", "sv_sigma", "sv_rho", "lam", "target_radius",
        "seed", "preconditioner", "iters", "status", "hit_maxiter",
        "relative_residual", "setup_time", "solve_time", "matvec_time_mean",
        "cond_proxy",
    ]

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=field_order)
        writer.writeheader()

        total_cells = sum(len(vals) for vals in axes.values()) * len(seeds)
        cell_idx = 0
        for axis_name, values in axes.items():
            for v in values:
                cfg = replace(BASELINE, **{axis_name: v})
                for seed in seeds:
                    cell_idx += 1
                    t0 = perf_counter()
                    rows = evaluate_cell(cfg, seed)
                    cell_t = perf_counter() - t0
                    for row in rows:
                        row["axis"] = axis_name
                        row["axis_value"] = v
                        writer.writerow({k: row.get(k, "") for k in field_order})
                    print(
                        f"[{cell_idx}/{total_cells}] axis={axis_name:13s} "
                        f"value={v:<8} seed={seed}  Tn={cfg.T * cfg.n:6d}  "
                        f"cell_time={cell_t:6.2f}s"
                    )
        # ensure flush
        f.flush()
    print(f"\nWrote {out_path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--quick", action="store_true", help="reduced grid, 1 seed")
    parser.add_argument(
        "--out",
        type=Path,
        default=_THIS_DIR / "results.csv",
        help="output CSV path",
    )
    args = parser.parse_args()
    sweep(args.out, quick=args.quick)


if __name__ == "__main__":
    main()

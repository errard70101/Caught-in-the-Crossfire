"""Thread 2b stress-grid sweep.

Grid (per ``NEXT_THREAD_PLAN.md``, Thread 2b):

    n         in {5, 10, 20}
    T         in {480, 1920, 5000, 10000}
    p         in {2, 12, 24}
    sv_sigma  in {0.1, 0.3, 0.5}

Other parameters held at the Thread 2 baseline (``sv_rho=0.95``,
``lam=1e4``, ``target_radius=0.9``). Three seeds per cell.

Each cell runs four paths via ``cost_runner.run_cell``:

    direct_cholmod
    direct_splu
    pcg_time_avg_chol
    pcg_time_avg_chol_frozen_amortized_50  (derived)

The memory-estimate skip rule applies to the two direct paths only; the
PCG path runs in every cell. Per-segment timeouts protect against
runaway factorisations on the largest grid points.

Output: ``results.csv`` with one row per (cell, path).
"""

from __future__ import annotations

import argparse
import csv
import sys
from itertools import product
from pathlib import Path
from time import perf_counter

_THIS_DIR = Path(__file__).resolve().parent
if str(_THIS_DIR) not in sys.path:
    sys.path.insert(0, str(_THIS_DIR))

from cost_runner import run_cell


# ---------------------------------------------------------------------------
# Grids
# ---------------------------------------------------------------------------


FULL_GRID = {
    "n": [5, 10, 20],
    "T": [480, 1920, 5000, 10000],
    "p": [2, 12, 24],
    "sv_sigma": [0.1, 0.3, 0.5],
}
FULL_SEEDS = [0, 1, 7]

QUICK_GRID = {
    "n": [5, 10],
    "T": [480, 1920],
    "p": [2, 12],
    "sv_sigma": [0.3],
}
QUICK_SEEDS = [0]


# ---------------------------------------------------------------------------
# Timeout policy (per segment, in seconds)
# ---------------------------------------------------------------------------


def timeout_for_cell(n: int, T: int, p: int) -> float:
    Tn = n * T
    if Tn <= 20_000:
        return 60.0
    if Tn <= 50_000:
        return 300.0
    if Tn <= 100_000:
        return 600.0
    return 900.0


# ---------------------------------------------------------------------------
# Sweep driver
# ---------------------------------------------------------------------------


_FIELD_ORDER = [
    "n", "T", "p", "Tn", "sv_sigma", "sv_rho",
    "lam", "target_radius", "seed",
    "path", "status",
    "phase1_assembly_time", "phase2_factor_time", "phase3_solve_time",
    "total_time", "iters", "hit_maxiter", "relative_residual",
    "H_B_nnz", "Kbar_nnz_estimate", "Kbar_csr_bytes_estimate",
    "M_m_nnz", "L_factor_nnz", "skip_direct",
]


def sweep(out_path: Path, quick: bool, max_bytes: float, max_nnz: float, amortize_k: int) -> None:
    grid = QUICK_GRID if quick else FULL_GRID
    seeds = QUICK_SEEDS if quick else FULL_SEEDS

    cells = list(product(grid["n"], grid["T"], grid["p"], grid["sv_sigma"], seeds))
    total = len(cells)
    print(f"Running {total} cells -> {out_path}")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=_FIELD_ORDER)
        writer.writeheader()
        f.flush()

        sweep_t0 = perf_counter()
        for idx, (n, T, p, sigma, seed) in enumerate(cells, 1):
            cell_t0 = perf_counter()
            timeout_s = timeout_for_cell(n, T, p)
            try:
                rows = run_cell(
                    n=n, T=T, p=p, sv_sigma=sigma, seed=seed,
                    timeout_s=timeout_s,
                    max_bytes=max_bytes, max_nnz=max_nnz,
                    amortize_k=amortize_k,
                )
            except Exception as exc:  # noqa: BLE001
                print(f"[{idx}/{total}] (n={n},T={T},p={p},sigma={sigma},seed={seed})  "
                      f"FAILED at cell level: {exc}")
                continue
            for r in rows:
                writer.writerow({k: r.get(k, "") for k in _FIELD_ORDER})
            f.flush()
            cell_t = perf_counter() - cell_t0
            elapsed = perf_counter() - sweep_t0
            avg = elapsed / idx
            eta = avg * (total - idx)
            print(f"[{idx}/{total}] n={n:<3d} T={T:<6d} p={p:<3d} sigma={sigma:<4} "
                  f"seed={seed}  Tn={n*T:<8d}  cell={cell_t:6.1f}s  "
                  f"elapsed={elapsed/60:5.1f}m  eta={eta/60:5.1f}m")

    print(f"\nWrote {out_path} in {(perf_counter() - sweep_t0)/60:.1f} min")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--quick", action="store_true",
                   help="reduced grid for development (~8 cells)")
    p.add_argument("--out", type=Path, default=_THIS_DIR / "results.csv")
    p.add_argument("--max-bytes", type=float, default=6.0 * 1024**3,
                   help="skip direct paths above this estimated Kbar CSR size")
    p.add_argument("--max-nnz", type=float, default=1e8,
                   help="skip direct paths above this estimated Kbar nnz")
    p.add_argument("--amortize-k", type=int, default=50,
                   help="amortisation horizon for the frozen-Ū best-case row")
    args = p.parse_args()
    sweep(args.out, args.quick, args.max_bytes, args.max_nnz, args.amortize_k)


if __name__ == "__main__":
    main()

"""Thread 2c stress-grid and lambda-slice sweep.

Implements ``protocols/THREAD2C_MATRIX_FREE_PROTOCOL.md`` benchmark
grid: small correctness cells, a stress grid that mirrors Thread 2b for
direct cross-thread comparability, and the lambda stress slice that
checks whether large aggregation penalties break the banded route
before they break CHOLMOD.

Cells
-----

Main stress grid (3 x 4 x 3 x 3 x 3 = 324 cells, mirrors Thread 2b's
grid so per-cell timings are directly comparable):

    n in {5, 10, 20}
    T in {480, 1920, 5000, 10000}
    p in {2, 12, 24}
    sv_sigma in {0.1, 0.3, 0.5}
    seeds in {0, 1, 7}
    lam = 1e4

The protocol's headline feasibility cell ``(n=20, T=10000, p=24)`` is
inside this grid. Both explicit paths are skipped at that cell by the
Kbar-memory rule; the banded path is the only one expected to run.

Lambda stress slice (4 x 3 x 3 = 36 cells, per protocol §Benchmark
Grid):

    lambda in {1e4, 1e5, 1e6, 1e7}
    cells:
      (n=5,  T=1920,  p=2,  sv_sigma=0.3)
      (n=10, T=5000,  p=12, sv_sigma=0.3)
      (n=20, T=10000, p=12, sv_sigma=0.3)
    seeds in {0, 1, 7}

Tests whether large lambda breaks the banded Cholesky earlier than
CHOLMOD. ``lam=1e4`` cells overlap with the main grid; the sweep
de-duplicates so each ``(n, T, p, sv, seed, lam)`` runs once.

Small correctness sanity cells (6 cells; tiny so essentially free):

    (n=3, T=20, p=2, sv_sigma=0.3, lam=1e4)
    (n=5, T=30, p=3, sv_sigma=0.5, lam=1e4)
    seeds in {0, 1, 7}

These also live in the output CSV so the same plotting code can
include sanity columns when desired.

Quick mode
----------
``--quick`` reduces to a single seed on a small (n, T, p) subset for
~5 min wiring validation before the full run.

Output
------
One row per ``(cell, path)`` to ``results.csv``. ``cell`` here means
``(n, T, p, sv_sigma, lam, seed)``. Three paths run per cell:
``direct_cholmod``, ``pcg_time_avg_chol_explicit_avgK``,
``pcg_banded_time_avg_precision_chol``. Failures and skips emit
diagnostic rows so the table never silently drops cells.

Per-segment timeouts protect against runaway factorisations on the
headline cells.
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path
from time import perf_counter

_THIS_DIR = Path(__file__).resolve().parent
if str(_THIS_DIR) not in sys.path:
    sys.path.insert(0, str(_THIS_DIR))

from cost_runner_2c import run_cell  # noqa: E402


# ---------------------------------------------------------------------------
# Cell grids
# ---------------------------------------------------------------------------


_SMALL_CORRECTNESS_CELLS = [
    dict(n=3, T=20, p=2, sv_sigma=0.3, lam=1e4),
    dict(n=5, T=30, p=3, sv_sigma=0.5, lam=1e4),
]
_SMALL_CORRECTNESS_SEEDS = [0, 1, 7]


_MAIN_N = [5, 10, 20]
_MAIN_T = [480, 1920, 5000, 10000]
_MAIN_P = [2, 12, 24]
_MAIN_SIGMA = [0.1, 0.3, 0.5]
_MAIN_SEEDS = [0, 1, 7]
_MAIN_LAM = 1e4


_LAMBDA_SLICE_CELLS = [
    dict(n=5,  T=1920,  p=2,  sv_sigma=0.3),
    dict(n=10, T=5000,  p=12, sv_sigma=0.3),
    dict(n=20, T=10000, p=12, sv_sigma=0.3),
]
_LAMBDA_SLICE_LAMS = [1e4, 1e5, 1e6, 1e7]
_LAMBDA_SLICE_SEEDS = [0, 1, 7]


_QUICK_CELLS = [
    dict(n=3,  T=60,   p=2, sv_sigma=0.3, lam=1e4),
    dict(n=5,  T=480,  p=2, sv_sigma=0.3, lam=1e4),
    dict(n=10, T=1920, p=2, sv_sigma=0.3, lam=1e4),
    dict(n=10, T=1920, p=12, sv_sigma=0.3, lam=1e4),
    dict(n=20, T=5000, p=12, sv_sigma=0.3, lam=1e4),
]
_QUICK_SEEDS = [0]


def _build_cells_full() -> list[dict]:
    """Build a deduplicated cell list: correctness + main grid + lambda slice."""
    cells: list[dict] = []
    seen: set[tuple] = set()

    def _add(c: dict) -> None:
        key = (c["n"], c["T"], c["p"], c["sv_sigma"], c["lam"], c["seed"])
        if key in seen:
            return
        seen.add(key)
        cells.append(c)

    # Small correctness cells (across all seeds).
    for spec in _SMALL_CORRECTNESS_CELLS:
        for seed in _SMALL_CORRECTNESS_SEEDS:
            _add({**spec, "seed": seed})

    # Main stress grid.
    for n in _MAIN_N:
        for T in _MAIN_T:
            for p in _MAIN_P:
                for sigma in _MAIN_SIGMA:
                    for seed in _MAIN_SEEDS:
                        _add(dict(
                            n=n, T=T, p=p, sv_sigma=sigma,
                            lam=_MAIN_LAM, seed=seed,
                        ))

    # Lambda stress slice.
    for spec in _LAMBDA_SLICE_CELLS:
        for lam in _LAMBDA_SLICE_LAMS:
            for seed in _LAMBDA_SLICE_SEEDS:
                _add({**spec, "lam": lam, "seed": seed})

    return cells


def _build_cells_quick() -> list[dict]:
    cells: list[dict] = []
    for spec in _QUICK_CELLS:
        for seed in _QUICK_SEEDS:
            cells.append({**spec, "seed": seed})
    return cells


# ---------------------------------------------------------------------------
# Per-cell timeout policy (mirrors Thread 2b's ladder).
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
# CSV writer
# ---------------------------------------------------------------------------


_FIELD_ORDER = [
    # Cell coordinates.
    "n", "T", "p", "Tn", "sv_sigma", "sv_rho",
    "lam", "target_radius", "seed",
    # Path.
    "path", "status",
    # Phased timings.
    "phase1_assembly_time", "phase2_factor_time", "phase3_solve_time",
    "total_time", "iters", "hit_maxiter", "relative_residual",
    # Per-path memory accounting.
    "L_factor_nnz", "bandwidth_u", "banded_ab_bytes", "banded_factor_bytes",
    # Per-cell shared memory accounting / skip bookkeeping.
    "H_B_nnz", "Kbar_nnz_estimate", "Kbar_csr_bytes_estimate", "M_m_nnz",
    "skip_direct", "banded_total_bytes_estimate", "skip_banded",
]


# ---------------------------------------------------------------------------
# Sweep driver
# ---------------------------------------------------------------------------


def _load_done_keys(out_path: Path) -> set[tuple]:
    """Return the set of (n,T,p,sv_sigma,lam,seed) already in the CSV."""
    if not out_path.exists():
        return set()
    import pandas as pd
    try:
        df = pd.read_csv(out_path, usecols=["n", "T", "p", "sv_sigma", "lam", "seed"])
        return set(
            zip(df["n"], df["T"], df["p"], df["sv_sigma"], df["lam"], df["seed"])
        )
    except Exception:
        return set()


def sweep(
    out_path: Path,
    quick: bool,
    max_bytes_explicit: float,
    max_nnz_explicit: float,
    max_bytes_banded: float,
    resume: bool = False,
) -> None:
    cells = _build_cells_quick() if quick else _build_cells_full()
    total = len(cells)

    # Resume: skip cells already present in the CSV.
    done_keys: set[tuple] = set()
    if resume and out_path.exists():
        done_keys = _load_done_keys(out_path)
        skipped = sum(
            1 for c in cells
            if (c["n"], c["T"], c["p"], c["sv_sigma"], c["lam"], c["seed"]) in done_keys
        )
        print(f"Resume mode: {skipped}/{total} cells already done, running remaining "
              f"{total - skipped} cells -> {out_path}")
    else:
        print(f"Running {total} cells -> {out_path}")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    file_mode = "a" if resume and out_path.exists() and done_keys else "w"
    with out_path.open(file_mode, newline="") as f:
        writer = csv.DictWriter(f, fieldnames=_FIELD_ORDER)
        if file_mode == "w":
            writer.writeheader()
        f.flush()

        sweep_t0 = perf_counter()
        run_idx = 0  # count of cells actually run this session
        for idx, c in enumerate(cells, 1):
            n, T, p = c["n"], c["T"], c["p"]
            sigma, seed, lam = c["sv_sigma"], c["seed"], c["lam"]
            # Skip already-done cells in resume mode.
            if resume and (n, T, p, sigma, lam, seed) in done_keys:
                continue
            run_idx += 1
            cell_t0 = perf_counter()
            timeout_s = timeout_for_cell(n, T, p)
            try:
                rows = run_cell(
                    n=n, T=T, p=p, sv_sigma=sigma, seed=seed, lam=lam,
                    timeout_s=timeout_s,
                    max_bytes_explicit=max_bytes_explicit,
                    max_nnz_explicit=max_nnz_explicit,
                    max_bytes_banded=max_bytes_banded,
                )
            except Exception as exc:  # noqa: BLE001
                print(
                    f"[{idx}/{total}] "
                    f"(n={n}, T={T}, p={p}, sv={sigma}, lam={lam:.0e}, "
                    f"seed={seed}) FAILED at cell level: {exc}"
                )
                continue
            for r in rows:
                writer.writerow({k: r.get(k, "") for k in _FIELD_ORDER})
            f.flush()
            cell_t = perf_counter() - cell_t0
            elapsed = perf_counter() - sweep_t0
            remaining = total - len(done_keys) - run_idx
            avg = elapsed / run_idx if run_idx > 0 else 0.0
            eta = avg * remaining
            print(
                f"[{idx}/{total}] n={n:<3d} T={T:<6d} p={p:<3d} "
                f"sigma={sigma:<4} lam={lam:.0e} seed={seed}  "
                f"Tn={n * T:<8d}  cell={cell_t:6.1f}s  "
                f"elapsed={elapsed / 60:6.1f}m  eta={eta / 60:6.1f}m"
            )

    print(f"\nWrote {out_path} in {(perf_counter() - sweep_t0) / 60:.1f} min")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--quick", action="store_true",
        help="reduced grid for wiring validation (~5 cells, ~5 min)",
    )
    p.add_argument(
        "--resume", action="store_true",
        help="append to existing CSV, skipping already-completed cells",
    )
    p.add_argument(
        "--out", type=Path,
        default=None,
        help="output CSV (default: results.csv or results_quick.csv)",
    )
    p.add_argument(
        "--max-bytes-explicit", type=float, default=6.0 * 1024**3,
        help="skip direct/explicit-pre paths above this estimated Kbar CSR size",
    )
    p.add_argument(
        "--max-nnz-explicit", type=float, default=1e8,
        help="skip direct/explicit-pre paths above this estimated Kbar nnz",
    )
    p.add_argument(
        "--max-bytes-banded", type=float, default=6.0 * 1024**3,
        help="skip banded path above this estimated ab + factor size",
    )
    args = p.parse_args()

    if args.out is None:
        name = "results_quick.csv" if args.quick else "results.csv"
        args.out = _THIS_DIR / name

    sweep(
        out_path=args.out,
        quick=args.quick,
        max_bytes_explicit=args.max_bytes_explicit,
        max_nnz_explicit=args.max_nnz_explicit,
        max_bytes_banded=args.max_bytes_banded,
        resume=args.resume,
    )


if __name__ == "__main__":
    main()

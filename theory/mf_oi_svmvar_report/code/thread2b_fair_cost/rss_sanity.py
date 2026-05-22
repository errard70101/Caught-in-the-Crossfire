"""Subprocess-based RSS sanity check.

The main sweep reports ``nnz`` proxies as memory cost because they are
deterministic and reproducible across runs. To verify that the proxies
track real process RSS we run a small subset of cells in a *fresh*
subprocess per (cell, path) so that ``resource.getrusage`` peak RSS is
not polluted by earlier allocations.

This is a sanity check, not a benchmark: we report a handful of points
per (n, T, p) corner and cross-check against ``L_factor_nnz`` and
``Kbar_nnz_estimate`` from the main run.

Output: ``rss_sanity.csv``.
"""

from __future__ import annotations

import argparse
import csv
import json
import resource
import subprocess
import sys
from pathlib import Path

_THIS_DIR = Path(__file__).resolve().parent


# ---------------------------------------------------------------------------
# Worker (executed in subprocess)
# ---------------------------------------------------------------------------


def _worker_main() -> None:
    """Run one (n, T, p, sv_sigma, seed, path) and print JSON with RSS."""
    spec = json.loads(sys.argv[2])
    path_name = spec["path"]
    n, T, p = spec["n"], spec["T"], spec["p"]
    sv_sigma = spec["sv_sigma"]
    seed = spec["seed"]

    # Imports inside so they show up in this subprocess's RSS only.
    sys.path.insert(0, str(_THIS_DIR))
    from cost_runner import run_cell

    rows = run_cell(
        n=n, T=T, p=p, sv_sigma=sv_sigma, seed=seed,
        timeout_s=600.0,
    )
    target = next((r for r in rows if r["path"] == path_name), None)

    # ru_maxrss is in kilobytes on Linux, bytes on macOS. We report both
    # the raw value and a normalised MB figure assuming macOS (bytes).
    # The note explains the convention.
    rusage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    payload = {
        "n": n, "T": T, "p": p, "sv_sigma": sv_sigma, "seed": seed,
        "path": path_name,
        "ru_maxrss_raw": int(rusage),
        # macOS returns bytes; Linux returns KB. Both reported.
        "ru_maxrss_MB_macos": rusage / 1024**2,
        "ru_maxrss_MB_linux": rusage / 1024,
        "status": target["status"] if target else "path_not_found",
        "total_time": target["total_time"] if target else None,
        "L_factor_nnz": target["L_factor_nnz"] if target else None,
        "Kbar_nnz_estimate": target["Kbar_nnz_estimate"] if target else None,
        "H_B_nnz": target["H_B_nnz"] if target else None,
    }
    print(json.dumps(payload))


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------


def _run_one_subprocess(spec: dict) -> dict:
    cmd = [
        sys.executable, str(__file__), "_worker", json.dumps(spec),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=1200)
    if proc.returncode != 0:
        return {
            **spec,
            "ru_maxrss_raw": -1,
            "status": f"subprocess_failed:rc={proc.returncode}",
            "stderr_tail": proc.stderr[-400:],
        }
    line = proc.stdout.strip().splitlines()[-1]
    return json.loads(line)


def driver(out_path: Path, sample_cells: list[dict]) -> None:
    print(f"Running {len(sample_cells)} sanity points -> {out_path}")
    fields = [
        "n", "T", "p", "sv_sigma", "seed", "path",
        "status", "total_time", "L_factor_nnz", "H_B_nnz",
        "Kbar_nnz_estimate",
        "ru_maxrss_raw", "ru_maxrss_MB_macos", "ru_maxrss_MB_linux",
        "stderr_tail",
    ]
    with out_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for idx, spec in enumerate(sample_cells, 1):
            print(f"  [{idx}/{len(sample_cells)}] {spec}")
            row = _run_one_subprocess(spec)
            writer.writerow(row)
            f.flush()
    print(f"Wrote {out_path}")


DEFAULT_SAMPLES = [
    # baseline corners across the stress grid
    {"n": 5, "T": 1920, "p": 2, "sv_sigma": 0.3, "seed": 0, "path": "direct_cholmod"},
    {"n": 5, "T": 1920, "p": 2, "sv_sigma": 0.3, "seed": 0, "path": "pcg_time_avg_chol_explicit_avgK"},
    {"n": 10, "T": 1920, "p": 12, "sv_sigma": 0.3, "seed": 0, "path": "direct_cholmod"},
    {"n": 10, "T": 1920, "p": 12, "sv_sigma": 0.3, "seed": 0, "path": "pcg_time_avg_chol_explicit_avgK"},
    {"n": 20, "T": 1920, "p": 12, "sv_sigma": 0.3, "seed": 0, "path": "direct_cholmod"},
    {"n": 20, "T": 1920, "p": 12, "sv_sigma": 0.3, "seed": 0, "path": "pcg_time_avg_chol_explicit_avgK"},
    {"n": 10, "T": 5000, "p": 12, "sv_sigma": 0.3, "seed": 0, "path": "direct_cholmod"},
    {"n": 10, "T": 5000, "p": 12, "sv_sigma": 0.3, "seed": 0, "path": "pcg_time_avg_chol_explicit_avgK"},
    {"n": 20, "T": 5000, "p": 12, "sv_sigma": 0.3, "seed": 0, "path": "direct_cholmod"},
    {"n": 20, "T": 5000, "p": 12, "sv_sigma": 0.3, "seed": 0, "path": "pcg_time_avg_chol_explicit_avgK"},
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=_THIS_DIR / "rss_sanity.csv")
    args = parser.parse_args()
    driver(args.out, DEFAULT_SAMPLES)


if __name__ == "__main__":
    # Dispatch worker vs driver
    if len(sys.argv) > 1 and sys.argv[1] == "_worker":
        _worker_main()
    else:
        main()

"""Plots for the Thread 2c no-explicit-Kbar_avg benchmark.

Reads ``results.csv`` (from ``sweep_2c.py``) and produces:

1. ``fig_total_time_vs_T.{pdf,png}``     -- median total time vs T, one
   line per path, faceted by n. Includes ``sv_sigma = 0.3`` slice.
2. ``fig_memory_vs_Tn.{pdf,png}``        -- banded ab + factor bytes vs
   CHOLMOD L factor bytes vs Kbar CSR bytes, all on the same axes so the
   matrix-free storage win is visible.
3. ``fig_phase_breakdown.{pdf,png}``     -- stacked bars
   (assembly, factor, solve) per path at representative (n, T) points.
4. ``fig_iters_vs_sv_sigma.{pdf,png}``   -- PCG iteration count vs
   sv_sigma for both PCG paths; identical curves are the Step B
   alignment evidence carried forward into the full sweep.
5. ``fig_lambda_sensitivity.{pdf,png}``  -- total time vs lambda for the
   protocol's 3-cell lambda slice; tests whether large aggregation
   penalty breaks the banded route before CHOLMOD.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


_THIS_DIR = Path(__file__).resolve().parent


_PATH_COLORS = {
    "direct_cholmod": "#1f77b4",
    "pcg_time_avg_chol_explicit_avgK": "#d62728",
    "pcg_banded_time_avg_precision_chol": "#2ca02c",
}
_PATH_ORDER = [
    "direct_cholmod",
    "pcg_time_avg_chol_explicit_avgK",
    "pcg_banded_time_avg_precision_chol",
]
_PATH_LABEL = {
    "direct_cholmod": "direct CHOLMOD",
    "pcg_time_avg_chol_explicit_avgK": "PCG (CHOLMOD on explicit Kbar_avg)",
    "pcg_banded_time_avg_precision_chol": "PCG (banded, no-explicit-Kbar_avg)",
}

_CSR_BYTES_PER_NNZ = 16.0  # matches memory_estimate.py


def _ok_only(df: pd.DataFrame) -> pd.DataFrame:
    keep = df["status"].astype(str) == "ok"
    return df.loc[keep].copy()


# ---------------------------------------------------------------------------
# 1. Total time vs T
# ---------------------------------------------------------------------------


def plot_total_time_vs_T(df: pd.DataFrame, out_dir: Path) -> None:
    df = _ok_only(df)
    df = df[df["sv_sigma"] == 0.3]
    df = df[df["lam"] == 1e4]

    n_vals = sorted(df["n"].unique())
    if not n_vals:
        return
    p_pick = 12 if 12 in df["p"].unique() else df["p"].mode().iloc[0]
    df = df[df["p"] == p_pick]

    fig, axes = plt.subplots(
        1, len(n_vals), figsize=(4.5 * len(n_vals), 3.8), sharey=True
    )
    if len(n_vals) == 1:
        axes = [axes]

    for ax, n_val in zip(axes, n_vals):
        sub_n = df[df["n"] == n_val]
        for path in _PATH_ORDER:
            sub_p = sub_n[sub_n["path"] == path]
            if sub_p.empty:
                continue
            grp = sub_p.groupby("T", as_index=False)["total_time"].median()
            grp = grp.sort_values("T")
            ax.plot(
                grp["T"], grp["total_time"] * 1e3,
                marker="o", label=_PATH_LABEL[path],
                color=_PATH_COLORS[path], linewidth=1.7,
            )
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_title(f"n = {n_val}")
        ax.set_xlabel("T")
        ax.grid(True, which="both", alpha=0.3)

    axes[0].set_ylabel("total time (ms, median)")
    axes[-1].legend(fontsize=8, loc="upper left")
    fig.suptitle(
        f"Thread 2c total cost vs T (sv_sigma = 0.3, p = {p_pick}, lam = 1e4)",
        fontsize=11,
    )
    fig.tight_layout()
    for ext in ("pdf", "png"):
        fig.savefig(
            out_dir / f"fig_total_time_vs_T.{ext}",
            dpi=160, bbox_inches="tight",
        )
    plt.close(fig)


# ---------------------------------------------------------------------------
# 2. Memory vs Tn (peak storage, all paths)
# ---------------------------------------------------------------------------


def plot_memory_vs_Tn(df: pd.DataFrame, out_dir: Path) -> None:
    df = _ok_only(df)
    df = df[df["sv_sigma"] == 0.3]
    df = df[df["lam"] == 1e4]

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.3))

    # Left: per-path peak storage proxy.
    # direct_cholmod: Kbar CSR bytes + L factor (nnz * 16 B)
    # pcg_explicit_avgK: same as direct (assembles Kbar_avg with same pattern)
    # pcg_banded: banded ab + factor bytes
    sub_direct = df[df["path"] == "direct_cholmod"]
    if not sub_direct.empty:
        g = sub_direct.groupby("Tn", as_index=False).agg(
            kbar_bytes=("Kbar_csr_bytes_estimate", "median"),
            l_nnz=("L_factor_nnz", "median"),
        )
        g["bytes"] = g["kbar_bytes"] + g["l_nnz"] * _CSR_BYTES_PER_NNZ
        g = g.sort_values("Tn")
        axes[0].plot(
            g["Tn"], g["bytes"] / 1024**2, marker="o",
            label="direct CHOLMOD: Kbar CSR + L factor",
            color=_PATH_COLORS["direct_cholmod"],
        )

    sub_pcgex = df[df["path"] == "pcg_time_avg_chol_explicit_avgK"]
    if not sub_pcgex.empty:
        g = sub_pcgex.groupby("Tn", as_index=False).agg(
            kbar_bytes=("Kbar_csr_bytes_estimate", "median"),
            l_nnz=("L_factor_nnz", "median"),
        )
        g["bytes"] = g["kbar_bytes"] + g["l_nnz"] * _CSR_BYTES_PER_NNZ
        g = g.sort_values("Tn")
        axes[0].plot(
            g["Tn"], g["bytes"] / 1024**2, marker="s",
            label="PCG explicit Kbar_avg: Kbar_avg + L factor",
            color=_PATH_COLORS["pcg_time_avg_chol_explicit_avgK"],
        )

    sub_band = df[df["path"] == "pcg_banded_time_avg_precision_chol"]
    if not sub_band.empty:
        g = sub_band.groupby("Tn", as_index=False).agg(
            ab=("banded_ab_bytes", "median"),
            fac=("banded_factor_bytes", "median"),
        )
        g["bytes"] = g["ab"] + g["fac"]
        g = g.sort_values("Tn")
        axes[0].plot(
            g["Tn"], g["bytes"] / 1024**2, marker="^",
            label="PCG banded: ab + cholesky factor",
            color=_PATH_COLORS["pcg_banded_time_avg_precision_chol"],
        )

    axes[0].set_xscale("log")
    axes[0].set_yscale("log")
    axes[0].set_xlabel("Tn")
    axes[0].set_ylabel("peak storage proxy (MB, median)")
    axes[0].set_title("Per-path peak storage")
    axes[0].grid(True, which="both", alpha=0.3)
    axes[0].legend(fontsize=8)

    # Right: bandwidth u vs Tn (banded path only).
    if not sub_band.empty:
        g = sub_band.groupby(["n", "p", "Tn"], as_index=False).agg(
            u=("bandwidth_u", "median"),
        )
        for (n_v, p_v), sub in g.groupby(["n", "p"]):
            sub = sub.sort_values("Tn")
            axes[1].plot(
                sub["Tn"], sub["u"], marker="o",
                label=f"n={n_v}, p={p_v}",
            )
    axes[1].set_xscale("log")
    axes[1].set_xlabel("Tn")
    axes[1].set_ylabel("scalar half-bandwidth u")
    axes[1].set_title("Banded path bandwidth")
    axes[1].grid(True, which="both", alpha=0.3)
    axes[1].legend(fontsize=7, loc="best", ncol=2)

    fig.suptitle(
        "Thread 2c memory accounting (sv_sigma = 0.3, lam = 1e4)",
        fontsize=11,
    )
    fig.tight_layout()
    for ext in ("pdf", "png"):
        fig.savefig(
            out_dir / f"fig_memory_vs_Tn.{ext}",
            dpi=160, bbox_inches="tight",
        )
    plt.close(fig)


# ---------------------------------------------------------------------------
# 3. Phase breakdown
# ---------------------------------------------------------------------------


def plot_phase_breakdown(df: pd.DataFrame, out_dir: Path) -> None:
    df = _ok_only(df)
    df = df[df["sv_sigma"] == 0.3]
    df = df[df["lam"] == 1e4]

    points = [
        (5, 480, 2),
        (10, 1920, 12),
        (20, 5000, 12),
        (20, 10000, 12),
    ]
    sets = []
    for (n_v, T_v, p_v) in points:
        sub = df[(df["n"] == n_v) & (df["T"] == T_v) & (df["p"] == p_v)]
        if not sub.empty:
            sets.append((n_v, T_v, p_v, sub))
    if not sets:
        return

    fig, axes = plt.subplots(
        1, len(sets), figsize=(3.9 * len(sets), 4.0), sharey=True
    )
    if len(sets) == 1:
        axes = [axes]
    for ax, (n_v, T_v, p_v, sub) in zip(axes, sets):
        med = sub.groupby("path", as_index=False).agg(
            asm=("phase1_assembly_time", "median"),
            fac=("phase2_factor_time", "median"),
            sol=("phase3_solve_time", "median"),
        )
        med = med[med["path"].isin(_PATH_ORDER)].copy()
        med["path"] = pd.Categorical(med["path"], categories=_PATH_ORDER, ordered=True)
        med = med.sort_values("path")
        x = np.arange(len(med))
        ax.bar(x, med["asm"] * 1e3, color="#bbbbbb", label="assembly")
        ax.bar(
            x, med["fac"] * 1e3, bottom=med["asm"] * 1e3,
            color="#7f7f7f", label="factor/setup",
        )
        ax.bar(
            x, med["sol"] * 1e3,
            bottom=(med["asm"] + med["fac"]) * 1e3,
            color="#000000", label="solve/PCG",
        )
        ax.set_xticks(x)
        ax.set_xticklabels(
            [_PATH_LABEL[p] for p in med["path"]],
            rotation=30, ha="right", fontsize=7,
        )
        ax.set_title(f"n={n_v}, T={T_v}, p={p_v}")
        ax.set_yscale("log")
        ax.grid(True, axis="y", which="both", alpha=0.3)

    axes[0].set_ylabel("time (ms, log)")
    axes[-1].legend(fontsize=8, loc="upper left")
    fig.suptitle(
        "Thread 2c phase breakdown (sv_sigma = 0.3, lam = 1e4)", fontsize=11
    )
    fig.tight_layout()
    for ext in ("pdf", "png"):
        fig.savefig(
            out_dir / f"fig_phase_breakdown.{ext}",
            dpi=160, bbox_inches="tight",
        )
    plt.close(fig)


# ---------------------------------------------------------------------------
# 4. iters vs sv_sigma (alignment carry-over)
# ---------------------------------------------------------------------------


def plot_iters_vs_sv(df: pd.DataFrame, out_dir: Path) -> None:
    df = _ok_only(df)
    df = df[df["lam"] == 1e4]
    df = df[df["path"].isin([
        "pcg_time_avg_chol_explicit_avgK",
        "pcg_banded_time_avg_precision_chol",
    ])]

    # Pick a representative (n, T, p) where both PCG paths run.
    (n_pick, T_pick, p_pick) = (5, 1920, 2)
    sub = df[(df["n"] == n_pick) & (df["T"] == T_pick) & (df["p"] == p_pick)]
    if sub.empty:
        return

    fig, ax = plt.subplots(figsize=(5.4, 3.6))
    for path in [
        "pcg_time_avg_chol_explicit_avgK",
        "pcg_banded_time_avg_precision_chol",
    ]:
        sub_p = sub[sub["path"] == path]
        if sub_p.empty:
            continue
        grp = sub_p.groupby("sv_sigma", as_index=False)["iters"].median()
        grp = grp.sort_values("sv_sigma")
        ax.plot(
            grp["sv_sigma"], grp["iters"], marker="o",
            label=_PATH_LABEL[path], color=_PATH_COLORS[path],
        )
    ax.set_yscale("log")
    ax.set_xlabel("sv_sigma")
    ax.set_ylabel("PCG iters (median)")
    ax.set_title(
        f"PCG iteration alignment (n={n_pick}, T={T_pick}, p={p_pick}, "
        f"lam=1e4)"
    )
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=8)
    fig.tight_layout()
    for ext in ("pdf", "png"):
        fig.savefig(
            out_dir / f"fig_iters_vs_sv_sigma.{ext}",
            dpi=160, bbox_inches="tight",
        )
    plt.close(fig)


# ---------------------------------------------------------------------------
# 5. Lambda sensitivity
# ---------------------------------------------------------------------------


def plot_lambda_sensitivity(df: pd.DataFrame, out_dir: Path) -> None:
    df = _ok_only(df)
    cells = [
        (5,  1920,  2),
        (10, 5000,  12),
        (20, 10000, 12),
    ]
    sets = []
    for (n_v, T_v, p_v) in cells:
        sub = df[(df["n"] == n_v) & (df["T"] == T_v) & (df["p"] == p_v) & (df["sv_sigma"] == 0.3)]
        if not sub.empty and sub["lam"].nunique() > 1:
            sets.append((n_v, T_v, p_v, sub))
    if not sets:
        return

    fig, axes = plt.subplots(
        1, len(sets), figsize=(4.3 * len(sets), 3.8), sharey=False
    )
    if len(sets) == 1:
        axes = [axes]
    for ax, (n_v, T_v, p_v, sub) in zip(axes, sets):
        for path in _PATH_ORDER:
            sub_p = sub[sub["path"] == path]
            if sub_p.empty:
                continue
            grp = sub_p.groupby("lam", as_index=False)["total_time"].median()
            grp = grp.sort_values("lam")
            ax.plot(
                grp["lam"], grp["total_time"] * 1e3, marker="o",
                label=_PATH_LABEL[path], color=_PATH_COLORS[path],
            )
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xlabel("lambda")
        ax.set_title(f"n={n_v}, T={T_v}, p={p_v}")
        ax.grid(True, which="both", alpha=0.3)

    axes[0].set_ylabel("total time (ms, median)")
    axes[-1].legend(fontsize=8, loc="best")
    fig.suptitle(
        "Thread 2c lambda stress slice (sv_sigma = 0.3)", fontsize=11
    )
    fig.tight_layout()
    for ext in ("pdf", "png"):
        fig.savefig(
            out_dir / f"fig_lambda_sensitivity.{ext}",
            dpi=160, bbox_inches="tight",
        )
    plt.close(fig)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", type=Path, default=_THIS_DIR / "results.csv")
    parser.add_argument("--out-dir", type=Path, default=_THIS_DIR)
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(args.results)
    plot_total_time_vs_T(df, args.out_dir)
    plot_memory_vs_Tn(df, args.out_dir)
    plot_phase_breakdown(df, args.out_dir)
    plot_iters_vs_sv(df, args.out_dir)
    plot_lambda_sensitivity(df, args.out_dir)
    print(f"Plots written to {args.out_dir}")


if __name__ == "__main__":
    main()

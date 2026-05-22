"""Plots for the Thread 2b fair-cost benchmark.

Reads ``results.csv`` written by ``sweep.py``. Produces three figures:

1. ``fig_total_time_vs_T.{pdf,png}``  -- median total time vs T, one line
   per path. Stratified by ``n``, with ``p`` fixed at the largest still-
   feasible value per (n, T).
2. ``fig_memory_vs_Tn.{pdf,png}``     -- L factor nnz, Kbar nnz estimate,
   H_B nnz vs Tn for each path.
3. ``fig_phase_breakdown.{pdf,png}``  -- stacked bars of
   (assembly, factor, solve) per path at a representative ``(n, T)`` set.
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
    "direct_splu": "#aec7e8",
    "pcg_time_avg_chol_explicit_avgK": "#d62728",
    "pcg_time_avg_chol_frozen_amortized_50": "#ff9896",
}
_PATH_ORDER = [
    "direct_cholmod",
    "direct_splu",
    "pcg_time_avg_chol_explicit_avgK",
    "pcg_time_avg_chol_frozen_amortized_50",
]
_PATH_LABEL = {
    "direct_cholmod": "direct CHOLMOD",
    "direct_splu": "direct SPLU",
    "pcg_time_avg_chol_explicit_avgK": "PCG (time-avg CHOLMOD)",
    "pcg_time_avg_chol_frozen_amortized_50": "PCG amortised 50",
}


def _ok_only(df: pd.DataFrame) -> pd.DataFrame:
    keep = df["status"].astype(str).isin({"ok", "derived_best_case"})
    return df.loc[keep].copy()


def plot_total_time_vs_T(df: pd.DataFrame, out_dir: Path) -> None:
    df = _ok_only(df)
    sv_sigma_main = 0.3  # production-nominal slice
    df = df[df["sv_sigma"] == sv_sigma_main]

    n_vals = sorted(df["n"].unique())
    fig, axes = plt.subplots(1, len(n_vals), figsize=(4.4 * len(n_vals), 3.6), sharey=True)
    if len(n_vals) == 1:
        axes = [axes]

    for ax, n_val in zip(axes, n_vals):
        sub_n = df[df["n"] == n_val]
        # Pick the largest still-feasible p value per (n, T) for a clean
        # comparison line. (Smaller p is easier; we want the stress.)
        for path in _PATH_ORDER:
            sub_p = sub_n[sub_n["path"] == path]
            if sub_p.empty:
                continue
            grp = sub_p.groupby("T", as_index=False)["total_time"].median()
            grp = grp.sort_values("T")
            ax.plot(grp["T"], grp["total_time"] * 1e3, marker="o",
                    label=_PATH_LABEL[path], color=_PATH_COLORS[path], linewidth=1.6)
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_title(f"n = {n_val}")
        ax.set_xlabel("T")
        ax.grid(True, which="both", alpha=0.3)

    axes[0].set_ylabel("total time (ms, median)")
    axes[-1].legend(fontsize=8, loc="upper left")
    fig.suptitle(f"Total per-iteration cost vs T (sv_sigma = {sv_sigma_main})",
                 fontsize=11)
    fig.tight_layout()
    for ext in ("pdf", "png"):
        fig.savefig(out_dir / f"fig_total_time_vs_T.{ext}", dpi=160, bbox_inches="tight")
    plt.close(fig)


def plot_memory_vs_Tn(df: pd.DataFrame, out_dir: Path) -> None:
    """Memory proxies: L factor nnz, Kbar estimated nnz, H_B nnz."""
    df = _ok_only(df)
    df = df[df["sv_sigma"] == 0.3]

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))

    # Left: L factor nnz per path (only direct_cholmod and PCG-Kbar_avg).
    for path in ["direct_cholmod", "direct_splu", "pcg_time_avg_chol_explicit_avgK"]:
        sub = df[(df["path"] == path) & (df["L_factor_nnz"] > 0)]
        if sub.empty:
            continue
        grp = sub.groupby("Tn", as_index=False)["L_factor_nnz"].median()
        axes[0].plot(grp["Tn"], grp["L_factor_nnz"], marker="o",
                     label=_PATH_LABEL[path], color=_PATH_COLORS[path])
    axes[0].set_xscale("log")
    axes[0].set_yscale("log")
    axes[0].set_xlabel("Tn")
    axes[0].set_ylabel("L factor nnz (median)")
    axes[0].set_title("Factor fill-in")
    axes[0].grid(True, which="both", alpha=0.3)
    axes[0].legend(fontsize=8)

    # Right: H_B nnz vs Kbar nnz estimate vs L_factor_nnz (direct_cholmod).
    sub = df[(df["path"] == "direct_cholmod") & (df["L_factor_nnz"] > 0)]
    if not sub.empty:
        grp = sub.groupby("Tn", as_index=False).agg(
            H_B_nnz=("H_B_nnz", "median"),
            Kbar_nnz=("Kbar_nnz_estimate", "median"),
            L_nnz=("L_factor_nnz", "median"),
        )
        axes[1].plot(grp["Tn"], grp["H_B_nnz"], marker="s", label="H_B nnz (mf storage)",
                     color="#2ca02c")
        axes[1].plot(grp["Tn"], grp["Kbar_nnz"], marker="^", label="Kbar nnz (direct input)",
                     color="#9467bd")
        axes[1].plot(grp["Tn"], grp["L_nnz"], marker="o", label="L factor nnz (CHOLMOD)",
                     color="#1f77b4")
    axes[1].set_xscale("log")
    axes[1].set_yscale("log")
    axes[1].set_xlabel("Tn")
    axes[1].set_ylabel("nonzero entries (median)")
    axes[1].set_title("Storage breakdown")
    axes[1].grid(True, which="both", alpha=0.3)
    axes[1].legend(fontsize=8)

    fig.suptitle("Memory proxies for Thread 2b paths (sv_sigma = 0.3)", fontsize=11)
    fig.tight_layout()
    for ext in ("pdf", "png"):
        fig.savefig(out_dir / f"fig_memory_vs_Tn.{ext}", dpi=160, bbox_inches="tight")
    plt.close(fig)


def plot_phase_breakdown(df: pd.DataFrame, out_dir: Path) -> None:
    """Stacked bars (assembly, factor, solve) per path at four (n, T) points."""
    df = _ok_only(df)
    df = df[df["sv_sigma"] == 0.3]
    df = df[df["p"] == df["p"].mode().iloc[0]]  # most common p (likely 2 or 12)

    pivot_points = []
    for (n_val, T_val) in [(5, 480), (5, 1920), (10, 1920), (20, 1920)]:
        sub = df[(df["n"] == n_val) & (df["T"] == T_val)]
        if not sub.empty:
            pivot_points.append((n_val, T_val, sub))
    if not pivot_points:
        return

    fig, axes = plt.subplots(1, len(pivot_points),
                             figsize=(3.8 * len(pivot_points), 3.8), sharey=True)
    if len(pivot_points) == 1:
        axes = [axes]
    for ax, (n_val, T_val, sub) in zip(axes, pivot_points):
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
        ax.bar(x, med["fac"] * 1e3, bottom=med["asm"] * 1e3, color="#7f7f7f", label="factor/setup")
        ax.bar(x, med["sol"] * 1e3,
               bottom=(med["asm"] + med["fac"]) * 1e3,
               color="#000000", label="solve/PCG")
        ax.set_xticks(x)
        ax.set_xticklabels([_PATH_LABEL[p] for p in med["path"]],
                           rotation=30, ha="right", fontsize=8)
        ax.set_title(f"n={n_val}, T={T_val}")
        ax.set_yscale("log")
        ax.grid(True, axis="y", which="both", alpha=0.3)

    axes[0].set_ylabel("time (ms, log)")
    axes[-1].legend(fontsize=8)
    fig.suptitle("Phase breakdown by path (sv_sigma = 0.3)", fontsize=11)
    fig.tight_layout()
    for ext in ("pdf", "png"):
        fig.savefig(out_dir / f"fig_phase_breakdown.{ext}", dpi=160, bbox_inches="tight")
    plt.close(fig)


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
    print(f"Plots written to {args.out_dir}")


if __name__ == "__main__":
    main()

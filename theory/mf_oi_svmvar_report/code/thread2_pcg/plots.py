"""Plots for the Thread 2 PCG benchmark.

Reads ``results.csv`` from the same directory and emits:

    fig_iters_vs_sv_sigma.{pdf,png}    iter_PCG vs SV dispersion
    fig_wallclock_vs_T.{pdf,png}       wallclock vs T (per-cell aggregate)
    fig_iters_vs_lambda.{pdf,png}      bonus: lambda sensitivity
    fig_iters_vs_radius.{pdf,png}      bonus: VAR persistence sensitivity
    fig_iters_vs_p.{pdf,png}           bonus: lag length sensitivity

Each plot aggregates over seeds with the median and shows min/max as a band.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

_HERE = Path(__file__).resolve().parent

PCG_METHODS = ["none", "jacobi", "block_jacobi", "time_averaged_lu", "time_averaged_chol"]
ALL_METHODS = PCG_METHODS + ["direct_splu", "direct_cholmod"]
COLOURS = {
    "none": "#cc0000",
    "jacobi": "#ff8800",
    "block_jacobi": "#0066cc",
    "time_averaged_lu": "#009933",
    "time_averaged_chol": "#66cc33",
    "direct_splu": "#666666",
    "direct_cholmod": "#222222",
}
MARKERS = {
    "none": "o",
    "jacobi": "s",
    "block_jacobi": "D",
    "time_averaged_lu": "^",
    "time_averaged_chol": "v",
    "direct_splu": "x",
    "direct_cholmod": "+",
}
LABELS = {
    "none": "none",
    "jacobi": "Jacobi",
    "block_jacobi": "block-Jacobi",
    "time_averaged_lu": "time-avg LU",
    "time_averaged_chol": "time-avg CHOLMOD",
    "direct_splu": "direct LU",
    "direct_cholmod": "direct CHOLMOD",
}


def _agg(df: pd.DataFrame, axis: str, value_col: str) -> pd.DataFrame:
    """Median / min / max across seeds, for each (axis_value, preconditioner)."""
    sub = df[df.axis == axis].copy()
    grouped = sub.groupby(["axis_value", "preconditioner"])[value_col]
    out = grouped.agg(["median", "min", "max"]).reset_index()
    return out


def _plot_axis(
    df: pd.DataFrame,
    axis: str,
    value_col: str,
    title: str,
    xlabel: str,
    ylabel: str,
    out_stem: Path,
    *,
    log_x: bool = False,
    log_y: bool = False,
    methods: list[str] = PCG_METHODS,
    annotate_hit_maxiter: bool = False,
) -> None:
    agg = _agg(df, axis, value_col)
    fig, ax = plt.subplots(figsize=(6.5, 4.0))
    for method in methods:
        sub = agg[agg.preconditioner == method].sort_values("axis_value")
        if sub.empty:
            continue
        ax.plot(
            sub.axis_value,
            sub["median"],
            label=LABELS[method],
            color=COLOURS[method],
            marker=MARKERS[method],
            linewidth=1.6,
            markersize=5,
        )
        ax.fill_between(
            sub.axis_value, sub["min"], sub["max"],
            color=COLOURS[method], alpha=0.15, linewidth=0,
        )
    if annotate_hit_maxiter:
        sub_df = df[df.axis == axis]
        hits = sub_df.groupby(["axis_value", "preconditioner"]).hit_maxiter.max().reset_index()
        for _, row in hits[hits.hit_maxiter == 1].iterrows():
            method = row.preconditioner
            if method not in methods:
                continue
            v = row.axis_value
            med = agg[(agg.axis_value == v) & (agg.preconditioner == method)]["median"].values
            if len(med):
                ax.scatter([v], med, marker="x", s=120, color=COLOURS[method], zorder=5)
    if log_x:
        ax.set_xscale("log")
    if log_y:
        ax.set_yscale("log")
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend(frameon=False, loc="best", fontsize=9)
    ax.grid(True, which="both", linestyle=":", alpha=0.4)
    fig.tight_layout()
    for ext in ("pdf", "png"):
        fig.savefig(out_stem.with_suffix(f".{ext}"), dpi=150)
    plt.close(fig)


def main() -> None:
    df = pd.read_csv(_HERE / "results.csv")

    _plot_axis(
        df, "sv_sigma", "iters",
        title="PCG iterations vs SV dispersion (n=5, T=480, p=2, λ=1e4)",
        xlabel=r"$\sigma_{\mathrm{SV}}$",
        ylabel="iter_PCG (median across seeds; x = hit maxiter)",
        out_stem=_HERE / "fig_iters_vs_sv_sigma",
        log_y=True,
        annotate_hit_maxiter=True,
    )
    _plot_axis(
        df, "T", "solve_time",
        title="Wallclock vs T (n=5, p=2, σ_SV=0.3, λ=1e4)",
        xlabel="T",
        ylabel="solve time (seconds)",
        out_stem=_HERE / "fig_wallclock_vs_T",
        log_x=True, log_y=True,
        methods=ALL_METHODS,
    )
    _plot_axis(
        df, "lam", "iters",
        title="PCG iterations vs λ (n=5, T=480, p=2, σ_SV=0.3)",
        xlabel=r"$\lambda$",
        ylabel="iter_PCG (median)",
        out_stem=_HERE / "fig_iters_vs_lambda",
        log_x=True, log_y=True,
    )
    _plot_axis(
        df, "target_radius", "iters",
        title="PCG iterations vs VAR persistence (n=5, T=480, p=2, σ_SV=0.3, λ=1e4)",
        xlabel="companion spectral radius",
        ylabel="iter_PCG (median)",
        out_stem=_HERE / "fig_iters_vs_radius",
        log_y=True,
    )
    _plot_axis(
        df, "p", "iters",
        title="PCG iterations vs VAR lag length (n=5, T=480, σ_SV=0.3, λ=1e4)",
        xlabel="p",
        ylabel="iter_PCG (median)",
        out_stem=_HERE / "fig_iters_vs_p",
        log_y=True,
    )
    print("Wrote plots to:", _HERE)


if __name__ == "__main__":
    main()

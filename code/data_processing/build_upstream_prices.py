#!/usr/bin/env python3
"""Build a WPI/PPI-spliced upstream price pressure series for Taiwan.

The legacy Taiwan WPI series ends in 2022-12. The newer PPI series begins in
2021-01. This script uses the 2021-01--2022-12 overlap to rescale the PPI level
to the WPI level, then appends adjusted PPI from 2023-01 onward.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from config import RAW_TW_MACRO


OVERLAP_START = "2021-01-01"
OVERLAP_END = "2022-12-01"
SPLICE_START = "2023-01-01"


def read_series(filename: str, value_name: str) -> pd.DataFrame:
    path = RAW_TW_MACRO / filename
    df = pd.read_csv(path, parse_dates=["Date"])
    df[value_name] = pd.to_numeric(df["Value"], errors="coerce")
    return df[["Date", value_name]].sort_values("Date").reset_index(drop=True)


def main() -> None:
    wpi = read_series("tw_wpi_raw.csv", "wpi_index")
    ppi = read_series("tw_ppi_index_raw.csv", "ppi_index")
    ppi_yoy = read_series("tw_ppi_yoy_raw.csv", "ppi_yoy_official")

    data = wpi.merge(ppi, on="Date", how="outer").merge(ppi_yoy, on="Date", how="outer")
    data = data.sort_values("Date").reset_index(drop=True)

    overlap = data[
        (data["Date"] >= pd.Timestamp(OVERLAP_START))
        & (data["Date"] <= pd.Timestamp(OVERLAP_END))
        & data["wpi_index"].notna()
        & data["ppi_index"].notna()
    ].copy()
    if overlap.empty:
        raise RuntimeError("No WPI/PPI overlap found.")

    mean_ratio = (overlap["wpi_index"] / overlap["ppi_index"]).mean()
    endpoint_ratio = (
        overlap.loc[overlap["Date"] == pd.Timestamp(OVERLAP_END), "wpi_index"].iloc[0]
        / overlap.loc[overlap["Date"] == pd.Timestamp(OVERLAP_END), "ppi_index"].iloc[0]
    )

    data["ppi_index_adjusted"] = data["ppi_index"] * mean_ratio
    data["tw_upstream_prices_index"] = data["wpi_index"]
    use_ppi = data["Date"] >= pd.Timestamp(SPLICE_START)
    data.loc[use_ppi, "tw_upstream_prices_index"] = data.loc[use_ppi, "ppi_index_adjusted"]
    data["source_component"] = "WPI"
    data.loc[use_ppi, "source_component"] = "PPI adjusted to WPI level"
    data.loc[data["tw_upstream_prices_index"].isna(), "source_component"] = ""

    data["tw_upstream_prices_yoy"] = data["tw_upstream_prices_index"].pct_change(12) * 100
    data["wpi_yoy_from_index"] = data["wpi_index"].pct_change(12) * 100
    data["ppi_yoy_from_index"] = data["ppi_index"].pct_change(12) * 100
    data["wpi_mom"] = data["wpi_index"].pct_change() * 100
    data["ppi_mom"] = data["ppi_index"].pct_change() * 100

    overlap_yoy = data[
        (data["Date"] >= pd.Timestamp("2022-01-01"))
        & (data["Date"] <= pd.Timestamp(OVERLAP_END))
    ]
    overlap_mom = data[
        (data["Date"] >= pd.Timestamp("2021-02-01"))
        & (data["Date"] <= pd.Timestamp(OVERLAP_END))
    ]

    diagnostics = pd.DataFrame(
        [
            ("overlap_start", OVERLAP_START[:7]),
            ("overlap_end", OVERLAP_END[:7]),
            ("splice_start", SPLICE_START[:7]),
            ("overlap_months_level", len(overlap)),
            ("mean_level_ratio_wpi_over_ppi", mean_ratio),
            ("endpoint_ratio_2022_12", endpoint_ratio),
            (
                "corr_wpi_ppi_yoy_2022",
                overlap_yoy[["wpi_yoy_from_index", "ppi_yoy_from_index"]].corr().iloc[0, 1],
            ),
            ("corr_wpi_ppi_mom_overlap", overlap_mom[["wpi_mom", "ppi_mom"]].corr().iloc[0, 1]),
            ("mean_abs_yoy_gap_2022", (overlap_yoy["wpi_yoy_from_index"] - overlap_yoy["ppi_yoy_from_index"]).abs().mean()),
            ("mean_abs_mom_gap_overlap", (overlap_mom["wpi_mom"] - overlap_mom["ppi_mom"]).abs().mean()),
        ],
        columns=["metric", "value"],
    )

    out = data[
        [
            "Date",
            "tw_upstream_prices_index",
            "tw_upstream_prices_yoy",
            "source_component",
            "wpi_index",
            "ppi_index",
            "ppi_index_adjusted",
            "wpi_yoy_from_index",
            "ppi_yoy_from_index",
            "ppi_yoy_official",
        ]
    ].copy()
    out["splice_method"] = f"PPI scaled by 2021-01--2022-12 mean WPI/PPI ratio ({mean_ratio:.8f})"

    RAW_TW_MACRO.mkdir(parents=True, exist_ok=True)
    out_path = RAW_TW_MACRO / "tw_upstream_prices_raw.csv"
    diag_path = RAW_TW_MACRO / "tw_upstream_prices_splice_diagnostics.csv"
    out.to_csv(out_path, index=False)
    diagnostics.to_csv(diag_path, index=False)

    start = out.loc[out["tw_upstream_prices_index"].notna(), "Date"].min().strftime("%Y-%m")
    end = out.loc[out["tw_upstream_prices_index"].notna(), "Date"].max().strftime("%Y-%m")
    print(f"Saved {out_path} ({start} to {end})")
    print(f"Saved {diag_path}")
    print(diagnostics.to_string(index=False))


if __name__ == "__main__":
    main()

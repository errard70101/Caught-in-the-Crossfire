#!/usr/bin/env python3
"""Construct real manufacturing and services wage growth series."""

from __future__ import annotations

import pandas as pd

from config import RAW_TW_MACRO


def read_value(filename: str, column_name: str) -> pd.DataFrame:
    df = pd.read_csv(RAW_TW_MACRO / filename, parse_dates=["Date"])
    df[column_name] = pd.to_numeric(df["Value"], errors="coerce")
    return df[["Date", column_name]].sort_values("Date")


def main() -> None:
    cpi = read_value("tw_cpi_index_raw.csv", "cpi_index")
    mfg_total = read_value("tw_mfg_total_wages_raw.csv", "tw_mfg_total_wages_nominal")
    svc_total = read_value("tw_svc_total_wages_raw.csv", "tw_svc_total_wages_nominal")
    mfg_regular = read_value("tw_mfg_regular_wages_raw.csv", "tw_mfg_regular_wages_nominal")
    svc_regular = read_value("tw_svc_regular_wages_raw.csv", "tw_svc_regular_wages_nominal")

    data = (
        mfg_total
        .merge(svc_total, on="Date", how="outer")
        .merge(mfg_regular, on="Date", how="outer")
        .merge(svc_regular, on="Date", how="outer")
        .merge(cpi, on="Date", how="left")
        .sort_values("Date")
        .reset_index(drop=True)
    )

    nominal_cols = [
        "tw_mfg_total_wages_nominal",
        "tw_svc_total_wages_nominal",
        "tw_mfg_regular_wages_nominal",
        "tw_svc_regular_wages_nominal",
    ]
    for col in nominal_cols:
        data.loc[data[col] <= 0, col] = pd.NA
        real_col = col.replace("_nominal", "_real")
        yoy_col = col.replace("_nominal", "_real_yoy")
        data[real_col] = data[col] / data["cpi_index"] * 100
        data[yoy_col] = data[real_col].pct_change(12) * 100

    # Baseline model variables use regular earnings. Total earnings include
    # bonuses and show large Lunar New Year timing spikes in monthly YoY growth.
    data["tw_mfg_wages"] = data["tw_mfg_regular_wages_real_yoy"]
    data["tw_svc_wages"] = data["tw_svc_regular_wages_real_yoy"]

    data["source"] = (
        "Authors' construction from DGBAS A046201010/A046301010 wages "
        "deflated by DGBAS CPI index"
    )
    data["transform"] = "100 * YoY percent change of nominal wage / CPI index"

    out = data[
        [
            "Date",
            "tw_mfg_wages",
            "tw_svc_wages",
            "tw_mfg_total_wages_nominal",
            "tw_svc_total_wages_nominal",
            "tw_mfg_total_wages_real",
            "tw_svc_total_wages_real",
            "tw_mfg_regular_wages_nominal",
            "tw_svc_regular_wages_nominal",
            "tw_mfg_regular_wages_real",
            "tw_svc_regular_wages_real",
            "tw_mfg_total_wages_real_yoy",
            "tw_svc_total_wages_real_yoy",
            "cpi_index",
            "source",
            "transform",
        ]
    ].copy()

    out_path = RAW_TW_MACRO / "tw_real_wages_raw.csv"
    out.to_csv(out_path, index=False)

    valid = out.dropna(subset=["tw_mfg_wages", "tw_svc_wages"])
    print(
        f"Saved {out_path} ({len(out)} rows; transformed series "
        f"{valid['Date'].min():%Y-%m} to {valid['Date'].max():%Y-%m})"
    )


if __name__ == "__main__":
    main()

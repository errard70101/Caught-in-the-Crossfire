#!/usr/bin/env python3
"""Download monthly series from FRED via public CSV endpoint (no API key needed)."""

from __future__ import annotations

import time
from io import StringIO
from pathlib import Path

import pandas as pd
import requests

from config import FRED_SERIES, RAW_US, RAW_CN, RAW_GL, RAW_TW_FIN, SAMPLE_START, SAMPLE_END

FRED_CSV_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv"

DEST_MAP = {
    "us_ffr": RAW_US,
    "us_ipi": RAW_US,
    "us_credit_spread": RAW_US,
    "gl_vix": RAW_GL,
    "tw_twdusd": RAW_TW_FIN,
}


def download_fred_series(name: str, series_id: str, dest_dir: Path) -> Path:
    """Download a single FRED series as CSV."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    out_path = dest_dir / f"{name}_raw.csv"

    params = {
        "id": series_id,
        "cosd": "2000-01-01",  # fetch slightly early for YoY / lag computations
        "coed": SAMPLE_END,
    }
    print(f"  Downloading {name} ({series_id})...", end=" ")
    resp = requests.get(FRED_CSV_URL, params=params, timeout=30)
    resp.raise_for_status()

    # FRED CSV uses "observation_date" as date column
    df = pd.read_csv(
        StringIO(resp.text),
        parse_dates=["observation_date"],
    )
    df = df.rename(columns={"observation_date": "date", series_id: name})
    df[name] = pd.to_numeric(df[name], errors="coerce")

    # For daily series (VIX, TWD/USD), aggregate to monthly
    if df["date"].diff().dt.days.median() < 15:
        df = df.set_index("date").resample("ME").agg(
            **{name: (name, "mean")}
        )
        df.index = df.index.to_period("M").to_timestamp()
        df = df.reset_index().rename(columns={"index": "date"})

    df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m")
    df.to_csv(out_path, index=False)

    n_obs = df[name].notna().sum()
    print(f"{n_obs} obs, {df['date'].iloc[0]} to {df['date'].iloc[-1]}")
    return out_path


def main() -> None:
    print("=" * 60)
    print("FRED Data Download")
    print("=" * 60)

    for name, series_id in FRED_SERIES.items():
        dest = DEST_MAP[name]
        try:
            download_fred_series(name, series_id, dest)
        except Exception as e:
            print(f"  ERROR: {name} ({series_id}): {e}")
        time.sleep(0.5)  # polite rate limiting

    print("\nDone.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Download daily NTD/USD data and construct monthly realized volatility."""

from __future__ import annotations

from io import StringIO

import numpy as np
import pandas as pd
import requests

from config import RAW_TW_FIN, SAMPLE_END


FRED_CSV_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv"
FRED_SERIES = "DEXTAUS"


def download_daily_twdusd() -> pd.DataFrame:
    params = {
        "id": FRED_SERIES,
        "cosd": "2000-01-01",
        "coed": SAMPLE_END,
    }
    resp = requests.get(FRED_CSV_URL, params=params, timeout=30)
    resp.raise_for_status()

    df = pd.read_csv(StringIO(resp.text), parse_dates=["observation_date"])
    df = df.rename(columns={"observation_date": "date", FRED_SERIES: "tw_twdusd"})
    df["tw_twdusd"] = pd.to_numeric(df["tw_twdusd"], errors="coerce")
    df = df.dropna(subset=["tw_twdusd"]).sort_values("date")
    df["source"] = "FRED DEXTAUS"
    return df


def construct_monthly_volatility(daily: pd.DataFrame) -> pd.DataFrame:
    df = daily.copy()
    df["log_fx"] = np.log(df["tw_twdusd"])
    df["daily_log_return"] = df["log_fx"].diff()
    df.loc[df["daily_log_return"].abs() > 0.25, "daily_log_return"] = np.nan
    df["month"] = df["date"].dt.to_period("M")

    monthly = df.groupby("month").agg(
        tw_fx_vol=("daily_log_return", lambda x: x.std(skipna=True) * 100),
        tw_fx_rv=("daily_log_return", lambda x: np.sqrt(np.nansum(np.square(x))) * 100),
        tw_twdusd=("tw_twdusd", "mean"),
        trading_days=("daily_log_return", "count"),
    )
    monthly = monthly.reset_index()
    monthly["date"] = monthly["month"].astype(str)
    monthly["source"] = "Authors' construction from FRED DEXTAUS daily data"
    return monthly[["date", "tw_fx_vol", "tw_fx_rv", "tw_twdusd", "trading_days", "source"]]


def main() -> None:
    RAW_TW_FIN.mkdir(parents=True, exist_ok=True)

    daily = download_daily_twdusd()
    daily_out = RAW_TW_FIN / "tw_twdusd_daily_raw.csv"
    daily.to_csv(daily_out, index=False)

    monthly = construct_monthly_volatility(daily)
    monthly_out = RAW_TW_FIN / "tw_fx_vol_raw.csv"
    monthly.to_csv(monthly_out, index=False)

    print(f"Saved {daily_out} ({len(daily)} daily observations)")
    print(
        f"Saved {monthly_out} ({len(monthly)} monthly observations, "
        f"{monthly['date'].iloc[0]} to {monthly['date'].iloc[-1]})"
    )


if __name__ == "__main__":
    main()

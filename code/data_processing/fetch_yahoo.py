#!/usr/bin/env python3
"""Download TAIEX data from Yahoo Finance for monthly returns and volatility."""

from __future__ import annotations

import pandas as pd
import yfinance as yf

from config import RAW_TW_FIN, SAMPLE_START, SAMPLE_END


def download_taiex() -> pd.DataFrame:
    """Download TAIEX (^TWII) daily data and compute monthly series."""
    print("  Downloading ^TWII from Yahoo Finance...", end=" ")
    ticker = yf.Ticker("^TWII")
    # Fetch from slightly before sample start for first-month return calculation
    daily = ticker.history(start="2000-11-01", end=SAMPLE_END, auto_adjust=True)

    if daily.empty:
        raise RuntimeError("No data returned for ^TWII")

    daily = daily[["Close", "Volume"]].copy()
    daily.index = daily.index.tz_localize(None)
    daily = daily.rename(columns={"Close": "close", "Volume": "volume"})
    daily["log_ret"] = daily["close"].apply(pd.np.log if hasattr(pd, "np") else __import__("numpy").log).diff()

    # Monthly aggregation
    monthly = daily.resample("ME").agg(
        close_last=("close", "last"),
        volume_mean=("volume", "mean"),
        log_ret_sum=("log_ret", "sum"),
        log_ret_std=("log_ret", "std"),
        trading_days=("close", "count"),
    )
    monthly.index = monthly.index.to_period("M").to_timestamp()
    monthly["date"] = monthly.index.strftime("%Y-%m")

    # Variables for the model
    monthly["tw_taiex_ret"] = monthly["log_ret_sum"] * 100  # monthly log return in %
    monthly["tw_taiex_vol"] = monthly["log_ret_std"] * 100  # monthly realized vol in %
    monthly["tw_taiex_level"] = monthly["close_last"].apply(__import__("numpy").log)  # log level
    monthly["tw_turnover"] = monthly["volume_mean"]  # daily avg volume

    out = monthly[["date", "tw_taiex_ret", "tw_taiex_vol", "tw_taiex_level", "tw_turnover"]].copy()
    out = out[(out["date"] >= "2001-01") & (out["date"] <= "2025-12")]
    out = out.reset_index(drop=True)

    print(f"{len(out)} observations, {out['date'].iloc[0]} to {out['date'].iloc[-1]}")
    return out


def main() -> None:
    print("=" * 60)
    print("Yahoo Finance Download (TAIEX)")
    print("=" * 60)

    RAW_TW_FIN.mkdir(parents=True, exist_ok=True)
    try:
        df = download_taiex()
        out_path = RAW_TW_FIN / "taiex_raw.csv"
        df.to_csv(out_path, index=False)
        print(f"  Saved to {out_path}")
    except Exception as e:
        print(f"  ERROR: {e}")

    print("\nDone.")


if __name__ == "__main__":
    main()

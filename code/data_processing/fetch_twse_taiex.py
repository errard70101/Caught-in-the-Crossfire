#!/usr/bin/env python3
"""Download TAIEX price and total-return indices from TWSE.

The TWSE historical price-index endpoint (MI_5MINS_HIST) is available over the
full project sample. The total-return endpoint (MFI94U) starts in 2003M1 and is
kept for post-2003 robustness checks.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from datetime import datetime

import numpy as np
import pandas as pd
import requests

from config import RAW_TW_FIN, SAMPLE_END, SAMPLE_END_YM, SAMPLE_START, SAMPLE_START_YM


TWSE_BASE = "https://www.twse.com.tw"
USER_AGENT = "Mozilla/5.0 (compatible; Caught-in-the-Crossfire data pipeline)"


@dataclass(frozen=True)
class TwseEndpoint:
    name: str
    report_path: str
    endpoint: str
    start_ym: str


PRICE_INDEX = TwseEndpoint(
    name="price",
    report_path="indicesReport",
    endpoint="MI_5MINS_HIST",
    # Fetch one month before the model sample so the first sample-month return
    # includes the previous month-end close.
    start_ym="2000-12",
)
MARKET_TURNOVER = TwseEndpoint(
    name="market_turnover",
    report_path="exchangeReport",
    endpoint="FMTQIK",
    start_ym=SAMPLE_START_YM,
)
TOTAL_RETURN_INDEX = TwseEndpoint(
    name="total_return",
    report_path="indicesReport",
    endpoint="MFI94U",
    start_ym="2003-01",
)


def month_starts(start_ym: str, end_ym: str) -> list[pd.Timestamp]:
    """Return month-start timestamps from start_ym through end_ym inclusive."""
    return list(pd.period_range(start=start_ym, end=end_ym, freq="M").to_timestamp())


def twse_month_date(month: pd.Timestamp) -> str:
    """TWSE monthly API accepts any date in the target month as YYYYMMDD."""
    return month.strftime("%Y%m01")


def roc_date_to_timestamp(value: str) -> pd.Timestamp:
    """Convert TWSE ROC date strings such as ' 90/01/02' to Timestamp."""
    year, month, day = (int(part) for part in value.strip().split("/"))
    return pd.Timestamp(year + 1911, month, day)


def parse_number(value: str) -> float:
    """Parse TWSE numeric strings containing thousands separators."""
    return float(value.replace(",", "").strip())


def fetch_month(endpoint: TwseEndpoint, month: pd.Timestamp) -> list[list[str]]:
    """Fetch one month of raw rows from a TWSE index endpoint."""
    url = f"{TWSE_BASE}/{endpoint.report_path}/{endpoint.endpoint}"
    params = {"response": "json", "date": twse_month_date(month)}
    last_error: Exception | None = None
    for attempt in range(1, 6):
        try:
            response = requests.get(url, params=params, headers={"User-Agent": USER_AGENT}, timeout=30)
            response.raise_for_status()
            payload = response.json()
            if payload.get("stat") != "OK":
                raise RuntimeError(f"{endpoint.endpoint} {params['date']} returned {payload.get('stat')}")
            data = payload.get("data", [])
            if not data:
                raise RuntimeError(f"{endpoint.endpoint} {params['date']} returned no rows")
            returned_month = roc_date_to_timestamp(data[0][0]).to_period("M")
            expected_month = month.to_period("M")
            if returned_month != expected_month:
                raise RuntimeError(
                    f"{endpoint.endpoint} {params['date']} returned {returned_month}, "
                    f"expected {expected_month}"
                )
            return data
        except Exception as exc:
            last_error = exc
            wait = 1.5 * attempt
            print(
                f"    retry {attempt}/5 for {endpoint.endpoint} {params['date']} "
                f"after {type(exc).__name__}; sleeping {wait:.1f}s"
            )
            time.sleep(wait)
    raise RuntimeError(f"Failed to fetch {endpoint.endpoint} {params['date']}") from last_error


def download_price_index() -> pd.DataFrame:
    """Download daily TAIEX price index from TWSE."""
    rows: list[dict[str, object]] = []
    months = month_starts(PRICE_INDEX.start_ym, SAMPLE_END_YM)
    for index, month in enumerate(months, start=1):
        data = fetch_month(PRICE_INDEX, month)
        for row in data:
            rows.append(
                {
                    "date": roc_date_to_timestamp(row[0]).date().isoformat(),
                    "open": parse_number(row[1]),
                    "high": parse_number(row[2]),
                    "low": parse_number(row[3]),
                    "close": parse_number(row[4]),
                    "source": "TWSE MI_5MINS_HIST",
                }
            )
        if index % 12 == 0:
            print(f"    fetched {index:3d}/{len(months)} price-index months")
        time.sleep(0.25)

    df = pd.DataFrame(rows).drop_duplicates("date").sort_values("date")
    return df[df["date"] <= SAMPLE_END].reset_index(drop=True)


def download_market_turnover() -> pd.DataFrame:
    """Download daily TWSE market turnover from FMTQIK."""
    rows: list[dict[str, object]] = []
    months = month_starts(MARKET_TURNOVER.start_ym, SAMPLE_END_YM)
    for index, month in enumerate(months, start=1):
        data = fetch_month(MARKET_TURNOVER, month)
        for row in data:
            rows.append(
                {
                    "date": roc_date_to_timestamp(row[0]).date().isoformat(),
                    "trade_volume": parse_number(row[1]),
                    "trade_value": parse_number(row[2]),
                    "transactions": parse_number(row[3]),
                    "taiex_close": parse_number(row[4]),
                    "taiex_change": parse_number(row[5]),
                    "source": "TWSE FMTQIK",
                }
            )
        if index % 12 == 0:
            print(f"    fetched {index:3d}/{len(months)} turnover months")
        time.sleep(0.25)

    df = pd.DataFrame(rows).drop_duplicates("date").sort_values("date")
    return df[(df["date"] >= SAMPLE_START) & (df["date"] <= SAMPLE_END)].reset_index(drop=True)


def download_total_return_index() -> pd.DataFrame:
    """Download daily TAIEX total-return index from TWSE."""
    rows: list[dict[str, object]] = []
    months = month_starts(TOTAL_RETURN_INDEX.start_ym, SAMPLE_END_YM)
    for index, month in enumerate(months, start=1):
        data = fetch_month(TOTAL_RETURN_INDEX, month)
        for row in data:
            rows.append(
                {
                    "date": roc_date_to_timestamp(row[0]).date().isoformat(),
                    "total_return_index": parse_number(row[1]),
                    "source": "TWSE MFI94U",
                }
            )
        if index % 12 == 0:
            print(f"    fetched {index:3d}/{len(months)} total-return months")
        time.sleep(0.25)

    df = pd.DataFrame(rows).drop_duplicates("date").sort_values("date")
    return df[(df["date"] <= SAMPLE_END)].reset_index(drop=True)


def make_turnover_monthly(daily: pd.DataFrame) -> pd.DataFrame:
    """Aggregate daily TWSE market turnover into monthly averages."""
    data = daily.copy()
    data["date"] = pd.to_datetime(data["date"])
    data = data.set_index("date").sort_index()
    monthly = data.resample("ME").agg(
        tw_turnover=("trade_value", "mean"),
        tw_trade_volume=("trade_volume", "mean"),
        tw_transactions=("transactions", "mean"),
        turnover_trading_days=("trade_value", "count"),
    )
    monthly.index = monthly.index.to_period("M").to_timestamp()
    monthly["date"] = monthly.index.strftime("%Y-%m")
    monthly["turnover_source"] = "TWSE FMTQIK"
    return monthly.reset_index(drop=True)


def make_price_monthly(daily: pd.DataFrame, turnover_daily: pd.DataFrame) -> pd.DataFrame:
    """Aggregate daily TAIEX price-index data into model monthly variables."""
    data = daily.copy()
    data["date"] = pd.to_datetime(data["date"])
    data = data.set_index("date").sort_index()
    data["log_ret"] = np.log(data["close"]).diff()

    monthly = data.resample("ME").agg(
        close_last=("close", "last"),
        log_ret_sum=("log_ret", "sum"),
        log_ret_std=("log_ret", "std"),
        trading_days=("close", "count"),
    )
    monthly.index = monthly.index.to_period("M").to_timestamp()
    monthly["date"] = monthly.index.strftime("%Y-%m")
    monthly["tw_taiex_price_ret"] = monthly["log_ret_sum"] * 100
    monthly["tw_taiex_price_vol"] = monthly["log_ret_std"] * 100
    monthly["tw_taiex_level"] = np.log(monthly["close_last"])
    monthly["source"] = "TWSE MI_5MINS_HIST"

    turnover_monthly = make_turnover_monthly(turnover_daily)
    monthly = monthly.reset_index(drop=True).merge(turnover_monthly, on="date", how="left")

    out = monthly[
        [
            "date",
            "tw_taiex_price_ret",
            "tw_taiex_price_vol",
            "tw_taiex_level",
            "tw_turnover",
            "tw_trade_volume",
            "tw_transactions",
            "close_last",
            "trading_days",
            "turnover_trading_days",
            "source",
            "turnover_source",
        ]
    ].copy()
    return out[(out["date"] >= SAMPLE_START_YM) & (out["date"] <= SAMPLE_END_YM)].reset_index(drop=True)


def make_model_taiex_monthly(price_monthly: pd.DataFrame, total_return_monthly: pd.DataFrame) -> pd.DataFrame:
    """Create the model-facing TAIEX monthly file.

    Baseline return and volatility use the total-return index. Price-index return
    and volatility are retained for the 2001M1 robustness sample.
    """
    total_return = total_return_monthly[
        ["date", "tw_taiex_tr_ret", "tw_taiex_tr_vol", "tw_taiex_tr_level", "total_return_last"]
    ].copy()
    data = price_monthly.merge(total_return, on="date", how="left")
    data["tw_taiex_ret"] = data["tw_taiex_tr_ret"]
    data["tw_taiex_vol"] = data["tw_taiex_tr_vol"]
    data["return_source"] = "TWSE MFI94U"
    data.loc[data["tw_taiex_ret"].isna(), "return_source"] = ""
    data["level_source"] = "TWSE MI_5MINS_HIST"

    cols = [
        "date",
        "tw_taiex_ret",
        "tw_taiex_vol",
        "tw_taiex_level",
        "tw_turnover",
        "tw_trade_volume",
        "tw_transactions",
        "tw_taiex_price_ret",
        "tw_taiex_price_vol",
        "tw_taiex_tr_ret",
        "tw_taiex_tr_vol",
        "tw_taiex_tr_level",
        "close_last",
        "total_return_last",
        "trading_days",
        "turnover_trading_days",
        "source",
        "turnover_source",
        "return_source",
        "level_source",
    ]
    return data[cols].copy()


def make_total_return_monthly(daily: pd.DataFrame) -> pd.DataFrame:
    """Aggregate daily TAIEX total-return index into robustness-check variables."""
    data = daily.copy()
    data["date"] = pd.to_datetime(data["date"])
    data = data.set_index("date").sort_index()
    data["log_ret"] = np.log(data["total_return_index"]).diff()

    monthly = data.resample("ME").agg(
        total_return_last=("total_return_index", "last"),
        log_ret_sum=("log_ret", "sum"),
        log_ret_std=("log_ret", "std"),
        trading_days=("total_return_index", "count"),
    )
    monthly.index = monthly.index.to_period("M").to_timestamp()
    monthly["date"] = monthly.index.strftime("%Y-%m")
    monthly["tw_taiex_tr_ret"] = monthly["log_ret_sum"] * 100
    monthly["tw_taiex_tr_vol"] = monthly["log_ret_std"] * 100
    monthly["tw_taiex_tr_level"] = np.log(monthly["total_return_last"])
    monthly["source"] = "TWSE MFI94U"
    # The official total-return series starts in 2003M1, so there is no
    # previous month-end observation for a full January 2003 monthly return.
    monthly.loc[monthly["date"] == TOTAL_RETURN_INDEX.start_ym, "tw_taiex_tr_ret"] = np.nan

    out = monthly[
        [
            "date",
            "tw_taiex_tr_ret",
            "tw_taiex_tr_vol",
            "tw_taiex_tr_level",
            "total_return_last",
            "trading_days",
            "source",
        ]
    ].copy()
    return out[(out["date"] >= TOTAL_RETURN_INDEX.start_ym) & (out["date"] <= SAMPLE_END_YM)].reset_index(drop=True)


def save_csv(df: pd.DataFrame, filename: str) -> None:
    path = RAW_TW_FIN / filename
    df.to_csv(path, index=False)
    print(f"  saved {filename}: {len(df)} rows")


def main() -> None:
    print("=" * 60)
    print("TWSE Download (TAIEX price and total-return indices)")
    print("=" * 60)
    print(f"Run date: {datetime.now().date().isoformat()}")

    RAW_TW_FIN.mkdir(parents=True, exist_ok=True)

    print("\nDownloading TAIEX price index (MI_5MINS_HIST)...")
    price_daily = download_price_index()

    print("\nDownloading TWSE market turnover (FMTQIK)...")
    turnover_daily = download_market_turnover()
    price_monthly = make_price_monthly(price_daily, turnover_daily)

    print("\nDownloading TAIEX total-return index (MFI94U)...")
    total_return_daily = download_total_return_index()
    total_return_monthly = make_total_return_monthly(total_return_daily)

    model_monthly = make_model_taiex_monthly(price_monthly, total_return_monthly)

    save_csv(price_daily, "twse_taiex_price_daily_raw.csv")
    save_csv(turnover_daily, "twse_market_turnover_daily_raw.csv")
    save_csv(price_monthly, "twse_taiex_price_monthly_raw.csv")
    save_csv(total_return_daily, "twse_taiex_total_return_daily_raw.csv")
    save_csv(total_return_monthly, "twse_taiex_total_return_monthly_raw.csv")
    save_csv(model_monthly, "taiex_raw.csv")

    print("\nCoverage summary")
    print(
        "  price daily: "
        f"{price_daily['date'].iloc[0]} to {price_daily['date'].iloc[-1]} "
        f"({len(price_daily)} trading days)"
    )
    print(
        "  price monthly: "
        f"{price_monthly['date'].iloc[0]} to {price_monthly['date'].iloc[-1]} "
        f"({len(price_monthly)} months)"
    )
    print(
        "  market turnover daily: "
        f"{turnover_daily['date'].iloc[0]} to {turnover_daily['date'].iloc[-1]} "
        f"({len(turnover_daily)} trading days)"
    )
    print(
        "  total-return daily: "
        f"{total_return_daily['date'].iloc[0]} to {total_return_daily['date'].iloc[-1]} "
        f"({len(total_return_daily)} trading days)"
    )
    print(
        "  total-return monthly: "
        f"{total_return_monthly['date'].iloc[0]} to {total_return_monthly['date'].iloc[-1]} "
        f"({len(total_return_monthly)} months)"
    )


if __name__ == "__main__":
    main()

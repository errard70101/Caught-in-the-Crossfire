#!/usr/bin/env python3
"""Download TWSE investor-flow and margin/short-balance variables.

Model variables produced:
- tw_foreign_inv: monthly foreign investor net buying amount, NTD.
- tw_margin_buy: YoY percent change in month-end margin purchase amount balance.
- tw_short_sell: YoY percent change in month-end short-sale unit balance.

TWSE's institutional-investor aggregate endpoint starts in 2004M4, so
tw_foreign_inv cannot cover the full 2003M1 baseline window from this source.
The margin endpoint is available from 2001 and is sampled on each month-end
trading day using the existing TWSE market-turnover calendar.
"""

from __future__ import annotations

import time
from datetime import datetime

import numpy as np
import pandas as pd
import requests

from config import RAW_TW_FIN, SAMPLE_END_YM, SAMPLE_START_YM
from fetch_twse_taiex import USER_AGENT, month_starts, parse_number, twse_month_date


TWSE_BASE = "https://www.twse.com.tw"
FOREIGN_START_YM = "2004-04"


def fetch_json(url: str, params: dict[str, str], attempts: int = 5) -> dict:
    """Fetch a TWSE JSON payload with light retry handling."""
    last_error: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            response = requests.get(url, params=params, headers={"User-Agent": USER_AGENT}, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as exc:
            last_error = exc
            wait = 1.5 * attempt
            print(
                f"    retry {attempt}/{attempts} for {url} {params} "
                f"after {type(exc).__name__}; sleeping {wait:.1f}s"
            )
            time.sleep(wait)
    raise RuntimeError(f"Failed to fetch {url} {params}") from last_error


def fetch_ok_json(url: str, params: dict[str, str], label: str, attempts: int = 8) -> dict:
    """Fetch a TWSE payload whose stat must be OK, retrying flaky TWSE replies."""
    last_stat = ""
    for attempt in range(1, attempts + 1):
        payload = fetch_json(url, params)
        if payload.get("stat") == "OK":
            return payload
        last_stat = str(payload.get("stat"))
        wait = 5.0 * attempt
        print(f"    retry {attempt}/{attempts} for {label}: {last_stat}; sleeping {wait:.1f}s")
        time.sleep(wait)
    raise RuntimeError(f"{label} returned {last_stat}")


def find_row(data: list[list[str]], prefixes: tuple[str, ...]) -> list[str]:
    """Return the first row whose label starts with one of the given prefixes."""
    for row in data:
        label = row[0].strip()
        if any(label.startswith(prefix) for prefix in prefixes):
            return row
    raise ValueError(f"Could not find row starting with {prefixes}")


def download_foreign_investor_monthly() -> pd.DataFrame:
    """Download monthly aggregate institutional-investor flows from BFI82U."""
    url = f"{TWSE_BASE}/fund/BFI82U"
    rows: list[dict[str, object]] = []
    months = month_starts(FOREIGN_START_YM, SAMPLE_END_YM)

    for index, month in enumerate(months, start=1):
        date = twse_month_date(month)
        payload = fetch_ok_json(
            url,
            {"response": "json", "monthDate": date, "type": "month"},
            f"BFI82U {date}",
        )
        data = payload.get("data", [])
        foreign = find_row(data, ("外資及陸資", "外資"))
        rows.append(
            {
                "date": month.strftime("%Y-%m"),
                "tw_foreign_inv_buy": parse_number(foreign[1]),
                "tw_foreign_inv_sell": parse_number(foreign[2]),
                "tw_foreign_inv": parse_number(foreign[3]),
                "foreign_investor_label": foreign[0].strip(),
                "source": "TWSE BFI82U monthly",
            }
        )
        if index % 12 == 0:
            print(f"    fetched {index:3d}/{len(months)} foreign-investor months")
        time.sleep(0.5)

    return pd.DataFrame(rows)


def month_end_trading_dates() -> pd.DataFrame:
    """Use the existing TWSE turnover daily file as the trading-day calendar."""
    path = RAW_TW_FIN / "twse_market_turnover_daily_raw.csv"
    if not path.exists():
        raise FileNotFoundError(
            f"{path} not found; run code/data_processing/fetch_twse_taiex.py first "
            "to build the TWSE trading-day calendar."
        )
    daily = pd.read_csv(path, parse_dates=["date"])
    daily = daily[(daily["date"].dt.strftime("%Y-%m") >= SAMPLE_START_YM) & (daily["date"].dt.strftime("%Y-%m") <= SAMPLE_END_YM)]
    out = daily.groupby(daily["date"].dt.to_period("M"))["date"].max().reset_index(drop=True)
    return pd.DataFrame({"month": out.dt.strftime("%Y-%m"), "query_date": out.dt.strftime("%Y%m%d")})


def download_margin_short_monthly() -> pd.DataFrame:
    """Download month-end margin purchase and short-sale balances from MI_MARGN."""
    url = f"{TWSE_BASE}/exchangeReport/MI_MARGN"
    calendar = month_end_trading_dates()
    rows: list[dict[str, object]] = []

    for index, item in calendar.iterrows():
        date = item["query_date"]
        payload = fetch_ok_json(
            url,
            {"response": "json", "date": date, "selectType": "MS"},
            f"MI_MARGN {date}",
        )
        table = payload.get("tables", [{}])[0]
        data = table.get("data", [])
        margin_units = find_row(data, ("融資(交易單位)",))
        short_units = find_row(data, ("融券(交易單位)",))
        margin_amount = find_row(data, ("融資金額",))
        rows.append(
            {
                "date": item["month"],
                "month_end_trading_date": pd.to_datetime(date).date().isoformat(),
                "margin_buy_units_balance": parse_number(margin_units[5]),
                "short_sell_units_balance": parse_number(short_units[5]),
                "margin_buy_amount_balance_thousand_ntd": parse_number(margin_amount[5]),
                "source": "TWSE MI_MARGN month-end trading day",
            }
        )
        if (index + 1) % 12 == 0:
            print(f"    fetched {index + 1:3d}/{len(calendar)} margin/short months")
        time.sleep(0.5)

    df = pd.DataFrame(rows)
    df["tw_margin_buy"] = df["margin_buy_amount_balance_thousand_ntd"].pct_change(12) * 100
    df["tw_short_sell"] = df["short_sell_units_balance"].pct_change(12) * 100
    df["tw_margin_buy_log_level"] = np.log(df["margin_buy_amount_balance_thousand_ntd"])
    df["tw_short_sell_log_level"] = np.log(df["short_sell_units_balance"])
    return df


def save_csv(df: pd.DataFrame, filename: str) -> None:
    path = RAW_TW_FIN / filename
    df.to_csv(path, index=False)
    print(f"  saved {filename}: {len(df)} rows")


def main() -> None:
    print("=" * 60)
    print("TWSE Download (foreign flows, margin buying, short selling)")
    print("=" * 60)
    print(f"Run date: {datetime.now().date().isoformat()}")

    RAW_TW_FIN.mkdir(parents=True, exist_ok=True)

    print("\nDownloading monthly foreign-investor flows (BFI82U)...")
    foreign = download_foreign_investor_monthly()

    print("\nDownloading month-end margin and short balances (MI_MARGN)...")
    margin_short = download_margin_short_monthly()

    save_csv(foreign, "twse_foreign_investor_monthly_raw.csv")
    save_csv(margin_short, "twse_margin_short_monthly_raw.csv")

    print("\nCoverage summary")
    print(
        "  foreign investor monthly: "
        f"{foreign['date'].iloc[0]} to {foreign['date'].iloc[-1]} "
        f"({len(foreign)} months)"
    )
    print(
        "  margin/short monthly: "
        f"{margin_short['date'].iloc[0]} to {margin_short['date'].iloc[-1]} "
        f"({len(margin_short)} months)"
    )


if __name__ == "__main__":
    main()

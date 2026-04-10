"""
fetch_stat_gov.py — Download Taiwan macro indicators from eng.stat.gov.tw

The stat.gov.tw website embeds time-series data in hidden form fields
(ContentPlaceHolder1_hidChartData). Each indicator page (sid=t.1 through t.12)
contains multiple series with monthly data going back to the 1970s-1990s.

This script fetches ALL relevant indicators for the OI-SVMVAR model.

Usage:
    python fetch_stat_gov.py
"""

import requests, re, json, pandas as pd, os, warnings, time
warnings.filterwarnings('ignore')

from config import RAW_DIR, SAMPLE_START, SAMPLE_END

STAT_GOV_BASE = "https://eng.stat.gov.tw/Point.aspx"
MACRO_DIR = os.path.join(RAW_DIR, "taiwan_macro")

# ── Indicator definitions ────────────────────────────────────────────────
# Each entry: (sid, series_index, output_filename, description)
# series_index refers to position in the hidChartData array

STAT_GOV_SERIES = [
    # Prices (sid=t.2)
    ("t.2", 0, "tw_cpi_index",      "CPI (base year=2021)"),
    ("t.2", 2, "tw_cpi_yoy",        "CPI Change Rate (yoy, %)"),
    ("t.2", 3, "tw_core_cpi_yoy",   "Core CPI Change Rate (yoy, %)"),
    ("t.2", 4, "tw_cpi_sa_mom",     "SA CPI MoM (%)"),

    # Labor (sid=t.3)
    ("t.3", 0, "tw_unemployment",    "Unemployment Rate (%)"),
    ("t.3", 1, "tw_unemployment_sa", "SA Unemployment Rate (%)"),
    ("t.3", 3, "tw_employed",        "Employed Persons (thousands)"),

    # Wages & Hours (sid=t.4)
    ("t.4", 0, "tw_payrolls",       "Employees on Payrolls"),
    ("t.4", 1, "tw_regular_wages",  "Monthly Regular Earnings (NTD)"),
    ("t.4", 2, "tw_total_wages",    "Total Monthly Earnings (NTD)"),
    ("t.4", 3, "tw_working_hours",  "Monthly Working Hours"),

    # Production & Orders (sid=t.5)
    ("t.5", 0, "tw_ipi",            "Industrial Production Index"),
    ("t.5", 2, "tw_mfg_prod",       "Manufacturing Production Index"),
    ("t.5", 4, "tw_retail_growth",   "Retail Trade Growth Rate (yoy, %)"),
    ("t.5", 6, "tw_export_orders",   "Value of Export Orders (USD mn)"),

    # Trade (sid=t.8, monthly)
    ("t.8", 0, "tw_imports",        "Imports (customs basis, USD mn)"),
    ("t.8", 1, "tw_exports",        "Exports (customs basis, USD mn)"),

    # Business Cycle (sid=t.11)
    ("t.11", 0, "tw_leading_index",  "Trend-adjusted Leading Index"),
    ("t.11", 1, "tw_coincident_idx", "Trend-adjusted Coincident Index"),
]


def fetch_stat_gov_page(sid: str) -> list:
    """Fetch all chart series from a stat.gov.tw indicator page."""
    url = f"{STAT_GOV_BASE}?sid={sid}&n=4141&sms=11480"
    r = requests.get(url, timeout=30,
                     headers={"User-Agent": "Mozilla/5.0"}, verify=False)
    r.raise_for_status()

    match = re.search(
        r'id="ContentPlaceHolder1_hidChartData"\s+value="([^"]*)"', r.text
    )
    if not match:
        raise ValueError(f"hidChartData not found for sid={sid}")

    raw = match.group(1).replace("&quot;", '"').replace("&amp;", "&")
    return json.loads(raw)


def series_to_dataframe(series_data: list) -> pd.DataFrame:
    """Convert a stat.gov.tw chart series to a clean DataFrame."""
    df = pd.DataFrame(series_data)
    df["Date"] = pd.to_datetime(df["Date"])
    df["Value"] = df["Value"].str.replace(",", "").str.strip()
    df["Value"] = pd.to_numeric(df["Value"], errors="coerce")
    df = df.sort_values("Date").reset_index(drop=True)
    return df[["Date", "Value"]]


def main():
    os.makedirs(MACRO_DIR, exist_ok=True)

    # Group downloads by sid to minimize HTTP requests
    by_sid = {}
    for sid, idx, fname, desc in STAT_GOV_SERIES:
        by_sid.setdefault(sid, []).append((idx, fname, desc))

    total = len(STAT_GOV_SERIES)
    done = 0

    for sid, items in sorted(by_sid.items()):
        print(f"\n── Fetching sid={sid} ({len(items)} series) ──")
        try:
            all_series = fetch_stat_gov_page(sid)
        except Exception as e:
            print(f"  ✗ Failed to fetch sid={sid}: {e}")
            continue

        for idx, fname, desc in items:
            if idx >= len(all_series):
                print(f"  ✗ {fname}: index {idx} out of range (only {len(all_series)} series)")
                continue

            series = all_series[idx]
            data_pts = series.get("data", [])
            if not data_pts:
                print(f"  ✗ {fname}: no data points")
                continue

            df = series_to_dataframe(data_pts)
            outpath = os.path.join(MACRO_DIR, f"{fname}_raw.csv")
            df.to_csv(outpath, index=False)

            done += 1
            print(f"  ✓ {fname}: {len(df)} obs "
                  f"({df['Date'].iloc[0].strftime('%Y-%m')} → "
                  f"{df['Date'].iloc[-1].strftime('%Y-%m')})")

        time.sleep(0.5)  # polite delay between pages

    print(f"\n{'='*50}")
    print(f"Downloaded {done}/{total} series to {MACRO_DIR}")


if __name__ == "__main__":
    main()

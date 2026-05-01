"""Download China macroeconomic variables.

Primary source for the model variables is Trading Economics' public chart data,
which republishes NBS/PBoC monthly series with long historical coverage. OECD is
kept only for the existing CPI diagnostic series.
"""

import base64
import io
import json
import os
import re
import time
import warnings
import zlib

import pandas as pd
import requests

warnings.filterwarnings("ignore")

from config import RAW_DIR, SAMPLE_START, SAMPLE_END

CHINA_DIR = os.path.join(RAW_DIR, "china")
TE_CHART_HOST = "https://d3ii0wo49og5mi.cloudfront.net"
TE_CHART_TOKEN = "20260324:loboantunes"
TE_OBFUSCATION_KEY = b"tradingeconomics-charts-core-api-key"
TE_PAGE_HEADERS = {"User-Agent": "Mozilla/5.0"}
TE_CHART_HEADERS = {"User-Agent": "Mozilla/5.0", "x-api-key": TE_CHART_TOKEN}

# ── OECD SDMX definitions ────────────────────────────────────────────────
OECD_SERIES = [
    {
        "url": ("https://sdmx.oecd.org/public/rest/data/"
                "OECD.SDD.TPS,DSD_PRICES@DF_PRICES_ALL,/"
                "CHN.M.N.CPI.PA._T.N.GY?format=csv"
                "&startPeriod=2000&endPeriod=2025"),
        "filename": "cn_cpi_yoy",
        "description": "China CPI YoY % (OECD)",
    },
]

# ── Trading Economics chart definitions ──────────────────────────────────
TE_SERIES = {
    "cn_ipi": {
        "page_url": "https://tradingeconomics.com/china/industrial-production",
        "description": "China industrial production YoY % (NBS via Trading Economics)",
        "raw_column": "cn_ipi",
        "impute_missing_january": True,
    },
    "cn_ppi": {
        "page_url": "https://tradingeconomics.com/china/producer-prices-change",
        "description": "China producer prices YoY % (NBS via Trading Economics)",
        "raw_column": "cn_ppi",
        "impute_missing_january": False,
    },
    "cn_m2": {
        "page_url": "https://tradingeconomics.com/china/money-supply-m2",
        "description": "China M2 level, CNY billion (PBoC via Trading Economics)",
        "raw_column": "cn_m2",
        "impute_missing_january": False,
    },
}


def fetch_oecd_csv(url: str) -> pd.DataFrame:
    """Fetch a CSV from the OECD SDMX API."""
    r = requests.get(url, timeout=30,
                     headers={"User-Agent": "Mozilla/5.0", "Accept": "text/csv"})
    r.raise_for_status()
    df = pd.read_csv(io.StringIO(r.text))
    out = df[["TIME_PERIOD", "OBS_VALUE"]].copy()
    out.columns = ["Date", "Value"]
    out["Date"] = pd.to_datetime(out["Date"])
    return out.sort_values("Date").reset_index(drop=True)


def extract_te_page_metadata(page_url: str) -> tuple[str, str]:
    """Extract Trading Economics chart symbol and data vintage from a page."""
    r = requests.get(page_url, timeout=30, headers=TE_PAGE_HEADERS)
    r.raise_for_status()
    symbols = [x for x in re.findall(r"TESymbol\s*=\s*'([^']*)'", r.text) if x]
    vintages = [x for x in re.findall(r"TELastUpdate\s*=\s*'([^']*)'", r.text) if x]
    if not symbols or not vintages:
        raise RuntimeError(f"Could not extract Trading Economics metadata from {page_url}")
    return symbols[-1].lower(), vintages[-1]


def decompress_te_payload(payload: str) -> str:
    """Decode Trading Economics' obfuscated compressed chart payload."""
    raw = base64.b64decode(payload)
    decoded = bytes(
        byte ^ TE_OBFUSCATION_KEY[i % len(TE_OBFUSCATION_KEY)]
        for i, byte in enumerate(raw)
    )
    return zlib.decompress(decoded, 15 + 32).decode("utf-8")


def fetch_te_chart_series(page_url: str) -> tuple[pd.DataFrame, dict[str, str]]:
    """Fetch one Trading Economics chart series as a date/value DataFrame."""
    symbol, vintage = extract_te_page_metadata(page_url)
    url = f"{TE_CHART_HOST}/economics/{symbol}?span=max&v={vintage}00"
    r = requests.get(url, timeout=30, headers=TE_CHART_HEADERS)
    r.raise_for_status()
    decoded = decompress_te_payload(r.json())
    chart = json.loads(decoded)
    serie = chart[0]["series"][0]["serie"]
    data = pd.DataFrame(serie["data"], columns=["Value", "UnixTime", "ReferenceDate", "Date"])
    data["Date"] = pd.to_datetime(data["Date"])
    data["Value"] = pd.to_numeric(data["Value"], errors="coerce")
    data = data[["Date", "Value"]].dropna(subset=["Date"]).sort_values("Date")
    data = data.drop_duplicates(subset=["Date"], keep="last")
    metadata = {
        "symbol": symbol,
        "vintage": vintage,
        "source": serie.get("source", ""),
        "unit": serie.get("unit", ""),
        "name": serie.get("name", ""),
    }
    return data.reset_index(drop=True), metadata


def fill_missing_january_with_february(df: pd.DataFrame) -> pd.DataFrame:
    """Fill missing China January values with the same year's February value.

    NBS commonly reports industrial value-added for January-February together.
    The February observation is therefore used as the January proxy, with an
    explicit imputation flag preserved in the raw file.
    """
    out = df.copy()
    out["is_imputed"] = False
    periods = out["Date"].dt.to_period("M")
    full = pd.period_range(periods.min(), periods.max(), freq="M")
    missing = full.difference(pd.PeriodIndex(periods, freq="M"))
    additions = []
    for period in missing:
        if period.month != 1:
            continue
        feb = pd.Period(year=period.year, month=2, freq="M")
        feb_value = out.loc[periods == feb, "Value"]
        if not feb_value.empty:
            additions.append({
                "Date": period.to_timestamp(),
                "Value": float(feb_value.iloc[0]),
                "is_imputed": True,
            })
    if additions:
        out = pd.concat([out, pd.DataFrame(additions)], ignore_index=True)
    return out.sort_values("Date").reset_index(drop=True)


def main():
    os.makedirs(CHINA_DIR, exist_ok=True)
    ok, fail = 0, 0

    # ── OECD series ──
    for spec in OECD_SERIES:
        print(f"  Fetching {spec['description']}...")
        try:
            df = fetch_oecd_csv(spec["url"])
            path = os.path.join(CHINA_DIR, f"{spec['filename']}_raw.csv")
            df.to_csv(path, index=False)
            print(f"  ✓ {spec['filename']}: {len(df)} obs "
                  f"({df['Date'].iloc[0].strftime('%Y-%m')} → "
                  f"{df['Date'].iloc[-1].strftime('%Y-%m')})")
            ok += 1
        except Exception as e:
            print(f"  ✗ {spec['filename']}: {e}")
            fail += 1
        time.sleep(0.5)

    # ── Trading Economics chart series ──
    for fname, spec in TE_SERIES.items():
        print(f"  Fetching {spec['description']}...")
        try:
            df, meta = fetch_te_chart_series(spec["page_url"])
            if spec["impute_missing_january"]:
                df = fill_missing_january_with_february(df)
            elif "is_imputed" not in df.columns:
                df["is_imputed"] = False

            df = df.rename(columns={"Value": spec["raw_column"], "Date": "date"})
            df["date"] = df["date"].dt.strftime("%Y-%m")
            df["source"] = meta["source"]
            df["unit"] = meta["unit"]
            df["te_symbol"] = meta["symbol"]
            df["te_vintage"] = meta["vintage"]
            path = os.path.join(CHINA_DIR, f"{fname}_raw.csv")
            df.to_csv(path, index=False)
            imputed = int(df["is_imputed"].sum())
            print(f"  ✓ {fname}: {len(df)} obs "
                  f"({df['date'].iloc[0]} → {df['date'].iloc[-1]}), "
                  f"imputed={imputed}")
            ok += 1
        except Exception as e:
            print(f"  ✗ {fname}: {e}")
            fail += 1
        time.sleep(1)

    print(f"\n{'='*50}")
    print(f"Downloaded {ok} series ({fail} failed) to {CHINA_DIR}")
    if fail:
        print("\nSome China series failed. Re-run later or inspect source page metadata.")


if __name__ == "__main__":
    main()

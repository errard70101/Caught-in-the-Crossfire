"""
fetch_china.py — Download China macroeconomic variables

Sources:
  - OECD SDMX API:  CPI YoY (working)
  - FRED (via CSV):  IPI, PPI, M2 (intermittent availability)
  - Manual:          Total Social Financing (PBoC), NBS data

Usage:
    python fetch_china.py
"""

import requests, pandas as pd, io, os, warnings, time
warnings.filterwarnings("ignore")

from config import RAW_DIR, SAMPLE_START, SAMPLE_END

CHINA_DIR = os.path.join(RAW_DIR, "china")

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

# ── FRED definitions (may time out — retry when available) ────────────────
FRED_SERIES = {
    "CHNCPIALLMINMEI":  ("cn_cpi_index",  "China CPI Index (OECD MEI)"),
    "CHNPRCNTO01IXOBM": ("cn_ppi_index",  "China PPI Index (OECD)"),
    "CHNPROINDMISMEI":  ("cn_ipi",        "China IPI (OECD MEI)"),
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


def fetch_fred_csv(series_id: str) -> pd.DataFrame | None:
    """Try to fetch a series from FRED public CSV endpoint."""
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
    try:
        r = requests.get(url, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
        if not r.ok or len(r.text) < 50:
            return None
        df = pd.read_csv(io.StringIO(r.text))
        df.columns = ["Date", "Value"]
        df["Value"] = pd.to_numeric(
            df["Value"].replace(".", pd.NA), errors="coerce"
        )
        df = df.dropna()
        return df
    except Exception:
        return None


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

    # ── FRED series ──
    for sid, (fname, label) in FRED_SERIES.items():
        print(f"  Fetching {label} from FRED...")
        df = fetch_fred_csv(sid)
        if df is not None and len(df) > 10:
            path = os.path.join(CHINA_DIR, f"{fname}_raw.csv")
            df.to_csv(path, index=False)
            print(f"  ✓ {fname}: {len(df)} obs "
                  f"({df['Date'].iloc[0]} → {df['Date'].iloc[-1]})")
            ok += 1
        else:
            print(f"  ✗ {fname}: FRED unavailable (try again later)")
            fail += 1
        time.sleep(1)

    print(f"\n{'='*50}")
    print(f"Downloaded {ok} series ({fail} failed) to {CHINA_DIR}")
    if fail:
        print("\nNote: FRED may be rate-limited. Re-run later for missing series.")
        print("Manual download needed for:")
        print("  - cn_tsf (Total Social Financing): PBoC website")


if __name__ == "__main__":
    main()

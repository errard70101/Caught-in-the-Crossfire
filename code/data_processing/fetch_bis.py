"""
fetch_bis.py — Download BIS Real Effective Exchange Rate for Taiwan

Source: BIS SDMX API (stats.bis.org)
Series: WS_EER/M.R.B.TW (Monthly, Real, Broad basket, Taiwan)

Usage:
    python fetch_bis.py
"""

import requests, pandas as pd, io, os, warnings
warnings.filterwarnings("ignore")

from config import RAW_DIR

GLOBAL_DIR = os.path.join(RAW_DIR, "global")
BIS_URL = "https://stats.bis.org/api/v1/data/WS_EER/M.R.B.TW?format=csv"


def main():
    os.makedirs(GLOBAL_DIR, exist_ok=True)

    print("  Fetching Taiwan REER from BIS...")
    r = requests.get(BIS_URL, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
    r.raise_for_status()

    df = pd.read_csv(io.StringIO(r.text))
    out = df[["TIME_PERIOD", "OBS_VALUE"]].copy()
    out.columns = ["Date", "Value"]
    out["Date"] = pd.to_datetime(out["Date"])
    out = out.sort_values("Date").reset_index(drop=True)

    path = os.path.join(GLOBAL_DIR, "tw_reer_raw.csv")
    out.to_csv(path, index=False)
    print(f"  ✓ tw_reer: {len(out)} obs "
          f"({out['Date'].iloc[0].strftime('%Y-%m')} → "
          f"{out['Date'].iloc[-1].strftime('%Y-%m')})")


if __name__ == "__main__":
    main()

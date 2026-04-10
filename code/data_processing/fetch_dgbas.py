"""
fetch_dgbas.py — Download data from DGBAS nstatdb API

Source: nstatdb.dgbas.gov.tw (National Statistics Database)
Note: API availability is intermittent (403 errors common). Re-run when accessible.

Data layout: orgdata[col_idx][row_idx] (column-major)
Row labels in ROC calendar: "113年1月" = 2024-01

Usage:
    python fetch_dgbas.py
"""

import requests, pandas as pd, json, warnings, re, os, time
warnings.filterwarnings("ignore")

from config import RAW_DIR

BASE = "https://nstatdb.dgbas.gov.tw/dgbasAll/webMain.aspx"
HEADERS = {"User-Agent": "Mozilla/5.0"}

# ── Tables to download ───────────────────────────────────────────────────
DGBAS_TABLES = [
    # (funid, col_idx, filename, subdir, description)
    ("A030201010", 0, "tw_wpi",          "taiwan_macro",  "WPI 總指數 (ends 2022-12, replaced by PPI)"),
    # Import/export prices only return sub-categories, not total index
    # Would need HTML page scraping to get total — skip for now
]


def roc_to_date(label: str) -> pd.Timestamp | None:
    """Convert ROC date '90年1月' → 2001-01-01."""
    m = re.match(r"(\d+)年(\d+)月", label)
    if m:
        return pd.Timestamp(int(m.group(1)) + 1911, int(m.group(2)), 1)
    return None


def fetch_table(funid: str) -> dict | None:
    """Fetch a DGBAS JSON table."""
    url = f"{BASE}?sys=220&funid={funid}&outmode=8&jsonplus=1"
    r = requests.get(url, timeout=15, headers=HEADERS, verify=False)
    if r.ok and len(r.text) > 100:
        return r.json()
    return None


def extract_monthly(data: dict, col_idx: int = 0) -> pd.DataFrame:
    """Extract monthly series from DGBAS JSON (column-major layout)."""
    rows = data["nrow"]
    vals = data["orgdata"][col_idx]

    dates, values = [], []
    for i, row_info in enumerate(rows):
        label = row_info[0] if isinstance(row_info, list) else str(row_info)
        if "月" in label:
            dt = roc_to_date(label)
            v = vals[i]
            if dt and v is not None and str(v) not in ("", "-"):
                try:
                    dates.append(dt)
                    values.append(float(str(v).replace(",", "")))
                except ValueError:
                    pass

    return (pd.DataFrame({"Date": dates, "Value": values})
              .sort_values("Date").reset_index(drop=True))


def main():
    ok, fail = 0, 0

    for funid, col_idx, filename, subdir, desc in DGBAS_TABLES:
        outdir = os.path.join(RAW_DIR, subdir)
        os.makedirs(outdir, exist_ok=True)

        print(f"  Fetching {desc} ({funid})...")
        data = fetch_table(funid)
        if data is None:
            print(f"  ✗ {filename}: API returned error (403?)")
            fail += 1
            continue

        df = extract_monthly(data, col_idx)
        if len(df) == 0:
            print(f"  ✗ {filename}: no monthly data found")
            fail += 1
            continue

        path = os.path.join(outdir, f"{filename}_raw.csv")
        df.to_csv(path, index=False)
        print(f"  ✓ {filename}: {len(df)} obs "
              f"({df['Date'].iloc[0].strftime('%Y-%m')} → "
              f"{df['Date'].iloc[-1].strftime('%Y-%m')})")
        ok += 1
        time.sleep(0.5)

    print(f"\nDownloaded {ok} series ({fail} failed)")


if __name__ == "__main__":
    main()

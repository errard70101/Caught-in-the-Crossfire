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
# positions are 1-based DGBAS field selections. Multiple positions return
# multiple columns in the same JSON payload.
DGBAS_TABLES = [
    {
        "funid": "A030601015",
        "fields": {
            "tw_import_prices": 5,  # 進口物價總指數_新臺幣計價_未經季節調整
            "tw_export_prices": 9,  # 出口物價總指數_新臺幣計價_未經季節調整
            "tw_wpi": 13,           # 躉售物價總指數，資料至 2022-12
        },
        "subdir": "taiwan_macro",
        "description": "Price total indices: import/export prices and legacy WPI",
    },
    {
        "funid": "A046101010",
        "fields": {
            "tw_mfg_emp": 4,   # 製造業
            "tw_svc_emp": 34,  # 服務業部門
        },
        "codlst0": "100",     # 性別：合計
        "subdir": "taiwan_macro",
        "description": "Employees by industry: manufacturing and services",
    },
    {
        "funid": "A046201010",
        "fields": {
            "tw_mfg_total_wages": 4,   # 製造業
            "tw_svc_total_wages": 34,  # 服務業部門
        },
        "codlst0": "100",     # 性別：合計
        "subdir": "taiwan_macro",
        "description": "Total monthly earnings by industry: manufacturing and services",
    },
    {
        "funid": "A046301010",
        "fields": {
            "tw_mfg_regular_wages": 4,   # 製造業
            "tw_svc_regular_wages": 34,  # 服務業部門
        },
        "codlst0": "100",     # 性別：合計
        "subdir": "taiwan_macro",
        "description": "Regular monthly earnings by industry: manufacturing and services",
    },
    {
        "funid": "A046401010",
        "fields": {
            "tw_mfg_hours": 4,   # 製造業
            "tw_svc_hours": 34,  # 服務業部門
        },
        "codlst0": "100",     # 性別：合計
        "subdir": "taiwan_macro",
        "description": "Monthly hours worked per employee by industry: manufacturing and services",
    },
    {
        "funid": "A060101010",
        "fields": {
            "tw_building_permits_area": 1,              # 總計
            "tw_building_permits_residential_area": 10, # 住宿類(H類)-住宅(H-2)
        },
        "subdir": "taiwan_macro",
        "description": "Building permit floor area by use: total and residential",
    },
    {
        "funid": "A060102010",
        "fields": {
            "tw_building_permits_structure_area": 1, # 總樓地板面積(平方公尺), total structure
            "tw_building_permits_value": 2,          # 工程造價(新臺幣千元), total structure
        },
        "subdir": "taiwan_macro",
        "description": "Building permit floor area and construction value by structure: total",
    },
    {
        "funid": "A060103010",
        "fields": {
            "tw_use_permits_area": 1,              # 總計
            "tw_use_permits_residential_area": 10, # 住宿類(H類)-住宅(H-2)
        },
        "subdir": "taiwan_macro",
        "description": "Occupancy/use permit floor area by use: total and residential",
    },
]


def make_bitstring(length: int, positions: list[int]) -> str:
    """Return a DGBAS 1/0 selection string from 1-based positions."""
    selected = set(positions)
    return "".join("1" if i in selected else "0" for i in range(1, length + 1))


def roc_to_date(label: str) -> pd.Timestamp | None:
    """Convert ROC date '90年1月' → 2001-01-01."""
    m = re.match(r"(\d+)年(\d+)月", label)
    if m:
        return pd.Timestamp(int(m.group(1)) + 1911, int(m.group(2)), 1)
    return None


def fetch_metadata(funid: str) -> dict:
    """Fetch table metadata, including selectable field count."""
    url = f"{BASE}?sys=212&x=2100&funid={funid}&plus=0&r=1"
    r = requests.get(url, timeout=15, headers=HEADERS, verify=False)
    r.raise_for_status()
    return r.json()


def fetch_table(funid: str, fldlst: str = "", codlst0: str = "") -> dict | None:
    """Fetch a DGBAS JSON table."""
    url = f"{BASE}?sys=220&funid={funid}&outmode=8&jsonplus=1"
    if fldlst:
        url += f"&fldlst={fldlst}"
    if codlst0:
        url += f"&codlst0={codlst0}"
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

    for spec in DGBAS_TABLES:
        funid = spec["funid"]
        fields = spec["fields"]
        subdir = spec["subdir"]
        desc = spec["description"]
        outdir = os.path.join(RAW_DIR, subdir)
        os.makedirs(outdir, exist_ok=True)

        print(f"  Fetching {desc} ({funid})...")
        try:
            metadata = fetch_metadata(funid)
            fldlst = make_bitstring(int(metadata["fldCnt"]), list(fields.values()))
            data = fetch_table(funid, fldlst=fldlst, codlst0=spec.get("codlst0", ""))
        except Exception as e:
            print(f"  ✗ {funid}: API returned error ({e})")
            fail += len(fields)
            continue
        if data is None:
            print(f"  ✗ {funid}: API returned empty data")
            fail += len(fields)
            continue

        col_labels = [" / ".join(str(x) for x in col if str(x)) for col in data.get("ncol", [])]
        for col_idx, filename in enumerate(fields):
            df = extract_monthly(data, col_idx)
            if len(df) == 0:
                print(f"  ✗ {filename}: no monthly data found")
                fail += 1
                continue
            if filename == "tw_wpi":
                df.loc[df["Value"] == 0, "Value"] = pd.NA

            path = os.path.join(outdir, f"{filename}_raw.csv")
            df.to_csv(path, index=False)
            label = col_labels[col_idx] if col_idx < len(col_labels) else ""
            print(f"  ✓ {filename}: {len(df)} obs "
                  f"({df['Date'].iloc[0].strftime('%Y-%m')} → "
                  f"{df['Date'].iloc[-1].strftime('%Y-%m')}) {label}")
            ok += 1
        time.sleep(0.5)

    print(f"\nDownloaded {ok} series ({fail} failed)")


if __name__ == "__main__":
    main()

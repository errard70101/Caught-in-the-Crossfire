"""Download monetary/financial data from the CBC (中央銀行) Statistics Database.

Source: https://cpx.cbc.gov.tw/
Uses the PxWeb-style JSON API: GetJsonRangeData → SetJsonFromArray → GetJsonFromArray

Multi-dimensional tables (e.g. 項目 × 資料 × 種類) return flattened columns
as the cross-product of Table1 × Table2 × Table3 ... We build composite column
names and then select the ones we need.
"""

import itertools
import json
import time
import warnings
from pathlib import Path

import pandas as pd
import requests

from config import RAW_TW_FIN, SAMPLE_START_YM, SAMPLE_END_YM

CBC_BASE = "https://cpx.cbc.gov.tw"

# ── Tables and columns to download ───────────────────────────────────────
# "select_cols": dict mapping {output_column_name: composite_key} where
#   composite_key is the "|"-joined cross-product label to keep.
#   For simple (1 extra dim) tables, the key is just the 項目 name.
CBC_DOWNLOADS = [
    # ── Interest Rates ────────────────────────────────────────────────
    {
        "pxfilename": "EG37M01.px",
        "select_cols": {"tw_overnight": "隔夜-加權平均|原始值"},
        "output_name": "tw_overnight_raw.csv",
        "description": "Interbank overnight rate (weighted avg)",
    },
    {
        "pxfilename": "EG2AM01.px",
        "select_cols": {"tw_policy_rate": "重貼現率"},
        "output_name": "tw_policy_rate_raw.csv",
        "description": "CBC rediscount rate",
    },
    {
        "pxfilename": "EG43M01.px",
        "select_cols": {"tw_10y_bond": "十年期政府公債次級市場利率"},
        "output_name": "tw_10y_bond_raw.csv",
        "description": "10-year government bond yield (secondary market)",
    },
    # ── Monetary Aggregates ───────────────────────────────────────────
    # Cross-product columns: Table1(item)|Table2(日平均/期底)|Table3(金額/年增率)
    {
        "pxfilename": "EF01M01.px",
        "select_cols": {
            "tw_m1b": "貨幣總計數-M1B|期底|金額",
            "tw_m2":  "貨幣總計數-M2|期底|金額",
        },
        "output_name": "tw_monetary_raw.csv",
        "description": "M1B and M2 (month-end level, 100M NTD)",
    },
    # ── Loans ─────────────────────────────────────────────────────────
    # Cross-product: Table1(item)|Table2(期底餘額/年增率)
    {
        "pxfilename": "EFA4M01.px",
        "select_cols": {
            "tw_bank_loans_total": "貨幣機構放款與投資(性質別)-合計|期底餘額",
            "tw_bank_loans_private": "主要金融機構放款與投資對象別-對民間部門債權|期底餘額",
        },
        "output_name": "tw_bank_loans_raw.csv",
        "description": "Total bank loans and private-sector loans",
    },
    # Cross-product: Table1(item)|Table2(原始值/年增率)
    {
        "pxfilename": "EF99M01.px",
        "select_cols": {
            "tw_consumer_loans": "消費者貸款-小計|原始值",
            "tw_housing_loans": "消費者貸款-購置住宅貸款|原始值",
        },
        "output_name": "tw_consumer_loans_raw.csv",
        "description": "Consumer and housing loans",
    },
]


def _create_session() -> requests.Session:
    s = requests.Session()
    s.headers.update({
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/131.0.0.0 Safari/537.36"
        ),
    })
    return s


def _build_col_names(header_set: dict) -> list[str]:
    """Build composite column names from the cross-product of Table1×Table2×...

    The CBC API returns data columns as the flattened cross-product of all
    header tables. For a 1-table header, names are just the Table1 values.
    For multi-table headers, names are "val1|val2|val3".
    """
    table_keys = sorted(header_set.keys())  # Table1, Table2, ...
    header_lists = [[h["data"] for h in header_set[k]] for k in table_keys]

    if len(header_lists) == 1:
        return header_lists[0]

    return ["|".join(combo) for combo in itertools.product(*header_lists)]


def fetch_cbc_table(
    session: requests.Session,
    pxfilename: str,
) -> pd.DataFrame:
    """Download one CBC table and return a DataFrame with composite column names.

    The API always returns ALL items regardless of the selection sent in
    SetJsonFromArray, so we request everything and filter later.
    """
    # Step 1: load range page (sets session cookies)
    session.get(f"{CBC_BASE}/Range/RangeSelect?pxfilename={pxfilename}", timeout=30)

    # Step 2: get available dimensions
    r_range = session.post(
        f"{CBC_BASE}/Range/GetJsonRangeData",
        json={"pxfilename": pxfilename},
        headers={"Content-Type": "application/json",
                 "X-Requested-With": "XMLHttpRequest"},
        timeout=30,
    )
    r_range.raise_for_status()
    range_data = r_range.json()

    # Select ALL values for every dimension
    selection_values = [
        {"Key": dim["Key"], "Value": dim["Value"]}
        for dim in range_data["values"]
    ]

    # Step 3: set selection (server-side session)
    r_set = session.post(
        f"{CBC_BASE}/Data/SetJsonFromArray",
        json={"pxfilename": pxfilename, "range": {"values": selection_values}},
        headers={"Content-Type": "application/json",
                 "X-Requested-With": "XMLHttpRequest"},
        timeout=30,
    )
    r_set.raise_for_status()

    # Step 4: visit data page (required to initialize server state)
    session.get(f"{CBC_BASE}/Data/DataMain?pxfilename={pxfilename}", timeout=30)

    # Step 5: get actual data
    r_data = session.post(
        f"{CBC_BASE}/Data/GetJsonFromArray",
        json={"pxfilename": pxfilename},
        headers={"Content-Type": "application/json",
                 "X-Requested-With": "XMLHttpRequest"},
        timeout=30,
    )
    r_data.raise_for_status()

    # Response is double-encoded JSON
    raw = r_data.json()
    data = json.loads(raw) if isinstance(raw, str) else raw

    # Build composite column names from cross-product of header tables
    col_names = _build_col_names(data["headerSet"])
    rows = data["data"]

    df = pd.DataFrame(rows, columns=["period"] + col_names)

    # Convert data columns to numeric
    for col in col_names:
        df[col] = pd.to_numeric(
            df[col].replace({"-": None, "…": None, "..": None}),
            errors="coerce",
        )

    return df


def filter_sample(df: pd.DataFrame) -> pd.DataFrame:
    """Keep only rows within the sample period."""
    start = SAMPLE_START_YM.replace("-", "M")
    end = SAMPLE_END_YM.replace("-", "M")
    return df[(df["period"] >= start) & (df["period"] <= end)].copy()


def period_to_date(period_series: pd.Series) -> pd.Series:
    """Convert CBC period strings like '2001M01' to datetime."""
    return pd.to_datetime(period_series.str.replace("M", "-"), format="%Y-%m")


def main():
    RAW_TW_FIN.mkdir(parents=True, exist_ok=True)

    session = _create_session()
    all_ok = True

    for spec in CBC_DOWNLOADS:
        px = spec["pxfilename"]
        desc = spec["description"]
        out_path = RAW_TW_FIN / spec["output_name"]
        select_cols = spec["select_cols"]

        print(f"\n{'─'*60}")
        print(f"📥 {px}: {desc}")

        try:
            df = fetch_cbc_table(session, px)
            df = filter_sample(df)

            # Select and rename columns
            keep = {"period": "period"}
            for out_name, composite_key in select_cols.items():
                if composite_key not in df.columns:
                    avail = [c for c in df.columns if c != "period"]
                    raise KeyError(
                        f"Column '{composite_key}' not found. "
                        f"Available: {avail[:10]}..."
                    )
                keep[composite_key] = out_name

            df = df[list(keep.keys())].rename(columns=keep)

            # Add proper date column
            df.insert(0, "date", period_to_date(df["period"]))
            df = df.drop(columns=["period"])

            df.to_csv(out_path, index=False)

            n_obs = len(df)
            n_missing = df.iloc[:, 1:].isna().sum().sum()
            date_range = f"{df['date'].min():%Y-%m} to {df['date'].max():%Y-%m}"
            print(f"  ✅ {n_obs} obs ({date_range}), missing cells: {n_missing}")
            print(f"  → {out_path.relative_to(out_path.parents[3])}")

        except Exception as e:
            print(f"  ❌ FAILED: {e}")
            all_ok = False

        # Polite delay between requests
        time.sleep(1.0)

    print(f"\n{'='*60}")
    if all_ok:
        print("✅ All CBC downloads completed successfully.")
    else:
        print("⚠️  Some CBC downloads failed. Check output above.")


if __name__ == "__main__":
    warnings.filterwarnings("ignore", message=".*Unverified HTTPS.*")
    main()

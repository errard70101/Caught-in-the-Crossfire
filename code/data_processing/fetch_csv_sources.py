#!/usr/bin/env python3
"""Download CSV/XLSX sources: US EPU, Global EPU, GPR, BBD Trade Policy Uncertainty."""

from __future__ import annotations

from pathlib import Path
from io import BytesIO

import pandas as pd
import requests

from config import RAW_US, RAW_GL, SAMPLE_START_YM, SAMPLE_END_YM

SOURCES = {
    "us_epu": {
        "url": "https://www.policyuncertainty.com/media/US_Policy_Uncertainty_Data.csv",
        "dest": RAW_US,
        "parser": "epu_csv",
    },
    "gl_gepu": {
        "url": "https://www.policyuncertainty.com/media/Global_Policy_Uncertainty_Data.csv",
        "dest": RAW_GL,
        "parser": "gepu_csv",
    },
    "gl_gpr": {
        "url": "https://www.matteoiacoviello.com/gpr_files/data_gpr_export.xls",
        "dest": RAW_GL,
        "parser": "gpr_xls",
    },
    "us_tpu": {
        "url": "https://www.policyuncertainty.com/media/Categorical_EPU_Data.xlsx",
        "dest": RAW_US,
        "parser": "bbd_categorical",
    },
}


def _make_monthly_date(year: int, month: int) -> str:
    return f"{year:04d}-{month:02d}"


def parse_epu_csv(content: bytes, name: str) -> pd.DataFrame:
    """Parse Baker-Bloom-Davis US EPU CSV."""
    df = pd.read_csv(BytesIO(content))
    cols = [c.strip() for c in df.columns]
    df.columns = cols
    df = df.rename(columns={"Year": "year", "Month": "month"})
    # The EPU column name varies; pick the one containing "EPU" or the 3rd column
    epu_col = [c for c in df.columns if "news" in c.lower() or "epu" in c.lower()]
    if epu_col:
        val_col = epu_col[0]
    else:
        val_col = df.columns[2]
    df["date"] = df.apply(lambda r: _make_monthly_date(int(r["year"]), int(r["month"])), axis=1)
    df[name] = pd.to_numeric(df[val_col], errors="coerce")
    out = df[["date", name]].dropna()
    out = out[(out["date"] >= SAMPLE_START_YM) & (out["date"] <= SAMPLE_END_YM)]
    return out.reset_index(drop=True)


def parse_gepu_csv(content: bytes, name: str) -> pd.DataFrame:
    """Parse Global EPU CSV."""
    df = pd.read_csv(BytesIO(content))
    cols = [c.strip() for c in df.columns]
    df.columns = cols
    df = df.rename(columns={"Year": "year", "Month": "month"})
    gepu_col = [c for c in df.columns if "gepu" in c.lower() or "global" in c.lower()]
    val_col = gepu_col[0] if gepu_col else df.columns[2]
    df["date"] = df.apply(lambda r: _make_monthly_date(int(r["year"]), int(r["month"])), axis=1)
    df[name] = pd.to_numeric(df[val_col], errors="coerce")
    out = df[["date", name]].dropna()
    out = out[(out["date"] >= SAMPLE_START_YM) & (out["date"] <= SAMPLE_END_YM)]
    return out.reset_index(drop=True)


def parse_gpr_xls(content: bytes, name: str) -> pd.DataFrame:
    """Parse Iacoviello GPR Excel file."""
    df = pd.read_excel(BytesIO(content))
    cols = [c.strip() for c in df.columns]
    df.columns = cols
    # Find the date and GPR columns
    date_col = [c for c in df.columns if "date" in c.lower() or "month" in c.lower()]
    gpr_col = [c for c in df.columns if c.upper() == "GPR" or c.upper() == "GPRD"]
    if not gpr_col:
        gpr_col = [c for c in df.columns if "gpr" in c.lower()]
    if date_col:
        df["date_raw"] = pd.to_datetime(df[date_col[0]])
    else:
        df["date_raw"] = pd.to_datetime(df.iloc[:, 0])
    df["date"] = df["date_raw"].dt.strftime("%Y-%m")
    val_col = gpr_col[0] if gpr_col else df.columns[1]
    df[name] = pd.to_numeric(df[val_col], errors="coerce")
    out = df[["date", name]].dropna()
    out = out[(out["date"] >= SAMPLE_START_YM) & (out["date"] <= SAMPLE_END_YM)]
    return out.reset_index(drop=True)


def parse_bbd_categorical(content: bytes, name: str) -> pd.DataFrame:
    """Parse BBD Categorical EPU xlsx — extract Trade Policy column (#9)."""
    df = pd.read_excel(BytesIO(content))
    cols = [c.strip() for c in df.columns]
    df.columns = cols
    # Drop footer rows where Year is not numeric
    df = df[pd.to_numeric(df["Year"], errors="coerce").notna()].copy()
    df = df.rename(columns={"Year": "year", "Month": "month"})
    trade_col = [c for c in df.columns if "trade" in c.lower()]
    if trade_col:
        val_col = trade_col[0]
    else:
        val_col = df.columns[9]
    df["date"] = df.apply(lambda r: _make_monthly_date(int(float(r["year"])), int(float(r["month"]))), axis=1)
    df[name] = pd.to_numeric(df[val_col], errors="coerce")
    out = df[["date", name]].dropna()
    out = out[(out["date"] >= SAMPLE_START_YM) & (out["date"] <= SAMPLE_END_YM)]
    return out.reset_index(drop=True)


PARSER_MAP = {
    "epu_csv": parse_epu_csv,
    "gepu_csv": parse_gepu_csv,
    "gpr_xls": parse_gpr_xls,
    "bbd_categorical": parse_bbd_categorical,
}


def download_and_parse(name: str, info: dict) -> Path | None:
    dest_dir: Path = info["dest"]
    dest_dir.mkdir(parents=True, exist_ok=True)
    out_path = dest_dir / f"{name}_raw.csv"

    print(f"  Downloading {name}...", end=" ")
    resp = requests.get(info["url"], timeout=60)
    resp.raise_for_status()

    parser = PARSER_MAP[info["parser"]]
    df = parser(resp.content, name)
    df.to_csv(out_path, index=False)
    print(f"{len(df)} observations, {df['date'].iloc[0]} to {df['date'].iloc[-1]}")
    return out_path


def main() -> None:
    print("=" * 60)
    print("CSV/XLSX Source Download")
    print("=" * 60)

    for name, info in SOURCES.items():
        try:
            download_and_parse(name, info)
        except Exception as e:
            print(f"  ERROR: {name}: {e}")

    print("\nDone.")


if __name__ == "__main__":
    main()

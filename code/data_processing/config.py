"""Shared configuration for the OI-SVMVAR data pipeline."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT / "data" / "raw"
CLEANED_DIR = ROOT / "data" / "cleaned"
FINAL_DIR = ROOT / "data" / "final"

RAW_TW_MACRO = RAW_DIR / "taiwan_macro"
RAW_TW_FIN = RAW_DIR / "taiwan_financial"
RAW_TW_POL = RAW_DIR / "taiwan_policy"
RAW_US = RAW_DIR / "us"
RAW_CN = RAW_DIR / "china"
RAW_GL = RAW_DIR / "global"

SAMPLE_START = "2001-01-01"
SAMPLE_END = "2025-12-31"
SAMPLE_START_YM = "2001-01"
SAMPLE_END_YM = "2025-12"

# DGBAS API
DGBAS_BASE = "https://nstatdb.dgbas.gov.tw/dgbasAll/webMain.aspx"
DGBAS_START_YM = 9001   # 民國90年1月 = 2001-01
DGBAS_END_YM = 11412    # 民國114年12月 = 2025-12

# FRED series to download (no API key needed via CSV endpoint)
FRED_SERIES = {
    # US variables
    "us_ffr": "FEDFUNDS",
    "us_ipi": "INDPRO",
    "us_credit_spread": "BAA10YM",
    # Global
    "gl_vix": "VIXCLS",
    # Taiwan exchange rate (daily → monthly avg in processing)
    "tw_twdusd": "DEXTAUS",
}

# China variables — NOT available on FRED with current data.
# cn_ipi, cn_ppi, cn_m2 require manual download from NBS/CEIC.
# Placeholder for future automation.
CHINA_MANUAL_VARS = ["cn_ipi", "cn_ppi", "cn_m2"]

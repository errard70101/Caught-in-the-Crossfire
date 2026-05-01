#!/usr/bin/env python3
"""Build an inventory of planned model variables and raw-data coverage."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from config import RAW_DIR


BASELINE_START = "2003-01"
BASELINE_END = "2025-12"
ROBUSTNESS_START = "2001-01"


def model_variables() -> list[dict[str, str]]:
    """Return the planned variable inventory specification."""
    return [
        # Macro, fixed classification
        row("macro", "tw_ipi", "Industrial Production Index", "DGBAS", "taiwan_macro/tw_ipi_raw.csv", "Value", "baseline"),
        row("macro", "tw_mfg_prod", "Manufacturing Production Index", "DGBAS", "taiwan_macro/tw_mfg_prod_raw.csv", "Value", "baseline"),
        row("macro", "tw_export_orders", "Export Orders Index", "MOEA", "taiwan_macro/tw_export_orders_raw.csv", "Value", "baseline"),
        row("macro", "tw_retail", "Retail Sales (real)", "DGBAS", "taiwan_macro/tw_retail_growth_raw.csv", "Value", "baseline"),
        row("macro", "tw_food_svc", "Food and Beverage Services Sales (real)", "DGBAS", "taiwan_macro/tw_food_svc_raw.csv", "Value", "baseline"),
        row("macro", "tw_exports_usd", "Exports (customs, real USD)", "MOF/DGBAS", "taiwan_macro/tw_exports_raw.csv", "Value", "baseline"),
        row("macro", "tw_imports_usd", "Imports (customs, real USD)", "MOF/DGBAS", "taiwan_macro/tw_imports_raw.csv", "Value", "baseline"),
        row("macro", "tw_business_cycle", "Business Cycle Indicator", "NDC/stat.gov.tw", "taiwan_macro/tw_business_cycle_raw.csv", "Value", "baseline"),
        row("macro", "tw_cpi", "CPI (YoY)", "DGBAS", "taiwan_macro/tw_cpi_yoy_raw.csv", "Value", "baseline"),
        row("macro", "tw_core_cpi", "Core CPI (YoY)", "DGBAS", "taiwan_macro/tw_core_cpi_yoy_raw.csv", "Value", "baseline"),
        row("macro", "tw_upstream_prices", "WPI/PPI-Spliced Upstream Price Index (YoY)", "Authors' construction from DGBAS WPI and PPI", "taiwan_macro/tw_upstream_prices_raw.csv", "tw_upstream_prices_yoy", "baseline", "available", "Uses WPI through the 2021-01--2022-12 overlap and PPI adjusted to the WPI level from 2023-01 onward."),
        row("macro", "tw_import_prices", "Import Price Index (YoY)", "DGBAS", "taiwan_macro/tw_import_prices_raw.csv", "Value", "baseline"),
        row("macro", "tw_export_prices", "Export Price Index (YoY)", "DGBAS", "taiwan_macro/tw_export_prices_raw.csv", "Value", "baseline"),
        row("macro", "tw_unemp", "Unemployment Rate (SA)", "DGBAS", "taiwan_macro/tw_unemployment_sa_raw.csv", "Value", "baseline"),
        row("macro", "tw_mfg_emp", "Manufacturing Employment (SA)", "DGBAS", "taiwan_macro/tw_mfg_emp_raw.csv", "Value", "baseline"),
        row("macro", "tw_svc_emp", "Services Employment (SA)", "DGBAS", "taiwan_macro/tw_svc_emp_raw.csv", "Value", "baseline"),
        row("macro", "tw_mfg_wages", "Real Manufacturing Regular Wages (YoY)", "DGBAS A046301010 + CPI", "taiwan_macro/tw_real_wages_raw.csv", "tw_mfg_wages", "baseline", "available", "Nominal manufacturing regular monthly earnings deflated by CPI and transformed to YoY growth; total earnings retained in the same raw file for robustness."),
        row("macro", "tw_svc_wages", "Real Services Regular Wages (YoY)", "DGBAS A046301010 + CPI", "taiwan_macro/tw_real_wages_raw.csv", "tw_svc_wages", "baseline", "available", "Nominal services regular monthly earnings deflated by CPI and transformed to YoY growth; total earnings retained in the same raw file for robustness."),
        row("macro", "tw_mfg_hours", "Manufacturing Hours per Employee", "DGBAS A046401010", "taiwan_macro/tw_mfg_hours_raw.csv", "Value", "baseline"),
        row("macro", "tw_svc_hours", "Services Hours per Employee", "DGBAS A046401010", "taiwan_macro/tw_svc_hours_raw.csv", "Value", "baseline"),
        row("macro", "tw_building_permits_residential_area", "Residential Building Permit Floor Area", "DGBAS A060101010", "taiwan_macro/tw_building_permits_residential_area_raw.csv", "Value", "baseline", "available", "Residential H-2 floor area from building permits; Taiwan counterpart to DHK housing permits."),
        row("macro", "tw_use_permits_residential_area", "Residential Use Permit Floor Area", "DGBAS A060103010", "taiwan_macro/tw_use_permits_residential_area_raw.csv", "Value", "baseline", "available", "Residential H-2 floor area from use/occupancy permits; Taiwan counterpart to DHK housing starts/completions."),
        # Financial, fixed classification
        row("financial", "tw_overnight", "Overnight Interbank Rate", "CBC", "taiwan_financial/tw_overnight_raw.csv", "tw_overnight", "baseline"),
        row("financial", "tw_10y_bond", "10-Year Government Bond Yield", "CBC", "taiwan_financial/tw_10y_bond_raw.csv", "tw_10y_bond", "baseline"),
        row("financial", "tw_term_spread", "Term Spread (10-year minus overnight)", "Computed", "", "", "baseline", "computed", "Compute from tw_10y_bond - tw_overnight."),
        row("financial", "tw_taiex_ret", "TAIEX Monthly Return", "TWSE MFI94U", "taiwan_financial/taiex_raw.csv", "tw_taiex_ret", "baseline", "available", "Baseline total-return monthly return starts in 2003M2.", baseline_start="2003-02"),
        row("financial", "tw_taiex_vol", "TAIEX Monthly Realized Volatility", "TWSE MFI94U", "taiwan_financial/taiex_raw.csv", "tw_taiex_vol", "baseline"),
        row("financial", "tw_turnover", "TAIEX Average Daily Turnover", "TWSE FMTQIK", "taiwan_financial/taiex_raw.csv", "tw_turnover", "baseline"),
        row("financial", "tw_foreign_inv", "Foreign Institutional Net Buying", "TWSE BFI82U", "taiwan_financial/twse_foreign_investor_monthly_raw.csv", "tw_foreign_inv", "baseline", "available", "Official TWSE BFI82U monthly aggregate starts in 2004M4."),
        row("financial", "tw_margin_buy", "Margin Buying Balance (YoY)", "TWSE MI_MARGN", "taiwan_financial/twse_margin_short_monthly_raw.csv", "tw_margin_buy", "baseline"),
        # Unclassified: Taiwan ambiguous
        row("unclassified", "tw_policy_rate", "CBC Discount Rate", "CBC", "taiwan_financial/tw_policy_rate_raw.csv", "tw_policy_rate", "baseline"),
        row("unclassified", "tw_m1b", "M1B Money Supply", "CBC", "taiwan_financial/tw_monetary_raw.csv", "tw_m1b", "baseline"),
        row("unclassified", "tw_m2", "M2 Money Supply", "CBC", "taiwan_financial/tw_monetary_raw.csv", "tw_m2", "baseline"),
        row("unclassified", "tw_bank_loans", "Bank Loans and Investments", "CBC", "taiwan_financial/tw_bank_loans_raw.csv", "tw_bank_loans_total", "baseline"),
        row("unclassified", "tw_consumer_loans", "Consumer Loans", "CBC", "taiwan_financial/tw_consumer_loans_raw.csv", "tw_consumer_loans", "baseline"),
        row("unclassified", "tw_taiex_level", "TAIEX Level (log)", "TWSE MI_5MINS_HIST", "taiwan_financial/taiex_raw.csv", "tw_taiex_level", "baseline"),
        row("unclassified", "tw_house_prices", "Housing Price Index", "Sinyi", "taiwan_financial/tw_house_prices_raw.csv", "tw_house_prices", "baseline", "available", "Baseline placeholder uses Sinyi Taiwan aggregate repeated within quarter. Additional candidates are saved in tw_house_sinyi_quarterly_raw.csv and tw_house_taipei_monthly_raw.csv."),
        # Unclassified: Taiwan exchange-rate / market funding
        row("unclassified", "tw_twdusd", "NTD/USD Exchange Rate", "FRED/CBC", "taiwan_financial/tw_twdusd_raw.csv", "tw_twdusd", "baseline"),
        row("unclassified", "tw_fx_vol", "NTD/USD Realized Volatility", "FRED", "taiwan_financial/tw_fx_vol_raw.csv", "tw_fx_vol", "baseline", "available", "Constructed from FRED DEXTAUS daily log returns; daily raw file saved as tw_twdusd_daily_raw.csv."),
        row("unclassified", "tw_reer", "Real Effective Exchange Rate", "BIS", "global/tw_reer_raw.csv", "Value", "baseline"),
        row("unclassified", "tw_short_sell", "Short Selling Balance (YoY)", "TWSE MI_MARGN", "taiwan_financial/twse_margin_short_monthly_raw.csv", "tw_short_sell", "baseline"),
        # Unclassified: US
        row("unclassified", "us_ffr", "Federal Funds Rate", "FRED", "us/us_ffr_raw.csv", "us_ffr", "baseline"),
        row("unclassified", "us_ipi", "U.S. Industrial Production", "FRED", "us/us_ipi_raw.csv", "us_ipi", "baseline"),
        row("unclassified", "us_credit_spread", "U.S. Credit Spread", "FRED", "us/us_credit_spread_raw.csv", "us_credit_spread", "baseline"),
        row("unclassified", "us_epu", "U.S. Economic Policy Uncertainty", "PolicyUncertainty.com", "us/us_epu_raw.csv", "us_epu", "baseline"),
        # Unclassified: China
        row("unclassified", "cn_ipi", "China Industrial Production", "NBS via Trading Economics", "china/cn_ipi_raw.csv", "cn_ipi", "baseline", "available", "January values missing from NBS releases are filled with the same year's February Jan-Feb YoY value and flagged in is_imputed."),
        row("unclassified", "cn_ppi", "China Producer Price Index", "NBS via Trading Economics", "china/cn_ppi_raw.csv", "cn_ppi", "baseline"),
        row("unclassified", "cn_m2", "China M2 Money Supply", "PBoC via Trading Economics", "china/cn_m2_raw.csv", "cn_m2", "baseline", "available", "Level series in CNY billion; transform to YoY growth during dataset construction."),
        # Unclassified: global/risk
        row("unclassified", "gl_vix", "VIX", "FRED", "global/gl_vix_raw.csv", "gl_vix", "baseline"),
        row("unclassified", "gl_gpr", "Global Geopolitical Risk", "Iacoviello", "global/gl_gpr_raw.csv", "gl_gpr", "baseline"),
        row("unclassified", "gl_gepu", "Global Economic Policy Uncertainty", "PolicyUncertainty.com", "global/gl_gepu_raw.csv", "gl_gepu", "baseline"),
        row("unclassified", "us_tpu", "U.S. Trade Policy Uncertainty", "PolicyUncertainty.com", "us/us_tpu_raw.csv", "us_tpu", "baseline"),
        # Auxiliary/robustness TAIEX rows
        row("auxiliary", "tw_taiex_price_ret", "TAIEX Price-Index Monthly Return", "TWSE MI_5MINS_HIST", "taiwan_financial/taiex_raw.csv", "tw_taiex_price_ret", "robustness"),
        row("auxiliary", "tw_taiex_price_vol", "TAIEX Price-Index Monthly Volatility", "TWSE MI_5MINS_HIST", "taiwan_financial/taiex_raw.csv", "tw_taiex_price_vol", "robustness"),
        row("auxiliary", "tw_trade_volume", "TWSE Average Daily Trade Volume", "TWSE FMTQIK", "taiwan_financial/taiex_raw.csv", "tw_trade_volume", "diagnostic"),
        row("auxiliary", "tw_transactions", "TWSE Average Daily Transactions", "TWSE FMTQIK", "taiwan_financial/taiex_raw.csv", "tw_transactions", "diagnostic"),
        row("auxiliary", "tw_ppi_index", "Producer Price Index", "DGBAS/stat.gov.tw", "taiwan_macro/tw_ppi_index_raw.csv", "Value", "diagnostic"),
        row("auxiliary", "tw_ppi_yoy", "Producer Price Index YoY", "DGBAS/stat.gov.tw", "taiwan_macro/tw_ppi_yoy_raw.csv", "Value", "diagnostic"),
        row("auxiliary", "tw_building_permits_area", "Total Building Permit Floor Area", "DGBAS A060101010", "taiwan_macro/tw_building_permits_area_raw.csv", "Value", "robustness", "available", "Total floor area by use; residential H-2 series is the baseline candidate."),
        row("auxiliary", "tw_use_permits_area", "Total Use Permit Floor Area", "DGBAS A060103010", "taiwan_macro/tw_use_permits_area_raw.csv", "Value", "robustness", "available", "Total floor area by use; residential H-2 series is the baseline candidate."),
        row("auxiliary", "tw_building_permits_structure_area", "Total Building Permit Floor Area by Structure", "DGBAS A060102010", "taiwan_macro/tw_building_permits_structure_area_raw.csv", "Value", "diagnostic", "available", "Same total building permit floor-area concept from the structure table; starts in 2002M1."),
        row("auxiliary", "tw_building_permits_value", "Building Permit Construction Value", "DGBAS A060102010", "taiwan_macro/tw_building_permits_value_raw.csv", "Value", "robustness", "available", "Engineering/construction value in NTD thousand; use cautiously because it mixes quantity and price effects."),
    ]


def row(
    classification: str,
    variable: str,
    label: str,
    source: str,
    raw_file: str,
    raw_column: str,
    role: str,
    status: str = "available",
    notes: str = "",
    baseline_start: str = "",
) -> dict[str, str]:
    return {
        "classification": classification,
        "variable": variable,
        "label": label,
        "source": source,
        "raw_file": raw_file,
        "raw_column": raw_column,
        "role": role,
        "status": status,
        "notes": notes,
        "baseline_start": baseline_start,
    }


def normalize_date_series(values: pd.Series) -> pd.PeriodIndex:
    """Convert common raw date formats to monthly PeriodIndex."""
    text = values.astype(str)
    if text.str.match(r"^\d{4}-\d{2}$").all():
        return pd.PeriodIndex(text, freq="M")
    dates = pd.to_datetime(text, errors="coerce")
    return dates.dt.to_period("M")


def coverage_for(raw_file: str, raw_column: str, start: str, end: str) -> dict[str, object]:
    path = RAW_DIR / raw_file
    if not raw_file or not raw_column:
        return empty_coverage()
    if not path.exists():
        out = empty_coverage()
        out["status_override"] = "missing_file"
        return out

    df = pd.read_csv(path)
    date_col = "date" if "date" in df.columns else "Date" if "Date" in df.columns else None
    if date_col is None or raw_column not in df.columns:
        out = empty_coverage()
        out["status_override"] = "bad_schema"
        return out

    periods = normalize_date_series(df[date_col])
    values = pd.to_numeric(df[raw_column], errors="coerce")
    valid = periods.notna()
    periods = periods[valid]
    values = values[valid]
    baseline = (periods >= pd.Period(start, "M")) & (periods <= pd.Period(end, "M"))
    expected = pd.period_range(start=start, end=end, freq="M")
    observed = pd.PeriodIndex(periods[baseline & values.notna()].drop_duplicates(), freq="M")
    missing_months = expected.difference(observed)

    return {
        "first_date": str(periods.min()) if len(periods) else "",
        "last_date": str(periods.max()) if len(periods) else "",
        "n_rows": int(len(df)),
        "n_nonmissing": int(values.notna().sum()),
        "baseline_window": f"{start}--{end}",
        "baseline_expected_months": int(len(expected)),
        "baseline_observed_months": int(len(observed)),
        "baseline_missing_months": int(len(missing_months)),
        "missing_month_examples": ";".join(str(x) for x in missing_months[:12]),
    }


def empty_coverage() -> dict[str, object]:
    return {
        "first_date": "",
        "last_date": "",
        "n_rows": "",
        "n_nonmissing": "",
        "baseline_window": f"{BASELINE_START}--{BASELINE_END}",
        "baseline_expected_months": "",
        "baseline_observed_months": "",
        "baseline_missing_months": "",
        "missing_month_examples": "",
    }


def main() -> None:
    rows = []
    for spec in model_variables():
        start = spec.get("baseline_start") or (ROBUSTNESS_START if spec["role"] == "robustness" else BASELINE_START)
        coverage = coverage_for(spec["raw_file"], spec["raw_column"], start, BASELINE_END)
        status = coverage.pop("status_override", spec["status"])
        if status == "available" and coverage.get("baseline_missing_months") not in ("", 0):
            status = "available_with_gaps"
        rows.append({**spec, "status": status, **coverage})

    out = RAW_DIR / "raw_data_inventory.csv"
    pd.DataFrame(rows).to_csv(out, index=False)
    print(f"Saved {out} ({len(rows)} rows)")


if __name__ == "__main__":
    main()

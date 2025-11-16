#!/usr/bin/env python3
"""
Download FRED-MD Dataset

Purpose: Download monthly FRED-MD dataset (1960-2021) for DHK replication
Reference: DHK (2025) - Section 4, Online Appendix B
Author: Claude Code
Date: 2025-11-16

Usage:
    python 01_download_fredmd.py
"""

import pandas as pd
import numpy as np
import requests
from pathlib import Path
from datetime import datetime

# Configuration
FRED_MD_URL = "https://files.stlouisfed.org/files/htdocs/fred-md/monthly/current.csv"
DATA_RAW_DIR = Path(__file__).parent.parent.parent.parent / "data" / "raw"
DATA_PROCESSED_DIR = Path(__file__).parent.parent.parent.parent / "data" / "processed"

# Date range for replication (matching DHK 2025)
START_DATE = "1960-01-01"
END_DATE = "2021-10-31"


def download_fredmd(url=FRED_MD_URL, save_path=None):
    """
    Download FRED-MD dataset from St. Louis Fed

    Parameters
    ----------
    url : str
        URL to FRED-MD current dataset
    save_path : str or Path, optional
        Where to save raw data. If None, saves to data/raw/fredmd_raw.csv

    Returns
    -------
    pd.DataFrame
        Raw FRED-MD dataset
    """
    print(f"Downloading FRED-MD dataset from: {url}")

    try:
        # Download data
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        # Save raw data
        if save_path is None:
            save_path = DATA_RAW_DIR / "fredmd_raw.csv"

        save_path.parent.mkdir(parents=True, exist_ok=True)

        with open(save_path, 'wb') as f:
            f.write(response.content)

        print(f"✓ Downloaded and saved to: {save_path}")

        # Read and return
        df = pd.read_csv(save_path)

        # Log download metadata
        metadata = {
            'download_date': datetime.now().isoformat(),
            'source_url': url,
            'rows': len(df),
            'columns': len(df.columns)
        }

        metadata_path = save_path.parent / "fredmd_download_metadata.txt"
        with open(metadata_path, 'w') as f:
            for key, value in metadata.items():
                f.write(f"{key}: {value}\n")

        print(f"✓ Metadata saved to: {metadata_path}")

        return df

    except requests.exceptions.RequestException as e:
        print(f"✗ Error downloading FRED-MD: {e}")
        print("\nAlternative: Download manually from:")
        print("https://research.stlouisfed.org/econ/mccracken/fred-databases/")
        raise


def extract_date_range(df, start_date=START_DATE, end_date=END_DATE):
    """
    Extract subset of FRED-MD for specified date range

    Parameters
    ----------
    df : pd.DataFrame
        Full FRED-MD dataset
    start_date : str
        Start date (YYYY-MM-DD)
    end_date : str
        End date (YYYY-MM-DD)

    Returns
    -------
    pd.DataFrame
        Subset of data for specified period
    """
    # FRED-MD has format: sasdate column with dates
    # First row is transformation codes, skip it

    # Read with proper handling
    # Row 0: transformation codes
    # Row 1+: data

    print(f"\nExtracting date range: {start_date} to {end_date}")

    # Parse date column (usually called 'sasdate' in FRED-MD)
    date_col = df.columns[0]  # First column is typically the date

    # Skip first row (transformation codes) when working with data
    df_data = df.iloc[1:].copy()

    # Convert to datetime
    df_data[date_col] = pd.to_datetime(df_data[date_col])

    # Filter date range
    mask = (df_data[date_col] >= start_date) & (df_data[date_col] <= end_date)
    df_subset = df_data[mask].copy()

    print(f"✓ Extracted {len(df_subset)} observations")
    print(f"  Date range: {df_subset[date_col].min()} to {df_subset[date_col].max()}")

    return df_subset


def get_variable_list_43var():
    """
    Get list of 43 variables used in DHK (2025) OI-TVC-43 model

    Based on Online Appendix B of DHK (2025)

    Returns
    -------
    dict
        Dictionary with keys: 'macro', 'financial', 'unclassified'
        Each containing list of variable names
    """
    # NOTE: These need to be verified against Online Appendix B
    # This is a preliminary list based on common FRED-MD variables

    variable_classification = {
        'macro': [
            'RPI',          # Real Personal Income
            'W875RX1',      # Real personal income ex transfers
            'INDPRO',       # IP Index
            'IPFPNSS',      # IP: Final Products
            'IPFINAL',      # IP: Final Products (Market Group)
            'IPCONGD',      # IP: Consumer Goods
            'IPDCONGD',     # IP: Durable Consumer Goods
            'IPNCONGD',     # IP: Nondurable Consumer Goods
            'IPBUSEQ',      # IP: Business Equipment
            'IPMAT',        # IP: Materials
            'IPDMAT',       # IP: Durable Materials
            'IPNMAT',       # IP: Nondurable Materials
            'CUMFNS',       # Capacity Utilization: Manufacturing
            'PAYEMS',       # All Employees: Total nonfarm
            'USGOOD',       # All Employees: Goods-Producing
            'UNRATE',       # Unemployment Rate
            'CLAIMSx',      # Initial Claims (transformed)
            'HOUST',        # Housing Starts
        ],

        'financial': [
            'TB3MS',        # 3-Month Treasury Bill
            'GS10',         # 10-Year Treasury Rate
            'BAA',          # Moody's Baa Corporate Bond Yield
            'COMPAPFFx',    # Commercial Paper - Fed Funds spread
            'TB3SMFFM',     # 3-Month T-Bill - Fed Funds
            'TB6SMFFM',     # 6-Month T-Bill - Fed Funds
            'T1YFFM',       # 1-Year T-Bill - Fed Funds
            'T5YFFM',       # 5-Year T-Note - Fed Funds
            'T10YFFM',      # 10-Year T-Note - Fed Funds
            'AAAxTREAS',    # Aaa Corporate - 10Y Treasury spread
            'BAAxTREAS',    # Baa Corporate - 10Y Treasury spread
            'S&P 500',      # S&P 500 Index
        ],

        'unclassified': [
            'FEDFUNDS',     # Federal Funds Rate (CRITICAL!)
            'S&P div yield',# S&P 500 Dividend Yield
            'S&P PE ratio', # S&P 500 Price-Earnings Ratio
            'M1REAL',       # Real M1 Money Stock
            'M2REAL',       # Real M2 Money Stock
            'TOTRESNS',     # Total Reserves of Depository Institutions
            'NONREVSL',     # Total Nonrevolving Credit
            'CONSPI',       # Nonrevolving consumer credit to Personal Income
            'BUSLOANS',     # Commercial and Industrial Loans
            'REALLN',       # Real Estate Loans
            'NONBORRES',    # Reserves of Depository Institutions
            'EXSZUSx',      # Switzerland / U.S. Foreign Exchange Rate
            'EXJPUSx',      # Japan / U.S. Foreign Exchange Rate
        ]
    }

    print("\n" + "="*60)
    print("IMPORTANT NOTE:")
    print("="*60)
    print("This variable list is PRELIMINARY and needs verification")
    print("against DHK (2025) Online Appendix B.")
    print("\nPlease verify:")
    print("1. Exact variable names in FRED-MD")
    print("2. Classification (macro/financial/unclassified)")
    print("3. Total count should be 43 variables")
    print(f"\nCurrent count: {sum(len(v) for v in variable_classification.values())} variables")
    print("="*60 + "\n")

    return variable_classification


def save_variable_classification(classification, save_path=None):
    """
    Save variable classification to CSV

    Parameters
    ----------
    classification : dict
        Variable classification dictionary
    save_path : str or Path, optional
        Where to save. If None, saves to data/processed/classification_scheme.csv
    """
    if save_path is None:
        save_path = DATA_PROCESSED_DIR / "classification_scheme.csv"

    save_path.parent.mkdir(parents=True, exist_ok=True)

    # Convert to DataFrame
    rows = []
    for category, variables in classification.items():
        for var in variables:
            rows.append({'variable': var, 'classification': category})

    df = pd.DataFrame(rows)
    df.to_csv(save_path, index=False)

    print(f"✓ Variable classification saved to: {save_path}")

    return df


def main():
    """Main execution function"""
    print("="*70)
    print("DHK (2025) Replication - Module 1: Data Collection")
    print("Task DHK-M1-001: Download FRED-MD Dataset")
    print("="*70)

    # Step 1: Download FRED-MD
    print("\n[Step 1/3] Downloading FRED-MD dataset...")
    df_raw = download_fredmd()

    # Step 2: Extract date range
    print("\n[Step 2/3] Extracting date range (1960-2021)...")
    df_subset = extract_date_range(df_raw)

    # Save subset
    subset_path = DATA_RAW_DIR / "fredmd_1960_2021.csv"
    df_subset.to_csv(subset_path, index=False)
    print(f"✓ Saved subset to: {subset_path}")

    # Step 3: Create variable list
    print("\n[Step 3/3] Creating variable classification...")
    classification = get_variable_list_43var()
    classification_df = save_variable_classification(classification)

    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"Total observations: {len(df_subset)}")
    print(f"Date range: {START_DATE} to {END_DATE}")
    print(f"\nVariable counts:")
    print(f"  Macro: {len(classification['macro'])}")
    print(f"  Financial: {len(classification['financial'])}")
    print(f"  Unclassified: {len(classification['unclassified'])}")
    print(f"  Total: {sum(len(v) for v in classification.values())}")

    print("\n⚠️  NEXT STEPS:")
    print("1. Verify variable list against DHK (2025) Online Appendix B")
    print("2. Check that all 43 variables are present in FRED-MD")
    print("3. Proceed to Task DHK-M1-002: Data transformation")
    print("="*70)


if __name__ == "__main__":
    main()

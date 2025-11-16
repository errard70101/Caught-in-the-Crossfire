#!/usr/bin/env python3
"""
Transform and Standardize FRED-MD Data

Purpose: Apply transformation codes and standardize variables for DHK replication
Reference: DHK (2025) - Section 4, FRED-MD documentation
Author: Claude Code
Date: 2025-11-16

Transformation codes (from FRED-MD):
    1: No transformation
    2: First difference: x(t) - x(t-1)
    3: Second difference: (x(t) - x(t-1)) - (x(t-1) - x(t-2))
    4: Log: log(x)
    5: First difference of log: log(x(t)) - log(x(t-1))
    6: Second difference of log
    7: First difference of percent change

Usage:
    python 02_transform_data.py
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json

# Configuration
DATA_RAW_DIR = Path(__file__).parent.parent.parent.parent / "data" / "raw"
DATA_PROCESSED_DIR = Path(__file__).parent.parent.parent.parent / "data" / "processed"


def apply_transformation(series, tcode):
    """
    Apply FRED-MD transformation code to a series

    Parameters
    ----------
    series : pd.Series
        Input time series
    tcode : int
        Transformation code (1-7)

    Returns
    -------
    pd.Series
        Transformed series
    """
    x = series.copy()

    if tcode == 1:  # No transformation
        return x

    elif tcode == 2:  # First difference
        return x.diff()

    elif tcode == 3:  # Second difference
        return x.diff().diff()

    elif tcode == 4:  # Log
        return np.log(x)

    elif tcode == 5:  # First difference of log (log returns)
        return np.log(x).diff()

    elif tcode == 6:  # Second difference of log
        return np.log(x).diff().diff()

    elif tcode == 7:  # First difference of percent change
        pct_change = (x / x.shift(1) - 1) * 100
        return pct_change.diff()

    else:
        raise ValueError(f"Unknown transformation code: {tcode}")


def get_transformation_codes(df_raw):
    """
    Extract transformation codes from FRED-MD dataset

    FRED-MD format:
    - Row 0: Transformation codes
    - Row 1+: Data

    Parameters
    ----------
    df_raw : pd.DataFrame
        Raw FRED-MD dataset

    Returns
    -------
    dict
        Dictionary mapping variable names to transformation codes
    """
    # First row contains transformation codes
    tcodes_row = df_raw.iloc[0]

    # Create dictionary (skip date column)
    tcodes = {}
    for col in df_raw.columns[1:]:  # Skip first column (date)
        try:
            tcodes[col] = int(tcodes_row[col])
        except (ValueError, TypeError):
            print(f"⚠️  Warning: Could not parse tcode for {col}, defaulting to 1")
            tcodes[col] = 1

    return tcodes


def transform_dataset(df, tcodes, verbose=True):
    """
    Apply transformations to entire dataset

    Parameters
    ----------
    df : pd.DataFrame
        Raw data (excluding transformation codes row)
    tcodes : dict
        Dictionary mapping variable names to transformation codes
    verbose : bool
        Whether to print progress

    Returns
    -------
    pd.DataFrame
        Transformed dataset
    """
    df_transformed = df.copy()

    # Date column (first column) - keep as is
    date_col = df.columns[0]

    if verbose:
        print(f"Transforming {len(df.columns) - 1} variables...")

    # Transform each variable
    for col in df.columns[1:]:  # Skip date column
        if col in tcodes:
            tcode = tcodes[col]
            df_transformed[col] = apply_transformation(df[col].astype(float), tcode)

            if verbose and (df.columns.get_loc(col) - 1) % 10 == 0:
                print(f"  Transformed {df.columns.get_loc(col)}/{len(df.columns)-1} variables...")

    if verbose:
        print(f"✓ Transformation complete")

    return df_transformed


def standardize_data(df, save_params=True, params_path=None):
    """
    Standardize data to zero mean and unit variance

    CRITICAL: Save mean and SD for later rescaling of IRFs!

    Parameters
    ----------
    df : pd.DataFrame
        Transformed data
    save_params : bool
        Whether to save standardization parameters
    params_path : str or Path, optional
        Where to save parameters

    Returns
    -------
    tuple
        (standardized_df, params_df)
    """
    df_standardized = df.copy()

    # Date column - keep as is
    date_col = df.columns[0]

    # Calculate parameters for each variable
    params = []

    for col in df.columns[1:]:  # Skip date column
        # Calculate mean and std (ignoring NaNs)
        mean = df[col].mean()
        std = df[col].std()

        # Standardize: (x - mean) / std
        df_standardized[col] = (df[col] - mean) / std

        # Save parameters
        params.append({
            'variable': col,
            'mean': mean,
            'std': std,
            'n_obs': df[col].notna().sum(),
            'n_missing': df[col].isna().sum()
        })

    # Create params DataFrame
    params_df = pd.DataFrame(params)

    # Save parameters
    if save_params:
        if params_path is None:
            params_path = DATA_PROCESSED_DIR / "transformation_params.csv"

        params_path.parent.mkdir(parents=True, exist_ok=True)
        params_df.to_csv(params_path, index=False)

        print(f"✓ Standardization parameters saved to: {params_path}")
        print(f"  CRITICAL: These parameters needed for rescaling IRFs!")

    return df_standardized, params_df


def create_subsets(df, classification_path=None):
    """
    Create 6-var, 30-var, 43-var subsets for different models

    Parameters
    ----------
    df : pd.DataFrame
        Standardized full dataset
    classification_path : str or Path, optional
        Path to classification scheme

    Returns
    -------
    dict
        Dictionary with keys: '6var', '30var', '43var'
    """
    # For now, create simple subsets
    # TODO: Use actual variable classification from DHK (2025)

    date_col = df.columns[0]

    # 6-variable subset (for testing)
    # Pick first 3 macro + first 3 financial
    subset_6var = df[[date_col] + list(df.columns[1:7])].copy()

    # 30-variable subset (CCM baseline)
    subset_30var = df[[date_col] + list(df.columns[1:31])].copy()

    # 43-variable subset (full OI-TVC-43)
    subset_43var = df[[date_col] + list(df.columns[1:44])].copy()

    subsets = {
        '6var': subset_6var,
        '30var': subset_30var,
        '43var': subset_43var
    }

    return subsets


def check_stationarity(df, verbose=True):
    """
    Optional: Check stationarity of transformed variables using ADF test

    Parameters
    ----------
    df : pd.DataFrame
        Transformed data
    verbose : bool
        Whether to print results

    Returns
    -------
    pd.DataFrame
        ADF test results
    """
    try:
        from statsmodels.tsa.stattools import adfuller

        date_col = df.columns[0]
        results = []

        if verbose:
            print("\nChecking stationarity (ADF test)...")

        for col in df.columns[1:]:  # Skip date column
            # Drop NaNs
            series = df[col].dropna()

            if len(series) > 10:  # Need enough observations
                try:
                    adf_result = adfuller(series)
                    results.append({
                        'variable': col,
                        'adf_statistic': adf_result[0],
                        'p_value': adf_result[1],
                        'is_stationary': adf_result[1] < 0.05  # 5% significance
                    })
                except:
                    results.append({
                        'variable': col,
                        'adf_statistic': np.nan,
                        'p_value': np.nan,
                        'is_stationary': False
                    })

        results_df = pd.DataFrame(results)

        if verbose:
            n_stationary = results_df['is_stationary'].sum()
            print(f"✓ ADF test complete: {n_stationary}/{len(results_df)} variables stationary")

        return results_df

    except ImportError:
        print("⚠️  statsmodels not installed, skipping stationarity check")
        return None


def main():
    """Main execution function"""
    print("="*70)
    print("DHK (2025) Replication - Module 1: Data Processing")
    print("Task DHK-M1-002: Transform and Standardize Data")
    print("="*70)

    # Step 1: Load raw data
    print("\n[Step 1/5] Loading raw FRED-MD data...")
    raw_path = DATA_RAW_DIR / "fredmd_raw.csv"

    if not raw_path.exists():
        print(f"✗ Error: {raw_path} not found")
        print("  Please run 01_download_fredmd.py first")
        return

    df_raw = pd.read_csv(raw_path)
    print(f"✓ Loaded {len(df_raw)} rows, {len(df_raw.columns)} columns")

    # Step 2: Extract transformation codes
    print("\n[Step 2/5] Extracting transformation codes...")
    tcodes = get_transformation_codes(df_raw)
    print(f"✓ Extracted transformation codes for {len(tcodes)} variables")

    # Save tcodes
    tcodes_path = DATA_PROCESSED_DIR / "transformation_codes.json"
    tcodes_path.parent.mkdir(parents=True, exist_ok=True)
    with open(tcodes_path, 'w') as f:
        json.dump(tcodes, f, indent=2)
    print(f"✓ Saved to: {tcodes_path}")

    # Step 3: Apply transformations
    print("\n[Step 3/5] Applying transformations...")
    df_data = df_raw.iloc[1:].copy()  # Skip first row (tcodes)
    df_transformed = transform_dataset(df_data, tcodes)

    # Save transformed data
    transformed_path = DATA_PROCESSED_DIR / "fredmd_transformed.csv"
    df_transformed.to_csv(transformed_path, index=False)
    print(f"✓ Saved to: {transformed_path}")

    # Step 4: Standardize
    print("\n[Step 4/5] Standardizing data (mean=0, std=1)...")
    df_standardized, params_df = standardize_data(df_transformed)

    # Save standardized data
    standardized_path = DATA_PROCESSED_DIR / "fredmd_standardized.csv"
    df_standardized.to_csv(standardized_path, index=False)
    print(f"✓ Saved to: {standardized_path}")

    # Step 5: Create subsets
    print("\n[Step 5/5] Creating subsets (6/30/43 variables)...")
    subsets = create_subsets(df_standardized)

    for name, subset in subsets.items():
        subset_path = DATA_PROCESSED_DIR / f"fredmd_{name}.csv"
        subset.to_csv(subset_path, index=False)
        print(f"✓ Saved {name}: {subset.shape} -> {subset_path}")

    # Optional: Stationarity check
    print("\n[Optional] Checking stationarity...")
    stationarity_df = check_stationarity(df_transformed)
    if stationarity_df is not None:
        stat_path = DATA_PROCESSED_DIR / "stationarity_tests.csv"
        stationarity_df.to_csv(stat_path, index=False)
        print(f"✓ Saved stationarity test results to: {stat_path}")

    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"Total observations: {len(df_standardized)}")
    print(f"Total variables: {len(df_standardized.columns) - 1}")
    print(f"\nMissing values after transformation:")
    missing_counts = df_standardized.isna().sum()[1:]  # Skip date column
    print(f"  Mean: {missing_counts.mean():.1f}")
    print(f"  Max: {missing_counts.max()}")

    print("\n✓ Data processing complete!")
    print("\n⚠️  NEXT STEPS:")
    print("1. Inspect transformation_params.csv - verify standardization")
    print("2. Check fredmd_6var.csv - use for initial testing")
    print("3. Proceed to Task DHK-M2-001: Implement model equations")
    print("="*70)


if __name__ == "__main__":
    main()

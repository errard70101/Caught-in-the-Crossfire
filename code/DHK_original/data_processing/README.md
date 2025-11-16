# Data Processing for DHK (2025) Replication

This directory contains Python scripts for downloading and processing FRED-MD data.

## Quick Start

```bash
# Install requirements
pip install -r ../requirements.txt

# Step 1: Download FRED-MD dataset
python 01_download_fredmd.py

# Step 2: Transform and standardize
python 02_transform_data.py
```

## Scripts

### `01_download_fredmd.py`
**Purpose**: Download monthly FRED-MD dataset (1960-2021)

**What it does**:
- Downloads current FRED-MD from St. Louis Fed
- Extracts date range 1960-01 to 2021-10
- Creates preliminary variable classification (43 variables)
- Saves to `data/raw/`

**Outputs**:
- `data/raw/fredmd_raw.csv` - Full downloaded dataset
- `data/raw/fredmd_1960_2021.csv` - Subset for replication
- `data/processed/classification_scheme.csv` - Variable classification

**Important**: Variable list needs verification against DHK (2025) Online Appendix B!

### `02_transform_data.py`
**Purpose**: Apply FRED-MD transformations and standardize

**What it does**:
- Reads transformation codes from FRED-MD (row 0)
- Applies transformations (log, diff, etc.) to each variable
- Standardizes to zero mean, unit variance
- **CRITICAL**: Saves mean/SD for rescaling IRFs later
- Creates 6/30/43 variable subsets
- Optional: ADF stationarity tests

**Outputs**:
- `data/processed/fredmd_transformed.csv` - After transformations
- `data/processed/fredmd_standardized.csv` - Standardized data
- `data/processed/transformation_params.csv` - **CRITICAL for IRFs!**
- `data/processed/fredmd_6var.csv` - Small test subset
- `data/processed/fredmd_30var.csv` - CCM baseline (30 vars)
- `data/processed/fredmd_43var.csv` - Full OI-TVC-43 model

## FRED-MD Transformation Codes

| Code | Transformation | Example Use |
|------|---------------|-------------|
| 1 | No transformation | Already stationary |
| 2 | First difference: Δx(t) | Make stationary |
| 3 | Second difference: Δ²x(t) | Remove trend |
| 4 | Log: log(x) | Growth rates |
| 5 | Log difference: Δlog(x) | Percentage change |
| 6 | Second log diff: Δ²log(x) | Acceleration |
| 7 | Diff of % change | Volatility |

## Variable Classification

The 43-variable model (OI-TVC-43) contains:
- **18 Macro variables**: IPI, employment, CPI, etc.
- **12 Financial variables**: Interest rates, spreads, stock prices
- **13 Unclassified variables**: Federal Funds Rate, money supply, credit, exchange rates

**Key Insight**: Unclassified variables include external shock sources (this is the innovation!)

## Critical Files

### `transformation_params.csv`
Contains mean and standard deviation for each variable.

**Structure**:
```csv
variable,mean,std,n_obs,n_missing
INDPRO,4.523,0.234,738,2
...
```

**Why critical**: When computing IRFs, we need to rescale results back to original units using these parameters!

## Data Quality Checks

After running both scripts, check:

1. **No excessive missing values**:
```python
import pandas as pd
df = pd.read_csv('../../data/processed/fredmd_standardized.csv')
print(df.isna().sum())
```

2. **Standardization worked**:
```python
# Should be ~0 and ~1
print(df.mean())  # Should be close to 0
print(df.std())   # Should be close to 1
```

3. **Variable count**:
- 6-var model: 6 variables + date
- 30-var model: 30 variables + date
- 43-var model: 43 variables + date

## Troubleshooting

### Download fails
If `01_download_fredmd.py` fails to download:
1. Visit https://research.stlouisfed.org/econ/mccracken/fred-databases/
2. Download `current.csv` manually
3. Save to `data/raw/fredmd_raw.csv`
4. Run `02_transform_data.py`

### Variable not found
If a variable in the classification list is not in FRED-MD:
- Check Online Appendix B for correct variable name
- Some variables may have been renamed
- Update `get_variable_list_43var()` in `01_download_fredmd.py`

### Too many missing values
Some transformations (diff, log) create NaNs at beginning:
- This is expected
- MCMC will handle missing values
- Alternative: trim first few observations after transformation

## Next Steps

After data processing is complete:

1. **Verify variable list** against DHK (2025) Online Appendix B
2. **Inspect outputs** - check `data/processed/` directory
3. **Test with 6-var model** - use `fredmd_6var.csv` for initial algorithm testing
4. **Proceed to Module 2** - Implement model equations (`code/DHK_original/model/`)

## References

- DHK (2025): Davidson, Hou, Koop - "Investigating Economic Uncertainty..."
- FRED-MD: McCracken & Ng (2016) - "FRED-MD: A Monthly Database for Macroeconomic Research"
- FRED-MD Documentation: https://research.stlouisfed.org/econ/mccracken/fred-databases/

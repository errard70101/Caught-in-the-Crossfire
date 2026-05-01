# 52 個 baseline 變數逐一盤點

**日期**: 2026-05-01  
**依據**: `data/raw/raw_data_inventory.csv`，由 `code/data_processing/build_raw_data_inventory.py` 重新產生  
**Baseline 視窗**: 2003M1--2025M12；`tw_taiex_ret` 因月報酬率計算需要前期值，實際 baseline 從 2003M2 開始  

## 總結

目前 baseline 規格共有 **52 個變數**。

| 分類 | 變數數 | 可直接使用 | 可計算 | 需處理 |
|---|---:|---:|---:|---:|
| 總體固定分類 | 22 | 22 | 0 | 0 |
| 金融固定分類 | 8 | 6 | 1 | 1 |
| 未分類 | 22 | 21 | 0 | 1 |
| **合計** | **52** | **49** | **1** | **2** |

狀態解讀：

| 狀態 | 數量 | 意義 |
|---|---:|---|
| `available` | 49 | raw data 在 baseline 視窗內完整覆蓋 |
| `computed` | 1 | 可由既有變數直接計算 |
| `needs_transform` | 0 | raw data 已有，但需確認定義與轉換 |
| `available_with_gaps` | 2 | raw data 已有，但 baseline 有缺月 |
| `missing_raw` | 0 | 尚未取得 raw data |

## 第一優先缺口

| 變數 | 問題 | 建議 |
|---|---|---|
| `tw_foreign_inv` | TWSE 官方 BFI82U 從 2004M4 開始，缺 2003M1--2004M3 | 決定補舊資料、改樣本起點、或改列 robustness |
| `gl_gepu` | 只缺 2025M12 | 等待更新、暫用 2025M11 補值，或 baseline 暫切到 2025M11 |

## 已補齊的 raw data

| 變數 | 檔案 | 覆蓋 | 說明 |
|---|---|---|---|
| `tw_house_prices` | `data/raw/taiwan_financial/tw_house_prices_raw.csv` | 2001M1--2026M3 | 暫以信義全台季指數重複至月頻；原始季資料另存 `tw_house_sinyi_quarterly_raw.csv` |
| `tw_fx_vol` | `data/raw/taiwan_financial/tw_fx_vol_raw.csv` | 2000M1--2025M12 | 由 FRED `DEXTAUS` 日頻匯率 log return 建構；日頻原始檔另存 `tw_twdusd_daily_raw.csv` |
| 台北市住宅價格月指數 | `data/raw/taiwan_financial/tw_house_taipei_monthly_raw.csv` | 2012M8--2026M1 | data.taipei 月指數，起點太晚，先保留為比較或 robustness |
| `tw_upstream_prices` | `data/raw/taiwan_macro/tw_upstream_prices_raw.csv` | 1981M1--2026M3 | 正式取代原 `tw_wpi` baseline 變數；2021M1--2022M12 重疊期採 WPI，2023M1 起採調整後 PPI |
| `tw_mfg_wages` / `tw_svc_wages` | `data/raw/taiwan_macro/tw_real_wages_raw.csv` | 1982M1--2026M2 | DGBAS 每人每月經常性薪資，分製造業/服務業，CPI deflate 後轉 YoY；總薪資保留作 robustness |
| `tw_mfg_hours` / `tw_svc_hours` | `data/raw/taiwan_macro/tw_mfg_hours_raw.csv`, `tw_svc_hours_raw.csv` | 1973M1--2026M2 | DGBAS 受僱員工每人每月工時，分製造業/服務業 |
| `tw_building_permits_residential_area` | `data/raw/taiwan_macro/tw_building_permits_residential_area_raw.csv` | 2001M1--2026M3 | DGBAS 核發建築物建造執照住宅(H-2)樓地板面積，對應 DHK `PERMIT` |
| `tw_use_permits_residential_area` | `data/raw/taiwan_macro/tw_use_permits_residential_area_raw.csv` | 2001M1--2026M3 | DGBAS 核發建築物使用執照住宅(H-2)樓地板面積，對應 DHK `HOUST`/住宅完工活動 |

## Macro 固定分類

| 變數 | 名稱 | 狀態 | 覆蓋 | Baseline 缺月 | 處理建議 |
|---|---|---|---|---:|---|
| `tw_ipi` | Industrial Production Index | `available` | 1996-01--2026-03 | 0 | 可進入清理/轉換 |
| `tw_mfg_prod` | Manufacturing Production Index | `available` | 1982-01--2026-03 | 0 | 可進入清理/轉換 |
| `tw_export_orders` | Export Orders Index | `available` | 1984-01--2026-03 | 0 | 可進入清理/轉換 |
| `tw_retail` | Retail Sales (real) | `available` | 2000-01--2026-03 | 0 | 可進入清理/轉換 |
| `tw_food_svc` | Food and Beverage Services Sales (real) | `available` | 2000-01--2026-03 | 0 | 可進入清理/轉換 |
| `tw_exports_usd` | Exports (customs, real USD) | `available` | 2001-01--2026-03 | 0 | 可進入清理/轉換 |
| `tw_imports_usd` | Imports (customs, real USD) | `available` | 2001-01--2026-03 | 0 | 可進入清理/轉換 |
| `tw_business_cycle` | Business Cycle Indicator | `available` | 1982-01--2026-03 | 0 | 可進入清理/轉換 |
| `tw_cpi` | CPI (YoY) | `available` | 1982-01--2026-03 | 0 | 可進入清理/轉換 |
| `tw_core_cpi` | Core CPI (YoY) | `available` | 1982-01--2026-03 | 0 | 可進入清理/轉換 |
| `tw_upstream_prices` | WPI/PPI-Spliced Upstream Price Index (YoY) | `available` | 1981-01--2026-03 | 0 | 重疊期用 WPI，2023M1 起接調整後 PPI |
| `tw_import_prices` | Import Price Index (YoY) | `available` | 1981-01--2026-03 | 0 | 可進入清理/轉換 |
| `tw_export_prices` | Export Price Index (YoY) | `available` | 1981-01--2026-03 | 0 | 可進入清理/轉換 |
| `tw_unemp` | Unemployment Rate (SA) | `available` | 1978-01--2026-03 | 0 | 可進入清理/轉換 |
| `tw_mfg_emp` | Manufacturing Employment (SA) | `available` | 1973-01--2026-02 | 0 | 可進入清理/轉換 |
| `tw_svc_emp` | Services Employment (SA) | `available` | 1973-01--2026-02 | 0 | 可進入清理/轉換 |
| `tw_mfg_wages` | Real Manufacturing Regular Wages (YoY) | `available` | 1973-01--2026-02 | 0 | DGBAS 製造業每人每月經常性薪資，CPI deflate 後轉 YoY |
| `tw_svc_wages` | Real Services Regular Wages (YoY) | `available` | 1973-01--2026-02 | 0 | DGBAS 服務業部門每人每月經常性薪資，CPI deflate 後轉 YoY |
| `tw_mfg_hours` | Manufacturing Hours per Employee | `available` | 1973-01--2026-02 | 0 | DGBAS 製造業受僱員工每人每月工時 |
| `tw_svc_hours` | Services Hours per Employee | `available` | 1973-01--2026-02 | 0 | DGBAS 服務業部門受僱員工每人每月工時 |
| `tw_building_permits_residential_area` | Residential Building Permit Floor Area | `available` | 2001-01--2026-03 | 0 | DGBAS 建造執照住宅(H-2)樓地板面積；baseline candidate |
| `tw_use_permits_residential_area` | Residential Use Permit Floor Area | `available` | 2001-01--2026-03 | 0 | DGBAS 使用執照住宅(H-2)樓地板面積；baseline candidate |

## Financial 固定分類

| 變數 | 名稱 | 狀態 | 覆蓋 | Baseline 缺月 | 處理建議 |
|---|---|---|---|---:|---|
| `tw_overnight` | Overnight Interbank Rate | `available` | 2001-01--2025-12 | 0 | 可進入清理/轉換 |
| `tw_10y_bond` | 10-Year Government Bond Yield | `available` | 2001-01--2025-12 | 0 | 可進入清理/轉換 |
| `tw_term_spread` | Term Spread (10-year minus overnight) | `computed` | -- | -- | 由 `tw_10y_bond - tw_overnight` 計算 |
| `tw_taiex_ret` | TAIEX Monthly Return | `available` | 2001-01--2025-12 | 0 | 可進入清理/轉換 |
| `tw_taiex_vol` | TAIEX Monthly Realized Volatility | `available` | 2001-01--2025-12 | 0 | 可進入清理/轉換 |
| `tw_turnover` | TAIEX Average Daily Turnover | `available` | 2001-01--2025-12 | 0 | 可進入清理/轉換 |
| `tw_foreign_inv` | Foreign Institutional Net Buying | `available_with_gaps` | 2004-04--2025-12 | 15 | 需補 2003M1--2004M3 或做樣本決策 |
| `tw_margin_buy` | Margin Buying Balance (YoY) | `available` | 2001-01--2025-12 | 0 | 可進入清理/轉換 |

## Unclassified

| 變數 | 名稱 | 狀態 | 覆蓋 | Baseline 缺月 | 處理建議 |
|---|---|---|---|---:|---|
| `tw_policy_rate` | CBC Discount Rate | `available` | 2001-01--2025-12 | 0 | 可進入清理/轉換 |
| `tw_m1b` | M1B Money Supply | `available` | 2001-01--2025-12 | 0 | 可進入清理/轉換 |
| `tw_m2` | M2 Money Supply | `available` | 2001-01--2025-12 | 0 | 可進入清理/轉換 |
| `tw_bank_loans` | Bank Loans and Investments | `available` | 2001-01--2025-12 | 0 | 可進入清理/轉換 |
| `tw_consumer_loans` | Consumer Loans | `available` | 2001-01--2025-12 | 0 | 可進入清理/轉換 |
| `tw_taiex_level` | TAIEX Level (log) | `available` | 2001-01--2025-12 | 0 | 可進入清理/轉換 |
| `tw_house_prices` | Housing Price Index | `available` | 2001-01--2026-03 | 0 | 暫用信義全台季指數重複至月頻 |
| `tw_twdusd` | NTD/USD Exchange Rate | `available` | 2000-01--2025-12 | 0 | 可進入清理/轉換 |
| `tw_fx_vol` | NTD/USD Realized Volatility | `available` | 2000-01--2025-12 | 0 | 由 FRED DEXTAUS 日頻資料建構 |
| `tw_reer` | Real Effective Exchange Rate | `available` | 1994-01--2026-02 | 0 | 可進入清理/轉換 |
| `tw_short_sell` | Short Selling Balance (YoY) | `available` | 2001-01--2025-12 | 0 | 可進入清理/轉換 |
| `us_ffr` | Federal Funds Rate | `available` | 2000-01--2025-12 | 0 | 可進入清理/轉換 |
| `us_ipi` | U.S. Industrial Production | `available` | 2000-01--2025-12 | 0 | 可進入清理/轉換 |
| `us_credit_spread` | U.S. Credit Spread | `available` | 2000-01--2025-12 | 0 | 可進入清理/轉換 |
| `us_epu` | U.S. Economic Policy Uncertainty | `available` | 2001-01--2025-12 | 0 | 可進入清理/轉換 |
| `cn_ipi` | China Industrial Production | `available` | 1990-01--2026-03 | 0 | 可進入清理/轉換 |
| `cn_ppi` | China Producer Price Index | `available` | 1993-01--2026-03 | 0 | 可進入清理/轉換 |
| `cn_m2` | China M2 Money Supply | `available` | 1996-01--2026-01 | 0 | 建構資料集時轉 YoY |
| `gl_vix` | VIX | `available` | 2000-01--2025-12 | 0 | 可進入清理/轉換 |
| `gl_gpr` | Global Geopolitical Risk | `available` | 2001-01--2025-12 | 0 | 可進入清理/轉換 |
| `gl_gepu` | Global Economic Policy Uncertainty | `available_with_gaps` | 2001-01--2025-11 | 1 | 需補 2025M12 或做終點決策 |
| `us_tpu` | U.S. Trade Policy Uncertainty | `available` | 2001-01--2025-12 | 0 | 可進入清理/轉換 |

## 下一步工作順序

1. 決定 `tw_foreign_inv` 的處理方式：補舊資料、樣本起點改為 2004M4、或降為 robustness。
2. 建構 `tw_term_spread`。
3. 更新 `gl_gepu`，或在 freeze dataset 時把終點暫定為 2025M11。
4. 最終選定房價指數來源與季轉月方法：目前已有信義全台/都會區季指數與台北市月指數；國泰指數公開頁以 PDF/下載入口為主，尚未取得可直接重現的 CSV。
5. 最終確認建照/使照採住宅樓地板面積或總樓地板面積；目前 baseline candidate 採住宅樓地板面積，總面積與工程造價保留作 robustness。

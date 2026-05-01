# 變數資料缺口盤點

**日期**: 2026-05-01  
**依據**: `docs/variable_planning.md` 與 `data/raw/raw_data_inventory.csv`  
**Baseline 視窗**: 2003M1--2025M12；TAIEX total-return return 例外為 2003M2--2025M12

> 2026-05-01 更新：`tw_house_prices`, `tw_fx_vol`, 中國變數、薪資/工時、
> 建照/使照 housing activity raw data 皆已補齊。
> 最新逐一盤點請以 `docs/variable_status_inventory_2026-05-01.md` 與重新產生的
> `data/raw/raw_data_inventory.csv` 為準。

## 總結

目前 baseline candidate 共有 **52 個變數**：

| 分類 | 變數數 | 狀態摘要 |
|---|---:|---|
| Macro 固定分類 | 22 | 22 個可用；原 `tw_wpi` 已正式改用 `tw_upstream_prices`；製造業與服務業人數、工時、實質經常性薪資、住宅建照/使照皆已建構 |
| Financial 固定分類 | 8 | 7 個可用或可計算；`tw_foreign_inv` 從 2004M4 才開始 |
| Unclassified | 22 | 21 個可用；`gl_gepu` 只缺 2025M12 |

按原始 inventory 狀態計算：

| 狀態 | 數量 | 解讀 |
|---|---:|---|
| `available` | 49 | 原始資料已在 baseline 視窗內完整覆蓋 |
| `computed` | 1 | `tw_term_spread` 可由 10Y 公債殖利率減隔夜拆款利率產生 |
| `needs_transform` | 0 | 原始資料已抓，但仍需轉換或確認定義 |
| `available_with_gaps` | 2 | 已有資料，但 baseline 有缺月 |
| `available_partial` | 0 | 已有部分資料，但覆蓋不足以直接用 |
| `missing_raw` | 0 | 尚未取得原始資料 |

## 中國變數處理結果（2026-05-01 更新）

三個中國 baseline 變數已補齊，來源為 Trading Economics 圖表資料後端轉載的 NBS/PBoC 月資料。原始檔均保留 `source`, `unit`, `te_symbol`, `te_vintage`, `is_imputed` 欄位以利追蹤。

| 變數 | 檔案 | 來源 | 覆蓋 | Baseline 缺月 | 備註 |
|---|---|---|---|---:|---|
| `cn_ipi` 中國工業增加值 | `data/raw/china/cn_ipi_raw.csv` | NBS via Trading Economics | 1990M1--2026M3 | 0 | NBS 未單獨發布的 1 月值，以同年 2 月 Jan-Feb YoY 補入並標記 `is_imputed=True` |
| `cn_ppi` 中國 PPI | `data/raw/china/cn_ppi_raw.csv` | NBS via Trading Economics | 1993M1--2026M3 | 0 | YoY percent |
| `cn_m2` 中國 M2 | `data/raw/china/cn_m2_raw.csv` | PBoC via Trading Economics | 1996M1--2026M1 | 0 | level, CNY billion；建構最終資料集時再轉 YoY |

## 第一優先：會直接卡住資料集的缺口

目前沒有 `missing_raw` 型缺口。仍會影響 baseline freeze 的只有 `tw_foreign_inv` 早期缺月、`gl_gepu` 端點缺 2025M12，以及 `tw_term_spread` 尚待在 final dataset 中 materialize。

## 第二優先：已有資料但需要決策

| 變數 | 分類 | 目前狀態 | 問題 | 建議處理 |
|---|---|---|---|---|
| `tw_upstream_prices` 上游物價壓力 | macro | `available` | 已正式取代原 `tw_wpi`，baseline 無缺月 | 2021M1--2022M12 重疊期採 WPI；2023M1 起採調整後 PPI |
| `tw_foreign_inv` 外資淨買賣超 | financial | `available_with_gaps` | 官方 TWSE BFI82U 從 2004M4 開始，缺 2003M1--2004M3 | 若堅持 2003M1 起始，需找舊制資料或改起始為 2004M4；若不想縮樣本，可考慮移除此變數 |
| `gl_gepu` 全球 EPU | unclassified | `available_with_gaps` | 只缺 2025M12 | 影響很小；可等待更新、用 2025M11 值暫補，或將 baseline 暫切到 2025M11 |

## 可直接進入清理與轉換的變數

### Macro 固定分類

完整覆蓋 baseline 的 macro 變數：

`tw_ipi`, `tw_mfg_prod`, `tw_export_orders`, `tw_retail`, `tw_food_svc`, `tw_exports_usd`, `tw_imports_usd`, `tw_business_cycle`, `tw_cpi`, `tw_core_cpi`, `tw_import_prices`, `tw_export_prices`, `tw_unemp`, `tw_mfg_emp`, `tw_svc_emp`, `tw_mfg_wages`, `tw_svc_wages`, `tw_mfg_hours`, `tw_svc_hours`, `tw_building_permits_residential_area`, `tw_use_permits_residential_area`

需處理後再用：

無。

### Financial 固定分類

完整覆蓋或可計算：

`tw_overnight`, `tw_10y_bond`, `tw_term_spread`, `tw_taiex_ret`, `tw_taiex_vol`, `tw_turnover`, `tw_margin_buy`

有早期缺口：

`tw_foreign_inv`

### Unclassified

完整覆蓋 baseline 的台灣國內/匯率變數：

`tw_policy_rate`, `tw_m1b`, `tw_m2`, `tw_bank_loans`, `tw_consumer_loans`, `tw_taiex_level`, `tw_twdusd`, `tw_reer`, `tw_short_sell`

完整覆蓋 baseline 的美國與全球變數：

`us_ffr`, `us_ipi`, `us_credit_spread`, `us_epu`, `gl_vix`, `gl_gpr`, `us_tpu`

需補齊或決策：

`tw_house_prices`, `tw_fx_vol`, `gl_gepu`

## 建議的下一輪工作順序

1. **處理兩個台灣 unclassified 缺口**：`tw_house_prices`, `tw_fx_vol`。這兩個是 DHK 對應變數，保留價值高。
2. **決定 `tw_foreign_inv` 的樣本策略**：補 2003M1--2004M3、改起始至 2004M4，或刪除。
3. **`tw_upstream_prices` 已正式取代 `tw_wpi`**：後續只需在資料附錄說明 WPI/PPI splice 規則。
4. **薪資問題已解決**：`tw_mfg_wages` 與 `tw_svc_wages` 均由 DGBAS 分業經常性薪資 deflate 後轉 YoY；總薪資保留作 robustness。

## 可行的精簡方案

若某些資料短期無法取得，仍需維持 40+ 變數與核心研究設計。優先保留外部衝擊變數；可考慮刪除或降為 robustness 的候選如下：

| 候選 | 理由 |
|---|---|
| `tw_foreign_inv` | 起始 2004M4，會縮短 baseline；且與股匯資金流動高度相關 |
| `tw_short_sell` | 資訊量可能有限，且與股市情緒重疊 |
| `tw_food_svc` | 與零售/服務消費資訊重疊 |
| `tw_turnover` | 金融市場 noise 較高，與 TAIEX volatility/return 有重疊 |

不建議優先刪除 `cn_ipi`, `cn_ppi`, `cn_m2`，因為中國變數是本研究 dual exposure 設計的必要部分；目前三者已補齊，可先保留在 baseline。

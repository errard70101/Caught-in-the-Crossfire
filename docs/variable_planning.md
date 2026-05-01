# OI-SVMVAR 變數規劃與資料來源清單

**專案**: Caught in the Crossfire — OI-SVMVAR Model (DHK 2025)
**資料頻率**: 月度 (Monthly)
**樣本期間**: Baseline 2003M1–2025M12（276 個月；TAIEX total return baseline），price-index robustness 2001M1–2025M12（300 個月）✅ 已確認
**變數數**: 52 個（原目標 ~43，52 仍在 DHK 建議的 40+ 範圍內；建照/使照為新增 housing activity 對應）✅ 已確認
**建立日期**: 2026-04-09
**決議日期**: 2026-04-09

> 此清單根據 `llm_logs/2025-11-08_discussion.md` 的變數規劃，
> 結合 `trade-war-BCA` 專案的 DGBAS API 基礎設施進行整理。
>
> 與 Davidson, Hou, and Koop (2025) 原始 OI-TVC-43 變數的逐項對照，
> 見 `docs/dhk_variable_crosswalk_2026-05-01.md`。

---

## 可複用的基礎設施

### 來自 `trade-war-BCA` 的 DGBAS API 架構

| 元件 | 說明 | 可複用程度 |
|------|------|-----------|
| `fetch_json()` | 通用 DGBAS API 抓取函數（含 SSL 處理、快取） | ✅ 直接複用 |
| `roc_month_to_timestamp()` | 民國年月轉 ISO 日期 | ✅ 直接複用 |
| `roc_quarter_to_iso()` | 民國季轉 ISO 季 | ⚠️ 本專案用月度，需調整 |
| `make_bitstring()` | 建構 DGBAS API 欄位選擇碼 | ✅ 直接複用 |
| DGBAS API 端點 | `https://nstatdb.dgbas.gov.tw/dgbasAll/webMain.aspx` | ✅ 直接複用 |

**已知 DGBAS API funid**:
- `A018102060` — GDP 支出面（季度，本專案不用）
- `A040107010` — 就業人數（月度 ✅）
- `A046401010` — 工時（月度 ✅）
- `A018201010` — 國民所得（季度，本專案不用）

**需要新查的 DGBAS funid**（本專案需要但 BCA 未用）:
- 工業生產指數 (IPI)
- 消費者物價指數 (CPI)
- 躉售物價指數 (WPI)
- 失業率
- 薪資
- 零售/餐飲營業額
- 進出口物價指數
- 出口/進口值

---

## 變數總覽

### 分類一：總體經濟變數 (Macroeconomic) — 分類固定為 "macro"

| # | 變數 | 英文代碼 | 轉換 | 來源 | API可行 | 起始年 | 備註 |
|---|------|---------|------|------|---------|--------|------|
| 1 | 工業生產指數 | `tw_ipi` | YoY% | DGBAS | ✅ 待查 funid | ~1981 | |
| 2 | 製造業生產指數 | `tw_mfg_prod` | YoY% | DGBAS | ✅ 待查 funid | ~1981 | IPI 子項 |
| 3 | 外銷訂單指數 | `tw_export_orders` | YoY% | MOEA | ⚠️ 需確認 | ~1988 | 經濟部統計 |
| 4 | 零售業營業額(實質) | `tw_retail` | YoY% | DGBAS | ✅ 待查 funid | ~1999 | 較晚起始 |
| 5 | 餐飲業營業額(實質) | `tw_food_svc` | YoY% | DGBAS | ✅ 待查 funid | ~1999 | 較晚起始 |
| 6 | 海關出口值(USD) | `tw_exports_usd` | YoY% | MOF/DGBAS | ✅ 待查 funid | ~1981 | |
| 7 | 海關進口值(USD) | `tw_imports_usd` | YoY% | MOF/DGBAS | ✅ 待查 funid | ~1981 | |
| ~~8~~ | ~~PMI~~ | — | — | — | — | — | ❌ 已刪除（2012 太晚） |
| ~~9~~ | ~~NMI~~ | — | — | — | — | — | ❌ 已刪除（2014 太晚） |
| 8 | 景氣對策信號 | `tw_business_cycle` | Level | NDC | ⚠️ 需確認 | ~1984 | |
| 11 | CPI 年增率 | `tw_cpi` | YoY% | DGBAS | ✅ 待查 funid | ~1981 | |
| 12 | 核心 CPI 年增率 | `tw_core_cpi` | YoY% | DGBAS | ✅ 待查 funid | ~2001? | 需確認起始 |
| 13 | 上游物價壓力（WPI/PPI splice） | `tw_upstream_prices` | YoY% | DGBAS + 作者建構 | ✅ | ~1981 | 正式取代 WPI；2021M1--2022M12 重疊期採 WPI，2023M1 起採調整後 PPI |
| 14 | 進口物價指數 YoY | `tw_import_prices` | YoY% | DGBAS | ✅ 待查 funid | ~1981 | |
| 15 | 出口物價指數 YoY | `tw_export_prices` | YoY% | DGBAS | ✅ 待查 funid | ~1981 | |
| 16 | 失業率(季調) | `tw_unemp` | Level% | DGBAS | ✅ 待查 funid | ~1978 | |
| 17 | 製造業受僱員工人數 | `tw_mfg_emp` | YoY% | DGBAS | ✅ 已有類似 | ~1981 | A040107010 可用 |
| 18 | 服務業受僱員工人數 | `tw_svc_emp` | YoY% | DGBAS | ✅ 待查 funid | ~1981 | |
| 19 | 製造業實質經常性薪資 | `tw_mfg_wages` | YoY% | DGBAS A046301010 + CPI | ✅ | ~1982 | 每人每月經常性薪資，CPI deflate 後轉 YoY；總薪資保留作 robustness |
| 20 | 服務業實質經常性薪資 | `tw_svc_wages` | YoY% | DGBAS A046301010 + CPI | ✅ | ~1982 | 每人每月經常性薪資，CPI deflate 後轉 YoY；總薪資保留作 robustness |
| 21 | 製造業每人每月工時 | `tw_mfg_hours` | Level | DGBAS A046401010 | ✅ | ~1973 | |
| 22 | 服務業每人每月工時 | `tw_svc_hours` | Level | DGBAS A046401010 | ✅ | ~1973 | |
| 23 | 核發建築物建造執照住宅樓地板面積 | `tw_building_permits_residential_area` | YoY% | DGBAS A060101010 | ✅ | 2001 | 對應 DHK `PERMIT` |
| 24 | 核發建築物使用執照住宅樓地板面積 | `tw_use_permits_residential_area` | YoY% | DGBAS A060103010 | ✅ | 2001 | 對應 DHK `HOUST`/housing completions；總面積與工程造價保留作 robustness |

**⚠️ 已處理**:
- ~~PMI/NMI~~ → 已刪除（起始太晚）
- 零售/餐飲 ~1999 起始 → 2001M1 樣本起始無問題

---

### 分類二：金融變數 (Financial) — 分類固定為 "financial"

| # | 變數 | 英文代碼 | 轉換 | 來源 | API可行 | 起始年 | 備註 |
|---|------|---------|------|------|---------|--------|------|
| 20 | 隔夜拆款利率 | `tw_overnight` | Level% | CBC | ⚠️ CBC 網站 | ~1990 | |
| 21 | 10年期公債殖利率 | `tw_10y_bond` | Level% | CBC | ⚠️ CBC 網站 | ~1999 | 公債市場較晚發展 |
| 22 | 期限利差 | `tw_term_spread` | Level bps | 計算 | — | ~1999 | = 10Y - Overnight |
| 23 | 台股月報酬率 | `tw_taiex_ret` | Return% | TWSE | ✅ TWSE API | 2003 | MFI94U 報酬指數；price-index robustness 見 `tw_taiex_price_ret` |
| 24 | 台股月波動率 | `tw_taiex_vol` | Std dev | TWSE | ✅ TWSE API | 2003 | MFI94U 日報酬→月 std；price-index robustness 見 `tw_taiex_price_vol` |
| 25 | 台股日均成交值 | `tw_turnover` | YoY% | TWSE | ✅ TWSE API | ~1990 | FMTQIK，日成交金額月平均 |
| 26 | 外資淨買賣超 | `tw_foreign_inv` | 月淨額 | TWSE | ⚠️ 需爬蟲 | ~2001 | 外資開放後 |
| 27 | 融資餘額變動 | `tw_margin_buy` | YoY% | TWSE | ⚠️ 需爬蟲 | ~1990 | |
| 28 | 融券餘額變動 | `tw_short_sell` | YoY% | TWSE | ⚠️ 需爬蟲 | ~1990 | |

**⚠️ 已處理**:
- ~~信用利差~~ → 已刪除（~2005 太晚）
- 10Y 公債殖利率 ~1999 → 2001M1 樣本起始無問題
- 外資買賣超 ~2001 → 剛好可用

---

### 分類三：未分類變數 (Unclassified) — 模型動態判定 macro/financial

#### 3a. 台灣國內模糊變數

| # | 變數 | 英文代碼 | 轉換 | 來源 | API可行 | 起始年 | DHK 對應 |
|---|------|---------|------|------|---------|--------|---------|
| 29 | 央行重貼現率 | `tw_policy_rate` | Level% | CBC | ⚠️ CBC | ~1981 | FEDFUNDS |
| 30 | M1b 年增率 | `tw_m1b` | YoY% | CBC | ⚠️ CBC | ~1981 | Money Supply |
| 31 | M2 年增率 | `tw_m2` | YoY% | CBC | ⚠️ CBC | ~1981 | Money Supply |
| 32 | 銀行放款投資 YoY | `tw_bank_loans` | YoY% | CBC | ⚠️ CBC | ~1981 | Loans |
| 33 | 消費者貸款 YoY | `tw_consumer_loans` | YoY% | CBC | ⚠️ CBC | ~1990? | Consumer Loans |
| 34 | TAIEX 水位(log) | `tw_taiex_level` | log | TWSE | ✅ TWSE API | ~1990 | S&P 500 |
| ~~35~~ | ~~信用利差~~ | — | — | — | — | — | ❌ 已刪除（~2005 太晚） |
| 34 | 房價指數 YoY | `tw_house_prices` | YoY% | Sinyi/Cathay | ❌ 手動 | ~2001(Q) | ✅ 季→月插值 |
| 37 | TWD/USD 匯率 | `tw_twdusd` | log | CBC/FRED | ✅ FRED | ~1981 | Exchange Rate |
| 38 | TWD/USD 波動率 | `tw_fx_vol` | Std dev | CBC/FRED | ✅ FRED | ~1981 | — |
| 39 | REER | `tw_reer` | log | BIS | ✅ BIS API | ~1994 | — |

#### 3b. 美國變數（全部 unclassified）

| # | 變數 | 英文代碼 | 轉換 | FRED代碼 | API可行 | 起始年 |
|---|------|---------|------|---------|---------|--------|
| 40 | 美國聯邦基金利率 | `us_ffr` | Level% | FEDFUNDS | ✅ FRED API | ~1954 |
| 41 | 美國工業生產指數 | `us_ipi` | YoY% | INDPRO | ✅ FRED API | ~1919 |
| 42 | 美國信用利差 | `us_credit_spread` | Level bps | BAA10YM | ✅ FRED API | ~1986 |
| 43 | 美國 EPU | `us_epu` | log | — | ✅ CSV下載 | ~1985 |

#### 3c. 中國變數（全部 unclassified）

| # | 變數 | 英文代碼 | 轉換 | 來源 | API可行 | 起始年 | 備註 |
|---|------|---------|------|------|---------|--------|------|
| 44 | 中國工業增加值 | `cn_ipi` | YoY% | NBS/FRED | ⚠️ | ~1995 | FRED: CHNIPI |
| 45 | 中國 PPI | `cn_ppi` | YoY% | NBS/CEIC | ⚠️ | ~1996 | |
| 46 | 中國 M2 年增率 | `cn_m2` | YoY% | FRED | ✅ FRED API | ~1996 | FRED: MYAGM2TWM052N（取代 TSF） |

#### 3d. 全球與美中關係（全部 unclassified）

| # | 變數 | 英文代碼 | 轉換 | 來源 | API可行 | 起始年 | 備註 |
|---|------|---------|------|------|---------|--------|------|
| 47 | VIX | `gl_vix` | log | FRED | ✅ VIXCLS | ~1990 | |
| 48 | GPR 地緣政治風險 | `gl_gpr` | log | Iacoviello | ✅ CSV下載 | ~1985 | |
| 49 | 全球 EPU | `gl_gepu` | log | PolicyUncertainty | ✅ CSV下載 | ~1997 | |
| 50 | US 貿易政策不確定 | `us_tpu` | log | BBD Categorical EPU | ✅ xlsx下載 | ~1985 | ✅ 取代 China EPU |

---

## 已確認的決定（2026-04-09 定案）

### 決定 1：PMI / NMI → ✅ 刪除
- PMI 2012M7 才開始、NMI 2014M1 → 太晚，無法納入 2001M1 起始的樣本
- 景氣對策信號 (NDC, 1984M1 起) 已在變數列表中，足以替代
- 總體固定分類目前為 22 個，已另補住宅建照/使照作為 DHK housing activity 對應

### 決定 2：台灣信用利差 → ✅ 刪除
- 公司債市場資料最早 ~2005M1，是所有變數中起始最晚的
- 期限利差 (10Y − Overnight) 已捕捉利率結構資訊
- 避免因單一變數犧牲樣本長度

### 決定 3：房價指數 → ✅ 保留，季→月插值
- 信義房價指數 ~2001Q1 起，與樣本起始一致
- 使用三次樣條插值 (cubic spline) 或 Chow-Lin temporal disaggregation 轉為月度

### 決定 4：中國金融變數 → ✅ 使用 M2（取代 TSF）
- China TSF ~2002M1 起，是第二大制約因素
- China M2 (FRED: `MYAGM2TWM052N`) ~1996M1 起，前推 6 年
- M2 作為廣義貨幣供給，同樣能捕捉中國金融面資訊

### 決定 5：第 14 個 unclassified 變數 → ✅ US Trade Policy Uncertainty (BBD)
> **🚨 發現**: China EPU (PolicyUncertainty.com) 已於 **2019M4 停更**，不可用。

- 來源: Baker-Bloom-Davis Categorical EPU 第 9 欄 "Trade Policy"
- 範圍: 1985M1–2024M12（月度，480 筆觀察值，已驗證可下載）
- 邏輯: 直接捕捉美國貿易政策不確定性，美中貿易戰是其主要驅動力

### 決定 6：樣本期間 → ✅ 情境 C（2001M1–2025M12，300 個月）

| 情境 | 起始 | 月數 | 排除的變數 |
|------|------|------|-----------|
| A | 1997M8 | ~341 | 零售、餐飲、核心CPI、10Y債、期限利差、外資、信用利差、房價、China TSF |
| B | 2000M1 | ~312 | 核心CPI、外資、信用利差、房價、China TSF |
| **C ✅** | **2001M1** | **~300** | **信用利差、China TSF（均已由上述決定處理）** |
| D | 2002M1 | ~288 | 信用利差 |

**確認的配置**:
- 300 個月觀察值，涵蓋 911、SARS、金融海嘯、歐債、美中貿易戰、COVID、地緣升溫
- 所有重要變數皆可用（外資、房價、核心CPI）
- 300 個觀察值對 ~43 變數的 VAR 估計綽綽有餘（DHK 用 ~240 個月）

---

## 資料下載策略（按來源分組）

### Group A: DGBAS API（可程式化）→ ~12 變數
複用 `trade-war-BCA` 的 `fetch_json()` 函數，僅需查對應 funid。

需要的 DGBAS 月度表:
1. 工業生產指數 (IPI)
2. 製造業生產指數
3. CPI / 核心 CPI
4. WPI
5. 進出口物價指數
6. 失業率
7. 就業人數（已有 funid: A040107010）
8. 薪資
9. 零售/餐飲營業額

### Group B: FRED API（可程式化）→ ~8 變數
使用 `fredapi` Python 套件或直接 URL。

| 變數 | FRED 代碼 |
|------|---------|
| US FFR | FEDFUNDS |
| US IPI | INDPRO |
| US BAA-10Y | BAA10YM |
| VIX | VIXCLS |
| TWD/USD | EXTAUS (或 DEXTA) |
| China IPI | — (FRED 可能有) |

### Group C: 公開 CSV 下載 → ~4 變數
| 變數 | URL |
|------|-----|
| US EPU | policyuncertainty.com/us_monthly.html |
| Global EPU | policyuncertainty.com/global_monthly.html |
| GPR | matteoiacoviello.com/gpr.htm |
| US Trade Policy Uncertainty | policyuncertainty.com (Categorical EPU xlsx, 第9欄) |

### Group D: TWSE API → ~3 變數 + robustness series
| 變數 | TWSE endpoint |
|------|---------------|
| TAIEX total return index（baseline return/volatility） | `MFI94U` |
| TAIEX price index（baseline level + robustness return/volatility） | `MI_5MINS_HIST` |
| TWSE market turnover（baseline turnover） | `FMTQIK` |

### Group E: CBC 網站（可能需手動或爬蟲）→ ~8 變數
| 變數 | CBC 表格 |
|------|---------|
| 重貼現率 | 金融統計月報 |
| M1b, M2 | 金融統計月報 |
| 銀行放款投資 | 金融統計月報 |
| 消費者貸款 | 金融統計月報 |
| 隔夜拆款利率 | 金融統計月報 |
| 10Y 公債殖利率 | 金融統計月報 |

### Group F: 其他（需個別處理）→ ~4 變數
| 變數 | 來源 | 備註 |
|------|------|------|
| 外銷訂單 | MOEA | 經濟部統計處 |
| 景氣對策信號 | NDC | 國發會 |
| REER | BIS | bis.org |
| 房價指數 | Sinyi/Cathay | 季度→月度插值 |
| 中國 PPI | NBS/CEIC | 可能需 CEIC 帳號 |
| 中國 M2 | FRED | MYAGM2TWM052N（已確認改用 M2） |

---

## 建議的優先順序

1. **先處理 Group A + B** (DGBAS + FRED)：最容易程式化，涵蓋 ~20 變數
2. **再處理 Group C + D** (CSV + TWSE)：簡單下載，~7 變數
3. **然後 Group E** (CBC)：需要研究 CBC 網站結構
4. **最後 Group F**：逐一解決特殊來源

---

## 最終確認的變數清單（52 個）

> 樣本期間: **Baseline 2003M1–2025M12（276 個月）；price-index robustness 2001M1–2025M12（300 個月）**
> 決議日期: 2026-04-09
> 變數數: 22 macro + 8 financial + 22 unclassified = **52 個**
> （原目標 ~43；52 仍在 DHK 建議的「40+ 避免遺漏變數偏誤」範圍；建照/使照補上 DHK housing starts/permits 對應）

### Macro（固定分類）— 22 個

| # | 變數 | 代碼 | 轉換 | 來源 |
|---|------|------|------|------|
| 1 | 工業生產指數 | `tw_ipi` | YoY% | DGBAS |
| 2 | 製造業生產指數 | `tw_mfg_prod` | YoY% | DGBAS |
| 3 | 外銷訂單指數 | `tw_export_orders` | YoY% | MOEA |
| 4 | 零售業營業額(實質) | `tw_retail` | YoY% | DGBAS |
| 5 | 餐飲業營業額(實質) | `tw_food_svc` | YoY% | DGBAS |
| 6 | 海關出口值(USD) | `tw_exports_usd` | YoY% | DGBAS |
| 7 | 海關進口值(USD) | `tw_imports_usd` | YoY% | DGBAS |
| 8 | 景氣對策信號 | `tw_business_cycle` | Level | NDC |
| 9 | CPI 年增率 | `tw_cpi` | YoY% | DGBAS |
| 10 | 核心 CPI 年增率 | `tw_core_cpi` | YoY% | DGBAS |
| 11 | 上游物價壓力（WPI/PPI splice） | `tw_upstream_prices` | YoY% | DGBAS + 作者建構 |
| 12 | 進口物價指數 YoY | `tw_import_prices` | YoY% | DGBAS |
| 13 | 出口物價指數 YoY | `tw_export_prices` | YoY% | DGBAS |
| 14 | 失業率(季調) | `tw_unemp` | Level% | DGBAS |
| 15 | 製造業受僱員工人數 | `tw_mfg_emp` | YoY% | DGBAS |
| 16 | 服務業受僱員工人數 | `tw_svc_emp` | YoY% | DGBAS |
| 17 | 製造業實質經常性薪資 | `tw_mfg_wages` | YoY% | DGBAS A046301010 + CPI |
| 18 | 服務業實質經常性薪資 | `tw_svc_wages` | YoY% | DGBAS A046301010 + CPI |
| 19 | 製造業每人每月工時 | `tw_mfg_hours` | Level | DGBAS A046401010 |
| 20 | 服務業每人每月工時 | `tw_svc_hours` | Level | DGBAS A046401010 |
| 21 | 住宅建造執照樓地板面積 | `tw_building_permits_residential_area` | YoY% | DGBAS A060101010 |
| 22 | 住宅使用執照樓地板面積 | `tw_use_permits_residential_area` | YoY% | DGBAS A060103010 |

### Financial（固定分類）— 8 個

| # | 變數 | 代碼 | 轉換 | 來源 |
|---|------|------|------|------|
| 23 | 隔夜拆款利率 | `tw_overnight` | Level% | CBC |
| 24 | 10年期公債殖利率 | `tw_10y_bond` | Level% | CBC |
| 25 | 期限利差 | `tw_term_spread` | Level bps | 計算 (24−23) |
| 26 | 台股月報酬率 | `tw_taiex_ret` | Return% | TWSE (MFI94U) |
| 27 | 台股月波動率 | `tw_taiex_vol` | Std dev | TWSE (MFI94U) |
| 28 | 台股日均成交值 | `tw_turnover` | YoY% | TWSE |
| 29 | 外資淨買賣超 | `tw_foreign_inv` | 月淨額 | TWSE |
| 30 | 融資餘額變動 | `tw_margin_buy` | YoY% | TWSE |

### Unclassified（模型動態分類）— 22 個

**台灣國內模糊（7 個）**:

| # | 變數 | 代碼 | 轉換 | 來源 |
|---|------|------|------|------|
| 31 | 央行重貼現率 | `tw_policy_rate` | Level% | CBC |
| 32 | M1b 年增率 | `tw_m1b` | YoY% | CBC |
| 33 | M2 年增率 | `tw_m2` | YoY% | CBC |
| 34 | 銀行放款投資 YoY | `tw_bank_loans` | YoY% | CBC |
| 35 | 消費者貸款 YoY | `tw_consumer_loans` | YoY% | CBC |
| 36 | TAIEX 水位(log) | `tw_taiex_level` | log | TWSE |
| 37 | 房價指數 YoY | `tw_house_prices` | YoY% | Sinyi（季→月插值） |

**台灣外部（3 個）**:

| # | 變數 | 代碼 | 轉換 | 來源 |
|---|------|------|------|------|
| 38 | TWD/USD 匯率 | `tw_twdusd` | log | FRED |
| 39 | TWD/USD 波動率 | `tw_fx_vol` | Std dev | FRED |
| 40 | REER | `tw_reer` | log | BIS |

**台灣金融市場模糊（1 個）**:

| # | 變數 | 代碼 | 轉換 | 來源 |
|---|------|------|------|------|
| 41 | 融券餘額變動 | `tw_short_sell` | YoY% | TWSE |

**美國（4 個）**:

| # | 變數 | 代碼 | 轉換 | FRED/來源 |
|---|------|------|------|----------|
| 42 | 美國聯邦基金利率 | `us_ffr` | Level% | FEDFUNDS |
| 43 | 美國工業生產指數 | `us_ipi` | YoY% | INDPRO |
| 44 | 美國信用利差 | `us_credit_spread` | Level bps | BAA10YM |
| 45 | 美國 EPU | `us_epu` | log | PolicyUncertainty |

**中國（3 個）**:

| # | 變數 | 代碼 | 轉換 | 來源 |
|---|------|------|------|------|
| 46 | 中國工業增加值 | `cn_ipi` | YoY% | FRED |
| 47 | 中國 PPI | `cn_ppi` | YoY% | NBS/CEIC |
| 48 | 中國 M2 年增率 | `cn_m2` | YoY% | FRED (MYAGM2TWM052N) |

**全球與貿易政策（4 個）**:

| # | 變數 | 代碼 | 轉換 | 來源 |
|---|------|------|------|------|
| 49 | VIX | `gl_vix` | log | FRED (VIXCLS) |
| 50 | GPR 地緣政治風險 | `gl_gpr` | log | Iacoviello |
| 51 | 全球 EPU | `gl_gepu` | log | PolicyUncertainty |
| 52 | US 貿易政策不確定 | `us_tpu` | log | BBD Categorical EPU #9 |

> **合計**: 22 macro + 8 financial + 22 unclassified = **52 個變數** ✅
> 
> 原目標 ~43，52 仍在 DHK 建議的 40+ 範圍內。若需精簡至 ~43，可考慮移除:
> - `tw_food_svc`（與零售高度相關）
> - `tw_short_sell`（資訊量有限）
> - `tw_turnover`（成交值，noise 較多）
> - `tw_margin_buy`（融資餘額，與股價高度相關）

---

## 資料下載進度（2026-05-01 更新）

### 已完成的下載腳本

| 腳本 | 來源 | 變數數 | 狀態 |
|------|------|--------|------|
| `fetch_fred.py` | FRED (CSV endpoint) | 5 | ✅ 完成 |
| `fetch_csv_sources.py` | PolicyUncertainty, Iacoviello | 4 | ✅ 完成 |
| `fetch_twse_taiex.py` | TWSE (TAIEX price index, turnover, total return index) | 4 + robustness series | ✅ 完成 |
| `fetch_cbc.py` | CBC 統計資料庫 API | 8 | ✅ 完成 |
| `fetch_stat_gov.py` | eng.stat.gov.tw | 19 | ✅ 完成 |
| `fetch_dgbas.py` | DGBAS nstatdb | prices, wages, hours, building/use permits | ✅ 完成 |
| `fetch_bis.py` | BIS SDMX API | 1 | ✅ 完成 |
| `fetch_china.py` | NBS/PBoC via Trading Economics | 3 | ✅ 完成 |

### 下載狀態：逐變數對照

#### ✅ 已下載（baseline raw data mostly complete）

**Taiwan Macro (19 series from stat.gov.tw)**:
- `tw_ipi`, `tw_mfg_prod`, `tw_export_orders`, `tw_retail_growth`, `tw_exports`, `tw_imports`
- `tw_cpi_index`, `tw_cpi_yoy`, `tw_core_cpi_yoy`, `tw_cpi_sa_mom`
- `tw_unemployment`, `tw_unemployment_sa`, `tw_employed`, `tw_payrolls`
- `tw_regular_wages`, `tw_total_wages`, `tw_working_hours`
- `tw_leading_index`, `tw_coincident_idx`

**Taiwan Macro (DGBAS nstatdb additions)**:
- `tw_import_prices`, `tw_export_prices`, `tw_wpi`, `tw_upstream_prices`
- `tw_mfg_emp`, `tw_svc_emp`
- `tw_mfg_regular_wages`, `tw_svc_regular_wages`, `tw_real_wages`
- `tw_mfg_hours`, `tw_svc_hours`
- `tw_building_permits_residential_area`, `tw_use_permits_residential_area`
- Auxiliary/robustness: `tw_building_permits_area`, `tw_use_permits_area`, `tw_building_permits_structure_area`, `tw_building_permits_value`

**Taiwan Financial (8 series from CBC + TWSE + FRED)**:
- `tw_overnight`, `tw_policy_rate`, `tw_10y_bond` (CBC)
- `tw_monetary` (M1B + M2, CBC), `tw_bank_loans`, `tw_consumer_loans` (CBC)
- `taiex` (TWSE: total-return baseline return/vol; price-index level and robustness return/vol; FMTQIK turnover)
- `tw_twdusd` (FRED: DEXTAUS)

**US (5 series from FRED + CSV)**:
- `us_ffr`, `us_ipi`, `us_credit_spread` (FRED)
- `us_epu`, `us_tpu` (PolicyUncertainty.com)

**China (3 series)**:
- `cn_ipi`, `cn_ppi`, `cn_m2`

**Global (4 series from various)**:
- `gl_vix` (FRED), `gl_gpr` (Iacoviello), `gl_gepu` (PolicyUncertainty)
- `tw_reer` (BIS)

#### ⚠️ 剩餘注意事項

| 變數 | 問題 | 建議解法 |
|------|------|---------|
| `tw_foreign_inv` 外資買賣超 | TWSE monthly aggregate starts in 2004M4 | 若維持 2003M1 baseline，需要截尾、補值或改作 robustness |
| `gl_gepu` 全球 EPU | 目前缺 2025M12 | 等 PolicyUncertainty 更新或截尾到 2025M11 |
| `tw_term_spread` 期限利差 | 已可由 `tw_10y_bond - tw_overnight` 計算 | 在 `build_dataset.py` 中 materialize |

### 技術備註

**stat.gov.tw API 機制** (新發現):
- 資料嵌入在 `ContentPlaceHolder1_hidChartData` 隱藏欄位中
- 每個 sid (t.1~t.12) 包含多個序列，以 JSON array 格式
- 無需認證，直接 GET 請求即可取得
- sid 對照: t.2=物價, t.3=勞動, t.4=薪資工時, t.5=生產零售, t.8=貿易, t.11=景氣

**CBC API (cpx.cbc.gov.tw)**:
- 4 步驟 session-based 流程: Range → GetJsonRangeData → SetJsonFromArray → GetJsonFromArray
- 回傳 double-encoded JSON, 需 `json.loads(r.json())`
- 多維交叉表需用 `itertools.product()` 建構欄名

**BIS REER**: `stats.bis.org/api/v1/data/WS_EER/M.R.B.TW?format=csv` (注意是 stats.bis.org 非 data.bis.org)

**DGBAS nstatdb**: JSON API 間歇性可用 (sys=220)，HTML 頁面持續 403。可用時用已知 funid 下載 WPI 等物價序列。

---

*Generated: 2026-04-09 | Decisions confirmed: 2026-04-09 | Download status updated: 2026-04-10*

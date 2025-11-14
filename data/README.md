# 資料管理說明

**建立日期**: 2025-11-14
**Phase**: Phase 1 - 資料收集
**目標**: 收集並整理40+變數的月度資料（約1990-2025）

---

## 📁 資料夾結構

```
data/
├── README.md                    # 本文件
├── data_dictionary.xlsx         # [將來建立] 變數定義與來源
│
├── raw/                        # 原始資料（不做任何處理）
│   ├── taiwan_macro/           # 台灣總體經濟變數（~19個）
│   ├── taiwan_financial/       # 台灣金融變數（~10個）
│   ├── taiwan_policy/          # 台灣政策與信用變數（~8個）
│   ├── us/                     # 美國變數（~4個）
│   ├── china/                  # 中國變數（~3個）
│   └── global/                 # 全球與美中關係變數（~3個）
│
├── cleaned/                    # 清理後資料
│   ├── taiwan_macro_cleaned.csv
│   ├── taiwan_financial_cleaned.csv
│   ├── taiwan_unclassified_domestic.csv
│   ├── us_variables.csv
│   ├── china_variables.csv
│   └── global_uscn_variables.csv
│
└── final/                      # 最終整合資料集
    └── final_dataset.csv       # 40+變數，~300-360月
```

---

## 📊 變數分類說明

### 台灣國內 - 明確歸類為總體經濟變數（~19個）

這些變數將在OI-SVMVAR模型中被分類為**"macroeconomic"**。

**來源**: 主計總處（DGBAS）、經濟部、國發會

| 變數 | 說明 | 來源 | 轉換 |
|------|------|------|------|
| IPI | 工業生產指數 | DGBAS | YoY成長率 |
| Manufacturing | 製造業生產指數 | DGBAS | YoY成長率 |
| Export Orders | 出口訂單指數 | DGBAS | YoY成長率 |
| Retail Sales | 零售業銷售額 | DGBAS | YoY成長率 |
| Food Service | 餐飲業銷售額 | DGBAS | YoY成長率 |
| Exports (Real) | 實質出口額（USD） | MOF | YoY成長率 |
| Imports (Real) | 實質進口額（USD） | MOF | YoY成長率 |
| PMI | 製造業採購經理人指數 | CIER | 水準值 |
| NMI | 非製造業經理人指數 | CIER | 水準值 |
| Business Cycle Signal | 景氣對策信號分數 | NDC | 水準值 |
| CPI | 消費者物價指數 | DGBAS | YoY成長率 |
| Core CPI | 核心CPI（扣除蔬果、能源） | DGBAS | YoY成長率 |
| WPI | 躉售物價指數 | DGBAS | YoY成長率 |
| Import Prices | 進口物價指數 | DGBAS | YoY成長率 |
| Export Prices | 出口物價指數 | DGBAS | YoY成長率 |
| Unemployment Rate | 失業率（季節調整） | DGBAS | 水準值(%) |
| Employment | 就業人數 | DGBAS | YoY成長率 |
| Manufacturing Wages | 製造業薪資（實質） | DGBAS | YoY成長率 |

---

### 台灣國內 - 明確歸類為金融變數（~10個）

這些變數將被分類為**"financial"**。

**來源**: 中央銀行（CBC）、台灣證券交易所（TWSE）

| 變數 | 說明 | 來源 | 轉換 |
|------|------|------|------|
| Overnight Rate | 隔夜拆款利率 | CBC | 水準值(%) |
| 10Y Bond Yield | 10年期公債殖利率 | CBC | 水準值(%) |
| Term Spread | 期限利差（10Y - Overnight） | 計算 | 水準值(bps) |
| TAIEX Return | 台股加權指數月報酬率 | TWSE | 月報酬率(%) |
| TAIEX Volatility | 台股波動率（標準差） | TWSE | 月度標準差 |
| Trading Volume | 平均日成交值 | TWSE | YoY成長率 |
| Foreign Investment | 外資淨買賣金額 | TWSE | 月度淨額 |
| Margin Trading | 融資餘額 | TWSE | YoY成長率 |
| Short Selling | 融券餘額 | TWSE | YoY成長率 |

---

### 台灣國內 - 未分類變數（政策與信用，~8個）

這些變數性質模糊，將被分類為**"unclassified"**。

**來源**: 中央銀行（CBC）、信義房價指數

| 變數 | 說明 | 來源 | 轉換 |
|------|------|------|------|
| Rediscount Rate | 央行重貼現率（政策利率） | CBC | 水準值(%) |
| M1b Growth | M1b貨幣供給成長率 | CBC | YoY成長率 |
| M2 Growth | M2貨幣供給成長率 | CBC | YoY成長率 |
| Bank Loans | 銀行放款與投資總額 | CBC | YoY成長率 |
| Consumer Loans | 消費者貸款 | CBC | YoY成長率 |
| TAIEX Level | 台股指數水準（非報酬） | TWSE | Log水準 |
| Credit Spread | 信用利差（企業債-公債） | 計算 | 水準值(bps) |
| Housing Prices | 房價指數 | Cathay/Sinyi | YoY成長率 |
| TWD/USD | 新台幣兌美元匯率 | CBC | Log水準 |
| TWD Volatility | 匯率波動率 | 計算 | 月度標準差 |
| REER | 實質有效匯率指數 | BIS/CBC | Log水準 |

---

### 外部變數 - 美國（~4個）

**全部歸類為"unclassified"** - 這是核心創新！

**來源**: FRED (Federal Reserve Economic Data)

| 變數 | 說明 | FRED代碼 | 轉換 |
|------|------|---------|------|
| US FFR | 美國聯邦基金利率 | FEDFUNDS | 水準值(%) |
| US IPI | 美國工業生產指數 | INDPRO | YoY成長率 |
| US Credit Spread | BAA-AAA信用利差 | BAA-AAA | 水準值(bps) |
| US EPU | 美國經濟政策不確定性指數 | 見網站 | Log水準 |

**US EPU來源**: https://www.policyuncertainty.com/us_monthly.html

---

### 外部變數 - 中國（~3個）

**全部歸類為"unclassified"**

**來源**: 中國國家統計局（NBS）、CEIC、FRED

| 變數 | 說明 | 來源 | 轉換 |
|------|------|------|------|
| China IPI | 中國工業增加值 | NBS/FRED | YoY成長率 |
| China PPI | 中國生產者物價指數 | NBS/CEIC | YoY成長率 |
| China TSF | 中國社會融資總量存量 | PBOC/CEIC | YoY成長率 |

**注意**: 中國資料2000年前可能有缺失，需特別處理。

---

### 外部變數 - 全球與美中關係（~3個）

**全部歸類為"unclassified"**

| 變數 | 說明 | 來源 | 轉換 |
|------|------|------|------|
| VIX | 美國波動率指數 | FRED (VIXCLS) | Log水準 |
| GPR | 地緣政治風險指數 | matteoiacoviello.com/gpr.htm | Log水準 |
| US-China TPU | 美中貿易政策不確定性 | PolicyUncertainty.com | Log水準 |
| Global EPU | 全球經濟政策不確定性 | PolicyUncertainty.com | Log水準 |

---

## 🔄 資料處理流程

### Step 1: 原始資料下載（raw/）

**原則**:
- 下載最原始的資料（不做任何處理）
- 每個檔案附上下載日期與來源URL
- 使用統一命名格式：`[變數名]_raw.csv`

**檔名範例**:
- `ipi_raw.csv`
- `cpi_raw.csv`
- `fedfunds_raw.csv`

**必須包含的metadata**:
- 下載日期
- 資料來源URL
- 原始頻率（月度、日度等）
- 原始基期（如2020=100）

---

### Step 2: 資料清理（cleaned/）

**處理步驟**（由code/data_processing/執行）:

1. **日期標準化**: 轉換為YYYY-MM格式
2. **變數轉換**:
   - YoY成長率：`(X_t / X_{t-12} - 1) * 100`
   - Log水準：`log(X_t)`
   - 月報酬率：`(P_t / P_{t-1} - 1) * 100`
   - 波動率：使用日度資料計算月度標準差
3. **季節調整**: 使用X-13-ARIMA（若需要）
4. **定態性檢定**: ADF test, PP test
5. **缺失值檢查**: 記錄缺失比例
6. **異常值偵測**: 檢查極端值（>3σ）

**輸出檔案**:
- `taiwan_macro_cleaned.csv`（19變數）
- `taiwan_financial_cleaned.csv`（10變數）
- `taiwan_unclassified_domestic.csv`（11變數）
- `us_variables.csv`（4變數）
- `china_variables.csv`（3變數）
- `global_uscn_variables.csv`（4變數）

每個檔案包含：
- `date`欄位（YYYY-MM）
- 各變數欄位（已轉換）
- 變數命名：小寫字母+底線（如`ipi_yoy`, `cpi_yoy`）

---

### Step 3: 資料整合（final/）

**Milestone 1.7任務**（由code/data_processing/05_merge_final.R執行）:

1. **日期對齊**: 找出所有變數的共同時間範圍
   - 目標：1995-01 至 2025-10（或最長可用範圍）
   - 預期觀察值：~300-360個月

2. **缺失值處理**:
   - 檢查缺失模式
   - 決策：刪除 vs. 插補 vs. 縮短樣本期間

3. **標準化**:
   - 所有變數標準化為 mean=0, sd=1
   - 記錄原始mean和sd（用於事後還原）

4. **最終驗證**:
   - 檢查所有變數無缺失
   - 檢查無極端異常值
   - 產生描述統計表

**輸出**:
- `final_dataset.csv`（主檔案，40+變數 × ~300-360月）
- `final_dataset_metadata.txt`（時間範圍、變數數、觀察值數）
- `standardization_parameters.csv`（每個變數的原始mean和sd）

---

## 📋 資料品質檢查清單

### 原始資料（raw/）檢查
- [ ] 所有檔案都有下載日期記錄
- [ ] 所有檔案都有來源URL記錄
- [ ] 日期範圍符合預期（至少1990-2025）
- [ ] 無明顯錯誤（如負的CPI、超過100%的失業率）

### 清理後資料（cleaned/）檢查
- [ ] 所有變數都已正確轉換（YoY, log等）
- [ ] 定態性檢定通過（p-value < 0.05 for ADF）
- [ ] 缺失值比例 < 5%
- [ ] 無極端異常值（或已記錄並解釋）

### 最終資料（final/）檢查
- [ ] 所有變數無缺失值
- [ ] 所有變數已標準化（mean≈0, sd≈1）
- [ ] 時間範圍一致（所有變數相同起訖日期）
- [ ] 描述統計表已產生
- [ ] 相關矩陣熱圖已產生

---

## 📊 預期產出（Milestone 1.7）

1. **最終資料集**: `final_dataset.csv`
   - 維度：300-360 rows × 40+ columns
   - 格式：date, var1, var2, ..., var40+

2. **資料字典**: `data_dictionary.xlsx`
   - 欄位：Variable Name, Description, Source, Transformation, Classification

3. **描述統計**: `descriptive_statistics.tex`
   - 表格：Mean, SD, Min, Max, N for each variable
   - 用於論文附錄

4. **相關矩陣**: `figures/correlation_heatmap.pdf`
   - 40+ × 40+熱圖
   - 用於初步探索性分析

---

## 🔗 相關程式碼

- `code/data_processing/01_download_taiwan.R` - 台灣資料下載
- `code/data_processing/02_download_us.R` - 美國資料下載
- `code/data_processing/03_download_china.R` - 中國資料下載
- `code/data_processing/04_clean_stationarity.R` - 清理與定態性檢定
- `code/data_processing/05_merge_final.R` - 整合最終資料集

---

## ⚠️ 重要提醒

### 資料來源可靠性
- **台灣DGBAS**: 非常可靠，官方統計
- **FRED**: 極可靠，Fed官方
- **中國NBS**: 可靠但需注意修正（中國常回溯修正資料）
- **EPU, GPR指數**: 學術界廣泛使用，可靠

### 資料頻率
- **全部使用月度資料**（不使用季度）
- 如有日度資料（如TAIEX），先彙總為月度再使用

### 缺失值策略
- **原則**: 優先使用完整資料，避免插補
- **例外**: 如單一變數缺失<5%且重要，可考慮線性插補
- **最終決策**: 記錄在data_dictionary.xlsx

### 樣本期間
- **理想**: 1990-01 至 2025-10（35年）
- **最低要求**: 2000-01 至 2025-10（25年）
- **實際**: 取決於中國資料可得性（2000年前可能缺失）

---

**最後更新**: 2025-11-14
**維護者**: Phase 1 Data Collection Team

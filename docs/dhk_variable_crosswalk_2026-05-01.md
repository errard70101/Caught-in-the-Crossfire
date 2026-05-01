# DHK (2025) OI-SVMVAR 變數對照表

**目的**: 在最終確認台灣 OI-SVMVAR 變數前，將目前 52 個 baseline candidate 變數與 Davidson, Hou, and Koop (2025) 原始 OI-TVC-43 變數架構逐項對照。

**本專案目前配置**: 52 variables = 22 macro + 8 financial + 22 unclassified。  
**DHK OI-TVC-43 配置**: 43 variables = 17 fixed macro + 10 fixed financial + 16 unclassified。

資料來源:
- Davidson, Hou, and Koop (2025), *Journal of Business and Economic Statistics*, 43(4), 992-1007.
- Strathprints accepted manuscript / appendix table: Table 2, "Description of the Data".

---

## 1. 核心結論

目前台灣變數與 DHK 原始設計在「角色架構」上可以對應：

| 面向 | DHK OI-TVC-43 | 本專案台灣配置 | 判斷 |
|---|---:|---:|---|
| 固定 macro block | 17 | 22 | 可對應，台灣端更強調產業、貿易、薪資、工時與住宅建築活動 |
| 固定 financial block | 10 | 8 | 可對應，但不是 Fama-French 複製；改用台灣市場金融狀態 |
| unclassified block | 16 | 22 | 高度對應；並加入本研究的外部衝擊來源 |
| 總變數數 | 43 | 52 | 仍符合 large model / 40+ variables 的精神 |

最重要的對應關係是：

1. DHK 將 **FFR, S&P 500, credit spread, money, credit, house price, term spreads, exchange rates** 放入 unclassified；我們已經用台灣對應變數完整保留這個設計。
2. 本專案額外把 **US/China/global/US-China uncertainty variables** 放入 unclassified，這不是偏離 DHK，而是本研究「外部衝擊傳導管道」的核心創新。
3. 台灣 financial block 無法自然複製 DHK 的 Fama-French equity factors；以 TAIEX return/volatility/turnover/foreign flow/margin 作為台灣金融市場狀態，是比較合理的在地化版本。

---

## 2. DHK 原始 OI-TVC-43 變數

### 2.1 Fixed macro variables

| DHK code | DHK label | Transformation | 台灣對應 |
|---|---|---|---|
| `PAYEMS` | All employees: total nonfarm | d log | `tw_mfg_emp`, `tw_svc_emp` |
| `INDPRO` | Industrial production index | d log | `tw_ipi`, `tw_mfg_prod` |
| `CUMFNS` | Capacity utilization: manufacturing | d | 部分由 `tw_mfg_prod` 承接；目前無直接產能利用率 |
| `HWIURATIO` | Help wanted-to-unemployed ratio | d | 目前無直接對應；可視為勞動市場 tightness 缺口 |
| `UNRATE` | Unemployment rate | d | `tw_unemp` |
| `RPI` | Real personal income | d log | `tw_mfg_wages`, `tw_svc_wages` 部分承接 |
| `CES0600000007` | Weekly hours: goods producing | level | `tw_mfg_hours`, `tw_svc_hours` |
| `HOUST` | Housing starts | log | `tw_use_permits_residential_area` |
| `PERMIT` | Housing permits | log | `tw_building_permits_residential_area` |
| `DPCERA3M086SBEA` | Real consumer spending | d log | `tw_retail`, `tw_food_svc` |
| `CMRMTSPLx` | Real manufacturing trade sales | d log | `tw_exports_usd`, `tw_imports_usd`, `tw_export_orders` |
| `NAPMNOI` | ISM new orders index | level | `tw_export_orders`; PMI/NMI 因起始太晚已排除 |
| `AMDMNOx` | Orders for durable goods | d log | `tw_export_orders`, `tw_mfg_prod` |
| `CES0600000008` | Avg. hourly earnings, goods producing | d2 log | `tw_mfg_wages`, `tw_svc_wages` |
| `WPSFD49207` | PPI, finished goods | d2 log | `tw_upstream_prices` |
| `PPICMM` | PPI, commodities | d2 log | `tw_upstream_prices`, `tw_import_prices`, `tw_export_prices` |
| `PCEPI` | PCE price index | d2 log | `tw_cpi`, `tw_core_cpi` |

### 2.2 Fixed financial variables

| DHK code | DHK label | Transformation | 台灣對應 |
|---|---|---|---|
| `excessreturn` | Excess return | level | `tw_taiex_ret` |
| `SMB` | Fama-French SMB factor | level | 無直接對應；可由台股個股資料自建，但目前不建議作 baseline |
| `HML` | Fama-French HML factor | level | 無直接對應；可由台股個股資料自建，但目前不建議作 baseline |
| `momentum` | Momentum factor | level | 無直接對應；可由台股個股資料自建，但目前不建議作 baseline |
| `R15_R11` | Small stock value spread | level | 無直接對應 |
| `aggind1` | Industry 1 return | level | `tw_taiex_ret` 部分承接；若要更接近 DHK 可加入產業指數報酬 |
| `aggind2` | Industry 2 return | level | 同上 |
| `aggind3` | Industry 3 return | level | 同上 |
| `aggind4` | Industry 4 return | level | 同上 |
| `aggind5` | Industry 5 return | level | 同上 |

目前台灣 fixed financial block 的替代設計：

| 台灣變數 | 角色 |
|---|---|
| `tw_taiex_ret` | 股票市場報酬，對應 DHK equity return |
| `tw_taiex_vol` | 股票市場 realized volatility，補強金融不確定性訊號 |
| `tw_turnover` | 市場交易活絡程度 |
| `tw_foreign_inv` | 外資流向，台灣金融傳導關鍵變數 |
| `tw_margin_buy` | 槓桿/散戶信用交易 |
| `tw_overnight` | 短期金融條件 |
| `tw_10y_bond` | 長端殖利率 |
| `tw_term_spread` | 利率曲線狀態 |

### 2.3 Unclassified variables

| DHK code | DHK label | Transformation | 台灣/本研究對應 |
|---|---|---|---|
| `S&P 500` | S&P 500 | d log | `tw_taiex_level`；外部端另有 `gl_vix` |
| `BAAT10Y` | Baa - 10y Treasury spread | level | `us_credit_spread`；台灣信用利差因資料太晚已排除 |
| `FEDFUNDS` | Federal funds rate | d | `tw_policy_rate`, `us_ffr` |
| `BOGMBASE` | Monetary base | d2 log | 台灣無 baseline；由 `tw_m1b`, `tw_m2` 承接貨幣面 |
| `M1 Real` | Real M1 money stock | d2 log | `tw_m1b` |
| `M2 Real` | Real M2 money stock | d2 log | `tw_m2` |
| `CONSUMER` | Consumer loans | d2 log | `tw_consumer_loans` |
| `BUSLOANS` | Commercial and industrial loans | d2 log | `tw_bank_loans` |
| `NONREVSL` | Total nonrevolving credit | d2 log | `tw_consumer_loans` 部分承接 |
| `RHPI` | Real house price index | d log | `tw_house_prices` |
| `GS10TB3Mx` | 10y Treasury - 3m T-bill | level | `tw_term_spread` |
| `TB3SMFFM` | 3m Treasury - FFR | level | 無直接對應；短端政策/市場利差可由 `tw_overnight`, `tw_policy_rate` 派生 |
| `AAAFFM` | Aaa corporate bond - FFR | level | 無直接對應；台灣公司債信用利差資料太晚 |
| `EXSZUSx` | CHF/USD exchange rate | d log | `tw_twdusd`, `tw_reer` |
| `EXUSUKx` | GBP/USD exchange rate | d log | `tw_twdusd`, `tw_reer` |
| `EXCAUSx` | CAD/USD exchange rate | d log | `tw_twdusd`, `tw_reer` |

本專案新增、但 DHK 沒有的 unclassified 外部衝擊來源：

| 變數 | 理由 |
|---|---|
| `us_ipi` | 美國實體需求/景氣來源 |
| `us_epu` | 美國政策不確定性 |
| `cn_ipi` | 中國實體需求/供應鏈來源 |
| `cn_ppi` | 中國上游價格與供應壓力 |
| `cn_m2` | 中國金融/信用環境 |
| `gl_vix` | 全球金融風險 |
| `gl_gpr` | 全球地緣政治風險 |
| `gl_gepu` | 全球政策不確定性 |
| `us_tpu` | 美國貿易政策不確定性；美中貿易戰管道 |
| `tw_fx_vol` | 匯率不確定性，對小型開放經濟體特別重要 |
| `tw_short_sell` | 台灣市場下行/避險交易訊號 |

---

## 3. 對應完整度評估

### 3.1 已高度對應

| DHK 構面 | 本專案變數 |
|---|---|
| 工業生產 | `tw_ipi`, `tw_mfg_prod` |
| 就業/失業 | `tw_mfg_emp`, `tw_svc_emp`, `tw_unemp` |
| 工時 | `tw_mfg_hours`, `tw_svc_hours` |
| 薪資/所得 | `tw_mfg_wages`, `tw_svc_wages` |
| 消費/銷售 | `tw_retail`, `tw_food_svc` |
| 訂單/貿易 | `tw_export_orders`, `tw_exports_usd`, `tw_imports_usd` |
| 物價 | `tw_cpi`, `tw_core_cpi`, `tw_upstream_prices`, `tw_import_prices`, `tw_export_prices` |
| 股市 | `tw_taiex_ret`, `tw_taiex_vol`, `tw_taiex_level` |
| 利率/利差 | `tw_overnight`, `tw_10y_bond`, `tw_term_spread`, `tw_policy_rate` |
| 貨幣/信用 | `tw_m1b`, `tw_m2`, `tw_bank_loans`, `tw_consumer_loans` |
| 房價 | `tw_house_prices` |
| 住宅建築活動 | `tw_building_permits_residential_area`, `tw_use_permits_residential_area` |
| 匯率 | `tw_twdusd`, `tw_reer`, `tw_fx_vol` |

### 3.2 與 DHK 不完全一致，但合理

| 差異 | 說明 | 建議 |
|---|---|---|
| 沒有 Fama-French SMB/HML/momentum | 台灣要自建長樣本個股因子，資料成本高且可能改變專案重心 | 不納入 baseline；必要時作 robustness |
| 沒有 5 個產業股票報酬 | DHK 用美國產業報酬補足金融市場橫斷面 | 可考慮加入台股產業指數報酬，但目前 52 變數已足夠 |
| 沒有台灣信用利差 | 公司債資料起始太晚，會犧牲樣本 | 保持刪除；用 `tw_term_spread`, `us_credit_spread` 承接 |
| 沒有直接 capacity utilization | 台灣長樣本月資料需再查 | 不是必要缺口；`tw_mfg_prod` 可部分承接 |
| 沒有 help wanted-to-unemployed ratio | 台灣職缺/求才資料可能晚或斷裂 | 不是必要缺口；可列為未來 robustness |
| 住宅建築活動不是件數而是樓地板面積 | 台灣目前採用建造/使用執照住宅樓地板面積，比件數更能反映建築活動規模 | 保留作 baseline candidate；總面積與工程造價作 robustness |

### 3.3 本研究有意識地超出 DHK 的部分

| 新增構面 | 變數 | 為何合理 |
|---|---|---|
| 美國外部衝擊 | `us_ffr`, `us_ipi`, `us_credit_spread`, `us_epu`, `us_tpu` | 台灣是小型開放經濟體，外部變數不可省略 |
| 中國外部衝擊 | `cn_ipi`, `cn_ppi`, `cn_m2` | 捕捉中國需求、價格、金融條件 |
| 全球風險 | `gl_vix`, `gl_gpr`, `gl_gepu` | 捕捉非單一國家的全球不確定性 |
| 匯率不確定性 | `tw_fx_vol` | DHK 有多個匯率；台灣更需要匯率水準與波動 |
| 台灣市場資金流 | `tw_foreign_inv`, `tw_margin_buy`, `tw_short_sell` | 台灣金融市場對外資與信用交易高度敏感 |

---

## 4. 對最終變數確認的建議

### 4.1 Baseline candidate 可以維持目前 52 變數

目前版本不是「偏離原論文」，而是「依照 DHK 變數角色做台灣化與小型開放經濟體擴充」。特別是 unclassified block 的設計，與 DHK 原始精神最一致。

### 4.2 真正需要決定的不是是否能對應，而是是否要再靠近 DHK

若要更貼近原論文，有三個可選補強方向：

| 優先度 | 補強 | 可能變數 | 評估 |
|---|---|---|---|
| 低 | 產能利用率 | 製造業產能利用率 | 若能找到長月資料可加入，否則用生產指數替代 |
| 低 | 股票橫斷面因子 | 台股 SMB/HML/momentum 或產業報酬 | 資料工程成本高；不建議作 baseline |

### 4.3 最終論文中的說法

建議將變數設計表述為：

> We follow Davidson, Hou, and Koop (2025) in organizing variables into fixed macroeconomic, fixed financial, and unclassified blocks. The domestic Taiwanese variables are selected to mirror the real activity, labor market, price, financial market, monetary, credit, housing, interest-rate, and exchange-rate information contained in the original U.S. OI-TVC-43 specification. We depart from the original U.S. application by placing external U.S., China, and global variables in the unclassified block, allowing the model to determine whether each external shock source transmits to Taiwan through macroeconomic or financial uncertainty over time.

---

## 5. 下一步

1. 保留目前 52 變數作為 baseline candidate。
2. 不再把「是否能對應 DHK」視為主要疑慮；目前架構已能對應。
3. 最後確認前，只需決定建照/使照採住宅樓地板面積或總樓地板面積；目前 baseline candidate 採住宅樓地板面積。

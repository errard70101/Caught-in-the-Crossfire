# 當前進行中的任務

**更新時間**: 2025-11-16 (by Claude - session: economic-uncertainty-paper-plan-01Fzd3sUR5qhsCJELNawabmx)
**當前Phase**: Phase 2.1 - DHK (2025) Paper Replication

---

## 🔴 進行中 (In Progress)

### 無

---

## 🟡 待開始 (Ready to Start)

### 📌 DHK (2025) Replication Tasks - HIGH PRIORITY

### Task-DHK-001: Review DHK Replication Plan
- **任務ID**: DHK-PLAN-001
- **優先級**: P0 (最高 - 需要人類決策)
- **負責**: User
- **預計時間**: 2-3 hours
- **階段**: Phase 2.1 準備

**說明**:
閱讀並討論DHK (2025) paper replication plan。需要做出關鍵決策才能開始實施。

**文件位置**:
- 📄 **Executive Summary**: `docs/DHK_REPLICATION_SUMMARY.md` ← START HERE
- 📄 **Full Plan**: `llm_logs/2025-11-16_DHK_replication_plan.md`
- 📄 **Technical Instructions**: `code/DHK_original/MODULE_INSTRUCTIONS.md`
- 📄 **User Guide**: `code/DHK_original/README.md`

**需要決策的問題**:
1. **程式語言**: R (推薦) vs MATLAB vs Python?
2. **時程**: 3-4個月可接受嗎？
3. **複製程度**: 完整複製 vs 重點複製 vs 最小可行複製？
4. **運算資源**: 有HPC cluster嗎？還是用個人電腦？
5. **實施者**: 你會寫code？還是需要完整程式碼？
6. **聯繫作者**: 是否寫信向DHK作者索取replication code？

**檢查清單**:
- [ ] 閱讀 DHK_REPLICATION_SUMMARY.md
- [ ] 瀏覽 2025-11-16_DHK_replication_plan.md (14,000字)
- [ ] 理解8個modules結構
- [ ] 回答6個決策問題
- [ ] 與Claude討論plan
- [ ] 批准或修改plan

---

### Task-DHK-002: 決定程式語言並設定開發環境
- **任務ID**: DHK-SETUP-001
- **優先級**: P1 (高)
- **負責**: 待分配
- **預計時間**: 3-4 hours
- **階段**: Module 0 - Setup
- **前置任務**: Task-DHK-001 (plan approval)

**說明**:
選擇程式語言（推薦R）並安裝所有必要套件和開發環境。

**如果選擇R**:
```r
# 1. 安裝R和RStudio
# 2. 安裝必要套件
install.packages(c(
  "Matrix",      # 稀疏矩陣
  "spam",        # 帶狀矩陣 (速度關鍵!)
  "mvtnorm",     # 多元常態分佈
  "MCMCpack",    # MCMC工具
  "coda",        # 收斂診斷
  "ggplot2",     # 視覺化
  "dplyr", "tidyr"  # 資料處理
))
```

**檢查清單**:
- [ ] 決定語言: R / MATLAB / Python
- [ ] 下載安裝IDE (RStudio / MATLAB / VSCode)
- [ ] 安裝所需套件/toolboxes
- [ ] 測試basic functionality
- [ ] 設定git workflow for code
- [ ] 記錄在 code/DHK_original/setup/installation_log.md

---

### Task-DHK-003: 聯繫DHK作者索取replication code
- **任務ID**: DHK-CONTACT-001
- **優先級**: P1 (高 - 可平行進行)
- **負責**: User (需人類執行)
- **預計時間**: 1 hour (撰寫 + 等待數週)
- **階段**: Module 0 - Setup
- **前置任務**: 無 (可立即開始)

**說明**:
聯繫Davidson, Hou, Koop (2025)作者，禮貌地請求提供OI-SVMVAR replication code。即使獲得code，仍需深入理解才能adapt to Taiwan。

**作者資訊**:
- **Sharada Nia Davidson**: University of Strathclyde
- **Chenghan Hou**: Hunan University (chenghan.hou@hotmail.com)
- **Gary Koop**: University of Strathclyde
- **Journal**: Journal of Business & Economic Statistics (2025)
- **DOI**: 10.1080/07350015.2025.2455064

**Email要點**:
- [ ] 簡短自我介紹（PhD student/researcher）
- [ ] 說明研究目的：applying DHK framework to Taiwan (small open economy)
- [ ] 禮貌請求replication code (MATLAB/R/Python)
- [ ] 表示願意引用致謝
- [ ] 提及online appendix是否包含code

**備註**: Claude可協助撰寫email草稿，但需要你發送。

---

### Task-DHK-004: 下載FRED-MD資料集
- **任務ID**: DHK-M1-001
- **優先級**: P1 (高)
- **負責**: 待分配
- **預計時間**: 2 hours
- **階段**: Module 1 - Data Collection
- **前置任務**: Task-DHK-002 (development environment)

**說明**:
下載FRED-MD monthly dataset (1960-2021)，extract 43 variables用於empirical application。

**資料來源**:
- Website: https://research.stlouisfed.org/econ/mccracken/fred-databases/
- Direct download: https://files.stlouisfed.org/files/htdocs/fred-md/monthly/current.csv
- Documentation: FRED-MD appendix

**Variable List** (from Online Appendix B):
- 30-variable baseline (CCM model)
- 43-variable extended (OI-TVC-43 model)
- Classification: 18 macro, 12 financial, 13 unclassified

**檢查清單**:
- [ ] 下載current FRED-MD dataset
- [ ] Extract subset: 1960-01 to 2021-10
- [ ] Verify 43 variables present
- [ ] 儲存至 data/raw/fredmd_raw.csv
- [ ] 記錄download date and source
- [ ] Create variable classification file
- [ ] 更新 data/README.md

**輸出檔案**:
- `data/raw/fredmd_raw.csv`
- `data/processed/variable_list_43var.csv`
- `data/processed/classification_scheme.csv`

---

### Task-DHK-005: 資料轉換與標準化
- **任務ID**: DHK-M1-002
- **優先級**: P1 (高)
- **負責**: 待分配
- **預計時間**: 3 hours
- **階段**: Module 1 - Data Processing
- **前置任務**: Task-DHK-004

**說明**:
Apply transformation codes (log, first difference, etc.) to each FRED-MD variable, then standardize to zero mean and unit variance.

**Transformation Codes** (from FRED-MD):
- 1: No transformation
- 2: First difference
- 4: Log
- 5: First difference of log
- etc.

**Standardization**:
- Mean = 0, SD = 1 for each variable
- **Critical**: Save mean and SD for later rescaling of IRFs

**檢查清單**:
- [ ] 實施 `code/DHK_original/data_processing/02_transform_data.R`
- [ ] Apply correct transformation to each variable
- [ ] 檢查stationarity (ADF test optional)
- [ ] Standardize: (x - mean)/sd
- [ ] Save transformation parameters
- [ ] Create 6-var, 30-var, 43-var subsets
- [ ] 儲存processed data

**輸出檔案**:
- `data/processed/fredmd_transformed.csv`
- `data/processed/fredmd_standardized.csv`
- `data/processed/transformation_params.csv` (mean, sd for each variable)
- `data/processed/test_6var.csv` (for testing)

---

### Task-DHK-006: 實施Model Equations
- **任務ID**: DHK-M2-001
- **優先級**: P1 (高)
- **負責**: 待分配
- **預計時間**: 40 hours (1-2 weeks)
- **階段**: Module 2 - Model Specification
- **前置任務**: Task-DHK-002

**說明**:
Implement core OI-SVMVAR equations (1)-(7) from DHK paper. This is foundational for all MCMC steps.

**Equations to Implement**:
1. Equation (1): VAR with SV in mean
2. Equation (2): Covariance structure
3. Equations (3)-(5): Volatility decomposition (macro, financial, unclassified)
4. Equation (6): Common volatility dynamics
5. Equation (7): Idiosyncratic volatilities

**參考**:
- Paper: Section 2.1
- Instructions: `code/DHK_original/MODULE_INSTRUCTIONS.md` - Module 2

**檢查清單**:
- [ ] Create `code/DHK_original/model/svmvar_equations.R`
- [ ] Implement create_lags() function
- [ ] Implement compute_var_mean() - Equation (1)
- [ ] Implement compute_covariance_matrix() - Equation (2)
- [ ] Implement decompose_volatility() - Equations (3)-(5)
- [ ] Implement compute_h_mean() - Equation (6)
- [ ] Implement AR(1) for idiosyncratic - Equation (7)
- [ ] Test on toy 6-variable example
- [ ] Write unit tests

---

### 🔥 Task-DHK-007: 實施B0 Sampler (Order-Invariant Algorithm)
- **任務ID**: DHK-M3-001
- **優先級**: P1 (最高 - CRITICAL)
- **負責**: 待分配
- **預計時間**: 80 hours (2 weeks intensive)
- **階段**: Module 3 - MCMC Algorithm
- **前置任務**: Task-DHK-006

**說明**:
實施DHK paper的核心創新：order-invariant B0 sampler using parameter transformation. **This is the hardest task.**

**Algorithm Steps** (Section 2.2):
1. Transform b̃0,i to w (Equation 14)
2. Sample w1 from absolute normal (Proposition 1)
3. Sample w_{-1} from conditional Gaussian (Equation 18)
4. Transform back to b̃0,i (Equation 15)

**Key Challenge**: Absolute normal distribution requires mixture approximation (Villani 2009, Appendix C)

**參考**:
- Paper: Section 2.2, Equations (8)-(18), Proposition 1
- Instructions: MODULE_INSTRUCTIONS.md - M3.1

**檢查清單**:
- [ ] Study Section 2.2 thoroughly
- [ ] Implement transform_b_to_w() - Equation (14)
- [ ] Implement sample_absolute_normal() - Proposition 1
- [ ] Implement sample_w_minus1() - Equation (18)
- [ ] Implement transform_w_to_b() - Equation (15)
- [ ] Assemble sample_B0_row()
- [ ] Implement sample_B0() (loop over all rows)
- [ ] Test on synthetic data with known B0
- [ ] Verify: diagonal elements = 1
- [ ] Check acceptance rate (target: 30-50%)

**Success Criterion**: Algorithm recovers known B0 in simulation

---

### Task-001: 下載台灣工業生產指數（IPI）
- **任務ID**: DATA-1.1.1
- **優先級**: P1 (高)
- **負責**: 待分配
- **預計時間**: 2小時
- **階段**: Milestone 1.1.1

**說明**:
從DGBAS（主計總處）下載台灣工業生產指數、製造業生產指數、出口訂單月度資料（1990-2025）。

**前置任務**: Task-000 (需要data/資料夾)

**資料來源**:
- 網站: https://statdb.dgbas.gov.tw
- 資料庫: 國民所得及經濟成長 → 工業生產指數

**檢查清單**:
- [ ] 訪問DGBAS統計資料庫
- [ ] 下載工業生產指數（月度，2020=100）
- [ ] 下載製造業生產指數
- [ ] 下載出口訂單指數
- [ ] 儲存原始資料至data/raw/taiwan_macro/
- [ ] 記錄資料來源URL和下載日期
- [ ] 初步檢查資料完整性（缺失值、時間範圍）
- [ ] 更新data/README.md

**輸出檔案**:
- `data/raw/taiwan_macro/ipi_raw.csv`
- `data/raw/taiwan_macro/manufacturing_production_raw.csv`
- `data/raw/taiwan_macro/export_orders_raw.csv`

---

### Task-002: 下載台灣CPI、WPI物價資料
- **任務ID**: DATA-1.1.6
- **優先級**: P1 (高)
- **負責**: 待分配
- **預計時間**: 1.5小時
- **階段**: Milestone 1.1.6

**說明**:
從DGBAS下載CPI（消費者物價指數）、Core CPI（核心CPI）、WPI（躉售物價指數）月度資料。

**前置任務**: Task-000

**檢查清單**:
- [ ] 下載CPI總指數（2021=100）
- [ ] 下載核心CPI（不含蔬果、能源）
- [ ] 下載WPI（2021=100）
- [ ] 儲存至data/raw/taiwan_macro/
- [ ] 記錄資料來源
- [ ] 檢查資料完整性

**輸出檔案**:
- `data/raw/taiwan_macro/cpi_raw.csv`
- `data/raw/taiwan_macro/core_cpi_raw.csv`
- `data/raw/taiwan_macro/wpi_raw.csv`

---

### Task-003: 下載台灣失業率與就業資料
- **任務ID**: DATA-1.1.8
- **優先級**: P1 (高)
- **負責**: 待分配
- **預計時間**: 1小時
- **階段**: Milestone 1.1.8

**說明**:
從DGBAS下載失業率（經季節調整）、就業人數月度資料。

**前置任務**: Task-000

**檢查清單**:
- [ ] 下載失業率（經季節調整）
- [ ] 下載就業人數（千人）
- [ ] 儲存至data/raw/taiwan_macro/
- [ ] 記錄資料來源
- [ ] 檢查資料完整性

**輸出檔案**:
- `data/raw/taiwan_macro/unemployment_rate_raw.csv`
- `data/raw/taiwan_macro/employment_raw.csv`

---

### Task-004: 下載美國聯邦基金利率（FFR）
- **任務ID**: DATA-1.4.1
- **優先級**: P1 (高) - **建議最先執行（最簡單）**
- **負責**: 待分配
- **預計時間**: 30分鐘
- **階段**: Milestone 1.4.1

**說明**:
從FRED下載美國聯邦基金利率（Federal Funds Rate）月度資料。這是最簡單的資料下載任務，建議作為練習。

**前置任務**: Task-000

**資料來源**:
- 網站: https://fred.stlouisfed.org
- Series ID: FEDFUNDS
- 頻率: Monthly
- 時間範圍: 1990-01 to 2025-10

**檢查清單**:
- [ ] 訪問FRED網站
- [ ] 搜尋FEDFUNDS系列
- [ ] 下載CSV格式（1990-2025）
- [ ] 儲存至data/raw/us/
- [ ] 記錄資料來源
- [ ] 檢查資料完整性

**輸出檔案**:
- `data/raw/us/fedfunds_raw.csv`

**備註**: 此任務最簡單，可作為熟悉FRED資料下載流程的練習。

---

### Task-005: 下載美國工業生產指數（US IPI）
- **任務ID**: DATA-1.4.2
- **優先級**: P1 (高)
- **負責**: 待分配
- **預計時間**: 30分鐘
- **階段**: Milestone 1.4.2

**說明**:
從FRED下載美國工業生產指數月度資料。

**前置任務**: Task-000

**資料來源**:
- Series ID: INDPRO
- 頻率: Monthly

**檢查清單**:
- [ ] 下載FRED INDPRO系列
- [ ] 儲存至data/raw/us/
- [ ] 記錄資料來源
- [ ] 檢查資料完整性

**輸出檔案**:
- `data/raw/us/indpro_raw.csv`

---

### Task-006: 聯繫DHK (2025)作者索取程式碼
- **任務ID**: CODE-2.1.1
- **優先級**: P2 (中) - **可提前開始**
- **負責**: 待分配（需人類執行）
- **預計時間**: 1小時（撰寫email + 等待回覆）
- **階段**: Milestone 2.1.1

**說明**:
聯繫Davidson, Hou, Koop (2025)作者，請求提供OI-SVMVAR的MATLAB/R/Python程式碼。這個任務可以提前開始，因為等待回覆可能需要數週。

**前置任務**: 無（可立即開始）

**作者聯絡資訊**:
- James B. Davidson (Cardiff University)
- Chen Hou (University of Edinburgh)
- Gary Koop (University of Strathclyde)
- 期刊: Journal of Business & Economic Statistics
- 年份: 2025

**檢查清單**:
- [ ] 在Journal of Business & Economic Statistics網站查找補充材料
- [ ] 如無程式碼，撰寫禮貌的email請求
- [ ] Email應包含:
  - [ ] 簡短自我介紹
  - [ ] 研究目的（Taiwan應用）
  - [ ] 請求程式碼
  - [ ] 願意引用致謝
- [ ] 記錄email發送日期
- [ ] 追蹤回覆狀態

**備註**: 此任務需要人類執行，但可以請AI協助撰寫email草稿。

---

## 🟢 已完成 (Completed) - 最近10項

1. ✅ **PLAN-DHK-001**: 創建DHK (2025) Replication Plan (2025-11-16)
   - 完整14,000字詳細計畫 (llm_logs/2025-11-16_DHK_replication_plan.md)
   - 模組化結構：8個modules, 詳細timeline
   - 技術說明文件 (code/DHK_original/MODULE_INSTRUCTIONS.md)
   - 使用指南 (code/DHK_original/README.md)
   - Executive Summary (docs/DHK_REPLICATION_SUMMARY.md)
   - 資料夾結構建立complete

2. ✅ **SETUP-001**: 建立專案管理系統與資料夾重整 (2025-11-16)
   - 建立完整 Phase 1-5 資料夾架構（方案B：完整架構）
   - 創建 34 個 .gitkeep 檔案保留空資料夾
   - 資料夾包含：data/(8個子資料夾), code/(5個), results/(5個), figures/(6個), tables/, paper/, presentations/, policy_brief/, docs/, archive/
   - 完成檢查清單所有項目

2. ✅ **PHASE0-FINAL**: Phase 0所有任務 (2025-11-14)
   - 全球文獻回顧（40+篇論文）
   - 台灣文獻回顧（10+篇論文）
   - 研究方向確定與方法論決策
   - 里程碑規劃文件建立

3. ✅ **DOC-014**: 創建AI協作指引（INSTRUCTIONS_FOR_AI_literature_integration.md）(2025-11-14)

4. ✅ **DOC-013**: 完成研究方向與里程碑文件（2025-11-14_research_direction_and_milestones.md）(2025-11-14)

5. ✅ **DOC-012**: 更新CLAUDE.md（Phase 0完成）(2025-11-14)

6. ✅ **DOC-011**: 更新README.md（Phase 0完成）(2025-11-14)

7. ✅ **LIT-002**: 完成台灣特定文獻回顧（taiwan_specific_uncertainty_literature.md）(2025-11-14)

8. ✅ **LIT-001**: 完成全球不確定性衝擊文獻回顧（uncertainty_shock_literature.md）(2025-11-14)

9. ✅ **DEC-001**: 核心方法論決策（不延伸DHK模型）(2025-11-08)

10. ✅ **DEC-002**: 變數分類策略確認（外部變數→unclassified）(2025-11-08)

---

## ⏸️ 暫停 (On Hold)

### 無

---

## ❌ 已取消 (Cancelled)

### 無

---

## 📊 任務統計

- **進行中**: 0 tasks
- **待開始**: 13 tasks (6 Taiwan data + 7 DHK replication)
- **已完成**: 12 tasks (Phase 0 + SETUP + DHK Plan)
- **暫停**: 0 tasks
- **已取消**: 0 tasks

### DHK Replication Progress
- **Module 0 (Setup)**: 0/3 tasks
- **Module 1 (Data)**: 0/2 tasks
- **Module 2 (Model)**: 0/1 tasks
- **Module 3 (MCMC)**: 0/1 tasks (critical!)
- **Modules 4-8**: Not yet created

---

## 🔔 提醒事項

### 給AI協作者
1. **開始新任務前**: 先閱讀[CURRENT_STATUS.md](../CURRENT_STATUS.md)
2. **完成任務後**: 立即更新本文件，將任務狀態改為"已完成"
3. **遇到問題**: 將任務狀態改為"暫停"，並在CURRENT_STATUS.md記錄阻礙
4. **每次工作**: 結束後建立工作階段紀錄（sessions/資料夾）

### 給人類協作者

#### 🔥 URGENT: DHK Replication需要你的決策 (Task-DHK-001)
**請先閱讀**: `docs/DHK_REPLICATION_SUMMARY.md` (Executive Summary)

**關鍵決策** (需要你回答):
1. 程式語言: R (推薦) vs MATLAB vs Python?
2. 時程: 3-4個月可以嗎？
3. 複製程度: 完整 vs 重點 vs 最小可行？
4. 運算資源: HPC cluster or 個人電腦?
5. 你會寫code嗎？還是需要完整程式碼？
6. 是否聯繫DHK作者要code?

**請與Claude討論後再開始實施**

#### 其他提醒
1. **Task-DHK-003（聯繫DHK作者）**: 需要人類執行，可請AI協助撰寫email
2. **Taiwan資料下載**: 大部分任務AI可執行，但需要檢查資料品質
3. **任務分配**: 可在"負責"欄位填寫負責人名稱

---

## 📋 任務ID命名規則

- **SETUP-XXX**: 專案設定與系統建立
- **DOC-XXX**: 文件撰寫與更新
- **DATA-X.X.X**: 資料收集（對應Milestone編號）
- **CODE-X.X.X**: 程式碼開發
- **ANAL-X.X.X**: 分析任務
- **LIT-XXX**: 文獻回顧
- **DEC-XXX**: 決策紀錄
- **PHASEXX-XXX**: 階段性總結任務
- **DHK-XXX**: DHK (2025) Paper Replication tasks
  - **DHK-PLAN-XXX**: Planning and documentation
  - **DHK-SETUP-XXX**: Setup and environment (Module 0)
  - **DHK-M1-XXX**: Data collection (Module 1)
  - **DHK-M2-XXX**: Model specification (Module 2)
  - **DHK-M3-XXX**: MCMC algorithm (Module 3) 🔥
  - **DHK-M4-XXX**: Simulation study (Module 4)
  - **DHK-M5-XXX**: Empirical application (Module 5)
  - **DHK-M6-XXX**: Analysis tools (Module 6)
  - **DHK-M7-XXX**: Visualization (Module 7)
  - **DHK-M8-XXX**: Documentation (Module 8)

---

**更新紀錄**:
- 2025-11-16 (afternoon): 加入 DHK Replication 完整計畫與tasks (7個初始tasks)
- 2025-11-16 (morning): 完成 SETUP-001 (資料夾結構建立 - 方案B完整架構)
- 2025-11-14: 初始建立，加入Phase 0完成任務與Phase 1初始任務

---

## 📚 DHK Replication 資源

### 必讀文件 (Priority Order)
1. 🔴 **START HERE**: `docs/DHK_REPLICATION_SUMMARY.md` - Executive Summary
2. 📘 **Full Plan**: `llm_logs/2025-11-16_DHK_replication_plan.md` - 14,000 words
3. 🔧 **Technical**: `code/DHK_original/MODULE_INSTRUCTIONS.md` - Implementation cookbook
4. 📖 **User Guide**: `code/DHK_original/README.md` - How to run
5. 📄 **Original Paper**: `references/Investigating Economic Uncertain.pdf`

### 計畫概要
- **8 Modules**: Data → Model → MCMC → Simulation → Empirical → Analysis → Viz → Docs
- **Timeline**: 3-4 months (300-400 hours)
- **Critical Module**: M3 (MCMC) - 最困難，novel algorithm
- **Computational Cost**: 120+ hours of machine time
- **Language**: R recommended (可討論)

### 關鍵里程碑
- **Week 1-2**: Data collection + Model equations
- **Week 3-6**: MCMC algorithm implementation (HARD!) 🔥
- **Week 7-8**: Simulation study validation
- **Week 9-11**: Empirical application (mostly waiting)
- **Week 12-13**: Finalization and documentation

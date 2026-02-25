# CM03 計劃書製作規格文件

**建立日期**: 2026-02-24
**用途**: 所有撰寫 session 的統一參照規格，避免重複討論格式問題
**申請條碼**: 
**計畫主持人**: 林世揚（國立東華大學經濟系）
**計畫名稱（中）**: 美中交火下的台灣：不確定性是透過哪些管道影響金融穩定呢？
**計畫名稱（英）**: Caught in the Crossfire: Time-Varying Transmission of U.S.-China Uncertainty to Taiwan

---

## 一、格式規範

參照範例（113WIA0110259）：

| 項目 | 規格 |
|------|------|
| 語言 | **全英文**（人文處可接受英文計畫書） |
| 排版工具 | LaTeX（article class, 12pt） |
| 字體大小 | 12pt |
| 行距 | 單行間距（single spacing）|
| 頁面邊界 | 上下左右各 2cm |
| 段落縮排 | 有縮排（`\indent`），段落間不留空行 |
| 頁數限制 | 人文處多年期：**45頁以內**（含參考文獻、圖表） |
| 方程式 | 有編號，使用 `equation` 環境 |
| 引用格式 | Author (Year) 格式（parenthetical），如 `\citet{davidson2025investigating}` |
| 粗體強調 | 僅用於第一次出現的關鍵術語 |
| 子節格式 | `(1)`, `(1.1)`, `(2)`, `(2.1)` 等（見範例）|

### LaTeX preamble 基準

```latex
\documentclass[12pt]{article}
\usepackage[margin=2cm]{geometry}
\usepackage{natbib}
\usepackage{amsmath, amssymb}
\usepackage{setspace}
\singlespacing
\setlength{\parindent}{1.5em}
```

---

## 二、CM03 完整結構

### 頁數分配規劃（目標：~35-40頁，留緩衝至45頁上限）

```
Section 1: Research project's background        6-8 頁
─────────────────────────────────────────────────────
The First Year
  Section 2: Methods, procedures, schedule      10-12 頁
  Section 3: Anticipated results & achievements  1 頁
─────────────────────────────────────────────────────
The Second Year
  Section 2: Methods, procedures, schedule       8-10 頁
  Section 3: Anticipated results & achievements  1 頁
─────────────────────────────────────────────────────
Section 4: Integrated research project           1-2 頁
References                                       3-4 頁
─────────────────────────────────────────────────────
總計                                            ~30-38 頁
```

---

## 三、各 Section 內容規格

### Section 1: Research project's background（共用）

**對應現有資料**: `research_proposal_v4.tex` 的 Introduction ≈ 本節主體

**結構**（仿範例的流動段落，不設小節標題）：

| 段落 | 任務 | 對應 v4.tex | 狀態 |
|------|------|------------|------|
| 段落 1-2 | Taiwan 夾在美中之間的處境 + uncertainty 的重要性 | 段落 1-2 | ✅ 已有 |
| 段落 3 | 方法論挑戰一：omitted variable bias → 需要大型模型 | 段落 3 | ✅ 已有 |
| 段落 4 | 方法論挑戰二：order dependence → 需要 OI 框架 | 段落 4 | ✅ 已有 |
| 段落 5 | 方法論挑戰三：two-step bias + perception gap → 需要 SVMVAR | 段落 5 | ✅ 已有 |
| 段落 6 | 方法論挑戰四：無法辨別傳導管道 | 段落 6（短，待補） | ⚠️ 不完整 |
| 段落 7 | 三個核心研究問題 | 段落 7 | ✅ 已有 |
| 段落 8 | OI-SVMVAR 的三大優勢 + "unclassified variables" 創新 | 段落 8 | ✅ 已有 |
| 段落 9（新增）| 本計畫的貢獻與定位（相較於 DHK 2025） | 尚未寫 | ❌ 待寫 |
| 段落 10（新增）| 計畫結構預覽（"The first year... the second year..."） | 尚未寫 | ❌ 待寫 |

**Section 1 寫作任務**: 補寫段落 9-10，並微調段落 6（目前過短）

---

### Year 1 - Section 2: Methods, procedures, and implementation schedule

**(1). Research principles, methods, and the innovation of research methods**

**(1.1) The OI-SVMVAR Framework**

內容：
- 模型的一般形式（VAR 結構）
- Stochastic volatility in mean 的設定
- 兩個潛在因子：h_t = (h_{m,t}, h_{f,t})'
- 關鍵方程式：需要寫出 SVM-VAR 的基本方程

**(1.2) Variable Classification and the Key Innovation**

內容：
- 三類變數的分類方式（macro, financial, unclassified）
- **核心創新**：外部變數（US, China, global）全部放入 unclassified
- 時變分類機率 π_{i,t} 的概念
- 對比 DHK (2025) 的原始應用（domestic ambiguous variables）

**(1.3) Order-Invariance and Why It Matters for Taiwan**

內容：
- 為什麼 Cholesky 在大型模型中會失敗
- DHK (2025) 的 order-invariant 解決方案
- 為什麼 block exogeneity restrictions 在 OI 框架下是不必要的

**(2). Anticipated problems and means of resolution**

**(2.1) Data Assembly and Preprocessing**

內容：
- 40+ 變數的月度資料（台灣、美國、中國、全球）
- 資料來源（DGBAS, CBC, FRED, NBS, PolicyUncertainty.com）
- 樣本期間：目標 2000-2025（25年, 300月）
- 資料轉換：YoY growth rates, seasonal adjustment, stationarity tests

**(2.2) Works planned for the first year**

內容（以條列或段落）：
- 完成全部資料收集與清理
- 取得 DHK (2025) replication code
- 適配代碼至台灣資料集
- 執行初步估計（小型模型30變數 + 大型模型43變數）
- 收斂診斷與初步結果驗證

---

### Year 1 - Section 3: Anticipated results and achievements

格式：bullet points（仿範例）

內容：
- Complete assembly of 40+ variable monthly dataset (2000–2025)
- Successful adaptation of DHK (2025) MCMC code to Taiwan dataset
- Preliminary OI-SVMVAR estimation results for small-scale model (30 variables)
- Initial time-varying classification probabilities for external variables
- Conference presentation of preliminary findings
- Research assistant training in Bayesian estimation and MCMC methods

---

### Year 2 - Section 2: Methods, procedures, and implementation schedule

> **架構說明（2026-02-24 討論後更新）**：Year 2 分為兩個平行主軸：
> 1. 完成 OI-SVMVAR 的完整實證分析（三步驟）
> 2. 建立 SOE-DSGE 理論模型，用 Bayesian 估計後進行 IRF Matching 驗證

**(1). Research principles, methods, and the innovation of research methods**

**(1.1) Steps 1–3: Full Three-Step Empirical Analysis (OI-SVMVAR)**

內容：
- **Step 1**：Time-varying classification — 從後驗分佈提取 π_{i,t}（各外部變數的 macro vs. financial 分類概率時間序列），識別關鍵 regime shifts（2008, 2018, 2020, 2022）
- **Step 2**：FEVD — 量化各外部衝擊對台灣 h_{m,t} 和 h_{f,t} 的貢獻，驗證 SOE 假設
- **Step 3**：IRF — 台灣變數對 h_{m,t}/h_{f,t} 的反應，以及 historical decomposition
- 穩健性：小型模型（30變數）vs. 大型模型（43變數）比較

**(1.2) A Small Open Economy DSGE Model with Financial Frictions**

內容：
- 理論基礎：參照 Alfaro, Bloom, Lin (2024, JPE) 的「金融不確定性乘數」模型架構
- 模型特徵：異質性廠商 + 財務摩擦（隨機融資楔子，stochastic financing wedge）+ 二階衝擊（second-moment shocks）
- 兩種外部不確定性衝擊（與 DHK 的 macro/financial factor 對應）：
  - **國外需求不確定性**（Foreign demand uncertainty）：生產力波動率跳升 → 對應 macro channel（透過 Trade/IS equation 傳導）
  - **國際融資不確定性**（International financing uncertainty）：借貸利差波動率跳升 → 對應 financial channel（透過 UIP/Financial Accelerator 傳導）
- **三層防禦邏輯**（用於回應「這兩種不確定性如何認定」的審查質疑）：
  - 第一層：資料驅動的分類（DHK 的 macro/financial factor loading 自然歸類）
  - 第二層：理論上 SOE 外部衝擊只能透過 Trade equation 或 UIP/Financial Accelerator 傳導，直接對應兩種不確定性
  - 第三層：IRF 軌跡匹配作為跨方法終極驗證

**(1.3) Bayesian Estimation and Impulse Response Matching**

內容：
- 貝氏 MCMC 估計 DSGE 結構參數（以台灣月度總體與金融資料為基礎）
- 先驗分佈設計：根據台灣 SOE 特性設定（開放度、資本帳管制程度等）
- **IRF Matching（核心驗證）**：
  - 將 DSGE 推導的結構性 IRF 與 Year 1 DHK 資料驅動 IRF 並排比較
  - 若 DSGE 的 IRF 軌跡能包覆或吻合 DHK 的 IRF → 驗證理論機制正確
  - 若有顯著偏差 → 新的學術發現（現有理論需要修正）
- 歷史反事實模擬（Counterfactual）：切斷金融管道後的台灣經濟路徑

**(2). Anticipated problems and means of resolution**

**(2.1) Computational and Estimation Challenges**

內容：
- OI-SVMVAR 估計：MCMC 每次約 30 小時，需 HPC 資源（大學 HPC 或雲端運算）
- Bayesian DSGE 估計：MCMC 收斂診斷（Geweke test, trace plots, effective sample size）
- IRF Matching 的識別挑戰：如何定義「匹配成功」的統計標準（信賴區間覆蓋率）

**(2.2) Works planned for the second year**

內容：
- 大型模型（43變數）OI-SVMVAR 完整估計
- 三步驟完整分析：分類概率 → FEVD → IRF（含穩健性檢驗）
- SOE-DSGE 模型建構與方程式推導
- Bayesian MCMC 估計（台灣月度資料）
- IRF Matching：DSGE 結構性 IRF vs. DHK 資料驅動 IRF 比對
- 歷史反事實模擬
- 論文撰寫與頂尖期刊投稿
- 政策簡報（為央行準備）

---

### Year 2 - Section 3: Anticipated results and achievements

內容（bullet points）：
- Full estimation results from 43-variable OI-SVMVAR model
- Time-varying classification plots for all external variables (macro vs. financial channel probabilities)
- FEVD tables quantifying U.S., China, and global shock contributions to Taiwan's uncertainty
- IRF figures showing dynamic responses through macro and financial channels
- Estimated SOE-DSGE model with posterior parameter distributions
- Structural IRFs from DSGE model aligned with Alfaro et al. (2024) financial uncertainty multiplier mechanism
- Impulse Response Matching comparison (DSGE structural IRFs vs. DHK data-driven IRFs)
- Historical counterfactual simulations (e.g., severing financial channel during 2018–2019 trade war)
- Robustness checks comparing small vs. large model results
- Journal submission to top-tier outlet (e.g., Journal of International Economics, Journal of Applied Econometrics)
- Policy brief for the Central Bank of China (Taiwan)

---

### Section 4: Integrated research project（共用總結）

~1-2頁的流動段落，總結整個計畫的：
- 核心問題與創新（unclassified variables 識別傳導管道）
- 兩年期計畫的銜接邏輯（Year 1: 建構基礎 → Year 2: 完整分析）
- 預期對學術界與政策界的雙重貢獻

---

### References

格式：仿範例（**Author, First Name Last Name.** Year. "Title." *Journal*, Vol(No): pp.）

關鍵必引文獻：
- Davidson, Hou, Koop (2025) - DHK 核心方法
- Carriero, Clark, Marcellino (2018) - omitted variable bias
- Baker, Bloom, Davis (2016) - EPU index
- Chan, Koop, Yu (2024) - order-invariant VAR
- Bloom (2009, 2014) - uncertainty impacts
- Handley (2022) - trade policy uncertainty
- Caldara et al. - financial vs. macro uncertainty
- Sin (2015) - Taiwan SVAR
- Caldara, Iacoviello - GPR index
- **Alfaro, Bloom, Lin (2024, JPE)** - Finance Uncertainty Multiplier（Year 2 DSGE 理論基礎）

---

## 四、CM02 摘要規格

**中文關鍵詞**（5個以內）：
不確定性衝擊、時變傳導管道、隨機波動均值向量自迴歸、小型開放經濟體、美中關係

**英文關鍵詞**：
uncertainty shock, time-varying transmission channel, stochastic volatility in mean VAR, small open economy, U.S.-China relations

**英文 Abstract**（~250字）：需要撰寫

**中文摘要**（~250字）：需要撰寫

**計畫概述**（300字以內，中文）：需要撰寫

---

## 五、寫作工作流程

### 分工原則

| 任務 | 負責方 |
|------|--------|
| 確認每段的論點是否正確 | **你（PI）** |
| 標記草稿中事實錯誤或論述偏差 | **你（PI）** |
| 將論點展開成符合 v4.tex 文風的段落 | **AI** |
| 數學方程式的正確性驗證 | **你（PI）** |
| 提供每個 section 的核心論點 bullet points | **你（PI）** |

### Session 拆分建議

由於 context window 限制，建議每個 session 只處理一個 section：

| Session | 任務 | 預計輸出 |
|---------|------|---------|
| Session A | 完成 Section 1（補段落 9-10，修段落 6） | ~7頁 |
| Session B | Year 1 Section 2 (1.1)-(1.3)：模型規格 | ~6頁 |
| Session C | Year 1 Section 2 (2.1)-(2.2)：資料與第一年工作 | ~4頁 |
| Session D | Year 2 Section 2 全部：三步驟分析 | ~8頁 |
| Session E | Section 3×2 + Section 4 + References | ~6頁 |
| Session F | CM02 摘要（中英文） | ~1頁 |

### 每個 Session 的啟動指令模板

新 session 開始時，給 AI 的指令：

```
請閱讀以下文件後開始工作：
1. NSTC-applicaiton/CM03_production_spec.md（本規格文件）
2. research_proposal_v4.tex（現有 Section 1 草稿）
3. llm_logs/2025-11-08_discussion.md（方法論決策）

今天的任務是：[指定 session 任務]
請依照規格文件的格式要求，先提出每段的論點架構讓我確認，
再展開成完整段落。
```

---

## 六、品質標準

AI 產出的文字必須符合以下標準（以 v4.tex 為參照）：

1. **每段有明確的論點任務**，且任務在該段首句清楚宣告
2. **技術主張需具體**（不能說「we use advanced methods」，要說「we employ the order-invariant SVMVAR framework of Davidson, Hou, and Koop (2025)」或者具體的方法）
3. **句子之間有邏輯咬合**（用 "However", "To overcome this", "Consequently", "Against this background" 等連接詞銜接論述）
4. **不使用 bullet points 在 Section 1, 2, 4**（只有 Section 3 用 bullets）
5. **不重複解釋同樣的概念**（每個方法論要點只在第一次出現時完整解釋）
6. **引用格式正確**（`\citet{}` 用於主詞位置，`\citep{}` 用於括號內）

---

*最後更新：2026-02-24*
*下一步：確認年期（1年or2年），然後開始 Session A（完成 Section 1）*

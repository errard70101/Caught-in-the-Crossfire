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
- 45 變數的月度資料（台灣、美國、中國、全球）
- 資料來源（DGBAS, CBC, FRED, NBS, PolicyUncertainty.com, Poilly & Tripier 2025）
- 樣本期間：目標 2000-2025（25年, 300月）
- 資料轉換：YoY growth rates, seasonal adjustment, stationarity tests

**(2.2) Works planned for the first year**

內容（以條列或段落）：
- 完成全部資料收集與清理
- 取得 DHK (2025) replication code
- 適配代碼至台灣資料集
- 執行初步估計（小型模型30變數 + 大型模型45變數）
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

> **架構說明（2026-04-11 更新）**：Year 2 已完成撰寫（`proposal/y2_sec2_methods.tex`）。
> 核心框架為 **Conditional Structural Modeling: A Competing Hypotheses Framework**。
> ⚠️ **注意**：先前的「SOE Nonlinear BCA」框架因考量弱識別與機制顆粒度不足，已歸檔作為歷史參考（保留於 `llm_logs/2026-02-28_bca-nonlinear-uncertainty-accounting.md`）。

**(1). Research principles, methods, and the innovation of research methods**

**(1.1) Steps 1–3: Full Three-Step Empirical Analysis (OI-SVMVAR)**

內容：
- **Step 1**：Time-varying classification — 從後驗分佈提取 π_{i,t}，識別關鍵 regime shifts。
- **Step 2**：FEVD — 量化各外部衝擊對台灣 h_{m,t} 和 h_{f,t} 的貢獻，驗證 SOE 假設。
- **Step 3**：IRF — 台灣變數對不確定性衝擊的反應，這些 IRF 將作為第二年結構模型的 empirical targets。

**(1.2) Conditional Structural Modeling: A Competing Hypotheses Framework**

內容：
- **Baseline model**：標準 SOE New Keynesian 模型，採用 Rotemberg 定價（避免 Calvo 的通膨預期反常），並透過三階微擾法（third-order perturbation）引入隨機波動。
- **競爭假說（四個可能傳導管道）**：
  1. **The real "wait-and-see" channel (Bloom 2009)**：不含金融摩擦。Trigger: 投資降但利差不動。
  2. **The financial accelerator channel (BGG)**：借款方代理問題。Trigger: 企業利差擴大、金融分類機率高。
  3. **The balance sheet / aggregate risk concentration channel (Di Tella 2017)**：中介機構風險與槓桿限制。Trigger: 金融業受創甚於一般企業、資金外流。
  4. **The exchange rate / imported inflation channel (Mumtaz & Theodoridis 2015)**：不完全匯率傳遞與 UIP。Trigger: 台幣貶值且出現停滯性通膨。

**(1.3) From Identification to Discrimination: The Year 1–Year 2 Bridge**

內容：
- 決策協議（Decision protocol）：透過 IRF 反應的時間差、通膨的正負號、以及外部變數的分類機率，來判定觸發哪一個/哪兩個假說。
- 對既有文獻的修正：引用 Born & Pfeifer (2021) 說明 markup channel 的實證不足。
- 反事實模擬與最適政策分析（如央行該採利率、匯率干預還是總體審慎措施）。

**(2). Anticipated problems and means of resolution**

**(2.1) Computational and Estimation Challenges**

內容：
- OI-SVMVAR 的 MCMC 高計算需求（需 HPC）。
- Dynare 三階微擾法的 pruning 挑戰。
- 兩階段估計（two-step procedure）：從 OI-SVMVAR 取得 h_{m,t} / h_{f,t} 作為 DSGE 的 observable inputs。

**(2.2) Works planned for the second year**

內容：
- Q1：完成 45 變數 OI-SVMVAR 完整實證與診斷。
- Q2：基於 Year 1 結果與四項判定準則，選擇對應的結構模型並建構。
- Q3：貝式估計、反事實模擬與最適政策分析。
- Q4：撰寫學術論文投稿、準備央行政策簡報。

---

### Year 2 - Section 3: Anticipated results and achievements

內容（bullet points）：
- Full estimation results from 43-variable OI-SVMVAR model
- Time-varying classification plots for all external variables (macro vs. financial channel probabilities)
- FEVD tables quantifying U.S., China, and global shock contributions to Taiwan's uncertainty
- IRF figures showing dynamic responses through macro and financial channels
- Model selection based on Competing Hypotheses framework and empirical triggers
- Bayesian estimation of the selected SOE DSGE model via third-order perturbation
- Counterfactual simulations isolating specific transmission channels (e.g., severing financial accelerator during 2018–2019 trade war)
- Optimal policy analysis evaluating Central Bank of China (Taiwan) interventions
- Robustness checks comparing small vs. large empirical model results
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
- **Chari, Kehoe & McGrattan (2007, Econometrica)** - BCA 原始框架（Year 2 理論基礎）
- Fernández-Villaverde et al. (2011, AER; 2015, REStud) - DSGE with Stochastic Volatility
- Andreasen (2012, Review of Economic Dynamics) - Third-order perturbation 標準做法
- `[TBD]` SOE-BCA 文獻（Lama 2011, Otsu 2010 等——待確認）

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

### Session 進度管理

**→ 請見 `NSTC-applicaiton/PROGRESS.md`**

各 section 的當前狀態、下一步行動、待決事項、以及 AI 執行計畫的連結，
均統一記錄於 `PROGRESS.md`。每個 writing session 結束後請更新該檔案。

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

*最後更新：2026-04-17*
*下一步：確認 14th unclassified variable，然後開始撰寫 Year 1 Section 2 (y1_sec2_methods.tex)*
內）

---

*最後更新：2026-02-28*
*下一步：完成 SOE-BCA 文獻研究（wedge 選擇、uncertainty shock 引入方式），然後補充 Year 2 的 [TBD] 細節*

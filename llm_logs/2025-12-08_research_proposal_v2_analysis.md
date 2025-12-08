# Research Proposal v2 分析與修改建議

**日期**: 2025-12-08
**目的**: 評估 `research_proposal_v2.tex` 的內容，與 `research_proposal_NSTC_en.tex` 比較，並檢視與 DHK (2025) 方法論的相容性

---

## 1. research_proposal_v2.tex 與 research_proposal_NSTC_en.tex 的差異分析

### 1.1 目前 v2 的內容

`research_proposal_v2.tex` 包含一個 Introduction section，有兩個標記為 `=== to be modified ===` 的段落待修改。目前內容主要聚焦於：

1. **Taiwan 的地緣經濟位置**：深度整合於美中經濟體系
2. **政策不確定性的時間維度**：強調重大政策變動從宣布到形成穩定政策軌跡之間存在漫長的不確定期間
3. **政策變動的可逆性**：計畫中的政策變動可能被修改、延遲或取消（以美中關稅談判為例）
4. **不確定性對經濟行為的影響**：引用 Bloom (2009, 2014) 和 Handley & Limão (2022) 強調不確定性對投資、消費和投資組合決策的影響

### 1.2 與 NSTC 版本的主要差異

| 面向 | research_proposal_v2.tex | research_proposal_NSTC_en.tex |
|------|--------------------------|-------------------------------|
| **篇幅** | ~15 行 | 完整研究計畫（~600 行） |
| **研究問題** | 尚未明確陳述 | 明確：外部衝擊通過哪個傳導管道影響台灣？ |
| **方法論** | 未提及 | 詳細描述 OI-SVMVAR 框架 |
| **敘事角度** | 政策不確定性的**過程**（從宣布到實施） | 外部衝擊的**傳導管道**（總經 vs. 金融） |
| **時間焦點** | 政策形成期間的不確定性 | 衝擊傳導的時變特性 |

### 1.3 v2 新觀點的評估

**v2 提供的新觀點：**
- 強調政策不確定性是一個**過程**而非單一事件
- 突顯政策宣布與最終實施之間的**時間間隔**
- 強調政策變動的**可逆性**和**可修改性**

**建議：部分保留**

這個觀點提供了有價值的 narrative framing，但需要與核心研究問題更緊密連結。目前的敘述偏向解釋「為什麼不確定性存在」，而非「我們如何測量和分析它的影響」。

**具體建議：**
1. 保留政策過程的敘述作為 motivation 的一部分
2. 但需要明確連結到核心研究問題：這種過程性的不確定性如何透過不同管道傳導到台灣？
3. 可整合到 NSTC 版本的 Section 1.1 Research Motivation 中

---

## 2. 與 DHK (2025) 方法論的相容性評估

### 2.1 DHK (2025) 方法論核心特徵

根據 Davidson, Hou, and Koop (2025) "Investigating Economic Uncertainty Using Stochastic Volatility in Mean VARs"：

**關鍵特徵：**
1. **Order-Invariant SVMVAR (OI-SVMVAR)**：解決傳統大型 VAR 的變數排序依賴問題
2. **Time-Varying Classification**：允許變數在不同時點被分類為總經或金融變數
3. **Unclassified Variables**：對於難以明確分類的變數，由資料決定其分類
4. **Large-Scale Models**：支援 43+ 變數的大型模型
5. **Two Latent Factors**：h_t = (h_m,t, h_f,t)' 代表總經和金融不確定性
6. **Stochastic Volatility in Mean**：不確定性因子進入 VAR 的條件均值

### 2.2 research_proposal_v2.tex 描述的相容性

**目前 v2 的描述與 DHK 方法的相容性：**

| v2 描述 | DHK 方法能否達成 | 說明 |
|---------|-----------------|------|
| 測量外部不確定性對台灣的影響 | ✅ 可達成 | 外部變數放入 unclassified category |
| 時變傳導機制 | ✅ 可達成 | Time-varying classification |
| 區分總經 vs. 金融管道 | ✅ 可達成 | 模型核心設計 |
| 政策過程的不確定性 | ⚠️ 部分相容 | 可捕捉不確定性水準變化，但非設計重點 |

**重要澄清：**

v2 強調的「政策從宣布到實施的過程」更接近於測量 **政策不確定性 (Policy Uncertainty)** 的概念（如 Baker, Bloom, Davis 2016 的 EPU），而 DHK 方法測量的是 **經濟不確定性 (Economic Uncertainty)**，定義為變數預測誤差的共同波動性。

**這兩者的關係：**
- 政策不確定性可以是經濟不確定性的**來源**之一
- 在 DHK 框架中，EPU 指數可作為 unclassified variable 納入模型
- 模型會判斷 EPU 是通過總經管道還是金融管道傳導

### 2.3 需要修改的內容

**必須修改：**

1. **明確定義不確定性概念**：目前 v2 混用了「政策不確定性」和「經濟不確定性」，需要澄清：
   - DHK 測量的是 economic uncertainty（預測誤差的共同波動）
   - 政策不確定性（如 EPU、US-China TPU）是外生衝擊來源
   - 我們的研究問題是：外部政策不確定性如何透過不同管道傳導到台灣的國內經濟不確定性？

2. **研究問題需更精確**：
   - 原始敘述：關注政策過程本身
   - 應調整為：關注外部衝擊的傳導管道

3. **方法論銜接**：v2 目前完全未提及方法論，需要補充為什麼 OI-SVMVAR 適合回答這個問題

---

## 3. Carriero, Clark, and Marcellino (2018) 的 Motivation 整合建議

### 3.1 CCM (2018) 的核心 Motivation

CCM (2018) "Measuring Uncertainty and Its Impact on the Economy" 提出的主要論點：

**對兩階段方法的批評：**

1. **測量誤差問題**：第一階段估計的不確定性在第二階段被當作觀測資料，可能導致內生性偏誤
2. **不確定性圍繞不確定性**：無法衡量不確定性估計本身的不確定性
3. **遺漏變數偏誤**：第二階段通常使用小型 VAR，可能有遺漏變數問題
4. **模型不一致**：第一階段假設時變波動性，第二階段卻使用同質變異數 VAR
5. **波動性與均值分離**：第一階段假設波動性不影響均值，但最終目標是分析波動性對均值的影響

**CCM 的解決方案：**
- 使用 SVMVAR 在單一模型中同時估計不確定性及其影響
- 使用大型資料集減少遺漏變數偏誤
- 區分總體經濟不確定性和金融不確定性

### 3.2 適合整合到 Introduction 的論點

**強烈建議納入的論點：**

1. **方法論一致性論點**（高度相關）：
   > "The assumption that variables have time-varying volatility in the first step is inconsistent with the use of a homoscedastic VAR in the second step." (CCM 2018, p.799)

   **應用於台灣研究**：現有台灣不確定性研究（如 Sin 2015）使用傳統 SVAR，假設同質變異數，這與我們觀察到的事實（不確定性明顯時變）不一致。

2. **遺漏變數偏誤論點**（高度相關）：
   > "The use of small VAR models to assess the effects of uncertainty can make the results subject to the common omitted variable bias and nonfundamentalness of the errors." (CCM 2018, p.799)

   **應用於台灣研究**：Sin (2015) 僅使用 6 變數 SVAR，可能嚴重低估或錯誤歸因不確定性來源。DHK (2025) 的模擬研究證實，小模型（約 30 變數）會高估不確定性影響。

3. **聯合估計優勢**（中度相關）：
   > "In our setup, uncertainty and its effects are estimated in a single step within the same model, which avoids both the estimated regressors problem and the use of two contradictory models." (CCM 2018, p.800)

   **應用**：強調 SVMVAR 框架的方法論優勢。

4. **總經 vs. 金融不確定性區分**（高度相關）：
   > "Macroeconomic uncertainty has large, significant effects on real activity but a limited impact on financial variables, whereas financial uncertainty shocks have a direct impact on financial variables and subsequently transmit to the macroeconomy." (CCM 2018, p.800)

   **應用**：這直接支持我們區分傳導管道的研究設計。但 DHK (2025) 使用更大的資料集後發現只有金融不確定性有顯著影響，這突顯了模型規模的重要性。

### 3.3 建議的 Introduction 結構

```
1. 台灣的地緣經濟位置與雙重暴露
   - 深度整合於美中經濟體系
   - 面臨來自兩大經濟體的政策與地緣政治不確定性

2. 不確定性傳導的過程特性 [整合 v2 內容]
   - 政策變動從宣布到實施的時間間隔
   - 期間的不確定性影響經濟行為
   - 引用 Bloom (2009), Handley & Limão (2022)

3. 核心研究問題
   - 外部不確定性衝擊如何傳導到台灣？
   - 主要通過總經管道還是金融管道？
   - 傳導機制是否隨時間變化？

4. 現有研究的方法論限制 [整合 CCM 2018]
   - 兩階段方法的問題
   - 小型模型的遺漏變數偏誤
   - 模型假設的不一致性

5. 本研究的方法論貢獻
   - 採用 DHK (2025) 的 OI-SVMVAR 框架
   - 大型模型（43+ 變數）減少遺漏變數偏誤
   - 時變分類識別傳導管道
   - 使用 unclassified variables 識別外部衝擊來源
```

---

## 4. 總結與行動項目

### 4.1 主要發現

1. **research_proposal_v2.tex** 提供了有價值的 narrative framing（政策過程的不確定性），但需要與核心方法論更緊密連結

2. **DHK (2025) 方法完全適用**於回答本研究問題，特別是：
   - Unclassified variables 機制適合放置外部衝擊來源
   - Time-varying classification 可識別傳導管道的時變特性
   - Order-invariance 對大型模型至關重要

3. **CCM (2018) 的 motivation** 高度相關，特別是：
   - 對兩階段方法的批評
   - 遺漏變數偏誤的論點
   - 總經 vs. 金融不確定性的區分

### 4.2 建議修改

| 優先級 | 項目 | 說明 |
|--------|------|------|
| 高 | 明確定義不確定性概念 | 區分 economic uncertainty 和 policy uncertainty |
| 高 | 精確陳述研究問題 | 聚焦於傳導管道而非政策過程本身 |
| 中 | 整合 CCM (2018) motivation | 加入對兩階段方法的批評 |
| 中 | 保留 v2 的敘事框架 | 但作為 motivation 的一部分，而非核心論述 |
| 低 | 統一術語使用 | 確保全文一致使用 economic uncertainty 定義 |

### 4.3 具體文本建議

**建議刪除或大幅修改的 v2 內容：**
- 無需刪除，但需要重新定位：v2 的內容應作為 motivation 的一部分，解釋為什麼不確定性重要，但核心論述應轉向傳導管道問題

**建議保留並整合的 v2 內容：**
- 政策從宣布到實施的時間間隔論述
- 美中貿易政策的例子
- 對 Bloom (2009, 2014) 和 Handley & Limão (2022) 的引用

**建議新增的內容：**
1. CCM (2018) 對兩階段方法的批評
2. DHK (2025) 關於模型規模重要性的發現
3. 明確的研究問題陳述：傳導管道識別
4. 方法論選擇的理由：為什麼 OI-SVMVAR 適合回答這個問題

---

## 附錄：關鍵引用

### CCM (2018) 關鍵段落

> "While this approach has the merit of bringing to the fore the effects that uncertainty can have on the macroeconomy, the fact that the uncertainty measure is not fully embedded in the econometric model at the estimation stage inevitably can complicate the task of making statistical inference on its effects." (p.799)

> "The two-step approach treats uncertainty, which is estimated in the first step, as an observable variable in the second step. It follows that the second step can potentially suffer from measurement errors in the regressors, which might lead to an endogeneity bias." (p.799)

### DHK (2025) 關鍵段落

> "Smaller SVMVARs overstate the effects of uncertainty, failing to reveal that only financial uncertainty has an adverse effect on the economy." (p.1)

> "When using large order-dependent SVMVARs, however, the uncertainty estimates produced depend on the variable ordering, distorting impulse response analysis. Thus, it becomes critical to adopt an order-invariant specification." (p.1)

> "We also find that many variables change classification with changes often occurring during crisis periods." (p.1)

---

## 5. 標記段落的具體修改建議

### 5.1 原始標記段落

**段落 A（第一個 `=== to be modified ===` 後）：**
```
Empirically, however, identifying external uncertainty shocks and their effects
on Taiwan is challenging. First, it is difficult to separate shocks to the
expected path of policies from shocks to current policy levels, even though
both often move together in response to the same news. Second, external and
domestic sources of uncertainty are tightly intertwined: developments in
U.S.–China relations can simultaneously alter global risk sentiment, Taiwan's
domestic political outlook, and expectations about cross-strait policy. Third,
existing measures of uncertainty, such as global financial volatility or
U.S.-based policy uncertainty indices, may not fully capture how external
shocks are transmitted to a small open economy like Taiwan.
```

**段落 B（第二個 `=== to be modified ===` 前）：**
```
Against this background, this project addresses the following questions. First,
how do external monetary policy and trade policy uncertainty shocks affect
Taiwan's real activity, trade flows, and financial markets? Second, to what
extent do these effects differ across sectors with different exposures to the
United States and China? Third, has the transmission of external uncertainty
to Taiwan changed over time, particularly since the escalation of U.S.–China
tensions in the late 2010s?
```

### 5.2 段落 A 評估與修改建議

**評估：**

| 原文論點 | 相容性 | 建議 |
|---------|--------|------|
| 難以分離預期政策路徑衝擊與當前政策水準衝擊 | ⚠️ 部分相關 | 這更適合 narrative identification，非 DHK 框架重點 |
| 外部與國內不確定性來源糾纏 | ✅ 高度相關 | 正是需要大型模型的原因，可保留並強化 |
| 現有不確定性測量無法捕捉傳導機制 | ✅ 高度相關 | 這正是 DHK 方法論的貢獻，應強化論述 |

**建議修改方向：**

1. **刪除**關於「分離預期與當前政策衝擊」的論述（與 DHK 框架不直接相關）
2. **保留並強化**「外部與國內糾纏」的論點，連結到遺漏變數偏誤
3. **新增** CCM (2018) 對兩階段方法的批評
4. **新增**關於「傳導管道」識別的挑戰

**建議修改後文本：**

```latex
Empirically, however, identifying external uncertainty shocks and quantifying
their effects on Taiwan presents several methodological challenges. First,
external and domestic sources of uncertainty are tightly intertwined:
developments in U.S.–China relations can simultaneously alter global risk
sentiment, Taiwan's domestic political outlook, and expectations about
cross-strait policy. This interconnection means that small-scale econometric
models may suffer from severe omitted variable bias, potentially misattributing
domestic uncertainty dynamics to external sources or vice versa
\citep{carriero2018measuring}. Second, many existing approaches adopt a
two-step procedure---first estimating an uncertainty measure, then assessing
its macroeconomic effects in a separate model. This approach treats estimated
uncertainty as observable data, introducing potential measurement error bias
and model inconsistency \citep{carriero2018measuring}. Third, existing
uncertainty measures, such as global financial volatility indices or
country-specific policy uncertainty indices, do not distinguish between the
\textit{channels} through which uncertainty transmits to the economy. For a
small open economy like Taiwan, understanding whether external shocks propagate
primarily through macroeconomic channels (trade flows, production linkages) or
financial channels (capital flows, asset prices) carries distinct policy
implications.
```

### 5.3 段落 B 評估與修改建議

**評估：**

| 原文研究問題 | 與 DHK 框架相容性 | 建議 |
|-------------|------------------|------|
| 外部貨幣與貿易政策不確定性衝擊如何影響台灣？ | ✅ 可達成 | 保留，但需更精確 |
| 不同產業暴露程度的差異 | ⚠️ 需要額外資料 | 這需要產業層級資料，超出 DHK 框架 |
| 傳導是否隨時間變化？ | ✅ 核心特色 | 強化，這是 DHK 框架的主要優勢 |

**建議修改方向：**

1. **聚焦於傳導管道**：將「影響有多大」改為「通過哪個管道傳導」
2. **刪除或弱化**產業層級分析（除非有明確計畫）
3. **強調時變特性**：這是 DHK 框架的核心貢獻
4. **明確連結方法論**：說明為何 OI-SVMVAR 適合回答這些問題

**建議修改後文本：**

```latex
Against this background, this project addresses the following questions. First,
do external uncertainty shocks from the United States and China transmit to
Taiwan's economy primarily through \textit{macroeconomic channels}---affecting
real activity, trade flows, and production---or through \textit{financial
channels}---impacting asset prices, credit conditions, and capital flows?
Second, which external sources---U.S. monetary policy, U.S.–China trade policy
uncertainty, or broader geopolitical risks---contribute most to Taiwan's
domestic economic uncertainty? Third, has the transmission mechanism changed
over time, particularly during episodes of heightened U.S.–China tensions such
as the 2018–2019 trade war or the post-2020 technology decoupling?

To address these questions, this project employs the order-invariant stochastic
volatility in mean vector autoregression (OI-SVMVAR) framework developed by
\citet{davidson2025investigating}. This framework offers three key advantages
for our research objectives. First, it accommodates large-scale models (40+
variables), mitigating the omitted variable bias that plagues smaller models
\citep{carriero2018measuring}. Second, its order-invariant specification
ensures that results do not depend on arbitrary variable ordering---a critical
feature for credible inference in large VAR systems. Third, its time-varying
classification mechanism allows us to identify \textit{when} and \textit{how}
external shocks shift between macroeconomic and financial transmission
channels.
```

### 5.4 完整修改後的 Introduction 架構

建議將修改後的段落整合成以下結構：

```
[保留原有第一段：Taiwan's geoeconomic position]

[保留原有第二段：Policy uncertainty as a process - 從宣布到實施的時間間隔]

[修改後的段落 A：方法論挑戰]
- 外部與國內糾纏 → 遺漏變數偏誤風險
- 兩階段方法的問題 → CCM (2018) 批評
- 傳導管道識別的重要性

[修改後的段落 B：研究問題與方法論]
- 三個核心研究問題（聚焦傳導管道）
- OI-SVMVAR 框架的三大優勢
- 時變分類如何回答傳導管道問題
```

### 5.5 新增引用建議

需要在 `research_proposal.bib` 中確保包含以下引用：

```bibtex
@article{carriero2018measuring,
  title={Measuring Uncertainty and Its Impact on the Economy},
  author={Carriero, Andrea and Clark, Todd E and Marcellino, Massimiliano},
  journal={Review of Economics and Statistics},
  volume={100},
  number={5},
  pages={799--815},
  year={2018}
}

@article{davidson2025investigating,
  title={Investigating Economic Uncertainty Using Stochastic Volatility in
         Mean VARs: The Importance of Model Size, Order-Invariance and
         Classification},
  author={Davidson, James and Hou, Chenghan and Koop, Gary},
  journal={Journal of Econometrics},
  year={2025},
  note={Forthcoming}
}
```

---

## 6. 後續行動項目

| 優先級 | 項目 | 說明 |
|--------|------|------|
| **高** | 修改段落 A | 整合 CCM (2018) 批評，聚焦方法論挑戰 |
| **高** | 修改段落 B | 重新聚焦研究問題於傳導管道，連結 DHK 框架 |
| **中** | 檢查 .bib 檔案 | 確保包含 CCM (2018) 和 DHK (2025) 引用 |
| **中** | 統一術語 | 區分 policy uncertainty（衝擊來源）vs. economic uncertainty（測量目標） |
| **低** | 產業分析決策 | 決定是否保留產業層級分析問題，或留待後續研究 |

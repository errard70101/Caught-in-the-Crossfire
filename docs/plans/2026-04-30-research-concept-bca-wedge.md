# 研究構想：從實證 VAR 到 Simulated BCA 的模型篩選機制

**日期：** 2026-04-30
**主題：** 確立「Caught in the Crossfire」第二年計畫 (Year 2) 中，如何橋接第一年的實證結果與第二年的結構模型，並說明為何採用「Wedge 比較」優於傳統的「IRF 比較」。

---

## 1. 實證基礎：Empirical VAR (OI-SVMVAR)
第一年的核心任務是透過 43 個變數的 **Order-Invariant Stochastic Volatility in Mean VAR (OI-SVMVAR)** 讓數據說話。
*   **目標**：動態識別美中外部不確定性衝擊是透過「總體經濟管道 (Macroeconomic channel)」還是「金融管道 (Financial channel)」傳遞至台灣。
*   **產出**：我們將獲得真實世界總體變數 (Y, C, I, L) 面對不確定性衝擊時的**實證衝擊反應函數 (Empirical IRFs)**。經驗上，這通常會呈現衰退特徵（產出、投資、勞動同時下降）。

## 2. 傳統作法的侷限：Empirical IRFs vs. Simulated IRFs
傳統的 DSGE 研究方法是：建立一個結構模型（例如帶有摩擦的 RBC 或 New Keynesian 模型），給予相同的不確定性衝擊，算出**理論衝擊反應函數 (Simulated IRFs)**，然後將兩者放在一起比較。
*   **致命傷：觀察等價性 (Observational Equivalence)**。不同的深層摩擦機制（如：極度僵固的價格 vs. 金融擔保品限制），只要參數調整得當，都能配適 (Curve-fitting) 出形狀極為相似的 Y, C, I, L 下降曲線。
*   **結論**：單純比較 IRF 無法嚴格證明台灣的衰退是由「金融管道」主導，這只是「對的結果，可能來自錯的原因」。

## 3. 方法論突破：Empirical Wedge vs. Simulated Wedge (Simulated BCA)
為了突破觀察等價性，我們引入 **Business Cycle Accounting (BCA)** 作為「共同語言」與「診斷透鏡」。我們將比較維度從「總體變數 (Y, C, I, L)」轉換為深層的「摩擦楔子 (Wedges)」。

### 步驟 A：萃取 Empirical Wedges
將第一年 BVAR 產生的真實 Y, C, I, L，代入 CKM (2007) 的無摩擦原型模型中。
*   **結果**：我們得到真實世界的 Wedge 動態。在不確定性衝擊下，這通常表現為**「勞動 Wedge 惡化」**與**「投資 Wedge 惡化」**（衰退的幾何特徵）。

### 步驟 B：揭露理論模型的 Accounting Illusions (萃取 Simulated Wedges)
將理論模型（如原始的 FVGQ 2020 純擔保品限制模型）模擬出的 Y, C, I, L，同樣代入 CKM 原型模型中。
*   **驚人發現**：在面對金融不確定性時，FVGQ 2020 模型中的企業家會產生強烈的預防性動機（瘋狂囤積資本、要勞工多加班）。
*   **BCA 的解讀**：BCA 原型模型看不到這種高階的預防性動機，它會將這種現象錯誤地解讀為**「巨大的投資補貼 (Positive Investment Subsidy, 投資 Wedge 改善)」**與**「技術進步 (Efficiency Wedge 改善)」**。這就是非線性模型在線性會計系統下產生的「會計幻覺 (Accounting Illusions)」。

### 步驟 C：嚴格的模型篩選器 (Strict Model Selection Device)
這正是計畫書的核心亮點。我們將「Empirical Wedge vs. Simulated Wedge」的矛盾，轉化為數學上的**反證法 (Proof by Contradiction)**：
1.  **推翻假說**：原始 FVGQ 2020 的純金融擔保品限制，會產生「投資 Wedge 改善」的擴張幻覺，這與實證數據的「Wedge 惡化」完全矛盾。因此，純擔保品限制**無法**解釋現實中的不確定性衰退。
2.  **引入新機制**：這賦予了我們強大的學術正當性去引入**「營運資金限制 (Working Capital frictions)」**。當流動性凍結迫使廠商大砍勞動需求時，Simulated BCA 才能產出與現實世界相符的「衰退 Wedge 幾何特徵」。
3.  **量化對決**：透過計算 Empirical Wedges 與不同模型 Theoretical Wedges 之間的 RMSE，量化地選出最能解釋台灣現況的傳導管道。

---
**總結**：將 IRF 轉換為 Wedge 的意義，在於將「結果的配適 (Fitting outcomes)」提升為「機制的驗證 (Validating mechanisms)」。Simulated BCA 是看穿非線性模型黑箱的 X 光機，是本計畫方法論最具突破性的創新。
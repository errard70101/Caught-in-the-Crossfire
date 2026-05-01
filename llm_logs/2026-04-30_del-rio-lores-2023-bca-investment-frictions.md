# 討論主題：解讀 del Río and Lores (2023) 對於投資摩擦與 BCA 方法論的推進

**日期：** 2026-04-30
**文獻：** del Río, F., & Lores, F.-X. (2023). Accounting for the role of investment frictions in recessions. *Economica*, 90(360), 1089-1118.
**目的：** 分析這篇最新的 BCA 實證應用文獻，了解其對「要素份額 (Factor Shares)」的處理方式，以及如何透過 BCA 辨識「投資摩擦 (Investment Frictions)」，並評估其對本計畫的參考價值。

---

## 1. 文獻核心貢獻拆解

這篇發表在 *Economica* 的論文，是對 Chari, Kehoe, and McGrattan (2007, CKM) 傳統 BCA 方法的一個重要實證擴充。他們針對 1982 年衰退與 2008 年大蕭條進行分析，核心創新點在於**「引入了要素所得分配 (Factor Income Distribution) 的動態特徵」**。

### 傳統 CKM 的缺陷：單一效率楔子 (Single Efficiency Wedge)
在傳統的 CKM BCA 中，他們假設生產函數是 Cobb-Douglas (CD)，並將資本與勞動的相對效率視為常數。這導致他們只能萃取出一個單一的、代表 TFP 的「總效率楔子 (Total Efficiency Wedge)」。
*   **問題**：這會掩蓋底層的結構變動。如果「資本效率 (Capital-efficiency)」和「勞動效率 (Labour-efficiency)」往相反方向走，總效率楔子看起來會沒什麼變，讓人誤以為 TFP 衝擊不重要（例如 Brinca et al. 2016 認為大蕭條中 TFP 幾乎沒作用）。

### del Río & Lores (2023) 的解法：VES 生產函數與雙效率楔子
他們放棄了 CD 假設，改用**「變動替代彈性 (Variable Elasticity of Substitution, VES)」**生產函數。
1.  **變動的要素份額 (Variable Factor Shares)**：在 VES 下，資本和勞動的產出彈性不再是常數，而是會隨著資本勞動比改變。這允許他們將真實資料中「勞動份額 (Labour Share) 的下降」直接與競爭性市場下的邊際生產力變動連結起來。
2.  **拆解雙效率楔子**：透過引入要素份額的資料，他們成功將傳統的單一 TFP 楔子，拆解為**「勞動效率楔子 (Labour-efficiency Wedge, $z_t$)」**與**「資本效率楔子 (Capital-efficiency Wedge, $q_t$)」**。

### 實證發現：投資摩擦與資本效率楔子的重要性
透過他們的新方法重新檢視 2008 年大蕭條，他們發現：
*   **大蕭條的真相**：不是 TFP 沒變動，而是勞動效率與資本效率往反方向走。
*   **投資摩擦的主導角色**：他們發現，**「資本效率楔子 (Capital-efficiency Wedge)」**是推動大蕭條產出下滑的主要力量。
*   **理論對應**：這強烈支持了所謂的 **「投資摩擦理論 (Investment Friction Theory)」**（例如 Carlstrom and Fuerst 1997, Bernanke et al. 1999 的金融加速器）。當金融摩擦導致廠商的投資成本上升時，如果這些額外成本沒有被計入國民所得帳的「投資 (Investment)」數據中，它們在 BCA 中就會顯現為**「資本效率楔子 (Capital-efficiency Wedge)」的下降**（而非純粹的 Investment Wedge）。

---

## 2. 對我們計畫 (Caught in the Crossfire) 的啟示與應用

這篇文獻對我們非常有幫助，特別是在**解釋 Empirical Wedges** 以及**處理要素份額 (Factor Shares)** 方面。

### 價值 A：深化我們對「投資 Wedge」的解讀
我們在前面的討論中指出，金融不確定性（如純擔保品限制）會導致「投資 Wedge 改善（擴張幻覺）」，而代理成本或營運資金限制會導致「投資 Wedge 惡化」。
*   del Río & Lores (2023) 提醒我們，國民所得帳 (NIPA) 的統計口徑很重要。如果金融摩擦的成本沒有被計入總體投資數據中，這個金融衝擊在 CKM 框架下可能會同時投射到 **Investment Wedge** 和 **Efficiency Wedge (特別是 Capital-efficiency)** 上。
*   **[計畫書寫作應用]**：在說明 Simulated BCA 萃取出的 Empirical Wedges 時，我們可以引用此文：
    > 「在解讀 Simulated BCA 萃取出的楔子時，我們必須意識到國民所得帳統計口徑的限制。如 del Río and Lores (2023) 所指出，若金融摩擦（如代理成本或外部融資溢價）未被完整計入總體投資支出，這些摩擦將不僅投射為投資楔子 (Investment Wedge) 的惡化，亦會顯著反映在資本效率楔子 (Capital-efficiency Wedge) 的衰退上。因此，在我們的模型篩選機制中，我們將綜合評估 Investment Wedge 與 Efficiency Wedge 的聯合動態，以作為辨識深層金融摩擦（如營運資金限制）的雙重指紋。」

### 價值 B：提供「勞動份額 (Labor Share) 變動」的另類視角
我們的「營運資金限制 (Working Capital)」假說是為了解釋不確定性衝擊下 Labor Wedge 的劇烈惡化。
*   這篇文獻提醒我們，如果採用 VES 生產函數，Labor Share 的變動可以被解釋為純粹的技術因素（資本勞動替代），而非市場摩擦 (Wedges)。
*   這為我們的競爭假說提供了一個「技術性對照組」。
*   **[計畫書寫作應用]**：
    > 「此外，針對實證資料中勞動份額 (Labor Share) 的波動，除了我們提議的『營運資金限制』所引發的 Labor Wedge 惡化外，我們亦將考慮 del Río and Lores (2023) 提出的 VES 生產技術假說。透過將生產函數的替代彈性設定為非單一 (Non-unitary elasticity)，我們可進一步檢驗：台灣面對不確定性時的勞動市場緊縮，究竟是源自金融摩擦溢出 (Spillover) 的勞動楔子，還是僅為變動替代彈性下的內生技術調整。這種嚴謹的交叉驗證將進一步鞏固我們最終模型選擇的學術地位。」

---

## 3. 總結

del Río and Lores (2023) 這篇文獻：
1.  **不會改變我們的核心戰略**：我們仍然以 Simulated BCA 為主軸，並以 CKM 2007 原型模型作為 Baseline。因為引入 VES 會讓會計框架變得異常複雜，且偏離我們測試「金融摩擦」的主軸。
2.  **提供了絕佳的解讀深度與防禦論述**：它讓我們在計畫書中展現出對 BCA 方法最新發展的掌握，並提供了一套更細緻的語言去解釋 Investment Wedge 與 Labor Share 的聯動關係。

我們將把這篇文獻的洞見，作為計畫書「預期困難與解讀限制」或「競爭假說的延伸檢驗」中的重要潤飾元素。
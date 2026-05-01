# 討論主題：解讀 Baqaee and Farhi (2020) 對於總體會計與不確定性研究的啟示

**日期：** 2026-04-30
**文獻：** Baqaee, D. R., & Farhi, E. (2020). Productivity and Misallocation in General Equilibrium. *The Quarterly Journal of Economics*, 135(1), 105-163.
**目的：** 分析這篇將個體層次的「扭曲 (Wedges / Markups)」與「生產網路 (Production Networks)」結合的經典文獻，評估其對我們「Simulated BCA 篩選機制」與計畫書擴充的價值。

---

## 1. 文獻核心貢獻拆解

這篇 QJE 是一篇建立在 Hulten (1978) 基礎上的總體會計 (Growth Accounting) 鉅作。Hulten 定理表明，在「完全競爭 (Efficient)」的經濟體中，總體 TFP 的變動等於各部門 TFP 衝擊乘上其「營收 Domar 權重 (Revenue-based Domar weights)」。

Baqaee and Farhi (2020) 也就是 **BF2020** 解決了這個定理在**「無效率 (Inefficient) 經濟體」**中的崩潰問題。當經濟體充滿扭曲（如 Markups, Taxes, 或金融摩擦的 Wedges）時：
1.  **純技術效應 (Pure Technology Effect)** 的權重不再是「營收 Domar 權重」，而是必須改用需要解算整個 Input-Output 矩陣才能得到的**「成本 Domar 權重 (Cost-based Domar weights)」**。
2.  衝擊會引發資源的重新分配，產生一個全新的一階項：**「配置效率變動 (Changes in Allocative Efficiency)」**。

**他們的核心數學公式 (Theorem 1)：**
$$ \text{d} \log Y = \tilde{\lambda}' \text{d} \log A - \tilde{\lambda}' \text{d} \log \mu - \tilde{\Lambda}' \text{d} \log \Lambda $$
(總產出變動 = 純技術效應 + 配置效率變動)

---

## 2. 對我們 Simulated BCA 的推薦與應用價值

雖然 BF2020 主要探討的是跨產業/廠商的「靜態資源錯置 (Misallocation)」與「加總 (Aggregation)」，而不是處理「跨期的時間序列動態 (Business Cycle Dynamics)」或是「高階不確定性衝擊 (Uncertainty shocks)」，但這篇文章對我們的計畫有兩個**極高層次的戰略價值**。

### 價值 A：完美防禦 Reviewer 對 BCA「單一代表性個體」的質疑
我們在 Simulated BCA 中使用的是 CKM (2007) 的**單一代表性個體 (Representative Agent)** 模型。審查委員一定會攻擊：「台灣的企業異質性這麼高，有生產網路、有不同產業的 Markup，你用一個單一代表性個體的 BCA 算出來的 Wedge 有什麼意義？」

**BF2020 提供了最高級別的防禦盾牌！**
根據 BF2020 的理論，當經濟體存在異質性扭曲 (Heterogeneous Wedges) 與生產網路時，任何個體的衝擊都會透過網路產生**資源重分配效應 (Allocative Efficiency effects)**。
*   在一個單一代表性個體的 CKM 巨觀會計系統眼中，這些底層跨產業的資源重分配，無法被歸類為單純的技術進步，**它們必定會被「錯誤地投射 (Projected)」到巨觀的 Wedges 上！**
*   **[計畫書寫作應用]**：我們可以在計畫書中引用 BF2020 寫道：
    > 「Baqaee and Farhi (2020) 證明了，在充滿微觀異質性扭曲的生產網路中，資源重分配效應會破壞傳統的總體加總。延續此邏輯，我們主張：當底層金融摩擦引發跨部門的資源重分配時，這些微觀的 Allocative Efficiency 變動，在巨觀的 CKM (2007) 會計框架下，必然會被非線性地投射 (Projected) 為總體的 Labor Wedge 或 Investment Wedge。因此，我們萃取出的 Simulated Wedges，本質上就是這些微觀錯置在總體層次上的『加總指紋 (Aggregated Signature)』。」

### 價值 B：提供 Year 3 或未來延伸研究的終極武器 (Production Networks)
目前的計畫書 (Year 2) 主要聚焦在「時間序列 (VAR)」與「總體動態 (DSGE)」。
如果我們想要把這個計畫的格局拉到極致（或是為了回應 Reviewer 要求擴充外部效度），我們可以直接把 BF2020 的 **"Input-Output Networks" (生產網路)** 概念拉進來當作未來擴充方向。

*   **[計畫書寫作應用]**：在計畫書的「延伸討論 (Extensions)」或「預期學術貢獻」中加入這一段：
    > 「本計畫第二年建立的 Simulated BCA 模型篩選機制，主要聚焦於跨期的金融傳導。未來的延伸研究將結合 Baqaee and Farhi (2020) 的非線性生產網路加總理論，探討當美中不確定性衝擊透過『全球供應鏈 (Global Value Chains)』不對稱地打擊台灣特定產業時，產業間的投入產出連結 (Input-output linkages) 如何放大這些錯置，並最終投射為我們所觀測到的總體衰退 Wedges。這將為開放經濟體的不確定性研究，開啟結合『總體動態』與『微觀網路』的新頁。」

---

## 3. 總結

**BF2020 (Baqaee & Farhi)** 和 **CD2006 (Christiano & Davis)** 就像是我們這份計畫書的左右護法。
*   **CD 2006** 處理了 **Time-series (時間序列)** 上的 Wedge 敏感性與 Spillover 問題。
*   **BF 2020** 處理了 **Cross-section (橫斷面/網路)** 上的 Wedge 加總與 Misallocation 問題。

把它們巧妙地編織進我們的論述中，這份國科會計畫書在「文獻掌握度」和「方法論深度」上，將絕對是無懈可擊的 Top Tier 水準。
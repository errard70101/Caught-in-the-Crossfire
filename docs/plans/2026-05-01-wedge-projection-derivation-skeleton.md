# 二階 Wedge 投影：推導骨架與可解性評估

**日期：** 2026-05-01
**目的：** 將 `2026-04-30-mathematical-doubts-bca-projection.md` 第 1 節的散文式論述形式化，
評估「BCA 一階線性原型如何投影 DGP 的二階風險修正項」是否能寫出 closed-form mapping，
作為 Year 2 方法論章節的 **核心定理 (Theorem)** 候選。

---

## 0. 結論先行 (TL;DR for tractability)

✅ **是 tractable 的**。在合理假設下（對 SV 過程做 AR(1)、對 Hessian 取 steady-state 線性化），
可以得到一個閉式線性映射：

$$\hat\tau_{x,t} \;=\; \underbrace{\frac{\frac{1}{2}\Phi'(\bar\Omega)}{1-\omega_\tau \rho_\Omega}}_{\text{投影係數 }\kappa_x}\; \Omega_t \;+\; (\text{first-moment passthrough})$$

更重要的是，可以證明 **Sign Identification Theorem**：
- 純二階摩擦（如純擔保品 + SV）→ 投影到 $\tau_x$，符號由 Hessian 決定（多半是「補貼方向」）。
- 一階摩擦（如 Working Capital + 外部融資溢價）→ 投影到 after-tax labor wedge $\log(1-\tau_{\ell,t})$；對融資溢價上升的反應無條件為負。

這個 sign restriction **不依賴模擬數值大小**，是純代數的 — 正好繞過 §2 提到的「FVGQ 模擬訊號太小」問題。

---

## 1. Setup

### 1.1 BCA 原型模型 (CKM 2007)

無摩擦代表性家計，加入四個外生楔子：efficiency $A_t$、labor $\tau_{\ell,t}$、investment $\tau_{x,t}$、government $g_t$。
代表性家計 Euler equation（一階對數線性化於確定均衡 SS）：

$$
\hat\tau_{x,t} - \gamma \tilde C_t \;=\; \mathbb{E}_t\!\left[-\gamma \tilde C_{t+1} + \omega_K \tilde R^k_{t+1} + \omega_\tau \hat\tau_{x,t+1}\right]
\tag{B}
$$

其中 $\gamma$ 是相對風險趨避，$\omega_K, \omega_\tau$ 為 SS 比例係數，$\tilde R^k_{t+1}$ 是資本回報率。
注意：BCA 的觀察方程式中 $\tau_{x,t}$ **沒有被假設成 AR(1)**；那是 CKM 後處理模型，但 wedge 萃取時 Kalman smoother 是把 $\tau_{x,t}$ 當每期自由的 latent state 反推。

### 1.2 真實 DGP（FVGQ-style，含隨機波動）

FVGQ 2020（或任何含 SV 的 DSGE）的真實 Euler 在二階展開下：

$$
-\gamma \tilde C_t \;=\; \mathbb{E}_t\!\left[-\gamma \tilde C_{t+1} + \omega_K \tilde R^k_{t+1}\right] \;+\; \tfrac{1}{2}\,\Phi(\Omega_t) \;+\; \text{(高階小項)}
\tag{D}
$$

其中：
- $\Omega_t = \mathrm{Var}_t(z_{t+1})$ 是條件變異數矩陣（驅動隨機波動衝擊的核心 state）。
- $\Phi(\Omega_t) \equiv \mathrm{tr}(H\,\Omega_t)$，$H$ 為原效用函數與生產函數的 Hessian。
- 在 FVGQ 中，$\Omega_t$ 由 $u_{A,t}$（巨觀不確定性）與 $u_{e,t}$（金融不確定性）兩個 SV 衝擊驅動。

### 1.3 BCA 觀察 DGP 數據時的恆等式

把 (D) 中的 $(\tilde C_t, \tilde C_{t+1}, \tilde R^k_{t+1})$ 代入 (B)，得：

$$
\hat\tau_{x,t} \;=\; \omega_\tau \mathbb{E}_t \hat\tau_{x,t+1} \;+\; \tfrac{1}{2}\Phi(\Omega_t)
\tag{P}
$$

**這是 wedge projection equation。** 它告訴我們：BCA Kalman smoother 反推出來的 $\hat\tau_{x,t}$
在 DGP 真值上必須滿足這條前瞻式方程，被 $\Omega_t$ 強迫驅動。

---

## 2. 主要定理 (Wedge Projection Theorem)

### 2.1 假設

- (A1) $\Omega_t$ 為純量過程（最簡情形：只有一個 SV 因子驅動全模型 ⇒ $\Omega_t = \sigma_t^2$）或可被一個低維 state 摘要。
- (A2) $\Omega_t$ 服從 AR(1)：$\Omega_t = (1-\rho_\Omega)\bar\Omega + \rho_\Omega \Omega_{t-1} + \eta_t$，$\rho_\Omega \in [0,1)$。
- (A3) $\Phi$ 在 $\bar\Omega$ 處可微，記 $\phi \equiv \Phi'(\bar\Omega)$。
- (A4) $|\omega_\tau| < 1$（成立，因為 $\omega_\tau$ 是 SS 比例係數）。

### 2.2 命題 1（投影係數的 closed form）

對 (P) 前瞻迭代：

$$
\hat\tau_{x,t} \;=\; \tfrac{1}{2}\sum_{j=0}^{\infty}\omega_\tau^{\,j}\,\mathbb{E}_t\Phi(\Omega_{t+j}).
$$

由 (A2)–(A3)：$\mathbb{E}_t\Phi(\Omega_{t+j}) \approx \Phi(\bar\Omega) + \phi\,\rho_\Omega^{j}(\Omega_t-\bar\Omega)$。代入並收斂級數：

$$
\boxed{\;\hat\tau_{x,t} \;=\; \frac{\Phi(\bar\Omega)}{2(1-\omega_\tau)} \;+\; \underbrace{\frac{\phi}{2(1-\omega_\tau\rho_\Omega)}}_{\equiv\,\kappa_x}\,\big(\Omega_t-\bar\Omega\big).\;}
\tag{T1}
$$

**解讀**：
- **持續性**：$\hat\tau_{x,t}$ 繼承 $\Omega_t$ 的 AR(1) 持續性 $\rho_\Omega$。BCA 後處理會看到一個「貌似 AR(1) 的 wedge」，但其真實驅動力是 SV state，這就是 BCA 把二階訊號偽裝為一階 AR(1) wedge 的代數機制。
- **量級**：$|\kappa_x|$ 由分母 $1-\omega_\tau\rho_\Omega \in (0,1)$ 放大；高 $\rho_\Omega$（Bloom 式持續性衝擊）放大幅度更明顯。
- **符號**：完全由 Hessian $\phi = \Phi'(\bar\Omega)$ 的符號決定 — 與摩擦結構掛鉤。

### 2.3 符號分析（Sign Lemma）

針對不同摩擦結構，$\Phi$ 對應的經濟內容：

| DGP 結構 | $\Phi(\Omega)$ 的主導項 | $\phi$ 符號 | $\hat\tau_x$ 對 $\Omega\uparrow$ 反應 |
|---|---|---|---|
| 純擔保品限制 (FVGQ baseline) | $+\tfrac{1}{2}u''' \mathrm{Var}(C)$ + 擔保品凸性 | **$\phi > 0$** | **$\hat\tau_x \uparrow$**（"投資補貼 / 擴張幻覺"） |
| 凹效用 + 二階預防動機 | $-\tfrac{1}{2}\gamma(\gamma+1)\sigma_C^2$ | **$\phi > 0$**（在 $\tau_x$ 為負稅率定義下） | 同上 |
| 工資 working capital（一階） | （見 §2.4，不入 $\Phi$） | — | **0**（不直接出現在 $\tau_x$） |

關鍵：純粹由二階風險修正驅動的摩擦，**幾乎都會把訊號投到 $\tau_x$**，且方向是
"看似補貼"。這就是 plans 一直在講的「Accounting Illusion」的代數來源 — 但現在是定理，不是 anecdote。

### 2.4 Working Capital 的一階通道（命題 2）

為避免符號混淆，本節把 CKM 的 after-tax labor wedge 記為

$$
\Lambda_{\ell,t}\equiv 1-\tau_{\ell,t}^{\text{tax}},
$$

並令本文前面的 $\hat\tau_{\ell,t}$ 讀作 $\hat\Lambda_{\ell,t}$。也就是說：
**$\hat\Lambda_{\ell,t}<0$ 代表勞動楔子惡化**；若改報稅率 $\tau_{\ell,t}^{\text{tax}}$，符號會反過來。

WC 假設廠商在生產前必須融資支付 $\theta_{wc}$ 比例的 wage bill。令
$q_t$ 為外部融資溢價（或 real borrowing spread），且 $\bar q$ 為 SS 值。
廠商的靜態問題可寫成：

$$
\max_{L_t}\; A_tF(K_t,L_t)-w_tL_t\,[1+\theta_{wc}q_t].
$$

因此 labor demand FOC 為

$$
A_tF_{L,t}
\;=\;
w_t\,[1+\theta_{wc}q_t].
\tag{WC-FOC}
$$

BCA 的 intratemporal labor equation 則是：

$$
-\frac{U_L(C_t,L_t)}{U_C(C_t,L_t)}
\;=\;
\Lambda_{\ell,t}^{BCA} A_tF_{L,t}.
\tag{BCA-L}
$$

真實 DGP 的 household FOC 給出 $-U_L/U_C=w_t$。把它和 (WC-FOC) 代入 (BCA-L)，得到精確投影恆等式：

$$
\Lambda_{\ell,t}^{BCA}
\;=\;
\frac{w_t}{A_tF_{L,t}}
\;=\;
\frac{1}{1+\theta_{wc}q_t}.
\tag{WC-P}
$$

對 (WC-P) 在 $\bar q$ 附近取 log-linear approximation：

$$
\hat\Lambda_{\ell,t}^{BCA}
\;=\;
-\,\underbrace{\frac{\theta_{wc}}{1+\theta_{wc}\bar q}}_{\lambda_{wc}>0}\,(q_t-\bar q)
\;+\;
O\!\left((q_t-\bar q)^2\right).
\tag{WC-LIN}
$$

令外部融資溢價在一階近似下響應金融緊縮衝擊：

$$
q_t-\bar q
\;=\;
\alpha_\xi \hat\xi_t+\alpha_\Omega(\Omega_t-\bar\Omega)+o(\|\hat\xi_t,\Omega_t-\bar\Omega\|),
\qquad
\alpha_\xi>0,\;\alpha_\Omega\ge 0.
\tag{RP}
$$

代回 (WC-LIN) 得到命題 2：

$$
\boxed{\;
\hat\Lambda_{\ell,t}^{BCA}
\;=\;
-\,\lambda_{wc}\alpha_\xi\hat\xi_t
-\,\lambda_{wc}\alpha_\Omega(\Omega_t-\bar\Omega)
\;+\;
O(\hat\xi_t^2)+O((\Omega_t-\bar\Omega)^2).
\;}
\tag{T2}
$$

若採最簡規格 $\bar q=0$、$\alpha_\Omega=0$，則回到原本的簡式：

$$
\hat\Lambda_{\ell,t}^{BCA}
\;=\;
-\,\theta_{wc}\alpha_\xi\hat\xi_t
\;+\;
O(\hat\xi_t^2).
$$

**解讀**：
- **一階大小**：若 $\hat\xi_t=O(\sigma)$，則 $|\hat\Lambda_{\ell,t}|=O(\sigma)$，大於純 SV Hessian 投影的 $|\hat\tau_{x,t}|=O(\sigma^2)$。
- **符號明確負向**：金融緊縮 $\hat\xi_t>0$ 或不確定性推升融資溢價 $\alpha_\Omega(\Omega_t-\bar\Omega)>0$ 時，$\hat\Lambda_{\ell,t}<0$（after-tax labor wedge 下降）。
- **不直接進入 $\tau_x$**：若 WC 只融資 wage bill，(WC-FOC) 是靜態 labor demand distortion；capital Euler 的直接二階投影仍由 §2.2 的 $\Phi(\Omega_t)$ 決定。WC 對 $\tau_x$ 的影響只會透過一般均衡變數 $(C,K,L,R^k)$ 間接出現，不產生 $\alpha_\xi\hat\xi_t$ 的一階 Euler 項。

### 2.5 主結果：可分辨性 (Identification Theorem)

**Theorem (Wedge Sign Identification).** 在假設 (A1)–(A4) 下，再加上
$\lambda_{wc}>0$、$\alpha_\xi>0$、$\alpha_\Omega\ge 0$，且
$\mathbb E[\hat\xi_t\mid\Omega_t-\bar\Omega]=\rho_{\xi\Omega}(\Omega_t-\bar\Omega)$、$\rho_{\xi\Omega}\ge0$。
對於 SV 環境中的不確定性衝擊 $\Omega_t$ 與其相伴的金融緊縮衝擊 $\xi_t$：

**Part I：純二階摩擦假說 $H_0^{\text{coll}}$.**
若 DGP 僅含擔保品凸性與 SV，且不含 wage-bill WC，則：

$$
\mathbb E[\hat\tau_{x,t}\mid \Delta\Omega_t]
\;=\;
\kappa_x\Delta\Omega_t+o(\Delta\Omega_t),
\qquad
\kappa_x=\frac{\phi}{2(1-\omega_\tau\rho_\Omega)}.
\tag{S1}
$$

在 FVGQ financial-collateral channel 中，§2.3 的 sign lemma 給出 $\phi_e>0$，因此
$\mathbb E[\hat\tau_{x,t}\mid \Delta\Omega_{e,t}>0]>0$。同時，因 labor wedge 是靜態條件，且 DGP 沒有直接的 labor-demand wedge：

$$
\mathbb E[\hat\Lambda_{\ell,t}\mid \Delta\Omega_t]
\;=\;
O(\Delta\Omega_t)
\quad\text{且沒有由 }\xi_t\text{ 驅動的 signed first-order term.}
\tag{S2}
$$

**Proof sketch.** (S1) 直接由命題 1 得到；分母為正，所以符號由 $\phi$ 決定。(S2) 來自 BCA labor identity：
$\Lambda_{\ell,t}=(-U_L/U_C)/(A_tF_L)$。若真實 DGP 的 household FOC 與 production block 與 BCA 相同，且沒有 WC 或 labor tax distortion，則一階上
$-U_L/U_C=A_tF_L$，所以 $\hat\Lambda_{\ell,t}=0$。剩餘項只能來自二階聚合、非線性或模型錯設，因此沒有 WC 那種固定負號。

**Part II：Working Capital 假說 $H_1^{\text{wc}}$.**
若 DGP 含 wage-bill WC，則由命題 2：

$$
\mathbb E[\hat\Lambda_{\ell,t}\mid \Delta\Omega_t]
\;=\;
-\,\lambda_{wc}\left(\alpha_\xi\rho_{\xi\Omega}+\alpha_\Omega\right)\Delta\Omega_t
\;+\;
o(\Delta\Omega_t)
\;<\;0,
\tag{S3}
$$

只要外部不確定性會推升融資溢價
$(\alpha_\xi\rho_{\xi\Omega}+\alpha_\Omega)>0$。此外，若金融緊縮 $\hat\xi_t$ 是一階 first-moment shock，則
$|\hat\Lambda_{\ell,t}|=O(\sigma)$，而純 Hessian 投影的 $|\hat\tau_{x,t}|=O(\sigma^2)$，故 WC labor signal 在局部量級上主導。若研究設計只給純 SV shock、沒有 contemporaneous first-moment tightening，兩者可同為 $O(\Delta\Omega_t)$；但 WC 的 labor wedge 符號仍由 (WC-P) 固定為負，不由 Hessian 或 risk-premium covariance 決定。

**Proof sketch.** (S3) 是 (T2) 對 $\Delta\Omega_t$ 取條件期望。因
$\lambda_{wc}>0$、$\alpha_\xi\rho_{\xi\Omega}+\alpha_\Omega>0$，係數必為負。又因 WC 進入的是 static labor demand FOC，而非 intertemporal Euler equation，$\tau_x$ 不含 $\alpha_\xi\hat\xi_t$ 的直接一階項；因此 wedge pattern 與 $H_0^{\text{coll}}$ 分離。

**可檢驗指紋**：
- $H_0^{\text{coll}}$：$\tau_x$ 對金融不確定性為正或由 Hessian 決定；after-tax labor wedge $\Lambda_\ell$ 沒有穩定負號。
- $H_1^{\text{wc}}$：after-tax labor wedge $\Lambda_\ell$ 對金融不確定性穩定為負；若資料報告的是 labor-tax rate $\tau_\ell^{tax}$，則同一結果表現為 $\tau_\ell^{tax}$ 上升。

**因此**：實證若出現 $\log(1-\tau_\ell)$ 顯著負向、$\tau_x$ 訊號弱或正向，則拒絕「純二階擔保品」解釋，支持 Working Capital 一階傳導。若只看到 $\tau_x$ 的正向補貼幻覺、而 labor wedge 沒有穩定惡化，則較接近 FVGQ baseline 的純擔保品機制。

---

## 3. 為什麼這是 A+ 級貢獻

1. **不靠 simulation 大小**：拒絕的是符號模式而非量級擬合。FVGQ preliminary 結果中 $\tau_x$ 訊號小（~1e-3）的問題不再是計畫殺手 — 因為定理告訴我們它不需要大，只需要 **方向是錯的**。
2. **形式化「Accounting Illusion」**：把 plans 散文中的 "BCA 看不到 $\frac{1}{2}\mathrm{tr}(H\Omega)$" 翻譯為一條**閉式投影方程 (P)** 與**可驗證符號模式**。
3. **與 Christiano-Davis (2006) 的對話**：CD 指控 BCA 把摩擦溢出到多個 wedge 是 BCA 的弱點；本定理把這個溢出**結構化**為與摩擦階數 (1st vs 2nd order) 相關的可識別模式 — 變成 BCA 的特徵 (feature) 而非缺陷 (bug)。
4. **與 del Río & Lores (2023) 的對話**：他們處理的是 NIPA 統計口徑導致的雙楔子漂移；本定理處理的是**非線性階數**導致的雙楔子漂移 — 是不同的 source of leakage，可以正交補強。

---

## 4. 接下來要做的事 (To formalize this into a paper)

優先序：

1. **(2 週) 把 (P) 寫嚴謹**：列出 FVGQ 2020 的完整 Euler，明確算出 $\Phi(\Omega_t)$ 的 closed form（含 $u'''$、$F_{KK}$、collateral multiplier 等具體項）。
2. **(2 週) 模擬驗證命題 1**：用既有 FVGQ Dynare code，繪製 $\hat\tau_{x,t}$ vs $\Omega_t$ 的散點圖，檢驗 $\kappa_x$ 預測值 vs 實際 GIRF。**這就是 plans 提到的 FVGQ preliminary 應該做的事**。
3. **(4 週) WC 模擬**：命題 2 的代數骨架已在 §2.4–§2.5 補上；下一步是在 FVGQ Dynare code 中加入 WC，檢驗 (T2) 與 sign identification theorem 是否成立。
4. **(同時進行) 拓展到多維 $\Omega_t$**：FVGQ 有 $u_A, u_e$ 兩個 SV state，要證明命題 1 推廣為 $\hat\tau_{x,t} = \kappa_{x,A}\Omega_{A,t} + \kappa_{x,e}\Omega_{e,t}$，且兩個 channel 可區分。
5. **(寫作) 以這個 theorem 為計畫書 Y2 Section 2 的核心**，取代目前的 Competing Hypotheses 散文式論述。

---

## 5. 已知的開放問題（不影響 tractability）

- **Pruning 與三階解的處理**：(D) 的二階展開假設 $E_t \tilde C_{t+1}$ 等於確定均衡值，但實際三階 pruning 解中還有 $\tilde C_t$ 對 $\Omega_t$ 的內生迴授（FVGQ 的 risk-adjusted SS 平移）。這會在 $\Phi$ 中加額外項，不會改變 sign，但會影響 $\kappa_x$ 的數值。
- **多維 $\Omega_t$ 的識別**：若 $u_A$ 與 $u_e$ 不正交（共動），則 $\kappa_{x,A}$ 與 $\kappa_{x,e}$ 不能單獨識別，需要額外假設。這在實證上未必是問題（OI-SVMVAR 把這兩個 latent factor 用 normalization 識別）。
- **Hessian 的計算**：對 FVGQ 這種有擔保品 occasionally binding 的模型，Hessian 在 binding/non-binding 邊界不連續。建議第一輪只取 always-binding 的局部解。

---

**總結：**
這個推導**完全 tractable**，且核心定理（Sign Identification Theorem）是現有 BCA 文獻沒有的結果。
建議當作 Year 2 計畫的方法論主軸，並在 Y2 Sec 2 重寫時取代 Competing Hypotheses 框架的部分散文。

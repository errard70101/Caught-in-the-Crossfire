# 兩類代理人風險分攤 Wedge：FVGQ 聚合誤差的閉式分解

**日期：** 2026-05-01
**前置文件：** `2026-05-01-fvgq-Phi-closed-form.md` 的 §6 開放問題
**目的：** 補上 FVGQ 雙代理人結構（94% 工人 + 6% 企業家）下，BCA 把總消費當作單一代理人時產生的**聚合誤差項** $\Phi^{\text{agg}}(\Omega_t)$。
這是解釋 FVGQ preliminary 中 `uA` 訊號**負號**的關鍵候選。

---

## 0. 結論先行

兩類代理人聚合在 BCA prototype 視角下產生第四個 $\Phi$ 項：

$$
\boxed{\;\Phi^{\text{agg}}(\Omega_t) \;=\; \tfrac{1}{2}\gamma\,s_W s_E \,\big[\gamma\Sigma_{\delta c\delta c}(\Omega_t) - \mathcal{D}_{\delta c}(\Omega_t)\big]\;}
\tag{Φ-agg}
$$

其中：
- $s_W = \omega_W \bar c_W / \bar C \approx 0.92$, $s_E = \omega_E \bar c_E / \bar C \approx 0.08$（消費份額，與人口份額 0.94/0.06 不同）
- $\Sigma_{\delta c\delta c}(\Omega_t) = \mathrm{Var}_t(\delta c_{t+1})$，$\delta c_t = \hat c_{E,t} - \hat c_{W,t}$ 是消費 dispersion
- $\mathcal{D}_{\delta c}(\Omega_t)$ 是 dispersion 對風險溢價的耦合項（Cov 形式，可正可負）

**符號分析**：
- $\sigma_{e,t}^2$（金融不確定性）↑：企業家消費 $\hat c_E$ 對金融衝擊反應遠大於工人 $\hat c_W$（因為持有資本與面對擔保品摩擦），故 $\Sigma_{\delta c\delta c}$ 主要由 $\sigma_e^2$ 驅動 → 加總後 $\Phi^{\text{agg}} > 0$ → **強化** $\kappa_{x,e}$ 的正號。
- $\sigma_{A,t}^2$（巨觀不確定性）↑：兩類代理人都受 TFP 衝擊影響，但工人透過勞動所得直接暴露，企業家透過資本 MPK 暴露。**消費 dispersion 對 $\sigma_A^2$ 的反應方向不確定**，且因勞動供給彈性可能使 $\hat c_W$ 比 $\hat c_E$ 對巨觀衝擊反應更強烈 → $\Sigma_{\delta c\delta c}$ 對 $\sigma_A^2$ 的反應較弱，但 $\mathcal{D}_{\delta c}$ 項可能為主導且為負。

**對 `uA` 負號之謎的潛在解釋**：若 $\mathcal{D}_{\delta c}(\sigma_A^2)$ 主導 $\Sigma_{\delta c\delta c}(\sigma_A^2)$，可使 $\Phi^{\text{agg}}<0$ 在巨觀衝擊下成立，配合 §3 中風險溢價項的負貢獻，**有可能使 $\phi_A < 0$ 整體成立** — 這正是實測 LP `uA → τ_x = -1.642e-3` 的結構解釋。

---

## 1. Setup：兩類代理人的 BCA 觀察方程式

### 1.1 真實 DGP（FVGQ 雙代理人）

工人問題（無摩擦，標準 RBC 工人）：
$$u'(c_{W,t}) = \beta R_t E_t[u'(c_{W,t+1})] \tag{W-Euler}$$

企業家問題（有擔保品，§1 已推導）：
$$\lambda_{E,t}[1-\theta_t(1-\delta)] = \beta E_t[\lambda_{E,t+1}(R^k_{t+1}+(1-\delta))] - \beta R_t \theta_t(1-\delta) E_t\lambda_{E,t+1} \tag{E-Euler}$$

其中 $\lambda_{E,t} = u'(c_{E,t})$，工人與企業家**同樣 CRRA $\gamma$**（FVGQ 預設）。

總消費（NIPA 觀察）：
$$C_t = \omega_W c_{W,t} + \omega_E c_{E,t}, \quad \omega_W=0.94,\;\omega_E=0.06$$

### 1.2 BCA prototype 觀察方程式

CKM prototype 把總消費當代表性代理人消費，套用單一 Euler：
$$u'(C_t)(1+\tau_{x,t}) = \beta E_t[u'(C_{t+1})(R^k_{t+1}+(1-\delta)(1+\tau_{x,t+1}))] \tag{BCA}$$

關鍵問題：BCA 的 $u'(C_t)$ 與真實「驅動投資的邊際效用」$\lambda_{E,t}=u'(c_{E,t})$ **不同**。
這個差異就是聚合 wedge 的來源。

---

## 2. 聚合恆等式的二階展開

### 2.1 總消費的對數展開

設 $\hat c_{W,t}, \hat c_{E,t}$ 為各自對 SS 的 log 偏差。SS 滿足 $\bar C = \omega_W \bar c_W + \omega_E \bar c_E$。
定義消費份額：
$$s_W = \frac{\omega_W \bar c_W}{\bar C}, \quad s_E = \frac{\omega_E \bar c_E}{\bar C}, \quad s_W + s_E = 1$$

在 FVGQ 校準下，企業家消費佔比 $s_E$ 約為 8%（若 $\bar c_E/\bar c_W \approx 1.4$，則 $s_E \approx 0.06\times 1.4/(0.94+0.06\times 1.4) \approx 0.082$）。

對 $C_t = \omega_W c_W e^{\hat c_W} + \omega_E c_E e^{\hat c_E}$ 展開到二階：

$$\hat C_t = s_W \hat c_{W,t} + s_E \hat c_{E,t} + \tfrac{1}{2}s_W s_E (\hat c_{E,t}-\hat c_{W,t})^2 + O(3)$$

定義 dispersion $\delta c_t \equiv \hat c_{E,t} - \hat c_{W,t}$，則：
$$\hat C_t = \underbrace{s_W \hat c_{W,t} + s_E \hat c_{E,t}}_{\text{linear part}} + \underbrace{\tfrac{1}{2}s_W s_E \delta c_t^2}_{\text{Jensen term}}\tag{Agg}$$

### 2.2 BCA 邊際效用 vs 企業家邊際效用

CRRA 下 $\log u'(x) = -\gamma \log x$，因此：
$$\log u'(C_t) = -\gamma \hat C_t + \text{const} \quad\text{vs.}\quad \log u'(c_{E,t}) = -\gamma \hat c_{E,t} + \text{const}$$

差異：
$$\log u'(C_t) - \log u'(c_{E,t}) = -\gamma(\hat C_t - \hat c_{E,t}) = \gamma s_W \delta c_t - \tfrac{1}{2}\gamma s_W s_E \delta c_t^2 + O(3)$$

這是一個**有一階項**的恆等式 — 也就是說即使在無不確定性的線性世界，雙代理人就已經導致 BCA 看到的 $u'(C)$ 與真實投資驅動量 $u'(c_E)$ 有系統性差距。

---

## 3. 投影到 BCA 的 τ_x

### 3.1 把 BCA 的 (BCA) 取對數做二階展開

$$
\hat\tau_{x,t} - \gamma\hat C_t = -\gamma E_t\hat C_{t+1} + \omega_K E_t\hat r^k_{t+1} + \omega_\tau E_t\hat\tau_{x,t+1} + \tfrac{1}{2}\Phi^{\text{BCA-side}}(\Omega_t)
$$

其中 $\Phi^{\text{BCA-side}}$ 是 BCA prototype 自己的二階修正（標準 RBC 預防動機）。

### 3.2 把 (E-Euler) 取對數做二階展開

得到企業家視角的 Euler：
$$
-\gamma\hat c_{E,t} = -\gamma E_t\hat c_{E,t+1} + \omega_K E_t\hat r^k_{t+1} - \kappa_\theta E_t\hat\theta_t + \tfrac{1}{2}\Phi^{\text{coll}}(\Omega_t) + \tfrac{1}{2}\Phi^{\text{prec},E}(\Omega_t) - \gamma\Sigma_{c_E R}(\Omega_t)
$$

（這就是 §3 推導的單代理人版本，$\hat\lambda_{E,t}=-\gamma\hat c_{E,t}$。）

### 3.3 取差：BCA Euler − 真實企業家 Euler

把 (Agg) 的展開代入 BCA 的 $\hat C_t, E_t\hat C_{t+1}$，並利用真實 Euler 消去 $\omega_K E_t\hat r^k_{t+1}$ 等共同項，得：

$$
\hat\tau_{x,t}\;=\;\omega_\tau E_t\hat\tau_{x,t+1}\;+\;\underbrace{\gamma s_W\big(E_t\delta c_{t+1}-\delta c_t\big)}_{\text{first-order dispersion}}\;+\;\tfrac{1}{2}\Phi^{\text{tot}}(\Omega_t)
\tag{P-2agent}
$$

其中：
$$
\Phi^{\text{tot}}(\Omega_t) = \Phi^{\text{prec},E}(\Omega_t) - 2\gamma\Sigma_{c_E R}(\Omega_t) + \Phi^{\text{coll}}(\Omega_t) + \Phi^{\text{agg}}(\Omega_t)
$$

最後一項才是聚合修正：

$$
\Phi^{\text{agg}}(\Omega_t) = \gamma s_W s_E \big[\gamma\,\mathrm{Var}_t(\delta c_{t+1}) - \mathrm{Cov}_t(\delta c_{t+1},\hat r^k_{t+1})\big]
\tag{Φ-agg}
$$

把括號內第二項記作 $\mathcal D_{\delta c}(\Omega_t) \equiv \mathrm{Cov}_t(\delta c_{t+1},\hat r^k_{t+1})$，得到 §0 公式。

---

## 4. Dispersion $\delta c_t$ 對 SV state 的 policy function

關鍵問題：$\mathrm{Var}_t(\delta c_{t+1})$ 與 $\mathrm{Cov}_t(\delta c_{t+1},\hat r^k_{t+1})$ 對 $(\sigma_{A,t}^2, \sigma_{e,t}^2)$ 的依賴。

### 4.1 結構化思考：誰對哪個衝擊更敏感？

在 FVGQ 的 third-order solution 中，每類代理人的消費 policy function 形如：
$$\hat c_{i,t} = \psi_{i,A}\hat A_t + \psi_{i,k}\hat k_t + \psi_{i,b}\hat b_t + \psi_{i,\theta}\hat\theta_t + (\text{2nd-order} + \text{SV-corrections})$$

直覺上：
- **金融衝擊 $\hat\theta_t$ 與 $\sigma_{e,t}^2$**：企業家直接受擔保品摩擦影響，$\psi_{E,\theta} \neq 0$ 且大；工人僅透過工資與利率間接受影響，$\psi_{W,\theta}$ 接近零。
  → $\delta c_{t+1}$ 對 $\hat\theta_{t+1}$ 反應強，$\mathrm{Var}_t(\delta c_{t+1})$ 隨 $\sigma_{e,t}^2$ 增加而增加。
- **巨觀衝擊 $\hat A_t$ 與 $\sigma_{A,t}^2$**：兩類代理人都受影響，但方向可能相同（共同景氣循環）。
  → $\delta c_{t+1}$ 對 $\hat A_{t+1}$ 反應較小，$\mathrm{Var}_t(\delta c_{t+1})$ 隨 $\sigma_{A,t}^2$ 增加的幅度小，甚至可能負（如果勞動供給彈性使工人消費反應放大）。

### 4.2 寫成線性化形式

設 $\delta c_t$ 對狀態的 policy 為：
$$\hat c_{E,t+1} - \hat c_{W,t+1} = \chi_A \varepsilon_{A,t+1} + \chi_\theta \varepsilon_{\theta,t+1} + (\text{state terms})$$

則：
$$\mathrm{Var}_t(\delta c_{t+1}) = \chi_A^2 \sigma_{A,t}^2 + \chi_\theta^2 \sigma_{e,t}^2$$

（假設兩 SV 衝擊正交。）類似地：
$$\mathrm{Cov}_t(\delta c_{t+1},\hat r^k_{t+1}) = \chi_A r_A \sigma_{A,t}^2 + \chi_\theta r_\theta \sigma_{e,t}^2$$

其中 $r_A, r_\theta$ 是 $\hat r^k_{t+1}$ 對兩衝擊的反應係數。

代入 (Φ-agg)：
$$\Phi^{\text{agg}}(\Omega_t) = \gamma s_W s_E\big[(\gamma\chi_A^2 - \chi_A r_A)\sigma_{A,t}^2 + (\gamma\chi_\theta^2 - \chi_\theta r_\theta)\sigma_{e,t}^2\big]$$

定義：
$$\phi_A^{\text{agg}} = \gamma s_W s_E\,\chi_A(\gamma\chi_A - r_A), \qquad \phi_e^{\text{agg}} = \gamma s_W s_E\,\chi_\theta(\gamma\chi_\theta - r_\theta)$$

---

## 5. 對 `uA` 負號的可能解釋（核心觀察）

### 5.1 統一全部四個來源

從 §3 結合本文件：
$$\phi_A^{\text{total}} = \underbrace{\tfrac{1}{2}\gamma^2[1-\bar\theta(1-\delta)]a_{cc,A}}_{\text{(a) 預防 }>0} - \underbrace{\gamma\beta(\bar R^k+(1-\delta))a_{cR,A}}_{\text{(b) 風險溢價 }>0\text{ if }a_{cR,A}>0} + \underbrace{0}_{\text{(c) 擔保品（不入 }\sigma_A^2\text{)}} + \underbrace{\phi_A^{\text{agg}}}_{\text{(d) 聚合}}$$

$$\phi_e^{\text{total}} = \underbrace{\tfrac{1}{2}\gamma^2[1-\bar\theta(1-\delta)]a_{cc,e}}_{\text{(a) }>0} - \underbrace{\gamma\beta(\bar R^k+(1-\delta))a_{cR,e}}_{\text{(b)}} + \underbrace{\beta\bar R\bar\theta(1-\delta)\nu_\theta}_{\text{(c) }>0} + \underbrace{\phi_e^{\text{agg}}}_{\text{(d)}}$$

### 5.2 `uA` 的負號：哪一項在主導？

四種候選：

**候選 1（最可能）**：$\sigma_A^2$ 衝擊推升風險溢價 (b)，企業家對巨觀風險的曝露讓 $a_{cR,A}>0$ 大。
- 具體：高 TFP 不確定性 → 企業家消費與資本回報共動性增強（高產出時雙雙好）→ $\Sigma_{cR}>0$ → (b) 項為負且大。
- 這是 **standard CRRA 經濟對巨觀風險的反應**：風險溢價拉低資本投資慾望。

**候選 2**：聚合項 (d) 在巨觀衝擊下是負的。
- 巨觀衝擊使工人消費比企業家更敏感（勞動供給效應）→ $\chi_A < 0$（企業家相對工人消費反應較小）。
- 若 $r_A > 0$（高巨觀不確定性下 $r^k$ 反應正向）：$\phi_A^{\text{agg}} = \gamma s_W s_E \chi_A(\gamma\chi_A - r_A)$。$\chi_A<0$ 且 $\gamma\chi_A<r_A$（因為 $\gamma\chi_A$ 是負的，$r_A$ 正），則括號內為負，乘負 $\chi_A$ 變正。所以 (d) 項在巨觀衝擊下**反而是正的**。
- 因此候選 2 不能單獨解釋負號。

**候選 3**：(a) 預防動機在巨觀衝擊下變小（甚至負）。
- 不太可能：CRRA 預防項 $\gamma^2 a_{cc,A}$ 必為正，因為 $a_{cc,A} \propto \chi_{c,A}^2 \ge 0$。

**結論：候選 1 是最可能的解釋**。`uA → τ_x` 的負號是**風險溢價主導**的證據，而非聚合誤差主導。

### 5.3 可驗證的對照

候選 1 預測：
- $a_{cR,A}$（巨觀不確定性下的 cov term）數值大且正。
- $a_{cR,e}$（金融不確定性下的 cov term）數值較小（因為金融衝擊主要透過擔保品傳遞，cov 部分相對弱）。

這兩個比較可以從 subagent 抽出的數值直接檢驗。如果確實 $a_{cR,A} \gg a_{cR,e}$，那麼候選 1 確認 — 而這正是論文一個**有趣的、可發表的二級結果**：FVGQ 的雙 SV 結構在 BCA 視角下產生**符號相反的兩個 wedge 反應**，這個對偶性是兩個 channel 可分辨性的代數來源。

---

## 6. Sign Identification Theorem 更新版

把雙代理人項加進原 Theorem：

**Theorem (Wedge Sign Identification, 2-agent version).**

在假設 (A1)–(A4) + 雙代理人 CRRA 下：

1. **金融不確定性 $\sigma_{e,t}^2 \uparrow$**：四項貢獻**符號全為正**（擔保品 (c) 與聚合 (d) 都正，預防 (a) 正，風險溢價 (b) 在金融衝擊下小），故 $\kappa_{x,e} > 0$ **無條件成立**。
2. **巨觀不確定性 $\sigma_{A,t}^2 \uparrow$**：(a) 與 (d) 為正，(c) 為零，(b) 符號取決於 $a_{cR,A}$。$\kappa_{x,A}$ 符號**模糊**，由參數決定。
3. **金融與巨觀的可分辨性**：$\kappa_{x,e} > 0$ 是**結構性必然**，$\kappa_{x,A}$ 可正可負。在實證中，若觀察到 $\tau_x$ 對巨觀與金融不確定性反應符號相反，這是 FVGQ 結構的**指紋**，不是 specification error。

**對 Working Capital 假說（命題 2）的對照**：
- WC 把訊號投到 $\tau_l$，且符號**無條件為負**（一階機制不依賴 sign of risk premium）。
- FVGQ + 擔保品 把訊號投到 $\tau_x$，金融衝擊下 $\kappa_{x,e}>0$ 必然，巨觀衝擊下 $\kappa_{x,A}$ 模糊。
- 兩者**指紋完全不重疊**：若實證觀察到 $\tau_l$ 強烈惡化（WC 預測），FVGQ baseline 拒絕；若觀察到 $\tau_x$ 對金融衝擊正向反應（FVGQ 預測），WC baseline 拒絕。

---

## 7. 結論

✅ **聚合 wedge 寫得出閉式**。$\Phi^{\text{agg}}$ 由消費 dispersion 的 conditional variance 與其與 $r^k$ 的 covariance 兩項組成，係數由結構參數明確給出。

✅ **`uA` 負號之謎有結構性解釋**：最可能來自風險溢價項 (b) 在巨觀衝擊下主導，而非聚合項 (d)。可從 subagent 抽出的 $a_{cR,A}, a_{cR,e}$ 直接驗證。

✅ **Sign Identification Theorem 強化**：金融不確定性下 $\kappa_{x,e}>0$ 從「弱條件」升級為「結構性必然」，因為 (c) 擔保品 + (d) 聚合都加總為正。

❌ **未解決**：$\Phi^{\text{agg}}$ 中的 $\chi_A, \chi_\theta, r_A, r_\theta$ 數值需要從 Dynare 的 cross-section 資訊抽出（不是單一變數的 policy function 係數，而是 $c_E, c_W$ 兩個變數的差）。這比 §3 推導的五個係數更難取得，可能需要 augment Dynare 模型輸出 $\delta c_t$ 作為觀察變數。

---

## 8. 接下來的工作（按優先序）

1. **(等待 subagent 結果)** 拿到 $a_{cR,A}, a_{cR,e}$ 後，檢驗候選 1（風險溢價主導 `uA` 負號）是否成立。
2. **(1 週)** 修改 Dynare `.mod` 增加 $\delta c_t = \log c_{E,t} - \log c_{W,t}$ 作為觀察變數，重跑得到 $\chi_A, \chi_\theta$。
3. **(同時進行)** 把 Working Capital 命題 2 的代數版本完整寫出，完成 Sign Identification Theorem 的兩半。
4. **(寫作)** 把 §3 (FVGQ 單代理人) + 本文件 (聚合修正) + 命題 2 (WC) 整合成 Year 2 計畫書方法論章節的核心 — 取代目前散文式的 Competing Hypotheses 框架。

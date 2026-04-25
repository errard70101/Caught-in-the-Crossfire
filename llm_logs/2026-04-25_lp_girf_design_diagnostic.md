# LP/GIRF 信賴區間過寬的研究設計診斷與修正

**Date:** 2026-04-25
**Spec:** `docs/superpowers/specs/2026-04-24-fvgq2020-preliminary-simulated-bca-design.md`
**Plan:** `docs/superpowers/plans/2026-04-24-fvgq2020-preliminary-simulated-bca.md`
**Code:** `code/bca_uncertainty_simulation/fvgq2020_preliminary/`
**Predecessor memo:** `llm_logs/2026-04-24_fvgq2020_preliminary_results.md`

## 問題描述

`bca_lp_*.png` 與 `bca_girf_*.png` 中所有 wedge 的 5-95% 區間都涵蓋零，
表面上看像是「結果不顯著」。經研究設計面診斷後，判定主要是**呈現方式**
與**控制變數選擇**造成的視覺與量級扭曲，而非 DGP 本身對 (uA, ue) 沒有
反應。

## 區間意義釐清

| 物件 | 目前呈現 | 實際意義 |
|------|---------|---------|
| GIRF 5-95% band (N=1000 antithetic pairs) | 看似「mean 不顯著」 | **跨初始狀態的 state-dependent 離散度**，不是 mean GIRF 的精度 |
| LP MC band (B=10000 × T=400) | 看似 DGP 反應微弱 | **T=400 短樣本下實證家的估計分布**，不是 T=20000 全樣本的 LP 精度 |

GIRF 的 mean SE 為 `std(diffs)/√N ≈ band/(2·1.645·√1000) ≈ band/65` —— 比
原本顯示的橫斷面 90% 區間窄兩個數量級。把 N=1000 條路徑的「橫斷面異質性」
當成「平均反應的估計誤差」，等於把人群身高的離散度誤當成平均身高的標準誤。

## 已實作的修正（2026-04-25）

### 修正 1：GIRF 圖改為單一 mean precision 帶

`run_bca_analysis.m` 額外儲存 `se_mean, ci_lo_mean, ci_hi_mean, N` 至每個
GIRF struct（`girf.<tag>`、`girf_likelihood.<tag>`、
`girf_transformed.<tag>`、`girf_transformed_likelihood.<tag>`）。

**初版（2026-04-25 早上）** 的 `plot_girf_single` 採雙帶呈現
（外層 5–95% pair-dispersion + 內層 mean precision），但因為 dispersion
帶寬度約是 precision 帶的 **26 倍**（理論值 √1000 ≈ 31.6 同量級），視覺
上 mean 線被外帶完全壓過，且容易讓讀者誤判 mean 為「不顯著」。

**修訂版（2026-04-25 下午，現行）** 的 `plot_girf_single` 改為**只**畫
mean ± 1.96·SE/√N 一條帶與 mean 線。完整外帶資訊仍保留在
`wedges_girf.mat` 與 `wedges_girf_likelihood.mat` 的 `q05/q95` 欄位中，
未來若需要 state-dependent dispersion 的視覺呈現（例如項目 6 的 conditional
GIRF），可從 `.mat` 重繪。`plot_girf_compare` 同步改為比較 mean precision
帶。

新圖檔（已重新生成於 2026-04-25 09:32）：

- `output/bca_girf_{macro,fin}.png`：fixed-point 版本
- `output/bca_girf_{macro,fin}_likelihood.png`：likelihood-smoothed 版本
- `output/bca_girf_compare_{macro,fin}.png`：fixed vs likelihood 對照

### 修正 2：DGP-precision LP 圖（fixed-point T=20000 HAC）

新增頭條圖 `bca_lp_<ts>_dgp.png`，**直接讀取既有的 `lp_results.mat`**
（已是 fixed-point T=20000 HAC SE 的 LP）並繪製。它與 `bca_lp_<ts>_fixed.png`
（B=10000 × T=400 MC 短樣本帶）形成互補：

| 圖檔 | 樣本長度 | 區間意義 |
|------|---------|---------|
| `bca_lp_<ts>_dgp.png` | T=20000 | **DGP precision**：總體真值的精度估計 |
| `bca_lp_<ts>_fixed.png` | T=400 × B=10000 | **Empirical relevance**：25 年資料的實務情境 |
| `bca_lp_<ts>.png` | T=20000 (likelihood) | likelihood-smoothed wedge 上的 DGP precision |

這樣讀者可以分辨「DGP 真的沒反應」vs「短樣本看不出反應」。

### 修正 3：移除 contemporaneous SV-state 控制變數的敏感度 LP

原本控制集合 `[eA, ed, ethet, ud, sigAt, sigdt, siget, lagged_targets]`
中的 `sigAt, sigdt, siget` 是當期 SV 狀態。但根據 `.mod` 中的方程：

```
sigAt = (1-rhosigA)*sigA + rhosigA*sigAt(-1) + (1-rhosigA^2)^0.5*metaA*uA
```

`sigAt` **由 uA 在當期構成**，是 (uA → wedge) 因果鏈的中介變數
(mediator)。把 mediator 放進 control 等於關掉因果通路本身——這是教科書
級的後門偏誤誤用。

新增 sensitivity LP：控制集合改為 `[eA, ed, ethet, ud, lagged_targets]`，
完全捨棄 SV-state 控制。輸出：

- `output/lp_results_no_svctrl.mat`
- `output/lp_results_likelihood_no_svctrl.mat`
- `output/lp_no_svctrl_peak_comparison.csv`（baseline vs no-SV peak 比較表）
- `output/bca_lp_<ts>_no_svctrl.png`（baseline 與 sensitivity 並排比較圖）

預期觀察：`uA, ue` 的 LP 係數量級會放大。若放大後仍然小，說明 wedge 對
SV shock 的反應確實微弱；若放大顯著，原本的「不顯著」是 over-controlling
造成的人為現象。

## 未來實作（記錄優先順序）

### 項目 4：加大 SV shock 規模到 4–6 標準差

**動機：** SV shock `uA` 透過 `σ_A,t = ρ·σ_A,t-1 + scale·uA` 進入模型，
再以 `σ²·∂²/∂z²` 的二階項影響輸出。同期樣本中存在四個一階 level shock
(`eA, ed, ethet`) 在量級上壓過二階通路。FVGQ (2020) 原文 IRF 用的是 vol
從低到高水平的 jump（相當於數個 SD），不是 `2 SD` 的 innovation。

**規格：**
- 修改 `run_fvgq2020_simulation.m` Phase 3：`exp2_shock_size` 從 `2` 改為
  分別嘗試 `4, 6, 8`（同時保留 baseline = 2 作為對照）
- 預期效果：mean GIRF 量級線性放大；state-dependence 帶寬可能非線性放
  大（高階非線性的證據）；mean 顯著性應改善
- 報告：對每個 shock size，記錄 mean peak / SE / state-dep band，列表
  比較

**檔案異動：**
- `run_fvgq2020_simulation.m`：在 `run_experiment2` 加入 shock_size 迴圈
- `run_bca_analysis.m`：對每個 shock size 各儲存一份 `wedges_girf_size<k>.mat`
- `plot_bca_responses.m`：新增 `bca_girf_<ts>_size_grid.png`（多 shock size
  並排）

**估計工時：** ~2 小時（需重跑 Experiment 2，每個 shock size N=1000 對；
總時間視 simult\_ 速度而定）

### 項目 5：以標準 GIRF 差分取代 antithetic ±ε 配對

**動機：** Antithetic 配對 `+ε vs −ε` 的變異數縮減邏輯成立的前提是反應
對 ε **線性對稱**。但 SV channel 是 `|ε|·η` 進入未來 σ → σ² 影響輸出，
+ε 與 −ε 對未來 vol 的效果**同號**（兩者都拉高 |scale·ε| 的當期 vol
innovation），antithetic 配對在 SV 上**沒有變異數消減效果**，反而把訊號
對沖掉。

**規格：** 採用 Koop-Pesaran-Potter (1996) 標準 GIRF：

```
GIRF(h, shock, history) = E[Y_{t+h} | shock_t = k·σ, history_t]
                        − E[Y_{t+h} | shock_t = 0, history_t]
```

實作：
- 從 ergodic distribution 抽 N 個 history（沿用現有暖機路徑各時點當作初
  始狀態）
- 每個 history 跑兩條：一條 shock_t = k·σ 後續 ε 從標準分布抽樣 M 次取平
  均；一條 shock_t = 0 同樣 M 次平均（相同 future ε 序列以共同隨機數縮減
  變異）
- GIRF = mean over N histories of (shock path − no-shock path)

**檔案異動：**
- `run_fvgq2020_simulation.m`：替換 `run_experiment2` 為新的 GIRF 邏輯
  (N 個 history × M 個 future innovation draw，而非 N 個 antithetic pair)
- `run_bca_analysis.m`：GIRF 計算邏輯改為先對 future innovations 平均，
  再對 history 求 mean 與 quantiles

**估計工時：** ~4 小時（涉及變更計算結構，建議先在 plan 中設新 task）

### 項目 6：條件 GIRF（依 ergodic σ 分位數）

**動機：** 目前的 5-95% band 把所有狀態的反應混在一起，掩蓋了
state-dependence 的方向性。把 history 依 ergodic σ_A 與 σ_e 分位數分組
（例如低/中/高 vol regime, 三組 = 33%/34%/33%）後分別計算 mean GIRF，
可以同時呈現 state-dependence **與**每個 regime 內的精度。

**規格：**
- 從 history 集合中根據 σ 排序分為三組
- 每組計算 group mean GIRF + group SE/√n_g
- 圖：`bca_girf_<ts>_by_regime.png`，三個 regime 三條線疊在同一個 panel

**額外延伸：** 也可以條件 on (σ_A, σ_e) 聯合分位數，看 macro-vol 高 vs
fin-vol 高的 wedge 反應差異——這正是 §7 設計關心的「哪個 channel 主導」。

**檔案異動：**
- `run_bca_analysis.m`：新增 conditional GIRF 計算邏輯
- `plot_bca_responses.m`：新增 regime-conditional 繪圖函數

**估計工時：** ~2 小時（在項目 5 的新 GIRF 結構下實作會更乾淨；建議放在
項目 5 之後）

## 建議的實作順序

| 順序 | 項目 | 原因 |
|------|------|------|
| 1 | **修正 1, 2, 3（已完成）** | 純呈現/控制集合修正，零成本，立即得到正確判讀 |
| 2 | **項目 4（shock size 加大）** | 只動 simult\_ 階段參數，最低成本驗證訊號上限 |
| 3 | **項目 5（標準 GIRF 差分）** | 結構性修正，與項目 6 為 prerequisite |
| 4 | **項目 6（條件 GIRF）** | 在項目 5 完成後最有資訊量 |

## 修正 1, 2, 3 執行結果（2026-04-25 09:13）

### 結果一：GIRF mean precision band 揭露顯著反應

修正 1 把 `mean ± 1.96·SE/√N` 加為內帶後，原本「5-95% dispersion 全部覆
蓋零」的視覺印象完全顛覆。在 fixed-point transformed wedges 上：

| Shock | Wedge | Peak mean | h | 95% CI for mean | Dispersion 5-95% | 分位帶 / 平均 CI 寬度比 |
|-------|-------|-----------|---|-----------------|------------------|------------------------|
| macro `uA` | log_efficiency | -2.03e-3 | 5 | [-3.24e-3, -8.27e-4] | [-3.59e-2, +2.74e-2] | 26.2x |
| macro `uA` | log_labor | -1.53e-3 | 6 | [-2.61e-3, -4.48e-4] | [-2.96e-2, +2.62e-2] | 25.8x |
| macro `uA` | log_investment | +7.34e-4 | 10 | [+3.62e-4, +1.11e-3] | [-8.19e-3, +1.14e-2] | 26.3x |
| fin `ue` | log_efficiency | +6.55e-4 | 4 | [+1.77e-4, +1.13e-3] | [-1.19e-2, +1.32e-2] | 26.3x |
| fin `ue` | log_labor | +4.94e-4 | 6 | [+2.29e-4, +7.58e-4] | [-6.39e-3, +7.37e-3] | 26.0x |
| fin `ue` | log_investment | +6.77e-5 | 46 | [+1.38e-5, +1.22e-4] | [-1.31e-3, +1.41e-3] | 25.2x |

**所有 6 個 (shock × wedge) 組合的 mean precision CI 都不涵蓋零**。
分位帶寬比平均 CI 寬度大 ~26 倍——精確匹配 `2·1.645·√(1000) /
(1.96·1.96·2) ≈ 26.5` 的理論值。

跨 horizon 看 mean CI 排除零的比例：

| Wedge | Macro shock | Financial shock |
|-------|-------------|-----------------|
| log_efficiency | 81.7% (49/60) | 53.3% (32/60) |
| log_labor | 100% (60/60) | 100% (60/60) |
| log_investment | 75.0% (45/60) | 93.3% (56/60) |

**結論：mean GIRF 在大多數 horizon 顯著非零**。原本的「不顯著」是把
state-dependent dispersion 誤當成 mean 精度造成的視覺假象。

### 結果二：DGP-precision LP 仍極為微弱（但 SV channel 在 state 層面顯著）

T=20000 HAC fixed-point LP 在多數 horizon **無法**拒絕零：

| Wedge | Macro shock 排除零 % | Financial shock 排除零 % |
|-------|---------------------|--------------------------|
| log_efficiency | 3.3% (2/61) | 1.6% (1/61) |
| log_labor | 0.0% (0/61) | 0.0% (0/61) |
| log_investment | 4.9% (3/61) | 6.6% (4/61) |

**但是**——`bca_lp_*_dgp.png` 右下角的 SV-state sanity-check panel 顯示，
DGP 中 SV channel 在 state 層面**極度乾淨且顯著**：

| LHS | shock | h=0 peak β | 95% CI |
|-----|-------|------------|--------|
| `sigAt` | `uA` | **0.685** | [0.674, 0.696] |
| `siget` | `ue` | **0.698** | [0.687, 0.709] |

CI 半寬 ~0.011，相對 peak 量級（0.69）只有 1.6%——這是教科書級的
identification。所以 channel 完全存在；問題出在從 σ_t 到 wedge 的
傳導。peak wedge β 量級只有 1×10⁻³ 而 HAC SE ~1×10⁻³，訊噪比剛好在
拒絕零的門檻附近，所以幾乎所有 horizon CI 都涵蓋零。

**新解讀**：LP 的問題不是「沒識別出來」——是「DGP 中 σ_t → wedge_t+h
的線性投影本身就小到 LP 在 T=20000 都無法可靠分辨」。GIRF 的
paired-difference 設計把 history 變異控制掉、N=1000 條路徑做平均，
有效樣本量遠大於 LP 的 T=20000，因此可以挑出這個小訊號。

### 結果三：移除 SV-state 控制揭露 LP 估計**不穩定**（不是訊號變強或變弱）

`lp_no_svctrl_peak_comparison.csv` 的 peak 比較：

| Wedge | Shock | Baseline peak (h) | No-SV-ctrl peak (h) | Ratio |
|-------|-------|-------------------|---------------------|-------|
| log_efficiency | macro | +1.03e-3 (15) | -7.15e-4 (19) | -0.69 |
| log_efficiency | fin | +1.04e-3 (25) | -5.97e-4 (37) | -0.57 |
| log_labor | macro | +1.02e-3 (3) | -6.95e-4 (58) | -0.68 |
| log_labor | fin | -8.58e-4 (15) | +7.53e-4 (20) | -0.88 |
| log_investment | macro | +1.43e-3 (58) | +1.08e-3 (23) | 0.76 |
| log_investment | fin | +1.85e-3 (15) | +1.35e-3 (36) | 0.73 |

我的事前預測（移除 mediator 後 LP 係數會放大）**錯了**。事後深入比較
發現問題比「縮小」更嚴重——是**整體不穩定**：

#### 三條診斷指標

| 指標 | Baseline (含 SV ctrl) | 無 SV ctrl | 解讀 |
|------|----------------------|-----------|------|
| **平均 CI 寬度比** | 1.0 | **0.74–0.76x** | 移除 3 個共線 regressors 確實壓低 SE 約 25%（多元共線性確認） |
| **拒絕零 horizon 比率** | efficiency 1–3%, labor 0%, investment 5–7% | efficiency 0%, labor 0%, investment 2–8% | SE 變窄但 point estimate 也變小，拒絕零比率沒有改善 |
| **Horizon-by-horizon 同號比率** | — | efficiency 23%/41%, labor 28%/38%, investment 51%/54% (macro/fin) | **接近隨機 50%；efficiency 與 labor 甚至遠低於隨機** |

#### 為什麼「同號比率近隨機」是震撼點

如果 baseline LP 與 no_svctrl LP 都在估同一個真實參數 β(h)，sign agreement
應遠高於 50%（隨機水準）——只要兩個版本都接近 β(h) 的真實符號，sign
agreement 就會接近 100%。

但實際上 efficiency wedge 在 macro shock 下 sign agreement 只有 **23%**——
**比隨機還低**。這只可能在以下情境發生：兩個 LP 估計與真實 β(h) 都沒有
高相關，且兩個的誤差結構**負相關**（一邊偏正時另一邊偏負）。

技術解釋：

1. Baseline 加了 (sigAt, sigdt, siget) 三個與 (uA, ue) 高度共線的 regressors
2. 在多元共線性下，OLS 對 design matrix 的微小變動極度敏感
   （Belsley-Kuh-Welsch 條件數爆炸現象）
3. 拿掉三個共線 regressors 後，殘餘 controls 中 lagged_targets 仍部分
   捕捉 SV 傳導，但**捕捉的方式跟 baseline 完全不同**
4. 兩個版本各自在小訊號 + 大共線雜訊中估出**不相關的雜訊**

**結論：baseline 與 no_svctrl 的 LP 圖形差異不是「兩個版本之間的 trade-off」，
而是「兩個版本都不穩定到不能信賴點估計」**。CI 變窄 25% 是「清掉假相關」
的副產品，不是「找到真訊號」的後果。

#### 對 LP 角色的最終判斷

把結果二（DGP-precision LP 拒絕零比率 0–7%）和結果三（baseline vs no_svctrl
sign agreement 23–54%，近隨機）合起來：

- **LP 在這個問題上不只低效率，而且不穩定**
- 不同合理的 control 集合會給出形狀甚至方向都不同的 LP curve
- 這意味著任何用 LP 講的故事（例如「ue 主要走 τ_x channel」）**對 control
  specification 高度敏感，無法穩健支持**
- §7 設計絕不能以 LP signature 作為主要對標物件

### 整體結論

| 修正 | 結果 | 強度等級 |
|------|------|---------|
| 1 (GIRF mean precision 帶) | **問題解決**：mean GIRF 在絕大多數 horizon 顯著（macro 75–100%、fin 53–100%）；原本的「不顯著」是把 state-dependent dispersion 誤當作 mean 精度的視覺假象 | ★★★ |
| 2 (DGP-precision LP, T=20000 HAC) | **發現 DGP channel 在 state 層面極為乾淨**（sigAt 對 uA 反應 0.685, CI 半寬 1.6%）但 wedge LP 仍涵蓋零（拒絕零 0–7% horizons），確認問題在 σ_t→wedge 的線性投影量級小於 LP 解析度 | ★★★ |
| 3 (移除 SV-state 控制) | **LP 估計不穩定**：baseline vs no_svctrl 的 sign agreement 只有 23–54%，efficiency 與 labor wedge 接近或低於隨機水準 → LP 對 control specification 極度敏感，沒有可信內在訊號 | ★★★ |

**三項合在一起的判讀：**

1. **DGP 是好的**：FVGQ 第三階解的 SV channel 在 state 層面乾淨且強，
   GIRF 的 paired-difference 設計能把 wedge response 識別到 mean ± 1.96·SE
   不涵蓋零。
2. **LP 不是好工具**：對 SV shock 的識別效率不足（即使 T=20000）且結果
   對 control specification 不穩定。任何用 LP 講的 channel ranking 故事
   都不該作為強論點。
3. **§7 對標物件確定為 GIRF mean signature**，而非任何 LP 變體。LP 圖仍
   可在論文 robustness 章節呈現「實證家面對 25 年資料看到什麼」，但要
   配合 sign-agreement 的警語。

## 後續判斷

修正 1 解除視覺扭曲、修正 2-3 釐清 LP 角色之後，項目 4-6 的優先順序需要
重新評估：

- **項目 4（加大 shock size）**：仍有價值，但動機改變。
  原本動機是「測試訊號能否壓過 level shock 雜訊」；現在發現 mean GIRF
  在 2 SD 下已顯著，所以項目 4 的角色變成「測試 wedge signature 在不同
  shock 規模下的形狀穩定性」——若 4 SD 的形狀與 2 SD 形狀相同（線性
  scaling），可確認非線性的角色；若形狀變化，是高階非線性的關鍵證據。
- **項目 5（標準 GIRF 差分）**：antithetic 對 SV 不對稱的論點仍成立。
  在 KPP-1996 標準差分下 mean GIRF 應更乾淨；項目 5 完成後可比較與目前
  antithetic 結果的差異。
- **項目 6（regime-conditional GIRF）**：state-dispersion 26x 已確認顯著
  state-dependence；conditional GIRF 應在項目 5 之後實作以利用更乾淨的
  GIRF 結構。

**建議下一步：項目 5（標準 GIRF 差分）優先於項目 4**——因為當前 mean
GIRF 已顯著，「形狀對不對」比「能不能挑出來」更重要，而 antithetic 有
原則性問題需要先修。項目 4 與項目 6 在項目 5 完成後同步推進。

## 圖檔交叉索引

| 圖檔 | 看什麼 | 統計學上是什麼 |
|------|--------|---------------|
| `bca_girf_<ts>.png` / `_likelihood.png` | mean GIRF 的可信精度 | 1000 antithetic pairs 的 mean ± 1.96·SE/√N |
| `bca_lp_<ts>.png` (likelihood headline) | T=20000 likelihood-smoothed wedge LP | HAC 95% CI |
| `bca_lp_<ts>_dgp.png` | T=20000 fixed-point wedge LP（含 SV-state sanity 子圖） | HAC 95% CI；SV-state 子圖確認 channel 在 state 層面乾淨 |
| `bca_lp_<ts>_fixed.png` | T=400 短樣本 fixed-point MC LP | B=10000 monte-carlo median + 2.5–97.5% band |
| `bca_lp_<ts>_no_svctrl.png` | baseline vs 移除 SV ctrl 的 LP 比較 | 兩個 HAC LP 並列；sign agreement 接近隨機警示 LP 不穩定 |
| `bca_lp_compare_<ts>.png` | fixed vs likelihood LP 對照 | 兩個 LP 並列 |
| `bca_girf_compare_<ts>.png` | fixed vs likelihood GIRF mean precision 對照 | 兩個 mean ± 1.96·SE/√N 並列 |
| `bca_measured_wedges_{fixed,likelihood}.png` | wedge 時序 (CKM-style 指數，t=1=100) | 描述性 |

## 對 §7 設計的意涵

若修正 1, 2, 3 後 mean GIRF 顯著（兩個 shock 在多 horizon 的 0 在 95% CI
之外），則：

1. FVGQ 的 SV channel 確實會被 CKM 翻譯成可量化的 wedge 反應
2. **LP-GIRF 落差**仍是衡量高階非線性的關鍵診斷物件（Insight 1）
3. §7 的 RA + LWZ + CGK 設計可以以 FVGQ preliminary 的 wedge signature 作
   為「已知答案」，驗證新模型是否能再現相同的 (efficiency, labor,
   investment) 投影模式

若仍不顯著，則項目 4 必跑——shock size 是排除「訊噪比天生過低」的關鍵。

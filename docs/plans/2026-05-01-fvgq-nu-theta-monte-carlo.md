# FVGQ `ν_θ` Monte Carlo 驗證

日期：2026-05-01  
Script：`code/bca_uncertainty_simulation/fvgq2020_preliminary/matlab/mc_nu_theta.m`  
輸出：`output/mc_nu_theta_grid.csv`, `output/mc_nu_theta_summary.csv`

## 設定

使用 `simulated_workspace.mat` 中的 Dynare 6.2 pruned third-order decision rule，直接呼叫 `simult_(M_, options_, sss_state, oo_.dr, ex, 3)`。起點為 stochastic steady state，僅覆寫初始 `siget`。Grid 為 `sige ± 2*std(siget)` 的 11 點；`.mod` 中 `sige=-4.7975`, `rhosige=0.75`, `metae=1.0479`，故 `std(siget)=metae`。每個 grid 跑 1000 條、T=200；條件矩使用第 1 期 cross-sectional MC 分布。所有 innovations 均抽 N(0,1)。無模擬失敗。

## Grid 結果

| siget | sigma_e^2 | E[log lambda] | Var_t(log c) | Cov_t(log c, log rk) |
|---:|---:|---:|---:|---:|
| -6.8934 | 1.029e-06 | -0.213383 | 1.53559e-04 | -2.55019e-06 |
| -6.4742 | 2.380e-06 | -0.213402 | 1.53483e-04 | -2.51249e-06 |
| -6.0551 | 5.503e-06 | -0.213422 | 1.53428e-04 | -2.48926e-06 |
| -5.6359 | 1.273e-05 | -0.213444 | 1.53393e-04 | -2.47980e-06 |
| -5.2167 | 2.943e-05 | -0.213468 | 1.53379e-04 | -2.48559e-06 |
| -4.7975 | 6.806e-05 | -0.213494 | 1.53390e-04 | -2.51028e-06 |
| -4.3784 | 1.574e-04 | -0.213521 | 1.53433e-04 | -2.55970e-06 |
| -3.9592 | 3.640e-04 | -0.213550 | 1.53517e-04 | -2.64180e-06 |
| -3.5400 | 8.417e-04 | -0.213580 | 1.53652e-04 | -2.76675e-06 |
| -3.1208 | 1.947e-03 | -0.213612 | 1.53853e-04 | -2.94683e-06 |
| -2.7017 | 4.502e-03 | -0.213646 | 1.54136e-04 | -3.19654e-06 |

## Regression

以 `sigma_e^2=exp(2*siget)` 為 x、11 點全域 OLS：

- `ν_θ = d E[log lambda] / d sigma_e^2 = -4.933e-02`, SE `1.324e-02`, 95% CI `[-7.928e-02, -1.937e-02]`。
- `a_cc,e^MC = 1.635e-04`, SE `1.585e-05`, 95% CI `[1.276e-04, 1.993e-04]`。
- `a_cR,e^MC = -1.619e-04`, SE `1.435e-05`, 95% CI `[-1.943e-04, -1.294e-04]`。

Sanity check：全域 `a_cc,e^MC` 只有先前 ghxu 係數 `4.115e-04` 的 39.7%，不算通過。但若只用 SS 附近中央 3 點，斜率為 `4.347e-04`，與 `4.115e-04` 相差 +5.6%。判讀：局部 perturbation sanity check 成立；±2 unconditional std 的 11 點全域回歸受非線性影響，不能視為單一局部導數。

## Collateral Term

校準係數 `beta*Rbar*theta_bar*(1-delta)=0.093849`。因此每單位 `sigma_e^2` 的擔保品項為 `0.093849*ν_θ = -4.629e-03`。對一個 unit `ue` shock，`Delta sigma_e^2=9.44e-5`，擔保品修正為 `-4.370e-07`。

把它加進原本 `κ_x,e=2.04e-03` 後：

`κ_x,e^revised = 2.03956e-03`，相對 LP 實測 `+1.886e-03` 高約 8.1%。此 MC 抽到的擔保品項很小且為負，沒有提供原先期待的正向補缺；目前吻合度主要來自原本的 `κ_x,e`，不是 `ν_θ`。

## 技術障礙

Dynare pruning function 可用，未遇到路徑爆炸或非正消費。主要限制是估計目標本身：全域 grid 線性斜率與 SS 局部導數不同，導致 `a_cc,e` sanity check 在全域規格下失敗。若 theorem 需要的是 SS 局部 `ν_θ`，下一步應改用更窄 grid 或 common-random-number central difference，而不是 ±2 std 全域 OLS。

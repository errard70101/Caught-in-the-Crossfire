# FVGQ aggregation wedge numerical check

**日期：** 2026-05-01  
**來源：** `fvgq2020_preliminary/output/simulated_workspace.mat`  
**輸出：** `output/cE_extraction/cE_cW_sv_loading_results.{json,csv}`

`.mod` 已有單獨代理人消費：`ce`, `cw`，且
`cspt = ifrac*ce + (1-ifrac)*cw`，`ifrac=0.06`。不需修改或重跑 Dynare。

## 1. cE / cW SV-loading

所有係數為 log-deviation。`ghxu` 使用 `order_var` 重新對齊，並用
`cspt = s_E ce + s_W cw` 通過一階加總檢查。

| channel | ψ_E | ψ_W | ghxu_E | ghxu_W |
|---|---:|---:|---:|---:|
| A: `eA`, `sigAt` | -9.852e-4 | 5.812e-3 | -7.389e-4 | 4.359e-3 |
| e: `ethet`, `siget` | -5.266e-3 | 3.477e-4 | -3.949e-3 | 2.608e-4 |

SS consumption shares: `s_W=0.97249`, `s_E=0.02751`; `γ=2`.

## 2. χ and r

用前次 cspt 相同邏輯，以 `ghu`/`ghxu` 算
`∂Var/∂σ²` 與 `∂Cov/∂σ²`，再回推有效 loading：

| channel | χ | r | ∂Var/∂σ² | ∂Cov/∂σ² |
|---|---:|---:|---:|---:|
| A | -8.410e-1 | 2.710e-2 | 7.073e-1 | -2.279e-2 |
| e | -5.892e-1 | -8.806e-3 | 3.472e-1 | 5.189e-3 |

## 3. Aggregation wedge

套入
`φ^agg = γ s_W s_E [γ ∂Var(δc)/∂σ² - ∂Cov(δc,rk)/∂σ²]`：

| channel | φ^agg |
|---|---:|
| A | 7.692e-2 |
| e | 3.688e-2 |

兩項都是正的；A channel 不會產生負號反轉。

## 4. Updated κ and LP comparison

沿用前次報告的 convention：
`κ = φ / [2(1-ω_τ ρ_σ)]`，其中 `1-ω_τ ρ_σ=0.27025`，完整分母為 `0.5405`。

| channel | φ original | φ updated | κ updated | LP |
|---|---:|---:|---:|---:|
| A | 8.399e-1 | 9.168e-1 | 1.696 | -1.642e-3 |
| e | 1.105e-3 | 3.799e-2 | 7.028e-2 | 1.886e-3 |

若改用 `0.27025` 當分母，κ 只會全部加倍，結論不變。

## 5. Conclusion

聚合項不能解釋 `(a)` `uA` 負號：`φ_A^agg>0`，更新後 κ_A 仍為正且遠離 LP 負值。  
對 `(b)` `ue` 量級，聚合項確實大幅提高 κ_e，但若直接比較 κ，會從 `2.04e-3` 推到 `7.03e-2`，反而高於 LP 約 37 倍；若轉成單位 `ue` impact，仍小於 LP peak。它不是完整的四個數量級修正。

技術障礙：主要是 Dynare `oo_.dr.gh*` row 不是宣告順序，必須用 `order_var` 對齊；未遇到缺少 `c_E/c_W` 變數的問題。

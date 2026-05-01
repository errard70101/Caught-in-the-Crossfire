# Research Plan Diagnostic: Caught in the Crossfire

**Date:** 2026-05-01  
**Input:** Free review of the current research plan, recent `llm_logs`, plans, data status, and preliminary simulation outputs.

## Overview

The strongest part of the project remains the Year 1 empirical idea: use DHK-style OI-SVMVAR unclassified variables not to ask "which uncertainty dominates Taiwan?", but to ask "through which domestic channel do external U.S.-China shocks enter Taiwan?" This is a genuine small-open-economy reinterpretation of the DHK classification device, not a country replication.

The main risk is now scope drift. The repo contains three partially competing Year 2 narratives: archived SOE nonlinear BCA, the written conditional SOE DSGE competing-hypotheses framework, and the newer Simulated BCA / wedge-comparison model-selection idea. The latter is promising, but it should not be allowed to weaken the clean Year 1 contribution or make the NSTC proposal look over-committed.

## Key Findings

### 1. The Core Direction Is Still Sound

The key methodological decisions from `llm_logs/2025-11-08_discussion.md` still look correct:

- Keep DHK's two-factor structure: \(h_t=(h_{m,t},h_{f,t})'\).
- Do not add a third global uncertainty factor.
- Do not impose block exogeneity inside the order-invariant sampler.
- Put external variables in the unclassified block and interpret their time-varying classification as the transmission-channel object.

This should remain the center of gravity.

### 2. Current Documents Are Inconsistent

Several files disagree on the final empirical design:

- Variable count appears as 43, 45, and 47.
- Unclassified count appears as 16 and 22.
- Sample appears as 2000M1-2025M6, 2000M1-2025M12, and 2001M1-2025M12.
- Year 2 is described as SOE nonlinear BCA, conditional SOE DSGE, and Simulated BCA model selection in different places.

This is not cosmetic. Reviewers will infer that the project is still unsettled if these numbers are not harmonized.

### 3. Data Status Is Better Than Old Task Files Suggest

The old project-management files still say data collection is near 0%, but `data/raw` already contains 39 CSV files and 45 numeric series columns. A quick inventory found:

- 42 numeric series have complete 2001M1-2025M12 coverage.
- `cn_m2` ends at 2013M12 and cannot enter a 2001-2025 balanced panel as-is.
- `tw_wpi` ends at 2022M12 and needs a PPI splice or replacement.
- `gl_gepu` currently ends at 2025M11, missing only 2025M12.
- Important planned variables are still missing: China IPI/PPI, TWSE foreign flows, margin buying, short selling, house prices, import/export price indices, sector employment, and NDC business-cycle signal score.

The project can already build a 40+ variable preliminary panel, but not yet the final planned 47-variable panel.

### 4. Lightweight Transmission-Channel Proxy Check

I built a quick diagnostic from the downloaded raw data. This is not an OI-SVMVAR estimate. It uses 16 Taiwan macro anchors and 5 available Taiwan financial anchors to construct two standardized first principal components, then checks whether external variables are more correlated with the macro proxy or financial proxy.

Common transformed sample: 2002M1-2025M11, 287 observations.

| External variable | Mean abs corr: macro | Mean abs corr: financial | Macro-dominant share, 36m rolling | Latest dominant |
|---|---:|---:|---:|---|
| US IPI YoY | 0.473 | 0.202 | 0.845 | Macro |
| US credit spread | 0.531 | 0.357 | 0.802 | Macro |
| Global GPR | 0.203 | 0.122 | 0.798 | Macro |
| US TPU | 0.249 | 0.172 | 0.651 | Macro |
| China CPI YoY | 0.313 | 0.230 | 0.536 | Macro |
| Global EPU | 0.300 | 0.311 | 0.504 | Macro/latest near tied |
| US FFR change | 0.237 | 0.262 | 0.472 | Macro/latest |
| US EPU | 0.231 | 0.276 | 0.429 | Macro/latest |
| VIX | 0.368 | 0.566 | 0.258 | Financial |

Event-window dominance switches across episodes, which is exactly the kind of pattern the formal OI-SVMVAR is designed to estimate. Examples: VIX is financial in 2018-2019 and 2022-2023, while GPR flips across windows. The caveat is important: the financial anchor is currently weak because TWSE foreign flows, margin, and short-selling variables are missing.

### 5. Recent Simulated BCA Work Is Promising But Not Yet a Safe Core Claim

The April 2026 FVGQ simulated-BCA work shows useful methodological instincts:

- LP estimates of wedge responses are unstable and sensitive to controls.
- GIRF mean signatures are more appropriate for nonlinear uncertainty shocks.
- BCA/wedge comparisons can help distinguish mechanisms beyond raw IRF fit.

But the current result set is still preliminary and partly superseded by later implementation changes. It should be framed as a model-diagnostic extension, not as an already established "new stochastic BCA framework."

## Research Questions

### RQ1: When do U.S., China, and global uncertainty sources transmit through Taiwan's macro versus financial channel?

**Type:** Descriptive / mechanism  
**Hypothesis:** VIX and U.S. credit conditions should load more often on the financial factor, while U.S. and China real-activity variables should load more often on the macro factor; trade-policy and geopolitical variables should switch across regimes.  
**Strategy:** OI-SVMVAR time-varying classification probabilities \(\pi_{i,t}\).  
**Priority:** Highest.

### RQ2: Which external source contributes most to Taiwan's domestic uncertainty factors?

**Type:** Quantification  
**Hypothesis:** U.S. financial variables explain more of \(h_{f,t}\), while China real-activity variables explain more of \(h_{m,t}\), with trade-policy uncertainty becoming important after 2018.  
**Strategy:** FEVD on posterior draws.  
**Priority:** Highest.

### RQ3: What are the real economic consequences of channel-specific external uncertainty?

**Type:** Mechanism / policy  
**Hypothesis:** Financial-channel shocks should move TAIEX volatility, exchange-rate volatility, and rates before real activity; macro-channel shocks should hit exports, IPI, employment, and wages more directly.  
**Strategy:** Generalized IRFs and event-window posterior summaries.  
**Priority:** High.

### RQ4: Which structural mechanism can reproduce the empirical channel signature?

**Type:** Structural validation  
**Hypothesis:** If empirical IRFs show labor/investment wedge deterioration, pure collateral constraints may be insufficient; working-capital or agency-cost mechanisms become more credible.  
**Strategy:** Conditional SOE DSGE model comparison, optionally using Simulated BCA as an additional diagnostic.  
**Priority:** Medium until Year 1 results exist.

## Recommendations

1. Freeze the Year 1 design first. Use "more than forty monthly variables" in proposal prose unless the exact table is fully final. In technical tables, choose either a core balanced specification or a full intended specification and make all files match.

2. Build the final dataset pipeline next. A `build_dataset.py` or equivalent should merge raw files, apply transformations, generate stationarity diagnostics, record missing values, and output a balanced panel plus metadata.

3. Strengthen the financial anchor block before interpreting \(h_{f,t}\). TWSE foreign net buying, margin buying, short selling, and a better turnover series should be treated as priority data tasks. Without them, the financial factor may be too equity-volatility/rate-heavy.

4. Handle China variables pragmatically. Do not let China M2 ending in 2013 or China IPI/PPI acquisition block the entire project. Define a core model using currently reliable external variables, then add China IPI/PPI/M2 as an extended robustness specification when acquired.

5. Keep Simulated BCA as a Year 2 diagnostic, not the headline contribution. The immediate proposal should emphasize conditional competing hypotheses. The wedge-comparison idea can be a stronger second paper or an extension if Year 1 produces clean empirical wedge targets.

6. Update stale management files. `project_management/CURRENT_STATUS.md`, `ACTIVE_TASKS.md`, and `data/README.md` lag behind the actual 2026 data work and will mislead future AI sessions.

## Suggested Next Steps

1. Harmonize `CM03_production_spec.md`, `PROGRESS.md`, `y1_sec2_methods.tex`, `y2_sec2_methods.tex`, `README.md`, and `docs/variable_planning.md` around one empirical specification.
2. Implement `build_dataset.py` and produce a first balanced preliminary panel.
3. Add a data-readiness table: target variable, current raw file, transformation, coverage, missing count, classification block, and final inclusion decision.
4. Decide whether the grant version should say "core 43/45-variable model plus extended 47-variable robustness" rather than trying to force every planned variable into the baseline.

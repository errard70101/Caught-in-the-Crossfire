# Research Direction Clarification and Project Milestones

**Date**: 2025-11-14
**Purpose**: Define core research direction and establish comprehensive project tracking system
**Status**: Active project management document

---

## 📌 Core Research Direction (Finalized)

### Research Title

**English**: "Caught in the Crossfire: Time-Varying Transmission of U.S.-China Uncertainty to Taiwan"

**中文**: 困在美中交火之間：不確定性衝擊對台灣之時變傳導機制研究

### One-Sentence Research Question

**"Do external uncertainty shocks from the U.S. and China transmit to Taiwan primarily through macroeconomic channels or financial channels? And how does this transmission mechanism change over time?"**

---

## 🎯 Core Innovation: What Makes This NOT Country Replication

### DHK (2025) Asked:
"In the U.S. economy, which type of uncertainty (macroeconomic vs. financial) has a greater impact on real activity?"

### We Ask:
"For external shocks hitting Taiwan, which transmission channel (macroeconomic vs. financial) do they primarily use? And how does this channel evolve over time?"

### Key Methodological Insight:
- **DHK's "unclassified variables"** were domestic ambiguous variables (S&P 500, Fed Funds, exchange rate)
- **Our "unclassified variables"** are ALL external shock sources (US variables, China variables, global indicators)
- This allows the model to **objectively identify transmission channels** rather than researcher-imposed classifications

---

## 🔬 Methodological Framework Summary

### Model Specification (Maintained from DHK 2025)
- **Two latent factors**: h_t = (h_macro,t, h_financial,t)'
- These represent **Taiwan's domestic** macroeconomic and financial uncertainty
- **40+ variables** in monthly frequency

### Variable Classification Strategy

#### Taiwan Domestic - Clearly Macro (~19 variables):
- Industrial production, manufacturing, export orders
- CPI, core CPI, WPI, import/export prices
- Unemployment, employment, wages

#### Taiwan Domestic - Clearly Financial (~10 variables):
- TAIEX returns, volatility, trading volume
- Interest rates, term spread, credit spreads
- Foreign investment flows, margin trading

#### **UNCLASSIFIED (External Shocks)** (~14 variables) - **THIS IS THE KEY INNOVATION**:
- **US**: Federal Funds Rate, IPI, credit spread (BAA-AAA), EPU index
- **China**: Industrial production, PPI, total social financing (TSF)
- **Global**: VIX, global EPU, geopolitical risk (GPR)
- **US-China relations**: Trade policy uncertainty index, bilateral relation indicators
- **Policy variables**: Taiwan CBC rediscount rate, M1b, M2 (these bridge domestic and external)

### Three-Step Analysis Plan

**Step 1: Identify Transmission Channels**
- Tool: Time-varying classification probabilities π_{i,t}
- Plot: Time series of each external variable's probability of being "macro" vs. "financial"
- Output: Regime identification (when did US FFR transmit through financial vs. macro channel?)

**Step 2: Quantify Shock Sources**
- Tool: Forecast Error Variance Decomposition (FEVD)
- Calculation: % of variance in Taiwan's h_macro,t explained by each external variable
- Calculation: % of variance in Taiwan's h_financial,t explained by each external variable
- Output: Ranking of external shock importance

**Step 3: Analyze Economic Consequences**
- Tool: Impulse Response Functions (IRF)
- IRF Set 1: Taiwan variables → h_macro,t shock and h_financial,t shock
- IRF Set 2: Taiwan variables → identified external variable shocks (order-invariant)
- Output: Real economy impacts through different channels

---

## 🚫 Critical "Do NOT" List (From 11-08 Discussion)

### DO NOT Extend the Model:
❌ **NO third uncertainty factor** (e.g., h_global,t) - requires rewriting entire MCMC algorithm
❌ **NO fourth factor** (e.g., h_domestic_m, h_domestic_f, h_global_m, h_global_f) - computational impossibility
✅ **MAINTAIN** 2-factor structure: h_t = (h_macro,t, h_financial,t)' representing Taiwan's domestic uncertainty

### DO NOT Impose Block Exogeneity:
❌ **NO zero restrictions** (traditional SOE assumption: domestic → global = 0)
❌ **NO Cholesky decomposition** with forced variable ordering
✅ **USE** DHK's order-invariant approach; **VERIFY** SOE assumption post-estimation via FEVD

### DO NOT Misframe the Research Question:
❌ **WRONG**: "Which uncertainty (macro vs. financial) dominates in Taiwan?" (that's DHK's US question)
❌ **WRONG**: "How much do US-China shocks affect Taiwan?" (magnitude question, not channel question)
✅ **CORRECT**: "Which transmission channel do external shocks use to hit Taiwan?"

---

## 📊 Comprehensive TODO List and Milestones

### PHASE 0: Literature Review and Research Design ✅ COMPLETED

#### Milestone 0.1: Global Literature Review ✅
- [x] Core uncertainty shock literature (40+ papers)
- [x] Small open economy transmission literature
- [x] Macro vs. financial uncertainty decomposition literature
- [x] Order-invariant VAR methodology papers
- **Output**: `literature/uncertainty_shock_literature.md`

#### Milestone 0.2: Taiwan-Specific Literature ✅
- [x] Taiwan uncertainty studies (Sin 2015, Huang et al. 2019)
- [x] US-China trade war impact on Taiwan
- [x] Geopolitical risk and Taiwan financial markets
- [x] Recent event studies (Pelosi 2022, TAIEX crash 2025)
- **Output**: `literature/taiwan_specific_uncertainty_literature.md`

#### Milestone 0.3: Research Direction Finalization ✅
- [x] Core research question defined: "Which transmission channel?"
- [x] Methodological framework confirmed: Apply DHK (2025), no extensions
- [x] Variable classification strategy determined
- [x] Three-step analysis plan established
- **Output**: This document + updated README.md + CLAUDE.md

---

### PHASE 1: Data Collection 🔄 CURRENT PHASE

**Timeline**: Months 1-3 (December 2025 - February 2026)
**Estimated Workload**: 120-150 hours

#### Milestone 1.1: Taiwan Macroeconomic Variables (Target: ~19 variables)
- [ ] **1.1.1**: Download IPI, Manufacturing Production, Export Orders (source: DGBAS)
- [ ] **1.1.2**: Download Retail Sales, Food Service Sales (source: DGBAS)
- [ ] **1.1.3**: Download Exports, Imports in real USD terms (source: Ministry of Finance)
- [ ] **1.1.4**: Download PMI (M-Score), NMI (source: CIER)
- [ ] **1.1.5**: Download Business Cycle Signal Score (景氣對策信號) (source: NDC)
- [ ] **1.1.6**: Download CPI, Core CPI, WPI (source: DGBAS)
- [ ] **1.1.7**: Download Import/Export Price Indices (source: DGBAS)
- [ ] **1.1.8**: Download Unemployment Rate, Employment (seasonally adjusted) (source: DGBAS)
- [ ] **1.1.9**: Download Manufacturing Wages (real, YoY growth) (source: DGBAS)
- [ ] **1.1.10**: Verify all series cover 1990-2025 (or longest available)
- [ ] **1.1.11**: Apply transformations: YoY growth rates, seasonal adjustment (X-13-ARIMA)
- [ ] **1.1.12**: Conduct stationarity tests (ADF, PP tests)

**Deliverable**: `data/taiwan_macro_raw.csv` + `data/taiwan_macro_cleaned.csv` + transformation documentation

#### Milestone 1.2: Taiwan Financial Variables (Target: ~10 variables)
- [ ] **1.2.1**: Download overnight call rate, 10Y govt bond yield (source: CBC)
- [ ] **1.2.2**: Calculate term spread (10Y - overnight)
- [ ] **1.2.3**: Download TAIEX daily data (source: TWSE)
- [ ] **1.2.4**: Calculate TAIEX monthly return, volatility, average trading volume
- [ ] **1.2.5**: Download foreign investor net buy/sell data (source: TWSE)
- [ ] **1.2.6**: Download margin trading balance, short selling balance (source: TWSE)
- [ ] **1.2.7**: Download VIX (US, as global risk proxy) (source: CBOE via FRED)
- [ ] **1.2.8**: Apply transformations and stationarity tests

**Deliverable**: `data/taiwan_financial_raw.csv` + `data/taiwan_financial_cleaned.csv`

#### Milestone 1.3: Unclassified - Policy and Credit Variables (Target: ~8 variables)
- [ ] **1.3.1**: Download CBC rediscount rate (policy rate) (source: CBC)
- [ ] **1.3.2**: Download M1b, M2 growth rates (source: CBC)
- [ ] **1.3.3**: Download total bank loans and investments, consumer loans (source: CBC)
- [ ] **1.3.4**: Download TAIEX level (index value, not return)
- [ ] **1.3.5**: Calculate or obtain credit spread (5Y A-rated corporate - 5Y govt bond)
- [ ] **1.3.6**: Download housing price index (Cathay/Sinyi, interpolate to monthly if needed)
- [ ] **1.3.7**: Download TWD/USD spot rate, calculate monthly volatility (source: CBC)
- [ ] **1.3.8**: Download Real Effective Exchange Rate (REER) index (source: BIS or CBC)

**Deliverable**: `data/taiwan_unclassified_domestic.csv`

#### Milestone 1.4: Unclassified - US Variables (Target: ~4 variables)
- [ ] **1.4.1**: Download US Federal Funds Rate (source: FRED series FEDFUNDS)
- [ ] **1.4.2**: Download US Industrial Production Index (source: FRED series INDPRO)
- [ ] **1.4.3**: Download US BAA-AAA credit spread (source: FRED)
- [ ] **1.4.4**: Download US EPU index or macro uncertainty index (source: PolicyUncertainty.com or Ludvigson website)
- [ ] **1.4.5**: Apply transformations (e.g., IPI to YoY growth)

**Deliverable**: `data/us_variables.csv`

#### Milestone 1.5: Unclassified - China Variables (Target: ~3 variables)
- [ ] **1.5.1**: Download China Industrial Production (Value Added) YoY growth (source: NBS China or FRED series CHNGDPYY)
- [ ] **1.5.2**: Download China Producer Price Index (PPI) YoY growth (source: NBS China or CEIC)
- [ ] **1.5.3**: Download China Total Social Financing (TSF) stock YoY growth (source: PBOC or CEIC)
- [ ] **1.5.4**: Handle missing data issues (China data may have gaps pre-2000)

**Deliverable**: `data/china_variables.csv`

#### Milestone 1.6: Unclassified - Global and US-China Relations (Target: ~3 variables)
- [ ] **1.6.1**: Download VIX index (if not already in financial section) (source: FRED series VIXCLS)
- [ ] **1.6.2**: Download Geopolitical Risk (GPR) index (source: matteoiacoviello.com/gpr.htm)
- [ ] **1.6.3**: Download or construct US-China trade policy uncertainty index
  - Option A: Use Baker-Bloom-Davis US-China trade policy uncertainty
  - Option B: Construct text-based index from news sources
- [ ] **1.6.4**: Download Global EPU index (source: PolicyUncertainty.com)

**Deliverable**: `data/global_uscn_variables.csv`

#### Milestone 1.7: Data Integration and Final Dataset Construction
- [ ] **1.7.1**: Merge all datasets by date (monthly frequency)
- [ ] **1.7.2**: Handle missing values:
  - Check start/end dates for each series
  - Decide on common sample period (likely 1995-2025 or 2000-2025)
  - Document any interpolation or imputation methods
- [ ] **1.7.3**: Standardize all variables (mean 0, variance 1)
- [ ] **1.7.4**: Create data dictionary with variable definitions, sources, transformations
- [ ] **1.7.5**: Generate descriptive statistics table
- [ ] **1.7.6**: Create correlation matrix heatmap
- [ ] **1.7.7**: Final dataset validation and quality checks

**Deliverable**:
- `data/final_dataset.csv` (40+ variables, ~300-360 monthly observations)
- `data/data_dictionary.xlsx`
- `data/descriptive_statistics.tex`
- `figures/correlation_heatmap.pdf`

---

### PHASE 2: Model Implementation 📅 PLANNED

**Timeline**: Months 4-6 (March 2025 - May 2026)
**Estimated Workload**: 150-200 hours

#### Milestone 2.1: Obtain and Study DHK (2025) Code
- [ ] **2.1.1**: Contact DHK authors for replication code
  - Email: Request MATLAB/R/Python code from Journal of Business & Economic Statistics
  - Alternative: Check journal supplementary materials webpage
- [ ] **2.1.2**: Study the MCMC algorithm implementation
  - Understand parameter transformation (Equation 14 in paper)
  - Understand time-varying classification Markov chain
  - Understand prior specifications (Minnesota priors on VAR coefficients)
- [ ] **2.1.3**: Run original code with DHK's US dataset to verify replication
- [ ] **2.1.4**: Document code structure and key functions

**Deliverable**: `code/DHK_original/` directory + `docs/DHK_code_documentation.md`

#### Milestone 2.2: Adapt Code for Taiwan Dataset
- [ ] **2.2.1**: Modify data loading functions to read Taiwan dataset
- [ ] **2.2.2**: Update variable classification arrays:
  - Set Taiwan domestic macro variables as "macro"
  - Set Taiwan domestic financial variables as "financial"
  - **Set all external variables as "unclassified"**
- [ ] **2.2.3**: Adjust prior hyperparameters (if needed for Taiwan-specific characteristics)
- [ ] **2.2.4**: Set MCMC parameters:
  - Total iterations: 50,000
  - Burn-in: 25,000
  - Thinning: every 5th draw → 5,000 posterior draws
- [ ] **2.2.5**: Test run with small dataset (10 variables, 100 observations) to verify code works

**Deliverable**: `code/taiwan_OI_SVMVAR/` directory

#### Milestone 2.3: Production Estimation Runs
- [ ] **2.3.1**: Secure high-performance computing resources
  - Option A: University HPC cluster
  - Option B: Cloud computing (AWS, Google Cloud)
  - Estimate: Need ~30 hours per run × 3-5 runs = 90-150 compute hours
- [ ] **2.3.2**: **Run 1**: Small model (30 variables) for comparison
  - Select 30 most important variables
  - Estimate OI-SVMVAR
  - Save posterior draws
- [ ] **2.3.3**: **Run 2**: Large model (43 variables) - **Main specification**
  - Full variable set
  - Estimate OI-SVMVAR
  - Save posterior draws
- [ ] **2.3.4**: **Run 3**: Robustness - alternative sample period (e.g., exclude COVID-19)
- [ ] **2.3.5**: **Run 4**: Robustness - alternative variable transformations
- [ ] **2.3.6**: Convergence diagnostics:
  - Trace plots for key parameters
  - Geweke test, Heidelberger-Welch test
  - Effective sample size calculation

**Deliverable**:
- `results/mcmc_output_small.mat`
- `results/mcmc_output_large_main.mat`
- `results/mcmc_output_robust1.mat`
- `results/mcmc_output_robust2.mat`
- `results/convergence_diagnostics.pdf`

---

### PHASE 3: Analysis (Three-Step Research Design) 📅 PLANNED

**Timeline**: Months 7-10 (June 2025 - September 2026)
**Estimated Workload**: 180-220 hours

#### Milestone 3.1: Step 1 - Identify Transmission Channels (Time-Varying Classification)
- [ ] **3.1.1**: Extract time-varying classification probabilities π_{i,t} for all unclassified variables
- [ ] **3.1.2**: Create time-series plots:
  - Plot 1: US Federal Funds Rate classification over time
  - Plot 2: US IPI classification over time
  - Plot 3: China IPI classification over time
  - Plot 4: VIX classification over time
  - Plot 5: US-China relations index classification over time
  - Plot 6: All external variables in one multi-panel figure
- [ ] **3.1.3**: Identify regime shifts:
  - Mark 2008 financial crisis
  - Mark 2012 Xi Jinping era / Taiwan firm profit decline
  - Mark 2018 US-China trade war
  - Mark 2020 COVID-19 pandemic
  - Mark 2022 Pelosi visit
- [ ] **3.1.4**: Statistical tests for structural breaks in classification probabilities
- [ ] **3.1.5**: Write interpretation:
  - Which external shocks transmitted through macro vs. financial channels?
  - When did transmission mechanisms shift?
  - Do findings support hypotheses?

**Deliverable**:
- `figures/classification_timeseries/` directory with all plots
- `tables/regime_shift_dates.tex`
- `results/step1_interpretation.md`

#### Milestone 3.2: Step 2 - Quantify Shock Sources (FEVD)
- [ ] **3.2.1**: Compute Forecast Error Variance Decomposition at horizons h = 1, 6, 12, 24 months
- [ ] **3.2.2**: For Taiwan h_macro,t:
  - Calculate % explained by each US variable
  - Calculate % explained by each China variable
  - Calculate % explained by global/US-China variables
  - Calculate % explained by Taiwan domestic variables
- [ ] **3.2.3**: For Taiwan h_financial,t:
  - Repeat FEVD calculations as in 3.2.2
- [ ] **3.2.4**: Create FEVD decomposition tables:
  - Table 1: Contributions to h_macro,t (all horizons)
  - Table 2: Contributions to h_financial,t (all horizons)
- [ ] **3.2.5**: Create stacked bar charts showing decomposition at h=12 months
- [ ] **3.2.6**: **Verify SOE assumption**:
  - Check if Taiwan domestic shocks explain <5% of US/China/global variable variance
  - Document results
- [ ] **3.2.7**: Rank external shock sources by importance

**Deliverable**:
- `tables/fevd_macro_uncertainty.tex`
- `tables/fevd_financial_uncertainty.tex`
- `figures/fevd_decomposition_h12.pdf`
- `results/soe_assumption_verification.md`
- `results/shock_source_ranking.md`

#### Milestone 3.3: Step 3 - Analyze Economic Consequences (IRF)
- [ ] **3.3.1**: Compute Impulse Response Functions with 68% and 90% credible intervals
- [ ] **3.3.2**: **IRF Set 1**: Taiwan variables → uncertainty shocks
  - IRF 1.1: Taiwan IPI, employment, CPI → h_macro,t shock
  - IRF 1.2: Taiwan IPI, employment, CPI → h_financial,t shock
  - IRF 1.3: TAIEX, TWD/USD, credit spread → h_macro,t shock
  - IRF 1.4: TAIEX, TWD/USD, credit spread → h_financial,t shock
  - **Compare with DHK (2025) US results**
- [ ] **3.3.3**: **IRF Set 2**: Taiwan variables → external variable shocks (order-invariant identification)
  - IRF 2.1: Taiwan variables → US FFR shock
  - IRF 2.2: Taiwan variables → US-China relations index shock
  - IRF 2.3: Taiwan variables → China IPI shock
  - IRF 2.4: Taiwan variables → VIX shock
- [ ] **3.3.4**: Create multi-panel IRF figures
- [ ] **3.3.5**: Conduct hypothesis tests:
  - Are h_macro,t and h_financial,t shocks significantly different in their impacts?
  - Do external shocks have asymmetric effects?
- [ ] **3.3.6**: Historical decomposition:
  - Decompose Taiwan IPI variance into contributions from each shock over time
  - Identify which shocks drove major recessions (2008, 2020)

**Deliverable**:
- `figures/irf_uncertainty_shocks/` directory
- `figures/irf_external_shocks/` directory
- `figures/historical_decomposition.pdf`
- `tables/irf_summary_statistics.tex`
- `results/step3_interpretation.md`

#### Milestone 3.4: Robustness Checks and Model Comparison
- [ ] **3.4.1**: Compare small model (30 var) vs. large model (43 var) results:
  - Do conclusions about transmission channels differ?
  - Do FEVD rankings change?
  - **Demonstrate importance of large model**
- [ ] **3.4.2**: Alternative sample period robustness:
  - Exclude COVID-19 period (2020-2021) and re-estimate
  - Pre-2018 vs. post-2018 subsample comparison
- [ ] **3.4.3**: Alternative prior specifications:
  - Tighter vs. looser Minnesota prior hyperparameters
  - Sensitivity analysis
- [ ] **3.4.4**: Compare with traditional Cholesky identification:
  - Estimate model with Cholesky decomposition
  - Show results depend on variable ordering
  - **Demonstrate value of order-invariance**

**Deliverable**:
- `tables/small_vs_large_model_comparison.tex`
- `tables/robustness_checks_summary.tex`
- `results/robustness_interpretation.md`

---

### PHASE 4: Policy Implications and Interpretation 📅 PLANNED

**Timeline**: Months 11-14 (October 2025 - January 2027)
**Estimated Workload**: 80-100 hours

#### Milestone 4.1: Synthesize Main Findings
- [ ] **4.1.1**: Main Finding 1: Which transmission channel dominates?
  - Summary of time-varying classification results
  - Summary of FEVD importance rankings
- [ ] **4.1.2**: Main Finding 2: Time-varying nature of transmission
  - Document regime shifts (2008→2012→2018→2020→2022)
  - Explain economic drivers of shifts
- [ ] **4.1.3**: Main Finding 3: Comparison with DHK (2025) US results
  - How do Taiwan results differ from US?
  - What does this tell us about small open economies?

**Deliverable**: `results/main_findings_summary.md`

#### Milestone 4.2: Policy Implications for Central Bank of China (Taiwan)
- [ ] **4.2.1**: Policy Implication 1: Which channel to monitor
  - If financial channel dominates → focus on financial stability tools
  - If macro channel dominates → focus on aggregate demand management
- [ ] **4.2.2**: Policy Implication 2: Early warning indicators
  - Which external variables provide most reliable signals?
  - Construct real-time monitoring dashboard concept
- [ ] **4.2.3**: Policy Implication 3: Exchange rate management
  - Does TWD/USD flexibility help or hurt under different external shocks?
  - Recommendations for CBC foreign exchange intervention strategy
- [ ] **4.2.4**: Policy Implication 4: Monetary policy response
  - Should CBC follow Fed rate hikes? (depends on transmission channel)
  - Different responses needed for US vs. China shocks

**Deliverable**: `results/cbc_policy_implications.md`

#### Milestone 4.3: Broader Research Implications
- [ ] **4.3.1**: Methodological contribution:
  - First application of "unclassified variables" for transmission channel identification
  - Demonstration that DHK framework generalizes to SOE context
- [ ] **4.3.2**: Empirical contribution:
  - New evidence on dual US-China exposure
  - Documentation of time-varying transmission mechanisms
- [ ] **4.3.3**: Comparison with existing Taiwan studies:
  - How do our findings compare with Sin (2015)?
  - What did small-model studies miss?

**Deliverable**: `results/research_contributions.md`

---

### PHASE 5: Writing and Dissemination 📅 PLANNED

**Timeline**: Months 15-18 (February 2027 - May 2027)
**Estimated Workload**: 200-250 hours

#### Milestone 5.1: Research Paper Writing
- [ ] **5.1.1**: Introduction (10-12 pages)
  - Motivation: Taiwan's unique position
  - Research question and contribution
  - Preview of main findings
  - Related literature (brief overview, detailed in next section)
- [ ] **5.1.2**: Literature Review (8-10 pages)
  - **Section 2.1**: Uncertainty measurement and identification
  - **Section 2.2**: Small open economy and external shock transmission
  - **Section 2.3**: Macro vs. financial uncertainty decomposition
  - **Section 2.4**: Order-invariant VAR methods
  - **Section 2.5**: Taiwan context and research gaps
- [ ] **5.1.3**: Methodology (12-15 pages)
  - **Section 3.1**: OI-SVMVAR framework (based on DHK 2025)
  - **Section 3.2**: Variable classification strategy (**emphasize unclassified external variables**)
  - **Section 3.3**: Identification and estimation
  - **Section 3.4**: Three-step analysis plan
- [ ] **5.1.4**: Data (6-8 pages)
  - **Section 4.1**: Data sources and construction
  - **Section 4.2**: Descriptive statistics
  - **Section 4.3**: Preliminary analysis (correlations, unit root tests)
- [ ] **5.1.5**: Results (20-25 pages)
  - **Section 5.1**: Time-varying classification (Step 1 results + figures)
  - **Section 5.2**: FEVD analysis (Step 2 results + tables)
  - **Section 5.3**: IRF analysis (Step 3 results + figures)
  - **Section 5.4**: Robustness checks
  - **Section 5.5**: Comparison with small model and traditional methods
- [ ] **5.1.6**: Discussion and Policy Implications (8-10 pages)
  - **Section 6.1**: Interpretation of main findings
  - **Section 6.2**: Policy implications for CBC
  - **Section 6.3**: Comparison with DHK (2025) and implications for SOEs
  - **Section 6.4**: Limitations and future research
- [ ] **5.1.7**: Conclusion (3-4 pages)
- [ ] **5.1.8**: Appendices:
  - Appendix A: Data definitions and sources
  - Appendix B: Additional robustness checks
  - Appendix C: Supplementary figures and tables
- [ ] **5.1.9**: Full draft completion and internal review
- [ ] **5.1.10**: Revisions based on feedback

**Deliverable**: `paper/main_paper.pdf` (60-80 pages)

#### Milestone 5.2: Policy Brief for CBC
- [ ] **5.2.1**: Executive summary (1 page)
- [ ] **5.2.2**: Key findings in non-technical language (2-3 pages)
- [ ] **5.2.3**: Policy recommendations (2-3 pages):
  - Which indicators to monitor
  - How to respond to different external shocks
  - Exchange rate management guidance
- [ ] **5.2.4**: Visual dashboard mockup (1-2 pages)
- [ ] **5.2.5**: Translation to Traditional Chinese
- [ ] **5.2.6**: Submission to CBC Research Department

**Deliverable**:
- `policy_brief/CBC_policy_brief_EN.pdf`
- `policy_brief/CBC_policy_brief_ZH.pdf`

#### Milestone 5.3: Conference Presentations
- [ ] **5.3.1**: Prepare 45-minute seminar presentation
- [ ] **5.3.2**: Prepare 15-minute conference presentation
- [ ] **5.3.3**: Target conferences:
  - Asian Meeting of Econometric Society (AMES)
  - Taipei International Conference on Growth, Trade and Dynamics (TIGCTD)
  - Western Economic Association International (WEAI)
  - International Association for Applied Econometrics (IAAE)
  - Royal Economic Society (RES) Annual Conference
- [ ] **5.3.4**: Submit to 3-4 conferences

**Deliverable**: `presentations/` directory

#### Milestone 5.4: Journal Submission
- [ ] **5.4.1**: Target journal selection:
  - **Tier 1 targets**: Journal of Applied Econometrics, Journal of International Economics
  - **Tier 2 targets**: Journal of Economic Dynamics and Control, Economic Modelling
  - **Regional targets**: Pacific Economic Review, Asian Economic Journal
- [ ] **5.4.2**: Format paper according to journal requirements
- [ ] **5.4.3**: Write cover letter emphasizing:
  - Novel application of "unclassified variables" for transmission channel identification
  - Policy relevance for small open economies
  - Validation of DHK (2025) in new context
- [ ] **5.4.4**: Initial submission to top choice journal
- [ ] **5.4.5**: Respond to referee reports and revise
- [ ] **5.4.6**: Resubmission cycle

**Deliverable**: Accepted journal publication

---

## 📈 Progress Tracking Dashboard

### Overall Project Status: **15% Complete**

| Phase | Status | Completion % | Start Date | End Date (Target) |
|-------|--------|--------------|------------|-------------------|
| Phase 0: Literature & Design | ✅ Complete | 100% | Nov 2025 | Nov 14, 2025 |
| Phase 1: Data Collection | 🔄 In Progress | 0% | Nov 2025 | Feb 2026 |
| Phase 2: Model Implementation | ⏳ Planned | 0% | Mar 2026 | May 2026 |
| Phase 3: Analysis | ⏳ Planned | 0% | Jun 2026 | Sep 2026 |
| Phase 4: Policy Implications | ⏳ Planned | 0% | Oct 2026 | Jan 2027 |
| Phase 5: Writing & Dissemination | ⏳ Planned | 0% | Feb 2027 | May 2027 |

### Next Immediate Actions (Priority Order)

1. **Milestone 1.1**: Download Taiwan macroeconomic variables from DGBAS
2. **Milestone 1.2**: Download Taiwan financial variables from TWSE and CBC
3. **Milestone 1.4**: Download US variables from FRED (easiest, do first for practice)
4. **Milestone 2.1**: Contact DHK authors for replication code
5. **Milestone 5.1**: Begin drafting Introduction section (can start in parallel)

---

## 🎓 Expected Timeline Summary

- **Total Duration**: 18 months (November 2025 - May 2027)
- **Data Collection**: 3 months
- **Model Implementation**: 3 months
- **Analysis**: 4 months
- **Policy Implications**: 4 months
- **Writing & Submission**: 4 months

---

## 📚 Key Deliverables Checklist

### Data
- [ ] Final cleaned dataset (40+ variables, ~300-360 months)
- [ ] Data dictionary and descriptive statistics
- [ ] Correlation matrices and preliminary analysis

### Code
- [ ] Adapted OI-SVMVAR estimation code
- [ ] Analysis scripts (classification, FEVD, IRF)
- [ ] Visualization scripts
- [ ] Replication package

### Results
- [ ] Time-varying classification plots for all external variables
- [ ] FEVD decomposition tables
- [ ] IRF figures (uncertainty shocks + external shocks)
- [ ] Robustness check tables

### Writing
- [ ] Main research paper (60-80 pages)
- [ ] Policy brief for CBC (English + Chinese)
- [ ] Conference presentations (slides)
- [ ] Journal submission ready manuscript

---

## 🚀 Success Metrics

### Academic Impact
- [ ] Acceptance at top-tier journal (Journal of Applied Econometrics or equivalent)
- [ ] 3+ conference presentations at international meetings
- [ ] Citations from subsequent small open economy uncertainty studies

### Policy Impact
- [ ] CBC acknowledges and uses findings in policy reports
- [ ] Media coverage in Taiwan economic news
- [ ] Referenced in government policy documents

### Methodological Impact
- [ ] Demonstrates value of "unclassified variables" for transmission channel identification
- [ ] Provides template for other SOE uncertainty studies
- [ ] Validates DHK (2025) framework generalizability

---

*Last Updated: 2025-11-14*
*Next Review: Upon completion of Phase 1 (Data Collection)*

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Title**: "Caught in the Crossfire: Time-Varying Transmission of U.S.-China Uncertainty to Taiwan"

**Research Objective**: Apply order-invariant stochastic volatility in mean vector autoregressions (OI-SVMVAR) to identify **time-varying transmission channels** through which external uncertainty shocks from the United States and China impact Taiwan's economy—distinguishing between **macroeconomic channels** (real economy) and **financial channels** (financial markets).

**Methodological Foundation**: Based on Davidson, Hou, and Koop (2025) "Investigating Economic Uncertainty Using Stochastic Volatility in Mean VARs: The Importance of Model Size, Order-Invariance and Classification"

**Core Innovation**: Exploiting DHK (2025)'s "unclassified variables" feature to identify transmission channels of external shocks—a novel application beyond the original paper's focus on domestic uncertainty decomposition.

**Primary Language**: Traditional Chinese (繁體中文) for discussions and documentation, though code and technical content may be in English.

## Research Context

### Core Research Question

**"Do external uncertainty shocks from the U.S. and China transmit to Taiwan primarily through macroeconomic channels or financial channels? And how does this transmission mechanism change over time?"**

This question is fundamentally different from DHK (2025)'s question of "which uncertainty type (macro vs. financial) dominates in the U.S."

### Key Methodological Features

1. **Large-Scale Model**: Requires 40+ variables to avoid omitted variable bias (small models with ~30 variables produce biased results)

2. **Order-Invariance**: Solves the variable ordering problem inherent in traditional large VAR models (results do not depend on arbitrary variable ordering)

3. **Time-Varying Classification**: Variables can be classified as:
   - **Macroeconomic variables** (總體經濟變數): Clearly real economy indicators (Taiwan IPI, employment, CPI, exports, etc.)
   - **Financial variables** (金融變數): Clearly financial market indicators (TAIEX returns/volatility, credit spreads, etc.)
   - **Unclassified variables** (未分類變數): **[KEY INNOVATION]** All external shock sources placed here:
     - US variables: FFR, IPI, credit spread, EPU
     - China variables: IPI, PPI, total social financing
     - Global indicators: VIX, GPR, global EPU
     - US-China relations: Trade policy uncertainty, geopolitical risk indices

4. **Two Latent Uncertainty Factors** (maintained from DHK):
   - h_t = (h_macro,t, h_financial,t)'
   - These represent **Taiwan's domestic** macro and financial uncertainty
   - External variables' classification reveals their **transmission channel** to Taiwan

### Three-Step Research Design

**Step 1: Identify Transmission Channels**
- Tool: Time-varying classification probabilities
- Output: Time-series plots showing when external variables are classified as "macro" vs. "financial"
- Question: When did US monetary policy affect Taiwan through financial vs. macro channels?

**Step 2: Quantify Shock Sources**
- Tool: Forecast Error Variance Decomposition (FEVD)
- Output: % of Taiwan's h_macro,t and h_financial,t explained by each external variable
- Question: Which external shock (US, China, US-China relations) contributes most?

**Step 3: Analyze Economic Consequences**
- Tool: Impulse Response Functions (IRF)
- Output: Dynamic responses of Taiwan's economy to external shocks
- Question: What are the real economic impacts through different channels?

### Critical Methodological Decisions (from 11-08 Discussion)

**Decision 1: Do NOT extend the model**
- Maintain DHK (2025)'s 2-factor structure: h_t = (h_macro,t, h_financial,t)'
- Do NOT add a third "global uncertainty" factor (would require rewriting entire MCMC algorithm)
- Use "unclassified variables" approach instead (fully within DHK framework)

**Decision 2: Do NOT impose block exogeneity restrictions**
- Traditional SOE models impose zero restrictions (domestic variables cannot affect global variables)
- DHK (2025)'s innovation is to AVOID such restrictions (they cause order-dependence problems)
- Use DHK's order-invariant approach; verify SOE assumption post-estimation via FEVD

**Decision 3: Focus on transmission channels, not impact magnitude**
- DHK (2025) asked: "Which uncertainty (macro vs. financial) dominates in the US?"
- We ask: "Which transmission channel (macro vs. financial) do external shocks use to hit Taiwan?"
- This is a fundamentally different—and more policy-relevant—question for small open economies

## Repository Structure

```
/
├── llm_logs/                    # Research discussion logs
│   ├── 2025-11-08_discussion.md # CRITICAL: Core methodological decisions
│   ├── 2025-11-14_research_direction_clarification.md # Research direction summary
│   └── discussion-template.md   # Template for logging new discussions
├── literature/                  # Literature review materials
│   ├── uncertainty_shock_literature.md        # Global uncertainty literature (40+ papers)
│   └── taiwan_specific_uncertainty_literature.md  # Taiwan-specific studies
├── references/                  # Reference papers
│   └── Investigating Economic Uncertain.pdf  # Davidson, Hou, Koop (2025)
├── CLAUDE.md                    # This file - guide for Claude Code instances
├── README.md                    # Project overview and documentation
└── research_proposal.tex        # Research proposal (LaTeX)
```

## Working with LLM Discussion Logs

### CRITICAL: Read 2025-11-08_discussion.md First

The `llm_logs/2025-11-08_discussion.md` file contains the **entire methodological decision-making process**. Key decisions include:

1. **Variable Classification Strategy**:
   - Taiwan domestic macro variables: IPI, employment, CPI, exports, wages
   - Taiwan domestic financial variables: TAIEX returns/volatility, interest rates, credit spreads
   - **Unclassified (external)**: US FFR, US IPI, China IPI, VIX, EPU, GPR, US-China relations

2. **Why Include US and China Variables**:
   - Taiwan is a small open economy—omitting external variables causes severe omitted variable bias
   - External shocks must be modeled explicitly to avoid misattributing them to Taiwan's domestic uncertainty

3. **Why NOT Extend the Model**:
   - Adding a third uncertainty factor requires rewriting DHK (2025)'s entire MCMC algorithm
   - Attempting to impose block exogeneity restrictions would violate DHK's order-invariance innovation
   - The "unclassified variables" approach fully solves the problem within the existing framework

4. **Research Contribution Positioning**:
   - This is NOT "country replication"
   - Novel application: Using "unclassified variables" to identify transmission channels
   - Methodological demonstration: DHK's framework can answer questions beyond domestic uncertainty decomposition

When adding new discussion logs:
- Use the template in `llm_logs/discussion-template.md`
- Include date, model used, and purpose
- Document key insights and action items

## Working with Literature Review

The `literature/` directory contains two comprehensive literature review files:

### 1. `uncertainty_shock_literature.md` (Global Literature)

Organized in 4 phases covering 40+ papers:

**Phase 1: Core Uncertainty Shock Literature**
- Foundational measurement papers (Baker-Bloom-Davis EPU, Jurado-Ludvigson-Ng)
- VAR-based identification (Carriero-Clark-Marcellino)
- Order-invariant methods (Chan-Koop-Yu 2024) directly supporting DHK (2025)

**Phase 2: Small Open Economy & Uncertainty Transmission**
- International spillover mechanisms and transmission channels
- Panel VAR studies including Taiwan
- Korea and Singapore as comparable cases
- **Key finding**: Global uncertainty delivers deeper, longer-lasting effects than domestic uncertainty for SOEs

**Phase 3: Decomposition of Uncertainty Types**
- Separating macro vs. financial uncertainty (Caldara et al., Brianti 2025)
- **Critical policy implication**: Macro uncertainty allows simultaneous output/inflation stabilization; financial shocks require trade-offs
- Macro uncertainty causes deflation; financial uncertainty doesn't

**Phase 4: Taiwan/Asia-Pacific Context**
- Taiwan-specific studies (Sin 2015, Huang et al. 2019)
- US-China trade war impacts on Taiwan
- Taiwan's "caught in crossfire" position

### 2. `taiwan_specific_uncertainty_literature.md` (Taiwan Studies)

Detailed review of Taiwan-specific empirical evidence:

- **Taiwan EPU indices**: Huang et al. (2019), World Uncertainty Index (1956-2025)
- **Sin (2015)**: SVAR with 6 variables (4 Taiwan + 2 China)—shows China EPU affects Taiwan but suffers from small-model bias
- **Recent events**: 2022 Pelosi visit (bond yield study), 2025 TAIEX crash (9.7% drop), TWD surge
- **Firm-level evidence**: Taiwan firms' profitability in China declined post-2012, accelerated post-2018 trade war
- **Data availability**: Long time series available from DGBAS, CBC, FRED

### Research Gaps Identified

1. **Methodological Gaps**:
   - No order-invariant SVMVAR applied to any small open economy
   - No large-scale (40+ variable) uncertainty model for Taiwan (Sin 2015 used only 6 variables)
   - Time-varying classification not explored for Taiwan variables

2. **Substantive Gaps**:
   - No macro vs. financial uncertainty **transmission channel** decomposition for Taiwan
   - Dual US-China exposure not quantitatively modeled with channel identification
   - Unknown whether TWD/USD, TAIEX behave as macro or financial variables across different regimes

3. **Policy Gaps**:
   - CBC lacks guidance on which transmission channel to monitor/respond to
   - Unknown whether exchange rate flexibility helps or hurts under external uncertainty

### Novel Contributions This Research Makes

1. **Methodological**: First application of "unclassified variables" to identify external shock transmission channels
2. **Empirical**: Data-driven identification of time-varying transmission mechanisms for dual US-China exposure
3. **Policy**: Clear guidance for CBC on which policy tools to use based on dominant transmission channel
4. **Validation**: Tests whether DHK (2025) findings generalize to small open economy context

## Expected Research Workflow

### Phase 0: Literature Review ✓ (Completed)
- [x] Systematic review of global uncertainty shock literature (40+ papers)
- [x] Taiwan-specific studies review (10+ papers)
- [x] Methodological foundations documented
- [x] Research gaps identified and contributions positioned

### Phase 1: Research Design ✓ (Completed - 2025-11-14)
- [x] Core research question finalized: "Which transmission channel?"
- [x] Methodological framework confirmed: Apply DHK (2025), no extensions
- [x] Three-step analysis plan established
- [x] Variable classification strategy determined

### Phase 2: Data Collection (Current Phase)
- [ ] Assemble Taiwan macro variables (IPI, CPI, employment, exports, wages, etc.) - 1990-2025, monthly
- [ ] Assemble Taiwan financial variables (TAIEX, interest rates, credit spreads, foreign investment, etc.)
- [ ] Obtain US variables from FRED (FFR, IPI, BAA-AAA spread, EPU)
- [ ] Obtain China variables (IPI, PPI, TSF)
- [ ] Construct/obtain global indicators (VIX, GPR, US-China relations indices)
- [ ] Data cleaning: stationarity tests, seasonal adjustment, standardization

### Phase 3: Model Implementation
- [ ] Obtain DHK (2025) replication code (MATLAB/R/Python)
- [ ] Adapt code for Taiwan dataset
- [ ] Conduct preliminary estimation runs (~30 hours per run)
- [ ] Convergence diagnostics and validation

### Phase 4: Analysis (Three-Step Research Design)
- [ ] **Step 1**: Time-varying classification analysis
  - Plot classification probabilities for external variables over time
  - Identify regime shifts (2008, 2012, 2018, 2020, 2022)
- [ ] **Step 2**: Forecast error variance decomposition
  - Quantify % of Taiwan h_macro,t explained by each external variable
  - Quantify % of Taiwan h_financial,t explained by each external variable
- [ ] **Step 3**: Impulse response functions
  - IRFs of Taiwan variables to h_macro,t and h_financial,t shocks
  - IRFs of Taiwan variables to identified external shocks
- [ ] Robustness checks (alternative specifications, sample periods)

### Phase 5: Policy Implications and Writing
- [ ] Interpret findings for Central Bank of China (Taiwan) policy
- [ ] Complete research paper
- [ ] Policy brief for CBC and government agencies
- [ ] Conference presentations
- [ ] Journal submission

## Key Concepts and Terminology

### English Terms

- **SVMVAR**: Stochastic Volatility in Mean Vector Autoregression
- **OI-SVMVAR**: Order-Invariant SVMVAR (solves variable ordering problem)
- **DHK (2025)**: Davidson, Hou, and Koop (2025) reference paper
- **h_t = (h_m,t, h_f,t)'**: Taiwan's domestic macro and financial uncertainty factors
- **Transmission Channel**: The pathway (macro vs. financial) through which external shocks affect Taiwan
- **Time-Varying Classification**: Variable's classification (macro vs. financial) changes over time
- **Unclassified Variables**: Variables whose macro/financial nature is determined by the model, not researcher
- **FEVD**: Forecast Error Variance Decomposition
- **IRF**: Impulse Response Function

### Chinese Terms (繁體中文)

- **總體經濟變數**: Macroeconomic variables
- **金融變數**: Financial variables
- **未分類變數**: Unclassified variables
- **傳導管道**: Transmission channel
- **時變分類**: Time-varying classification
- **遺漏變數偏誤**: Omitted variables bias
- **順序不變性**: Order-invariance
- **小型開放經濟體**: Small open economy (SOE)
- **央行**: Central Bank of China (Taiwan) - CBC

## Critical Technical Challenges

1. **Data Availability**:
   - Challenge: Long time series (35+ years) for 40+ Taiwan variables
   - Mitigation: DGBAS and CBC provide comprehensive data; use FRED for US/global variables

2. **Computational Complexity**:
   - Challenge: MCMC estimation ~30 hours per run for 43-variable model
   - Mitigation: Secure high-performance computing resources; optimize code; prioritize critical specifications

3. **Code Implementation**:
   - Challenge: DHK (2025) developed novel MCMC algorithm; requires advanced programming
   - Mitigation: Obtain original replication code; study algorithm thoroughly before adaptation

4. **Research Positioning**:
   - Challenge: Must demonstrate this is NOT just "country replication"
   - Mitigation: Emphasize novel application of "unclassified variables" for transmission channel identification

## Comparison with DHK (2025)

| Dimension | DHK (2025) - US Study | Our Study - Taiwan |
|-----------|----------------------|-------------------|
| **Economy Type** | Large, relatively closed | Small, highly open |
| **Core Question** | Which uncertainty (macro vs. financial) dominates? | Which transmission channel (macro vs. financial) do external shocks use? |
| **Unclassified Variables** | Domestic ambiguous variables (S&P 500, Fed Funds, exchange rate) | **External shock sources** (US, China, global variables) |
| **Policy Relevance** | Fed should monitor which uncertainty type | CBC should know which channel to respond to |
| **Innovation Type** | Methodological (solve order-dependence, large models) | **Application** (use time-varying classification for channel identification) |
| **Model Extension** | New MCMC algorithm development | No extension—full application of existing framework |

**Key Distinction**: We use DHK's tool to answer a fundamentally different question that is uniquely relevant for small open economies.

## Development Notes

- This is a research-focused repository, not a software project
- Code development will primarily involve econometric estimation routines (MCMC)
- Maintain bilingual documentation: Chinese for research context, English for technical implementation
- Document all data sources and transformations meticulously for reproducibility
- Expected timeline: 18 months from data collection to journal submission

## Important Reminders for Claude Code Instances

1. **Always read `llm_logs/2025-11-08_discussion.md` first** when starting work—it contains all critical methodological decisions

2. **Do NOT suggest model extensions** (e.g., adding third uncertainty factor, imposing block exogeneity)—these were explicitly rejected after thorough analysis

3. **Focus on transmission channels, not impact magnitude**—the research question is "which channel?" not "how much?"

4. **External variables go in "unclassified"**—this is the core innovation

5. **Maintain 2-factor structure**: h_t = (h_macro,t, h_financial,t)' represents Taiwan's domestic uncertainty only

6. **Avoid over-emphasizing geopolitics/semiconductors**—while contextually relevant, these can cause the research to lose focus on the core methodological contribution

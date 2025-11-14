# Caught in the Crossfire

**Time-Varying Transmission of U.S.-China Uncertainty to Taiwan**

---

## Overview

This repository contains research materials for a study investigating how external uncertainty shocks from the United States and China transmit to Taiwan's economy. The project applies cutting-edge order-invariant stochastic volatility in mean vector autoregression (OI-SVMVAR) methodology to identify **time-varying transmission channels**—distinguishing whether external shocks impact Taiwan through **macroeconomic channels** (real economy) or **financial channels** (financial markets).

### Core Research Question

**"Do external uncertainty shocks from the U.S. and China transmit to Taiwan primarily through macroeconomic channels or financial channels? And how does this transmission mechanism change over time?"**

### Research Motivation

Taiwan, as a small open economy (SOE), faces unique exposure to external uncertainty:
- **Dual Dependence**: Economically integrated with both the US (technology, exports) and China (trade, investment)
- **Policy Relevance**: The Central Bank of China (Taiwan) needs to know which transmission channel dominates to select appropriate policy responses
- **Methodological Challenge**: Traditional VAR models cannot objectively identify time-varying transmission mechanisms without imposing arbitrary restrictions

Understanding **which channel** external shocks use to impact Taiwan is more policy-relevant than simply knowing **that** they impact Taiwan. Different channels require different policy tools.

---

## Key Innovation: Exploiting "Unclassified Variables" for Transmission Channel Identification

### The DHK (2025) Framework

This study applies the methodology from **Davidson, Hou, and Koop (2025)**, which allows variables to be classified as:
1. **Macroeconomic variables**: Clearly real economy variables (e.g., industrial production, employment)
2. **Financial variables**: Clearly financial market variables (e.g., stock returns, credit spreads)
3. **Unclassified variables**: Variables with ambiguous or time-varying characteristics

The model endogenously determines whether unclassified variables behave more like macro or financial variables **at each point in time**.

### Our Novel Application

**Key Insight**: We place all **external shock sources** (US variables, China variables, global indicators, US-China relations) into the "unclassified" category.

This allows the model to objectively identify:
- Whether US Federal Funds Rate shocks transmit to Taiwan through macro channels (affecting trade/production) or financial channels (affecting capital flows/exchange rates)
- Whether this transmission mechanism shifts during different episodes (2008 financial crisis vs. 2018 trade war vs. 2020 pandemic)
- Which external shock source has the greatest impact on Taiwan's macro vs. financial uncertainty

**This is NOT country replication**—we use DHK's framework to answer a fundamentally different question than they asked for the US.

---

## Three-Step Research Design

### Step 1: Identify Transmission Channels (Time-Varying Classification)
- **Tool**: Time-varying classification probabilities from the OI-SVMVAR model
- **Output**: Time-series plots showing when external variables (VIX, US-China relations, etc.) are classified as "macro" vs. "financial"
- **Research Question**: When did US monetary policy primarily affect Taiwan through financial channels vs. macro channels?

### Step 2: Quantify Shock Sources (Forecast Error Variance Decomposition)
- **Tool**: FEVD analysis
- **Output**: Percentage of Taiwan's macro uncertainty (h_m,t) and financial uncertainty (h_f,t) explained by each external variable
- **Research Question**: Which external shock—US, China, or US-China relations—contributes most to Taiwan's uncertainty?

### Step 3: Analyze Economic Consequences (Impulse Response Functions)
- **Tool**: IRF analysis
- **Output**: Dynamic responses of Taiwan's GDP, employment, stock market to identified external shocks
- **Research Question**: What are the real economic impacts of external shocks transmitted through different channels?

---

## Repository Structure

```
/
├── llm_logs/                    # Research discussion logs
│   ├── 2025-11-08_discussion.md # Core methodological decisions
│   ├── 2025-11-14_*.md          # Research direction clarification
│   └── discussion-template.md   # Template for new discussions
├── literature/                  # Literature review materials
│   ├── uncertainty_shock_literature.md        # Global uncertainty literature
│   └── taiwan_specific_uncertainty_literature.md  # Taiwan-specific studies
├── references/                  # Reference papers
│   └── Investigating Economic Uncertain.pdf  # Davidson, Hou, Koop (2025)
├── CLAUDE.md                    # Guide for Claude Code instances
├── README.md                    # This file
└── research_proposal.tex        # Research proposal (LaTeX)
```

---

## Methodological Approach

### Why Order-Invariant SVMVAR?

The DHK (2025) framework solves three critical problems:

1. **Model Size**: Requires 40+ variables to avoid omitted variable bias (small models produce incorrect conclusions)
2. **Order-Invariance**: Results do not depend on arbitrary variable ordering (unlike traditional Cholesky decomposition)
3. **Time-Varying Classification**: Transmission mechanisms can shift across different economic regimes

### Our Model Specification

**Two Latent Uncertainty Factors** (maintained from DHK):
- h_t = (h_macro,t, h_financial,t)'
- These represent Taiwan's domestic macro and financial uncertainty

**Variable Classification Strategy**:
- **Macro**: Taiwan IPI, employment, CPI, exports, wages, etc.
- **Financial**: TAIEX returns, stock volatility, credit spreads, interest rate spreads
- **Unclassified** (KEY INNOVATION):
  - **US variables**: FFR, IPI, credit spread, EPU
  - **China variables**: IPI, PPI, total social financing
  - **Global indicators**: VIX, GPR, global EPU
  - **US-China relations**: Trade policy uncertainty, geopolitical risk indices

The model will reveal whether these external variables transmit shocks to Taiwan through h_macro,t (macro channel) or h_financial,t (financial channel), and how this evolves over time.

---

## Research Contributions

### 1. Methodological Contribution
- **First application** of "unclassified variables" feature to identify **transmission channels** of external shocks
- Demonstrates that DHK's framework can answer questions beyond macro vs. financial uncertainty decomposition

### 2. Empirical Contribution
- **Data-driven identification** of time-varying external shock transmission mechanisms
- Quantification of relative importance of US, China, and US-China relations for Taiwan
- Detection of structural breaks in transmission channels (e.g., 2008, 2012, 2018)

### 3. Policy Contribution
- Guidance for Central Bank of China (Taiwan) on which policy tools to use depending on which transmission channel dominates
- Evidence on whether exchange rate flexibility helps or hurts under different types of external shocks
- Implications for small open economy monetary policy design

---

## Data Requirements

### Frequency and Coverage
- **Frequency**: Monthly
- **Time Period**: ~1990–2025 (35+ years)
- **Total Variables**: 40+ variables

### Data Categories

**Taiwan Domestic Variables** (30+ variables):
- Output: IPI, manufacturing production, export orders, retail sales
- Prices: CPI, core CPI, WPI, import/export price indices
- Labor: Unemployment rate, employment, wages
- Financial: TAIEX returns/volatility, interest rates, credit growth, foreign investment

**External Variables (Unclassified)** (10+ variables):
- **US**: Federal Funds Rate, IPI, BAA-AAA credit spread, EPU/uncertainty index
- **China**: Industrial production, PPI, total social financing
- **Global**: VIX, global EPU, geopolitical risk (GPR)
- **US-China**: Trade policy uncertainty, bilateral relations indicators

### Data Sources
- Taiwan: DGBAS (Directorate-General of Budget, Accounting and Statistics), CBC (Central Bank of China)
- US: Federal Reserve Economic Data (FRED)
- Global: Baker-Bloom-Davis EPU, Caldara-Iacoviello GPR, VIX (CBOE)

---

## Expected Findings

### Hypothesis 1: Time-Varying Transmission Channels
- US monetary policy (FFR) transmits through financial channels during normal periods (affecting capital flows/exchange rates)
- US monetary policy transmits through macro channels during global recessions (affecting export demand)

### Hypothesis 2: Differential China vs. US Transmission
- Chinese shocks primarily transmit through macro channels (trade/supply chain effects)
- US shocks transmit through both channels with time-varying dominance

### Hypothesis 3: Structural Breaks
- 2008 financial crisis: External shocks primarily through financial channels
- 2018 trade war: Shift toward macro channel transmission
- 2020 pandemic: Mixed transmission depending on shock type

---

## Research Progress

### Phase 0: Literature Review ✓ (Completed)
- [x] Global uncertainty shock literature (20+ papers)
- [x] Taiwan-specific studies (10+ papers)
- [x] Methodological foundations (DHK 2025, Chan-Koop-Yu 2024, etc.)
- [x] Research gap identification and positioning

### Phase 1: Research Design ✓ (Completed)
- [x] Core research question finalized
- [x] Methodological framework confirmed (apply DHK 2025, no extensions)
- [x] Three-step analysis plan established
- [x] Variable classification strategy determined

### Phase 2: Data Collection (Current Phase)
- [ ] Assemble Taiwan macro variables (1990-2025, monthly)
- [ ] Assemble Taiwan financial variables
- [ ] Obtain US variables (FRED)
- [ ] Obtain China variables
- [ ] Construct/obtain global uncertainty indices
- [ ] Data cleaning and transformation (stationarity, seasonal adjustment)

### Phase 3: Model Implementation (Planned)
- [ ] Obtain DHK (2025) replication code
- [ ] Adapt code for Taiwan dataset
- [ ] Conduct preliminary estimation runs
- [ ] Diagnostic checks and convergence validation

### Phase 4: Analysis (Planned)
- [ ] Step 1: Time-varying classification analysis
- [ ] Step 2: Forecast error variance decomposition
- [ ] Step 3: Impulse response function analysis
- [ ] Robustness checks (alternative specifications, sample periods)

### Phase 5: Writing and Dissemination (Planned)
- [ ] Complete research paper
- [ ] Policy brief for Central Bank of China (Taiwan)
- [ ] Conference presentations
- [ ] Journal submission

---

## Key Literature

### Methodological Foundation

**Davidson, J., Hou, K., & Koop, G. (2025)**
"Investigating Economic Uncertainty Using Stochastic Volatility in Mean VARs: The Importance of Model Size, Order-Invariance and Classification"
*Journal of Business & Economic Statistics* (forthcoming)

**Chan, J. C., Koop, G., & Yu, X. (2024)**
"Large Order-Invariant Bayesian VARs with Stochastic Volatility"
*Journal of Business & Economic Statistics*, 42(2), 825-837

**Brianti, M. (2025)**
"Financial Shocks, Uncertainty Shocks, and Corporate Liquidity"
*Journal of Applied Econometrics*

### Taiwan Context

**Sin, C.-Y. (2015)**
"The Economic Fundamental and Economic Policy Uncertainty of Mainland China and Their Impacts on Taiwan and Hong Kong"
*North American Journal of Economics and Finance*, 40, 298-311

**Huang, Y.-L., Yeh, C.-C., & Chen, M.-C. (2019)**
"An Economic Policy Uncertainty Index for Taiwan"
*Taiwan Economic Review*, 49(2)

### Small Open Economy Literature

**Galí, J., & Monacelli, T. (2005)**
"Monetary Policy and Exchange Rate Volatility in a Small Open Economy"
*Review of Economic Studies*, 72(3), 707-734

See `literature/` directory for comprehensive literature review with 40+ papers.

---

## Technical Requirements

### Computational
- High-performance computing resources (estimation ~30 hours per run for 43-variable model)
- MATLAB, R, or Python environment for MCMC implementation
- Sufficient storage for MCMC output (5,000+ posterior draws)

### Software
- Bayesian estimation packages
- Time-series analysis tools
- Visualization software for time-varying probabilities

---

## Comparison with DHK (2025)

| Dimension | DHK (2025) - US Study | Our Study - Taiwan |
|-----------|----------------------|-------------------|
| **Economy Type** | Large, relatively closed | Small, highly open |
| **Core Question** | Which uncertainty (macro vs. financial) dominates? | Which transmission channel (macro vs. financial) dominates? |
| **Unclassified Variables** | Domestic ambiguous variables (S&P 500, Fed Funds, exchange rate) | **External shock sources** (US, China, global variables) |
| **Policy Relevance** | Fed should monitor which uncertainty type | CBC should know which channel external shocks use |
| **Innovation** | Methodological: solve order-dependence, large models, time-varying classification | **Application**: use time-varying classification to identify transmission channels |

**Key Distinction**: We use DHK's tool to answer a fundamentally different question that is uniquely relevant for small open economies.

---

## Documentation Language

- **Research Context and Discussions**: Traditional Chinese (繁體中文)
- **Code and Technical Documentation**: English
- **README and Proposal**: English with Chinese translation

This bilingual approach ensures accessibility for both international researchers and local policy stakeholders.

---

## Citation

If you use materials from this repository, please cite:

```
[Author Name]. (2025). "Caught in the Crossfire: Time-Varying Transmission
of U.S.-China Uncertainty to Taiwan." [Research in Progress]
```

---

## Acknowledgments

This research builds on the groundbreaking methodological innovations by Davidson, Hou, and Koop (2025) and extensive prior work on uncertainty measurement, small open economy macroeconomics, and international shock transmission.

---

*Last Updated: 2025-11-14*

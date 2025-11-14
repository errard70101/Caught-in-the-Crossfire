# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Title**: "Caught in the Crossfire" - Investigating Economic Uncertainty in Taiwan Using Stochastic Volatility in Mean VARs

**Research Objective**: Apply order-invariant stochastic volatility in mean vector autoregressions (OI-SVMVAR) to analyze economic uncertainty in Taiwan, distinguishing between macroeconomic and financial uncertainty sources.

**Methodological Foundation**: Based on Davidson, Hou, and Koop (2025) "Investigating Economic Uncertainty Using Stochastic Volatility in Mean VARs: The Importance of Model Size, Order-Invariance and Classification"

**Primary Language**: Traditional Chinese (繁體中文) for discussions and documentation, though code and technical content may be in English.

## Research Context

### Key Methodological Features

1. **Large-Scale Model**: Requires 40+ variables (small models with ~30 variables produce biased results)
2. **Order-Invariance**: Solves the variable ordering problem inherent in traditional large VAR models
3. **Time-Varying Classification**: Variables can be classified as:
   - **Macroeconomic variables** (總體經濟變數): Real economy indicators
   - **Financial variables** (金融變數): Financial market indicators
   - **Unclassified variables** (未分類變數): Ambiguous variables whose classification can change over time (e.g., exchange rates, policy rates)

4. **Taiwan-Specific Considerations**:
   - Small open economy requiring inclusion of US variables
   - US-China relationship indicators as uncertainty sources
   - Geopolitical risk factors unique to Taiwan

### Research Questions

- Which type of uncertainty (macro vs. financial) has greater impact on Taiwan's real economy?
- How do key variables (e.g., TWD/USD exchange rate, TAIEX) shift between macro and financial classifications over time?
- How do US variables and US-China relations transmit uncertainty to Taiwan?

## Repository Structure

```
/
├── llm_logs/                    # LLM conversation logs for research brainstorming
│   ├── 2025-11-08_discussion.md # Extensive discussion on methodology and data
│   └── discussion-template.md   # Template for logging new discussions
├── literature/                  # Literature review and related work
│   └── uncertainty_shock_literature.md  # Comprehensive literature review
├── references/                  # Reference papers and materials
│   └── Investigating Economic Uncertain.pdf  # Davidson, Hou, Koop (2025)
└── research_proposal.md         # Research proposal template (to be filled)
```

## Working with LLM Discussion Logs

The `llm_logs/` directory contains detailed research discussions in Traditional Chinese. Key discussion in `2025-11-08_discussion.md` covers:

- Rationale for applying DHK (2025) methodology to Taiwan
- Proposed 43-variable database structure for Taiwan
- Justification for including US variables (US FFR, US IPI, US credit spreads)
- Proposal to include US-China relationship indicators
- Data availability challenges and computational complexity considerations

When adding new discussion logs:
- Use the template in `llm_logs/discussion-template.md`
- Include date, model used, and purpose
- Document key insights and next action items

## Working with Literature Review

The `literature/` directory contains comprehensive literature review materials to strengthen research motivation and identify gaps.

**Key document**: `uncertainty_shock_literature.md` provides systematic review organized in 4 phases:

1. **Phase 1: Core Uncertainty Shock Literature**
   - Foundational measurement papers (Baker-Bloom-Davis EPU, Jurado-Ludvigson-Ng)
   - VAR-based identification (Carriero-Clark-Marcellino, Banbura-Giannone-Reichlin)
   - Order-invariant methods (Chan-Koop-Yu 2024) directly supporting DHK (2025)

2. **Phase 2: Small Open Economy & Uncertainty Transmission**
   - International spillover mechanisms and transmission channels
   - Panel VAR studies including Taiwan as emerging market
   - Korea and Singapore as comparable cases

3. **Phase 3: Decomposition of Uncertainty Types**
   - Separating macro vs. financial uncertainty (Caldara et al., Brianti 2025)
   - Different policy responses required for each type
   - Macro uncertainty causes deflation; financial uncertainty doesn't

4. **Phase 4: Taiwan/Asia-Pacific Context**
   - Taiwan-specific studies (Sin 2015, Huang et al. 2019)
   - US-China trade war impacts on Taiwan
   - Taiwan's "caught in crossfire" position

**Research Gaps Identified**:
- No order-invariant SVMVAR applied to small open economies
- No macro vs. financial uncertainty decomposition for Taiwan
- No quantitative study of dual US-China uncertainty exposure
- No guidance for CBC on responding to different uncertainty types

**Novel Contributions This Research Makes**:
1. First order-invariant SVMVAR for small open economy
2. First dual US-China exposure quantification
3. Taiwan-specific geopolitical risk integration
4. Solves real CBC policy puzzle
5. Validates DHK (2025) in new context
6. Globally relevant (semiconductor industry)

## Expected Research Workflow

### Phase 0: Literature Review ✓ (Completed)
- Systematic review of global uncertainty shock literature
- Identification of methodological foundations
- Documentation of research gaps
- Positioning of Taiwan research contributions

### Phase 1: Data Collection (Current Phase)
- Assemble 40+ monthly frequency variables from ~1990 onward
- Include Taiwan macro variables (IPI, CPI, unemployment, exports, etc.)
- Include Taiwan financial variables (TAIEX, interest rates, credit spreads, etc.)
- Include US variables (FFR, IPI, credit spreads)
- Include US-China relationship indicators
- Standardize transformations (stationary, seasonal adjustment)

### Phase 2: Model Implementation
- Implement or adapt MCMC algorithm for OI-SVMVAR estimation
- Expected computational intensity: ~30 hours per estimation for 43-variable model
- Likely requires R, MATLAB, or Python with advanced numerical capabilities

### Phase 3: Analysis
- Estimate separate uncertainty factors: h_t = (h_macro,t, h_financial,t)'
- Analyze impulse responses and variance decompositions
- Identify time-varying classification of unclassified variables
- Compare results with small-model estimates to demonstrate size importance

### Phase 4: Policy Implications
- Determine whether macro or financial uncertainty dominates in Taiwan
- Provide guidance for Central Bank of China (Taiwan) policy responses

## Key Concepts and Terminology

- **SVMVAR**: Stochastic Volatility in Mean Vector Autoregression
- **OI-SVMVAR**: Order-Invariant SVMVAR (solves variable ordering problem)
- **DHK (2025)**: Davidson, Hou, and Koop (2025) reference paper
- **h_t = (h_m,t, h_f,t)'**: Macro and financial uncertainty factors
- **遺漏變數偏誤 (Omitted Variables Bias)**: Key problem solved by large models
- **時變分類 (Time-Varying Classification)**: Dynamic variable classification feature

## Technical Challenges

1. **Data Availability**: Long time series (35+ years) for 40+ Taiwan variables may be difficult to obtain
2. **Computational Complexity**: MCMC estimation is computationally intensive; requires access to original code or reimplementation
3. **Model Adaptation**: May need to modify framework to distinguish domestic vs. global uncertainty rather than macro vs. financial
4. **Publication Strategy**: Must position as solving Taiwan-specific policy puzzle, not just "country replication"

## Development Notes

- This is a research-focused repository, not a software project
- Code development (when it begins) will primarily involve econometric estimation routines
- Maintain bilingual documentation: Chinese for research context, English for technical implementation
- Document all data sources and transformations meticulously for reproducibility

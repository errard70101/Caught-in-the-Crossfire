# Caught in the Crossfire

**Research Project: Investigating Economic Uncertainty in Taiwan Using Stochastic Volatility in Mean VARs**

---

## Overview

This repository contains research materials for a study investigating economic uncertainty in Taiwan, with particular focus on distinguishing between macroeconomic and financial uncertainty sources. The project applies cutting-edge order-invariant stochastic volatility in mean vector autoregression (OI-SVMVAR) methodology to analyze Taiwan's unique position as a small open economy "caught in the crossfire" of US-China economic tensions.

### Research Motivation

Taiwan faces a unique combination of economic challenges:
- **Small Open Economy**: Highly dependent on international trade and capital flows
- **Dual Exposure**: Simultaneous economic dependence on both the US (technology, defense) and China (trade, investment)
- **Geopolitical Risk**: Taiwan Strait tensions create distinct uncertainty not faced by comparable economies
- **Semiconductor Centrality**: Taiwan's dominance in semiconductor manufacturing makes its economic stability globally significant

Understanding whether **macroeconomic uncertainty** or **financial uncertainty** has a greater impact on Taiwan's economy is critical for effective Central Bank policy responses.

---

## Key Research Questions

1. Which type of uncertainty (macro vs. financial) has a greater impact on Taiwan's real economy?
2. How do key variables like the TWD/USD exchange rate and TAIEX stock index shift between macro and financial classifications over time?
3. How do US variables and US-China relations transmit uncertainty to Taiwan?
4. What are the appropriate Central Bank of China (Taiwan) policy responses to different uncertainty types?

---

## Methodological Approach

### Based on Davidson, Hou, and Koop (2025)

The study applies the order-invariant SVMVAR methodology from Davidson, Hou, and Koop (2025), which addresses three critical challenges:

1. **Model Size**: Requires 40+ variables (smaller models produce biased results due to omitted variables)
2. **Order-Invariance**: Solves the variable ordering problem inherent in traditional large VAR models
3. **Time-Varying Classification**: Allows variables to shift between macro/financial classifications over time

### Novel Contributions

This is **not** simple country replication. The Taiwan research makes six novel contributions:

1. **Methodological**: First application of order-invariant SVMVAR to a small open economy
2. **Dual Exposure**: First quantitative decomposition of dual US-China uncertainty exposure
3. **Geopolitical Risk**: Integration of Taiwan-specific geopolitical uncertainty indicators
4. **Policy Puzzle**: Solves real Central Bank policy question (macro vs. financial uncertainty dominance)
5. **Validation**: Tests whether DHK (2025) findings hold in small open economy context
6. **Global Relevance**: Taiwan's semiconductor industry makes uncertainty dynamics globally important

---

## Repository Structure

```
/
├── llm_logs/                    # Research discussion logs
│   ├── 2025-11-08_discussion.md # Methodology and data discussion
│   └── discussion-template.md   # Template for new discussions
├── literature/                  # Literature review materials
│   └── uncertainty_shock_literature.md  # Comprehensive literature review
├── references/                  # Reference papers
│   └── Investigating Economic Uncertain.pdf  # Davidson, Hou, Koop (2025)
├── CLAUDE.md                    # Guide for Claude Code instances
├── README.md                    # This file
└── research_proposal.md         # Research proposal (to be completed)
```

---

## Research Progress

### ✓ Completed

- [x] Initial project setup and methodological framework
- [x] Comprehensive literature review (20+ papers reviewed)
- [x] Research gap identification and contribution positioning
- [x] 43-variable database design for Taiwan

### 🔄 In Progress

- [ ] Data collection (40+ monthly variables from ~1990 onward)
  - Taiwan macroeconomic variables (IPI, CPI, unemployment, exports, etc.)
  - Taiwan financial variables (TAIEX, interest rates, credit spreads, etc.)
  - US variables (FFR, IPI, credit spreads)
  - US-China relationship indicators

### 📋 Planned

- [ ] Model implementation (MCMC algorithm for OI-SVMVAR estimation)
- [ ] Estimation and analysis (impulse responses, variance decompositions)
- [ ] Policy implications for Central Bank of China (Taiwan)
- [ ] Research paper preparation

---

## Key Literature

### Methodological Foundation

- **Davidson, Hou, and Koop (2025)**: "Investigating Economic Uncertainty Using Stochastic Volatility in Mean VARs: The Importance of Model Size, Order-Invariance and Classification"
- **Chan, Koop, and Yu (2024)**: "Large Order-Invariant Bayesian VARs with Stochastic Volatility" - *Journal of Business & Economic Statistics*
- **Brianti (2025)**: "Financial Shocks, Uncertainty Shocks, and Corporate Liquidity" - *Journal of Applied Econometrics*

### Taiwan Context

- **Sin (2015)**: "The Economic Fundamental and Economic Policy Uncertainty of Mainland China and Their Impacts on Taiwan and Hong Kong"
- **Huang, Yeh, and Chen (2019)**: "An Economic Policy Uncertainty Index for Taiwan" - *Taiwan Economic Review*

### Uncertainty Measurement

- **Baker, Bloom, and Davis (2016)**: "Measuring Economic Policy Uncertainty" - *Quarterly Journal of Economics*
- **Jurado, Ludvigson, and Ng (2015)**: "Measuring Uncertainty" - *American Economic Review*

See `literature/uncertainty_shock_literature.md` for complete literature review with 20+ papers.

---

## Technical Details

### Model Specification

- **Variables**: 40+ monthly frequency variables (1990-present)
- **Uncertainty Factors**: h_t = (h_macro,t, h_financial,t)'
- **Classification**: Macro variables, financial variables, and time-varying unclassified variables
- **Estimation**: Bayesian MCMC methods (expected ~30 hours per estimation for 43-variable model)

### Data Sources

- Taiwan statistical agencies (DGBAS, CBC)
- US Federal Reserve Economic Data (FRED)
- Baker-Bloom-Davis Economic Policy Uncertainty Index
- Ludvigson Macro and Financial Uncertainty Indexes

---

## Research Team

This is an independent research project. For inquiries or collaboration opportunities, please open an issue in this repository.

---

## Documentation Language

- **Research Context and Discussions**: Traditional Chinese (繁體中文)
- **Code and Technical Documentation**: English
- **README and CLAUDE.md**: English

This bilingual approach ensures accessibility for both international researchers and local policy stakeholders.

---

## License

Research materials in this repository are for academic purposes. Please cite appropriately if using these materials.

---

## Acknowledgments

This research builds on methodological innovations by Davidson, Hou, and Koop (2025) and extensive prior work on uncertainty measurement and small open economy macroeconomics.

---

*Last Updated: 2025-11-14*

# Global Uncertainty Shock Literature Review

**Purpose**: Identify related empirical global uncertainty shock literature to improve the motivation for the Taiwan economic uncertainty research proposal.

**Date Created**: 2025-11-14
**Last Updated**: 2025-11-14

---

## Phase 1: Core Uncertainty Shock Literature

### 1.1 Foundational Uncertainty Measurement Papers

#### Economic Policy Uncertainty (EPU) Indices

**Baker, Bloom, and Davis (2016)** - "Measuring Economic Policy Uncertainty"
- **Publication**: Quarterly Journal of Economics, 131(4), 1593-1636
- **Methodology**: Newspaper-based index using 10 major US newspapers, searching for articles containing: (1) "economic" or "economy", (2) "uncertain" or "uncertainty", and (3) policy-related terms ("congress", "deficit", "Federal Reserve", "legislation", "regulation", "White House")
- **Validation**: Human readings of 12,000 newspaper articles confirm the index proxies for policy-related economic uncertainty
- **Additional components**: Federal tax code provisions set to expire, forecaster disagreement over future inflation and government purchases
- **Key findings**: US EPU spikes near presidential elections, Gulf Wars I and II, 9/11 attacks, Lehman Brothers failure, 2011 debt ceiling dispute
- **Data availability**: www.PolicyUncertainty.com provides country-level indices including Taiwan
- **Relevance to Taiwan**: Global EPU index framework provides benchmark for Taiwan EPU measurement

#### Macro Uncertainty Measures

**Jurado, Ludvigson, and Ng (2015)** - "Measuring Uncertainty"
- **Publication**: American Economic Review, 105(3), 1177-1216
- **Methodology**: Data-rich environment with diffusion index forecasting; removes forecastable component before computing conditional volatility
- **Key findings**:
  - Their estimates show significant independent variation from popular uncertainty proxies
  - Much of the variation in proxies is NOT driven by uncertainty
  - Quantitatively important uncertainty episodes occur far more infrequently than indicated by proxies
  - When uncertainty episodes occur, they are larger, more persistent, and more correlated with real activity
- **Data availability**: FRED maintains JLN uncertainty series at 1-month, 3-month, and 12-month horizons
- **Relevance to Taiwan**: Methodological approach for proper uncertainty measurement distinguishes signal from noise

**Ludvigson Macro and Financial Uncertainty Indexes**
- **Source**: Sydney Ludvigson's website maintains separate macro and financial uncertainty indexes
- **Key distinction**: Separates uncertainty stemming from macroeconomic fundamentals vs. financial market conditions
- **Relevance to Taiwan**: Directly addresses the macro vs. financial uncertainty decomposition central to the Taiwan research

#### Financial Uncertainty Measures

**VIX and Related Measures**
- Standard financial market volatility proxies widely used in uncertainty literature
- Criticized by JLN (2015) as conflating volatility with true uncertainty

### 1.2 VAR-Based Uncertainty Shock Identification

**Carriero, Clark, and Marcellino (2018)** - "Measuring Uncertainty and Its Impact on the Economy"
- **Publication**: Review of Economics and Statistics
- **Methodology**: Large VAR model with stochastic volatility
- **Key findings**:
  - Substantial commonality in uncertainty across variables
  - Sizable effects on key macroeconomic and financial variables
- **Relevance to Taiwan**: Framework for extracting common uncertainty factors from large-scale VARs

**Carriero, Clark, and Marcellino (2019)** - "Large Bayesian Vector Autoregressions with Stochastic Volatility and Non-Conjugate Priors"
- **Publication**: Journal of Econometrics, 212(1), 137-154
- **Methodology**: New Bayesian algorithm computationally efficient for large VARs with stochastic volatility
- **Key contribution**: Allows jointly modeling many variables with time-varying volatility
- **Relevance to Taiwan**: Computational methods applicable to 40+ variable Taiwan model

**Carriero, Clark, Marcellino (other works)**
- "Endogenous Uncertainty": Structural VAR where uncertainty impacts both mean and variance
- "Addressing COVID-19 Outliers in BVARs with Stochastic Volatility": Outlier-adjusted SV models combining transitory and persistent volatility changes

**Banbura, Giannone, and Reichlin (2010)** - "Large Bayesian VARs"
- **Publication**: Journal of Applied Econometrics, 25(1), 71-92
- **Key findings**:
  - VAR with Bayesian shrinkage appropriate for large dynamic models
  - Setting degree of shrinkage in relation to cross-sectional dimension improves forecasting
  - Large VARs with shrinkage produce credible impulse responses suitable for structural analysis
  - Controls for over-fitting while preserving sample information when data exhibit strong collinearity (typical for macro time series)
- **Relevance to Taiwan**: Foundation for large-scale Bayesian VAR estimation with 40+ variables

**Chan, Koop, and Yu (2024)** - "Large Order-Invariant Bayesian VARs with Stochastic Volatility"
- **Publication**: Journal of Business & Economic Statistics, 42(2), 825-837
- **Problem addressed**: Lower triangular parameterization of error covariance matrix makes many BVAR-SV specifications non-invariant to variable ordering; problem worsens in large VARs
- **Solution**: Specification avoiding lower triangular parameterization; multivariate stochastic volatility allows identification while maintaining order invariance
- **Key findings**:
  - Variable ordering can substantially affect predictive standard deviations
  - Order-invariant approach produces best forecasts in 20-variable macro forecasting exercise
  - Some ordering choices lead to poor forecasts in conventional approach
- **Relevance to Taiwan**: **DIRECTLY RELEVANT** - Addresses the order-invariance problem central to Davidson, Hou, and Koop (2025) methodology

**Factor Stochastic Volatility Approaches**
- "Large Bayesian VARs with Factor Stochastic Volatility: Identification, Order Invariance and Structural Analysis" (arXiv:2207.03988)
- Order-invariant reduced-form VAR with factor SV; with sign restrictions, structural model is point-identified
- **Relevance to Taiwan**: Alternative order-invariant identification strategy

---

## Phase 2: Small Open Economy & Uncertainty Transmission

### 2.1 International Uncertainty Spillovers

**General Spillover Literature**

Key transmission mechanisms:
- **Exchange rate channel**: Currency adjustments transmit uncertainty effects
- **Aggregate demand channel**: Trade linkages propagate shocks
- **Financial channel**: Investment and credit channels emphasizing US interest rates
- **Supply chain channel**: Transnational supply chains (trade credit and inventory turnover)

**Panel VAR Studies on Emerging Markets**
- Monthly panel VAR for 15 emerging markets: Brazil, Chile, Colombia, India, Indonesia, Malaysia, Mexico, Peru, Philippines, Russia, South Africa, South Korea, **Taiwan**, Thailand, Turkey
- **Key findings**: US uncertainty shocks negatively affect EM stock prices and exchange rates, raise country spreads, decrease capital inflows, decrease output and consumer prices, increase net exports
- **Heterogeneity**: Differential monetary policy responses rationalize heterogeneity in cross-border transmission

**Global VAR (GVAR) Approaches**
- US policy uncertainty shocks are significant in driving business cycle fluctuations globally
- **Time-varying spillovers**: TVP-VAR models reveal evolving spillover effects capturing how uncertainty transmits across markets regionally and globally

**Spillover Network Analysis**
- Combines spillover index approach and LASSO-VAR to construct EPU spillover networks
- **Finding**: Transnational contagion of EPU is significant; spillover networks are time-varying
- **COVID-19 context**: Spillover networks show significant changes during pandemic

**US Monetary Policy Uncertainty Spillovers**
- US monetary policy rate hikes lead to declines in EM output growth, inflation, and exchange rate depreciation, especially when accompanied by policy uncertainty surges
- Different mechanisms for advanced vs. emerging countries: for emerging countries, the expected component of yields reacts to uncertainty

### 2.2 Small Open Economy Vulnerabilities

**Galí and Monacelli (2005)** - "Monetary Policy and Exchange Rate Volatility in a Small Open Economy"
- **Publication**: Review of Economic Studies, 72(3), 707-734
- **Framework**: Small open economy Calvo sticky price model
- **Policy regimes compared**: Domestic inflation targeting, CPI-based Taylor rules, exchange rate peg
- **Key finding**: Regimes differ substantially in exchange rate volatility they entail
- **Relevance to Taiwan**: Benchmark DSGE model for small open economy monetary policy analysis

**Uncertainty Shocks and Monetary Policy Rules in Small Open Economies**
- **Key finding**: Currently followed interest rate rules under flexible inflation-targeting regimes are ineffective in stabilizing economies during high global uncertainty periods in EMEs
- **Policy implication**: Best monetary policy rule depends on whether shock is first-moment or second-moment (uncertainty) shock
- **Relevance to Taiwan**: Directly addresses Central Bank of China (Taiwan) policy responses to uncertainty

**Exchange Rate as Shock Absorber**
- In US: real effective exchange rate amplifies uncertainty shock effects
- In open economies: exchange rate typically helps absorb shocks
- Negative effects of increased uncertainty often counteracted by real exchange rate depreciation
- **Relevance to Taiwan**: TWD/USD dynamics under uncertainty crucial for understanding transmission

**Asia-Pacific Trade and Capital Flow Vulnerabilities (2025 outlook)**
- Asia-Pacific faces greater vulnerability to uncertain trade environment and weaker global demand
- Asset price volatility increases potential for disrupting capital flows and investment
- Trade uncertainty leads export-oriented firms to hold back investments, raises supply chain doubts
- Geopolitical risks lead to capital flow pullbacks and risk premium increases
- **Information asymmetry**: Increased geopolitical risk reduces cross-border investment activities of US investors in Asia-Pacific markets
- **Relevance to Taiwan**: Export-oriented economy highly vulnerable to trade uncertainty and US-China tensions

**Korea as Comparable Case**
- "Variance Risk Premium in a Small Open Economy with Volatile Capital Flows: The Case of Korea"
- Studies VRP, economic uncertainty, and macroeconomic variables using regression and FAVAR analyses
- **Relevance to Taiwan**: Methodological precedent for small open economy with volatile capital flows

**Economic Uncertainty and Spillover Networks in Asia-Pacific**
- Uses FAVAR model with 35 economic indicators for 12 Asia-Pacific countries (2000-2020)
- Calculates macro economic uncertainty indexes and constructs uncertainty spillover networks
- Includes both **South Korea** and **Singapore** as comparators
- **Relevance to Taiwan**: Regional spillover network analysis framework

---

## Phase 3: Decomposition of Uncertainty Types

### 3.1 Macro vs. Financial Uncertainty

**Caldara, Fuentes-Albero, Gilchrist, and Zakrajšek (2016)** - "The Macroeconomic Impact of Financial and Uncertainty Shocks"
- **Publication**: European Economic Review, Vol. 88
- **Challenge addressed**: High comovement between financial distress and uncertainty proxies complicates identification; both are "fast moving" variables; difficult to impose zero contemporaneous restrictions or sign restrictions since both have same qualitative effects
- **Identification strategy**: Penalty function approach where each structural innovation is identified by maximizing impulse response of its respective target variable over pre-specified horizon
- **Key findings**:
  - Financial shocks generate slowly-building, economically significant recessions with slow recoveries
  - Uncertainty shocks generate similar adverse effects IF transmitted through financial channel
  - Without financial transmission, uncertainty shocks have significantly smaller effects
- **Relevance to Taiwan**: **CRITICAL** - Demonstrates importance of distinguishing financial from uncertainty channels; methodology for separate identification

**Caggiano, Castelnuovo, and Figueres (2021)** - "Financial Uncertainty and Real Activity: The Good, the Bad, and the Ugly"
- **Publication**: European Economic Review
- **Methodology**: VAR with novel combination of sign, ratio, and narrative restrictions to separately identify financial uncertainty and credit supply shocks
- **Key findings**:
  - Finance uncertainty multiplier is around 2
  - Credit supply disruptions double the negative output response to uncertainty shock
  - Financial uncertainty effects are amplified through credit channel
- **Relevance to Taiwan**: Quantifies financial channel amplification of uncertainty effects

**Brianti (2025)** - "Financial Shocks, Uncertainty Shocks, and Corporate Liquidity"
- **Publication**: Journal of Applied Econometrics (2025)
- **Identification**: Structural VAR with sign restrictions separately identifying financial shocks, macro uncertainty, and financial uncertainty shocks
- **Key distinguishing feature**: Corporate liquidity responses differ:
  - Financial shocks: firms draw down liquidity (lose external finance access)
  - Uncertainty shocks: firms increase liquid assets (precautionary motive)
- **Macro vs. Financial Uncertainty**:
  - All three shocks have contractionary effects
  - **ONLY macro uncertainty shocks trigger deflationary patterns**
  - Different conditional correlation between output and inflation has policy implications
- **Policy implications**:
  - Macro uncertainty shocks: allow simultaneous stabilization of output and inflation
  - Financial shocks: may require trading off price stability vs. output stabilization
- **Relevance to Taiwan**: **HIGHLY RELEVANT** - Provides structural identification strategy for distinguishing macro vs. financial uncertainty; different policy responses required

**Interaction Effects: Macro Uncertainty Amplifying Financial Volatility**
- Research on US and Japan: increase in financial volatility lowers industrial production and business-fixed investment more persistently when macroeconomic uncertainty is higher
- **Non-linear effects**: Financial volatility impact depends on state of macro uncertainty
- **Relevance to Taiwan**: Suggests interaction terms between macro and financial uncertainty may be important

**Cholesky Decomposition Critique**
- Cholesky decomposition may be ill-suited for capturing contemporaneous interactions among uncertainty variables
- Imposes restrictive zero-impact assumptions
- **Relevance to Taiwan**: Supports Davidson, Hou, Koop (2025) order-invariant approach over traditional Cholesky identification

---

## Phase 4: Taiwan/Asia-Pacific Context

### 4.1 Taiwan-Specific or Comparable Studies

**Sin (2015)** - "The Economic Fundamental and Economic Policy Uncertainty of Mainland China and Their Impacts on Taiwan and Hong Kong"
- **Publication**: The North American Journal of Economics and Finance, 40, 298-311
- **Methodology**: Structural VAR applied to Taiwan and Hong Kong economies investigating impacts of Chinese economy
- **Model specification**:
  - Four domestic variables: output, interest rate, price level, real exchange rate
  - Two foreign variables: Mainland China output, China monthly EPU index
- **Identification**: Based on fact that China has causal effect on Taiwan and Hong Kong but not reverse; uses both short-run and long-run restrictions
- **Relevance to Taiwan**: **DIRECTLY APPLICABLE** - Demonstrates small economy VAR framework with China as external shock source

**Huang, Yeh, and Chen (2019)** - "An Economic Policy Uncertainty Index for Taiwan"
- **Publication**: Taiwan Economic Review, 49(2)
- **Contribution**: Constructs Taiwan-specific EPU index following Baker, Bloom, Davis methodology
- **Data availability**: Provides time series for Taiwan EPU
- **Relevance to Taiwan**: **ESSENTIAL DATA SOURCE** for Taiwan EPU measurement

**World Uncertainty Index for Taiwan**
- **Source**: FRED (Federal Reserve Economic Data)
- **Coverage**: Q1 1956 to Q2 2025
- **Relevance to Taiwan**: Long historical series for Taiwan uncertainty

**EPU Spillover Effects on Asia**
- Panel VAR study on international EPU spillovers across business cycles using OECD countries data
- **Finding**: Unexpected elevations of EPU from abroad have contractionary real effects
- **Heterogeneity**: Spillover effects depend on business cycle state of recipient country
- **Relevance to Taiwan**: Taiwan's business cycle state may condition response to foreign uncertainty

**Chinese EPU and Asian Stock Markets**
- Recent studies examine predictive power of Chinese EPU for individual stock returns in major Asian markets: Taiwan, Japan, Hong Kong, India, South Korea
- **Finding**: Chinese policy uncertainty has significant predictive power for Asian markets
- **Relevance to Taiwan**: TAIEX response to Chinese uncertainty is empirically documented

**Comparable Small Open Economy Studies**

**South Korea:**
- Structural Bayesian VAR analysis of domestic and foreign uncertainty shocks (Cheng, 2017)
- Includes real effective exchange rate as key transmission mechanism
- FAVAR analysis with 35 economic indicators
- **Similarity to Taiwan**: Export-oriented, US-dependent, exposed to China

**Singapore:**
- Factor-augmented VAR analysis of monetary policy and asset prices
- Small open economy framework
- **Similarity to Taiwan**: Trade-dependent, financial center characteristics

**1997-98 Asian Financial Crisis Context**
- Thailand, Indonesia, South Korea most affected by crisis
- **Taiwan less affected but suffered from regional loss of demand and confidence**
- Currency devaluations accompanied by declining stock markets due to financial crisis and policy uncertainty
- **Lessons**: Uncertainty about future economic policies prolongs recovery; structural reforms needed to reduce uncertainty
- **Relevance to Taiwan**: Historical episode demonstrating vulnerability to regional uncertainty contagion despite relatively strong fundamentals

### 4.2 US-China Relations & Geopolitical Risk

**Taiwan's Strategic Position in US-China Economic Rivalry**
- Technology takes center stage in US-China rivalry
- Taiwan's strategic importance rises due to semiconductor dominance
- Taiwan became US 7th largest trading partner by 2024 (7.1% annual trade growth)
- **Vulnerability**: Taiwan and South Korea especially vulnerable given quantities of electronics they export to China

**US-China Trade War Impact on Taiwan**

**Direct Trade Effects:**
- Taiwanese firms' revenue and profitability in China declined after 2012 (Xi's policies)
- US-China trade war (2018 onward) reduced China's export dependence on US, disrupting Taiwanese firm operations
- Taiwan-US trade deficit has grown significantly

**Business Uncertainty and Adaptation:**
- China's military assertiveness and rising defense spending heightened uncertainty
- Taiwanese businesses reconsidering reliance on Chinese market
- Many firms exploring alternative production sites in Southeast Asia or repatriating to Taiwan
- **Strategic response**: Diversify supply chains toward Southeast Asia, US, domestic reinvestment
- Global companies delaying/pausing investment due to rising uncertainty

**Geopolitical Risk Effects:**
- Increased geopolitical risk reduces cross-border investment activities
- Information asymmetry between domestic and international investors during high geopolitical risk
- Capital flow volatility increases
- **Taiwan Strait tensions**: Unique geopolitical risk factor not faced by other small open economies

**Ongoing Structural Tensions:**
- Fundamental structural differences between US and China remain unresolved
- No thaw in sight: US-China trade war likely to persist beyond 2025
- Businesses and capital markets should brace for continued uncertainty and fluctuations
- **Policy implication**: Taiwan faces persistent external uncertainty requiring robust policy frameworks

**Trade War Uncertainty Transmission Mechanisms:**
- **Tariffs and counter-tariffs**: Direct cost increases and supply chain disruptions
- **Sanctions**: Technology restrictions affecting semiconductor industry
- **Investment uncertainty**: Delayed FDI decisions due to unclear future trade environment
- **Supply chain restructuring**: Costs and uncertainty of relocating production

**Taiwan's Dual Exposure:**
- Economic dependence on both US (technology, defense) and China (trade, investment)
- **Caught in crossfire**: Cannot easily decouple from either economy
- Makes Taiwan particularly sensitive to US-China uncertainty shocks
- **Research gap**: Limited empirical analysis of Taiwan's dual exposure using modern uncertainty measurement techniques

---

## Key Gaps and Opportunities for Taiwan Research

### 1. Methodological Gaps

**Order-Invariance in Uncertainty Research**
- Chan, Koop, Yu (2024) developed order-invariant BVAR-SV methodology
- Davidson, Hou, Koop (2025) apply this to macro vs. financial uncertainty decomposition
- **GAP**: No application to small open economies, especially those with dual exposure to major powers
- **OPPORTUNITY**: Taiwan is ideal test case for order-invariant SVMVAR in small open economy context

**Large vs. Small Models**
- DHK (2025) demonstrate 30-variable models produce biased results; 40+ variables needed
- Most small open economy studies use ~10-20 variables
- **GAP**: No large-scale (40+ variable) uncertainty decomposition for any Asian small open economy
- **OPPORTUNITY**: Taiwan research addresses omitted variables bias highlighted in DHK (2025)

### 2. Substantive Gaps in Taiwan Literature

**Macro vs. Financial Uncertainty Decomposition**
- Brianti (2025), Caldara et al. (2016) show macro and financial uncertainty have different effects and require different policy responses
- Sin (2015) studies China EPU impact on Taiwan but does NOT decompose uncertainty types
- **GAP**: No study decomposes Taiwan uncertainty into macro vs. financial components
- **OPPORTUNITY**: Critical for Central Bank of China (Taiwan) policy guidance

**Time-Varying Classification of Ambiguous Variables**
- DHK (2025) allow exchange rates, policy rates to shift between macro/financial classification over time
- **GAP**: No study examines whether TWD/USD, TAIEX, Taiwan policy rates behave as macro or financial variables across different periods
- **OPPORTUNITY**: Understanding classification shifts could explain Taiwan's vulnerability during different crisis types (1997 Asian crisis vs. 2008 global financial crisis vs. 2018 trade war)

**Dual Exposure to US and China**
- Extensive literature on US uncertainty spillovers to EMs
- Growing literature on China uncertainty spillovers to Asia
- **GAP**: No study examines economy simultaneously exposed to BOTH US and China uncertainty with quantitative decomposition
- **OPPORTUNITY**: Taiwan's "caught in crossfire" position makes it uniquely suited to study dual uncertainty transmission
- **Policy relevance**: Taiwan cannot decouple from either economy; needs framework for managing dual exposure

### 3. Geopolitical Risk Integration

**Taiwan Strait Tensions as Unique Uncertainty Source**
- Geopolitical risk literature focuses on oil-producing regions, trade wars, Brexit
- **GAP**: Taiwan Strait military tensions as economic uncertainty source understudied
- **OPPORTUNITY**: Include geopolitical risk indicators specific to Taiwan Strait; test whether these should be classified as macro or financial shocks

**Supply Chain Restructuring Uncertainty**
- US-China decoupling forcing supply chain restructuring
- Taiwan semiconductor industry at center of tech competition
- **GAP**: Uncertainty from forced supply chain restructuring not well-modeled in VAR frameworks
- **OPPORTUNITY**: Include indicators of supply chain stress (export order volatility, FDI policy uncertainty)

### 4. Policy-Relevant Questions Unanswered

**Which Uncertainty Type Dominates in Taiwan?**
- Literature shows macro vs. financial uncertainty have different effects
- **GAP**: Unknown whether Taiwan's small open economy is more vulnerable to macro or financial uncertainty
- **POLICY IMPORTANCE**: If macro uncertainty dominates, focus on stabilizing real economy; if financial uncertainty dominates, focus on financial stability

**How Should CBC Respond to Different Uncertainty Types?**
- Brianti (2025): macro uncertainty allows simultaneous output and inflation stabilization; financial shocks require trade-offs
- **GAP**: No guidance for CBC on appropriate policy response to macro vs. financial uncertainty shocks
- **OPPORTUNITY**: Structural analysis of Taiwan VAR can provide impulse responses guiding CBC policy

**Does Exchange Rate Help or Hurt Under Uncertainty?**
- Literature mixed: exchange rate amplifies uncertainty in US, absorbs in other open economies
- **GAP**: Unknown whether TWD/USD flexibility helps or hurts Taiwan under uncertainty
- **POLICY IMPORTANCE**: Informs CBC exchange rate management strategy

### 5. Data and Measurement Opportunities

**Long Time Series for Taiwan**
- Huang, Yeh, Chen (2019) provide Taiwan EPU index
- FRED provides World Uncertainty Index for Taiwan (1956-2025)
- Taiwan statistical agencies provide comprehensive macro data
- **OPPORTUNITY**: Sufficient data history to estimate large VARs and identify structural breaks

**Comparison with Korea and Singapore**
- Korea and Singapore comparable small open economies with good data
- **OPPORTUNITY**: Three-country comparison (Taiwan, Korea, Singapore) could identify common vs. unique uncertainty vulnerabilities

### 6. Publication and Contribution Strategy

**Why This is NOT Just "Country Replication"**

The Taiwan research makes MULTIPLE novel contributions beyond applying DHK (2025) to a new country:

1. **Methodological**: First application of order-invariant SVMVAR to small open economy
2. **Dual exposure**: First quantitative decomposition of dual US-China uncertainty exposure
3. **Geopolitical risk**: Integration of Taiwan-specific geopolitical uncertainty
4. **Policy puzzle**: Solves real CBC policy question (macro vs. financial uncertainty)
5. **Validation**: Tests whether DHK (2025) findings (model size matters, order-invariance matters) hold in small open economy context
6. **Regional significance**: Taiwan's semiconductor dominance makes its uncertainty dynamics globally relevant

**Target Journals:**
- Journal of Applied Econometrics (methodological innovation + policy application)
- Journal of International Economics (international uncertainty transmission)
- Pacific Economic Review (regional focus, policy relevance)
- Journal of Economic Dynamics and Control (DSGE/VAR methodology)

---

## Summary: How This Literature Supports Taiwan Research Motivation

### Strong Methodological Foundation
- Order-invariant BVAR-SV methods are cutting-edge (Chan, Koop, Yu 2024; DHK 2025)
- Large model necessity is established (DHK 2025; Banbura et al. 2010)
- Macro vs. financial decomposition is theoretically and empirically justified (Brianti 2025; Caldara et al. 2016)

### Established Policy Relevance
- Different uncertainty types require different policy responses (Brianti 2025)
- Small open economies vulnerable to global uncertainty (extensive spillover literature)
- Monetary policy effectiveness depends on uncertainty type (Caggiano et al. 2021)

### Clear Research Gap
- No large-scale uncertainty decomposition for Taiwan
- Dual US-China exposure not quantitatively modeled
- Taiwan "caught in crossfire" position unique and policy-relevant

### Timely and Important
- US-China tensions show no signs of abating (persisting beyond 2025)
- Taiwan semiconductor industry at center of tech competition
- CBC needs guidance on managing external uncertainty shocks

**CONCLUSION**: The Taiwan research is well-motivated by existing literature, addresses clear gaps, and makes multiple novel contributions using state-of-the-art methodology to solve a real policy problem.

---

## Bibliography

### Core Methodological Papers

Baker, S. R., Bloom, N., & Davis, S. J. (2016). Measuring Economic Policy Uncertainty. *Quarterly Journal of Economics*, 131(4), 1593-1636.

Banbura, M., Giannone, D., & Reichlin, L. (2010). Large Bayesian VARs. *Journal of Applied Econometrics*, 25(1), 71-92.

Brianti, M. (2025). Financial Shocks, Uncertainty Shocks, and Corporate Liquidity. *Journal of Applied Econometrics*.

Caggiano, G., Castelnuovo, E., & Figueres, J. M. (2021). Financial Uncertainty and Real Activity: The Good, the Bad, and the Ugly. *European Economic Review*, 136, 103772.

Caldara, D., Fuentes-Albero, C., Gilchrist, S., & Zakrajšek, E. (2016). The Macroeconomic Impact of Financial and Uncertainty Shocks. *European Economic Review*, 88, 185-207.

Carriero, A., Clark, T. E., & Marcellino, M. (2018). Measuring Uncertainty and Its Impact on the Economy. *Review of Economics and Statistics*, 100(5), 799-815.

Carriero, A., Clark, T. E., & Marcellino, M. (2019). Large Bayesian Vector Autoregressions with Stochastic Volatility and Non-Conjugate Priors. *Journal of Econometrics*, 212(1), 137-154.

Chan, J. C., Koop, G., & Yu, X. (2024). Large Order-Invariant Bayesian VARs with Stochastic Volatility. *Journal of Business & Economic Statistics*, 42(2), 825-837.

Davidson, J., Hou, K., & Koop, G. (2025). Investigating Economic Uncertainty Using Stochastic Volatility in Mean VARs: The Importance of Model Size, Order-Invariance and Classification. [Working Paper]

Jurado, K., Ludvigson, S. C., & Ng, S. (2015). Measuring Uncertainty. *American Economic Review*, 105(3), 1177-1216.

### Small Open Economy and Spillover Papers

Galí, J., & Monacelli, T. (2005). Monetary Policy and Exchange Rate Volatility in a Small Open Economy. *Review of Economic Studies*, 72(3), 707-734.

### Taiwan and Asia-Pacific Papers

Huang, Y.-L., Yeh, C.-C., & Chen, M.-C. (2019). An Economic Policy Uncertainty Index for Taiwan. *Taiwan Economic Review*, 49(2). [Abstract in English available]

Sin, C.-Y. (2015). The Economic Fundamental and Economic Policy Uncertainty of Mainland China and Their Impacts on Taiwan and Hong Kong. *The North American Journal of Economics and Finance*, 40, 298-311.

### Data Sources

Baker, Bloom, Davis Economic Policy Uncertainty Index: www.PolicyUncertainty.com

Federal Reserve Economic Data (FRED): World Uncertainty Index for Taiwan, JLN Uncertainty Indexes

Sydney Ludvigson Macro and Financial Uncertainty Indexes: www.sydneyludvigson.com

---

*Literature search completed: 2025-11-14*

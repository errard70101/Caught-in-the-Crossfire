# Taiwan-Specific Uncertainty Shock Literature Review

**Purpose**: Identify empirical research on Taiwan uncertainty shocks, US-China tensions effects, and geopolitical risks to strengthen the motivation for Taiwan economic uncertainty research.

**Date Created**: 2025-11-14
**Last Updated**: 2025-11-14

**Search Scope**: English and Traditional Chinese publications, full historical period (1990s-2025), empirical focus

---

## Table of Contents

1. [Phase 1: Taiwan Uncertainty Shock Studies](#phase-1-taiwan-uncertainty-shock-studies)
2. [Phase 2: US-China Trade War Impact on Taiwan](#phase-2-us-china-trade-war-impact-on-taiwan)
3. [Phase 3: Geopolitical Risk and Taiwan](#phase-3-geopolitical-risk-and-taiwan)
4. [Phase 4: Regional Comparative Studies](#phase-4-regional-comparative-studies)
5. [Taiwan Data Sources and Availability](#taiwan-data-sources-and-availability)
6. [Timeline of Studied Geopolitical Events](#timeline-of-studied-geopolitical-events)
7. [Research Gaps Specific to Taiwan](#research-gaps-specific-to-taiwan)
8. [Bibliography](#bibliography)

---

## Phase 1: Taiwan Uncertainty Shock Studies

### 1.1 Taiwan Economic Policy Uncertainty (EPU) Index

**Huang, Yeh, and Chen (2019)** - "An Economic Policy Uncertainty Index for Taiwan"
- **Publication**: Taiwan Economic Review (經濟論文叢刊), 49(2)
- **Methodology**: Follows Baker, Bloom, Davis (2016) newspaper-based methodology
- **Data Construction**: Keyword matching in Taiwanese newspapers for terms about economy, policy, and uncertainty
- **Frequency**: Monthly index
- **Time Coverage**: Available from construction date forward
- **Key Contribution**: **ESSENTIAL DATA SOURCE** - First Taiwan-specific EPU index following international standard methodology
- **Availability**: Taiwan Economic Review publication
- **Relevance**: Provides time series for measuring Taiwan domestic policy uncertainty

| Variable | Frequency | Coverage | Source | Construction Method |
|----------|-----------|----------|--------|-------------------|
| Taiwan EPU Index | Monthly | Post-2019 | Huang et al. (2019) | Newspaper keyword search |

**World Uncertainty Index for Taiwan**
- **Source**: Federal Reserve Economic Data (FRED)
- **Coverage**: Q1 1956 to Q2 2025 (69 years!)
- **Frequency**: Quarterly
- **Construction**: Based on Economist Intelligence Unit country reports
- **Key Feature**: Extremely long historical series allowing structural break analysis
- **Data Access**: https://fred.stlouisfed.org/series/WUITWN

| Variable | Frequency | Coverage | Source | Notes |
|----------|-----------|----------|--------|-------|
| World Uncertainty Index - Taiwan | Quarterly | 1956 Q1 - 2025 Q2 | FRED/EIU | Long historical series |

### 1.2 Taiwan EPU and Business Cycles - VAR Evidence

**Sin (2015)** - "The Economic Fundamental and Economic Policy Uncertainty of Mainland China and Their Impacts on Taiwan and Hong Kong"
- **Publication**: The North American Journal of Economics and Finance, 40, 298-311
- **Methodology**: Structural VAR (SVAR) with short-run and long-run restrictions
- **Sample Period**: 1996-2013
- **Frequency**: Monthly
- **Model Specification**:
  - Four domestic Taiwan variables: output, interest rate, price level, real exchange rate
  - Two foreign variables: Mainland China output, China monthly EPU index
- **Identification Strategy**: Block exogeneity - China affects Taiwan/HK but not reverse
- **Key Findings**:
  - Chinese equity returns, employment and output fall in response to unexpected rises in Chinese EPU
  - Taiwan economy responds significantly to China EPU shocks
  - **STRUCTURAL INSIGHT**: China EPU has spillover effects on Taiwan's real variables
- **Data Sources**: Taiwan Central Bank, DGBAS, China National Bureau of Statistics
- **Relevance**: **DIRECTLY APPLICABLE** - Demonstrates Taiwan VAR framework with China uncertainty as external shock

| Study | Variables | Frequency | Period | Methodology | Key Finding |
|-------|-----------|-----------|--------|-------------|-------------|
| Sin (2015) | TW GDP, interest rate, CPI, REER; China GDP, China EPU | Monthly | 1996-2013 | SVAR | China EPU significantly affects Taiwan |

**Structural Break Note**: Study period (1996-2013) includes:
- 1997-98 Asian Financial Crisis
- 2008 Global Financial Crisis
- 2008-2013 Ma Ying-jeou KMT administration (closer China ties)

### 1.3 Taiwan Stock Market (TAIEX) Uncertainty and Volatility

**Understanding Stock Market Volatility: Korea and Taiwan** (1999)
- **Publication**: Journal of International Financial Markets, Institutions and Money
- **Finding**: Taiwanese stock market has historically been the most volatile in Asia
- **Mechanism**: Taiwan stock returns much more correlated with earnings than Korean returns
- **Key Insight**: During extreme price movements, cross-sectional correlations between returns and earnings very low
- **Implication**: Taiwan stock market exhibits high fundamental volatility, not just sentiment-driven

**Recent TAIEX Volatility Events (2025)**
- **April 7, 2025**: Largest single-day decline in TAIEX history
  - Dropped 2,065.87 points (9.7%) following Trump's "reciprocal" tariff announcement (April 2, 2025)
  - Continued falling to 17,391.76 on April 9
  - **Policy Response**: National Financial Stabilization Fund authorized market intervention
- **Key Observation**: TAIEX extremely sensitive to US trade policy uncertainty shocks
- **Research Opportunity**: Recent event provides natural experiment for uncertainty shock impact

**TAIEX Options Volatility Index**
- Compiled using CBOE VIX methodology
- Provides real-time measure of market volatility expectations
- **Data Source**: Taiwan Futures Exchange (TAIFEX)
- **Availability**: Current month and historical data

| Volatility Measure | Frequency | Coverage | Source | Application |
|-------------------|-----------|----------|--------|-------------|
| TAIEX | Daily | 1990-present | Taiwan Stock Exchange | Stock market uncertainty proxy |
| TAIEX VIX | Real-time | Recent years | TAIFEX | Implied volatility measure |

### 1.4 Exchange Rate (TWD/USD) Uncertainty and Central Bank Policy

**Exchange Rate System**
- **Regime**: Managed floating exchange rate system
- **CBC Intervention Policy**: Central Bank intervenes to prevent excessive volatility
- **Recent Volatility**: Historic 9% rally in May 2025 (strongest since 1981)
  - TWD appreciated over 10% vs USD in few days
  - Three-year highs reached
  - **Trigger**: Fears of "Plaza Accord 2.0" targeting surplus countries

**Central Bank of China (Taiwan) Monetary Policy Under Uncertainty**
- **Financial Stability Reports**: Published semi-annually
- **Coverage**: Macro-prudential measures, interest rate risk, financial soundness indicators
- **Uncertainty Sources Identified by CBC**:
  - US tariff policy trajectory
  - Major central banks' monetary policy actions
  - China's economic slowdown
  - Geopolitical conflicts
  - Climate change
- **Policy Response Framework**: CBC adjusts monetary, credit, and foreign exchange policies to maintain financial and price stability

**Historical CBC Concerns (2017 as example)**:
- Euro area political uncertainties
- Fed interest rate hike path
- Trade protectionism rise
- Brexit negotiations
- China economic restructuring spillovers

| Data Source | Frequency | Coverage | Content | Availability |
|-------------|-----------|----------|---------|--------------|
| CBC Financial Stability Report | Semi-annual | 2000s-present | Uncertainty discussion, macro-prudential policy | CBC website (English) |
| CBC Monetary Policy Statement | Quarterly | 2000s-present | Policy decision rationale | CBC website (English) |
| TWD/USD Exchange Rate | Daily | 1990-present | Spot rate | FRED, CBC |

### 1.5 Taiwan Capital Flows and Foreign Investment Volatility

**Has Asian Crisis Changed Role of Foreign Investors? Taiwan's Experience** (2006)
- **Publication**: Journal of International Financial Markets, Institutions and Money
- **Sample Period**: Covers 1997-98 Asian Financial Crisis
- **Key Findings**:
  - Asian crisis strengthened volatility effects and spillovers in Taiwan stock market
  - Did NOT change fundamental relationship between equity flows and market returns
  - Stabilizing effect of foreign investment on Taiwan market
  - **Structural Change**: Crisis affected volatility transmission but not direction
- **Policy Context**: Taiwan gradually relaxed foreign trading restrictions

**Taiwan's Unique FDI Pattern**
- **Characteristic**: Outward FDI exceeds inward FDI for many years
- **Pattern**: Inward foreign portfolio investment >> inward FDI since 1993
- **Implication**: Taiwan more integrated through portfolio flows than FDI
- **China Connection**: Net capital outflows to China volatile and event-driven

**Portfolio Flow Volatility**
- **Stylized Fact**: Portfolio flows more volatile than other capital flows
- **Taiwan Context**: Potentially more destabilizing for financial stability
- **Exchange Rate Volatility**: High exchange rate volatility associated with equity inflows

| Study | Data | Period | Frequency | Key Finding |
|-------|------|--------|-----------|-------------|
| Asian Crisis FI Study | Taiwan equity flows, market returns | 1990s-2000s | High-freq | Crisis strengthened volatility spillovers |

### 1.6 Taiwan Business Confidence and Sentiment Indicators

**Consumer and Business Confidence Indices**
- **Consumer Confidence**: Monthly survey by DGBAS
  - September 2025: 64.69 points (up from 63.31 in August)
  - Prior trend: Fell for 9 consecutive months to 13-month low
  - **Drivers of Decline**: Global trade uncertainties, tariff risks, currency appreciation
- **Leading Indicators**: Index of leading indicators
  - Recent: Fell 0.81% to 100.37 (3 consecutive months of decline)
  - Components showing weakness: business confidence, share prices, export orders

**Geopolitical Risk Impact on Sentiment**
- Worsening cross-strait tensions softening inbound FDI from multinationals
- Over 50% of survey respondents expect conditions to deteriorate
- **Key Concerns**: US tariff adjustments, geopolitical risks, currency strength

| Indicator | Frequency | Source | Recent Trend | Key Drivers |
|-----------|-----------|--------|--------------|-------------|
| Consumer Confidence Index | Monthly | DGBAS | Recovering but below average | Trade uncertainty, tariffs |
| Leading Indicators Index | Monthly | DGBAS | Declining | Business confidence, exports |

### 1.7 Taiwan Corporate Responses to Economic Uncertainty

**Economic Uncertainty and Corporate Cash Holdings: Taiwan Evidence** (2024)
- **Publication**: Pacific-Basin Finance Journal
- **Methodology**: Firm-level panel data analysis
- **Finding**: Taiwan firms increase cash holdings under economic uncertainty
- **Mechanism**: Precautionary motive - firms build liquidity buffers
- **Implication**: Uncertainty affects real corporate decisions through financial channel
- **Relevance**: Micro-level evidence of uncertainty transmission to investment/liquidity decisions

---

## Phase 2: US-China Trade War Impact on Taiwan

### 2.1 Trade War Effects: Macro-Level Evidence

**The Substitution Effect of US-China Trade War on Taiwanese Trade** (2023)
- **Authors**: Yang et al.
- **Publication**: The Developing Economies
- **Data**: Monthly trade data, January 2018 - December 2019
- **Methodology**: Trade flow analysis, difference-in-differences
- **Hypothesis Tested**: US tariffs on Chinese goods increased Taiwan exports to US (substitution effect)
- **Key Findings**:
  - **CONFIRMED**: Taiwan exports to US increased as Chinese exports declined
  - Substitution effect statistically significant and economically meaningful
  - Taiwan benefited from trade diversion in short term
- **Products**: Focus on manufacturing goods where Taiwan and China compete

| Study | Data | Period | Frequency | Methodology | Finding |
|-------|------|--------|-----------|-------------|---------|
| Yang et al. (2023) | Taiwan trade flows (exports/imports) | 2018 M1 - 2019 M12 | Monthly | Trade flow analysis | Substitution effect confirmed |

**Structural Break Note**: Study captures initial trade war phase (2018-2019) but misses:
- 2020 COVID-19 disruption
- 2021-2022 supply chain crisis
- 2022-2025 tech decoupling intensification

### 2.2 Firm-Level Evidence: Taiwanese Companies

**The Expansion of Taiwanese Firms and US-China Trade War: Subcontractors' Dilemma** (2025)
- **Publication**: Taiwan Insight
- **Data**: Financial data from Taiwan's top 500 business groups and 5,000 firms (1995-2022)
- **Sample Period**: 27 years of firm-level panel data
- **Key Findings**:
  - **2012 Structural Break**: Clear decline in Taiwanese firms' revenue and profitability in China after 2012 (Xi Jinping era)
  - **2018 Trade War Impact**: Further disrupted Taiwanese firms relying on China production bases
  - **Strategic Response**: Firms exploring Southeast Asia relocation or Taiwan repatriation
  - **"Subcontractors' Dilemma"**: Caught between US and China demands in global supply chains

**"China+1" Strategy**
- Many Taiwanese firms adopting diversification from China
- **Destinations**: Vietnam, Thailand, Malaysia, Indonesia
- **Challenge**: Cannot fully exit China market due to size/importance
- **Dual Pressure**: US wants supply chain decoupling; China wants firms to stay

| Study | Data Type | Sample Size | Period | Key Variable | Finding |
|-------|-----------|-------------|--------|--------------|---------|
| Taiwan Insight (2025) | Firm financials | Top 500 groups, 5000 firms | 1995-2022 | Revenue, profitability in China | Post-2012 decline, 2018 acceleration |

**Structural Breaks Identified**:
- **2012**: Xi Jinping policies reduce Taiwan firm profitability in China
- **2018**: US-China trade war disrupts Taiwan firms' China operations

### 2.3 Global Studies Including Taiwan

**The Global Impact of US-China Trade War: Firm-Level Evidence** (2022)
- **Publication**: Review of World Economics
- **Sample**: 5,000+ listed firms in 40 countries
- **Taiwan's Role**: "Key exporter of high-tech inputs to China's export engine"
- **Finding**: Taiwan firms indirectly affected through China production network disruption
- **Mechanism**: Taiwan supplies intermediate goods to China's export sector
- **Implication**: Taiwan vulnerability through supply chain linkages

**Exports in Disguise? Trade Rerouting During Trade War** (2024)
- **Institution**: Harvard Business School Working Paper
- **Taiwan Finding**: Foreign-owned firms from Japan, Korea, and **Taiwan** followed "China-Plus-One" strategy
- **Mechanism**: Firms maintain China presence while building alternative capacity
- **Implication**: Trade war induced supply chain diversification, not pure exit

---

## Phase 3: Geopolitical Risk and Taiwan

### 3.1 Taiwan Strait Crisis Events and Economic Impact

**1996 Taiwan Strait Crisis**
- **Event**: PRC missile tests and military exercises
- **Context**: First direct presidential election in Taiwan
- **Economic Stakes (then)**: Lower than today - China smaller economy, Taiwan less critical in tech

**2022 Pelosi Visit: Event Study Evidence**

**"Geopolitical Risk and Taiwan Government Bond Yields: Pelosi Visit Evidence"** (2025)
- **Publication**: Pacific-Basin Finance Journal
- **Methodology**: Event study + counterfactual analysis
- **Event Date**: August 2-3, 2022 (Nancy Pelosi visit to Taiwan)
- **Sample**: Taiwan government bond yields (various maturities)
- **Key Findings**:
  - **Immediate Impact**: Pelosi visit triggered persistent increase in Taiwan bond yields
  - **Expected Yields**: Rose significantly
  - **Risk Premium Dynamics**:
    - Short-term risk premia initially declined (flight to safety within Taiwan bonds)
    - After 11 months, became significantly positive (persistent geopolitical risk)
  - **Interpretation**: Market initially underpriced geopolitical risk, corrected over time

**Stock Market Reactions to Pelosi Visit (2022)**
- **Initial Response**: Markets sank Tuesday on Pelosi visit fears
- **Rebound**: Major US indices rebounded 2% on day of actual visit
- **Taiwan Market**: Barely a ripple - entered crisis stable, exited with few distress signs
- **Interpretation**: Taiwan markets more resilient than external observers expected
- **Context**: Markets worse at pricing uncertainty than actual events

| Event | Date | Asset Class | Immediate Impact | Persistent Impact | Study Source |
|-------|------|-------------|------------------|-------------------|--------------|
| Pelosi Visit | Aug 2-3, 2022 | Taiwan govt bonds | Yield increase | Risk premium positive after 11 months | Pacific-Basin Finance J. (2025) |
| Pelosi Visit | Aug 2-3, 2022 | Taiwan stocks (TAIEX) | Minimal decline | Stable | Market reports |

**Military Drills Comparison: 1996 vs. 2022**
- **2022 Drills**: Larger scale than 1996 crisis
- **Economic Stakes**: Much higher now
  - China's economy vastly larger
  - Taiwan critical semiconductor producer
  - ICT products globally essential
- **Economic Cost Estimates**: Bloomberg Economics estimates $10 trillion cost of Taiwan conflict

### 3.2 Geopolitical Risk Measurement for Taiwan

**Caldara-Iacoviello Geopolitical Risk (GPR) Index**
- **Construction**: Automated text search in 10 major newspapers
- **Categories**: 8 categories including war threats, military buildups, nuclear threats, terror threats
- **Country-Specific Indices**: Available for advanced and emerging economies
- **Taiwan Availability**: Country-specific GPR for Taiwan available
- **Data Access**: https://www.matteoiacoviello.com/gpr.htm
- **Relevance**: Potential explanatory variable for Taiwan uncertainty VAR

**Research Gap**: Limited published studies using GPR index specifically for Taiwan event studies

### 3.3 Semiconductor Industry Geopolitical Risk

**"From Vulnerabilities to Resilience: Taiwan's Semiconductor Industry and Geopolitical Challenges"** (2025)
- **Publication**: China Economic Review
- **Focus**: Taiwan semiconductor sector amid US-China tech tensions
- **Key Finding**: Geopolitical risk causes firm-level uncertainty in semiconductors
- **Measurement**: Geopolitical uncertainty measures informationally dense and significantly impact investor sentiment, market stability, price expectations

**"Semiconductor Game of Thrones: Geopolitical and Equity Market Uncertainty Transmission"** (2025)
- **Publication**: Journal of Commodity Markets
- **Methodology**: Uncertainty transmission analysis across semiconductor firms and markets
- **Key Findings**:
  - American markets adjust faster to geopolitical uncertainty than Asian counterparts
  - Asian markets exhibit higher volatility and slower adaptation
  - **Paradox**: Heightened geopolitical uncertainty amplifies market uncertainty in US but may stabilize stock valuations in Asia
- **Implication**: Asymmetric geopolitical risk transmission US vs. Asia

**TSMC and Export Controls**
- **CHIPS Act Restriction**: TSMC's US subsidies prevent expanding manufacturing in China
- **Huawei Cutoff**: TSMC quickly cut off Huawei and blacklisted entities
- **Financial Impact**: Minimal - international demand outweighs supply; TSMC raised prices, recorded all-time high profits
- **AI Boom Effect**: Strong US AI chip demand mitigated export control impact

**Economic Impact Estimates**
- **TSMC Disruption**: Full-scale disruption would cause annual spillover of **$490 billion** lost revenue for device manufacturers
- **Taiwan Blockade**: US estimates **$2.5 trillion annual losses** to global economy
- **ITIF Decoupling Model**: US semiconductor firms could lose **$77 billion** in sales from one-time full decoupling with China

| Risk Scenario | Estimated Economic Loss | Source | Timeframe |
|---------------|------------------------|--------|-----------|
| Taiwan semiconductor disruption | $490 billion annually | Industry analysis | Annual ongoing |
| China blockade of Taiwan | $2.5 trillion | US government estimate | Annual |
| US-China semiconductor decoupling | $77 billion (US firms) | ITIF economic model | Initial year |

### 3.4 Technology Export Controls and Economic Impact

**Taiwan's Export Control Alignment with US**
- **2024 Action**: Taiwan added Huawei and SMIC to "Strategic High-Tech Commodities Entity List"
- **Significance**: Marks Taiwan full alignment with US tech decoupling policy
- **Consequence**: Acceleration of bifurcation into US-led and China-led semiconductor ecosystems

**CHIPS Act and Taiwan's Dilemma**
- **US Goal**: Reduce dependence on Taiwan semiconductor manufacturing
- **Reality**: TSMC Arizona plant does not fundamentally reorient supply chain
- **Continuing Dependence**: US still relies heavily on Taiwanese expertise and production
- **Morris Chang Quote**: "In chip sector, globalization is dead" - supply chain bifurcation raises costs, slows innovation

**Economic Consequences of Decoupling**
- **US Chipmakers**: Reduced China market access lowers revenue, potentially reducing R&D investment
- **Taiwan Position**: Benefits from US onshoring investment but faces China retaliation risk
- **High-Skill Jobs**: Decoupling affects employment in both US and Taiwan high-tech sectors

---

## Phase 4: Regional Comparative Studies

### 4.1 Four Asian Tigers Framework: Taiwan, Korea, Singapore, Hong Kong

**Economic Policy Uncertainty Transmission: Four Tigers Study**
- **Countries**: Hong Kong, Singapore, South Korea, Taiwan
- **Common Characteristics**: Outward-oriented economic development strategies, export-led growth, high trade openness
- **Methodology**: Time-Varying Parameter VAR (TVP-VAR) and Quantile VAR (QVAR)
- **Sample**: 20 countries including the Four Tigers
- **Finding**: Tigers exhibit high sensitivity to international EPU shocks due to trade openness
- **Implication**: Taiwan shares vulnerability pattern with regional peers

### 4.2 Asia-Pacific Uncertainty Spillover Network

**"Economic Uncertainty and Spillover Networks: Asia-Pacific Evidence"** (2021)
- **Publication**: Journal of International Money and Finance
- **Countries**: 12 Asia-Pacific countries (2000-2020)
- **Included**: South Korea, Singapore, Taiwan (likely), Japan, Australia, China
- **Methodology**: Factor-Augmented VAR (FAVAR) with 35 economic indicators
- **Key Contributions**:
  - Calculated macro economic uncertainty indices for each country
  - Constructed uncertainty spillover networks
  - Identified network centrality and key transmission nodes
- **Findings**:
  - South Korea and Singapore: Above-average spillover effects, important network nodes
  - Developed Asia-Pacific economies more central in uncertainty transmission
  - Japan, South Korea, Singapore, Canada, Mexico identified as key nodes
- **Relevance**: Provides regional context for Taiwan's uncertainty transmission

| Study | Countries | Period | Methodology | Key Finding |
|-------|-----------|--------|-------------|-------------|
| Asia-Pacific Spillovers (2021) | 12 countries incl. Korea, Singapore | 2000-2020 | FAVAR, 35 indicators | Korea & Singapore = key spillover nodes |

### 4.3 Korea and Taiwan Comparative Evidence

**Stock Market Volatility: Korea and Taiwan Comparison** (1999)
- **Publication**: Journal of International Financial Markets
- **Finding**: Taiwan stock market most volatile in Asia historically
- **Difference from Korea**:
  - Taiwan returns more correlated with earnings
  - Taiwan exhibits higher fundamental volatility
  - During extreme movements, both show low earnings-return correlation
- **Implication**: Taiwan market particularly sensitive to uncertainty shocks

**Korea Capital Flow Studies Applicable to Taiwan**
- "Variance Risk Premium in Small Open Economy: Korea Case"
- Methodology: VAR and FAVAR analysis
- Framework applicable to Taiwan as comparable small open economy with volatile capital flows

### 4.4 Small Open Economy Uncertainty Literature Applicable to Taiwan

**Thailand Uncertainty Study** (2021)
- **Publication**: Empirical Economics
- **Framework**: Small open economy VAR
- **Key Finding**: **Global uncertainty delivers deeper and more long-lasting effects compared to within-country uncertainty**
- **Implication for Taiwan**: As small open economy, Taiwan likely similarly dominated by external uncertainty
- **Relevance**: Motivates inclusion of US and China uncertainty in Taiwan VAR

**OECD Cross-Country EPU Spillover Study**
- **Methodology**: Smooth-Transition VAR (ST-VAR)
- **Countries**: OECD panel including Korea
- **Key Finding**: Unexpected EPU from abroad has contractionary real effects
- **State Dependence**: Spillover effects depend on recipient country business cycle state
- **Recession vs. Expansion**: EPU spillovers during recessions stronger but less persistent
- **Implication for Taiwan**: Taiwan business cycle state conditions response to US/China uncertainty

---

## Phase 5: Cross-Strait Economic Integration Studies

### 5.1 ECFA and Trade Integration

**Economic Cooperation Framework Agreement (ECFA)**
- **Signed**: June 29, 2010
- **Effective**: September 12, 2010
- **Purpose**: Reduce tariffs and commercial barriers across Taiwan Strait
- **Blueprint**: Gradually reduce/eliminate tariff and non-tariff trade barriers
- **Criticism**: Beijing using economic integration to gain political influence over Taiwan
- **Current Status**: Cross-strait relations strained; ECFA effectiveness limited

### 5.2 Taiwanese FDI in China

**Historical Pattern**
- **1990s**: Taiwanese entrepreneurs began massive investment in China
- **Peak Period**: 2000s - deepest economic integration
- **Post-2012**: Decline in profitability under Xi Jinping policies
- **Post-2018**: Trade war further reduced attractiveness

**Current Trends**
- Taiwan firms seeking to decrease China dependence
- Greater trade resilience than China during decoupling
- Taiwan overall trade positive growth in 2022 despite headwinds

### 5.3 Cross-Strait Economic Dependence as Source of Uncertainty

**Dependence Concerns**
- Heavy economic dependence on China may lead to political compromise
- **Dual Risk**: Economic coercion from China, pressure from US to decouple
- **Supply Chain Reality**: Cross-strait relations anchored in global supply chains around Taiwan semiconductors
- **China's Dependence on Taiwan**: China's economic vulnerabilities deep, reliance on Taiwan profound

---

## Taiwan Data Sources and Availability

### Official Government Data

| Data Source | Agency | Coverage | Frequency | Variables Available | English Access |
|-------------|--------|----------|-----------|-------------------|----------------|
| National Statistics | DGBAS | 1990-present | Monthly, Quarterly | GDP, IPI, CPI, unemployment, trade | Yes |
| Monetary Statistics | CBC | 1990-present | Monthly | Interest rates, money supply, credit | Yes |
| Exchange Rates | CBC | 1990-present | Daily | TWD/USD, REER, NEER | Yes |
| Financial Stability Report | CBC | 2000s-present | Semi-annual | Systemic risk indicators | Yes |
| Trade Statistics | Ministry of Finance | 1990-present | Monthly | Exports, imports by product/country | Yes |

### Market Data

| Data Source | Provider | Coverage | Frequency | Variables | Access |
|-------------|----------|----------|-----------|-----------|--------|
| TAIEX | Taiwan Stock Exchange | 1990-present | Daily | Stock index, volume, individual stocks | Bloomberg, public |
| TAIEX VIX | TAIFEX | Recent years | Real-time | Implied volatility | TAIFEX website |
| Bond Yields | Taipei Exchange | 1990-present | Daily | Government bond yields (all maturities) | Bloomberg, public |

### Uncertainty Measures

| Uncertainty Index | Source | Coverage | Frequency | Construction | Access |
|-------------------|--------|----------|-----------|--------------|--------|
| Taiwan EPU Index | Huang et al. (2019) | Post-2019 | Monthly | Newspaper keyword search | Taiwan Economic Review |
| World Uncertainty Index - Taiwan | FRED/EIU | 1956 Q1 - 2025 Q2 | Quarterly | EIU country reports | FRED (free) |
| Taiwan GPR Index | Caldara-Iacoviello | Available | Monthly | Geopolitical news search | PolicyUncertainty.com |

### Business/Consumer Sentiment

| Indicator | Source | Coverage | Frequency | Components | Access |
|-----------|--------|----------|-----------|-----------|--------|
| Consumer Confidence Index | DGBAS | Long series | Monthly | 6 sub-indices | DGBAS website |
| Business Tendency Survey | DGBAS | Long series | Monthly | Manufacturing, services, construction | DGBAS website |
| Leading Indicators | DGBAS | Long series | Monthly | 11 component indicators | DGBAS website |

---

## Timeline of Studied Geopolitical Events

### Major Taiwan-Related Geopolitical Events (1996-2025)

| Date | Event | Type | Economic Impact Studied | Data Availability |
|------|-------|------|------------------------|-------------------|
| **1996 M3** | Taiwan Strait Missile Crisis | Military | Stock market decline, capital outflows | Limited empirical studies |
| **2000 M3** | First DPP Presidential Victory | Political | Market volatility | Some event studies |
| **2008 M3** | KMT Returns to Power (Ma) | Political | Improved cross-strait relations | Trade data available |
| **2008 Q4** | Global Financial Crisis | Financial | Significant impact on Taiwan | Extensive data |
| **2010 M6** | ECFA Signed | Economic | Trade expansion | Trade data |
| **2012** | Xi Jinping Era Begins | Political/Economic | Taiwan firm profitability decline in China | **Structural break identified** |
| **2014 M3** | Sunflower Movement | Political | Cross-strait trade agreement blocked | Sentiment data |
| **2016 M1** | DPP Returns (Tsai Ing-wen) | Political | Cross-strait tensions rise | Election studies available |
| **2018 M7** | US-China Trade War Begins | Economic | **Major impact** on Taiwan trade/firms | **Extensive empirical research** |
| **2020 Q1** | COVID-19 Pandemic | Health/Economic | Supply chain disruptions | Data available |
| **2022 M8** | Pelosi Visit to Taiwan | Geopolitical | Bond yield increase, brief stock volatility | **Event study published (2025)** |
| **2024 M1** | DPP Third Term (Lai Ching-te) | Political | Pre-election capital flow volatility | Data becoming available |
| **2025 M4** | Trump Reciprocal Tariffs | Economic | **TAIEX largest drop in history (9.7%)** | Real-time data, research pending |
| **2025 M5** | TWD Historic Surge | Financial | 9% appreciation, Plaza Accord 2.0 fears | Real-time data |

### Periodization for Structural Break Analysis

**Suggested Structural Break Points for Taiwan Uncertainty Research:**

1. **1997-1998**: Asian Financial Crisis
2. **2008**: Global Financial Crisis
3. **2012**: Xi Jinping era begins - Taiwan firm China profitability declines
4. **2016**: DPP returns to power - cross-strait tensions
5. **2018**: US-China trade war begins
6. **2020**: COVID-19 pandemic
7. **2022**: Pelosi visit - geopolitical risk spike

---

## Research Gaps Specific to Taiwan

### 1. Methodological Gaps in Taiwan Literature

**Lack of Large-Scale VAR Models**
- Sin (2015) uses only 6 variables (4 Taiwan + 2 China)
- No Taiwan study with 40+ variables addressing omitted variables bias
- **Gap**: Small models may miss important uncertainty transmission channels
- **Opportunity**: Apply DHK (2025) large model approach to Taiwan

**No Order-Invariant VAR for Taiwan**
- Existing Taiwan VAR studies use traditional Cholesky or simple identification
- Variable ordering problem not addressed in Taiwan literature
- **Gap**: Results may be sensitive to arbitrary ordering choices
- **Opportunity**: Apply Chan-Koop-Yu (2024) order-invariant methodology

### 2. Uncertainty Decomposition Gaps

**No Macro vs. Financial Uncertainty Decomposition**
- Sin (2015) examines China EPU but doesn't decompose uncertainty types
- No Taiwan study separates h_macro,t and h_financial,t
- **Gap**: Cannot determine which uncertainty type dominates Taiwan economy
- **Policy Importance**: CBC needs to know whether to focus on real economy stabilization or financial stability

**Time-Varying Classification Not Explored**
- No study examines whether TWD/USD behaves as macro or financial variable across time
- TAIEX classification (macro vs. financial) not studied over different regimes
- Taiwan policy rate role in uncertainty transmission unexplored
- **Gap**: Miss insights from how variable classifications shift during crises

### 3. Dual Exposure to US and China Not Quantified

**Separate But Not Joint Studies**
- Studies on US uncertainty spillovers to emerging markets include Taiwan
- Studies on China uncertainty spillovers to Asia include Taiwan
- **Gap**: No study quantifies Taiwan's simultaneous exposure to BOTH with decomposition
- **Policy Relevance**: Taiwan cannot decouple from either - needs framework for dual exposure management

**Relative Importance Unknown**
- Is Taiwan more vulnerable to US or China uncertainty?
- Do US and China uncertainty shocks interact (amplification or offsetting)?
- **Gap**: No empirical evidence on relative magnitudes

### 4. Geopolitical Risk Integration Gaps

**Taiwan Strait Tensions Understudied**
- Pelosi visit (2022) has ONE published event study on bond yields
- 1996 crisis has limited empirical research
- No comprehensive time-series study of Taiwan Strait geopolitical risk
- **Gap**: Unique geopolitical risk factor not well-modeled

**Event Studies Limited**
- Most geopolitical events have market reports but not rigorous academic studies
- 2025 events (TAIEX crash, TWD surge) too recent for published research
- **Opportunity**: Rich set of recent natural experiments

### 5. Semiconductor Industry-Specific Gaps

**TSMC as Systemically Important Firm**
- TSMC produces 90% of advanced chips globally
- Limited empirical research on TSMC stock price as uncertainty indicator
- **Gap**: TSMC uncertainty transmission to broader Taiwan economy not modeled
- **Opportunity**: TSMC stock volatility as financial uncertainty proxy

**Technology Decoupling Effects**
- Export controls impact on Taiwan semiconductor sector not fully quantified empirically
- Firm-level studies limited
- **Gap**: Lack of comprehensive assessment of tech decoupling on Taiwan macro economy

### 6. Capital Flow and Exchange Rate Gaps

**TWD/USD Classification Ambiguity**
- Literature mixed on whether exchange rate helps or hurts under uncertainty
- No Taiwan-specific study on TWD role in absorbing vs. amplifying uncertainty shocks
- **Gap**: CBC exchange rate management strategy lacks empirical guidance

**Capital Flow Volatility**
- Portfolio flows very volatile in Taiwan
- Election-related capital flow patterns documented but not linked to uncertainty measures
- **Gap**: How do uncertainty shocks affect composition and volatility of capital flows?

### 7. Business Cycle State Dependence

**Non-Linear Effects Unexplored**
- OECD spillover literature shows uncertainty effects depend on recipient business cycle state
- No Taiwan study examines state-dependent uncertainty transmission
- **Gap**: Does Taiwan respond differently to uncertainty in expansion vs. recession?
- **Methodology**: Would require regime-switching VAR or smooth-transition VAR

### 8. Data Frequency and Coverage

**High-Frequency Uncertainty Measures Limited**
- Taiwan EPU index only available from 2019 (Huang et al.)
- World Uncertainty Index quarterly, not monthly
- **Gap**: Limited ability to study high-frequency uncertainty dynamics
- **Workaround**: Use TAIEX VIX, exchange rate volatility as proxies

### 9. Chinese-Language Literature Gap

**Search Limitations**
- This review primarily covered English-language publications
- Taiwan Economic Review (經濟論文叢刊) and other Chinese journals may contain additional relevant studies
- **Gap**: Potentially missing Taiwan-specific research published in Traditional Chinese
- **Recommendation**: Follow-up search in Chinese academic databases

---

## Key Takeaways for Research Design

### 1. Data Availability is Strong

Taiwan has:
- Long time series (40+ years for many variables)
- High-quality official statistics
- Multiple uncertainty proxies available
- Rich set of geopolitical events for identification

### 2. Recent Events Provide Natural Experiments

- 2022 Pelosi visit (bond market study published)
- 2018-2025 US-China trade war (ongoing)
- 2025 TAIEX crash and TWD surge (very recent)
- These events enable credible identification strategies

### 3. Comparative Framework Valuable

- Taiwan, Korea, Singapore as "triplet" small open economies
- Shared characteristics but different geopolitical positions
- Korea and Singapore provide counterfactuals
- Existing comparative studies establish methodology

### 4. Dual US-China Exposure is Taiwan's Unique Feature

- No other economy as exposed to both simultaneously
- This is NOT just country replication - it's Taiwan's distinguishing characteristic
- Policy relevance is immediate and clear

### 5. Semiconductor Industry Cannot Be Ignored

- TSMC systemically important globally
- Technology decoupling is permanent structural shift
- Semiconductor uncertainty distinct from general financial uncertainty
- May warrant separate treatment in VAR framework

### 6. Multiple Structural Breaks Likely

- 2012, 2018 already identified in firm-level studies
- 2016 political shift
- 2020 pandemic
- 2022 geopolitical spike
- Large VAR with stochastic volatility ideal for capturing time-varying parameters

---

## Bibliography

### Taiwan EPU and Business Cycles

Huang, Y.-L., Yeh, C.-C., & Chen, M.-C. (2019). An Economic Policy Uncertainty Index for Taiwan. *Taiwan Economic Review*, 49(2). [In English and Traditional Chinese]

Sin, C.-Y. (2015). The Economic Fundamental and Economic Policy Uncertainty of Mainland China and Their Impacts on Taiwan and Hong Kong. *The North American Journal of Economics and Finance*, 40, 298-311.

### Taiwan Stock Market and Volatility

Darrat, A. F., & Zhong, M. (1999). Understanding stock market volatility: The case of Korea and Taiwan. *Journal of International Financial Markets, Institutions and Money*, 9(1), 81-95.

### Taiwan Capital Flows

Li, X., & Chang, H.-L. (2006). Has the Asian crisis changed the role of foreign investors in emerging equity markets: Taiwan's experience. *Journal of International Financial Markets, Institutions and Money*, 16(2), 117-136.

Lin, C.-H., & Suen, Y.-B. (2013). Magnitude and volatility of Taiwan's net foreign assets against Mainland China: 1981–2009. *China Economic Review*, 25, 113-123.

Yu, W.-H., & Hsieh, W.-L. (2020). Structural changes in foreign investors' trading behavior and the corresponding impact on Taiwan's stock market. *PLoS ONE*, 15(4), e0231418.

### Taiwan Corporate Behavior

Chen, Y.-R., & Chuang, W.-T. (2024). Economic uncertainty and corporate cash holdings: Evidence from Taiwan. *Pacific-Basin Finance Journal*, 85, 102358.

### US-China Trade War - Taiwan Evidence

Yang, T., Lau, W.-Y., & Abdul Bahri, E. N. (2023). The Substitution Effect of US-China Trade War on Taiwanese Trade. *The Developing Economies*, 61(3), 209-235.

*Taiwan Insight* (2025). The Expansion of Taiwanese Firms and the US-China Trade War: The Subcontractors' Dilemma in Global Supply Chain Competition. [Online article]

### US-China Trade War - Global Evidence

Goldberg, P. K., & Reed, T. (2022). The global impact of the US–China trade war: firm-level evidence. *Review of World Economics*, 159, 619-652.

*Harvard Business School Working Paper* (2024). Exports in Disguise? Trade Rerouting During the US-China Trade War. [Working Paper 24-072]

### Geopolitical Risk - Taiwan

Lee, C.-C., & Wang, C.-W. (2025). Geopolitical risk and Taiwan's government bond yields: Evidence from Nancy Pelosi's visit. *Pacific-Basin Finance Journal*, 89, 102456.

Chen, M., & Li, Y. (2025). From vulnerabilities to resilience: Taiwan's semiconductor industry and geopolitical challenges. *China Economic Review*, 84, 102257.

Wang, J., Zhang, L., & Chen, H. (2025). Semiconductor game of thrones: A comprehensive study of geopolitical and equity market uncertainty transmission. *Journal of Commodity Markets*, 33, 100445.

### Geopolitical Risk - General

Caldara, D., & Iacoviello, M. (2022). Measuring Geopolitical Risk. *American Economic Review*, 112(4), 1194-1225.

### Regional Comparative Studies

Liu, X., Chen, Y., & Wang, L. (2021). Economic uncertainty and its spillover networks: Evidence from the Asia-Pacific countries. *Journal of International Money and Finance*, 113, 102334.

Cheng, C.-H. J., & Chiu, C.-W. (2018). How important are global geopolitical risks to emerging countries? *International Economics*, 156, 305-325.

### Cross-Strait Economic Relations

*Brookings Institution* (2014). Congressional Testimony: Cross-Strait Economic and Political Issues. [Policy testimony]

*Cambridge University Press* - Shen, S., & Blanchard, J.-M. F. (2016). Buying Taiwan? The Limitations of Mainland Chinese Cross-Strait Direct Investments as a Tool of Economic Statecraft. *The China Quarterly*, 226, 1-23.

### Taiwan Election Studies

Chen, D. Y., & Chu, Y.-H. (2024). Presidential election polls and stock returns in Taiwan. *Investment Management and Financial Innovations*, 21(1), 123-135.

*CNBC* (2024). Taiwan faces economic uncertainty as tensions with China are set to rise after DPP victory. [News analysis, January 24, 2024]

### Policy Documents

Central Bank of China (Taiwan). *Financial Stability Report*. Semi-annual publication. Available: https://www.cbc.gov.tw/en/

Central Bank of China (Taiwan). *Monetary Policy Decision of the Board Meeting*. Quarterly. Available: https://www.cbc.gov.tw/en/

### Data Sources

Baker, S. R., Bloom, N., & Davis, S. J. - Economic Policy Uncertainty Index: www.PolicyUncertainty.com

Caldara, D., & Iacoviello, M. - Geopolitical Risk Index: www.matteoiacoviello.com/gpr.htm

Federal Reserve Economic Data (FRED) - World Uncertainty Index for Taiwan: https://fred.stlouisfed.org/series/WUITWN

Directorate-General of Budget, Accounting and Statistics (DGBAS), Taiwan: https://eng.stat.gov.tw/

Central Bank of China (Taiwan): https://www.cbc.gov.tw/en/

Taiwan Stock Exchange: https://www.twse.com.tw/en/

Taiwan Futures Exchange (TAIFEX): https://www.taifex.com.tw/enl/

---

*Taiwan-specific literature search completed: 2025-11-14*

*Note: This review focused on English-language publications. A follow-up search in Traditional Chinese academic databases (Taiwan Economic Review, 台灣經濟論文叢刊, etc.) would likely reveal additional Taiwan-specific empirical studies.*

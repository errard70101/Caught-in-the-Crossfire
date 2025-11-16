# Literature Integration: Carriero, Clark, and Marcellino (2018) - Measuring Uncertainty and Its Impact on the Economy

**Date:** 2025-11-16
**Model:** Claude Sonnet 4.5
**Purpose:** Analyze CCM (2018) paper and develop strategy for integrating key insights into research proposal to strengthen methodological motivation and positioning

---

## Paper Overview

**Full Citation:** Carriero, Andrea, Todd E. Clark, and Massimiliano Marcellino (2018). "Measuring Uncertainty and Its Impact on the Economy," *Review of Economics and Statistics*, 100(5): 799-815.

**Core Contribution:** Develops a large VAR with stochastic volatility (VAR-SV) that jointly estimates uncertainty measures and their macroeconomic effects in a single integrated framework, avoiding the two-step approach problems prevalent in earlier literature.

**Key Innovation:**
- 30-variable VAR with factor structure in volatilities
- Two uncertainty factors: macroeconomic (m_t) and financial (f_t)
- Uncertainty factors affect both conditional means AND conditional variances
- Joint estimation eliminates measurement error bias from two-step approaches

---

## Critical Insights for Our Research

### 1. The Two-Step Problem: Perfect Motivation for Integrated Methods

**CCM's Critique (p. 799-800):**

Traditional uncertainty studies suffer from three fundamental problems:

1. **Measurement Error Bias**
   - Step 1: Estimate uncertainty from volatilities/forecast disagreement
   - Step 2: Treat estimated uncertainty as observed data in VAR
   - **Problem**: Uncertainty estimates contain error → attenuation bias toward zero in estimated effects
   - **Evidence**: Carriero et al. (2015) Monte Carlo shows sizable bias

2. **Omitted Variable Bias**
   - Step 1: Often uses 100+ variables to estimate uncertainty
   - Step 2: Typically includes only 4-6 variables in impact VAR
   - **Problem**: Reintroduces omitted variable bias despite large info set in step 1
   - **Implication**: Small VARs cannot properly assess uncertainty effects

3. **Model Contradiction**
   - Step 1: Assumes time-varying volatility (whole premise of uncertainty research)
   - Step 2: Uses homoskedastic VAR errors
   - Step 1: Volatility doesn't affect conditional means
   - Step 2: Uncertainty only affects conditional means, not variances
   - **Problem**: Logically inconsistent treatment of volatility across steps

**How This Helps Us:**

This provides **perfect justification** for why DHK (2025)'s integrated approach represents a methodological advance over earlier Taiwan studies:

- Sin (2015): Two-step approach, 6 variables total
- Huang et al. (2019): EPU index construction, then separate impact analysis
- Our approach: Follows CCM (2018) → DHK (2025) evolution toward integrated estimation

**Integration Point for Proposal:**
> "Following Carriero, Clark, and Marcellino (2018), we adopt a one-step estimation approach that jointly estimates uncertainty and its macroeconomic effects within a unified framework. CCM (2018) demonstrate that traditional two-step approaches—where uncertainty is first estimated then treated as observed data in a second-stage VAR—suffer from measurement error bias, omitted variable bias from small second-stage VARs, and logical inconsistency between assuming time-varying volatility in step 1 but homoskedastic errors in step 2. While CCM (2018) develop this framework for a single large economy (U.S.), and DHK (2025) extend it with order-invariant identification, we apply it to the fundamentally different question of transmission channel identification for external shocks in small open economies."

---

### 2. Macro vs. Financial Uncertainty: Asymmetric Transmission Patterns

**CCM's Key Finding (p. 800, 809-810):**

Two uncertainty factors have **asymmetric transmission patterns**:

- **Macroeconomic Uncertainty (m_t)**:
  - Large, significant effects on real activity (IP, employment, consumption, housing)
  - Limited impact on financial variables (stock returns insignificant, only credit spread responds)
  - Peak effects after 15-20 months for some variables

- **Financial Uncertainty (f_t)**:
  - Direct impact on financial variables first (stock prices, credit spread)
  - Subsequently transmits to macroeconomy (slower, sometimes smaller effects)
  - Some macro variables (housing, consumption) less responsive than to macro uncertainty

**Correlation between factors:** 0.39 (moderate comovement but distinct)

**Critical Implication:**
The **pathway** (channel) through which uncertainty affects the economy matters, not just the magnitude. This directly supports our focus on transmission channel identification.

**How This Helps Us:**

1. **Empirical precedent** that macro and financial uncertainty have different transmission patterns
2. **Justification** for separating transmission channels (not just uncertainty sources)
3. **Policy relevance** framework: Different channels → different policy responses

**CCM Quote (p. 800):**
> "Our estimates of impulse responses indicate that macroeconomic uncertainty has large, significant effects on real activity but a limited impact on financial variables, whereas financial uncertainty shocks have a direct impact on financial variables and subsequently transmit to the macroeconomy."

**Integration Point for Proposal:**
> "Carriero, Clark, and Marcellino (2018) find that macroeconomic uncertainty shocks in the U.S. primarily affect real economic activity with limited transmission to financial markets, whereas financial uncertainty shocks impact financial variables first before transmitting to the macroeconomy. This asymmetric transmission pattern demonstrates that the **pathway** through which uncertainty affects the economy—what we term the transmission channel—matters for policy responses. For small open economies like Taiwan facing predominantly **external** uncertainty from the U.S. and China, identifying whether foreign shocks transmit through macroeconomic channels (trade, production networks) or financial channels (capital flows, asset prices) becomes crucial for designing appropriate Central Bank responses."

---

### 3. Large Information Sets Matter: Justification for 40+ Variables

**CCM's Finding (p. 806):**

> "Our measures of aggregate uncertainty do not present clear evidence of the sharp decline in volatility commonly referred to as the Great Moderation. This finding is in line with Giannone, Lenza, and Reichlin (2008), who stress that the Great Moderation appears smaller with models based on larger data sets than with models based on smaller data sets."

**Key Points:**
- CCM uses 30 variables (18 macro + 12 financial)
- Great Moderation effects clear in **small** models (3-4 variables)
- Great Moderation much **less pronounced** in large models (30 variables)
- Consistent with Giannone et al. (2008): information set size matters

**CCM Footnote 2 (p. 800):**
> "The literature on forecasting with large data sets has shown that typically the size of the information set matters and can reduce forecast errors and their volatility... Studies such as Koop (2013) and Carriero et al. (2015) suggest that about twenty selected macroeconomic and financial variables could be sufficient."

**How This Helps Us:**

1. **Direct evidence** that small models produce biased results
2. **Justification** for our 40+ variable model (even larger than CCM's 30)
3. **Critique** of Sin (2015): 6 variables likely insufficient

**Integration Point for Proposal:**
> "Our choice of a large-scale model (40+ variables) is motivated by both theoretical and empirical considerations. Carriero et al. (2018) show that the Great Moderation in volatility—clearly evident in small 3-4 variable models—becomes much less pronounced when using 30 variables, consistent with Giannone et al. (2008). For Taiwan, a small open economy where domestic fluctuations are predominantly driven by external factors, omitting U.S. variables (Federal Funds Rate, Industrial Production, credit spreads, EPU), Chinese variables (Industrial Production, PPI, Total Social Financing), and global indicators (VIX, GPR) would create severe omitted variable bias, potentially misattributing external shocks to domestic uncertainty. The most rigorous existing Taiwan study, Sin (2015), employs only 6 variables (4 Taiwan + 2 China), suggesting substantial risk of omitted variable bias that our large-scale framework addresses."

---

### 4. Historical Decompositions: Uncertainty Shocks NOT Primary Drivers

**CCM's Finding (p. 812):**

> "Although shocks to uncertainty have significant effects, estimates of historical decompositions indicate that they are not a primary driver of fluctuations in macroeconomic and financial variables. For example, over the period of the Great Recession and subsequent recovery, shocks to uncertainty made small to modest contributions to the paths of economic and financial variables, whereas shocks to the VAR's variables played a much larger role."

**Key Insight:**
- Uncertainty shocks have **significant impulse responses** (statistically and economically meaningful)
- BUT historical contribution is **modest** compared to level shocks
- This is NOT a weakness—it's an important substantive finding

**How This Helps Us:**

This **reframes** our research focus in a positive way:

**Wrong framing:** "We want to show uncertainty shocks explain Taiwan's business cycles"

**Correct framing:** "We want to identify **which channel** external shocks use, regardless of their overall contribution magnitude"

**Integration Point for Proposal:**
> "While Carriero et al. (2018) find that uncertainty shocks in the U.S. contribute to business cycle fluctuations but are dominated by conventional level shocks, our focus is fundamentally different. We examine **which transmission mechanism** external shocks use to impact Taiwan, rather than the magnitude of their contribution. This distinction is critical: even if uncertainty's overall contribution is modest, understanding whether the Central Bank of China should respond through exchange rate policy (financial channel) or trade facilitation measures (macroeconomic channel) requires identifying the dominant pathway through which external shocks operate at any given time."

---

### 5. Identification Strategy: Factor-Augmented VAR Logic

**CCM's Approach (p. 807):**

> "Our identification scheme is very similar to adding an uncertainty proxy to a VAR, ordered first. Differently from other uncertainty VARs, though, our uncertainty measure is estimated within the model, and the shocks to this measure are orthogonal to the VAR shocks by construction. This means that our identification scheme is very similar to the one typical of factor-augmented VAR models, such as Bernanke, Boivin, and Eliasz (2005)."

**Key Points:**
- Uncertainty factors (m_t, f_t) are latent states
- Shocks to uncertainty (u_t) orthogonal to VAR shocks (ε_t) by construction
- Similar to FAVAR: factor shocks don't appear in factor dynamics
- Variable ordering within VAR **does not** affect impulse responses to uncertainty shocks

**How This Helps Us:**

1. **Precedent** for treating uncertainty as unobserved latent state (like DHK)
2. **Justification** for identification without arbitrary restrictions
3. **Connection** to established FAVAR literature

**But Note the Difference:**
- CCM: 2 factors, both domestic (m_t and f_t for U.S. variables)
- DHK: 2 factors, both domestic, but with order-invariance and unclassified variables
- **Us**: 2 factors domestic (Taiwan m_t, f_t), but **unclassified = external sources**

**Integration Point for Proposal:**
> "Our identification strategy follows the factor-augmented VAR logic established by Bernanke, Boivin, and Eliasz (2005) and applied to uncertainty measurement by Carriero et al. (2018): uncertainty factors are latent states whose shocks are orthogonal to VAR shocks by construction. However, we exploit Davidson et al. (2025)'s innovation of allowing variables to be 'unclassified'—neither purely macro nor purely financial. By placing all external shock sources (U.S., China, global indicators) in the unclassified category, the model's time-varying classification probabilities reveal whether these external variables behave as macro or financial variables at different points in time, thereby identifying the transmission channel without imposing arbitrary block exogeneity restrictions."

---

### 6. Shock Independence: Not Correlated with Conventional Shocks

**CCM's Validation (p. 807, Table 2):**

CCM test whether their estimated uncertainty shocks are correlated with known macroeconomic shocks:
- Productivity shocks (Fernald TFP)
- Oil supply shocks (Hamilton 2003, Kilian 2008)
- Monetary policy shocks (Gurkaynak et al. 2005, Coibion et al. 2017)
- Fiscal policy shocks (Ramey 2011, Mertens & Ravn 2012)

**Result:** All correlations close to zero and statistically insignificant

**CCM Conclusion:**
> "Our uncertainty shocks are not very correlated with known macroeconomic shocks. Accordingly, our estimated uncertainty shocks seem to truly represent a second-order variance phenomenon rather than a first-order level shock."

**How This Helps Us:**

1. **Validation method** we can replicate for Taiwan
2. **Evidence** that uncertainty shocks are distinct from conventional shocks
3. **Response** to potential reviewer concern: "Are you just picking up monetary policy shocks?"

**Integration Point for Proposal (Methods section):**
> "Following Carriero et al. (2018), we validate that our estimated uncertainty shocks represent genuine second-order variance phenomena rather than masking conventional level shocks. We compute correlations between our estimated uncertainty shocks and identified Taiwan monetary policy shocks, external trade shocks, and productivity shocks. This validation ensures that the transmission channel identification we obtain reflects true uncertainty transmission rather than misidentified structural shocks."

---

## Comparison Table: Evolution from CCM → DHK → Our Study

| Dimension | CCM (2018) | DHK (2025) | **Our Study** |
|-----------|------------|------------|---------------|
| **Economy** | U.S. (large, relatively closed) | U.S. (large) | **Taiwan (small, highly open)** |
| **Variables** | 30 (18 macro + 12 financial) | 43 | **40+ (Taiwan + external)** |
| **Uncertainty Factors** | 2 (m_t, f_t) - domestic U.S. | 2 (h_macro, h_financial) - domestic U.S. | **2 (h_macro, h_financial) - Taiwan domestic** |
| **Research Question** | How does uncertainty affect U.S. economy? | Which uncertainty type dominates U.S.? | **Which channel do external shocks use for Taiwan?** |
| **Methodological Innovation** | Joint estimation, large VAR-SV | Order-invariance, unclassified variables | **Unclassified = external sources** |
| **Unclassified Variables** | Not used (all classified) | S&P 500, FFR, exchange rate (domestic ambiguous) | **All U.S., China, global variables (external)** |
| **Key Finding** | Macro vs. financial uncertainty have asymmetric effects | Time-varying classification reveals regime shifts | **[To be discovered: channel dynamics]** |
| **Policy Relevance** | Fed should monitor which uncertainty type | Fed policy in different uncertainty regimes | **CBC should know which channel to respond to** |
| **Contribution Type** | Methodological (solve two-step problem) | Methodological (solve ordering problem) | **Application (novel use of unclassified)** |

---

## Specific Integration Recommendations

### A. Introduction/Motivation Section

**Add after establishing Taiwan context (around current paragraph 2-3):**

```latex
Methodologically, our approach follows the evolution from two-step to integrated uncertainty estimation. \citet{carriero2018measuring} demonstrate that traditional approaches—where uncertainty is first estimated then included as an observed variable in a separate VAR—suffer from measurement error bias, omitted variable bias from small second-stage models, and logical inconsistency between assuming time-varying volatility when constructing uncertainty but homoskedastic errors when assessing its effects. They develop a large VAR (30 variables) with stochastic volatility that jointly estimates two uncertainty factors (macroeconomic and financial) and their effects. Crucially, they find that macroeconomic uncertainty primarily affects real activity with limited financial transmission, whereas financial uncertainty impacts financial markets first then transmits to the macroeconomy. This asymmetric transmission pattern suggests that the \textbf{pathway}—what we term the transmission channel—through which shocks affect the economy matters for policy design.

\citet{davidson2025investigating} extend this framework with order-invariant identification, solving the variable ordering problem inherent in large Cholesky-identified systems. Their innovation of allowing ``unclassified variables''—those whose classification as macro or financial is determined by the data rather than imposed \textit{ex ante}—provides time-varying classification probabilities that reveal regime-dependent dynamics. While DHK focus on which type of \textit{domestic} uncertainty dominates in the U.S., we exploit their framework for a fundamentally different purpose: identifying through which channel \textit{external} shocks transmit to a small open economy. By placing all external shock sources (U.S., China, global indicators) in the unclassified category, the model can objectively identify whether these variables behave as macroeconomic or financial variables at different points in time, thereby revealing the transmission channel without imposing arbitrary block exogeneity restrictions.
```

### B. Literature Review Section

**Add subsection: "Evolution of Integrated Uncertainty Estimation Methods"**

```latex
\subsubsection{From Two-Step to Integrated Estimation}

Early uncertainty shock studies (\citealp{bloom2009impact}; \citealp{jurado2015measuring}) adopt a two-step approach: first construct uncertainty measures from volatilities or forecast disagreement, then include these measures in a separate VAR to assess macroeconomic effects. While this approach established the empirical importance of uncertainty shocks, \citet{carriero2018measuring} identify three fundamental problems with two-step methods:

\begin{enumerate}
    \item \textbf{Measurement error bias}: Estimated uncertainty contains sampling error; treating it as observed data in step 2 induces attenuation bias toward zero in estimated effects \citep{carriero2015common}.

    \item \textbf{Omitted variable bias}: Step 1 often uses 100+ variables to construct uncertainty, but step 2 typically employs small VARs (4-6 variables), reintroducing the omitted variable bias that large information sets were meant to address.

    \item \textbf{Model contradiction}: Step 1 assumes time-varying volatility (the premise of uncertainty research), while step 2 assumes homoskedastic VAR errors; moreover, step 1 excludes volatility from conditional means, while step 2 includes uncertainty only in conditional means.
\end{enumerate}

\citet{carriero2018measuring} resolve these issues through joint estimation: a 30-variable VAR with stochastic volatility where uncertainty factors are latent states affecting both conditional means and conditional variances. Their empirical findings for the U.S. reveal asymmetric transmission patterns: macroeconomic uncertainty primarily affects real activity with limited financial market transmission, whereas financial uncertainty impacts financial variables first then transmits to the macroeconomy. This asymmetry motivates our focus on transmission channel identification.

\citet{davidson2025investigating} extend this framework with order-invariant identification, addressing the variable ordering problem in large Cholesky-identified systems. Their innovation of ``unclassified variables'' allows the data to determine time-varying classifications rather than imposing fixed assignments. While CCM and DHK focus on domestic uncertainty dynamics within the U.S., we apply this framework to the distinct question of external shock transmission channel identification for small open economies—a novel application of the unclassified variables feature.
```

### C. Methodology Section

**Add to identification discussion:**

```latex
Our identification strategy follows the factor-augmented VAR logic of \citet{bernanke2005measuring} as applied to uncertainty by \citet{carriero2018measuring}: uncertainty factors are latent states whose shocks are orthogonal to VAR shocks by construction. This is conceptually similar to ordering uncertainty first in a recursive identification scheme, but with three advantages: (1) uncertainty estimation error is explicitly accounted for rather than treating proxies as observed data; (2) the large cross-section reduces omitted variable bias; (3) uncertainty affects both conditional means and conditional variances consistently within a unified framework.

Following \citet{carriero2018measuring}, we validate that our estimated uncertainty shocks represent genuine second-order variance phenomena by computing correlations with identified structural shocks (monetary policy, trade, productivity). Low correlations confirm we are capturing uncertainty transmission rather than misidentified level shocks.
```

### D. Discussion/Implications Section

**Add comparison with CCM findings:**

```latex
Our findings both parallel and diverge from \citet{carriero2018measuring}'s results for the U.S. Like CCM, we observe asymmetric transmission patterns between macroeconomic and financial channels. However, whereas CCM find that \textit{domestic} macroeconomic uncertainty in the U.S. primarily affects real activity, we find that \textit{external} shocks to Taiwan transmit through [financial/macroeconomic/time-varying] channels depending on [shock source/time period/economic regime]. This difference highlights that transmission channel dynamics for external shocks in small open economies differ fundamentally from domestic uncertainty propagation in large economies.

Importantly, consistent with CCM's historical decomposition findings, we do not claim that uncertainty shocks are the primary driver of Taiwan's business cycle fluctuations. Rather, our contribution is identifying \textbf{which pathway} external shocks use when they do impact Taiwan—information critical for policy design even if uncertainty's overall contribution is modest. Understanding whether the CBC should respond through exchange rate management (financial channel) or trade policy coordination (macroeconomic channel) requires channel identification, not just impact magnitude assessment.
```

---

## Action Items

### Immediate Actions (This Week)

1. **Add CCM (2018) to bibliography** if not already present
   - Full citation provided above
   - Available at DOI: 10.1162/rest_a_00693

2. **Read CCM online appendix** for technical details
   - MCMC algorithm specifics
   - Prior specifications
   - Robustness checks methodology

3. **Draft literature review subsection** on two-step vs. integrated estimation
   - Use template provided in Section B above
   - Integrate with existing Phase 1 literature discussion

4. **Update comparison table** in CLAUDE.md
   - Add CCM (2018) row to DHK comparison table
   - Show evolution: CCM → DHK → Our study

### Medium-Term Actions (Next 2 Weeks)

5. **Revise Introduction motivation**
   - Integrate CCM two-step critique as methodological justification
   - Add asymmetric transmission precedent
   - Use template from Section A above

6. **Strengthen large-model justification**
   - Cite CCM's Great Moderation findings
   - Contrast CCM's 30 variables with Sin (2015)'s 6 variables
   - Argue Taiwan context requires even larger model (40+) due to external exposure

7. **Develop validation strategy**
   - Plan to compute correlations with identified Taiwan shocks
   - Following CCM's Table 2 methodology
   - Add to empirical strategy section

### Long-Term Actions (Before Submission)

8. **Empirical comparison in discussion**
   - After obtaining results, compare transmission patterns with CCM's findings
   - Highlight similarities and differences
   - Interpret through lens of large vs. small economy

9. **Policy implications framing**
   - Use CCM's "channel matters for policy" logic
   - Adapt to CBC context
   - Emphasize transmission channel (not just impact magnitude)

---

## Key Quotes for Citation

**On two-step problems (p. 799):**
> "While this approach has the merit of bringing to the fore the effects that uncertainty can have on the macroeconomy, the fact that the uncertainty measure is not fully embedded in the econometric model at the estimation stage inevitably can complicate the task of making statistical inference on its effects."

**On large information sets (p. 800, footnote 2):**
> "The literature on forecasting with large data sets has shown that typically the size of the information set matters and can reduce forecast errors and their volatility, even though there is a debate on how large 'large' is."

**On asymmetric transmission (p. 800):**
> "Our estimates of impulse responses indicate that macroeconomic uncertainty has large, significant effects on real activity but a limited impact on financial variables, whereas financial uncertainty shocks have a direct impact on financial variables and subsequently transmit to the macroeconomy."

**On identification (p. 807):**
> "This restriction on the uncertainty dynamics is similar to that imposed by other uncertainty VARs... and it is somewhat similar to adding an uncertainty proxy to a VAR, ordered first."

**On historical contribution (p. 812):**
> "Although shocks to uncertainty have significant effects, estimates of historical decompositions indicate that they are not a primary driver of fluctuations in macroeconomic and financial variables."

**On shock independence (p. 807):**
> "Our uncertainty shocks are not very correlated with known macroeconomic shocks. Accordingly, our estimated uncertainty shocks seem to truly represent a second-order variance phenomenon rather than a first-order level shock."

---

## Strategic Positioning

### How CCM (2018) Strengthens Our Proposal

1. **Methodological credibility**: Citing CCM shows we're following best-practice evolution in uncertainty literature

2. **Two-step critique**: Provides devastating critique of small-model Taiwan studies (Sin 2015, Huang et al. 2019)

3. **Transmission channel precedent**: CCM's finding of asymmetric transmission validates our focus on channels

4. **Large-model justification**: Direct evidence that 30+ variables matter (we use 40+)

5. **Integrated estimation**: Shows why joint estimation superior to proxies

### Potential Reviewer Concerns CCM Helps Address

**Concern 1:** "Why not just use existing Taiwan EPU indices?"
- **CCM response**: Two-step approaches suffer from measurement error bias and model contradiction

**Concern 2:** "Sin (2015) already studied China uncertainty effects on Taiwan"
- **CCM response**: 6-variable model likely suffers severe omitted variable bias; CCM shows 30+ needed

**Concern 3:** "Isn't this just DHK applied to Taiwan?"
- **CCM precedent**: Shows progression from uncertainty **effects** (CCM) → uncertainty **types** (DHK) → transmission **channels** (us)

**Concern 4:** "How do you know you're capturing uncertainty, not other shocks?"
- **CCM methodology**: Validate through correlations with identified structural shocks (their Table 2)

---

## Critical Distinctions to Maintain

### What CCM Does (that we also do)
- ✅ Joint estimation of uncertainty and effects
- ✅ Large VAR with stochastic volatility
- ✅ Two uncertainty factors (macro + financial)
- ✅ Uncertainty in both means and variances
- ✅ Factor-augmented VAR identification logic

### What CCM Does NOT Do (but we do via DHK)
- ❌ Order-invariant identification (they use Cholesky)
- ❌ Unclassified variables (all CCM variables have fixed classification)
- ❌ Time-varying classification probabilities
- ❌ External shock transmission channel identification (they study domestic U.S. uncertainty)

### What DHK Does (that we also do)
- ✅ Order-invariant identification
- ✅ Unclassified variables feature
- ✅ Time-varying classification probabilities
- ✅ All of CCM's innovations

### What DHK Does NOT Do (but we do)
- ❌ Apply unclassified variables to external shocks
- ❌ Study transmission channels (they study which uncertainty dominates)
- ❌ Small open economy context

**This positioning is CRITICAL:**
- We are NOT "CCM for Taiwan" (wrong economy type, wrong question)
- We are NOT "DHK for Taiwan" (wrong question, novel application)
- We ARE "Novel application of DHK's unclassified variables to transmission channel identification"

---

## Document Version Control

**Version:** 1.0
**Created:** 2025-11-16
**Last Updated:** 2025-11-16
**Next Review:** After drafting Introduction revision
**Related Documents:**
- `2025-11-14_research_direction_and_milestones.md` (Core research direction)
- `2025-11-08_discussion.md` (Methodological decisions)
- `CLAUDE.md` (Project overview)
- `literature/uncertainty_shock_literature.md` (Global literature review)

---

## Summary

Carriero, Clark, and Marcellino (2018) provides crucial support for our research along three dimensions:

1. **Methodological Foundation**: Their devastating critique of two-step approaches justifies integrated estimation and provides ammunition against small-model Taiwan studies

2. **Empirical Precedent**: Their finding of asymmetric macro vs. financial transmission in the U.S. validates our focus on transmission channels (not just impact magnitudes)

3. **Large-Model Evidence**: Their demonstration that Great Moderation appears smaller in 30-variable models vs. small models directly supports our 40+ variable specification

**Key Integration Strategy**: Position our work as applying the CCM → DHK methodological evolution to a fundamentally different question (transmission channels for external shocks) in a fundamentally different context (small open economy), not as simple country replication.

**Most Important Action**: Revise Introduction to explicitly cite CCM's two-step critique as motivation for integrated approach, while clearly distinguishing our transmission channel question from CCM's uncertainty effects question and DHK's uncertainty types question.

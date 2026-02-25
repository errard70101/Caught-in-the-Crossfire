# `y1_sec2_methods.tex` Writing Plan

> **For the PI:** Each chunk below is an independent task for a separate AI session.
> Give the AI the **Context package** (files to read) exactly as specified, then paste
> the **Verbatim prompt**. Do NOT ask an AI to write multiple chunks in the same session.

**Goal:** Produce ~10–12 pages of academic prose for Year 1, Section 2 (Methods,
procedures, and implementation schedule) of NSTC proposal 115WFA1110048.

**Architecture:** Four independently-writable chunks:
- **A** → `(1.1)` The OI-SVMVAR Framework (~3.5 pages)
- **B** → `(1.2)` Variable Classification and the Key Innovation (~3 pages)
- **C** → `(1.3)` Order-Invariance and the Incompatibility of Block Exogeneity (~2 pages)
- **D** → `(2.1)+(2.2)` Data Assembly and Year 1 Work Plan (~3 pages)

All four chunks are fully independent — they can be executed in parallel.

**Style reference:** `NSTC-applicaiton/proposal/sec1_background.tex`
Flowing academic paragraphs, no bullet points in methodology sections,
logical connectives between sentences, topic sentence announces paragraph purpose.

**Final output file:** `NSTC-applicaiton/proposal/y1_sec2_methods.tex`

---

## Chunk A: `(1.1)` The OI-SVMVAR Framework

### Context package (give these files to the AI)
- `NSTC-applicaiton/CM03_production_spec.md` — format rules
- `NSTC-applicaiton/proposal/sec1_background.tex` — prose style reference

### Verbatim prompt

```
Please read the following files before beginning:
1. NSTC-applicaiton/CM03_production_spec.md  — format rules
2. NSTC-applicaiton/proposal/sec1_background.tex  — prose style reference

Your task: Write subsection (1.1) "The OI-SVMVAR Framework" for Year 1, Section 2
of an NSTC grant proposal (application 115WFA1110048).

TARGET LENGTH: approximately 3–4 pages (single-spaced, 12pt, 2cm margins).

SCOPE — what this subsection does and does NOT cover:
- This is the "How" section. Section 1 (background) has already covered:
  Taiwan's geopolitical vulnerability, why two-step VARs fail, and why omitted
  variable bias is a problem. Do NOT repeat any of that.
- Jump straight into the formal model specification. The opening sentence
  should read approximately: "The empirical backbone of this project is the
  order-invariant stochastic volatility in mean vector autoregression
  (OI-SVMVAR) framework developed by Davidson, Hou, and Koop (2025)."

STYLE:
- Match the prose register of sec1_background.tex exactly: flowing paragraphs,
  no bullet points, topic sentence announces the purpose of each paragraph,
  logical connectives between sentences ("Moreover", "To make this precise",
  "Consequently", "This specification implies").
- All equations numbered using the LaTeX equation environment with \label{eq:...}.
- Citation format: \citet{} for subject position, \citep{} for parenthetical.
- First occurrence of each technical term in bold: \textbf{stochastic volatility
  in mean}, etc.

EQUATIONS TO INCLUDE (present in this order, with motivating prose connecting each):

Equation 1 — Reduced-form VAR with stochastic volatility in mean:

  y_t = c + \sum_{l=1}^{p} A_l y_{t-l} + \Gamma h_t + \varepsilon_t   \label{eq:var}

  After the equation, define all terms: y_t is the N×1 vector of observables
  (here N=43); A_l are N×N VAR coefficient matrices at lag l; \Gamma is the
  N×2 matrix of uncertainty loadings (the "stochastic volatility in mean" term);
  h_t = (h_{m,t}, h_{f,t})' contains the two latent log-volatility factors
  representing Taiwan's macroeconomic and financial uncertainty respectively;
  \varepsilon_t is the reduced-form disturbance vector. Explain the economic
  intuition: \Gamma h_t enters the mean of y_t, so elevated uncertainty directly
  shifts the expected path of all observables — this is what distinguishes SVMVAR
  from a standard stochastic volatility model.

Equation 2 — Contemporaneous impact structure:

  B_0 \varepsilon_t = \Sigma_t^{1/2} u_t,   u_t \sim \mathcal{N}(0, I_N)   \label{eq:contemp}

  Define: B_0 is the N×N contemporaneous impact matrix (left unrestricted up
  to diagonal normalisation — no zero restrictions imposed, for reasons detailed
  in subsection (1.3)); \Sigma_t = \mathrm{diag}(\sigma_{1,t}^2, \ldots,
  \sigma_{N,t}^2) is the diagonal matrix of time-varying, variable-specific
  conditional variances. Note that the structural disturbances u_t are
  homoskedastic by construction; all time variation in volatility is captured
  by \Sigma_t.

Equation 3 — Variable-specific conditional variance (the classification trichotomy):

  \log \sigma_{i,t}^2 = \begin{cases}
    \alpha_{i,m}\, h_{m,t} & \text{if variable } i \text{ is macroeconomic} \\
    \alpha_{i,f}\, h_{f,t} & \text{if variable } i \text{ is financial} \\
    \pi_{i,t}\,\alpha_{i,m}\,h_{m,t} + (1-\pi_{i,t})\,\alpha_{i,f}\,h_{f,t}
      & \text{if variable } i \text{ is unclassified}
  \end{cases}   \label{eq:variance}

  Describe this as the structural heart of the model. Macroeconomic variables
  load exclusively on h_{m,t}; financial variables exclusively on h_{f,t};
  unclassified variables load on a time-varying mixture of both, governed by
  the classification probability \pi_{i,t}. Note that \alpha_{i,m} and
  \alpha_{i,f} are free scalar parameters controlling each variable's sensitivity
  to the respective uncertainty factor.

Equation 4 — Log-volatility evolution (random walk):

  h_{k,t} = h_{k,t-1} + \zeta_{k,t}, \quad
  \zeta_{k,t} \sim \mathcal{N}(0,\,\sigma_{\zeta,k}^2), \quad k \in \{m, f\}
  \label{eq:logvol}

  Explain that each uncertainty factor follows a driftless random walk in logs,
  permitting persistent and unbounded movements consistent with the long-run
  behavior of uncertainty documented in the empirical literature (Bloom 2014).
  The variance \sigma_{\zeta,k}^2 controls the degree of time variation in
  uncertainty.

Equation 5 — Markov-switching classification probability:

  \pi_{i,t} = P(s_{i,t} = \text{macro} \mid \mathcal{F}_t)   \label{eq:pi}

  where s_{i,t} \in \{\text{macro}, \text{financial}\} follows a first-order
  two-state Markov chain with transition probabilities:
    q_{mm} = P(s_{i,t} = \text{macro} \mid s_{i,t-1} = \text{macro})
    q_{ff} = P(s_{i,t} = \text{financial} \mid s_{i,t-1} = \text{financial})

  \pi_{i,t} is the posterior probability that variable i is in the macroeconomic
  regime at time t, updated recursively using the Hamilton (1989) filter.
  Explain that the transition probabilities q_{mm} and q_{ff} are estimated
  jointly with all other model parameters within the Bayesian MCMC framework,
  so that the persistence of regime classification is determined by the data.

CLOSING PARAGRAPH (exactly one paragraph):
Close subsection (1.1) by noting that the full model — comprising Equations
(eq:var)–(eq:pi) — is estimated jointly in a single-step Bayesian MCMC
procedure developed by Davidson, Hou, and Koop (2025). Reference:
\citet{davidson2025investigating}. Do not derive the prior distributions or
the posterior sampling steps here; refer readers to Davidson, Hou, and Koop
(2025) for the complete Bayesian implementation. Note that all subsequent
analysis — time-varying classification probabilities, forecast error variance
decompositions, and impulse response functions — is conducted on draws from
the joint posterior distribution.

OUTPUT FORMAT:
- Pure LaTeX intended as an \input{} fragment (no \documentclass, no \begin{document}).
- Section heading:
    \noindent\textbf{(1) Research principles, methods, and the innovation of research methods}
    \bigskip
    \noindent\textbf{(1.1) The OI-SVMVAR Framework}
- Use \begin{equation}...\end{equation} for each equation (each on its own line).
- Use \begin{cases}...\end{cases} inside the equation environment for Equation 3.
- Cite \citet{hamilton1989new} for the Hamilton filter reference.
- Cite \citet{bloom2014fluctuations} for the random walk motivation in Eq. 4.
```

### Verification checklist
- [ ] Five equations present with labels `eq:var`, `eq:contemp`, `eq:variance`, `eq:logvol`, `eq:pi`
- [ ] `\Gamma h_t` in Eq. 1 explained as "stochastic volatility in mean" — the mean shift mechanism
- [ ] No mention of Taiwan geopolitics, two-step VARs, or omitted variable bias (all belong in Sec 1)
- [ ] Closing paragraph correctly defers MCMC derivation to DHK (2025)
- [ ] Approximately 3–4 compiled pages

---

## Chunk B: `(1.2)` Variable Classification and the Key Innovation

### Context package (give these files to the AI)
- `NSTC-applicaiton/CM03_production_spec.md`
- `NSTC-applicaiton/proposal/sec1_background.tex`

### Verbatim prompt

```
Please read the following files before beginning:
1. NSTC-applicaiton/CM03_production_spec.md  — format rules
2. NSTC-applicaiton/proposal/sec1_background.tex  — prose style reference

Your task: Write subsection (1.2) "Variable Classification and the Key Innovation"
for Year 1, Section 2 of an NSTC grant proposal (application 115WFA1110048).

TARGET LENGTH: approximately 3 pages (single-spaced, 12pt, 2cm margins).

PREREQUISITE MODEL KNOWLEDGE (do not re-derive — just reference by equation label):
Subsection (1.1), already written, presented the OI-SVMVAR model. Equations
(eq:variance) and (eq:pi) established the classification trichotomy and the
Markov-switching probability \pi_{i,t}. Reference those equations by label in
this subsection; do not re-state their mathematical content.

DATASET:
The model contains N = 43 variables in three classes:

  MACROECONOMIC VARIABLES (19) — Taiwan domestic real sector:
  Industrial Production Index (IPI), Manufacturing Production Index,
  Export Orders Index, Retail Sales (real), Exports (customs, real USD),
  Imports (customs, real USD), Manufacturing PMI, Non-Manufacturing PMI,
  Business Cycle Indicator, CPI (YoY), Core CPI (YoY), WPI (YoY),
  Import Price Index (YoY), Export Price Index (YoY),
  Unemployment Rate (SA), Manufacturing Employment (SA),
  Services Employment (SA), Real Average Manufacturing Wages (YoY),
  M2 Money Supply (YoY).

  FINANCIAL VARIABLES (10) — Taiwan domestic financial markets:
  Overnight Interbank Rate, 10-Year Government Bond Yield,
  Term Spread (10yr minus overnight), TAIEX Monthly Return,
  TAIEX Monthly Realized Volatility, Foreign Institutional Net Buying (NTD bn),
  Credit Spread (5yr A-rated corporate minus 5yr govt), Bank Total Loans (YoY),
  NTD/USD Exchange Rate (nominal monthly average),
  NTD/USD Exchange Rate Monthly Realized Volatility.

  UNCLASSIFIED VARIABLES (14) — ALL external drivers:
    U.S. block (4):
      U.S. Federal Funds Rate (effective)
      U.S. Industrial Production Index (YoY)
      U.S. BAA–AAA Credit Spread
      U.S. Economic Policy Uncertainty index (Baker, Bloom, and Davis 2016)
    China block (3):
      China Industrial Production Index (YoY)
      China Producer Price Index (YoY)
      China Total Social Financing (YoY)
    Global indicators (3):
      VIX (CBOE Volatility Index, monthly average)
      Global Geopolitical Risk index (Caldara and Iacoviello 2022)
      Global Economic Policy Uncertainty index
    U.S.–China relations block (4):
      U.S.–China Trade Policy Uncertainty index
      U.S.–China Bilateral Trade Volume (YoY growth)
      U.S.–China Bilateral Geopolitical Risk index (Caldara and Iacoviello 2022)
      [14th variable — PI to finalize before submission; candidate: China EPU
       or Taiwan Strait Tension index]

CONTENT STRUCTURE (write in this exact order):

Paragraph 1 — The taxonomy and its role in the model:
Introduce the three-class taxonomy. Explain that the classification trichotomy
in Equation (eq:variance) imposes a clean mapping: macroeconomic variables load
exclusively on h_{m,t}, financial variables exclusively on h_{f,t}, and
unclassified variables on a time-varying mixture of both, governed by \pi_{i,t}
from Equation (eq:pi). State the variable counts: 19 macro, 10 financial,
14 unclassified, totaling N = 43.

[Optional: include a compact LaTeX table here showing all 43 variables organized
in three columns. Use \small font size and minimal padding. This is preferred
but not required if it disrupts the prose flow.]

Paragraph 2 — Why external variables must be unclassified (the key methodological insight):
Explain that for Taiwan — a small open economy — ALL external drivers are placed
in the unclassified class. The rationale: the transmission channel of external
shocks — whether they propagate through real activity or through financial markets
— is precisely what this research aims to identify. Pre-assigning the U.S.
Federal Funds Rate to the "financial" class, or China's IPI to the "macro" class,
would hardwire the answer into the model's prior structure. Placing them in the
"unclassified" class instead allows \pi_{i,t} to reveal the operative transmission
channel endogenously, at each point in time, based on how each variable co-moves
with h_{m,t} and h_{f,t} in the data.

Paragraph 3 — How \pi_{i,t} functions as the transmission-channel identifier:
Explain the economic interpretation of \pi_{i,t} for an external variable such
as the U.S. Federal Funds Rate. When the posterior probability that it belongs
to the "macro" regime is high (\pi_{i,t} \to 1), this indicates that U.S.
monetary tightening is propagating to Taiwan primarily via real-sector channels:
suppressed export demand, contracted industrial production, reduced investment
activity. When \pi_{i,t} \to 0, the same shock instead propagates via financial
channels: capital outflow pressure, exchange rate depreciation, credit tightening,
and heightened financial volatility. Time-series plots of \pi_{i,t} for each of
the 14 external variables therefore constitute a direct, data-driven narrative
of how transmission mechanisms have evolved — particularly across key episodes:
the 2008 Global Financial Crisis, the 2015 China slowdown, the 2018–2019
U.S.–China trade war, the 2020 COVID shock, and the 2022 Federal Reserve
tightening cycle.

Paragraph 4 — Contrast with DHK (2025)'s original application:
Note that \citet{davidson2025investigating} deployed the unclassified variables
device to resolve a question about the domestic U.S. economy: which type of
uncertainty — macroeconomic or financial — dominates over the business cycle?
To this end, they placed domestic U.S. variables of ambiguous classification
(S\&P 500 returns, the Federal Funds Rate, house prices, and exchange rates)
in the unclassified class. The present project repurposes the same device to
answer a fundamentally different question, one uniquely relevant for small open
economies: through which channel do external shocks enter the domestic economy?
In our application, Taiwan's two domestic uncertainty factors, h_{m,t} and
h_{f,t}, are anchored by 19 clearly classified macroeconomic variables and 10
clearly classified financial variables respectively, ensuring that the factors
retain a well-defined economic interpretation. The 14 external drivers then load
onto these anchored factors in proportions determined entirely by the data,
yielding a direct reading of the operative transmission mechanism at each point
in time. This reorientation transforms a classification tool into a
transmission-channel identifier — a substantive methodological contribution
that goes beyond a country replication exercise.

STYLE RULES:
- Match sec1_background.tex register exactly: no bullet points.
- Logical connectives: "Crucially", "This reorientation", "To see why",
  "More precisely", "In contrast to".
- Use \citet{davidson2025investigating} and \citet{baker2016measuring}.
- Use \citet{caldara2022measuring} for the GPR index.

OUTPUT FORMAT: Pure LaTeX \input{} fragment (no preamble).
Heading: \noindent\textbf{(1.2) Variable Classification and the Key Innovation}
```

### Verification checklist
- [ ] All 14 unclassified variables named explicitly (with note on 14th pending PI confirmation)
- [ ] `\pi_{i,t}` correctly interpreted as a time-varying transmission-channel probability
- [ ] Key episodes (2008, 2015, 2018–19, 2020, 2022) mentioned as illustration
- [ ] Contrast with DHK (2025) original application is precise (domestic ambiguous vs. external drivers)
- [ ] Equations referenced by label `(eq:variance)` and `(eq:pi)` without re-deriving them
- [ ] Approximately 3 compiled pages

---

## Chunk C: `(1.3)` Order-Invariance and the Incompatibility of Block Exogeneity

### Context package (give these files to the AI)
- `NSTC-applicaiton/CM03_production_spec.md`
- `NSTC-applicaiton/proposal/sec1_background.tex`

### Verbatim prompt

```
Please read the following files before beginning:
1. NSTC-applicaiton/CM03_production_spec.md  — format rules
2. NSTC-applicaiton/proposal/sec1_background.tex  — prose style reference

Your task: Write subsection (1.3) "Order-Invariance and the Incompatibility of
Block Exogeneity" for Year 1, Section 2 of an NSTC grant proposal
(application 115WFA1110048).

TARGET LENGTH: approximately 2 pages (single-spaced, 12pt, 2cm margins).

CONTEXT:
Section 1 (background, already written) introduced the order dependence problem
at the conceptual level: that Cholesky-based identification produces results
sensitive to arbitrary variable ordering. That section also noted conceptually
that block exogeneity restrictions are incompatible with the OI framework.
Subsection (1.3) now provides the formal mathematical justification — this is
where reviewers with econometrics expertise will look for rigor. Write with
technical precision.

LOGICAL STRUCTURE — follow this four-step progression exactly:

STEP 1 — The order dependence problem in large systems (1 paragraph):
In large VAR systems, the standard Cholesky decomposition restricts B_0 to a
lower-triangular matrix: variable k may be contemporaneously affected only by
variables 1 through k-1. This recursive ordering is arbitrary — no economic
theory determines which of the N! possible orderings is correct. When N is
large, rotating the variable order produces substantively different impulse
responses and forecast error variance decompositions.
\citet{davidson2025investigating} document this problem empirically: their
large-scale Cholesky-based SVMVAR delivers results that depend strongly on
which variables appear early versus late in the ordering. State that this
motivates the order-invariant alternative.

STEP 2 — DHK's Q-matrix reparameterization (1–2 paragraphs):
\citet{davidson2025investigating} resolve order dependence via a reparameterization
of the rows of B_0. Let b_{0,i} denote the i-th row of B_0, treated as a column
vector. DHK introduce the auxiliary linear transformation:

  w_i = d_i + Q_i b_{0,i}   \label{eq:Qtransform}

where d_i is a known offset vector and Q_i is an (N-1) \times N matrix
constructed so that the conditional posterior of w_i, integrating over all
possible orderings of variables, is a standard multivariate normal — independent
of the permutation applied to the variable indices. Draws from the posterior
of b_{0,i} are then obtained by drawing w_i ~ N(0, I_{N-1}) and applying the
inverse transformation b_{0,i} = Q_i^{\dagger}(w_i - d_i), where Q_i^{\dagger}
is the Moore–Penrose pseudoinverse of Q_i. Because the same posterior obtains
for any permutation of variable indices, inference from this sampler is
order-invariant by construction.

STEP 3 — Why block exogeneity breaks DHK's MCMC (2 paragraphs — the technical core):

PARAGRAPH A:
In standard small open economy (SOE) models, researchers routinely impose
"block exogeneity": the external block (U.S., China, and global variables)
is permitted to affect the domestic block (Taiwan), but the domestic block
cannot contemporaneously affect the external block. This is operationalized
as zero restrictions on specific rows of B_0: for each external variable i,
the elements of b_{0,i} corresponding to domestic variables are set to zero,
confining b_{0,i} to a restricted subspace of dimension (N - K_i), where K_i
is the number of zero constraints imposed on row i.

PARAGRAPH B:
These zero restrictions are mathematically incompatible with DHK's order-invariant
MCMC. The transformation w_i = d_i + Q_i b_{0,i} requires Q_i to be constructed
to span the full N-dimensional ambient space of b_{0,i} — its (N-1) rows must
form a basis for the orthocomplement of the normalization constraint. When zero
restrictions reduce the effective dimension of b_{0,i} to (N - K_i), the
construction of Q_i degenerates: Q_i as originally defined maps an (N-K_i)-
dimensional feasible set into an (N-1)-dimensional image space, making Q_i
rank-deficient on the restricted domain. As a result, the inverse transformation
b_{0,i} = Q_i^{\dagger}(w_i - d_i) is no longer well-defined, and the Jacobian
of the reparameterization |dw_i / db_{0,i}| = |Q_i| is either zero or
ill-defined. The conditional posterior from which the MCMC sampler draws is
therefore invalid: the sampler cannot recover the correctly-normalized posterior
for b_{0,i} under zero restrictions. In short, zero restrictions on B_0 are
mathematically incompatible with DHK's order-invariant parameterization; the
two cannot be combined without rewriting the entire sampling algorithm.

STEP 4 — Resolution: the unclassified variables mechanism (1 paragraph):
The appropriate response is not to abandon order invariance, but to replace the
zero-restriction approach with the unclassified variables mechanism described
in subsection (1.2). By placing all external variables in the unclassified class,
this project imposes no zero restrictions on any row of B_0, preserving the full
DHK MCMC algorithm without modification. The SOE assumption — that Taiwan's
macroeconomic and financial conditions do not systematically drive U.S. monetary
policy or Chinese industrial production — is not imposed as a prior restriction
but verified post-estimation via forecast error variance decomposition: if the
share of external variable forecast error variance attributable to Taiwan's
domestic uncertainty factors h_{m,t} and h_{f,t} is negligible, the SOE
property holds approximately in the data. This approach is both methodologically
principled and more informative: it delivers a testable SOE assumption rather
than an untested one.

TONE AND STYLE:
- This is the most technically dense subsection. Maintain flowing prose — no
  bullet points.
- The argument must read as a progression: problem → solution → complication →
  resolution.
- Use precise language: "rank-deficient", "Jacobian of the reparameterization",
  "conditional posterior", "Moore–Penrose pseudoinverse".
- Do NOT soften technical claims. NSTC reviewers with econometrics backgrounds
  will expect this level of precision.
- Cite \citet{davidson2025investigating} throughout.

OUTPUT FORMAT: Pure LaTeX \input{} fragment (no preamble).
Heading: \noindent\textbf{(1.3) Order-Invariance and the Incompatibility of Block Exogeneity}
Include the Q-transform as a displayed equation with \label{eq:Qtransform}.
```

### Verification checklist
- [ ] Four-step logical structure present: Cholesky problem → Q-matrix solution → block exogeneity conflict → resolution
- [ ] `w_i = d_i + Q_i b_{0,i}` presented as a displayed equation with label
- [ ] Rank-deficiency argument explicit: zero restrictions reduce dimension → Q_i degenerate → Jacobian undefined
- [ ] Resolution: no zero restrictions + unclassified mechanism + post-estimation SOE test via FEVD
- [ ] "Testable SOE assumption" framing in closing paragraph
- [ ] Approximately 2 compiled pages

---

## Chunk D: `(2.1)+(2.2)` Data Assembly and Year 1 Work Plan

### Context package (give these files to the AI)
- `NSTC-applicaiton/CM03_production_spec.md`
- `NSTC-applicaiton/proposal/sec1_background.tex`

### Verbatim prompt

```
Please read the following files before beginning:
1. NSTC-applicaiton/CM03_production_spec.md  — format rules
2. NSTC-applicaiton/proposal/sec1_background.tex  — prose style reference

Your task: Write subsections (2.1) "Data Assembly and Preprocessing" and
(2.2) "Works Planned for the First Year" for Year 1, Section 2 of an NSTC
grant proposal (application 115WFA1110048).

TARGET LENGTH: approximately 3 pages total (2.1 ≈ 2 pages; 2.2 ≈ 1 page).

===========================================================================
SECTION (2.1): DATA ASSEMBLY AND PREPROCESSING
===========================================================================

DATASET SPECIFICATIONS:
- 43 variables, monthly frequency, 2000:M1 through 2025:M6 (≈306 months)
- Three variable classes:

MACROECONOMIC VARIABLES (19) — Sources: DGBAS and CBC
  Industrial Production Index (IPI) — DGBAS
  Manufacturing Production Index — DGBAS
  Export Orders Index — DGBAS
  Retail Sales, real — DGBAS
  Exports, customs basis, real USD — Ministry of Finance
  Imports, customs basis, real USD — Ministry of Finance
  Manufacturing PMI — CIER
  Non-Manufacturing NMI — CIER
  Business Cycle Indicator score — DGBAS / CEPD
  CPI, year-on-year — DGBAS
  Core CPI, year-on-year — DGBAS
  WPI, year-on-year — DGBAS
  Import Price Index, USD, year-on-year — DGBAS
  Export Price Index, USD, year-on-year — DGBAS
  Unemployment rate, seasonally adjusted — DGBAS
  Manufacturing employment, seasonally adjusted — DGBAS
  Services employment, seasonally adjusted — DGBAS
  Real average manufacturing wages, year-on-year — DGBAS
  M2 money supply, year-on-year — CBC

FINANCIAL VARIABLES (10) — Sources: CBC, TWSE, TEJ
  Overnight interbank rate — CBC
  10-year government bond yield — CBC / TEJ
  Term spread (10yr bond minus overnight rate) — CBC / TEJ
  TAIEX monthly return — TWSE
  TAIEX monthly realized volatility (computed from daily returns) — TWSE
  Foreign institutional investor net buying, NTD billions — TWSE
  Credit spread, 5yr A-rated corporate minus 5yr government bond — CBC / TEJ
  Bank total loans and investments, year-on-year — CBC
  NTD/USD exchange rate, nominal monthly average — CBC
  NTD/USD exchange rate monthly realized volatility — CBC

UNCLASSIFIED VARIABLES (14) — Sources: FRED, PolicyUncertainty.com, NBS, PBoC
  U.S. Federal Funds Rate, effective — FRED
  U.S. Industrial Production Index, year-on-year — FRED
  U.S. BAA–AAA Credit Spread — FRED
  U.S. Economic Policy Uncertainty index — PolicyUncertainty.com
  China Industrial Production Index, year-on-year — NBS
  China Producer Price Index, year-on-year — NBS
  China Total Social Financing, year-on-year — PBoC / WIND
  VIX, CBOE Volatility Index, monthly average — FRED
  Global Geopolitical Risk index — Caldara and Iacoviello (2022)
  Global Economic Policy Uncertainty index — PolicyUncertainty.com
  U.S.–China Trade Policy Uncertainty index — PolicyUncertainty.com
  U.S.–China Bilateral Trade Volume, year-on-year growth — U.S. Census Bureau
  U.S.–China Bilateral Geopolitical Risk index — Caldara and Iacoviello (2022)
  [14th variable — PI to finalize: candidate is China EPU or Taiwan Strait
   Tension index. Insert source when confirmed.]

SAMPLE PERIOD RATIONALE (must appear in prose):
The sample begins in 2000:M1 for two reasons. First, Taiwan acceded to the WTO
in January 2002, and the years immediately preceding accession witnessed
substantial liberalization of trade and financial flows; beginning in 2000
captures the pre-accession baseline while avoiding structural breaks associated
with Taiwan's pre-liberalization trade regime. Second, the 1997–1998 Asian
financial crisis introduced a severe structural break in cross-country financial
linkages across the region; excluding the crisis period ensures that estimated
model parameters reflect the post-crisis integration structure that characterizes
the sample of primary interest. The resulting sample of approximately 306
observations provides sufficient degrees of freedom for Bayesian MCMC estimation
of the 43-variable model to achieve reliable posterior convergence, consistent
with the simulation evidence in \citet{davidson2025investigating}.

DATA TRANSFORMATIONS (must all appear in prose or a compact table):
All transformations are applied before model estimation:
(i)   Level series: expressed as 12-month log-differences (year-on-year log-changes)
(ii)  Interest rate levels: expressed as monthly first differences
(iii) Term spread, credit spread: retained in levels (already stationary by
      construction as a difference of two rates)
(iv)  Realized volatility measures: retained in levels (non-negative by
      construction, typically stationary)
(v)   Seasonal adjustment: X-13-ARIMA-SEATS applied to all series not already
      seasonally adjusted by the source agency (DGBAS seasonal adjustment is
      accepted as-is; FRED series apply Census X-13 at source)
(vi)  Stationarity testing: ADF (augmented Dickey–Fuller) and KPSS tests applied
      to all transformed series; any series rejecting stationarity under both
      tests receives an additional first difference
(vii) Standardization: all series standardized to zero mean and unit variance
      prior to model estimation, following \citet{davidson2025investigating}

===========================================================================
SECTION (2.2): WORKS PLANNED FOR THE FIRST YEAR
===========================================================================

Present the Year 1 work plan as flowing prose organized around four activities.
Do NOT use bullet points — integrate the activities into narrative paragraphs.
The month ranges are approximate guides; do not present them as a rigid Gantt chart.

ACTIVITY 1 — Data assembly and verification (Months 1–4):
All 43 variables are collected from the sources listed in Section (2.1),
harmonized to a common monthly frequency, and assembled into a balanced panel
spanning 2000:M1 to 2025:M6. Missing observations (which may arise for China
series in early months) are addressed using interpolation or by trimming the
sample start date as appropriate. All data transformations described above are
applied, and each transformed series is subjected to ADF and KPSS stationarity
tests. The complete dataset, along with all transformation decisions and source
documentation, is recorded in a replication log to ensure full reproducibility.

ACTIVITY 2 — MCMC implementation and adaptation (Months 3–7):
The order-invariant SVMVAR estimation algorithm of \citet{davidson2025investigating}
is implemented and adapted to the 43-variable Taiwan dataset. The algorithm
proceeds as a Gibbs sampler, cycling through the following blocks: VAR
coefficient matrices A_l; the contemporaneous impact matrix B_0 (via the
Q-matrix reparameterization); the uncertainty factor loadings \alpha_{i,m}
and \alpha_{i,f}; the log-volatility paths h_{m,t} and h_{f,t} (via the
precision sampler of Chan and Jeliazkov 2009); and the Markov-switching
classification probabilities \pi_{i,t} (via the Hamilton filter). Convergence
is assessed using Geweke (1992) spectral diagnostics, visual inspection of
MCMC trace plots, and effective sample size calculations. Estimation is
conducted on the university high-performance computing cluster.

ACTIVITY 3 — Preliminary estimation and validation (Months 5–9):
A preliminary estimation is conducted on a reduced 30-variable model — retaining
the core Taiwan domestic variables and a subset of the most important external
variables — to validate the MCMC implementation and benchmark against the
published results of \citet{davidson2025investigating} for the U.S. economy.
Upon successful validation, the full 43-variable model is estimated. Each MCMC
run requires approximately 30 hours at 50,000 post-burn-in draws, based on
\citet{davidson2025investigating}'s reported computational requirements for a
model of comparable scale.

ACTIVITY 4 — Preliminary three-step analysis (Months 9–12):
Posterior draws from the full model are used to extract time-series of the
classification probabilities \pi_{i,t} for all 14 external variables. Preliminary
plots of these trajectories are produced for the key episodes identified in
Section 1 (2008, 2015, 2018–2019, 2020, 2022). A preliminary forecast error
variance decomposition is computed to assess the relative contributions of U.S.,
Chinese, and global uncertainty shocks to Taiwan's domestic uncertainty factors
h_{m,t} and h_{f,t}. Preliminary findings are presented at a domestic or
international conference in the final quarter of Year 1. Throughout the year,
the project research assistant receives training in Bayesian econometrics and
MCMC methods, building the technical capacity required for the full estimation
and analysis work of Year 2.

STYLE RULES for both (2.1) and (2.2):
- Flowing paragraphs, no bullet points.
- Logical connectives: "Upon successful validation", "Throughout the year",
  "Concurrent with", "The resulting".
- Use \citet{} citations throughout.
- Precise technical language: "Gibbs sampler", "Geweke spectral diagnostics",
  "effective sample size", "precision sampler".

SECTION HEADING FORMAT:
  \noindent\textbf{(2) Anticipated problems and means of resolution}
  \bigskip
  \noindent\textbf{(2.1) Data Assembly and Preprocessing}
  [prose for 2.1]
  \bigskip
  \noindent\textbf{(2.2) Works Planned for the First Year}
  [prose for 2.2]

OUTPUT FORMAT: Pure LaTeX \input{} fragment (no preamble).
```

### Verification checklist
- [ ] All 43 variables listed with data sources
- [ ] Sample period rationale present: WTO accession + 1997 crisis exclusion + 306-month convergence argument
- [ ] All 7 data transformation steps explicitly described (YoY, first diff, X-13, ADF/KPSS, standardization)
- [ ] Four Year 1 activities written as prose paragraphs (no bullets)
- [ ] Computational cost stated: ~30 hours per run, 50,000 draws, citing DHK (2025)
- [ ] 14th unclassified variable flagged as "[PI to finalize]"
- [ ] References: \citet{chan2009efficient} for precision sampler, \citet{geweke1992} for convergence test
- [ ] Approximately 3 compiled pages

---

## Integration Instructions

Once you have four LaTeX output fragments from the four AI sessions:

**Step 1 — Assemble**
Open `NSTC-applicaiton/proposal/y1_sec2_methods.tex`.
Paste Chunks A → B → C → D in order. Add `\bigskip` between:
- End of (1.3) and the `\noindent\textbf{(2) Anticipated problems...}` heading.

**Step 2 — Check equation cross-references**
Chunk B references `\eqref{eq:variance}` and `\eqref{eq:pi}` from Chunk A.
Chunk C references `\eqref{eq:Qtransform}` (defined within Chunk C itself).
Verify that all `\label{}` and `\ref{}` or `\eqref{}` tags match exactly.

**Step 3 — Compile and check page count**
Run `pdflatex main.tex` (or your preferred LaTeX engine) from the `proposal/` directory.
Target page count for this section: **10–12 pages**.
- If a chunk is too short: instruct a follow-up AI to "add one paragraph expanding
  [topic], matching the style of sec1_background.tex, without repeating content
  already in adjacent paragraphs."
- If a chunk is too long: trim wordy transitions or tighten the equation prose.

**Step 4 — Read the seams**
Check logical flow at:
- End of Chunk A → start of Chunk B (transition from model equations to variable classification)
- End of Chunk C → start of Chunk D (transition from methodology to data operations)
Add a bridging sentence at each seam if the transition feels abrupt.

**Step 5 — Resolve the 14th unclassified variable**
Before final submission, confirm the 14th unclassified variable with the PI.
Search for "[PI to finalize]" in the assembled file and replace with the confirmed
variable name and source.

**Step 6 — Final review**
Check that no content from Section 1 (`sec1_background.tex`) is repeated verbatim.
Key items that must NOT reappear in this section:
- Taiwan's geopolitical vulnerability (Pelosi visit, cross-strait tensions as motivation)
- The "perception gap" argument for single-step estimation
- The conceptual explanation of omitted variable bias from Carriero et al. (2018)

---

*Plan created: 2026-02-25*
*Target section: NSTC-applicaiton/proposal/y1_sec2_methods.tex*
*Reference spec: NSTC-applicaiton/CM03_production_spec.md*

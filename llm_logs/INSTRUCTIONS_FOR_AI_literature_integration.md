# Instructions for AI: Integrating Literature into Research Proposal Introduction Motivation

**Task ID**: Literature-Integration-Proposal-Intro
**Created**: 2025-11-14
**Priority**: High
**Estimated Time**: 2-3 hours for AI execution

---

## 🎯 Task Objective

**Goal**: Revise the Introduction section (specifically the Motivation subsection) of `research_proposal.tex` to accurately reflect the **correct research direction** established on 2025-11-14, using evidence from two comprehensive literature review files.

**Current Problem**: The existing `research_proposal.tex` has **gone off-track**. It over-emphasizes:
- Taiwan's unique geopolitical position
- Semiconductor industry importance
- Being "caught in crossfire" as a political/economic narrative
- Research question: "Which uncertainty (macro vs financial) dominates Taiwan?" (this is DHK's US question, NOT ours)

**Correct Direction**: The research should focus on:
- **Transmission channel identification**: Which channel (macro vs. financial) do external shocks use?
- **Time-varying mechanisms**: How do transmission channels evolve over time?
- **Novel methodological application**: Using "unclassified variables" to identify channels (not asking DHK's question)

---

## 📚 Required Reading (IN THIS ORDER)

### CRITICAL: Read These First to Understand Research Direction

1. **`llm_logs/2025-11-14_research_direction_and_milestones.md`**
   - Section: "Core Research Direction (Finalized)"
   - Section: "Core Innovation: What Makes This NOT Country Replication"
   - Section: "Critical 'Do NOT' List"
   - **Why**: Understand what the research IS and IS NOT about

2. **`CLAUDE.md`**
   - Section: "Core Research Question"
   - Section: "Critical Methodological Decisions (from 11-08 Discussion)"
   - Section: "Comparison with DHK (2025)"
   - **Why**: Understand methodological positioning

3. **`README.md`**
   - Section: "Key Innovation: Exploiting 'Unclassified Variables' for Transmission Channel Identification"
   - Section: "Three-Step Research Design"
   - **Why**: Understand the analysis framework

### Literature Review Files (Evidence Source)

4. **`literature/uncertainty_shock_literature.md`**
   - 40+ papers on global uncertainty shock literature
   - **Key sections to extract**:
     - Phase 2: Small Open Economy & Uncertainty Transmission (lines ~95-163)
     - Phase 3: Decomposition of Uncertainty Types (lines ~165-213)
     - "Key Gaps and Opportunities for Taiwan Research" (lines ~319-440)

5. **`literature/taiwan_specific_uncertainty_literature.md`**
   - Taiwan-specific empirical studies
   - **Key sections to extract**:
     - Phase 1: Taiwan Uncertainty Shock Studies (lines ~25-201)
     - Phase 2: US-China Trade War Impact on Taiwan (lines ~203-280)
     - "Research Gaps Specific to Taiwan" (lines ~559-663)

### Current Proposal (To Be Revised)

6. **`research_proposal.tex`**
   - Lines 31-52: Current Introduction Motivation section
   - **Problem**: Completely misaligned with correct research direction

---

## ❌ Common Mistakes to AVOID

### Mistake 1: Over-Emphasizing Taiwan's Uniqueness
**Wrong**: "Taiwan is caught in the crossfire between US and China, with unique geopolitical risks and semiconductor dominance making it globally critical..."

**Why Wrong**: This frames the research as "Taiwan special case study" rather than methodological innovation

**Correct**: "Taiwan, as a representative small open economy simultaneously exposed to both US and Chinese shocks, provides an ideal setting to test whether external uncertainty transmission channels can be objectively identified using DHK (2025)'s time-varying classification framework..."

### Mistake 2: Asking the Wrong Research Question
**Wrong**: "Which type of uncertainty—macroeconomic or financial—has a greater impact on Taiwan's economy?"

**Why Wrong**: This is DHK (2025)'s US question, not ours

**Correct**: "Through which transmission channel—macroeconomic or financial—do external uncertainty shocks from the US and China primarily impact Taiwan? And how does this transmission mechanism evolve over time?"

### Mistake 3: Positioning as Country Replication
**Wrong**: "We apply DHK (2025) to Taiwan to see if their US findings generalize..."

**Why Wrong**: This is weak motivation; "country replication" has low publication value

**Correct**: "We exploit DHK (2025)'s 'unclassified variables' feature in a novel way: by placing all external shock sources in the unclassified category, the model can objectively identify whether these shocks transmit through macro or financial channels—a question DHK did not address and traditional methods cannot answer without arbitrary restrictions..."

### Mistake 4: Over-Using Dramatic Events as Motivation
**Wrong**: "The 2025 TAIEX crash of 9.7%, the 2022 Pelosi visit, and Taiwan's semiconductor dominance illustrate..."

**Why Wrong**: Reads like journalism, not academic research; loses focus on methodological contribution

**Correct**: Event studies can be mentioned as **evidence** in literature review, but NOT as primary motivation

### Mistake 5: Failing to Distinguish from DHK (2025)
**Wrong**: Treating the research as "DHK for Taiwan" without clearly articulating the different question

**Why Wrong**: Reviewers will reject as mere replication

**Correct**: Explicitly state in first paragraph of motivation: "While DHK (2025) ask which uncertainty dominates in the US, we ask which transmission channel external shocks use in a small open economy—a fundamentally different question enabled by a novel application of their framework..."

---

## ✅ Correct Structure for Revised Introduction Motivation

### Paragraph 1: Research Question and Novel Application
**Purpose**: Immediately establish this is NOT country replication

**Required Elements**:
- One-sentence research question: "Through which channels do external shocks transmit?"
- Distinction from DHK: "Unlike DHK (2025) who ask which uncertainty dominates domestically, we ask..."
- Novel application: "By placing external shocks in 'unclassified' category, we leverage time-varying classification to identify transmission channels..."

**Evidence to Use**:
- From `uncertainty_shock_literature.md`: Chan-Koop-Yu (2024) order-invariance innovation (lines ~78-87)
- From `CLAUDE.md`: "Comparison with DHK (2025)" table

**Example Opening**:
```latex
\textbf{First}, this research exploits a novel application of Davidson, Hou, and Koop (2025)'s methodological framework to address a question they did not examine: through which transmission channels—macroeconomic (real economy) or financial (capital markets)—do external uncertainty shocks impact small open economies? While DHK (2025) investigate which type of uncertainty (macro vs. financial) dominates within the US economy, we leverage their "unclassified variables" feature in an innovative way: by treating all external shock sources (US, China, global indicators) as unclassified, the model can objectively identify whether these shocks transmit through macro or financial channels, and how this mechanism evolves over time. Traditional VAR models cannot answer this question without imposing arbitrary block exogeneity restrictions that DHK's order-invariant framework was designed to avoid \citep{chan2024large, davidson2025investigating}.
```

### Paragraph 2: Methodological Justification (Large Models Matter)
**Purpose**: Establish why 40+ variables are needed

**Required Elements**:
- DHK finding: small models (30 variables) produce biased results
- Implication for Taiwan: External variables cannot be omitted
- Evidence: Sin (2015) used only 6 variables, likely suffered omitted variable bias

**Evidence to Use**:
- From `uncertainty_shock_literature.md` lines ~329-333 ("Large vs. Small Models")
- From `taiwan_specific_uncertainty_literature.md` lines ~562-566 ("Lack of Large-Scale VAR Models")
- Sin (2015) details from `taiwan_specific_uncertainty_literature.md` lines ~57-76

**Template**:
```latex
\textbf{Second}, methodological rigor requires large-scale modeling to avoid omitted variable bias. DHK (2025) demonstrate that models with approximately 30 variables yield substantially different—and incorrect—conclusions compared to models with 43 variables. For Taiwan, a small open economy where domestic fluctuations are predominantly driven by external factors \citep{sin2015economic, thailand2021}, omitting US, Chinese, and global variables would severely bias estimates. The most rigorous existing Taiwan study, \citet{sin2015economic}, employs only six variables (four Taiwan plus two China variables) in a structural VAR. While pioneering, this small-scale approach likely suffers from the omitted variable bias that DHK's large-model framework was designed to overcome. Furthermore, \citet{thailand_uncertainty2021} find that for small open economies, "global uncertainty delivers deeper and more long-lasting effects compared to within-country uncertainty," underscoring the necessity of explicitly modeling external shock sources.
```

### Paragraph 3: Time-Varying Transmission Channels (Core Innovation)
**Purpose**: Explain why time-varying classification matters for transmission channel identification

**Required Elements**:
- Why transmission channels can shift over time (different episodes: 2008 financial crisis vs. 2018 trade war)
- Why this matters for policy (different channels require different policy tools)
- Evidence: Brianti (2025) shows macro uncertainty allows output/inflation co-stabilization; financial shocks require trade-offs

**Evidence to Use**:
- From `uncertainty_shock_literature.md` lines ~189-202 (Brianti 2025 policy implications)
- From `taiwan_specific_uncertainty_literature.md` lines ~434-439 (Thailand study: external shocks deeper/longer)
- From `uncertainty_shock_literature.md` lines ~132-144 (Small open economy vulnerabilities)

**Template**:
```latex
\textbf{Third}, understanding transmission channels is more policy-relevant for small open economies than merely knowing impact magnitudes. \citet{brianti2025} demonstrates that macroeconomic uncertainty shocks trigger deflationary patterns, allowing central banks to simultaneously stabilize output and inflation, whereas financial shocks may require policymakers to trade off price stability against output stabilization. For the Central Bank of China (Taiwan), knowing whether external shocks (e.g., US Federal Reserve rate hikes, US-China trade tensions) transmit primarily through macroeconomic channels (affecting export demand and production) or financial channels (affecting capital flows and exchange rates) directly determines the appropriate policy toolkit. Moreover, this transmission mechanism may shift across different episodes: the 2008 global financial crisis likely featured predominantly financial transmission, while the 2018 US-China trade war plausibly operated through macroeconomic channels. DHK (2025)'s time-varying classification framework is ideally suited to identify these regime-dependent dynamics, which previous Taiwan studies imposing fixed classifications \citep{sin2015economic} cannot capture.
```

### Paragraph 4: Research Gap and Dual US-China Exposure
**Purpose**: Establish empirical gap specific to Taiwan context

**Required Elements**:
- No study has quantitatively decomposed transmission channels for dual US-China exposure
- Taiwan as ideal case: cannot decouple from either economy
- But DO NOT over-dramatize geopolitics

**Evidence to Use**:
- From `uncertainty_shock_literature.md` lines ~349-354 ("Dual Exposure to US and China Not Quantified")
- From `taiwan_specific_uncertainty_literature.md` lines ~589-596 ("Dual Exposure to US and China Not Quantified")
- Firm-level evidence from `taiwan_specific_uncertainty_literature.md` lines ~236-250

**Template**:
```latex
\textbf{Fourth}, Taiwan's simultaneous economic dependence on both the United States and China creates a unique empirical opportunity to study dual external exposures. Existing literature examines US uncertainty spillovers to emerging markets \citep{carriere2013large} and Chinese uncertainty spillovers to Asia \citep{sin2015economic} separately, but no study quantitatively decomposes transmission channels for an economy simultaneously exposed to both powers. Firm-level evidence shows that Taiwanese companies' revenue and profitability in China declined sharply after 2012, with further deterioration following the 2018 trade war onset \citep{taiwaninsight2025}, while Taiwan simultaneously became the US's 7th largest trading partner by 2024. Unlike other emerging markets that can partially decouple from either economy, Taiwan's deep integration with both US and Chinese supply chains makes transmission channel identification particularly salient for policy design. Quantifying whether US Federal Funds Rate shocks transmit through financial channels (capital flow reversals) versus macroeconomic channels (export demand), and whether this differs from Chinese Industrial Production shocks, addresses a critical gap in the small open economy literature.
```

---

## 📊 Evidence Integration Strategy

### From `uncertainty_shock_literature.md`

**Use These Findings**:
1. **Lines ~78-92**: Chan-Koop-Yu (2024) order-invariance solves variable ordering problem
   - **Where to use**: Paragraph 1, establishing methodological foundation

2. **Lines ~189-202**: Brianti (2025) - macro vs financial uncertainty have different policy implications
   - **Where to use**: Paragraph 3, policy relevance justification

3. **Lines ~329-333**: DHK demonstrate large models (40+ var) necessary vs. small models (30 var)
   - **Where to use**: Paragraph 2, large model justification

4. **Lines ~349-354**: Gap - no study quantifies dual US-China exposure with transmission channels
   - **Where to use**: Paragraph 4, research gap

5. **Lines ~399-409**: Why this is NOT country replication
   - **Where to use**: Paragraph 1, distinguish from DHK

**Do NOT Over-Use**:
- Specific Taiwan events (2025 TAIEX crash, Pelosi visit) - these belong in literature review, NOT motivation
- Semiconductor industry importance - mention briefly if at all

### From `taiwan_specific_uncertainty_literature.md`

**Use These Findings**:
1. **Lines ~57-76**: Sin (2015) used only 6 variables, shows China EPU affects Taiwan
   - **Where to use**: Paragraph 2, as example of small-model bias

2. **Lines ~562-572**: Methodological gaps - no large VAR, no order-invariant method for Taiwan
   - **Where to use**: Paragraph 2, research gap

3. **Lines ~577-582**: No macro vs financial transmission channel decomposition for Taiwan
   - **Where to use**: Paragraph 3, substantive gap

4. **Lines ~589-601**: Dual US-China exposure not quantified
   - **Where to use**: Paragraph 4, empirical gap

5. **Lines ~236-250**: Firm-level evidence of Taiwan-China-US triangular relationship
   - **Where to use**: Paragraph 4, as supporting evidence (briefly)

**Do NOT Include in Motivation**:
- Detailed event studies (Pelosi visit bond yields) - save for literature review
- TAIEX volatility comparisons with Korea - not central to research question
- Geopolitical risk discussions beyond brief acknowledgment

---

## 🎨 Stylistic Guidelines

### Tone
- **Academic and measured**: Avoid journalistic drama ("caught in crossfire of great power competition")
- **Methodologically focused**: Emphasize innovation in applying DHK framework
- **Policy-relevant**: Connect to Central Bank needs, but don't oversell urgency

### Structure
- **Each paragraph = one key motivation point**
- **First sentence of each paragraph states the point clearly**
- **Citations integrated naturally, not parenthetical dumps**
- **Build logical progression**: Method → Gap → Contribution

### Length
- **Total motivation section**: 3-4 pages (approximately 1,200-1,600 words)
- **Each paragraph**: 300-400 words
- **Balance**: 50% methodological motivation, 30% empirical gap, 20% policy relevance

### Citations
- **Cite DHK (2025) at least 5-6 times**: Establish foundation
- **Cite small open economy literature**: 3-4 citations (Thailand, Korea studies)
- **Cite Taiwan-specific studies**: 2-3 citations (Sin 2015, Huang et al. 2019)
- **Cite Brianti (2025), Caldara et al.**: For policy implications of uncertainty types

---

## 🔍 Self-Check Questions Before Finalizing

Ask yourself these questions. If any answer is "yes," revise:

1. ❌ Does the motivation make it sound like the research question is "which uncertainty dominates Taiwan?" → **WRONG QUESTION**
2. ❌ Does it emphasize Taiwan's geopolitical uniqueness more than methodological innovation? → **WRONG FRAMING**
3. ❌ Could a reviewer read this and think "this is just DHK applied to Taiwan"? → **NEED CLEARER DISTINCTION**
4. ❌ Does it mention semiconductors or specific crises as primary motivation? → **TOO JOURNALISTIC**
5. ❌ Are citations to Taiwan events (2025 crash, Pelosi) in the motivation section? → **BELONGS IN LIT REVIEW**

✅ **Correct Check**:
- Does the first paragraph clearly state this is about "transmission channel identification"?
- Is it clear why placing external variables in "unclassified" is a novel application?
- Is the distinction from DHK (2025) crystal clear in the first 2 paragraphs?
- Is the policy relevance tied to "which channel" rather than "how much impact"?
- Are Taiwan-specific elements framed as "empirical opportunity" not "unique special case"?

---

## 📤 Expected Output Format

### Deliverable 1: Revised Motivation Section (LaTeX)
```latex
\subsection{Research Motivation}

[Paragraph 1: Novel application of DHK framework for transmission channel identification]
[300-400 words]

\textbf{First}, this research exploits a novel application...
[Include 2-3 citations: DHK 2025, Chan-Koop-Yu 2024]

[Paragraph 2: Large model necessity and Taiwan-specific omitted variable bias risk]
[300-400 words]

\textbf{Second}, methodological rigor requires large-scale modeling...
[Include 3-4 citations: DHK 2025, Sin 2015, Thailand study]

[Paragraph 3: Time-varying transmission channels and policy relevance]
[300-400 words]

\textbf{Third}, understanding transmission channels is more policy-relevant...
[Include 2-3 citations: Brianti 2025, CBC policy documents]

[Paragraph 4: Research gap - dual US-China exposure empirical opportunity]
[300-400 words]

\textbf{Fourth}, Taiwan's simultaneous economic dependence on both...
[Include 2-3 citations: Taiwan firm studies, spillover literature]
```

### Deliverable 2: Summary of Changes Made
Provide a brief bullet list:
- Changed research question from [old] to [new]
- Added emphasis on transmission channel identification
- Removed over-emphasis on [geopolitics/semiconductors/specific events]
- Added citation to [X, Y, Z] from literature files
- Clarified distinction from DHK (2025) by explaining [novel application]

### Deliverable 3: Citation Additions Needed
List any papers mentioned in the two literature files that should be added to the bibliography:
- Brianti (2025) - if not already present
- Thailand uncertainty study (2021) - get full citation
- Specific Taiwan firm study - verify citation details

---

## 🚀 Execution Workflow

### Step 1: Read and Internalize (30 minutes)
1. Read `2025-11-14_research_direction_and_milestones.md` sections listed above
2. Read `CLAUDE.md` sections listed above
3. Read `README.md` sections listed above
4. **Confirm understanding**: Can you articulate in one sentence what makes this NOT country replication?

### Step 2: Extract Evidence (45 minutes)
1. Open `literature/uncertainty_shock_literature.md`
2. Extract key findings from lines indicated above
3. Open `literature/taiwan_specific_uncertainty_literature.md`
4. Extract key findings from lines indicated above
5. Create evidence map: [Motivation Point] → [Supporting Evidence from Literature]

### Step 3: Draft Revision (60 minutes)
1. Write Paragraph 1 (Novel application)
2. Write Paragraph 2 (Large model justification)
3. Write Paragraph 3 (Time-varying channels, policy relevance)
4. Write Paragraph 4 (Dual exposure empirical gap)

### Step 4: Self-Check (20 minutes)
1. Run through "Self-Check Questions" above
2. Verify all "Do NOT" mistakes are avoided
3. Check citation balance and integration

### Step 5: Finalize (15 minutes)
1. Format in LaTeX
2. Prepare summary of changes
3. List any bibliography additions needed

---

## 📋 Quick Reference Card

**Core Research Question**: "Through which transmission channel (macro vs. financial) do external U.S.-China shocks impact Taiwan, and how does this evolve over time?"

**NOT**: "Which uncertainty dominates Taiwan?" (that's DHK's US question)

**Core Innovation**: Placing external shocks in "unclassified" → model identifies transmission channels objectively

**NOT**: Applying DHK to Taiwan to replicate their findings

**Key Distinction from DHK**:
- **They ask**: Which uncertainty type affects US?
- **We ask**: Which channel do external shocks use for Taiwan?

**Evidence Priority**:
1. Methodological foundation (DHK, Chan-Koop-Yu, Brianti)
2. Small open economy gaps (Thailand, Korea, Sin 2015 limitations)
3. Dual US-China exposure gap
4. Policy relevance (CBC needs)

**Avoid**:
- Over-emphasizing geopolitics, semiconductors
- Journalistic tone with dramatic events
- Positioning as country replication

---

## ✅ Success Criteria

Your revision is successful if:

1. ✅ A reviewer reading this motivation would understand this is about "transmission channel identification," not "uncertainty impact measurement"
2. ✅ The distinction from DHK (2025) is crystal clear by end of first paragraph
3. ✅ The novel application of "unclassified variables" is prominently featured
4. ✅ Taiwan is framed as "empirical opportunity" not "special unique case"
5. ✅ Policy relevance is tied to "which channel to respond to" not just "uncertainty matters"
6. ✅ All claims are supported by citations to the two literature files
7. ✅ No dramatic events or geopolitical narratives dominate the motivation
8. ✅ Logical flow: Method innovation → Large model need → Time-varying channels → Dual exposure gap

---

**Good luck! This task is critical to ensuring the research proposal accurately reflects the correct research direction established on 2025-11-14.**

*Document Version: 1.0*
*Last Updated: 2025-11-14*

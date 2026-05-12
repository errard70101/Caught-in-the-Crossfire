# v2 Proposal Introduction Redesign

**Date:** 2026-05-12
**Target file:** `NSTC-applicaiton/proposal/v2/main.tex`, Section 1 (Research Project Background), lines 21–302
**Status:** Design — awaiting user review before implementation planning

## 1. Goal

Restructure Section 1 of the v2 proposal to:

1. Eliminate the heavy duplication currently present in subsection 1.1 (three near-identical drafts mashed together across lines 23–114).
2. Eliminate the overlap between paragraph 3 of 1.1 (three-year sketch) and subsection 1.6 (three-year overview).
3. Eliminate the citation redundancy between subsection 1.3 (Challenges) and subsection 1.4 (Literature) by merging them into one challenge-driven section.
4. Reduce total length from ~280 lines to ~215 lines without losing argumentative substance.

## 2. Design Approach (Option B: Tighter, 4 subsections)

Keep paragraphs 1–3 of the current 1.1 verbatim (lines 23–36). Replace everything after with four subsections:

- 1.2 Research Questions
- 1.3 Open Challenges and Relation to the Literature
- 1.4 Research Design and Main Contributions
- 1.5 Three-Year Roadmap

## 3. Content Specification by Subsection

### 3.1 Paragraphs 1–3 (retained from current 1.1, lines 23–36)

**Status:** Keep verbatim.

- Para 1 (line 25): Taiwan exposed to US (financial / monetary / tech), China (trade / production / cross-strait), global semiconductor. Figure `tw_taifex_vix_bloom_style.pdf` references major uncertainty episodes.
- Para 2 (line 34): Identification difficulty — same external shock reaches Taiwan through multiple channels (capital flows, exchange rates, export demand, production expectations); US tightening and China slowdown examples.
- Para 3 (line 36): Project asks how external uncertainty from US/China/global operates in Taiwan; structure is source → channel → mechanism; Year 1 / Year 2 / Year 3 sketch in one sentence each.

### 3.2 Subsection 1.2 Research Questions (~20 lines)

**Function:** Convert the meta-question from para 3 into three sharp, testable RQs. Do not explain why each is hard (that is 1.3's job).

**Structure:**

- One-sentence framing: "The project is organized around three layered research questions."
- Numbered list of three RQs, each followed by **at most one sentence** of clarification:
  - **RQ1 (source):** Which external uncertainty source — US, China, or global — contributes most to Taiwan's domestic macroeconomic and financial uncertainty?
  - **RQ2 (channel):** Do these external shocks transmit primarily through macroeconomic or financial channels, and does the dominant channel vary over time?
  - **RQ3 (mechanism):** Can the time-varying empirical channels be linked to structural frictions — collateral constraints, risk-premium channels, or working-capital frictions?

**Diff vs. current 1.2 (lines 116–149):** Drop the three explanatory paragraphs after the numbered list (lines 132–149). Their content is absorbed by 1.3 (motivation for the methodology) and 1.4 (how the design addresses each layer).

### 3.3 Subsection 1.3 Open Challenges and Relation to the Literature (~80 lines)

**Function:** This is the key innovative subsection of Option B. Each methodological challenge is paired with the literature that has engaged it and the gap that remains. Literature appears **in service of challenges**, not as a standalone strand review.

**Structure:** Brief framing paragraph + four challenge paragraphs + closing summary.

**Framing (2–3 sentences):** Existing literature offers building blocks but no integrated approach to identifying Taiwan's external-uncertainty transmission channel. The following four challenges define what is missing.

**Challenge C1 — External and domestic uncertainty are intertwined (OVB):**
- Cite: `bloom2009impact`, `bloom2014fluctuations`, `baker2016measuring`, `handley2022tpu` (single-indicator / small-model precedents); `carriero2018measuring` (critique of small-model OVB).
- Cite (Taiwan-specific precedent): `huang2021taiwan` constructs a Baker–Davis-style text-based EPU index for Taiwan and uses a Diebold–Yilmaz spillover model to examine linkages with US and Japan EPU indices; finds roughly half of Taiwan's economic uncertainty originates domestically with significant US and Japan spillover.
- Gap: Even this Taiwan-focused work delivers a single scalar EPU index and a reduced-form spillover decomposition. It does not (a) separate Taiwan's domestic uncertainty into macroeconomic vs financial components, (b) identify whether external uncertainty enters through macro or financial channels, or (c) jointly estimate uncertainty and its macroeconomic effects in one model.
- Delta: This project builds a unified monthly dataset that combines Taiwan domestic anchors with US, Chinese, and global drivers, and estimates two latent uncertainty factors (macro / financial) jointly with their VAR dynamics — addressing all three gaps above.

**Challenge C2 — Identification in large VARs:**
- Cite: Cholesky-ordering dependence; small-open-economy block-exogeneity tradition (too rigid).
- Cite: `davidson2025investigating` — OI-SVMVAR resolves ordering dependence and avoids pre-imposed zero restrictions.
- Gap: OI-SVMVAR has not yet been adapted to the small-open-economy external-shock problem; its unclassified block mechanism has been used to classify ambiguous domestic variables, not to identify external transmission channels.
- Delta: This project repurposes the unclassified block to place external drivers there and let the data classify their channel.

**Challenge C3 — Two-step bias / generated-regressor problem:**
- Cite: `carriero2018measuring` on measurement-error and model-consistency problems in two-step uncertainty designs.
- Cite: `davidson2025investigating` for joint first-stage estimation.
- Gap: Even with joint first-stage estimation, downstream structural validation in the literature typically uses point estimates of the latent uncertainty factor, ignoring the posterior distribution.
- Delta: This project develops an MCMC-integrated wedge-level local projection that propagates the first-stage posterior into the third-year mechanism test.

**Challenge C4 — Reduced-form evidence does not reveal mechanism:**
- Cite: `chari2007business` (BCA prototype); subsequent BCA literature on small open economies (efficiency / external wedges).
- Gap: BCA has been used as a positive accounting device but not connected to uncertainty-driven second-moment risk corrections. There is no existing wedge-projection framework that converts a financial-channel uncertainty response into testable wedge signatures.
- Delta: This project derives how competing mechanisms (collateral / risk-premium / working-capital) project into distinct BCA wedge signatures.

**Closing summary (2–3 sentences):** These four gaps jointly define the methodological contribution of the three-year project. The next subsection describes how the research design addresses each gap.

**Diff vs. current 1.3 + 1.4 (lines 151–226):** Merge the two subsections. Drop the three-strand literature framing in current 1.4. Move the macro-uncertainty literature (Bloom / Baker / Handley) into C1 instead of giving it a separate strand. Keep all current citations.

### 3.4 Subsection 1.4 Research Design and Main Contributions (~50 lines)

**Function:** Map the four gaps in 1.3 to the project's design choices and list the four contributions (1 project-level + 3 year-specific).

**Structure:** Two chunks — Design (3 paragraphs) and Contributions (4 bullets or numbered).

**Design Para A — OI-SVMVAR justification (addresses C1, C2, C3):**
- Why OI-SVMVAR: jointly estimates uncertainty and its macroeconomic effects, accommodates a large information set, order-invariant in large VAR systems, avoids block-exogeneity.

**Design Para B — Key adaptation: external drivers as unclassified block (addresses C2's gap):**
- Domestic real-side variables anchor the macro uncertainty factor; domestic financial variables anchor the financial uncertainty factor.
- External drivers (US monetary, Chinese real-side, global financial, geopolitical risk, trade-policy uncertainty) sit in the unclassified block.
- Posterior classification probabilities provide a data-driven, time-varying measure of the operative transmission channel.

**Design Para C — Wedge-projection and MCMC-integrated LP (addresses C4 and C3's residual gap):**
- Year 2 derives how second-moment risk corrections in a nonlinear structural model project into BCA wedges.
- Year 3 estimates wedge-level local projections that take the full posterior of the Year 1 uncertainty factors as input.

**Contributions:**

- **Project-level (methodological):** Repurposing the OI-SVMVAR unclassified-block mechanism from classifying ambiguous domestic variables to identifying the channel through which external shocks enter a small open economy.
- **Year 1 (empirical identification):** Monthly Taiwan external-uncertainty dataset + Taiwan-specific macro/financial uncertainty factors + time-varying classification probabilities for external drivers.
- **Year 2 (theoretical mapping):** Wedge-projection framework that converts transmission-channel evidence into testable structural predictions (collateral / risk-premium load on investment wedge; working-capital loads on labor wedge).
- **Year 3 (empirical validation):** MCMC-integrated mechanism test that propagates first-stage posterior into the final validation, mitigating generated-regressor bias.

**Diff vs. current 1.5 (lines 228–270):** Drop the opening paragraph that re-describes OI-SVMVAR mechanics (overlaps with 1.3 C2). Reorganize the design into three explicitly gap-mapped paragraphs. Keep the 1 + 3 contribution structure.

### 3.5 Subsection 1.5 Three-Year Roadmap (~30 lines, prose)

**Function:** Concrete deliverables per year plus inter-year dependencies. Prose, not table (per user preference). Does NOT re-narrate the story (already in para 3 and 1.4).

**Structure:** Four paragraphs.

**Para 1 — Year 1 deliverables:** (a) Taiwan monthly external-uncertainty dataset (variable list, time span, sources detailed in §3); (b) posterior distribution of macro / financial uncertainty factors from OI-SVMVAR estimation; (c) time-varying classification probabilities for external drivers; (d) main IRFs and FEVDs.

**Para 2 — Year 2 deliverables:** (a) Mathematical derivation of the wedge-projection framework (second-moment risk correction → BCA wedges); (b) wedge signatures for competing frictions (collateral / risk-premium / working-capital); (c) characterization of efficiency wedge and external wedge in the small-open-economy setting. **Explicit note on parallelism:** Year 2 theoretical derivation can proceed in parallel with Year 1 empirical work; it does not require Year 1 outputs.

**Para 3 — Year 3 deliverables:** (a) Taiwan BCA wedges time series; (b) MCMC-integrated wedge-level local projection results; (c) comparative mechanism indicator (posterior odds or model averaging weights); (d) policy interpretation. **Explicit note on dependencies:** Year 3 depends on both Year 1's posterior draws and Year 2's wedge-signature hypotheses as inputs.

**Para 4 — Integration closing (3–4 sentences):** Tie the three years back to RQ1–RQ3 and state that the integrated final deliverable is a three-dimensional mapping (source × channel × mechanism) of Taiwan's external-uncertainty transmission.

**Diff vs. current 1.6 (lines 272–302):** Replace the three "each year asks ..." narrative paragraphs (which duplicate para 3) with four "each year produces ..." deliverable paragraphs that include parallelism / dependency notes — information not in para 3.

## 4. Migration Plan (Current → New)

| Current location | Content | Action |
|---|---|---|
| Lines 23–36 (1.1 paras 1–3) | Motivation + identification + 3-year sketch | **Keep verbatim** |
| Lines 38–82 (1.1 black-text middle) | Older draft duplicating paras 1–3 | **Delete** |
| Lines 84–114 (1.1 blue-text tail) | Yet another draft duplicating same points | **Delete** |
| Lines 116–130 (1.2 numbered RQs) | Three RQs | **Keep, drop blue color markup** |
| Lines 132–149 (1.2 explanations) | One paragraph per RQ explaining why hard | **Delete** — content absorbed into 1.3 |
| Lines 151–185 (1.3 four challenges) | C1–C4 prose | **Rewrite into new 1.3** with embedded citations |
| Lines 187–226 (1.4 literature strands) | Three strands + four advances | **Merge into new 1.3**; "four advances" content moves to new 1.4 contributions |
| Lines 228–270 (1.5 design + contributions) | OI-SVMVAR + adaptation + 1+3 contributions | **Rewrite into new 1.4**, dropping mechanics overlap with 1.3 C2 |
| Lines 272–302 (1.6 three-year overview) | Three "each year asks ..." paras | **Rewrite into new 1.5** as deliverable paragraphs with parallelism/dependency notes |

## 5. Style Cleanup

- Remove all `\textcolor{blue}{...}` revision markup throughout Section 1; the new draft is the canonical version.
- Keep all current citations (`bloom2009impact`, `bloom2014fluctuations`, `baker2016measuring`, `handley2022tpu`, `carriero2018measuring`, `davidson2025investigating`, `chari2007business`). Verify they exist in the bib file.
- Verify the figure reference `fig:taiwan-vix-events` still points to the existing `figures/tw_taifex_vix_bloom_style.pdf`.

## 6. Length Estimate

| Subsection | Estimated lines |
|---|---|
| Paras 1–3 (kept) | ~35 |
| 1.2 Research Questions | ~20 |
| 1.3 Open Challenges and Relation to the Literature | ~80 |
| 1.4 Research Design and Main Contributions | ~50 |
| 1.5 Three-Year Roadmap | ~30 |
| **Total Section 1** | **~215** |

Reduction from current ~280 lines is roughly 25%, driven primarily by deduplication in 1.1 and consolidation of 1.3 + 1.4.

## 7. Out of Scope

- No changes to Sections 2–5 (Preliminary Progress, Year 1, Year 2, Year 3) or the appendix sections.
- No changes to the bibliography file (only verify citations resolve).
- No new figures or tables.
- No changes to the abstract or front matter.

## 8. Implementation Note

The next step after user approval of this spec is to invoke the writing-plans skill to produce a step-by-step implementation plan covering: (1) extracting and preserving paras 1–3, (2) drafting each new subsection in order, (3) deleting superseded blocks, (4) recompiling and visually checking the PDF, (5) running a duplication / citation audit.

## 9. Deviations During Implementation (2026-05-12)

During execution, the user decided that a dedicated §1.2 Research Questions subsection would either restate paragraph 3 of §1.1 or trespass into the following subsections. The subsection was therefore **dropped**, and the three keywords `source` / `channel` / `mechanism` were italicized in paragraph 3 of §1.1 so the RQ structure remains visible.

The final implemented structure (after renumbering) is:

- 1.1 Motivation and Taiwan Context (paras 1–3 retained verbatim, with emph on the three keywords)
- 1.2 Open Challenges and Relation to the Literature (corresponds to §3.3 of this spec)
- 1.3 Research Design and Main Contributions (corresponds to §3.4 of this spec)
- 1.4 Three-Year Roadmap (corresponds to §3.5 of this spec)

The §3.2 Research Questions section of this spec is therefore historical; it was not implemented. All other sections of this spec were implemented as specified.

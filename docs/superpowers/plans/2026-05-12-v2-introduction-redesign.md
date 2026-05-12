# v2 Proposal Introduction Redesign — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restructure Section 1 of `NSTC-applicaiton/proposal/v2/main.tex` from 6 redundant subsections (~280 lines) into 5 focused subsections (~215 lines), per the spec at `docs/superpowers/specs/2026-05-12-v2-introduction-redesign.md`.

**Architecture:** Incremental top-to-bottom rewrite, anchored on subsection header strings (not line numbers, which shift). After each subsection rewrite: recompile with XeLaTeX, visually check the rendered PDF, commit. The final two tasks are global audits (`\textcolor{blue}` cleanup, citation/duplication audit).

**Tech Stack:** LaTeX (XeLaTeX via `latexmk`), AEA `.bst` bibliography style, `references.bib` in `NSTC-applicaiton/proposal/`.

---

## Pre-flight

**Spec reference:** `docs/superpowers/specs/2026-05-12-v2-introduction-redesign.md` — every task below cites the relevant spec section.

**Target file:** `NSTC-applicaiton/proposal/v2/main.tex`

**Build command:** `cd NSTC-applicaiton/proposal/v2 && latexmk -xelatex main.tex` (or equivalent — check existing `.latexmkrc` if present)

**Anchor strings** (used in Edit operations to avoid line-number drift):
- `\subsection{Motivation and Taiwan Context}`
- `\subsection{Research Questions}`
- `\subsection{Empirical and Methodological Challenges}`
- `\subsection{Relation to the Literature}`
- `\subsection{Research Design and Main Contributions}`
- `\subsection{Overview of the Three-Year Project}`
- `\section{Preliminary Progress and Feasibility}` (Section 1 ends just before this)

---

## Task 1: Baseline snapshot and verification

**Files:**
- Read: `NSTC-applicaiton/proposal/v2/main.tex`
- Read: `NSTC-applicaiton/proposal/references.bib`

- [ ] **Step 1: Verify current Section 1 boundaries are intact**

Run: `grep -n "^\\\\section\|^\\\\subsection" NSTC-applicaiton/proposal/v2/main.tex | head -20`

Expected: Section 1 starts at `\section{Research Project Background}` and contains subsections "Motivation and Taiwan Context", "Research Questions", "Empirical and Methodological Challenges", "Relation to the Literature", "Research Design and Main Contributions", "Overview of the Three-Year Project". Section 2 starts at `\section{Preliminary Progress and Feasibility}`.

- [ ] **Step 2: Compile baseline PDF**

Run: `cd NSTC-applicaiton/proposal/v2 && latexmk -xelatex main.tex`

Expected: Successful compilation, `main.pdf` updated. Record the current PDF page count for Section 1 (will compare at the end).

- [ ] **Step 3: Confirm `huang2021taiwan` exists in references.bib**

Run: `grep -A 2 "huang2021taiwan" NSTC-applicaiton/proposal/references.bib`

Expected: Entry present (added in prior step), with title "An Economic Policy Uncertainty Index for Taiwan" and author "Huang, Yu-Lieh and Yeh, Jin-Huei and Chen, Chung-Chi".

- [ ] **Step 4: Commit pre-flight checkpoint (optional, only if dirty state needs preserving)**

If there are uncommitted changes unrelated to this plan, stash them first.

---

## Task 2: Clean up 1.1 Motivation duplicates (keep paragraphs 1–3 only)

**Spec reference:** §3.1 (retained paragraphs), §4 (migration plan rows 1–3).

**Files:**
- Modify: `NSTC-applicaiton/proposal/v2/main.tex`

**What to delete:** Everything between paragraph 3 (ends at line 36, the paragraph that begins "This project therefore asks how external uncertainty shocks...") and the next subsection `\subsection{Research Questions}` (currently at line 116).

This block contains two duplicate drafts (black-text version at lines 44–82, blue-text version at lines 84–114) that restate paragraphs 1–3 with different wording. All content in this block is duplicated in paragraphs 1–3 and must be deleted.

- [ ] **Step 1: Locate the deletion block**

Run: `sed -n '36,116p' NSTC-applicaiton/proposal/v2/main.tex | head -90`

Expected: Output starts with the closing of paragraph 3 (ends with "tests which wedge signature best matches the response to the uncertainty shocks identified in Year 1."), followed by ~80 lines of duplicate prose, ending just before `\subsection{Research Questions}`.

- [ ] **Step 2: Delete the duplicate block via Edit**

Use the Edit tool to replace the entire duplicate region with a single blank line. The `old_string` should start with the closing line of paragraph 3 (so the anchor is unique) and end with the line just before `\subsection{Research Questions}`. The `new_string` should retain only the paragraph 3 closing line plus one blank line.

- [ ] **Step 3: Verify paragraph 3 is intact and 1.2 immediately follows**

Run: `grep -n "wedge signature\|\\\\subsection{Research Questions}" NSTC-applicaiton/proposal/v2/main.tex | head -5`

Expected: The paragraph-3 closing line appears once, followed shortly by `\subsection{Research Questions}` with no intervening duplicate prose.

- [ ] **Step 4: Recompile and check**

Run: `cd NSTC-applicaiton/proposal/v2 && latexmk -xelatex main.tex`

Expected: Compiles cleanly. Open `main.pdf`, page 1 of Section 1 should now show only paragraphs 1–3 of Motivation followed immediately by 1.2 Research Questions.

- [ ] **Step 5: Commit**

```bash
git add NSTC-applicaiton/proposal/v2/main.tex
git commit -m "proposal v2: remove duplicate drafts from §1.1 Motivation"
```

---

## Task 3: Rewrite 1.2 Research Questions

**Spec reference:** §3.2.

**Files:**
- Modify: `NSTC-applicaiton/proposal/v2/main.tex`

**Target length:** ~20 lines.

**Required content:**
- One framing sentence: "The project is organized around three layered research questions."
- Numbered list of 3 RQs, each followed by at most one sentence of clarification:
  - **RQ1 (source):** Which external uncertainty source — US, China, or global — contributes most to Taiwan's domestic macroeconomic and financial uncertainty?
  - **RQ2 (channel):** Do these external shocks transmit primarily through macroeconomic or financial channels, and does the dominant channel vary over time?
  - **RQ3 (mechanism):** Can the time-varying empirical channels be linked to structural frictions — collateral constraints, risk-premium channels, or working-capital frictions?
- No long explanatory paragraphs after the list. The "why each is hard" goes into the new 1.3.

**Forbidden content (in this subsection):**
- Explanations of OVB, ordering dependence, two-step bias, or BCA mechanism — those belong in 1.3 / 1.4.
- Any `\textcolor{blue}{...}` markup.

- [ ] **Step 1: Locate current 1.2**

Use Read on lines containing `\subsection{Research Questions}` through the line just before `\subsection{Empirical and Methodological Challenges}`.

- [ ] **Step 2: Draft replacement LaTeX prose**

Write the new 1.2 following the required content above. Use `\begin{enumerate}` ... `\end{enumerate}` for the numbered list. No `\textcolor{...}`.

- [ ] **Step 3: Replace via Edit**

Use Edit to swap the old 1.2 block for the new prose. The `old_string` anchor should include `\subsection{Research Questions}` to make it unique.

- [ ] **Step 4: Recompile and check**

Run: `cd NSTC-applicaiton/proposal/v2 && latexmk -xelatex main.tex`

Expected: Clean compile. PDF shows 1.2 as a short subsection (3 numbered RQs + brief framing).

- [ ] **Step 5: User review checkpoint**

Pause and show the rendered 1.2 to the user for prose-level review before committing. Iterate if requested.

- [ ] **Step 6: Commit**

```bash
git add NSTC-applicaiton/proposal/v2/main.tex
git commit -m "proposal v2: rewrite §1.2 Research Questions (tightened, no inline explanations)"
```

---

## Task 4: Merge old 1.3 + 1.4 into new 1.3 (Open Challenges and Relation to the Literature)

**Spec reference:** §3.3 (the key subsection of Option B).

**Files:**
- Modify: `NSTC-applicaiton/proposal/v2/main.tex`

**Target length:** ~80 lines. New subsection title: `Open Challenges and Relation to the Literature`.

**Required structure:**
1. Framing paragraph (2–3 sentences): existing literature offers building blocks but no integrated approach; four challenges define what is missing.
2. **C1 — External and domestic uncertainty intertwined (OVB):**
   - Cite single-indicator / small-model precedents: `bloom2009impact`, `bloom2014fluctuations`, `baker2016measuring`, `handley2022tpu`.
   - Cite critique: `carriero2018measuring`.
   - Cite Taiwan-specific precedent: `huang2021taiwan` — constructs Baker–Davis-style text-based EPU for Taiwan, uses Diebold–Yilmaz spillover model with US/Japan EPU; finds ~half of Taiwan uncertainty domestic, US/Japan spillover significant.
   - Gap statement (explicit three points): even `huang2021taiwan` (a) delivers a single scalar EPU index, (b) does not separate Taiwan domestic uncertainty into macro vs financial components, (c) does not identify whether external uncertainty enters Taiwan via macro or financial channels, and (d) does not jointly estimate uncertainty with macro effects in one model.
   - Delta: this project builds a unified monthly dataset combining TW domestic anchors with US, Chinese, and global drivers, and estimates two latent uncertainty factors jointly with VAR dynamics.
3. **C2 — Identification in large VARs:**
   - Note Cholesky ordering dependence and rigidity of small-open-economy block-exogeneity.
   - Cite `davidson2025investigating` — OI-SVMVAR resolves ordering dependence, avoids pre-imposed zero restrictions.
   - Gap: OI-SVMVAR's unclassified block has been used for ambiguous domestic variables, not for identifying external-shock transmission channels.
   - Delta: this project repurposes the unclassified block to place external drivers there and let the data classify their channel.
4. **C3 — Two-step bias / generated-regressor problem:**
   - Cite `carriero2018measuring` (measurement-error / model-consistency critique) and `davidson2025investigating` (joint first-stage estimation).
   - Gap: downstream structural validation in existing literature still typically uses point estimates of latent uncertainty factors, ignoring posterior.
   - Delta: MCMC-integrated wedge-level local projection propagates first-stage posterior into Year 3 mechanism test.
5. **C4 — Reduced-form evidence does not reveal mechanism:**
   - Cite `chari2007business` (BCA prototype) and subsequent small-open-economy BCA literature.
   - Gap: BCA has not been connected to uncertainty-driven second-moment risk corrections; no existing wedge-projection framework.
   - Delta: this project derives how collateral / risk-premium / working-capital mechanisms project into distinct BCA wedge signatures.
6. Closing summary (2–3 sentences): these four gaps jointly define the project's methodological contribution; next subsection describes the design.

**Forbidden content:**
- The "three strands of literature" framing from old 1.4 (Bloom strand / Davidson strand / BCA strand) — literature must appear *in service of challenges*, not as standalone strand survey.
- `\textcolor{blue}{...}` markup.

- [ ] **Step 1: Locate current 1.3 and 1.4**

Run: `grep -n "\\\\subsection{Empirical and Methodological Challenges}\|\\\\subsection{Relation to the Literature}\|\\\\subsection{Research Design and Main Contributions}" NSTC-applicaiton/proposal/v2/main.tex`

Expected: Three line numbers identifying the start of old 1.3, old 1.4, and old 1.5. Old 1.3 + 1.4 spans from the first to just before the third.

- [ ] **Step 2: Draft replacement LaTeX prose**

Write the new combined 1.3 following the required structure above. Use one paragraph per challenge (C1–C4), with citations woven in via `\citep{...}` or `\citet{...}` as natural.

- [ ] **Step 3: Replace via Edit**

Use Edit to swap the entire old 1.3 + 1.4 block for the new prose. Anchor the `old_string` on `\subsection{Empirical and Methodological Challenges}` and end just before `\subsection{Research Design and Main Contributions}`.

- [ ] **Step 4: Recompile and check all citations resolve**

Run: `cd NSTC-applicaiton/proposal/v2 && latexmk -xelatex main.tex 2>&1 | grep -i "warning\|undefined" | head`

Expected: No "Citation ... undefined" warnings for any of the cited keys (`huang2021taiwan`, `bloom2009impact`, `bloom2014fluctuations`, `baker2016measuring`, `handley2022tpu`, `carriero2018measuring`, `davidson2025investigating`, `chari2007business`).

- [ ] **Step 5: User review checkpoint**

Show the rendered 1.3 to the user. This is the most important subsection in the redesign — request feedback on argument flow, citation placement, and whether each gap statement is sharp enough.

- [ ] **Step 6: Commit**

```bash
git add NSTC-applicaiton/proposal/v2/main.tex
git commit -m "proposal v2: merge §1.3 Challenges and §1.4 Literature into challenge-driven §1.3"
```

---

## Task 5: Rewrite 1.4 Research Design and Main Contributions

**Spec reference:** §3.4.

**Files:**
- Modify: `NSTC-applicaiton/proposal/v2/main.tex`

**Target length:** ~50 lines. Title remains `Research Design and Main Contributions`.

**Required structure (two chunks):**

**Chunk A — Design (3 paragraphs, each gap-mapped):**
- Para A1 — OI-SVMVAR justification (addresses C1, C2, C3): joint estimation of uncertainty and macro effects, large information set, order-invariance, no block-exogeneity. Cite `davidson2025investigating`.
- Para A2 — Key adaptation: external drivers as unclassified block (addresses the C2 gap). Domestic real-side variables anchor macro factor; domestic financial variables anchor financial factor; external drivers (US monetary, Chinese real-side, global financial, geopolitical risk, trade-policy uncertainty) sit in the unclassified block. Posterior classification probabilities give time-varying channel identification.
- Para A3 — Wedge-projection + MCMC-integrated LP (addresses C4 and residual C3). Year 2 derives wedge-projection framework; Year 3 estimates wedge-level local projections that take the full Year 1 posterior as input.

**Chunk B — Contributions (1 project-level + 3 year-specific):**
- Project-level (methodological): repurposing OI-SVMVAR unclassified-block from classifying ambiguous domestic variables to identifying external-shock transmission channels in a small open economy.
- Year 1 (empirical identification): monthly TW external-uncertainty dataset + TW macro/financial uncertainty factors + time-varying classification probabilities.
- Year 2 (theoretical mapping): wedge-projection framework; collateral/risk-premium load on investment wedge, working-capital loads on labor wedge.
- Year 3 (empirical validation): MCMC-integrated mechanism test propagating first-stage posterior, mitigating generated-regressor bias.

**Forbidden content:**
- Re-describing OI-SVMVAR mechanics in depth (already covered in 1.3 C2).
- `\textcolor{blue}{...}` markup.

- [ ] **Step 1: Locate current 1.5**

Run: `grep -n "\\\\subsection{Research Design and Main Contributions}\|\\\\subsection{Overview of the Three-Year Project}" NSTC-applicaiton/proposal/v2/main.tex`

Expected: Two line numbers; old 1.5 spans between them.

- [ ] **Step 2: Draft replacement LaTeX prose**

Write the new 1.4 following the structure above. Contributions can be `\paragraph{Project-level contribution.}` style or `\textbf{...}` lead-ins, matching the current document convention.

- [ ] **Step 3: Replace via Edit**

Use Edit to swap the old 1.5 block for the new prose.

- [ ] **Step 4: Recompile and check**

Run: `cd NSTC-applicaiton/proposal/v2 && latexmk -xelatex main.tex`

Expected: Clean compile.

- [ ] **Step 5: User review checkpoint**

Show the rendered 1.4. Confirm the design ↔ challenge mapping reads cleanly and contributions are crisp.

- [ ] **Step 6: Commit**

```bash
git add NSTC-applicaiton/proposal/v2/main.tex
git commit -m "proposal v2: rewrite §1.4 Design and Contributions with explicit gap-mapping"
```

---

## Task 6: Rewrite 1.5 Three-Year Roadmap (prose, deliverable-focused)

**Spec reference:** §3.5.

**Files:**
- Modify: `NSTC-applicaiton/proposal/v2/main.tex`

**Target length:** ~30 lines. New subsection title: `Three-Year Roadmap`.

**Required structure (4 paragraphs):**

- Para 1 — Year 1 deliverables: (a) TW monthly external-uncertainty dataset (variable list, time span, sources detailed in §3); (b) posterior distribution of macro / financial uncertainty factors from OI-SVMVAR; (c) time-varying classification probabilities for external drivers; (d) main IRFs and FEVDs.
- Para 2 — Year 2 deliverables: (a) mathematical derivation of wedge-projection framework (second-moment risk correction → BCA wedges); (b) wedge signatures for competing frictions (collateral / risk-premium / working-capital); (c) characterization of efficiency and external wedges in SOE setting. **Explicit parallelism note:** Year 2 theoretical derivation proceeds in parallel with Year 1 empirical work — does not require Year 1 outputs.
- Para 3 — Year 3 deliverables: (a) Taiwan BCA wedges time series; (b) MCMC-integrated wedge-level local projection results; (c) comparative mechanism indicator (posterior odds or model averaging weights); (d) policy interpretation. **Explicit dependency note:** Year 3 depends on Year 1 posterior draws and Year 2 wedge-signature hypotheses.
- Para 4 — Integration closing (3–4 sentences): tie back to RQ1–RQ3; state final deliverable as a three-dimensional (source × channel × mechanism) mapping of TW external-uncertainty transmission.

**Forbidden content:**
- "Each year asks ..." narrative format (duplicates paragraph 3 of 1.1).
- `\textcolor{blue}{...}` markup.
- Tables (per user preference for prose).

- [ ] **Step 1: Locate current 1.6**

Run: `grep -n "\\\\subsection{Overview of the Three-Year Project}\|\\\\section{Preliminary Progress and Feasibility}" NSTC-applicaiton/proposal/v2/main.tex`

Expected: Two line numbers; old 1.6 spans between them.

- [ ] **Step 2: Draft replacement LaTeX prose**

Write the new 1.5 with title `\subsection{Three-Year Roadmap}` and four paragraphs as specified.

- [ ] **Step 3: Replace via Edit**

Use Edit to swap the old 1.6 block for the new prose.

- [ ] **Step 4: Recompile and check**

Run: `cd NSTC-applicaiton/proposal/v2 && latexmk -xelatex main.tex`

Expected: Clean compile. PDF should show Section 1 ending with the new 1.5, immediately followed by Section 2 (Preliminary Progress and Feasibility).

- [ ] **Step 5: User review checkpoint**

Show the rendered 1.5.

- [ ] **Step 6: Commit**

```bash
git add NSTC-applicaiton/proposal/v2/main.tex
git commit -m "proposal v2: rewrite §1.5 Three-Year Roadmap (deliverable-focused prose)"
```

---

## Task 7: Strip remaining `\textcolor{blue}{...}` markup in Section 1

**Spec reference:** §5 (style cleanup).

**Files:**
- Modify: `NSTC-applicaiton/proposal/v2/main.tex`

**Rationale:** Prior tasks should have removed most blue markup by replacing whole subsections, but the retained paragraphs 1–3 (lines 23–36) were originally clean and the new content was written without blue. This task verifies and removes any stragglers in Section 1.

- [ ] **Step 1: Search Section 1 for residual blue markup**

Run: `awk '/^\\section{Research Project Background}/,/^\\section{Preliminary Progress and Feasibility}/' NSTC-applicaiton/proposal/v2/main.tex | grep -n "textcolor"`

Expected: No matches. If matches appear, proceed to Step 2; otherwise skip to Step 4.

- [ ] **Step 2: Remove each `\textcolor{blue}{...}` wrapper**

For each match, use Edit to replace `\textcolor{blue}{TEXT}` with just `TEXT`. Be careful with nested braces.

- [ ] **Step 3: Re-run the search to confirm zero residue**

Run the same `awk | grep` from Step 1.

Expected: No matches.

- [ ] **Step 4: Recompile**

Run: `cd NSTC-applicaiton/proposal/v2 && latexmk -xelatex main.tex`

Expected: Clean compile.

- [ ] **Step 5: Commit (only if changes were made)**

```bash
git add NSTC-applicaiton/proposal/v2/main.tex
git commit -m "proposal v2: strip residual blue revision markup from §1"
```

---

## Task 8: Final audit — citations, duplication, length

**Spec reference:** §5 (citation verification), §6 (length estimate).

**Files:**
- Read-only: `NSTC-applicaiton/proposal/v2/main.tex`, `NSTC-applicaiton/proposal/references.bib`, `NSTC-applicaiton/proposal/v2/main.log`

- [ ] **Step 1: Verify all citations in new Section 1 resolve**

Run: `grep -i "undefined\|warning.*citation" NSTC-applicaiton/proposal/v2/main.log | head`

Expected: No undefined-citation warnings.

- [ ] **Step 2: Extract all `\cite*{}` keys in Section 1**

Run: `awk '/^\\section{Research Project Background}/,/^\\section{Preliminary Progress and Feasibility}/' NSTC-applicaiton/proposal/v2/main.tex | grep -oE "\\\\cite[a-z]*\\{[^}]+\\}" | sort -u`

Expected: Each cite key listed has a corresponding `@article{KEY,` or similar entry in `references.bib`. Cross-check manually.

- [ ] **Step 3: Duplication audit — search for phrases known to repeat**

Run: `awk '/^\\section{Research Project Background}/,/^\\section{Preliminary Progress and Feasibility}/' NSTC-applicaiton/proposal/v2/main.tex | grep -cE "monthly data|VIX|baker2016measuring"`

Expected (rough guide): each phrase appears no more than twice in Section 1. Investigate any phrase appearing three or more times.

- [ ] **Step 4: Length check**

Run: `awk '/^\\section{Research Project Background}/,/^\\section{Preliminary Progress and Feasibility}/' NSTC-applicaiton/proposal/v2/main.tex | wc -l`

Expected: Approximately 200–230 lines (spec target: ~215). If significantly higher, identify which subsection bloated.

- [ ] **Step 5: Visual check of rendered PDF**

Open `NSTC-applicaiton/proposal/v2/main.pdf` and confirm:
- Section 1 page count is shorter than the baseline measured in Task 1.
- No widow / orphan issues at subsection boundaries.
- Figure `tw_taifex_vix_bloom_style.pdf` still renders correctly in paragraph 1 of 1.1.

- [ ] **Step 6: Update PROGRESS.md to reflect the Section 1 redesign**

Open `NSTC-applicaiton/PROGRESS.md`. Add a dated entry noting: Section 1 of v2 main.tex restructured per spec `docs/superpowers/specs/2026-05-12-v2-introduction-redesign.md`; new subsections are 1.1 Motivation (paras 1–3 retained), 1.2 RQs, 1.3 Challenges + Literature merged, 1.4 Design + Contributions, 1.5 Three-Year Roadmap; added `huang2021taiwan` to bib.

- [ ] **Step 7: Final commit**

```bash
git add NSTC-applicaiton/proposal/v2/main.tex NSTC-applicaiton/PROGRESS.md
git commit -m "proposal v2: audit §1 redesign — verify citations, length, update PROGRESS"
```

---

## Self-Review Notes

**Spec coverage check:**
- Spec §3.1 (paras 1–3 retained) → Task 2 confirms via deletion of duplicates.
- Spec §3.2 (1.2 RQs) → Task 3.
- Spec §3.3 (1.3 merged Challenges + Literature) → Task 4 (the key task; includes `huang2021taiwan` in C1 per the updated spec).
- Spec §3.4 (1.4 Design + Contributions) → Task 5.
- Spec §3.5 (1.5 Three-Year Roadmap prose) → Task 6.
- Spec §4 (migration plan) → distributed across Tasks 2–6.
- Spec §5 (style cleanup: blue markup, citation verification, figure ref) → Tasks 7 and 8.
- Spec §6 (length estimate ~215 lines) → Task 8 Step 4.
- Spec §7 (out-of-scope items) → respected throughout; no Section 2–5 or bib edits beyond `huang2021taiwan`.

**Type / name consistency:**
- Subsection titles match across spec and plan: "Research Questions", "Open Challenges and Relation to the Literature", "Research Design and Main Contributions", "Three-Year Roadmap".
- Citation keys consistent: `huang2021taiwan`, `bloom2009impact`, `bloom2014fluctuations`, `baker2016measuring`, `handley2022tpu`, `carriero2018measuring`, `davidson2025investigating`, `chari2007business`.

**Placeholder scan:** No TBDs / TODOs in the plan body. Each task specifies exact files, exact anchor strings, exact commands.

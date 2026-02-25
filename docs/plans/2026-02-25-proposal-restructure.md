# Proposal Restructure Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Reorganize scattered `.tex` files into a modular `\input`-based LaTeX structure inside `NSTC-applicaiton/proposal/`, archive old drafts, and create empty shells for unwritten sections.

**Architecture:** A single `main.tex` holds the preamble and `\input` directives; each CM03 section lives in its own file. The `.bib` file moves into the proposal folder. Old drafts go to `archive/proposal_drafts/`.

**Tech Stack:** LaTeX (article class, natbib), existing `aea.bst` bibliography style.

---

### Task 1: Archive old draft versions

**Files:**
- Create dir: `archive/proposal_drafts/`
- Move: all old `.tex` files from root (see list below)

**Step 1: Create archive directory**

```bash
mkdir -p archive/proposal_drafts
```

**Step 2: Move old `.tex` files**

```bash
mv research_proposal.tex archive/proposal_drafts/
mv research_proposal_NSTC.tex archive/proposal_drafts/
mv research_proposal_NSTC_en.tex archive/proposal_drafts/
mv research_proposal_revised.tex archive/proposal_drafts/
mv research_proposal_v2.tex archive/proposal_drafts/
mv research_proposal_v3.tex archive/proposal_drafts/
```

Note: Do NOT move compiled artifacts (`.pdf`, `.aux`, `.log`, `.out`) — leave those at root or delete them. Do NOT move `research_proposal_v4.tex` yet — it stays until migration is verified.

**Step 3: Verify**

```bash
ls archive/proposal_drafts/
```
Expected: 6 `.tex` files listed.

**Step 4: Commit**

```bash
git add -A
git commit -m "archive: move old proposal draft versions to archive/proposal_drafts/"
```

---

### Task 2: Create proposal folder and migrate bibliography

**Files:**
- Create dir: `NSTC-applicaiton/proposal/`
- Create: `NSTC-applicaiton/proposal/references.bib` (copy from `research_proposal.bib`)

**Step 1: Create proposal directory**

```bash
mkdir -p NSTC-applicaiton/proposal
```

**Step 2: Copy bibliography**

```bash
cp research_proposal.bib NSTC-applicaiton/proposal/references.bib
```

Note: Copy (not move) for now — `research_proposal_v4.tex` still references `research_proposal.bib` at root.

**Step 3: Verify**

```bash
ls NSTC-applicaiton/proposal/
```
Expected: `references.bib`

---

### Task 3: Create sec1_background.tex

**Files:**
- Create: `NSTC-applicaiton/proposal/sec1_background.tex`
- Source: body content from `research_proposal_v4.tex` (lines 9–31, everything between `\begin{document}` and `\bibliographystyle`)

**Step 1: Create the file**

Extract only the body paragraphs — no preamble, no `\begin{document}`, no `\section{}` heading, no bibliography commands. The content is the 10 paragraphs of Section 1 text.

File should contain exactly:
```latex
Taiwan is deeply integrated with both the U.S. and Chinese economies...

[... all body paragraphs from v4.tex lines 9–31 ...]

...suggesting a broad research agenda extending well beyond the Taiwan case.

The remainder of this proposal proceeds as follows...
```

**Step 2: Verify**

Open `sec1_background.tex` and confirm:
- Starts with "Taiwan is deeply integrated..."
- Ends with "...second year."
- No `\documentclass`, `\begin{document}`, `\section{}`, or `\bibliography{}` lines present

---

### Task 4: Create empty shell files for unwritten sections

**Files:**
- Create: `NSTC-applicaiton/proposal/y1_sec2_methods.tex`
- Create: `NSTC-applicaiton/proposal/y1_sec3_results.tex`
- Create: `NSTC-applicaiton/proposal/y2_sec2_methods.tex`
- Create: `NSTC-applicaiton/proposal/y2_sec3_results.tex`
- Create: `NSTC-applicaiton/proposal/sec4_integrated.tex`

**Step 1: Create each shell file**

Each file contains only a `% TODO` comment indicating which session writes it per `CM03_production_spec.md`:

`y1_sec2_methods.tex`:
```latex
% Year 1 Section 2: Methods, procedures, and implementation schedule
% Sessions B + C per CM03_production_spec.md
% (1.1) The OI-SVMVAR Framework
% (1.2) Variable Classification and the Key Innovation
% (1.3) Order-Invariance and Why It Matters for Taiwan
% (2.1) Data Assembly and Preprocessing
% (2.2) Works planned for the first year
```

`y1_sec3_results.tex`:
```latex
% Year 1 Section 3: Anticipated results and achievements
% Session E per CM03_production_spec.md
```

`y2_sec2_methods.tex`:
```latex
% Year 2 Section 2: Methods, procedures, and implementation schedule
% Session D per CM03_production_spec.md
% (1.1) Steps 1-3: Full Three-Step Empirical Analysis (OI-SVMVAR)
% (1.2) A Small Open Economy DSGE Model with Financial Frictions
% (1.3) Bayesian Estimation and Impulse Response Matching
% (2.1) Computational and Estimation Challenges
% (2.2) Works planned for the second year
```

`y2_sec3_results.tex`:
```latex
% Year 2 Section 3: Anticipated results and achievements
% Session E per CM03_production_spec.md
```

`sec4_integrated.tex`:
```latex
% Section 4: Integrated research project
% Session E per CM03_production_spec.md
```

---

### Task 5: Create main.tex

**Files:**
- Create: `NSTC-applicaiton/proposal/main.tex`

**Step 1: Write main.tex**

Preamble per `CM03_production_spec.md` format spec:

```latex
\documentclass[12pt]{article}
\usepackage[margin=2cm]{geometry}
\usepackage{natbib}
\usepackage{amsmath, amssymb}
\usepackage{setspace}
\usepackage{xcolor}
\singlespacing
\setlength{\parindent}{1.5em}

\begin{document}

\section{Research project's background}
\input{sec1_background}

\bigskip
\noindent\textbf{The First Year}

\subsection{Methods, procedures, and implementation schedule}
\input{y1_sec2_methods}

\subsection{Anticipated results and achievements}
\input{y1_sec3_results}

\bigskip
\noindent\textbf{The Second Year}

\subsection{Methods, procedures, and implementation schedule}
\input{y2_sec2_methods}

\subsection{Anticipated results and achievements}
\input{y2_sec3_results}

\section{Integrated research project}
\input{sec4_integrated}

\bibliographystyle{../../../../aea}
\bibliography{references}

\end{document}
```

Note: `aea.bst` lives at the project root. The relative path `../../../../aea` goes up from `NSTC-applicaiton/proposal/` to root. Alternatively, copy `aea.bst` into the proposal folder.

**Step 2: Copy aea.bst into proposal folder (simpler than relative path)**

```bash
cp aea.bst NSTC-applicaiton/proposal/aea.bst
```

Then use `\bibliographystyle{aea}` in main.tex (no path needed).

---

### Task 6: Compile and verify

**Step 1: Compile**

```bash
cd NSTC-applicaiton/proposal
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

**Step 2: Verify output**

- `main.pdf` is generated
- Section 1 content appears correctly (all 10 paragraphs)
- No LaTeX errors in the log (warnings about missing sections are OK since shells are empty)
- Bibliography renders correctly

**Step 3: Open PDF to visually confirm**

```bash
open main.pdf
```

---

### Task 7: Archive research_proposal_v4.tex and commit

**Step 1: Move v4 to archive**

```bash
mv research_proposal_v4.tex archive/proposal_drafts/
```

**Step 2: Commit everything**

```bash
git add -A
git commit -m "refactor: modularize proposal into NSTC-applicaiton/proposal/ with \input structure"
```

---

## After This Plan

Next session: write `y1_sec2_methods.tex` (Year 1 Section 2) per Sessions B+C in `CM03_production_spec.md`.

Start with subsection (1.1): The OI-SVMVAR Framework.

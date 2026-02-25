# Design: Modular Proposal Structure

**Date**: 2026-02-25
**Status**: Approved by PI

## Goal

Reorganize scattered `.tex` files into a modular, `\input`-based LaTeX structure inside `NSTC-applicaiton/proposal/`, and archive old draft versions.

## Archive Structure

Old draft versions moved to `archive/proposal_drafts/` (kept for future reference):

- `research_proposal.tex`
- `research_proposal_NSTC.tex`
- `research_proposal_NSTC_en.tex`
- `research_proposal_revised.tex`
- `research_proposal_v2.tex`
- `research_proposal_v3.tex`

Note: Compiled artifacts (`.pdf`, `.aux`, `.log`, `.out`) are NOT archived.

## New Proposal Structure

```
NSTC-applicaiton/proposal/
  main.tex                  ← preamble + \input all sections
  sec1_background.tex       ← content migrated from research_proposal_v4.tex
  y1_sec2_methods.tex       ← Year 1 Section 2 (to be written)
  y1_sec3_results.tex       ← Year 1 Section 3 (to be written)
  y2_sec2_methods.tex       ← Year 2 Section 2 (to be written)
  y2_sec3_results.tex       ← Year 2 Section 3 (to be written)
  sec4_integrated.tex       ← Section 4 (to be written)
  references.bib            ← migrated from root research_proposal.bib
```

## main.tex Design

Preamble per `CM03_production_spec.md`:
- `\documentclass[12pt]{article}`
- `geometry` (2cm margins), `natbib`, `amsmath`, `amssymb`, `setspace`, `singlespacing`
- `\parindent{1.5em}`

Body:
```latex
\section{Research project's background}
\input{sec1_background}

\section*{The First Year}
\subsection{Methods, procedures, and implementation schedule}
\input{y1_sec2_methods}
\subsection{Anticipated results and achievements}
\input{y1_sec3_results}

\section*{The Second Year}
\subsection{Methods, procedures, and implementation schedule}
\input{y2_sec2_methods}
\subsection{Anticipated results and achievements}
\input{y2_sec3_results}

\section{Integrated research project}
\input{sec4_integrated}

\bibliographystyle{aea}
\bibliography{references}
```

## What Stays at Root (Temporary)

`research_proposal_v4.tex` remains at root until migration is confirmed correct, then archived.

## Next Step

Write Year 1 Section 2 (`y1_sec2_methods.tex`) per Sessions B+C of `CM03_production_spec.md`.

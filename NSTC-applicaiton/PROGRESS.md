# NSTC Grant Writing Progress Dashboard

**Application**: 115WFA1110048 - 3-year individual project (人文處)  
**Title**: Caught in the Crossfire: Time-Varying Transmission of U.S.-China Uncertainty to Taiwan  
**Page limit**: 45 pages (including references, figures, and tables)  
**Language**: English

> Start every grant-writing session here. This file tracks the current writing workflow and the source-of-truth hierarchy inside `NSTC-applicaiton/`.

## Current source-of-truth hierarchy

| Priority | File | Role |
|----------|------|------|
| 1 | `proposal/v2/main.tex` | Current master proposal draft |
| 2 | `CM03_production_spec.md` | Formatting and editorial rules |
| 3 | `proposal/data_appendix.tex` | Data appendix for the current proposal package |
| 4 | `proposal/references.bib` | Bibliography used by the current proposal package |
| 5 | `example/` | Formatting reference only |

## Current status

- The active proposal draft is **`NSTC-applicaiton/proposal/v2/main.tex`**.
- The current proposal structure is **three-year**.
- Section 1 (Research Project Background) was restructured on 2026-05-12 into four subsections: 1.1 Motivation and Taiwan Context, 1.2 Open Challenges and Relation to the Literature (challenge-driven, with literature woven into each of C1–C4), 1.3 Research Design and Main Contributions, 1.4 Three-Year Roadmap. The redesign spec is at `docs/superpowers/specs/2026-05-12-v2-introduction-redesign.md`. The Huang–Yeh–Chen (2021) Taiwan EPU paper was added to the bib as the Taiwan-specific precedent in §1.2 C1.
- Legacy split section files in `NSTC-applicaiton/proposal/` are **not** the source of truth for the current proposal text.
- Archived drafts under `archive/` remain historical reference only.

## Immediate workflow rules

1. Read this file first.
2. Edit proposal content in `proposal/v2/main.tex` unless a task explicitly targets another file.
3. Use `CM03_production_spec.md` for format, style, and document-hierarchy decisions.
4. Use `docs/variable_planning.md` for dataset details and sample-design questions.
5. Do not treat `proposal/y1_sec2_methods.tex` or other older split files as the current proposal draft unless the workflow is explicitly changed here.

## Current priorities

1. Keep auxiliary NSTC documents aligned with `proposal/v2/main.tex`.
2. Use `proposal/v2/main.tex` as the canonical statement of the current research design.
3. Only migrate or revise legacy split files after the consolidated `v2` draft requires it.

## Notes on related files

| File or folder | Current meaning |
|----------------|-----------------|
| `proposal/v2/main.tex` | Active draft |
| `proposal/data_appendix.tex` | Active supporting appendix |
| `proposal/sec1_background.tex`, `proposal/y1_sec2_methods.tex`, `proposal/y2_sec2_methods.tex`, etc. | Legacy split drafts; not current source of truth |
| `archive/proposal_drafts/` | Historical drafts |
| `llm_logs/2026-02-28_bca-nonlinear-uncertainty-accounting.md` | Historical methodology discussion, not current proposal source |

*Last updated: 2026-05-12*

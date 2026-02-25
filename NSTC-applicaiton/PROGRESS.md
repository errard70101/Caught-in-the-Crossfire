# NSTC Grant Writing Progress Dashboard

**Application**: 115WFA1110048 — 2-year individual project (人文處)
**Title**: Caught in the Crossfire: Time-Varying Transmission of U.S.-China Uncertainty to Taiwan
**Page limit**: 45 pages (including references, figures, tables)
**Language**: English
**Deadline**: Past due — complete as soon as possible

> **Start every grant writing session here.** This file is the single source of
> truth for section status, blockers, and next actions.
> Update the status column after each completed session.

---

## Section Status

| Section | Output File | Status | Est. Pages | Blocker |
|---------|-------------|--------|-----------|---------|
| CM02: Abstract (EN + ZH) | — | ❌ Not started | ~1 | Needs Sec 1–4 done first |
| **Sec 1: Background** | `proposal/sec1_background.tex` | ✅ Complete | ~7 | — |
| **Y1 Sec 2: Methods** | `proposal/y1_sec2_methods.tex` | 🔲 Plan ready | ~10–12 | 14th unclassified var (see Blockers) |
| Y1 Sec 3: Results | `proposal/y1_sec3_results.tex` | ❌ Not started | ~1 | — |
| Y2 Sec 2: Methods | `proposal/y2_sec2_methods.tex` | ❌ Not started | ~8–10 | — |
| Y2 Sec 3: Results | `proposal/y2_sec3_results.tex` | ❌ Not started | ~1 | — |
| Sec 4: Integrated Summary | `proposal/sec4_integrated.tex` | ❌ Not started | ~1–2 | — |
| References | `proposal/references.bib` | ⚠️ Partial | ~3–4 | Needs full cite list |

**Total written**: ~7 / ~35–40 target pages

---

## Immediate Next Actions

1. **[PI decision needed]** Confirm the 14th unclassified variable (see Blockers below)
2. Run Chunks A–D from `writing-plans/2026-02-25-y1-sec2-methods.md` (can be parallelized across AI sessions)
3. Assemble the four AI outputs into `proposal/y1_sec2_methods.tex`
4. Write `proposal/y1_sec3_results.tex` (~1 page, bullet points — fast)
5. Start `proposal/y2_sec2_methods.tex` (no writing plan yet — create one)

---

## Open Blockers / PI Decisions Needed

| # | Decision | Options | Notes |
|---|----------|---------|-------|
| 1 | **14th unclassified variable** | (a) China EPU index (PolicyUncertainty.com) OR (b) Taiwan Strait Tension index | Needed before running Chunk B and D prompts |
| 2 | **DHK log-volatility form** | (a) Random walk `h_{k,t} = h_{k,t-1} + ζ` OR (b) AR(1) with mean reversion | Verify against DHK (2025) paper before running Chunk A |
| 3 | **Computational resource** | (a) University HPC cluster OR (b) Cloud computing | Affects wording in Y1 Sec 2 (2.2) Activity 2 |
| 4 | **red-text sentence in Sec 1** | Remove or keep the `\textcolor{red}{...}` sentence on monthly data frequency | `sec1_background.tex` line 3, currently marked as unresolved |

---

## Writing Plans (AI Execution Prompts)

| Section | Plan File | Status |
|---------|-----------|--------|
| Y1 Sec 2: Methods | `writing-plans/2026-02-25-y1-sec2-methods.md` | ✅ Ready — 4 chunks, copy-paste prompts |
| All others | — | ❌ Not created yet |

---

## Key Reference Files

| File | Purpose |
|------|---------|
| `CM03_production_spec.md` | Format rules, page targets, quality standards — **read before writing any section** |
| `proposal/sec1_background.tex` | **Style reference** — all new sections must match this prose register |
| `example/113WIA0110259_BASE.PDF` | Target format example |
| `llm_logs/2025-11-08_discussion.md` | Core methodological decisions (variable classification, no block exogeneity, etc.) |
| `llm_logs/2025-11-16_svmvar-order-invariance-discussion.md` | Q-matrix singularity argument — source for Y1 Sec 2 (1.3) |

---

## Session Log

| Date | Session | Output | Notes |
|------|---------|--------|-------|
| 2026-02-24 | Section 1 writing | `sec1_background.tex` complete | 7 pages, approved |
| 2026-02-25 | Y1 Sec 2 planning | `writing-plans/2026-02-25-y1-sec2-methods.md` | 4-chunk AI plan ready |

---

*Last updated: 2026-02-25*

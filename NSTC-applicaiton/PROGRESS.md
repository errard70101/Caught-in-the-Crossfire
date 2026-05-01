# NSTC Grant Writing Progress Dashboard

**Application**: 115WFA1110048 — 3-year individual project (人文處)
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
| **Y2 Sec 2: Methods** | `proposal/y2_sec2_methods.tex` | ✅ Complete | ~6–8 | — |
| Y2 Sec 3: Results | `proposal/y2_sec3_results.tex` | ❌ Not started | ~1 | — |
| **Y3 Sec 2: Methods** | `proposal/y3_sec2_methods.tex` | ✅ Complete | ~4–5 | — |
| Y3 Sec 3: Results | `proposal/y3_sec3_results.tex` | ❌ Not started | ~1 | — |
| Sec 4: Integrated Summary | `proposal/sec4_integrated.tex` | ❌ Not started | ~1–2 | — |
| References | `proposal/references.bib` | ⚠️ Partial | ~3–4 | Needs full cite list |

**Total written**: ~7 / ~35–40 target pages

---

## Immediate Next Actions

1. Run Chunks B, C, and D from `writing-plans/2026-02-25-y1-sec2-methods.md` (can be parallelized across AI sessions)
2. Assemble the four AI outputs into `proposal/y1_sec2_methods.tex`
3. Write `proposal/y1_sec3_results.tex` (~1 page, bullet points — fast)
4. Write `proposal/y2_sec3_results.tex` (~1 page, bullet points — based on Y2 Sec 2 Competing Hypotheses framework)
5. Write `proposal/sec4_integrated.tex` (~1-2 pages)

---

## Open Blockers / PI Decisions Needed

| # | Decision | Options | Notes |
|---|----------|---------|-------|
| 1 | **~~14th unclassified variable~~** | Resolved | Added China EPU, Taiwan Strait Tension, and U.S. Regional TPU (Poilly & Tripier 2025). Total variables: 45. |
| 2 | **DHK log-volatility form** | (a) Random walk `h_{k,t} = h_{k,t-1} + ζ` OR (b) AR(1) with mean reversion | Verify against DHK (2025) paper before running Chunk A |
| 3 | **Computational resource** | (a) University HPC cluster OR (b) Cloud computing | Affects wording in Y1 Sec 2 (2.2) Activity 2 |
| 4 | **red-text sentence in Sec 1** | Remove or keep the `\textcolor{red}{...}` sentence on monthly data frequency | `sec1_background.tex` line 3, currently marked as unresolved |
| 5 | **~~SOE-BCA literature review~~** | Resolved | Shifted to Competing Hypotheses framework; Y2 Sec 2 written. |

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
| `CM03_production_spec.md` | Format rules, page targets, quality standards — **read before writing any section** (v2: Year 2 updated to SOE-BCA) |
| `proposal/sec1_background.tex` | **Style reference** — all new sections must match this prose register |
| `example/113WIA0110259_BASE.PDF` | Target format example |
| `llm_logs/2025-11-08_discussion.md` | Core methodological decisions (variable classification, no block exogeneity, etc.) |
| `llm_logs/2025-11-16_svmvar-order-invariance-discussion.md` | Q-matrix singularity argument — source for Y1 Sec 2 (1.3) |
| `llm_logs/2026-02-28_bca-nonlinear-uncertainty-accounting.md` | **[Historical]** Previous Year 2 framework discussion (SOE Nonlinear BCA). Kept for reference. |

---

## Session Log

| Date | Session | Output | Notes |
|------|---------|--------|-------|
| 2026-02-24 | Section 1 writing | `sec1_background.tex` complete | 7 pages, approved |
| 2026-02-25 | Y1 Sec 2 planning | `writing-plans/2026-02-25-y1-sec2-methods.md` | 4-chunk AI plan ready |
| 2026-02-28 | Year 2 framework shift | `CM03_production_spec.md` updated | Year 2 changed from SOE-DSGE+IRF Matching → SOE Nonlinear BCA; old spec archived to `archive/proposal_drafts/CM03_production_spec_v1_dsge.md` |
| 2026-04-11 | Year 2 final framework | `proposal/y2_sec2_methods.tex` | Framework shifted to Competing Hypotheses; successfully wrote Y2 Sec 2. BCA approach archived as historical option. |

---

*Last updated: 2026-04-17*
Empirical BCA Validation via MCMC local projections. Old Y2 Methods archived. |

---

*Last updated: 2026-05-01*

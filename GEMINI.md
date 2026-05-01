# Gemini CLI Context for "Caught in the Crossfire"

## Project Overview
This repository contains academic research materials for a study titled **"Caught in the Crossfire: Time-Varying Transmission of U.S.-China Uncertainty to Taiwan."** The project investigates how external uncertainty shocks from the United States and China transmit to Taiwan's economy, distinguishing between **macroeconomic channels** (real economy) and **financial channels** (financial markets).

**Methodological Foundation:** The research applies the **Order-Invariant Stochastic Volatility in Mean Vector Autoregression (OI-SVMVAR)** methodology based on the paper by **Davidson, Hou, and Koop (2025)**. 
**Key Innovation:** It exploits the "unclassified variables" feature from DHK (2025) by placing all external shock sources (U.S., China, global) into this category to dynamically identify their transmission channels.

*Note: The primary language for research context and discussions is Traditional Chinese (繁體中文), while code, technical documentation, and LaTeX proposals are generally in English.*

## Directory Overview
- `code/data_processing/`: **Automated data download pipeline** — Python scripts downloading from FRED, CBC, stat.gov.tw, OECD, BIS, TWSE, PolicyUncertainty.com. See `docs/variable_planning.md` for full variable-to-script mapping.
- `data/raw/`: Downloaded CSV files organized by category (`taiwan_macro/`, `taiwan_financial/`, `us/`, `china/`, `global/`). Git-ignored; re-download by running scripts.
- `docs/variable_planning.md`: **Master variable list** — 47 variables, 6 confirmed design decisions, download status tracker.
- `llm_logs/`: Records AI collaboration sessions, core methodological decisions, and discussions.
- `NSTC-applicaiton/`: Grant application materials for the National Science and Technology Council (NSTC), written in LaTeX.
- `literature/`: Comprehensive literature review materials on uncertainty shocks and Taiwan-specific studies.
- `references/`: Key reference papers (PDF format).
- `results/`, `figures/`, `tables/`: Standard research pipeline directories for analysis outputs.

## Information Architecture

1. **`PROGRESS.md`**: 🔥 **OPEN THIS FIRST, EVERY SESSION.** It links to:
   - **`CM03_production_spec.md`**: Format rules (read when writing).
   - **`writing-plans/`**: AI prompts (read when executing).
2. **`README.md`**: Project overview + pointer to `PROGRESS.md`.
3. **`CLAUDE.md`**: Methodology + pointer to `PROGRESS.md`.
4. **`memory/MEMORY.md` (or `GEMINI.md`)**: Contains stable facts only, no status.
5. **`llm_logs/2025-11-08_discussion.md`**: Contains critical, immutable methodological decisions.

## Development & Collaboration Workflows

### 1. General Workflow
- **Start of Session:** Always open `PROGRESS.md` first to understand the current state and tasks.
- **Task Execution:** When writing, consult `CM03_production_spec.md` for format rules; use `writing-plans/` for AI execution prompts.
- **Task Completion:** Immediately update `PROGRESS.md` when a task is finished.
- **Logging:** Keep this memory file (`GEMINI.md` / `MEMORY.md`) strictly focused on stable facts. Record new AI sessions or major decisions in the `llm_logs/` directory.

### 2. Grant Writing (NSTC Application)
- Before working on LaTeX grant proposals (e.g., `research_proposal_v4.tex`), you **MUST** read `NSTC-applicaiton/CM03_production_spec.md`.
- Follow the exact structural specifications, page limits, and style guidelines detailed in the spec.
- The grant application is written strictly in English using LaTeX (`article` class).

### 3. Core Methodological Constraints (Strict Directives)
- **Do NOT extend the DHK (2025) model**: Maintain the exact 2-factor structure for domestic uncertainty ($h_{macro,t}$, $h_{financial,t}$). Do not attempt to add a third "global uncertainty" factor.
- **Do NOT impose block exogeneity restrictions**: Rely strictly on the data-driven, order-invariant classification.
- **External Variables = Unclassified**: All external shock sources (U.S., China, global) must be placed in the "unclassified" category to identify their transmission channels.
- **Focus on the "Which" not the "How Much"**: The core question is *which transmission channel* external shocks use, rather than purely tracking the magnitude of the impact.

### 4. Data Pipeline (Phase 2 — In Progress as of 2026-04)
- **Sample**: 2001M1–2025M12 (300 months), 47 variables (17 macro + 8 financial + 22 unclassified)
- **Scripts**: 9 Python scripts in `code/data_processing/` — each script is self-contained, downloads to `data/raw/<category>/`
- **Status**: ~35 of 47 variables downloaded. Gaps: China IPI/PPI/M2 (FRED/NBS intermittent), TWSE flows, Sinyi housing prices, sector employment.
- **Key API discoveries**:
  - **eng.stat.gov.tw**: Data embedded in hidden form field `ContentPlaceHolder1_hidChartData` (JSON)
  - **cpx.cbc.gov.tw**: 4-step session-based API with double-encoded JSON responses
  - **DGBAS nstatdb**: Intermittent availability (403); column-major data layout `orgdata[col][row]`
  - **BIS REER**: `stats.bis.org` (not `data.bis.org`)
- **Design decisions**: See `docs/variable_planning.md` § "已確認的決定" for 6 confirmed choices (PMI dropped, credit spread dropped, M2 replaces TSF, etc.)

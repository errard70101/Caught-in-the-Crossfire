# MF-OI-SVMVAR Protocol Specs

These files are executable research protocols, not proposal prose. They define the mathematical objects, algorithms, validation invariants, benchmark accounting, and forbidden claims for each technical thread before further code or benchmark work proceeds.

Use this order:

1. `GLOBAL_DEFINITIONS.md`
2. `THREAD1_MATVEC_PROTOCOL.md`
3. `THREAD2_PCG_CORRECTION_PROTOCOL.md`
4. `THREAD2B_FAIR_COST_CORRECTION_PROTOCOL.md`
5. `THREAD3_PO_DRAWS_PROTOCOL.md`
6. `THREAD2C_MATRIX_FREE_PROTOCOL.md`
7. `THREAD4_LAMBDA_PROTOCOL.md`
8. `THREAD5_LAG_STABILITY_PROTOCOL.md`
9. `THREAD6_B0_IDENTIFICATION_PROTOCOL.md`
10. `THREAD_SV_CLASSIFICATION_PROTOCOL.md`
11. `THREAD7_FULL_MCMC_PROTOCOL.md`

Path map for review:

| Thread | Protocol | Implementation or expected path | Main check artifacts |
| --- | --- | --- | --- |
| Global | `protocols/GLOBAL_DEFINITIONS.md` | n/a | shared notation, scope-versus-`main.tex` map, benchmark rules |
| Thread 1 matvec | `protocols/THREAD1_MATVEC_PROTOCOL.md` | `code/thread1_matvec/` | `THREAD1_NOTE.md`, `test_equivalence.py`, `test_time_avg_precision.py` |
| Thread 2 PCG correction | `protocols/THREAD2_PCG_CORRECTION_PROTOCOL.md` | `code/thread2_pcg/` | `THREAD2_NOTE.md`, `results.csv`, `summary_median.csv`, figures |
| Thread 2b fair cost | `protocols/THREAD2B_FAIR_COST_CORRECTION_PROTOCOL.md` | `code/thread2b_fair_cost/` | `THREAD2B_NOTE.md`, `results.csv`, total-time and memory figures |
| Thread 3 PO draws | `protocols/THREAD3_PO_DRAWS_PROTOCOL.md` | `code/thread3_po_draws/` | `THREAD3_NOTE.md`, `po_moments.csv`, `po_functionals.csv`, `pcg_tolerance.csv` |
| Thread 2c no-explicit-`Kbar` | `protocols/THREAD2C_MATRIX_FREE_PROTOCOL.md` | `code/thread2c_matrix_free_preconditioner/` | `THREAD2C_NOTE.md`, correctness logs, benchmark CSV, memory/time plots |
| Thread 4 lambda | `protocols/THREAD4_LAMBDA_PROTOCOL.md` | `code/thread4_lambda_sensitivity/` | `THREAD4_NOTE.md`, `lambda_sensitivity.csv`, residual and posterior-stability plots |
| Thread 5 lag/SUR | `protocols/THREAD5_LAG_STABILITY_PROTOCOL.md` | `code/thread5_lag_stability/` | `THREAD5_NOTE.md`, `lag_stability_screening.csv`, SUR update diagnostics |
| Thread 6 `B0` identification | `protocols/THREAD6_B0_IDENTIFICATION_PROTOCOL.md` | `code/thread6_b0_identification/` or `THREAD6_NOTE.md` if theory-only | rank-diagnostic definition, recovery CSVs, lambda/latent-draw plots |
| Thread SV/classification | `protocols/THREAD_SV_CLASSIFICATION_PROTOCOL.md` | `code/thread_sv_classification/` | `THREAD_SV_CLASSIFICATION_NOTE.md`, ARMH/ESS diagnostics, classification recovery outputs |
| Thread 7 full MCMC | `protocols/THREAD7_FULL_MCMC_PROTOCOL.md` | `code/thread7_full_mcmc/` | `THREAD7_NOTE.md`, synthetic recovery summaries, per-block timing, mixing diagnostics |

Paths are relative to `theory/mf_oi_svmvar_report/`. Existing paths are the
current review targets; expected paths should be created by the corresponding
future thread before it is marked complete.

Review gate:

- No Thread 2/2b/3 rerun should be treated as final until the relevant correction protocols are reviewed.
- No Thread 2c implementation should start until `THREAD2C_MATRIX_FREE_PROTOCOL.md` is reviewed and its solver choice, storage rules, and acceptance tests are accepted.
- No full MCMC implementation should start until Threads 1-6, the SV/classification protocol for enabled volatility or classification blocks, and `THREAD7_FULL_MCMC_PROTOCOL.md` have been reviewed.
- If protocol text and implementation disagree, the protocol controls unless the protocol is explicitly revised first.

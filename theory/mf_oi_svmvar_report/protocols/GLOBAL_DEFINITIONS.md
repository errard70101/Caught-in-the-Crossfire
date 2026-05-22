# Global Mathematical Definitions and Benchmark Rules

This file defines shared notation and rules for the MF-OI-SVMVAR computational threads. The goal is to remove ambiguity before implementation.

## Scope Versus `main.tex`

Threads 1-4 use a controlled Gaussian latent-path problem. They are not the full
mixed-frequency OI-SVMVAR posterior in `main.tex`. In the controlled problem,
the whole high-frequency path `y` is treated as the latent object and the
observed/missing selection matrices are suppressed. This is equivalent to the
full model only in the degenerate bookkeeping case where the sampled block is
the full path and selection is identity.

The production notation in `main.tex` samples only missing entries `y^m` after
conditioning on observed high-frequency entries `y^o`. The correspondence is:

| Protocol object | `main.tex` production object | Meaning |
| --- | --- | --- |
| `K` | `Kbar = A' D A + lambda M_m' M_m` | Conditional precision for the sampled path block. |
| `H_B` | `A = H_B S^m` | VAR residual operator restricted to missing entries. |
| `M` | `M_m` | Aggregation matrix restricted to missing entries. |
| `lambda M' y_L` | `A' D r + lambda M_m' y_tilde^L` | Conditional mean right-hand side. |
| full `y` | `y^m` with `y* = S^o y^o + S^m y^m` | Sampled latent block and reconstructed full path. |

Thus protocol statements written as

```text
K = H_B' D H_B + lambda M' M
```

should be read as the full-latent test analogue of the production equation for
`Kbar`. Production code must restore `S^o`, `S^m`, `A = H_B S^m`, `M_m`, and the
complete right-hand side containing `A' D r`.

## Core Objects

Let `n` be the number of variables, `T` the number of high-frequency dates, `p` the VAR lag order, and `Tn = T * n`.

The latent high-frequency vector is stacked date-major:

```text
y = (y_1', y_2', ..., y_T')' in R^{Tn}.
```

The VAR residual operator is

```text
H_B =
[ I                              ]
[ -B_1  I                        ]
[ -B_2 -B_1  I                   ]
[ ...                            ]
[ -B_p ... -B_1 I                ],
```

with unavailable pre-sample lags truncated at the first `p` dates. This truncation is a boundary convention, not a claim about exact steady-state initialization.

The stochastic-volatility precision block is

```text
D_t = B0' diag(1 / U_t) B0,
```

where `U_t` stores diagonal innovation variances, not precision entries.

Order-invariant target:

```text
B0 is a general dense contemporaneous impact matrix subject to the model's
normalization and labeling rules.
```

Do not impose triangular or recursive zero restrictions in production
computational paths. Lower-triangular `B0` is allowed only as a legacy or
controlled-DGP test option and must be labeled order-dependent.

The full latent-state precision is

```text
K = H_B' blockdiag(D_1, ..., D_T) H_B + lambda M' M.
```

The right-hand side for the controlled Gaussian posterior is usually

```text
h = lambda M' y_L,
```

so the target posterior is

```text
y | rest ~ N(K^{-1} h, K^{-1}).
```

## Time-Averaged Precision

The only approved definition of the time-averaged precision block is

```text
D_bar = (1 / T) sum_{t=1}^T D_t
      = B0' diag((1 / T) sum_{t=1}^T 1 / U_t) B0.
```

Do not replace this with

```text
B0' diag(1 / mean_t U_t) B0.
```

That is a different object. Under stochastic volatility, `mean(1 / U_t) != 1 / mean(U_t)`.

The corresponding time-averaged preconditioner target is

```text
K_pre = H_B' (I_T kron D_bar) H_B + lambda M' M.
```

Any implementation that uses a different `D_bar` must be named explicitly, for example `time_avg_volatility`, and cannot be reported as the time-averaged precision preconditioner.

## Matrix-Free Terminology

Use precise storage language:

- `K-free` means the full SV-dependent precision `K` is not assembled as a global `Tn x Tn` sparse matrix.
- `K_pre-free` or `Kbar_avg-free` means the time-averaged preconditioner matrix is not assembled as a global `Tn x Tn` sparse matrix.
- `H_B-materialized` means the time-invariant VAR shell is stored as a sparse `Tn x Tn` matrix.
- A method can be `K-free` while still materializing `H_B`.
- A method is not a no-explicit-`Kbar_avg` method if it builds global sparse `K_pre`.

Every benchmark row or note must state whether it stores:

```text
H_B, H_B.T, K, K_pre, M, M.T.
```

If both `H_B` and a copied transpose are cached, memory accounting must count both.

## Benchmark Accounting Rules

Solver-level comparisons must report:

```text
total_time = assembly_time + factor_or_preconditioner_setup_time + solve_time.
```

No path may omit preconditioner setup from total time unless it is clearly marked as an amortized or derived best-case row.

Direct sparse baseline:

```text
direct_cholmod_total = assemble K + factor K + solve K x = b.
```

Matrix-free PCG with explicit preconditioner:

```text
pcg_explicit_pre_total = build K_pre + factor K_pre + PCG solve with K matvec.
```

Structured matrix-free PCG:

```text
pcg_structured_pre_total = structured setup + structured apply/solve + PCG solve with K matvec.
```

Thread 1 matvec timings are not solver-level evidence. Solver claims require Thread 2/2b/2c style accounting.

## Validation Invariants

Matvec invariant:

```text
||K_exp x - K_mf x|| / ||K_exp x|| < 1e-10
```

Preconditioner invariant:

```text
||K_pre_exp x - K_pre_structured x|| / ||K_pre_exp x|| < 1e-10
```

Direct-solve invariant:

```text
||b - K x|| / ||b|| <= reported solver tolerance or direct numerical precision.
```

Sampler invariant for scalar functionals `c_j`:

```text
|mean(c_j' y_draw) - c_j' K^{-1} h| <= 2 * MCSE_j
Var(c_j' y_draw) matches c_j' K^{-1} c_j within sampling error.
```

## Forbidden Claims

Do not claim:

- Zhu's homoskedastic matrix-free sampler automatically extends to SV.
- `O(Tn)` memory implies `O(Tn)` compute.
- Matrix-free PCG is production-ready unless total time, memory, and accuracy all support it.
- No `Tn x Tn` matrix is materialized if `H_B` or another global shell is stored.
- A preconditioner is time-averaged precision if it uses `1 / mean(U_t)`.

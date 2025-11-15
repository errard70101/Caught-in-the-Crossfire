# Research Note: Mathematical Incompatibility of Order-Invariance and Zero Restrictions

**Date Created:** 2025-11-16
**Source Discussion:** `2025-11-16_svmvar-order-invariance-discussion.md`
**Status:** CRITICAL METHODOLOGICAL INSIGHT
**Relevance:** Fundamental constraint for Taiwan SVMVAR research design

---

## Executive Summary

This note documents a **critical methodological finding**: attempting to combine order-invariant methods (Davidson, Hou, Koop 2025) with zero restrictions (small open economy block exogeneity) is **mathematically infeasible**. This incompatibility has direct implications for our Taiwan research strategy.

**Key Takeaway:** We must choose between:
1. Full order-invariance (DHK 2025 approach) + post-estimation verification of SOE assumption, OR
2. Traditional recursive identification with zero restrictions + accepting order-dependence

**Recommendation:** Maintain full DHK (2025) framework as decided in 2025-11-08 discussion.

---

## The Original Question

**Research Context:**
For small open economies (SOEs), traditional VAR models impose **block exogeneity restrictions**: global variables can affect domestic variables, but domestic variables cannot affect global variables. This is implemented through zero restrictions in the B₀ matrix:

```
B₀ = [ B^gg    0    ]  ← Global block
     [ B^dg   B^dd  ]  ← Domestic block
```

Where B^gd = 0 enforces "domestic variables do not affect global variables."

**The Proposed Hybrid Approach:**
- Apply order-invariant methods within the domestic (Taiwan) variable block
- Simultaneously impose zero restrictions on the global-to-domestic block
- Goal: Combine benefits of both approaches

**Verdict:** This is mathematically impossible.

---

## Mathematical Proof of Incompatibility

### 1. Core Definitions

**Order Invariance Property:**
For any two variable orderings π₁ and π₂, with corresponding B₀ matrices B₀^(1) and B₀^(2), order invariance requires:

```
P_π B₀^(1) P_π' = B₀^(2)
```

Where P_π is the permutation matrix mapping ordering π₁ to π₂.

**Zero Restriction:**
B₀[i,j] = 0 for specific (i,j) pairs (e.g., domestic → global effects).

### 2. The Fundamental Contradiction

**Proof by Contradiction:**

Assume B₀^(1)[i,j] = 0 under ordering π₁.

Under order invariance, for ordering π₂:
```
B₀^(2)[π(i), π(j)] = (P_π B₀^(1) P_π')[π(i), π(j)] = B₀^(1)[i,j] = 0
```

**Problem:** The location of the zero restriction **changes with variable ordering**.

- Under π₁: Zero at position (i,j)
- Under π₂: Zero at position (π(i), π(j))

**Conclusion:** Zero restrictions are inherently **order-dependent**, while order-invariance requires results to be **order-independent**. These two requirements are **logically incompatible**.

### 3. MCMC Algorithm Breakdown

Davidson et al. (2025)'s MCMC algorithm relies on a parameter transformation:

```
w = d + QB₀
B₀ = Q⁻¹(w - d)
```

**Critical Assumption:** Q must be invertible (non-singular).

**Under Zero Restrictions:**
- Zero restrictions make Q singular (det(Q) = 0)
- Q⁻¹ does not exist
- The inverse transformation is **undefined**
- Jacobian for change-of-variables becomes zero or undefined
- MCMC sampling scheme **collapses**

### 4. Likelihood Function Issues

**Structural Problem:**
- Zero restrictions cause the likelihood function to factorize:
  ```
  L(θ|data) = L_global(θ_g|data_g) × L_domestic(θ_d|data_d, data_g)
  ```
- Global and domestic blocks become **conditionally independent**
- Gradient of log-likelihood becomes **discontinuous** at zero restriction boundaries
- Posterior distribution p(b₀,ᵢ|·) has **discontinuous conditional distributions**

**Implication:** Standard MCMC samplers (Gibbs, Metropolis-Hastings) fail at discontinuities.

---

## Why This Matters: Conceptual Incompatibility

### Order-Invariance Philosophy
- **Assumption:** True economic relationships are symmetric and reversible
- **Implication:** Variable ordering is arbitrary; results should not depend on it
- **Method:** Allow all contemporaneous interactions; let data determine strength

### Block Exogeneity Philosophy
- **Assumption:** Causal structure is known a priori (global → domestic, not reverse)
- **Implication:** Variable ordering encodes economic structure (global first, then domestic)
- **Method:** Impose zero restrictions to enforce one-way causality

**These are fundamentally different worldviews** about economic structure identification.

---

## Implications for Taiwan SVMVAR Research

### What We CANNOT Do

❌ **Cannot:** Mix order-invariance and zero restrictions
❌ **Cannot:** Modify DHK (2025) algorithm to "partially" apply order-invariance
❌ **Cannot:** Use computational tricks to force both properties simultaneously

### What We SHOULD Do (Based on 2025-11-08 Decision)

✅ **Maintain full DHK (2025) framework:**
- Apply order-invariance to ALL variables (Taiwan + US + China + global)
- Do NOT impose zero restrictions on B₀ matrix
- Let the data reveal contemporaneous relationships

✅ **Verify SOE assumption post-estimation:**
- Use Forecast Error Variance Decomposition (FEVD)
- Check if Taiwan variables explain <5% of variance in US/China/global variables
- If confirmed: SOE assumption holds empirically
- If violated: Reveals important feedback effects (novel finding!)

✅ **Justify methodologically:**
- DHK (2025) deliberately avoids zero restrictions to achieve order-invariance
- Our contribution is applying their framework to SOE context
- Testing whether order-invariant methods generalize beyond large closed economies

### Why This Is Still Valid for Taiwan

**Potential Concern:** "Taiwan is too small to affect US/China—shouldn't we impose this?"

**Responses:**

1. **Empirical vs. A Priori Restrictions:**
   - Traditional approach: Impose SOE assumption as hard constraint
   - DHK approach: Test SOE assumption empirically
   - Our approach is more rigorous (falsifiable)

2. **Contemporaneous vs. Lagged Effects:**
   - Zero restrictions affect contemporaneous relationships (B₀)
   - Taiwan may have small contemporaneous effects due to:
     - Same-day stock market reactions (TAIEX ↔ S&P 500)
     - High-frequency semiconductor supply chain linkages
   - Even if lagged effects are asymmetric (global → Taiwan), contemporaneous effects may be symmetric

3. **Methodological Consistency:**
   - Mixing methods violates both frameworks
   - Better to fully adopt one coherent framework
   - DHK (2025) framework is more recent and addresses known problems (order-dependence)

---

## Alternative Approaches (If DHK Framework Is Abandoned)

### Option A: Traditional Recursive Identification
- **Method:** Cholesky decomposition with predetermined ordering
- **Ordering:** Global variables first, Taiwan variables last
- **Pros:** Well-established, computationally simple
- **Cons:** Results depend on arbitrary ordering within blocks; known to produce biased results in large VARs

### Option B: Soft Restrictions (Bayesian Shrinkage)
- **Method:** Instead of B^gd = 0, use B^gd ~ N(0, τ²I) with small τ
- **Mechanism:** Prior distribution "shrinks" domestic → global effects toward zero
- **Pros:** Preserves MCMC algorithm feasibility; allows data to override if evidence is strong
- **Cons:** Introduces additional hyperparameter (τ); results sensitive to τ choice

### Option C: Two-Stage Estimation
- **Stage 1:** Estimate global VAR independently (US + China + global variables only)
- **Stage 2:** Extract global uncertainty factors; include as exogenous variables in Taiwan-only VAR
- **Pros:** Clean separation; computationally efficient
- **Cons:** Ignores potential feedback; uncertainty estimates from Stage 1 may be contaminated by omitting Taiwan variables

---

## Recommended Research Strategy

### Primary Strategy (Endorsed)
**Approach:** Full DHK (2025) order-invariant framework
**Rationale:**
1. Methodologically consistent
2. Allows empirical testing of SOE assumption
3. Aligns with our "transmission channel identification" research question
4. Demonstrates robustness of DHK methods to SOE context

**Post-Estimation Checks:**
- Report FEVD: "Taiwan variables explain X% of US uncertainty, Y% of China uncertainty"
- If X, Y < 5%: SOE assumption validated empirically
- If X, Y > 5%: Document as interesting finding; investigate mechanisms

### Robustness Check (Optional)
**Approach:** Soft restrictions (Option B)
**Implementation:**
- Set τ² = 0.01 (strong shrinkage toward zero)
- Re-estimate model
- Compare classification probabilities and FEVD results
- Report in robustness section

**Purpose:** Show that results are not driven by allowing Taiwan → US/China effects

---

## Documentation and Communication

### For Research Paper

**Methods Section Should Explicitly State:**
> "We do not impose block exogeneity restrictions (zero restrictions on Taiwan → US/China effects) a priori. Following Davidson et al. (2025), we apply order-invariant identification to all variables. The small open economy assumption is verified post-estimation through forecast error variance decomposition, which shows Taiwan variables explain <X% of US/China uncertainty variance. This data-driven approach avoids the order-dependence problems that plague traditional recursive identification in large VARs."

### For Referee/Reviewer Concerns

**Anticipated Question:** "Why didn't you impose standard SOE restrictions?"

**Response Template:**
> "While small open economy restrictions (block exogeneity) are common in the literature, they are incompatible with order-invariant methods (see Section X). Imposing zero restrictions would reintroduce the order-dependence problem that Davidson et al. (2025) explicitly solve. Our FEVD results (Table Y) confirm the SOE assumption holds empirically, demonstrating that the data supports the restrictions without needing to impose them a priori. This approach is more rigorous as it allows the SOE assumption to be tested rather than assumed."

---

## Lessons Learned

### Technical Lessons
1. **Not all methodological combinations are feasible:** Seemingly reasonable hybrid approaches may be mathematically impossible
2. **Algorithm assumptions matter:** DHK's MCMC algorithm is specifically designed for unrestricted B₀; modifications are non-trivial
3. **Order-invariance is a package deal:** Cannot "partially" apply it

### Research Design Lessons
1. **Consistency over patchwork:** Better to fully adopt one coherent framework than mix incompatible methods
2. **A priori restrictions vs. empirical validation:** Modern methods favor letting data speak
3. **Trade-offs are unavoidable:** Every identification strategy makes assumptions; acknowledge them explicitly

### Practical Lessons
1. **Consult multiple sources:** Claude initially said "feasible"; Gemini correctly identified impossibility
2. **Demand mathematical proof:** Intuition can mislead; formal proofs reveal contradictions
3. **Document decision rationale:** Future reviewers will ask; pre-empt with clear explanation

---

## Action Items

- [x] Document mathematical incompatibility in research note (this document)
- [ ] Update research proposal methods section to explicitly address order-invariance vs. zero restrictions trade-off
- [ ] Add post-estimation SOE validation to analysis plan (FEVD Taiwan → US/China < 5%)
- [ ] Prepare response template for referee reports questioning lack of block exogeneity
- [ ] Consider robustness check with soft restrictions (low priority)

---

## Related Documents

- **Primary Decision:** `llm_logs/2025-11-08_discussion.md` (original decision to adopt full DHK framework)
- **Source Discussion:** `llm_logs/2025-11-16_svmvar-order-invariance-discussion.md` (mathematical proof)
- **Research Direction:** `llm_logs/2025-11-14_research_direction_and_milestones.md` (overall strategy)
- **Methodological Reference:** `references/Investigating Economic Uncertain.pdf` (DHK 2025 paper)

---

## Mathematical Appendix: Detailed Proof

### Proposition
**Order-invariance and zero restrictions are mutually exclusive properties.**

### Formal Statement
Let V be a set of n variables, and let Π be the set of all permutations of V.
Let B₀(π) denote the contemporaneous impact matrix under ordering π ∈ Π.

**Order-Invariance (OI):** ∀π₁, π₂ ∈ Π, the implied structural shocks ε and impulse responses are identical.

**Zero Restriction (ZR):** ∃(i,j) such that B₀(π)[i,j] = 0 for some canonical ordering π*.

**Claim:** OI ∧ ZR → ⊥ (contradiction)

### Proof
1. Suppose ZR holds: B₀(π*)[i,j] = 0 for variables v_i, v_j in ordering π*.

2. Consider permutation π' that swaps v_i with v_k (k ≠ i, j):
   - Under π*: v_i at position i, v_j at position j → B₀[i,j] = 0
   - Under π': v_k at position i, v_j at position j → B₀'[i,j] = ?

3. By OI, the structural relationship between v_i and v_j must be preserved:
   - If B₀(π*)[i,j] = 0 represents "v_j does not contemporaneously affect v_i"
   - Under π', this zero must appear at positions corresponding to v_i and v_j
   - But v_i is no longer at position i

4. Two cases:
   - **Case A:** Zero moves to new position [k,j] → Different economic structure (v_k ≠ v_i)
   - **Case B:** Zero remains at [i,j] → Now refers to v_k and v_j (different relationship)

5. Either case violates OI: the structural economic relationship changes with ordering.

**Conclusion:** ZR forces economic structure to depend on ordering, contradicting OI. ∎

---

**END OF RESEARCH NOTE**

*This document should be referenced whenever questions arise about:*
- *Why we don't impose SOE block exogeneity restrictions*
- *The feasibility of mixed identification strategies*
- *Mathematical foundations of order-invariant methods*

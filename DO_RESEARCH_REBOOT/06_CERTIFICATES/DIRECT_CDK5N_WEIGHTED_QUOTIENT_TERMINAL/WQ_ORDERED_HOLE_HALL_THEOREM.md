# WQ_ORDERED_HOLE_HALL_THEOREM.md + WQ_GUARD_NORMAL_FORM.md (condensed)

Hall (STEP 04/§8): variables z_{i,r} (10 gaps × holes); equations
Σ_r z_{i,r} = d_i (d_i=σ_i−p_i ≥ 0 required); lower bounds Σ_i z≥1 on
S-less nonempty holes; z=0 on incompatible pairs; exact S placement +
inorder compatibility separately enforced. Feasibility ⟺ (A) d_i≥0 +
(B) positive-supply gaps eligible + (C) 1,024 subset inequalities
Σ_{i∈I}d_i ≥ |{r:N(r)⊆I}| — necessity/sufficiency via capacitated
max-flow (AFSP_allocate: soundness+completeness vs brute force 80/80).
BST-order restriction hunt (§8 tripwire): full reconstruction verifier
(actual BSTs, true canonical order, S positions, intervals, uniqueness)
67/67 + solver agreement — NO omitted restriction found; tripwire silent.
Guard normal form (STEP 05/§9): Γ_T(σ) = prefix topology + rotation cases
+ S assignments + hole compatibility + 1,024-capacity system (+ terminal
root); theorem Γ_T(σ) ⟺ realizable (AF-2 biconditional + AF-1 substitution;
Catalan completions never enumerated). Status: PROVED (construction +
solver + reconstruction verification).

# AFSP_INTEGER_ALLOCATION_THEOREM.md + AFSP_SATURATION_PUMPING.md + AFSP_EDGE_GUARD_FACTORIZATION.md (condensed)

AF-2 (STEP 05): variables z_{i,r} (gap×hole); equations p_i+Σz=σ_i;
S-less-nonempty lower bounds; interval compatibility; S uniqueness.
Max-flow lower-bound circulation decides feasibility; exact demands
enforced (equality, not ≤). Soundness+completeness vs brute force 80/80;
frozen inorder+balanced reconstruction valid 64/64. PROVED.
AF-3 (STEP 06): reservoir extends OCCUPIED deep frontiers below active
cone only (landing depth ≥7; never fills empty holes); preserves depths/
costs/steps/H/S-skeleton/emptiness/signature. Tests: 30 occupied-extension
+ saturation fuzz to 2,000-key gaps + 264/265/266/267 boundary sweep;
0 mismatch. Integer-tight intervals: below-cone room argument (true fit
⇒ capacity; loud failure if insufficient — never triggered). PROVED
within stated discipline.
AF-4 (STEP 07): templates (prefix, word, B-transition, S-assignments) +
AF-2 guard; guard theorem (satisfiable ⟺ realizable) via AF-2
biconditional + AF-1 substitution; Catalan completions never enumerated.
H=1 kernel: 5,280 templates (all step cases incl. D(v)+K(v)). PROVED
(construction + solver verification).

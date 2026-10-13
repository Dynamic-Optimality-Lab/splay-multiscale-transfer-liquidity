# CC_HALL_GUARD_THEOREM.md + CC_INTERVAL_TYPE_REDUCTION.md + CC_GUARD_COMPLETENESS.md (condensed)

Hall (AF-2 form): z_{i,r} with exact demands Σz=d_i, lower bounds on S-less
nonempty holes, interval compatibility, S uniqueness. Max-flow decides;
subset form (A)d_i≥0 + (B) eligibility + (C) 1,024 inequalities verified
EQUIVALENT on 600 randomized instances (0 disagreements; contiguous and
noncontiguous N-sets). BST-order tripwire (§8): full reconstruction
verifier (true canonical order, S positions, intervals, uniqueness) 67/67;
source-derived hole gap-sets contiguous 27,142/27,142 with 44 distinct
types (≤55 ✓). No omitted restriction found.
Interval reduction: gap-compat sets of BST-interval holes are contiguous
(proved from key order; verified); 55 nonempty interval types; r_J counts;
guard schema B_Hall ≤ 1024(10+55+3)+128·55 = 76,672 (arithmetic verified:
1024×68=69,632 + 7,040).
Completeness: Γ_T(σ) ⟺ realizable (AF-2 biconditional + AF-1 substitution;
Catalan completions never enumerated; reconstruction 64/64). H=1 kernel:
5,280 templates (all step cases + D(v)+K(v)); kernel-vs-graph: 134/134
negative macros match templates + B-depths 6/7/8.

# Equality-case completion before the source audit

This refines the SAME paired-return mechanism in PC00; no second algorithm
or potential campaign is launched. Determine the saturation equality case,
not just a weak depth inequality.

If a tracked return interval is retreat-only, every paired step contributes
epsilon_B-2epsilon_A<=0. Equality can hold only for (epsilon_A,epsilon_B)
=(1,2) at EVERY step. Combining this with the actual return parity should
force an odd gap L and d_A=L-1,d_B=2(L-1) at a saturated return. Any other
departure type or parity must produce a genuine negative block. No assertion
that such intervals exist in every closed word is made.

Investigate the exact structural witness for an equality step. Let r be
the common old root, x the target, and p the original B path's depth1
parent in its last same-side outer double. B should end with x->p->r,
where p is strictly between x,r in key order. A's epsilon1 should place r
as a child of x, with p below r. Thus the originally agreed pair(r,p)
becomes an A/B ancestor inversion. Prove this from source subtrees.

During a monotone retreat run, the open intervals between successive roots
are disjoint. Their p witnesses should therefore be distinct, and the new
inversions should persist through subsequent retreats because both keys
remain in the far-side subtree. They may change at the final return or
later approaching accesses; no global credit or monotonicity is inferred.

This is the source meaning of the exceptional equality case, derived
constructively from PC00's epsilon law. Check those witnesses on the fixed
19-block data and in the symbolic proof. Keep D's global saturated-transition
proposal and its fixed fringe adversary unchanged. A failure of scalar D
does not invalidate this local paired lemma or prove that every possible
separator discharge theorem fails.

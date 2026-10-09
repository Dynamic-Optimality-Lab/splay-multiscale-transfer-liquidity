# PIVOT-2 — exact conditional cycle-to-prefix reduction

STATUS: CONDITIONAL for the cost bound; the implication is completely proved. It does not prove its universal cycle premise.

Let K be a fixed finite ordered key set of size n≥1 and T0 a BST on K. Pair Access starts at (T0,T0). For a finite walk H define S_A(H)=sum a_i, E_B(H)=sum b_i, W_3(H)=E_B(H)−3S_A(H). Assume every reachable closed walk has W_3≤0. Then every finite present-legal H satisfies

\[
E_B(H)\le3S_A(H)+g(T_0),\qquad
g(T_0)=(\mathrm{Cat}_n^2-1)\lfloor n/2\rfloor.
\]

There are Cat_n BST shapes on K and at most V=Cat_n² pair states; keys, rather than labels of dense integer ranks, are fixed. Each edge has b_i≤ceil((n−1)/2)=floor(n/2), so its W_3 reward is at most floor(n/2). In any finite walk containing a repeated vertex, remove the intervening closed subwalk. Its reward is nonpositive, so removal can only increase the total reward. Iterate until the remaining path is simple, with at most V−1 edges. Its reward is at most (V−1)floor(n/2). This proves the bound for all H under the same cycle premise. For n=1 all events cost zero and g=0. For an empty key set the only present-legal history is empty and the bound is trivial.

Conversely, if all histories from the diagonal have a finite upper reward bound, no reachable closed walk can have positive reward: append arbitrarily many repetitions after a path reaching its start. This proves the exact finite-graph equivalence. Reachability is essential to the converse; all-pair cycle control is a sufficient stronger premise.

The formula above is a conservative explicit startup bound reconstructed here. The source defines g_C(T0) as the finite maximum residual over simple reachable paths; it does not pin this particular closed formula. A tighter g is optional. Neither bound depends on history length. No O(n) overhead claim is needed for the eventual-monotonicity reduction.

Source: audits/PIVOT_RECURRENT_EXCESS.md:12-20 (standard author-recorded cycle excision); scripts/wp6_cycle_ratio.py:58-100 (finite pair graph); lean/WP6/GCStaticKeep2Step.lean:740 onward (arithmetic reward lemmas only). General list/cycle-excision formalization is not claimed kernel-checked.

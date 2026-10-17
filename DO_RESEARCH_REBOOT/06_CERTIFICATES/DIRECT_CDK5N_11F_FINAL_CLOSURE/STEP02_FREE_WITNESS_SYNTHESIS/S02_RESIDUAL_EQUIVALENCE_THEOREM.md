# S02_RESIDUAL_EQUIVALENCE_THEOREM.md — residual = original under pins (Gate F)

For partial assignment a: `F(a,xi) <=> F_residual(xi)` holds because (i) Tier-1
is exact constant folding under asserted equalities (Step-01 O2 ledger), and
(ii) source-derived stage pins (B-words, H/q, skeletons, completions) are
conjoined — never substituted for — the original relation; the final Tier-1
verification runs the FULL original root under the complete candidate env.
Necessary filters (sig/mu equality, marked-count, q/H admissibility, A-depth<=4,
universe membership) are each relation-entailed; pruning beyond them is ordering
(short words/canonical first), and duplicate skeletons are skipped by signature
(sound: identical pin-sets decide identically). Explored (word, completion) combos
are never repeated within a query (enumeration order).

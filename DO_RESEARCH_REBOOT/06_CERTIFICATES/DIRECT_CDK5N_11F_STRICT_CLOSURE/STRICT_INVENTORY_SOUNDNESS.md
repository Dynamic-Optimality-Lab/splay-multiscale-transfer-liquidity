# STRICT_INVENTORY_SOUNDNESS.md — A7 (+A5 realizability)

## Repairs
- Exact S-cover (exposed XOR one hidden claim) + exposed/hidden uniqueness + fullrank global order.
- Atom ownership via (gap,port) cells with exact hidden-S positions (order fidelity theorem).
- Gap supply equations (equality) + port occupancy derived + empty-port restrictions.
- Compatibility: `z>0 ==> LE rank-overlap(port interval, gap S-span)` (NECESSARY condition;
  value-overlap implies rank overlap by order-faithfulness). Integer-room sufficiency is
  reconstruction-checked (OPEN sub-point: rank-only reasoning cannot decide integer room in dense
  universes; bites only solver-synthesized models, which are extraction-verified in practice).
- Widths (proved sufficient, exact integer semantics, no wrap): counters<=266 (9b); sums<=2660
  (12b); ranks<=135 (8b); bounds<=136 (8b); S-index<=8 (4b); sig<=266 (9b); mu 9b popcount=5.

## Reconstruction soundness/completeness
Sound: satisfying assignment -> ordered BST completion (per-port sorted hidden-S + anonymous
fillers; position-order verified) + B fringe blocks. Completeness: valid completions induce
assignments (conservation identities). Incompatible-port/cross-gap moves rejected adversarially.

## A5 boundary realizability (construction)
Given valid (mu,b,alpha7,sig): B = core b + per-gap balanced blocks (sig counts; always fits);
A = alpha top-3-levels + arbitrary BST completion to depth 6 + remaining S in ports (intervals
flexible: choose prefix to fit; always possible) + fringe per sig. Hence every valid abstract state
has a canonical representative (the 10-check boundary predicate is exact, not merely local).

## Gates A7 (+A5): REPRODUCED + REPAIRED (compat added; widths audited; realizability proved).

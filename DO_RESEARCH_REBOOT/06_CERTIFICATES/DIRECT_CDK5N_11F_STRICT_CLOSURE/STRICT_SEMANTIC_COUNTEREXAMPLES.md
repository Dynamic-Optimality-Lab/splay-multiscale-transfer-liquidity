# STRICT_SEMANTIC_COUNTEREXAMPLES.md — audit dispositions (reproduce or disprove each)

## Method
For each suspected defect: reproduce (concrete source counterexample or SAT phantom model) and
repair, or disprove (prove already satisfied). No dismissal by prior tests.

## Dispositions
- A1 (separate A/B targets): REPRODUCED as soundness gap (no binding existed). REPAIRED (same-key
  conjuncts: S-exact sidx==core-id; fringe same-gap + fungibility theorem). Adversarial S/gap
  mismatches rejected (STRICT_SEMANTIC_REGRESSIONS.json).
- A2 (paths not root-terminated): REPRODUCED as gap (no root/no-repeat constraints).
  REPAIRED (path[dd]==current root + pairwise distinct, A and B). Shortened/duplicated paths
  rejected adversarially.
- A3 (root-run rule unsound for D(x),K(x)): REPRODUCED as proof defect (collapse-to-first wrong
  when first op is a no-op DELETE). REPAIRED (corrected normal form: drop full-no-ops, keep first
  B-changing KEEP; greedy executable + preservation fuzz 60/60 + <=5-event bound verified).
  Implementation needed no change (interpreter consumes normalized words; non-normal still sound).
- A4 (B validity insufficient): REPRODUCED as gap (no one-parent/connectivity). REPAIRED (parent/
  depth vars + exactly-one-claimant + depth chains + gap-core attachment; reconstruction support).
  Duplicated/disconnected B rejected adversarially.
- A5 (boundary weaker than authoritative): AUDITED — local field constraints + realizability THEOREM
  (construction below) satisfy the 10-check boundary predicate. No counterexample found; the gap
  was missing proof, now supplied. Realizability: given (mu,b,alpha7,sig): B = core + balanced
  gap blocks (sig counts, always fits); A = alpha top + arbitrary BST completion to depth 6 with
  remaining S in ports (intervals flexible: choose prefix to fit) + fringe per sig. Constructive
  spot tests build completions for sampled states (verifier V4-adjacent).
- A6 (alpha omits grandchildren): REPRODUCED as fidelity gap (authoritative vis has 7 positions;
  predecessor had 3). REPAIRED (alpha-7 + derived canonical beta + port/empty propagation;
  R3 justification: same coordinate completed to authoritative content, no new coordinate).
- A7 (inventory arithmetic/compat): REPRODUCED as gap (no interval compat on z; latent inclusive-lo
  subtlety). REPAIRED (LE rank-overlap compat = necessary condition; widths audited: sums<=2660
  in 12b, counters<=266 in 9b, no overflow; integer-room caveat documented as OPEN sub-point:
  only affects solver-synthesized models in dense universes, extraction-verified in practice).
  Incompatible-port/cross-gap moves rejected adversarially.
- A8 (q accounting): REPRODUCED as gap (intermediate genuine KEEPs unaccounted). REPAIRED
  (non-terminal genuine prohibition = macro segmentation discipline; terminal-only q exact).
  Unsplit two-genuine words rejected by circuit.

## No architecture counterexample (Outcome C territory): none found. Representation intact.

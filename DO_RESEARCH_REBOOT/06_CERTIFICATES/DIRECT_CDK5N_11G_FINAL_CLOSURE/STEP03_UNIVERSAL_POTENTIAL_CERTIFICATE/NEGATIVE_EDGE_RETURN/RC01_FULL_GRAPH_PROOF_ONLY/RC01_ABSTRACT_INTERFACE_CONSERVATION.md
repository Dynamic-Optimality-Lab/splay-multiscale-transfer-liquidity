# RC-01 Abstract Interface Conservation (what the interface does/doesn't carry)

Carried (exact, per frozen conjuncts): mu (transition-invariant), sigma
(frozen), B-controller arrays, A-shadow, ranks/bounds, accessed-key
identities per edge, weights, H/q per edge certificate. NOT carried:
splay paths of previous edges, rotation histories, push logs, debt
tallies, witness compatibility across edges, global concrete trees.
Consequence: any cross-edge conservation law must be a function of the
carried data plus the closed-walk condition alone. Searched candidates:
core size (nonincreasing on S; increasable on U — fails conservation);
ancestor sets (same); marked depth sums (unbounded both ways); shadow
occupancy (unbounded); signature (static, no debt capacity); mu (static).
RESULT: no vertex-expressible conserved-or-monotone quantity found that
forces repayment. This is a negative inventory result, not a proof of
nonexistence.

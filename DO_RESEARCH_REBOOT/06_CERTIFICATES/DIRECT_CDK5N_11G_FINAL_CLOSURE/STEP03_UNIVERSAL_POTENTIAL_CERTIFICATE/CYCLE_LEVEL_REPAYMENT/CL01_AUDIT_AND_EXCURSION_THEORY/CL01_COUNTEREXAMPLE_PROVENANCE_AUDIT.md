# CL-01 Counterexample Provenance Audit (4-level scope)

For each of the 5 verified violations: (1) VALID stored endpoints
(147-field keys recomputed; validity predicates ok) — INDEPENDENTLY
RECOMPUTED. (2) Correct potential arithmetic (C2/C5/Phi/guard/inequality
recomputed from stored features) — INDEPENDENTLY RECOMPUTED. (3) Original
ssertify certification (ssertify-ok at capture; envs stored) — ORIGINAL
EVIDENCE, not re-executed (no Z3 in CL-01). (4) Independent edge-predicate
replay (fresh Z3 re-solve of the frozen relation on stored envs) — NOT
PERFORMED (recorded gap; original certification stands unrebutted).
Scope verdict: levels 1-2 independently verified; level 3 original;
level 4 open. The refutation stands on levels 1-3 (valid edge + failed
inequality); level 4 would strengthen but is not required to sustain it.

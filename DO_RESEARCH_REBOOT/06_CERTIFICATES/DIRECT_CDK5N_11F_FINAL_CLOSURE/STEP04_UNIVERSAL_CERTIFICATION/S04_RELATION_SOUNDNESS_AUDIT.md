# S04_RELATION_SOUNDNESS_AUDIT.md — F04-16/F04-17/F04-18/F04-19

Low: every satisfying witness replays a source-compatible macro (13 synthesized
+ replayed + Tier-1 verified); conjunct-wise audit (all True). High: fiber env
conjunct-wise all True; only authorized WQ overapproximation. Weights/sorts:
OO -4..4 realized; OM structural -3..6 with marked q 0..4 => w 2..6 enforced
by EQ(w1,6-q) + depth-derived q (measured q ≤ 4 on all genuine witnesses;
relation allows q ≤ 8 structurally — out-of-genuine-range q has no source
witness by the depth bound, hence no phantom edge). Signed arithmetic exact
(Int; width audit; adversarial overflow/signed units). No phantom transitions:
forward-simulation-only methodology (BFS + verified witnesses); projections
audited free-var-clean; MO/MM as specified (MO zero-only, MM FALSE).

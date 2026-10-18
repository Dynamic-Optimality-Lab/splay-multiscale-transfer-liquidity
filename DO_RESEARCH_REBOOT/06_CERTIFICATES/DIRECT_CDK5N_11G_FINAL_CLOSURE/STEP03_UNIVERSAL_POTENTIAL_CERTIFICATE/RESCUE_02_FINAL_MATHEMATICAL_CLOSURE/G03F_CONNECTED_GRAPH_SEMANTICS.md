# G03F Connected-Graph Semantics

Source-pinned queries AND(low_root, 147 source pins), weight free, distinctly
enumerate symbolic successors (blocking on full dest tuples). Self-test on a
ledger edge FAILED to recover it within 60 s caps (witness freedom too large;
method unverified, not disproven). Each query costs ~5 min; 4 queries in
budget, 0 successors solved — recorded as solver-blocker, not absence. Concrete chaining (replay +
per-leg ssertify, MSET-fixed) is the productive connected construction:
11/11 joins (Rescue-01), 783 certificated legs / 101 closed walks here, all
with exact 147-field endpoint equality (repaired canon). Every stored edge
carries full states, weight, witness/model, provenance. No incomplete state
is inserted. The connected subgraph is liftable by construction (TYPE-A
candidates if negative); abstract-only edges are untouched.

# SR02 Feature Semantics (Gate A proof sketch)

Totality: all four features are total functions of the 147-field valid
state (parent-walk depths terminate on valid trees; subtree sizes finite;
mu-bit tests total; shadow reads total). No defaults: eval returns None
only on unreachable nodes (invalid states); all 246 stored endpoints
evaluate (S1). Symbolic agreement: grounded recompute matches stored
(SR01 S1); DAG encoding not constructed (blocked, recorded). Sector
coverage: features read only state fields (mask/signature agnostic by
construction); validity predicate enforced at edge endpoints (ssertify).

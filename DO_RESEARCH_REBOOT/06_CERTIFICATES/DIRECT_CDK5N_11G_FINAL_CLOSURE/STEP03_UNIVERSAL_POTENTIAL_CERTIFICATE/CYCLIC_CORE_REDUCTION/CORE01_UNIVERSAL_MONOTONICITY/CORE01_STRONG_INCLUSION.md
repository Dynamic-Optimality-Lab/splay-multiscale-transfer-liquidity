# CORE-01 Strong Inclusion vs Cardinality (Gate E, I)

Proved wherever monotonicity is proved (rotation lemmas + OM theorem):
C(t) subset C(s) as SETS of S-indices (index-stable; no identity claim
beyond indices needed). Cardinality rho(t) <= rho(s) follows immediately.
E4 CAUTION OBSERVED: set equality on closed walks does NOT follow
(reverse inclusion unproved); do NOT claim fixed membership. Cardinality
constancy on closed walks follows from telescoping under universal
monotonicity. Reference identity: core slots ARE S-indices by compiler
construction (cross-checked: T-A tests, ssertify envs, feature code);
no extra physical-identity theorem required for the index-set statement.
Gap slots (9-18) may enter/leave the closure as ancestors (they are
unmarked but can be ancestor links); inclusion accounts them correctly
(set semantics, verified on 48 full-state edges incl. gap-heavy cases).

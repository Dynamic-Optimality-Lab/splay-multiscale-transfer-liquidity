# Clean-room contract (frozen pre-reveal, WP-3)

## Semantic specification
The clean-room evaluator reimplements, from `math/theorems/*` + this contract + input histories ONLY:
ordinary bottom-up Splay (cost depth+1), KEEP/DELETE pair dynamics, the frozen
(T7, T5_{P,rho}, T6) ledger semantics of the frozen candidate, weaker-domain
`LegalPairInstance`, absent-key empty-trace path. Outputs: per-KEEP (need, paid,
margin) + full ledger diagnostics in `io_schema.json` format.

## Authoring boundary
Authors must not read, import, or receive: `python/adversary/*`, `python/solver/*`,
development/validation corpora, candidate outcomes/failures, H4L bank bytes pre-reveal,
solver state, or any discovery module. Allowed: `math/`, `schemas/`, input histories,
this contract. Violation fails the WP-5 seal audit.

## Implementation bytes
WP-5-owned. They must be committed and hash-frozen BEFORE H4L reveal; post-reveal
changes use only the preregistered replay interface (mechanically audited).

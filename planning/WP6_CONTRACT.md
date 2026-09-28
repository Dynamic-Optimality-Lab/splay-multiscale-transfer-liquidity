# WP-6 CONTRACT (compiled before implementation; immutable for WP-6)

Binding: CURRENT_PHASE=WP-6, PREVIOUS_PHASE=WP-5.
Authority: WorkPlan.md WP-6 + v0.4.1 spec #5 (theorems), #6 (lifecycle+review),
#9 (bridge pin-or-blocked), #10 (seal/conditional repro/export), #11
(governance/export/successor), #12 (gates/terminals) + prereg/
theorem_gate_matrix.yaml + schemas/review.schema.json +
schemas/theorem_status.schema.json.
Mode: contract compiled 2026-09-28 on branch wp5x-k6c2-specialized BEFORE any
WP-6 implementation (contract lock: implementation must satisfy the contract,
never the reverse).

## Entry predicate
- WP-6-REQ-001: previous-phase (WP-5) independently revalidated VERIFIED_COMPLETE
  with SURVIVES_FINITE_TESTS holding (a non-empty finite-surviving set).
- WP-6-REQ-002: one primary candidate at a time, in canonical order.
- WP-6-REQ-003: PA conjunction machine-checked BEFORE any MSTL-17 PROVE step
  (prerequisites: MSTL-08U/09/11/13/14/15/22 REVIEWED + LIQ0-01/02/04/05/06/09/10
  at required statuses, per spec #5 and theorem_gate_matrix.yaml).

## Scope (arbitrary-n war to bridge or honest terminal; PHASEs 17-19)
- WP-6-REQ-010: arbitrary-n case-complete proofs over
  ROOT/ZIG/LL/RR/LR/RL x T5/T6/T7 branches, exact arithmetic.
- WP-6-REQ-011: block partition + telescoping with A(n)=0 (additive target;
  nonzero BLOCKED until bridge-derived class frozen).
- WP-6-REQ-012: proof chain 13/14 -> 15 -> 17 -> 18 -> 19 (per-file obligations
  in math/proofs/MSTL-*.md; chain order preserved).
- WP-6-REQ-013: audited bridge against pinned bytes (L3 present/L2 absent per
  prereg/bridge_manifest.yaml), or BLOCKED_BY_SOURCE routing (L2 absent =>
  MSTL-19 BLOCKED_BY_SOURCE => DYNAMIC_OPTIMALITY_PROVED unreachable).
- WP-6-REQ-014: Layer-C attacks with 3-route certificates (dual lifecycle,
  3-route refutation per spec #6).
- WP-6-REQ-015: human ACCEPT/REJECT/BLOCKED per schemas/review.schema.json
  (genuine verdicts only, never fabricated; byte-change invalidates review).
- WP-6-REQ-016: integrability incl. signed path if Branch-B dormant set used.
- WP-6-REQ-017: seal + conditional repro + export packet + verifier
  (MST_LIQ_EXPORT.json, scripts/reproduce_all.py, artifacts/v04/seal/).
- WP-6-REQ-018: S01-S20 report.
- WP-6-REQ-019: MUST NOT substitute stock/finite/formal/review roles; MUST NOT
  claim DOC-negative (MST0-20/21 OUT_OF_SCOPE); REFUTED only via exact witness
  + hashes + validation; late Branch-A theorem death uses frozen Branch-B set
  or successor (no new synthesis); successor only if 5 conditions hold.

## Files (exact paths)
- WP-6-REQ-020: lean/{Liquidity,PairAccess,Bridge}/ (deterministic builds;
  sorry/admit/purpose-axioms/opaque-oracles forbidden; endpoint/
  length-independence audits).
- WP-6-REQ-021: math/proofs/MSTL-{08U,09,11,12,13,14,15,17,18,19}.md (+ existing
  dev/setup notes preserved, not overwritten).
- WP-6-REQ-022: math/reviews/MSTL-*.review.json (schema-valid, hash-bound).
- WP-6-REQ-023: math/proof_status.json (truth/prove/refute tracks per
  schemas/theorem_status.schema.json; REFUTED only via full refute track).
- WP-6-REQ-024: artifacts/v04/{proofs,audits,seal}/ + MST_LIQ_EXPORT.json +
  scripts/reproduce_all.py.
- WP-6-REQ-025: planning/WP6_CONTRACT.md (this file).

## Code/behavior
- WP-6-REQ-030: deterministic builds (lake build exit 0, lean-toolchain
  v4.21.0); WP-6 STEP logs at every significant execution step.
- WP-6-REQ-031: endpoint/length-independence audits; exact integer/rational
  decisions (no float-determined signs).
- WP-6-REQ-032: hostile negation-derived attacks (disjoint instances) with
  3-route certificates where refutation is claimed.

## Verification
- WP-6-REQ-040: lake build + full pytest + kill matrix + all audits + export
  verifier + conditional repro + fresh-checkout repro.
- WP-6-REQ-041: every MSTL node claimed REVIEWED has a genuine human ACCEPT on
  exact bytes (review_hash bound in proof_status.json).

## Statuses/exit
- WP-6-REQ-050: exactly one terminal: DYNAMIC_OPTIMALITY_PROVED (iff full PA
  chain REVIEWED + bridge audited) else an honest terminal from
  {PROMOTED_CANDIDATE_SET_REJECTED, SYNCHRONOUS_REPAYMENT_REFUTED,
  GLOBAL_INTEGRABILITY_REFUTED, PAIR_ACCESS_ROUTE_REFUTED_NO_DOC_NEGATIVE,
  BRIDGE_BLOCKED_NO_CLAIM, RESOURCE_LIMIT_NO_CLAIM, LEGACY_EMBEDDING_FAIL,
  AXIS_INCONCLUSIVE} (spec #12 set).
- WP-6-REQ-051: obstructions preserved (L2-absent record kept); successor
  embedding only if its 5 conditions hold.

## Logging/Path
- WP-6-REQ-060: WP-6 STEP <ID> comment+log lines in executing code; final
  line numbers inventoried in Path.md and matching committed bytes.
- WP-6-REQ-061: Path.md WP-6 entry: previous-phase revalidation, entry gate,
  scope, files, code, tests, benchmarks, threats/stops, gates, statuses,
  hashes, commands/exit codes, failures/repairs, log inventory, commit/push,
  exit matrix, compliance verdict.

# WP-6 CONTRACT (H5-successor revision; supersedes the BLOCKED_ON_ENTRY version)

Supersession: the prior revision (compiled under the old entry routing, verdict
WP-6 = BLOCKED_ON_ENTRY, commit 1f43527) is preserved in git history and
Path.md and remains the correct record of that gate. This revision is recompiled
from the AMENDED WorkPlan.md H5-successor law and does not erase the old
reasoning. Original WP-5 PROMOTED_SET_REJECTED remains historical truth.

Binding: CURRENT_PHASE=WP-6, PREVIOUS_PHASE=WP-5 (revalidated COMPLETE with the
rejection terminal) + specialized H5 successor route (K6 63 -> fresh H5 63/63 ->
WP6_ENTRY_SET_FROZEN, hash 9dcdea2b7926cf94765e1fd818a73f0459c72404b4f4bf5c36b3ec65a27e5748).
Authority: WorkPlan.md WP-6 + v0.4.1 spec #5 (theorems), #6 (lifecycle+review),
#9 (bridge pin-or-blocked), #10 (seal/conditional repro/export), #11
(governance/export/successor), #12 (gates/terminals) + prereg/
theorem_gate_matrix.yaml + schemas/review.schema.json +
schemas/theorem_status.schema.json.
Mode: contract compiled 2026-09-28 on branch wp5x-k6c2-specialized BEFORE any
WP-6 implementation (contract lock: implementation must satisfy the contract,
never the reverse).

## Entry predicate (amended WorkPlan law)
- WP-6-REQ-001: SPECIALIZED_H5_WP6_ENTRY (branch == wp5x-k6c2-specialized AND
  H5 terminal == H5_K6C2_SET_SURVIVES_FRESH_HOLDOUT AND wp6_entry_set.status ==
  WP6_ENTRY_SET_FROZEN AND count == 63 AND survivor-set hash ==
  9dcdea2b7926cf94765e1fd818a73f0459c72404b4f4bf5c36b3ec65a27e5748 AND H5
  count/hash agree AND clean-room zero mismatches AND K6/H5 identities bind
  exactly AND identity hashes unchanged AND H5 lifecycle sealed AND no post-H5
  mutation). Verified by scripts/check_wp6_h5_entry_gate.py ->
  artifacts/v04/wp6_h5_entry_gate.json (WP6_H5_ENTRY_PASS). The old
  SURVIVES_FINITE_TESTS-only gate (scripts/check_wp6_entry_gate.py) is
  preserved as historical evidence, not the controlling gate on this branch.
- WP-6-REQ-002: one candidate at a time in the EXACT serialized order of
  artifacts/v04/wp5x_k6c2/h5/wp6_entry_set.json (candidate #1
  P_all|6|2|FLAT(2), identity
  0909c74accb193302d1a9213601567bebcba414de679e362b10ad3007b4fb7fd);
  every candidate artifact carries key/P/k/C/rho/identity/entry-set/source
  hashes; exact refutation retires (preserved/minimized/replayed/hashed, never
  mutated) and advances; first lawful full-route closure stops the search;
  resource-limit leaves a candidate unresolved, never dead; no
  mutation/synthesis/search/new values/dynamic-P/new axis.
- WP-6-REQ-003 (revised placement): PA conjunction machine-checked BEFORE any
  MSTL-17 PROVE step (not an entry requirement); zero REVIEWED MSTL nodes at
  start is EXPECTED; L2 gates ONLY MSTL-19/bridge audit (missing L2 never
  blocks MSTL-08U/09/11/12/13/14/15/17/18).

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
  chain REVIEWED + bridge audited) else an honest terminal from the amended
  WorkPlan set: WP6_H5_ENTRY_PASS, CANDIDATE_REFUTED_AT_<NODE>,
  CANDIDATE_UNRESOLVED_RESOURCE_LIMIT, PROVED_PENDING_HUMAN_REVIEW,
  AWAITING_HUMAN_REVIEW, BRIDGE_BLOCKED_BY_SOURCE, ALL_63_CANDIDATES_REFUTED,
  ALL_63_CANDIDATES_UNRESOLVED_OR_REFUTED, or the spec #12 refuted/no-claim set.
- WP-6-REQ-051: obstructions preserved (L2-absent record kept); successor
  embedding only if its 5 conditions hold.

## Logging/Path
- WP-6-REQ-060: WP-6 STEP <ID> comment+log lines in executing code; final
  line numbers inventoried in Path.md and matching committed bytes.
- WP-6-REQ-061: Path.md WP-6 entry: previous-phase revalidation, entry gate,
  scope, files, code, tests, benchmarks, threats/stops, gates, statuses,
  hashes, commands/exit codes, failures/repairs, log inventory, commit/push,
  exit matrix, compliance verdict.

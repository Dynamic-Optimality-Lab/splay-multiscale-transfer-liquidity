# WP-1 CONTRACT (compiled before implementation; immutable for WP-1)

Binding: CURRENT_PHASE=WP-1, PREVIOUS_PHASE=WP-0 (revalidated VERIFIED_COMPLETE 2026-09-27: run_phase00 green + closure PASS on current tree).
Authority: WorkPlan.md WP-1 + v0.4.1 spec §§2,3,5 + math/theorems/{LIQ0-01,LIQ0-02,MSTL-16}.md + sealed witness bundle (obstruction MST0-14R_LEGAL_WITNESS.json: T0=vine-right-28, H=[D27,D28,K28,K27], steps table, residual_growth table, dep hashes matching parent_contract).

## Entry predicate
- WP-1-REQ-001: FOUNDATION_FROZEN in Path (COMPLETE) + freeze manifest verifies + proof_status 27xUNPROVED.

## Scope (no rho>1, no fresh, no theorems beyond LIQ0-01 evidence)
- WP-1-REQ-002: exact splay/pair under weaker domain incl. absent-key path (cost defined, trace [], tree unchanged, no T7/T5).
- WP-1-REQ-003: ZIG-L/R orientation preserved in trace, normalized to ZIG class.
- WP-1-REQ-004: T5_{P_all,1} single activation + replay equations (A: T7->T5 per StepEv; B: T5 per StepEv; T6 after full B trace; DELETE A-only) in BOTH engines.
- WP-1-REQ-005: LIQ0-01 evidence: (a) operator equality FLAT(1)==T5_1 by construction + Lean rfl; (b) differential primary-vs-independent agreement on corpus; (c) sealed-bundle step-table exact reproduction; (d) residual_growth file-table reproduction (8 rows).
- WP-1-REQ-006: review package (statement+negation+evidence, verdict PENDING-HUMAN); human ACCEPT solicited, never fabricated.

## Files (exact paths)
- WP-1-REQ-007: python/liquidity/legacy_embedding.py (primary, pointer-based).
- WP-1-REQ-008: python/independent/{splay,pair,ledger}.py (tuple-based, zero imports from python/liquidity).
- WP-1-REQ-009: math/proofs/LIQ0-01.md (Layer A) + lean/Liquidity/LegacyEmbedding.lean (Layer B, machine-checked).
- WP-1-REQ-010: math/reviews/LIQ0-01.PACKAGE.md (+ .review.json ONLY on genuine human verdict).
- WP-1-REQ-011: artifacts/v04/obstruction_import/{MST0-14R_LEGAL_WITNESS.json, INDEPENDENT_REPLAY.json} (vendored bytes + SHA record) + n28_replay.json (my reproduction).
- WP-1-REQ-012: artifacts/v04/parent_import/replay/{corpus_report.json} (differential agreement report).
- WP-1-REQ-013: tests/test_legacy_embedding.py (LEG-01..10) + scripts/run_phase01.py (+ runlog record).

## Directories: python/liquidity, python/independent, math/proofs, math/reviews, lean/Liquidity, artifacts/v04/{obstruction_import,parent_import/replay}, tests. Formats: .py exact-int; .json canonical sorted; witness bytes verbatim.

## Independent-verification tuple (no shortening)
INDEPENDENT_AGREEMENT = [final_tree_A, final_tree_B, cost_a, cost_y, need, paid, margin, active_pre, latent_pre, event_trace, canonical_serialization]

## Named-test contract (semantic lock)
- LEG-01: T5_{FLAT(1)} == T5_1 operator equality (unit, all modes/classes incl. ROOT/no-event).
- LEG-02: primary-vs-independent full IV-tuple agreement on differential corpus (>=20k episodes + exhaustive tiny).
- LEG-03: n28 sealed step-table exact reproduction (every L/P/S/a/y/need/paid/margin/rA/rB/dA/dB field).
- LEG-04: residual_growth file-table 8 rows reproduced (28..512); spec-§1 alternate rows recorded as observations only.
- LEG-05: absent-key path (cost, empty trace, unchanged tree/ledger).
- LEG-06: ZIG-L/R normalization to ZIG class with orientation retained.
- LEG-07: share-nothing audit (independent imports nothing from liquidity; AST scan).
- LEG-08: sabotage detection (tampered trace => checker reports MISMATCH; verifies checker soundness).
- LEG-09: determinism (rerun hash match).
- LEG-10: review-package completeness (statement+negation+evidence present; verdict field honest).

## Mutants (each introduced + rejected)
M-WP1-01: skip one activation => LEG-02/03 fail. M-WP1-02: flip ZIG class => LEG-06 fails.
M-WP1-03: spend LATENT in T6 => LEG-02 fails. M-WP1-04: remove ROOT guard (activate on empty trace) => LEG-05 fails.

## Stress: n=1 trees, empty H, absent keys 0/n+1, long histories, malformed witness (rejected by schema-ish asserts), corrupted vendored bytes (hash mismatch fails).

## Theorems/reviews/statuses
- LIQ0-01 Layer A (induction over trace; construction equality for operator part) + Layer B (Lean: t5_rho 1 = t5_one by rfl + energy/support lemmas, machine-checked) + Layer C (differential + sealed agreement). Status advance to PROVED_PENDING_REVIEW on evidence; REVIEWED only on genuine human ACCEPT. MSTL-16 preamble drafted, no status change. No other status moves.

## Threats/stops/invariants: LIQ-T03/T04/T11/T12 controls exercised; LIQ-STOP-03/04/05/06/07/08 armed (STOP-05 on any FLAT(1) divergence => TERM-LEGACY_FAIL); INV-EMBED checked.
## Anti-overfitting: REG family labeled KNOWN/CONTAMINATED; no fresh data (H4L EMPTY re-asserted); finite replay never called proof in package.
## Logging/Path/exit: STEP logs + inventory; runlog record; Path WP-1 entry + closeout; exit LEGACY_SEMANTICS_CERTIFIED (+REVIEWED iff human ACCEPT) else honest BLOCKED_EXTERNAL on review pending.

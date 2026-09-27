# WP-2 CONTRACT (compiled before implementation; immutable for WP-2)

Binding: CURRENT_PHASE=WP-2, PREVIOUS_PHASE=WP-1 (revalidated VERIFIED_COMPLETE 2026-09-27: run_phase01 green + exit gate PASS on current tree).
Authority: WorkPlan.md WP-2 + v0.4.1 spec #2 (mu totalization), #3 (rho class/ladder/forbiddens), #5 (LIQ0/MSTL obligations) + math/theorems/LIQ0-02..10 + MSTL-10/11/12/13 + prereg/liquidity_axis.yaml (frozen content, verified not rewritten).

## Entry predicate
- WP-2-REQ-001: LEGACY_SEMANTICS_CERTIFIED (Path COMPLETE) + LIQ0-01 REVIEWED (proof_status) + freeze manifest verifies + H4L EMPTY (no bank bytes anywhere).

## Scope (no candidates, no repayment/integrability theorems, no fresh data)
- WP-2-REQ-002: mu(ev) total (ROOT/no-event 0, ZIG 1, doubles 2) + ZIG-L/R normalization map.
- WP-2-REQ-003: rho class (rho_ZIG,rho_DOUBLE) 0..8 + FLAT/ROT subfamilies + ladder 12 + ROOT 0 + forbidden-dependency enforcement (static allowlist: mode + normalized class only).
- WP-2-REQ-004: T5_{P,rho} bounded iteration + eligibleLatentCount gating + partial activation + first-eligible order + exact integer books.
- WP-2-REQ-005: diagnostics per KEEP (sealed-compatible record + capacity/actual per side + Q diagnostic-only).
- WP-2-REQ-006: LIQ0-02..10 proofs (A) + Lean machine-checked (B) + differential/independent evidence (C); MSTL-10/MSTL-11 Class-B transport via T5-rho lemmas; MSTL-13 dev lemma; MSTL-12 signed setup; signed T5 accounting defined, Branch B dormant.
- WP-2-REQ-007: review packages ×9; human ACCEPT solicited per theorem, never fabricated.

## Files (exact paths)
- WP-2-REQ-008: python/liquidity/{multiplicity.py, activation.py, profiles.py, diagnostics.py}.
- WP-2-REQ-009: python/independent rho extension (ledger_rho in ledger.py or rho.py; no liquidity imports).
- WP-2-REQ-010: schemas/keep_record.schema.json (exists; verify conformance of diagnostics output).
- WP-2-REQ-011: lean/Liquidity/{Activation,Multiplicity,Preservation}.lean (machine-checked, no sorry).
- WP-2-REQ-012: math/proofs/LIQ0-{02..10}.md + MSTL-{10,11,12,13}-dev notes.
- WP-2-REQ-013: math/reviews/LIQ0-{02..10}.PACKAGE.md (+ .review.json ONLY on genuine verdicts).
- WP-2-REQ-014: tests/test_activation.py (ACT-01..14) + scripts/run_phase02.py + scripts/test_wp2_mutants.py.

## Directories/formats: python/liquidity, lean/Liquidity, math/proofs, math/reviews, tests; .py exact-int deterministic; .json canonical sorted; Lean Init+local imports only.

## Independent-verification tuple (no shortening)
INDEPENDENT_AGREEMENT_RHO = [capacity_per_event, actual_activations, active_pool, latent_pool, energy, support_multiset, first_eligible_order, per_keep_record]

## Named-test contract (semantic lock)
- ACT-01: mu values on all classes + ROOT/no-event 0.
- ACT-02: rho profiles exact (FLAT r=(r,r); ROT r=(r,2r); ladder 12; ROOT 0).
- ACT-03: forbidden-dependency static audit (constructor rejects n/tree/residual/need/future/holdout inputs; AST scan of profiles.py).
- ACT-04: activation counts = min(eligible, cap) + partial behavior + first-eligible order.
- ACT-05: energy conservation across rho ladder on random ledgers (both engines).
- ACT-06: support/provenance preservation + no SPENT resurrection.
- ACT-07: determinism (rerun hash match).
- ACT-08: differential rho agreement primary-vs-independent (ladder × ledgers × events).
- ACT-09: diagnostics schema conformance (keep_record 13 fields) + Q correctness on REG-001 (Q=2) and n512 (Q=2).
- ACT-10: multiplicity present-key (sum mu = depth over corpus) + absent-key (empty trace, zero opportunities).
- ACT-11: 16 §38 mutants killed (mapping below).
- ACT-12: review packages complete + honest verdict states.
- ACT-13: H4L EMPTY re-asserted (no bank bytes).
- ACT-14: LIQ0-01 still REVIEWED (no regression; rerun LEG smoke: n28 exact).

## Mutant mapping (§38, 16; each introduced + rejected by test_wp2_mutants.py)
1 double-step 2→1 (ACT-05/08), 2 ZIG capacity changed (ACT-04/08), 3 rho on n (ACT-03/08), 4 rho on need (ACT-03/08), 5 rho on future key (ACT-03), 6 rho on residual (ACT-03), 7 activation creates credit (ACT-05), 8 changes support (ACT-06), 9 changes provenance (ACT-06), 10 SPENT→ACTIVE (ACT-06), 11 last-LATENT order (ACT-04/08), 12 B-only hidden activation (ACT-08), 13 unbounded (ACT-04), 14 T7 coeff altered (ACT-08), 15 T6 spends LATENT (ACT-08), 16 FLAT(1)!=old T5 (ACT-14/LEG-03).

## Theorems/reviews/statuses
- LIQ0-02..10 → PROVED_PENDING_REVIEW on A+B+C; REVIEWED only on genuine per-theorem ACCEPT. MSTL-10/11 dev PROVED (transport lemmas); MSTL-13 dev lemma; MSTL-12 setup (signed defs, no proof claimed). Others unchanged.
## Threats/stops/invariants: T02/03/04/05/06/13/14/15/17/18; STOP-09/10/11; INV energy/support/prov/nores/det/blind. Axis-wide vs profile-specific gates (ROT dies alone on LIQ0-02 falsity).
## Anti-overfitting: no synthesis; REG labeled; validation blind; leakage static audit; OOD untouched.
## Logging/Path/exit: STEP 40+ logs + inventory; WP-2 runlog record; Path WP-2 entry + closeout; exit LIQUIDITY_AXIS_FROZEN (all PROVED + energy/support/preservation REVIEWED as required by consumers) or AXIS_INCONCLUSIVE.

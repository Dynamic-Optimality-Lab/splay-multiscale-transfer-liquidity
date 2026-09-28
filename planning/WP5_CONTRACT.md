# WP-5 CONTRACT (compiled before implementation; immutable for WP-5)

Binding: CURRENT_PHASE=WP-5, PREVIOUS_PHASE=WP-4 (revalidated COMPLETE 2026-09-28:
PROMOTED_SET_SURVIVES_DEV, 3 identities + outlines, firewall COMMITMENT_PUBLISHED
unlocks 0, zero H4L evaluations).
Mode: initial execution (never claimed complete; no audit findings supplied).
Authority: WorkPlan.md WP-5 + v0.4.1 spec #4 (identity/family IDs, ordering), #8
(reveal protocol, clean-room execution, large-n, OOD), #5 MSTL-22/25 + prereg/
h4l_holdout.yaml + schemas.

## Entry predicate
- WP-5-REQ-001: promoted set + eligibility + firewall COMMITMENT_PUBLISHED +
  clean-room contract frozen + independent evaluator ready (all verified, not cited).

## Scope (finite tests only; finite survival is never a theorem premise)
- WP-5-REQ-002: freeze promoted set + set hash; transition firewall to
  CANDIDATE_SET_FROZEN; reveal ONCE (verify commitment, publish seed+bank to
  artifacts/v04/h4l_reveal/, single transition to REVEALED_ONCE, unlocks 0->1).
- WP-5-REQ-003: clean-room evaluator implemented SOLELY from math/theorems/* +
  clean-room contract + input histories (stdlib only; never imports liquidity/
  solver/adversary/holdout/independent); implementation bytes committed BEFORE reveal.
- WP-5-REQ-004: fresh H4L evaluation of the frozen set in predetermined
  (sorted-key) order until each candidate is exhausted (full 70k) or first violation;
  canonical first/max violations + primary+independent replay bundles.
- WP-5-REQ-005: clean-room agreement (full-bank per-KEEP need/paid equality).
- WP-5-REQ-006: large-n attack sizes [16,32,64,128,256,512,1024,2048,4096] x40
  with per-KEEP diagnostics; OOD battery sizes [24,48,96,192] x2000 = 8000
  (long-range random-walk histories + spine-heavy trees, disjoint stream, labeled OOD).
- WP-5-REQ-007: 16 fresh-context mutants killed; MSTL-22/25 dev notes (no status
  changes); post-freeze edits would mint POST_HOLDOUT IDs (none occur).
- MUST NOT: upgrade finite survival, relabel known witnesses, evaluate before reveal,
  reveal twice, regenerate the bank, touch H4L secret outside the reveal driver.

## Files (exact paths)
- WP-5-REQ-008: planning/WP5_CONTRACT.md (this file).
- WP-5-REQ-009: python/cleanroom/evaluator.py (frozen pre-reveal).
- WP-5-REQ-010: scripts/{run_phase05.py, reveal_h4l.py, emit_wp5_runlog.py,
  test_wp5_mutants.py}; tests/test_fresh_h4l.py (FRSH-01..14).
- WP-5-REQ-011: artifacts/v04/{candidates/commit/set.json, h4l_reveal/,
  cleanroom/{impl_freeze.json, agreement.json}, large_n/, ood/} +
  math/proofs/{MSTL-22-dev,MSTL-25-dev}.md (dev forms only).

## Named-test contract
- FRSH-01: set freeze (3 identities bound, set hash recorded, firewall
  CANDIDATE_SET_FROZEN reached lawfully from COMMITMENT_PUBLISHED).
- FRSH-02: clean-room implementation frozen pre-reveal (bytes committed before the
  reveal commit; stdlib-only import audit).
- FRSH-03: reveal-once (exactly one CANDIDATE_SET_FROZEN->REVEALED_ONCE transition,
  unlocks==1, commitment re-verified at reveal, seed+bank published to h4l_reveal/).
- FRSH-04: revealed bank matches commitment (shard SHAs + total 70000 + sorted IDs).
- FRSH-05: fresh evaluation order/exhaustion (sorted-key order; per-candidate full
  70k or first-violation stop with bundle).
- FRSH-06: clean-room agreement (full-bank per-KEEP need/paid equality, all final).
- FRSH-07: large-n (9 sizes x40, diagnostics recorded, violations recorded).
- FRSH-08: OOD labeled + disjoint (8000 episodes, distribution distinct from H4L
  strata by construction record, zero H4L-ID overlap).
- FRSH-09: second reveal refused (unlocks stays 1).
- FRSH-10: regeneration refused (commitment exists).
- FRSH-11: post-reveal bank reads allowed ONLY via firewall guard (guard passes now).
- FRSH-12: 16 mutants killed (delegates to test_wp5_mutants.py).
- FRSH-13: finite != theorem (MSTL statuses unchanged; no universal claim in bytes).
- FRSH-14: zero pre-reveal evaluations (first-evaluation timestamp strictly after
  reveal timestamp in eval log).

## Mutants (each introduced + killed)
M-WP5-01 tampered shard byte; -02 seed mismatch (wrong seed recompute);
-03 second reveal; -04 regen after reveal; -05 unsorted shard order;
-06 corrupted episode ID; -07 wrong-size episode (n mismatch); -08 illegal history
key; -09 clean-room forbidden import; -10 clean-room/list disagreement injection;
-11 large-n tree-shape corruption; -12 OOD mislabel (H4L stratum name);
-13 H4L-ID reuse in OOD; -14 dropped KEEP record field; -15 verdict flip
ACCEPT->REJECT confusion (review binding); -16 nondeterministic reduce order.

## Logging/Path/exit
- STEP 132+ logs; WP-5 runlog (phase PHASE-14-16); Path WP-5 entry + closeout.
- Exit: SURVIVES_FINITE_TESTS ceiling (>=1 surviving with agreement) or
  per-candidate gate freezes / PROMOTED_SET_REJECTED (fresh). Branch-B activation
  on full fresh rejection is WP-6-owned (record the trigger fact only).

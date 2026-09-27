# WP-3 CONTRACT (compiled before implementation; immutable for WP-3)

Binding: CURRENT_PHASE=WP-3, PREVIOUS_PHASE=WP-2 (revalidated VERIFIED_COMPLETE 2026-09-27: run_phase02 green on current tree).
Mode: initial execution (never claimed complete; no audit findings pasted — verified empty set).
Authority: WorkPlan.md WP-3 + v0.4.1 spec #4 (predicate/scope), #7 (Branch B), #8 (H4L/validation/OOD/clean-room) + prereg/{predicate_family,h4l_holdout,liquidity_search_space}.yaml.

## Entry predicate
- WP-3-REQ-001: LIQUIDITY_AXIS_FROZEN (Path COMPLETE) + LIQ0-01..10 REVIEWED + freeze verifies + H4L EMPTY.

## Scope (no H4L evaluation, no synthesis, no theorems)
- WP-3-REQ-002: predicate family enumerated + definition-hashed (P_all, P_keep, case-restricted canonical enumeration).
- WP-3-REQ-003: (P,k,C,rho) scope locked; validation spec + 9-engine budget tables + OOD spec frozen with exact numbers.
- WP-3-REQ-004: H4L generator implemented from WP-0 contract + certified hash-equivalent; bank generated to OPERATOR-SECRET storage only; commitment (sha256(seed||bank)+metadata) published; secret seed never in repo.
- WP-3-REQ-005: firewall automaton (7 states, readers/writers, unlock<=1, fail-closed); reveal() fails before CANDIDATE_SET_FROZEN.
- WP-3-REQ-006: clean-room contract (spec + boundary + I/O schema) frozen; implementation bytes are WP-5-owned (not built here).
- WP-3-REQ-007: dormant Branch-B identities/grammar frozen (signed defs, status DORMANT, no synthesis).
- WP-3-REQ-008: human ACCEPT on generator/commitment hashes (genuine, never fabricated).

## Files (exact paths)
- WP-3-REQ-009: python/holdout/{h4l_generate.py, h4l_verify.py, firewall.py} + h4l_evaluate.py STUB (import = fail).
- WP-3-REQ-010: artifacts/v04/holdouts/{h4l_commitment.json, firewall_state.json} (public metadata ONLY).
- WP-3-REQ-011: artifacts/v04/cleanroom/contract/{spec.md, boundary.md, io_schema.json}.
- WP-3-REQ-012: artifacts/v04/candidates/branchB/{dormant identities}.
- WP-3-REQ-013: prereg updates (predicate hashes, budget tables, OOD counts) + freeze manifest rebuilt.
- WP-3-REQ-014: tests/test_holdout_firewall.py (HOLD-01..14) + scripts/run_phase03.py + emit_wp3_runlog.py.

## Secret layout (outside repo, never committed): $H4L_SECRET/{seed.bin, bank/*.json.zst, manifest.json}. Default: Temp/h4l-secret. .gitignore guards.

## Named-test contract
- HOLD-01: generator contract frozen (params match prereg).
- HOLD-02: implementation certified (reproduces commitment on tiny banks; code hash recorded).
- HOLD-03: real bank generated to secret storage; repo contains zero bank bytes/seeds.
- HOLD-04: commitment verifies (recompute from secret store).
- HOLD-05: pre-reveal read via firewall fails closed.
- HOLD-06: second unlock/reveal fails closed.
- HOLD-07: regen-after-reveal fails closed.
- HOLD-08: repo-wide scan finds no seed/bank material.
- HOLD-09: predicate family closed + hashed (P_all, P_keep + enumerated case predicates).
- HOLD-10: scope lock (search space exact; no template terms).
- HOLD-11: clean-room contract frozen (spec/boundary/schema present).
- HOLD-12: dormant Branch-B set frozen (signed defs, DORMANT).
- HOLD-13: validation/adversarial/OOD tables exact.
- HOLD-14: zero H4L evaluations logged (evaluation stub refuses).

## IV tuple: N/A (no theorem-facing computation in WP-3; firewall + generator tested directly). Stated explicitly, not proxied.
## Mutants: firewall-bypass attempts (read-before-freeze, double-reveal, regen, seed-in-repo, quota violation, stratum bleed) — each must fail closed.
## Stress: tiny-bank determinism (same seed => identical bank), empty-size edge, dedup resample cap, malformed commitment rejected, wrong-seed reveal rejected.
## Logging: STEP 80+ logs; WP-3 runlog (phase PHASE-07-08); Path WP-3 entry + closeout.
## Exit: H4L_COMMITMENT_PUBLISHED + TRANSFER_GRAMMAR_FROZEN (zero evaluations) or STOP terminals.

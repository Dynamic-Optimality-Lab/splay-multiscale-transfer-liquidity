# WP-0 CONTRACT (compiled before implementation; immutable for WP-0)

Binding: CURRENT_PHASE=WP-0, PREVIOUS_PHASE=NOT_APPLICABLE (no earlier WP; pre-foundation audit instead).
Authority: WorkPlan.md WP-0 + v0.4.1 spec §§1,9,10,11 + amendment CC-001/002/003/032/034/040/041/042/043/044/045/046/047/048/049/051 + planning matrices.

## Entry predicate
- WP-0-REQ-001: CONTRACT_CLOSURE_PASS + WORKPLAN_COVERAGE_PASS hold on current tree (rerun, not cited).

## Pins (spec §1)
- WP-0-REQ-002: arch nav/closure/seal full SHAs verified reachable (clone/API): 8958891…/9859e65…/3062c018….
- WP-0-REQ-003: obstruction evidence commit 19ef254… verified; lifecycle OPEN recorded; never called sealed.
- WP-0-REQ-004: content SHA-256 re-verified for transfer_grammar_v0.3.yaml, event_ontology_v0.3.yaml, mstc0002.py, splay.py against prereg/parent_contract.yaml.
- WP-0-REQ-005: prereg/bridge_manifest.yaml created (L3 record + L2-absent => MSTL-19 BLOCKED_BY_SOURCE path).

## Freeze (spec §§1,8,10)
- WP-0-REQ-006: prereg/freeze_manifest.sha256 over all prereg/*.yaml (+ itself excluded, no-self-hash); recomputation verifies.
- WP-0-REQ-007: H4L generator CONTRACT frozen (params already exact in prereg/h4l_holdout.yaml); no implementation bytes required yet.
- WP-0-REQ-008: v03/history/ exact nav-tree import (566 blobs) + byte-equality manifest (SHA-256 per file); tree disposition extended to full manifest.
- WP-0-REQ-009: 224 parent controls import-verified (count + vocabulary).
- WP-0-REQ-010: WORKPLAN_COVERAGE_PASS rerun post-freeze.
- WP-0-REQ-011: env lock values: python 3.13.7 + dep hashes, Lean v4.21.0 + lakefile + lean-toolchain + lake-manifest.json committed; solver policy (stdlib-only exact, no external binaries); RNG/zstd/hash recorded.
- WP-0-REQ-012: math/proof_status.json: 27 theorems, truth UNPROVED, prove UNPROVED, refute NO_WITNESS, null hashes.

## Code
- WP-0-REQ-013: python/audit/verify_parent.py — full-SHA reachability + content-hash compare + ledger counts (26 arch rows) + toolchain string; fail-closed codes.
- WP-0-REQ-014: python/audit/log.py — 33-field runlog writer (exact required set); one execution record emitted for the phase00 run with all fields populated.
- WP-0-REQ-015: scripts/run_phase00.py — executes checks in order with [WP-0][STEP xx] logs; exit 0 iff all green.
- WP-0-REQ-016: tests/test_foundation.py — named tests below, exact meanings, incl. 2 negative probes.

## Named-test contract (semantic lock)
- TEST-F-01: arch nav commit reachable and equals pin.
- TEST-F-02: arch closure commit reachable.
- TEST-F-03: arch seal commit reachable.
- TEST-F-04: obstruction evidence commit reachable; message contains witness marker.
- TEST-F-05: 4 content SHA-256 match parent_contract.
- TEST-F-06: bridge manifest valid; L2-absent recorded.
- TEST-F-07: env lock python matches runtime; lean string exact.
- TEST-F-08: freeze manifest recomputation verifies.
- TEST-F-09: proof_status 27 rows, all UNPROVED/NO_WITNESS/null hashes.
- TEST-F-10: v03/history manifest verifies (sample-full: every file rehashed).
- TEST-F-11: closure checker PASS.
- TEST-F-12: coverage checker PASS.
- TEST-F-13: 27 theorem files present, each with Negation: + First consumer:.
- TEST-F-14: gate matrix exact 26-key set.
- TEST-F-15 (negative): corrupted freeze-manifest copy fails verification (fail-closed probe).
- TEST-F-16 (negative): missing required artifact makes run_phase00 exit nonzero.

## Independent verification tuples
- PINS_AGREE = [local clone cat-file, GitHub API commit records, parent_contract values] all equal per SHA.
- CONTENT_AGREE = [re-downloaded raw bytes SHA-256, parent_contract content hashes] equal per file.
- No shared logic between verify_parent.py (API+hashlib) and test_foundation.py (file/assert layer) beyond data files.

## Logging/Path/exit
- WP-0-REQ-017: second grep audit (independent counts: CC 66, theorems 27, firewall 7, lifecycle 13, sections 12).
- WP-0-REQ-018: clean-tree gate enforced for authoritative records.
- WP-0-REQ-019: Path.md WP-0 entry + log inventory (final line numbers) + closeout; append-only.
- WP-0-REQ-020: exit FOUNDATION_FROZEN; commit `v0.4.1 WP-0 FOUNDATION_FROZEN`; push; HEAD verified; tree clean.
- MUST NOT: synthesis, theorems, H4L bytes/generation, fresh claims.

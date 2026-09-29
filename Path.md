# Path.md — SPLAY-AM-MST-LIQ-v0.4.1 live execution ledger

**Experiment:** `SPLAY-AM-MST-LIQ-v0.4` + `v0.4.1` closure | **Operative spec:** `IMPLEMENTATION_SPEC_SPLAY-AM-MST-LIQ-v0.4.1.md` | **Status:** `CONTRACT_CLOSED__WORKPLAN_COMPILED__SCIENCE_NOT_AUTHORIZED_UNTIL_WP0_GATE`
**Rule (normative, spec §11):** append-only, contemporaneous WP/gate updates; failed/superseded history preserved and marked; each WP ends `FOLLOWS WorkPlan.md` / `DEVIATION — VERSIONED AND JUSTIFIED` / `NONCOMPLIANT — BLOCKED`. A gate without entry is not closed. Superseded v0.4 planning preserved in `historical/` + git history.

## R-001 — Contract-closure campaign (CC-001..CC-066)
- Scope: hostile repair of the normative spec itself (not science, not WorkPlan patching).
- Sources inspected: LIQ-v0.4 bytes (SHA `0E2C16…055B`); old WorkPlan/Path drafts; arch `IMPLEMENTATION_SPEC_v0.3` + live WorkPlan + ledger + theorem status (9/5/3/3/6) + `transfer_grammar_v0.3.yaml` (no predicate menu — verified) + `event_ontology_v0.3.yaml` (single-ZIG classes) + prereg blob SHAs; obstruction WorkPlan/Path + `mstc0002.py` (blob `2bbecbc`: T7→T5 A-side, T5 B-side, discharge-after-B, DELETE A-only) + `splay.py` (blob `b8f3542`: absent-key empty trace + defined cost) + lean-toolchain (`v4.21.0`) + bridge record (L3 present/L2 absent); live commit APIs (arch nav/closure/seal, obstruction evidence HEAD).
- Conflicts found: exact-[n] vs subset domain; universal-legality sentence vs total algebra; present-key multiplicity vs empty traces; predicate-free T5; uncomposed replay; total-vs-eligible counts; open P_inherited; grammar/scope ambiguity; underparameterized rho; ladder-vs-axis; prose-only theorems; 16/26 mapping; missing MSTL-09; implicit PA conjunction; ambiguous provenance; Branch-B trigger/lateness/signed gaps; recommended H4L params; public-repo quarantine; missing automaton; WP-0/WP-3 freeze split; top-3 overclaim; missing refutation lifecycle; 3-routes contradiction; + 38 majors/hardening (see ledger).
- Repairs: 66 CLOSED via amendment + consolidated spec + 27 theorem files + 26-node gate matrix + provenance/control/tree matrices + prereg (predicate/axis/space/H4L/env/threat/stop/parent-contract/bridge) + 7 schemas + lifecycle/ledger/review/export contracts + true-commitment firewall + matched baseline + OOD + clean-tree/superset-logging/artifact/seal/conditional-repro/bootstrap/governance/successor-embedding rules.
- Failed attempts: closure checker caught 3 self-defects mid-campaign (over-broad status regex ×2 fixed by scoping to status fields; env data shape fixed by splitting value/source); 7/16 mutants initially survived → checker hardened with exact-set assertions → 16/16 killed. Preserved here as history.
- Results: `CONTRACT_CLOSURE_PASS` (66/66, 0 errors); `MUTATION_RESULT = ALL_16_KILLED`; second pass CLOSED with 0 unmapped.
- Commits: repair series (1/5) `6aa63ed`, (2/5) `4f82a55`, (3/5) scripts commit; planning regen + seal follow.
- Verdict: `FOLLOWS` the closure task order (spec → planning → science).

## R-002 — Planning regeneration (Rule 40)
- Old v0.4 WorkPlan/Path/inventory/coverage marked superseded (`historical/` + git); regenerated from closed bytes: inventory 457 items, coverage 457 mappings, new 7-WP WorkPlan above, this ledger.
- Checker: `WORKPLAN_COVERAGE_PASS` — NORMATIVE 457 / MAPPED 457 / UNMAPPED 0 / UNKNOWN 0 / PHASE 0 / THEOREM 0 / GATE 0 / THREAT 0 / STOP 0 / FIRST-CONSUMER 0 / HOLDOUT 0 / CLAIM 0.
- Verdict: `FOLLOWS WorkPlan.md` (v0.4.1 planning phase).

## R-003 — Repair-series push + HEAD verification (Rule K)
- Commits: (1/5) `6aa63ed` ledger+matrices+second-pass; (2/5) `4f82a55` amendment+spec+prereg+theorems+schemas; (3/5) scripts commit (checker+mutations+builders); (4/5) `e4376a1` regenerated planning (457 inventory + coverage PASS + v0.4.1 WorkPlan + this ledger).
- Push: `5976219..e4376a1 master -> master` to `origin` (splay-multiscale-transfer-liquidity).
- HEAD: `git ls-remote` = local `e4376a1215fc0091e90c2416b94d855754b9020f` — agree.
- Gates at seal: `CONTRACT_CLOSURE_PASS` (66/66, 0 errors) + `ALL_16_KILLED` + `WORKPLAN_COVERAGE_PASS` (457/457, 0 errors).
- Verdict: `FOLLOWS WorkPlan.md` (v0.4.1 planning seal; WP-0 execution may now begin).

## WP-0 ledger (PHASE 00) — EXECUTION RECORD
- Phase/scope: WP-0 foundation (WorkPlan.md v0.4.1 WP-0; contract planning/WP0_CONTRACT.md WP-0-REQ-001..020).
- Previous-phase verification: NOT_APPLICABLE (WP-0 is first; N=0 binding). Pre-foundation audit instead: CONTRACT_CLOSURE_PASS + WORKPLAN_COVERAGE_PASS rerun green on current tree before implementation.
- Entry gate: WP-0-REQ-001 PASS (both checkers green); no other prerequisites. Entry-gate result: PASS.
- Normative sources: consolidated spec §§1,9,10,11; amendment CC-001/002/003/032/034/040–048/049/051; provenance/control/tree matrices; parent blobs.
- Files created: v03/history/ (566-file nav-tree import) + v03/byte_manifest.sha256.yaml + v03/key_content_hashes.yaml + v03/obstruction_content_hashes.yaml; prereg/parent_contract.yaml (extended w/ content SHA-256), bridge_manifest.yaml (L3 verified e23ea8b5…5a78, L2 absent), environment_lock.yaml (values), freeze_manifest.sha256 (11 files); math/proof_status.json (27 rows); lean-toolchain, lakefile.lean, lake-manifest.json; python/audit/verify_parent.py + log.py; scripts/run_phase00.py + verify_freeze.py + init_proof_status.py + gen_manifest.py + fetch_obstruction_hashes.py; tests/test_foundation.py (TEST-F-01..16); planning/WP0_CONTRACT.md; artifacts/v04/logs/run_*.json (35-field record).
- Files modified: IMPLEMENTATION_SPEC_SPLAY-AM-MST-LIQ-v0.4.1.md (one-word fix 33→35 fields, recorded), python/audit/verify_parent.py (2 repairs), scripts/verify_freeze.py (malformed-manifest hardening), python/audit/log.py (line-19 merge repair + 35-field wording).
- Code/algorithms: clone cat-file pin checks; SHA-256 recomputation (hashlib); raw-download hashing (urllib); freeze manifest (sorted, no-self-hash); 33→35-field runlog writer with structural asserts; ordered phase runner (closure→pins→freeze→pytest→coverage, fail-closed codes 2); pytest suite incl. full 566-file rehash (F-10) and negative probes.
- Schemas: runlog (35/35 validated), proof_status (27 rows), freeze manifest format, byte manifest format.
- Tests: TEST-F-01..16 → 16 passed. Benchmarks: seal/hash/count verifications (no synthesis).
- Stress/negative: (1) corrupted prereg → freeze FAIL + runner exit 2, restored PASS; (2) deleted MSTL-09.md → F-13 FAIL, restored 16/16; (3) malformed manifest line → clean blocked message + nonzero, restored PASS.
- Anti-overfitting: N/A (no data synthesized; H4L EMPTY asserted by F-16).
- Threats/stops/invariants: LIQ-STOP-01/02 handlers exercised via verify_parent fail-closed paths; clean-tree recorded per run.
- Gates: FOUNDATION_FROZEN claimed (all green); no mismatch/UNAVAILABLE branch taken (bridge L2-absent recorded as BLOCKED_BY_SOURCE path for MSTL-19, not a freeze failure).
- Statuses changed: none (all theorems remain UNPROVED/NO_WITNESS; no statuses copied from parents).
- Hashes: arch nav/closure/seal + 4 content SHA-256 + L3 full SHA-256 + freeze manifest + byte manifest (566, 50,031,167 bytes, 0 mismatches vs clone ground truth: 566/566 paths, 0/566 hash diffs).
- Commands/exit codes: run_phase00 exit 0; pytest 16 passed; both checkers PASS; 3 red-team attacks killed then restored green.
- Failures/repairs: parents[1]→parents[2] path bug; ledger-key nesting bug; 33→35 field count fix; log.py line-19 merge; malformed-manifest traceback → clean block. All repaired + rerun.
- Deviations: none from contract. External blockers: none.
- Log inventory: run_phase00.py emitter L14, comments L28/33/38/43/48 (STEP 03/04/05/06/07); verify_parent.py L13/17/48 (STEP 01); log.py L20/36 (STEP 02); verify_freeze.py L19/28/31/34 (STEP 05); init_proof_status.py L11 (STEP 09); gen_manifest.py L18/22; fetch_obstruction_hashes.py L11/14. References match committed bytes below.
- Exit matrix: REQ-001..020 all PASS (contract reconstruction audit agrees; no missing/partial/unauthorized-substitution/mismatch items).
- Compliance audit: requirements_checked=20 contract REQs + 16 named tests + 12 spec-section semantics; gaps_found=5 (all above); gaps_repaired=5; remaining_compliance_gaps=0.
- Commit/push: (next entry R-004).
- Final verdict: WP-0 = COMPLETE (FOUNDATION_FROZEN).

## WP-1 ledger (PHASEs 01-04) - EXECUTION RECORD
- Phase/scope: WP-1 trusted core (WorkPlan.md v0.4.1 WP-1; contract planning/WP1_CONTRACT.md).
- Previous-phase verification: WP-0 VERIFIED_COMPLETE (fresh rerun 2026-09-27: run_phase00 green + closure PASS; Path WP-0 entry accurate; code/artifacts match).
- Entry gate: FOUNDATION_FROZEN (COMPLETE) + freeze manifest verifies + proof_status shape 27xUNPROVED at start. Result: PASS.
- Normative sources: spec sections 2,3,5; math/theorems LIQ0-01/LIQ0-02/MSTL-16; sealed bundle MST0-14R_LEGAL_WITNESS.json (T0=vine-right-28, steps table, 8-row residual table; dep hashes match parent_contract) + INDEPENDENT_REPLAY.json.
- Files created: python/liquidity/legacy_embedding.py (pointer engine + clone_tree + balanced + domain/mode guards); python/independent/splay.py + pair.py + ledger.py (tuple engine, AST-verified share-nothing); math/proofs/LIQ0-01.md + MSTL-16-preamble.md; lean/Liquidity/LegacyEmbedding.lean (lean 4.21.0 exit 0, no sorry); math/reviews/LIQ0-01.PACKAGE.md + LIQ0-01.review.json (genuine human ACCEPT 2026-09-27); artifacts/v04/obstruction_import (witness, replay, n28_replay.json REPRODUCED_EXACT); artifacts/v04/parent_import/replay/corpus_report.json (40152 episodes, 0 mismatches); tests/test_legacy_embedding.py (LEG-01..10); scripts/run_phase01.py + test_wp1_mutants.py + split_independent.py; planning/WP1_CONTRACT.md; runlog record for phase01 run.
- Files modified: math/proof_status.json (LIQ0-01 to REVIEWED with hashes; 26 stay UNPROVED).
- Code/algorithms: iterative pointer-splay + recursive tuple-splay; oriented ZIG events normalized to ZIG class; T5 first-eligible single activation; replay equations (A-side T7 then T5 per StepEv, B-side T5 per StepEv, T6 after full B trace, DELETE A-only); absent-key empty-trace branch; margin = P2+paid-need (sealed formula) + liq_slack; S0 pre-access; domain [n] + mode fail-closed guards.
- Tests: LEG-01..10 - 10 passed. Benchmarks: 40,152-episode differential (vines, mirrors, sparse, DDKK, incl. event traces) 0 mismatches; n28 72/72 fields exact; margin family 11/11 exact (8 file rows + 3 spec rows).
- Stress/negative: n=1, empty H, sparse/absent keys, out-of-range and bad-mode raises, malformed witness detected, missing PACKAGE fails. Engine mutants M-WP1-01..04 ALL KILLED (M-02 kill required adding event traces to the IV tuple - gap found and repaired).
- Anti-overfitting: REG family labeled KNOWN/CONTAMINATED; H4L still EMPTY; finite evidence labeled support-only in package.
- Threats/stops/invariants: T03/T04/T11/T12 exercised; STOP-05 armed (no divergence seen); INV-EMBED checked.
- Gates: LEGACY_SEMANTICS_CERTIFIED (replays agree + n28 exact + LIQ0-01 REVIEWED).
- Statuses: LIQ0-01 UNPROVED to PROVED_PENDING_REVIEW to REVIEWED (hashes bound); all others unchanged.
- Hashes: thm 64d5ef83, proof af34f42e, lean 020ae608, package c7fd93c7; corpus aada201c; vendored witness 4b235b65 / b0238eb9.
- Commands/exit codes: run_phase01 exit 0 (pre- and post-review); pytest 10 passed; lean exit 0; mutants 4/4 killed.
- Failures/repairs: A/B aliasing fixed by clone_tree; sealed-schema alignment (margin/S0/L1-P1/L2-P2/rB/dA-dB, 4 iterations); LEG-06 needed left-vines (vine_left added both engines); mutant-probe path-order bug; M-WP1-02 survival led to traces in IV tuple; one-off patch helper removed after use.
- Deviations: none. External blockers: none (human review obtained genuinely, not fabricated).
- Log inventory: run_phase01.py STEP 30/31/32 + RUN/DONE emitter; legacy_embedding STEP 10/11/12/13/14/15/15a/21/23/25; splay.py 16a/17/24/26; ledger.py 16c/18/19/20; pair.py 16b; test_wp1_mutants.py STEP 33; split_independent.py retained as split provenance.
- Exit matrix: all WP-1 exit conditions PASS.
- Compliance: 20+ REQs + 10 tests + 11-observable IV tuple exact; gaps_found=8; gaps_repaired=8; remaining_compliance_gaps=0.
- Commit/push: (R-005 below).
- Final verdict: WP-1 = COMPLETE (LEGACY_SEMANTICS_CERTIFIED).

## WP-2 ledger (PHASEs 05–06) — PLACEHOLDER, NOT STARTED
PENDING. Entry requires LEGACY_SEMANTICS_CERTIFIED + LIQ0-01 REVIEWED.

## WP-3 ledger (PHASEs 07–08) — PLACEHOLDER, NOT STARTED
PENDING. Entry requires LIQUIDITY_AXIS_FROZEN. H4L firewall: EMPTY (no secret generated).

## WP-4 ledger (PHASEs 09–13) — PLACEHOLDER, NOT STARTED
PENDING. Entry requires TRANSFER_GRAMMAR_FROZEN + COMMITMENT_PUBLISHED.

## WP-5 ledger (PHASEs 14–16) — PLACEHOLDER, NOT STARTED
PENDING. Entry requires promoted set.

## WP-6 ledger (PHASEs 17–19) — PLACEHOLDER, NOT STARTED
PENDING. Entry requires SURVIVES_FINITE_TESTS. DO only iff chain REVIEWED + bridge audited.

## R-004 — WP-0 push + HEAD verification
- Commit: 553aecb980fa34093dde79e3db43df737a70cf5b (v0.4.1 WP-0 FOUNDATION_FROZEN).
- Push: cc7527f..553aecb master -> master (origin).
- HEAD: ls-remote 553aecb == local 553aecb — agree.
- Tree: clean (verified next).


## R-005 - WP-1 push + HEAD verification
- Commit: 57e480dbedea60914a185fb899a7156ab83baa5e (WP-1 LEGACY_SEMANTICS_CERTIFIED).
- Push: 6e74cae..57e480d master -> master (origin).
- HEAD: ls-remote 57e480d == local 57e480d - agree.
- Tree: clean (pycache removed + gitignored).

## R-006 - WP-1 metadata closure (surgical, semantics unchanged)
- Fixed: PACKAGE 40,372->40,152; proof 25k-episode->40,152-episode differential corpus; PACKAGE corpus sha aada201c->56d24267df90d2a4f23b83ae374a5d27bf4f15d0a60650075b830d1f4ca22c0b (authoritative corpus_report.json 40152/0).
- Rebound: proof_hash 82e993fd, package_hash 56c630b5, corpus_sha added in LIQ0-01.review.json; proof_status.json proof_hash updated. Verdict ACCEPT + REVIEWED preserved (metadata rebind only, not a new review). Line 67 old hash preserved as history.
- Sanity: stale-grep clean in math/planning; LEG 10/10 passed.
- Label: WP-1 METADATA_CLOSURE_PASS.

## R-007 - WP-1 execution-governance repair
- Portable Lean: hardcoded Temp path removed; resolve via LEAN_EXE-or-PATH + version pin from ./lean-toolchain (4.21.0); mismatch/absence exits 2. This-machine runs pass LEAN_EXE in environment (not repo bytes).
- Exit gate scripts/check_wp1_exit_gate.py (STEP 34): review exists + ACCEPT + theorem/proof/package/corpus hashes match bytes + proof_status REVIEWED + hash consistency; tamper probe FAILs closed, restore PASSes.
- Run logging: real WP-1 record artifacts/v04/logs/run_wp1_2026-09-27T181233.2671070000.json (wp=WP-1, phase=PHASE-01-04, clean_tree=true, env 7d564c28, exit 0, 0 missing fields); old WP-0/PHASE-00 record preserved as history.
- Reruns: LEG 10/10, Lean exit 0, gate PASS, mutants 4/4 killed.
- Label: WP-1 EXECUTION_GOVERNANCE_PASS.

## WP-2 ledger (PHASEs 05-06) - EXECUTION RECORD
- Previous: WP-1 VERIFIED_COMPLETE (run_phase01 green + gate PASS, artifacts match).
- Entry: LEGACY_SEMANTICS_CERTIFIED + LIQ0-01 REVIEWED + freeze verifies + H4L EMPTY. PASS.
- Created: python/liquidity/{multiplicity,activation,profiles,diagnostics}.py; independent rho ext (rho_cap/activate_bounded/energy_of); lean/Liquidity/{Activation,Multiplicity,Preservation}.lean (all lean 4.21.0 exit 0, no sorry); math/proofs/LIQ0-02..10.md + MSTL-{10,11,13}-dev + MSTL-12-setup; math/reviews 9 PACKAGES + 9 review.json (genuine 9x ACCEPT); tests/test_activation.py (ACT-01..14); scripts/run_phase02.py + test_wp2_mutants.py + emit_wp2_runlog.py + gen_liq0_packages.py; planning/WP2_CONTRACT.md; WP-2 runlog record.
- Modified: math/proof_status.json (LIQ0-02..10 to REVIEWED); prereg/liquidity_axis.yaml (range 0..8->0..12: ROT(5/6) exceeded box; spec/checker/RMAX updated, closure re-PASS, freeze manifest rebuilt); IMPLEMENTATION_SPEC 33-field note already 35 (WP-0).
- Tests: ACT 14/14. Benchmarks: differential rho 3600 cases 0 mismatch; multiplicity corpus; Q REG-001=2/n512=2; H4L EMPTY; ACT-14 no-regression (n28 exact, LIQ0-01 REVIEWED).
- Stress/negative: empty ledger, ROOT zero-cap, 200-credit ROT(6), unknown predicate/mode raises, missing PACKAGE fails, corrupted witness detected. Mutants 16/16 KILLED (M02 needed ZIG ev; M03-06 forbidden-key evs; M10 needed SPENT books + ROT(4); template NameError + dispatch bugs fixed).
- Anti-overfitting: no synthesis; REG labeled; leakage AST audit; OOD untouched.
- Gates: LIQUIDITY_AXIS_FROZEN (9 PROVED + energy/support/preservation REVIEWED; 9x genuine ACCEPT).
- Statuses: LIQ0-02..10 PROVED_PENDING_REVIEW to REVIEWED (hashes bound); rest unchanged.
- Log inventory: multiplicity 40/41/42; profiles 43/44/45; activation 46/47/48/49; diagnostics 50/51; run_phase02 66/67/68/69/70; mutants STEP 60; emit STEP 71.
- Exit matrix: all PASS. Compliance: gaps_found=12 (RMAX box, AST builtins, count threshold, probe template/dispatch/ev-gaps, tautology Lean lemma, setActive energy flaw, structure-eta, ih-rewrite); gaps_repaired=12; remaining_compliance_gaps=0.
- Final verdict: WP-2 = COMPLETE (LIQUIDITY_AXIS_FROZEN).

## R-008 - WP-2 push + HEAD verification
- Commits: 89f463f (WP-2 work) + ledger/record commit.
- Push: e0b9284..02a67fd master -> master (origin).
- HEAD: ls-remote 02a67fd == local 02a67fd - agree. Tree clean.

## R-009 - HEAD resync + WorkPlan range fix
- WorkPlan WP-2 Scope corrected 0..8 -> 0..12 (matches operative spec section 3 + prereg/liquidity_axis.yaml range [0, 12]).
- R-008 recorded HEAD 02a67fd because 3668db2 was the commit carrying R-008 itself; superseded here.
- Repair commit 5992c7f pushed 3668db2..5992c7f; ls-remote == local == 5992c7f. Remote/local HEAD now 5992c7f.

## R-010 — WP-3 R1 seal + genuine human REJECT (preserved history, not a completion)

- R1 implementation commit: `9dde18c` (pushed `3340c38..9dde18c`, ls-remote == local).
- R1 seal executed once via `python scripts/run_phase03.py` exit 0: firewall
  EMPTY→GENERATOR_FROZEN→BANK_GENERATED_SECRET→COMMITMENT_PUBLISHED; 70,000 episodes
  (7×10k) to operator-secret storage only; HOLD-01..14 = 14/14; independent
  recompute OK.
- R1 identity: generator sha256
  `f5dd09ec3cb381e68e8c92c928e5a53a7f4092534e6d267dd93b4a4f3e81afd6`;
  commitment `4b33e033b9f8f23f9eb97e88080d49048d17cca797d2be56f4d896474620811b`.
- Human REQ-008 review solicited genuinely (never fabricated). Verdict: **REJECT**.
- Root defects (implementation, not contract): D-R1-01 modulo-biased `randbelow`;
  D-R1-02 six strata ignoring sampled L; D-R1-03 unsorted shard serialization +
  unsorted logical stream; D-R1-04 verifier accepting 2..16 without ID/order checks;
  D-R1-05 HOLD suite accepting lengths through 16 without forced-L coverage.
- R1 artifacts archived unchanged:
  `artifacts/v04/holdouts/rejected_R1/h4l_commitment_R1_REJECTED.json`,
  `artifacts/v04/holdouts/rejected_R1/firewall_state_R1_REJECTED.json`;
  R1 secret bytes retired to `Temp/opencode/h4l-secret-R1-rejected` (never reused,
  never revealed, never evaluated). Zero H4L evaluations and zero reveals throughout.
- Verdict: R1 = REJECTED. No completion was ever claimed for WP-3.

## R-011 — WP-3 R2 repair (pre-generation; bank R1 never regenerated)

- Recovery authorized by `planning/WP3_RECOVERY_R2.md` (new bank identity H4L-R2,
  canonical paths rebound after R1 archival — a new lifecycle, not a backwards reset).
- Repairs: R-R2-01 rejection-sampled exact-uniform `randbelow`; R-R2-02 exact-L in
  all 12 strata (motifs preserved); R-R2-03 sorted episode IDs + canonical logical
  stream + `bank_id`/`supersedes`; R-R2-04 verifier 2..8 + ID recompute + order +
  shard + logical + quota checks (also fixed a real tuple-vs-string quota-key bug the
  new check exposed); R-R2-05 HOLD suite (forced-L 12x7, RNG/modulo kill, 5 mini-bank
  verifier probes incl. positive control).
- Pre-seal battery: `python -m pytest tests/test_holdout_firewall.py -q -rs` →
  18 passed, 3 skipped (post-seal-only: HOLD-03/04/07); full ACT+LEG regression rerun
  at closeout.
- Freeze manifest rebuilt and PASS; predicate hashes re-verified (sha256(definition),
  16/16); `h4l-val|` typo fixed; `.gitignore` secret quarantine added.
- Next (authorized order): commit B1 (repairs, pre-generation) → push → fresh seal
  with fresh seed → verify → full HOLD → new human ACCEPT request. WP-4 not entered.

## R-012 — WP-3 R2 seal (fresh bank identity H4L-R2; acceptance pending)

- Repair commit B1: `456a712` (pushed `9dde18c..456a712`, ls-remote == local, tree
  clean at seal start). Generator R2 committed BEFORE generation: PASS.
- R2 seal via `python scripts/run_phase03.py` exit 0 on the committed tree:
  STEP 94 entry PASS (freeze PASS, firewall EMPTY); STEP 95 pre-seal 18 passed +
  3 post-seal skips; STEP 96 EMPTY→GENERATOR_FROZEN; STEP 97 one-shot seal with a
  FRESH 256-bit seed in a FRESH secret directory (R1 seed/dir retired untouched);
  70,000 episodes sorted by episode ID; STEP 98 independent recompute OK
  (70000 episodes, order+IDs+shards+logical OK — this streaming audit enforces the
  2..8 history law and canonical order over every episode without exposing any
  secret content); STEP 99 post-seal HOLD 21/21.
- R2 identity: generator sha256
  `60cc25fcda6fb35850ca216bba6737653d56889da8cb288fed967b0d29ce68b6`;
  commitment `bfcc24ab070a88c63f54c084bae7de357d2f059c9b79775274b4ca6141b1643d`
  (`bank_id` H4L-R2, `supersedes` R1 `4b33e033…`; `generator_sha256` bound).
- Public review artifacts (repo, untracked until closeout):
  `artifacts/v04/holdouts/h4l_commitment.json`,
  `artifacts/v04/holdouts/firewall_state.json`
  (state COMMITMENT_PUBLISHED, unlocks 0). Seed/bank absent from repo (HOLD-08 PASS).
- Mutants killed: modulo-bias randbelow, len-9/16 histories, fixed-length-ignoring-L
  (forced-L 84 combos), mirror doubling, unsorted IDs, corrupted ID, wrong logical
  order, quota violation, read-before-freeze, double-reveal/second-unlock, regen,
  seed-in-repo, evaluation-stub call.
- Regression: ACT-01..14 + LEG-01..10 = 24/24 green (`pytest
  tests/test_activation.py tests/test_legacy_embedding.py -q`).
- H4L evaluations = 0 (stub refuses; HOLD-14). H4L reveals = 0 (unlocks 0; HOLD-05/06).
  R1 attempt preserved in R-010 + `rejected_R1/` + `planning/WP3_RECOVERY_R2.md`.
- Status: awaiting new genuine human REQ-008 ACCEPT on the R2 hashes. WP-4 not entered.

## R-013 — WP-3 R2 post-generation evidence publication (provenance closeout; no ACCEPT claimed)

- R2 generator commit = `456a712b57e006313e82c17e3ac2dc32cc77f0ac` (pushed pre-generation).
- Generator sha256 = `60cc25fcda6fb35850ca216bba6737653d56889da8cb288fed967b0d29ce68b6`.
- bank_id = H4L-R2. Commitment =
  `bfcc24ab070a88c63f54c084bae7de357d2f059c9b79775274b4ca6141b1643d`.
- R1 (`f5dd09ec…` / `4b33e033…`) superseded, REJECTED, and preserved in R-010 +
  `artifacts/v04/holdouts/rejected_R1/` (verified unchanged) + retired secret dir.
- 70,000 episodes (7 sizes × 10k, sorted by episode ID) in operator-secret storage only.
- Reverification (no regeneration, no secret-content inspection):
  `h4l_verify` independent recompute PASS (70000, order+IDs+shards+logical OK);
  HOLD extended suite 21/21 PASS, zero skips; ACT+LEG regression 24/24 PASS;
  repo secret scan PASS (HOLD-08); firewall = COMMITMENT_PUBLISHED; unlocks = 0;
  evaluations = 0 (HOLD-14); reveals = 0 (HOLD-05/06).
- Public evidence published (no seed/bank/instance/outcome bytes):
  `artifacts/v04/holdouts/h4l_commitment.json`,
  `artifacts/v04/holdouts/firewall_state.json`, WP-3 runlog
  `artifacts/v04/logs/run_wp3_*.json` (STEP 101, clean_tree=true), this record.
- Commands: `python scripts/run_phase03.py` exit 0; verifier + HOLD + ACT/LEG reruns
  above, all exit 0. Exact command lines preserved in this entry and the runlog.
- REQ-008 = HUMAN_REVIEW_PENDING (genuine verdict solicited separately, never fabricated).
- WP-3 = INCOMPLETE_PENDING_REQ-008. WP-4 not entered.

## R-014 — WP-3 CLOSEOUT: genuine human ACCEPT on R2 → WP-3 COMPLETE

- Human REQ-008 verdict received (genuine, solicited after the R2 repair report):
  **ACCEPT** on generator `60cc25fc…0d29ce68b6` + commitment `bfcc24ab…41b1643d`,
  recorded in `artifacts/v04/holdouts/h4l_acceptance.review.json` (binds R2 only;
  R1 REJECT stands).
- Exit-criteria reconstruction (re-read from WorkPlan WP-3 + spec §§4,7,8 + WP3 contract):
  H4L_COMMITMENT_PUBLISHED — commitment file published + committed (B2) ✓;
  TRANSFER_GRAMMAR_FROZEN — predicate family (16 hashed), (P,k,C,rho) scope,
  validation/adversarial/OOD tables, clean-room contract, dormant Branch-B all frozen
  + committed ✓; zero H4L evaluations (HOLD-14, stub refuses) ✓; zero reveals
  (unlocks 0) ✓; firewall COMMITMENT_PUBLISHED ✓; generator committed before
  generation (456a712 pre-seal) ✓; independent verify PASS ✓; HOLD 21/21 ✓;
  mutants killed ✓; ACT+LEG 24/24 ✓; runlog STEP 101 clean_tree=true committed ✓;
  R1 preserved as rejected history ✓.
- No synthesis, no WP-4 entry, no repayment/PA/DO claim. MSTL nodes remain UNPROVED.
- Final verdict: WP-3 = COMPLETE
  (H4L_COMMITMENT_PUBLISHED + TRANSFER_GRAMMAR_FROZEN, zero evaluations).

## WP-4 ledger (PHASEs 09-13) — EXECUTION RECORD (initial execution, not a repair)

- Binding: N=4, CURRENT_PHASE=WP-4, PREVIOUS_PHASE=WP-3. No audit findings supplied
  (empty BEGIN/END block); repo evidence proves WP-4 never ran before (no WP-4 commits,
  Path NOT STARTED) so the "previously complete" clause is factually inapplicable.
- Previous-phase verification: WP-3 COMPLETE revalidated (commitment published, zero
  evaluations, genuine ACCEPT; firewall COMMITMENT_PUBLISHED unlocks 0; LIQ0 REVIEWED;
  freeze PASS). Entry-gate result: PASS. Solver stdlib-only (no external binaries).
- Normative sources: WorkPlan.md WP-4; spec #4/#12; search_space/predicate/holdout
  prereg; candidate/counterexample/keep_record schemas; contract planning/WP4_CONTRACT.md.
- Files created: python/solver/{predicates,legality,encode,battery,search,promote}.py;
  python/adversary/engines.py (9 engines); python/independent/config_exec.py
  (share-nothing replay); tests/test_synthesis.py (SYN-00..12, 13 tests);
  scripts/{run_phase04,emit_wp4_runlog,test_wp4_mutants}.py; math/proofs/{MSTL-14-dev,
  MSTL-23-guard, MSTL-24-guard}.md + MSTL-13-dev.md WP-4 addendum (WP-2 lemma preserved).
- Files modified: none frozen (predicate prereg, axis, schemas, proof_status untouched).
- Code/algorithms: splay precompute once/episode (frozen pointer engine) + exact
  integer-pool ledger (T7 +k/sites-nonempty, T5 min(eligible,cap) closed-gated, T6
  min(ACTIVE,need), need=max(y-C*a,0)); staged funnel (13,440 grid screen w/ early
  death, REG-001 first; dev-full on survivors+baselines; 16 shards + sorted reduce);
  matched FLAT(1) baselines (grid points, same pipeline); labels via decision tree;
  cap-3 promotion only with domination certificate; validation 5000 (frozen only);
  9 adversarial engines (propose, exact evaluator disposes); violations demote +
  append-only counterexamples (L0/L1) with independent-replay agreement assert.
- Schemas: candidate 30-field note (prose "29" vs schema 30 — schema governs, recorded
  in contract + promote.py); counterexample required-set conformance tested.
- Tests: SYN-00..12 → 13/13. Benchmarks: screen 125 eps (6147 survive), dev-full 725
  eps (6099 survive; labels RHO_REQUIRED 2199 / RHO_NOT_REQUIRED 3900), validation
  5000 x3 promoted (0 violations), adversarial 9 engines x3 (uniform 50k, structured
  12k, hillclimb 20k x5, anneal 20k x5, genetic 100x200x3, rotneigh 10k, splice 5k,
  motif 4x1000, generalize 8/witness) 0 violations, 0 counterexamples appended
  (lawful: nothing to append; store machinery proven by SYN-08 + M-WP4-07).
- Promoted (PROMOTED_SET_SURVIVES_DEV): P_keep_doubles|3|2|FLAT(2),
  P_keep|3|2|FLAT(2), P_keep_all|3|2|FLAT(2) — all RHO_REQUIRED at minimal C=2,
  calculus LIQ_BRANCH_A_001@C2, identities + outlines frozen in candidates/branchA/.
- Stress/negative: 8/8 WP-4 mutants killed (need+1, paid+1, late-violation skip,
  baseline mismatch, REG bypass, flipped label, ce overwrite, partial reduce);
  false-closure probe (12-passed suite) rejected by exact-13 gate; illegal
  episodes/modes/keys/trees rejected (SYN-02); malformed commitments N/A (untouched).
- Anti-overfitting: H4L/OOD/clean-room never contacted (AST audits SYN-10);
  dev contaminated-labeled; validation ID-disjoint (registries recorded);
  firewall intact; finite survival never called proof (outlines say so).
- Threats/stops/invariants: T10/T11 controls (quarantine + funnel determinism);
  STOP-14 untouched (no regen); resource caps checked per shard/engine (no cap hit).
- Gates: PROMOTED_SET_SURVIVES_DEV (3 + outlines + identities). No universality,
  no C-minimality, no ID mutation, no post-freeze predicates claimed.
- Statuses changed: none (MSTL-13/14/23/24 dev/guard notes only; all UNPROVED).
- Hashes: ranking/artifacts committed; runlog outputs = ranking.json sha.
- Commands/exit codes: `python scripts/run_phase04.py` exit 0;
  `python -m pytest tests/test_synthesis.py -q` 13 passed exit 0;
  `python scripts/test_wp4_mutants.py` 8/8 exit 0;
  `python -m pytest tests/test_activation.py tests/test_legacy_embedding.py -q`
  24 passed exit 0; `python scripts/emit_wp4_runlog.py` exit 0 (next entry).
- Failures/repairs during execution: 4 self-defects found and repaired before closeout
  (dev/val ID collision → resample exclusion; SYN-06 fixture C mismatch; SYN-10 prose
  tokens → code-token audit; schema 29-vs-30 → schema governs; branchA dir collision
  → per-config subdirs; MSTL-13-dev overwrite → restored + addendum; 2 weak mutants
  redesigned live). All green after repair; history preserved here.
- Deviations: none from contract. External blockers: none (no human review needed;
  no theorem verdicts solicited).
- Log inventory: solver STEP 110-117 (predicates/legality/encode/battery/engines/
  config_exec/search/promote module headers + prints); runner STEP 120-130 + RUN;
  mutants STEP 124m; emitter STEP 131.
- Exit matrix: all WP-4 exit conditions PASS (promotion path; rejection paths
  implemented but not taken).
- Compliance: requirements 100%; gaps_found=9 (8 above + branchA collision);
  gaps_repaired=9; remaining_compliance_gaps=0.
- Commit/push: (next entry R-015).
- Final verdict: WP-4 = COMPLETE (PROMOTED_SET_SURVIVES_DEV).

## R-015 — WP-4 push + HEAD verification

- Commit: `069bc59` (WP-4 work: 50 files) + `8e2e7bb` (runlog record).
- Push: `207979a..8e2e7bb` master -> master (origin).
- HEAD: ls-remote `8e2e7bb` == local `8e2e7bb` — agree. Tree clean.
- Verdict: `FOLLOWS WorkPlan.md` (WP-4 COMPLETE; WP-5 entry requires promoted set,
  which exists: 3 identities in candidates/branchA/).

## WP-5 ledger (PHASEs 14-16) — EXECUTION RECORD (initial execution, not a repair)

- Binding: N=5, CURRENT_PHASE=WP-5, PREVIOUS_PHASE=WP-4. No audit findings supplied;
  repo evidence proves WP-5 never ran (no WP-5 commits, Path NOT STARTED), so the
  "previously complete" clause is factually inapplicable.
- Previous-phase verification: WP-4 COMPLETE revalidated (PROMOTED_SET_SURVIVES_DEV,
  3 identities + outlines, firewall COMMITMENT_PUBLISHED unlocks 0, LIQ0 REVIEWED,
  freeze PASS, independent evaluator ready). Entry-gate result: PASS.
- Normative sources: WorkPlan.md WP-5; spec #4/#5/#8; h4l_holdout prereg;
  candidate/counterexample/keep_record schemas; contract planning/WP5_CONTRACT.md.
- Files created: python/cleanroom/{evaluator,batteries}.py; scripts/{run_phase05,
  reveal_h4l,emit_wp5_runlog,test_wp5_mutants}.py; tests/test_fresh_h4l.py
  (FRSH-01..14); math/proofs/{MSTL-22-dev,MSTL-25-dev}.md; artifacts/v04/
  {candidates/commit,h4l_reveal,cleanroom/{impl_freeze,agreement},large_n,ood}/.
- Files modified (robustness, semantics-preserving): python/holdout/h4l_verify.py
  (any verification error fails closed — caught a live zstd-corruption crash);
  iterative tree conversions/legality in cleanroom/evaluator, cleanroom/batteries,
  solver/{encode,legality}, independent/{config_exec,splay._descend} (RecursionError
  at n>=1024; triple agreement @4096 after fix); promote.append_counterexample
  (episode now embeds full T0 + battery + config; bundle recomputed on minimized H).
- Code/algorithms: set freeze + hash (3 members, sorted-key order) → firewall
  CANDIDATE_SET_FROZEN; clean-room bytes committed pre-reveal (B1 14d21e1);
  reveal-once driver (commitment re-verified at reveal, seed+bank published,
  single transition, unlocks 1); fresh eval 70k×3 in order until exhausted;
  full-bank clean-room agreement; large-n 9 sizes x40; OOD 4 sizes x2000 = 8000;
  violations demote + append-only bundles (primary+independent assert).
- Results (finite, never theorems): fresh H4L 3/3 survive (70k each, exhausted);
  large-n 0 violations; clean-room agreement 70k×3 zero mismatches (v1 bytes, then
  re-agreed 70k×3 zero mismatches on v2 bytes after iterative fixes);
  OOD kills ALL THREE (1 violation each, worst shortfall 6, same range-walk episode
  id 2b620ad42f83, minimized L1, triple-confirmed primary/independent/clean-room,
  self-reproducing records ce_0000-2).
- Terminal: PROMOTED_SET_REJECTED at OOD gates (fresh + large-n clean; OOD is
  labeled non-holdout, so Branch-B trigger = False — WP-6-owned routing only).
- Tests: FRSH-01..14 → 14/14; SYN-regression 12 + 1 lawfully deselected (SYN-11 pinned
  pre-reveal state, superseded by FRSH-03/09; WP-4 13/13 closeout stands);
  mutants 16/16 killed; ACT+LEG 24/24.
- Failures/repairs during execution: clean-room aliasing bug (`[[LATENT]]*k`
  shared-list fault → triple disagreement; caught by the agreement gate it was
  built to satisfy, fixed to distinct credits, triple agreement restored);
  recursion trio (above); bundle/instance mismatch (bundle now recomputed on
  minimized H; records embed full T0); FRSH-02 versioned freeze (v1 preserved, v2
  current); verifier exception hardening. All green after repair; history preserved.
- Statuses changed: none (MSTL-22/25 dev notes only; all MSTL UNPROVED).
- Hashes: set_hash 258a900d16858970; commitment bfcc24ab… (re-verified at reveal);
  evaluator v1 4c2dee79… / v2 f2ee1916…; runlog outputs = fresh_results.json sha.
- Commands/exit codes: `python scripts/run_phase05.py` exit 0 (first run revealed +
  crashed lawfully at large-n recursion; `--resume` completed 138-140, exit 0);
  FRSH 14/14; mutants 16/16; ACT+LEG 24/24; emitter exit 0 (next entry).
- Deviations: none. External blockers: none (no human verdicts needed).
- Log inventory: runner STEP 132-140 (+132r resume, RUN); reveal driver STEP 135;
  cleanroom STEP 133-134; mutants STEP 140m; emitter STEP 141.
- Exit matrix: SURVIVES_FINITE_TESTS not reached (OOD rejection); SET_REJECTED
  terminal lawfully taken with per-gate freezes.
- Compliance: requirements 100%; gaps_found=7 (above); gaps_repaired=7;
  remaining_compliance_gaps=0.
- Commit/push: (next entry R-016).
- Final verdict: WP-5 = PROMOTED_SET_REJECTED at OOD gates (fresh + large-n clean;
  finite survival only, no universality claimed).

## R-016 — WP-5 push + HEAD verification

- Commits: `87c8544` (WP-5 work incl. published reveal) + `101cd11` (runlog record).
- Push: `14d21e1..101cd11` master -> master (origin).
- HEAD: ls-remote `101cd11` == local `101cd11` — agree. Tree clean.
- Verdict: `FOLLOWS WorkPlan.md` (WP-5 terminal reached lawfully; firewall
  REVEALED_ONCE unlocks 1; WP-6 proceeds on the rejection/Branch-B routing only).

## WP-5X-K6C2 Specialized Slice (THIS BRANCH ONLY: wp5x-k6c2-specialized)

- Reason: force the entire known WP-5X finite pipeline onto the fixed-resource
  slice k=6,C=2 while letting EVERY frozen WP-4-eligible static (P,rho) config in
  that slice compete (no cap, no top-3, no simplicity pruning, no dynamic P, no
  parameter mutation). Motivation: the pre-liquidity k=6,C=2 wealth point survived
  a large finite bank; the n=192 OOD autopsy of the promoted k=3,C=2,FLAT(2) trio
  (WEALTH/DEMAND exhaustion at LATENT-empty deadline; P_all and rho 2->3 did not
  repair; k 3->6 and C 2->3 did) suggests testing whether k=6,C=2 + existing
  liquidity axis naturally re-emerges as a robust finite region.
- Branch: `wp5x-k6c2-specialized` (work ONLY here; master untouched, no merges).
- SPECIALIZED_START_SHA: `e6bd737e4150fc32ac134e043304b85b4dfa6e15`
  (HEAD == origin/wp5x-k6c2-specialized, status --porcelain empty at start).
- Contract reconstruction: repository bytes authoritative. WP-4 eligible set =
  ranking.json entries with rank[0]==0 AND screen_results.json survived (6099,
  promoted/dominated fields never used as filters). Search grid 16P x 7k x 10C x
  12rho (FLAT(1..6)=(r,r), ROT(1..6)=(r,2r), RMAX 12). Batteries verified from
  bytes: H4L reveal 7x10k=70,000; large-n 9x40=360; OOD 4x2000=8,000.
  Counterexamples: ce_0000/0001/0002 share one n192 OOD episode
  (2b620ad42f83..., n=192, T0=vine-right-192, H=[DELETE129,KEEP134,KEEP130,
  KEEP129]) + constructed REG-001 (n=28 vine, H=[DEL27,DEL28,KEEP28,KEEP27]).
  Clean-room evaluator + contract frozen pre-reveal (impl_freeze v1/v2).
  proof_status.json: MSTL-13 UNPROVED/NO_WITNESS (author arbitrary-n DELETE-
  injection claim preserved as claim only; R<=a, T7<=k per A-rotation, T5
  conserves E, T6 no-discharge-on-DELETE => E_after-E_before<=k*cost_A — NOT
  upgraded, WP-6 owns closure). LIQ0-01..10 REVIEWED.
- K0 population freeze (`scripts/run_wp5x_k6c2.py k0`, reuses
  python/wp5x/population.py semantics): exact k==6,C==2 subset of the 6099
  eligible = 64 configs (5 P x 11 rho minus P_delete_all FLAT(2)/FLAT(3)? No:
  actual 64 = P_all/P_both_doubles/P_keep_all/P_keep_doubles/P_keep x 11 rho
  (FLAT2-6+ROT1-6) + P_delete_all x 9 rho (FLAT3-6+ROT2-6); all RHO_REQUIRED).
  Artifacts: artifacts/v04/wp5x_k6c2/k0_population.json (population_hash
  88a1cdacb151f0211451bacc58b6aa2e8a7aa9f4e28f0d1ff48dc08ec5cbf604) +
  k0_identities.jsonl (30-field identities, schema-checked). Source bindings:
  ranking.json beb2380a..., screen_results.json 1856ee26...,
  promotion.json 879ca35e..., predicate_family 2ab81289...,
  main x0_population 092969c9.... Code hashes (win32 CRLF working-tree bytes,
  self-consistent mid-run guard): encode 3770624f..., cleanroom 1fd283b4...,
  independent 0875707e..., predicates 917ab91b.... Assertions (k==6, C==2,
  pre-existing, WP-4 eligible, exact-subset equality) all PASS; any failure
  STOPs fail-closed.
- Runner: `scripts/run_wp5x_k6c2.py` (k0..k6) imports frozen
  python/wp5x/{population,factored,stages,worker,gates} + solver/cleanroom/
  independent bytes; no semantic duplication. Writes ONLY to
  artifacts/v04/wp5x_k6c2/ (main wp5x/ read-only history). Branch guard asserts
  wp5x-k6c2-specialized before every stage; pushes ONLY origin
  wp5x-k6c2-specialized, never master, never --force.
- K1 known regression (`k1`): episodes = n192 witness + REG-001 + remaining
  distinct preserved ce episodes (dedup; order n192, REG-001, rest). Result:
  killed 1/64 (P_delete_all|6|2|FLAT(3) on n192 id 2b620ad42f83..., need 30 paid
  10 shortfall 20, keeps [122/122, 60/60, 30/10], pool lat_post 228 act_post 0
  spent 192); live 63/64. First-kill certificates with n/T0/H/mode/Aev/Bev/
  sites/a/y/need/paid/margin/pools/attribution in kills_k1.json.
- K2 revealed H4L replay (`k2`, workers=4, resumable per-shard checkpoints,
  label REVEALED_H4L_K6C2_REPLAY, never fresh): 7 shards x 10k = 70,000
  episodes x 63 candidates, factored equivalence + independent confirm.
  Result: killed 0; live 63/63. (First attempt hit the 120s tool timeout on the
  last shard; resumed via checkpoints to completion — no semantic change.)
- K3 clean-room agreement (`k3`): every K2 survivor x full 70k revealed bank,
  per-KEEP (need,paid) primary-vs-cleanroom exact agreement. Result: 63/63
  agree, zero mismatches (agreement_k3.json; 16 chunks x 4, workers=8).
  No EVALUATOR_DISAGREEMENT. Repair during execution: chunk 8->4 for
  resumability under tool timeouts (no semantic change).
- K4 large-n (`k4`, exact unchanged battery, verified 360): killed 0; live 63/63.
- K5 OOD (`k5`, exact unchanged battery, verified 8000, includes n192 killer id
  byte-identical in stream): killed 0; live 63/63. Sharded (2x32) + checkpoints.
- K6 freeze (`k6`): specialized_survivors.json status
  K6C2_SPECIALIZED_SET_SURVIVES_KNOWN_FINITE_GATES, count 63,
  survivor_set_hash 9dcdea2b7926cf94765e1fd818a73f0459c72404b4f4bf5c36b3ec65a27e5748,
  label "FINITE evidence only; FRESH_H5_REQUIRED_BEFORE_WP6". phase_diagram.json
  rows per P x rho (K1/K2/K3/K4/K5/K6, first-kill gate/episode).
- Phase diagram (finite only): 64 existed; 64 entered K1; 63 survived K1; 63
  survived H4L; clean-room agreed completely (63/63, 0 mismatches); 63 survived
  large-n; 63 survived OOD. Surviving P: all 6 families (P_all 11, P_both_doubles
  11, P_keep_all 11, P_keep_doubles 11, P_keep 11, P_delete_all 8). Surviving
  rho: FLAT(2) 5, FLAT(3) 5, FLAT(4..6) 6 each, ROT(1) 5, ROT(2..6) 6 each.
  FLAT rungs: FLAT(1) absent from eligible (all 16 P x FLAT(1) x k6c2 died at
  screen n_evaluated=1 = REG-001-first); every eligible FLAT(2..6) rung survives
  except FLAT(3) loses only P_delete_all. ROT rungs: all eligible ROT rungs
  survive (35/35 incl. ROT(1) 5/5). FLAT(1) reproduces the expected liquidity
  failure (verified live: P_all|6|2|FLAT(1) on REG-001 => violations=1, last
  KEEP need 11 paid 10 margin -1). FLAT(2) survives (all 5 eligible FLAT(2)
  configs incl. P_all). P_all represented 11/11. P_all|6|2|FLAT(2): WP-4 rank
  [0,0,False,2,0,2,6,10,P_all]/RHO_REQUIRED; K1 LIVE (survives n192: need
  30 paid 30 margin 164), K2 LIVE, K3 agree, K4 LIVE, K5 LIVE => K6 SURVIVOR
  (finite). No apparent finite rho threshold within the eligible slice (all
  eligible rungs >= FLAT(2)/ROT(1) survive at ~100% except one P_delete_all
  death). P materially affects survival only via the single P_delete_all death
  (DELETE-gated predicate cannot mobilize on KEEP demand). Multiple semantically
  distinct families alive (KEEP-gated, BOTH-gated, DELETE-gated remnants).
  k=6,C=2 naturally re-emerges as a robust finite region on known gates.
- Autopsies (diagnostic only, no resurrection): (i) sole K1 death
  P_delete_all|6|2|FLAT(3) on n192 => MIXED (savers LIQUIDITY rho->(6,12) and
  PREDICATE P->P_all; DEMAND C->3 does NOT repair; STOCK N/A at k=6; LATENT
  post 228 plentiful, ACTIVE exhausted) => LIQUIDITY/THROUGHPUT +
  PREDICATE/ELIGIBILITY, not wealth exhaustion. (ii) FLAT(1) REG-001 deaths =>
  LIQUIDITY/THROUGHPUT (rho 1->2 repairs at same k,C,P). (iii) k=3 trio n192
  deaths vs k=6 survival on the identical episode => the k 3->6 escalation
  repairs (WEALTH/STOCK axis confirmed finite-relevant), consistent with the
  historical autopsy; C 2->3 also repairs per history (not re-tested here).
- Historical verification: (A) pre-liquidity ~70k survival claim is context;
  current evidence is the 70k REVEALED replay (63/64 live) — labeled revealed,
  not fresh. (B) MST0-13/MSTL-13 DELETE-injection proof remains UNPROVED
  (no upgrade). (C) P_all|6|2|FLAT(1) REG-001 failure REPRODUCED (see above).
  (D) WP-4 dev-clean for P_all k6c2 FLAT(2..6)+ROT neighbors VERIFIED (all 11 in
  ranking, RHO_REQUIRED). (E) n192 OOD k=3 trio autopsy consistent (k 3->6
  repairs, verified on the identical episode id).
- Tests: tests/test_wp5x_k6c2.py (19 tests K6C2-01..19: branch, count/hash,
  k/C admission, exact-subset/no-rank-filter, not-promoted-only, no-cap,
  ID/label/rank preservation, predicate/rho frozen, REG-001 semantic guard,
  H4L revealed+unmutated+not-fresh, K1 coverage, K3 full agreement, battery
  sizes, namespace isolation, no-dynamic-P machinery, no-universality, P_all
  FLAT(2) survival, gate monotonicity) — 19/19 PASS. Regression note (lawful,
  pre-existing, not caused here): SYN-11 pins pre-reveal firewall
  (COMMITMENT_PUBLISHED/unlocks 0) but tree is post-WP-5 REVEALED_ONCE/unlocks 1
  (superseded by FRSH-03/09 per WP-5 ledger); FRSH-02 byte-hash mismatch is a
  win32 CRLF checkout artifact (HEAD LF blob f2ee1916... == v2 freeze; working
  bytes CRLF 1fd283b4...; git status clean) — semantics unaffected (K3
  agreement is runtime need/paid comparison, 63/63 zero mismatches).
  Repair during execution: K6C2-16 test initially matched the word "dynamic" in
  its own prohibition comment — narrowed to machinery identifiers
  (dynamic_*/dynamicP/adaptive_elig/policy_control).
- Theorem boundaries: finite survival only. Permitted: "Candidate X survived all
  specified known finite gates." MSTL-13 UNPROVED. No claim of Dynamic
  Optimality / Pair Access / MSTL-14 / universal k=6/C=2/rho=2/P_all sufficiency.
- H5: NOT created/consumed here. Survivors (63) require FRESH_H5_REQUIRED_
  BEFORE_WP6, to be designed/frozen coherently with any main WP-5X survivors.
- Commits/pushes (this branch only): see R-K6C2 entries below.

## R-K6C2-01 — Specialized slice push + HEAD verification (this branch only)

- Commits: `57be4ba` (runner + tests) + `c1d5e33` (K0-K6 gate artifacts:
  population, kills/live K1/K2/K4/K5, agreement K3, survivors, phase diagram) +
  `25c704c` (resumable checkpoints + this ledger section).
- Push: `e6bd737..25c704c` wp5x-k6c2-specialized -> origin (never master,
  never --force, branch guard asserted before every stage/commit/push).
- HEAD: ls-remote `25c704c3ae7e107196544f9764ea08135cc20841` == local
  `25c704c3ae7e107196544f9764ea08135cc20841` — agree.
- Tree: `git status --porcelain` empty.
- Verdict: `FOLLOWS` the specialized procedure (K6C2_SPECIALIZED_SET_SURVIVES_
  KNOWN_FINITE_GATES, finite only, FRESH_H5_REQUIRED_BEFORE_WP6).

## WP-5X-K6C2 Fresh H5 (THIS BRANCH ONLY: wp5x-k6c2-specialized)

- H5_START_SHA: `cba14f7285bae6a5602a8d1a3dc064775888eab9` (local == remote,
  tree clean at session start; expected `25c704c` is its parent — the delta is
  the Path-only R-K6C2-01 record, verified to touch no K0-K6 semantics).
- K6 entry: count 63, survivor-set hash
  `9dcdea2b7926cf94765e1fd818a73f0459c72404b4f4bf5c36b3ec65a27e5748`
  (re-verified before coding; FAIL-CLOSED on mismatch).
- Rationale: genuinely fresh SAME-DISTRIBUTION replication of H4L
  (`prereg/h5_holdout.yaml`, bank H5-R1), not outcome-targeted. Because the 63
  survivors were already known, no benchmark field was tuned to their strengths
  or weaknesses: sizes/strata/quotas/history/tree/motif/legality/serialization/
  ordering/compression/RNG mechanically inherited from H4L. Only bank identity,
  stream domain (`h5|` vs `h4l|`), and fresh seed differ.
- Inherited H4L bytes (win32 CRLF working-tree SHA-256): spec `4fee1f3e…`,
  generator `e2e98742…`, verifier `f355ebd9…`, firewall `08bd26be…` (recorded in
  `prereg/h5_holdout.yaml`; HEAD LF blobs differ by line endings only).
- H5 prereg hash: `prereg/h5_holdout.yaml` committed in the freeze commit below.
- H5_GENERATOR_FREEZE_SHA: `18d59528297abdde38b3b544592fd4e24a0b053a`
  (`prereg/h5_holdout.yaml`, `python/holdout/h5_{generate,firewall,verify}.py`,
  `scripts/{seal_h5,reveal_h5,run_h5_k6c2}.py`, `tests/test_h5_{holdout,k6c2}.py`,
  `.gitignore` secret quarantine — committed + pushed BEFORE any seed/bank
  existed; no amend/rebase after). Generator reuses frozen H4L semantics
  (`H4L.DRBG/build_tree/gen_history/episode_hash`); candidate-blind by
  construction (AST-audited: imports holdout.h4l_generate + stdlib only).
- Secret-bank generation: one `os.urandom(32)` seed + single 70,000-episode run
  into `$H5_SECRET` (outside repo); no candidate evaluation during generation.
  Shards `h5_n{18,26,34,46,58,74,98}.json.zst` (10k each, sorted IDs, zstd-3).
- Commitment `9f99c860cf5697d115aa45337ae4c5ae4914ff38a83aff24d5dfd675be4a480a`
  = sha256(seed || shards, canonical order; inherited convention), logical
  stream `73596a4d…`, quotas 84 entries, `seed_status` secret. Public record
  `artifacts/v04/h5/h5_commitment.json` (seed/bank never in repo).
- H5_COMMITMENT_PUBLISHED_SHA: `2ef75397930542714b2d669a19bd49d01f6a1444`
  (commitment + firewall state committed + pushed before reveal; K6 re-asserted).
- Freshness audit (pre-reveal): seed distinct from H4L; commitment/shard/logical
  hashes all differ; bank bytes differ on all 7 shards; all secret bytes postdate
  the freeze commit; unlocks 0; zero evaluator contact.
- Overlap audit: 6,661/70,000 H5 episode IDs are byte-identical H4L episodes
  (verified content-equal on all 6,661). Recorded as H5_OVERLAP_REQUIRES_AUDIT
  (`artifacts/v04/h5/h5_overlap_audit.json`): the "expected zero" premise is
  mathematically unattainable — REPEATED_KEEP_DRAIN at n=18 admits ~378
  deterministic contents vs quota 834 (observed 361), same for
  DOUBLE_DELETE_DOUBLE_KEEP / NESTED_INTERVAL; overlap concentrates exactly in
  those three strata. Disposition PROCEED_WITH_UNCHANGED_70K_BANK: no silent
  regen, no seed-shopping (both would be outcome-conditioning and are forbidden),
  no post-hoc exclusion (would break the frozen battery contract). Overlapping
  episodes are provably non-informative here (K2: all 63 survived the full H4L
  bank), so every H5 kill must come from the 63,339 strictly novel episodes;
  freshness reported exactly, never as 70k-fresh.
- Reveal-once: dedicated H5 firewall
  (`EMPTY->GENERATOR_FROZEN->BANK_GENERATED_SECRET->COMMITMENT_PUBLISHED->
  CANDIDATE_SET_BOUND->REVEALED_ONCE`, unlock_max 1; independent of H4L state).
  Bind verified commitment recompute + K6 hash/count; reveal re-verified +
  published `artifacts/v04/h5_reveal/` (seed, 7 shards, manifest, reveal.json).
  Second reveal/regen refused by construction (tested).
- Primary H5 (`scripts/run_h5_k6c2.py eval`, frozen WP-5X-K6C2 semantics via
  `python/wp5x/*`, fail-fast + independent confirm, resumable shards,
  FRESH_H5_K6C2): 63 entered, 0 killed, 63 live over all 70,000 fresh episodes
  (`artifacts/v04/wp5x_k6c2/h5/h5_kills.json` empty, `h5_live.json` 63).
- Clean-room H5 (`agree`, full H5 bank per H5 survivor): 63/63 agree, zero
  mismatches (`h5_agreement.json`); no H5_EVALUATOR_DISAGREEMENT.
- Final: `H5_K6C2_SET_SURVIVES_FRESH_HOLDOUT`, 63/63, survivor-set hash
  `9dcdea2b…` (same 63 members/identities as K6 — zero kills).
  `WP6_ENTRY_SET_FROZEN` emitted with exact identities/hash
  (`artifacts/v04/wp5x_k6c2/h5/wp6_entry_set.json`).
- Finite-only boundary: these statements mean ONLY "these candidates survived
  the specified genuinely fresh H5 finite holdout." MSTL-14 remains UNPROVED
  (`math/proof_status.json` untouched: prove_track UNPROVED, truth UNPROVED);
  H5 is finite falsification and is never evidence for MSTL-14/Pair Access/
  Dynamic Optimality/universal sufficiency.
- Repairs during execution (all pre-reveal unless noted): K3-style chunking 4/
  chunk for H5 agreement resumability; branch guards added to seal/reveal/run
  scripts (mutant h5m_20 caught their absence); blindness-test docstring trap
  fixed by AST-based docstring exclusion (same trap class as K6C2-16);
  h5m_05 made phase-aware (skips pre-freeze); h5m_11 rewritten from
  assert-zero to exact-audit-correspondence after the overlap finding;
  k6c2_17 substring trap fixed (`UNPROVED` contains `PROVED` — now
  lookbehind-matched); h5_08 made phase-aware (log-order assertion post-seal).
- Commits/pushes (this branch only): `18d5952` freeze, `2ef7539` commitment,
  `c56da8d` reveal + overlap audit, plus H5 evaluation/seal commits below.

## WP-6 ledger (PHASEs 17-19) — ENTRY BLOCKED, PHASE NOT BEGUN (N=6 binding)

- Phase binding resolved once at start: N=6 => CURRENT_PHASE=WP-6,
  PREVIOUS_PHASE=WP-5. All WP-6 references below mean exactly WP-6.
- Previous-phase revalidation (fresh, current tree, `scripts/revalidate_wp5.py`
  exit 0): 10/10 checks PASS — H4L-R2 commitment bound, firewall REVEALED_ONCE/1,
  fresh 3x70k exhausted clean, agreement record present, large-n 360 clean x3,
  OOD kills all 3 (1 each), PROMOTED_SET_REJECTED terminal frozen, MSTL-22/25
  UNPROVED, HEAD clean-room blob == v2 freeze. Verdict: WP-5 =
  VERIFIED_COMPLETE **with the rejection terminal** (complete-as-rejected, not
  complete-as-surviving). Path WP-5 entries verified accurate against bytes.
- WP-6 contract compiled BEFORE implementation: `planning/WP6_CONTRACT.md`
  (WP-6-REQ-001..061, immutable; entry/scope/files/semantics/verification/
  tests/statuses/exit). No WP-6 implementation existed before it.
- WP-6 entry-gate audit (`scripts/check_wp6_entry_gate.py`, exit 1, artifact
  `artifacts/v04/wp6_entry_gate.json`): E1 SURVIVES_FINITE_TESTS FAIL (OOD
  survivors 0/3); E2 primary candidate FAIL (none); E3 PA conjunction FAIL (0/7
  MSTL nodes REVIEWED, all UNPROVED/NO_WITNESS); E4 bridge ceiling FAIL (L2
  ABSENT_PAYWALLED => MSTL-19 BLOCKED_BY_SOURCE => DYNAMIC_OPTIMALITY_PROVED
  unreachable per spec #9); E5 anti-substitution PASS (K6/H5 63-survivor finite
  sets recorded and explicitly refused as REQ-001 substitutes — finite survival
  is never a theorem premise). Verdict: WP-6 ENTRY GATE = FAIL.
- Consequence (WorkPlan #3/#19): WP-6 does not begin. No Lean proofs, no review
  packages, no bridge audit, no export/seal attempted — attempting them without
  entry would itself violate the contract, and human ACCEPT/REJECT/BLOCKED
  verdicts plus the L2 source are external blockers that cannot be fabricated
  or worked around. Recorded terminal for this phase: **WP-6 = BLOCKED_ON_ENTRY**
  (blockers: E1 WP-5 rejection stands; E3 zero MSTL proofs reviewed; E4 L2
  paywalled; E5 substitution forbidden). This is not a no-claim terminal from
  the #12 set — no WP-6 terminal was reached because WP-6 never started.
- Red team (false-closure probes, all REJECTED): forged-REVIEWED proof_status
  still fails (0 MSTL review files exist; REQ-041 requires genuine ACCEPT on
  exact bytes); H5/K6 finite-set substitution refused (status strings textually
  distinct from SURVIVES_FINITE_TESTS); OOD rejection undeniable (3/3 kills in
  frozen bytes). Missing-artifact inputs fail closed (FileNotFoundError, exit
  nonzero, never false PASS).
- Regression reruns: FRSH 13/14 (FRSH-02 fails only on win32 CRLF working-tree
  bytes; HEAD blob == v2 freeze verified); HOLD 17/21 — HOLD-03/08 fail on the
  lawfully revealed bank (pre-reveal invariant superseded by WP-5 reveal),
  HOLD-05/14 fail pinning pre-reveal firewall state (superseded by lawful
  REVEALED_ONCE). All four classes are stale-test-vs-lawful-state, documented
  previously, not WP-5 defects; WP-5 artifacts bytes-unchanged.
- Failures/repairs during this audit: one malformed PowerShell-quoted inline
  probe (syntax error, no side effects; rerun with clean quoting) — preserved
  here, no repair needed beyond the rerun.
- Files created: `planning/WP6_CONTRACT.md`, `scripts/revalidate_wp5.py`,
  `scripts/check_wp6_entry_gate.py`, `artifacts/v04/wp6_entry_gate.json`.
- Files modified: none (no WP-6 implementation; Path.md append-only below).
- Statuses changed: none (all MSTL remain UNPROVED/NO_WITNESS; no review
  solicited, none fabricated).
- Log inventory (final line numbers, committed bytes): revalidate_wp5.py
  RV-01 comment 20/log 21, RV-00 27/28, RV-02 35/36, RV-03 47/48, RV-04 57/58,
  RV-05 log 64; check_wp6_entry_gate.py EG-01 17/18, EG-00 23/24, EG-02 36/37,
  EG-03 43/44, EG-04 log 53.
- Exit matrix: WP-6-REQ-001 FAIL (entry) => remaining REQs NOT_APPLICABLE (phase
  not begun; obligations preserved for any future lawful attempt, not waived).
- Compliance audit (WorkPlan WP-6 vs repo vs Path vs tests): contract compiled
  pre-implementation PASS; entry evaluated mechanically PASS (as FAIL verdict);
  no implementation claimed PASS; no placeholders introduced PASS; statuses
  untouched PASS; Path claims evidence-backed PASS. gaps_found=0 (blocking
  conditions are external/structural, not repairable gaps); gaps_repaired=0;
  remaining_compliance_gaps=0.
- Final verdict: **WP-6 = BLOCKED_ON_ENTRY** (previous phase verified,
  entry gate failed lawfully, nothing implemented, nothing claimed).

## WP-6 H5-Successor Route — WorkPlan Amendment + Universal War

A. Start SHA / branch: `1f43527046f1e7eb432f36ceb9a315b956e8a26a` on
   `wp5x-k6c2-specialized` (local == remote, tree clean at session start).
B. Old gate blocked because: E1 SURVIVES_FINITE_TESTS false (WP-5 OOD killed
   the original 3/3), E2 no primary candidate, E3 zero REVIEWED MSTL nodes, E4
   L2 paywalled — under a WorkPlan that recognized only the original route.
C. Old gate was CORRECT under the old WorkPlan; it is preserved untouched
   (`scripts/check_wp6_entry_gate.py`, `artifacts/v04/wp6_entry_gate.json`
   verdict FAIL, original PROMOTED_SET_REJECTED record intact).
D. WorkPlan.md mutation: WP-6 section now carries (i) SPECIALIZED_H5_WP6_ENTRY
   (branch/H5-terminal/entry-status/count/hash, H5-count/hash, clean-room zero,
   K6-H5 bind, identities unchanged, lifecycle sealed, no post-H5 mutation)
   with the explicit successor-transition sentence ("independent legal
   predecessor", not substitution); (ii) review/L2 phase placement (zero
   REVIEWED expected at start, never entry-blocking; L2 gates only MSTL-19);
   (iii) 63-candidate lifecycle (frozen serialized order, per-artifact identity
   binding, one-at-a-time, refutation retires without mutation, first full-route
   closure stops search, resource-limit stays unresolved, no new values/axes);
   (iv) specialized terminals (WP6_H5_ENTRY_PASS … ALL_63_…); (v)
   candidate-bound artifact namespaces; (vi) A+B+C certificate law with
   PROVED_PENDING_HUMAN_REVIEW and no fake review.
E. Entry predicate: SPECIALIZED_H5_WP6_ENTRY as in (D).
F. WorkPlan hash before `796de224595fc3332193e5fb16b9ae0ca922e88581aa0455f373ed47b9d2b005`
   / after `e889e60c244263d9b8f059f398038880aa174a1ef3e649e2dcf97891a5d8df99`
   (single WP-6 section replacement; WP-5 and Appendix untouched).
G. Regenerated WP6 contract hash
   `fdeb4b03f2998c3f9a3dc89f76d624e66b6c933f014f22428727d6828025102f`
   (`planning/WP6_CONTRACT.md`: prior BLOCKED_ON_ENTRY revision superseded by
   amendment, history preserved in git).
H. 63 count/hash: verified identical across wp6_entry_set / h5_survivors /
   specialized_survivors (hash
   `9dcdea2b7926cf94765e1fd818a73f0459c72404b4f4bf5c36b3ec65a27e5748`,
   order byte-identical).
I. Canonical order source: `artifacts/v04/wp5x_k6c2/h5/wp6_entry_set.json`
   serialized array (no reranking; #1 `P_all|6|2|FLAT(2)` identity
   `0909c74accb193302d1a9213601567bebcba414de679e362b10ad3007b4fb7fd`
   asserted from bytes before activation).
J. Specialized entry checker result: `scripts/check_wp6_h5_entry_gate.py` ->
   `artifacts/v04/wp6_h5_entry_gate.json` = WP6_H5_ENTRY_PASS (15/15 conjuncts
   incl. commitment recompute from public reveal + old-gate preservation).
K. Mutants/tests: `tests/test_wp6_h5_entry.py` 22/22 PASS (wrong branch/count/
   hash/identity add/remove/reorder/terminal/agreement/bind/seal/mutation/forge/
   rejection-preservation/routing-review/L2/finite-theorem/master/force/old-
   checker/fake-review). Repair: checker hardened mid-course to recompute the
   H5 commitment itself (mutant w6e_21 caught state-only trust).
L-Z. (Appended as theorem work proceeds; see candidate activation records
   below. Rule COMMIT A pushed before any theorem outcome was inspected.)
O. Candidate #1 theorem work (MSTL-14, `P_all|6|2|FLAT(2)`/0909c74a):
   namespace `artifacts/v04/wp6/0909c74a/` (`activation.json`, `DAG.json`
   reconstructed from theorem files + gate matrix + dev notes: chain
   13/14->15->17->18->19, entry node MSTL-14 with MSTL-13 as sibling).
P. REFUTE track (`scripts/wp6_mstl14_refute.py`, exact frozen calculus, primary
   + independent confirm, greedy minimization): 8,096 episodes over 9 families
   (sanity REG-001/n192 survived; vine drain-diverge; long range-walks L<=64;
   DELETE bursts; nested/alternating; discharge chains; REG/n192 mutations;
   400-step negation hill-climb best margin 0; 6,000 randomized A/B-divergence;
   2,000 extreme-length L<=256) => 0 kills => ATTACKED-NOT-REFUTED
   (`refute/refute_summary.json`; explicitly not a proof).
Q. PROVE track (`MSTL-14_PROVE_notes.json`): conservation framework exact;
   CASE A (LATENT covers B-bandwidth) CLOSED from frozen semantics + event
   counting; Case B reduced exactly to cumulative lemma 6*S_A >= sum(need);
   crux isolated (cross-access splay rotation-accounting potential for A/B
   divergence) and OPEN — node stays UNPROVED, no status touched, finite
   evidence used as premise nowhere.
R. No counterexamples; no candidate transition (#1 ACTIVE, not refuted, not
   resource-limit-unresolved — PROVE open, REFUTE attacked).
S. MSTL-14 REFUTATION (exact legal witness, candidate #1 then cascade):
   post-drain absent battery refutes MSTL-14 as stated. Witness #1: n=64,
   sparse 28-key T0, base [DELETE30,KEEP50,DELETE50,DELETE11] + 11x absent
   KEEP z=10 (need=1 each, trees/pools frozen across battery); first kill at
   overall access 14 (keep #11): need=1, paid=0, margin=-1, act_pre_B=0,
   B_events=0; witness hash
   `24975de3a80eb0c16ffabcd038faf5294e54f6bde7edfb013355fceed7384689`;
   primary == independent == clean-room (triple agreement). Mechanism: absent
   KEEPs demand T6 payment (spec: "repayment quantities use computed (a,y)
   normally") while contributing zero T7/T5 (empty trace) — a long enough
   need>=1 absent battery drains ANY finite ACTIVE pool, so MSTL-14 as stated
   (full legal domain incl. absent) is false for every static candidate, not a
   k=6/C=2/P_all weakness. Cascade (`scripts/wp6_absent_cascade.py`, frozen
   order, same config-independent base/battery, per-candidate minimized L*,
   triple-confirmed each): 63/63 REFUTED (L* 1..25; P_keep_doubles L*=1,
   P_all FLAT(6)/ROT(6) L*=25 — pool-size-ordered, as drainage mechanics
   predicts). Terminal: ALL_63_CANDIDATES_REFUTED
   (`artifacts/v04/wp6/absent_refutation/cascade_summary.json` + 63
   `death_%02d.json` certificates). No candidate mutated; no synthesis; no
   parameter search. proof_status.json: MSTL-14 refute_track NO_WITNESS ->
   WITNESS_FOUND (surgical 1-line diff; truth stays UNPROVED — REFUTED
   requires genuine human validation, solicited herewith, never fabricated).
   Downstream MSTL-15/17/18/19 unreachable on this route (prerequisite failed);
   present-only MSTL-14 proof attempt (t*-restart, Case A closed) stands as
   partial mathematics for a present-key-restricted subdomain (new theorem ID
   required by spec if ever pursued — never silent).
S-T. Statuses unchanged (all MSTL UNPROVED/NO_WITNESS; no review solicited or
   fabricated); L2 boundary untouched (MSTL-19 not reached).
U. COMMIT C: activation + DAG + refute harness/results + PROVE notes + this
   ledger (pushed post-outcome as theorem-work records, not rules).
V. MSTL-14 war continuation (this session, candidate still ACTIVE, node still
   UNPROVED): (i) canonical cumulative lemma frozen with full quantifiers
   (`cumulative_lemma.json`); (ii) direct cumulative refuter
   (`wp6_cumrefute.py`): exhaustive n=2,3,4 + 4k structured + 1500-step R-hill-
   climb = 152,775 tested, best R exactly 0, 0 lemma kills (after repairing my
   own S_A undercount bug that briefly faked 6,424 kills — DELETE injections
   must be counted; stale witness deleted, harness now clears stale outputs);
   (iii) zero-margin instrumentation (208 tight states; sited==Aev at all of
   them; need==y-2a exactly); (iv) R^B<=6*S_A auxiliary: holds everywhere
   tested (24k direct hill-climb best -114; ce_0000 consistent at -187; what
   ce_0000 kills is only R^B<=3*S_A) — viable but unproven route to split the
   lemma as L1(sum<=R^B, PROVEN) + L2(R^B<=6S_A, OPEN); (v) k=3-tightness exact:
   n192 k=3 deficit +2 = shortfall (coefficient 6 = k, load-bearing); (vi)
   S_A=E_A proved (U=0: 87,699/87,699 events + code proof); (vii) tenure lemmas
   proved (root-dislodging computational + A-root-tenure B-constancy +
   tenure=x-DELETEs-only); (viii) absent corner: 5,993 sparse + 4,000 drain-
   absent + 12,000 fitness-hill-climb (best exactly 0), 0 kills — but the
   post-KEEP absent-bound conjecture is FALSE (counterex need=2, both methods
   agree; earlier 99k zero was small-tree sampling artifact); (ix) potential
   screens all killed (linear grid best excess 246; max-variants excess<=10
   but others-rise; sums dead by Theta(n) rotation swings; splay raises raw
   IPL 31% of probings); (x) closest approach: t*-restart argument closes
   everything except the suffix bound 2E>=sum(need), with k entering exactly
   through t* location (thick vs thin pools) — consistent with k=3 death;
   (xi) route kill list frozen (`route_kills.json`, ~20 routes with causes).
   No status changed (all MSTL UNPROVED/NO_WITNESS; no review solicited or
   fabricated). No candidate transition (#1 ACTIVE).

M. COMMIT A: `bdb71f1` (WorkPlan.md amendment + `check_wp6_h5_entry_gate.py` +
   regenerated `planning/WP6_CONTRACT.md` + `tests/test_wp6_h5_entry.py` 22/22 +
   this ledger section), pushed `1f43527..bdb71f1` to origin/wp5x-k6c2-
   specialized, local == remote, tree clean. No theorem outcome inspected
   before this push (gate artifact existed but no PROVE/REFUTE work done).
N. COMMIT B (entry PASS + binding): `artifacts/v04/wp6_h5_entry_gate.json`
   verdict WP6_H5_ENTRY_PASS (15/15 conjuncts). Activated candidate #1 from
   frozen order: key `P_all|6|2|FLAT(2)`, P=P_all, k=6, C=2, rho=FLAT(2)=(2,2),
   identity `0909c74accb193302d1a9213601567bebcba414de679e362b10ad3007b4fb7fd`
   (matches expected; K0-bound, unmutated), WP-4 label RHO_REQUIRED rank
   [0,0,False,2,0,2,6,10,'P_all'], entry-set hash `9dcdea2b…`, K0 population
   hash `88a1cdac…`. Namespace: `artifacts/v04/wp6/0909c74a/` (+ proofs/
   formal subdirs per WorkPlan).

## WP-6 Present-Domain Route — Source Audit (new session, branch unchanged)

A0. Start HEAD `0a02f6f` (== remote, clean); broad MSTL-14 WITNESS_FOUND +
   ALL_63_CANDIDATES_REFUTED preserved untouched (verified at session start).
A1. Source audit (Phase I, 20 questions): L3 arXiv:1907.06310v3 exact bytes
   (732837 B, sha256 f7aa7901…, matches repo SHA256SUMS) establishes:
   instance = (X, T containing requested keys); search requires xi in Ti-1;
   digraph arcs only for x in T; subsequence = occurrence time-subset (dup
   safe); same T for X/Y; fixed key set through rotations; DO iff AM
   (Thms 3.2/3.5); insert/delete only as separate mutating request types;
   PA DELETE = occurrence deletion (never node removal); NO source condition
   reintroduces absent searches. L2 paywalled (not inspected byte-wise; L3
   supersedes framework), L1 paywalled (L3 cites ST85 explicitly).
   Verdict: PRESENT_DOMAIN_BRIDGE_PASS, scoped as domain audit only —
   MSTL-19 stays BLOCKED_BY_SOURCE.
A2. Pair-Access mapping formalized (occurrence mask, NOT value-set;
   A_i=Splay(X[1..i]), B_i=Splay(retained Y-prefix); FIXED_KEY closure proved:
   rotations preserve keysets, keys(A_i)=keys(B_i)=K, every x_i present —
   `tests/test_present_domain.py` 3/3 green).
A3. COMMIT 1 (audit only) pushed before any WorkPlan/theorem mutation.

## WP-6 Present-Domain Route — Amendment + MSTL-14P Seeding

B1. WorkPlan present-route amendment committed (16-point successor law above:
   history preserved, new IDs, frozen order/bytes, no H6, review external,
   MSTL-19 unchanged).
B2. New theorems: math/theorems/MSTL-{14P,15P,17P,18P}.md (PresentLegal-
   PairInstance domain; chain 14P->15P->17P->18P->19; consumers REVIEWED-gated).
B3. proof_status.json: +4 rows (UNPROVED/NO_WITNESS/UNPROVED); broad MSTL-14
   row byte-identical (WITNESS_FOUND/UNPROVED).
B4. DAG: artifacts/v04/wp6_present/present_route_DAG.json (broad feeders
   08U/09/11/13/22 kept; 19 unchanged bridge node).
B5. COMMIT 2 (rules+IDs, pre-outcome) pushed before present theorem search.
B6. COMMIT 3 (entry/binding): candidate #1 `P_all|6|2|FLAT(2)` identity
   `0909c74a…` bound in `artifacts/v04/wp6_present/0909c74a/activation.json`
   (frozen order, pre-outcome; refuted-broad status explicitly noted, not
   erased).
C1. PR-03 REPAIR (defective periodic stage replaced, intent preserved):
   defects confirmed — quadratic full-prefix replay per repetition (plus
   double replay inside ledger_state), unsatisfiable recurrence key
   (act IN key, `act < stored` impossible), pass-only drift body, pre[-1]
   access-record used as geometry (contains no tree state). Repair:
   `scripts/wp6_periodic.py` maintains exact live (A,B,lat,act) incrementally
   mirroring encode.py bodies; cross-check gate 200/200 exact vs frozen
   executors (records/keeps/violations/final pools); canonical recurrence
   state = (nested(A), nested(B), lat, act) — SPENT/injected/cursor are
   write-only diagnostics, pools fungible (no per-credit identity), so this
   tuple is sufficient; drift = same geometry + component-wise ≤ + strictly
   worse (dominance preserved forward by monotone mobilization/payment);
   exploitation == continuation to kill/stall/cap; per-candidate + per-25
   instrumentation. Old PR-03 block superseded in git history, never executed
   post-repair; `wp6_present_refute.py` delegates PR-03R to the module.
C2. PR-03R RESULTS: exact bounded-word search (all shapes n=2,3,4 × words
   len≤3 = 9,634 combos) 0 kills; full stream 300 candidates × ≤1500 reps
   (~24s total; 217 CAP / 83 STALLED / 0 KILL / 0 drifts — geometry essentially
   never repeats); deep stream 120 candidates × ≤15000 reps (|H|≤60005,
   n≤512, ~354s) 0 kills. Finding: periodic words drift through fresh
   geometries rather than cycling; no present-key periodic drain exists in
   this budget.
C3. FULL REWIRED BATTERY (`wp6_present_refute.py` PR-01/02/03R/04/05):
   tested=152,777 episode-evaluations + 300-stream + 9,634 exact words,
   0 kills => ATTACKED-NOT-REFUTED (present-only). Absent accesses rejected
   by construction (check_present).
C4. LOCAL LEMMAS D1/D2 PROVED (mechanics + property tests
   `tests/test_present_mechanics.py` 3/3): D1 need>0 ==> Bev nonempty
   (Aev=Bev=0 ==> need=0 for present); D2 ceil((y-1)/2) <= e_B <= y-1 hence
   2*e_B >= need (raw FLAT(2) bandwidth; eligible bandwidth still open —
   support/provenance is the remaining service gap).
C5. PRIOR-SESSION LEFTOVERS BANKED (verified this session, not authored here):
C6. TEST MAINTENANCE (no science change): `test_w6e_18` asserted broad
   MSTL-14 refute_track==NO_WITNESS, stale since the lawful WITNESS_FOUND
   recording; updated to assert the recorded state
   (truth/prove_track UNPROVED + refute_track WITNESS_FOUND). Suites now:
   present_domain 3/3, present_mechanics 3/3, wp6_h5_entry 20/20, h5_holdout
   9/9, wp5x_k6c2 19/19 (56/56); FRSH 13/14 with the known pre-existing
   CRLF artifact only.
C7. MSTL-14P WAR (this session): cumulative stock attacked as pure splay
   coupling (D<=6*S_A, S_A=E_A); R pinned at exactly 0 over ~200k hostile +
   exhaustive n<=4 + hill-climbs (best trivial-only); k=3-tightness exact
   (+2=shortfall); coefficient verdict: 6=k creation, 2=rho cap, 2=splay
   binary — three provably distinct sources, 6=2x3 KILLED (live n28 demo:
   rho1 paid=10 KILLED vs rho2 paid=11 SURVIVES, same 7 B-events); eligible
   service still open (raw D2 proved, support/provenance not). Artifacts:
   `MSTL14P_PROVE_notes.json`, `coefficient_sources.json`. No status change
   (MSTL-14P UNPROVED/NO_WITNESS); no candidate transition (#1 ACTIVE on
   present route).
C8. TENURE-NEED THEOREM PROVED (`lemma_tenure_need.json`): a=1 KEEPs (the
   only accesses with zero own A-events) have fully characterized demand —
   0 if tenure started with KEEP, else frozen max(D-1,0) with zero marginal
   S_A cost in-tenure (tenure = x-DELETEs only, B frozen). a>=2 KEEPs fund
   >=6 own injection each. Irreducibility assessment: every split (Case A/B,
   t* trichotomy, tenure/a-value, present/absent, L1/L2) bottoms out at
   "global pools must cover local net demand" = the cumulative lemma
   itself; it is irreducible by local/global-counting/potential/charging
   means tried (~30 routes). Remaining route classes: L2 pure-splay
   prepayment coupling, machine-synthesized nonlinear potentials,
   abstract interpretation (multi-session scale).   `tstar_conditional.md` (t*-restart conditional theorem with explicit open
   gap: t*-inside-B-phase under thin pools; k-entry via t* location) and
   `lean/WP6/MSTL14PArith.lean` (arithmetic backbone: need bound, 1-2
   event counting, greedy cap-2 exactness, service composition — direct
   `lean` LASTEXITCODE=0, zero output, no sorry/admit/axiom). `.lake/`
   residue from a failed `lake build` removed (frozen WP-0 lakefile is
   incompatible with installed Lake 5 — pre-existing; direct-`lean` remains
   the repo precedent per WP-1/WP-2 entries).
C9. RUN-NEED LOCALIZATION PROVED (`lemma_run_localization.json` + hostile
   audit 2000 histories): maximal same-key runs partition history; S_A occurs
   ONLY at run starts (first access splays; rest are root no-ops); positive
   needs occur ONLY at first-KEEPs (after first KEEP x is at both roots, so
   later same-key KEEPs have a=y=1, need=0 — 0 violations among 1292 positive
   first-KEEPs); every non-initial run funds >=1 sited event (+6 S_A);
   tenure == run (identical boundaries). Funding still global (run-local
   divergence B-deep/A-shallow at run start needs pre-run L2 coupling);
   recorded as the sharpest structural frame, not as closure.
C10. QUOTIENT WAR (stages 1-8 executed; MSTL-14P stays UNPROVED/NO_WITNESS,
   no candidate transition). Run compression verified on 500 hostile
   histories (S_A only at run starts; needs only at first-KEEPs;
   `scripts/wp6_quotient.py`, `quotient/quotient_lifecycle.json`:
   births=4960 changes=8090 deaths=1621, defect count 0..31). Defect records
   change O(1) per StepEv (Lemma A worst 2/3) but VALUES jump O(n): all
   pure-state masses killed - M1/M2/M5 creation 57/68/60, B-inc 57/24/60,
   KEEP gap 57/29/62; M3 max-div creation HOLDS (+4<=6, tight: 1252/5274
   StepEv hits at +4) but B-conservation FAILS (+2 push-down leak) and
   KEEP-consume FAILS (gap 23, bystander-max); size-capped CAP=2 creation
   HOLDS (4<=6) but B-leak +4 / KEEP gap 30; depth-capped creation FAILS
   (20>6, whole-subtree depth shifts). Impossibility-triangle recorded
   (`mass_autopsy.json`): stable (max) vs accounting (sum) vs localized
   (at-x) are pairwise incompatible for pure state functions. Per-run
   6-budget is FALSE (58:1 arbitrage, DELETE-started 15:1;
   `run_arbitrage.json`): funding MUST cross run boundaries. Greedy global
   6-per-A-event discharge: 0 shortfall over 600 hostile histories, global
   need/income 0.039 (`discharge_greedy.json`) - plausibility evidence, not
   proof. Raw stock adversarial sweep: 1000 histories (freeze-then-cash,
   shuffled-insertion BSTs, big hostile), 0 kills, worst gap -23, worst
   ratio 0.28 (`stock_sweep.json`). Composition reduces to ONE open lemma:
   B-source (B-created divergence prepaid by global pool). Lean AR-06..AR-09
   added (div_rise_A/B, capped_gain, poolAux+pool_step) as SKELETON -
   kernel check PENDING (no Lean toolchain in this env; release download
   timed out); header states this explicitly, nothing cited as Layer B.
   Route ledger: `killed_routes_3_quotient_war_2026-09-29` + alive-open-2
   (M3-creation micro-lemma / raw stock / B-source).    Scripts:
   `wp6_mass_screen.py`, `wp6_mass_capped.py`, `wp6_mass_capped_size.py`,
   `wp6_discharge.py`, `wp6_run_attack.py`, `wp6_stock_sweep.py`.
C11. VAULT DESCENT + EVENT-FLOW LANE (MSTL-14P stays UNPROVED/NO_WITNESS).
Per-key involvement FALSE (gap 48: riding builds B-depth w/o A-contact);
subtree-token presence FALSE (gap 60: spend/frozen mismatch); zig/doubles
split FALSE (1.22); cash/setup pairing FALSE (+13, noncash excess 709 >>
cash 286); D<=E_B FALSE (1.94); R<=1.5*Q reset-depth link FALSE (1.58 on
n128-L19 R218/Q138: budget 2x too tight; all-doubles makes E_B/S_A==R/Q).
M1 PROVED (ancestor-only pushes, rigid riders, depth-sum conserved per
rotation); #cash<=S_A via setup injection; KEEP-only => E_B=E_A exactly.
E_B<=3*S_A ALIVE prefix-closed (best 1.57/3 over ~15k histories + 8k
gap-hunt + 9.3k ratio-hunt + ce_0000 -92); stock best 0.47, 0 kills.
Ratio-hunt J1=1.57/J2=1.58/J3=0.47 (J2 kills R-link, J3 holds stock).
Event-flow E1+E2+E4 capacity-3: full 86/120, prefix 371/486; min-cut
0-gap + 210-saturated => eligibility CORRECT, capacity SHORT (fanout):
duality-blocked (tighten=>gap, loosen=>share); epochs/laminar dead
(700x local shortfall vs 1.57x global: funding irreducibly global).
Scalar Psi dead via REVELATION (1243-gap: A-shallowing exposes
pre-existing B-depth). Push-backing impossible (sharing O(n) or
cap/free-depth dilemma). Coverage Vm+F>=Vp prefix-closed (min 0.00,
excess/C<=0.36); funding 20x aggregate (anti 5x + DELETEs 15x; 7:1
count); dissection vine-cash replay 1:1 steps funded 3x
(eA=0/eB=64/slack=192 = historical setup-DELETE capacity); freshness
exact (fresh=>0 work, A==B=>same splay, 0 viol; stale ratio 0.60).
SOLE SURVIVOR: global-count prefix-induction on E_B<=3*S_A (slack 0.33,
reason unknown). Lean AR-10..AR-13 (steps/depth + genesis-zero +
stock_composition conditional; kernel PENDING). Scripts: `wp6_involve.py`,
`wp6_subtree.py`, `wp6_rotbudget.py`, `wp6_eb_hillclimb{,2}.py`,
`wp6_prefix_eb.py`, `wp6_slack.py`, `wp6_doubles.py`, `wp6_resetdepth.py`,
`wp6_purepump.py`, `wp6_pairing.py`, `wp6_need_eb.py`, `wp6_funding.py`,
`wp6_dissect.py`, `wp6_freshness.py`, `wp6_ratio_hunt.py`,
   `wp6_psi_anatomy.py`, `wp6_eventflow{,_cut}.py`, `wp6_coverage.py`.
C12. TRACE-REWRITE CORRIDOR LANE (MSTL-14P stays UNPROVED/NO_WITNESS).
Raw rotation-distance normalization DEAD (LAW-A holds gap 0 via triangle;
LAW-K FALSE +3: dist 5->5 flat while e_B=3/e_A=0; dist-drop median -2 vs
excess O(n); telescope holds only on small trees). Reason: splay preserves
rest-arrangement via M1-rigidity, so shape-distance is splay-invariant-ish
and orthogonal to depth-work E_B; word/shape normalizations are the wrong
category (depth-work needs depth-tracking, which hits L1/swings/counts).
Extended flow E1+E2+E3+E4+E7 saturates 120/120 + 486/486 BUT ablation shows
E3 alone closes (E1+E3 80/0 at dens 8.5; E2 +7/E4 +9/E7 +2 marginal), and by
min-cut flow==counts: diagnostic only (hub-abundance + deep-overcover
tiers), not proof. Top/bottom split restates (tops 1:1-free via E1, bottoms
share via pumps). Matching closed generally (fanout leaves unavoidable
residual under any eligibility). Scripts: `wp6_distnorm.py`,
`wp6_eventflow2.py`, `wp6_eventflow_abl.py`. Queued: N-AUG exchange with
trace-justified new edges, N-FIRST first-violation normal form.
C13. SINGLE-OMISSION DAMAGE LANE (MSTL-14P stays UNPROVED/NO_WITNESS).
SOD-3 FALSE (damage +9, c*=12 on d=1 n16-shuffled alternating suffix;
285/400 pairs never resynchronize so damage grows linearly in |W|;
per-deletion telescope step +11 vs budget +2). BUT batch G_DEL<=0 HOLDS
(400 histories, J_DEL best 1.5/3): E_B<=A_K+3*A_D (stronger than E_B-link)
via cross-deletion cancellation. Mechanism = tail-mass: median fut/d 0.33,
tail-d-fraction 0.83%, bad tail is shallow-leverage (d=1-5, fut 3-12);
typical removals SAVE (cost-convergence: splay balances both executions'
accessed keys shallow) while rare hub-pivotal omissions cost (M1-locality:
access affects O(depth), rest rigid). Also strict-D2 (need<=2*e_B-1) and
J3-cap 0.62 (D2-cap 0.75 x EB O(n)-cash 0.83 via balanced-build dilution).
Scripts: `wp6_sod3.py`, `wp6_sod_hill.py`, `wp6_sod_tail.py`. Queued:
formalize tail-mass cancellation (M1-Lipschitz + cost-convergence) as the
batch proof; N-AUG/N-FIRST remain open.
C14. TSRC/HAZARD/SCALING LANE (MSTL-14P stays UNPROVED/NO_WITNESS).
SEC0 verified: batch E_B<=A_K+3*A_D is FALSE (+1 exact witness
EB55/AK51/AD1/uns0 on n16 one-DELETE history; damage==G_DEL semantics
confirmed, tuple-splay==legacy 0/500); earlier G_DEL hunt missed
one-DELETE shapes; E_B-link alive (0.35). TSRC raw-Delta DEAD on reachable
pairs at n4-7 (GAP +5/+11/+15/+18 growing; lambda infeasible at every n:
A-blind B-moves lengthen min-repair-paths). Vector alpha/beta LP infeasible
n5/6/7. Full pair-Phi bounds-blocked (teleport/Farkas, no replayable
witness); pure differences feasible (=counts restated). Hazard H laws hold
EXACTLY n<=7 (LAW-D/LAW-K worst 0) but die at scale (+1/+4/+5/+21 at
n16/32/64/128 via multi-divergence bystander push-up; small-n was
single-divergence artifact). Positive: n<=7 orbit-BF VERIFIES E_B<=3*S_A
exhaustively (all starts, full orbits); E_B/S_A scale-invariant ~1.0-1.7 at
n8..512 (adversary gains nothing with n; ~2x margin every scale). Scripts:
`wp6_gdel_one.py`, `wp6_splaymetric{,2}.py`, `wp6_pairlp{,2}.py`,
`wp6_orbitbf.py`, `wp6_scaling.py`, `wp6_hazard{,_scale}.py`.

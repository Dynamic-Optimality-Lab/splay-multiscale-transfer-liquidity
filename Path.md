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

## WP-0 ledger (PHASE 00) — PLACEHOLDER, NOT STARTED
Prescription/entry/files/code/results/proofs/status/deviations/bugs/anti-overfitting/gates/coverage/SHA/push/remote/verdict: PENDING. Entry requires closure PASS (satisfied); execution not started.

## WP-1 ledger (PHASEs 01–04) — PLACEHOLDER, NOT STARTED
PENDING. Entry requires FOUNDATION_FROZEN.

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

# IMPLEMENTATION SPEC SPLAY-AM-MST-LIQ-v0.4.1 (operative, consolidated)

**Experiment:** `SPLAY-AM-MST-LIQ-v0.4` + contract-closure `v0.4.1`. Historical v0.4: `historical/IMPLEMENTATION_SPEC_SPLAY-AM-MST-LIQ-v0.4.txt` (SHA-256 `0E2C166E…055B`). On any conflict, this document + `amendments/SPLAY-AM-MST-LIQ-v0.4.1-CONTRACT-CLOSURE.md` govern. Target: liquidity-aware multiscale synchronous transfer `(P,k,C,rho)` toward Pair Access and Dynamic Optimality. Normative stack: this spec + amendment + `prereg/*` + `math/theorems/*` + `schemas/*` + `planning/* matrices`.

## 1. Parent contract (CC-001/002/003/048)
- Architecture parent `splay-multiscale-transfer`: navigation `895889169772087e391e84c33228648c84684e1e`, closure `9859e654b76ba92c1d0e0809f62a7ffe1cac3b98`, seal `3062c0180157399cc0e877c0d238edc7f3aff7c0`; artifact content SHAs in `prereg/parent_contract.yaml`, re-verified at WP-0.
- Obstruction parent (trailing-hyphen name verified): evidence commit `19ef254dfc48c7b909c646f959e2d7364865b777`, mathematical status CONFIRMED (n=28 + triple replay), formal PENDING, human G5 PENDING, lifecycle seal OPEN. Never call it sealed.
- Precedence: architecture owns definitions; later parent supplies proof/refutation evidence only under byte-identical statements + transport theorem, else new MSTL bytes; no status copied (all LIQ statuses start UNPROVED).
- Bootstrap: import exact pinned tree; preserve history under `v03/history`; byte-equality manifest; classify every file per `planning/PARENT_TREE_DISPOSITION.yaml` (unclassified = closure failure); new results only under `v0.4.1` namespaces.

## 2. Legal domain (CC-004/005/006)
- `LegalPairInstance(T0,H,n)`: T0 valid BST; `keys(T0) ⊆ [n]`; modes KEEP/DELETE; access keys in `[n]` (presence NOT required); A,B start equal T0; exact replay semantics. Exact-equality `keys(T0)==[n]` only as labeled proof-restricted subdomain (new theorem ID, never silent).
- Class A (tree/history) theorems require `LegalPairInstance`. Class B (pure ledger algebra: discharge conservation, preservation, SPENT monotonicity, ledger parts of MSTL-15) stays total over arbitrary ledgers — no tree hypotheses.
- Absent-key semantics (exact, from obstruction `splay.py`): cost `depth_to_leaf+1`; StepEv trace empty; tree unchanged; zero T7/T5 opportunities; repayment quantities use computed `(a,y)` normally.
- Multiplicity: present-key `sum mu(ev)=depth_T(x)`; absent-key trace-empty statement. `mu`: ROOT/no-event 0, ZIG 1, LL/RR/LR/RL 2. Normalization: oriented ZIG-L/R preserved in trace, both map to ZIG class.

## 3. T5_rho + replay (CC-007/008/009/056/057)
- `T5_{P,1}(L,m,ev)`: inherited single activation gated by frozen predicate P (mode + normalized event class only). `P_all` fires always; `P_keep` on KEEP; case-restricted per allowlist (`prereg/predicate_family_v0.4.1.yaml`, closed, canonical enumeration frozen at WP-0).
- `T5_{P,rho}(L,m,ev)` = bounded deterministic iteration of `T5_{P,1}`, `rho(ev)` times; first-eligible ledger order; partial activation (all available, create nothing).
- Eligibility: LATENT + support-allowed + predicate-fires. Counts use `eligibleLatentCount`: `ACTIVE' = ACTIVE + min(q_elig, b)`, `LATENT' = LATENT - min(q_elig, b)`.
- Replay equations (verbatim): A-side per StepEv `T7 → T5_{P,rho}`; B-side per StepEv `T5_{P,rho}`; KEEP discharge unchanged T6 after complete B trace; DELETE no B replay/discharge. Ordering hash-bound in candidate identity. T7/T6/`required_C`/energy/support/provenance/splay/`depth+1`/Pair-Access unchanged.
- `rho(ROOT) = rho(no-event) = 0` (total function). Mathematical class `rho = (rho_ZIG, rho_DOUBLE)`, each `0..8`, symmetric doubles; `FLAT(r)=(r,r)`, `ROT(r)=(r,2r)`. Discovery ladder frozen: FLAT/ROT `r=1..6` (12); `r=7+` via versioned ladder extension, never a new axis.

## 4. Search space + attribution (CC-010/011/012/013/036/037/038)
- Scope B: non-liquidity mechanics fixed at inherited Branch-A architecture; synthesis searches enumerated `(P,k,C,rho)` only. `k ∈ 0..6`; `C ∈ {2,3,4,6,8,12,16,24,32,64}`; P from closed family. Objective: legality → conservation → immutable LIQ-REG-001 satisfied → dev-zero → validation-zero → smaller C → simpler rho → smaller base → smaller k → simpler P. No template-count terms. One legal `paid<need` kills instance at that C.
- Matched `rho=FLAT(1)` baseline over same space/pipeline/corpora. Labels: `RHO_REQUIRED / RHO_NOT_REQUIRED / C_ONLY_REPAIR / K_OR_P_REPAIR / MIXED_AXIS_REPAIR / NO_SURVIVOR`. Liquidity confirmed only under `RHO_REQUIRED`.
- Candidate identity (29 hash-bound fields per `schemas/candidate.schema.json`); `calculus_id = f(rule_family_id, C)`; C change mints new ID. Promotion wording: "candidate satisfies immutable LIQ-REG-001", never "repairs witness".
- Promotion: evaluate every eligible survivor (≤3 soft cap only with domination proof); terminal `PROMOTED_CANDIDATE_SET_REJECTED` unless full space eliminated (then `LIQUIDITY_CALCULUS_REJECTED`); next-candidate-until-exhausted ordering.

## 5. Theorems (CC-014/015/016/017/018/055/060/061/039)
- Exact bytes: `math/theorems/` — LIQ0-01..10 + MSTL-08U/09/10/11/12/13/14/15/16/17/18/19/22/23/24/25/26 (27 files: quantifiers/domain/negation/consumer). Full 26-node gate matrix `prereg/theorem_gate_matrix.yaml` (canonical; transport name superseded).
- PA prerequisites (conjunction, machine-checked): MSTL-08U/09/11/13/14/15/22 REVIEWED + LIQ0-01/02/04/05/06/09/10 at required statuses. MSTL-09 explicitly owned (WP-2 dev, WP-6 proof, in GATE-13). MSTL-12 = signed lower bound. MST0-20/21 OUT_OF_SCOPE (DOC-disproof outside LIQ).
- Provenance: transport later proof only under identical bytes + rho-invariance lemma; else reprove/new bytes; ACCEPT valid only for reviewed bytes.
- Multiplicity failure kills ROT profiles only (FLAT continues). S5/S6 = tested members unless family theorem closes; S10 = tested rung; S19 permits no-justified-resource answer.
- Additive term: `A(n)=0` only live target; nonzero BLOCKED until bridge-derived class frozen.

## 6. Lifecycle + review (CC-027/028/050/065)
- Truth: UNPROVED / PROVED_PENDING_REVIEW / REVIEWED / REFUTED / BLOCKED / NOT_REACHED / NOT_APPLICABLE. Prove track: UNPROVED→PROVE_RUNNING→PROVED_PENDING_REVIEW→REVIEWED. Refute track: NO_WITNESS→WITNESS_FOUND→MATHEMATICAL_COUNTEREXAMPLE_CONFIRMED→FORMAL_REFUTATION_PENDING→HUMAN_VALIDATION_PENDING→REFUTED.
- REJECT (package rejected, truth stays UNPROVED) != REFUTED (exact negation witness + candidate hash + primary + independent + formal-or-exempt replay + human validation). Formal mandatory where applicable (2 routes always mandatory); else MATH_CONFIRMED without promotion. Byte change invalidates review. Ledger `math/proof_status.json` per `schemas/theorem_status.schema.json`.
- Counterexample certificates: operation-deletion / parameter-family / exhaustive-global minimality; never claim stronger than certified.

## 7. Branch B (CC-019/020/021)
- Activates iff Branch-A promoted set rejected at development or fresh. Dormant Branch-B identities/grammar frozen pre-reveal; post-reveal only frozen set runs on H4L; else successor + new bank. Late theorem failure opens no synthesis.
- Signed `T5_{P,rho}`: activation preserves sign-mass; `E_signed = sum(m)` + proved lower bound MSTL-12; unsigned theorems never transfer silently.

## 8. H4L firewall (CC-022/023/024/025/031/034/035) + validation/budgets (CC-029/030)
- Exact parameters (`prereg/h4l_holdout.yaml`): sizes `[18,26,34,46,58,74,98]` ×10k =70k; quotas 833+remainder schedule; history law uniform 2..8; tree law random-BST + balanced/spine mixture; SHA-256 counter DRBG; 256-bit operator-secret seed never committed pre-reveal; dedup reject-resample; weaker-domain legality filter; canonical JSON + sorted IDs; `.json.zst` deterministic shards + per-shard/logical-stream SHA; commitment `sha256(seed||bank)` + metadata public pre-reveal.
- Secrecy: seed+bank outside public/discovery repo until reveal; no git/LFS/embedded-key fakery; else H4L BLOCKED. Automaton EMPTY→GENERATOR_FROZEN→BANK_GENERATED_SECRET→COMMITMENT_PUBLISHED→CANDIDATE_SET_FROZEN→REVEALED_ONCE→CONSUMED; unlock ≤1; fail-closed STOPs.
- WP-0 freezes generator contract; WP-3 implements + certifies hash-equivalence, then generates. Clean-room spec + authoring boundary + I/O schema + implementation bytes frozen pre-reveal. Legacy: H1 HISTORICAL_UNUSED EMPTY; H2R HISTORICAL_UNUSED COMMITTED/0; H3T HISTORICAL UNLOCKED_ONCE; n8 CONTAMINATED_CANARY.
- Validation: seeded structural generators (disjoint stream), sizes `[7,8,10,12,16]`, 5k episodes, ID-disjoint masks, frozen-candidates-only contact. Adversarial: 9 engines with frozen seeds/budgets/restarts/shards/caps/sorted-reduction (table at WP-0). OOD family (random-walk + spine-heavy, disjoint stream, `[24,48,96,192]`) labeled OOD, not fresh-holdout.

## 9. Bridge + DOC scope (CC-040/066)
- WP-0 pins Levy–Tarjan source/version/bytes/hash/statement/direction/conventions/assumptions/mapping/checklist/manifest (`prereg/bridge_manifest.yaml` at execution; obstruction record: L3 present, L2 absent). While L2 absent: MSTL-19 = BLOCKED_BY_SOURCE, `DYNAMIC_OPTIMALITY_PROVED` unreachable. No folklore bridges.
- DOC-disproof outside MST-LIQ. Transfer-route failure is never a DOC claim. MST0-20/21 OUT_OF_SCOPE.

## 10. Environment + exactness + logging + artifacts + seal + reproduction (CC-041..047)
- Env lock (`prereg/environment_lock.yaml`): Python 3.13.7 + dep hashes (WP-0), Lean `leanprover/lean4:v4.21.0`, lake config/manifest, solver builds, single-thread-deterministic (+ deterministic sharding), SHA-256-DRBG, deterministic zstd, env vars recorded; runs record env hash.
- Exactness: no float-determined signs; exact integer/rational decisions; sorted reductions; canonical tie-break/sharding; logical-stream hashes; exact cert replay; heuristics propose, evaluators dispose; exhaustion never impossibility.
- Logging (35 fields, parent superset): experiment/phase/WP/branch/UTC/commit/clean-tree/source-manifest/arch+obstruction+ancestor IDs/spec+amendment+prereg+gate-matrix+literature+env SHAs/candidate+family IDs/P/k/C/rho+profile+legal-domain SHAs/firewall/command/IO/stdout/stderr hashes/wall/peak/exit/status.
- Authoritative runs: committed code + `git status --porcelain` empty; else content manifest + diagnostic-only (no theorem/fresh claims). Generator committed before H4L generation.
- Artifacts: `.json.zst` deterministic + shard naming/order + per-shard SHA + manifest + logical-stream SHA + canonical serialization. Seal: manifest scope/exclusions/ordering, no-self-hash, deterministic archive + SHA, FINAL_RESULT from artifacts, rebuild-identical, stale detection, failure preservation, clean-checkout repro. Reproduction: reached-phase matrix (existing + NOT_REACHED/NOT_APPLICABLE + no illegal downstream artifacts).

## 11. Governance (CC-049/051/052/053/054/064)
- `WorkPlan.md` (compilation of this closed spec) + `Path.md` (append-only live ledger, contemporaneous updates, failed history preserved) are normative requirements.
- Canonical `prereg/theorem_gate_matrix.yaml`. Export `schemas/mst_liq_export.schema.json` + verifier binding all listed fields; import only after verifier passes.
- Successors: clone latest sealed architecture retaining axes; add one justified axis; prove backward embedding; preserve failures. Resource-limit claims need exact record fields + budgets.

## 12. Gates + phases + terminals
- PHASE 00→WP-0 … (7 WPs preserved; regenerated WorkPlan compiles this spec). Gates MSTL-GATE-0..19 + WP gates; first exact failure freezes candidate at gate; next-in-order until exhausted. Terminals: `DYNAMIC_OPTIMALITY_PROVED` (iff PA chain REVIEWED + bridge audited) or honest `PROMOTED_CANDIDATE_SET_REJECTED / SYNCHRONOUS_REPAYMENT_REFUTED / GLOBAL_INTEGRABILITY_REFUTED / PAIR_ACCESS_ROUTE_REFUTED_NO_DOC_NEGATIVE / BRIDGE_BLOCKED_NO_CLAIM / RESOURCE_LIMIT_NO_CLAIM / LEGACY_EMBEDDING_FAIL / AXIS_INCONCLUSIVE`.

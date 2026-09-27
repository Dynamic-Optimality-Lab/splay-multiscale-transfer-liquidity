# SPLAY-AM-MST-LIQ-v0.4.1 CONTRACT-CLOSURE Amendment

Historical spec: historical/IMPLEMENTATION_SPEC_SPLAY-AM-MST-LIQ-v0.4.txt (SHA-256 0E2C166E1B721DFC8A7E5327ED33AF29A1B4AC539CB71849F3C7231B32A8055B).
This amendment + IMPLEMENTATION_SPEC_SPLAY-AM-MST-LIQ-v0.4.1.md are operative; v0.4 prose bows to them on conflict.

## Per-finding repairs

### CC-001 [BLOCKER] -> contract completion
Finding: Architecture-parent identity not closed: nav vs closure vs seal commit ambiguous
Repair: Multi-identity parent contract: architecture_navigation_commit, architecture_closure_commit, architecture_seal_commit + per-artifact content SHAs (FINAL_RESULT/manifest/archive/WorkPlan/Path/ledger/theorem-status/candidate-set/spec); WP-0 re-verifies content SHAs against pinned commits
Artifacts: prereg/parent_contract.yaml, IMPLEMENTATION_SPEC_...v0.4.1.md#parent-contract
Backward compat: v0.4 pins single SHA; v0.4.1 names roles, old SHA retained as navigation
Status: CLOSED

### CC-002 [BLOCKER] -> contract completion
Finding: Obstruction parent lacks lifecycle refutation closure (Lean witness + G5 pending)
Repair: Split fields: obstruction_evidence_commit + mathematical_status=CONFIRMED + formal_certificate_status=PENDING + human_validation_status=PENDING + lifecycle_seal=OPEN; forbid calling it sealed; REFUTED lifecycle only after formal+human close
Artifacts: prereg/parent_contract.yaml
Backward compat: Narrows v0.4 wording; witness bytes unchanged
Status: CLOSED

### CC-003 [BLOCKER] -> contract completion
Finding: No dual-parent precedence rule; arch sealed nodes unproved while Dynamic later REVIEWED 08U/09/11/13/22
Repair: PARENT_PROVENANCE_MATRIX per object (definition/statement/proof/review/evidence source + rule): architecture owns definitions; later parent supplies proof/refutation evidence only under identical bytes + transport theorem, else new MSTL bytes
Artifacts: planning/PARENT_PROVENANCE_MATRIX.yaml
Backward compat: v0.4 silent-copy risk removed; no status values altered
Status: CLOSED

### CC-004 [BLOCKER] -> source-derived correction
Finding: Legal domain conflicts: v0.4 expects keys(T0)==[n]; obstruction legal_domain uses keys(T0) subset [n], absent access keys allowed
Repair: Adopt source-derived weaker domain: keys(T0) subset [n], valid BST, modes KEEP/DELETE, access keys in [n] (presence NOT required), A/B start equal T0, exact replay semantics; equality only as explicitly labeled proof-restricted subdomain (new ID, never silent)
Artifacts: IMPLEMENTATION_SPEC_...v0.4.1.md#legal-domain, prereg predicate/legal hashes
Backward compat: v0.4-era proofs under equality must be re-scoped, not auto-transported
Status: CLOSED

### CC-005 [BLOCKER] -> clarification
Finding: 'All universal theorems use LegalPairInstance' over-scopes: ledger algebra (discharge, preservation, SPENT monotonicity, MST0-15 parts) should stay total
Repair: Two theorem classes: A tree/history theorems require LegalPairInstance; B pure ledger algebra total over arbitrary ledgers/needs, MUST NOT add tree-legality hypotheses
Artifacts: math/theorems/*.md (per-theorem Domain:), theorem_gate_matrix.yaml
Backward compat: None adverse; class-B statements keep full strength
Status: CLOSED

### CC-006 [BLOCKER] -> contract completion
Finding: Weaker domain vs multiplicity theorem: present-key statement incompatible with absent-key legal traces (nonzero depth+1 cost, empty rotation trace)
Repair: Split theorem: present-key accesses sum mu(ev)=depth; absent-key accesses: trace empty, tree unchanged, cost=depth_to_leaf+1, zero activation opportunities; freeze both statements + absent-access replay semantics (no T7/T5, no discharge change)
Artifacts: math/theorems/LIQ0-02.md, spec#absent-access-semantics
Backward compat: v0.4 LIQ0-02 statement superseded by two precise statements
Status: CLOSED

### CC-007 [BLOCKER] -> source-derived correction
Finding: T5_1(L,m) undefined for candidate family: activation depends on frozen predicate P (P_all vs P_keep vs case-restricted)
Repair: Define T5_{P,1}(L,m,ev): P bound per predicate definition (mode + normalized event class only); P_all fires always, P_keep fires on KEEP, case-restricted per allowlist; T5_{P,rho} bounded iteration of that exact primitive
Artifacts: spec#T5-def, prereg/predicate_family_v0.4.1.yaml
Backward compat: Old FLAT(1)/P_all behavior provably unchanged (LIQ0-01)
Status: CLOSED

### CC-008 [BLOCKER] -> contract completion
Finding: T5_rho never inserted into A/B replay: ordering T7->T5rho / T5rho / discharge-after-B-trace not frozen
Repair: Freeze verbatim replay equations: A-side per StepEv T7->T5_{P,rho}; B-side per StepEv T5_{P,rho} (predicate-evaluated); KEEP discharge unchanged T6 after complete B trace; DELETE no B replay/discharge; ordering hash-bound in candidate identity
Artifacts: spec#replay-equations, candidate identity fields
Backward compat: Matches inherited execution at FLAT(1) by construction
Status: CLOSED

### CC-009 [BLOCKER] -> clarification
Finding: Activation-count identity uses total LATENT q, but #4 says eligible LATENT
Repair: Formulas use eligibleLatentCount(L,P,m,ev); define eligibility (LATENT + support-allowed + predicate-fires + ledger-order position); ACTIVE'=ACTIVE+min(q_elig,b), LATENT'=LATENT-min(q_elig,b)
Artifacts: spec#eligibility, math/theorems/LIQ0-*.md
Backward compat: At P_all/all-eligible reduces to v0.4 formula
Status: CLOSED

### CC-010 [BLOCKER] -> contract completion
Finding: P_inherited not closed: parent grammar defines T5 constraints, not a predicate menu
Repair: prereg/predicate_family_v0.4.1.yaml enumerates P_all, P_keep (exact mode tables) + case-restricted schema (normalized event-class allowlist) with canonical enumeration frozen at WP-0; no post-freeze predicates
Artifacts: prereg/predicate_family_v0.4.1.yaml
Backward compat: Supersets v0.4 'at minimum' list with exact bytes
Status: CLOSED

### CC-011 [BLOCKER] -> contract completion
Finding: Unclear whether full T1-T10 grammar reruns or only (P,k,C,rho) varies; objective mentions rule-template counts
Repair: Choose (B): non-liquidity mechanics held fixed at inherited Branch-A architecture; synthesis searches only enumerated (P,k,C,rho); drop rule-template/support-complexity objective terms; keep predicate-simplicity + profile-simplicity ordering
Artifacts: spec#search-space, prereg/liquidity_search_space.yaml
Backward compat: Full-grammar search explicitly out of scope (successor material)
Status: CLOSED

### CC-012 [BLOCKER] -> actual semantic change
Finding: Rho axis underparameterized: only (r,r),(r,2r); (1,3) is same axis but inexpressible
Repair: Mathematical class rho=(rho_ZIG,rho_DOUBLE), each in 0..8, symmetric across LL/RR/LR/RL; FLAT(r)=(r,r), ROT(r)=(r,2r) named subfamilies; ROOT/no-event rho=0
Artifacts: prereg/liquidity_axis.yaml
Backward compat: v0.4 12 profiles embed 1-1; old results comparable
Status: CLOSED

### CC-013 [BLOCKER] -> clarification
Finding: r<=6 vs successor rule: needing r=7 is not a new axis but #5 demands successor for larger families
Repair: Separate discovery ladder (frozen 12: FLAT/ROT r=1..6) from admissible class (0..8^2); r=7 uses versioned ladder extension; successor only for new degrees of freedom/dependencies outside rho-profile semantics
Artifacts: prereg/liquidity_axis.yaml#ladder
Backward compat: Strictly more permissive than v0.4 text; frozen ladder unchanged
Status: CLOSED

### CC-014 [BLOCKER] -> contract completion
Finding: Theorem targets lack exact bytes: LIQ0 names, MSTL-15 'such as', PA target form, telescope/bridge prose
Repair: Exact versioned statement files math/theorems/{LIQ0-01..10,MSTL-08U,09,10,11,12,13,14,15,16,17,18,19,22,23,24,25,26}.md with quantifiers/domain/constants/assumptions/conclusion/candidate-dependence/negation/first-consumer before synthesis
Artifacts: math/theorems/*.md (27 files)
Backward compat: Supersede prose-only targets
Status: CLOSED

### CC-015 [BLOCKER] -> contract completion
Finding: 26-node ledger not fully mapped: #42 maps 16, missing MST0-01..07,12,20,21
Repair: theorem_gate_matrix.yaml dispositions all 26: IDENTICAL_TRANSPORT / REPROVE_UNDER_RHO / GENERALIZED_NEW_BYTES / DOWNSTREAM_REBOUND / CONDITIONAL / NOT_APPLICABLE + justification; MSTL-12 added (signed bound); MST0-20/21 OUT_OF_SCOPE (DOC-disproof outside LIQ, CC-066)
Artifacts: prereg/theorem_gate_matrix.yaml
Backward compat: 16 mapped entries preserved, 10 added
Status: CLOSED

### CC-016 [BLOCKER] -> contract completion
Finding: MST0-09 mapped but missing from ladder/war (MSTL-GATE-13 mentions locality/preservation only); Dynamic gate needs 08U/09/11/13/14/15/22
Repair: MSTL-09 explicit identity/status/owner (WP-2 dev, WP-6 proof) + present in PA prerequisite conjunction + gate MSTL-GATE-13 checks 08U/09/11/13
Artifacts: prereg/theorem_gate_matrix.yaml, math/theorems/MSTL-09.md
Backward compat: Adds missing endgame check
Status: CLOSED

### CC-017 [BLOCKER] -> contract completion
Finding: 'After required upstream REVIEWED' not enumerated for Pair Access
Repair: Freeze PA prerequisites: MSTL-08U/09/11/13/14/15/22 REVIEWED + LIQ0-01/02/04/05/06/09/10 at required statuses; machine-checked before MSTL-17 PROVE track
Artifacts: spec#PA-prerequisites
Backward compat: Strictly explicit version of v0.4 intent
Status: CLOSED

### CC-018 [BLOCKER] -> contract completion
Finding: Theorem provenance ambiguous: MST0-08U/09/11/13/22 more mature in Dynamic than arch; 'parent proof' undefined
Repair: Provenance matrix rule: transport later proof only under byte-identical statements + rho-invariance transport theorem; else reprove or mint new MSTL bytes; inherited ACCEPT valid only for exact reviewed bytes
Artifacts: planning/PARENT_PROVENANCE_MATRIX.yaml
Backward compat: No statuses copied
Status: CLOSED

### CC-019 [BLOCKER] -> contract completion
Finding: Branch-B activation condition not operational (dev vs fresh vs theorem failure?)
Repair: Branch B activates iff Branch-A PROMOTED set rejected at development (no eligible survivor) OR fresh (PROMOTED_CANDIDATE_SET_REJECTED); late theorem failure does NOT open new synthesis (CC-020)
Artifacts: spec#branch-B-activation
Backward compat: Narrows v0.4 trigger prose
Status: CLOSED

### CC-020 [BLOCKER] -> firewall hardening
Finding: Late Branch-A theorem failure makes Branch B post-holdout adaptation (PHASE11 passed, H4L revealed)
Repair: All usable Branch-B identities/grammar frozen dormant pre-reveal; post-reveal only already-frozen Branch-B set may run on H4L; otherwise successor + new bank
Artifacts: spec#branch-B-freeze, prereg predicate/grammar
Backward compat: Forbids v0.4-permitted late adaptation
Status: CLOSED

### CC-021 [BLOCKER] -> contract completion
Finding: Signed Branch-B rho semantics unbound (unsigned LATENT/ACTIVE/SPENT vs signed masses)
Repair: Define signed T5_{P,rho}: activation preserves sign-mass, energy E_signed=sum(m) with proved lower bound MSTL-12; candidate identity binds signed energy/lower-bound definition; unsigned theorems do not transfer silently
Artifacts: spec#signed-semantics, math/theorems/MSTL-12.md
Backward compat: Branch B closed only when these bytes exist
Status: CLOSED

### CC-022 [BLOCKER] -> contract completion
Finding: H4L generator underspecified ('Recommended' sizes/strata; missing quotas/laws/RNG/seeds/dedup/serialization/hashes)
Repair: Freeze exact: sizes [18,26,34,46,58,74,98] x10k=70k; per-stratum quotas (equal split 833 or 834 with deterministic remainder schedule); history-length law; tree-shape law; SHA-256 counter DRBG; secret seed protocol; dedup-reject-resample; weaker-domain legality filter; canonical JSON serialization; sorted order; .json.zst shards; per-shard + logical-stream SHA; commitment construction
Artifacts: prereg/h4l_holdout.yaml
Backward compat: Recommendations promoted to normative values
Status: CLOSED

### CC-023 [BLOCKER] -> firewall hardening
Finding: Public Git is not quarantine: committed bytes/seeds readable by discovery
Repair: True commitment: pre-reveal public = commitment hash + non-sensitive metadata ONLY; seed + bank bytes held outside public/discovery repo (operator-held secret); reveal publishes + verifies; no .gitignore/LFS/encrypted-in-repo fakery; without inaccessible storage H4L BLOCKED
Artifacts: spec#H4L-secrecy, prereg/h4l_holdout.yaml
Backward compat: Supersedes old WorkPlan quarantine-by-commit
Status: CLOSED

### CC-024 [BLOCKER] -> firewall hardening
Finding: No exact H4L firewall state machine (states/transitions/readers/unlock count)
Repair: States EMPTY->GENERATOR_FROZEN->BANK_GENERATED_SECRET->COMMITMENT_PUBLISHED->CANDIDATE_SET_FROZEN->REVEALED_ONCE->CONSUMED; legal readers/writers per state; unlock count immutable <=1; violations fail closed with STOP IDs
Artifacts: spec#H4L-firewall, firewall.py contract
Backward compat: Compatible with v0.4 intent, exact
Status: CLOSED

### CC-025 [BLOCKER] -> clarification
Finding: WP-0 vs WP-3 disagree on H4L generator freeze ownership
Repair: WP-0 freezes GENERATOR CONTRACT (normative semantics); WP-3 implements code, certifies hash-equivalent/compliant implementation, then generates; no normative semantics invented in WP-3
Artifacts: spec#freeze-ownership
Backward compat: Resolves plan contradiction
Status: CLOSED

### CC-026 [BLOCKER] -> contract completion
Finding: Top-3 promotion makes LIQUIDITY_CALCULUS_REJECTED too strong (refutes 3, not grammar)
Repair: Evaluate every eligible survivor; <=3 cap allowed only with domination/equivalence proof; otherwise terminal PROMOTED_CANDIDATE_SET_REJECTED; LIQUIDITY_CALCULUS_REJECTED only after full declared space eliminated; 'second candidate' generalized to next-in-order-until-exhausted
Artifacts: spec#promotion, terminals
Backward compat: Honest renaming; old label retained only for full elimination
Status: CLOSED

### CC-027 [BLOCKER] -> lifecycle hardening
Finding: Refutation lifecycle missing: only UNPROVED->PROVED->REVIEWED yet terminals include REFUTED
Repair: Dual prove/refute lifecycle states (UNPROVED/PROVE_RUNNING/PROVED_PENDING_REVIEW/REVIEWED/NO_WITNESS/WITNESS_FOUND/MATHEMATICAL_COUNTEREXAMPLE_CONFIRMED/FORMAL_REFUTATION_PENDING/HUMAN_VALIDATION_PENDING/REFUTED/BLOCKED/NOT_REACHED/NOT_APPLICABLE); REJECT!=REFUTED; REFUTED needs exact negation witness + candidate hash + 3-route replay (primary/independent/formal-or-MATH_CONFIRMED) + human validation
Artifacts: spec#lifecycle, schemas/theorem_status.schema.json
Backward compat: Adds paths; existing path preserved
Status: CLOSED

### CC-028 [BLOCKER] -> clarification
Finding: 'Three execution routes' vs 'Lean where feasible' contradictory
Repair: Two routes mandatory (primary + independently structured); formal Lean mandatory where technically applicable, else MATHEMATICAL_COUNTEREXAMPLE_CONFIRMED preserved without promotion to REFUTED; applicability decided per-theorem pre-attack with recorded reason
Artifacts: spec#execution-routes
Backward compat: Resolves contradiction without weakening evidence bar
Status: CLOSED

### CC-029 [MAJOR] -> contract completion
Finding: Internal-validation contract unspecified (sizes/generators/masks/seeds/disjointness)
Repair: Freeze validation spec: generators (seeded structural, disjoint seed stream from dev), sizes [7,8,10,12,16], histories/law, 5k episodes, masks (states/cycles/histories disjoint from dev by ID sets), candidate-contact policy (frozen candidates only, no synthesis feedback)
Artifacts: prereg/liquidity_search_space.yaml#validation
Backward compat: New exact split; dev corpora unchanged
Status: CLOSED

### CC-030 [MAJOR] -> reproducibility hardening
Finding: Adversarial campaigns lack frozen budgets (iters/seeds/objectives/shards/caps/reduction)
Repair: Freeze per-engine: deterministic seeds, evaluation budgets (e.g., hillclimb 20k steps x5 restarts; anneal/genetic equivalents tabled), size ranges, objective=residual-hunt, shard counts, wall/mem caps, sorted reduction + tie-break, resource-limit record fields; survival reproducible
Artifacts: prereg/liquidity_search_space.yaml#adversarial
Backward compat: Effort becomes part of contract
Status: CLOSED

### CC-031 [MAJOR] -> firewall hardening
Finding: Clean-room verifier not frozen before reveal; post-failure authorship weakens independence
Repair: Freeze before reveal: clean-room semantic spec + forbidden imports + authoring boundary + I/O schema + independence requirements; implementation bytes hash-frozen pre-reveal; post-reveal changes only via preregistered replay interface, mechanically audited
Artifacts: spec#cleanroom, artifacts/v04/cleanroom/contract hash
Backward compat: Strengthens v0.4 independence claim
Status: CLOSED

### CC-032 [MAJOR] -> contract completion
Finding: Parent T01-T90/STOP-01-50/INV-001-070/tests never dispositioned ('inherited applicable' vague)
Repair: PARENT_CONTROL_DISPOSITION.yaml enumerates every parent T/STOP/INV/named-test with INHERITED_UNCHANGED / INHERITED_MODIFIED / SUPERSEDED / NOT_APPLICABLE + reason + replacement
Artifacts: planning/PARENT_CONTROL_DISPOSITION.yaml
Backward compat: No control silently dropped or kept
Status: CLOSED

### CC-033 [MAJOR] -> contract completion
Finding: New ladder drops parent gates (L6 translation, rotation refinement, heavy/pairing/bend, lower-bound, holdout-scope)
Repair: MSTL is overlay: every inherited gate either discharged-by-transport (recorded) or explicitly re-owned; gate matrix lists inherited gate + disposition
Artifacts: prereg/theorem_gate_matrix.yaml
Backward compat: Parent gates preserved
Status: CLOSED

### CC-034 [MAJOR] -> contract completion
Finding: H1/H2R/n8 lack LIQ disposition (only H3T declared historical)
Repair: Declare in LIQ: H1 HISTORICAL_UNUSED (EMPTY preserved), H2R HISTORICAL_UNUSED (COMMITTED/0 preserved, never unlocked here), n8 CONTAMINATED_CANARY (never fresh/validation), H3T HISTORICAL (UNLOCKED_ONCE preserved)
Artifacts: prereg/h4l_holdout.yaml#legacy-banks
Backward compat: Unlock counts preserved
Status: CLOSED

### CC-035 [MAJOR] -> contract completion
Finding: H4L fresh but not distribution-disjoint (strata overlap dev motifs); 'entirely different' claim at risk
Repair: Separate categories: development / internal validation / fresh H4L / OOD benchmark / clean-room / large-n / formal; freeze OOD family (different generator: long-range random-walk histories + adversarial spine-heavy trees, disjoint seed stream, sizes [24,48,96,192]) evaluated post-freeze, labeled OOD not fresh-holdout
Artifacts: prereg/h4l_holdout.yaml#ood
Backward compat: Adds category; H4L claims unchanged
Status: CLOSED

### CC-036 [MAJOR] -> contract completion
Finding: Attribution confounded: (P,k,C,rho) vary together; FLAT(1)/larger-C survivor would not prove liquidity
Repair: Matched rho=FLAT(1) baseline search over same P/k/C space + pipeline + corpora; labels RHO_REQUIRED / RHO_NOT_REQUIRED / C_ONLY_REPAIR / K_OR_P_REPAIR / MIXED_AXIS_REPAIR / NO_SURVIVOR; liquidity confirmed only under RHO_REQUIRED
Artifacts: spec#attribution, WP-4 ranking schema
Backward compat: Forbids v0.4-permitted overclaim
Status: CLOSED

### CC-037 [MAJOR] -> contract completion
Finding: Candidate identity 'at least' list incomplete (predicate/legal/mu/replay/required_C/discharge/executor hashes missing)
Repair: Identity hash-binds: calculus_id, rule_family_id, parent family, branch, predicate def/hash, k, C, rho profile def/hash, event-normalization/mu hash, legal-domain hash, credit types, support, scale, provenance, T7, T5_rho, T6, selection order, A/B replay order, discharge order, required_C hash, energy/lower-bound def, init, snapshot convention, executor semantics hash, mapping/ontology versions
Artifacts: schemas/candidate.schema.json
Backward compat: Superset of v0.4 list
Status: CLOSED

### CC-038 [MAJOR] -> clarification
Finding: Cross-C testing vs calculus-ID rule: C in identity but 'same rule at larger C' invites in-place mutation
Repair: rule_family_id + calculus_id=f(rule_family_id,C); changing C mints new ID; ladder runs are distinct frozen instances, never mutations
Artifacts: schemas/candidate.schema.json#family
Backward compat: Makes v0.4 ladder practice ID-safe
Status: CLOSED

### CC-039 [MAJOR] -> contract completion
Finding: A(n) open-ended escape hatch (nonzero permitted if later bridge-compatible)
Repair: Only live target A(n)=0; nonzero class BLOCKED until bridge-derived admissible class frozen from pinned sources; failed A=0 proof must not invent additive terms
Artifacts: spec#additive-term, math/theorems/MSTL-18.md
Backward compat: Narrows v0.4 permission
Status: CLOSED

### CC-040 [MAJOR] -> contract completion
Finding: Bridge/literature bytes unpinned; DECIDE records MST0-19 blocked on sources, yet LIQ allows DO_PROVED
Repair: WP-0 pins Levy-Tarjan source/version/bytes/hash/statement/direction/conventions/assumptions/mapping/checklist/manifest; if unavailable MSTL-19=BLOCKED_BY_SOURCE and DO unreachable; no folklore bridges
Artifacts: prereg/bridge_manifest.yaml
Backward compat: DO gated on bytes, not prose
Status: CLOSED

### CC-041 [MAJOR] -> reproducibility hardening
Finding: Environment/toolchain not frozen (Lean/lake/manifest/Python/solvers/threads/RNG/compression)
Repair: prereg/environment_lock.yaml: Python 3.13.7 + dep hashes at WP-0, Lean v4.21.0 + lake config/manifest (source: obstruction parent toolchain), solver builds/versions, single-thread-deterministic policy, SHA-256-DRBG RNG, zstd deterministic params, env vars; runs record env-lock hash
Artifacts: prereg/environment_lock.yaml
Backward compat: New normative lock
Status: CLOSED

### CC-042 [MAJOR] -> reproducibility hardening
Finding: Exact-arithmetic/determinism policy weaker than parent (float signs, sorted reductions)
Repair: Inherit explicitly: no float-determined residual signs; exact integer/rational theorem decisions; deterministic sorted reductions; canonical tie-break/sharding; logical-stream hashes; exact cert replay; heuristics propose, evaluators dispose; resource exhaustion never impossibility
Artifacts: spec#exactness
Backward compat: Restores parent guarantee
Status: CLOSED

### CC-043 [MAJOR] -> reproducibility hardening
Finding: Logging regresses: branch/ancestors/literature/gate-matrix/runtime hashes missing vs parent
Repair: Logging = parent superset + rho/dual-parent fields (33 fields incl. branch, clean-tree state, source-tree manifest, arch/obstruction/ancestor IDs, spec+amendment+prereg+gate-matrix+literature+env SHAs, candidate/family IDs, P/k/C/rho+profile+legal-domain SHAs, firewall, command/IO/std hashes, wall/peak/exit/status)
Artifacts: schemas/runlog.schema.json
Backward compat: Superset; old consumers unaffected
Status: CLOSED

### CC-044 [MAJOR] -> reproducibility hardening
Finding: Dirty-tree runs unverifiable (commit hash != executed bytes; generator-before-commit risk)
Repair: Authoritative runs require committed producer code + git status --porcelain empty; else full content manifest + diagnostic-only status (no theorem/fresh claims); generator committed before H4L generation
Artifacts: spec#clean-tree
Backward compat: New gate on old practice
Status: CLOSED

### CC-045 [MAJOR] -> reproducibility hardening
Finding: Large-artifact rules missing (H4L/large-n huge; logical hashes only at final repro)
Repair: .json.zst deterministic params, shard naming/order, per-shard SHA, manifest, logical-stream SHA, canonical serialization; no uncontrolled raw artifacts
Artifacts: spec#artifacts
Backward compat: Restores parent policy
Status: CLOSED

### CC-046 [MAJOR] -> reproducibility hardening
Finding: Final-seal mechanics underdefined (scope/order/self-ref/archive/manifest/rebuild/stale/failed-artifacts)
Repair: Exact: manifest scope+exclusions+ordering, seal ordering, no-self-hash policy, deterministic archive name+construction+SHA, FINAL_RESULT generation from artifacts, rebuild-identical check, stale detection, failed-artifact preservation, clean-checkout repro
Artifacts: spec#seal
Backward compat: New exact mechanics
Status: CLOSED

### CC-047 [MAJOR] -> contract completion
Finding: Reproduction impossible for early terminals (unconditional H4L/proof/Lean checklist)
Repair: Reached-phase matrix: each terminal verifies existing artifacts + explicit NOT_REACHED/NOT_APPLICABLE for later ones + absence of illegal downstream artifacts
Artifacts: spec#reproduction-matrix
Backward compat: Conditional version of v0.4 list
Status: CLOSED

### CC-048 [MAJOR] -> contract completion
Finding: No normative clone/bootstrap transaction ('additions relative to cloned parent')
Repair: Bootstrap: import exact pinned parent tree; preserve history as v0.3/history; byte-equality manifest; classify every file IMPORTED_UNCHANGED / SURGICALLY_MODIFIED / SUPERSEDED_BY_VERSIONED_FILE / EXPLICITLY_NOT_IMPORTED_WITH_REASON; new results only under v0.4.1 namespaces; PARENT_TREE_DISPOSITION.yaml, unclassified=closure failure
Artifacts: planning/PARENT_TREE_DISPOSITION.yaml
Backward compat: New gate
Status: CLOSED

### CC-049 [MAJOR] -> contract completion
Finding: WorkPlan/Path governance not normative (required only by external prompt)
Repair: v0.4.1 mandates WorkPlan.md (compilation of closed spec) + Path.md (append-only live ledger, contemporaneous WP/gate updates, failed history preserved)
Artifacts: spec#governance
Backward compat: Prompts prompt-rule into spec
Status: CLOSED

### CC-050 [MAJOR] -> lifecycle hardening
Finding: No canonical status ledger/review schema (lifecycle prose only; no REJECT/BLOCKED/hash-invalidation)
Repair: Mandate math/proof_status.json + schemas (states/tracks/transitions/review binding/hashes/invalidation/BLOCKED/NOT_REACHED); changed bytes invalidate review
Artifacts: schemas/theorem_status.schema.json, schemas/review.schema.json
Backward compat: New normative ledger
Status: CLOSED

### CC-051 [MAJOR] -> clarification
Finding: transport vs gate matrix filename inconsistent (layout vs #42)
Repair: Canonical prereg/theorem_gate_matrix.yaml for gates; theorem_transport_matrix.yaml SUPERSEDED (kept only as historical pointer); provenance matrix keeps transport rationale per object
Artifacts: prereg/theorem_gate_matrix.yaml
Backward compat: One name survives
Status: CLOSED

### CC-052 [MAJOR] -> reproducibility hardening
Finding: MST_LIQ_EXPORT.json without schema/verifier (main experiment would trust without rerun)
Repair: schemas/mst_liq_export.schema.json + import verifier binding version/seal/candidate history/IDs/semantic+legal+parent hashes/DAG/status/proof/Lean/review/bridge/counterexample/fresh-bank/claim
Artifacts: schemas/mst_liq_export.schema.json
Backward compat: New gate
Status: CLOSED

### CC-053 [MAJOR] -> contract completion
Finding: Successors not required to prove backward embedding (M-chain drawn, never required)
Repair: Every successor must prove legacy embedding (prior architecture recovered at old parameters) + retain axes + add one justified axis + preserve failures/witnesses
Artifacts: spec#successor
Backward compat: Strengthens #43
Status: CLOSED

### CC-054 [MAJOR] -> clarification
Finding: 'Clone full MST architecture' ambiguous recursively (could clone v0.3, losing rho)
Repair: Clone latest sealed architecture retaining accepted axes unless explicitly justified otherwise
Artifacts: spec#successor
Backward compat: Disambiguates #43
Status: CLOSED

### CC-055 [HARDENING] -> clarification
Finding: LIQ0-02 failure handling bundles whole axis (ROT death should not kill FLAT)
Repair: Separate gates: ROT-ineligible on LIQ0-02 falsity; FLAT continues on own obligations; axis dies only on axis-wide obligation failure
Artifacts: spec#profile-gates, math/theorems/LIQ0-02.md
Backward compat: Narrows failure blast radius
Status: CLOSED

### CC-056 [HARDENING] -> clarification
Finding: Event naming: ZIG-left/ZIG-right vs single ZIG normalization unmapped
Repair: Freeze normalization: trace preserves oriented ZIG-L/R; mu maps both to class ZIG (rho_ZIG); orientation retained in ledger/support records
Artifacts: spec#event-normalization
Backward compat: No behavior change
Status: CLOSED

### CC-057 [HARDENING] -> clarification
Finding: FLAT undefined on ROOT/no-event (ROT has mu(ROOT)=0; FLAT only for eligible non-ROOT)
Repair: rho_flat(ROOT)=0, rho(any,ROOT)=0, no-event calls T5 zero times; or prove callers exclude ROOT (choose former: total function)
Artifacts: prereg/liquidity_axis.yaml
Backward compat: Totalizes definition
Status: CLOSED

### CC-058 [HARDENING] -> clarification
Finding: 'Known n=28 witness is repaired' invites witness-mutation reading
Repair: Replace with 'candidate evaluates execSuffices=true on immutable LIQ-REG-001 (hash-bound, never modified)'
Artifacts: spec#promotion-wording
Backward compat: Wording fix with teeth
Status: CLOSED

### CC-059 [HARDENING] -> contract completion
Finding: 'Delta minimization' undefined (global vs local minimality)
Repair: Certificate levels: operation-deletion minimal / parameter-family minimal / exhaustive-global minimal; prohibit stronger wording than certificate supports
Artifacts: spec#minimization
Backward compat: New exact levels
Status: CLOSED

### CC-060 [HARDENING] -> clarification
Finding: S5/S6 'repair known family' overclaims conjectured DDKK closed form
Repair: Read as frozen tested members unless symbolic family theorem closes (new MSTL-FAM theorem with proof)
Artifacts: spec#success-wording
Backward compat: Restricts S5/S6 to evidence
Status: CLOSED

### CC-061 [HARDENING] -> clarification
Finding: S10 'smallest preregistered C survives' reads as global minimality proof
Repair: Read as 'smallest tested preregistered C ladder rung with survivor'; no global-minimality claim
Artifacts: spec#success-wording
Backward compat: Restricts S10
Status: CLOSED

### CC-062 [HARDENING] -> clarification
Finding: S19 demands 'exact missing resource', forcing stories for bare obstructions
Repair: Permit 'no justified missing resource identified' as honest S19 answer with preserved obstruction
Artifacts: spec#success-wording
Backward compat: Adds honest outcome
Status: CLOSED

### CC-063 [HARDENING] -> clarification
Finding: 'Second already-frozen candidate' should generalize to set exhaustion
Repair: Attempt next frozen candidate in predetermined order until set exhausted
Artifacts: spec#candidate-order
Backward compat: Generalizes to cap
Status: CLOSED

### CC-064 [HARDENING] -> reproducibility hardening
Finding: Resource-limit behavior underspecified (no record fields/budgets)
Repair: Exact resource-limit record (attempted/unattempted work, budgets, deterministic policy) required for RESOURCE_LIMIT_NO_CLAIM (and PROMOTED-set variant)
Artifacts: spec#resource-record
Backward compat: Restores parent practice
Status: CLOSED

### CC-065 [HARDENING] -> lifecycle hardening
Finding: Review REJECT/BLOCKED behavior missing (ACCEPT defined only); rejection must not equal refutation; byte-change invalidation
Repair: REJECT=proof package rejected (truth stays UNPROVED, re-review lawful); BLOCKED=truth BLOCKED until clearer; any theorem/proof byte change invalidates prior review binding (hash mismatch fails closed)
Artifacts: schemas/review.schema.json
Backward compat: Fills verdict gap
Status: CLOSED

### CC-066 [HARDENING] -> contract completion
Finding: Negative DOC route referenced ('independent negative theorem standard') but unbound
Repair: DOC-disproof explicitly OUTSIDE MST-LIQ; transfer-route failure never a DOC claim; terminology import from parent NEG contract by reference only (no evidentiary reuse); MST0-20/21 OUT_OF_SCOPE with reason
Artifacts: prereg/theorem_gate_matrix.yaml#MST0-20/21
Backward compat: Removes implied capability
Status: CLOSED

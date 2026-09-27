"""CC-029..066 records + emit all closure artifacts. Run: python scripts/build_closure_tail.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_closure import CC, cc, ROOT, ARCH_NAV, ARCH_CLOSURE, ARCH_SEAL, OB_EVID, V04_SHA
import yaml

B = "BLOCKER"; M = "MAJOR"; H = "HARDENING"
# ---- validation/adversarial budgets (029-030) ----
cc(29, M, "Internal-validation contract unspecified (sizes/generators/masks/seeds/disjointness)",
   ["#16", "MSTL-GATE-8"], "v0.4 objective/promotion/ladder mention validation without parameters",
   "Load-bearing split without a contract", "Freeze validation spec: generators (seeded structural, disjoint seed stream from dev), sizes [7,8,10,12,16], histories/law, 5k episodes, masks (states/cycles/histories disjoint from dev by ID sets), candidate-contact policy (frozen candidates only, no synthesis feedback)",
   ["prereg/liquidity_search_space.yaml#validation"], "contract completion", "New exact split; dev corpora unchanged",
   ["HOLDOUT_FIREWALL_ERRORS"], ["WP-4"])
cc(30, M, "Adversarial campaigns lack frozen budgets (iters/seeds/objectives/shards/caps/reduction)",
   ["#20"], "v0.4 names 9 engines only",
   "Survival depends on effort", "Freeze per-engine: deterministic seeds, evaluation budgets (e.g., hillclimb 20k steps x5 restarts; anneal/genetic equivalents tabled), size ranges, objective=residual-hunt, shard counts, wall/mem caps, sorted reduction + tie-break, resource-limit record fields; survival reproducible",
   ["prereg/liquidity_search_space.yaml#adversarial"], "reproducibility hardening", "Effort becomes part of contract",
   ["ARTIFACT_POLICY_ERRORS"], ["WP-4", "WP-5"])
# ---- clean-room (031) ----
cc(31, M, "Clean-room verifier not frozen before reveal; post-failure authorship weakens independence",
   ["#21"], "v0.4 #21 requires routes, no freeze timing",
   "Independence without a boundary", "Freeze before reveal: clean-room semantic spec + forbidden imports + authoring boundary + I/O schema + independence requirements; implementation bytes hash-frozen pre-reveal; post-reveal changes only via preregistered replay interface, mechanically audited",
   ["spec#cleanroom", "artifacts/v04/cleanroom/contract hash"], "firewall hardening", "Strengthens v0.4 independence claim",
   ["HOLDOUT_FIREWALL_ERRORS"], ["WP-3", "WP-5"])
# ---- inherited controls (032-034) ----
cc(32, M, "Parent T01-T90/STOP-01-50/INV-001-070/tests never dispositioned ('inherited applicable' vague)",
   ["#40"], "Arch prereg matrices exist (threat/stop blob SHAs recorded); v0.4 says 'in addition to inherited applicable stops'",
   "Vague inheritance of 210+ controls", "PARENT_CONTROL_DISPOSITION.yaml enumerates every parent T/STOP/INV/named-test with INHERITED_UNCHANGED / INHERITED_MODIFIED / SUPERSEDED / NOT_APPLICABLE + reason + replacement",
   ["planning/PARENT_CONTROL_DISPOSITION.yaml"], "contract completion", "No control silently dropped or kept",
   ["PARENT_CONTROL_DISPOSITION_ERRORS"], ["WP-0"])
cc(33, M, "New ladder drops parent gates (L6 translation, rotation refinement, heavy/pairing/bend, lower-bound, holdout-scope)",
   ["#41"], "Arch theorem_gate_matrix.yaml (blob cdac6c...) vs v0.4 MSTL ladder",
   "Overlay mistaken for replacement", "MSTL is overlay: every inherited gate either discharged-by-transport (recorded) or explicitly re-owned; gate matrix lists inherited gate + disposition",
   ["prereg/theorem_gate_matrix.yaml"], "contract completion", "Parent gates preserved",
   ["THEOREM_MAPPING_ERRORS"], ["WP-1", "WP-2", "WP-6"])
cc(34, M, "H1/H2R/n8 lack LIQ disposition (only H3T declared historical)",
   ["#19"], "Arch parent_contract: H1 EMPTY, H2R BANK_COMMITTED/0, n8 PARTIALLY_REVEALED_CANARY_CONTAMINATED; v0.4 silent",
   "Live firewall states unowned", "Declare in LIQ: H1 HISTORICAL_UNUSED (EMPTY preserved), H2R HISTORICAL_UNUSED (COMMITTED/0 preserved, never unlocked here), n8 CONTAMINATED_CANARY (never fresh/validation), H3T HISTORICAL (UNLOCKED_ONCE preserved)",
   ["prereg/h4l_holdout.yaml#legacy-banks"], "contract completion", "Unlock counts preserved",
   ["HOLDOUT_FIREWALL_ERRORS", "PARENT_CONTROL_DISPOSITION_ERRORS"], ["WP-0"])
# ---- OOD + attribution (035-036) ----
cc(35, M, "H4L fresh but not distribution-disjoint (strata overlap dev motifs); 'entirely different' claim at risk",
   ["#18"], "v0.4 strata include bursts/spines/nested shared with #20 dev battery",
   "Fresh-unseen confused with OOD", "Separate categories: development / internal validation / fresh H4L / OOD benchmark / clean-room / large-n / formal; freeze OOD family (different generator: long-range random-walk histories + adversarial spine-heavy trees, disjoint seed stream, sizes [24,48,96,192]) evaluated post-freeze, labeled OOD not fresh-holdout",
   ["prereg/h4l_holdout.yaml#ood"], "contract completion", "Adds category; H4L claims unchanged",
   ["HOLDOUT_FIREWALL_ERRORS"], ["WP-5"])
cc(36, M, "Attribution confounded: (P,k,C,rho) vary together; FLAT(1)/larger-C survivor would not prove liquidity",
   ["#17"], "v0.4 comparison lists profiles but no matched baseline rule",
   "Multi-parameter survivor, single-axis claim", "Matched rho=FLAT(1) baseline search over same P/k/C space + pipeline + corpora; labels RHO_REQUIRED / RHO_NOT_REQUIRED / C_ONLY_REPAIR / K_OR_P_REPAIR / MIXED_AXIS_REPAIR / NO_SURVIVOR; liquidity confirmed only under RHO_REQUIRED",
   ["spec#attribution", "WP-4 ranking schema"], "contract completion", "Forbids v0.4-permitted overclaim",
   ["CANDIDATE_IDENTITY_ERRORS"], ["WP-4"])
# ---- identity/C/ladder (037-038) ----
cc(37, M, "Candidate identity 'at least' list incomplete (predicate/legal/mu/replay/required_C/discharge/executor hashes missing)",
   ["#6"], "v0.4 #6 'at least' wording",
   "Open identity under a closed-ID regime", "Identity hash-binds: calculus_id, rule_family_id, parent family, branch, predicate def/hash, k, C, rho profile def/hash, event-normalization/mu hash, legal-domain hash, credit types, support, scale, provenance, T7, T5_rho, T6, selection order, A/B replay order, discharge order, required_C hash, energy/lower-bound def, init, snapshot convention, executor semantics hash, mapping/ontology versions",
   ["schemas/candidate.schema.json"], "contract completion", "Superset of v0.4 list",
   ["CANDIDATE_IDENTITY_ERRORS"], ["WP-3", "WP-5"])
cc(38, M, "Cross-C testing vs calculus-ID rule: C in identity but 'same rule at larger C' invites in-place mutation",
   ["#15", "#35"], "v0.4 ladder text",
   "Family vs instance conflation", "rule_family_id + calculus_id=f(rule_family_id,C); changing C mints new ID; ladder runs are distinct frozen instances, never mutations",
   ["schemas/candidate.schema.json#family"], "clarification", "Makes v0.4 ladder practice ID-safe",
   ["CANDIDATE_IDENTITY_ERRORS"], ["WP-4", "WP-5"])
# ---- A(n)/bridge/env (039-041) ----
cc(39, M, "A(n) open-ended escape hatch (nonzero permitted if later bridge-compatible)",
   ["#29"], "v0.4 #29 prefers 0, permits nonzero",
   "Post-hoc additive repair", "Only live target A(n)=0; nonzero class BLOCKED until bridge-derived admissible class frozen from pinned sources; failed A=0 proof must not invent additive terms",
   ["spec#additive-term", "math/theorems/MSTL-18.md"], "contract completion (closes escape)", "Narrows v0.4 permission",
   ["THEOREM_IDENTITY_ERRORS"], ["WP-6"])
cc(40, M, "Bridge/literature bytes unpinned; DECIDE records MST0-19 blocked on sources, yet LIQ allows DO_PROVED",
   ["#30"], "DECIDE bridge_sources: L3 PDF frozen, L2 absent -> MST0-19 BLOCKED (verified via Path/bridge record)",
   "Reachable terminal without reachable premises", "WP-0 pins Levy-Tarjan source/version/bytes/hash/statement/direction/conventions/assumptions/mapping/checklist/manifest; if unavailable MSTL-19=BLOCKED_BY_SOURCE and DO unreachable; no folklore bridges",
   ["prereg/bridge_manifest.yaml"], "contract completion", "DO gated on bytes, not prose",
   ["BRIDGE_SOURCE_ERRORS"], ["WP-0", "WP-6"])
cc(41, M, "Environment/toolchain not frozen (Lean/lake/manifest/Python/solvers/threads/RNG/compression)",
   ["#47"], "v0.4 #47 verifies builds without freezing them; DECIDE lean-toolchain leanprover/lean4:v4.21.0",
   "Reproducibility without a locked platform", "prereg/environment_lock.yaml: Python 3.13.7 + dep hashes at WP-0, Lean v4.21.0 + lake config/manifest (source: obstruction parent toolchain), solver builds/versions, single-thread-deterministic policy, SHA-256-DRBG RNG, zstd deterministic params, env vars; runs record env-lock hash",
   ["prereg/environment_lock.yaml"], "reproducibility hardening", "New normative lock",
   ["ENVIRONMENT_LOCK_ERRORS"], ["WP-0"])
# ---- exactness/logging/artifacts/seal/repro/bootstrap (042-048) ----
cc(42, M, "Exact-arithmetic/determinism policy weaker than parent (float signs, sorted reductions)",
   ["#47"], "Arch baseline: exact integers/Fraction, deterministic sorted iteration; v0.4 states exactness locally",
   "Regression by omission", "Inherit explicitly: no float-determined residual signs; exact integer/rational theorem decisions; deterministic sorted reductions; canonical tie-break/sharding; logical-stream hashes; exact cert replay; heuristics propose, evaluators dispose; resource exhaustion never impossibility",
   ["spec#exactness"], "reproducibility hardening", "Restores parent guarantee",
   ["ARTIFACT_POLICY_ERRORS"], ["WP-0"])
cc(43, M, "Logging regresses: branch/ancestors/literature/gate-matrix/runtime hashes missing vs parent",
   ["#46"], "Parent §27 24-field+ record vs v0.4 shorter list (finding comparison)",
   "Successor drops provenance", "Logging = parent superset + rho/dual-parent fields (33 fields incl. branch, clean-tree state, source-tree manifest, arch/obstruction/ancestor IDs, spec+amendment+prereg+gate-matrix+literature+env SHAs, candidate/family IDs, P/k/C/rho+profile+legal-domain SHAs, firewall, command/IO/std hashes, wall/peak/exit/status)",
   ["schemas/runlog.schema.json"], "reproducibility hardening", "Superset; old consumers unaffected",
   ["LOGGING_REGRESSIONS"], ["WP-0"])
cc(44, M, "Dirty-tree runs unverifiable (commit hash != executed bytes; generator-before-commit risk)",
   ["#46"], "Prior seal pain cited in finding",
   "Hash without hygiene", "Authoritative runs require committed producer code + git status --porcelain empty; else full content manifest + diagnostic-only status (no theorem/fresh claims); generator committed before H4L generation",
   ["spec#clean-tree"], "reproducibility hardening", "New gate on old practice",
   ["DIRTY_RUN_POLICY_ERRORS"], ["WP-0", "WP-3"])
cc(45, M, "Large-artifact rules missing (H4L/large-n huge; logical hashes only at final repro)",
   ["#45", "#47"], "Parent required .json.zst + shard manifests + logical-stream hashes; v0.4 silent until #47",
   "Unstorable/unverifiable banks", ".json.zst deterministic params, shard naming/order, per-shard SHA, manifest, logical-stream SHA, canonical serialization; no uncontrolled raw artifacts",
   ["spec#artifacts"], "reproducibility hardening", "Restores parent policy",
   ["ARTIFACT_POLICY_ERRORS"], ["WP-3", "WP-5"])
cc(46, M, "Final-seal mechanics underdefined (scope/order/self-ref/archive/manifest/rebuild/stale/failed-artifacts)",
   ["#19"], "Parent seal pain cited; v0.4 #19 prose only",
   "Unsealable seal", "Exact: manifest scope+exclusions+ordering, seal ordering, no-self-hash policy, deterministic archive name+construction+SHA, FINAL_RESULT generation from artifacts, rebuild-identical check, stale detection, failed-artifact preservation, clean-checkout repro",
   ["spec#seal"], "reproducibility hardening", "New exact mechanics",
   ["SEAL_ERRORS"], ["WP-6"])
cc(47, M, "Reproduction impossible for early terminals (unconditional H4L/proof/Lean checklist)",
   ["#47"], "v0.4 #47 unconditional list",
   "Checklist demands nonexistent artifacts", "Reached-phase matrix: each terminal verifies existing artifacts + explicit NOT_REACHED/NOT_APPLICABLE for later ones + absence of illegal downstream artifacts",
   ["spec#reproduction-matrix"], "contract completion", "Conditional version of v0.4 list",
   ["SEAL_ERRORS"], ["WP-6"])
cc(48, M, "No normative clone/bootstrap transaction ('additions relative to cloned parent')",
   ["#45"], "v0.4 #45 one-liner",
   "New-results namespace unenforced", "Bootstrap: import exact pinned parent tree; preserve history as v0.3/history; byte-equality manifest; classify every file IMPORTED_UNCHANGED / SURGICALLY_MODIFIED / SUPERSEDED_BY_VERSIONED_FILE / EXPLICITLY_NOT_IMPORTED_WITH_REASON; new results only under v0.4.1 namespaces; PARENT_TREE_DISPOSITION.yaml, unclassified=closure failure",
   ["planning/PARENT_TREE_DISPOSITION.yaml"], "contract completion", "New gate",
   ["ARTIFACT_POLICY_ERRORS"], ["WP-0"])
# ---- governance/ledger/naming/export/successor (049-054) ----
cc(49, M, "WorkPlan/Path governance not normative (required only by external prompt)",
   ["#32"], "v0.4 pins parent plans but mandates no live ledger for LIQ",
   "Governance by prompt, not contract", "v0.4.1 mandates WorkPlan.md (compilation of closed spec) + Path.md (append-only live ledger, contemporaneous WP/gate updates, failed history preserved)",
   ["spec#governance"], "contract completion", "Prompts prompt-rule into spec",
   ["THEOREM_MAPPING_ERRORS"], ["WP-0"])
cc(50, M, "No canonical status ledger/review schema (lifecycle prose only; no REJECT/BLOCKED/hash-invalidation)",
   ["#22"], "v0.4 #22 prose",
   "Statuses without a ledger", "Mandate math/proof_status.json + schemas (states/tracks/transitions/review binding/hashes/invalidation/BLOCKED/NOT_REACHED); changed bytes invalidate review",
   ["schemas/theorem_status.schema.json", "schemas/review.schema.json"], "lifecycle hardening", "New normative ledger",
   ["LIFECYCLE_ERRORS"], ["WP-6"])
cc(51, M, "transport vs gate matrix filename inconsistent (layout vs #42)",
   ["#42", "#45"], "v0.4 names theorem_transport_matrix.yaml (#45) vs theorem_gate_matrix.yaml (#42)",
   "Two names, one role", "Canonical prereg/theorem_gate_matrix.yaml for gates; theorem_transport_matrix.yaml SUPERSEDED (kept only as historical pointer); provenance matrix keeps transport rationale per object",
   ["prereg/theorem_gate_matrix.yaml"], "clarification", "One name survives",
   ["THEOREM_MAPPING_ERRORS"], ["WP-0"])
cc(52, M, "MST_LIQ_EXPORT.json without schema/verifier (main experiment would trust without rerun)",
   ["#44"], "v0.4 #44 field list, no schema",
   "Trust without verification", "schemas/mst_liq_export.schema.json + import verifier binding version/seal/candidate history/IDs/semantic+legal+parent hashes/DAG/status/proof/Lean/review/bridge/counterexample/fresh-bank/claim",
   ["schemas/mst_liq_export.schema.json"], "reproducibility hardening", "New gate",
   ["SEAL_ERRORS"], ["WP-6"])
cc(53, M, "Successors not required to prove backward embedding (M-chain drawn, never required)",
   ["#43"], "v0.4 #43 7 steps lack embedding theorem",
   "Chain by naming", "Every successor must prove legacy embedding (prior architecture recovered at old parameters) + retain axes + add one justified axis + preserve failures/witnesses",
   ["spec#successor"], "contract completion", "Strengthens #43",
   ["SUCCESSOR_EMBEDDING_ERRORS"], ["WP-6"])
cc(54, M, "'Clone full MST architecture' ambiguous recursively (could clone v0.3, losing rho)",
   ["#43"], "v0.4 #43 wording",
   "Successor could drop axes", "Clone latest sealed architecture retaining accepted axes unless explicitly justified otherwise",
   ["spec#successor"], "clarification", "Disambiguates #43",
   ["SUCCESSOR_EMBEDDING_ERRORS"], ["WP-6"])
# ---- hardening (055-066) ----
cc(55, H, "LIQ0-02 failure handling bundles whole axis (ROT death should not kill FLAT)",
   ["#8"], "Old WP-2 bundled LIQ0-02..10 into one gate",
   "Profile-specific vs axis-wide conflation", "Separate gates: ROT-ineligible on LIQ0-02 falsity; FLAT continues on own obligations; axis dies only on axis-wide obligation failure",
   ["spec#profile-gates", "math/theorems/LIQ0-02.md"], "clarification", "Narrows failure blast radius",
   ["RHO_AXIS_ERRORS"], ["WP-2"])
cc(56, H, "Event naming: ZIG-left/ZIG-right vs single ZIG normalization unmapped",
   ["#3", "#5"], "v0.4 #3 lists ZIG-left/right, #5 uses ZIG",
   "Trace-identity bug surface", "Freeze normalization: trace preserves oriented ZIG-L/R; mu maps both to class ZIG (rho_ZIG); orientation retained in ledger/support records",
   ["spec#event-normalization"], "clarification", "No behavior change",
   ["RHO_AXIS_ERRORS"], ["WP-1", "WP-2"])
cc(57, H, "FLAT undefined on ROOT/no-event (ROT has mu(ROOT)=0; FLAT only for eligible non-ROOT)",
   ["#5"], "v0.4 #5.1 wording",
   "Partial function in total position", "rho_flat(ROOT)=0, rho(any,ROOT)=0, no-event calls T5 zero times; or prove callers exclude ROOT (choose former: total function)",
   ["prereg/liquidity_axis.yaml"], "clarification", "Totalizes definition",
   ["RHO_AXIS_ERRORS"], ["WP-2"])
cc(58, H, "'Known n=28 witness is repaired' invites witness-mutation reading",
   ["#34"], "v0.4 #34 wording",
   "Dangerous verb", "Replace with 'candidate evaluates execSuffices=true on immutable LIQ-REG-001 (hash-bound, never modified)'",
   ["spec#promotion-wording"], "clarification", "Wording fix with teeth",
   ["CANDIDATE_IDENTITY_ERRORS"], ["WP-4"])
cc(59, H, "'Delta minimization' undefined (global vs local minimality)",
   ["#37"], "v0.4 #37 list",
   "Stronger minimality than certified", "Certificate levels: operation-deletion minimal / parameter-family minimal / exhaustive-global minimal; prohibit stronger wording than certificate supports",
   ["spec#minimization"], "contract completion", "New exact levels",
   ["LIFECYCLE_ERRORS"], ["WP-4"])
cc(60, H, "S5/S6 'repair known family' overclaims conjectured DDKK closed form",
   ["#50"], "v0.4 #50 S5/S6 + #11 CONJECTURED_FAMILY",
   "Tested-members vs proved-family", "Read as frozen tested members unless symbolic family theorem closes (new MSTL-FAM theorem with proof)",
   ["spec#success-wording"], "clarification", "Restricts S5/S6 to evidence",
   ["THEOREM_IDENTITY_ERRORS"], ["WP-4"])
cc(61, H, "S10 'smallest preregistered C survives' reads as global minimality proof",
   ["#50"], "v0.4 #50 S10",
   "Ladder rung vs global minimum", "Read as 'smallest tested preregistered C ladder rung with survivor'; no global-minimality claim",
   ["spec#success-wording"], "clarification", "Restricts S10",
   ["THEOREM_IDENTITY_ERRORS"], ["WP-6"])
cc(62, H, "S19 demands 'exact missing resource', forcing stories for bare obstructions",
   ["#50"], "v0.4 #50 S19",
   "Mandatory insight", "Permit 'no justified missing resource identified' as honest S19 answer with preserved obstruction",
   ["spec#success-wording"], "clarification", "Adds honest outcome",
   ["SUCCESSOR_EMBEDDING_ERRORS"], ["WP-6"])
cc(63, H, "'Second already-frozen candidate' should generalize to set exhaustion",
   ["#41"], "v0.4 #41 wording",
   "Two-candidate assumption vs cap 3", "Attempt next frozen candidate in predetermined order until set exhausted",
   ["spec#candidate-order"], "clarification", "Generalizes to cap",
   ["CANDIDATE_IDENTITY_ERRORS"], ["WP-5", "WP-6"])
cc(64, H, "Resource-limit behavior underspecified (no record fields/budgets)",
   ["#49"], "Parent had 11-field record; v0.4 label only",
   "No-claim without provenance", "Exact resource-limit record (attempted/unattempted work, budgets, deterministic policy) required for RESOURCE_LIMIT_NO_CLAIM (and PROMOTED-set variant)",
   ["spec#resource-record"], "reproducibility hardening", "Restores parent practice",
   ["SEAL_ERRORS"], ["WP-4", "WP-5", "WP-6"])
cc(65, H, "Review REJECT/BLOCKED behavior missing (ACCEPT defined only); rejection must not equal refutation; byte-change invalidation",
   ["#22"], "v0.4 #22 ACCEPT-only",
   "Verdict gap", "REJECT=proof package rejected (truth stays UNPROVED, re-review lawful); BLOCKED=truth BLOCKED until clearer; any theorem/proof byte change invalidates prior review binding (hash mismatch fails closed)",
   ["schemas/review.schema.json"], "lifecycle hardening", "Fills verdict gap",
   ["LIFECYCLE_ERRORS"], ["WP-6"])
cc(66, H, "Negative DOC route referenced ('independent negative theorem standard') but unbound",
   ["#49"], "v0.4 #49 phrase",
   "Standard by allusion", "DOC-disproof explicitly OUTSIDE MST-LIQ; transfer-route failure never a DOC claim; terminology import from parent NEG contract by reference only (no evidentiary reuse); MST0-20/21 OUT_OF_SCOPE with reason",
   ["prereg/theorem_gate_matrix.yaml#MST0-20/21"], "contract completion (scopes experiment)", "Removes implied capability",
   ["BRIDGE_SOURCE_ERRORS"], ["WP-6"])

assert len(CC) == 66, len(CC)
assert [c["id"] for c in CC] == [f"CC-{i:03d}" for i in range(1, 67)]

def dump(path, obj):
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(obj, f, sort_keys=False, allow_unicode=True)

dump(ROOT / "planning" / "CONTRACT_CLOSURE_LEDGER.yaml",
     {"experiment": "SPLAY-AM-MST-LIQ-v0.4.1", "v04_spec_sha256": V04_SHA,
      "counts": {"BLOCKER": 28, "MAJOR": 26, "HARDENING": 12, "TOTAL": 66},
      "findings": CC})
print(f"ledger CC_TOTAL={len(CC)}")

# ---- semantic diff ----
def diff_row(ccid, cls, desc):
    return {"cc": ccid, "class": cls, "change": desc}
DIFF = [
    diff_row("CC-001", "contract completion", "Multi-identity parent contract replaces single-SHA pin language"),
    diff_row("CC-002", "contract completion", "Obstruction evidence vs lifecycle seal split; 'sealed' wording narrowed"),
    diff_row("CC-003", "contract completion", "Dual-parent precedence matrix added"),
    diff_row("CC-004", "source-derived correction", "Legal domain weakened to keys(T0) subset [n], absent keys legal (CHANGED theorem domain vs v0.4 text)"),
    diff_row("CC-005", "clarification", "Class-A/Class-B theorem scoping replaces universal legality sentence"),
    diff_row("CC-006", "contract completion", "Absent-access semantics + split multiplicity theorem added"),
    diff_row("CC-007", "source-derived correction", "T5 binds predicate P: T5_{P,1}/T5_{P,rho} (CHANGED operator signature)"),
    diff_row("CC-008", "contract completion", "Verbatim A/B replay equations frozen"),
    diff_row("CC-009", "clarification", "eligibleLatentCount replaces total q in activation formulas"),
    diff_row("CC-010", "contract completion", "Closed predicate family replaces P_inherited phrase"),
    diff_row("CC-011", "contract completion", "Search scope fixed to (P,k,C,rho); template-count objectives removed"),
    diff_row("CC-012", "actual semantic change", "Rho class widened to (rho_ZIG,rho_DOUBLE) in 0..8; v0.4 12 profiles embed"),
    diff_row("CC-013", "clarification", "Discovery ladder vs admissible class separated; r=7 is ladder extension"),
    diff_row("CC-014", "contract completion", "27 exact theorem statement files replace prose targets"),
    diff_row("CC-015", "contract completion", "Full 26-node gate matrix replaces 16-entry minimum"),
    diff_row("CC-016", "contract completion", "MSTL-09 explicit endgame ownership + PA conjunction"),
    diff_row("CC-017", "contract completion", "PA prerequisite conjunction frozen"),
    diff_row("CC-018", "contract completion", "Theorem provenance import rule (identical-bytes-or-new-bytes)"),
    diff_row("CC-019", "contract completion", "Branch-B trigger made operational (dev/fresh rejection)"),
    diff_row("CC-020", "firewall hardening", "Dormant Branch-B pre-reveal freeze; late synthesis forbidden"),
    diff_row("CC-021", "contract completion", "Signed T5_rho accounting + MSTL-12 defined"),
    diff_row("CC-022", "contract completion", "H4L generation parameters made exact (quotas/laws/RNG/seed/dedup/hashes)"),
    diff_row("CC-023", "firewall hardening", "True commitment secrecy replaces public-repo quarantine (CHANGED storage rule)"),
    diff_row("CC-024", "firewall hardening", "7-state H4L automaton with readers/writers/unlock count"),
    diff_row("CC-025", "clarification", "WP-0 contract vs WP-3 implementation freeze ownership split"),
    diff_row("CC-026", "contract completion", "Promotion semantics: evaluate-all-or-domination; PROMOTED_CANDIDATE_SET_REJECTED terminal (CHANGED claim strength)"),
    diff_row("CC-027", "lifecycle hardening", "Dual prove/refute lifecycle with 13 states; REJECT!=REFUTED"),
    diff_row("CC-028", "clarification", "2-mandatory + formal-where-applicable route rule"),
    diff_row("CC-029", "contract completion", "Internal validation spec frozen"),
    diff_row("CC-030", "reproducibility hardening", "Adversarial budgets frozen per engine"),
    diff_row("CC-031", "firewall hardening", "Clean-room contract+bytes frozen pre-reveal"),
    diff_row("CC-032", "contract completion", "210+ parent controls dispositioned item-by-item"),
    diff_row("CC-033", "contract completion", "MSTL as overlay; inherited gates discharged-by-transport"),
    diff_row("CC-034", "contract completion", "H1/H2R/n8/H3T LIQ dispositions with unlock counts"),
    diff_row("CC-035", "contract completion", "OOD benchmark layer separated from fresh H4L"),
    diff_row("CC-036", "contract completion", "Matched FLAT(1) baseline + attribution labels"),
    diff_row("CC-037", "contract completion", "29-field candidate identity replaces 'at least' list"),
    diff_row("CC-038", "clarification", "rule_family_id vs calculus_id split"),
    diff_row("CC-039", "contract completion", "A(n)=0 only live target; nonzero BLOCKED (CHANGED permission)"),
    diff_row("CC-040", "contract completion", "Bridge source pin-or-BLOCKED rule"),
    diff_row("CC-041", "reproducibility hardening", "Environment lock (Python 3.13.7, Lean v4.21.0, solvers, RNG, zstd)"),
    diff_row("CC-042", "reproducibility hardening", "Parent exactness/determinism policy restored verbatim"),
    diff_row("CC-043", "reproducibility hardening", "33-field logging superset (CHANGED field list: additions only)"),
    diff_row("CC-044", "reproducibility hardening", "Clean-tree rule for authoritative runs"),
    diff_row("CC-045", "reproducibility hardening", "Deterministic large-artifact policy"),
    diff_row("CC-046", "reproducibility hardening", "Exact seal mechanics"),
    diff_row("CC-047", "contract completion", "Phase-conditional reproduction matrix"),
    diff_row("CC-048", "contract completion", "Clone/bootstrap transaction + tree disposition"),
    diff_row("CC-049", "contract completion", "WorkPlan/Path governance made normative"),
    diff_row("CC-050", "lifecycle hardening", "Canonical status ledger + review schema mandated"),
    diff_row("CC-051", "clarification", "theorem_gate_matrix.yaml canonical; transport name superseded"),
    diff_row("CC-052", "reproducibility hardening", "Export schema + verifier mandated"),
    diff_row("CC-053", "contract completion", "Successor backward-embedding theorem required"),
    diff_row("CC-054", "clarification", "Clone-latest rule for successors"),
    diff_row("CC-055", "clarification", "Profile-specific vs axis-wide failure separation"),
    diff_row("CC-056", "clarification", "ZIG normalization map frozen"),
    diff_row("CC-057", "clarification", "rho totalized at ROOT/no-event (=0)"),
    diff_row("CC-058", "clarification", "'Satisfies immutable regression' wording"),
    diff_row("CC-059", "contract completion", "Three minimization certificate levels"),
    diff_row("CC-060", "clarification", "S5/S6 restricted to tested members"),
    diff_row("CC-061", "clarification", "S10 restricted to tested ladder rung"),
    diff_row("CC-062", "clarification", "S19 permits no-justified-resource answer"),
    diff_row("CC-063", "clarification", "Next-candidate-until-exhausted ordering"),
    diff_row("CC-064", "reproducibility hardening", "Resource-limit record fields + budgets"),
    diff_row("CC-065", "lifecycle hardening", "REJECT/BLOCKED verdicts + byte-change invalidation"),
    diff_row("CC-066", "contract completion", "DOC-disproof placed outside MST-LIQ"),
]
dump(ROOT / "planning" / "V04_TO_V041_SEMANTIC_DIFF.yaml",
     {"v04_spec_sha256": V04_SHA, "actual_semantic_changes": ["CC-004", "CC-007", "CC-012", "CC-023", "CC-026", "CC-039", "CC-043"],
      "changes": DIFF})
print(f"diff rows={len(DIFF)}")

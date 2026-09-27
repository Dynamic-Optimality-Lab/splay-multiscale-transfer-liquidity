"""Build v0.4.1 contract-closure artifacts (deterministic).

Emits: planning/CONTRACT_CLOSURE_LEDGER.yaml, planning/V04_TO_V041_SEMANTIC_DIFF.yaml,
planning/PARENT_PROVENANCE_MATRIX.yaml, planning/PARENT_CONTROL_DISPOSITION.yaml,
planning/PARENT_TREE_DISPOSITION.yaml, amendments/...CONTRACT-CLOSURE.md,
prereg/*.yaml (predicate_family, liquidity_axis, liquidity_search_space, h4l_holdout,
theorem_gate_matrix, environment_lock, threat/stop matrices, parent_contract),
math/theorems/*.md, schemas/*.schema.json.
"""
import hashlib
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
ARCH_NAV = "895889169772087e391e84c33228648c84684e1e"
ARCH_CLOSURE = "9859e654b76ba92c1d0e0809f62a7ffe1cac3b98"
ARCH_SEAL = "3062c0180157399cc0e877c0d238edc7f3aff7c0"
OB_EVID = "19ef254dfc48c7b909c646f959e2d7364865b777"
V04_SHA = "0E2C166E1B721DFC8A7E5327ED33AF29A1B4AC539CB71849F3C7231B32A8055B"

CC = []
def cc(n, sev, find, secs, ev, cause, repair, arts, sem, compat, tests, cons):
    CC.append({"id": f"CC-{n:03d}", "severity": sev, "original_finding": find,
               "affected_spec_sections": secs, "source_evidence": ev, "root_cause": cause,
               "normative_repair": repair, "new_or_modified_artifacts": arts,
               "semantic_change": sem, "backward_compatibility_effect": compat,
               "tests_or_checker_rules": tests, "downstream_consumers": cons,
               "status": "CLOSED", "closure_evidence": f"v0.4.1 bytes + check_contract_closure.py rule for CC-{n:03d}"})

B = "BLOCKER"; M = "MAJOR"; H = "HARDENING"
# ---- parent identity / precedence (001-003) ----
cc(1, B, "Architecture-parent identity not closed: nav vs closure vs seal commit ambiguous",
   ["PHASE00"], f"GitHub API: HEAD={ARCH_NAV}, closure msg names {ARCH_CLOSURE[:7]}, evidence head {ARCH_SEAL[:7]}; spec navigation HEAD==remote HEAD verified",
   "One SHA cannot serve navigation, closure and seal roles", "Multi-identity parent contract: architecture_navigation_commit, architecture_closure_commit, architecture_seal_commit + per-artifact content SHAs (FINAL_RESULT/manifest/archive/WorkPlan/Path/ledger/theorem-status/candidate-set/spec); WP-0 re-verifies content SHAs against pinned commits",
   ["prereg/parent_contract.yaml", "IMPLEMENTATION_SPEC_...v0.4.1.md#parent-contract"], "contract completion (no scientific change)", "v0.4 pins single SHA; v0.4.1 names roles, old SHA retained as navigation",
   ["PARENT_IDENTITY_ERRORS"], ["WP-0"])
cc(2, B, "Obstruction parent lacks lifecycle refutation closure (Lean witness + G5 pending)",
   ["PHASE00"], f"DECIDE HEAD {OB_EVID[:7]} msg certifies n28 witness + triple replay; Path records formal witness + G5 validation pending",
   "Spec wording demands sealed/refutation-closure commit that does not exist", "Split fields: obstruction_evidence_commit + mathematical_status=CONFIRMED + formal_certificate_status=PENDING + human_validation_status=PENDING + lifecycle_seal=OPEN; forbid calling it sealed; REFUTED lifecycle only after formal+human close",
   ["prereg/parent_contract.yaml"], "contract completion", "Narrows v0.4 wording; witness bytes unchanged",
   ["PARENT_IDENTITY_ERRORS", "LIFECYCLE_ERRORS"], ["WP-0", "WP-1"])
cc(3, B, "No dual-parent precedence rule; arch sealed nodes unproved while Dynamic later REVIEWED 08U/09/11/13/22",
   ["PHASE00", "transport"], "Arch THEOREM_STATUS 9/5/3/3/6 vs DECIDE later REVIEWED set (Path R1-030 ACCEPT x5)",
   "Two parents, no per-object winner", "PARENT_PROVENANCE_MATRIX per object (definition/statement/proof/review/evidence source + rule): architecture owns definitions; later parent supplies proof/refutation evidence only under identical bytes + transport theorem, else new MSTL bytes",
   ["planning/PARENT_PROVENANCE_MATRIX.yaml"], "contract completion", "v0.4 silent-copy risk removed; no status values altered",
   ["PARENT_PRECEDENCE_ERRORS"], ["WP-0", "WP-6"])
# ---- legal domain (004-006) ----
cc(4, B, "Legal domain conflicts: v0.4 expects keys(T0)==[n]; obstruction legal_domain uses keys(T0) subset [n], absent access keys allowed",
   ["#10"], "Obstruction inherited/splay.py: descend->None for absent keys; audit states subset law; v0.4 #10 expects equality+presence",
   "Convenience equality contradicts source-derived weaker domain", "Adopt source-derived weaker domain: keys(T0) subset [n], valid BST, modes KEEP/DELETE, access keys in [n] (presence NOT required), A/B start equal T0, exact replay semantics; equality only as explicitly labeled proof-restricted subdomain (new ID, never silent)",
   ["IMPLEMENTATION_SPEC_...v0.4.1.md#legal-domain", "prereg predicate/legal hashes"], "source-derived correction (theorem domain widens vs v0.4 text)", "v0.4-era proofs under equality must be re-scoped, not auto-transported",
   ["LEGAL_DOMAIN_ERRORS"], ["WP-1", "WP-2", "WP-6"])
cc(5, B, "'All universal theorems use LegalPairInstance' over-scopes: ledger algebra (discharge, preservation, SPENT monotonicity, MST0-15 parts) should stay total",
   ["#15", "#22"], "Obstruction audit preserved MST0-15 as total; v0.4 #15 sentence universal",
   "One guard applied to unrelated algebra", "Two theorem classes: A tree/history theorems require LegalPairInstance; B pure ledger algebra total over arbitrary ledgers/needs, MUST NOT add tree-legality hypotheses",
   ["math/theorems/*.md (per-theorem Domain:)", "theorem_gate_matrix.yaml"], "clarification", "None adverse; class-B statements keep full strength",
   ["LEGAL_DOMAIN_ERRORS", "THEOREM_IDENTITY_ERRORS"], ["WP-2", "WP-6"])
cc(6, B, "Weaker domain vs multiplicity theorem: present-key statement incompatible with absent-key legal traces (nonzero depth+1 cost, empty rotation trace)",
   ["#8"], "Obstruction splay.py: splay_cost defined for absent keys; splay_trace returns (t,[]) — verified bytes above",
   "Present-key identity applied to empty traces", "Split theorem: present-key accesses sum mu(ev)=depth; absent-key accesses: trace empty, tree unchanged, cost=depth_to_leaf+1, zero activation opportunities; freeze both statements + absent-access replay semantics (no T7/T5, no discharge change)",
   ["math/theorems/LIQ0-02.md", "spec#absent-access-semantics"], "contract completion", "v0.4 LIQ0-02 statement superseded by two precise statements",
   ["LEGAL_DOMAIN_ERRORS", "RHO_AXIS_ERRORS"], ["WP-2"])
# ---- T5 semantics + replay (007-009) ----
cc(7, B, "T5_1(L,m) undefined for candidate family: activation depends on frozen predicate P (P_all vs P_keep vs case-restricted)",
   ["#4"], "Obstruction mstc0002.py t5activate(engine,mode) with p_all(mode); parent grammar T5 condition 'declared_B_access_path_condition'",
   "Predicate-free operator cannot serve a predicate-indexed family", "Define T5_{P,1}(L,m,ev): P bound per predicate definition (mode + normalized event class only); P_all fires always, P_keep fires on KEEP, case-restricted per allowlist; T5_{P,rho} bounded iteration of that exact primitive",
   ["spec#T5-def", "prereg/predicate_family_v0.4.1.yaml"], "source-derived correction", "Old FLAT(1)/P_all behavior provably unchanged (LIQ0-01)",
   ["T5_SEMANTIC_ERRORS"], ["WP-1", "WP-2"])
cc(8, B, "T5_rho never inserted into A/B replay: ordering T7->T5rho / T5rho / discharge-after-B-trace not frozen",
   ["#4"], "Obstruction mstc0002.py replay_step=t5activate(t7inject(...)) A-side; replay_access_B per-ev t5activate then discharge after full B trace; DELETE A-only",
   "Defined operator, undefined composition", "Freeze verbatim replay equations: A-side per StepEv T7->T5_{P,rho}; B-side per StepEv T5_{P,rho} (predicate-evaluated); KEEP discharge unchanged T6 after complete B trace; DELETE no B replay/discharge; ordering hash-bound in candidate identity",
   ["spec#replay-equations", "candidate identity fields"], "contract completion", "Matches inherited execution at FLAT(1) by construction",
   ["REPLAY_ORDER_ERRORS"], ["WP-1", "WP-2"])
cc(9, B, "Activation-count identity uses total LATENT q, but #4 says eligible LATENT",
   ["#4", "#14"], "mstc0002 activate_first scans ledger order for first LATENT; support/predicate may restrict eligibility",
   "Total vs eligible conflation", "Formulas use eligibleLatentCount(L,P,m,ev); define eligibility (LATENT + support-allowed + predicate-fires + ledger-order position); ACTIVE'=ACTIVE+min(q_elig,b), LATENT'=LATENT-min(q_elig,b)",
   ["spec#eligibility", "math/theorems/LIQ0-*.md"], "clarification", "At P_all/all-eligible reduces to v0.4 formula",
   ["T5_SEMANTIC_ERRORS"], ["WP-2"])
# ---- predicate/grammar closure (010-011) ----
cc(10, B, "P_inherited not closed: parent grammar defines T5 constraints, not a predicate menu",
   ["#15"], "Fetched transfer_grammar_v0.3.yaml: no predicate enumeration (verified)",
   "Symbolic phrase where a finite set is required", "prereg/predicate_family_v0.4.1.yaml enumerates P_all, P_keep (exact mode tables) + case-restricted schema (normalized event-class allowlist) with canonical enumeration frozen at WP-0; no post-freeze predicates",
   ["prereg/predicate_family_v0.4.1.yaml"], "contract completion", "Supersets v0.4 'at minimum' list with exact bytes",
   ["PREDICATE_GRAMMAR_ERRORS"], ["WP-3", "WP-4"])
cc(11, B, "Unclear whether full T1-T10 grammar reruns or only (P,k,C,rho) varies; objective mentions rule-template counts",
   ["#15", "#16"], "Parent grammar has T1-T10 + supports/scales + signed branch; v0.4 grid varies 4 vars but objective counts templates",
   "Two experiments described at once", "Choose (B): non-liquidity mechanics held fixed at inherited Branch-A architecture; synthesis searches only enumerated (P,k,C,rho); drop rule-template/support-complexity objective terms; keep predicate-simplicity + profile-simplicity ordering",
   ["spec#search-space", "prereg/liquidity_search_space.yaml"], "contract completion (narrows v0.4 scope)", "Full-grammar search explicitly out of scope (successor material)",
   ["PREDICATE_GRAMMAR_ERRORS"], ["WP-4"])
# ---- rho axis (012-013) ----
cc(12, B, "Rho axis underparameterized: only (r,r),(r,2r); (1,3) is same axis but inexpressible",
   ["#5"], "Axis claim is event-class bandwidth; v0.4 allows 2 rays only",
   "Axis confused with subfamilies", "Mathematical class rho=(rho_ZIG,rho_DOUBLE), each in 0..8, symmetric across LL/RR/LR/RL; FLAT(r)=(r,r), ROT(r)=(r,2r) named subfamilies; ROOT/no-event rho=0",
   ["prereg/liquidity_axis.yaml"], "actual semantic change (class widens; v0.4 profiles embed exactly)", "v0.4 12 profiles embed 1-1; old results comparable",
   ["RHO_AXIS_ERRORS"], ["WP-2", "WP-4"])
cc(13, B, "r<=6 vs successor rule: needing r=7 is not a new axis but #5 demands successor for larger families",
   ["#5", "#43"], "v0.4 #5 vs #43 text (both cited in finding)",
   "Ladder confused with axis", "Separate discovery ladder (frozen 12: FLAT/ROT r=1..6) from admissible class (0..8^2); r=7 uses versioned ladder extension; successor only for new degrees of freedom/dependencies outside rho-profile semantics",
   ["prereg/liquidity_axis.yaml#ladder"], "clarification", "Strictly more permissive than v0.4 text; frozen ladder unchanged",
   ["RHO_AXIS_ERRORS"], ["WP-4", "WP-6"])
# ---- theorems (014-018) ----
cc(14, B, "Theorem targets lack exact bytes: LIQ0 names, MSTL-15 'such as', PA target form, telescope/bridge prose",
   ["#14", "#28", "#29"], "v0.4 text (finding cites sections)",
   "Names where quantifiers/domains/negations are required", "Exact versioned statement files math/theorems/{LIQ0-01..10,MSTL-08U,09,10,11,12,13,14,15,16,17,18,19,22,23,24,25,26}.md with quantifiers/domain/constants/assumptions/conclusion/candidate-dependence/negation/first-consumer before synthesis",
   ["math/theorems/*.md (27 files)"], "contract completion", "Supersede prose-only targets",
   ["THEOREM_IDENTITY_ERRORS"], ["WP-2", "WP-6"])
cc(15, B, "26-node ledger not fully mapped: #42 maps 16, missing MST0-01..07,12,20,21",
   ["#42"], "Arch THEOREM_STATUS has 26 rows; v0.4 maps 16",
   "'At minimum' left as the whole contract", "theorem_gate_matrix.yaml dispositions all 26: IDENTICAL_TRANSPORT / REPROVE_UNDER_RHO / GENERALIZED_NEW_BYTES / DOWNSTREAM_REBOUND / CONDITIONAL / NOT_APPLICABLE + justification; MSTL-12 added (signed bound); MST0-20/21 OUT_OF_SCOPE (DOC-disproof outside LIQ, CC-066)",
   ["prereg/theorem_gate_matrix.yaml"], "contract completion", "16 mapped entries preserved, 10 added",
   ["THEOREM_MAPPING_ERRORS"], ["WP-6"])
cc(16, B, "MST0-09 mapped but missing from ladder/war (MSTL-GATE-13 mentions locality/preservation only); Dynamic gate needs 08U/09/11/13/14/15/22",
   ["#41"], "DECIDE gate text in finding; v0.4 #41 war list",
   "Mapped obligation with no owner in the endgame", "MSTL-09 explicit identity/status/owner (WP-2 dev, WP-6 proof) + present in PA prerequisite conjunction + gate MSTL-GATE-13 checks 08U/09/11/13",
   ["prereg/theorem_gate_matrix.yaml", "math/theorems/MSTL-09.md"], "contract completion", "Adds missing endgame check",
   ["THEOREM_MAPPING_ERRORS", "FIRST_CONSUMER_ERRORS"], ["WP-6"])
cc(17, B, "'After required upstream REVIEWED' not enumerated for Pair Access",
   ["#29"], "v0.4 #29 prose",
   "Conjunction left implicit", "Freeze PA prerequisites: MSTL-08U/09/11/13/14/15/22 REVIEWED + LIQ0-01/02/04/05/06/09/10 at required statuses; machine-checked before MSTL-17 PROVE track",
   ["spec#PA-prerequisites"], "contract completion", "Strictly explicit version of v0.4 intent",
   ["FIRST_CONSUMER_ERRORS"], ["WP-6"])
cc(18, B, "Theorem provenance ambiguous: MST0-08U/09/11/13/22 more mature in Dynamic than arch; 'parent proof' undefined",
   ["#13"], "DECIDE ACCEPT x5 vs arch statuses",
   "Two proof sources, no import rule", "Provenance matrix rule: transport later proof only under byte-identical statements + rho-invariance transport theorem; else reprove or mint new MSTL bytes; inherited ACCEPT valid only for exact reviewed bytes",
   ["planning/PARENT_PROVENANCE_MATRIX.yaml"], "contract completion", "No statuses copied",
   ["PARENT_PRECEDENCE_ERRORS"], ["WP-6"])
# ---- Branch B (019-021) ----
cc(19, B, "Branch-B activation condition not operational (dev vs fresh vs theorem failure?)",
   ["#31"], "v0.4 #31 prose",
   "Exact-failure undefined", "Branch B activates iff Branch-A PROMOTED set rejected at development (no eligible survivor) OR fresh (PROMOTED_CANDIDATE_SET_REJECTED); late theorem failure does NOT open new synthesis (CC-020)",
   ["spec#branch-B-activation"], "contract completion", "Narrows v0.4 trigger prose",
   ["BRANCH_B_ERRORS"], ["WP-4", "WP-5"])
cc(20, B, "Late Branch-A theorem failure makes Branch B post-holdout adaptation (PHASE11 passed, H4L revealed)",
   ["#31", "#18"], "v0.4 phase/reveal ordering",
   "Freshness architecture violated by late synthesis", "All usable Branch-B identities/grammar frozen dormant pre-reveal; post-reveal only already-frozen Branch-B set may run on H4L; otherwise successor + new bank",
   ["spec#branch-B-freeze", "prereg predicate/grammar"], "firewall hardening", "Forbids v0.4-permitted late adaptation",
   ["BRANCH_B_ERRORS", "HOLDOUT_FIREWALL_ERRORS"], ["WP-3", "WP-5"])
cc(21, B, "Signed Branch-B rho semantics unbound (unsigned LATENT/ACTIVE/SPENT vs signed masses)",
   ["#31"], "Parent grammar T9 + lower-bound route; v0.4 'obligations remain mandatory' only",
   "Available branch with undefined accounting", "Define signed T5_{P,rho}: activation preserves sign-mass, energy E_signed=sum(m) with proved lower bound MSTL-12; candidate identity binds signed energy/lower-bound definition; unsigned theorems do not transfer silently",
   ["spec#signed-semantics", "math/theorems/MSTL-12.md"], "contract completion", "Branch B closed only when these bytes exist",
   ["BRANCH_B_ERRORS"], ["WP-2", "WP-6"])
# ---- H4L firewall (022-025) ----
cc(22, B, "H4L generator underspecified ('Recommended' sizes/strata; missing quotas/laws/RNG/seeds/dedup/serialization/hashes)",
   ["#18"], "v0.4 #18 'Recommended' wording",
   "'Recommended' cannot produce reproducible fresh bank", "Freeze exact: sizes [18,26,34,46,58,74,98] x10k=70k; per-stratum quotas (equal split 833 or 834 with deterministic remainder schedule); history-length law; tree-shape law; SHA-256 counter DRBG; secret seed protocol; dedup-reject-resample; weaker-domain legality filter; canonical JSON serialization; sorted order; .json.zst shards; per-shard + logical-stream SHA; commitment construction",
   ["prereg/h4l_holdout.yaml"], "contract completion", "Recommendations promoted to normative values",
   ["HOLDOUT_FIREWALL_ERRORS"], ["WP-3"])
cc(23, B, "Public Git is not quarantine: committed bytes/seeds readable by discovery",
   ["#18"], "Repo is public GitHub (verified)",
   "Storage confused with secrecy", "True commitment: pre-reveal public = commitment hash + non-sensitive metadata ONLY; seed + bank bytes held outside public/discovery repo (operator-held secret); reveal publishes + verifies; no .gitignore/LFS/encrypted-in-repo fakery; without inaccessible storage H4L BLOCKED",
   ["spec#H4L-secrecy", "prereg/h4l_holdout.yaml"], "firewall hardening (forbids v0.4 plan of committing bank bytes)", "Supersedes old WorkPlan quarantine-by-commit",
   ["HOLDOUT_FIREWALL_ERRORS"], ["WP-3", "WP-5"])
cc(24, B, "No exact H4L firewall state machine (states/transitions/readers/unlock count)",
   ["#18"], "v0.4 quarantine prose",
   "Prose where an automaton is required", "States EMPTY->GENERATOR_FROZEN->BANK_GENERATED_SECRET->COMMITMENT_PUBLISHED->CANDIDATE_SET_FROZEN->REVEALED_ONCE->CONSUMED; legal readers/writers per state; unlock count immutable <=1; violations fail closed with STOP IDs",
   ["spec#H4L-firewall", "firewall.py contract"], "firewall hardening", "Compatible with v0.4 intent, exact",
   ["HOLDOUT_FIREWALL_ERRORS"], ["WP-3", "WP-5"])
cc(25, B, "WP-0 vs WP-3 disagree on H4L generator freeze ownership",
   ["#32"], "Old WorkPlan WP-0 vs WP-3 text",
   "Two owners for one freeze", "WP-0 freezes GENERATOR CONTRACT (normative semantics); WP-3 implements code, certifies hash-equivalent/compliant implementation, then generates; no normative semantics invented in WP-3",
   ["spec#freeze-ownership"], "clarification", "Resolves plan contradiction",
   ["HOLDOUT_FIREWALL_ERRORS"], ["WP-0", "WP-3"])
# ---- promotion/refutation (026-028) ----
cc(26, B, "Top-3 promotion makes LIQUIDITY_CALCULUS_REJECTED too strong (refutes 3, not grammar)",
   ["#32", "#49"], "v0.4 cap <=3 + terminal wording",
   "Claim exceeds elimination", "Evaluate every eligible survivor; <=3 cap allowed only with domination/equivalence proof; otherwise terminal PROMOTED_CANDIDATE_SET_REJECTED; LIQUIDITY_CALCULUS_REJECTED only after full declared space eliminated; 'second candidate' generalized to next-in-order-until-exhausted",
   ["spec#promotion", "terminals"], "contract completion (weakens claim to match evidence)", "Honest renaming; old label retained only for full elimination",
   ["CANDIDATE_IDENTITY_ERRORS"], ["WP-4", "WP-5"])
cc(27, B, "Refutation lifecycle missing: only UNPROVED->PROVED->REVIEWED yet terminals include REFUTED",
   ["#22", "#49"], "v0.4 #22 + #49 text",
   "Terminal states unreachable by defined transitions", "Dual prove/refute lifecycle states (UNPROVED/PROVE_RUNNING/PROVED_PENDING_REVIEW/REVIEWED/NO_WITNESS/WITNESS_FOUND/MATHEMATICAL_COUNTEREXAMPLE_CONFIRMED/FORMAL_REFUTATION_PENDING/HUMAN_VALIDATION_PENDING/REFUTED/BLOCKED/NOT_REACHED/NOT_APPLICABLE); REJECT!=REFUTED; REFUTED needs exact negation witness + candidate hash + 3-route replay (primary/independent/formal-or-MATH_CONFIRMED) + human validation",
   ["spec#lifecycle", "schemas/theorem_status.schema.json"], "lifecycle hardening", "Adds paths; existing path preserved",
   ["LIFECYCLE_ERRORS"], ["WP-6"])
cc(28, B, "'Three execution routes' vs 'Lean where feasible' contradictory",
   ["#21"], "v0.4 #21 text",
   "Optional third route breaks 'at least three'", "Two routes mandatory (primary + independently structured); formal Lean mandatory where technically applicable, else MATHEMATICAL_COUNTEREXAMPLE_CONFIRMED preserved without promotion to REFUTED; applicability decided per-theorem pre-attack with recorded reason",
   ["spec#execution-routes"], "clarification", "Resolves contradiction without weakening evidence bar",
   ["LIFECYCLE_ERRORS"], ["WP-5", "WP-6"])

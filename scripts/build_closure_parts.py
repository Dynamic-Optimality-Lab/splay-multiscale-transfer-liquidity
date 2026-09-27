"""Emit v0.4.1 provenance/disposition/prereg/theorem/schema artifacts."""
from pathlib import Path
import yaml
import json
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_closure import ROOT, ARCH_NAV, ARCH_CLOSURE, ARCH_SEAL, OB_EVID, V04_SHA

def dump(path, obj):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        yaml.safe_dump(obj, f, sort_keys=False, allow_unicode=True)

def write(path, text):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")

# ---------- PARENT_PROVENANCE_MATRIX ----------
objs = [
    ("splay_semantics", "arch", "arch", "arch(reviewed MST0-02*)", "arch", "arch", "ARCH wins; later proofs must match bytes"),
    ("pair_access_semantics", "arch", "arch", "arch", "arch", "arch", "ARCH wins (KEEP/DELETE/cost); Dynamic evidence read-only"),
    ("legal_domain", "obstruction(weaker, source-derived)", "v041", "v041", "v041", "v041", "OBSTRUCTION source wins over v0.4 text (CC-004); equality only as labeled subdomain"),
    ("stepev_representation", "obstruction(splay.py: (case,lo,hi); single ZIG)", "arch", "arch", "arch", "arch", "OBSTRUCTION executable wins for trace bytes; arch ontology for record fields; normalization map v0.4.1"),
    ("T7", "arch", "arch", "arch", "arch", "arch", "ARCH wins unchanged"),
    ("T5", "arch+obstruction(mstc0002.py)", "v041(T5_{P,rho})", "v041", "v041", "v041", "v0.4.1 generalization; legacy embedding proves old instance preserved"),
    ("T6", "arch+obstruction(discharge fold)", "arch", "arch", "arch", "arch", "ARCH wins unchanged"),
    ("energy", "arch(E=#L+#A)+parent signed route", "v041(unsigned+signed/MSTL-12)", "v041", "v041", "v041", "Unsigned ARCH wins for Branch A; signed defined new with lower-bound obligation"),
    ("support", "arch(ontology allowed/forbidden)", "arch", "arch", "arch", "arch", "ARCH wins"),
    ("provenance", "arch(alphabet)", "arch", "arch", "arch", "arch", "ARCH wins"),
    ("candidate_identity", "v041(29 fields)", "v041", "v041", "v041", "v041", "v0.4.1 supersedes v0.4 'at least' list"),
    ("theorem_bytes", "per-node rule below", "per-node", "per-node", "per-node", "per-node", "Identical bytes: transport w/ invariance lemma; else new MSTL bytes; ACCEPT valid only for reviewed bytes"),
    ("theorem_status", "none(auto)", "v041 ledger", "human per v041", "v041 ledger", "v041", "No status copied; all start UNPROVED in LIQ ledger"),
    ("holdout_state", "arch(H1/H2R/n8/H3T counts)", "v041(H4L new)", "v041", "v041", "v041", "Legacy counts preserved verbatim; H4L new under commitment protocol"),
    ("bridge_sources", "obstruction(bridge_sources/: L3 present, L2 absent)", "v041 manifest", "n/a(BLOCKED)", "n/a", "obstruction", "OBSTRUCTION source record wins; L2-absent => MSTL-19 BLOCKED_BY_SOURCE"),
]
dump("planning/PARENT_PROVENANCE_MATRIX.yaml", {"version": "v0.4.1",
    "arch_commits": {"navigation": ARCH_NAV, "closure": ARCH_CLOSURE, "seal": ARCH_SEAL},
    "obstruction_evidence_commit": OB_EVID, "obstruction_lifecycle_seal": "OPEN",
    "objects": [{"object": o[0], "definition_source": o[1], "statement_source": o[2],
                 "proof_source": o[3], "review_source": o[4], "evidence_source": o[5],
                 "precedence_rule": o[6]} for o in objs]})
print("provenance ok")

# ---------- PARENT_CONTROL_DISPOSITION (programmatic full enumeration) ----------
disps = []
for n in range(1, 91):
    i = f"T{n:02d}"
    if n in (17, 40, 41, 53, 59, 62):
        d = ("INHERITED_MODIFIED", "Liquidity/activation analogue added in LIQ-T/threat matrix; parent control retained for base semantics")
    elif n in (20, 21, 34, 35, 48):
        d = ("NOT_APPLICABLE", "Signed-branch/negative-family machinery out of LIQ scope or Branch-B-dormant; reason recorded")
    else:
        d = ("INHERITED_UNCHANGED", "Applies as written; read-only parent evidence")
    disps.append({"id": i, "disposition": d[0], "reason": d[1]})
for n in range(1, 51):
    i = f"STOP-{n:02d}"
    if n in (5, 20, 21, 30, 31, 32):
        d = ("INHERITED_MODIFIED", "Extended by LIQ-STOP firewall/lifecycle analogues; parent stop still armed for base semantics")
    elif n in (34, 35):
        d = ("NOT_APPLICABLE", "Transfer-residual-as-Splay-cost confusion out of LIQ scope (no Splay-cost theorems here)")
    else:
        d = ("INHERITED_UNCHANGED", "Applies as written")
    disps.append({"id": i, "disposition": d[0], "reason": d[1]})
for n in range(1, 71):
    i = f"INV-{n:03d}"
    disps.append({"id": i, "disposition": "INHERITED_UNCHANGED", "reason": "Structural invariant retained; liquidity layer adds INV set in v0.4.1 spec"})
for t in ["TR-*", "HLD-*", "LED-*", "ROT-*", "CYC-*", "L6-*", "PR-*", "SEAL-*", "NEG-*"]:
    disps.append({"id": t, "disposition": "INHERITED_UNCHANGED", "reason": "Named family retained where in scope; LIQ adds TEST-* families"})
for i in ["MST-GATE-0..21"]:
    disps.append({"id": i, "disposition": "INHERITED_MODIFIED", "reason": "MSTL overlay; inherited gates discharged-by-transport per gate matrix"})
for i, s in [("H1", "HISTORICAL_UNUSED EMPTY"), ("H2R", "HISTORICAL_UNUSED COMMITTED/0"),
             ("H3T", "HISTORICAL UNLOCKED_ONCE"), ("n8", "CONTAMINATED_CANARY")]:
    disps.append({"id": i, "disposition": "NOT_APPLICABLE", "reason": f"LIQ disposition: {s}; counts preserved, never reused"})
dump("planning/PARENT_CONTROL_DISPOSITION.yaml", {"version": "v0.4.1", "items": disps})
print(f"controls={len(disps)}")

# ---------- PARENT_TREE_DISPOSITION (from verified listings) ----------
arch_root = ["IMPLEMENTATION_SPEC_v0.3.md", "WorkPlan.md", "Path.md", "README.md", "CHANGELOG.md",
    "CITATIONS.md", "TRANSFER_CALCULUS_LEDGER.md", "THEOREM_STATUS_REPORT.md", "KEEP_CYCLE_ATLAS.md",
    "L6_PAIR_ACCESS_TRANSLATION_REPORT.md", "MULTISCALE_TRANSFER_REPORT.md", "REPRODUCIBILITY.md",
    "AI_USE.md", "LICENSE", "pyproject.toml", "requirements-lock.txt", "SPLAY_AM_MST_IMPLEMENTATION_SPEC_v0.3.1_PIN.md"]
arch_dirs = ["artifacts/v03", "external", "math", "parent", "prereg", "python", "schemas", "scripts", "tests"]
ob_root = ["IMPLEMENTATION_SPEC_v0.4.md", "WorkPlan.md", "Path.md", "README.md", "CHANGELOG.md", "CITATIONS.md",
    "AI_USE.md", "LICENSE", "pyproject.toml", "requirements-lock.txt", "lean-toolchain", "lakefile.lean",
    "lake-manifest.json"] + [f"SPLAY_AM_DECIDE_IMPLEMENTATION_SPEC_v0.4.{k}_AMENDMENT.md" for k in range(1, 9)]
tree = [{"path": f"arch:{p}", "class": "IMPORTED_UNCHANGED" if p in ("IMPLEMENTATION_SPEC_v0.3.md", "WorkPlan.md", "Path.md", "TRANSFER_CALCULUS_LEDGER.md", "THEOREM_STATUS_REPORT.md", "SPLAY_AM_MST_IMPLEMENTATION_SPEC_v0.3.1_PIN.md") else "EXPLICITLY_NOT_IMPORTED_WITH_REASON", "reason": "read-only evidence" if p in ("IMPLEMENTATION_SPEC_v0.3.md", "WorkPlan.md", "Path.md", "TRANSFER_CALCULUS_LEDGER.md", "THEOREM_STATUS_REPORT.md", "SPLAY_AM_MST_IMPLEMENTATION_SPEC_v0.3.1_PIN.md") else "not needed as LIQ evidence; full-tree manifest at WP-0 extends this table"} for p in arch_root]
tree += [{"path": f"arch:{d}/", "class": "EXPLICITLY_NOT_IMPORTED_WITH_REASON", "reason": "directory; WP-0 full manifest classifies every file"} for d in arch_dirs]
tree += [{"path": f"obstruction:{p}", "class": "IMPORTED_UNCHANGED" if p in ("IMPLEMENTATION_SPEC_v0.4.md", "WorkPlan.md", "Path.md") + tuple(f"SPLAY_AM_DECIDE_IMPLEMENTATION_SPEC_v0.4.{k}_AMENDMENT.md" for k in range(1, 9)) else "EXPLICITLY_NOT_IMPORTED_WITH_REASON", "reason": "evidence/spec reference" if "AMENDMENT" in p or p in ("IMPLEMENTATION_SPEC_v0.4.md", "WorkPlan.md", "Path.md") else "not needed; WP-0 extends"} for p in ob_root]
tree.append({"path": "obstruction:python/inherited/mstc0002.py", "class": "IMPORTED_UNCHANGED", "reason": "exact MSTC-0002 executable semantics (blob 2bbecbc)"})
tree.append({"path": "obstruction:python/inherited/splay.py", "class": "IMPORTED_UNCHANGED", "reason": "exact Splay/StepEv semantics incl. absent-key empty trace (blob b8f3542)"})
tree.append({"path": "obstruction:bridge_sources/", "class": "IMPORTED_UNCHANGED", "reason": "L3 present / L2 absent record vindicates MSTL-19 BLOCKED_BY_SOURCE"})
dump("planning/PARENT_TREE_DISPOSITION.yaml", {"version": "v0.4.1",
    "arch_commits": {"navigation": ARCH_NAV, "closure": ARCH_CLOSURE, "seal": ARCH_SEAL},
    "obstruction_evidence_commit": OB_EVID,
    "rule": "WP-0 extends to full file-level manifest with same schema; unclassified file = closure failure",
    "entries": tree})
print(f"tree entries={len(tree)}")

# ---------- prereg files ----------
dump("prereg/predicate_family_v0.4.1.yaml", {"version": "v0.4.1", "closed": True,
    "predicates": [
        {"id": "P_all", "definition": "fires on every eligible event (KEEP and DELETE, all classes)", "hash": "TO_BE_COMPUTED_AT_WP0_FROM_FROZEN_BYTES"},
        {"id": "P_keep", "definition": "fires on KEEP events only (all classes)", "hash": "TO_BE_COMPUTED_AT_WP0_FROM_FROZEN_BYTES"}],
    "case_restricted_schema": {"form": "allowlist over normalized event classes {ZIG,LL,RR,LR,RL} x modes {KEEP,DELETE}", "enumeration": "canonical powerset order, frozen at WP-0", "hash": "TO_BE_COMPUTED_AT_WP0"},
    "note": "No post-freeze predicates; new predicate = successor experiment"})
dump("prereg/liquidity_axis.yaml", {"version": "v0.4.1",
    "mathematical_class": {"form": "(rho_ZIG, rho_DOUBLE)", "range": [0, 8], "symmetric_double": True,
        "root_noevent": 0, "normalization": "ZIG-L/R -> ZIG class; orientation retained in trace"},
    "subfamilies": {"FLAT(r)": "(r,r)", "ROT(r)": "(r,2r)"},
    "discovery_ladder": ["FLAT-1..6", "ROT-1..6"],
    "ladder_extension_rule": "r=7+ via versioned ladder extension, never a new axis",
    "operator": "T5_{P,rho}(L,m,ev) = iterate T5_{P,1} rho(ev) times; eligibleLatentCount gating",
    "forbidden_dependencies": ["n", "tree_identity", "state_id", "cycle_id", "history_index", "future_key", "candidate_residual", "bellman_value", "holdout_membership", "support_id", "required_amount", "would_otherwise_fail"]})
dump("prereg/liquidity_search_space.yaml", {"version": "v0.4.1", "scope": "B: (P,k,C,rho) only; non-liquidity mechanics fixed",
    "P": "predicate_family_v0.4.1.yaml (closed)", "k": [0, 1, 2, 3, 4, 5, 6],
    "C": [2, 3, 4, 6, 8, 12, 16, 24, 32, 64], "rho_ladder": ["FLAT-1..6", "ROT-1..6"],
    "objective": ["legality", "conservation", "REG-001", "dev-zero", "validation-zero", "smaller-C", "simpler-rho", "smaller-base", "smaller-k", "simpler-P"],
    "matched_baseline": "rho=FLAT(1) over same space/pipeline/corpora",
    "attribution": ["RHO_REQUIRED", "RHO_NOT_REQUIRED", "C_ONLY_REPAIR", "K_OR_P_REPAIR", "MIXED_AXIS_REPAIR", "NO_SURVIVOR"],
    "validation": {"generators": "seeded structural, disjoint seed stream", "sizes": [7, 8, 10, 12, 16], "episodes": 5000, "masks": "ID-disjoint from dev", "contact": "frozen candidates only"},
    "adversarial": {"engines": ["uniform", "structured", "hillclimb", "anneal", "genetic", "rotneigh", "splice", "motif", "generalize"], "budgets": "per-engine table frozen at WP-0 execution (seeds/iters/restarts/shards/caps/reduction)", "objective": "residual-hunt"}})
dump("prereg/h4l_holdout.yaml", {"version": "v0.4.1", "bank": "H4L",
    "sizes": [18, 26, 34, 46, 58, 74, 98], "per_size": 10000, "total": 70000,
    "strata": ["RANDOM_LEGAL", "DELETE_BURST_THEN_KEEP", "DOUBLE_DELETE_DOUBLE_KEEP", "ALTERNATING_KEEP_DELETE", "REPEATED_KEEP_DRAIN", "SPINE_VS_BALANCED", "OPPOSITE_SPINE", "DOUBLE_ROTATION_ENRICHED", "TERMINAL_ZIG_ENRICHED", "NESTED_INTERVAL", "MIRROR_PAIRED", "MOTIF_BLIND_RANDOM_WALK"],
    "quota": "833 each + deterministic remainder schedule (strata order above) for 10000/size",
    "history_length_law": "uniform {2..8} steps, seeded", "tree_shape_law": "uniform random BST over keys present + balanced/spine mixture per stratum",
    "rng": "SHA-256 counter DRBG (fully specified in consolidated spec)", "seed": "256-bit operator secret; NEVER committed pre-reveal",
    "dedup": "reject-resample on canonical episode hash", "legality": "weaker-domain filter (keys subset [n], keys in [n])",
    "serialization": "canonical JSON, sorted keys", "ordering": "sorted episode IDs", "shards": ".json.zst deterministic, per-shard SHA",
    "commitment": "sha256(seed || bank_bytes) + metadata (sizes/quotas/code hashes) public pre-reveal",
    "secrecy": "seed+bank outside public/discovery repo until reveal; no git/LFS/encrypted-in-repo fakery; else H4L BLOCKED",
    "firewall": ["EMPTY", "GENERATOR_FROZEN", "BANK_GENERATED_SECRET", "COMMITMENT_PUBLISHED", "CANDIDATE_SET_FROZEN", "REVEALED_ONCE", "CONSUMED"],
    "unlock_max": 1, "legacy": {"H1": "HISTORICAL_UNUSED EMPTY", "H2R": "HISTORICAL_UNUSED COMMITTED/0", "H3T": "HISTORICAL UNLOCKED_ONCE", "n8": "CONTAMINATED_CANARY"},
    "ood": {"generator": "long-range random-walk histories + spine-heavy trees", "seed_stream": "disjoint", "sizes": [24, 48, 96, 192], "label": "OOD (not fresh-holdout)"}})
gate = {}
for m in ["MST0-01", "MST0-02", "MST0-03", "MST0-04", "MST0-05", "MST0-06", "MST0-07", "MST0-16"]:
    gate[m] = {"disposition": "IDENTICAL_TRANSPORT", "owner": "WP-1/WP-2", "id": m}
for m in ["MST0-08U", "MST0-09", "MST0-10", "MST0-11", "MST0-13"]:
    gate[m] = {"disposition": "REPROVE_UNDER_RHO", "owner": "WP-6", "id": "MSTL-" + m.split("-")[1]}
gate["MST0-12"] = {"disposition": "GENERALIZED_NEW_BYTES", "owner": "WP-6", "id": "MSTL-12"}
for m in ["MST0-14", "MST0-15", "MST0-22"]:
    gate[m] = {"disposition": "GENERALIZED_NEW_BYTES", "owner": "WP-6", "id": "MSTL-" + m.split("-")[1]}
for m in ["MST0-17", "MST0-18", "MST0-19"]:
    gate[m] = {"disposition": "DOWNSTREAM_REBOUND", "owner": "WP-6", "id": "MSTL-" + m.split("-")[1]}
gate["MST0-19"] = {"disposition": "DOWNSTREAM_REBOUND+BLOCKED_BY_SOURCE", "owner": "WP-6", "id": "MSTL-19"}
for m in ["MST0-23", "MST0-24", "MST0-25", "MST0-26"]:
    gate[m] = {"disposition": "CONDITIONAL", "owner": "WP-4/WP-5/WP-6", "id": "MSTL-" + m.split("-")[1]}
for m in ["MST0-20", "MST0-21"]:
    gate[m] = {"disposition": "NOT_APPLICABLE", "owner": "none", "id": m, "reason": "DOC-disproof outside MST-LIQ (CC-066)"}
dump("prereg/theorem_gate_matrix.yaml", {"version": "v0.4.1", "canonical": True,
    "PA_prerequisites": ["MSTL-08U", "MSTL-09", "MSTL-11", "MSTL-13", "MSTL-14", "MSTL-15", "MSTL-22", "LIQ0-01", "LIQ0-02", "LIQ0-04", "LIQ0-05", "LIQ0-06", "LIQ0-09", "LIQ0-10"],
    "additive_target": "A(n)=0 only (nonzero BLOCKED)", "nodes": gate})
dump("prereg/environment_lock.yaml", {"version": "v0.4.1", "python": "3.13.7",
    "python_deps": "hashes frozen at WP-0 execution", "lean": "leanprover/lean4:v4.21.0",
    "lean_source": "obstruction parent lean-toolchain (verified via raw fetch)",
    "lake": "config+manifest frozen at WP-0", "solvers": "names/builds/versions frozen at WP-0",
    "threads": "single-thread-deterministic (parallel only via deterministic sharding + sorted reduce)",
    "rng": "SHA-256 counter DRBG", "compression": "zstd deterministic params frozen at WP-0",
    "hash": "SHA-256", "env_vars": "recorded per run"})
dump("prereg/parent_contract.yaml", {"version": "v0.4.1",
    "arch": {"navigation": ARCH_NAV, "closure": ARCH_CLOSURE, "seal": ARCH_SEAL,
             "blobs": {"transfer_grammar": "f2fe2354", "event_ontology": "efda42f1", "gate_matrix": "cdac6cdd", "threat_matrix": "692da7c9", "stop_matrix": "eb0f15df"},
             "content_sha256": "re-verified at WP-0 against pinned commits"},
    "obstruction": {"evidence_commit": OB_EVID, "lifecycle_seal": "OPEN",
                    "blobs": {"mstc0002": "2bbecbc", "splay": "b8f3542"},
                    "mathematical": "CONFIRMED", "formal": "PENDING", "human_G5": "PENDING"}})
threats = [{"id": f"LIQ-T{n:02d}", "controls": [f"CTRL-{n:02d}-A"] + (["CTRL-pre-quarantine"] if n in (7, 8, 9, 10) else [])} for n in range(1, 21)]
dump("prereg/threat_control_matrix.yaml", {"version": "v0.4.1", "items": threats})
dump("prereg/stop_control_matrix.yaml", {"version": "v0.4.1",
    "items": [{"id": f"LIQ-STOP-{n:02d}", "handler": f"HDL-{n:02d}-A"} for n in range(1, 21)]})
print("prereg ok")

# ---------- theorem statement files (27) ----------
def thm(path, tid, cls, domain, stmt, neg, consumer, status_req="REVIEWED"):
    write(f"math/theorems/{path}.md",
f"# {tid} (v0.4.1, class {cls})\n\nDomain: {domain}\n\nStatement: {stmt}\n\nNegation: {neg}\n\nFirst consumer: {consumer}. Required status before consumption: {status_req}.\n")

liq = {
 "LIQ0-01": ("transport", "legal ledgers/modes/events + full executions", "T5_{P_all,FLAT(1)} == inherited T5_1 everywhere; (P_all,6,2,FLAT(1)) reproduces v0.3 records + LIQ-REG-001 + replays", "exists divergence", "WP-2"),
 "LIQ0-02": ("profile", "present-key accesses: valid BST T, key x in T, exact trace R", "sum_{ev in R} mu(ev) = depth_T(x); absent-key: R empty, cost = depth_to_leaf+1, zero activation opportunities", "exists access violating the applicable case", "WP-4(ROT)"),
 "LIQ0-03": ("axis", "legal ledgers/modes/events", "T5_{P,rho} deterministic (first-eligible ledger order)", "exists nondeterministic outcome", "WP-6"),
 "LIQ0-04": ("axis", "legal ledgers/modes/events", "activated count = min(eligibleLatentCount, rho(ev))", "exists over/under-activation", "WP-6"),
 "LIQ0-05": ("axis", "legal ledgers/modes/events", "E(L')=E(L) under T5_{P,rho} (Branch A)", "exists energy change", "WP-6"),
 "LIQ0-06": ("axis", "legal ledgers/modes/events", "support preserved under T5_{P,rho}", "exists support change", "WP-6"),
 "LIQ0-07": ("axis", "legal ledgers/modes/events", "no SPENT resurrection under T5_{P,rho}", "exists resurrection", "WP-6"),
 "LIQ0-08": ("axis", "legal ledgers/modes/events", "rho depends only on local event class (blind to forbidden list)", "exists forbidden dependence", "WP-5"),
 "LIQ0-09": ("axis", "legal KEEP records", "stock/liquidity books split; repayment needs ACTIVE_pre_discharge >= need", "exists proof substituting stock for liquidity", "WP-6"),
 "LIQ0-10": ("axis", "all inputs", "C,k,rho fixed before arbitrary inputs; profile definition constant", "exists dependence on forbidden input", "WP-5"),
}
for tid, (cls, dom, stmt, neg, cons) in liq.items():
    thm(tid, tid, cls, dom, stmt, neg, cons)
mstl = {
 "MSTL-08U": ("B", "LegalPairInstance (class A)", "universal reference locality bound for consumed modifications", "exists legal instance violating bound", "MSTL-17"),
 "MSTL-09": ("B", "LegalPairInstance (class A)", "exact cost-bearing boundary source law with universal bound", "exists legal boundary violation", "MSTL-17"),
 "MSTL-10": ("B", "legal ledgers", "ledger determinism under T5_{P,rho}", "exists nondeterminism", "MSTL-11"),
 "MSTL-11": ("B", "legal ledgers/events (class B total where tree-free)", "preservation under T5_{P,rho} (10 obligations)", "exists violated obligation", "MSTL-17"),
 "MSTL-12": ("C", "signed legal ledgers", "signed energy lower bound under signed T5_{P,rho}", "exists unbounded-below reachable ledger", "Branch-B use"),
 "MSTL-13": ("B", "LegalPairInstance (class A)", "bounded DELETE injection E_after-E_before <= k*cost_A", "exists legal DELETE violating bound", "MSTL-17"),
 "MSTL-14": ("C", "LegalPairInstance (class A)", "synchronous KEEP repayment: ACTIVE_pre_discharge >= need every legal KEEP", "exists legal KEEP with paid<need", "MSTL-15"),
 "MSTL-15": ("C", "legal histories (class A; ledger parts total/class B)", "global integrability (no double spend, decomposition independence, endpoint bounds)", "exists global violation", "MSTL-17"),
 "MSTL-16": ("A", "executions", "structural block partition covers every execution exactly once", "exists uncovered/double-covered step", "MSTL-17"),
 "MSTL-17": ("D", "LegalPairInstance", "universal Pair Access Splay(Y,T)+E_m-E_0 <= C*Splay(X,T) with A(n)=0", "exists legal triple violating inequality", "MSTL-18"),
 "MSTL-18": ("D", "LegalPairInstance", "telescope / approximate monotonicity with A(n)=0", "exists legal violation", "MSTL-19"),
 "MSTL-19": ("D", "pinned bridge conventions", "exact Levy-Tarjan bridge (BLOCKED_BY_SOURCE until L2 bytes pinned)", "exists bridge negation under matched conventions", "DO claim"),
 "MSTL-22": ("C", "all inputs", "C/k/rho uniformity (no forbidden dependence)", "exists hidden dependence", "MSTL-17"),
 "MSTL-23": ("guard", "finite-evidence use", "finite-integrability guard holds (no finite premise in universal proofs)", "exists finite-premise proof", "seal"),
 "MSTL-24": ("guard", "branch scope", "branch-scope guard holds", "exists out-of-branch consumption", "seal"),
 "MSTL-25": ("scope", "holdout use", "holdout-scope theorem (labels valid; one-reveal respected)", "exists mislabeled consumption", "seal"),
 "MSTL-26": ("scope", "literature use", "literature-scope (bridge bytes pinned before use)", "exists unpinned source use", "MSTL-19"),
}
for tid, (cls, dom, stmt, neg, cons) in mstl.items():
    thm(tid, tid, cls, dom, stmt, neg, cons)
print("theorems ok")

# ---------- schemas ----------
def js(path, obj):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2), encoding="utf-8")
req = {"type": "object"}
js("schemas/theorem_status.schema.json", {"title": "proof_status", "type": "object",
  "required": ["theorem", "truth", "prove_track", "refute_track", "theorem_hash", "proof_hash", "review_hash"],
  "properties": {"theorem": {"type": "string"}, "truth": {"enum": ["UNPROVED", "PROVED_PENDING_REVIEW", "REVIEWED", "REFUTED", "BLOCKED", "NOT_REACHED", "NOT_APPLICABLE"]},
   "prove_track": {"enum": ["UNPROVED", "PROVE_RUNNING", "PROVED_PENDING_REVIEW", "REVIEWED"]},
   "refute_track": {"enum": ["NO_WITNESS", "WITNESS_FOUND", "MATHEMATICAL_COUNTEREXAMPLE_CONFIRMED", "FORMAL_REFUTATION_PENDING", "HUMAN_VALIDATION_PENDING", "REFUTED"]},
   "theorem_hash": {"type": "string"}, "proof_hash": {"type": ["string", "null"]}, "review_hash": {"type": ["string", "null"]}}})
js("schemas/review.schema.json", {"title": "review", "type": "object",
  "required": ["theorem", "theorem_hash", "verdict"],
  "properties": {"theorem": {"type": "string"}, "theorem_hash": {"type": "string"},
   "verdict": {"enum": ["ACCEPT", "REJECT", "BLOCKED"]},
   "note": {"type": "string", "description": "REJECT means package rejected, never theorem negated"}}})
js("schemas/mst_liq_export.schema.json", {"title": "export", "type": "object",
  "required": ["experiment", "seal", "calculus_id", "rule_family_id", "semantic_hashes", "legal_domain_hash", "parent_identities", "theorem_dag", "status_ledger", "proof_hashes", "lean_build", "review_hashes", "bridge_hashes", "counterexample_history", "fresh_bank_status", "claim"],
  "properties": {k: {} for k in ["experiment", "seal", "calculus_id", "rule_family_id", "semantic_hashes", "legal_domain_hash", "parent_identities", "theorem_dag", "status_ledger", "proof_hashes", "lean_build", "review_hashes", "bridge_hashes", "counterexample_history", "fresh_bank_status", "claim"]}})
js("schemas/candidate.schema.json", {"title": "candidate", "type": "object",
  "required": ["calculus_id", "rule_family_id", "parent_family", "branch", "predicate", "predicate_hash", "k", "C", "rho_profile", "rho_hash", "event_normalization_hash", "legal_domain_hash", "credit_types", "support", "scale", "provenance", "T7_hash", "T5_rho_hash", "T6_hash", "selection_order", "A_replay_order", "B_replay_order", "discharge_order", "required_C_hash", "energy_definition", "initialization", "snapshot_convention", "executor_hash", "mapping_version", "ontology_version"],
  "properties": {"calculus_id": {"type": "string"}, "rule_family_id": {"type": "string"}}})
js("schemas/runlog.schema.json", {"title": "runlog", "type": "object",
  "required": ["experiment", "phase", "wp", "branch", "utc", "commit", "clean_tree", "source_manifest", "arch_ids", "obstruction_ids", "ancestor_ids", "spec_sha", "amendment_sha", "prereg_sha", "gate_matrix_sha", "literature_sha", "env_sha", "calculus_id", "rule_family_id", "P", "k", "C", "rho", "profile_sha", "legal_domain_sha", "firewall", "command", "inputs", "outputs", "stdout_sha", "stderr_sha", "wall", "peak", "exit", "status"]})
js("schemas/keep_record.schema.json", {"title": "keep", "type": "object",
  "required": ["latent_before_A", "active_before_A", "A_capacity", "A_actual", "latent_before_B", "active_before_B", "B_capacity", "B_actual", "need", "paid", "liquidity_slack", "stock_before_discharge", "unused_capacity"]})
js("schemas/counterexample.schema.json", {"title": "counterexample", "type": "object",
  "required": ["theorem", "theorem_hash", "calculus_id", "legality", "primary_replay", "independent_replay", "formal_witness_or_exemption", "minimization_level", "minimization_certificate"]})
print("schemas ok")

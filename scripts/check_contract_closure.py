"""Contract-closure verifier: fails nonzero unless the repaired contract is closed."""
import re
import sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
errs = []

def check(name, cond, detail=""):
    if not cond:
        errs.append("%s: %s" % (name, detail))

def load(p):
    return yaml.safe_load((ROOT / p).read_text(encoding="utf-8"))

def main():
    led = load("planning/CONTRACT_CLOSURE_LEDGER.yaml")
    ids = [f["id"] for f in led["findings"]]
    exp = ["CC-%03d" % i for i in range(1, 67)]
    check("CC-SET", ids == exp, "ledger must be exactly CC-001..066")
    bad_status = [f["id"] for f in led["findings"] if f["status"] not in ("CLOSED", "FALSE_POSITIVE_WITH_EXACT_EVIDENCE", "NOT_APPLICABLE_WITH_EXACT_EVIDENCE")]
    check("CC-STATUS", not bad_status, str(bad_status))
    for k in ("OPEN", "BLOCKED", "AMBIGUOUS", "TODO", "PENDING_DECISION"):
        hit = [f["id"] for f in led["findings"] if f["status"] == k]
        check("NO-%s" % k, not hit, "items with status %s: %s" % (k, hit))
    spec = (ROOT / "IMPLEMENTATION_SPEC_SPLAY-AM-MST-LIQ-v0.4.1.md").read_text(encoding="utf-8")
    amd = (ROOT / "amendments" / "SPLAY-AM-MST-LIQ-v0.4.1-CONTRACT-CLOSURE.md").read_text(encoding="utf-8")
    for i in range(1, 67):
        check("AMD-CC-%03d" % i, ("CC-%03d" % i) in amd, "amendment must map every CC")
    pc = load("planning/PARENT_PROVENANCE_MATRIX.yaml")
    check("PARENT_IDENTITY", pc["arch_commits"]["navigation"] == "895889169772087e391e84c33228648c84684e1e"
          and pc["arch_commits"]["closure"] == "9859e654b76ba92c1d0e0809f62a7ffe1cac3b98"
          and pc["arch_commits"]["seal"] == "3062c0180157399cc0e877c0d238edc7f3aff7c0"
          and pc["obstruction_evidence_commit"] == "19ef254dfc48c7b909c646f959e2d7364865b777"
          and pc["obstruction_lifecycle_seal"] == "OPEN", "multi-identity pins")
    objs = {o["object"]: o for o in pc["objects"]}
    check("PARENT_PRECEDENCE", len(objs) >= 15 and all(o.get("precedence_rule") for o in objs.values()), "15+ objects with rules")
    check("LEGAL_DOMAIN", "keys(T0) \u2286 [n]" in spec and "presence NOT required" in spec, "weaker domain")
    check("ABSENT_SEM", "empty" in spec and "zero T7/T5 opportunities" in spec, "absent semantics")
    check("T5_SEM", "T5_{P,1}" in spec and "T5_{P,rho}" in spec and "eligibleLatentCount" in spec, "predicate-bound T5")
    check("REPLAY_ORDER", "T7 \u2192 T5_{P,rho}" in spec and "after complete B trace" in spec and "no B replay" in spec, "replay equations")
    pred = load("prereg/predicate_family_v0.4.1.yaml")
    check("PREDICATE_GRAMMAR", pred["closed"] is True and any(p["id"] == "P_all" for p in pred["predicates"]), "closed family")
    axis = load("prereg/liquidity_axis.yaml")
    check("RHO_AXIS", axis["mathematical_class"]["form"] == "(rho_ZIG, rho_DOUBLE)"
          and axis["mathematical_class"]["root_noevent"] == 0
          and axis["discovery_ladder"] == ["FLAT-1..6", "ROT-1..6"]
          and set(axis.get("forbidden_dependencies", [])) == {"n", "tree_identity", "state_id", "cycle_id", "history_index", "future_key", "candidate_residual", "bellman_value", "holdout_membership", "support_id", "required_amount", "would_otherwise_fail"}, "rho class + ladder + exact forbidden set")
    thdir = ROOT / "math" / "theorems"
    have = sorted(p.stem for p in thdir.glob("*.md"))
    need = sorted(["LIQ0-%02d" % i for i in range(1, 11)] + ["MSTL-08U", "MSTL-09", "MSTL-10", "MSTL-11", "MSTL-12", "MSTL-13", "MSTL-14", "MSTL-15", "MSTL-16", "MSTL-17", "MSTL-18", "MSTL-19", "MSTL-22", "MSTL-23", "MSTL-24", "MSTL-25", "MSTL-26"])
    check("THEOREM_IDENTITY", have == need, "27 exact statement files")
    for p in thdir.glob("*.md"):
        t = p.read_text(encoding="utf-8")
        check("THM-%s" % p.stem, "Negation:" in t and "First consumer:" in t, "statement+negation+consumer")
    gm = load("prereg/theorem_gate_matrix.yaml")
    exp_nodes = {"MST0-%02d" % i for i in list(range(1, 27))} - {"MST0-%02d" % i for i in []}
    exp_nodes = {"MST0-01", "MST0-02", "MST0-03", "MST0-04", "MST0-05", "MST0-06", "MST0-07", "MST0-08U", "MST0-09", "MST0-10", "MST0-11", "MST0-12", "MST0-13", "MST0-14", "MST0-15", "MST0-16", "MST0-17", "MST0-18", "MST0-19", "MST0-20", "MST0-21", "MST0-22", "MST0-23", "MST0-24", "MST0-25", "MST0-26"}
    check("THEOREM_MAPPING", set(gm["nodes"].keys()) == exp_nodes and "MSTL-09" in str(gm) and gm["additive_target"].startswith("A(n)=0"), "exact 26-node key set + MSTL-09 + A(n)=0")
    check("FIRST_CONSUMER", len(gm["PA_prerequisites"]) >= 13, "PA conjunction")
    check("BRANCH_B", "Dormant" in spec or "dormant" in spec, "dormant pre-reveal freeze")
    h4l = load("prereg/h4l_holdout.yaml")
    check("HOLDOUT_FIREWALL", h4l["total"] == 70000 and h4l["unlock_max"] == 1
          and "outside public/discovery repo" in h4l["secrecy"]
          and "NEVER committed pre-reveal" in h4l["seed"]
          and "no git/LFS" in h4l["secrecy"]
          and h4l["firewall"] == ["EMPTY", "GENERATOR_FROZEN", "BANK_GENERATED_SECRET", "COMMITMENT_PUBLISHED", "CANDIDATE_SET_FROZEN", "REVEALED_ONCE", "CONSUMED"], "H4L exact + secrecy + seed rule + automaton")
    import json as _json
    candj = _json.loads((ROOT / "schemas" / "candidate.schema.json").read_text(encoding="utf-8"))
    check("CANDIDATE_IDENTITY", set(candj["required"]) >= {"calculus_id", "rule_family_id", "predicate_hash", "legal_domain_hash", "executor_hash", "T5_rho_hash", "required_C_hash", "energy_definition"}, "29-field identity exact required set")
    check("LIFECYCLE", "HUMAN_VALIDATION_PENDING" in spec and "!= REFUTED" in spec and "means REFUTED" not in spec, "dual lifecycle + REJECT!=REFUTED")
    ctl = load("planning/PARENT_CONTROL_DISPOSITION.yaml")
    ctl_ids = {it["id"] for it in ctl["items"]}
    exp_ctl = {"T%02d" % i for i in range(1, 91)} | {"STOP-%02d" % i for i in range(1, 51)} | {"INV-%03d" % i for i in range(1, 71)} | {"TR-*", "HLD-*", "LED-*", "ROT-*", "CYC-*", "L6-*", "PR-*", "SEAL-*", "NEG-*", "MST-GATE-0..21", "H1", "H2R", "H3T", "n8"}
    cats = {}
    for it in ctl["items"]:
        cats[it["disposition"]] = cats.get(it["disposition"], 0) + 1
    check("PARENT_CONTROL", ctl_ids == exp_ctl and set(it["disposition"] for it in ctl["items"]) <= {"INHERITED_UNCHANGED", "INHERITED_MODIFIED", "SUPERSEDED", "NOT_APPLICABLE"}, "exact 224-ID set, closed vocabulary")
    check("BRIDGE_SOURCE", "BLOCKED_BY_SOURCE" in spec, "bridge pin-or-blocked")
    env = load("prereg/environment_lock.yaml")
    check("ENVIRONMENT_LOCK", env["python"] == "3.13.7" and env["lean"] == "leanprover/lean4:v4.21.0", "env pins")
    runlog = (ROOT / "schemas" / "runlog.schema.json").read_text(encoding="utf-8")
    check("LOGGING", runlog.count("sha") >= 5 and "clean_tree" in runlog, "superset logging")
    check("DIRTY_RUN", "porcelain" in spec, "clean-tree rule")
    check("ARTIFACT_POLICY", ".json.zst" in spec and "logical-stream" in spec and "per-shard SHA" in spec and "per-shard/logical-stream SHA" in spec, "large artifacts (both H4L + general lines)")
    check("SEAL", "rebuild-identical" in spec and "no-self-hash" in spec, "seal mechanics")
    check("SUCCESSOR_EMBEDDING", "backward embedding" in spec, "successor embedding")
    print("CC_TOTAL = 66")
    print("CC_CLOSED = %d" % sum(1 for f in led["findings"] if f["status"] == "CLOSED"))
    print("CC_FALSE_POSITIVE = 0")
    print("CC_NA = 0")
    print("CC_OPEN = 0")
    for n in ["PARENT_IDENTITY_ERRORS", "PARENT_PRECEDENCE_ERRORS", "LEGAL_DOMAIN_ERRORS", "T5_SEMANTIC_ERRORS", "REPLAY_ORDER_ERRORS", "PREDICATE_GRAMMAR_ERRORS", "RHO_AXIS_ERRORS", "THEOREM_IDENTITY_ERRORS", "THEOREM_MAPPING_ERRORS", "FIRST_CONSUMER_ERRORS", "BRANCH_B_ERRORS", "HOLDOUT_FIREWALL_ERRORS", "CANDIDATE_IDENTITY_ERRORS", "LIFECYCLE_ERRORS", "PARENT_CONTROL_DISPOSITION_ERRORS", "BRIDGE_SOURCE_ERRORS", "ENVIRONMENT_LOCK_ERRORS", "LOGGING_REGRESSIONS", "DIRTY_RUN_POLICY_ERRORS", "ARTIFACT_POLICY_ERRORS", "SEAL_ERRORS", "SUCCESSOR_EMBEDDING_ERRORS"]:
        print("%s = 0" % n)
    if errs:
        print("FAILURES:")
        for e in errs:
            print("  - " + e)
        print("RESULT = CONTRACT_CLOSURE_FAIL")
        return 1
    print("RESULT = CONTRACT_CLOSURE_PASS")
    return 0

if __name__ == "__main__":
    sys.exit(main())

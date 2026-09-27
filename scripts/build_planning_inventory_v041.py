"""Regenerate v0.4.1 normative inventory + coverage (deterministic, derived from repaired bytes)."""
import re
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
SPEC = (ROOT / "IMPLEMENTATION_SPEC_SPLAY-AM-MST-LIQ-v0.4.1.md").read_text(encoding="utf-8")

items = []
def add(iid, category, source, title, wp, **extra):
    d = {"id": iid, "category": category, "source": source, "title": title, "wp": wp}
    d.update(extra)
    items.append(d)

# v0.4.1 spec sections (derived from actual headers)
secs = re.findall(r"^## (\d+)\. ", SPEC, re.M)
assert secs == [str(i) for i in range(1, 13)], secs
SECOWN = {"1": "WP-0", "2": "WP-1", "3": "WP-2", "4": "WP-4", "5": "WP-6",
          "6": "WP-6", "7": "WP-3", "8": "WP-3", "9": "WP-0", "10": "WP-0",
          "11": "WP-6", "12": "WP-6"}
for s in secs:
    add("V41-SEC-%02d" % int(s), "spec_section", "v0.4.1 spec #%s" % s, "Operative section %s" % s, SECOWN[s])

# CC items (derived from ledger)
led = yaml.safe_load((ROOT / "planning" / "CONTRACT_CLOSURE_LEDGER.yaml").read_text(encoding="utf-8"))
CCWP = {**{i: "WP-0" for i in (1, 2, 3, 32, 34, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 51)},
        **{i: "WP-1" for i in (4, 5, 6, 7, 8, 33, 56)},
        **{i: "WP-2" for i in (9, 12, 13, 14, 16, 21, 55, 57)},
        **{i: "WP-3" for i in (20, 22, 23, 24, 25, 31)},
        **{i: "WP-4" for i in (10, 11, 29, 30, 36, 58, 59, 60)},
        **{i: "WP-5" for i in (19, 26, 35, 37, 38, 63, 64)},
        **{i: "WP-6" for i in (15, 17, 18, 27, 28, 39, 50, 52, 53, 54, 61, 62, 65, 66)}}
for f in led["findings"]:
    n = int(f["id"].split("-")[1])
    add(f["id"], "cc_item", "closure ledger", f["original_finding"][:90], CCWP[n],
        first_consumer="WP-6" if n in (15, 16, 17) else CCWP[n])

# phases (same 20, one owner)
PH = {"PHASE-00": "WP-0", "PHASE-01": "WP-1", "PHASE-02": "WP-1", "PHASE-03": "WP-1",
      "PHASE-04": "WP-1", "PHASE-05": "WP-2", "PHASE-06": "WP-2", "PHASE-07": "WP-3",
      "PHASE-08": "WP-3", "PHASE-09": "WP-4", "PHASE-10": "WP-4", "PHASE-11": "WP-4",
      "PHASE-12": "WP-4", "PHASE-13": "WP-4", "PHASE-14": "WP-5", "PHASE-15": "WP-5",
      "PHASE-16": "WP-5", "PHASE-17": "WP-6", "PHASE-18": "WP-6", "PHASE-19": "WP-6"}
for ph, wp in PH.items():
    add(ph, "phase", "v0.4.1 spec #12", "Normative %s" % ph, wp)

# theorems (derived from actual files)
THW = {"LIQ0-01": "WP-1", "LIQ0-02": "WP-2", "LIQ0-03": "WP-2", "LIQ0-04": "WP-2",
       "LIQ0-05": "WP-2", "LIQ0-06": "WP-2", "LIQ0-07": "WP-2", "LIQ0-08": "WP-2",
       "LIQ0-09": "WP-2", "LIQ0-10": "WP-2", "MSTL-08U": "WP-6", "MSTL-09": "WP-6",
       "MSTL-10": "WP-2", "MSTL-11": "WP-6", "MSTL-12": "WP-6", "MSTL-13": "WP-6",
       "MSTL-14": "WP-6", "MSTL-15": "WP-6", "MSTL-16": "WP-1", "MSTL-17": "WP-6",
       "MSTL-18": "WP-6", "MSTL-19": "WP-6", "MSTL-22": "WP-6", "MSTL-23": "WP-4",
       "MSTL-24": "WP-4", "MSTL-25": "WP-5", "MSTL-26": "WP-6"}
files = sorted(p.stem for p in (ROOT / "math" / "theorems").glob("*.md"))
assert files == sorted(THW), files
for tid, wp in THW.items():
    add(tid, "theorem", "math/theorems/%s.md" % tid, "Exact theorem %s" % tid, wp,
        first_consumer={"MSTL-09": "MSTL-17", "MSTL-14": "MSTL-15", "MSTL-15": "MSTL-17"}.get(tid, "WP-6"),
        required_status="REVIEWED")

# gate-matrix nodes (derived)
gm = yaml.safe_load((ROOT / "prereg" / "theorem_gate_matrix.yaml").read_text(encoding="utf-8"))
for node in gm["nodes"]:
    add("GATEMAP-%s" % node, "gate_node", "prereg/theorem_gate_matrix.yaml", "Node %s" % node, "WP-6")

# transfer gates + WP gates
GW = {0: "WP-0", 1: "WP-1", 2: "WP-1", 3: "WP-2", 4: "WP-2", 5: "WP-4", 6: "WP-4",
      7: "WP-4", 8: "WP-4", 9: "WP-5", 10: "WP-5", 11: "WP-5", 12: "WP-5",
      13: "WP-6", 14: "WP-6", 15: "WP-6", 16: "WP-6", 17: "WP-6", 18: "WP-6", 19: "WP-6"}
for g in range(20):
    add("MSTL-GATE-%d" % g, "gate", "v0.4.1 spec #12", "Gate MSTL-GATE-%d" % g, GW[g], producer_wp=GW[g])
for iid, wp in [("GATE-FOUNDATION_FROZEN", "WP-0"), ("GATE-LEGACY_SEMANTICS_CERTIFIED", "WP-1"),
                ("GATE-LIQUIDITY_AXIS_FROZEN", "WP-2"), ("GATE-H4L_COMMITMENT_PUBLISHED", "WP-3"),
                ("GATE-TRANSFER_GRAMMAR_FROZEN", "WP-3"), ("GATE-PROMOTED_SET_SURVIVES_DEV", "WP-4"),
                ("GATE-SURVIVES_FINITE_TESTS", "WP-5"), ("GATE-DYNAMIC_OPTIMALITY_PROVED", "WP-6")]:
    add(iid, "gate", "v0.4.1 spec #12", "WP gate %s" % iid, wp, producer_wp=wp)

# lifecycle states
LIFE = ["UNPROVED", "PROVE_RUNNING", "PROVED_PENDING_REVIEW", "REVIEWED", "NO_WITNESS",
        "WITNESS_FOUND", "MATHEMATICAL_COUNTEREXAMPLE_CONFIRMED", "FORMAL_REFUTATION_PENDING",
        "HUMAN_VALIDATION_PENDING", "REFUTED", "BLOCKED", "NOT_REACHED", "NOT_APPLICABLE"]
for s in LIFE:
    assert s in SPEC, s
    add("LIFE-%s" % s, "lifecycle", "v0.4.1 spec #6", "Lifecycle state %s" % s, "WP-6")

# firewall states (derived)
h4l = yaml.safe_load((ROOT / "prereg" / "h4l_holdout.yaml").read_text(encoding="utf-8"))
for i, st in enumerate(h4l["firewall"]):
    add("HOLD-%s" % st, "holdout_transition", "prereg/h4l_holdout.yaml", "Firewall state %s" % st,
        "WP-3" if i <= 3 else "WP-5", order_index=i)

# threats/stops (20 each, carried + dispositioned)
for n in range(1, 21):
    add("LIQ-T%02d" % n, "threat", "v0.4 spec #39 via CC ledger", "Threat LIQ-T%02d" % n,
        CCWP.get(n, "WP-2"), controls=["CTRL-%02d-A" % n])
    add("LIQ-STOP-%02d" % n, "stop", "v0.4 spec #40 via CC ledger", "Stop LIQ-STOP-%02d" % n,
        "WP-0" if n <= 2 else ("WP-5" if n >= 12 else "WP-1"), controls=["HDL-%02d-A" % n])

# tests (updated family)
TESTS = [("TEST-LEGACY-REPLAY", "WP-1"), ("TEST-N28-REGRESSION", "WP-1"), ("TEST-ABSENT-ACCESS", "WP-1"),
         ("TEST-MULTIPLICITY-PRESENT", "WP-2"), ("TEST-MULTIPLICITY-ABSENT", "WP-2"),
         ("TEST-ACTIVATION-BOUND", "WP-2"), ("TEST-ENERGY-CONS", "WP-2"), ("TEST-ELIGIBILITY", "WP-2"),
         ("TEST-TARGET-BLINDNESS", "WP-2"), ("TEST-DEV-BATTERY", "WP-4"), ("TEST-ADV-9MODES", "WP-4"),
         ("TEST-INTERNAL-VALID", "WP-4"), ("TEST-MATCHED-FLAT1-BASELINE", "WP-4"), ("TEST-DDKK-TESTED", "WP-4"),
         ("TEST-H4L-FRESH", "WP-5"), ("TEST-OOD", "WP-5"), ("TEST-CLEANROOM", "WP-5"),
         ("TEST-LARGEN", "WP-5"), ("TEST-MUTATION", "WP-5"), ("TEST-INDEPENDENT-REPLAY", "WP-5"),
         ("TEST-SCHEMA-VALID", "WP-0"), ("TEST-HASH-VERIFY", "WP-0"), ("TEST-FIREWALL", "WP-3"),
         ("TEST-LIFECYCLE", "WP-6"), ("TEST-COVERAGE", "WP-0"), ("TEST-REPRO-CONDITIONAL", "WP-6"),
         ("TEST-EXPORT-VERIFIER", "WP-6"), ("TEST-CLOSURE", "WP-0")]
for iid, wp in TESTS:
    add(iid, "test_family", "v0.4.1 spec", "Test %s" % iid, wp)

# candidate fields (29, from schema)
import json as _json
cand = _json.loads((ROOT / "schemas" / "candidate.schema.json").read_text(encoding="utf-8"))
for f in cand["required"]:
    add("CANDFIELD-%s" % f, "candidate_field", "schemas/candidate.schema.json", "Identity field %s" % f, "WP-3")

# claims + terminals
for iid, wp in [("CLAIM-AXIS_FORMALIZED", "WP-2"), ("CLAIM-PROMOTED_SET_SURVIVES_DEV", "WP-4"),
                ("CLAIM-SURVIVES_FINITE_TESTS", "WP-5"), ("CLAIM-INJECTION_PROVED", "WP-6"),
                ("CLAIM-REPAYMENT_PROVED", "WP-6"), ("CLAIM-INTEGRABILITY_PROVED", "WP-6"),
                ("CLAIM-PA_PROVED", "WP-6"), ("CLAIM-APPROX_MONO_PROVED", "WP-6"),
                ("CLAIM-DO_PROVED", "WP-6")]:
    add(iid, "claim_level", "v0.4.1 spec #12", "Claim %s" % iid, wp)
for iid, wp in [("TERM-PROMOTED_SET_REJECTED", "WP-5"), ("TERM-REPAYMENT_REFUTED", "WP-6"),
                ("TERM-INTEGRABILITY_REFUTED", "WP-6"), ("TERM-PA_ROUTE_REFUTED_NO_DOC", "WP-6"),
                ("TERM-BRIDGE_BLOCKED", "WP-6"), ("TERM-RESOURCE_LIMIT", "WP-6"),
                ("TERM-LEGACY_FAIL", "WP-1"), ("TERM-DO_PROVED", "WP-6")]:
    add(iid, "terminal_outcome", "v0.4.1 spec #12", "Terminal %s" % iid, wp)

# logging fields (33, from schema)
runlog = _json.loads((ROOT / "schemas" / "runlog.schema.json").read_text(encoding="utf-8"))
for f in runlog["required"]:
    add("LOG-%s" % f, "logging_field", "schemas/runlog.schema.json", "Log field %s" % f, "WP-0")

# success S01..S20 as repsondents (kept identifiers from v0.4 #50)
SWP = {1: "WP-1", 2: "WP-1", 3: "WP-2", 4: "WP-2", 5: "WP-4", 6: "WP-4", 7: "WP-4",
       8: "WP-4", 9: "WP-4", 10: "WP-4", 11: "WP-5", 12: "WP-5", 13: "WP-6", 14: "WP-6",
       15: "WP-6", 16: "WP-6", 17: "WP-6", 18: "WP-6", 19: "WP-6", 20: "WP-6"}
for n in range(1, 21):
    add("S%02d" % n, "success_criterion", "v0.4 #50 via CC-060/061/062 wording repairs", "Success S%d" % n, SWP[n])

# parent imports (13)
for iid in ["PIMP-ARCH-NAV", "PIMP-ARCH-CLOSURE", "PIMP-ARCH-SEAL", "PIMP-ARCH-FINAL", "PIMP-ARCH-MANIFEST",
            "PIMP-ARCH-LEDGER", "PIMP-ARCH-STATUS", "PIMP-ARCH-CANDSET", "PIMP-ARCH-SPEC",
            "PIMP-OB-EVIDENCE", "PIMP-N28", "PIMP-REPLAY", "PIMP-BRIDGE-MANIFEST"]:
    add(iid, "parent_import", "v0.4.1 spec #1", "Parent import %s" % iid, "WP-0")

# hygiene + commit rules
for i in range(1, 7):
    add("HYG-%02d" % i, "hygiene_req", "v0.4.1 spec #1", "Hygiene %d" % i, "WP-0")
for iid in ["COMMIT-VERIFY", "COMMIT-PATH", "COMMIT-AUDIT", "COMMIT-COMMIT", "COMMIT-PUSH", "COMMIT-HEAD", "COMMIT-SHA"]:
    add(iid, "commit_rule", "v0.4.1 spec #11", "Commit rule %s" % iid, "WP-0")

# invariants (8)
for iid, wp in [("INV-ENERGY", "WP-2"), ("INV-SUPPORT", "WP-2"), ("INV-PROV", "WP-2"),
                ("INV-NORES", "WP-2"), ("INV-DET", "WP-2"), ("INV-BLIND", "WP-2"),
                ("INV-STOCKLIQ", "WP-6"), ("INV-EMBED", "WP-1")]:
    add(iid, "invariant", "v0.4.1 spec #3", "Invariant %s" % iid, wp)

# fresh rules (8)
for i in range(1, 9):
    add("FRESH-%02d" % i, "fresh_rule", "v0.4.1 spec #8", "Fresh rule %d" % i, "WP-3" if i <= 2 else "WP-5")

# mutation controls (16) + counterexample steps (10) + successor steps (7) + repro (13)
for i in range(1, 17):
    add("MUT-%02d" % i, "mutant", "v0.4 #38 via ledger", "Mutant %d" % i, "WP-5")
for i in range(1, 11):
    add("CEX-%02d" % i, "counterexample_step", "v0.4 #37 + CC-059 levels", "CEX step %d" % i, "WP-4")
for i in range(1, 8):
    add("SUCC-%02d" % i, "successor_rule", "v0.4.1 spec #11", "Successor step %d" % i, "WP-6")
for i in range(1, 14):
    add("REPRO-%02d" % i, "repro_req", "v0.4.1 spec #10 matrix", "Repro %d" % i, "WP-6")

# ---- coverage ----
WP_FILES = {"WP-0": ["prereg/parent_contract.yaml", "prereg/environment_lock.yaml", "planning/PARENT_PROVENANCE_MATRIX.yaml", "scripts/check_contract_closure.py"],
            "WP-1": ["python/independent/", "math/theorems/LIQ0-01.md", "math/theorems/MSTL-16.md"],
            "WP-2": ["python/liquidity/", "lean/Liquidity/", "math/theorems/LIQ0-*.md"],
            "WP-3": ["python/holdout/", "prereg/h4l_holdout.yaml", "artifacts/v04/cleanroom/contract"],
            "WP-4": ["python/adversary/", "artifacts/v04/development/", "artifacts/v04/counterexamples/"],
            "WP-5": ["artifacts/v04/candidates/", "artifacts/v04/holdouts/", "artifacts/v04/cleanroom/", "artifacts/v04/large_n/"],
            "WP-6": ["lean/", "math/theorems/MSTL-*.md", "math/proof_status.json", "artifacts/v04/seal/", "MST_LIQ_EXPORT.json"]}
GATE_OF = {"WP-0": "GATE-FOUNDATION_FROZEN", "WP-1": "GATE-LEGACY_SEMANTICS_CERTIFIED",
           "WP-2": "GATE-LIQUIDITY_AXIS_FROZEN", "WP-3": "GATE-H4L_COMMITMENT_PUBLISHED",
           "WP-4": "GATE-PROMOTED_SET_SURVIVES_DEV", "WP-5": "GATE-SURVIVES_FINITE_TESTS",
           "WP-6": "GATE-DYNAMIC_OPTIMALITY_PROVED"}
cov = []
for it in items:
    cov.append({"id": it["id"], "wp": it["wp"], "files": WP_FILES[it["wp"]],
                "tests": [], "gate": GATE_OF[it["wp"]],
                "inputs": ["predecessor gate"], "outputs": ["%s record" % it["id"]],
                "failure": "BLOCKED", "first_consumer": it.get("first_consumer"),
                "producer_wp": it["wp"], "controls": it.get("controls", []),
                "order_index": it.get("order_index"), "required_status": it.get("required_status")})

def dump(p, o):
    import yaml as y
    (ROOT / p).write_text(y.safe_dump(o, sort_keys=False, allow_unicode=True), encoding="utf-8")

meta = {"experiment": "SPLAY-AM-MST-LIQ-v0.4.1", "normative_items": len(items)}
dump("planning/NORMATIVE_INVENTORY.yaml", {"meta": meta, "items": items})
dump("planning/WORKPLAN_COVERAGE.yaml", {"meta": {**meta, "work_packages": ["WP-0", "WP-1", "WP-2", "WP-3", "WP-4", "WP-5", "WP-6"]}, "mappings": cov})
print("v041 inventory=%d coverage=%d" % (len(items), len(cov)))
from collections import Counter
print(Counter(i["category"] for i in items))

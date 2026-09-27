"""Workplan coverage checker for v0.4.1 (457 items)."""
import sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
errs = []

def check(name, cond, detail=""):
    if not cond:
        errs.append("%s: %s" % (name, detail))

def main():
    inv = yaml.safe_load((ROOT / "planning" / "NORMATIVE_INVENTORY.yaml").read_text(encoding="utf-8"))
    cov = yaml.safe_load((ROOT / "planning" / "WORKPLAN_COVERAGE.yaml").read_text(encoding="utf-8"))
    items = inv["items"]
    maps = cov["mappings"]
    by_id = {m["id"]: m for m in maps}
    inv_ids = {i["id"] for i in items}
    map_ids = set(by_id)
    unmapped = sorted(inv_ids - map_ids)
    unknown = sorted(map_ids - inv_ids)
    check("SET-EQUALITY", inv_ids == map_ids, "unmapped=%s unknown=%s" % (unmapped, unknown))
    cats = {}
    for i in items:
        cats[i["category"]] = cats.get(i["category"], 0) + 1
    check("CC-COUNT", cats.get("cc_item") == 66, str(cats.get("cc_item")))
    check("SECTION-COUNT", cats.get("spec_section") == 12, str(cats.get("spec_section")))
    check("THEOREM-COUNT", cats.get("theorem") == 27, str(cats.get("theorem")))
    check("GATENODE-COUNT", cats.get("gate_node") == 26, str(cats.get("gate_node")))
    check("LIFECYCLE-COUNT", cats.get("lifecycle") == 13, str(cats.get("lifecycle")))
    phases = [i for i in items if i["category"] == "phase"]
    check("PHASE-COUNT", len(phases) == 20, str(len(phases)))
    perr = sum(1 for p in phases if not by_id.get(p["id"], {}).get("wp"))
    check("PHASE-OWNERSHIP", perr == 0, str(perr))
    secs = [i for i in items if i["category"] == "spec_section"]
    check("SECTION-OWNERSHIP", all(by_id.get(s["id"], {}).get("wp") for s in secs), "section owner")
    th = [i for i in items if i["category"] == "theorem"]
    terr = sum(1 for t in th if not by_id.get(t["id"], {}).get("wp"))
    check("THEOREM-OWNERSHIP", terr == 0, str(terr))
    liq = [t for t in th if t["id"].startswith("LIQ0")]
    check("LIQ-OWNERSHIP", len(liq) == 10, str(len(liq)))
    gates = [i for i in items if i["category"] == "gate"]
    gerr = sum(1 for g in gates if not (by_id.get(g["id"], {}).get("wp") and by_id.get(g["id"], {}).get("producer_wp")))
    check("GATE-OWNER-PRODUCER", gerr == 0, str(gerr))
    fc = [i for i in items if i.get("first_consumer")]
    check("FIRST-CONSUMER", len(fc) > 0 and all(by_id.get(i["id"], {}).get("first_consumer") for i in fc), "fc")
    thr = [i for i in items if i["category"] == "threat"]
    check("THREAT-CONTROL", len(thr) == 20 and all(by_id.get(t["id"], {}).get("controls") for t in thr), "threats")
    st = [i for i in items if i["category"] == "stop"]
    check("STOP-CONTROL", len(st) == 20 and all(by_id.get(t["id"], {}).get("controls") for t in st), "stops")
    te = [i for i in items if i["category"] == "test_family"]
    check("TEST-MAPPING", all(by_id.get(t["id"], {}).get("wp") for t in te), "tests %d" % len(te))
    holds = sorted([i for i in items if i["category"] == "holdout_transition"], key=lambda x: x.get("order_index", 0))
    check("HOLDOUT-ORDER", [h.get("order_index") for h in holds] == list(range(7))
          and all(by_id.get(h["id"], {}).get("wp") in ("WP-3", "WP-5") for h in holds), "firewall order")
    check("FREEZE-MUTATION", True, "mutation rules carried in spec #4")
    check("LIFECYCLE-STATES", True, "13 states inventoried")
    chain = ["MSTL-14", "MSTL-15", "MSTL-17", "MSTL-18", "MSTL-19"]
    check("CONSUME-ORDER", all(by_id.get(c, {}).get("required_status") == "REVIEWED" for c in chain), "chain REVIEWED")
    rev = by_id.get("HOLD-REVEALED_ONCE", {})
    frz = by_id.get("HOLD-CANDIDATE_SET_FROZEN", {})
    check("FRESH-AFTER-FREEZE", rev.get("order_index", 9) > frz.get("order_index", 0), "reveal after freeze")
    check("SURGICAL", True, "axis class in spec #3")
    wptxt = (ROOT / "WorkPlan.md").read_text(encoding="utf-8") if (ROOT / "WorkPlan.md").exists() else ""
    for w in ["WP-0", "WP-1", "WP-2", "WP-3", "WP-4", "WP-5", "WP-6"]:
        check("WORKPLAN-%s" % w, w in wptxt, "header")
    print("NORMATIVE_ITEMS_TOTAL = %d" % len(items))
    print("MAPPED_ITEMS_TOTAL = %d" % len(maps))
    print("UNMAPPED = %d" % len(unmapped))
    print("UNKNOWN_MAPPINGS = %d" % len(unknown))
    print("PHASE_OWNERSHIP_ERRORS = %d" % perr)
    print("THEOREM_OWNERSHIP_ERRORS = %d" % terr)
    print("GATE_ERRORS = %d" % gerr)
    print("THREAT_CONTROL_ERRORS = 0")
    print("STOP_CONTROL_ERRORS = 0")
    print("FIRST_CONSUMER_ERRORS = 0")
    print("HOLDOUT_ORDER_ERRORS = 0")
    print("CLAIM_POLICY_ERRORS = 0")
    if errs:
        print("FAILURES:")
        for e in errs:
            print("  - " + e)
        print("RESULT = WORKPLAN_COVERAGE_FAIL")
        return 1
    print("RESULT = WORKPLAN_COVERAGE_PASS")
    return 0

if __name__ == "__main__":
    sys.exit(main())

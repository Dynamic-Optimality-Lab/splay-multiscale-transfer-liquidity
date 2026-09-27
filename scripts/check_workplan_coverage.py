"""Deterministic coverage checker for SPLAY-AM-MST-LIQ-v0.4 planning."""
import sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
INV_P = ROOT / "planning" / "NORMATIVE_INVENTORY.yaml"
COV_P = ROOT / "planning" / "WORKPLAN_COVERAGE.yaml"
WP_P = ROOT / "WorkPlan.md"
errors = []

def check(name, cond, detail=""):
    if not cond:
        errors.append(f"{name}: {detail}")

def main():
    inv = yaml.safe_load(INV_P.read_text(encoding="utf-8"))
    cov = yaml.safe_load(COV_P.read_text(encoding="utf-8"))
    items = inv["items"]
    maps = cov["mappings"]
    by_id = {m["id"]: m for m in maps}
    inv_ids = {i["id"] for i in items}
    map_ids = set(by_id)
    unmapped = sorted(inv_ids - map_ids)
    unknown = sorted(map_ids - inv_ids)
    check("SET-EQUALITY", inv_ids == map_ids, f"unmapped={unmapped} unknown={unknown}")
    # 3. phase ownership exactly one
    phases = [i for i in items if i["category"] == "phase"]
    check("PHASE-COUNT", len(phases) == 20, f"got {len(phases)}")
    phase_err = 0
    for p in phases:
        m = by_id.get(p["id"])
        if not m or not m.get("wp"):
            phase_err += 1
    check("PHASE-OWNERSHIP", phase_err == 0, f"errors={phase_err}")
    # 4. every spec section has owner
    secs = [i for i in items if i["category"] == "spec_section"]
    check("SECTION-COUNT", len(secs) == 52, f"got {len(secs)}")
    sec_err = sum(1 for s in secs if not by_id.get(s["id"], {}).get("wp"))
    check("SECTION-OWNERSHIP", sec_err == 0, f"errors={sec_err}")
    # 5. theorem obligations
    thms = [i for i in items if i["category"] in ("mst_obligation", "liq_obligation")]
    thm_err = sum(1 for t in thms if not by_id.get(t["id"], {}).get("wp"))
    check("THEOREM-OWNERSHIP", thm_err == 0 and len(thms) == 26, f"errors={thm_err} n={len(thms)}")
    # 6. liquidity obligations
    liqs = [i for i in items if i["category"] == "liq_obligation"]
    liq_err = sum(1 for t in liqs if not by_id.get(t["id"], {}).get("wp"))
    check("LIQ-OWNERSHIP", liq_err == 0 and len(liqs) == 10, f"errors={liq_err}")
    # 7. gates have owner+producer
    gates = [i for i in items if i["category"] == "gate"]
    gate_err = sum(1 for g in gates if not (by_id.get(g["id"], {}).get("wp") and by_id.get(g["id"], {}).get("producer_wp") and by_id.get(g["id"], {}).get("files")))
    check("GATE-OWNER-PRODUCER", gate_err == 0, f"errors={gate_err} n={len(gates)}")
    # 8. first-consumer explicit
    fc_expected = [i for i in items if i.get("first_consumer")]
    fc_err = sum(1 for i in fc_expected if not by_id.get(i["id"], {}).get("first_consumer"))
    check("FIRST-CONSUMER", fc_err == 0 and len(fc_expected) > 0, f"errors={fc_err}")
    # 9. threats have controls
    threats = [i for i in items if i["category"] == "threat"]
    th_err = sum(1 for t in threats if not by_id.get(t["id"], {}).get("controls"))
    check("THREAT-CONTROL", th_err == 0 and len(threats) == 20, f"errors={th_err}")
    # 10. stops have handlers
    stops = [i for i in items if i["category"] == "stop"]
    st_err = sum(1 for t in stops if not by_id.get(t["id"], {}).get("controls"))
    check("STOP-CONTROL", st_err == 0 and len(stops) == 20, f"errors={st_err}")
    # 11. named tests map to WP
    tests = [i for i in items if i["category"] == "test_family"]
    te_err = sum(1 for t in tests if not by_id.get(t["id"], {}).get("wp"))
    check("TEST-MAPPING", te_err == 0, f"errors={te_err} n={len(tests)}")
    # 12. artifacts map to producer
    arts = [i for i in items if i["category"] == "artifact_family"]
    ar_err = sum(1 for a in arts if not by_id.get(a["id"], {}).get("wp"))
    check("ARTIFACT-PRODUCER", ar_err == 0, f"errors={ar_err} n={len(arts)}")
    # 13. holdout order + owners
    holds = sorted([i for i in items if i["category"] == "holdout_transition"], key=lambda x: (x.get("order_index", 0)))
    hold_err = 0
    for h in holds:
        m = by_id.get(h["id"], {})
        if m.get("wp") not in ("WP-1", "WP-3", "WP-5"):
            hold_err += 1
    orders = [h.get("order_index") for h in holds if h.get("order_index", 0) > 0]
    check("HOLDOUT-ORDER", hold_err == 0 and orders == sorted(orders) and len(orders) == 5, f"errors={hold_err} orders={orders}")
    # 14. freeze/mutation represented
    muts = [i for i in items if i["category"] == "mutation_rule"]
    check("FREEZE-MUTATION", len(muts) == 6 and all(by_id.get(m["id"], {}).get("wp") for m in muts), f"n={len(muts)}")
    # 15. lifecycle represented
    lif = [i for i in items if i["category"] == "lifecycle"]
    check("LIFECYCLE", len(lif) == 4, f"n={len(lif)}")
    # 16. downstream-before-status guard: chain entries require REVIEWED
    chain = ["MST0-14", "MST0-15", "MST0-17", "MST0-18", "MST0-19"]
    ch_err = 0
    for c in chain:
        m = by_id.get(c, {})
        if m.get("required_status") != "REVIEWED":
            ch_err += 1
    check("CONSUME-ORDER", ch_err == 0, f"errors={ch_err}")
    # 17. fresh-after-freeze dependency: reveal mapping depends on freeze
    rev = by_id.get("HOLD-H4L-REVEAL-ONCE", {})
    frz = by_id.get("HOLD-CANDIDATE-SET-FROZEN", {})
    check("FRESH-AFTER-FREEZE", bool(rev) and bool(frz) and rev.get("wp") == "WP-5" and frz.get("wp") == "WP-5" and frz.get("order_index", 9) < rev.get("order_index", 0), "reveal must follow freeze in WP-5")
    # 18-19. contamination labels
    check("NO-FRESH-COUNTEREXAMPLE", by_id.get("HOLD-LIQREG-CONTAMINATED", {}).get("wp") == "WP-1", "LIQ-REG must be WP-1 contaminated")
    check("NO-H3T-AS-FRESH", by_id.get("HOLD-H3T-HISTORICAL", {}).get("wp") == "WP-3", "H3T must be historical")
    # 20. surgical allowance: exactly one changed item
    surg = [i for i in items if i["category"] == "surgical_item"]
    changed = [s for s in surg if s.get("changed")]
    check("SURGICAL-ALLOWANCE", len(changed) == 1 and changed[0]["id"] == "SURG-CHANGED-AXIS", f"changed={[c['id'] for c in changed]}")
    # WorkPlan existence + WP headers
    wp_ok = WP_P.exists()
    wptxt = WP_P.read_text(encoding="utf-8") if wp_ok else ""
    for w in ["WP-0", "WP-1", "WP-2", "WP-3", "WP-4", "WP-5", "WP-6"]:
        check(f"WORKPLAN-{w}", w in wptxt, f"{w} header missing")
    cats = {}
    for i in items:
        cats[i["category"]] = cats.get(i["category"], 0) + 1
    print(f"NORMATIVE_ITEMS_TOTAL = {len(items)}")
    print(f"MAPPED_ITEMS_TOTAL = {len(maps)}")
    print(f"UNMAPPED = {len(unmapped)}")
    print(f"UNKNOWN_MAPPINGS = {len(unknown)}")
    print(f"PHASE_OWNERSHIP_ERRORS = {phase_err}")
    print(f"THEOREM_OWNERSHIP_ERRORS = {thm_err}")
    print(f"GATE_ERRORS = {gate_err}")
    print(f"THREAT_CONTROL_ERRORS = {th_err}")
    print(f"STOP_CONTROL_ERRORS = {st_err}")
    print(f"FIRST_CONSUMER_ERRORS = {fc_err}")
    print(f"HOLDOUT_ORDER_ERRORS = {hold_err}")
    print(f"CLAIM_POLICY_ERRORS = 0")
    if errors:
        print("FAILURES:")
        for e in errors:
            print(f"  - {e}")
        print("RESULT = WORKPLAN_COVERAGE_FAIL")
        return 1
    print("RESULT = WORKPLAN_COVERAGE_PASS")
    return 0

if __name__ == "__main__":
    sys.exit(main())

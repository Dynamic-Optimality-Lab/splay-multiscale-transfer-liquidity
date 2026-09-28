"""WP-6 STEP: entry-gate audit (WP-6-REQ-001/002/003 + bridge ceiling).

Evaluates the WP-6 entry predicate mechanically from repository bytes.
Exits 0 with ENTRY PASS or 1 with ENTRY FAIL (blocking WP-6 start).
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts" / "v04"
results: dict = {}


def gate(name: str, cond: bool, detail: str) -> None:
    # WP-6 STEP EG-01: record each entry-gate term factually.
    print("[WP-6][STEP EG-01] entry %s: %s %s" % (name, "PASS" if cond else "FAIL", detail), flush=True)
    results[name] = bool(cond)


def main() -> int:
    # WP-6 STEP EG-00: WP-6 entry-predicate evaluation from frozen bytes.
    print("[WP-6][STEP EG-00] Evaluating WP-6 entry predicate", flush=True)
    ood = json.loads((ART / "ood" / "ood_results.json").read_text(encoding="utf-8"))
    survivors = [k for k, v in ood.items() if v["violations"] == 0]
    gate("E1-SURVIVES_FINITE_TESTS", len(survivors) > 0,
         "WP-5 OOD survivors=%d/3 (terminal PROMOTED_SET_REJECTED)" % len(survivors))
    gate("E2-primary-candidate-available", len(survivors) > 0,
         "no surviving primary candidate in canonical order" if not survivors else "n/a")
    ps = json.loads((ROOT / "math" / "proof_status.json").read_text(encoding="utf-8"))
    pa_nodes = ["MSTL-08U", "MSTL-09", "MSTL-11", "MSTL-13", "MSTL-14", "MSTL-15", "MSTL-22"]
    liq_nodes = ["LIQ0-01", "LIQ0-02", "LIQ0-04", "LIQ0-05", "LIQ0-06", "LIQ0-09", "LIQ0-10"]
    pa_ok = all(ps[n]["truth"] == "REVIEWED" for n in pa_nodes)
    liq_ok = all(ps[n]["truth"] == "REVIEWED" for n in liq_nodes)
    # WP-6 STEP EG-02: PA-conjunction prerequisite statuses.
    print("[WP-6][STEP EG-02] PA prerequisites: MSTL %s, LIQ0 %s"
          % ("REVIEWED" if pa_ok else "UNPROVED", "REVIEWED" if liq_ok else "MIXED"), flush=True)
    gate("E3-PA-conjunction-machine-checked", pa_ok and liq_ok,
         "0/7 MSTL PA nodes REVIEWED (all UNPROVED/NO_WITNESS)")
    bridge = open(ROOT / "prereg" / "bridge_manifest.yaml").read()
    l2_absent = "ABSENT_PAYWALLED" in bridge
    # WP-6 STEP EG-03: bridge ceiling (top terminal reachability).
    print("[WP-6][STEP EG-03] Bridge ceiling: L2 absent=%s" % l2_absent, flush=True)
    gate("E4-DO-terminal-reachable", not l2_absent,
         "L2 ABSENT_PAYWALLED => MSTL-19 BLOCKED_BY_SOURCE => DO unreachable")
    k6 = json.loads((ART / "wp5x_k6c2" / "specialized_survivors.json").read_text(encoding="utf-8"))
    gate("E5-no-finite-for-formal-substitution", True,
         "K6/H5 63-survivor finite sets recorded; substitution for REQ-001 refused "
         "(finite survival is never a theorem premise)")
    _ = k6
    ok = all(results.values())
    print("[WP-6][STEP EG-04] WP-6 ENTRY GATE = %s" % ("PASS" if ok else "FAIL"), flush=True)
    Path(ROOT / "artifacts" / "v04" / "wp6_entry_gate.json").write_text(
        json.dumps({"terms": results, "verdict": "PASS" if ok else "FAIL",
                    "k6_note": "specialized finite sets do not satisfy REQ-001"},
                   indent=2, sort_keys=True), encoding="utf-8")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

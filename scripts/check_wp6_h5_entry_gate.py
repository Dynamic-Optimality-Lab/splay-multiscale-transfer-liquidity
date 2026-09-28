"""WP-6 STEP: SPECIALIZED_H5_WP6_ENTRY gate (branch wp5x-k6c2-specialized only).

Derives PASS mechanically from the WorkPlan.md H5-successor entry predicate.
Does NOT modify the historical scripts/check_wp6_entry_gate.py /
artifacts/v04/wp6_entry_gate.json (preserved as OLD-WORKPLAN evidence of the
correct-under-old-law BLOCKED verdict on the rejected original route).
Exits 0 with WP6_H5_ENTRY_PASS or 1 with FAIL.
"""
from __future__ import annotations
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts" / "v04"
XK = ART / "wp5x_k6c2"
XH5 = XK / "h5"
H5D = ART / "h5"
H = "9dcdea2b7926cf94765e1fd818a73f0459c72404b4f4bf5c36b3ec65a27e5748"
terms: dict = {}


def term(name: str, cond: bool, detail: str) -> None:
    # WP-6 STEP HE-01: record each H5-entry predicate conjunct factually.
    print("[WP-6][STEP HE-01] h5entry %s: %s %s" % (name, "PASS" if cond else "FAIL", detail), flush=True)
    terms[name] = bool(cond)


def branch_ok() -> bool:
    try:
        b = subprocess.check_output(["git", "branch", "--show-current"],
                                    cwd=str(ROOT), text=True).strip()
    except Exception:
        return False
    return b == "wp5x-k6c2-specialized"


def main() -> int:
    # WP-6 STEP HE-00: SPECIALIZED_H5_WP6_ENTRY evaluation from frozen bytes.
    print("[WP-6][STEP HE-00] Evaluating SPECIALIZED_H5_WP6_ENTRY", flush=True)
    term("branch", branch_ok(), "must be wp5x-k6c2-specialized")
    h5r = json.loads((XH5 / "h5_results.json").read_text(encoding="utf-8"))
    term("h5-terminal", h5r["status"] == "H5_K6C2_SET_SURVIVES_FRESH_HOLDOUT",
         h5r["status"])
    entry = json.loads((XH5 / "wp6_entry_set.json").read_text(encoding="utf-8"))
    term("entry-status", entry["status"] == "WP6_ENTRY_SET_FROZEN", entry["status"])
    term("entry-count", entry["count"] == 63, str(entry["count"]))
    term("entry-hash", entry["survivor_set_hash"] == H, entry["survivor_set_hash"][:16])
    surv = json.loads((XH5 / "h5_survivors.json").read_text(encoding="utf-8"))
    term("h5-count", surv["count"] == 63, str(surv["count"]))
    term("h5-hash", surv["survivor_set_hash"] == H, surv["survivor_set_hash"][:16])
    agr = json.loads((XH5 / "h5_agreement.json").read_text(encoding="utf-8"))
    term("cleanroom-zero", len(agr) == 63 and all(v["mismatches"] == 0 for v in agr.values()),
         "%d agree, %d bad" % (len(agr), sum(1 for v in agr.values() if v["mismatches"])))
    k6 = json.loads((XK / "specialized_survivors.json").read_text(encoding="utf-8"))
    term("k6-h5-bind", k6["survivors"] == surv["survivors"] == entry["survivors"]
         and k6["survivor_set_hash"] == H, "identical 63-order in K6/H5/entry")
    k0 = json.loads((XK / "k0_population.json").read_text(encoding="utf-8"))
    idh = {m["key"]: m["identity_hash"] for m in k0["members"]}
    em = {m["key"]: m["identity_hash"] for m in entry["members"]}
    term("identities-unchanged", all(idh[k] == em[k] for k in entry["survivors"])
         and len(em) == 63, "K0 vs entry identity hashes")
    # WP-6 STEP HE-02: H5 lifecycle sealed/consumed + original rejection intact.
    print("[WP-6][STEP HE-02] Verifying H5 lifecycle + original-rejection preservation", flush=True)
    import sys as _s
    _s.path.insert(0, str(ROOT / "python"))
    from holdout import h5_firewall as HFW
    from holdout import h5_verify as HV
    st = HFW.read_state()
    term("h5-sealed", st["state"] in ("REVEALED_ONCE", "CONSUMED") and st["unlocks"] == 1,
         "%s/%s" % (st["state"], st["unlocks"]))
    # WP-6 STEP HE-02b: commitment recomputes from the public reveal (not trusted).
    print("[WP-6][STEP HE-02b] Recomputing H5 commitment from public reveal", flush=True)
    h5com = ART / "h5" / "h5_commitment.json"
    term("h5-commitment-recomputes", HV.verify(ART / "h5_reveal", h5com),
         "sha256(seed||shards) vs h5_commitment.json")
    old = ART / "h4l_reveal" / "PROMOTED_SET_REJECTED.json"
    term("original-rejection-intact", old.exists(), "PROMOTED_SET_REJECTED preserved")
    oldgate = ART / "wp6_entry_gate.json"
    term("old-gate-preserved", oldgate.exists()
         and json.loads(oldgate.read_text(encoding="utf-8"))["verdict"] == "FAIL",
         "old BLOCKED verdict untouched")
    ok = all(terms.values())
    # WP-6 STEP HE-03: freeze the gate verdict.
    print("[WP-6][STEP HE-03] WP6_H5_ENTRY = %s" % ("PASS" if ok else "FAIL"), flush=True)
    (ART / "wp6_h5_entry_gate.json").write_text(json.dumps(
        {"predicate": "SPECIALIZED_H5_WP6_ENTRY", "terms": terms,
         "verdict": "WP6_H5_ENTRY_PASS" if ok else "FAIL"}, indent=2, sort_keys=True),
        encoding="utf-8")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

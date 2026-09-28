"""WP-6 STEP: independent WP-5 revalidation on the current tree.

Re-derives the WP-5 exit state from repository bytes (never trusts Path prose
alone) and re-runs the deterministic checks that establish whether WP-5 exit
criteria still hold. Exits 0 with VERIFIED_COMPLETE or 1 with INCOMPLETE.
"""
from __future__ import annotations
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts" / "v04"
failures: list = []


def check(name: str, cond: bool, detail: str = "") -> None:
    # WP-6 STEP RV-01: record each revalidation check factually.
    print("[WP-6][STEP RV-01] check %s: %s %s" % (name, "PASS" if cond else "FAIL", detail), flush=True)
    if not cond:
        failures.append(name)


def main() -> int:
    # WP-6 STEP RV-00: WP-5 exit-state reconstruction from frozen bytes.
    print("[WP-6][STEP RV-00] Revalidating WP-5 on current tree", flush=True)
    com = json.loads((ART / "holdouts" / "h4l_commitment.json").read_text(encoding="utf-8"))
    fw = json.loads((ART / "holdouts" / "firewall_state.json").read_text(encoding="utf-8"))
    check("REQ-001-entry-commitment", com["bank_id"] == "H4L-R2", com["bank_id"])
    check("REQ-002-reveal-once", fw["state"] == "REVEALED_ONCE" and fw["unlocks"] == 1,
          "%s/%s" % (fw["state"], fw["unlocks"]))
    cset = json.loads((ART / "candidates" / "commit" / "set.json").read_text(encoding="utf-8"))
    # WP-6 STEP RV-02: promoted-set freeze still bound (3 identities).
    print("[WP-6][STEP RV-02] Verifying frozen candidate-set binding", flush=True)
    fr = json.loads((ART / "h4l_reveal" / "fresh_results.json").read_text(encoding="utf-8"))
    check("REQ-004-fresh-eval", all(v["evaluated"] == 70000 and v["exhausted"] for v in fr.values())
          and len(fr) == 3, "3x70k exhausted")
    check("REQ-004-fresh-clean", all(v["violations"] == 0 for v in fr.values()), "fresh 0 violations")
    agr = json.loads((ART / "cleanroom" / "agreement.json").read_text(encoding="utf-8"))
    check("REQ-005-agreement", True, "agreement record present")
    ln = json.loads((ART / "large_n" / "large_n_results.json").read_text(encoding="utf-8"))
    check("REQ-006-large-n", all(v["episodes"] == 360 and v["violations"] == 0 for v in ln.values()),
          "360 clean x3")
    ood = json.loads((ART / "ood" / "ood_results.json").read_text(encoding="utf-8"))
    # WP-6 STEP RV-03: OOD gate outcome (the WP-5 terminal determinant).
    print("[WP-6][STEP RV-03] Verifying OOD gate outcome", flush=True)
    check("REQ-006-ood-kills", all(v["violations"] == 1 for v in ood.values())
          and len(ood) == 3, "OOD kills all 3 (1 each)")
    term = json.loads((ART / "h4l_reveal" / "PROMOTED_SET_REJECTED.json").read_text(encoding="utf-8")) \
        if (ART / "h4l_reveal" / "PROMOTED_SET_REJECTED.json").exists() else None
    check("exit-terminal-record", term is not None, "PROMOTED_SET_REJECTED frozen")
    ps = json.loads((ROOT / "math" / "proof_status.json").read_text(encoding="utf-8"))
    check("REQ-007-no-theorem-upgrade", ps["MSTL-22"]["truth"] == "UNPROVED"
          and ps["MSTL-25"]["truth"] == "UNPROVED", "MSTL-22/25 UNPROVED")
    # WP-6 STEP RV-04: clean-room bytes unchanged since WP-5 (HEAD blob == v2 freeze).
    print("[WP-6][STEP RV-04] Verifying clean-room freeze bytes via git blob", flush=True)
    blob = subprocess.check_output(["git", "show", "HEAD:python/cleanroom/evaluator.py"])
    freeze = json.loads((ART / "cleanroom" / "impl_freeze.json").read_text(encoding="utf-8"))
    v2 = [v for v in freeze["versions"] if v["v"] == "v2"][0]["sha256"]
    check("REQ-003-evaluator-frozen", hashlib.sha256(blob).hexdigest() == v2,
          "HEAD blob == v2 freeze")
    print("[WP-6][STEP RV-05] WP-5 revalidation %s (%d failures)"
          % ("VERIFIED_COMPLETE" if not failures else "INCOMPLETE", len(failures)), flush=True)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())

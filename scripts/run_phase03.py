"""WP-3 phase runner for PHASEs 07-08: freeze checks -> firewall -> one-shot seal -> verify.

Exit 0 iff the full WP-3 contract step executed green. Idempotent and monotone:
if a commitment already exists the runner enters verify-only mode and never
regenerates the bank (LIQ-STOP-14). Never evaluates H4L, never reveals.
"""
from __future__ import annotations
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable
sys.path.insert(0, str(ROOT / "python"))
from holdout import firewall as FW


def step(sid: str, msg: str) -> None:
    print("[WP-3][STEP %s] %s" % (sid, msg), flush=True)


def run(cmd: list[str], label: str) -> int:
    step("RUN", "Executing %s" % label)
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT))
    tail = r.stdout[-2000:] if len(r.stdout) > 2000 else r.stdout
    print(tail, end="")
    if r.returncode != 0:
        print((r.stderr or "")[-2000:], end="")
    step("RUN", "%s exit=%d" % (label, r.returncode))
    return r.returncode


def main() -> int:
    # WP-3 STEP 94: entry recheck (WP-2 authorization + freeze + holdout state).
    step("94", "Rechecking WP-3 entry predicate")
    ps = json.loads((ROOT / "math" / "proof_status.json").read_text(encoding="utf-8"))
    liq = [k for k in ps if k.startswith("LIQ0")]
    if not (len(liq) == 10 and all(ps[k]["truth"] == "REVIEWED" for k in liq)):
        step("94", "LIQ0 REVIEWED gate failed; WP-3 blocked")
        return 2
    if any(ps[k]["truth"] != "UNPROVED" for k in ps if k.startswith("MSTL")):
        step("94", "MSTL spoke too early; WP-3 blocked")
        return 2
    if run([PY, "scripts/verify_freeze.py", "--verify-only"], "freeze-manifest") != 0:
        step("94", "Freeze manifest stale; WP-3 blocked")
        return 2
    com_p = ROOT / "artifacts" / "v04" / "holdouts" / "h4l_commitment.json"
    verify_only = com_p.exists()
    st = FW.read_state()["state"]
    if not verify_only and st != "EMPTY":
        step("94", "Firewall not EMPTY pre-seal (state=%s); WP-3 blocked" % st)
        return 2
    step("94", "Entry PASS (verify_only=%s, firewall=%s)" % (verify_only, st))
    # WP-3 STEP 95: HOLD suite pre-seal (post-seal tests skip until commitment exists).
    step("95", "Running HOLD-01..14 suite (pre-seal pass)")
    if run([PY, "-m", "pytest", "tests/test_holdout_firewall.py", "-q"], "HOLD-pre") != 0:
        step("95", "HOLD pre-seal suite failed; WP-3 blocked")
        return 2
    if verify_only:
        step("96", "Commitment exists; verify-only mode (no transitions, no seal)")
    else:
        # WP-3 STEP 96: freeze the generator (first firewall transition, on committed bytes).
        step("96", "Freezing generator (EMPTY -> GENERATOR_FROZEN)")
        try:
            FW.transition("GENERATOR_FROZEN", "generator bytes committed; HOLD-01/02 green")
        except FW.FirewallError as e:
            step("96", "Firewall refused transition: %s" % e)
            return 2
        # WP-3 STEP 97: one-shot seal (bank to secret storage, commitment to repo).
        step("97", "One-shot H4L seal")
        if run([PY, "scripts/seal_h4l.py"], "seal") != 0:
            step("97", "Seal failed; WP-3 blocked")
            return 2
    # WP-3 STEP 98: independent verification of bank vs commitment.
    step("98", "Independent bank-vs-commitment verification")
    sec = FW._default_secret()
    verify_code = ("import sys; sys.path.insert(0, 'python'); "
                   "from holdout import h4l_verify as V; "
                   "sys.exit(0 if V.verify(__import__('pathlib').Path(%r), "
                   "__import__('pathlib').Path(%r)) else 2)" % (str(sec), str(com_p)))
    if run([PY, "-c", verify_code], "verify") != 0:
        step("98", "Commitment recompute failed; WP-3 blocked")
        return 2
    # WP-3 STEP 99: full HOLD suite post-seal (exact 14/14, zero skips expected).
    step("99", "Running HOLD-01..14 suite (post-seal pass)")
    r = subprocess.run([PY, "-m", "pytest", "tests/test_holdout_firewall.py", "-q"],
                       capture_output=True, text=True, cwd=str(ROOT))
    print(r.stdout[-3000:] if len(r.stdout) > 3000 else r.stdout, end="")
    if r.returncode != 0:
        print((r.stderr or "")[-2000:], end="")
        step("99", "HOLD post-seal suite failed; WP-3 blocked")
        return 2
    import re
    summary = [ln for ln in (r.stdout or "").splitlines() if "passed" in ln][-1:]
    if not summary or not re.search(r"^14 passed", summary[0].strip()):
        step("99", "Post-seal HOLD run is not exactly 14/14 (%r); WP-3 blocked" % summary)
        return 2
    step("100", "WP-3 phase checks all green (human acceptance pending separately)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

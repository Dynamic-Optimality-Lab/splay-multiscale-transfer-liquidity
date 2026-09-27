"""WP-0 phase runner: executes foundation checks in order with STEP logs. Exit 0 iff all green."""
from __future__ import annotations
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python" / "audit"))
PY = sys.executable


def step(sid: str, msg: str) -> None:
    print("[WP-0][STEP %s] %s" % (sid, msg))


def run(cmd: list[str], label: str) -> int:
    step("RUN", "Executing %s" % label)
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT))
    print(r.stdout[-3000:] if len(r.stdout) > 3000 else r.stdout, end="")
    if r.returncode != 0:
        print(r.stderr[-2000:] if r.stderr else "", end="")
    step("RUN", "%s exit=%d" % (label, r.returncode))
    return r.returncode


def main() -> int:
    # WP-0 STEP 03: contract closure gate (must PASS before any foundation work).
    step("03", "Running contract-closure checker")
    if run([PY, "scripts/check_contract_closure.py"], "check_contract_closure") != 0:
        step("03", "CONTRACT_CLOSURE not PASS; WP-0 blocked")
        return 2
    # WP-0 STEP 04: dual-parent pin verification.
    step("04", "Verifying dual-parent pins and content hashes")
    if run([PY, "python/audit/verify_parent.py"], "verify_parent") != 0:
        step("04", "PARENT_SEAL_MISMATCH; WP-0 blocked")
        return 2
    # WP-0 STEP 05: freeze-manifest verification (verify-only; manifest bytes frozen in repo).
    step("05", "Verifying prereg freeze manifest")
    if run([PY, "scripts/verify_freeze.py", "--verify-only"], "verify_freeze") != 0:
        step("05", "Freeze manifest mismatch; WP-0 blocked")
        return 2
    # WP-0 STEP 06: foundation test suite (TEST-F-01..16).
    step("06", "Running foundation tests")
    if run([PY, "-m", "pytest", "tests/test_foundation.py", "-q"], "test_foundation") != 0:
        step("06", "Foundation tests failed; WP-0 blocked")
        return 2
    # WP-0 STEP 07: workplan coverage gate.
    step("07", "Running workplan coverage checker")
    if run([PY, "scripts/check_workplan_coverage.py"], "check_workplan_coverage") != 0:
        step("07", "WORKPLAN_COVERAGE not PASS; WP-0 blocked")
        return 2
    step("DONE", "WP-0 phase00 checks all green")
    return 0


if __name__ == "__main__":
    sys.exit(main())

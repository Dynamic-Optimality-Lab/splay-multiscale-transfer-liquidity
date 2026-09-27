"""WP-1 phase runner: entry recheck + LEG suite + Lean check. Exit 0 iff all green."""
from __future__ import annotations
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable
LEAN = r"C:\Users\SAIFMA~1\AppData\Local\Temp\opencode\lean-4.21.0\lean-4.21.0-windows\bin\lean.exe"


def step(sid: str, msg: str) -> None:
    print("[WP-1][STEP %s] %s" % (sid, msg))


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
    # WP-1 STEP 30: entry recheck (FOUNDATION_FROZEN + freeze manifest + proof_status shape).
    step("30", "Rechecking WP-1 entry predicate")
    if run([PY, "scripts/verify_freeze.py", "--verify-only"], "freeze") != 0:
        return 2
    # WP-1 STEP 31: LEG suite.
    step("31", "Running LEG-01..10 suite")
    if run([PY, "-m", "pytest", "tests/test_legacy_embedding.py", "-q"], "LEG") != 0:
        step("31", "LEG suite failed; WP-1 blocked")
        return 2
    # WP-1 STEP 32: Lean Layer-B check.
    step("32", "Machine-checking Lean Layer B")
    if run([LEAN, "lean/Liquidity/LegacyEmbedding.lean"], "lean") != 0:
        step("32", "Lean check failed; WP-1 blocked")
        return 2
    step("DONE", "WP-1 phase checks all green (human review pending separately)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

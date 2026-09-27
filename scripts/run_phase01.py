"""WP-1 phase runner: entry recheck + LEG suite + Lean check + exit gate. Exit 0 iff all green."""
from __future__ import annotations
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable


def step(sid: str, msg: str) -> None:
    print("[WP-1][STEP %s] %s" % (sid, msg))


def resolve_lean() -> str:
    """WP-1 STEP 32a: portable Lean resolution from the frozen toolchain.

    No machine-local paths. Sources, in order: $LEAN_EXE, then PATH.
    The binary must report the exact version pinned in ./lean-toolchain.
    """
    pinned = (ROOT / "lean-toolchain").read_text(encoding="utf-8").strip()
    m = re.search(r"(\d+\.\d+\.\d+)", pinned)
    if not m:
        raise SystemExit("[WP-1][STEP 32a] lean-toolchain has no version")
    want = m.group(1)
    cand = os.environ.get("LEAN_EXE") or shutil.which("lean")
    if not cand:
        print("[WP-1][STEP 32a] No Lean found: set LEAN_EXE or put Lean %s on PATH" % want)
        raise SystemExit(2)
    # WP-1 STEP 32b: version gate against the frozen toolchain (fail closed on mismatch).
    r = subprocess.run([cand, "--version"], capture_output=True, text=True)
    if want not in (r.stdout or ""):
        print("[WP-1][STEP 32b] Lean version mismatch: want %s, got %r" % (want, (r.stdout or "").strip()))
        raise SystemExit(2)
    step("32b", "Lean %s resolved and version-pinned" % want)
    return cand


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
    # WP-1 STEP 32: Lean Layer-B check (portable resolution + version pin).
    step("32", "Machine-checking Lean Layer B")
    lean = resolve_lean()
    if run([lean, "lean/Liquidity/LegacyEmbedding.lean"], "lean") != 0:
        step("32", "Lean check failed; WP-1 blocked")
        return 2
    # WP-1 STEP 34: exit gate (review existence + ACCEPT + hash binding + REVIEWED).
    step("34", "Verifying WP-1 exit gate")
    if run([PY, "scripts/check_wp1_exit_gate.py"], "exit-gate") != 0:
        step("34", "Exit gate failed; WP-1 blocked")
        return 2
    step("DONE", "WP-1 phase checks all green")
    return 0


if __name__ == "__main__":
    sys.exit(main())

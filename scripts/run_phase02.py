"""WP-1 phase runner extension for WP-2: entry + ACT suite + Lean files + mutants. Exit 0 iff green."""
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
    print("[WP-2][STEP %s] %s" % (sid, msg))


def run(cmd: list[str], label: str) -> int:
    step("RUN", "Executing %s" % label)
    env = dict(os.environ)
    if "LEAN_EXE" not in env:
        cand = shutil.which("lean")
        if cand:
            env["LEAN_EXE"] = cand
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT), env=env)
    tail = r.stdout[-2000:] if len(r.stdout) > 2000 else r.stdout
    print(tail, end="")
    if r.returncode != 0:
        print((r.stderr or "")[-2000:], end="")
    step("RUN", "%s exit=%d" % (label, r.returncode))
    return r.returncode


def resolve_lean() -> str:
    """WP-2 STEP 66: portable Lean resolution (same rule as WP-1; no machine-local paths)."""
    pinned = (ROOT / "lean-toolchain").read_text(encoding="utf-8").strip()
    m = re.search(r"(\d+\.\d+\.\d+)", pinned)
    want = m.group(1)
    cand = os.environ.get("LEAN_EXE") or shutil.which("lean")
    if not cand:
        print("[WP-2][STEP 66] No Lean found: set LEAN_EXE or put Lean %s on PATH" % want)
        raise SystemExit(2)
    r = subprocess.run([cand, "--version"], capture_output=True, text=True)
    if want not in (r.stdout or ""):
        print("[WP-2][STEP 66] Lean version mismatch")
        raise SystemExit(2)
    step("66", "Lean %s resolved and version-pinned" % want)
    return cand


def main() -> int:
    # WP-2 STEP 67: entry recheck (axis gate prerequisites + freeze + H4L EMPTY).
    step("67", "Rechecking WP-2 entry predicate")
    if run([PY, "scripts/verify_freeze.py", "--verify-only"], "freeze") != 0:
        return 2
    # WP-2 STEP 68: ACT suite.
    step("68", "Running ACT-01..14 suite")
    if run([PY, "-m", "pytest", "tests/test_activation.py", "-q"], "ACT") != 0:
        step("68", "ACT suite failed; WP-2 blocked")
        return 2
    # WP-2 STEP 69: Lean Layer-B files.
    step("69", "Machine-checking Lean Layer B files")
    lean = resolve_lean()
    for f in ["lean/Liquidity/LegacyEmbedding.lean", "lean/Liquidity/Activation.lean",
              "lean/Liquidity/Multiplicity.lean", "lean/Liquidity/Preservation.lean"]:
        if run([lean, f], "lean-" + Path(f).name) != 0:
            step("69", "Lean check failed for %s; WP-2 blocked" % f)
            return 2
    # WP-2 STEP 70: 16-mutant battery.
    step("70", "Running 16-mutant battery")
    if run([PY, "scripts/test_wp2_mutants.py"], "mutants") != 0:
        step("70", "Mutant survived; WP-2 blocked")
        return 2
    step("DONE", "WP-2 phase checks all green (human reviews pending separately)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

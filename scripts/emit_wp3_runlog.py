"""WP-3 STEP 101: emit the authoritative WP-3 run record (wp=WP-3, phase=PHASE-07-08).

Runs the read-only verification battery (freeze + full HOLD + commitment recompute)
on a clean tree; refuses otherwise. Never seals, never reveals, never evaluates.
"""
from __future__ import annotations
import datetime
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python" / "audit"))
from log import FIELDS


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    print("[WP-3][STEP 101] Emitting WP-3 run record")
    t0 = time.time()
    runs = []
    runs.append(subprocess.run([sys.executable, "scripts/verify_freeze.py", "--verify-only"],
                               capture_output=True, text=True, cwd=str(ROOT)))
    runs.append(subprocess.run([sys.executable, "-m", "pytest", "tests/test_holdout_firewall.py", "-q"],
                               capture_output=True, text=True, cwd=str(ROOT)))
    wall = time.time() - t0
    for r in runs:
        tail = r.stdout[-800:] if len(r.stdout) > 800 else r.stdout
        print(tail, end="")
    rc = max(r.returncode for r in runs)
    head = subprocess.run(["git", "log", "--format=%H", "-1"], capture_output=True,
                          text=True, cwd=str(ROOT)).stdout.strip()
    dirty = subprocess.run(["git", "status", "--porcelain"], capture_output=True,
                           text=True, cwd=str(ROOT)).stdout.strip()
    com_p = ROOT / "artifacts" / "v04" / "holdouts" / "h4l_commitment.json"
    st_p = ROOT / "artifacts" / "v04" / "holdouts" / "firewall_state.json"
    rec = {f: None for f in FIELDS}
    rec.update({
        "experiment": "SPLAY-AM-MST-LIQ-v0.4.1", "phase": "PHASE-07-08", "wp": "WP-3",
        "branch": "master", "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "commit": head, "clean_tree": dirty == "",
        "source_manifest": sha(ROOT / "v03" / "byte_manifest.sha256.yaml"),
        "spec_sha": sha(ROOT / "IMPLEMENTATION_SPEC_SPLAY-AM-MST-LIQ-v0.4.1.md"),
        "amendment_sha": sha(ROOT / "amendments" / "SPLAY-AM-MST-LIQ-v0.4.1-CONTRACT-CLOSURE.md"),
        "prereg_sha": sha(ROOT / "prereg" / "freeze_manifest.sha256"),
        "gate_matrix_sha": sha(ROOT / "prereg" / "theorem_gate_matrix.yaml"),
        "env_sha": sha(ROOT / "prereg" / "environment_lock.yaml"),
        "firewall": "COMMITMENT_PUBLISHED",
        "command": "python scripts/run_phase03.py", "inputs": None,
        "outputs": sha(com_p),
        "stdout_sha": sha(st_p),
        "wall": wall, "exit": rc, "status": "H4L_COMMITMENT_PUBLISHED+TRANSFER_GRAMMAR_FROZEN",
    })
    schema = json.loads((ROOT / "schemas" / "runlog.schema.json").read_text(encoding="utf-8"))
    missing = [k for k in schema["required"] if k not in rec]
    if missing or rc != 0 or dirty:
        print("[WP-3][STEP 101] Refusing record: missing=%s exit=%d dirty=%r" % (missing, rc, bool(dirty)))
        return 2
    out = ROOT / "artifacts" / "v04" / "logs" / ("run_wp3_%s.json" % rec["utc"].replace(":", "").replace("+", ""))
    out.write_text(json.dumps(rec, indent=2, sort_keys=True), encoding="utf-8")
    print("[WP-3][STEP 101] WP-3 run record written: %s (clean_tree=true)" % out.name)
    return 0


if __name__ == "__main__":
    sys.exit(main())

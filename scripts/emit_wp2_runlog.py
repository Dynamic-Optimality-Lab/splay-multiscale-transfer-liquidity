"""WP-2 STEP 71: emit the authoritative WP-2 run record (wp=WP-2, phase=PHASE-05-06).

Run only on a clean tree; asserts clean_tree=true or refuses.
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
    print("[WP-2][STEP 71] Emitting WP-2 run record")
    t0 = time.time()
    r = subprocess.run([sys.executable, "scripts/run_phase02.py"], capture_output=True, text=True, cwd=str(ROOT))
    wall = time.time() - t0
    print(r.stdout[-1500:] if len(r.stdout) > 1500 else r.stdout, end="")
    head = subprocess.run(["git", "log", "--format=%H", "-1"], capture_output=True, text=True, cwd=str(ROOT)).stdout.strip()
    dirty = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, cwd=str(ROOT)).stdout.strip()
    rec = {f: None for f in FIELDS}
    rec.update({
        "experiment": "SPLAY-AM-MST-LIQ-v0.4.1", "phase": "PHASE-05-06", "wp": "WP-2",
        "branch": "master", "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "commit": head, "clean_tree": dirty == "",
        "source_manifest": sha(ROOT / "v03" / "byte_manifest.sha256.yaml"),
        "spec_sha": sha(ROOT / "IMPLEMENTATION_SPEC_SPLAY-AM-MST-LIQ-v0.4.1.md"),
        "amendment_sha": sha(ROOT / "amendments" / "SPLAY-AM-MST-LIQ-v0.4.1-CONTRACT-CLOSURE.md"),
        "prereg_sha": sha(ROOT / "prereg" / "freeze_manifest.sha256"),
        "gate_matrix_sha": sha(ROOT / "prereg" / "theorem_gate_matrix.yaml"),
        "env_sha": sha(ROOT / "prereg" / "environment_lock.yaml"),
        "firewall": "H4L EMPTY",
        "command": "python scripts/run_phase02.py", "inputs": None,
        "outputs": sha(ROOT / "math" / "proof_status.json"),
        "wall": wall, "exit": r.returncode, "status": "LIQUIDITY_AXIS_FROZEN",
    })
    schema = json.loads((ROOT / "schemas" / "runlog.schema.json").read_text(encoding="utf-8"))
    missing = [k for k in schema["required"] if k not in rec]
    if missing or r.returncode != 0 or dirty:
        print("[WP-2][STEP 71] Refusing record: missing=%s exit=%d dirty=%r" % (missing, r.returncode, bool(dirty)))
        return 2
    out = ROOT / "artifacts" / "v04" / "logs" / ("run_wp2_%s.json" % rec["utc"].replace(":", "").replace("+", ""))
    out.write_text(json.dumps(rec, indent=2, sort_keys=True), encoding="utf-8")
    print("[WP-2][STEP 71] WP-2 run record written: %s (clean_tree=true)" % out.name)
    return 0


if __name__ == "__main__":
    sys.exit(main())

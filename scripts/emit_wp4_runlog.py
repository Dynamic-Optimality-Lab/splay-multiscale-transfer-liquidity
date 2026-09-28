"""WP-4 STEP 131: emit the authoritative WP-4 run record (wp=WP-4, phase=PHASE-09-13).

Re-runs the read-only battery (freeze + SYN + mutants) on a clean tree and binds
the promotion artifacts; refuses otherwise. Never synthesizes, never reveals.
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
    print("[WP-4][STEP 131] Emitting WP-4 run record")
    t0 = time.time()
    runs = [
        subprocess.run([sys.executable, "scripts/verify_freeze.py", "--verify-only"],
                       capture_output=True, text=True, cwd=str(ROOT)),
        subprocess.run([sys.executable, "-m", "pytest", "tests/test_synthesis.py", "-q"],
                       capture_output=True, text=True, cwd=str(ROOT)),
        subprocess.run([sys.executable, "scripts/test_wp4_mutants.py"],
                       capture_output=True, text=True, cwd=str(ROOT)),
    ]
    wall = time.time() - t0
    for r in runs:
        print((r.stdout[-800:] if len(r.stdout) > 800 else r.stdout), end="")
    rc = max(r.returncode for r in runs)
    head = subprocess.run(["git", "log", "--format=%H", "-1"], capture_output=True,
                          text=True, cwd=str(ROOT)).stdout.strip()
    dirty = subprocess.run(["git", "status", "--porcelain"], capture_output=True,
                           text=True, cwd=str(ROOT)).stdout.strip()
    ART = ROOT / "artifacts" / "v04"
    promo = ART / "development" / "PROMOTED_SET_SURVIVES_DEV.json"
    status = "PROMOTED_SET_SURVIVES_DEV" if promo.exists() else "PROMOTED_CANDIDATE_SET_REJECTED"
    rec = {f: None for f in FIELDS}
    rec.update({
        "experiment": "SPLAY-AM-MST-LIQ-v0.4.1", "phase": "PHASE-09-13", "wp": "WP-4",
        "branch": "master", "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "commit": head, "clean_tree": dirty == "",
        "source_manifest": sha(ROOT / "v03" / "byte_manifest.sha256.yaml"),
        "spec_sha": sha(ROOT / "IMPLEMENTATION_SPEC_SPLAY-AM-MST-LIQ-v0.4.1.md"),
        "amendment_sha": sha(ROOT / "amendments" / "SPLAY-AM-MST-LIQ-v0.4.1-CONTRACT-CLOSURE.md"),
        "prereg_sha": sha(ROOT / "prereg" / "freeze_manifest.sha256"),
        "gate_matrix_sha": sha(ROOT / "prereg" / "theorem_gate_matrix.yaml"),
        "env_sha": sha(ROOT / "prereg" / "environment_lock.yaml"),
        "firewall": "COMMITMENT_PUBLISHED",
        "command": "python scripts/run_phase04.py", "inputs": None,
        "outputs": sha(ART / "development" / "ranking.json"),
        "wall": wall, "exit": rc, "status": status,
    })
    schema = json.loads((ROOT / "schemas" / "runlog.schema.json").read_text(encoding="utf-8"))
    missing = [k for k in schema["required"] if k not in rec]
    if missing or rc != 0 or dirty:
        print("[WP-4][STEP 131] Refusing record: missing=%s exit=%d dirty=%r" % (missing, rc, bool(dirty)))
        return 2
    out = ART / "logs" / ("run_wp4_%s.json" % rec["utc"].replace(":", "").replace("+", ""))
    out.write_text(json.dumps(rec, indent=2, sort_keys=True), encoding="utf-8")
    print("[WP-4][STEP 131] WP-4 run record written: %s (clean_tree=true)" % out.name)
    return 0


if __name__ == "__main__":
    sys.exit(main())

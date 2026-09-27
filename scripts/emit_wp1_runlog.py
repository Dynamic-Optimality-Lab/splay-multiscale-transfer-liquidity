"""WP-1 STEP 35: emit the authoritative WP-1 run record (wp=WP-1, not a WP-0 record).

Run only on a clean tree; the record asserts clean_tree=true. The mislabeled
WP-0/PHASE-00 record for the phase01 command is preserved as history.
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
    print("[WP-1][STEP 35] Emitting WP-1 run record")
    t0 = time.time()
    # WP-1 STEP 35a: rerun the phase checks so command/exit are truthful for THIS record.
    r = subprocess.run([sys.executable, "scripts/run_phase01.py"], capture_output=True, text=True, cwd=str(ROOT))
    wall = time.time() - t0
    print(r.stdout[-1500:] if len(r.stdout) > 1500 else r.stdout, end="")
    head = subprocess.run(["git", "log", "--format=%H", "-1"], capture_output=True, text=True, cwd=str(ROOT)).stdout.strip()
    dirty = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, cwd=str(ROOT)).stdout.strip()
    rec = {f: None for f in FIELDS}
    rec.update({
        "experiment": "SPLAY-AM-MST-LIQ-v0.4.1", "phase": "PHASE-01-04", "wp": "WP-1",
        "branch": "master", "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "commit": head, "clean_tree": dirty == "",
        "source_manifest": sha(ROOT / "v03" / "byte_manifest.sha256.yaml"),
        "spec_sha": sha(ROOT / "IMPLEMENTATION_SPEC_SPLAY-AM-MST-LIQ-v0.4.1.md"),
        "amendment_sha": sha(ROOT / "amendments" / "SPLAY-AM-MST-LIQ-v0.4.1-CONTRACT-CLOSURE.md"),
        "prereg_sha": sha(ROOT / "prereg" / "freeze_manifest.sha256"),
        "gate_matrix_sha": sha(ROOT / "prereg" / "theorem_gate_matrix.yaml"),
        "env_sha": sha(ROOT / "prereg" / "environment_lock.yaml"),
        "firewall": "H4L EMPTY",
        "command": "python scripts/run_phase01.py", "inputs": None,
        "outputs": sha(ROOT / "artifacts" / "v04" / "parent_import" / "replay" / "corpus_report.json"),
        "wall": wall, "exit": r.returncode, "status": "LEGACY_SEMANTICS_CERTIFIED",
    })
    schema = json.loads((ROOT / "schemas" / "runlog.schema.json").read_text(encoding="utf-8"))
    missing = [k for k in schema["required"] if k not in rec]
    if missing or r.returncode != 0 or dirty:
        print("[WP-1][STEP 35] Refusing record: missing=%s exit=%d dirty=%r" % (missing, r.returncode, bool(dirty)))
        return 2
    out = ROOT / "artifacts" / "v04" / "logs" / ("run_wp1_%s.json" % rec["utc"].replace(":", "").replace("+", ""))
    out.write_text(json.dumps(rec, indent=2, sort_keys=True), encoding="utf-8")
    print("[WP-1][STEP 35] WP-1 run record written: %s (clean_tree=true)" % out.name)
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""WP-0 STEP 02: append-only 35-field runlog writer (schema: schemas/runlog.schema.json)."""
from __future__ import annotations
import hashlib
import json
import subprocess
import datetime
from pathlib import Path

FIELDS = ["experiment", "phase", "wp", "branch", "utc", "commit", "clean_tree",
          "source_manifest", "arch_ids", "obstruction_ids", "ancestor_ids", "spec_sha",
          "amendment_sha", "prereg_sha", "gate_matrix_sha", "literature_sha", "env_sha",
          "calculus_id", "rule_family_id", "P", "k", "C", "rho", "profile_sha",
          "legal_domain_sha", "firewall", "command", "inputs", "outputs", "stdout_sha",
          "stderr_sha", "wall", "peak", "exit", "status"]

def _sha_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def write_run(root: Path, command: str, exit_code: int, status: str, wall: float = 0.0) -> Path:
    print("[WP-0][STEP 02] Writing 35-field run record for: %s" % command)
    logs = root / "artifacts" / "v04" / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    head = subprocess.run(["git", "log", "--format=%H", "-1"], capture_output=True, text=True, cwd=str(root)).stdout.strip()
    dirty = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, cwd=str(root)).stdout.strip()
    rec = {f: None for f in FIELDS}
    rec.update({"experiment": "SPLAY-AM-MST-LIQ-v0.4.1", "phase": "PHASE-00", "wp": "WP-0",
                "branch": "master", "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "commit": head, "clean_tree": dirty == "", "command": command, "exit": exit_code, "status": status, "wall": wall})
    missing = [f for f in FIELDS if f not in rec]
    assert not missing, missing
    # Nulls allowed only for science fields absent in WP-0 (documented); structural fields must be set.
    for f in ["experiment", "phase", "wp", "branch", "utc", "commit", "command", "exit", "status"]:
        assert rec[f] not in (None, ""), f
    out = logs / ("run_%s.json" % rec["utc"].replace(":", "").replace("+", ""))
    out.write_text(json.dumps(rec, indent=2, sort_keys=True), encoding="utf-8")
    print("[WP-0][STEP 02] Run record written: %s" % out.name)
    return out

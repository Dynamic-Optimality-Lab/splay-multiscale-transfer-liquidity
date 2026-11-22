"""Prior byte preservation plus a seal for this self-contained checkpoint.

The user explicitly authorizes a commit and push. Unlike the old immutable
research gate, this checker permits HEAD to advance while preserving old bytes.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent


def fingerprint(path):
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def prior_check():
    baseline = json.loads((HERE / "PRIOR_BASELINE.json").read_text(encoding="utf-8"))
    for row in baseline["files"]:
        actual = fingerprint(ROOT / row["path"])
        assert all(actual[k] == row[k] for k in actual), row["path"]
    changed = subprocess.check_output(
        ["git", "diff", "--name-only", baseline["old_HEAD"], "--"],
        cwd=ROOT, text=True).splitlines()
    relative = HERE.relative_to(ROOT).as_posix() + "/"
    assert all(name.startswith(relative) for name in changed), changed
    return {"passed": True, "prior_paths": len(baseline["files"]),
            "old_HEAD": baseline["old_HEAD"], "authorized_git_commit_allowed": True}


def inventory():
    return [{"path": p.relative_to(HERE).as_posix(), **fingerprint(p)}
            for p in sorted(HERE.rglob("*"))
            if p.is_file() and p.name != "FINAL_MANIFEST.json"]


def seal(verify=False):
    path = HERE / "FINAL_MANIFEST.json"
    actual = inventory()
    if verify:
        saved = json.loads(path.read_text(encoding="utf-8"))
        assert saved["files"] == actual
        return {"passed": True, "files": len(actual),
                "bytes": sum(row["bytes"] for row in actual)}
    assert not path.exists(), "A sealed checkpoint is immutable."
    data = {"checkpoint": HERE.name, "files": actual,
            "scope": "Byte integrity; universal Omega5/A proof remains OPEN."}
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return {"sealed_files": len(actual), "bytes": sum(r["bytes"] for r in actual)}


if __name__ == "__main__":
    if "--seal" in sys.argv:
        print(json.dumps(seal()))
    elif "--verify-seal" in sys.argv:
        print(json.dumps(seal(True)))
    else:
        print(json.dumps(prior_check()))

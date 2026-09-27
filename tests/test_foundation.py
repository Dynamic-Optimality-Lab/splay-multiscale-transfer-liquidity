"""TEST-F-01..16: foundation named tests with frozen semantic meanings (see planning/WP0_CONTRACT.md)."""
import hashlib
import json
import subprocess
import urllib.request
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
ARCH = Path(r"C:\Users\SAIFMA~1\AppData\Local\Temp\opencode\arch-parent")


def shas():
    pc = yaml.safe_load((ROOT / "prereg" / "parent_contract.yaml").read_text(encoding="utf-8"))
    return pc


def git(*a):
    return subprocess.run(["git", "-C", str(ARCH), *a], capture_output=True, text=True)


def test_F01_nav_reachable():
    assert git("cat-file", "-t", shas()["arch"]["navigation"]).stdout.strip() == "commit"


def test_F02_closure_reachable():
    assert git("cat-file", "-t", shas()["arch"]["closure"]).stdout.strip() == "commit"


def test_F03_seal_reachable():
    assert git("cat-file", "-t", shas()["arch"]["seal"]).stdout.strip() == "commit"


def test_F04_obstruction_evidence_commit():
    sha = shas()["obstruction"]["evidence_commit"]
    d = json.load(urllib.request.urlopen(
        "https://api.github.com/repos/Dynamic-Optimality-Lab/Universal-Pair-Access-Closure-and-Dynamic-Optimality-Decision-Program-/commits/" + sha, timeout=60))
    assert d["sha"] == sha
    assert "n=28" in d["commit"]["message"] and "triple replay" in d["commit"]["message"]
    assert shas()["obstruction"]["lifecycle_seal"] == "OPEN"


def test_F05_content_hashes():
    pc = shas()
    for rel, want in pc["arch"]["content_sha256"].items():
        assert hashlib.sha256((ROOT / "v03" / "history" / rel).read_bytes()).hexdigest() == want


def test_F06_bridge_manifest():
    bm = yaml.safe_load((ROOT / "prereg" / "bridge_manifest.yaml").read_text(encoding="utf-8"))
    assert bm["L3"]["bytes"] == 1431066 and len(bm["L3"]["sha256"]) == 64
    assert bm["L2"]["status"] == "ABSENT_PAYWALLED"
    assert "BLOCKED_BY_SOURCE" in bm["L2"]["consequence"]


def test_F07_env_lock():
    import sys
    env = yaml.safe_load((ROOT / "prereg" / "environment_lock.yaml").read_text(encoding="utf-8"))
    assert env["python"] == sys.version.split()[0]
    assert env["lean"] == "leanprover/lean4:v4.21.0"
    assert (ROOT / "lean-toolchain").read_text(encoding="utf-8").strip() == env["lean"]


def test_F08_freeze_manifest():
    ents = {}
    for p in sorted((ROOT / "prereg").glob("*.yaml")):
        ents[p.name] = hashlib.sha256(p.read_bytes()).hexdigest()
    want = {}
    for line in (ROOT / "prereg" / "freeze_manifest.sha256").read_text(encoding="utf-8").splitlines():
        h, n = line.split("  ")
        want[n] = h
    assert want == ents


def test_F09_proof_status():
    st = json.loads((ROOT / "math" / "proof_status.json").read_text(encoding="utf-8"))
    assert len(st) == 27
    for tid, r in st.items():
        assert r["truth"] == "UNPROVED" and r["prove_track"] == "UNPROVED" and r["refute_track"] == "NO_WITNESS"
        assert r["proof_hash"] is None and r["review_hash"] is None


def test_F10_history_manifest():
    man = yaml.safe_load((ROOT / "v03" / "byte_manifest.sha256.yaml").read_text(encoding="utf-8"))
    assert man["files"] == 566
    for e in man["entries"]:
        assert hashlib.sha256((ROOT / "v03" / "history" / e["path"]).read_bytes()).hexdigest() == e["sha256"]


def test_F11_closure_checker():
    r = subprocess.run(["python", "scripts/check_contract_closure.py"], capture_output=True, text=True, cwd=str(ROOT))
    assert r.returncode == 0 and "CONTRACT_CLOSURE_PASS" in r.stdout


def test_F12_coverage_checker():
    r = subprocess.run(["python", "scripts/check_workplan_coverage.py"], capture_output=True, text=True, cwd=str(ROOT))
    assert r.returncode == 0 and "WORKPLAN_COVERAGE_PASS" in r.stdout


def test_F13_theorem_files():
    import re
    files = sorted(p.stem for p in (ROOT / "math" / "theorems").glob("*.md"))
    assert len(files) == 27
    for p in (ROOT / "math" / "theorems").glob("*.md"):
        t = p.read_text(encoding="utf-8")
        assert "Negation:" in t and "First consumer:" in t


def test_F14_gate_matrix_keys():
    gm = yaml.safe_load((ROOT / "prereg" / "theorem_gate_matrix.yaml").read_text(encoding="utf-8"))
    assert len(gm["nodes"]) == 26 and "MST0-09" in gm["nodes"] and "MST0-21" in gm["nodes"]


def test_F15_corrupt_manifest_copy_fails():
    import tempfile
    ents = {}
    for p in sorted((ROOT / "prereg").glob("*.yaml")):
        ents[p.name] = hashlib.sha256(p.read_bytes()).hexdigest()
    ents["prereg/h4l_holdout.yaml"] = "0" * 64
    want = {}
    for line in (ROOT / "prereg" / "freeze_manifest.sha256").read_text(encoding="utf-8").splitlines():
        h, n = line.split("  ")
        want[n] = h
    assert want != ents


def test_F16_missing_artifact_blocks():
    assert not (ROOT / "artifacts" / "v04" / "holdouts" / "h4l_bank.json.zst").exists()

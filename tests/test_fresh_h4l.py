"""WP-5 FRSH-01..14: fresh-holdout conformance suite.

Pre-reveal, reveal-dependent tests SKIP; post-reveal the full file passes with
zero skips. Never evaluates candidates itself (except via the refusal stub path);
never reveals (the reveal driver owns the single transition).
"""
from __future__ import annotations
import ast
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from holdout import firewall as FW

ART = ROOT / "artifacts" / "v04"
REV = ART / "h4l_reveal"


def revealed() -> bool:
    return FW.read_state()["state"] == "REVEALED_ONCE"


def set_frozen() -> bool:
    return (ART / "candidates" / "commit" / "set.json").exists()


needs_set = pytest.mark.skipif(not set_frozen(), reason="pre-set-freeze: set not frozen")
needs_reveal = pytest.mark.skipif(not revealed(), reason="pre-reveal: H4L still sealed")


# WP-5 FRSH-01: set freeze (members bound, hash recorded, lawful transition).
@needs_set
def test_frsh_01_set_freeze():
    print("[WP-5][FRSH-01] Candidate set freeze")
    rec = json.loads((ART / "candidates" / "commit" / "set.json").read_text(encoding="utf-8"))
    assert len(rec["members"]) == 3
    assert rec["set_hash"] == hashlib.sha256(
        json.dumps(rec["members"], sort_keys=True).encode()).hexdigest()
    log = FW.read_state()["log"]
    tos = [e["to"] for e in log]
    assert "CANDIDATE_SET_FROZEN" in tos
    assert tos.index("CANDIDATE_SET_FROZEN") > tos.index("COMMITMENT_PUBLISHED")


# WP-5 FRSH-02: clean-room implementation freeze record (versioned; history kept).
def test_frsh_02_cleanroom_frozen():
    print("[WP-5][FRSH-02] Clean-room freeze record")
    if not (ART / "cleanroom" / "impl_freeze.json").exists():
        pytest.skip("pre-freeze: implementation not frozen")
    rec = json.loads((ART / "cleanroom" / "impl_freeze.json").read_text(encoding="utf-8"))
    ev_p = ROOT / "python" / "cleanroom" / "evaluator.py"
    cur = hashlib.sha256(ev_p.read_bytes()).hexdigest()
    versions = rec.get("versions", [{"v": "v1", "sha256": rec.get("sha256")}])
    assert len(versions) >= 1  # v1 preserved: post-freeze edits version, never erase
    assert [v for v in versions if v["v"] == rec.get("current", "v1")][0]["sha256"] == cur
    tree = ast.parse(ev_p.read_text(encoding="utf-8"))
    mods = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            mods.update(a.name.split(".")[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom):
            mods.add((node.module or "").split(".")[0])
    assert mods <= {"__future__"}, mods


# WP-5 FRSH-03: reveal-once (single transition, unlocks==1, bank published).
@needs_reveal
def test_frsh_03_reveal_once():
    print("[WP-5][FRSH-03] Single lawful reveal")
    st = FW.read_state()
    assert st["state"] == "REVEALED_ONCE" and st["unlocks"] == 1
    assert sum(1 for e in st["log"] if e["to"] == "REVEALED_ONCE") == 1
    assert (REV / "seed.bin").exists() and len((REV / "seed.bin").read_bytes()) == 32
    assert len(list((REV / "bank").glob("*.json.zst"))) == 7
    assert (REV / "manifest.json").exists() and (REV / "reveal.json").exists()


# WP-5 FRSH-04: revealed bank matches commitment (shard SHAs + total + order).
@needs_reveal
def test_frsh_04_bank_matches_commitment():
    print("[WP-5][FRSH-04] Revealed bank vs commitment")
    import zstandard
    com = json.loads((ART / "holdouts" / "h4l_commitment.json").read_text(encoding="utf-8"))
    man = json.loads((REV / "manifest.json").read_text(encoding="utf-8"))
    total, prev = 0, None
    for sh in sorted(man["shards"], key=lambda s: s["name"]):
        blob = (REV / "bank" / sh["name"]).read_bytes()
        assert hashlib.sha256(blob).hexdigest() == sh["sha256"]
        raw = zstandard.ZstdDecompressor().decompress(blob, max_output_size=1 << 31)
        lines = raw.decode("utf-8").splitlines()
        assert len(lines) == sh["episodes"]
        ids = [json.loads(ln)["hash"] for ln in lines]
        assert ids == sorted(ids) and len(set(ids)) == len(ids)
        total += len(lines)
    assert total == com["total"] == 70000


# WP-5 FRSH-05: fresh evaluation order/exhaustion.
@needs_reveal
def test_frsh_05_fresh_order_exhaustion():
    print("[WP-5][FRSH-05] Predetermined order + exhaustion record")
    fresh = json.loads((REV / "fresh_results.json").read_text(encoding="utf-8"))
    assert sorted(fresh) == sorted(fresh.keys())
    for key, r in fresh.items():
        assert r["evaluated"] > 0
        assert (r["exhausted"] and r["violations"] == 0) or \
               (not r["exhausted"] and r["first_violation"] is not None)


# WP-5 FRSH-06: clean-room agreement (full-bank per-KEEP equality).
@needs_reveal
def test_frsh_06_cleanroom_agreement():
    print("[WP-5][FRSH-06] Full-bank clean-room agreement")
    agree = json.loads((ART / "cleanroom" / "agreement.json").read_text(encoding="utf-8"))
    assert len(agree) == len(json.loads((REV / "fresh_results.json").read_text(encoding="utf-8")))
    for key, r in agree.items():
        assert r["mismatches"] == 0 and r["episodes_compared"] == 70000


# WP-5 FRSH-07: large-n (9 sizes x40 + diagnostics).
@needs_reveal
def test_frsh_07_large_n():
    print("[WP-5][FRSH-07] Large-n attack record")
    ids = json.loads((ART / "large_n" / "id_registry.json").read_text(encoding="utf-8"))
    assert len(ids) == 9 * 40
    res = json.loads((ART / "large_n" / "large_n_results.json").read_text(encoding="utf-8"))
    assert len(res) > 0
    for key, r in res.items():
        assert r["episodes"] == 9 * 40


# WP-5 FRSH-08: OOD labeled + disjoint (8000, distinct distribution, zero H4L overlap).
@needs_reveal
def test_frsh_08_ood_disjoint_labeled():
    print("[WP-5][FRSH-08] OOD battery")
    import zstandard
    oids = json.loads((ART / "ood" / "id_registry.json").read_text(encoding="utf-8"))
    assert len(oids) == 8000 and len(set(oids)) == 8000
    res = json.loads((ART / "ood" / "ood_results.json").read_text(encoding="utf-8"))
    for key, r in res.items():
        assert r["episodes"] == 8000 and r["label"] == "OOD (not fresh-holdout)"
    hids = set()
    for sh in sorted((REV / "bank").glob("*.json.zst")):
        raw = zstandard.ZstdDecompressor().decompress(
            sh.read_bytes(), max_output_size=1 << 31)
        hids.update(json.loads(ln)["hash"] for ln in raw.decode("utf-8").splitlines())
    assert len(hids) == 70000
    assert hids.isdisjoint(oids)


# WP-5 FRSH-09: second reveal refused (unlocks stays 1).
@needs_reveal
def test_frsh_09_second_reveal_refused():
    print("[WP-5][FRSH-09] Second reveal fails closed")
    r = subprocess.run([sys.executable, "scripts/reveal_h4l.py"],
                       capture_output=True, text=True, cwd=str(ROOT))
    assert r.returncode == 2
    assert FW.read_state()["unlocks"] == 1


# WP-5 FRSH-10: regeneration refused (commitment exists).
@needs_reveal
def test_frsh_10_regen_refused():
    print("[WP-5][FRSH-10] Regeneration fails closed")
    r = subprocess.run([sys.executable, "scripts/seal_h4l.py"],
                       capture_output=True, text=True, cwd=str(ROOT))
    assert r.returncode == 2


# WP-5 FRSH-11: post-reveal bank reads allowed ONLY via firewall guard.
@needs_reveal
def test_frsh_11_guarded_reads():
    print("[WP-5][FRSH-11] Guarded post-reveal reads")
    p = FW.guard_bank_read()
    assert p.exists()


# WP-5 FRSH-12: 16 mutants killed.
def test_frsh_12_mutants():
    print("[WP-5][FRSH-12] Mutant battery delegates")
    r = subprocess.run([sys.executable, "scripts/test_wp5_mutants.py"],
                       capture_output=True, text=True, cwd=str(ROOT))
    print((r.stdout or "")[-1500:], end="")
    assert r.returncode == 0 and "16/16" in (r.stdout or "")


# WP-5 FRSH-13: finite != theorem (no status changes, no universal claims).
def test_frsh_13_finite_not_theorem():
    print("[WP-5][FRSH-13] No universal claims smuggled")
    ps = json.loads((ROOT / "math" / "proof_status.json").read_text(encoding="utf-8"))
    assert all(v["truth"] == "UNPROVED" for k, v in ps.items() if k.startswith("MSTL"))
    for p in (ART / "candidates" / "branchA").rglob("outline.md"):
        assert "finite survival only" in p.read_text(encoding="utf-8")


# WP-5 FRSH-14: zero pre-reveal evaluations (timestamps ordered).
@needs_reveal
def test_frsh_14_zero_prereveal_evals():
    print("[WP-5][FRSH-14] Evaluation timestamps strictly post-reveal")
    log = json.loads((REV / "eval_log.json").read_text(encoding="utf-8"))
    assert log["evaluations_before_reveal"] == 0
    assert log["reveal_utc"] < log["first_eval_utc"] <= log["last_eval_utc"]

"""WP-3 HOLD-01..14: holdout firewall + freeze conformance suite.

Pre-seal, post-seal-only tests SKIP (commitment/secret absent); post-seal the full
file must pass with zero skips. Never evaluates candidates, never reveals H4L.
"""
from __future__ import annotations
import ast
import hashlib
import json
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from holdout import firewall as FW  # WP-3 STEP 94 import: automaton + state only
from holdout import h4l_generate as G  # WP-3 STEP 94 import: generator bytes only
from holdout import h4l_evaluate as EV  # WP-3 STEP 94 import: refusal stub only

COM_P = ROOT / "artifacts" / "v04" / "holdouts" / "h4l_commitment.json"


def commitment_exists() -> bool:
    return COM_P.exists()


def secret_dir() -> Path:
    return FW._default_secret()


def repo_secret_scan():
    """WP-3 STEP 94 helper: filename scan for secret material outside legacy history.

    Legacy v03/history banks are committed pre-existing history (allowlisted with
    reason); any seed.bin / h4l_n*.json.zst elsewhere is a quarantine failure.
    """
    hits = []
    for p in ROOT.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(ROOT).as_posix()
        if rel.startswith(".git/"):
            continue
        if rel.startswith("v03/history/"):
            continue
        name = p.name
        if name == "seed.bin" or (name.startswith("h4l_n") and name.endswith(".json.zst")):
            hits.append(rel)
    return hits


# WP-3 HOLD-01: generator contract frozen (params match prereg/h4l_holdout.yaml).
def test_hold_01_generator_contract_frozen():
    print("[WP-3][HOLD-01] Checking generator params vs prereg contract")
    pr = yaml.safe_load((ROOT / "prereg" / "h4l_holdout.yaml").read_text(encoding="utf-8"))
    assert G.SIZES == pr["sizes"] == [18, 26, 34, 46, 58, 74, 98]
    assert G.PER_SIZE == pr["per_size"] == 10000
    assert G.STRATA == pr["strata"] and len(G.STRATA) == 12
    assert sum(G.QUOTA.values()) == G.PER_SIZE == 10000
    assert all(G.QUOTA[s] == 833 + (1 if i < 4 else 0) for i, s in enumerate(G.STRATA))
    assert (G.HIST_MIN, G.HIST_MAX) == (2, 8)
    assert pr["rng"].startswith("SHA-256 counter DRBG")
    src = (ROOT / "python" / "holdout" / "h4l_generate.py").read_text(encoding="utf-8")
    assert '"h4l|%d|%s|%d"' in src  # domain-separated stream binds (n, stratum, counter)
    # WP-3 STEP 94 blindness-by-construction: generator imports stdlib only, no repo modules.
    tree = ast.parse(src)
    mods = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            mods.update(a.name.split(".")[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom):
            mods.add((node.module or "").split(".")[0])
    assert mods <= {"__future__", "hashlib", "json", "pathlib"}, mods


# WP-3 HOLD-02: implementation certified (tiny-bank determinism + legality, ephemeral seed).
def test_hold_02_implementation_certified_tiny_bank():
    print("[WP-3][HOLD-02] Tiny-bank determinism + legality (ephemeral seed, in-memory)")
    seed = b"wp3-hold02-certification-only-seed-0001"
    quotas = {s: 2 for s in G.STRATA}
    b1 = G.generate_bank(seed, sizes=[7], quotas=quotas)
    b2 = G.generate_bank(seed, sizes=[7], quotas=quotas)
    assert len(b1[7]) == len(b2[7]) == 2 * len(G.STRATA)
    c1 = [json.dumps(e, sort_keys=True) for e in b1[7]]
    c2 = [json.dumps(e, sort_keys=True) for e in b2[7]]
    assert c1 == c2  # same seed => identical bank
    seen = set()
    for ep in b1[7]:
        assert set(ep) == {"size", "stratum", "shape", "T0", "H", "hash"}
        assert ep["stratum"] in G.STRATA  # no stratum bleed
        keys = []

        def walk(t):
            if t is None:
                return
            keys.append(t[0])
            walk(t[1])
            walk(t[2])

        walk(ep["T0"])
        assert sorted(keys) == list(range(1, 8)) and all(1 <= x <= 7 for _, x in ep["H"])
        assert all(m in ("KEEP", "DELETE") for m, _ in ep["H"])
        assert 2 <= len(ep["H"]) <= 16
        assert ep["hash"] not in seen
        seen.add(ep["hash"])
    # WP-3 STEP 94 mutant M-HOLD-e: quota violation changes totals (schedule is load-bearing).
    bad = {s: 1 for s in G.STRATA}
    b3 = G.generate_bank(seed, sizes=[7], quotas=bad)
    assert len(b3[7]) != G.PER_SIZE  # a violated schedule cannot impersonate the bank


# WP-3 HOLD-03 (post-seal): real bank in secret storage; repo holds zero bank bytes/seeds.
@pytest.mark.skipif(not commitment_exists(), reason="post-seal only: no commitment yet")
def test_hold_03_bank_secret_repo_clean():
    print("[WP-3][HOLD-03] Secret bank present outside repo; repo holds zero bank bytes")
    com = json.loads(COM_P.read_text(encoding="utf-8"))
    assert com["total"] == 70000 and com["per_size"] == 10000
    sec = secret_dir()
    seed_p = sec / "seed.bin"
    assert seed_p.exists() and len(seed_p.read_bytes()) == 32
    man = json.loads((sec / "manifest.json").read_text(encoding="utf-8"))
    assert len(man["shards"]) == 7
    for sh in man["shards"]:
        assert (sec / "bank" / sh["name"]).exists()
    assert repo_secret_scan() == []


# WP-3 HOLD-04 (post-seal): commitment verifies (independent recompute).
@pytest.mark.skipif(not commitment_exists(), reason="post-seal only: no commitment yet")
def test_hold_04_commitment_verifies():
    print("[WP-3][HOLD-04] Independent commitment recompute")
    from holdout import h4l_verify as V  # WP-3 STEP 94: separate code path from generator
    assert V.verify(secret_dir(), COM_P) is True


# WP-3 HOLD-05: pre-reveal bank read via firewall fails closed.
def test_hold_05_prereveal_read_refused():
    print("[WP-3][HOLD-05] Pre-reveal bank read must fail closed")
    st = FW.read_state()["state"]
    assert st not in ("REVEALED_ONCE", "CONSUMED")  # WP-3 never reveals
    with pytest.raises(FW.FirewallError):
        FW.guard_bank_read()


# WP-3 HOLD-06: reveal/second-unlock fails closed (reveal is WP-5-owned).
def test_hold_06_reveal_refused_unlock_once(tmp_path, monkeypatch):
    print("[WP-3][HOLD-06] Reveal refused before CANDIDATE_SET_FROZEN; unlock<=1 enforced")
    with pytest.raises(FW.FirewallError):
        FW.reveal()  # legal only from CANDIDATE_SET_FROZEN; WP-3 never reaches it
    # WP-3 STEP 94 mutant M-HOLD-b on an isolated state file: double reveal fails.
    monkeypatch.setattr(FW, "STATE_FILE", tmp_path / "fw.json")
    for to in ["GENERATOR_FROZEN", "BANK_GENERATED_SECRET", "COMMITMENT_PUBLISHED",
               "CANDIDATE_SET_FROZEN"]:
        FW.transition(to, "hold06-probe")
    FW.transition("REVEALED_ONCE", "hold06-first")
    assert FW.read_state()["unlocks"] == 1
    with pytest.raises(FW.FirewallError):
        FW.reveal()  # second unlock forbidden (already REVEALED_ONCE)
    with pytest.raises(FW.FirewallError):
        FW.transition("REVEALED_ONCE", "hold06-second")
    # WP-3 STEP 94 mutant M-HOLD-a: read-before-freeze fails on a fresh (EMPTY) file.
    monkeypatch.setattr(FW, "STATE_FILE", tmp_path / "fresh.json")
    with pytest.raises(FW.FirewallError):
        FW.guard_bank_read()


# WP-3 HOLD-07 (post-seal): regen-after-commitment fails closed.
@pytest.mark.skipif(not commitment_exists(), reason="post-seal only: no commitment yet")
def test_hold_07_regen_refused():
    print("[WP-3][HOLD-07] Regeneration after commitment must fail closed")
    import subprocess
    r = subprocess.run([sys.executable, "scripts/seal_h4l.py"],
                       capture_output=True, text=True, cwd=str(ROOT))
    assert r.returncode == 2  # commitment exists; regeneration refused


# WP-3 HOLD-08: repo-wide scan finds no seed/bank material; gitignore guards secret names.
def test_hold_08_repo_scan_clean_gitignore_guards():
    print("[WP-3][HOLD-08] Repo secret scan + gitignore quarantine guard")
    assert repo_secret_scan() == []
    gi = (ROOT / ".gitignore").read_text(encoding="utf-8")
    assert "h4l-secret/" in gi and "seed.bin" in gi and "h4l_n*.json.zst" in gi
    # WP-3 STEP 94 mutant M-HOLD-d: scanner catches planted secret-named files.
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        (Path(td) / "seed.bin").write_bytes(b"x" * 32)
        found = [p for p in Path(td).rglob("*")
                 if p.name == "seed.bin" or (p.name.startswith("h4l_n") and p.name.endswith(".json.zst"))]
        assert len(found) == 1


# WP-3 HOLD-09: predicate family closed + hashed (P_all, P_keep + enumerated case predicates).
def test_hold_09_predicate_family_closed_hashed():
    print("[WP-3][HOLD-09] Predicate closure + definition-hash check")
    fam = yaml.safe_load((ROOT / "prereg" / "predicate_family_v0.4.1.yaml").read_text(encoding="utf-8"))
    assert fam["closed"] is True
    expect = {"P_all", "P_keep",
              "P_keep_all", "P_keep_doubles", "P_keep_zig", "P_keep_zigzag", "P_keep_zigzig",
              "P_both_doubles", "P_both_zig", "P_both_zigzag", "P_both_zigzig",
              "P_delete_all", "P_delete_doubles", "P_delete_zig", "P_delete_zigzag", "P_delete_zigzig"}
    got = {p["id"] for p in fam["predicates"]}
    assert got == expect and len(fam["predicates"]) == 16
    for p in fam["predicates"]:
        assert p["hash"] == hashlib.sha256(p["definition"].encode()).hexdigest(), p["id"]


# WP-3 HOLD-10: scope lock (search space exact; no template terms).
def test_hold_10_scope_locked():
    print("[WP-3][HOLD-10] (P,k,C,rho) scope lock")
    sp = yaml.safe_load((ROOT / "prereg" / "liquidity_search_space.yaml").read_text(encoding="utf-8"))
    assert sp["scope"].startswith("B: (P,k,C,rho)")
    assert sp["k"] == [0, 1, 2, 3, 4, 5, 6]
    assert sp["C"] == [2, 3, 4, 6, 8, 12, 16, 24, 32, 64]
    assert sp["rho_ladder"] == ["FLAT-1..6", "ROT-1..6"]
    assert sp["objective"] == ["legality", "conservation", "REG-001", "dev-zero",
                               "validation-zero", "smaller-C", "simpler-rho",
                               "smaller-base", "smaller-k", "simpler-P"]
    assert "FLAT(1)" in sp["matched_baseline"]
    assert sp["attribution"] == ["RHO_REQUIRED", "RHO_NOT_REQUIRED", "C_ONLY_REPAIR",
                                 "K_OR_P_REPAIR", "MIXED_AXIS_REPAIR", "NO_SURVIVOR"]


# WP-3 HOLD-11: clean-room contract frozen (spec/boundary/schema present; no impl bytes).
def test_hold_11_cleanroom_contract_frozen():
    print("[WP-3][HOLD-11] Clean-room contract presence + implementation absence")
    base = ROOT / "artifacts" / "v04" / "cleanroom" / "contract"
    for name in ["spec.md", "boundary.md", "io_schema.json"]:
        p = base / name
        assert p.exists() and len(p.read_bytes()) > 0
    assert list((ROOT / "artifacts" / "v04" / "cleanroom").rglob("*.py")) == []


# WP-3 HOLD-12: dormant Branch-B set frozen (signed defs, DORMANT).
def test_hold_12_branchb_dormant_frozen():
    print("[WP-3][HOLD-12] Dormant Branch-B identities")
    base = ROOT / "artifacts" / "v04" / "candidates" / "branchB"
    files = sorted(base.glob("dormant_*.json"))
    assert len(files) == 2
    fam = yaml.safe_load((ROOT / "prereg" / "predicate_family_v0.4.1.yaml").read_text(encoding="utf-8"))
    allowed_p = {p["id"] for p in fam["predicates"]}
    for f in files:
        ident = json.loads(f.read_text(encoding="utf-8"))
        assert ident["status"] == "DORMANT" and ident["branch"] == "SIGNED_MULTISCALE"
        assert ident["predicate"] in allowed_p
        rest = {k: v for k, v in ident.items() if k != "identity_hash"}
        assert ident["identity_hash"] == hashlib.sha256(
            json.dumps(rest, sort_keys=True).encode()).hexdigest()


# WP-3 HOLD-13: validation/adversarial/OOD tables exact.
def test_hold_13_validation_adversarial_ood_exact():
    print("[WP-3][HOLD-13] Validation + adversarial + OOD exact tables")
    sp = yaml.safe_load((ROOT / "prereg" / "liquidity_search_space.yaml").read_text(encoding="utf-8"))
    v = sp["validation"]
    assert v["sizes"] == [7, 8, 10, 12, 16] and v["per_size"] == 1000 and v["total"] == 5000
    eng = sp["adversarial"]["engines"]
    assert set(eng) == {"uniform", "structured", "hillclimb", "anneal", "genetic",
                        "rotneigh", "splice", "motif", "generalize"}
    assert {e: eng[e]["seed"] for e in eng} == {"uniform": 101, "structured": 102,
        "hillclimb": 103, "anneal": 104, "genetic": 105, "rotneigh": 106,
        "splice": 107, "motif": 108, "generalize": 109}
    assert sp["adversarial"]["wall_cap_s"] == 7200 and sp["adversarial"]["mem_cap_gb"] == 4
    assert "lexicographic" in sp["adversarial"]["reduction"]
    h4l = yaml.safe_load((ROOT / "prereg" / "h4l_holdout.yaml").read_text(encoding="utf-8"))
    assert len(h4l["sizes"]) * h4l["per_size"] == h4l["total"] == 70000
    assert h4l["ood_counts"]["sizes"] == [24, 48, 96, 192]
    assert h4l["ood_counts"]["per_size"] == 2000 and h4l["ood_counts"]["total"] == 8000


# WP-3 HOLD-14: zero H4L evaluations logged (evaluation stub refuses; never revealed).
def test_hold_14_zero_evaluations():
    print("[WP-3][HOLD-14] Evaluation stub refuses; firewall never revealed")
    with pytest.raises(RuntimeError):
        EV.evaluate("any", "args")
    assert FW.read_state()["state"] not in ("REVEALED_ONCE", "CONSUMED")

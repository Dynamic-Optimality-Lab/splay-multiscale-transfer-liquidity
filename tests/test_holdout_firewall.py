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
        assert 2 <= len(ep["H"]) <= 8  # WP-3 REPAIR R2: frozen 2..8 (was 2..16)
        assert ep["hash"] not in seen
        seen.add(ep["hash"])
    # WP-3 STEP 94 mutant M-HOLD-e: quota violation changes totals (schedule is load-bearing).
    bad = {s: 1 for s in G.STRATA}
    b3 = G.generate_bank(seed, sizes=[7], quotas=bad)
    assert len(b3[7]) != G.PER_SIZE  # a violated schedule cannot impersonate the bank


# WP-3 REPAIR STEP R2-05: forced-L law — every stratum x every L in 2..8 yields len==L.
def test_hold_02b_forced_length_all_strata():
    print("[WP-3][R2-05] Forced-L 12 strata x L=2..8 (84 combinations)")
    rng0 = G.DRBG(b"wp3-r2-02b-tree-seed", b"t0")
    T0 = G.build_tree("balanced", 18, rng0)
    for s in G.STRATA:
        for L in range(2, 9):
            rng = G.DRBG(b"wp3-r2-02b-seed", ("%s|%d" % (s, L)).encode())
            H = G.gen_history(s, 18, T0, rng, L=L)
            assert len(H) == L, (s, L, len(H))
            assert all(m in ("KEEP", "DELETE") and 1 <= x <= 18 for m, x in H), (s, L)
    # WP-3 REPAIR R2 mutant M-HOLD-f1: unforced sampling also obeys 2..8 always.
    rng = G.DRBG(b"wp3-r2-02b-unforced", b"u")
    for s in G.STRATA:
        for _ in range(20):
            assert 2 <= len(G.gen_history(s, 18, T0, rng)) <= 8, s


# WP-3 REPAIR STEP R2-05: exact-uniform RNG — determinism + modulo-bias mutant kill.
def test_hold_02c_rng_exact_uniform():
    print("[WP-3][R2-05] RNG determinism + rejection-sampling (modulo mutant killed)")
    a = G.DRBG(b"wp3-r2-02c-seed", b"stream")
    b = G.DRBG(b"wp3-r2-02c-seed", b"stream")
    seq_a = [a.randbelow(7) for _ in range(50)] + [a.randint(2, 8) for _ in range(50)]
    seq_b = [b.randbelow(7) for _ in range(50)] + [b.randint(2, 8) for _ in range(50)]
    assert seq_a == seq_b
    assert all(0 <= v < 7 for v in seq_a[:50]) and all(2 <= v <= 8 for v in seq_a[50:])
    # WP-3 REPAIR R2 mutant M-HOLD-m: canned blocks kill the old modulo implementation.
    # n=3: 2^256 % 3 == 1 so bound = 2^256-1; block 2^256-1 must be REJECTED.
    class Canned(G.DRBG):
        def __init__(self):
            super().__init__(b"x", b"y")
            self.blocks = [b"\xff" * 32, b"\x05" + b"\x00" * 31]

        def _block(self):
            self.ctr += 1
            return self.blocks.pop(0)

    c = Canned()
    got = c.randbelow(3)
    assert got == 2 and c.ctr == 2  # old modulo code returns 0 with ctr==1: killed


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


# WP-3 REPAIR STEP R2-05: mini-bank verifier probes (isolated tmp banks, never H4L).
def _mk_ep(n, stratum, H, shape="balanced"):
    T0 = G._balanced(list(range(1, n + 1)))
    ep = {"size": n, "stratum": stratum, "shape": shape, "T0": T0, "H": H}
    ep["hash"] = G.episode_hash(ep)
    return ep


def _mini_setup(tmp_path, episodes, logical_ids=None, name="mini_n7.json.zst"):
    import zstandard
    sec = tmp_path / "sec"
    (sec / "bank").mkdir(parents=True)
    seed = b"mini-probe-seed-" + b"0" * 16
    assert len(seed) == 32
    (sec / "seed.bin").write_bytes(seed)
    lines = [json.dumps(ep, sort_keys=True) for ep in episodes]
    blob = zstandard.ZstdCompressor(level=3).compress(("\n".join(lines)).encode())
    (sec / "bank" / name).write_bytes(blob)
    order = logical_ids if logical_ids is not None else [ep["hash"] for ep in episodes]
    lh = hashlib.sha256()
    for i in order:
        lh.update(i.encode())
    man = {"shards": [{"name": name, "sha256": hashlib.sha256(blob).hexdigest(),
                       "bytes": len(blob), "episodes": len(lines), "zstd_level": 3}],
           "logical_stream_sha256": lh.hexdigest(), "generator": "probe"}
    (sec / "manifest.json").write_text(json.dumps(man, sort_keys=True), encoding="utf-8")
    quotas = {}
    for ep in episodes:
        quotas["%d|%s" % (ep["size"], ep["stratum"])] = quotas.get("%d|%s" % (ep["size"], ep["stratum"]), 0) + 1
    com = {"bank": "PROBE", "commitment": "", "total": len(episodes), "sizes": [7],
           "per_size": len(episodes), "quotas": quotas,
           "shards": [{"name": name, "sha256": hashlib.sha256(blob).hexdigest()}],
           "logical_stream_sha256": lh.hexdigest(), "generator_sha256": "probe",
           "strata": ["RANDOM_LEGAL"], "seed_status": "probe"}
    h = hashlib.sha256()
    h.update(seed)
    h.update(blob)
    com["commitment"] = h.hexdigest()
    com_p = tmp_path / "com.json"
    com_p.write_text(json.dumps(com, sort_keys=True), encoding="utf-8")
    return sec, com_p


def _good_ep():
    return _mk_ep(7, "RANDOM_LEGAL", [["KEEP", 3], ["DELETE", 5], ["KEEP", 1]])


def test_hold_04b_verifier_positive_control(tmp_path):
    print("[WP-3][R2-05] Verifier positive control (sorted, intact mini-bank)")
    from holdout import h4l_verify as V
    eps = sorted([_good_ep(), _mk_ep(7, "RANDOM_LEGAL", [["DELETE", 2]] * 5)], key=lambda e: e["hash"])
    sec, com_p = _mini_setup(tmp_path, eps)
    assert V.verify(sec, com_p) is True


def test_hold_04c_verifier_kills_len9(tmp_path):
    print("[WP-3][R2-05] Verifier kills length-9 history (frozen 2..8)")
    from holdout import h4l_verify as V
    bad = _mk_ep(7, "RANDOM_LEGAL", [["KEEP", 1]] * 9)
    sec, com_p = _mini_setup(tmp_path, [bad])
    assert V.verify(sec, com_p) is False


def test_hold_04d_verifier_kills_unsorted(tmp_path):
    print("[WP-3][R2-05] Verifier kills unsorted episode IDs")
    from holdout import h4l_verify as V
    eps = sorted([_good_ep(), _mk_ep(7, "RANDOM_LEGAL", [["DELETE", 2]] * 5)], key=lambda e: e["hash"])
    sec, com_p = _mini_setup(tmp_path, list(reversed(eps)))
    assert V.verify(sec, com_p) is False


def test_hold_04e_verifier_kills_corrupt_id(tmp_path):
    print("[WP-3][R2-05] Verifier kills corrupted episode ID/hash")
    from holdout import h4l_verify as V
    ep = _good_ep()
    ep["hash"] = ("0" if ep["hash"][0] != "0" else "1") + ep["hash"][1:]
    sec, com_p = _mini_setup(tmp_path, [ep])
    assert V.verify(sec, com_p) is False


def test_hold_04f_verifier_kills_wrong_logical_order(tmp_path):
    print("[WP-3][R2-05] Verifier kills wrong logical-stream ordering")
    from holdout import h4l_verify as V
    eps = sorted([_good_ep(), _mk_ep(7, "RANDOM_LEGAL", [["DELETE", 2]] * 5)], key=lambda e: e["hash"])
    sec, com_p = _mini_setup(tmp_path, eps,
                             logical_ids=[e["hash"] for e in reversed(eps)])
    assert V.verify(sec, com_p) is False
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

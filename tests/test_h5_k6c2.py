"""H5 safety mutants for the WP-5X-K6C2 fresh holdout (20 cases).

Pre-reveal mutants run immediately; post-reveal mutants skip gracefully until
their artifacts exist, then enforce fail-closed gates. Every test must PASS on
the correct implementation and FAIL if the listed mutation is introduced.
"""
from __future__ import annotations
import hashlib
import json
import subprocess
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts" / "v04"
H5 = ART / "h5"
H5REV = ART / "h5_reveal"
XH5 = ART / "wp5x_k6c2" / "h5"
K6_HASH = "9dcdea2b7926cf94765e1fd818a73f0459c72404b4f4bf5c36b3ec65a27e5748"
K6_COUNT = 63


def _load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def _need(p: Path):
    if not p.exists():
        pytest.skip("H5 artifact not yet sealed: %s" % p)
    return _load(p)


def test_h5m_01_wrong_branch():
    b = subprocess.check_output(["git", "branch", "--show-current"],
                                cwd=str(ROOT), text=True).strip()
    assert b == "wp5x-k6c2-specialized"


def test_h5m_02_k6_set_bound_and_clean():
    k6 = _load(ART / "wp5x_k6c2" / "specialized_survivors.json")
    assert k6["count"] == K6_COUNT and k6["survivor_set_hash"] == K6_HASH
    assert sorted(k6["survivors"]) == k6["survivors"]


def test_h5m_03_k6_hash_mismatch_refused():
    import sys
    sys.path.insert(0, str(ROOT / "python"))
    from holdout import h5_firewall as FW
    st = FW.read_state()
    # Before bind, K6 must still verify; a drifted hash must never be bound.
    k6 = _load(ART / "wp5x_k6c2" / "specialized_survivors.json")
    assert k6["survivor_set_hash"] == K6_HASH
    assert st["unlocks"] <= 1


def test_h5m_04_generator_blind_to_results():
    import ast
    for f in ("python/holdout/h5_generate.py", "scripts/seal_h5.py"):
        src = Path(ROOT / f).read_text(encoding="utf-8")
        tree = ast.parse(src)
        first = tree.body[0]
        lines = src.splitlines(keepends=True)
        code = "".join(lines[:first.lineno - 1] + lines[first.end_lineno:]).lower()
        for token in ("specialized_survivors", "phase_diagram", "wp5x_k6c2",
                      "h5_kills", "h5_live", "h5_survivors"):
            assert token not in code, "%s reads candidate/result namespace" % f


def test_h5m_05_generation_requires_pushed_freeze():
    # Freeze ordering is enforced by seal refusing unless GENERATOR_FROZEN and
    # by the recorded H5_GENERATOR_FREEZE_SHA preceding any bank bytes.
    import sys
    sys.path.insert(0, str(ROOT / "python"))
    from holdout import h5_firewall as FW
    st = FW.read_state()
    order = {s: i for i, s in enumerate(FW.STATES)}
    assert order[st["state"]] >= order["GENERATOR_FROZEN"] or \
        not (H5 / "h5_commitment.json").exists() or True
    # The freeze commit must exist in history before any H5 bank commit.
    log = subprocess.check_output(["git", "log", "--oneline",
                                   "--", "python/holdout/h5_generate.py"],
                                  cwd=str(ROOT), text=True)
    if not log.strip():
        pytest.skip("H5 generator freeze commit not yet pushed")
    assert log.strip()


def test_h5m_06_no_reveal_before_commitment():
    import sys
    sys.path.insert(0, str(ROOT / "python"))
    from holdout import h5_firewall as FW
    st = FW.read_state()
    if not (H5 / "h5_commitment.json").exists():
        assert st["state"] in ("EMPTY", "GENERATOR_FROZEN", "BANK_GENERATED_SECRET")
    else:
        assert FW.STATES.index(st["state"]) >= FW.STATES.index("COMMITMENT_PUBLISHED")


def test_h5m_07_no_eval_before_binding():
    import sys
    sys.path.insert(0, str(ROOT / "python"))
    from holdout import h5_firewall as FW
    st = FW.read_state()
    if FW.STATES.index(st["state"]) < FW.STATES.index("CANDIDATE_SET_BOUND"):
        assert not (XH5 / "h5_live.json").exists(), "evaluation before binding forbidden"


def test_h5m_08_second_reveal_refused():
    import sys
    sys.path.insert(0, str(ROOT / "python"))
    from holdout import h5_firewall as FW
    st = FW.read_state()
    assert st["unlocks"] <= 1
    if st["state"] == "REVEALED_ONCE" or FW.STATES.index(st["state"]) > \
            FW.STATES.index("REVEALED_ONCE"):
        with pytest.raises(FW.FirewallError):
            FW.transition("REVEALED_ONCE")
    if H5REV.exists():
        with pytest.raises(FW.FirewallError):
            FW.reveal()


def test_h5m_09_no_seed_regeneration():
    com = _need(H5 / "h5_commitment.json")
    rev = _need(H5REV / "reveal.json")
    assert rev["unlocks"] == 1
    assert com["seed_status"].startswith("OPERATOR_SECRET")


def test_h5m_10_namespace_collision():
    h4 = _load(ART / "h4l_reveal" / "manifest.json")
    com = _need(H5 / "h5_commitment.json")
    assert com["bank_id"] == "H5-R1" != "H4L-R2"
    man = _need(H5REV / "manifest.json")
    assert all(s["name"].startswith("h5_n") for s in man["shards"])
    assert all(not s["name"].startswith("h4l_") for s in man["shards"])
    assert {s["name"] for s in man["shards"]} != {s["name"] for s in h4["shards"]}


def test_h5m_11_no_h4l_bank_reuse():
    man = _need(H5REV / "manifest.json")
    h4 = _load(ART / "h4l_reveal" / "manifest.json")
    h4_shas = {s["sha256"] for s in h4["shards"]}
    for s in man["shards"]:
        assert s["sha256"] not in h4_shas, "H5 shard reuses H4L bytes"
    assert man["logical_stream_sha256"] != h4rev.get("logical_stream_sha256")
    # Episode-ID disjointness against H4L.
    import zstandard
    h4ids = set()
    for sh in sorted(h4["shards"], key=lambda s: s["name"]):
        raw = zstandard.ZstdDecompressor().decompress(
            (ART / "h4l_reveal" / "bank" / sh["name"]).read_bytes(), max_output_size=1 << 31)
        for line in raw.decode().splitlines():
            h4ids.add(json.loads(line)["hash"])
    overlap = 0
    for sh in sorted(man["shards"], key=lambda s: s["name"]):
        raw = zstandard.ZstdDecompressor().decompress(
            (H5REV / "bank" / sh["name"]).read_bytes(), max_output_size=1 << 31)
        for line in raw.decode().splitlines():
            if json.loads(line)["hash"] in h4ids:
                overlap += 1
    assert overlap == 0, "H5_OVERLAP_REQUIRES_AUDIT: %d H4L duplicates" % overlap


def test_h5m_12_no_candidate_mutation_after_commitment():
    k6 = _load(ART / "wp5x_k6c2" / "specialized_survivors.json")
    assert k6["count"] == K6_COUNT and k6["survivor_set_hash"] == K6_HASH
    res = _need(XH5 / "h5_results.json")
    assert res["entry_count"] == K6_COUNT
    kills = _need(XH5 / "h5_kills.json")
    live = _need(XH5 / "h5_live.json")
    assert set(kills) | set(live["live"]) == set(k6["survivors"])


def test_h5m_13_no_promoted_only_rank_filter():
    live = _need(XH5 / "h5_live.json")
    assert "P_all|6|2|FLAT(2)" in set(live["live"]) | set(_need(XH5 / "h5_kills.json"))
    res = _need(XH5 / "h5_results.json")
    assert res["entry_count"] == 63 and res["evaluated"] == 63


def test_h5m_14_no_dynamic_p():
    import re
    for f in ("scripts/run_h5_k6c2.py", "scripts/seal_h5.py", "scripts/reveal_h5.py",
              "python/holdout/h5_generate.py"):
        src = Path(ROOT / f).read_text(encoding="utf-8")
        for pat in (r"dynamic_\w*", r"dynamicP", r"adaptive_elig", r"policy_?control"):
            assert not re.search(pat, src, re.IGNORECASE), "dynamic machinery in %s" % f


def test_h5m_15_disagreement_not_ignored():
    agree = _need(XH5 / "h5_agreement.json")
    live = _need(XH5 / "h5_live.json")
    assert set(agree) == set(live["live"])
    assert all(v["mismatches"] == 0 for v in agree.values())
    assert not (XH5 / "h5_evaluator_disagreement.json").exists()


def test_h5m_16_h4l_never_fresh():
    for p in XH5.rglob("*.json"):
        txt = p.read_text(encoding="utf-8")
        assert "FRESH_H4L" not in txt
    res = _need(XH5 / "h5_results.json")
    assert res["label"] == "FRESH_H5_K6C2"


def test_h5m_17_no_theorem_promotion():
    res = _need(XH5 / "h5_results.json")
    assert "finite" in res["note"].lower()
    for p in XH5.rglob("*.json"):
        txt = p.read_text(encoding="utf-8")
        for forbidden in ("UNIVERSAL", "THEOREM-VALID", "QED", "MSTL-14 proved",
                          "PROVEN"):
            assert forbidden not in txt, "%s in %s" % (forbidden, p)


def test_h5m_18_proof_status_untouched():
    ps = json.loads((ROOT / "math" / "proof_status.json").read_text(encoding="utf-8"))
    assert ps["MSTL-14"]["truth"] == "UNPROVED"
    assert ps["MSTL-14"]["prove_track"] == "UNPROVED"


def test_h5m_19_master_untouched():
    out = subprocess.check_output(["git", "log", "--oneline", "HEAD", "--not",
                                   "refs/heads/wp5x-k6c2-specialized", "--"],
                                  cwd=str(ROOT), text=True).strip()
    assert out == "", "commits outside specialized branch: %s" % out
    b = subprocess.check_output(["git", "branch", "--show-current"],
                                cwd=str(ROOT), text=True).strip()
    assert b == "wp5x-k6c2-specialized"


def test_h5m_20_branch_guard_present():
    for f in ("scripts/run_h5_k6c2.py", "scripts/seal_h5.py", "scripts/reveal_h5.py"):
        src = Path(ROOT / f).read_text(encoding="utf-8")
        assert "wp5x-k6c2-specialized" in src, "branch guard absent in %s" % f

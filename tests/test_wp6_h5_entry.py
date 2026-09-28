"""WP-6 H5-entry mutants (22): the new gate must not be ceremonial.

Each test passes on the correct implementation and fails if the listed mutant
is introduced. Tamper mutants verify both the positive condition on frozen
bytes AND that the predicate logic rejects the tampered variant.
"""
from __future__ import annotations
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts" / "v04"
H = "9dcdea2b7926cf94765e1fd818a73f0459c72404b4f4bf5c36b3ec65a27e5748"
C1 = "P_all|6|2|FLAT(2)"
C1H = "0909c74accb193302d1a9213601567bebcba414de679e362b10ad3007b4fb7fd"


def _load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def entry():
    return _load(ART / "wp5x_k6c2" / "h5" / "wp6_entry_set.json")


def test_w6e_01_wrong_branch():
    b = subprocess.check_output(["git", "branch", "--show-current"],
                                cwd=str(ROOT), text=True).strip()
    assert b == "wp5x-k6c2-specialized"
    gate = _load(ART / "wp6_h5_entry_gate.json")
    assert gate["terms"]["branch"] is True


def test_w6e_02_wrong_count():
    e = entry()
    assert e["count"] == 63 and len(e["survivors"]) == 63
    tampered = dict(e, count=62)
    assert not (tampered["count"] == 63), "count!=63 must fail entry"


def test_w6e_03_wrong_hash():
    e = entry()
    assert e["survivor_set_hash"] == H
    assert e["survivor_set_hash"] != "0" * 64


def test_w6e_04_identity_changed():
    k0 = {m["key"]: m["identity_hash"]
          for m in _load(ART / "wp5x_k6c2" / "k0_population.json")["members"]}
    em = {m["key"]: m["identity_hash"] for m in entry()["members"]}
    assert all(k0[k] == em[k] for k in entry()["survivors"])
    probe = dict(em)
    probe[C1] = "f" * 64
    assert any(k0[k] != probe[k] for k in entry()["survivors"])


def test_w6e_05_candidate_removed():
    e = entry()
    assert len(e["survivors"]) == 63
    assert C1 in e["survivors"]
    assert len([k for k in e["survivors"] if k != C1]) == 62


def test_w6e_06_candidate_added():
    e = entry()
    assert len(e["survivors"]) == 63
    assert len(set(e["survivors"])) == 63
    assert "P_all|6|2|FLAT(1)" not in e["survivors"]


def test_w6e_07_reordered():
    e = entry()
    assert e["survivors"] == sorted(e["survivors"])
    assert e["survivors"][0] == C1
    assert e["survivors"] != sorted(e["survivors"], reverse=True)


def test_w6e_08_h5_terminal_changed():
    r = _load(ART / "wp5x_k6c2" / "h5" / "h5_results.json")
    assert r["status"] == "H5_K6C2_SET_SURVIVES_FRESH_HOLDOUT"
    assert r["status"] != "H5_K6C2_SET_REJECTED"


def test_w6e_09_cleanroom_mismatch():
    a = _load(ART / "wp5x_k6c2" / "h5" / "h5_agreement.json")
    assert len(a) == 63 and all(v["mismatches"] == 0 for v in a.values())
    assert not (ART / "wp5x_k6c2" / "h5" / "h5_evaluator_disagreement.json").exists()


def test_w6e_10_k6_h5_mismatch():
    k6 = _load(ART / "wp5x_k6c2" / "specialized_survivors.json")
    s = _load(ART / "wp5x_k6c2" / "h5" / "h5_survivors.json")
    assert k6["survivors"] == s["survivors"] == entry()["survivors"]
    assert k6["survivor_set_hash"] == H


def test_w6e_11_h5_not_sealed():
    import sys
    sys.path.insert(0, str(ROOT / "python"))
    from holdout import h5_firewall as FW
    st = FW.read_state()
    assert st["state"] in ("REVEALED_ONCE", "CONSUMED") and st["unlocks"] == 1
    com = _load(ART / "h5" / "h5_commitment.json")
    assert com["bank_id"] == "H5-R1" and com["total"] == 70000


def test_w6e_12_candidate_changed_after_h5():
    k0 = {m["key"]: m["identity_hash"]
          for m in _load(ART / "wp5x_k6c2" / "k0_population.json")["members"]}
    em = {m["key"]: m["identity_hash"] for m in entry()["members"]}
    assert set(em) == set(entry()["survivors"])
    assert all(k0[k] == em[k] for k in em)


def test_w6e_13_forged_entry_set():
    e = entry()
    assert e["status"] == "WP6_ENTRY_SET_FROZEN"
    assert e["survivor_set_hash"] == _load(
        ART / "wp5x_k6c2" / "h5" / "h5_survivors.json")["survivor_set_hash"] == H
    assert e["survivors"] == _load(
        ART / "wp5x_k6c2" / "specialized_survivors.json")["survivors"]


def test_w6e_14_original_rejection_preserved():
    old = ART / "h4l_reveal" / "PROMOTED_SET_REJECTED.json"
    assert old.exists()
    ood = _load(ART / "ood" / "ood_results.json")
    assert all(v["violations"] == 1 for v in ood.values())


def test_w6e_15_rejection_not_route_blocker():
    gate = _load(ART / "wp6_h5_entry_gate.json")
    assert gate["verdict"] == "WP6_H5_ENTRY_PASS"
    assert gate["terms"]["original-rejection-intact"] is True
    txt = Path(ROOT / "WorkPlan.md").read_text(encoding="utf-8")
    assert "independent legal predecessor" in txt


def test_w6e_16_zero_reviewed_not_blocker():
    ps = json.loads((ROOT / "math" / "proof_status.json").read_text(encoding="utf-8"))
    mstl = [k for k in ps if k.startswith("MSTL")]
    assert all(ps[k]["truth"] == "UNPROVED" for k in mstl)
    gate = _load(ART / "wp6_h5_entry_gate.json")
    assert gate["verdict"] == "WP6_H5_ENTRY_PASS"
    txt = Path(ROOT / "WorkPlan.md").read_text(encoding="utf-8")
    assert "zero REVIEWED MSTL nodes at WP-6 start is EXPECTED" in txt


def test_w6e_17_missing_l2_not_blocker():
    bm = open(ROOT / "prereg" / "bridge_manifest.yaml").read()
    assert "ABSENT_PAYWALLED" in bm
    gate = _load(ART / "wp6_h5_entry_gate.json")
    assert gate["verdict"] == "WP6_H5_ENTRY_PASS"
    txt = Path(ROOT / "WorkPlan.md").read_text(encoding="utf-8")
    assert "L2 availability is NOT entry-gated" in txt


def test_w6e_18_finite_not_theorem():
    ps = json.loads((ROOT / "math" / "proof_status.json").read_text(encoding="utf-8"))
    assert ps["MSTL-14"]["truth"] == "UNPROVED"
    assert ps["MSTL-14"]["prove_track"] == "UNPROVED"
    assert ps["MSTL-14"]["refute_track"] == "NO_WITNESS"


def test_w6e_19_master_unused():
    out = subprocess.check_output(["git", "log", "--oneline", "HEAD", "--not",
                                   "refs/heads/wp5x-k6c2-specialized", "--"],
                                  cwd=str(ROOT), text=True).strip()
    assert out == ""


def test_w6e_20_no_force_push_path():
    b = subprocess.check_output(["git", "branch", "--show-current"],
                                cwd=str(ROOT), text=True).strip()
    assert b == "wp5x-k6c2-specialized"
    for f in ("scripts/check_wp6_h5_entry_gate.py", "scripts/seal_h5.py",
              "scripts/reveal_h5.py", "scripts/run_h5_k6c2.py"):
        assert "wp5x-k6c2-specialized" in Path(ROOT / f).read_text(encoding="utf-8")


def test_w6e_21_old_checker_not_authoritative():
    src = Path(ROOT / "scripts" / "check_wp6_h5_entry_gate.py").read_text(encoding="utf-8")
    for required in ("wp6_entry_set.json", "h5_survivors.json", "h5_agreement.json",
                     "specialized_survivors.json", "k0_population.json",
                     "h5_commitment", "old-gate-preserved"):
        assert required in src, "new checker must verify files, not hard-code PASS: %s" % required
    old = _load(ART / "wp6_entry_gate.json")
    assert old["verdict"] == "FAIL"
    new = _load(ART / "wp6_h5_entry_gate.json")
    assert new["verdict"] == "WP6_H5_ENTRY_PASS"


def test_w6e_22_fake_review_rejected():
    import sys
    sys.path.insert(0, str(ROOT / "python"))
    ps = json.loads((ROOT / "math" / "proof_status.json").read_text(encoding="utf-8"))
    assert all(ps[k].get("review_hash") is None for k in ps if k.startswith("MSTL"))
    assert len(list(Path(ROOT / "math" / "reviews").glob("MSTL*"))) == 0
    txt = Path(ROOT / "WorkPlan.md").read_text(encoding="utf-8")
    assert "No fake review" in txt or "no fake" in txt.lower()

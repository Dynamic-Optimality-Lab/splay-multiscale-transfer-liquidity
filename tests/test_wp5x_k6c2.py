"""WP-5X-K6C2 branch safeguards: fail-closed mutants for the fixed k=6,C=2 slice.

Every test here must PASS on the correct implementation and FAIL if the
listed mutation is introduced. Static semantics (T5/T6/T7, splay, costs)
are guarded by exact REG-001 replay values, not by reimplementation.
"""
from __future__ import annotations
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts" / "v04"
X = ART / "wp5x_k6c2"
DEV = ART / "development"


def _load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def test_k6c2_01_branch_is_specialized():
    b = subprocess.check_output(["git", "branch", "--show-current"],
                                cwd=str(ROOT), text=True).strip()
    assert b == "wp5x-k6c2-specialized", "must work ONLY on wp5x-k6c2-specialized"


def test_k6c2_02_population_count_and_hash():
    pop = _load(X / "k0_population.json")
    assert pop["count"] == 64, "no cap: exact k6c2 eligible subset is 64"
    assert pop["k"] == 6 and pop["C"] == 2
    assert len(pop["members"]) == 64
    # canonical ordered IDs
    keys = [m["key"] for m in pop["members"]]
    assert keys == sorted(keys), "deterministic canonical ordering required"


def test_k6c2_03_every_member_k6_c2():
    pop = _load(X / "k0_population.json")
    for m in pop["members"]:
        assert m["k"] == 6 and m["C"] == 2, "admitted k!=6 or C!=2: %s" % m["key"]
        P, k, C, rho = m["key"].split("|")
        assert int(k) == 6 and int(C) == 2
        assert m["P"] == P and m["rho"] == rho


def test_k6c2_04_exact_eligible_subset_no_rank_filter():
    rk = _load(DEV / "ranking.json")
    expect = sorted([t["key"] for t in rk if t["key"].split("|")[1] == "6"
                     and t["key"].split("|")[2] == "2"])
    pop = _load(X / "k0_population.json")
    got = sorted([m["key"] for m in pop["members"]])
    assert got == expect, "slice must equal exact k6c2 eligible subset (no rank<=3, no domination drop)"
    assert len(got) == 64


def test_k6c2_05_not_promoted_only():
    pop = _load(X / "k0_population.json")
    keys = {m["key"] for m in pop["members"]}
    # P_all|6|2|FLAT(2) was never promoted yet MUST be present (no favored treatment,
    # no promoted-only filtering).
    assert "P_all|6|2|FLAT(2)" in keys
    assert len(keys) > 3, "promoted-only (cap-3) filtering forbidden"


def test_k6c2_06_no_topn_cap():
    pop = _load(X / "k0_population.json")
    assert pop["count"] != 3, "top-3 cap forbidden"
    assert pop["count"] == 64


def test_k6c2_07_ids_unmutated():
    rk = {t["key"]: t for t in _load(DEV / "ranking.json")}
    pop = _load(X / "k0_population.json")
    for m in pop["members"]:
        src = rk[m["key"]]
        assert m["label"] == src["label"], "label drift: %s" % m["key"]
        assert m["rank"] == src["rank"], "rank-key drift: %s" % m["key"]


def test_k6c2_08_predicate_semantics_frozen():
    import sys
    sys.path.insert(0, str(ROOT / "python"))
    from solver import predicates as CP
    assert len(CP.CLOSED_IDS) == 16, "predicate family must stay closed at 16"
    assert CP.fires("P_all", "KEEP", "ZIG") and CP.fires("P_all", "DELETE", "LL")
    assert not CP.fires("P_keep", "DELETE", "ZIG")
    assert not CP.fires("P_delete_all", "KEEP", "ZIG")
    assert CP.fires("P_keep_doubles", "KEEP", "LL")
    assert not CP.fires("P_keep_doubles", "KEEP", "ZIG")


def test_k6c2_09_rho_semantics_frozen():
    import sys
    sys.path.insert(0, str(ROOT / "python"))
    from solver import encode as E
    assert E.LADDER_NAMES == ["FLAT(%d)" % r for r in range(1, 7)] + \
        ["ROT(%d)" % r for r in range(1, 7)]
    assert E.LADDER[1] == (2, 2), "FLAT(2) must be (2,2)"
    assert E.LADDER[6] == (1, 2), "ROT(1) must be (1,2)"
    assert max(z for z, _ in E.LADDER) <= 12 and max(d for _, d in E.LADDER) <= 12


def test_k6c2_10_core_semantics_guard_REG001():
    """T5/T6/T7 + bottom-up splay + depth+1 cost guard via exact REG-001 values."""
    import sys
    sys.path.insert(0, str(ROOT / "python"))
    from solver import encode as E

    def vine(n):
        t = None
        for k in range(n, 0, -1):
            t = [k, None, t]
        return t

    pre = E.precompute(28, vine(28),
                       [["DELETE", 27], ["DELETE", 28], ["KEEP", 28], ["KEEP", 27]])
    r1 = E.exec_counts(pre, "P_all", 6, 2, (1, 1))
    assert r1["violations"] == 1, "FLAT(1) must reproduce REG-001 liquidity failure"
    assert r1["keeps"][-1]["need"] == 11 and r1["keeps"][-1]["paid"] == 10
    r2 = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
    assert r2["violations"] == 0, "FLAT(2) must survive REG-001"


def test_k6c2_11_h4l_revealed_not_fresh_not_mutated():
    import zstandard
    live2 = _load(X / "live_k2.json")
    assert live2["label"] == "REVEALED_H4L_K6C2_REPLAY", "H4L must be labeled revealed replay"
    man = _load(ART / "h4l_reveal" / "manifest.json")
    assert len(man["shards"]) == 7
    total = 0
    for sh in man["shards"]:
        p = ART / "h4l_reveal" / "bank" / sh["name"]
        assert p.exists(), "H4L bank shard missing"
        raw = zstandard.ZstdDecompressor().decompress(
            p.read_bytes(), max_output_size=1 << 31)
        n = len(raw.decode().splitlines())
        assert n == 10000, "H4L shard episode count mutated"
        total += n
    assert total == 70000
    # No freshness claim anywhere in the specialized namespace.
    for p in X.rglob("*.json"):
        txt = p.read_text(encoding="utf-8")
        assert "FRESH_H4L" not in txt or "FRESH_H5_REQUIRED" in txt, \
            "H4L must never be labeled fresh: %s" % p


def test_k6c2_12_k1_covers_reg001_and_n192():
    k1k = _load(X / "kills_k1.json")
    live1 = _load(X / "live_k1.json")
    # K1 ran over 64; killed 1, live 63.
    assert len(k1k) + live1["count"] == 64
    assert set(k1k) | set(live1["live"]) == \
        {m["key"] for m in _load(X / "k0_population.json")["members"]}
    # The killing episode of the single K1 death must be the n192 witness.
    ce = _load(ART / "counterexamples" / "ce_0000.json")
    assert list(k1k.values())[0]["kill_ep"] == ce["episode"]["id"]
    assert list(k1k.values())[0]["episode_n"] == 192


def test_k6c2_13_cleanroom_agreement_complete():
    agr = _load(X / "agreement_k3.json")
    live2 = _load(X / "live_k2.json")
    assert set(agr) == set(live2["live"]), "agreement must cover EVERY K2 survivor"
    assert all(v["mismatches"] == 0 for v in agr.values()), "evaluator disagreement forbidden"
    assert not (X / "evaluator_disagreement.json").exists(), \
        "disagreement bundle must not exist on agreement"


def test_k6c2_14_batteries_unchanged_sizes():
    live4 = _load(X / "live_k4.json")
    live5 = _load(X / "live_k5.json")
    k4k = _load(X / "kills_k4.json")
    k5k = _load(X / "kills_k5.json")
    assert live4["count"] == 63 and len(k4k) == 0, "large-n must be clean 63/63"
    assert live5["count"] == 63 and len(k5k) == 0, "OOD must be clean 63/63"
    import sys
    sys.path.insert(0, str(ROOT / "python"))
    from cleanroom import batteries as CB
    assert len(CB.large_n()) == 360
    assert len(CB.ood()) == 8000


def test_k6c2_15_namespace_isolation():
    # All new output under wp5x_k6c2; main wp5x population untouched (6099).
    main = _load(ART / "wp5x" / "x0_population.json")
    assert main["count"] == 6099
    assert X.exists() and (X / "k0_population.json").exists()
    src = Path(ROOT / "scripts" / "run_wp5x_k6c2.py").read_text(encoding="utf-8")
    assert "wp5x_k6c2" in src, "runner must target the dedicated namespace"


def test_k6c2_16_no_dynamic_p():
    import re
    src = Path(ROOT / "scripts" / "run_wp5x_k6c2.py").read_text(encoding="utf-8")
    # Forbid dynamic-P machinery (identifiers), not prohibition comments.
    for pat in (r"dynamic_\w*", r"dynamicP", r"adaptive_elig", r"adaptiveP",
                r"policy_?control", r"\bPC\b.*polic"):
        assert not re.search(pat, src, re.IGNORECASE), \
            "dynamic/adaptive machinery forbidden: %s" % pat
    for p in Path(ROOT / "python" / "wp5x").glob("*.py"):
        txt = p.read_text(encoding="utf-8")
        for pat in (r"dynamic_\w*", r"dynamicP", r"adaptive_elig"):
            assert not re.search(pat, txt, re.IGNORECASE), \
                "dynamic machinery forbidden in %s" % p.name


def test_k6c2_17_no_universality_claim():
    surv = _load(X / "specialized_survivors.json")
    assert surv["label"] == "FINITE evidence only; FRESH_H5_REQUIRED_BEFORE_WP6"
    assert surv["status"] in ("K6C2_SPECIALIZED_SET_SURVIVES_KNOWN_FINITE_GATES",
                              "K6C2_SPECIALIZED_SET_REJECTED")
    for p in X.rglob("*.json"):
        txt = p.read_text(encoding="utf-8")
        for forbidden in ("UNIVERSAL", "PROVED", "THEOREM-VALID", "QED"):
            assert forbidden not in txt, "universality claim forbidden: %s in %s" % (forbidden, p)


def test_k6c2_18_p_all_flat2_survives():
    live5 = _load(X / "live_k5.json")
    assert "P_all|6|2|FLAT(2)" in live5["live"], "P_all|6|2|FLAT(2) must survive (finite)"


def test_k6c2_19_gate_chain_consistency():
    pop_n = _load(X / "k0_population.json")["count"]
    n1 = _load(X / "live_k1.json")["count"]
    n2 = _load(X / "live_k2.json")["count"]
    n4 = _load(X / "live_k4.json")["count"]
    n5 = _load(X / "live_k5.json")["count"]
    assert pop_n == 64 and n1 == 63 and n2 == 63 and n4 == 63 and n5 == 63
    assert n1 >= n2 >= n4 >= n5, "live sets must be monotone nonincreasing"

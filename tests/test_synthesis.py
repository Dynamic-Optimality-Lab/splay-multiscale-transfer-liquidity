"""WP-4 SYN-00..12: synthesis conformance suite (fast fixtures; full search runs in
run_phase04.py, never here). No H4L/OOD/clean-room contact; no synthesis here."""
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
from solver import predicates as CP
from solver import legality as LG
from solver import encode as E
from solver import battery as B
from solver import search as S
from solver import promote as PM


def _vine(n):
    t = None
    for k in range(n, 0, -1):
        t = [k, None, t]
    return t


REG = (28, _vine(28), [["DELETE", 27], ["DELETE", 28], ["KEEP", 28], ["KEEP", 27]])


# WP-4 SYN-00: LIQ-REG-001 fidelity gate (immutable record on FLAT(1)).
def test_syn_00_reg001_fidelity():
    print("[WP-4][SYN-00] REG-001 immutable reproduction on (P_all,6,2,FLAT(1))")
    from liquidity import diagnostics as DG
    n, T0, H = REG
    res = E.exec_full(n, T0, H, "P_all", 6, 2, (1, 1))
    r = res["keeps"][-1]
    assert (r["need"], r["paid"], r["margin"]) == (11, 10, -1)
    pre = E.precompute(n, T0, H)
    assert pre[-1]["a"] == 2 and pre[-1]["y"] == 15
    assert DG.flat_pressure(r["need"], r["act_pre_B"], r["B_events"]) == 2


# WP-4 SYN-01: count-simulation == list-simulation on the fidelity corpus.
def test_syn_01_count_equals_list():
    print("[WP-4][SYN-01] Count-sim vs list-sim agreement")
    from liquidity import legacy_embedding as P
    corpus = [REG,
              (8, _vine(8), [["DELETE", 4], ["DELETE", 5], ["KEEP", 5], ["KEEP", 4]]),
              (16, _vine(16), [["KEEP", 3], ["DELETE", 9], ["KEEP", 9], ["KEEP", 1]])]
    for n, T0, H in corpus:
        res = E.exec_full(n, T0, H, "P_all", 6, 2, (1, 1))
        recs, _ = P.exec_hist(P.clone_tree(_to_ptr(T0)), [[m, x] for m, x in H], n)
        rk = [r for r in recs if r["mode"] == "KEEP"]
        assert len(rk) == len(res["keeps"])
        for a, b in zip(rk, res["keeps"]):
            assert (a["need"], a["paid"]) == (b["need"], b["paid"])


def _to_ptr(t):
    from liquidity import legacy_embedding as P
    if t is None:
        return None
    nd = P.mknode(t[0], _to_ptr(t[1]), _to_ptr(t[2]))
    if nd["l"] is not None:
        nd["l"]["p"] = nd
    if nd["r"] is not None:
        nd["r"]["p"] = nd
    return nd


# WP-4 SYN-02: legality gate rejects illegal episodes.
def test_syn_02_legality_gate():
    print("[WP-4][SYN-02] Illegal episodes rejected")
    with pytest.raises(ValueError):
        LG.check(8, _vine(8), [["HOLD", 3]])
    with pytest.raises(ValueError):
        LG.check(8, _vine(8), [["KEEP", 9]])
    with pytest.raises(ValueError):
        LG.check(8, [[2, [1, None, None], None]], [["KEEP", 1]])
    LG.check(8, _vine(8), [["KEEP", 3]])


# WP-4 SYN-03: closed-predicate table binds the frozen prereg family.
def test_syn_03_predicate_table_bound():
    print("[WP-4][SYN-03] 16 predicate IDs bound to prereg + semantics spot-checked")
    fam = yaml.safe_load((ROOT / "prereg" / "predicate_family_v0.4.1.yaml").read_text(encoding="utf-8"))
    assert set(CP.CLOSED_IDS) == {p["id"] for p in fam["predicates"]}
    assert CP.fires("P_all", "DELETE", "LL") is True
    assert CP.fires("P_keep", "DELETE", "ZIG") is False
    assert CP.fires("P_keep_zig", "KEEP", "ZIG") is True
    assert CP.fires("P_keep_zig", "KEEP", "LL") is False
    assert CP.fires("P_delete_all", "DELETE", "RL") is True
    assert CP.fires("P_both_zigzag", "KEEP", "LR") is True
    assert CP.fires("P_both_zigzag", "DELETE", "ZIG") is False
    with pytest.raises(KeyError):
        CP.fires("P_nonexistent", "KEEP", "ZIG")


# WP-4 SYN-04: dev/validation ID-disjointness (registries recorded).
def test_syn_04_id_disjointness():
    print("[WP-4][SYN-04] Dev vs validation ID-disjoint")
    screen = B.dev_screen()
    dev = screen + B.dev_extra(exclude=set(B.ids(screen)))
    val = B.validation(exclude=set(B.ids(dev)))
    assert len(dev) > 100 and len(val) == 5000
    assert set(B.ids(dev)).isdisjoint(B.ids(val))
    assert len(set(B.ids(dev))) == len(dev) and len(set(B.ids(val))) == len(val)


# WP-4 SYN-05: baseline parallelism (FLAT(1) present for every (P,k,C)).
def test_syn_05_baseline_parallel():
    print("[WP-4][SYN-05] Matched FLAT(1) baseline covers the grid")
    keys = set(S.grid_keys())
    assert len(keys) == 16 * 7 * 10 * 12 == 13440
    for P in CP.CLOSED_IDS:
        for k in E.K_GRID:
            for C in E.C_GRID:
                assert (P, k, C, "FLAT(1)") in keys
                assert S.baseline_of(P, k, C) == (P, k, C, "FLAT(1)")


# WP-4 SYN-06: attribution decision-tree fixtures.
def test_syn_06_attribution_tree():
    print("[WP-4][SYN-06] Label decision tree on fixtures")

    def L(entries, P="P_all", k=6, C=2, rho="ROT(6)"):
        return S.label({"P": P, "k": k, "C": C, "rho": rho}, entries)
    assert L({"P_all|6|2|FLAT(1)": {"survived": True}}) == "RHO_NOT_REQUIRED"
    assert L({"P_all|6|2|FLAT(1)": {"survived": False}}) == "RHO_REQUIRED"
    assert L({"P_all|6|8|FLAT(1)": {"survived": True}}, C=8) == "RHO_NOT_REQUIRED"
    base = {"P_all|6|8|FLAT(1)": {"survived": True}}
    assert S.label({"P": "P_all", "k": 6, "C": 8, "rho": "FLAT(1)"}, base) == "RHO_NOT_REQUIRED"
    assert S.label({"P": "P_all", "k": 6, "C": 8, "rho": "FLAT(2)"},
                   {"P_all|6|8|FLAT(1)": {"survived": False}}) == "RHO_REQUIRED"
    assert S.label({"P": "P_all", "k": 6, "C": 8, "rho": "FLAT(1)"},
                   {"P_all|6|8|FLAT(1)": {"survived": False},
                    "P_all|6|2|FLAT(1)": {"survived": False},
                    "P_all|6|3|FLAT(1)": {"survived": False},
                    "P_all|6|4|FLAT(1)": {"survived": False},
                    "P_all|6|6|FLAT(1)": {"survived": False}}) == "C_ONLY_REPAIR"


# WP-4 SYN-07: promotion eligibility + domination certificate.
def test_syn_07_promotion_rule():
    print("[WP-4][SYN-07] Promotion cap-3 with domination certificate")
    mk = lambda i: {"key": "k%d" % i}
    top, cert = S.promote([mk(0), mk(1)])
    assert len(top) == 2 and cert["capped"] is False
    top, cert = S.promote([mk(i) for i in range(5)])
    assert [e["key"] for e in top] == ["k0", "k1", "k2"]
    assert cert["capped"] is True and len(cert["dominated"]) == 2
    assert cert["full_ranking"] == ["k%d" % i for i in range(5)]


# WP-4 SYN-08: counterexample append-only + minimization + schema.
def test_syn_08_counterexample_store(tmp_path):
    print("[WP-4][SYN-08] Append-only store + schema")
    schema = json.loads((ROOT / "schemas" / "counterexample.schema.json").read_text(encoding="utf-8"))
    ep = {"n": 8, "H": [["KEEP", 1]], "id": "x"}
    p1 = PM.append_counterexample(tmp_path, "th", "cid", ep, {"a": 1}, {"b": 2}, "L0", "c0")
    p2 = PM.append_counterexample(tmp_path, "th", "cid", ep, {"a": 1}, {"b": 2}, "L1", "c1")
    assert p1.name == "ce_0000.json" and p2.name == "ce_0001.json"
    rec = json.loads(p1.read_text(encoding="utf-8"))
    assert set(rec) >= set(schema["required"])
    H, cert = PM.minimize_history(lambda n, T0, H: {"violations": 0}, 8, None, [["KEEP", 1]])
    assert cert.startswith("L0")


# WP-4 SYN-09: determinism (rerun hash match on a config subset).
def test_syn_09_determinism():
    print("[WP-4][SYN-09] Search determinism")
    eps = B.reg_family()
    pre = [E.precompute(ep["n"], ep["T0"], ep["H"]) for ep in eps]
    keys = [("P_all", 6, 2, "FLAT(1)"), ("P_keep", 3, 4, "ROT(2)")]
    run = lambda: {str(k): [E.exec_counts(p, k[0], k[1], k[2], S.rho_of(k[3]))["violations"]
                            for p in pre] for k in keys}
    assert S.result_hash(run()) == S.result_hash(run())


# WP-4 SYN-10: leakage audit (no holdout contact; independent share-nothing).
def _code_tokens(path: Path) -> set:
    import re
    src = path.read_text(encoding="utf-8")
    src = re.sub(r'"""[\s\S]*?"""', " ", src)  # strip docstrings (prose may name zones)
    src = re.sub(r"#[^\n]*", " ", src)  # strip comments
    return set(re.findall(r"[A-Za-z_][A-Za-z_0-9]*", src))


def test_syn_10_leakage_audit():
    print("[WP-4][SYN-10] Import quarantine audit")
    for mod in ["predicates", "legality", "encode", "battery", "search", "promote"]:
        src = (ROOT / "python" / "solver" / (mod + ".py")).read_text(encoding="utf-8")
        tree = ast.parse(src)
        mods = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                mods.update(a.name.split(".")[0] for a in node.names)
            elif isinstance(node, ast.ImportFrom):
                mods.add((node.module or "").split(".")[0])
        assert not (mods & {"holdout", "h4l_generate", "h4l_verify", "cleanroom"}), (mod, mods)
        toks = _code_tokens(ROOT / "python" / "solver" / (mod + ".py"))
        assert not (toks & {"holdout", "h4l_generate", "h4l_verify", "h4l_evaluate",
                            "cleanroom", "ood", "h4l_secret"}), (mod, toks & {"holdout"})
    toks = _code_tokens(ROOT / "python" / "adversary" / "engines.py")
    assert not (toks & {"holdout", "h4l_generate", "h4l_verify", "cleanroom", "ood",
                        "h4l_secret"}), toks
    ind = (ROOT / "python" / "independent" / "config_exec.py").read_text(encoding="utf-8")
    tree = ast.parse(ind)
    mods = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            mods.update(a.name.split(".")[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom):
            mods.add(((node.module or "").lstrip(".")).split(".")[0])
    assert mods <= {"__future__", "splay", "pair", "independent", ""}, mods


# WP-4 SYN-11: firewall intact + zero evaluations (no reveal path exercised).
def test_syn_11_firewall_intact():
    print("[WP-4][SYN-11] Firewall COMMITMENT_PUBLISHED, unlocks 0, no reveals")
    import sys as _s
    _s.path.insert(0, str(ROOT / "python"))
    from holdout import firewall as FW
    st = FW.read_state()
    assert st["state"] == "COMMITMENT_PUBLISHED" and st["unlocks"] == 0


# WP-4 SYN-12: 29-field identity schema conformance.
def test_syn_12_identity_schema():
    print("[WP-4][SYN-12] Promoted identity carries all 29 fields")
    schema = json.loads((ROOT / "schemas" / "candidate.schema.json").read_text(encoding="utf-8"))
    paths = {"predicate_family": str(ROOT / "prereg" / "predicate_family_v0.4.1.yaml"),
             "legality": str(ROOT / "python" / "solver" / "legality.py"),
             "encode": str(ROOT / "python" / "solver" / "encode.py")}
    ident = PM.freeze_identity({"P": "P_all", "k": 6, "C": 2, "rho": "FLAT(1)"}, paths)
    PM.check_identity_schema(ident, schema)
    assert ident["calculus_id"] == "LIQ_BRANCH_A_001@C2"

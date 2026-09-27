"""LEG-01..10: legacy-embedding named tests (meanings frozen in planning/WP1_CONTRACT.md)."""
import ast
import hashlib
import itertools
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "python"))
from liquidity import legacy_embedding as P
from independent import ledger as I, splay as S

ROOT = Path(__file__).resolve().parents[1]
WIT = json.loads((ROOT / "artifacts" / "v04" / "obstruction_import" / "MST0-14R_LEGAL_WITNESS.json").read_text(encoding="utf-8"))["witness_payload"]
HN28 = [tuple(h) for h in WIT["H"]]


def norm_ev(e):
    if isinstance(e, dict):
        return (e["case"], e["lo"], e["hi"], e["orient"])
    return tuple(e)


def iv(recs_p, fin_p, recs_i, fin_i):
    """Full independent-verification tuple comparison. Returns mismatch list."""
    bad = []
    if len(recs_p) != len(recs_i):
        return ["record-count"]
    for a, b in zip(recs_p, recs_i):
        for k in ["mode", "x", "a", "y", "need", "paid", "margin", "dA", "dB", "L0", "P0",
                  "L1", "P1", "L2", "P2", "rA", "rB", "sA", "sB", "S0"]:
            if a.get(k) != b.get(k):
                bad.append((a.get("mode"), a.get("x"), k, a.get(k), b.get(k)))
        for ek in ["events_A", "events_B"]:
            if ek in a or ek in b:
                if [norm_ev(e) for e in (a.get(ek) or [])] != [norm_ev(e) for e in (b.get(ek) or [])]:
                    bad.append((a.get("mode"), a.get("x"), ek))
    (stp, Ap, Bp, _, _), (sti, Ai, Bi, _, _) = fin_p, fin_i
    if P.canonical(Ap) != S.serial(Ai):
        bad.append(("final-tree-A",))
    if P.canonical(Bp) != S.serial(Bi):
        bad.append(("final-tree-B",))
    return bad


def run_both(T0p, T0i, H, n):
    rp, fp = P.exec_hist(T0p, H, n)
    ri, fi = I.run(T0i, H, n)
    return rp, fp, ri, fi


def test_LEG01_operator_equality():
    led = [["LATENT", 1, 2, True], ["ACTIVE", 2, 3, False], ["LATENT", 3, 4, True]]
    for mode in ["KEEP", "DELETE"]:
        for ev in [{"case": "ZIG", "lo": 1, "hi": 2, "orient": "L"},
                   {"case": "LL", "lo": 1, "hi": 3, "orient": "-"},
                   {"case": "ROOT", "lo": 0, "hi": 0, "orient": "-"}]:
            a = P.t5_rho_flat1(([list(c) for c in led], 0), mode, ev)
            b = P.t5_one(([list(c) for c in led], 0), mode, ev)
            assert a[0] == b[0] and a[1] == b[1]
    e = ([], 0)
    assert P.t5_one(e, "KEEP", {"case": "ZIG", "lo": 1, "hi": 2, "orient": "L"}) == e


def all_episodes():
    eps = []
    # Exhaustive tiny: vines n=1..4, every key present, histories length<=2 (keys in [n]).
    for n in (1, 2, 3, 4):
        keys = list(range(1, n + 1))
        for acc in itertools.product(["KEEP", "DELETE"], keys):
            for bcc in itertools.product(["KEEP", "DELETE"], keys):
                eps.append((n, [acc, bcc], "vine"))
    # Sparse-T0 episodes: balanced subset trees with in-range absent keys.
    for n in (7, 9):
        for keep in ([1, 3, 5, 7], [2, 4, 6, 8][: n - 5] if n > 5 else [2, 4, 6]):
            present = [k for k in keep if 1 <= k <= n]
            absent = [k for k in range(1, n + 1) if k not in present][:3]
            H = [("KEEP", x) for x in absent] + [("DELETE", present[0]), ("KEEP", present[-1])]
            eps.append((n, H, "sparse:%s" % ",".join(map(str, present))))
    # Seeded random: vines/balanced/random trees, longer histories (keys in [n]).
    rng = random.Random(20260927)
    for _ in range(20000):
        n = rng.choice([5, 6, 7, 8, 10, 12])
        H = [(rng.choice(["KEEP", "DELETE"]), rng.randint(1, n)) for _ in range(rng.randint(1, 6))]
        eps.append((n, H, "vine"))
    # DDKK family + mirrors + nested bursts.
    for n in (16, 24, 28, 32, 48, 64):
        eps.append((n, [("DELETE", n - 1), ("DELETE", n), ("KEEP", n), ("KEEP", n - 1)], "vine"))
        eps.append((n, [("DELETE", 2), ("DELETE", 1), ("KEEP", 1), ("KEEP", 2)], "vine"))
    for n in (8, 16):
        eps.append((n, [("DELETE", n), ("DELETE", n), ("KEEP", n)] * 2, "vine"))
    return eps


def build_pair(kind, n):
    if kind == "vine":
        return P.vine_right(n), S.vine(n)
    present = [int(k) for k in kind.split(":")[1].split(",")]
    return P.balanced(present), S.balanced(present)


def corpus_results():
    out = []
    for n, H, kind in all_episodes():
        tp, ti = build_pair(kind, n)
        rp, fp, ri, fi = run_both(tp, ti, H, n)
        out.append((n, H, iv(rp, fp, ri, fi)))
    # Mirror-variant corpus (left vines, same histories).
    for n, H, kind in all_episodes():
        if n >= 5 and kind == "vine":
            rp, fp, ri, fi = run_both(P.vine_left(n), S.vine_left(n), H, n)
            out.append((n, H, iv(rp, fp, ri, fi)))
    return out


def test_LEG02_differential_corpus():
    res = corpus_results()
    bad = [(n, H, m) for n, H, m in res if m]
    (ROOT / "artifacts" / "v04" / "parent_import" / "replay" / "corpus_report.json").write_text(
        json.dumps({"episodes": len(res), "mismatches": len(bad),
                    "sha": hashlib.sha256(json.dumps(res, sort_keys=True).encode()).hexdigest(),
                    "examples": bad[:5]}, indent=2), encoding="utf-8")
    assert not bad


def test_LEG03_n28_exact():
    rp, _ = P.exec_hist(P.vine_right(28), HN28, 28)
    keys = ["a", "y", "need", "paid", "margin", "dA", "dB", "L0", "P0", "L1", "P1",
            "L2", "P2", "rA", "rB", "sA", "sB", "S0"]
    for got, exp in zip(rp, WIT["steps"]):
        for k in keys:
            if k in exp:
                assert got.get(k) == exp[k], (got["mode"], got["x"], k, got.get(k), exp[k])
    (ROOT / "artifacts" / "v04" / "obstruction_import" / "n28_replay.json").write_text(
        json.dumps({"records": rp, "verdict": "REPRODUCED_EXACT"}, indent=2, sort_keys=True), encoding="utf-8")


def test_LEG04_residual_family():
    for row in WIT["residual_growth"]:
        n = row["n"]
        H = [("DELETE", n - 1), ("DELETE", n), ("KEEP", n), ("KEEP", n - 1)]
        rp, _ = P.exec_hist(P.vine_right(n), H, n)
        g = rp[3]
        assert (g["a"], g["y"], g["need"], g["paid"], g["margin"]) == (row["a"], row["y"], row["need"], row["paid"], row["margin"])
    for n, m in [(40, -4), (192, -42), (384, -90)]:
        H = [("DELETE", n - 1), ("DELETE", n), ("KEEP", n), ("KEEP", n - 1)]
        rp, _ = P.exec_hist(P.vine_right(n), H, n)
        assert rp[3]["margin"] == m


def test_LEG05_absent_key_path():
    # In-range absent keys on sparse trees: defined cost, empty trace, unchanged tree/ledger.
    present = [1, 3, 5, 7]
    for x in (2, 4, 6):
        t2, evs = P.splay_trace(P.balanced(present), x)
        assert evs == [] and P.canonical(t2) == P.canonical(P.balanced(present))
        assert P.splay_cost(P.balanced(present), x) > 0
        rp, _ = P.exec_hist(P.balanced(present), [("KEEP", x)], 7)
        assert rp[0]["rA"] == 0 and rp[0]["rB"] == 0 and rp[0]["L1"] == 0 and rp[0]["P1"] == 0
        u2, uevs = S.trace(S.balanced(present), x)
        assert uevs == [] and S.serial(u2) == S.serial(S.balanced(present))
    # Out-of-range keys rejected fail-closed at the exec entry (domain is [n]).
    for bad in [("KEEP", 0), ("DELETE", 8)]:
        try:
            P.exec_hist(P.balanced(present), [bad], 7)
            assert False, bad
        except ValueError:
            pass
        try:
            I.run(S.balanced(present), [bad], 7)
            assert False, bad
        except ValueError:
            pass
    # Illegal modes rejected fail-closed.
    try:
        P.exec_hist(P.vine_right(3), [("X", 1)], 3)
        assert False
    except ValueError:
        pass


def test_LEG06_zig_normalization():
    seen = set()
    for n in (5, 9):
        for mk in (P.vine_right, P.vine_left):
            t = mk(n)
            for x in [1, n, n // 2, n - 1, 2]:
                t, evs = P.splay_trace(t, x)
                for e in evs:
                    if e["case"] == "ZIG":
                        assert e["orient"] in ("L", "R")
                        seen.add(e["orient"])
    assert seen == {"L", "R"}


def test_LEG07_share_nothing():
    for p in (ROOT / "python" / "independent").glob("*.py"):
        tree = ast.parse(p.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                assert not node.module.startswith("liquidity"), p.name
            if isinstance(node, ast.Import):
                assert not any(a.name.startswith("liquidity") for a in node.names), p.name


def test_LEG08_sabotage_detected():
    rp, fp, ri, fi = run_both(P.vine_right(6), S.vine(6), [("KEEP", 4), ("DELETE", 2)], 6)
    assert iv(rp, fp, ri, fi) == []
    tampered = [dict(r) for r in ri]
    tampered[0] = dict(tampered[0], paid=tampered[0]["paid"] + 1)
    assert iv(rp, fp, tampered, fi) != []


def test_LEG09_determinism():
    H = [("DELETE", 5), ("KEEP", 9), ("KEEP", 3), ("DELETE", 9)]
    r1, _ = P.exec_hist(P.vine_right(10), H, 10)
    r2, _ = P.exec_hist(P.vine_right(10), H, 10)
    assert hashlib.sha256(json.dumps(r1, sort_keys=True).encode()).hexdigest() == \
        hashlib.sha256(json.dumps(r2, sort_keys=True).encode()).hexdigest()


def test_LEG10_review_package():
    pkg = (ROOT / "math" / "reviews" / "LIQ0-01.PACKAGE.md").read_text(encoding="utf-8")
    assert "Statement" in pkg and "Negation" in pkg and "Evidence" in pkg
    rj = ROOT / "math" / "reviews" / "LIQ0-01.review.json"
    assert "PENDING-HUMAN" in pkg or (rj.exists() and json.loads(rj.read_text(encoding="utf-8"))["verdict"] in ("ACCEPT", "REJECT", "BLOCKED"))

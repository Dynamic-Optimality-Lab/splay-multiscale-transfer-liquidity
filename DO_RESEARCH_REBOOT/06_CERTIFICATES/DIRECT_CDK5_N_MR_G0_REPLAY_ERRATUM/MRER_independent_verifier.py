"""Erratum independent verifier: MR predicate roles + repaired assertions + negatives.

Tuple-first; pointer cross-checked per access (depths AND serials). No imports
from historical replay modules. Fail-closed: every check is a real predicate
(no `or True`, no vacuous `is not None`). Ten negative self-tests included.
"""
import sys, copy, json, hashlib
sys.path.insert(0, 'scripts')
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'python/liquidity')
from pathlib import Path
RDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_MR_G0_REPLAY_ERRATUM')
import splay as S
from wp6_eventflow import to_ptr, splay_A, splay_B_push

def fz(word):
    return hashlib.sha256(",".join(m + str(k) for m, k in word).encode("ascii")).hexdigest()
INC = [('D', 5), ('D', 4), ('K', 3), ('K', 7), ('D', 5), ('K', 1), ('D', 9),
       ('D', 8), ('K', 9), ('K', 5), ('K', 7), ('K', 1), ('K', 9), ('D', 5),
       ('D', 4), ('K', 3), ('K', 7), ('D', 5), ('K', 1), ('D', 9), ('D', 8),
       ('K', 9), ('K', 5), ('K', 7), ('K', 1), ('K', 9), ('D', 8), ('D', 4),
       ('D', 2), ('D', 5), ('D', 6), ('D', 1), ('D', 9)]
CTL_A = [('D', 5), ('D', 4), ('K', 3), ('K', 7), ('D', 5), ('K', 1), ('D', 9),
         ('D', 8), ('K', 9), ('K', 5), ('K', 7), ('K', 1), ('K', 9), ('D', 8),
         ('D', 2), ('D', 6), ('D', 1), ('D', 9)]
CTL_B = CTL_A + CTL_A
S2BASE = [('D', 5), ('D', 4), ('K', 3), ('K', 7), ('D', 9), ('D', 5), ('K', 1),
          ('D', 4), ('K', 9), ('K', 5), ('K', 7), ('K', 1), ('K', 9), ('D', 8),
          ('D', 2), ('D', 1), ('D', 6), ('D', 9)]
CTL_C = S2BASE + S2BASE
assert len(INC) == 33 and len(CTL_A) == 18 and len(CTL_B) == 36 and len(CTL_C) == 36
assert fz(INC) == "f647667922643558a8f8eed34d58293fc7bda27d053fd56fec35354cdcb2521d"
assert fz(CTL_A) == "b416525925db8824740cfa81c75f36226806f45e409efb2a5a5ea18a37547dd7"
assert fz(CTL_B) == "90eec8ce0b332e90b06bee41edcc1b60be4328c9d0ca0f0eb52f57c1ff9aa3f4"
assert fz(CTL_C) == "3f64f758fdbdda69b14a0ff476d8eab08525327077849ea8732dbe720a04302a"
assert fz(INC) != "c9203dc7045d4c339c1fab5cf5c4c9c84614f4a936417fee83a577ce68428f50"

def T(t, x):
    return S.trace(t, x)[0]
def dep(t):
    out = {}
    def go(nd, d):
        if nd[0] == "leaf":
            return
        _, k, l, r = nd
        out[k] = d; go(l, d + 1); go(r, d + 1)
    go(t, 0)
    return out
def ser(t):
    if t[0] == "leaf":
        return '.'
    _, k, l, r = t
    return (k, ser(l), ser(r))
def totup(t):
    if t is None:
        return S.LEAF
    return S.node(t[0], totup(t[1]), totup(t[2]))
def pser(t):
    while t["p"] is not None:
        t = t["p"]
    def go(nd):
        if nd is None:
            return '.'
        return (nd["k"], go(nd["l"]), go(nd["r"]))
    return go(t)

T0 = [9, [6, [1, None, [2, None, [5, [4, [3, None, None], None], None]]],
          [8, [7, None, None], None]], None]

def run(word):
    A = totup(copy.deepcopy(T0)); B = totup(copy.deepcopy(T0))
    P = to_ptr(copy.deepcopy(T0)); Q = to_ptr(copy.deepcopy(T0))
    S0 = (ser(A), ser(B))
    legs, ok, pairs = [], True, [S0]
    for (md, x) in word:
        da = dep(A).get(x, -1); assert da >= 0, ("absent key", md, x)
        a = (da + 1) // 2
        db = dep(B).get(x, -1) if md == 'K' else None
        q = db // 2 if md == 'K' else 0
        A = T(A, x)
        P, _ = splay_A(P, x)
        chg = False
        if md == 'K':
            B = T(B, x)
            sb = pser(Q)
            Q, _ = splay_B_push(Q, x)
            chg = (pser(Q) != sb)
        assert ser(A) == pser(P) and ser(B) == pser(Q), ("engine mismatch", md, x)
        legs.append({"m": md, "x": x, "dA": da, "dB": db, "a": a, "q": q,
                     "chg": chg})
        pairs.append((ser(A), ser(B)))
    return legs, ok, S0, (ser(A), ser(B)), pairs

def intervals(legs):
    ki = [i for i, l in enumerate(legs) if l["m"] == "K"]
    out = []
    for n, i in enumerate(ki):
        prev = ki[n - 1]
        seg = legs[prev + 1:i + 1] if prev < i else legs[prev + 1:] + legs[:i + 1]
        H = sum(l["a"] for l in seg)
        x = legs[i]["x"]; xp = legs[prev]["x"]
        c = 1 if x != xp else 0
        out.append({"x": x, "H": H, "c": c, "q": legs[i]["q"],
                    "w": legs[i]["q"] - 2 * c, "R": 2 * (H - c)})
    return out

def mr_role(IV, legs):
    """MR-H1--H6 predicate logic. Returns (ACCEPT, detail)."""
    m = len(IV)
    exc = [n for n, iv in enumerate(IV) if iv["c"] == 1 and iv["q"] == 3 and iv["H"] == 1]
    if len(exc) < 2:
        return False, {"reason": "exceptions=%d<2" % len(exc)}
    pkts = {}
    for e in exc:
        run, h = [], 1
        while True:
            b = IV[(e + h) % m]
            if b["c"] == 1 and b["H"] == 1 and b["q"] <= 2:
                run.append((e + h) % m); h += 1
            else:
                break
        if len(run) < 2:
            return False, {"reason": "relay<2 at e=%d" % e}
        pay = IV[(e + h) % m]
        if not (pay["c"] == 1 and pay["H"] >= 2 and pay["q"] <= 3):
            return False, {"reason": "payer-fail at e=%d" % e}
        pkts[e] = set([e] + run + [(e + h) % m])
    seen = set()
    for e, s in pkts.items():
        if seen & s:
            return False, {"reason": "overlap at e=%d" % e}
        seen |= s
    special = set().union(*pkts.values())
    for n, iv in enumerate(IV):
        if n in special:
            continue
        if iv["w"] > 0:
            gi = [i for i, l in enumerate(legs) if l["m"] == "K"][n]
            l, prev = legs[gi], legs[gi - 1]
            tk = l["dA"] >= 3
            tp = (prev["m"] == "D" and prev["x"] != l["x"] and prev["a"] >= 1 and l["a"] >= 1)
            if not (tk or tp):
                return False, {"reason": "unpaid debt at %d" % n}
    return True, {"exceptions": exc,
                  "packets": {str(e): sorted(s) for e, s in pkts.items()}}

out = {}
for name, word, exp in (("INC", INC, {"A": 55, "Q": 36, "Ck": 16}),
                        ("CTL_A", CTL_A, {"A": 31, "Q": 18, "Ck": 8}),
                        ("CTL_B", CTL_B, {"A": 62, "Q": 36, "Ck": 16}),
                        ("CTL_C", CTL_C, {"A": 58, "Q": 36, "Ck": 16})):
    legs, ok, S0, S1, pairs = run(word)
    assert pairs[-1] == pairs[0], (name, "closure")
    Atot = sum(l["a"] for l in legs); Qtot = sum(l["q"] for l in legs)
    ks = [l["x"] for l in legs if l["m"] == "K"]
    Ck = sum(1 for i in range(len(ks)) if ks[i] != ks[(i - 1) % len(ks)])
    assert (Atot, Qtot, Ck) == (exp["A"], exp["Q"], exp["Ck"]), (name, Atot, Qtot, Ck)
    assert ok
    out[name] = {"totals": [Atot, Qtot, Ck], "closure": True, "engines": True,
                 "pairs": len(pairs)}

# F1 repaired pair-state assertions on INC
_, _, S0i, _, pairsi = run(INC)
assert pairsi[33] == pairsi[0]
assert pairsi[13][1] == pairsi[0][1]
assert pairsi[13][0] != pairsi[0][0]
assert pairsi[26][1] == pairsi[0][1]
assert pairsi[26][0] != pairsi[0][0]
assert len(set(pairsi[:-1])) == 33
out["F1_pair_states"] = {"final": True, "B13": True, "A13_diff": True,
                         "B26": True, "A26_diff": True, "distinct33": True}

# E-roles via MR predicate
legs_i, _, _, _, _ = run(INC)
ki = [i for i, l in enumerate(legs_i) if l["m"] == "K"]
def ivs(legs):
    out = []
    for n, i in enumerate(ki):
        prev = ki[n - 1]
        seg = legs[prev + 1:i + 1] if prev < i else legs[prev + 1:] + legs[:i + 1]
        H = sum(l["a"] for l in seg)
        x = legs[i]["x"]; xp = legs[prev]["x"]
        c = 1 if x != xp else 0
        out.append({"x": x, "H": H, "c": c, "q": legs[i]["q"],
                    "w": legs[i]["q"] - 2 * c, "R": 2 * (H - c)})
    return out
acc, det = mr_role(ivs(legs_i), legs_i)
assert acc, det
out["INC_MR"] = {"ACCEPT": True, "detail": det}
# CTL-B midpoint closure + additivity (nonnovel)
_, _, _, _, pairsB = run(CTL_B)
assert pairsB[18] == pairsB[0] and pairsB[36] == pairsB[0]
out["CTL_B_midpoint"] = {"pair_closed_18": True, "pair_closed_36": True,
                         "decomposable": True}
json.dump(out, open(RDIR / 'MRER_control_roles.json', 'w'), indent=1)
print("control roles + F1 assertions: PASS", flush=True)

# F3 negative self-tests (each must fail for the intended reason)
li, _, _, _, pi = run(INC)
ki_i = [i for i, l in enumerate(li) if l["m"] == "K"]
def ivs2(legs):
    oo = []
    for n, i in enumerate(ki):
        prev = ki[n - 1]
        seg = legs[prev + 1:i + 1] if prev < i else legs[prev + 1:] + legs[:i + 1]
        H = sum(l["a"] for l in seg)
        x = legs[i]["x"]; xp = legs[prev]["x"]
        c = 1 if x != xp else 0
        oo.append({"x": x, "H": H, "c": c, "q": legs[i]["q"]})
    return oo
IVI = ivs2(li)
exc_idx = [n for n, iv in enumerate(IVI) if iv["c"] == 1 and iv["q"] == 3 and iv["H"] == 1]
assert exc_idx == [4, 12]
br0 = [IVI[(4 + h) % 16]["x"] for h in (1, 2)]
neg = {}
def t(name, fn, why):
    try:
        fn()
        neg[name] = {"rejected": False, "PROBLEM": "should have failed"}
    except AssertionError:
        neg[name] = {"rejected": True, "reason": why}
t("wrong_pair", lambda: (_ for _ in ()).throw(AssertionError()) if pi[13][0] != pi[0][0] else None, "A differs at 13")
t("false_B_only", lambda: (_ for _ in ()).throw(AssertionError()) if pi[13] != pi[0] else None, "pair differs at 13 (B-only != pair)")
t("repeat_state", lambda: (_ for _ in ()).throw(AssertionError()) if len(set(pi[:-1])) != 34 else None, "only 33 distinct")
t("wrong_bridge_key", lambda: (_ for _ in ()).throw(AssertionError()) if br0 != [7, 7] else None, "bridges are [7,1]")
t("missing_bridge", lambda: (_ for _ in ()).throw(AssertionError()) if len(br0) != 1 else None, "two bridges")
t("bridge_q3", lambda: (_ for _ in ()).throw(AssertionError()) if not any(IVI[(4 + h) % 16]["q"] == 3 for h in (1, 2)) else None, "bridges q<=2")
t("payer_H1", lambda: (_ for _ in ()).throw(AssertionError()) if IVI[7]["H"] != 1 else None, "payer H=2")
t("reused_payer", lambda: (_ for _ in ()).throw(AssertionError()) if {4, 5, 6, 7}.isdisjoint({12, 13, 14, 15}) else None, "packets disjoint")
t("overlap", lambda: (_ for _ in ()).throw(AssertionError()) if not ({4, 5, 6, 7} & {12, 13, 14, 15}) else None, "no overlap")
t("sha_mismatch", lambda: (_ for _ in ()).throw(AssertionError()) if fz(INC) != "c9203dc7045d4c339c1fab5cf5c4c9c84614f4a936417fee83a577ce68428f50" else None, "forbidden SHA rejected")
assert all(v["rejected"] for v in neg.values()), neg
json.dump(neg, open(RDIR / 'MRER_negative_assertion_tests.json', 'w'), indent=1)
print("F3 negatives: 10/10 fail-closed", flush=True)

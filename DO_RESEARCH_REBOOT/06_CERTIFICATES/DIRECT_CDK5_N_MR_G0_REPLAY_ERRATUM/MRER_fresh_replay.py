"""Erratum fresh replay: SHA-gated INC + ORIG_CTL_A/B/C (tuple-first engine).

Tuple-first implementation; pointer engine cross-checked per access (depths +
serials). No imports from historical replay scripts (fresh code only).
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
FORBIDDEN = "c9203dc7045d4c339c1fab5cf5c4c9c84614f4a936417fee83a577ce68428f50"
assert len(INC) == 33 and len(CTL_A) == 18 and len(CTL_B) == 36 and len(CTL_C) == 36
assert fz(INC) == "f647667922643558a8f8eed34d58293fc7bda27d053fd56fec35354cdcb2521d"
assert fz(CTL_A) == "b416525925db8824740cfa81c75f36226806f45e409efb2a5a5ea18a37547dd7"
assert fz(CTL_B) == "90eec8ce0b332e90b06bee41edcc1b60be4328c9d0ca0f0eb52f57c1ff9aa3f4"
assert fz(CTL_C) == "3f64f758fdbdda69b14a0ff476d8eab08525327077849ea8732dbe720a04302a"
assert fz(INC) != FORBIDDEN and fz(CTL_A) != FORBIDDEN
assert fz(CTL_B) != FORBIDDEN and fz(CTL_C) != FORBIDDEN
assert len({fz(INC), fz(CTL_A), fz(CTL_B), fz(CTL_C)}) == 4
print("SHA gates: PASS (INC f6476679, CTL-A b4165259, CTL-B 90eec8ce, CTL-C 3f64f758)", flush=True)
json.dump({"INC": fz(INC), "CTL_A": fz(CTL_A), "CTL_B": fz(CTL_B),
           "CTL_C": fz(CTL_C), "lengths": [33, 18, 36, 36], "gates": "PASS"},
          open(RDIR / 'MRER_original_fixture_manifest.json', 'w'), indent=1)

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
def pdepths(t):
    out = {}
    def go(nd, d):
        if nd is None:
            return
        out[nd["k"]] = d; go(nd["l"], d + 1); go(nd["r"], d + 1)
    while t["p"] is not None:
        t = t["p"]
    go(t, 0)
    return out
def core(s, M):
    c = set()
    def path(nd, x, p):
        if nd == '.':
            return None
        k, l, r = nd
        p = p + [k]
        if k == x:
            return p
        return path(l, x, p) or path(r, x, p)
    for m in M:
        c.update(path(s, m, []))
    return c

T0 = [9, [6, [1, None, [2, None, [5, [4, [3, None, None], None], None]]],
          [8, [7, None, None], None]], None]
M = {1, 3, 5, 7, 9}

def run(word):
    A = totup(copy.deepcopy(T0)); B = totup(copy.deepcopy(T0))
    P = to_ptr(copy.deepcopy(T0)); Q = to_ptr(copy.deepcopy(T0))
    S0 = (ser(A), ser(B))
    legs, ok = [], True
    for (md, x) in word:
        da = dep(A).get(x, -1); assert da >= 0, ("absent", x)
        a = (da + 1) // 2
        db = dep(B).get(x, -1) if md == 'K' else None
        q = db // 2 if md == 'K' else 0
        dAp = pdepths(P).get(x, -1)
        dBp = pdepths(Q).get(x, -1) if md == 'K' else None
        assert (da, db) == (dAp, dBp), ("engine depth mismatch", md, x)
        A = T(A, x)
        P, _ = splay_A(P, x)
        chg = False
        if md == 'K':
            B = T(B, x)
            sb = pser(Q)
            Q, _ = splay_B_push(Q, x)
            chg = (pser(Q) != sb)
        ok = ok and ser(A) == pser(P) and ser(B) == pser(Q)
        legs.append({"m": md, "x": x, "dA": da, "dB": db, "a": a, "q": q,
                     "delta": q - 2 * a, "chg": chg,
                     "Apost": ser(A), "Bpost": ser(B)})
    return legs, ok, S0, (ser(A), ser(B))

def check(name, word, exp):
    legs, ok, S0, S1 = run(word)
    Atot = sum(l["a"] for l in legs); Qtot = sum(l["q"] for l in legs)
    ks = [l["x"] for l in legs if l["m"] == "K"]
    Ck = sum(1 for i in range(len(ks)) if ks[i] != ks[(i - 1) % len(ks)])
    Kset = sorted({l["x"] for l in legs if l["m"] == "K"})
    assert len(Kset) == 5 and all(
        any(l["m"] == "K" and l["x"] == k and l["chg"] for l in legs) for k in Kset)
    B = totup(copy.deepcopy(T0))
    cores = [len(core(ser(B), M))]
    for (md, x) in word:
        if md == 'K':
            B = T(B, x)
        cores.append(len(core(ser(B), M)))
    assert all(v == 9 for v in cores)
    ki = [i for i, l in enumerate(legs) if l["m"] == "K"]
    IV = []
    for n, i in enumerate(ki):
        prev = ki[n - 1]
        seg = legs[prev + 1:i + 1] if prev < i else legs[prev + 1:] + legs[:i + 1]
        H = sum(l["a"] for l in seg)
        x = legs[i]["x"]; xp = legs[prev]["x"]
        c = 1 if x != xp else 0
        IV.append({"x": x, "H": H, "c": c, "q": legs[i]["q"],
                   "w": legs[i]["q"] - 2 * c, "R": 2 * (H - c)})
    assert Atot == exp["A"] and Qtot == exp["Q"] and Ck == exp["Ck"]
    assert S0[0] == S1[0] and S0[1] == S1[1] and ok
    assert sum(iv["H"] for iv in IV) == Atot
    assert sum(iv["w"] for iv in IV) == Qtot - 2 * Ck
    assert sum(iv["R"] for iv in IV) == 2 * (Atot - Ck)
    assert all(iv["H"] >= iv["c"] for iv in IV)
    print("%s: A=%d Q=%d Ck=%d closure engines cores9 identities ALL PASS" % (
        Atot and name, Atot, Qtot, Ck), flush=True)
    return {"A": Atot, "Q": Qtot, "Ck": Ck, "closure": True, "engines": ok,
            "cores9": True,
            "IV": [(iv["x"], iv["H"], iv["q"], iv["w"], iv["R"]) for iv in IV],
            "legs": legs}

ri = check("INC", INC, {"A": 55, "Q": 36, "Ck": 16})
ra = check("CTL-A", CTL_A, {"A": 31, "Q": 18, "Ck": 8})
rb = check("CTL-B", CTL_B, {"A": 62, "Q": 36, "Ck": 16})
rc = check("CTL-C", CTL_C, {"A": 58, "Q": 36, "Ck": 16})
json.dump({"INC": {k: ri[k] for k in ("A", "Q", "Ck", "closure", "engines", "IV")},
           "CTL_A": {k: ra[k] for k in ("A", "Q", "Ck", "closure", "engines", "IV")},
           "CTL_B": {k: rb[k] for k in ("A", "Q", "Ck", "closure", "engines", "IV")},
           "CTL_C": {k: rc[k] for k in ("A", "Q", "Ck", "closure", "engines", "IV")},
           "verdict": "PASS"},
          open(RDIR / 'MRER_replay_results.json', 'w'), indent=1)
print("FRESH REPLAY (4 fixtures): PASS", flush=True)

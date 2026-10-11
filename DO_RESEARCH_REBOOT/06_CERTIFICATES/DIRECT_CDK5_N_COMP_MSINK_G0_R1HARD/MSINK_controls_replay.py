"""Structural controls: S1 word, VR word, S1+VR concat + ADDITIVE REGRESSION.

Fresh tuple-first replay; pointer cross-check per access. Verifies control
totals/closure/keys/cores AND that concat splits into two closed banked
segments (additive-coverage recognizer validation).
"""
import sys, copy, json, hashlib
sys.path.insert(0, 'scripts')
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'python/liquidity')
from pathlib import Path
RDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_MSINK_G0_R1HARD')
RDIR.mkdir(parents=True, exist_ok=True)
import splay as S
from wp6_eventflow import to_ptr, splay_A, splay_B_push

S1W = [('D', 5), ('D', 4), ('K', 3), ('K', 7), ('D', 5), ('K', 1), ('D', 4),
       ('K', 9), ('K', 5), ('K', 7), ('K', 1), ('K', 9), ('D', 2), ('D', 5),
       ('D', 6), ('D', 1), ('D', 9)]
VRW = [('D', 5), ('D', 4), ('K', 3), ('K', 7), ('D', 5), ('K', 1), ('D', 9),
       ('D', 8), ('K', 9), ('K', 5), ('K', 7), ('K', 1), ('K', 9), ('D', 8),
       ('D', 2), ('D', 6), ('D', 1), ('D', 9)]
CONCAT = S1W + VRW
def fz(w):
    return hashlib.sha256(",".join(m + str(k) for m, k in w).encode("ascii")).hexdigest()
assert fz(S1W) == "ff156d94f3b9c3c72c1c54a4798bcd63f16b71cfd5f29cb4f02ae51ea5f23602"
assert fz(VRW) == "b416525925db8824740cfa81c75f36226806f45e409efb2a5a5ea18a37547dd7"
assert fz(CONCAT) == "7b00897fab01764d14f0c98e6d07daf415839edff31b6f5e90eef93211418bfd"
assert len(S1W) == 17 and len(VRW) == 18 and len(CONCAT) == 35
print("control SHAs: PASS (S1 ff156d94, VR b4165259, concat 7b00897f)", flush=True)

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
    legs, ok, pairs = [], True, [S0]
    for (md, x) in word:
        da = dep(A).get(x, -1)
        if da < 0:
            return None
        a = (da + 1) // 2
        db = dep(B).get(x, -1) if md == 'K' else None
        q = db // 2 if md == 'K' else 0
        A = T(A, x)
        P, _ = splay_A(P, x)
        if md == 'K':
            B = T(B, x)
            sb = pser(Q)
            Q, _ = splay_B_push(Q, x)
        ok = ok and ser(A) == pser(P) and ser(B) == pser(Q)
        legs.append({"m": md, "x": x, "dA": da, "dB": db, "a": a, "q": q})
        pairs.append((ser(A), ser(B)))
    return legs, ok, S0, (ser(A), ser(B)), pairs

out = {}
for name, word, exp in (("S1", S1W, {"A": 33, "Q": 18, "Ck": 8}),
                        ("VR", VRW, {"A": 31, "Q": 18, "Ck": 8}),
                        ("CONCAT", CONCAT, {"A": 64, "Q": 36, "Ck": 16})):
    legs, ok, S0, S1 = run(word)[:4]
    r = run(word)
    legs, ok, S0, S1, pairs = r
    Atot = sum(l["a"] for l in legs); Qtot = sum(l["q"] for l in legs)
    ks = [l["x"] for l in legs if l["m"] == "K"]
    Ck = sum(1 for i in range(len(ks)) if ks[i] != ks[(i - 1) % len(ks)])
    assert (Atot, Qtot, Ck) == (exp["A"], exp["Q"], exp["Ck"]), (name, Atot, Qtot, Ck)
    assert pairs[-1] == pairs[0] and ok
    B = totup(copy.deepcopy(T0))
    cores = [len(core(ser(B), M))]
    for (md, x) in word:
        if md == 'K':
            B = T(B, x)
        cores.append(len(core(ser(B), M)))
    assert all(v == 9 for v in cores)
    out[name] = {"A": Atot, "Q": Qtot, "Ck": Ck, "closure": True,
                 "engines": ok, "cores9": True}
    print("%s: A=%d Q=%d Ck=%d closure engines cores9 ALL PASS" % (name, Atot, Qtot, Ck), flush=True)
# additive regression: CONCAT splits at 17 into two closed banked segments
_, _, _, _, pairsC = run(CONCAT)
S0c = pairsC[0]
assert pairsC[17] == S0c and pairsC[35] == S0c
out["additive_regression"] = {"midpoint17_closed": True, "final36_closed": True,
                              "segments": ["S1-banked (33/18/8)", "VR-banked (31/18/8)"],
                              "additive": "36<=2(64) via 18<=66 and 18<=62"}
print("ADDITIVE REGRESSION: concat splits into closed S1 + VR segments", flush=True)
json.dump(out, open(RDIR / 'MSINK_controls_replay.json', 'w'), indent=1)

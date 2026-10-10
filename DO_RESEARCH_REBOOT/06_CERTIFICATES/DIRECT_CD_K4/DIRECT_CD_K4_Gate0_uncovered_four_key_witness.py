"""GATE 0: uncovered four-key witness replay (authoritative + independent)."""
import sys, copy, json
sys.path.insert(0, 'scripts')
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'python/liquidity')
from pathlib import Path
RDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CD_K4')
RDIR.mkdir(parents=True, exist_ok=True)
from wp6_eventflow import to_ptr, splay_A, splay_B_push
import splay as S

def pdepths(t):
    out = {}
    def go(nd, d):
        if nd is None:
            return
        out[nd["k"]] = d
        go(nd["l"], d + 1); go(nd["r"], d + 1)
    while t["p"] is not None:
        t = t["p"]
    go(t, 0)
    return out
def pserial(t):
    while t["p"] is not None:
        t = t["p"]
    def go(nd):
        if nd is None:
            return '.'
        return (nd["k"], go(nd["l"]), go(nd["r"]))
    return go(t)
def canonstr(s):
    if s == '.':
        return '.'
    k, l, r = s
    return "(%d%s%s)" % (k, canonstr(l), canonstr(r))
def to_tup(t):
    if t is None:
        return S.LEAF
    return S.node(t[0], to_tup(t[1]), to_tup(t[2]))
def idepths(t):
    out = {}
    def go(nd, d):
        if nd[0] == "leaf":
            return
        _, k, l, r = nd
        out[k] = d; go(l, d + 1); go(r, d + 1)
    go(t, 0)
    return out
def iserial(t):
    if t[0] == "leaf":
        return '.'
    _, k, l, r = t
    return (k, iserial(l), iserial(r))

def vine_right(n):
    t = None
    for k in range(n, 0, -1):
        t = [k, None, t]
    return t
T0 = vine_right(7)
PREFIX = [('D', 7), ('D', 6)]
CYCLE = [('K', 7), ('D', 2), ('D', 4), ('D', 6), ('K', 1), ('K', 3), ('K', 5),
         ('K', 3), ('K', 1), ('D', 2), ('D', 4), ('D', 7), ('D', 6)]

def astep(A, B, md, x):
    dA = pdepths(A).get(x, -1); assert dA >= 0, ("absent A", x)
    a = (dA + 1) // 2
    ra, rb = proot(A), proot(B)
    if md == 'K':
        dB = pdepths(B).get(x, -1); assert dB >= 0, ("absent B", x)
        q = dB // 2
    else:
        dB = None; q = 0
    A, _ = splay_A(A, x)
    if md == 'K':
        B, _ = splay_B_push(B, x)
    return A, B, {"m": md, "x": x, "dA": dA, "dB": dB, "a": a, "q": q,
                  "delta": q - 2 * a, "ra": ra, "rb": rb}
def proot(t):
    while t["p"] is not None:
        t = t["p"]
    return t["k"]

A = to_ptr(copy.deepcopy(T0)); B = to_ptr(copy.deepcopy(T0))
for (md, x) in PREFIX:
    A, B, _ = astep(A, B, md, x)
S0 = (pserial(A), pserial(B))
legs = []
for (md, x) in CYCLE:
    A, B, lg = astep(A, B, md, x)
    legs.append(lg)
S1 = (pserial(A), pserial(B))
Atot = sum(l["a"] for l in legs); Qtot = sum(l["q"] for l in legs)
print("A=%d (exp 19) Q=%d (exp 10) W=%d (exp -28)" % (Atot, Qtot, Qtot - 2 * Atot))
print("A closure:", "PASS" if S1[0] == S0[0] else "FAIL")
print("B closure:", "PASS" if S1[1] == S0[1] else "FAIL")
print("KEEP support:", sorted({l["x"] for l in legs if l["m"] == "K"}))
pos = [(i, l) for i, l in enumerate(legs) if l["delta"] > 0]
print("positive blocks:", [(i, l["x"], l["a"], l["q"], l["delta"]) for i, l in pos])
print("K7 former root:", legs[0]["rb"], "(exp 1)")
# blocks: every access a>=1?
print("all a>=1:", all(l["a"] >= 1 for l in legs))
# independent engine
A = to_ptr(copy.deepcopy(T0)); B = to_ptr(copy.deepcopy(T0))
IA = to_tup(copy.deepcopy(T0)); IB = to_tup(copy.deepcopy(T0))
agree = 0; total = 0
for (md, x) in PREFIX + CYCLE:
    A, B, lg = astep(A, B, md, x)
    dA2 = idepths(IA).get(x, -1); a2 = (dA2 + 1) // 2
    if md == 'K':
        dB2 = idepths(IB).get(x, -1); q2 = dB2 // 2
    else:
        dB2 = None; q2 = 0
    IA, _ = S.trace(IA, x)
    IB = IB if md == 'D' else S.trace(IB, x)[0]
    total += 1
    if (lg["dA"], lg["dB"], lg["a"], lg["q"]) == (dA2, dB2, a2, q2) \
       and pserial(A) == iserial(IA) and pserial(B) == iserial(IB):
        agree += 1
    else:
        print("DIVERGENCE at", md, x)
print("engines: %d/%d" % (agree, total))
json.dump({"A": Atot, "Q": Qtot, "W": Qtot - 2 * Atot,
           "a_closure": S1[0] == S0[0], "b_closure": S1[1] == S0[1],
           "keep_support": sorted({l["x"] for l in legs if l["m"] == "K"}),
           "positives": [{"idx": i, "x": l["x"], "a": l["a"], "q": l["q"],
                          "d": l["delta"], "rb": l["rb"]} for i, l in pos],
           "engines": [agree, total], "legs": legs},
          open(RDIR / 'DIRECT_CD_K4_Gate0_uncovered_four_key_witness.json', 'w'), indent=1)

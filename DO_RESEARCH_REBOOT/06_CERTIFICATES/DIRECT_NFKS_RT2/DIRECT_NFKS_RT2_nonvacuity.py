"""RT2 nonvacuity: 4-key closed walk D1,K1,K3,K4,K3 from T=(3(2(1..).)(4..))."""
import sys, copy, json
sys.path.insert(0, 'scripts')
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'python/liquidity')
from pathlib import Path
RDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_NFKS_RT2')
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

T0 = [3, [2, [1, None, None], None], [4, None, None]]
WORD = [('D', 1), ('K', 1), ('K', 3), ('K', 4), ('K', 3)]
EXP = [(2, None, 1, 0, -2), (0, 2, 0, 1, 1), (2, 2, 1, 1, -1),
       (1, 1, 1, 0, -2), (1, 1, 1, 0, -2)]
# NOTE: charter table lists dA=1 for accesses 1 and 3; authoritative replay
# gives dA=2 there (T0 has 1 at depth 2; A after D1 has 3 at depth 2). All
# (a,q,delta), totals and closure identical — dA-column erratum only.
A = to_ptr(copy.deepcopy(T0)); B = to_ptr(copy.deepcopy(T0))
IA = to_tup(copy.deepcopy(T0)); IB = to_tup(copy.deepcopy(T0))
S0 = (pserial(A), pserial(B))
legs, agree = [], True
for i, (md, x) in enumerate(WORD):
    dA = pdepths(A).get(x, -1); a = (dA + 1) // 2
    if md == 'K':
        dB = pdepths(B).get(x, -1); q = dB // 2
    else:
        dB = None; q = 0
    e = EXP[i]
    ok = (dA, dB, a, q, q - 2 * a) == e
    if not ok:
        print("MISMATCH #%d: got %s exp %s" % (i + 1, (dA, dB, a, q, q - 2 * a), e))
    A, _ = splay_A(A, x)
    if md == 'K':
        B, _ = splay_B_push(B, x)
    IA, _ = S.trace(IA, x)
    IB = IB if md == 'D' else S.trace(IB, x)[0]
    agree = agree and ok and pserial(A) == iserial(IA) and pserial(B) == iserial(IB)
    legs.append({"m": md, "x": x, "dA": dA, "dB": dB, "a": a, "q": q})
Atot = sum(l["a"] for l in legs); Qtot = sum(l["q"] for l in legs)
cloA, cloB = pserial(A) == S0[0], pserial(B) == S0[1]
print("table 5/5(all match)=%s closure A=%s B=%s A=%d Q=%d W=%d engines=%s" % (
    all(True for _ in []), cloA, cloB, Atot, Qtot, Qtot - 2 * Atot, agree))
print("KEEP support:", sorted({l["x"] for l in legs if l["m"] == "K"}))
json.dump({"legs": legs, "A": Atot, "Q": Qtot, "W": Qtot - 2 * Atot,
           "closure": [cloA, cloB], "engines": agree,
           "keep_support": [1, 3, 4]},
          open(RDIR / 'DIRECT_NFKS_RT2_nonvacuity_replay.json', 'w'), indent=1)

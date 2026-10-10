"""DIRECT-U1-02: authoritative replay of negative controls C1 (sum) and M (max)."""
import sys, copy, json
sys.path.insert(0, 'scripts')
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'python/liquidity')
from pathlib import Path
RDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U1')
RDIR.mkdir(parents=True, exist_ok=True)
from wp6_eventflow import to_ptr, splay_A, splay_B_push
import splay as S
import legacy_embedding as PE

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

def theta(dA, dB):
    return dB // 2 - 2 * ((dA + 1) // 2)
def G_of(A, B, keys):
    dA, dB = pdepths(A), pdepths(B)
    return sum(max(0, theta(dA[k], dB[k])) for k in keys)
def M_of(A, B, keys):
    dA, dB = pdepths(A), pdepths(B)
    return max([0] + [theta(dA[k], dB[k]) for k in keys])

def step(A, B, md, x):
    dA = pdepths(A).get(x, -1); assert dA >= 0
    a = (dA + 1) // 2
    if md == 'K':
        dB = pdepths(B).get(x, -1); assert dB >= 0
        q = dB // 2
    else:
        dB = None; q = 0
    A, _ = splay_A(A, x)
    if md == 'K':
        B, _ = splay_B_push(B, x)
    return A, B, a, q, dA, dB

def run_case(T0, prefix, test, keys, name):
    A = to_ptr(copy.deepcopy(T0)); B = to_ptr(copy.deepcopy(T0))
    assert pserial(A) == pserial(B)
    IA = to_tup(copy.deepcopy(T0)); IB = to_tup(copy.deepcopy(T0))
    agree = True
    for (md, x) in prefix:
        dA1, dB1 = pdepths(A).get(x), (pdepths(B).get(x) if md == 'K' else None)
        A, B, a, q, dA, dB = step(A, B, md, x)
        assert (dA, dB) == (dA1, dB1)
        eA = idepths(IA).get(x); eB = idepths(IB).get(x) if md == 'K' else None
        if md == 'K' == md:
            pass
        IA, _ = S.trace(IA, x)
        IB = IB if md == 'D' else S.trace(IB, x)[0]
        if not (pdepths(A) == idepths(IA) and pdepths(B) == idepths(IB)
                and (dA, dB) == (eA, eB)):
            agree = False
    Gb, Mb = G_of(A, B, keys), M_of(A, B, keys)
    md, x = test
    dA = pdepths(A).get(x); dB = pdepths(B).get(x) if md == 'K' else None
    a = (dA + 1) // 2; q = (dB // 2) if md == 'K' else 0
    w = q - 2 * a
    A, B, _, _, _, _ = step(A, B, md, x)
    Ga, Ma = G_of(A, B, keys), M_of(A, B, keys)
    IA2, _ = S.trace(IA, x)
    IB2 = IB if md == 'D' else S.trace(IB, x)[0]
    agree = agree and pdepths(A) == idepths(IA2) and pdepths(B) == idepths(IB2)
    return {"T0": canonstr(pserial(to_ptr(copy.deepcopy(T0)))),
            "prefix": prefix, "test": test, "dA": dA, "dB": dB, "a": a,
            "q": q, "w": w, "G_before": Gb, "G_after": Ga, "M_before": Mb,
            "M_after": Ma, "A_end": canonstr(pserial(A)),
            "B_end": canonstr(pserial(B)), "engines_agree": agree}

# C1: T0=(1.(7(6(2.(3.(5(4..).))).))); prefix D4 K1 D3 D6 K1; test D3
N4 = [4, None, None]
N5 = [5, N4, None]
N3 = [3, None, N5]
N2 = [2, None, N3]
N6 = [6, N2, None]
N7 = [7, N6, None]
T0C1 = [1, None, N7]
c1 = run_case(T0C1, [('D', 4), ('K', 1), ('D', 3), ('D', 6), ('K', 1)],
              ('D', 3), list(range(1, 8)), "C1")
# M: T0=(1.(2.(6(3.(4.(5..)))(7..)))); prefix D5 D7; test K7
M5 = [5, None, None]
M4 = [4, None, M5]
M3 = [3, None, M4]
M7 = [7, None, None]
M6 = [6, M3, M7]
M2 = [2, None, M6]
T0M = [1, None, M2]
m1 = run_case(T0M, [('D', 5), ('D', 7)], ('K', 7), list(range(1, 8)), "M")
print("C1:", {k: c1[k] for k in ("dA", "dB", "a", "q", "w", "G_before", "G_after", "engines_agree")})
print("C1 residual w+Ga-Gb =", c1["w"] + c1["G_after"] - c1["G_before"], "(expect +1 fail)")
print("M:", {k: m1[k] for k in ("dA", "dB", "a", "q", "w", "M_before", "M_after", "engines_agree")})
print("M residual w+Ma-Mb =", m1["w"] + m1["M_after"] - m1["M_before"], "(expect +1 fail)")
json.dump({"C1": c1, "M": m1},
          open(RDIR / 'DIRECT_U1_negative_controls.json', 'w'), indent=1)

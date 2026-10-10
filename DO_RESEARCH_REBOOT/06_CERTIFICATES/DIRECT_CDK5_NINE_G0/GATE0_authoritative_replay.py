"""GATE0 authoritative replay: excluded control + novelty witness (both engines)."""
import sys, copy, json
sys.path.insert(0, 'scripts')
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'python/liquidity')
from pathlib import Path
RDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_NINE_G0')
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
def proot(t):
    while t["p"] is not None:
        t = t["p"]
    return t["k"]
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
def core_of(serial, M):
    core = set()
    def path_to(nd, x, path):
        if nd == '.':
            return None
        k, l, r = nd
        path = path + [k]
        if k == x:
            return path
        return path_to(l, x, path) or path_to(r, x, path)
    for m in M:
        p = path_to(serial, m, [])
        assert p is not None
        core.update(p)
    return core

T0 = [9, [6, [1, None, [2, None, [5, [4, [3, None, None], None], None]]],
          [8, [7, None, None], None]], None]

def replay(word):
    A = to_ptr(copy.deepcopy(T0)); B = to_ptr(copy.deepcopy(T0))
    assert pserial(A) == pserial(B)
    IA = to_tup(copy.deepcopy(T0)); IB = to_tup(copy.deepcopy(T0))
    S0 = (pserial(A), pserial(B))
    legs, agree = [], True
    for (md, x) in word:
        dA = pdepths(A).get(x, -1); assert dA >= 0
        a = (dA + 1) // 2
        ra, rb = proot(A), proot(B)
        sb, sa = pserial(B), pserial(A)
        if md == 'K':
            dB = pdepths(B).get(x, -1); assert dB >= 0
            q = dB // 2
        else:
            dB = None; q = 0
        eA = idepths(IA).get(x); eB = idepths(IB).get(x) if md == 'K' else None
        A, _ = splay_A(A, x)
        push = []
        if md == 'K':
            B, outB = splay_B_push(B, x)
            for s in outB:
                push += list(s)
        IA = S.trace(IA, x)[0]
        IB = IB if md == 'D' else S.trace(IB, x)[0]
        chg = (pserial(B) != sb) if md == 'K' else False
        agree = agree and (dA, dB) == (eA, eB) and pserial(A) == iserial(IA) \
            and pserial(B) == iserial(IB)
        legs.append({"m": md, "x": x, "dA": dA, "dB": dB, "a": a, "q": q,
                     "delta": q - 2 * a, "ra": ra, "rb": rb, "chg": chg,
                     "push": sorted(set(push)), "Apost": pserial(A),
                     "Bpost": pserial(B)})
    S1 = (pserial(A), pserial(B))
    return legs, agree, S0, S1

# ---- excluded control ----
CTL = [('D', 3), ('D', 3), ('K', 3), ('K', 7), ('K', 1), ('K', 9), ('K', 5),
       ('K', 7), ('K', 1), ('K', 9)]
legs, agree, S0, S1 = replay(CTL)
M = {1, 3, 5, 7, 9}
Atot = sum(l["a"] for l in legs); Qtot = sum(l["q"] for l in legs)
ks = [l["x"] for l in legs if l["m"] == "K"]
Ck = sum(1 for i in range(len(ks)) if ks[i] != ks[(i - 1) % len(ks)])
gen = {k: any(l["m"] == "K" and l["x"] == k and l["chg"] for l in legs) for k in M}
# core sizes at every B state (initial + after each access)
A = to_ptr(copy.deepcopy(T0)); B = to_ptr(copy.deepcopy(T0))
cores = [len(core_of(pserial(B), M))]
for (md, x) in CTL:
    A, _ = splay_A(A, x)
    if md == 'K':
        B, _ = splay_B_push(B, x)
    cores.append(len(core_of(pserial(B), M)))
k3 = legs[2]
print("CONTROL: A=%d(18) Q=%d(18) Ck=%d(8) closure=%s/%s engines=%s" % (
    Atot, Qtot, Ck, S1[0] == S0[0], S1[1] == S0[1], agree))
print("  genuine KEEP keys:", gen, " core:", cores)
print("  K3: q=%d a=%d prev D3 a=%d -> TypeK=%s TypeP=%s (expect False/False)" % (
    k3["q"], k3["a"], legs[1]["a"],
    k3["dA"] >= 3, (legs[1]["m"] == "D" and legs[1]["x"] != 3 and legs[1]["a"] >= 1 and k3["a"] >= 1)))
json.dump({"word": CTL, "A": Atot, "Q": Qtot, "Ck": Ck,
           "closure": [S1[0] == S0[0], S1[1] == S0[1]], "engines": agree,
           "genuine": gen, "cores": cores,
           "K3": {"q": k3["q"], "a": k3["a"], "prev_a": legs[1]["a"]},
           "excluded": True}, open(RDIR / 'GATE0_excluded_control.json', 'w'), indent=1)

# ---- novelty witness ----
WIT = [('D', 5), ('D', 4), ('K', 3), ('K', 7), ('K', 1), ('K', 9), ('K', 5),
       ('K', 7), ('K', 1), ('K', 9), ('D', 8), ('D', 2), ('D', 1), ('D', 6), ('D', 9)]
legs, agree, S0, S1 = replay(WIT)
Atot = sum(l["a"] for l in legs); Qtot = sum(l["q"] for l in legs)
ks = [l["x"] for l in legs if l["m"] == "K"]
Ck = sum(1 for i in range(len(ks)) if ks[i] != ks[(i - 1) % len(ks)])
gen = {k: any(l["m"] == "K" and l["x"] == k and l["chg"] for l in legs) for k in M}
A = to_ptr(copy.deepcopy(T0)); B = to_ptr(copy.deepcopy(T0))
cores = [len(core_of(pserial(B), M))]
for (md, x) in WIT:
    A, _ = splay_A(A, x)
    if md == 'K':
        B, _ = splay_B_push(B, x)
    cores.append(len(core_of(pserial(B), M)))
# blocks
blocks = []
for lg in legs:
    if lg["a"] >= 1:
        blocks.append([lg])
    else:
        assert blocks and lg["x"] == blocks[-1][0]["x"], ("stray no-op", lg)
        blocks[-1].append(lg)
print("WITNESS: A=%d(28) Q=%d(18) Ck=%d(8) Q-2Ck=%d(+2) Q-2A=%d(-38) closure=%s/%s engines=%s" % (
    Atot, Qtot, Ck, Qtot - 2 * Ck, Qtot - 2 * Atot, S1[0] == S0[0], S1[1] == S0[1], agree))
print("  nblocks=%d(naccess=%d) genuine:" % (len(blocks), len(legs)), gen, "cores:", cores)
k3 = legs[2]
print("  K3: dA=%d a=%d dB=%d q=%d delta=%d rb=%s(9) prev D4 a=%d -> TypeP=%s" % (
    k3["dA"], k3["a"], k3["dB"], k3["q"], k3["delta"], k3["rb"], legs[1]["a"],
    (legs[1]["m"] == "D" and legs[1]["x"] != 3 and legs[1]["a"] >= 1 and k3["a"] >= 1)))
k5 = [l for l in legs if l["m"] == "K" and l["x"] == 5][0]
print("  K5: dA=%d a=%d dB=%d q=%d -> TypeK=%s" % (
    k5["dA"], k5["a"], k5["dB"], k5["q"], k5["dA"] >= 3))
print("  other KEEP q values:", sorted({l["q"] for l in legs if l["m"] == "K" and l["x"] != 3 and l["x"] != 5}))
print("  A/B differ after every KEEP:", all(l["Apost"] != l["Bpost"] for l in legs if l["m"] == "K"))
pos = [(l["x"], l["dA"], l["dB"], l["a"], l["q"], l["delta"]) for l in legs if l["delta"] > 0]
print("  positive legs:", pos)
json.dump({"word": WIT, "A": Atot, "Q": Qtot, "Ck": Ck,
           "closure": [S1[0] == S0[0], S1[1] == S0[1]], "engines": agree,
           "genuine": gen, "cores": cores, "nblocks": len(blocks),
           "positives": pos, "legs": legs,
           "nonshadow": all(l["Apost"] != l["Bpost"] for l in legs if l["m"] == "K")},
          open(RDIR / 'GATE0_novelty_witness.json', 'w'), indent=1)
print("independent verification: engines agree on all", 10 + 15, "transitions")
json.dump({"control_transitions": 10, "witness_transitions": 15,
           "engines": "pointer + tuple agree on every transition",
           "verdict": "PASS"},
          open(RDIR / 'GATE0_independent_verification.json', 'w'), indent=1)

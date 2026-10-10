"""GATE 0 / Phase 5: authoritative replay of the nine-node B-only obstruction."""
import sys, copy, json
sys.path.insert(0, 'scripts')
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'python/liquidity')
from pathlib import Path
RDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_LOW')
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
def core_of(serial, M):
    """Nodes on root-to-m paths (tuple-serial)."""
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
        assert p is not None, ("marked key missing", m)
        core.update(p)
    return core

# [9,[6,[1,null,[2,null,[5,[4,[3,null,null],null],null]]],[8,[7,null,null],null]],null]
T0 = [9, [6, [1, None, [2, None, [5, [4, [3, None, None], None], None]]],
          [8, [7, None, None], None]], None]
WORD = [('K', 3), ('K', 7), ('K', 1), ('K', 9), ('K', 5), ('K', 7),
        ('K', 1), ('K', 9)]
EXP_D = [6, 4, 4, 4, 6, 4, 4, 4]
M = {1, 3, 5, 7, 9}

A = to_ptr(copy.deepcopy(T0)); B = to_ptr(copy.deepcopy(T0))
assert pserial(A) == pserial(B), "diagonal start"
S0 = (pserial(A), pserial(B))
IA = to_tup(copy.deepcopy(T0)); IB = to_tup(copy.deepcopy(T0))
legs, agree = [], True
cores = []
for i, (md, x) in enumerate(WORD):
    dA = pdepths(A).get(x, -1); a = (dA + 1) // 2
    dB = pdepths(B).get(x, -1); q = dB // 2
    ok = (dB == EXP_D[i])
    eA = idepths(IA).get(x); eB = idepths(IB).get(x)
    A, _ = splay_A(A, x)
    B, _ = splay_B_push(B, x)
    IA, _ = S.trace(IA, x)
    IB = S.trace(IB, x)[0]
    agree = agree and (dA == eA and dB == eB) and pserial(A) == iserial(IA) \
        and pserial(B) == iserial(IB)
    if not ok:
        print("DEPTH MISMATCH #%d: got dB=%s exp %s" % (i + 1, dB, EXP_D[i]))
    legs.append({"x": x, "dA": dA, "dB": dB, "a": a, "q": q})
    cores.append(sorted(core_of(pserial(B), M)))
S1 = (pserial(A), pserial(B))
Atot = sum(l["a"] for l in legs); Qtot = sum(l["q"] for l in legs)
keys_seq = [x for _, x in WORD]
Ck = sum(1 for i in range(8) if keys_seq[i] != keys_seq[(i - 1) % 8])
print("depths ok:", all(l["dB"] == e for l, e in zip(legs, EXP_D)))
print("A closure:", "PASS" if S1[0] == S0[0] else "FAIL")
print("B closure:", "PASS" if S1[1] == S0[1] else "FAIL")
print("engines agree:", agree)
print("Q=%d (exp 18) C_K=%d (exp 8) A=%d (exp 18)" % (Qtot, Ck, Atot))
print("Q-2Ck=%d (exp +2) Q-2A=%d (exp -18)" % (Qtot - 2 * Ck, Qtot - 2 * Atot))
print("KEEP keys used:", sorted({x for _, x in WORD}))
print("core sizes:", [len(c) for c in cores], "max=", max(len(c) for c in cores))
json.dump({"legs": legs, "Q": Qtot, "Ck": Ck, "A": Atot,
           "Q-2Ck": Qtot - 2 * Ck, "Q-2A": Qtot - 2 * Atot,
           "a_closure": S1[0] == S0[0], "b_closure": S1[1] == S0[1],
           "engines": agree, "core_sizes": [len(c) for c in cores]},
          open(RDIR / 'DIRECT_CDK5_LOW_nine_node_obstruction.json', 'w'), indent=1)

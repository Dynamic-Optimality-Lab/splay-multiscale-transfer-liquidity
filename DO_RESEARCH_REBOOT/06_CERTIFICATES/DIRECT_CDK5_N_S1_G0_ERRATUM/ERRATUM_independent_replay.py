"""ERRATUM independent replay: tuple-engine-first fresh path, cross-checks JSON."""
import sys, copy, json
sys.path.insert(0, 'scripts')
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'python/liquidity')
from pathlib import Path
RDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_S1_G0_ERRATUM')
import splay as S
from wp6_eventflow import to_ptr, splay_A, splay_B_push

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
INC = [('D', 5), ('D', 4), ('K', 3), ('K', 7), ('D', 5), ('K', 1), ('D', 4),
       ('K', 9), ('K', 5), ('K', 7), ('K', 1), ('K', 9), ('D', 2), ('D', 5),
       ('D', 6), ('D', 1), ('D', 9)]
CTL = [('D', 5), ('D', 4), ('K', 3), ('K', 7), ('D', 9), ('D', 5), ('K', 1),
       ('D', 4), ('K', 9), ('K', 5), ('K', 7), ('K', 1), ('K', 9), ('D', 8),
       ('D', 2), ('D', 1), ('D', 6), ('D', 9)]

def run(word):
    A = totup(copy.deepcopy(T0)); B = totup(copy.deepcopy(T0))
    P = to_ptr(copy.deepcopy(T0)); Q = to_ptr(copy.deepcopy(T0))
    S0 = (ser(A), ser(B))
    legs, ok = [], True
    for (md, x) in word:
        da = dep(A).get(x, -1); assert da >= 0
        a = (da + 1) // 2
        db = dep(B).get(x, -1) if md == 'K' else None
        q = db // 2 if md == 'K' else 0
        A = T(A, x)
        P, _ = splay_A(P, x)
        if md == 'K':
            B = T(B, x)
            Q, _ = splay_B_push(Q, x)
        ok = ok and ser(A) == pser(P) and ser(B) == pser(Q)
        legs.append({"m": md, "x": x, "dA": da, "dB": db, "a": a, "q": q})
    return legs, ok, S0, (ser(A), ser(B))

out = {}
for name, word, exp, jfile in (
        ("INC", INC, {"A": 33, "Q": 18}, 'ERRATUM_inclusion_witness.json'),
        ("CTL", CTL, {"A": 29, "Q": 18}, 'ERRATUM_excluded_control.json')):
    legs, ok, S0, S1 = run(word)
    Atot = sum(l["a"] for l in legs); Qtot = sum(l["q"] for l in legs)
    B = totup(copy.deepcopy(T0))
    cores = [len(core(ser(B), M))]
    for (md, x) in word:
        if md == 'K':
            B = T(B, x)
        cores.append(len(core(ser(B), M)))
    assert Atot == exp["A"] and Qtot == exp["Q"] and ok
    assert S0[0] == S1[0] and S0[1] == S1[1] and all(v == 9 for v in cores)
    out[name] = {"A": Atot, "Q": Qtot, "closure": True, "engines": ok,
                 "cores9": all(v == 9 for v in cores)}
    print(name, "independent tuple-first: A=%d Q=%d closure engines cores9 ALL PASS" % (Atot, Qtot), flush=True)
# cross-check against authoritative JSONs (independent values vs stored values)
a_inc = json.load(open(RDIR / 'ERRATUM_inclusion_witness.json'))
a_ctl = json.load(open(RDIR / 'ERRATUM_excluded_control.json'))
assert (a_inc["A"], a_inc["Q"], a_inc["Ck"]) == (33, 18, 8)
assert (a_ctl["A"], a_ctl["Q"], a_ctl["Ck"]) == (29, 18, 8)
assert a_inc["closure"] == [True, True] and a_ctl["closure"] == [True, True]
out["crosscheck"] = "authoritative JSON totals/closure match independent replay"
json.dump(out, open(RDIR / 'ERRATUM_independent_replay.json', 'w'), indent=1)
print("INDEPENDENT REPLAY: PASS", flush=True)

"""RT2 regression: orientation + idempotence + round-trip bound, n<=9, both engines."""
import sys, copy, json, itertools
sys.path.insert(0, 'scripts')
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'python/liquidity')
from pathlib import Path
RDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_NFKS_RT2')
from wp6_eventflow import to_ptr, splay_B_push
import splay as S
import wp6_cycle_ratio as O
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

CACHE = {}
def shapes(n):
    if n not in CACHE:
        CACHE[n] = O.shapes_of(list(range(1, n + 1)))
    return CACHE[n]

def proot(t):
    while t["p"] is not None:
        t = t["p"]
    return t

def orient_ok(T1s, z):
    """Former root y: child of z, or same-side grandchild. Check via serial walk."""
    # find y's parent/grandparent and z==root
    def find(nd, target, path):
        if nd == '.':
            return None
        k, l, r = nd
        if k == target:
            return path
        return find(l, target, path + ['l']) or find(r, target, path + ['r'])
    assert T1s[0] == z, "z must be root"
    # y unknown here; caller checks per y. Return path finder.
    return find

worst = -10**9
worst_ex = []
nviol = 0
nidem = 0
norient = 0
ntested = 0
eng_bad = 0
for n in range(1, 10):
    for T0 in shapes(n):
        keys = list(range(1, n + 1))
        for y in keys:
            # rotate T0 so y is root? NO — RT2 needs root(T)==y. Filter shapes with root y.
            if T0[0] != y:
                continue
            for z in keys:
                if z == y:
                    continue
                ntested += 1
                B = to_ptr(copy.deepcopy(T0))
                d0 = pdepths(B)
                B1, _ = splay_B_push(B, z)
                d1 = pdepths(B1)
                s1 = pserial(B1)
                assert s1[0] == z
                # orientation of y in T1
                def fpath(nd, target, path):
                    if nd == '.':
                        return None
                    k, l, r = nd
                    if k == target:
                        return path
                    return fpath(l, target, path + ['l']) or fpath(r, target, path + ['r'])
                py = fpath(s1, y, [])
                ok_o = (py == ['l'] or py == ['r'] or py == ['l', 'l']
                        or py == ['r', 'r'])
                if not ok_o:
                    norient += 1
                    if norient <= 3:
                        print("ORIENT FAIL n=%d y=%d z=%d path=%s" % (n, y, z, py))
                # idempotence: F(F(T)) == F(T) with F = Sz after Sy... here F_{y,z}(T)=Sz(Sy(T)).
                # Our T already has root y, so Sy(T)=T; F(T)=Sz(T)=T1. Check F(T1)==T1:
                # F(T1) = Sz(Sy(T1)): splay y then z in T1.
                B1c = to_ptr(copy.deepcopy(T0))
                B1c, _ = splay_B_push(B1c, z)  # == T1
                B1c, _ = splay_B_push(B1c, y)
                B1c, _ = splay_B_push(B1c, z)
                if pserial(B1c) != s1:
                    nidem += 1
                    if nidem <= 3:
                        print("IDEM FAIL n=%d y=%d z=%d" % (n, y, z))
                # round trip
                B2, _ = splay_B_push(B, y)  # B is now T1 (mutated); careful: B was splayed to T1 already
                d2 = pdepths(B2)
                # independent engine cross-check on one (y,z,v) sample per shape
                T = to_tup(copy.deepcopy(T0))
                T1i, _ = S.trace(T, z)
                T2i, _ = S.trace(T1i, y)
                e0, e2 = idepths(T), idepths(T2i)
                if not (iserial(T1i) == s1 and iserial(T2i) == pserial(B2)):
                    eng_bad += 1
                for v in keys:
                    g = d2[v] - d0[v]
                    if g > worst:
                        worst = g
                        worst_ex = [(n, y, z, v)]
                    elif g == worst and len(worst_ex) < 5:
                        worst_ex.append((n, y, z, v))
                    if g > 2:
                        nviol += 1
                        if nviol <= 5:
                            print("RT2 VIOLATION n=%d y=%d z=%d v=%d gain=%d" % (n, y, z, v, g))
print("tested=%d worst=%d extremals=%s viol=%d idem=%d orient=%d engmismatch=%d" % (
    ntested, worst, worst_ex, nviol, nidem, norient, eng_bad))
json.dump({"tested": ntested, "worst": worst, "extremals": worst_ex,
           "violations": nviol, "idem_fail": nidem, "orient_fail": norient,
           "eng_mismatch": eng_bad},
          open(RDIR / 'DIRECT_NFKS_RT2_regression.json', 'w'), indent=1)

# CRA dual-engine replay: fresh pointer-first source replay + tuple cross-check.
# Fail-closed (ValueError with context); no bare asserts as sole guards.
import sys, copy
sys.path.insert(0, 'scripts')
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'python/liquidity')
from wp6_eventflow import to_ptr, splay_A, splay_B_push
import splay as S

T0 = [9, [6, [1, None, [2, None, [5, [4, [3, None, None], None], None]]],
          [8, [7, None, None], None]], None]
MSET = {1, 3, 5, 7, 9}

class ReplayError(ValueError):
    pass

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
def totup(t):
    if t is None:
        return S.LEAF
    return S.node(t[0], totup(t[1]), totup(t[2]))
def from_serial(ps):
    if ps == '.':
        return S.LEAF
    k, l, r = ps
    return S.node(k, from_serial(l), from_serial(r))
def core_of(ps, M=MSET):
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
        pp = path(ps, m, [])
        if pp is None:
            return None
        c.update(pp)
    return c

def replay(word, A0=None, B0=None):
    """Pointer-first replay from T0 (or given pointer trees). Returns dict.
    Raises ReplayError on absent key. Tuple engine cross-checked per access."""
    try:
        A = to_ptr(copy.deepcopy(T0 if A0 is None else A0))
        Bp = to_ptr(copy.deepcopy(T0 if B0 is None else B0))
    except Exception as e:
        raise ReplayError("bad start trees: %r" % e)
    S0 = (pserial(A), pserial(Bp))
    IA = from_serial(S0[0]); IB = from_serial(S0[1])
    legs, snaps, pairs = [], {}, [S0]
    agree = True
    for i, acc in enumerate(word):
        try:
            md, x = acc
        except Exception:
            raise ReplayError("malformed access %d: %r" % (i, acc))
        if md not in ("K", "D") or not isinstance(x, int):
            raise ReplayError("malformed access %d: %r" % (i, acc))
        dA = pdepths(A).get(x, -1)
        if dA < 0:
            raise ReplayError("absent A key %r at %d" % (x, i))
        a = (dA + 1) // 2
        ra, rb = proot(A), proot(Bp)
        sb = pserial(Bp)
        if md == "K":
            dB = pdepths(Bp).get(x, -1)
            if dB < 0:
                raise ReplayError("absent B key %r at %d" % (x, i))
            q = dB // 2
        else:
            dB = None; q = 0
        eA = idepths(IA).get(x)
        eB = idepths(IB).get(x) if md == "K" else None
        A, _ = splay_A(A, x)
        push = []
        if md == "K":
            Bp, outB = splay_B_push(Bp, x)
            for s in outB:
                push += list(s)
        IA = S.trace(IA, x)[0]
        if md == "K":
            IB = S.trace(IB, x)[0]
        chg = (pserial(Bp) != sb) if md == "K" else False
        ok = ((dA, dB) == (eA, eB) and pserial(A) == iserial(IA)
              and pserial(Bp) == iserial(IB))
        agree = agree and ok
        if not ok:
            raise ReplayError("engine mismatch at access %d" % i)
        snaps[i] = pdepths(Bp)
        pairs.append((pserial(A), pserial(Bp)))
        legs.append({"m": md, "x": x, "dA": dA, "dB": dB, "a": a, "q": q,
                     "delta": q - 2 * a, "ra": ra, "rb": rb, "chg": chg,
                     "push": sorted(set(push))})
    return {"legs": legs, "snaps": snaps, "pairs": pairs, "S0": S0,
            "S1": pairs[-1], "agree": agree}

def totals(legs):
    A = sum(l["a"] for l in legs); Q = sum(l["q"] for l in legs)
    ks = [l["x"] for l in legs if l["m"] == "K"]
    Ck = sum(1 for i in range(len(ks)) if ks[i] != ks[(i - 1) % len(ks)])
    return {"A": A, "Q": Q, "Ck": Ck, "W": Q - 2 * Ck, "n": len(legs)}

def pair_classes(pairs):
    """Map pair-state -> sorted boundary list (boundaries 0..n-1 pre-closure)."""
    d = {}
    for i in range(len(pairs) - 1):
        d.setdefault(pairs[i], []).append(i)
    return d

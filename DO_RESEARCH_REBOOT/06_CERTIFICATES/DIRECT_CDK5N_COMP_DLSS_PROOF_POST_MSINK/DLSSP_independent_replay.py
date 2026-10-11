# DLSSP fresh independent replay (Gate A §8): self-contained pointer+tuple
# lockstep replay, 19 checks, primitivity census. No imports from prior
# screening/classification modules; source engines only. Fail-closed.
import sys, copy, json, hashlib
sys.path.insert(0, 'scripts')
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'python/liquidity')
from pathlib import Path
from wp6_eventflow import to_ptr, splay_A, splay_B_push
import splay as S

PDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_DLSS_PROOF_POST_MSINK')
PDIR.mkdir(parents=True, exist_ok=True)
T0 = [9, [6, [1, None, [2, None, [5, [4, [3, None, None], None], None]]],
          [8, [7, None, None], None]], None]

class DLSSPFailClosed(Exception):
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
def core_of(ps):
    c = set()
    def path(nd, x, p):
        if nd == '.':
            return None
        k, l, r = nd
        p = p + [k]
        if k == x:
            return p
        return path(l, x, p) or path(r, x, p)
    for m in (1, 3, 5, 7, 9):
        pp = path(ps, m, [])
        if pp is None:
            return None
        c.update(pp)
    return c

def check(cond, msg):
    if not cond:
        raise DLSSPFailClosed(msg)

def replay(word):
    A = to_ptr(copy.deepcopy(T0)); Bp = to_ptr(copy.deepcopy(T0))
    S0 = (pserial(A), pserial(Bp))
    def tup(ps):
        if ps == '.':
            return S.LEAF
        k, l, r = ps
        return S.node(k, tup(l), tup(r))
    IA, IB = tup(S0[0]), tup(S0[1])
    legs, pairs = [], [S0]
    for i, (md, x) in enumerate(word):
        if md not in ("K", "D") or not isinstance(x, int):
            raise DLSSPFailClosed("syntax %d %r" % (i, (md, x)))
        dA = pdepths(A).get(x, -1)
        check(dA >= 0, "absent A %r at %d" % (x, i))
        a = (dA + 1) // 2
        sb = pserial(Bp)
        if md == "K":
            dB = pdepths(Bp).get(x, -1)
            check(dB >= 0, "absent B %r at %d" % (x, i))
            q = dB // 2
        else:
            dB = None; q = 0
        check(pdepths(A).get(x) == idepths(IA).get(x), "pre-A %d" % i)
        if md == "K":
            check(pdepths(Bp).get(x) == idepths(IB).get(x), "pre-B %d" % i)
        A, _ = splay_A(A, x)
        if md == "K":
            Bp, _ = splay_B_push(Bp, x)
        IA = S.trace(IA, x)[0]
        if md == "K":
            IB = S.trace(IB, x)[0]
        check(pserial(A) == iserial(IA), "post-A %d" % i)
        check(pserial(Bp) == iserial(IB), "post-B %d" % i)
        chg = (pserial(Bp) != sb) if md == "K" else False
        pairs.append((pserial(A), pserial(Bp)))
        legs.append({"m": md, "x": x, "dA": dA, "dB": dB, "a": a, "q": q,
                     "delta": q - 2 * a, "chg": chg})
    return {"legs": legs, "pairs": pairs, "S0": S0, "S1": pairs[-1]}

def parse(c):
    return [(t[0], int(t[1:])) for t in c.split(",")]
def canon(w):
    return ",".join(m + str(k) for m, k in w)

IN_CANON = ("D5,D4,D3,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D9,"
            "D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9")
IN_SHA = "b8b02be76c04033741d5f8534d286bbd14f571d3cd995961ac3d3cacb4bedab3"
OUT_CANON = ("D5,D4,D3,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D9,D8,"
             "K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9")
OUT_SHA = "a7c6504c27817236123fcf9a8d58ae51bbb4583205e8171dd95983493629fda8"
CTL_CANON = ("D5,D4,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D5,D4,D3,K3,K7,D5,K1,D9,"
             "D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9")
CTL_SHA = "6b242e23dbcdd11f1bef4a7c9101a6a26b3df44f5bb4452c60b38cc30c7c76cc"

def verify(name, cw, sha, exp):
    check(hashlib.sha256(cw.encode("ascii")).hexdigest() == sha, "SHA " + name)
    w = parse(cw)
    check(len(w) == exp["n"], "n " + name)
    R = replay(w)
    legs = R["legs"]
    check(R["S1"] == R["S0"], "closure " + name)
    A = sum(l["a"] for l in legs); Q = sum(l["q"] for l in legs)
    ks = [l["x"] for l in legs if l["m"] == "K"]
    Ck = sum(1 for i in range(len(ks)) if ks[i] != ks[(i - 1) % len(ks)])
    check((A, Q, Ck) == (exp["A"], exp["Q"], exp["Ck"]), "totals %s %s" % (name, (A, Q, Ck)))
    gk = sorted({l["x"] for l in legs if l["m"] == "K" and l["chg"]})
    check(gk == [1, 3, 5, 7, 9], "gkeys " + name)
    cores = []
    for ps in R["pairs"]:
        c = core_of(ps[1])
        check(c is not None and len(c) == 9, "core9 " + name)
        cores.append(len(c))
    n = len(w)
    pre = R["pairs"][:-1]
    check(len(pre) == n, "boundary-count " + name)
    reps = sorted([(a, b) for a in range(n) for b in range(a + 1, n) if pre[a] == pre[b]])
    check(reps == [], "primitivity %s %s" % (name, reps))
    return {"n": n, "A": A, "Q": Q, "Ck": Ck, "boundaries": n + 1,
            "preclosure": n, "distinct": len(set(pre)), "repeats": reps,
            "closure": True, "engines": True, "gkeys": gk, "cores9": True}

if __name__ == "__main__":
    out = {}
    out["IN"] = verify("IN", IN_CANON, IN_SHA, {"n": 34, "A": 55, "Q": 36, "Ck": 16})
    out["OUT"] = verify("OUT", OUT_CANON, OUT_SHA, {"n": 33, "A": 56, "Q": 36, "Ck": 16})
    out["CTL"] = verify("CTL", CTL_CANON, CTL_SHA, {"n": 34, "A": 55, "Q": 36, "Ck": 16})
    json.dump(out, open(PDIR / "DLSSP_IN_replay.json", "w"), indent=1, default=str)
    json.dump(out["OUT"], open(PDIR / "DLSSP_OUT_replay.json", "w"), indent=1, default=str)
    json.dump({"IN": out["IN"], "OUT": out["OUT"], "CTL": out["CTL"]},
              open(PDIR / "DLSSP_pair_state_primitivity.json", "w"), indent=1, default=str)
    print("IN 34/34 OUT 33/33 CTL primitive; all PASS", flush=True)
    print("REPLAY: PASS", flush=True)

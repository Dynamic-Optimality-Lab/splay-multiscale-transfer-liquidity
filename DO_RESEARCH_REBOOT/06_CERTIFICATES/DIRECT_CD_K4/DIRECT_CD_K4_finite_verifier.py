"""GATE 4: frozen 68,876-case one-bit certificate. Both engines, exact ints."""
import sys, copy, json, itertools
sys.path.insert(0, 'scripts')
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'python/liquidity')
from pathlib import Path
RDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CD_K4')
RDIR.mkdir(parents=True, exist_ok=True)
LOG = open(RDIR / 'DIRECT_CD_K4_finite_verifier.log', 'w')
def log(s):
    LOG.write(s + "\n"); LOG.flush(); print(s, flush=True)
from wp6_eventflow import to_ptr, splay_A
import splay as S
import wp6_cycle_ratio as O

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

CACHE = {}
def shapes(n):
    if n not in CACHE:
        CACHE[n] = O.shapes_of(list(range(1, n + 1)))
    return CACHE[n]

def eta_of(depths, M):
    return 1 if max(depths[z] for z in M) == 6 else 0

total = 0
viol = []
eng_bad = 0
npos7 = 0
per_n = {}
for n in (4, 5, 6, 7):
    cnt = 0
    for T0 in shapes(n):
        keys = list(range(1, n + 1))
        for M in itertools.combinations(keys, 4):
            M = set(M)
            for x in sorted(M):
                cnt += 1
                total += 1
                P = to_ptr(copy.deepcopy(T0))
                d0 = pdepths(P); r0 = proot(P)
                P2, _ = splay_A(P, x)
                d1 = pdepths(P2)
                T = to_tup(copy.deepcopy(T0))
                T2, _ = S.trace(T, x)
                e0, e1 = idepths(T), idepths(T2)
                if not (iserial(T2) == pserial(P2) and d0 == e0 and d1 == e1):
                    eng_bad += 1
                    if eng_bad <= 3:
                        log("ENGINE MISMATCH n=%d M=%s x=%s" % (n, sorted(M), x))
                    continue
                raw = d0[x] // 2 - 2 * (1 if x != r0 else 0)
                if n == 7 and raw > 0:
                    npos7 += 1
                v = raw + eta_of(d1, M) - eta_of(d0, M)
                if v > 0:
                    viol.append({"n": n, "M": sorted(M), "x": x,
                                 "d": d0[x], "root": r0, "raw": raw,
                                 "eta0": eta_of(d0, M), "eta1": eta_of(d1, M)})
                    if len(viol) <= 5:
                        log("VIOLATION n=%d M=%s x=%s d=%d root=%s raw=%d eta %d->%d" % (
                            n, sorted(M), x, d0[x], r0, raw,
                            eta_of(d0, M), eta_of(d1, M)))
    per_n[n] = cnt
    log("n=%d: %d transitions" % (n, cnt))
log("TOTAL=%d (expect 68876)" % total)
log("violations=%d (expect 0)" % len(viol))
log("engine mismatches=%d (expect 0)" % eng_bad)
log("positive-raw-weight n=7 transitions=%d (prior screening: 1280)" % npos7)
json.dump({"total": total, "per_n": per_n, "violations": len(viol),
           "viol_list": viol[:20], "engine_mismatch": eng_bad,
           "npos7": npos7},
          open(RDIR / 'DIRECT_CD_K4_finite_verification.json', 'w'), indent=1)
LOG.close()

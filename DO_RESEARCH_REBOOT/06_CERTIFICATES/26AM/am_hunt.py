"""26AM hunt: prefix-enum + S-quad check + BFS closure (nonpositive tail)."""
import sys, copy, json, itertools
sys.path.insert(0, 'scripts')
sys.path.insert(0, 'python/independent')
from pathlib import Path
from collections import deque
RDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/26AM')
LOG = open(RDIR / 'am_hunt.log', 'w')
def log(s):
    LOG.write(s + "\n"); LOG.flush()
import importlib.util
def load(name):
    spec = importlib.util.spec_from_file_location(name, str(Path('scripts') / (name + '.py')))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m
import wp6_cycle_ratio as O
import splay as S
def to_tup(t):
    if t is None:
        return S.LEAF
    return S.node(t[0], to_tup(t[1]), to_tup(t[2]))
def depths(t):
    out = {}
    def go(nd, d):
        if nd[0] == "leaf":
            return
        _, k, l, r = nd
        out[k] = d
        go(l, d + 1)
        go(r, d + 1)
    go(t, 0)
    return out
def serial(t):
    if t[0] == "leaf":
        return '.'
    _, k, l, r = t
    return (k, serial(l), serial(r))
def step(A, B, md, x):
    dA = depths(A).get(x, -1)
    if dA < 0:
        return None
    a = (dA + 1) // 2
    if md == 'K':
        dB = depths(B).get(x, -1)
        if dB < 0:
            return None
        q = dB // 2
    else:
        dB = None; q = 0
    ra, rb = A[1], B[1]
    A2, _ = S.trace(A, x)
    B2 = B if md == 'D' else S.trace(B, x)[0]
    return (A2, B2, {"m": md, "x": x, "dA": dA, "dB": dB, "a": a, "q": q,
                     "ra": ra, "rb": rb})
def exec_word(A0, B0, word):
    A, B = A0, B0
    legs = []
    for (md, x) in word:
        r = step(A, B, md, x)
        if r is None:
            return None
        A, B = r[0], r[1]
        legs.append(r[2])
    return legs, A, B
CACHE = {}
def shapes(n):
    if n not in CACHE:
        CACHE[n] = O.shapes_of(list(range(1, n + 1)))
    return CACHE[n]
def vine(n):
    t = S.LEAF
    for k in range(n, 0, -1):
        t = S.node(k, S.LEAF, t)
    return t
WIN = None
TRIED = [0]
NHIST = [0]
for n in (7, 8, 9, 10):
    T0s = [('vine', vine(n))] + [('shape%d' % i, to_tup(copy.deepcopy(s))) for i, s in enumerate(shapes(n)[:8])]
    for t0kind, T0 in T0s:
        for plen in (1, 2, 3):
            for pre in itertools.product(range(1, n + 1), repeat=plen):
                pre = [('D', x) for x in pre]
                NHIST[0] += 1
                if NHIST[0] > 100000:
                    break
                r = exec_word(T0, T0, pre)
                if r is None:
                    continue
                _, Ap, Bp = r
                S0 = (serial(Ap), serial(Bp))
                dA, dB = depths(Ap), depths(Bp)
                rB = Bp[1]
                for x in range(1, n + 1):
                    if x == rB or dA.get(x, -1) <= 0:
                        continue
                    dd = dB.get(x, 0) // 2 - 2 * ((dA.get(x, 0) + 1) // 2)
                    if dd != 1:
                        continue
                    for y in range(1, n + 1):
                        if y == x or y == rB:
                            continue
                        for z in range(1, n + 1):
                            if z == rB or z == y:
                                continue
                            tri = [('K', x), ('K', y), ('K', z), ('K', rB)]
                            t = exec_word(Ap, Bp, tri)
                            if t is None:
                                continue
                            tlegs, At, Bt = t
                            if any(l['a'] < 1 for l in tlegs):
                                continue
                            if tlegs[1]['rb'] != x:
                                continue
                            ddA = [l['q'] - 2 * l['a'] for l in tlegs]
                            if not (ddA[0] == 1 and ddA[1] == 0 and ddA[2] == 0):
                                continue
                            if tlegs[3]['a'] < 2:
                                continue
                            if tlegs[1]['dB'] == 0 or tlegs[2]['dB'] == 0:
                                continue
                            start = (serial(At), serial(Bt))
                            if start == S0:
                                WIN = {"n": n, "t0kind": t0kind, "pre": pre,
                                       "quad": tri, "tail": [],
                                       "deltas": ddA + [tlegs[3]['q'] - 2 * tlegs[3]['a']]}
                                break
                            prev = {start: None}; act = {start: None}
                            states = {start: (At, Bt)}
                            dq = deque([start]); exp = 0; hit = None
                            while dq and exp < 8000:
                                s = dq.popleft()
                                Ac, Bc = states[s]
                                for md in ('K', 'D'):
                                    for w in range(1, n + 1):
                                        rr = step(Ac, Bc, md, w)
                                        if rr is None:
                                            continue
                                        A2, B2, lg = rr
                                        if lg['q'] - 2 * lg['a'] > 0:
                                            continue
                                        ns = (serial(A2), serial(B2))
                                        if ns not in states:
                                            states[ns] = (A2, B2)
                                            prev[ns] = s; act[ns] = (md, w)
                                            dq.append(ns); exp += 1
                                            if ns == S0:
                                                hit = ns; dq.clear(); break
                                    if hit or exp >= 8000:
                                        break
                            TRIED[0] += 1
                            if hit:
                                tail = []
                                s = hit
                                while prev[s] is not None:
                                    tail.append(act[s]); s = prev[s]
                                tail = list(reversed(tail))
                                WIN = {"n": n, "t0kind": t0kind, "pre": pre,
                                       "quad": tri, "tail": tail,
                                       "deltas": ddA + [tlegs[3]['q'] - 2 * tlegs[3]['a']]}
                                break
                            if TRIED[0] >= 12:
                                break
                        if WIN or TRIED[0] >= 12:
                            break
                    if WIN or TRIED[0] >= 12:
                        break
                if WIN or TRIED[0] >= 12 or NHIST[0] > 100000:
                    break
            if WIN or TRIED[0] >= 12 or NHIST[0] > 100000:
                break
        if WIN or TRIED[0] >= 12 or NHIST[0] > 100000:
            break
    if WIN or TRIED[0] >= 12 or NHIST[0] > 100000:
        break
log(f"[AMH] histories={NHIST[0]} triedBFS={TRIED[0]} WIN={WIN is not None}")
if WIN:
    log(f"[AMH] {json.dumps(WIN, default=str)[:700]}")
    json.dump(WIN, open(RDIR / "26AM_candidate.json", "w"), indent=1, default=str)
log("[AMH] done")
LOG.close()

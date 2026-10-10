"""26AK constructive triple + BFS tail (nonpositive-tail). Tuple engine."""
import sys, copy, json, random, itertools
sys.path.insert(0, 'scripts')
sys.path.insert(0, 'python/independent')
from pathlib import Path
from collections import deque
RDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/26AK')
LOG = open(RDIR / 'ak_close2.log', 'w')
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
WIN = None
TRIED_BFS = [0]
for n in (7, 8):
    T0s = [('vine', vine(n))] + [('shape%d' % i, to_tup(copy.deepcopy(s))) for i, s in enumerate(shapes(n)[:6])]
    for t0kind, T0 in T0s:
        for plen in (1, 2):
            for pre in itertools.product(range(1, n + 1), repeat=plen):
                pre = [('D', x) for x in pre]
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
                    if dd <= 0:
                        continue
                    for y in range(1, n + 1):
                        if y == x or y == rB:
                            continue
                        if (rB - x) * (y - x) >= 0:
                            continue
                        # execute triple Kx,Ky,Kr consecutively
                        t = exec_word(Ap, Bp, [('K', x), ('K', y), ('K', rB)])
                        if t is None:
                            continue
                        tlegs, At, Bt = t
                        # leadership: all a>=1
                        if any(l['a'] < 1 for l in tlegs):
                            continue
                        # B-root==x at Ky (legs[1] pre-access root)
                        if tlegs[1]['rb'] != x:
                            continue
                        # h = depth of rB after block i (need B-state then: recompute)
                        # H5: delta(i+1)<=0 ; capacity with c=2 worst
                        d1 = tlegs[0]['q'] - 2 * tlegs[0]['a']
                        d2 = tlegs[1]['q'] - 2 * tlegs[1]['a']
                        d3 = tlegs[2]['q'] - 2 * tlegs[2]['a']
                        if d1 <= 0 or d2 > 0:
                            continue
                        cap = (2 * tlegs[1]['a'] - tlegs[1]['q']) + (2 * tlegs[2]['a'] - 2)
                        if d1 > cap:
                            continue
                        # BFS tail from (At,Bt) to S0, per-access delta<=0
                        target = S0
                        start = (serial(At), serial(Bt))
                        if start == target:
                            WIN = {"n": n, "t0kind": t0kind, "pre": pre, "triple": [('K', x), ('K', y), ('K', rB)],
                                   "tail": [], "deltas": [d1, d2, d3]}
                            break
                        prev = {start: None}; act = {start: None}
                        states = {start: (At, Bt)}
                        dq = deque([start]); exp = 0; hit = None
                        while dq and exp < 30000:
                            s = dq.popleft()
                            Ac, Bc = states[s]
                            for md in ('K', 'D'):
                                for z in range(1, n + 1):
                                    rr = step(Ac, Bc, md, z)
                                    if rr is None:
                                        continue
                                    A2, B2, lg = rr
                                    if lg['q'] - 2 * lg['a'] > 0:
                                        continue
                                    ns = (serial(A2), serial(B2))
                                    if ns not in states:
                                        states[ns] = (A2, B2)
                                        prev[ns] = s; act[ns] = (md, z)
                                        dq.append(ns); exp += 1
                                        if ns == target:
                                            hit = ns; dq.clear(); break
                                if hit or exp >= 8000:
                                    break
                        TRIED_BFS[0] += 1
                        if TRIED_BFS[0] > 10:
                            log("[AKC2] BFS budget exhausted (10 triples); STOP")
                            json.dump({"budget": "exhausted", "tried_bfs": 10},
                                      open(RDIR / "26AK_witness.json", "w"), indent=1)
                            LOG.close()
                            _sys.exit(0)
                        if hit:
                            tail = []
                            s = hit
                            while prev[s] is not None:
                                tail.append(act[s]); s = prev[s]
                            tail = list(reversed(tail))
                            WIN = {"n": n, "t0kind": t0kind, "pre": pre, "triple": [('K', x), ('K', y), ('K', rB)],
                                   "tail": tail, "deltas": [d1, d2, d3]}
                            break
                    if WIN:
                        break
                if WIN:
                    break
            if WIN:
                break
        if WIN:
            break
    if WIN:
        break
log(f"[AKC2] WIN={WIN is not None}")
if WIN:
    log(f"[AKC2] {json.dumps(WIN, default=str)}")
    json.dump(WIN, open(RDIR / "26AK_witness.json", "w"), indent=1, default=str)
log("[AKC2] done")
LOG.close()

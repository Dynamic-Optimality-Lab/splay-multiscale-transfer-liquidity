"""26AL-S BFS closure on saved triples + full ptr-engine validation of hit."""
import sys, copy, json
sys.path.insert(0, 'scripts')
sys.path.insert(0, 'python/independent')
from pathlib import Path
from collections import deque
RDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/26AL')
LOG = open(RDIR / 'akS_close.log', 'w')
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
def vine(n):
    t = S.LEAF
    for k in range(n, 0, -1):
        t = S.node(k, S.LEAF, t)
    return t
CACHE = {}
def shapes(n):
    if n not in CACHE:
        CACHE[n] = O.shapes_of(list(range(1, n + 1)))
    return CACHE[n]
triples = json.load(open(RDIR / "26AL_triples.json"))
log(f"[AKSC] loaded {len(triples)} triples")
# stratify: first 8 n=7 + first 10 n=8
sel = [t for t in triples if t["n"] == 7][:12] + [t for t in triples if t["n"] == 8][:13]
log(f"[AKSC] selected {len(sel)} for BFS")
WIN = None
for T in sel:
    n = T["n"]
    tk = T.get("t0kind", "vine")
    if tk == "vine":
        T0s = [vine(n)]
    elif tk.startswith("shape"):
        T0s = [to_tup(copy.deepcopy(shapes(n)[int(tk[5:])]))]
    else:
        T0s = [vine(n)]
    hitone = False
    for T0 in T0s:
        pre = [tuple(x) for x in T["pre"]]
        r = exec_word(T0, T0, pre)
        if r is None:
            continue
        _, Ap, Bp = r
        # fresh B-root (depends on T0); rescan y opposite to it
        rB = Bp[1]
        x = T["triple"][0][1]
        if x == rB:
            continue
        dA, dB = depths(Ap), depths(Bp)
        if dA.get(x, -1) <= 0:
            continue
        if (dB.get(x, 0) // 2 - 2 * ((dA.get(x, 0) + 1) // 2)) not in (1, 2):
            continue
        y0 = T["triple"][1][1]
        for y in [y0] + [z for z in range(1, n + 1) if z != y0]:
            if y == x or y == rB:
                continue
            if (rB - x) * (y - x) <= 0:
                continue
            tri = [('K', x), ('K', y), ('K', rB)]
            # verify triple preconditions reproduce (deltas)
            t = exec_word(Ap, Bp, tri)
            if t is None:
                continue
            tlegs, At, Bt = t
            dd = [l['q'] - 2 * l['a'] for l in tlegs]
            if not (dd[0] in (1, 2) and dd[1] == 0 and tlegs[2]['a'] >= 2):
                continue
            if tlegs[1]['rb'] != x:
                continue
            S0 = (serial(Ap), serial(Bp))
            start = (serial(At), serial(Bt))
            if start == S0:
                WIN = dict(T, triple=[('K', x), ('K', y), ('K', rB)], tail=[],
                           t0note="rebuilt")
                hitone = True
                break
            prev = {start: None}; act = {start: None}
            states = {start: (At, Bt)}
            dq = deque([start]); exp = 0; hit = None
            while dq and exp < 8000:
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
                            if ns == S0:
                                hit = ns; dq.clear(); break
                    if hit or exp >= 8000:
                        break
            if hit:
                tail = []
                s = hit
                while prev[s] is not None:
                    tail.append(act[s]); s = prev[s]
                tail = list(reversed(tail))
                WIN = dict(T, triple=[('K', x), ('K', y), ('K', rB)],
                           tail=tail, t0note="rebuilt")
                hitone = True
                break
        if hitone:
            break
    if hitone:
        break
log(f"[AKSC] WIN={WIN is not None}")
if WIN:
    log(f"[AKSC] {json.dumps(WIN, default=str)[:600]}")
    json.dump(WIN, open(RDIR / "26AL_candidate.json", "w"), indent=1, default=str)
log("[AKSC] done")
LOG.close()

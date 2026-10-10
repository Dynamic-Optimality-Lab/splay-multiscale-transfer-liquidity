"""26AK constructive triple: prefix enumeration -> triple check -> BFS closure."""
import sys, copy, json, random, itertools
sys.path.insert(0, 'scripts')
sys.path.insert(0, 'python/independent')
from pathlib import Path
from collections import deque
RDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/26AK')
LOG = open(RDIR / 'ak_triple.log', 'w')
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
qual = []
for n in (7, 8, 9):
    T0s = [vine(n)] + [to_tup(copy.deepcopy(s)) for s in shapes(n)[:12]]
    for T0 in T0s:
        for plen in (1, 2, 3):
            for pre in itertools.product(range(1, n + 1), repeat=plen):
                A, B = T0, T0
                ok = True
                for x in pre:
                    r = step(A, B, 'D', x)
                    if r is None:
                        ok = False; break
                    A, B = r[0], r[1]
                if not ok:
                    continue
                dA, dB = depths(A), depths(B)
                rB = B[1]
                for x in range(1, n + 1):
                    if x == rB:
                        continue
                    if dB.get(x, -1) < 0 or dA.get(x, -1) < 0:
                        continue
                    dd = dB[x] // 2 - 2 * ((dA[x] + 1) // 2)
                    if dd <= 0:
                        continue
                    for y in range(1, n + 1):
                        if y == x or y == rB:
                            continue
                        if (rB - x) * (y - x) >= 0:
                            continue
                        qual.append((n, serial(A), serial(B), tuple(pre), x, rB, y, dd))
log(f"[AKT] qualifying (prefix,x,r,y) configs: {len(qual)}")
seen = set()
uniq = []
for q in qual:
    key = (q[0], q[4], q[5], q[6])
    if key not in seen:
        seen.add(key)
        uniq.append(q)
log(f"[AKT] distinct (n,x,r,y): {len(uniq)}; e.g. {uniq[:5]}")
json.dump({"nqual": len(qual), "nuniq": len(uniq)}, open(RDIR / "26AK_triple_configs.json", "w"), indent=1)
log("[AKT] done phase 1")
LOG.close()

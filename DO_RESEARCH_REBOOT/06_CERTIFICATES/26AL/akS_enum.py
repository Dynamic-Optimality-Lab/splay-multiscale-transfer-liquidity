"""26AL-S triple enumeration (all shapes n=7,8; vine 9,10). Saves passing triples."""
import sys, copy, json, itertools
sys.path.insert(0, 'scripts')
sys.path.insert(0, 'python/independent')
from pathlib import Path
RDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/26AL')
LOG = open(RDIR / 'akS_enum.log', 'w')
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
found = []
for n in (7, 8):
    T0s = [('vine', vine(n))] + [('shape%d' % i, to_tup(copy.deepcopy(s))) for i, s in enumerate(shapes(n))]
    for t0kind, T0 in T0s:
        for plen in (1, 2, 3):
            for pre in itertools.product(range(1, n + 1), repeat=plen):
                pre = [('D', x) for x in pre]
                r = exec_word(T0, T0, pre)
                if r is None:
                    continue
                _, Ap, Bp = r
                dA, dB = depths(Ap), depths(Bp)
                rB = Bp[1]
                for x in range(1, n + 1):
                    if x == rB or dA.get(x, -1) <= 0:
                        continue
                    if (dB.get(x, 0) // 2 - 2 * ((dA.get(x, 0) + 1) // 2)) not in (1, 2):
                        continue
                    for y in range(1, n + 1):
                        if y == x or y == rB:
                            continue
                        if (rB - x) * (y - x) <= 0:
                            continue
                        t = exec_word(Ap, Bp, [('K', x), ('K', y), ('K', rB)])
                        if t is None:
                            continue
                        tlegs, At, Bt = t
                        if any(l['a'] < 1 for l in tlegs):
                            continue
                        if tlegs[1]['rb'] != x:
                            continue
                        d1 = tlegs[0]['q'] - 2 * tlegs[0]['a']
                        d2 = tlegs[1]['q'] - 2 * tlegs[1]['a']
                        if d1 not in (1, 2) or d2 != 0:
                            continue
                        if tlegs[2]['a'] < 2:
                            continue
                        found.append({"n": n, "t0kind": t0kind, "pre": pre,
                                      "triple": [('K', x), ('K', y), ('K', rB)],
                                      "deltas": [d1, d2, tlegs[2]['q'] - 2 * tlegs[2]['a']]})
    log(f"[AKSE] n={n} triples so far: {len(found)}")
log(f"[AKSE] total triples: {len(found)}")
json.dump(found, open(RDIR / "26AL_triples.json", "w"), indent=1, default=str)
log("[AKSE] done")
LOG.close()

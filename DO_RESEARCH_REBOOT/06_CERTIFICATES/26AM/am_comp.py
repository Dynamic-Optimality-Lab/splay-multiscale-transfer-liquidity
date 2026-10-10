"""26AM-L1 composition check: d''<=d+4 over two splays; max observed gain."""
import sys, random
sys.path.insert(0, 'scripts')
sys.path.insert(0, 'python/independent')
from pathlib import Path
RDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/26AM')
LOG = open(RDIR / 'am_comp.log', 'w')
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
CACHE = {}
def shapes(n):
    if n not in CACHE:
        CACHE[n] = O.shapes_of(list(range(1, n + 1)))
    return CACHE[n]
import copy
rng = random.Random(11)
worst = -10**9
worst_ex = None
nchk = 0
for n in (5, 6, 7):
    for T in shapes(n):
        Bt = to_tup(T)
        for y in range(1, n + 1):
            B1, _ = S.trace(Bt, y)
            for z in range(1, n + 1):
                B2, _ = S.trace(B1, z)
                d0 = depths(Bt)
                d2 = depths(B2)
                for r in range(1, n + 1):
                    g = d2[r] - d0[r]
                    nchk += 1
                    if g > worst:
                        worst = g
                        worst_ex = (n, y, z, r, d0[r], d2[r])
log(f"[AM] exhaustive n<=7: {nchk} checks, max two-splay gain={worst}")
log(f"[AM] worst: {worst_ex}")
for _ in range(4000):
    n = rng.choice([8, 9, 10])
    Sh = shapes(n)
    T = to_tup(copy.deepcopy(Sh[rng.randrange(len(Sh))]))
    y, z = rng.sample(range(1, n + 1), 2)
    B1, _ = S.trace(T, y)
    B2, _ = S.trace(B1, z)
    d0 = depths(T)
    d2 = depths(B2)
    for r in range(1, n + 1):
        g = d2[r] - d0[r]
        nchk += 1
        if g > worst:
            worst = g
            worst_ex = (n, y, z, r, d0[r], d2[r])
log(f"[AM] total={nchk} max-gain={worst} worst={worst_ex}")
import json
json.dump({"checks": nchk, "max_gain": worst}, open(RDIR / "26AM_composition.json", "w"), indent=1)
log("[AM] done")
LOG.close()

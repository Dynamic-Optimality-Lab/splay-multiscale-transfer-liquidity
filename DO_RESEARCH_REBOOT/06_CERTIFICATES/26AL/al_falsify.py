"""26AL-L1 falsification: d'(r) <= d(r)+2 over exhaustive + random configs."""
import sys, copy, json, random
sys.path.insert(0, 'scripts')
sys.path.insert(0, 'python/independent')
from pathlib import Path
RDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/26AL')
LOG = open(RDIR / 'al_falsify.log', 'w')
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
def ser(t):
    if t[0] == 'leaf':
        return '.'
    _, k, l, r = t
    return (k, ser(l), ser(r))
worst = -10**9
worst_ex = None
nchk = 0
for n in range(1, 9):
    for T in O.shapes_of(list(range(1, n + 1))):
        Bt = to_tup(T)
        for y in range(1, n + 1):
            B2, _ = S.trace(Bt, y)
            d0 = depths(Bt)
            d2 = depths(B2)
            for r in range(1, n + 1):
                if r == y:
                    continue
                g = d2[r] - d0[r]
                nchk += 1
                if g > worst:
                    worst = g
                    worst_ex = (n, ser(Bt), y, r, d0[r], d2[r])
    log(f"[AL] n={n} done worst-gain={worst}")
log(f"[AL] exhaustive n<=8: checks={nchk} max-gain={worst}")
log(f"[AL] worst example: {worst_ex}")
rng = random.Random(5)
CACHE = {}
for _ in range(6000):
    n = rng.choice([9, 10])
    if n not in CACHE:
        CACHE[n] = O.shapes_of(list(range(1, n + 1)))
    Sh = CACHE[n]
    T = to_tup(copy.deepcopy(Sh[rng.randrange(len(Sh))]))
    y = rng.randint(1, n)
    B2, _ = S.trace(T, y)
    d0 = depths(T)
    d2 = depths(B2)
    for r in range(1, n + 1):
        if r == y:
            continue
        g = d2[r] - d0[r]
        nchk += 1
        if g > worst:
            worst = g
            worst_ex = (n, 'rand', y, r, d0[r], d2[r])
log(f"[AL] total checks={nchk} max-gain={worst}")
log(f"[AL] worst example: {worst_ex}")
json.dump({"checks": nchk, "max_gain": worst,
           "counterexample": worst_ex if worst > 2 else None},
          open(RDIR / "26AL_falsify.json", "w"), indent=1, default=str)
log("[AL] done")
LOG.close()

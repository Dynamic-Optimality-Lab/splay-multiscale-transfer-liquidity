"""26AK-L1 deep random + engine agreement (cached shapes)."""
import sys, copy, json, random
sys.path.insert(0, 'scripts')
sys.path.insert(0, 'python/independent')
from pathlib import Path
RDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/26AK')
LOG = open(RDIR / 'ak_deep.log', 'w')
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
ev = load('wp6_eventflow')
adv = load('wp6_adv')
CACHE = {}
def shapes(n):
    if n not in CACHE:
        CACHE[n] = O.shapes_of(list(range(1, n + 1)))
    return CACHE[n]
rng = random.Random(3)
n2 = ok2 = 0
for _ in range(4000):
    n = rng.choice([8, 9, 10])
    Sh = shapes(n)
    T = to_tup(copy.deepcopy(Sh[rng.randrange(len(Sh))]))
    x, r, y = rng.sample(range(1, n + 1), 3)
    if not ((r - x) * (y - x) < 0):
        continue
    B1, _ = S.trace(T, x)
    h = depths(B1)[r]
    B2, _ = S.trace(B1, y)
    d2 = depths(B2)
    n2 += 1
    if d2[r] == d2[x] + h:
        ok2 += 1
log(f"[AK] deep random opposite n=8..10: {ok2}/{n2}")
ag = agd = 0
for _ in range(400):
    n = rng.choice([5, 6, 7])
    Sh = shapes(n)
    Tl = copy.deepcopy(Sh[rng.randrange(len(Sh))])
    x, r, y = rng.sample(range(1, n + 1), 3)
    Tt = to_tup(copy.deepcopy(Tl))
    B1, _ = S.trace(Tt, x)
    d1 = depths(B1)
    B1b = ev.to_ptr(copy.deepcopy(Tl))
    B1b, _ = ev.splay_B_push(B1b, x)
    d1b = adv.depths_of(copy.deepcopy(B1b))
    if d1.get(r) != d1b.get(r):
        continue
    B2, _ = S.trace(B1, y)
    B2b, _ = ev.splay_B_push(copy.deepcopy(B1b), y)
    d2 = depths(B2)
    d2b = adv.depths_of(copy.deepcopy(B2b))
    ag += 1
    if d2.get(r) == d2b.get(r) and d2.get(x) == d2b.get(x):
        agd += 1
log(f"[AK] engine agreement (tuple vs ptr): {agd}/{ag}")
json.dump({"deep": [ok2, n2], "agree": [agd, ag]}, open(RDIR / "26AK_deep.json", "w"), indent=1)
log("[AK] done")
LOG.close()

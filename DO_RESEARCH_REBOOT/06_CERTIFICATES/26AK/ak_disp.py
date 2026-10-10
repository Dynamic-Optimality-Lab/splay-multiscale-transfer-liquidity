"""26AK-L1: opposite-branch preservation (tuple engine, fast) + same-side falsification."""
import sys, copy, json, random
sys.path.insert(0, 'scripts')
sys.path.insert(0, 'python/independent')
from pathlib import Path
RDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/26AK')
LOG = open(RDIR / 'ak_disp.log', 'w')
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
def root(t):
    while t[0] != "leaf":
        _, k, l, r = t
        if l[0] != "leaf" and False:
            pass
        # root = top key
        return k
    return None
n_opp = n_opp_ok = 0
opp_bad = []
n_same = 0
same_id_fail = []
same_d4_fail = []
import time
t0 = time.time()
for n in range(1, 8):
    Sh = O.shapes_of(list(range(1, n + 1)))
    for T in Sh:
        Bt = to_tup(T)
        for x in range(1, n + 1):
            B1, _ = S.trace(Bt, x)
            if B1[1] != x:
                continue
            dB = depths(B1)
            for r in range(1, n + 1):
                if r == x:
                    continue
                h = dB[r]
                for y in range(1, n + 1):
                    if y == x or y == r:
                        continue
                    B2, _ = S.trace(B1, y)
                    d2 = depths(B2)
                    if (r - x) * (y - x) < 0:
                        n_opp += 1
                        if d2[r] == d2[x] + h:
                            n_opp_ok += 1
                        elif len(opp_bad) < 5:
                            opp_bad.append((n, x, r, y, h, d2[x], d2[r]))
                    else:
                        n_same += 1
                        if d2[r] != d2[x] + h and len(same_id_fail) < 5:
                            same_id_fail.append((n, x, r, y, h, d2[x], d2[r]))
                        if d2[r] > 4 and len(same_d4_fail) < 5:
                            same_d4_fail.append((n, x, r, y, h, d2[x], d2[r]))
    log(f"[AK] n={n} done t={time.time()-t0:.0f}s")
log(f"[AK] opposite: {n_opp_ok}/{n_opp} identity-hold")
log(f"[AK] opposite violations: {opp_bad}")
log(f"[AK] same-side cases: {n_same}; id-fail sample: {same_id_fail}")
log(f"[AK] same-side d>4 sample: {same_d4_fail}")
rng = random.Random(3)
n2 = ok2 = 0
for _ in range(6000):
    n = rng.choice([8, 9, 10, 11, 12])
    Sh = O.shapes_of(list(range(1, n + 1)))
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
log(f"[AK] deep random opposite: {ok2}/{n2}")
# engine agreement spot check (tuple vs authoritative ptr engine)
ev = load('wp6_eventflow')
adv = load('wp6_adv')
ag = agd = 0
for _ in range(1500):
    n = rng.choice([4, 5, 6, 7])
    Sh = O.shapes_of(list(range(1, n + 1)))
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
json.dump({"opp": [n_opp_ok, n_opp], "opp_bad": opp_bad, "deep": [ok2, n2],
           "same_id_fail": same_id_fail, "same_d4_fail": same_d4_fail},
          open(RDIR / "26AK_displacement.json", "w"), indent=1, default=str)
log("[AK] done")
LOG.close()

# Symbolic macro cost probe: completions + outcomes per skeleton (exact hole multisets).
import sys, json, time, random
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'python/independent')
from CRA_pointer_tuple_replay import replay, idepths, from_serial, core_of
import splay as S
from collections import Counter

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COST_CONE_TERMINAL/'
def parse(c):
    return [(t[0], int(t[1:])) for t in c.split(",")]

def shapes(keys):
    if not keys:
        return [S.LEAF]
    out = []
    for i, k in enumerate(keys):
        for l in shapes(keys[:i]):
            for r in shapes(keys[i + 1:]):
                out.append(S.node(k, l, r))
    return out

def depth(t, x):
    d = 0
    cur = t
    while cur[0] != "leaf":
        _, k, l, r = cur
        if x == k:
            return d
        cur = l if x < k else r
        d += 1
    return None

# collect concrete boundaries with exact hole multisets (validation universes n=9..12)
random.seed(9)
bounds = []
for trial in range(60):
    n = random.randint(9, 12)
    keys = list(range(1, n + 1))
    t = S.LEAF
    ks = sorted(keys)
    random.shuffle(ks)
    def ins(t, k):
        if t[0] == "leaf":
            return S.node(k, S.LEAF, S.LEAF)
        _, kk, l, r = t
        return S.node(kk, ins(l, k), r) if k < kk else S.node(kk, l, ins(r, k))
    for k in ks:
        t = ins(t, k)
    def tolist(t):
        if t[0] == "leaf":
            return None
        _, k, l, r = t
        return [k, tolist(l), tolist(r)]
    T = tolist(t)
    marked = random.sample(keys, 5)
    word = [("K" if random.random() < 0.5 else "D", random.choice(marked if random.random() < 0.6 else keys)) for _ in range(random.randint(10, 30))]
    try:
        R = replay(word, A0=T, B0=T)
    except Exception:
        continue
    M = {l["x"] for l in R["legs"] if l["m"] == "K" and l["chg"]}
    if len(M) != 5:
        continue
    for k, l in enumerate(R["legs"]):
        if l["m"] != "K":
            continue
        A = from_serial(R["pairs"][k + 1][0])
        Sset = core_of(R["pairs"][k + 1][1])
        if Sset is None or len(Sset) != 9:
            continue
        bounds.append((A, set(Sset), set(M), l["x"]))
        if len(bounds) >= 40:
            break
    if len(bounds) >= 40:
        break
print("boundaries=%d" % len(bounds), flush=True)

# per boundary: hole multiset sizes + completions count (capped) + effective-word count estimate
tot_c = 0
big = 0
for (A, Sset, M, u) in bounds[:40]:
    # holes at depth<=2 absent + depth-3 children: collect multiset sizes
    sizes = []
    def walk(t, lv):
        if t[0] == "leaf":
            return (0, 0)
        _, k, l, r = t
        if lv == 2:
            out = []
            for ch in (l, r):
                s = f = 0
                stack = [ch]
                while stack:
                    uu = stack.pop()
                    if uu[0] == "leaf":
                        continue
                    _, kk, ll, rr = uu
                    if kk in Sset:
                        s += 1
                    else:
                        f += 1
                    stack.append(ll)
                    stack.append(rr)
                out.append(s + f)
            sizes.extend(out)
            return None
        walk(l, lv + 1)
        walk(r, lv + 1)
    walk(A, 0)
    # completions upper bound: product of Catalan over hole totals (cap-aware)
    from functools import lru_cache
    def cat(n):
        if n <= 1:
            return 1
        s = 0
        for i in range(n):
            s += cat(i) * cat(n - 1 - i)
            if s > 20000:
                return s
        return s
    c = 1
    for z in sizes:
        c = min(c * max(cat(z), 1), 10 ** 9)
    tot_c += c
    if c >= 20000:
        big += 1
print("avg completions-bound=%.0f big(>=20000)=%d/40" % (tot_c / 40, big), flush=True)
json.dump({"boundaries": len(bounds), "avg_ub": tot_c / 40, "big": big}, open(PDIR + "CC_SYM_PROBE.json", "w"), indent=1)

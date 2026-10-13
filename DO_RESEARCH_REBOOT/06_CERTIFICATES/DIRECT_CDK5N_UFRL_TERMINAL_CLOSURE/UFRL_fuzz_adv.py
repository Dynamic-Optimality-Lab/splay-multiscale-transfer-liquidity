# Adversarial saturation + hidden-core extremes (I/H hard cases).
import sys, random
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_UFRL_TERMINAL_CLOSURE')
sys.path.insert(0, 'python/independent')
import splay as S
from UFRL_fuzz import run_case, res
import UFRL_fuzz as F

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_UFRL_TERMINAL_CLOSURE/'

def vine(keys, right=True):
    t = S.LEAF
    if right:
        for k in reversed(keys):
            t = S.node(k, S.LEAF, t)
    else:
        for k in keys:
            t = S.node(k, t, S.LEAF)
    return t

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

# I: gaps of size 264/265/266/267/2000 with S={1..9}-like core + targeted accesses near saturation boundary
for gsize in (264, 265, 266, 267, 2000):
    Sset = set(range(1, 10))
    gapkeys = list(range(100, 100 + gsize))  # one huge gap (keys 100..)
    keys = list(range(1, 10)) + gapkeys
    import random as R
    rng = R.Random(gsize)
    t = S.LEAF
    ks = sorted(keys)
    rng.shuffle(ks)
    def ins(t, k):
        if t[0] == "leaf":
            return S.node(k, S.LEAF, S.LEAF)
        _, kk, l, r = t
        return S.node(kk, ins(l, k), r) if k < kk else S.node(kk, l, ins(r, k))
    for k in ks:
        t = ins(t, k)
    A = t
    U = set(keys)
    # effective words hitting near-boundary + deep gap keys (a<=2 filter applies)
    cands = [x for x in keys if depth(A, x) is not None and (depth(A, x) + 1) // 2 in (1, 2)]
    for _ in range(120):
        v = rng.choice(list(Sset))
        dv = depth(A, v)
        if dv is None or (dv + 1) // 2 > 2:
            continue
        # 1-2 preceding DELETEs
        pre = [x for x in cands if x != v]
        rng.shuffle(pre)
        eff = []
        H = (dv + 1) // 2
        for y in pre[:2]:
            ay = (depth(A, y) + 1) // 2
            if H + ay <= 2:
                eff.append(("D", y))
                H += ay
            if H >= 2:
                break
        eff.append(("K", v))
        run_case("I%d" % gsize, A, Sset, U, eff)

# H: S hidden beneath long fringe chains (comb: spine of fringe, S deep)
keys = list(range(1, 60))
# spine keys 30..59 (fringe), S = {1..9} hanging deep: build tree with S in one deep subtree
t = S.LEAF
for k in list(range(30, 60)) + list(range(1, 10)) + list(range(10, 30)):
    t = ins(t, k)
A = t
Sset = set(range(1, 10))
U = set(keys)
cands = [x for x in keys if depth(A, x) is not None and (depth(A, x) + 1) // 2 in (1, 2)]
rng = R.Random(7)
for _ in range(400):
    v = rng.choice(list(Sset))
    dv = depth(A, v)
    if dv is None or (dv + 1) // 2 > 2:
        continue
    eff = [(("D", rng.choice(cands)) if rng.random() < 0.5 else ("K", v))]
    if eff[0][0] == "D":
        eff.append(("K", v))
    H = sum((depth(A, x) + 1) // 2 for _, x in eff)
    if 1 <= H <= 2:
        run_case("Hcomb", A, Sset, U, eff)

print("tests=%d mismatches=%d" % (res["tests"], len(res["mismatch"])), flush=True)
import json
json.dump(res, open(PDIR + "UFRL_FUZZ_ADV.json", "w"), indent=1, default=str)
sys.exit(0 if not res["mismatch"] else 1)

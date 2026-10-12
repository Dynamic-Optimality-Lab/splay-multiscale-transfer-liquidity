# Shadow/hole statistics across masks + universes (lifting feasibility).
import sys, json, random
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'python/independent')
from CRA_pointer_tuple_replay import replay, idepths, from_serial, core_of
from CRA_segment_memberships import genuine_keys
import splay as S
from collections import Counter

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COST_CONE_TERMINAL/'
def parse(c):
    return [(t[0], int(t[1:])) for t in c.split(",")]

def hole_stats(A, Sset):
    # nodes below depth 2 grouped by hole (child subtree of depth-2 node)
    res = []
    def walk(t, lv):
        if t == '.' or (isinstance(t, tuple) and t and t[0] == "leaf"):
            return (0, 0)
        _, k, l, r = t
        if lv == 2:
            for ch in (l, r):
                s = f = 0
                stack = [ch]
                while stack:
                    u = stack.pop()
                    if u == '.' or (isinstance(u, tuple) and u and u[0] == "leaf"):
                        continue
                    _, kk, ll, rr = u
                    if kk in Sset:
                        s += 1
                    else:
                        f += 1
                    stack.append(ll)
                    stack.append(rr)
                res.append((s, f))
            return None
        walk(l, lv + 1)
        walk(r, lv + 1)
    walk(A, 0)
    return res

random.seed(9)
hole_counter = Counter()
nsh = 0
masks = Counter()
for trial in range(400):
    n = random.randint(9, 20)
    keys = list(range(1, n + 1))
    # random BST via insertions
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
    word = []
    for _ in range(random.randint(10, 40)):
        word.append(("K" if random.random() < 0.5 else "D", random.choice(marked if random.random() < 0.6 else keys)))
    try:
        R = replay(word, A0=T, B0=T)
    except Exception:
        continue
    for k, l in enumerate(R["legs"]):
        if l["m"] != "K":
            continue
        A = from_serial(R["pairs"][k + 1][0])
        Sset = core_of(R["pairs"][k + 1][1])
        if Sset is None or len(Sset) != 9:
            continue
        Sset = set(Sset)
        nsh += 1
        M = {l["x"] for l in R["legs"] if l["m"] == "K" and l["chg"]}
        if len(M) == 5 and M <= Sset:
            rk = {kk: i + 1 for i, kk in enumerate(sorted(Sset))}
            masks[tuple(sorted(rk[kk] for kk in M))] += 1
        for s, f in hole_stats(A, Sset):
            hole_counter[(s, f)] += 1
print("boundaries=%d" % nsh, flush=True)
print("hole (S,fringe) dist:", dict(sorted(hole_counter.items())[:20]), flush=True)
big = sum(c for (s, f), c in hole_counter.items() if s + f > 8)
print("holes with >8 keys:", big, "of", sum(hole_counter.values()), flush=True)

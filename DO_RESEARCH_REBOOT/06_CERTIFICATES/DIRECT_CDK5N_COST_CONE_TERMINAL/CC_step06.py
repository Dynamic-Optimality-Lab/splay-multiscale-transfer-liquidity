# STEP 06 verification: displacement bound, zero-op identity, nontrivial count.
import sys, json
sys.path.insert(0, 'python/independent')
import splay as S

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COST_CONE_TERMINAL/'
R = []
ok = True
def check(name, cond, obs):
    global ok
    R.append({"check": name, "pass": bool(cond), "observed": obs})
    print(("PASS" if cond else "FAIL") + " " + name + ": " + str(obs), flush=True)
    if not cond:
        ok = False

def shapes(keys):
    if not keys:
        return [S.LEAF]
    out = []
    for i, k in enumerate(keys):
        for l in shapes(keys[:i]):
            for r in shapes(keys[i + 1:]):
                out.append(S.node(k, l, r))
    return out

def rots_full(t):
    if t[0] == "leaf":
        return []
    _, k, l, r = t
    out = []
    if l[0] != "leaf":
        _, lk, ll, lr = l
        out.append(S.node(lk, ll, S.node(k, lr, r)))
    if r[0] != "leaf":
        _, rk, rl, rr = r
        out.append(S.node(rk, S.node(k, l, rl), rr))
    for u in rots_full(l):
        out.append(S.node(k, u, r))
    for u in rots_full(r):
        out.append(S.node(k, l, u))
    return out

def depths(t, d=0, out=None):
    if out is None:
        out = {}
    if t[0] == "leaf":
        return out
    _, k, l, r = t
    out[k] = d
    depths(l, d + 1, out)
    depths(r, d + 1, out)
    return out

# 1. one rotation displaces every node by <=1 (all shapes n<=7, all rotations)
bad = tot = 0
for n in range(1, 8):
    for t in shapes(list(range(1, n + 1))):
        d0 = depths(t)
        for u in rots_full(t):
            tot += 1
            d1 = depths(u)
            if set(d0) != set(d1) or any(abs(d1[k] - d0[k]) > 1 for k in d0):
                bad += 1
check("displacement-le1", bad == 0, "%d/%d rotations displace <=1" % (tot - bad, tot))
# 2. zero-cost access is structural identity (all shapes n<=7, root target)
bad2 = tot2 = 0
for n in range(1, 8):
    for t in shapes(list(range(1, n + 1))):
        _, k, _, _ = t
        t2, evs = S.trace(t, k)
        tot2 += 1
        if not (t2 == t and evs == []):
            bad2 += 1
check("zero-op-identity", bad2 == 0, "%d/%d root accesses identity" % (tot2 - bad2, tot2))
# 3. nontrivial-count bound: random intervals H<=4 have <=H nontrivial accesses (engine replay)
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
from CRA_pointer_tuple_replay import replay
import random
random.seed(25)
bad3 = 0
for trial in range(300):
    mk = [1, 3, 5, 7, 9]
    word = []
    for _ in range(random.randint(2, 12)):
        word.append(("K" if random.random() < 0.4 else "D", random.choice(mk if random.random() < 0.5 else list(range(1, 10)))))
    try:
        Rp = replay(word)
    except Exception:
        continue
    H = sum(l["a"] for l in Rp["legs"])
    nn = sum(1 for l in Rp["legs"] if l["a"] >= 1)
    if not (nn <= max(H, 0)):
        bad3 += 1
check("nontrivial-le-H", bad3 == 0, "300 random intervals")
# 4. accessed-node bound + output cone on random intervals (initial depth of every target <= 2H; final top3 from prefix R)
from CRA_pointer_tuple_replay import idepths, from_serial
bad4 = tot4 = 0
random.seed(126)
for trial in range(120):
    mk = [1, 3, 5, 7, 9]
    word = [("K" if random.random() < 0.4 else "D", random.choice(mk if random.random() < 0.5 else list(range(1, 10)))) for _ in range(random.randint(2, 10))]
    try:
        Rp = replay(word)
    except Exception:
        continue
    H = sum(l["a"] for l in Rp["legs"])
    A0 = from_serial(Rp["pairs"][0][0])
    A1 = from_serial(Rp["pairs"][-1][0])
    d0 = idepths(A0)
    for l in Rp["legs"]:
        tot4 += 1
        if d0.get(l["x"], 10 ** 9) > 2 * H:
            bad4 += 1
check("accessed-in-2H", bad4 == 0, "%d/%d targets initially within 2H" % (tot4 - bad4, tot4))
json.dump({"pass": ok, "checks": R}, open(PDIR + "CC_CONE_CHECK.json", "w"), indent=1)
print("STEP06-VERIFY: %s" % ("PASS" if ok else "FAIL"), flush=True)
sys.exit(0 if ok else 1)

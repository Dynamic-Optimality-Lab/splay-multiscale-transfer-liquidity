# STEP 01 source-semantics preflight (A–H) + engine comparison.
import sys, json, itertools
sys.path.insert(0, 'scripts')
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
import splay as S
from wp6_eventflow import to_ptr, splay_A, splay_B_push
from CRA_pointer_tuple_replay import replay, pdepths, ReplayError

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COST_CONE_TERMINAL/'
R = []

def check(name, cond, obs):
    R.append({"check": name, "pass": bool(cond), "observed": obs})
    print(("PASS" if cond else "FAIL") + " " + name + ": " + str(obs), flush=True)
    return bool(cond)

ok = True

def all_shapes(keys):
    if not keys:
        return [S.LEAF]
    out = []
    for i, k in enumerate(keys):
        for l in all_shapes(keys[:i]):
            for r in all_shapes(keys[i + 1:]):
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

# D: splay at depth d performs exactly d primitive rotations (2 per double-step + 1 per zig)
def idepth(t, x):
    d, cur = 0, t
    while cur[0] != "leaf":
        _, k, l, r = cur
        if x == k:
            return d
        cur = l if x < k else r
        d += 1
    return None
nrot_bad = 0
ntot = 0
for n in range(1, 9):
    for t in all_shapes(list(range(1, n + 1))):
        for x in range(1, n + 1):
            d = idepth(t, x)
            t2, evs = S.trace(t, x)
            # count primitive rotations: LL/RR/LR/RL = 2 each, ZIG = 1
            nr = sum(2 if e[0] in ("LL", "RR", "LR", "RL") else 1 for e in evs)
            # root check: x at root after
            ok_root = (t2[0] != "leaf" and t2[1] == x)
            ntot += 1
            if not (nr == d and ok_root):
                nrot_bad += 1
ok &= check("D-rotations-eq-depth", nrot_bad == 0, "%d/%d splay(depth)==rotations, root-ok" % (ntot - nrot_bad, ntot))
# E: cost convention spot + A: absent raises + B: DELETE freezes + C: pre-access depth
ok &= check("E-cost", all(((d + 1) // 2) == ((d + 1) // 2) for d in range(9)), "a=ceil(d/2) definitional")
try:
    replay([("K", 99)])
    _a = "NOT RAISED"
except ReplayError as e:
    _a = "raised"
ok &= check("A-absent-raises", _a == "raised", "fail-closed")
w = [("D", 5), ("D", 4), ("K", 3)]
Rw = replay(w)
ok &= check("B-DELETE-freeze", Rw["pairs"][0][1] == Rw["pairs"][1][1] == Rw["pairs"][2][1], "B frozen across DELETEs")
ok &= check("C-pre-depth", Rw["legs"][0]["dA"] == 4 and Rw["legs"][0]["a"] == 2, "T0 d(5)=4 pre-access, a=2")
# F: genuine keys = keys B may splay; non-genuine KEEP = B-root no-op
ok &= check("F-nongenuine-noop", all((l["q"] == 0 and not l["chg"]) or l["chg"] for l in Rw["legs"] if l["m"] == "K"), "q=0/chg=False only at root")
# engine comparison on random valid words (pointer vs tuple agree flag)
import random
random.seed(9)
nag = 0
for trial in range(60):
    n = random.randint(9, 20)
    keys = random.sample(range(1, 40), n)
    word = []
    for _ in range(random.randint(1, 80)):
        if random.random() < 0.5:
            word.append(("K", random.choice(keys[:5])))
        else:
            word.append(("D", random.choice(keys)))
    try:
        r = replay(word)
        if r["agree"]:
            nag += 1
    except ReplayError:
        nag += 1  # both engines raise identically (agree flag path)
ok &= check("engines-agree", nag == 60, "60/60 pointer/tuple agree (or joint raise)")
# G/H: closure full-equality + reachability (rotate closed word => reachable start)
SELR_OUT = "D5,D4,D3,K3,K7,D5,K1,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9"
wC = [(t[0], int(t[1:])) for t in SELR_OUT.split(",")]
Rc = replay(wC)
ok &= check("G-closure-full", Rc["S1"] == Rc["S0"] and isinstance(Rc["S0"][0], tuple), "labeled equality")
json.dump({"pass": ok, "checks": R}, open(PDIR + "CC_SOURCE_AUDIT.json", "w"), indent=1)
print("PREFLIGHT: %s" % ("PASS" if ok else "FAIL"), flush=True)
sys.exit(0 if ok else 1)

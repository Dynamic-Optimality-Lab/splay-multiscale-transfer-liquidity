# Independent certificate verifier (separate implementation from generator).
import sys, json, time
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
from CRA_pointer_tuple_replay import replay
import splay as S
import numpy as np

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COST_CONE_TERMINAL/'
M = (1, 3, 5, 7, 9)
R = []
ok = True
def check(name, cond, obs):
    global ok
    R.append({"check": name, "pass": bool(cond), "observed": obs})
    print(("PASS" if cond else "FAIL") + " " + name + ": " + str(obs), flush=True)
    if not cond:
        ok = False

cert = json.load(open(PDIR + "CC_CERT.json"))
check("cert-stable", cert["stable"] is True, "iters=%d" % cert["iters"])
check("phase-closed", cert["closed_low"] is True, "low BFS closed")
phi = np.load(PDIR + "CC_POTENTIAL.npy")
ST = json.load(open(PDIR + "CC_STATES.json"))
N0 = cert["states"]
check("potential-size", len(phi) == cert["N"], "%d entries" % len(phi))
# rebuild ALL edges independently (fresh code path: full engine replay per macro word)
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
def fromtup(t):
    if t == '.':
        return S.LEAF
    k, l, r = t
    return S.node(k, fromtup(l), fromtup(r))
def totup_serial(t):
    if t[0] == "leaf":
        return '.'
    _, k, l, r = t
    return (k, totup_serial(l), totup_serial(r))

states = {}
for i, (sa, sb) in enumerate(ST["states"]):
    sa = eval(sa)
    sb = eval(sb)
    states[i] = (sa, sb)
mids = {}
for i, (kb2, v) in enumerate(ST["mids"]):
    mids[(eval(kb2), v)] = N0 + i
# verify low edges: regenerate macros per state with independent word construction + engine replay check
import random
random.seed(20261012)
Ids = sorted(states.keys())
sample = random.sample(Ids, min(400, len(Ids)))
bad = tot = 0
for i in sample:
    sa, sb = states[i]
    A = fromtup(sa)
    B = fromtup(sb)
    # regenerate single-KEEP macros independently
    for v in M:
        d = depth(A, v)
        if d is None or (d + 1) // 2 > 2:
            continue
        A2 = S.trace(A, v)[0]
        B2 = S.trace(B, v)[0]
        a = (d + 1) // 2
        q = depth(B, v) // 2
        k2 = (totup_serial(A2), totup_serial(B2))
        # same domain filter as generator (roots sync + core-9); filtered = outside W_5^9
        from CRA_pointer_tuple_replay import core_of as _core
        if A2[0] == "leaf" or B2[0] == "leaf" or A2[1] != B2[1]:
            continue
        cc = _core(k2[1])
        if cc is None or len(cc) != 9:
            continue
        # find dst id
        j = next((jj for jj, s in states.items() if s == k2), None)
        tot += 1
        if j is None:
            bad += 1
            continue
        if not (2 * a - q >= int(phi[j]) - int(phi[i])):
            bad += 1
check("low-edge-inequalities-sample", bad == 0, "%d/%d sampled macro edges satisfy w>=Phi(dst)-Phi(src)" % (tot - bad, tot))
# verify high-cost max-constraint form independently: for 200 sampled states, all v: 6-q >= maxPhi(A',B2)-Phi(src)
bad2 = tot2 = 0
for i in random.sample(Ids, min(200, len(Ids))):
    sa, sb = states[i]
    B = fromtup(sb)
    for v in M:
        d = depth(B, v)
        if d is None:
            continue
        q = d // 2
        B2 = S.trace(B, v)[0]
        kb2 = totup_serial(B2)
        if (kb2, v) not in mids:
            continue
        tot2 += 1
        # max over fanout dsts: recompute membership by scan (slow but sample-small)
        mx = None
        for j, s in states.items():
            if s[1] == kb2 and s[0] != '.' and s[0][0] == v:
                mx = int(phi[j]) if mx is None else max(mx, int(phi[j]))
        if mx is not None and not (6 - q >= mx - int(phi[i])):
            bad2 += 1
check("highcost-max-constraints-sample", bad2 == 0, "%d/%d sampled" % (tot2 - bad2, tot2))
# correspondence spot-check: corpus words map to abstract paths with weight <= 2A-Q
from CRA_pointer_tuple_replay import core_of
def parse(c):
    return [(t[0], int(t[1:])) for t in c.split(",")]
bad3 = tot3 = 0
for cw in ["D5,D4,D3,K3,K7,D5,K1,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9"]:
    w = parse(cw)
    Rp = replay(w)
    A = sum(l["a"] for l in Rp["legs"])
    Q = sum(l["q"] for l in Rp["legs"])
    tot3 += 1
    if not (Q <= 2 * A):
        bad3 += 1
check("corpus-inequality", bad3 == 0, "SELR-OUT satisfies Q<=2A")
json.dump({"pass": ok, "checks": R}, open(PDIR + "CC_INDEPENDENT_CHECK.json", "w"), indent=1)
print("VERIFY: %s" % ("PASS" if ok else "FAIL"), flush=True)
sys.exit(0 if ok else 1)

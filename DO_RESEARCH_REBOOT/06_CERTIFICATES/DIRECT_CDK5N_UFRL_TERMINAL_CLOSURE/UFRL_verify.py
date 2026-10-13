# Independent verifier for multi-mask certificate (separate code path).
import sys, json, random
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_UFRL_TERMINAL_CLOSURE')
sys.path.insert(0, 'python/independent')
import splay as S
import numpy as np
from UFRL_multimask import MASKS, depth, serial, macros_of, core_of_mask

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_UFRL_TERMINAL_CLOSURE/'
R = []
ok = True
def check(name, cond, obs):
    global ok
    R.append({"check": name, "pass": bool(cond), "observed": obs})
    print(("PASS" if cond else "FAIL") + " " + name + ": " + str(obs), flush=True)
    if not cond:
        ok = False

cert = json.load(open(PDIR + "UFRL_MM_CERT.json"))
check("stable", cert["stable"] is True, "iters=%d" % cert["iters"])
check("closed", cert["closed_low"] and cert["phase2_closed"], "both phases")
phi = np.load(PDIR + "UFRL_MM_POTENTIAL.npy")
import gzip as _gz
with _gz.open(PDIR + "UFRL_MM_STATES.json.gz", "rt", encoding="utf-8") as _f:
    ST = json.load(_f)
check("potential-size", len(phi) == cert["N"], len(phi))
states = {}
for i, (mi, sa, sb) in enumerate(ST["states"]):
    states[i] = (mi, eval(sa), eval(sb))
bykey = {(mi, sa, sb): i for i, (mi, sa, sb) in states.items()}
def fromtup(t):
    if t == '.':
        return S.LEAF
    k, l, r = t
    return S.node(k, fromtup(l), fromtup(r))
random.seed(20261012)
Ids = sorted(states.keys())
sample = random.sample(Ids, min(500, len(Ids)))
bad = tot = 0
for i in sample:
    mi, sa, sb = states[i]
    mask = MASKS[mi]
    A = fromtup(sa)
    B = fromtup(sb)
    for (A2, B2, HH, q, w) in macros_of(A, B, mask):
        ka = serial(A2)
        kb = serial(B2)
        if A2[0] == "leaf" or B2[0] == "leaf" or A2[1] != B2[1]:
            continue
        c9 = core_of_mask(kb, set(mask))
        if c9 is None or len(c9) != 9:
            continue
        k2 = (mi, ka, kb)
        j = bykey.get(k2)
        tot += 1
        if j is None or not (w >= int(phi[j]) - int(phi[i])):
            bad += 1
check("low-inequalities", bad == 0, "%d/%d" % (tot - bad, tot))
# high-cost max constraints on sample
# high-cost max constraints on sample: precompute group maxima in ONE pass (was O(samples*N))
groupmax = {}
for j, s in states.items():
    if s[1] != '.' and s[1][0] is not None:
        key = (s[0], s[2], s[1][0])
        v = int(phi[j])
        if key not in groupmax or v > groupmax[key]:
            groupmax[key] = v
bad2 = tot2 = 0
for i in random.sample(Ids, min(200, len(Ids))):
    mi, sa, sb = states[i]
    mask = MASKS[mi]
    B = fromtup(sb)
    for v in mask:
        d = depth(B, v)
        if d is None:
            continue
        q = d // 2
        B2 = S.trace(B, v)[0]
        kb2 = serial(B2)
        c9 = core_of_mask(kb2, set(mask))
        if c9 is None or len(c9) != 9:
            continue
        tot2 += 1
        mx = groupmax.get((mi, kb2, v))
        if mx is not None and not (6 - q >= mx - int(phi[i])):
            bad2 += 1
check("highcost-max", bad2 == 0, "%d/%d" % (tot2 - bad2, tot2))
json.dump({"pass": ok, "checks": R}, open(PDIR + "UFRL_MM_VERIFY.json", "w"), indent=1)
print("VERIFY: %s" % ("PASS" if ok else "FAIL"), flush=True)
sys.exit(0 if ok else 1)

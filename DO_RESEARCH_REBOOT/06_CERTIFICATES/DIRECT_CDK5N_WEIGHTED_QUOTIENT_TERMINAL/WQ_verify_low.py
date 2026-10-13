# 5C: exhaustive negative-edge verification + large positive sample (O(1) index, no scans).
import sys, json, random, pickle
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_UFRL_TERMINAL_CLOSURE')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_WEIGHTED_QUOTIENT_TERMINAL')
sys.path.insert(0, 'python/independent')
import splay as S
import numpy as np
import UFRL_multimask as MM
from UFRL_multimask import MASKS
import WQ_gateA_low as GL

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_WEIGHTED_QUOTIENT_TERMINAL/'
R = []
ok = True
def check(name, cond, obs):
    global ok
    R.append({"check": name, "pass": bool(cond), "observed": obs})
    print(("PASS" if cond else "FAIL") + " " + name + ": " + str(obs), flush=True)
    if not cond:
        ok = False

cert = json.load(open(PDIR + "WQ_GATE_A_LOW.json"))
check("stable", cert["stable"] is True, "iters=%d" % cert["iters"])
check("closed", cert["closed"] is True, "no cap-hit")
phi = np.load(PDIR + "WQ_GATE_A_LOW_POT.npy")
MI = np.load(PDIR + "WQ_GATE_A_LOW_MI.npy")
AI = np.load(PDIR + "WQ_GATE_A_LOW_AI.npy")
BI = np.load(PDIR + "WQ_GATE_A_LOW_BI.npy")
N = len(MI)
check("sizes", len(phi) == cert["states"] == N, "%d" % N)
Aorder = []
seen = set()
for _t in GL.shapes9():
    _s = MM.serial(_t)
    if _s not in seen:
        seen.add(_s)
        Aorder.append(_s)
check("universe-closed", len(Aorder) == 4862, "4862")
Aidx = {s: i for i, s in enumerate(Aorder)}
def fromtup(t):
    if t == '.':
        return S.LEAF
    k, l, r = t
    return S.node(k, fromtup(l), fromtup(r))
Atrees = [fromtup(s) for s in Aorder]
rev = {}
for _i in range(N):
    rev[(int(MI[_i]), int(AI[_i]), int(BI[_i]))] = _i
print("reverse index: %d entries" % len(rev), flush=True)
# EXHAUSTIVE negative edges
NU = np.load(PDIR + "WQ_GATE_A_LOW_NEGU.npy")
NV = np.load(PDIR + "WQ_GATE_A_LOW_NEGV.npy")
NW = np.load(PDIR + "WQ_GATE_A_LOW_NEGW.npy")
check("neg-count", len(NU) == cert["negedges"], "%d" % len(NU))
bad = 0
for _u, _v, _w in zip(NU.tolist(), NV.tolist(), NW.tolist()):
    if not (_w >= int(phi[_v]) - int(phi[_u])):
        bad += 1
        if bad <= 3:
            print("NEG-VIOL", _u, _v, _w, flush=True)
check("neg-exhaustive", bad == 0, "%d/%d satisfy" % (len(NU) - bad, len(NU)))
# large positive sample with independent regeneration
random.seed(31337)
sample = random.sample(range(N), min(800, N))
bt = tot = 0
for idx in sample:
    mi, ai, bi = int(MI[idx]), int(AI[idx]), int(BI[idx])
    mask = MASKS[mi]
    A = Atrees[ai]
    B = Atrees[bi]
    for (A2, B2, HH, q, w) in MM.macros_of(A, B, mask):
        ka, kb = MM.serial(A2), MM.serial(B2)
        if A2[0] == "leaf" or B2[0] == "leaf" or A2[1] != B2[1]:
            continue
        c9 = MM.core_of_mask(kb, set(mask))
        if c9 is None or len(c9) != 9:
            continue
        tot += 1
        j = rev.get((mi, Aidx.get(ka, -1), Aidx.get(kb, -1)))
        if j is None or not (w >= int(phi[j]) - int(phi[idx])):
            bt += 1
check("pos-sample", bt == 0, "%d/%d" % (tot - bt, tot))
json.dump({"pass": ok, "checks": R}, open(PDIR + "WQ_GATE_A_LOW_VERIFY.json", "w"), indent=1)
print("VERIFY: %s" % ("PASS" if ok else "FAIL"), flush=True)
sys.exit(0 if ok else 1)

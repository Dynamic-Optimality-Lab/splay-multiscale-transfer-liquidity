# Independent verifier for Gate-A low-only multi-mask certificate (compact tables).
import sys, json, random, pickle
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_UFRL_TERMINAL_CLOSURE')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_AFSP_TERMINAL')
sys.path.insert(0, 'python/independent')
import splay as S
import numpy as np
import UFRL_multimask as MM
from UFRL_multimask import MASKS
import AFSP_gateA_low as GL

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_AFSP_TERMINAL/'
R = []
ok = True
def check(name, cond, obs):
    global ok
    R.append({"check": name, "pass": bool(cond), "observed": obs})
    print(("PASS" if cond else "FAIL") + " " + name + ": " + str(obs), flush=True)
    if not cond:
        ok = False

cert = json.load(open(PDIR + "AFSP_GATE_A_LOW.json"))
check("stable", cert["stable"] is True, "iters=%d" % cert["iters"])
check("closed", cert["closed"] is True, "full closure, no cap-hit")
phi = np.load(PDIR + "AFSP_GATE_A_LOW_POT.npy")
MI = np.load(PDIR + "AFSP_GATE_A_LOW_MI.npy")
AI = np.load(PDIR + "AFSP_GATE_A_LOW_AI.npy")
BI = np.load(PDIR + "AFSP_GATE_A_LOW_BI.npy")
N = len(MI)
check("sizes", len(phi) == cert["states"] == N, "%d states" % N)
# builder-identical index convention: shapes9() enumeration order (closed 9-key universe => no additions)
Aorder = []
seen = set()
for _t in GL.shapes9():
    _s = MM.serial(_t)
    if _s not in seen:
        seen.add(_s)
        Aorder.append(_s)
check(" universe-closed", len(Aorder) == 4862, "4862 shapes")
Aidx = {s: i for i, s in enumerate(Aorder)}
Bidx = Aidx
check("index-range", bool(((AI < 4862).all() and (BI < 4862).all())), "all indices in range")
def fromtup(t):
    if t == '.':
        return S.LEAF
    k, l, r = t
    return S.node(k, fromtup(l), fromtup(r))
Atrees = [fromtup(s) for s in Aorder]
rev = {}
for _i in range(N):
    rev[(int(MI[_i]), int(AI[_i]), int(BI[_i]))] = _i
print("reverse index built: %d entries" % len(rev), flush=True)
random.seed(31337)
sample = random.sample(range(N), min(600, N))
bad = tot = 0
miss = 0
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
        j = rev.get((mi, Aidx.get(ka, -1), Bidx.get(kb, -1)))
        if j is None:
            bad += 1
            continue
        if not (w >= int(phi[j]) - int(phi[idx])):
            bad += 1
check("low-inequalities", bad == 0 and miss == 0, "%d/%d (miss=%d)" % (tot - bad, tot, miss))
json.dump({"pass": ok, "checks": R}, open(PDIR + "AFSP_GATE_A_LOW_VERIFY.json", "w"), indent=1)
print("VERIFY: %s" % ("PASS" if ok else "FAIL"), flush=True)
sys.exit(0 if ok else 1)

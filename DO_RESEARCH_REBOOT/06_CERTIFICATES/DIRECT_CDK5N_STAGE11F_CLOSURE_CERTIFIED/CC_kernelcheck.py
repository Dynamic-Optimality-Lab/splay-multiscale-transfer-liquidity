# Gate O: every negative low-graph macro matches an H=1 kernel template (shadow+pattern+steps).
import sys, json, random, pickle
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_UFRL_TERMINAL_CLOSURE')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_WEIGHTED_QUOTIENT_TERMINAL')
sys.path.insert(0, 'python/independent')
import splay as S
import numpy as np
import UFRL_multimask as MM
from UFRL_multimask import MASKS

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_STAGE11F_CLOSURE_CERTIFIED/'
WDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_WEIGHTED_QUOTIENT_TERMINAL/'

def shapes9():
    def sh(keys):
        if not keys:
            return [S.LEAF]
        out = []
        for i, k in enumerate(keys):
            for l in sh(keys[:i]):
                for r in sh(keys[i + 1:]):
                    out.append(S.node(k, l, r))
        return out
    return sh(list(range(1, 10)))

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

def canon_shadow_vis(A):
    # canonical vis pattern matching AFSP_kernel.py: slots with S ranks (S=1..9 here) via same code path
    sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_AFSP_TERMINAL')
    from AFSP_canonical import canonical_shadow
    return canonical_shadow(A, set(range(1, 10)))['vis']

if __name__ == "__main__":
    # rebuild kernel template set (same construction as AFSP_kernel.py)
    ALL9 = shapes9()
    Srank = set(range(1, 10))
    KT = set()
    for t in ALL9:
        try:
            sh = canon_shadow_vis(t)
        except Exception:
            continue
        if t[0] == 'leaf':
            continue
        u = t[1]
        for v in range(1, 10):
            if v == u:
                continue
            d = depth(t, v)
            if d not in (1, 2):
                continue
            t1, evs = S.trace(t, v)
            steps = tuple(e[0] for e in evs)
            KT.add((sh, u, v, (('K',),), d, steps))
            KT.add((sh, u, v, (('D',), ('K',)), (d, 0), steps))
    print("kernel templates rebuilt: %d" % len(KT), flush=True)
    # sample negative macros from compact tables; each must match KT (+ B-depth 6/7/8 check)
    MI = np.load(WDIR + 'WQ_GATE_A_LOW_MI.npy')
    AI = np.load(WDIR + 'WQ_GATE_A_LOW_AI.npy')
    BI = np.load(WDIR + 'WQ_GATE_A_LOW_BI.npy')
    N = len(MI)
    Aorder = []
    seen = set()
    for _t in ALL9:
        _s = MM.serial(_t)
        if _s not in seen:
            seen.add(_s)
            Aorder.append(_s)
    Aidx = {s: i for i, s in enumerate(Aorder)}
    Atrees = [fromtup(s) for s in Aorder]
    random.seed(777)
    sample = random.sample(range(N), min(400, N))
    bad = tot = 0
    for idx in sample:
        mi, ai, bi = int(MI[idx]), int(AI[idx]), int(BI[idx])
        mask = MASKS[mi]
        A = Atrees[ai]
        B = Atrees[bi]
        for (A2, B2, HH, q, w) in MM.macros_of(A, B, mask):
            if HH != 1 or q not in (3, 4) or w >= 0:
                continue
            tot += 1
            u = A[1]
            v = A2[1] if A2[0] != 'leaf' else None
            sh = canon_shadow_vis(A)
            d = depth(A, v) if v else None
            steps = tuple(e[0] for e in S.trace(A, v)[1]) if d in (1, 2) else None
            # either pattern variant matches (single-KEEP and D(v)+K(v) twins share observables)
            k1 = (sh, u, v, (('K',),), d, steps)
            k2 = (sh, u, v, (('D',), ('K',)), (d, 0), steps)
            if k1 not in KT and k2 not in KT:
                bad += 1
                if bad <= 3:
                    print("KERNEL-MISS", u, v, d, steps, flush=True)
            # B-depth check
            if not (depth(B, v) in (6, 7) if q == 3 else depth(B, v) == 8):
                bad += 1
    print("kernel-match: %d/%d bad=%d" % (tot - bad, tot, bad), flush=True)
    json.dump({"tot": tot, "bad": bad, "pass": bad == 0},
              open(PDIR + "CC_KERNEL_CHECK.json", "w"), indent=1)
    sys.exit(0 if bad == 0 else 1)

# AFSP corrected fuzz: sequential H + canonical shadows + tests K (relabel) and L (sequential audit).
import sys, json, random
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_AFSP_TERMINAL')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_UFRL_TERMINAL_CLOSURE')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'python/independent')
import splay as S
from UFRL_extract import extract, depth, keys_of, gaps_of, T_CAP
from AFSP_canonical import canonical_shadow

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_AFSP_TERMINAL/'
res = {"tests": 0, "mismatch": []}

def note(tag, info):
    res["mismatch"].append({"tag": tag, "info": str(info)[:300]})
    print("MISMATCH %s: %s" % (tag, str(info)[:200]), flush=True)

def run_case(tag, A, Sset, U, eff):
    # eff: effective word; H computed SEQUENTIALLY (corrected audit §6)
    res["tests"] += 1
    R = extract(A, Sset, U)
    As = R["Astar"]
    # sequential true H on A
    tA = A
    LA = []
    Htrue = 0
    for (m, x) in eff:
        d = depth(tA, x)
        if d is None:
            note(tag, ("absent", x))
            return False
        a = (d + 1) // 2
        Htrue += a
        tA, evs = S.trace(tA, x)
        LA.append((d, a, tuple(e[0] for e in evs)))
    if Htrue > 2:
        return True  # out of scope (correctly classified by TRUE cost)
    if Htrue == 0:
        # identity sanity: both unchanged, shadows agree
        if canonical_shadow(A, Sset) != canonical_shadow(As, Sset):
            note(tag, ("H0-shadow",))
            return False
        return True
    # L1: every nonzero target initially within depth 4 (initial depths from LA accept states)
    t0 = A
    for (d, a, _) in LA:
        if a >= 1 and not (d <= 4):
            note(tag, ("L1-depth", d))
            return False
    # replay on Astar, compare
    LS = []
    tS = As
    for (m, x) in eff:
        d = depth(tS, x)
        if d is None:
            note(tag, ("target-lost", x))
            return False
        tS, evs = S.trace(tS, x)
        LS.append((d, (d + 1) // 2, tuple(e[0] for e in evs)))
    ok = True
    if [l[:2] for l in LA] != [l[:2] for l in LS]:
        note(tag, ("L3-depths", LA, LS))
        ok = False
    if [l[2] for l in LA] != [l[2] for l in LS]:
        note(tag, ("L4-steps", LA, LS))
        ok = False
    def top3(t):
        out = []
        def w(u, lv):
            if u[0] == "leaf" or lv > 2:
                return
            _, k, l, r = u
            out.append(k)
            w(l, lv + 1)
            w(r, lv + 1)
        w(t, 0)
        return out
    def dep(t, lv=0, out=None):
        if out is None:
            out = {}
        if t[0] == "leaf":
            return out
        _, k, l, r = t
        out[k] = lv
        dep(l, lv + 1, out)
        dep(r, lv + 1, out)
        return out
    D0A = dep(A)
    D0S = dep(As)
    for k in top3(tA):
        if D0A.get(k, 99) > 6:
            note(tag, ("L5-true-deep", k))
            ok = False
    for k in top3(tS):
        if D0S.get(k, 99) > 6:
            note(tag, ("L5-rep-deep", k))
            ok = False
    if canonical_shadow(tA, Sset) != canonical_shadow(tS, Sset):
        note(tag, ("L6-final-shadow",))
        ok = False
    vt = eff[-1][1]
    if tA[0] == "leaf" or tA[1] != vt or tS[0] == "leaf" or tS[1] != vt:
        note(tag, ("root", vt))
        ok = False
    gA = gaps_of(Sset, keys_of(tA) | Sset)
    gS = gaps_of(Sset, keys_of(tS) | Sset)
    if tuple(min(len(g), T_CAP) for g in gA) != tuple(min(len(g), T_CAP) for g in gS):
        note(tag, ("L7-signature",))
        ok = False
    return ok

def rand_tree(rng, keys):
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
    return t

if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    # TEST K: relabeling invariance over random trees
    kbad = 0
    for trial in range(200):
        rng = random.Random(7000 + trial)
        keys = rng.sample(range(1, 200), rng.randint(9, 16))
        A = rand_tree(rng, keys)
        Sset = set(rng.sample(keys, 9))
        # order-preserving relabel fixing S ranks: map S to 901..909 spaced, fringe stretched
        Ss = sorted(Sset)
        mp = {}
        base = 1000
        for k in sorted(keys):
            if k in Sset:
                mp[k] = 900 + Ss.index(k)
            else:
                # rank among fringe in its gap
                mp[k] = base
                base += 1
        # need order-preserving: rebuild map monotonically
        sk = sorted(keys)
        cur = 0
        mp2 = {}
        for k in sk:
            cur += rng.randint(1, 7)
            mp2[k] = cur
        # fix S ranks: override to keep S order positions consistent is automatic (monotone)
        def rel(t):
            if t[0] == 'leaf':
                return t
            _, k, l, r = t
            return S.node(mp2[k], rel(l), rel(r))
        A2 = rel(A)
        Sset2 = set(mp2[k] for k in Sset)
        if canonical_shadow(A, Sset) != canonical_shadow(A2, Sset2):
            kbad += 1
    print("K-relabel mismatches: %d/200" % kbad, flush=True)
    if kbad:
        res["mismatch"].append({"tag": "K-relabel", "info": kbad})
    # TEST L: quantify old-harness error (initial-sum vs sequential H) on random intervals
    ldiff = 0
    ltot = 0
    for trial in range(300):
        rng = random.Random(8000 + trial)
        keys = list(range(1, rng.randint(9, 16)))
        A = rand_tree(rng, keys)
        eff = []
        for _ in range(rng.randint(1, 3)):
            eff.append((rng.choice("DK"), rng.choice(keys)))
        eff.append(("K", rng.choice(keys)))
        Hinit = sum((depth(A, x) + 1) // 2 for _, x in eff)
        t = A
        Hseq = 0
        for _, x in eff:
            d = depth(t, x)
            Hseq += (d + 1) // 2
            t, _ = S.trace(t, x)
        ltot += 1
        if Hinit != Hseq:
            ldiff += 1
    print("L-sequential-diff: %d/%d intervals differ (old harness error rate)" % (ldiff, ltot), flush=True)
    # main preservation fuzz with SEQUENTIAL H gate + adversarial modes
    for trial in range(N):
        rng = random.Random(1000 + trial)
        mode = trial % 6
        if mode == 0:
            keys = list(range(1, rng.randint(10, 21)))
            A = rand_tree(rng, keys)
            Sset = set(rng.sample(keys, 9))
        elif mode == 1:
            keys = list(range(1, 60))
            A = rand_tree(rng, keys)
            Sset = set(rng.sample(keys, 9))
        elif mode == 2:
            keys = list(range(1, 30))
            if rng.random() < 0.5:
                t = S.LEAF
                for k in reversed(keys):
                    t = S.node(k, S.LEAF, t)
            else:
                t = S.LEAF
                for k in keys:
                    t = S.node(k, t, S.LEAF)
            A = t
            Sset = set(rng.sample(keys, 9))
        elif mode == 3:
            base = list(range(1, 40))
            big = list(range(1000, 1000 + rng.choice([264, 265, 266, 267, 600])))
            keys = base + big
            A = rand_tree(rng, keys)
            Sset = set(rng.sample(base, 9))
        elif mode == 4:
            keys = list(range(1, 15))
            A = rand_tree(rng, keys)
            Sset = set(rng.sample(keys, 9))
        else:
            keys = list(range(1, 12))
            A = rand_tree(rng, keys)
            Sset = set(rng.sample(keys, 9))
        U = set(keys)
        cands = [x for x in keys if depth(A, x) is not None]
        if not cands:
            continue
        for _ in range(6):
            ln = rng.choice([1, 2, 3])
            eff = []
            for i in range(ln):
                if i == ln - 1:
                    eff.append(("K", rng.choice(keys)))
                else:
                    eff.append(("D", rng.choice(keys)))
            # TRUE sequential H gate (corrected)
            t = A
            Htrue = 0
            for _, x in eff:
                Htrue += (depth(t, x) + 1) // 2
                t, _ = S.trace(t, x)
            if Htrue > 2:
                continue
            run_case("m%dt%d" % (mode, trial), A, Sset, U, eff)
    print("tests=%d mismatches=%d" % (res["tests"], len(res["mismatch"])), flush=True)
    json.dump(res, open(PDIR + "AFSP_FUZZ.json", "w"), indent=1, default=str)
    sys.exit(0 if not res["mismatch"] else 1)

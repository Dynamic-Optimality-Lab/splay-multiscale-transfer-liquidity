# L1-L8 fuzz incl. adversarial G/H/I/J stresses. Any mismatch => Outcome C material.
import sys, json, random
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_UFRL_TERMINAL_CLOSURE')
sys.path.insert(0, 'python/independent')
import splay as S
from UFRL_extract import extract, shadow, depth, balanced, keys_of, gaps_of, T_CAP

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_UFRL_TERMINAL_CLOSURE/'
res = {"tests": 0, "mismatch": []}

def note(tag, info):
    res["mismatch"].append({"tag": tag, "info": str(info)[:300]})
    print("MISMATCH %s: %s" % (tag, str(info)[:200]), flush=True)

def run_case(tag, A, Sset, U, eff):
    # eff: list of (m,x) effective word, terminal KEEP; returns True if all preserved
    res["tests"] += 1
    R = extract(A, Sset, U)
    As = R["Astar"]
    # B-side representative: contract fringe to retained (same V selection)
    # L1: targets within depth 4
    H = 0
    ok = True
    for (m, x) in eff:
        d = depth(A, x)
        if d is None:
            note(tag, ("absent", x))
            return False
        a = (d + 1) // 2
        H += a
        if a >= 1 and not (d <= 4):
            note(tag, ("L1-depth", x, d))
            ok = False
    if H > 2:
        return True  # out of scope (not low-cost); not a failure
    if H == 0:
        return True
    # replay effective word on both, compare depths/costs/steps
    LA = []
    tA = A
    for (m, x) in eff:
        d = depth(tA, x)
        tA, evs = S.trace(tA, x)
        LA.append((d, (d + 1) // 2 if d is not None else None, tuple(e[0] for e in evs)))
    LS = []
    tS = As
    for (m, x) in eff:
        d = depth(tS, x)
        # x must exist in Astar (retained targets)
        if d is None:
            note(tag, ("target-lost", x))
            return False
        tS, evs = S.trace(tS, x)
        LS.append((d, (d + 1) // 2, tuple(e[0] for e in evs)))
    # L3/L4: depths + step types agree
    if [l[:2] for l in LA] != [l[:2] for l in LS]:
        note(tag, ("L3-depths", LA, LS))
        ok = False
    if [l[2] for l in LA] != [l[2] for l in LS]:
        note(tag, ("L4-steps", LA, LS))
        ok = False
    # L5: final top-3 nodes were initially within depth 6 in both
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
    d0A = {}
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
    # L6: shadows agree (initial was smoke-checked; final here) + root + inventory
    if shadow(tA, Sset) != shadow(tS, Sset):
        note(tag, ("L6-final-shadow",))
        ok = False
    # root agreement (terminal target at root both)
    vt = eff[-1][1]
    if tA[0] == "leaf" or tA[1] != vt or tS[0] == "leaf" or tS[1] != vt:
        note(tag, ("root", vt))
        ok = False
    # L7: saturated signatures agree (compute gap counts both universes)
    gA = gaps_of(Sset, keys_of(tA) | Sset)
    gS = gaps_of(Sset, keys_of(tS) | Sset)
    sA = tuple(min(len(g), T_CAP) for g in gA)
    sS = tuple(min(len(g), T_CAP) for g in gS)
    if sA != sS:
        note(tag, ("L7-signature", sA, sS))
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
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    for trial in range(N):
        rng = random.Random(1000 + trial)
        mode = trial % 6
        if mode == 0:
            n = rng.randint(9, 20)
            keys = list(range(1, n + 1))
            A = rand_tree(rng, keys)
            Sset = set(rng.sample(keys, 9))
        elif mode == 1:  # G: frontier multiplicity in one gap
            keys = list(range(1, 60))
            A = rand_tree(rng, keys)
            Sset = set(rng.sample(keys, 9))
        elif mode == 2:  # H: vine (S possibly deep) + combs
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
        elif mode == 3:  # I: saturation gaps
            base = list(range(1, 40))
            big = list(range(1000, 1000 + rng.choice([264, 265, 266, 267, 600])))
            keys = base + big
            A = rand_tree(rng, keys)
            Sset = set(rng.sample(base, 9))
        elif mode == 4:  # J: two-access patterns over depths
            keys = list(range(1, 15))
            A = rand_tree(rng, keys)
            Sset = set(rng.sample(keys, 9))
        else:
            keys = list(range(1, 12))
            A = rand_tree(rng, keys)
            Sset = set(rng.sample(keys, 9))
        U = set(keys)
        # effective words H<=2: 1-3 accesses ending KEEP, targets with a<=2
        cands = [(m, x) for m in ("D", "K") for x in keys if depth(A, x) is not None and (depth(A, x) + 1) // 2 <= 2]
        if not cands:
            continue
        for _ in range(6):
            ln = rng.choice([1, 2, 3])
            eff = []
            for i in range(ln):
                if i == ln - 1:
                    eff.append(("K", rng.choice(keys)))
                else:
                    eff.append(rng.choice([c for c in cands if c[0] == "D"] or [("D", rng.choice(keys))]))
            H = sum((depth(A, x) + 1) // 2 for _, x in eff)
            if H > 2 or H == 0:
                continue
            run_case("m%dt%d" % (mode, trial), A, Sset, U, eff)
    print("tests=%d mismatches=%d" % (res["tests"], len(res["mismatch"])), flush=True)
    json.dump(res, open(PDIR + "UFRL_FUZZ.json", "w"), indent=1, default=str)
    sys.exit(0 if not res["mismatch"] else 1)

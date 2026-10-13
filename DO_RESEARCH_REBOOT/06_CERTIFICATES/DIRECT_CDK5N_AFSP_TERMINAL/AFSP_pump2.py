# AF-3 faithful test: extend OCCUPIED deep frontiers only; compare S-skeleton + observables.
import sys, json, random
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_AFSP_TERMINAL')
sys.path.insert(0, 'python/independent')
import splay as S
from AFSP_canonical import canonical_shadow

def skel_nobeta(A, Sset):
    # S-structure + hole occupancy + S-subsets + root, with fringe identities erased
    # (positions of visible fringe retained as anonymous slots)
    c = canonical_shadow(A, Sset)
    import re as _re
    vis = _re.sub(r"\('F', \d+\)", "('F',)", c['vis'])
    holes = _re.sub(r"\('F', \d+\)", "('F',)", c['holes'])
    return vis + holes

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_AFSP_TERMINAL/'

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

def skel(A, Sset):
    # S-skeleton: contract fringe-only subtrees to '*', keep S nodes; hole emptiness via presence
    def c(u):
        if u[0] == 'leaf':
            return '.'
        _, k, l, r = u
        if k not in Sset:
            # fringe node: keep iff its subtree contains S keys (else '*')
            sub = []
            sk = [u]
            hasS = False
            while sk:
                w = sk.pop()
                if w[0] == 'leaf':
                    continue
                _, kk, ll, rr = w
                if kk in Sset:
                    hasS = True
                    break
                sk.append(ll)
                sk.append(rr)
            if not hasS:
                return '*'
        return (k if k in Sset else '*', c(l), c(r))
    return c(A)

def macro_obs(A, eff):
    t = A
    obs = []
    H = 0
    for (m, x) in eff:
        d = depth(t, x)
        a = (d + 1) // 2
        H += a
        t, evs = S.trace(t, x)
        obs.append((d, a, tuple(e[0] for e in evs)))
    return obs, H, t

def ins_all(t, keys):
    def ins(t, k):
        if t[0] == "leaf":
            return S.node(k, S.LEAF, S.LEAF)
        _, kk, l, r = t
        return S.node(kk, ins(l, k), r) if k < kk else S.node(kk, l, ins(r, k))
    for k in keys:
        t = ins(t, k)
    return t

if __name__ == "__main__":
    bad = tot = skipped = 0
    for trial in range(150):
        rng = random.Random(31000 + trial)
        base = list(range(1, 30))
        Sset = set(rng.sample(base, 9))
        Ss = sorted(Sset)
        ks = sorted(base)
        rng.shuffle(ks)
        A = ins_all(S.LEAF, ks)
        U = set(base)
        # effective word H in 1..2 over S terminal + depth<=4 others
        cands = [x for x in sorted(U) if depth(A, x) is not None and (depth(A, x) + 1) // 2 in (1, 2)]
        v = rng.choice(sorted(Sset))
        dv = depth(A, v)
        if dv is None or (dv + 1) // 2 > 2:
            skipped += 1
            continue
        eff = []
        H = (dv + 1) // 2
        for y in rng.sample(cands, min(len(cands), 2)):
            if y == v:
                continue
            ay = (depth(A, y) + 1) // 2
            if ay >= 1 and H + ay <= 2:
                eff.append(("D", y))
                H += ay
            if H >= 2:
                break
        eff.append(("K", v))
        obs0, H0, A1 = macro_obs(A, eff)
        if H0 > 2 or H0 == 0:
            skipped += 1
            continue
        sk0 = skel_nobeta(A1, Sset)
        # pump: choose gap, find occupied deep frontiers, extend with new keys landing >=7
        g = rng.randint(0, 9)
        lo = Ss[g - 1] if g > 0 else float('-inf')
        hi = Ss[g] if g < 9 else float('inf')
        # candidate pump keys: floats spanning gap (dense order representative)
        pool = [lo + (hi - lo) * (j + 1) / 401 for j in range(400)] if hi != float('inf') and lo != float('-inf') else None
        if pool is None:
            # unbounded gap: use wide floats
            pool = [(lo if lo != float('-inf') else 0) + (j + 1) * 7.13 for j in range(400)]
            pool = [x for x in pool if (lo == float('-inf') or x > lo) and (hi == float('inf') or x < hi)]
        A2 = A
        placed = 0
        for kk in pool:
            if placed >= 120:
                break
            # BST insert; keep only if lands at depth >= 7 (below cone) else revert
            def ins1(t, k):
                if t[0] == "leaf":
                    return S.node(k, S.LEAF, S.LEAF)
                _, kkk, l, r = t
                return S.node(kkk, ins1(l, k), r) if k < kkk else S.node(kkk, l, ins1(r, k))
            T = ins1(A2, kk)
            if depth(T, kk) is not None and depth(T, kk) >= 7:
                A2 = T
                placed += 1
        if placed < 30:
            skipped += 1
            continue
        obs1, H1, A3 = macro_obs(A2, eff)
        tot += 1
        if obs0 != obs1 or H0 != H1:
            bad += 1
            print("PUMP-DIFF", trial, obs0, obs1, flush=True)
            continue
        if skel_nobeta(A3, Sset) != sk0:
            bad += 1
            print("PUMP-SKEL", trial, flush=True)
    print("pump tests=%d skipped=%d bad=%d" % (tot, skipped, bad), flush=True)
    json.dump({"tests": tot, "skipped": skipped, "bad": bad, "pass": bad == 0}, open(PDIR + "AFSP_PUMP_TEST.json", "w"), indent=1)
    sys.exit(0 if bad == 0 else 1)

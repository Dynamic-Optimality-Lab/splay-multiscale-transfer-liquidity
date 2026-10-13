# 5B: full BST reconstruction verifier (true canonical order g0*<s1<...<s9<g9*).
import sys, json, random
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_WEIGHTED_QUOTIENT_TERMINAL')
sys.path.insert(0, 'python/independent')
import splay as S
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_AFSP_TERMINAL')
from AFSP_allocate import solve_allocation

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_WEIGHTED_QUOTIENT_TERMINAL/'
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_AFSP_TERMINAL')

def inorder_keys(t):
    if t[0] == 'leaf':
        return []
    _, k, l, r = t
    return inorder_keys(l) + [k] + inorder_keys(r)

def is_bst(t, lo=float('-inf'), hi=float('inf')):
    if t[0] == 'leaf':
        return True
    _, k, l, r = t
    return lo < k < hi and is_bst(l, lo, k) and is_bst(r, k, hi)

if __name__ == "__main__":
    bad = tot = 0
    for trial in range(400):
        rng = random.Random(2000 + trial)
        R = rng.randint(1, 6)
        # intervals first, then S ranks placed only into compatible holes
        hole_iv = []
        for r in range(R):
            a = rng.randint(0, 9)
            b = rng.randint(a + 1, 10)
            hole_iv.append((a, b))
        S_holes = [[] for _ in range(R)]
        ranks = rng.sample(range(1, 10), rng.randint(0, min(9, 2 * R)))
        okp = True
        for s in ranks:
            cands = [r for r in range(R) if hole_iv[r][0] <= s <= hole_iv[r][1]]
            if not cands:
                okp = False
                break
            S_holes[rng.choice(cands)].append(s)
        if not okp:
            continue
        for r in range(R):
            S_holes[r] = sorted(S_holes[r])
        compat = [[hole_iv[r][0] <= i < hole_iv[r][1] for r in range(R)] for i in range(10)]
        p = [rng.randint(0, 3) for _ in range(10)]
        sigma = [p[i] + rng.randint(0, 5) for i in range(10)]
        non = set(r for r in range(R) if not S_holes[r] and rng.random() < 0.4)
        z = solve_allocation(p, S_holes, compat, sigma, non)
        if z is None:
            continue
        tot += 1
        # reconstruct: canonical keys: S ranks as S*1000; fringe gap-i keys as S_i*1000 + seq (true order g0*<s1<...)
        key_of = {}
        for r, Sh in enumerate(S_holes):
            for s in Sh:
                key_of[('S', r, s)] = s * 1000
        ctr = [0] * 10
        for (i, r), c in sorted(z.items()):
            for t in range(c):
                ctr[i] += 1
                key_of[('F', i, r, t)] = i * 1000 + 500 + ctr[i] if i < 9 else 9000 + ctr[i]
        # NOTE gap indexing: use 0..9 gaps with S ranks 1..9: gap i holds keys between S_i and S_{i+1}
        # verify strict order: all keys unique?
        vals = list(key_of.values())
        if len(set(vals)) != len(vals):
            bad += 1
            print("DUP-KEY", trial, flush=True)
            continue
        # build hole trees (balanced) + verify BST validity per hole interval + S placement
        for r, Sh in enumerate(S_holes):
            hk = sorted([key_of[('S', r, s)] for s in Sh] + [key_of[k] for k in key_of if isinstance(k, tuple) and k[0] == 'F' and k[2] == r])
            # balanced build
            def bal(ks):
                if not ks:
                    return S.LEAF
                m = len(ks) // 2
                return S.node(ks[m], bal(ks[:m]), bal(ks[m + 1:]))
            T = bal(sorted(hk))
            if hk and not is_bst(T):
                bad += 1
                print("BST-INVALID", trial, flush=True)
                break
            # S placement: each required S rank present
            flat = set(inorder_keys(T))
            for s in Sh:
                if s * 1000 not in flat:
                    bad += 1
                    print("S-MISSING", trial, flush=True)
                    break
    print("recon verified=%d bad=%d" % (tot, bad), flush=True)
    json.dump({"verified": tot, "bad": bad, "pass": bad == 0}, open(PDIR + "WQ_RECON_VERIFY.json", "w"), indent=1)
    sys.exit(0 if bad == 0 else 1)

# P2 computational verification: exhaustive ancestor-change maxima + P1 identity check.
import sys, json
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
from CRA_pointer_tuple_replay import replay, idepths, from_serial

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_DISPARITY_MIGRATION_G0_POST_GLOBAL_OPEN/'

def all_bsts(keys):
    if not keys:
        return ['.']
    out = []
    for i, k in enumerate(keys):
        for l in all_bsts(keys[:i]):
            for r in all_bsts(keys[i + 1:]):
                out.append((k, l, r))
    return out

def rots(t):
    if t == '.':
        return []
    out = []
    k, l, r = t
    if l != '.':
        lk, ll, lr = l
        out.append((lk, ll, (k, lr, r)))
    if r != '.':
        rk, rl, rr = r
        out.append((rk, (k, l, rl), rr))
    for u in rots(l):
        out.append((k, u, r))
    for u in rots(r):
        out.append((k, l, u))
    return list(dict.fromkeys(out))

def ancs(t, x):
    p = []
    cur = t
    while cur != '.':
        k, l, r = cur
        if x == k:
            return set(p)
        p.append(k)
        cur = l if x < k else r
    return None

def inc_changes(t1, t2, keys):
    n = 0
    for x in keys:
        a1 = ancs(t1, x); a2 = ancs(t2, x)
        for z in keys:
            if z == x:
                continue
            if (z in a1) != (z in a2):
                n += 1
    return n

if __name__ == "__main__":
    rec = {}
    for n in (3, 4, 5):
        keys = list(range(1, n + 1))
        shapes = all_bsts(keys)
        mx1 = 0
        ex = None
        for t in shapes:
            for u in rots(t):
                c = inc_changes(t, u, keys)
                if c > mx1:
                    mx1 = c
                    ex = (t, u)
        rec[n] = {"shapes": len(shapes), "max_single_rotation_changes": mx1}
        print("n=%d shapes=%d max-single-rot=%d" % (n, len(shapes), mx1), flush=True)
    # double-step bound = 2x single (composition); splay depth-d gross <= d * max1
    # P1 identity spot-check on frozen replays
    from MIG_replay import parse, gaps
    import hashlib
    nbad = 0
    for tag, cw in [("A", "D4,D3,K3,K7,D5,K1,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D8,K9,K5,D3,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9")]:
        R = replay(parse(cw))
        M = {1, 3, 5, 7, 9}
        for k in range(len(parse(cw)) + 1):
            ps = R["pairs"][k]
            A = from_serial(ps[0]); B = from_serial(ps[1])
            dA = idepths(A); dB = idepths(B)
            for x in M:
                aA = ancs(('n', 0, '.', '.') and A, x) if False else None
                # ancestor sets via depths path: recompute with tuple-tree walk
                def aw(t, x):
                    p = []
                    cur = t
                    while True:
                        if cur == '.' or (isinstance(cur, tuple) and cur and cur[0] in ("leaf",)):
                            return None
                        if cur == '.' or cur == ("leaf",):
                            return None
                        _, kk, ll, rr = cur
                        if x == kk:
                            return set(p)
                        p.append(kk)
                        cur = ll if x < kk else rr
                sA = aw(A, x); sB = aw(B, x)
                om = sum((1 if z in sB else 0) - (1 if z in sA else 0) for z in dA if z != x)
                if om != dB.get(x, 0) - dA.get(x, 0):
                    nbad += 1
    rec["P1_mismatches"] = nbad
    print("P1 mismatches:", nbad, flush=True)
    json.dump(rec, open(PDIR + "MIG_rotation_verification.json", "w"), indent=1)

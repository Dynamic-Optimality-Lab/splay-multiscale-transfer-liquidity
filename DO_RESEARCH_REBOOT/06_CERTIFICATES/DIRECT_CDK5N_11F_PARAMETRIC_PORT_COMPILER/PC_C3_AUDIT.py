# PC_C3_AUDIT.py — corrected primitive-rotation accounting (C3).
# Primitive rotations per access = access depth d (zig-zig/zag = 2 rotations, zig = 1).
# Macro total <= 2H <= 4. Displacement <= 1/primitive (<=4/macro). Ports (>=7) stay >=3.
import sys, random
sys.path.insert(0, 'python/independent')
import splay as S

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER/'


def prim_count(frames):
    n = 0
    fr = list(frames)
    while fr:
        if len(fr) >= 2 and fr[-1][0] == fr[-2][0]:
            n += 2  # zig-zig / zig-zag = TWO primitive rotations
            fr = fr[:-2]
        else:
            n += 1  # zig = one
            fr = fr[:-1]
    return n


def depths(t):
    out = {}
    def go(s, d):
        if s[0] == 'leaf':
            return
        _, k, l, r = s
        out[k] = d
        go(l, d + 1)
        go(r, d + 1)
    go(t, 0)
    return out


if __name__ == '__main__':
    import json
    rng = random.Random(61)
    N = 3000
    maxprim = 0
    maxdisp = 0
    cases = {'LL': 0, 'RR': 0, 'LR': 0, 'RL': 0, 'ZIG': 0}
    for trial in range(N):
        n = rng.randint(10, 40)
        ks = list(range(1, n + 1))
        t = S.LEAF
        ins = sorted(ks)
        rng.shuffle(ins)
        def _ins(t, k):
            return S.node(k, S.LEAF, S.LEAF) if t[0] == 'leaf' else (S.node(t[1], _ins(t[2], k), t[3]) if k < t[1] else S.node(t[1], t[2], _ins(t[3], k)))
        for k in ins:
            t = _ins(t, k)
        H, P, tg = 0, 0, t
        d0 = depths(t)
        word = []
        cand = list(ks)
        rng.shuffle(cand)
        for x in cand:
            d = S.lookup(tg, x)[1]
            a = (d + 1) // 2
            if H + a <= 2 and (a > 0 or len(word) < 3):
                word.append(x)
                H += a
                fr = S._descend(tg, x, [])[1]
                P += prim_count(fr)
                assert prim_count(fr) == d, ('prim==depth', trial, x)  # C3 identity
                tg = S.trace(tg, x)[0]
                if H == 2 and rng.random() < 0.7:
                    break
        assert P <= 2 * H <= 4, ('macro-prim-bound', trial, P, H)
        maxprim = max(maxprim, P)
        d1 = depths(tg)
        disp = max(abs(d1[k] - d0[k]) for k in ks)
        assert disp <= P, ('disp<=prim', trial)
        maxdisp = max(maxdisp, disp)
        # port-depth invariant: nodes starting >=7 end >= 7-P >= 3
        for k in ks:
            if d0[k] >= 7:
                assert d1[k] >= 7 - P >= 3, ('port-depth', trial, k)
        # case census via source events not exposed; recount shapes from frames
    print('C3: trials=%d maxprim=%d (bound 4) maxdisp=%d prim==depth exact; ports>=3 holds' % (N, maxprim, maxdisp), flush=True)
    json.dump({'trials': N, 'maxprim': maxprim, 'maxdisp': maxdisp, 'bound': 4}, open(PDIR + 'PC_C3_AUDIT.json', 'w'), indent=1)

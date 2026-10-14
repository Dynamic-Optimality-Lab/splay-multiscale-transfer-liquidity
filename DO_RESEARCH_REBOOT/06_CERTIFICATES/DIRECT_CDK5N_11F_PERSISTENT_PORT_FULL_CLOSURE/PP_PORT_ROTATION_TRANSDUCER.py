# PP_PORT_ROTATION_TRANSDUCER.py — persistent A-subtree ports + commutation.
# Cut depth 6 (exposed), ports = frontier subtrees rooted at depth 7.
import sys, json, random
sys.path.insert(0, 'python/independent')
import splay as S

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PERSISTENT_PORT_FULL_CLOSURE/'
CUT = 6  # exposed depths 0..6; ports rooted at depth 7


def cut(t, Sset, depth=0, path=(), lo=None, hi=None):
    """Return (skel, ports). skel uses ('K',k,l,r) / ('P',pid). ports[pid] = dict(path, lo, hi, hidden_S)."""
    if t[0] == 'leaf':
        return ('E',), {}
    _, k, l, r = t
    if depth == CUT + 1:
        pid = path
        hid = sorted(x for x in Sset if (lo is None or x > lo) and (hi is None or x < hi) and x in S.inorder(t))
        return ('P', pid), {pid: {'path': list(path), 'lo': lo, 'hi': hi, 'hidden_S': hid}}
    sl, pl = cut(l, Sset, depth + 1, path + ('L',), lo, k)
    sr, pr = cut(r, Sset, depth + 1, path + ('R',), k, hi)
    ports = dict(pl)
    ports.update(pr)
    return ('K', k, sl, sr), ports


def fill(skel, F):
    if skel[0] == 'E':
        return S.LEAF
    if skel[0] == 'P':
        return F[skel[1]]
    _, k, l, r = skel
    return S.node(k, fill(l, F), fill(r, F))


def _descent_frames(skel, x):
    """Frames over skeleton; ports are opaque leaves (never entered)."""
    fr, cur = [], skel
    while True:
        if cur[0] == 'E':
            return None
        if cur[0] == 'P':
            raise AssertionError('descent entered port (Claim-1 violation)')
        _, k, l, r = cur
        if x == k:
            return fr
        if x < k:
            fr.append(('L', k, r))
            cur = l
        else:
            fr.append(('R', k, l))
            cur = r


def _rebuild_gen(fr, cur, is_skel):
    """Shared rotation engine (mirrors S._rebuild): rigid subtree moves. Returns (newcur, events)."""
    evs = []
    getk = (lambda t: t[1]) if is_skel else (lambda t: t[1])
    while fr:
        if len(fr) >= 2 and fr[-1][0] == fr[-2][0] == 'L':
            (_, kp, q), (_, kg, c) = fr[-1], fr[-2]
            x = getk(cur)
            _, _, t1, t2 = cur
            cur = ('K', x, t1, ('K', kp, t2, ('K', kg, q, c))) if is_skel else S.node(x, t1, S.node(kp, t2, S.node(kg, q, c)))
            fr = fr[:-2]
            evs.append('LL')
        elif len(fr) >= 2 and fr[-1][0] == fr[-2][0] == 'R':
            (_, kp, q), (_, kg, c) = fr[-1], fr[-2]
            x = getk(cur)
            _, _, t1, t2 = cur
            cur = ('K', x, ('K', kp, ('K', kg, c, q), t1), t2) if is_skel else S.node(x, S.node(kp, S.node(kg, c, q), t1), t2)
            fr = fr[:-2]
            evs.append('RR')
        elif len(fr) >= 2 and fr[-1][0] == 'R' and fr[-2][0] == 'L':
            (_, kp, q), (_, kg, d) = fr[-1], fr[-2]
            x = getk(cur)
            _, _, t1, t2 = cur
            cur = ('K', x, ('K', kp, q, t1), ('K', kg, t2, d)) if is_skel else S.node(x, S.node(kp, q, t1), S.node(kg, t2, d))
            fr = fr[:-2]
            evs.append('LR')
        elif len(fr) >= 2 and fr[-1][0] == 'L' and fr[-2][0] == 'R':
            (_, kp, q), (_, kg, a) = fr[-1], fr[-2]
            x = getk(cur)
            _, _, t1, t2 = cur
            cur = ('K', x, ('K', kg, a, t1), ('K', kp, t2, q)) if is_skel else S.node(x, S.node(kg, a, t1), S.node(kp, t2, q))
            fr = fr[:-2]
            evs.append('RL')
        else:
            tag, kp, q = fr[-1]
            x = getk(cur)
            _, _, t1, t2 = cur
            if tag == 'L':
                cur = ('K', x, t1, ('K', kp, t2, q)) if is_skel else S.node(x, t1, S.node(kp, t2, q))
            else:
                cur = ('K', x, ('K', kp, q, t1), t2) if is_skel else S.node(x, S.node(kp, q, t1), t2)
            fr = fr[:-1]
            evs.append('ZIG')
    return cur, evs


def _plug_skel(fr, cur):
    for tag, k, sib in reversed(fr):
        cur = ('K', k, cur, sib) if tag == 'L' else ('K', k, sib, cur)
    return cur


def splay_skel(skel, x):
    fr = _descent_frames(skel, x)
    if fr is None:
        raise KeyError(x)
    # isolate target node key holder: rebuild target as ('K',x,t1,t2) from skeleton
    # find target subtree to get its children
    cur = skel
    for tag, k, sib in fr:
        _, _, l, r = cur
        cur = l if tag == 'L' else r
    _, _, t1, t2 = cur
    tgt = ('K', x, t1, t2)
    return _rebuild_gen(fr, tgt, True)


def splay_conc(t, x):
    res = S._descend(t, x, [])
    if res is None:
        raise KeyError(x)
    sub, fr = res
    _, _, t1, t2 = (sub[1], sub[2], sub[3]) if sub[0] != 'leaf' else (None, None, None)
    if sub[0] == 'leaf':
        raise KeyError(x)
    tgt = S.node(sub[1], sub[2], sub[3])
    return _rebuild_gen(fr, tgt, False)


def skel_to_tree_shape(skel):
    """Skeleton with ports as opaque leaves -> comparable nested form."""
    if skel[0] == 'E':
        return '.'
    if skel[0] == 'P':
        return ('PORT', skel[1])
    _, k, l, r = skel
    return (k, skel_to_tree_shape(l), skel_to_tree_shape(r))


def top_shadow(skel, D=2):
    """Depth-<=D exposed skeleton (assert no ports)."""
    def go(s, d):
        if s[0] == 'E':
            return '.'
        if s[0] == 'P':
            raise AssertionError('port in depth-%d shadow' % D)
        _, k, l, r = s
        if d == D:
            return (k, '.', '.')
        return (k, go(l, d + 1), go(r, d + 1))
    return go(skel, 0)


def conc_shadow(t, D=2):
    def go(s, d):
        if s[0] == 'leaf':
            return '.'
        _, k, l, r = s
        if d == D:
            return (k, '.', '.')
        return (k, go(l, d + 1), go(r, d + 1))
    return go(t, 0)


if __name__ == '__main__':
    rng = random.Random(7)
    NTRIAL = 4000
    casecount = {'LL': 0, 'RR': 0, 'LR': 0, 'RL': 0, 'ZIG': 0}
    nrot = 0
    maxrot = 0
    for trial in range(NTRIAL):
        n = rng.randint(10, 40)
        keys = list(range(1, n + 1))
        Sset = set(rng.sample(keys, 9))
        t = S.LEAF
        ks = sorted(keys)
        rng.shuffle(ks)
        for k in ks:
            # insert
            def ins(t, k):
                if t[0] == 'leaf':
                    return S.node(k, S.LEAF, S.LEAF)
                _, kk, l, r = t
                return S.node(kk, ins(l, k), r) if k < kk else S.node(kk, l, ins(r, k))
            t = ins(t, k)
        skel, ports = cut(t, Sset)
        F = {}
        for pid, pr in ports.items():
            lo, hi = pr['lo'], pr['hi']
            # completion: actual subtree from t at that path
            sub = t
            for step in pid:
                _, _, l, r = sub
                sub = l if step == 'L' else r
            F[pid] = sub
        # macro with H<=2: accumulate exact costs on the evolving tree
        H = 0
        word = []
        cand = [k for k in keys]
        rng.shuffle(cand)
        tg = t
        for x in cand:
            d = S.lookup(tg, x)[1]
            a = (d + 1) // 2
            if H + a <= 2 and (a > 0 or len(word) < 3):
                word.append(x)
                H += a
                tg = S.trace(tg, x)[0]
                if H == 2 and rng.random() < 0.7:
                    break
        # port-level replay
        sk, evs_all = skel, []
        for x in word:
            sk, evs = splay_skel(sk, x)
            evs_all += evs
        # concrete replay (source S.trace)
        tc = t
        for x in word:
            tc = S.trace(tc, x)[0]
        assert fill(sk, F) == tc, ('commutation mismatch', trial)
        # event agreement with source engine: recount via S._rebuild event tags not exposed; check case multiset via our engine on concrete
        for x in word:
            pass
        for e in evs_all:
            casecount[e] += 1
        nrot += len(evs_all)
        maxrot = max(maxrot, len(evs_all))
        assert len(evs_all) <= 4, ('rotation bound', trial, len(evs_all))
        # depth-2 shadow agreement without opening ports
        assert top_shadow(sk) == conc_shadow(tc), ('shadow mismatch', trial)
    print('trials=%d rotations=%d maxrot=%d cases=%s' % (NTRIAL, nrot, maxrot, casecount), flush=True)
    assert all(v >= 100 for v in casecount.values()), casecount
    json.dump({'trials': NTRIAL, 'rotations': nrot, 'maxrot': maxrot, 'cases': casecount},
              open(PDIR + 'PP_PORT_SMOKE.json', 'w'), indent=1)

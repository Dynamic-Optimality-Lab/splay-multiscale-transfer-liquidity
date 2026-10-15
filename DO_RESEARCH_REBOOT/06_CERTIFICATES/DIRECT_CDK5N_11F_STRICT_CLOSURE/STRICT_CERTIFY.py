# STRICT_CERTIFY.py — grounded certification vs the REPAIRED relation (tags SL, alpha-7).
# Caller pre-segments words at genuine KEEPs (A8 discipline); single macro in, terminal genuine.
import sys
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE')
import splay as S
from CRA_pointer_tuple_replay import replay, from_serial
from PC_CONCRETIZE import (AModel, BModel, depths_keys, gap_of, build_envA, build_envB,
                           build_envBT, build_envW, build_envI, shadow_of, serial)


def alpha7_of(T, Sset, Ss):
    """7-position abstract shadow + canonical beta. Positions: root,L,R,LL,LR,RL,RR."""
    if T[0] == 'leaf':
        return None
    _, k, l, r = T
    kids = {'root': (2, None), 'L': (2, None), 'R': (2, None),
            'LL': (2, None), 'LR': (2, None), 'RL': (2, None), 'RR': (2, None)}
    def sub(s, pos):
        if s[0] == 'leaf':
            kids[pos] = (2, None)
            return
        _, kk, ll, rr = s
        kids[pos] = (0, kk)
        if pos == 'L':
            sub(ll, 'LL')
            sub(rr, 'LR')
        elif pos == 'R':
            sub(ll, 'RL')
            sub(rr, 'RR')
    kids['root'] = (0, k)
    sub(l, 'L')
    sub(r, 'R')
    order = ['root', 'L', 'R', 'LL', 'LR', 'RL', 'RR']
    ino = ['LL', 'L', 'LR', 'root', 'RL', 'R', 'RR']
    beta = {}
    n = 0
    for p in ino:
        kk, key = kids[p]
        if kk == 0 and key not in Sset:
            n += 1
            beta[p] = n
        else:
            beta[p] = 0
    out = {}
    for p in order:
        kk, key = kids[p]
        if kk == 2:
            out[p] = (2, 0, 0)
        elif key in Sset:
            out[p] = (0, 1, Ss.index(key))
        else:
            out[p] = (0, 0, 0)
    return out


def ssertify(d, L, A0l, B0l, Sset, M, word, H, tag='SL', force_mid=False):
    Ss = sorted(Sset)
    try:
        R = replay(word, A0=A0l, B0=B0l)
    except Exception:
        return ('skip', 'replay-exc')
    if not R['agree']:
        return ('skip', 'disagree')
    term = R['legs'][-1]
    if not (term['m'] == 'K' and term['chg'] and term['x'] in M):
        return ('skip', 'nongen-term')
    # A8 discipline: no intermediate genuine (marked + B-changing) KEEPs (unless force_mid test mode)
    for l in R['legs'][:-1]:
        if l['m'] == 'K' and l['x'] in M and l['chg'] and not force_mid:
            return ('skip', 'mid-genuine')
    Hc = sum(l['a'] for l in R['legs'])
    if Hc != H or H > 2:
        return ('skip', 'Hmix')
    dBc = term['dB']
    qc = dBc // 2
    wc = 2 * Hc - qc
    # terminal all-core ancestors (exact-agreement class; counted openly)
    Rp = replay(word[:-1], A0=A0l, B0=B0l) if len(word) > 1 else None
    Bpre = from_serial((Rp if Rp else {'pairs': [R['pairs'][0]]})['pairs'][-1][1])
    tx = word[-1][1]
    dk = depths_keys(Bpre)
    a = dk[tx][1]
    while a is not None:
        if a not in Sset:
            return ('skip', 'fringe-anc')
        a = dk[a][1]
    dB = dk[tx][0]
    bm0 = BModel(Bpre, Sset)
    if not bm0.ok:
        return ('skip', 'nontree')
    skpath, skdirs = bm0.path_to_core(tx)
    if len(skpath) - 1 != dB:
        return ('skip', 'depthmix')
    q = dB // 2
    w = 2 * H - q
    A0 = from_serial(R['pairs'][0][0])
    am = AModel(A0, Sset)
    winfo = []
    binfo = []
    Acur = A0
    key2slot = {v['key']: sid for sid, v in am.slots.items()}
    for (md, x) in word:
        dd = S.lookup(Acur, x)[1]
        dkA = depths_keys(Acur)
        chain = [x]
        dirs = []
        cur = x
        while True:
            dd_cur, par, side = dkA[cur]
            if par is None:
                break
            dirs.append(side)
            cur = par
            chain.append(cur)
        try:
            pslots = [key2slot[kk] for kk in chain]
        except KeyError:
            return ('skip', 'apath')
        winfo.append({'isK': md == 'K', 'slot': pslots[0], 'd': dd, 'path': pslots, 'dirs': dirs})
        Acur = S.trace(Acur, x)[0]
    if len(winfo) != len(word):
        return ('skip', 'apath')
    Bcur = from_serial(R['pairs'][0][1])
    Btrees = [Bcur]
    bmodels = [BModel(Bcur, Sset)]
    battach = [gap_match(bmodels[0], Sset, gap_pops(Bcur, Sset), Bcur)]
    if battach[0] is None:
        return ('skip', 'gap-match')
    for (md, x) in word:
        bm = bmodels[-1]
        if not bm.ok:
            return ('skip', 'bev')
        if md == 'D':
            binfo.append({'T': 0, 'd': 0, 'path': [0], 'dirs': []})
            bmodels.append(bm)
            Btrees.append(Bcur)
            battach.append(battach[-1])
            continue
        if x in Sset:
            pth, drs = bm.path_to_core(x)
            Tt, dd = bm.sidx[x], len(pth) - 1
            if dd != S.lookup(Bcur, x)[1]:
                return ('skip', 'bev')
            pth = [bm.sidx[kk] for kk in pth]
        else:
            g = gap_of(Ss, x)
            att = battach[-1]
            if g not in att:
                return ('skip', 'gap-match')
            pk, side = att[g]
            cp, cd = bm.path_to_core(pk)
            pth = [9 + g] + [bm.sidx[kk] for kk in cp]
            drs = [side] + cd
            Tt, dd = 9 + g, len(pth) - 1
        binfo.append({'T': Tt, 'd': dd, 'path': pth, 'dirs': drs})
        Rw = replay([(md, x)], A0=serial(Acur), B0=serial(Bcur))
        Bcur = from_serial(Rw['pairs'][-1][1])
        bmodels.append(BModel(Bcur, Sset))
        Btrees.append(Bcur)
        battach.append(gap_match(bmodels[-1], Sset, gap_pops(Bcur, Sset), Bcur))
        if battach[-1] is None:
            return ('skip', 'gap-match')
    Ad = from_serial(R['pairs'][-1][0])
    Bd = from_serial(R['pairs'][-1][1])
    bmd = BModel(Bd, Sset)
    if not bmd.ok:
        return ('skip', 'dst-nontree')
    env = {}
    build_envA(env, am, Sset, tag + 'w')
    build_envI(env, am, Sset, tag + 'v')
    # hsrank for hidden claims
    for (s, b), hk in am.phS.items():
        for kk in hk:
            env[f'{tag}v_hsr{s}_{b}_{Ss.index(kk)}'] = am.V.index(kk)
    att_s = gap_match(bmodels[0], Sset, gap_pops(Btrees[0], Sset), Btrees[0])
    att_t = gap_match(bmd, Sset, gap_pops(Bd, Sset), Bd)
    if att_s is None or att_t is None:
        return ('skip', 'gap-match')
    build_envBT(env, binfo, tag + 'bt')
    build_envW(env, winfo, tag + 'w')
    env[tag + 'bt_q'] = q
    env[tag + '_H'] = H
    env[tag + '_w'] = w
    mu = sum(1 << Ss.index(m) for m in M)
    env[tag + 's_mu'] = mu
    env[tag + 't_mu'] = mu
    for (pre, Bm, att, vst) in ((tag + 's', bmodels[0], att_s, tag + 'sb0'), (tag + 't', bmd, att_t, tag + 'sb5')):
        build_envB_strict(env, Bm, Sset, pre + '_b', att, vst)
    # intermediate boundary structs (bs[1..4] <-> bmodels[1..4]; pad with last when short)
    while len(bmodels) < 6:
        bmodels.append(bmodels[-1])
        Btrees.append(Btrees[-1])
    nev_guess = len(word)
    for e in range(1, 5):
        att = gap_match(bmodels[e], Sset, gap_pops(Btrees[e], Sset), Btrees[e])
        if att is None:
            if e < nev_guess:
                return ('skip', 'gap-match')
            for i in range(19):
                env[f'{tag}sb{e}_bpar{i}'] = 19
                env[f'{tag}sb{e}_bdep{i}'] = 0
            continue
        build_envB_strict(env, bmodels[e], Sset, 'ZZ_topology_unused', att, tag + 'sb%d' % e)
    for pre, T in ((tag + 's', A0), (tag + 't', Ad)):
        a7 = alpha7_of(T, Sset, Ss)
        for p, key in enumerate(['root', 'L', 'R', 'LL', 'LR', 'RL', 'RR']):
            kk, isS, ii = a7[key]
            env[f'{pre}_ak{p}'] = kk
            env[f'{pre}_aS{p}'] = isS
            env[f'{pre}_aI{p}'] = ii
    for pre in (tag + 's', tag + 't'):
        am2 = am if pre == tag + 's' else AModel(Ad, Sset)
        for i in range(10):
            env[pre + f'_sg{i}'] = am2.sig[i]
    try:
        r = d.ev_iter(L['root'], env)
    except Exception as ex:
        return ('fail', {'reason': 'eval-exc', 'ex': repr(ex)[:200]})
    if r is not True:
        return ('fail', {'word': word, 'H': H, 'q': q, 'w': w, 'env': env})
    return ('ok', {'H': H, 'q': q, 'w': w, 'dB': dB, 'env': env})


def gap_pops(B, Sset):
    Ss = sorted(Sset)
    from PC_CONCRETIZE import gap_of
    import splay as _S
    p = [0] * 10
    for k in _S.inorder(B):
        if k not in Sset:
            p[gap_of(Ss, k)] += 1
    return p


def null_spans(B, Sset, bm):
    """Span-valid empty core NULLs in KEY space: (k,side) -> (loB,hiB) key bounds (None=inf).
    Only core NULLs with NO core child (skeleton-empty); fringe-occupied positions excluded."""
    import splay as _S
    sys.path.insert(0, 'python/independent')
    from PC_CONCRETIZE import depths_keys
    Ss = sorted(Sset)
    dk = depths_keys(B)
    ch = {}
    def go(s):
        if s[0] == 'leaf':
            return
        _, k, l, r = s
        ch[k] = (l[1] if l[0] != 'leaf' else None, r[1] if r[0] != 'leaf' else None)
        go(l)
        go(r)
    go(B)
    out = {}
    for k in Ss:
        i = bm.sidx[k]
        for side in (0, 1):
            e = bm.sk.get((i, side))
            if e is not None and e[0] == 'C':
                continue
            # empty core NULL: ancestor key bounds (strict BST insertion range)
            loB, hiB = (None, k) if side == 0 else (k, None)
            a = dk[k][1]
            cur = k
            while a is not None:
                side_a = 0 if ch[a][0] == cur else 1
                if side_a == 0:
                    hiB = a if hiB is None or a < hiB else hiB
                else:
                    loB = a if loB is None or a > loB else loB
                cur = a
                a = dk[a][1]
            out[(k, side)] = (loB, hiB)
    return out


def gap_match(bm, Sset, pops=None, B=None):
    """Distinct EMPTY-core-NULL assignment with exact key-span coverage. B required."""
    S = set(Sset)
    if B is None:
        return None
    spans = null_spans(B, Sset, bm)
    Ss = sorted(Sset)
    def covers(loB, hiB, g):
        lo = Ss[g - 1] if g > 0 else None
        hi = Ss[g] if g < 9 else None
        left_ok = (loB is None) or (hi is None) or (loB < hi)
        right_ok = (hiB is None) or (lo is None) or (lo < hiB)
        return left_ok and right_ok
    gs = [g for g in range(10) if pops is None or pops[g] > 0]
    used, out = set(), {}
    for g in sorted(gs, key=lambda g: sum(1 for (k, s) in spans if covers(spans[(k, s)][0], spans[(k, s)][1], g))):
        hit = None
        for (k, side) in sorted(spans):
            if (k, side) not in used and covers(spans[(k, side)][0], spans[(k, side)][1], g):
                hit = (k, side)
                break
        if hit is None:
            return None
        used.add(hit)
        out[g] = hit
    return out


def build_envB_strict(env, bm, Sset, vpre, attach, vpre_st=None):
    if vpre_st is None:
        vpre_st = vpre
    Ss = sorted(Sset)
    gap_at = {}
    for g, (k, side) in attach.items():
        gap_at[(bm.sidx[k], side)] = g
    for k in Ss:
        i = bm.sidx[k]
        for side in (0, 1):
            e = bm.sk.get((i, side))
            if e is not None and e[0] == 'C':
                env[f'{vpre}_bkl{i}' if side == 0 else f'{vpre}_bkr{i}'] = 0
                env[f'{vpre}_brl{i}' if side == 0 else f'{vpre}_brr{i}'] = e[1]
            elif (i, side) in gap_at:
                env[f'{vpre}_bkl{i}' if side == 0 else f'{vpre}_bkr{i}'] = 0
                env[f'{vpre}_brl{i}' if side == 0 else f'{vpre}_brr{i}'] = 9 + gap_at[(i, side)]
            else:
                env[f'{vpre}_bkl{i}' if side == 0 else f'{vpre}_bkr{i}'] = 2
                env[f'{vpre}_brl{i}' if side == 0 else f'{vpre}_brr{i}'] = 19
    for g in range(10):
        i = 9 + g
        env[f'{vpre}_bkl{i}'] = 2
        env[f'{vpre}_bkr{i}'] = 2
        env[f'{vpre}_brl{i}'] = 19
        env[f'{vpre}_brr{i}'] = 19
    rootS = next(k for k in Ss if bm.cpar[k] is None)
    env[f'{vpre}_broot'] = bm.sidx[rootS]
    ch = {}
    for k in Ss:
        i = bm.sidx[k]
        for side in (0, 1):
            e = bm.sk.get((i, side))
            if e is not None and e[0] == 'C':
                ch[(i, side)] = e[1]
            elif (i, side) in gap_at:
                ch[(i, side)] = 9 + gap_at[(i, side)]
            else:
                ch[(i, side)] = None
    blo = {bm.sidx[rootS]: 0}
    bhi = {bm.sidx[rootS]: 18}
    order = [bm.sidx[rootS]]
    seen = set()
    while order:
        i = order.pop(0)
        if i in seen:
            continue
        seen.add(i)
        r = 2 * i + 1 if i < 9 else 2 * (i - 9)
        for side in (0, 1):
            c = ch.get((i, side))
            if c is None:
                continue
            if side == 0:
                blo[c], bhi[c] = blo[i], r - 1
            else:
                blo[c], bhi[c] = r + 1, bhi[i]
            order.append(c)
    for i in range(19):
        if i >= 9 and i not in blo:
            blo[i], bhi[i] = 2 * (i - 9), 2 * (i - 9)
        env[f'{vpre}_blo{i}'] = blo[i]
        env[f'{vpre}_bhi{i}'] = bhi[i]
    par = {}
    for (i, side), c in ch.items():
        if c is not None:
            par[c] = i
    for i in range(19):
        env[f'{vpre_st}_bpar{i}'] = par.get(i, 19)
    dep = {bm.sidx[rootS]: 0}
    for i in range(19):
        if i == bm.sidx[rootS]:
            continue
        dd, cur = 0, i
        while cur in par:
            cur = par[cur]
            dd += 1
            if dd > 20:
                break
        dep[i] = dd
    for i in range(19):
        env[f'{vpre_st}_bdep{i}'] = dep.get(i, 0)
    return rootS

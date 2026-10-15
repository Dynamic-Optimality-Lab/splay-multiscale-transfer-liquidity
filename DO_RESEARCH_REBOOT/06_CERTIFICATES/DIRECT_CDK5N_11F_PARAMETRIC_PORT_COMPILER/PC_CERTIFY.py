# PC_CERTIFY.py — certify(d, L, A0l, B0l, Sset, M, word, H): full grounded certification.
# Returns ('ok', info) | ('skip', reason) | ('fail', info). Tags fixed to build tag 'PL'.
import sys
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
import splay as S
from CRA_pointer_tuple_replay import replay, from_serial
from PC_CONCRETIZE import (AModel, BModel, depths_keys, gap_of, build_envA, build_envB,
                           build_envBT, build_envW, build_envI, shadow_of, serial)


def certify(d, L, A0l, B0l, Sset, M, word, H, tag='PL'):
    Ss = sorted(Sset)
    try:
        R = replay(word, A0=A0l, B0=B0l)
    except Exception as ex:
        return ('skip', 'replay-exc')
    if not R['agree']:
        return ('skip', 'disagree')
    term = R['legs'][-1]
    if not term['chg']:
        return ('skip', 'nongenuine')
    Hc = sum(l['a'] for l in R['legs'])
    if Hc != H:
        return ('skip', 'Hmix')
    dBc = R['legs'][-1]['dB']
    qc = dBc // 2 if R['legs'][-1]['m'] == 'K' else 0
    wc = 2 * Hc - qc
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
    bmodels = [BModel(Bcur, Sset)]
    for (md, x) in word:
        bm = bmodels[-1]
        if not bm.ok:
            return ('skip', 'bev')
        if md == 'D':
            binfo.append({'T': 0, 'd': 0, 'path': [0], 'dirs': []})
            bmodels.append(bm)
            continue
        pth, drs = bm.path_to_core(x)
        if len(pth) - 1 != S.lookup(Bcur, x)[1]:
            return ('skip', 'bev')
        binfo.append({'T': bm.sidx[x], 'd': len(pth) - 1,
                      'path': [bm.sidx[kk] for kk in pth], 'dirs': drs})
        Rw = replay([(md, x)], A0=serial(Acur), B0=serial(Bcur))
        Bcur = from_serial(Rw['pairs'][-1][1])
        bmodels.append(BModel(Bcur, Sset))
    Ad = from_serial(R['pairs'][-1][0])
    Bd = from_serial(R['pairs'][-1][1])
    bmd = BModel(Bd, Sset)
    if not bmd.ok:
        return ('skip', 'dst-nontree')
    env = {}
    build_envA(env, am, Sset, tag + 'w')
    build_envI(env, am, Sset, tag + 'v')
    build_envB(env, bmodels[0], Sset, tag + '_b0')
    build_envBT(env, binfo, tag + 'bt')
    build_envW(env, winfo, tag + 'w')
    env[tag + 'bt_q'] = q
    env[tag + '_H'] = H
    env[tag + '_w'] = w
    mu = sum(1 << Ss.index(m) for m in M)
    env[tag + 's_mu'] = mu
    env[tag + 't_mu'] = mu
    for pre, Bm in ((tag + 's', bmodels[0]), (tag + 't', bmd)):
        build_envB(env, Bm, Sset, pre + '_b')
    for pre, T in ((tag + 's', A0), (tag + 't', Ad)):
        sh = shadow_of(T)
        rk, (lk, lr), (rk2, rr) = sh
        env[pre + '_arS'] = 1 if rk in Sset else 0
        env[pre + '_arI'] = Ss.index(rk) if rk in Sset else 0
        for kk, ref, cS, cI, cK in ((lk, lr, pre + '_aLS', pre + '_aLI', pre + '_aLk'),
                                    (rk2, rr, pre + '_aRS', pre + '_aRI', pre + '_aRk')):
            env[cK] = kk
            env[cS] = 1 if (ref is not None and ref in Sset) else 0
            env[cI] = Ss.index(ref) if (ref is not None and ref in Sset) else 0
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
    return ('ok', {'H': H, 'q': q, 'w': w, 'dB': dB, 'Hc': Hc, 'qc': qc, 'wc': wc, 'env': env,
                   'mu': mu, 'sig_s': [am.sig[i] for i in range(10)]})

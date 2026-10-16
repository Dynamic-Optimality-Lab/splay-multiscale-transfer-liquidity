# CW_HIGH_RUN.py — Gate F grounded: high fibers with witnessed q (C_M relabeled S).
import sys, json, random, copy
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE')
import splay as S
from CRA_pointer_tuple_replay import replay, from_serial
from CRA_segment_memberships import genuine_keys, keep_support
from PC_TYPED_DAG import DAG
from STRICT_HIGH_COMPILER import build_shigh
from STRICT_CERTIFY import gap_match, gap_pops, build_envB_strict, alpha7_of
from PC_CONCRETIZE import serial, depths_keys, AModel, BModel

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE/'
RDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_MSINK_G0_R1HARD/'


def CM_of(B, M):
    dk = depths_keys(B)
    out = set()
    for m in M:
        if m not in dk:
            return None
        a = m
        while a is not None:
            out.add(a)
            a = dk[a][1]
    return out


def parse(c):
    return [(t[0], int(t[1:])) for t in c.split(',')]


def iter_anc(dk, x):
    a = dk[x][1]
    while a is not None:
        yield a
        a = dk[a][1]


if __name__ == '__main__':
    d = DAG()
    Hh = build_shigh(d, 'SH')
    print('built strict-high: nodes=%d' % d.count(), flush=True)
    rows = []
    for seed in ('concat35', 'mr33'):
        for l in open(RDIR + 'state_' + seed + '/survivors.jsonl'):
            rows.append(json.loads(l))
    bycanon = {}
    for r in rows:
        bycanon.setdefault(r['canon'], []).append(r)
    WORDS = sorted(bycanon)[:40]
    nok = nskip = 0
    skips = {}
    fibers = set()
    for cw in WORDS:
        w = parse(cw)
        try:
            R = replay(w)
        except Exception:
            continue
        if not (R['S1'] == R['S0'] and R['agree']):
            continue
        G = set(genuine_keys(R['legs']))
        K = set(keep_support(R['legs']))
        if len(G) != 5 or K != G:
            continue
        first = None
        okc = True
        for ps in R['pairs']:
            c = CM_of(from_serial(ps[1]), G)
            if first is None:
                first = c
            if c != first:
                okc = False
                break
        if not okc or first is None or len(first) != 9:
            continue
        Sset = set(first)
        Ss = sorted(Sset)
        M = set(G)
        segs = []
        cur = []
        for acc, l in zip(w, R['legs']):
            cur.append(acc)
            if l['m'] == 'K' and l['x'] in M and l['chg']:
                segs.append(list(cur))
                cur = []
        idx = 0
        for seg in segs:
            A0ll = serial(from_serial(R['pairs'][idx][0]))
            B0ll = serial(from_serial(R['pairs'][idx][1]))
            idx += len(seg)
            seglegs = R['legs'][idx - len(seg):idx]
            H = sum(l['a'] for l in seglegs)
            if H < 3:
                continue
            # terminal genuine q from source B-depth (all-core automatic: paths in C_M)
            term = seglegs[-1]
            Bpre = from_serial(R['pairs'][idx - len(seg)][1])
            dk = depths_keys(Bpre)
            tx = term['x']
            if any(a not in Sset for a in iter_anc(dk, tx)):
                nskip += 1
                skips['fringe-path'] = skips.get('fringe-path', 0) + 1
                continue
            dB = dk[tx][0]
            q = dB // 2
            # fiber assignment
            Bd = from_serial(R['pairs'][idx][1])
            Ad = from_serial(R['pairs'][idx][0])
            A0 = from_serial(R['pairs'][idx - len(seg)][0])
            bmd = BModel(Bd, Sset)
            bm0 = BModel(Bpre, Sset)
            if not (bmd.ok and bm0.ok):
                nskip += 1
                skips['nontree'] = skips.get('nontree', 0) + 1
                continue
            att = gap_match(bmd, Sset, gap_pops(Bd, Sset), Bd)
            att0 = gap_match(bm0, Sset, gap_pops(Bpre, Sset), Bpre)
            if att is None or att0 is None:
                nskip += 1
                skips['gap-match'] = skips.get('gap-match', 0) + 1
                continue
            mu = sum(1 << Ss.index(m) for m in M)
            amd = AModel(Ad, Sset)
            am0 = AModel(A0, Sset)
            env = {}
            env['SHg_fmu'] = mu
            for i in range(10):
                env['SHg_fsg%i' % i] = amd.sig[i]
            build_envB_strict(env, bmd, Sset, 'SHt_b', att, 'SHt_b')
            # NOTE t.b vars are 'SHt_b_*'; fiber g.b vars 'SHg_fb_*': assign both from bmd
            build_envB_strict(env, bmd, Sset, 'SHg_fb', att, 'SHg_fb')
            env['SHg_fv'] = Ss.index(tx)
            # s state
            env['SHs_mu'] = mu
            build_envB_strict(env, bm0, Sset, 'SHs_b', att0, 'SHs_b')
            for pre, T, amx in (('SHs', A0, am0), ('SHt', Ad, amd)):
                a7 = alpha7_of(T, Sset, Ss)
                for p, key in enumerate(['root', 'L', 'R', 'LL', 'LR', 'RL', 'RR']):
                    kk, isS, ii = a7[key]
                    env[f'{pre}_ak{p}'] = kk
                    env[f'{pre}_aS{p}'] = isS
                    env[f'{pre}_aI{p}'] = ii
                for i in range(10):
                    env[f'{pre}_sg{i}'] = amx.sig[i]
            env['SHt_mu'] = mu
            # B-trace (terminal genuine): core path (all in C_M)
            pth, drs = bm0.path_to_core(tx)
            env['SHbt_bT0'] = bm0.sidx[tx]
            env['SHbt_bd0'] = len(pth) - 1
            for k in range(19):
                env[f'SHbt_bp0_{k}'] = bm0.sidx[pth[k]] if k < len(pth) else 0
            for k in range(18):
                env[f'SHbt_bdir0_{k}'] = drs[k] if k < len(drs) else 0
            for e in range(1, 5):
                env[f'SHbt_bT{e}'] = 0
                env[f'SHbt_bd{e}'] = 0
                for k in range(19):
                    env[f'SHbt_bp{e}_{k}'] = 0
                for k in range(18):
                    env[f'SHbt_bdir{e}_{k}'] = 0
            env['SH_q'] = q
            env['SH_w1'] = 6 - q
            # BStruct vars for s.b/t.b/g.b validity: assign par/dep via strict builder pieces
            for (vpre, Bm, atx) in (('SHs_b', bm0, att0), ('SHt_b', bmd, att), ('SHg_fb', bmd, att)):
                build_envB_strict(env, Bm, Sset, 'ZZ_topology_unused', atx,
                                  'SHsbs' if vpre == 'SHs_b' else ('SHsbt' if vpre == 'SHt_b' else 'SHsbg'))
            r = d.ev_iter(Hh['root'], env)
            assert r is True, ('high-grounded', seg, H, q)
            fibers.add((mu, tuple(amd.sig), tx))
            nok += 1
    print('high grounded: ok=%d skipped=%d fibers=%d skips=%s' % (nok, nskip, len(fibers), skips), flush=True)
    json.dump({'grounded': nok, 'skipped': nskip, 'skip_reasons': skips, 'fibers': len(fibers)},
              open(PDIR + 'CW_HIGH_EDGE_RESULTS.json', 'w'), indent=1)

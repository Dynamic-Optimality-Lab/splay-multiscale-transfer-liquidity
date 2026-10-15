# STRICT_ADVERSARIAL_TEST.py — every repair rejects invalid witnesses (A1/A2/A4/A7/A8).
import sys, json, random, copy
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE')
import splay as S
from CRA_pointer_tuple_replay import replay, from_serial
from PC_TYPED_DAG import DAG
from STRICT_LOW_COMPILER import build_slow
from STRICT_CERTIFY import ssertify, gap_match, gap_pops, build_envB_strict
from PC_CONCRETIZE import serial, AModel, BModel, depths_keys
from STRICT_SOURCE_REPAIRS import normalize_word

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE/'
res = {}


def base_edge(d, L):
    """One certified grounded edge + env (fringe-bearing 12-key universe, single KEEP)."""
    import random as _r
    rng = _r.Random(901)
    for trial in range(120):
        n = 20
        ks = list(range(1, n + 1))
        Sset = set(rng.sample(ks, 9))
        Ss = sorted(Sset)
        t = S.LEAF
        ins = sorted(ks)
        rng.shuffle(ins)
        def _ins(t, k):
            return S.node(k, S.LEAF, S.LEAF) if t[0] == 'leaf' else (S.node(t[1], _ins(t[2], k), t[3]) if k < t[1] else S.node(t[1], t[2], _ins(t[3], k)))
        for k in ins:
            t = _ins(t, k)
        from PC_CONCRETIZE import serial as _serial
        from STRICT_CERTIFY import ssertify as _ss
        T0 = _serial(t)
        M = set(rng.sample(Ss, 5))
        m0 = rng.choice(sorted(M))
        try:
            from CRA_pointer_tuple_replay import replay as _rp
            Rw = _rp([('K', m0)], A0=T0, B0=T0)
        except Exception:
            continue
        if not Rw['agree'] or not Rw['legs'][0]['chg']:
            continue
        from CRA_pointer_tuple_replay import from_serial as _fs
        tA = _fs(Rw['pairs'][-1][0])
        T1Al, T1Bl = _serial(tA), _serial(_fs(Rw['pairs'][-1][1]))
        # single S-target KEEP with H<=2
        for x in Ss:
            dd = S.lookup(tA, x)[1]
            a = (dd + 1) // 2
            if a > 2 or x not in M:
                continue
            st, info = _ss(d, L, T1Al, T1Bl, Sset, M, [('K', x)], a)
            if st == 'ok' and any(v > 0 for k, v in info['env'].items() if k.startswith('SLv_z')):
                return info['env'], info
    raise AssertionError('no fringe base edge found')


if __name__ == '__main__':
    d = DAG()
    L = build_slow(d, 'SL')
    env0, info0 = base_edge(d, L)
    assert d.ev_iter(L['root'], env0) is True
    print('base edge ok (H,q,w)=(%s,%s,%s)' % (info0['H'], info0['q'], info0['w']), flush=True)

    def tamp(ev, k, v):
        e = dict(ev)
        e[k] = v
        return e

    # A1: B-target changed to a different S key -> REJECT
    e = tamp(env0, 'SLbt_bT0', (env0['SLbt_bT0'] + 1) % 9)
    r = d.ev_iter(L['root'], e)
    res['A1-S-mismatch-reject'] = (r is False)
    print('A1 S-mismatch rejected:', r is False, flush=True)

    # A1: B-target to different gap (fringe case via gap id) -> REJECT (path/B-depth break too)
    e = tamp(env0, 'SLbt_bT0', 9 + 3)
    e = tamp(e, 'SLbt_bd0', 2)
    r = d.ev_iter(L['root'], e)
    res['A1-gap-mismatch-reject'] = (r is False)
    print('A1 gap-mismatch rejected:', r is False, flush=True)

    # A2: shortened A path (evd-1, path no longer root-terminated) -> REJECT
    e = dict(env0)
    dd = e['SLw_ed0']
    if dd >= 1:
        e = tamp(e, 'SLw_ed0', dd - 1)
        r = d.ev_iter(L['root'], e)
        res['A2-short-path-reject'] = (r is False)
        print('A2 shortened path rejected:', r is False, flush=True)
    else:
        res['A2-short-path-reject'] = 'n/a (dd=0)'

    # A2: duplicated path node -> REJECT
    e = dict(env0)
    e = tamp(e, 'SLw_ep0_1', e['SLw_ep0_0'])
    r = d.ev_iter(L['root'], e)
    res['A2-dup-node-reject'] = (r is False)
    print('A2 duplicated node rejected:', r is False, flush=True)

    # A4: duplicated B child (two parents claim one core node) -> REJECT
    e = dict(env0)
    # core-0 left ref := core-1 left ref target (duplicate claim on that node)
    e['SLs_b_brl0'] = e['SLs_b_brl1']
    r = d.ev_iter(L['root'], e)
    res['A4-dup-child'] = (r is False)
    print('A4 duplicated B child rejected:', r is False, flush=True)

    # A7: same-gap port move to an LE-incompatible port (sums hold -> isolates compat).
    # Fallback: cross-gap move (breaks per-gap conservation). Either must REJECT.
    from STRICT_INVENTORY import gap_bounds
    inv = L['inv']
    e = dict(env0)
    src = None
    for k, v in env0.items():
        if k.startswith('SLv_z') and v and v > 0:
            parts = k.split('_')
            src = (int(parts[1][1:]), int(parts[2]), int(parts[3]), v)
            break
    assert src is not None, 'need allocated cell in base edge'
    i0, s0, b0, v0 = src
    tgt = None
    for s2 in range(127):
        for b2 in range(2):
            if (s2, b2) == (s0, b0):
                continue
            if env0.get(f'SLv_z{i0}_{s2}_{b2}', 0) != 0:
                continue
            plo2, phi2 = inv.port_bounds(s2, b2)
            glo2, ghi2 = gap_bounds(d, inv, i0)
            try:
                plo2v, phi2v = d.ev_iter(plo2, env0), d.ev_iter(phi2, env0)
                glo2v, ghi2v = d.ev_iter(glo2, env0), d.ev_iter(ghi2, env0)
            except Exception:
                continue
            if not (plo2v <= ghi2v and glo2v <= phi2v):
                tgt = (s2, b2)
                break
        if tgt:
            break
    if tgt is not None:
        s2, b2 = tgt
        e[f'SLv_z{i0}_{s0}_{b0}'] = v0 - 1
        e[f'SLv_z{i0}_{s2}_{b2}'] = env0.get(f'SLv_z{i0}_{s2}_{b2}', 0) + 1
        r = d.ev_iter(L['root'], e)
        res['A7-incompat-port-reject'] = (r is False)
        print('A7 incompatible port rejected:', r is False, flush=True)
    else:
        # fallback: cross-gap move breaks per-gap conservation -> REJECT
        i2 = (i0 + 5) % 10
        e[f'SLv_z{i0}_{s0}_{b0}'] = v0 - 1
        e[f'SLv_z{i2}_{s0}_{b0}'] = env0.get(f'SLv_z{i2}_{s0}_{b0}', 0) + 1
        r = d.ev_iter(L['root'], e)
        res['A7-cross-gap-reject'] = (r is False)
        print('A7 cross-gap move rejected:', r is False, flush=True)

    # A8: unsplit two-genuine word must be REJECTED by the circuit (intermediate genuine forbidden)
    from STRICT_CERTIFY import ssertify as _ss
    keys = list(range(1, 10))
    Sset = set(keys)
    A = S.balanced(keys)
    M = {1, 2, 3, 4, 5}
    word = [('K', 2), ('K', 3)]
    R = replay(word, A0=serial(A), B0=serial(A))
    assert R['agree']
    gens = [i for i, l in enumerate(R['legs']) if l['m'] == 'K' and l['x'] in M and l['chg']]
    if len(gens) >= 2:
        H = sum(l['a'] for l in R['legs'])
        st, info = _ss(d, L, serial(A), serial(A), Sset, M, word, H, force_mid=True)
        assert st != 'skip', info
        if st == 'fail' and isinstance(info, dict) and 'env' in info:
            res['A8-unsplit-rejected'] = True
            print('A8 unsplit two-genuine rejected by circuit: True', flush=True)
        elif st == 'ok':
            res['A8-unsplit-rejected'] = False
            print('A8 WARNING: unsplit accepted', info['H'], info['q'], info['w'], flush=True)
        else:
            res['A8-unsplit-rejected'] = 'skip:' + str(info)
            print('A8 skipped:', info, flush=True)
    else:
        res['A8-unsplit-rejected'] = 'n/a (need 2 genuine legs)'
        print('A8 n/a', flush=True)

    # A3: normalize_word preservation fuzz (endpoints, H, genuine-q sequence, terminal)
    import copy as _cp
    nok = 0
    rng = random.Random(801)
    for trial in range(60):
        n = rng.randint(8, 16)
        ks = list(range(1, n + 1))
        t = S.LEAF
        ins = sorted(ks)
        rng.shuffle(ins)
        def _ins(t, k):
            return S.node(k, S.LEAF, S.LEAF) if t[0] == 'leaf' else (S.node(t[1], _ins(t[2], k), t[3]) if k < t[1] else S.node(t[1], t[2], _ins(t[3], k)))
        for k in ins:
            t = _ins(t, k)
        T0 = serial(t)
        word = []
        for _ in range(rng.randint(1, 6)):
            md = 'K' if rng.random() < 0.6 else 'D'
            word.append((md, rng.choice(ks)))
        try:
            R1 = replay(word, A0=_cp.deepcopy(T0), B0=_cp.deepcopy(T0))
        except Exception:
            continue
        if not R1['agree']:
            continue
        w2 = normalize_word(word, _cp.deepcopy(T0), _cp.deepcopy(T0))
        try:
            R2 = replay(w2, A0=_cp.deepcopy(T0), B0=_cp.deepcopy(T0))
        except Exception:
            print('A3-NORM-REPLAY-FAIL', trial)
            raise AssertionError('normalize-replay')
        assert R2['agree']
        assert R1['pairs'][-1] == R2['pairs'][-1], 'endpoints'
        assert sum(l['a'] for l in R1['legs']) == sum(l['a'] for l in R2['legs']), 'H'
        t1, t2 = R1['legs'][-1], R2['legs'][-1]
        assert (t1['m'], t1.get('dB'), t1['chg']) == (t2['m'], t2.get('dB'), t2['chg']), 'terminal'
        g1 = [(l['x'], l['dB']) for l in R1['legs'] if l['m'] == 'K' and l['chg']]
        g2 = [(l['x'], l['dB']) for l in R2['legs'] if l['m'] == 'K' and l['chg']]
        assert g1 == g2, 'genuine-seq'
        assert len(w2) <= 5 or sum(l['a'] for l in R2['legs']) > 2, 'bound-or-high'
        nok += 1
    res['A3-normalize-preserve'] = nok
    print('A3 normalize preservation: %d/60' % nok, flush=True)
    json.dump(res, open(PDIR + 'STRICT_SEMANTIC_REGRESSIONS.json', 'w'), indent=1)
    print('adversarial done', flush=True)

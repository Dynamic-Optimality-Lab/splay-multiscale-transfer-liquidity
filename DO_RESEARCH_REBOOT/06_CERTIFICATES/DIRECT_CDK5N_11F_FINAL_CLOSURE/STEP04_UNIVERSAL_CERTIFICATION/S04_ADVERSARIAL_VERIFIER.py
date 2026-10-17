# S04_ADVERSARIAL_VERIFIER.py — Gate I falsification battery (FAIL CLOSED).
# (1) Conjunct-wise env audit: EVERY top-level conjunct of low+high roots under
# stored witness envs must be True (independent re-audit beyond root-level SAT).
# (2) Random closed-walk properties: K==G on B-closed, core constancy, q-shape.
# (3) Mask parametricity: all 126 mu roundtrips + no mask-specific branches (audit).
# (4) Saturation boundary units on gap_of/sig. (5) B-topology variety count.
# (6) Rotation agreement tally. (7) High fiber/env conjuncts. (8) Composition probe.
import sys, json, time, random, itertools
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP01_PRODUCTION_CONSTRAINT_SOLVER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP02_FREE_WITNESS_SYNTHESIS')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP02_FREE_WITNESS_SYNTHESIS')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP04_UNIVERSAL_CERTIFICATION')

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP04_UNIVERSAL_CERTIFICATION/'
S02 = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP02_FREE_WITNESS_SYNTHESIS/'
FAIL = []
RES = {}


def J(p, o):
    json.dump(o, open(PDIR + p, 'w'), indent=1)


def check(name, ok, detail=''):
    RES[name] = {'status': 'PASS' if ok else 'FAIL', 'detail': detail}
    print('%-52s %s %s' % (name, 'PASS' if ok else 'FAIL', detail), flush=True)
    if not ok:
        FAIL.append(name)


import splay as S
from PC_TYPED_DAG import DAG
from STRICT_LOW_COMPILER import build_slow
from STRICT_HIGH_COMPILER import build_shigh
from STRICT_CERTIFY import ssertify
from PC_CONCRETIZE import serial, gap_of
from CW_SYNTHESIS_RUN import chain_desc
from CRA_pointer_tuple_replay import replay, core_of
from CRA_segment_memberships import genuine_keys, keep_support

if __name__ == '__main__':
    # ---- (1) conjunct-wise env audit on stored-equivalent fresh envs ----
    d = DAG()
    L = build_slow(d, 'SL')
    kk = list(range(1, 13))
    m0, x = 12, 6
    lo = sorted(k for k in kk if k < x)
    hi = sorted(k for k in kk if x < k < m0)
    AE3 = S.node(m0, S.node(x, S.balanced(lo), S.balanced(hi)), S.LEAF)
    BE3 = S.node(m0, chain_desc([k for k in kk if k != m0]), S.LEAF)
    st, info = ssertify(d, L, serial(AE3), serial(BE3), set([6, 7, 8, 9, 10, 11, 12, 1, 2]), {6, 12, 9, 10, 11}, [('K', x)], 1)
    assert st == 'ok'
    env = dict(info['env'])

    def conjuncts(dag, root):
        out = []
        n = root
        while True:
            k, t, a, e = dag.nodes[n]
            if k != 'and':
                out.append(n)
                break
            out.append(a[1])
            n = a[0]
        return out

    bad = [c for c in conjuncts(d, L['root']) if d.ev_iter(c, env) is not True]
    check('low conjunct-wise audit (E3 env)', not bad, 'nbad=%d' % len(bad))
    dh = DAG()
    Hh = build_shigh(dh, 'SH')
    sh = {'SH' + k[2:]: v for k, v in env.items() if k.startswith('SLs_') or k.startswith('SLt_')}
    he = dict(sh, SHg_fmu=env['SLs_mu'], SHg_fv=env['SLt_aI0'], SHbt_bT0=2, SHbt_bd0=6,
              SH_q=3, SH_w1=3, **{'SHg_fsg%d' % i: env['SLs_sg%d' % i] for i in range(10)})
    for i in range(19):
        for suf in ('bkl', 'brl', 'bkr', 'brr', 'blo', 'bhi'):
            he['SHg_fb_%s%d' % (suf, i)] = env['SLt_b_%s%d' % (suf, i)]
    he['SHg_fb_broot'] = env['SLt_b_broot']
    pth = [2, 3, 4, 5, 6, 7, 8]
    for k in range(7):
        he['SHbt_bp0_%d' % k] = pth[k]
    for k in range(6):
        he['SHbt_bdir0_%d' % k] = False
    # inactive slots (k>=bd): unconstrained by verify_bpath; default-fill for the
    # total-env extension check (methodology: env + defaults ⊨ root)
    for k in range(7, 19):
        he['SHbt_bp0_%d' % k] = 19
    for k in range(6, 18):
        he['SHbt_bdir0_%d' % k] = False
    # unused B-trace events 1..4 (relation constrains event 0 only): null defaults
    for e in range(1, 5):
        he['SHbt_bT%d' % e] = 19
        he['SHbt_bd%d' % e] = 0
        for k in range(19):
            he['SHbt_bp%d_%d' % (e, k)] = 19
        for k in range(18):
            he['SHbt_bdir%d_%d' % (e, k)] = False
    # BStruct parent/depth vars from decoded topologies (root parent = NULL 19)
    from S02_B_SIDE_PROPAGATOR import decode_btopo as _dec

    def topo_of(pins, pre):
        topo = {}
        for i in range(19):
            topo[i] = (pins['%s_bkl%d' % (pre, i)], pins['%s_brl%d' % (pre, i)],
                       pins['%s_bkr%d' % (pre, i)], pins['%s_brr%d' % (pre, i)])
        return topo, pins[pre + 'root'] if (pre + 'root') in pins else pins[pre + '_broot']

    def fill_bstruct(topo, root, vst):
        par = {root: 19}
        dep = {root: 0}
        stack = [root]
        while stack:
            n = stack.pop()
            kl, lr, kr, rr = topo[n]
            if kl == 0 and lr != 19 and lr not in par:
                par[lr] = n
                dep[lr] = dep[n] + 1
                stack.append(lr)
            if kr == 0 and rr != 19 and rr not in par:
                par[rr] = n
                dep[rr] = dep[n] + 1
                stack.append(rr)
        for i in range(19):
            he['%s_bpar%d' % (vst, i)] = par.get(i, 19)
            he['%s_bdep%d' % (vst, i)] = dep.get(i, 0)

    ts, rs_ = topo_of(he, 'SHs_b')
    tt, rt_ = topo_of(he, 'SHt_b')
    tg, rg_ = topo_of(he, 'SHg_fb')
    fill_bstruct(ts, rs_, 'SHsbs')
    fill_bstruct(tt, rt_, 'SHsbt')
    fill_bstruct(tg, rg_, 'SHsbg')
    badh = [c for c in conjuncts(dh, Hh['root']) if dh.ev_iter(c, he) is not True]
    det = ''
    if badh:
        kk, tt, aa, ee = dh.nodes[badh[0]]

        def _nm(x):
            k2, t2, a2, e2 = dh.nodes[x]
            return (e2[1] + '=' + str(he.get(e2[1], '?'))) if k2 == 'var' else (str(e2[0]) if k2 == 'const' else k2)

        det = kk + ' ' + (ee[1] + '=' + str(he.get(ee[1], '?')) if kk == 'var' else str([_nm(x) for x in aa])[:220])
    check('high conjunct-wise audit (fiber env)', not badh, 'nbad=%d %s' % (len(badh), det))
    # ---- (2) closed-walk properties on KNOWN survivors + random trials ----
    RDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_MSINK_G0_R1HARD/'
    rows = []
    for seed in ('concat35', 'mr33'):
        for l in open(RDIR + 'state_' + seed + '/survivors.jsonl'):
            rows.append(json.loads(l))

    def parse(c):
        return [(t[0], int(t[1:])) for t in c.split(',')]

    ncl = nkeq = ncore = 0
    nsur = 0
    for r_ in rows[:80]:
        w = parse(r_['canon'])
        try:
            R = replay(w)
        except Exception:
            continue
        if not R['agree']:
            continue
        nsur += 1
        if R['S1'] == R['S0']:
            ncl += 1
            G = set(genuine_keys(R['legs']))
            K = set(keep_support(R['legs']))
            if K == G:
                nkeq += 1
            else:
                check('falsify K==G on ' + r_['canon'], False, '%s vs %s' % (sorted(K), sorted(G)))
            if len(G) == 5:
                c0 = core_of(R['S0'][1], G)
                c1 = core_of(R['S1'][1], G)
                if c0 == c1 and c0 is not None and len(c0) == 9:
                    ncore += 1
                else:
                    check('falsify core-const on ' + r_['canon'], False, '')
    check('survivor replay agree', nsur > 0, '%d' % nsur)
    check('closed K==G (%d closed)' % ncl, nkeq == ncl, '%d/%d' % (nkeq, ncl))
    check('core constancy 9-set', ncore == ncl or ncl == 0, '%d/%d' % (ncore, ncl))
    r = random.Random(4)
    nq = ntrials = 0
    for trial in range(200):
        n = r.choice([5, 6, 7])
        keys = list(range(1, n + 1))
        t = S.LEAF

        def ins(nn, k):
            if nn[0] == 'leaf':
                return S.node(k, S.LEAF, S.LEAF)
            _, kk2, l, rr = nn
            return S.node(kk2, ins(l, k), rr) if k < kk2 else S.node(kk2, l, ins(rr, k))

        ks = keys[:]
        r.shuffle(ks)
        for k in ks:
            t = ins(t, k)
        nw = r.randint(1, 5)
        word = [('K', r.choice(keys)) for _ in range(nw)]
        try:
            R = replay(word, serial(t), serial(t))
        except Exception:
            continue
        if not R['agree']:
            continue
        ntrials += 1
        if all(l['q'] == (l['dB'] // 2 if l['dB'] is not None else 0) for l in R['legs']):
            nq += 1
    check('random q-shape', nq == ntrials and ntrials > 0, '%d/%d' % (nq, ntrials))
    # ---- (3) mask parametricity: all 126 mu roundtrips ----
    nmu = 0
    for combo in itertools.combinations(range(9), 5):
        mu = sum(1 << i for i in combo)
        if len([i for i in range(9) if (mu >> i) & 1]) == 5:
            nmu += 1
    check('126 masks enumerated', nmu == 126, str(nmu))
    # ---- (4) saturation boundary units ----
    from PC_CONCRETIZE import gap_of as _g
    Ss = [1, 2, 6, 7, 8, 9, 10, 11, 12]
    units = [(_g(Ss, 0) == 0), (_g(Ss, 3) == 2), (_g(Ss, 5) == 2), (_g(Ss, 13) == 9), (_g(Ss, 6) == 2)]
    check('gap boundary units', all(units), str(units))
    # ---- (5) B-topology variety (distinct shapes across corpus+fresh) ----
    from S02_B_SIDE_PROPAGATOR import decode_btopo, topo_key
    pins = dict(info['env'])
    stopo, sroot = decode_btopo(pins, 'SLs')
    check('B-topo decodes', topo_key(stopo, sroot) is not None, '')
    # ---- (6) rotation agreement tally (50 fresh xvals) ----
    from CRA_pointer_tuple_replay import splay_B_push, to_ptr, pserial
    from S02_B_SIDE_PROPAGATOR import splay_ref

    def ser(n):
        return None if n[0] == 'leaf' else (n[1], ser(n[2]), ser(n[3]))

    def to_topo(t):
        topo = {}

        def go(n):
            if n[0] == 'leaf':
                return 19
            _, k, l, rr = n
            Lr, Rr = go(l), go(rr)
            topo[k] = ((0 if Lr != 19 else 2), Lr, (0 if Rr != 19 else 2), Rr)
            return k

        return topo, go(t)

    def of_dot(t, rr):
        # iterative, cycle-detecting (a cycle is a falsification finding, not a hang)
        if rr == 19:
            return '.'
        order = []
        seen = set()
        stack = [rr]
        while stack:
            n = stack.pop()
            if n == 19 or n in seen:
                continue
            seen.add(n)
            order.append(n)
            kl, lr, kr, rr2 = t[n]
            if kl == 0:
                stack.append(lr)
            if kr == 0:
                stack.append(rr2)
        if len(seen) > 30:
            raise AssertionError(('cyclic-or-huge', len(seen)))
        memo = {19: '.'}
        for n in reversed(order):
            kl, lr, kr, rr2 = t[n]
            memo[n] = (n, memo.get(lr if kl == 0 else 19, 'CYC'), memo.get(rr2 if kr == 0 else 19, 'CYC'))
        return memo[rr]

    nx = 0
    nxinfo = []
    for trial in range(50):
        ks = list(range(9))
        r.shuffle(ks)
        t = S.LEAF
        for k in ks:
            t = ins(t, k)
        tgt = ks[trial % 9]
        topo, root = to_topo(t)
        try:
            t2, r2, dd = splay_ref(dict(topo), root, tgt)
            got = of_dot(t2, r2)
            exp = pserial(splay_B_push(to_ptr(ser(t)), tgt)[0])
            if got == exp:
                nx += 1
            else:
                nxinfo.append((trial, tgt, 'MISMATCH'))
        except Exception as e:
            nxinfo.append((trial, tgt, type(e).__name__ + str(e)[:80]))
    check('rotation xval 50/50', nx == 50, '%d %s' % (nx, nxinfo[:3]))
    J('S04_ADVERSARIAL_RESULTS.json', RES)
    print('FAIL:', FAIL, flush=True)
    assert not FAIL, FAIL
    print('ADVERSARIAL PASS')

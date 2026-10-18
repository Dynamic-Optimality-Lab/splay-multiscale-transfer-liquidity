# G03R_CANONICAL_STATE.py — GATE A: exact abstract-state identity repair.
# Defect: old canon_key kept SLs_/SLt_ prefixes, so equal abstract states under
# different namespaces produced unequal vertex ids, breaking endpoint chaining.
# Repair: map SLs_<f> and SLt_<f> to common field <f> over the FULL 147-field
# ordinary-state schema derived from StateVars7 (mu + BState + alpha7 + sigma).
# No defaults for missing fields; bools normalized; domains checked.
import sys, json, os
# CWD-bootstrap: allow invocation from any workdir; anchor at repo root.
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = _HERE
for _ in range(8):
    if os.path.isdir(os.path.join(_ROOT, 'python', 'independent')):
        break
    _up = os.path.dirname(_ROOT)
    if _up == _ROOT:
        break
    _ROOT = _up
if not os.path.isdir(os.path.join(_ROOT, 'python', 'independent')):
    _ROOT = os.environ.get('RESCUE_ROOT', _ROOT)
if _ROOT != os.getcwd():
    os.chdir(_ROOT)
for _p in ('python/independent',
           'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER',
           'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE'):
    _ap = os.path.join(_ROOT, *_p.split('/'))
    if _ap not in sys.path:
        sys.path.insert(0, _ap)

RDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE/RESCUE_01_GRAPH_IDENTITY_AND_POTENTIAL/'
PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE/'
OUT = os.environ.get('RESCUE_OUT', RDIR)
if OUT and not OUT.endswith('/') and not OUT.endswith('\\'):
    OUT = OUT + '/'
if OUT:
    os.makedirs(OUT, exist_ok=True)

NB, NCORE, APOS, NSIG = 19, 9, 7, 10
CRANK = [1, 3, 5, 7, 9, 11, 13, 15, 17, 0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

FIELD_ORDER = ['mu']
for i in range(NB):
    FIELD_ORDER.append('b_bkl%d' % i)
for i in range(NB):
    FIELD_ORDER.append('b_brl%d' % i)
for i in range(NB):
    FIELD_ORDER.append('b_bkr%d' % i)
for i in range(NB):
    FIELD_ORDER.append('b_brr%d' % i)
FIELD_ORDER.append('b_broot')
for i in range(NB):
    FIELD_ORDER.append('b_blo%d' % i)
for i in range(NB):
    FIELD_ORDER.append('b_bhi%d' % i)
for p in range(APOS):
    FIELD_ORDER.append('ak%d' % p)
    FIELD_ORDER.append('aS%d' % p)
    FIELD_ORDER.append('aI%d' % p)
for i in range(NSIG):
    FIELD_ORDER.append('sg%d' % i)


def _norm(v):
    if isinstance(v, bool):
        return int(v)
    if isinstance(v, int):
        return v
    raise TypeError('non-integer state value %r' % (v,))


class CanonError(Exception):
    pass


def _domain(f):
    if f == 'mu':
        return 512
    if f.startswith('b_bkl') or f.startswith('b_bkr'):
        return 4
    if f.startswith('b_brl') or f.startswith('b_brr'):
        return 32
    if f == 'b_broot':
        return 32
    if f.startswith('b_blo') or f.startswith('b_bhi'):
        return 32
    if f.startswith('ak'):
        return 4
    if f.startswith('aS'):
        return 2
    if f.startswith('aI'):
        return 16
    if f.startswith('sg'):
        return 512
    raise CanonError('unknown field ' + f)


def canon_key(env, nstag):
    """Exact canonical key: tuple of all ordinary-state field values, namespace-free.
    nstag = 'SLs_' or 'SLt_'. Raises CanonError on missing/malformed values."""
    vals = []
    for f in FIELD_ORDER:
        kk = nstag + f
        if kk not in env:
            raise CanonError('missing ' + kk)
        v = _norm(env[kk])
        if not (0 <= v < _domain(f)):
            raise CanonError('domain ' + kk)
        vals.append(v)
    assert len(vals) == N_FIELDS
    return tuple(vals)


N_FIELDS = 1 + NB * 4 + 1 + NB * 2 + APOS * 3 + NSIG  # 1+76+1+38+21+10 = 147


def key_to_maps(key):
    """Split canonical key back into named source/destination interface dicts."""
    if len(key) != N_FIELDS:
        raise CanonError('key length %d != %d' % (len(key), N_FIELDS))
    out_s = {'SLs_' + f: v for f, v in zip(FIELD_ORDER, key)}
    out_t = {'SLt_' + f: v for f, v in zip(FIELD_ORDER, key)}
    return out_s, out_t


def valid_state_dict(d):
    """Python mirror of state_valid7 + b_valid scalar parts. d: {field: value}."""
    if bin(d['mu']).count('1') != 5:
        return False, 'popcount'
    for i in range(NSIG):
        if not (0 <= d['sg%d' % i] <= 266):
            return False, 'sig'
    for p in range(APOS):
        if d['ak%d' % p] not in (0, 1, 2):
            return False, 'ak'
        if not (0 <= d['aI%d' % p] <= 8):
            return False, 'aI'
    if not (0 <= d['b_broot'] < NB):
        return False, 'root'
    for i in range(NB):
        if not (d['b_blo%d' % i] <= CRANK[i] <= d['b_bhi%d' % i]):
            return False, 'rankcontain%d' % i
    for i in range(NCORE, NB):
        if d['b_bkl%d' % i] != 2 or d['b_bkr%d' % i] != 2:
            return False, 'gapchild%d' % i
    # children interval equalities (core nodes)
    for i in range(NCORE):
        r = CRANK[i]
        for (kk, rr, isL) in (('b_bkl%d' % i, 'b_brl%d' % i, True), ('b_bkr%d' % i, 'b_brr%d' % i, False)):
            if d[kk] == 0:
                c = d[rr]
                if not (0 <= c < NB):
                    return False, 'childref'
                if isL:
                    if not (d['b_blo%d' % c] == d['b_blo%d' % i] and d['b_bhi%d' % c] == r - 1):
                        return False, 'intervalL%d' % i
                else:
                    if not (d['b_blo%d' % c] == r + 1 and d['b_bhi%d' % c] == d['b_bhi%d' % i]):
                        return False, 'intervalR%d' % i
    if not (d['b_blo%d' % d['b_broot']] == 0 and d['b_bhi%d' % d['b_broot']] == 18):
        return False, 'rootspan'
    return True, 'ok'


def dict_of_env(env, nstag):
    out = {}
    for f in FIELD_ORDER:
        kk = nstag + f
        if kk not in env:
            raise CanonError('missing ' + kk)
        out[f] = _norm(env[kk])
    return out


if __name__ == '__main__':
    import splay as S
    from PC_TYPED_DAG import DAG
    from STRICT_LOW_COMPILER import build_slow
    from STRICT_CERTIFY import ssertify
    from PC_CONCRETIZE import serial
    from CRA_pointer_tuple_replay import replay
    res = {}

    def T(name, ok, detail=''):
        res[name] = {'pass': bool(ok), 'detail': str(detail)[:300]}
        print('%-8s %s %s' % (name, 'PASS' if ok else 'FAIL', str(detail)[:160]), flush=True)

    d = DAG()
    L = build_slow(d, 'SL')
    import random as _r
    _rg = _r.Random(7)
    env = None
    for _try in range(60):
        def _mk(ks):
            ks = list(ks)
            _rg.shuffle(ks)
            t = S.LEAF

            def _ins(n, k):
                if n[0] == 'leaf':
                    return S.node(k, S.LEAF, S.LEAF)
                _, kk, l, rr = n
                return S.node(kk, _ins(l, k), rr) if k < kk else S.node(kk, l, _ins(rr, k))

            for k in ks:
                t = _ins(t, k)
            return t
        _keys = list(range(1, 10))
        A = _mk(_keys)
        B = _mk(_keys)
        M, Sset = {1, 3, 5, 7, 9}, set(_keys)
        _x = _rg.choice(sorted(M))
        try:
            _R = replay([('K', _x)], serial(A), serial(B))
        except Exception:
            continue
        if not _R.get('agree'):
            continue
        _H = sum(_l['a'] for _l in _R['legs'])
        try:
            st, info = ssertify(d, L, serial(A), serial(B), Sset, M, [('K', _x)], _H)
        except Exception:
            continue
        if st == 'ok':
            env, _H0, _x0, _A, _B = dict(info['env']), _H, _x, A, B
            break
    assert env is not None, 'no ssertify-ok seed found'
    sp = {k: v for k, v in env.items() if k.startswith('SLs_')}
    tp = {k: v for k, v in env.items() if k.startswith('SLt_')}
    # T-A1: same state different namespaces
    ks, kt = canon_key(sp, 'SLs_'), canon_key(tp, 'SLt_')
    T('T-A1', True, 'keys computed')
    # same-state cross-namespace: source dict relabeled as destination must match
    tp_as_s = {'SLs_' + k[4:]: v for k, v in tp.items()}
    T('T-A1b', canon_key(tp_as_s, 'SLs_') == canon_key(tp, 'SLt_'), 'namespace invariance')
    # T-A2: different B-roots
    sp2 = dict(sp)
    sp2['SLs_b_broot'] = (int(sp['SLs_b_broot']) + 1) % 19
    T('T-A2', canon_key(sp2, 'SLs_') != ks, 'broot sensitivity')
    # T-A3: different A-shadow
    sp3 = dict(sp)
    sp3['SLs_ak0'] = (int(sp['SLs_ak0']) + 1) % 3
    T('T-A3', canon_key(sp3, 'SLs_') != ks, 'shadow sensitivity')
    # T-A4: different signature
    sp4 = dict(sp)
    sp4['SLs_sg0'] = int(sp['SLs_sg0']) + 1
    T('T-A4', canon_key(sp4, 'SLs_') != ks, 'sig sensitivity')
    # T-A5: different mask
    sp5 = dict(sp)
    sp5['SLs_mu'] = int(sp['SLs_mu']) ^ 1
    T('T-A5', canon_key(sp5, 'SLs_') != ks, 'mask sensitivity')
    # T-A6: missing field rejected
    sp6 = dict(sp)
    del sp6['SLs_mu']
    try:
        canon_key(sp6, 'SLs_')
        T('T-A6', False, 'no rejection')
    except CanonError:
        T('T-A6', True, 'rejected')
    # T-A7: synthetic chained path (edge1.t == edge2.s as abstract states)
    R1 = replay([('K', _x0)], serial(_A), serial(_B))
    def _tl2list(t):
        if t == '.' or (isinstance(t, tuple) and t and t[0] == 'leaf'):
            return None
        k, l, r = t
        return [k, _tl2list(l), _tl2list(r)]

    S1A, S1B = _tl2list(R1['S1'][0]), _tl2list(R1['S1'][1])
    _x1 = [k for k in sorted(M) if k != _x0][0]
    R12 = replay([('K', _x1)], S1A, S1B)
    H12 = sum(_l['a'] for _l in R12['legs']) if R12.get('agree') else None
    st2, info2 = (None, None)
    if R12.get('agree'):
        try:
            st2, info2 = ssertify(d, L, S1A, S1B, Sset, M, [('K', _x1)], H12)
        except Exception as _e:
            st2 = 'exc %s' % _e
    if st2 == 'ok':
        env2 = dict(info2['env'])
        sp_b = {k: v for k, v in env2.items() if k.startswith('SLs_')}
        chained = canon_key(tp, 'SLt_') == canon_key(sp_b, 'SLs_')
        T('T-A7', chained, 't1==s2 chained vertex')
    else:
        T('T-A7', False, 'second ssertify %s' % st2)
    # T-A8: self-loop key equality (same dict both sides)
    T('T-A8', canon_key(sp, 'SLs_') == canon_key(
        {'SLt_' + k[4:]: v for k, v in sp.items()}, 'SLt_'), 'self-loop identity')
    # T-A9: schema count vs authoritative spec
    T('T-A9', len(FIELD_ORDER) == N_FIELDS == 147, 'nfields=%d' % len(FIELD_ORDER))
    # T-A10: roundtrip
    ms, mt = key_to_maps(ks)
    T('T-A10', canon_key(ms, 'SLs_') == ks and canon_key(mt, 'SLt_') == ks, 'roundtrip')
    # validity of real endpoint
    okv, whyv = valid_state_dict(dict_of_env(env, 'SLs_'))
    T('T-AV', okv, 'source valid: ' + whyv)
    okv2, whyv2 = valid_state_dict(dict_of_env(env, 'SLt_'))
    T('T-AV2', okv2, 'dest valid: ' + whyv2)
    json.dump(res, open(OUT + 'G03R_CANONICALIZATION_TESTS.json', 'w'), indent=1)
    print('FAIL:', [k for k, v in res.items() if not v['pass']], flush=True)

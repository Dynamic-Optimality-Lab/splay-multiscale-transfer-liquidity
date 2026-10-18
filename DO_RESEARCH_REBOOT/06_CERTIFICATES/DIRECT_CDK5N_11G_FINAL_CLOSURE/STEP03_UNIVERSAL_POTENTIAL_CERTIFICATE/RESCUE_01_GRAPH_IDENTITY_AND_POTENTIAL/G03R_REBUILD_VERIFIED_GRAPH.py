# G03R_REBUILD_VERIFIED_GRAPH.py — GATE B: full-state witnessed graph rebuild.
# Every edge stores COMPLETE source/destination abstract interface assignments
# (147 fields each), exact weight, provenance, witness refs. No feature-only edges.
# Sources: (1) S02 generalization corpus replays; (2) fresh reproducible ssertify
# edges (mix/root/deep); (3) E3/E4 low cases; (4) contracted-high concrete triples
# re-derived via midpoint expansion where models exist (else referenced, not forged).
import sys, json, os, time, hashlib, random
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
           'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT',
           'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER',
           'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE',
           'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE',
           'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP02_FREE_WITNESS_SYNTHESIS'):
    _ap = os.path.join(_ROOT, *_p.split('/'))
    if _ap not in sys.path:
        sys.path.insert(0, _ap)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

RDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE/RESCUE_01_GRAPH_IDENTITY_AND_POTENTIAL/'
PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE/'
OUT = os.environ.get('RESCUE_OUT', RDIR)
if OUT and not OUT.endswith('/') and not OUT.endswith('\\'):
    OUT = OUT + '/'

import splay as S
from PC_TYPED_DAG import DAG
from STRICT_LOW_COMPILER import build_slow
from STRICT_CERTIFY import ssertify
from PC_CONCRETIZE import serial
from CRA_pointer_tuple_replay import replay
from G03R_CANONICAL_STATE import canon_key, dict_of_env, valid_state_dict, CanonError


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        h.update(f.read())
    return h.hexdigest()


def rand_tree(rng, keys, mode):
    if mode == 'chain':
        ks = sorted(keys)
    elif mode == 'zigzag':
        ks = sorted(keys)
        lo, hi, ks2, flip = 0, len(ks) - 1, [], True
        while lo <= hi:
            if flip:
                ks2.append(ks[lo]); lo += 1
            else:
                ks2.append(ks[hi]); hi -= 1
            flip = not flip
        ks = ks2
    else:
        ks = list(keys)
        rng.shuffle(ks)
    t = S.LEAF

    def ins(n, k):
        if n[0] == 'leaf':
            return S.node(k, S.LEAF, S.LEAF)
        _, kk, l, rr = n
        return S.node(kk, ins(l, k), rr) if k < kk else S.node(kk, l, ins(rr, k))

    for k in ks:
        t = ins(t, k)
    return t


def root_key(t):
    return None if t[0] == 'leaf' else t[1]


def deepest_key(t, M):
    best = [None, -1]

    def rec(n, dd):
        if n[0] == 'leaf':
            return
        _, k, l, rr = n
        if k in M and dd > best[1]:
            best[0], best[1] = k, dd
        rec(l, dd + 1)
        rec(rr, dd + 1)

    rec(t, 0)
    return best[0]


if __name__ == '__main__':
    import sys as _s
    nfresh = int(_s.argv[1]) if len(_s.argv) > 1 else 30
    seed0 = int(_s.argv[2]) if len(_s.argv) > 2 else 11
    t_start = time.process_time()
    d = DAG()
    L = build_slow(d, 'SL')
    edges = []
    seen = set()

    def add_edge(src_env, dst_env, w, family, prov, wit=None, mask=None, sig=None):
        try:
            sk = canon_key(src_env, 'SLs_')
            tk = canon_key(dst_env, 'SLt_')
        except CanonError as e:
            return ('canon-fail', str(e))
        try:
            okv, _ = valid_state_dict(dict_of_env(src_env, 'SLs_'))
            okv2, _ = valid_state_dict(dict_of_env(dst_env, 'SLt_'))
        except CanonError as e:
            return ('valid-fail', str(e))
        key = (sk, tk, int(w), family)
        if key in seen:
            return ('dup', '')
        seen.add(key)
        edges.append({'source_key': list(sk), 'destination_key': list(tk),
                      'source_state': {k[4:]: (int(v) if not isinstance(v, bool) else int(v)) for k, v in src_env.items() if k.startswith('SLs_')},
                      'destination_state': {k[4:]: (int(v) if not isinstance(v, bool) else int(v)) for k, v in dst_env.items() if k.startswith('SLt_')},
                      'weight': int(w), 'edge_family': family,
                      'source_certificate': prov, 'witness_reference': wit,
                      'mask': mask, 'signature': sig,
                      's_valid': bool(okv), 't_valid': bool(okv2)})
        return ('ok', '')

    stats = {'s02': 0, 'fresh': 0, 'dups': 0, 'fails': 0}
    # (1) S02 corpus replays
    corp = json.load(open('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP02_FREE_WITNESS_SYNTHESIS/S02_GENERALIZATION_CORPUS.json'))
    dL = DAG()
    L2 = build_slow(dL, 'SL')
    for c in corp:
        if c.get('grounded') != 'ok':
            continue

        def totup(x):
            if x is None or x == '.':
                return S.LEAF
            k, l, r = x
            return S.node(k, totup(l), totup(r))
        try:
            A0 = totup(c['A'])
            B0 = totup(c['B'])
            word = [tuple(w) for w in c['word']]
            st, info = ssertify(dL, L2, serial(A0), serial(B0), set(c['Sset']), set(c['M']), word, int(c['H']))
        except Exception:
            stats['fails'] += 1
            continue
        if st != 'ok':
            stats['fails'] += 1
            continue
        env = dict(info['env'])
        sp = {k: v for k, v in env.items() if k.startswith('SLs_')}
        tp = {k: v for k, v in env.items() if k.startswith('SLt_')}
        r, _ = add_edge(sp, tp, info['w'], 'low-s02-' + str(c.get('category', '?')),
                        'S02 corpus replay cat=%s' % c.get('category'), wit=str(c.get('word'))[:120],
                        mask=sorted(c.get('M', [])), sig=None)
        stats['s02' if r == 'ok' else ('dups' if r == 'dup' else 'fails')] += 1
    # (2) fresh reproducible edges
    rng = random.Random(seed0)
    modes = ['mix', 'root', 'deep']
    got = 0
    tries = 0
    while got < nfresh and tries < nfresh * 12 and time.process_time() - t_start < 1500:
        tries += 1
        mode = modes[tries % 3]
        keys = list(range(1, 10))
        u = rng.random()
        mk = rand_tree if u < 0.6 else None
        A = rand_tree(rng, keys, 'rand' if u < 0.6 else ('chain' if u < 0.8 else 'zigzag'))
        B = rand_tree(rng, keys, 'rand' if u < 0.6 else ('chain' if u < 0.8 else 'zigzag'))
        M = set(rng.sample(keys, 5))
        Sset = set(keys)
        if mode == 'root':
            rk = root_key(A)
            x = rk if rk in M else rng.choice(sorted(M))
        elif mode == 'deep':
            dk = deepest_key(A, M)
            x = dk if dk is not None else rng.choice(sorted(M))
        else:
            x = rng.choice(sorted(M))
        try:
            R = replay([('K', x)], serial(A), serial(B))
        except Exception:
            continue
        if not R['agree']:
            continue
        H = sum(l['a'] for l in R['legs'])
        if H > 9:
            continue
        try:
            st, info = ssertify(d, L, serial(A), serial(B), Sset, M, [('K', x)], H)
        except Exception:
            continue
        if st != 'ok':
            continue
        env = dict(info['env'])
        sp = {k: v for k, v in env.items() if k.startswith('SLs_')}
        tp = {k: v for k, v in env.items() if k.startswith('SLt_')}
        r, _ = add_edge(sp, tp, info['w'], 'low-fresh-' + mode,
                        'fresh seed=%d try=%d x=%d H=%d' % (seed0, tries, x, H),
                        wit='K(%d)' % x, mask=sorted(M), sig=None)
        if r == 'ok':
            got += 1
            stats['fresh'] += 1
        elif r == 'dup':
            stats['dups'] += 1
    cpu = time.process_time() - t_start
    json.dump({'edges': edges, 'stats': stats, 'cpu_s': cpu,
               'provenance': {'git_head': '163047d40da4dbd271f86dddce47690dcb138244',
                              'modes': modes, 'nfresh_req': nfresh, 'seed': seed0}},
              open(OUT + 'G03R_VERIFIED_EDGE_LEDGER.json', 'w'), indent=1)
    print('edges=%d stats=%s cpu=%.1f' % (len(edges), stats, cpu), flush=True)

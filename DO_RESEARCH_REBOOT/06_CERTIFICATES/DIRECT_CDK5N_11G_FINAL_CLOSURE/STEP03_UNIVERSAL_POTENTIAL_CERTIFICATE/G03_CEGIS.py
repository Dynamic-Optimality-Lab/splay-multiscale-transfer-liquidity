# G03_CEGIS.py — counterexample-guided potential synthesis (Gate D/G/H, Phase 9).
# Seeds: grounded (s,t,w) from S02 certificates + random replays (ssertify-built
# abstract envs). Template: affine Phi(s) = c + sum theta_i f_i(s) over frozen
# structural features (bounded integer coefficients). Synthesis: Z3 Int over seeds.
# Universal check per (family, weight): EXISTS s,t,witness (E_w AND Phi(t)-Phi(s) > w),
# capped; UNKNOWN recorded, never a certificate. Counterexamples rejoin as seeds.
import sys, json, time, itertools, random
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP01_PRODUCTION_CONSTRAINT_SOLVER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP02_FREE_WITNESS_SYNTHESIS')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP04_UNIVERSAL_CERTIFICATION')

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE/'
FAIL = []


def J(p, o):
    json.dump(o, open(PDIR + p, 'w'), indent=1)


def check(name, ok, detail=''):
    print('%-52s %s %s' % (name, 'PASS' if ok else 'FAIL', detail), flush=True)
    if not ok:
        FAIL.append(name)


import splay as S
from PC_TYPED_DAG import DAG
from STRICT_LOW_COMPILER import build_slow
from STRICT_CERTIFY import ssertify
from PC_CONCRETIZE import serial, from_serial
from CRA_pointer_tuple_replay import replay
from G03_POTENTIAL_FEATURES import eval_all, FEATURES
from CW_SYNTHESIS_RUN import chain_desc

FEAT = ['b_root', 'b_depth_sum', 'b_depth_max', 'b_marked_depth_sum', 'a_root_sidx',
        'a_nslots', 'a_marked_count', 'sig_sum', 'sig_nonempty', 'core_size']


def to_tup(n):
    if n[0] == 'leaf':
        return None
    _, k, l, r = n
    return (k, to_tup(l), to_tup(r))


if __name__ == '__main__':
    import sys as _s
    seed_cap = int(_s.argv[1]) if len(_s.argv) > 1 else 60
    t0 = time.process_time()
    d = DAG()
    L = build_slow(d, 'SL')
    # ---- seeds from S02 certificates (concrete) ----
    import json as _j
    certs = _j.load(open('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP02_FREE_WITNESS_SYNTHESIS/S02_FULL_WITNESS_CERTIFICATES.json'))
    gen = _j.load(open('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP02_FREE_WITNESS_SYNTHESIS/S02_GENERALIZATION_RESULTS.json'))
    seeds = []
    for name, c in certs.items():
        try:
            import ast as _ast
            A0s = _ast.literal_eval(c['A0']) if isinstance(c['A0'], str) else c['A0']
            B0s = _ast.literal_eval(c['B0']) if isinstance(c['B0'], str) else c['B0']

            def totup(x):
                if x is None or x == '.':
                    return S.LEAF
                k, l, r = x
                return S.node(k, totup(l), totup(r))
            A0t, B0t = totup(A0s), totup(B0s)
            word = [(e['mode'], e['key']) for e in c['events']]
            Sset = set(c.get('core', list(range(1, 10))))
            M = set(c['M'])
            H = int(c['H'])
            st, info = ssertify(d, L, serial(A0t), serial(B0t), Sset, M, word, H)
            if st != 'ok':
                continue
            env = dict(info['env'])
            sp = {k: v for k, v in env.items() if k.startswith('SLs_')}
            tp = {k: v for k, v in env.items() if k.startswith('SLt_')}
            fs = eval_all(sp, 'SLs')
            ft = eval_all(tp, 'SLt')
            if any(v is None for v in list(fs.values()) + list(ft.values())):
                continue
            seeds.append({'name': name, 's': fs, 't': ft, 'w': int(info['w'])})
        except Exception:
            continue
    # plus generalization corpus (proper nested-list format)
    corp = _j.load(open('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP02_FREE_WITNESS_SYNTHESIS/S02_GENERALIZATION_CORPUS.json'))
    for c in corp:
        if c.get('grounded') != 'ok':
            continue
        try:
            def totup2(x):
                if x is None or x == '.':
                    return S.LEAF
                k, l, r = x
                return S.node(k, totup2(l), totup2(r))
            A0t, B0t = totup2(c['A']), totup2(c['B'])
            word = [(m, k) for (m, k) in c['word']]
            st, info = ssertify(d, L, serial(A0t), serial(B0t), set(c['Sset']), set(c['M']), word, int(c['H']))
            if st != 'ok':
                continue
            env = dict(info['env'])
            sp = {k: v for k, v in env.items() if k.startswith('SLs_')}
            tp = {k: v for k, v in env.items() if k.startswith('SLt_')}
            fs = eval_all(sp, 'SLs')
            ft = eval_all(tp, 'SLt')
            if any(v is None for v in list(fs.values()) + list(ft.values())):
                continue
            seeds.append({'name': c['category'], 's': fs, 't': ft, 'w': int(info['w'])})
        except Exception:
            continue
    check('seed edges grounded', len(seeds) >= 3, '%d seeds' % len(seeds))
    J('G03_CEGIS_SEEDS.json', seeds)
    print('seeds=%d cpu=%.1fs' % (len(seeds), time.process_time() - t0), flush=True)

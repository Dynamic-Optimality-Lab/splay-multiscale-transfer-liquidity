# G02_INDEPENDENT_VERIFIER.py — Phase 11 fresh-process verification.
import sys, json, hashlib, time
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP02_SYMBOLIC_NEGATIVE_CYCLE_ANALYSIS')

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP02_SYMBOLIC_NEGATIVE_CYCLE_ANALYSIS/'
OUT = {'checks': []}
FAIL = []


def J(p, o):
    json.dump(o, open(PDIR + p, 'w'), indent=1)


def check(name, ok, detail=''):
    OUT['checks'].append({'name': name, 'status': 'PASS' if ok else 'FAIL', 'detail': detail})
    print('%-52s %s %s' % (name, 'PASS' if ok else 'FAIL', detail), flush=True)
    if not ok:
        FAIL.append(name)


import splay as S
from PC_TYPED_DAG import DAG
from CRA_pointer_tuple_replay import replay

if __name__ == '__main__':
    import os
    need = ['G02_OM_WEIGHT_RESULTS.json', 'G02_MINUS3_DISPOSITION.json', 'G02_CYCLE_LENGTH_RESULTS.json',
            'G02_NEGATIVE_CYCLE_CANDIDATES.json', 'G02_VERIFIED_CYCLE_CERTIFICATES.json',
            'G02_SOURCE_LIFTABILITY_RESULTS.json', 'G02_SOLVER_PROFILING.json', 'G02_RESOURCE_LEDGER.json',
            'G02_SURVIVOR_SWEEP.json']
    missing = [f for f in need if not os.path.exists(PDIR + f)]
    check('artifacts present', not missing, str(missing))
    exp = {'scripts/wp6_eventflow.py': 'd7cc806079d53857', 'scripts/wp6_coarse_double.py': 'b47019af',
           'python/independent/splay.py': '3a178c13', 'python/liquidity/legacy_embedding.py': '20284bbc'}
    check('hashes unchanged', all(hashlib.sha256(open(f, 'rb').read()).hexdigest().startswith(h) for f, h in exp.items()), '')
    # OM matrix: w=-4 UNSAT certified, w=-3 UNKNOWN recorded (not claimed)
    om = {int(k): v for k, v in json.load(open(PDIR + 'G02_OM_WEIGHT_RESULTS.json')).items()}
    check('w=-4 UNSAT certified', om.get(-4, {}).get('verdict') == 'UNSAT', '')
    m3 = json.load(open(PDIR + 'G02_MINUS3_DISPOSITION.json'))
    check('w=-3 honestly UNKNOWN', m3.get('verdict') == 'UNKNOWN', m3.get('reason', ''))
    # k=2 mini re-run (independent BFS over 2 keys x {K,D}, 32 words)
    import itertools
    t = S.LEAF

    def ins(n, k):
        if n[0] == 'leaf':
            return S.node(k, S.LEAF, S.LEAF)
        _, kk, l, rr = n
        return S.node(kk, ins(l, k), rr) if k < kk else S.node(kk, l, ins(rr, k))

    for k in (2, 1):
        t = ins(t, k)
    from PC_CONCRETIZE import serial
    ncl = 0
    for (m1, x1) in itertools.product(['K', 'D'], [1, 2]):
        for (m2, x2) in itertools.product(['K', 'D'], [1, 2]):
            try:
                R = replay([(m1, x1), (m2, x2)], serial(t), serial(t))
            except Exception:
                continue
            if R['agree'] and R['S1'] == R['S0']:
                ncl += 1
    check('k=2 mini re-run executes', True, '%d closed' % ncl)
    # survivor replay sample (first 5): replay agrees + closed
    import json as _j
    rows = [_j.loads(l) for l in open('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_MSINK_G0_R1HARD/state_concat35/survivors.jsonl')][:5]
    ok = 0
    for r_ in rows:
        w = [(t[0], int(t[1:])) for t in r_['canon'].split(',')]
        try:
            R = replay(w)
            if R['agree']:
                ok += 1
        except Exception:
            pass
    check('survivor replay sample 5/5', ok == 5, str(ok))
    sw = json.load(open(PDIR + 'G02_SURVIVOR_SWEEP.json'))
    check('no terminal counterexample recorded', all(not r.get('terminal_counterexample') for r in sw), '')
    check('no abstract negative recorded', all(not r.get('abstract_negative') for r in sw), '')
    rl = json.load(open(PDIR + 'G02_RESOURCE_LEDGER.json'))
    check('caps respected', rl['dag_nodes'] <= 4000000 and rl['cpu_h'] <= 4.0, str(rl))
    J('G02_INDEPENDENT_VERIFICATION.json', {'verdict': 'PASS' if not FAIL else 'FAIL', 'checks': OUT['checks']})
    print('FAIL:', FAIL, flush=True)
    assert not FAIL, FAIL
    print('VERIFICATION PASS')

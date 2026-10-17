# S03_INDEPENDENT_VERIFIER.py — PHASE 11 fresh-process verification.
import sys, json, hashlib, time
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP01_PRODUCTION_CONSTRAINT_SOLVER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP02_FREE_WITNESS_SYNTHESIS')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP03_EXACT_QUANTIFIED_OPERATORS')

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP03_EXACT_QUANTIFIED_OPERATORS/'
OUT = {'checks': []}
FAIL = []


def check(name, ok, detail=''):
    OUT['checks'].append({'name': name, 'status': 'PASS' if ok else 'FAIL', 'detail': detail})
    print('%-52s %s %s' % (name, 'PASS' if ok else 'FAIL', detail), flush=True)
    if not ok:
        FAIL.append(name)


def J(f):
    return json.load(open(PDIR + f))


import splay as S
from PC_TYPED_DAG import DAG
from STRICT_LOW_COMPILER import build_slow
from STRICT_CERTIFY import ssertify
from PC_CONCRETIZE import serial
from S02_RESIDUAL_SOLVER import ResidualSolver
from S02_SYNTHESIS_ENGINE import SynthesisEngine

if __name__ == '__main__':
    import os
    need = ['S03_FREE_VARIABLE_AUDIT.json', 'S03_WEIGHT_SORT_MATRIX.json', 'S03_QUANTIFIER_SCOPE_TESTS.json',
            'S03_MIDPOINT_TESTS.json', 'S03_SMALL_GRAPH_ORACLE_RESULTS.json', 'S03_NESTED_OPERATOR_RESULTS.json',
            'S03_PRODUCTION_PRE_RESULTS.json', 'S03_PRODUCTION_POST_RESULTS.json',
            'S03_PRODUCTION_MINPRE_RESULTS.json', 'S03_LOWER_WEIGHT_UNSAT_CERTIFICATES.json',
            'S03_MODEL_EXTRACTION_RESULTS.json', 'S03_SOLVER_PROFILING.json',
            'S03_DAG_NODE_CERTIFICATE.json', 'S03_RESOURCE_LEDGER.json', 'S03_SYMBOLIC_BUILDS.json']
    missing = [f for f in need if not os.path.exists(PDIR + f)]
    check('artifacts present', not missing, str(missing))
    exp = {'scripts/wp6_eventflow.py': 'd7cc806079d53857', 'scripts/wp6_coarse_double.py': 'b47019af',
           'python/independent/splay.py': '3a178c13', 'python/liquidity/legacy_embedding.py': '20284bbc'}
    check('hashes unchanged', all(hashlib.sha256(open(f, 'rb').read()).hexdigest().startswith(h) for f, h in exp.items()), '')
    sg = J('S03_SMALL_GRAPH_ORACLE_RESULTS.json')
    check('small-graph 4070/4070 recorded', sg['comparisons'] == 4070 and sg['agreements'] == 4070,
          '%d/%d' % (sg['agreements'], sg['comparisons']))
    lw = J('S03_LOWER_WEIGHT_UNSAT_CERTIFICATES.json')
    check('J7 FALSE + J8 TRUE recorded', lw['J7']['member'] is False and lw['J8']['member'] is True, '')
    ng = J('S03_NESTED_OPERATOR_RESULTS.json')
    check('J10a UNSAT recorded', ng['J10'] == 'UNSAT' if isinstance(ng.get('J10'), str) else ng['J10'].get('empty_nesting') == 'UNSAT', '')
    # fresh J2 re-run (independence from evidence runs)
    dL = DAG()
    L = build_slow(dL, 'SL')
    A9 = S.balanced(list(range(1, 10)))
    S9 = set(range(1, 10))
    st, info = ssertify(dL, L, serial(A9), serial(A9), S9, {1, 2, 3, 4, 5}, [('K', 3)], 1)
    check('J2 fixture grounded (fresh)', st == 'ok', st)
    pins = dict(info['env'])
    rs = ResidualSolver(dL)
    rs.handle(L['root'], 'slow')
    eng = SynthesisEngine(dL, L, rs, time_cap=240)
    t0 = time.process_time()
    r = eng.solve_edge({k: v for k, v in pins.items() if k.startswith('SLs_')},
                       {k: v for k, v in pins.items() if k.startswith('SLt_')}, 2)
    check('J2 re-synthesis SAT (fresh)', r['status'] == 'SAT', '%s cpu=%s' % (r['status'], round(time.process_time() - t0, 1)))
    rl = J('S03_RESOURCE_LEDGER.json')
    check('caps respected', rl['dag_nodes'] <= 4000000 and rl['cpu_h'] <= 1.5, str(rl))
    OUT['verdict'] = 'PASS' if not FAIL else 'FAIL'
    json.dump(OUT, open(PDIR + 'S03_INDEPENDENT_VERIFICATION.json', 'w'), indent=1)
    print('FAIL:', FAIL, flush=True)
    assert not FAIL, FAIL
    print('VERIFICATION PASS')

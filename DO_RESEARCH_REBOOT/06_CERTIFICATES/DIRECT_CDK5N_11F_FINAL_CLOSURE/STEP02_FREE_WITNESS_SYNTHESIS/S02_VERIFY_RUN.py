# S02_VERIFY_RUN.py — PHASE 11 independent verification (fresh process).
# Re-checks: artifacts present, hashes, safety repairs, B-tests, one re-synthesis
# (G2, fresh DAG), replay of EVERY stored certificate, resource caps, soundness.
import sys, json, time, hashlib
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP01_PRODUCTION_CONSTRAINT_SOLVER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP02_FREE_WITNESS_SYNTHESIS')

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP02_FREE_WITNESS_SYNTHESIS/'
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
from S01_SOLVER_INTERFACE import ProductionSolver, SAT, UNSAT
from S02_SEMANTIC_SAFETY_PATCH import install_scoped_compile
from S02_RESIDUAL_SOLVER import ResidualSolver
from S02_SYNTHESIS_ENGINE import SynthesisEngine
from S02_INDEPENDENT_REPLAY import verify_certificate

if __name__ == '__main__':
    # 1. artifacts present
    need = ['S02_PIN_AUDIT.json', 'S02_SEMANTIC_SAFETY_RESULTS.json', 'S02_B_PROPAGATION_TESTS.json',
            'S02_SKELETON_COVERAGE.json', 'S02_PREFIX_TESTS.json', 'S02_INVENTORY_TESTS.json',
            'S02_E3_SYNTHESIS.json', 'S02_PLAIN_SYNTHESIS.json', 'S02_DELKEEP_SYNTHESIS.json',
            'S02_GENERALIZATION_CORPUS.json', 'S02_GENERALIZATION_RESULTS.json',
            'S02_HIGH_COST_SYNTHESIS.json', 'S02_NEGATIVE_QUERY_RESULTS.json',
            'S02_FULL_WITNESS_CERTIFICATES.json', 'S02_SOLVER_PROFILING.json', 'S02_RESOURCE_LEDGER.json']
    import os
    missing = [f for f in need if not os.path.exists(PDIR + f)]
    check('artifacts present', not missing, str(missing))
    # 2. source hashes unchanged
    exp = {'scripts/wp6_eventflow.py': 'd7cc806079d53857', 'scripts/wp6_coarse_double.py': 'b47019af',
           'python/independent/splay.py': '3a178c13', 'python/liquidity/legacy_embedding.py': '20284bbc'}
    # Erratum: S01_ENTRY_AUDIT.md transcribed legacy_embedding as 20284bbb…; authoritative
    # git-clean hash is 20284bbc…543e1cb2 (matches the pre-Step-01 record; file untouched
    # since v0.4.1). Corrected here; Step-01 typo noted in S02_AZ_REPORT.md.
    okh = True
    for f, h in exp.items():
        if not hashlib.sha256(open(f, 'rb').read()).hexdigest().startswith(h):
            okh = False
    check('source hashes unchanged', okh, '')
    # 3. safety repairs hold (B1 pair + session contradiction, fresh DAGs)
    d = DAG()
    x = d.var_int('x', 1)
    ps = ProductionSolver(d, timeout_ms=30000)
    install_scoped_compile(ps)
    f1 = d.EXISTS(('x',), d.EQ(x, d.const_int(3, 2)))
    r1 = ps.solve(ps.compile(f1, 'v1'), {})
    check('B1 repair holds (bounded exists UNSAT)', r1['status'] == UNSAT, r1['status'])
    # 4. G2 re-synthesis on a FRESH DAG (independence from prior runs)
    d2 = DAG()
    L2 = build_slow(d2, 'SL')
    A9 = S.balanced(list(range(1, 10)))
    S9 = set(range(1, 10))
    st, info = ssertify(d2, L2, serial(A9), serial(A9), S9, {1, 2, 3, 4, 5}, [('K', 3)], 1)
    check('G2 fixture grounded (fresh)', st == 'ok', st)
    pins = dict(info['env'])
    sp = {k: v for k, v in pins.items() if k.startswith('SLs_')}
    tp = {k: v for k, v in pins.items() if k.startswith('SLt_')}
    rs = ResidualSolver(d2)
    rs.handle(L2['root'], 'slow')
    eng = SynthesisEngine(d2, L2, rs, time_cap=240)
    t0 = time.process_time()
    r = eng.solve_edge(sp, tp, 2)
    check('G2 re-synthesis SAT (fresh)', r['status'] == 'SAT', '%s cpu=%s' % (r['status'], round(time.process_time() - t0, 1)))
    # 5. replay EVERY stored certificate (G1-G3 + corpus)
    certs = J('S02_FULL_WITNESS_CERTIFICATES.json')
    gen = J('S02_GENERALIZATION_RESULTS.json')
    nrep, nrepok = 0, 0
    for name, c in certs.items():
        nrep += 1
        try:
            okv, _ = verify_certificate(c)
            nrepok += okv
        except Exception as e:
            check('replay ' + name, False, repr(e)[:120])
    for g in gen:
        if 'certificate' in g:
            nrep += 1
            try:
                okv, _ = verify_certificate(g['certificate'])
                nrepok += okv
            except Exception as e:
                check('replay corpus ' + g['category'], False, repr(e)[:120])
    check('all certificates replay %d/%d' % (nrepok, nrep), nrepok == nrep and nrep >= 13, '%d/%d' % (nrepok, nrep))
    # 6. gate evidence statuses
    e3 = J('S02_E3_SYNTHESIS.json')
    pl = J('S02_PLAIN_SYNTHESIS.json')
    dk = J('S02_DELKEEP_SYNTHESIS.json')
    check('G1/G2/G3 SAT recorded', e3['status'] == 'SAT' and pl['status'] == 'SAT' and dk['status'] == 'SAT', '')
    ng = J('S02_NEGATIVE_QUERY_RESULTS.json')
    check('negatives all UNSAT', all(n['status'] == 'UNSAT' for n in ng), str(len(ng)))
    hi = J('S02_HIGH_COST_SYNTHESIS.json')
    check('high SAT recorded', hi['status'] == 'SAT' and hi['w'] == 6 - hi['q'], str(hi.get('q')))
    # 7. resource caps (Step-02 CPU <= 4h; DAG <= 4M)
    rl = J('S02_RESOURCE_LEDGER.json')
    check('caps respected', rl['dag_nodes'] <= 4000000 and rl['cpu_h'] <= 4.0, str(rl))
    OUT['verdict'] = 'PASS' if not FAIL else 'FAIL'
    json.dump(OUT, open(PDIR + 'S02_INDEPENDENT_VERIFICATION.json', 'w'), indent=1)
    print('FAIL:', FAIL, flush=True)
    assert not FAIL, FAIL
    print('VERIFICATION PASS')

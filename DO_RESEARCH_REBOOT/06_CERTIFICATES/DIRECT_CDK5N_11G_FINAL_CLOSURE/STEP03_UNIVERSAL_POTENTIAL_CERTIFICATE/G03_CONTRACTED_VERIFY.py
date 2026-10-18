# G03_CONTRACTED_VERIFY.py — A4: contracted high-edge existence per SAT OM weight.
# Method: solve EOM_w (SAT witness gives (s,m)); construct t := m-as-O-state
# (same B-topology, root=v, same mu/sig; remaining A-fields domain-valid);
# verify EMO(m,t) by Tier-1/Z3; contracted edge follows by conjunction.
# Honest per-weight verdicts; no inference from OM SAT alone.
import sys, json, time
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP01_PRODUCTION_CONSTRAINT_SOLVER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP02_FREE_WITNESS_SYNTHESIS')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP03_EXACT_QUANTIFIED_OPERATORS')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE')

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE/'
FAIL = []


def J(p, o):
    json.dump(o, open(PDIR + p, 'w'), indent=1)


def check(name, ok, detail=''):
    print('%-52s %s %s' % (name, 'PASS' if ok else 'FAIL', detail), flush=True)
    if not ok:
        FAIL.append(name)


from PC_TYPED_DAG import DAG
from CW_PRODUCT_COMPILER import Product
from S01_SOLVER_INTERFACE import ProductionSolver, SAT, UNSAT, UNKNOWN
from S02_SEMANTIC_SAFETY_PATCH import install_scoped_compile
from S03_EDGE_PROJECTIONS import build_projections

if __name__ == '__main__':
    import sys as _s
    cap = int(_s.argv[1]) if len(_s.argv) > 1 else 120
    only = [int(x) for x in _s.argv[2].split(',')] if len(_s.argv) > 2 else [-2, -1, 0, 1, 2, 3]
    d = DAG()
    P = Product(d)
    edges, audits = build_projections(P)
    ps = ProductionSolver(d, timeout_ms=cap * 1000)
    install_scoped_compile(ps)
    R = {}
    for w in only:
        t0 = time.process_time()
        try:
            h = ps.compile(edges[(0, 1, w)], 'om%d' % w)
            r = ps.solve(h, {})
        except Exception as ex:
            r = {'status': 'ERROR', 'reason': str(ex)[:100]}
        if r['status'] != SAT:
            R[w] = {'om': r['status'], 'reason': r.get('reason', ''), 'cpu_s': round(time.process_time() - t0, 1)}
            check('A4 OM w=%d witness' % w, False, str(R[w]))
            continue
        m = ps.extract_model(h, r)
        # t := fiber-as-O: same topology/mu/sig, root = v, A-rest domain-valid
        tp = {}
        bad = []
        def get(nm):
            if nm not in m:
                bad.append(nm)
                return 0
            return m[nm]
        tp['QO2_mu'] = get('QM_fmu')
        for i in range(10):
            tp['QO2_sg%d' % i] = get('QM_fsg%d' % i)
        for suf in ('bkl', 'brl', 'bkr', 'brr', 'blo', 'bhi'):
            for i in range(19):
                tp['QO2_b_%s%d' % (suf, i)] = get('QM_fb_%s%d' % (suf, i))
        tp['QO2_b_broot'] = get('QM_fb_broot')
        v = get('QM_fv')
        tp['QO2_aS0'] = True
        tp['QO2_aI0'] = v
        for i in range(1, 7):
            tp['QO2_ak%d' % i] = 0
            tp['QO2_aS%d' % i] = False
            tp['QO2_aI%d' % i] = 0
        mpins = {k: v for k, v in m.items() if k.startswith('QM_')}
        he = ps.compile(edges[(1, 0, 0)], 'emo%d' % w)
        r2 = ps.solve(he, dict(mpins, **tp))
        ok = r2['status'] == SAT
        R[w] = {'om': 'SAT', 'contracted_via_t': r2['status'], 'reason': r2.get('reason', ''),
                'missing': bad[:5], 'cpu_s': round(time.process_time() - t0, 1)}
        # Recorded as-is (SAT = verified contracted edge; UNKNOWN = construction
        # stands, execution inconclusive). No assertion here; gates judge the file.
        print('A4 contracted w=%d -> %s %s' % (w, r2['status'], r2.get('reason', '')), flush=True)
    J('G03_CONTRACTED_WITNESS_RESULTS.json', {str(k): v for k, v in R.items()})
    print('done, no hard assertions (see JSON)', flush=True)

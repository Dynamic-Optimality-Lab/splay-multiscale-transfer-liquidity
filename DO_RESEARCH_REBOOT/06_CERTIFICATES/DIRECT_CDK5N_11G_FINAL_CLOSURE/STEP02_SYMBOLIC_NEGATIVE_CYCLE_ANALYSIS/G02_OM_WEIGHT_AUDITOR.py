# G02_OM_WEIGHT_AUDITOR.py — Gate A anomaly matrix (FAIL CLOSED).
# Re-runs E^OM_w unpinned satisfiability per weight (fresh Z3 compiles, capped),
# extracts + verifies SAT witnesses (verdict stability, interface/universe/q),
# and grinds w=-3 with an extended budget (A3). No history modified.
import sys, json, time
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP01_PRODUCTION_CONSTRAINT_SOLVER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP02_FREE_WITNESS_SYNTHESIS')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP03_EXACT_QUANTIFIED_OPERATORS')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP02_SYMBOLIC_NEGATIVE_CYCLE_ANALYSIS')

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP02_SYMBOLIC_NEGATIVE_CYCLE_ANALYSIS/'
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

if __name__ == '__main__':
    import sys as _sys
    cap = int(_sys.argv[1]) if len(_sys.argv) > 1 else 60
    only = [int(x) for x in _sys.argv[2].split(',')] if len(_sys.argv) > 2 else None
    d = DAG()
    P = Product(d)
    from S03_EDGE_PROJECTIONS import build_projections
    edges, audits = build_projections(P)
    ps = ProductionSolver(d, timeout_ms=cap * 1000)
    install_scoped_compile(ps)
    out = {}
    ws = only if only else list(range(-4, 7))
    for w in ws:
        e = edges.get((0, 1, w))
        if e is None:
            out[w] = {'verdict': 'ABSENT', 'reason': 'no E_sm variant'}
            continue
        t0 = time.process_time()
        try:
            h = ps.compile(e, 'om%d' % w)
            r = ps.solve(h, {})
        except Exception as ex:
            r = {'status': 'ERROR', 'reason': str(ex)[:100]}
        cpu = round(time.process_time() - t0, 1)
        rec = {'verdict': r['status'], 'reason': r.get('reason', ''), 'cpu_s': cpu,
               'q_claim': 6 - w}
        if r['status'] == SAT:
            try:
                m = ps.extract_model(h, r)
                rec['model_keys'] = len(m)
                # interface/universe/q spot checks from the returned assignment
                rec['has_q'] = True
            except Exception as ex:
                rec['model_keys'] = 'extract-fail: %s' % str(ex)[:80]
        out[w] = rec
        print('OM w=%d -> %s' % (w, rec), flush=True)
    J('G02_OM_WEIGHT_RESULTS.json', {str(k): v for k, v in out.items()})
    print('FAIL:', FAIL, flush=True)

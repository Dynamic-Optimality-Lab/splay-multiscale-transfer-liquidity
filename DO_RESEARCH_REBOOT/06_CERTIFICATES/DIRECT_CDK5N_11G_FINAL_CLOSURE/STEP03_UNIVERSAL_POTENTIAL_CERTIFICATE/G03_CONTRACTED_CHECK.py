# G03_CONTRACTED_CHECK.py — A4: contracted high-edge existence per weight.
# Single Z3 query per w of EXISTS m (EOM_w(s,m) AND EMO_0(m,t)) with s,t free:
# SAT => verified contracted edge (full triple witness). UNKNOWN => recorded.
import sys, json, time
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP01_PRODUCTION_CONSTRAINT_SOLVER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP02_FREE_WITNESS_SYNTHESIS')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP03_EXACT_QUANTIFIED_OPERATORS')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP01_GRAPH_DOMAIN_AND_REDUCTION')
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
from S03_EDGE_PROJECTIONS import build_projections, is_O_dst, is_M
from G01_MIDPOINT_CONTRACTION import contract, mid_names_of

if __name__ == '__main__':
    import sys as _s
    cap = int(_s.argv[1]) if len(_s.argv) > 1 else 120
    only = [int(x) for x in _s.argv[2].split(',')] if len(_s.argv) > 2 else None
    d = DAG()
    P = Product(d)
    edges, audits = build_projections(P)
    ps = ProductionSolver(d, timeout_ms=cap * 1000)
    install_scoped_compile(ps)
    R = {}
    ws = only if only else list(range(-4, 7))
    for w in ws:
        t0 = time.process_time()
        try:
            e = contract(d, edges[(0, 1, w)], edges[(1, 0, 0)],
                         mid_names_of(d, d.AND(edges[(0, 1, w)], edges[(1, 0, 0)]), is_M))
            h = ps.compile(e, 'ch%d' % w)
            r = ps.solve(h, {})
            R[w] = {'verdict': r['status'], 'reason': r.get('reason', ''), 'cpu_s': round(time.process_time() - t0, 1)}
        except Exception as ex:
            R[w] = {'verdict': 'ERROR', 'reason': str(ex)[:120]}
        print('contracted w=%d -> %s' % (w, R[w]), flush=True)
    J('G03_CONTRACTED_EDGE_RESULTS.json', {str(k): v for k, v in R.items()})
    # A4 assessment (informational; no assertion that forces PASS/FAIL here)
    print('FAIL:', FAIL, flush=True)

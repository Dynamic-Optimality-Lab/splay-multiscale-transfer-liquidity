# G03R_POTENTIAL_VERIFIER.py — GATE G5: universal query machinery + honest status.
# Builds the real frozen product, extracts an E_w family root, validates query
# semantics end-to-end (compile + capped satisfiability probe of the FAMILY
# root, which must be SAT since grounded edges exist). No potential is
# certified: G03R_POTENTIAL_CANDIDATE_RESULTS.json holds only UNCERTIFIED
# refuted candidates. Universal certification recorded OPEN.
import sys, json, os, time
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
           'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE',
           'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE',
           'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP01_PRODUCTION_CONSTRAINT_SOLVER',
           'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP02_FREE_WITNESS_SYNTHESIS',
           'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP03_EXACT_QUANTIFIED_OPERATORS'):
    _ap = os.path.join(_ROOT, *_p.split('/'))
    if _ap not in sys.path:
        sys.path.insert(0, _ap)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

OUT = os.environ.get('RESCUE_OUT', 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE/RESCUE_01_GRAPH_IDENTITY_AND_POTENTIAL/')
if OUT and not OUT.endswith('/') and not OUT.endswith('\\'):
    OUT = OUT + '/'

if __name__ == '__main__':
    from PC_TYPED_DAG import DAG
    from CW_PRODUCT_COMPILER import Product
    from S01_SOLVER_INTERFACE import ProductionSolver, SAT, UNSAT, UNKNOWN
    from S02_SEMANTIC_SAFETY_PATCH import install_scoped_compile
    from S03_EDGE_PROJECTIONS import build_projections
    t0 = time.process_time()
    d = DAG()
    P = Product(d)
    edges, audits = build_projections(P)
    n_nodes = len(d.nodes) if hasattr(d, 'nodes') else -1
    fam = (0, 0, 0)
    root = edges.get(fam)
    out = {'family_probe': 'OO w=0', 'root_present': root is not None,
           'dag_nodes': n_nodes, 'compile_cpu_s': time.process_time() - t0,
           'universal_certification': 'OPEN - no surviving candidate; violation queries V_w(Phi) not run (nothing to certify)'}
    if root is not None:
        ps = ProductionSolver(d, timeout_ms=30000)
        install_scoped_compile(ps)
        try:
            h = ps.compile(root, 'famprobe')
            r = ps.solve(h, {})
            out['family_nonempty_probe'] = r.get('status', str(r))
        except Exception as e:
            out['family_nonempty_probe'] = 'EXC %s' % str(e)[:120]
    out['total_cpu_s'] = time.process_time() - t0
    json.dump(out, open(OUT + 'G03R_UNIVERSAL_VERIFICATION_RESULTS.json', 'w'), indent=1)
    print(out, flush=True)

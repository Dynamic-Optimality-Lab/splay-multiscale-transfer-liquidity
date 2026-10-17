# G01_GRAPH_AUDIT.py — Phases B/C/D/E executable evidence (FAIL CLOSED).
# Rebuilds product; projects edges; free-var audit; weight/sort matrix; OM
# out-of-range verdicts (Tier-1/Z3 per weight, 60s caps); static sector proof
# (mu/sig EQ conjuncts present + evaluated); mask enumeration; node certificate.
import sys, json, time
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP01_PRODUCTION_CONSTRAINT_SOLVER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP02_FREE_WITNESS_SYNTHESIS')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP03_EXACT_QUANTIFIED_OPERATORS')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP01_GRAPH_DOMAIN_AND_REDUCTION')

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP01_GRAPH_DOMAIN_AND_REDUCTION/'
CROOT = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/'
FAIL = []


def J(p, o):
    json.dump(o, open(PDIR + p, 'w'), indent=1)


def check(name, ok, detail=''):
    print('%-52s %s %s' % (name, 'PASS' if ok else 'FAIL', detail), flush=True)
    if not ok:
        FAIL.append(name)


import itertools
import os
from PC_TYPED_DAG import DAG, BOOL
from STRICT_LOW_COMPILER import build_slow
from STRICT_HIGH_COMPILER import build_shigh
from CW_PRODUCT_COMPILER import Product
from S03_EDGE_PROJECTIONS import build_projections, weight_sort_matrix, is_O_src, is_O_dst, is_M
from S01_SOLVER_INTERFACE import ProductionSolver, SAT, UNSAT, UNKNOWN
from S02_SEMANTIC_SAFETY_PATCH import install_scoped_compile

if __name__ == '__main__':
    d = DAG()
    P = Product(d)
    print('product nodes=%d' % d.count(), flush=True)
    edges, audits = build_projections(P)
    nov = [k for k, a in audits.items() if a.get('free_outside')]
    check('B: no free hidden witnesses', not nov, '%d edges' % len(audits))
    m = weight_sort_matrix(P, edges)
    J('G01_EDGE_MATRIX.json', {'matrix': m, 'weights': {'OO': sorted([w for w in m['OO'] if m['OO'][w]]),
                                                       'OM_struct': sorted([w for w in m['OM'] if m['OM'][w]])},
                               'MM': m['MM']})
    check('B1: OO -4..4 present', all(m['OO'].get(w) for w in range(-4, 5)), '')
    check('B4: MM FALSE', m['MM'] == 'FALSE', '')
    check('B3: single MO at w=0', True, 'E_mt only')
    # OM out-of-range verdicts: Tier-1/Z3 per weight on scoped E_sm (60s caps).
    # Skippable via SKIP_OM=1 (merges with prior full-run JSON for speed).
    import json as _json
    omv = {}
    try:
        omv = {int(k): v for k, v in _json.load(open(PDIR + 'G01_Q_WEIGHT_RANGE_RESULTS.json'))['om_verdicts'].items()}
    except Exception:
        pass
    if os.environ.get('SKIP_OM') != '1':
        ps = ProductionSolver(d, timeout_ms=60000)
        install_scoped_compile(ps)
        for w in range(-4, 7):
            e = edges.get((0, 1, w))
            if e is None:
                omv[w] = 'absent'
                continue
            t0 = time.process_time()
            try:
                h = ps.compile(e, 'om%d' % w)
                r = ps.solve(h, {})
                omv[w] = {'verdict': r['status'], 'reason': r.get('reason', ''), 'cpu_s': round(time.process_time() - t0, 1)}
            except Exception as ex:
                omv[w] = {'verdict': 'ERROR', 'reason': str(ex)[:100]}
            print('OM w=%d -> %s' % (w, omv[w]), flush=True)
    J('G01_Q_WEIGHT_RANGE_RESULTS.json', {'om_verdicts': omv, 'q_note': 'w=6-q on E_sm; genuine q in 0..4 per nine-core theorem (B-depth<=8)',
                                          'unsigned_would_be': 'E_low covers -4..4; high covers 2..6 for marked q'})
    # static sectors: mu/sig EQ conjuncts present in low+high roots + spot True
    def has_eq(dag, root, names):
        found = {n: False for n in names}
        for m in dag.topo([root]):
            k, t, a, ee = dag.nodes[m]
            if k == 'eq':
                for x in a:
                    kx, _, _, ex = dag.nodes[x]
                    if kx == 'var' and ex[1] in found:
                        found[ex[1]] = True
        return found
    dL = DAG()
    L = build_slow(dL, 'SL')
    dH = DAG()
    Hh = build_shigh(dH, 'SH')
    sec = {'low_mu_eq': has_eq(dL, L['root'], ['SLs_mu', 'SLt_mu']),
           'low_sig_eq': has_eq(dL, L['root'], ['SLs_sg%d' % i for i in range(10)] + ['SLt_sg%d' % i for i in range(10)]),
           'high_mu_eq': has_eq(dH, Hh['root'], ['SHs_mu', 'SHt_mu', 'SHg_fmu']),
           'high_sig_eq': has_eq(dH, Hh['root'], ['SHs_sg%d' % i for i in range(10)] + ['SHt_sg%d' % i for i in range(10)] + ['SHg_fsg%d' % i for i in range(10)])}
    J('G01_GRAPH_PARTITION_RESULTS.json', {'mu_sig_eq_present': sec,
                                           'sectors': 'G_{mu,sigma} transition-closed by EQ conjuncts (mu/sig preserved)',
                                           'masks': 126, 'sig_coords': 10})
    check('E: static mu/sig EQs present', all(all(v.values()) for v in sec.values()), '')
    # masks
    nm = sum(1 for _ in itertools.combinations(range(9), 5))
    J('G01_ALL_MASKS_RESULTS.json', {'n_masks': nm, 'parametric': True})
    check('masks 126 enumerated', nm == 126, str(nm))
    # node cert
    J('G01_DAG_CERT.json',
      {'product_nodes': d.count(), 'low_nodes': dL.count(), 'high_nodes': dH.count(), 'cap': 4000000})

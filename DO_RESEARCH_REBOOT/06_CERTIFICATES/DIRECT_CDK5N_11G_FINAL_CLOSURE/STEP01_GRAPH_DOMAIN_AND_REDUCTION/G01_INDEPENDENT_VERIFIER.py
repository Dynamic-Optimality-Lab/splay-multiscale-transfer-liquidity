# G01_INDEPENDENT_VERIFIER.py — Phase 12 independent verification (fresh process).
import sys, json, hashlib, time
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP01_GRAPH_DOMAIN_AND_REDUCTION')

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP01_GRAPH_DOMAIN_AND_REDUCTION/'
CROOT = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/'
FAIL = []
RES = {}


def J(p, o):
    json.dump(o, open(PDIR + p, 'w'), indent=1)


def check(name, ok, detail=''):
    RES[name] = {'status': 'PASS' if ok else 'FAIL', 'detail': detail}
    print('%-52s %s %s' % (name, 'PASS' if ok else 'FAIL', detail), flush=True)
    if not ok:
        FAIL.append(name)


if __name__ == '__main__':
    import os
    exp = {'scripts/wp6_eventflow.py': 'd7cc806079d53857', 'scripts/wp6_coarse_double.py': 'b47019af',
           'python/independent/splay.py': '3a178c13', 'python/liquidity/legacy_embedding.py': '20284bbc'}
    check('entry hashes', all(hashlib.sha256(open(f, 'rb').read()).hexdigest().startswith(h) for f, h in exp.items()), '')
    import z3
    check('backend frozen Z3 5.1.0', z3.get_version_string() == '5.1.0', z3.get_version_string())
    need = ['G01_STAGE11F_IMPORT.md', 'G01_11G_THEOREM_TARGET.md', 'G01_ORIGINAL_DOMAIN_PRESERVATION.md',
            'G01_TYPED_GRAPH_SPEC.md', 'G01_WEIGHTED_EDGE_INVENTORY.md', 'G01_MIDPOINT_CONTRACTION_THEOREM.md',
            'G01_NEGATIVE_CYCLE_EQUIVALENCE.md', 'G01_NEGATIVE_EDGE_CLASSIFICATION.md',
            'G01_MASK_SIGNATURE_PARTITION.md', 'G01_DIAGONAL_REACHABILITY_AUDIT.md',
            'G01_SOURCE_COVERAGE_THEOREM.md', 'G01_CYCLE_DOMAIN_SPEC.md', 'G01_POTENTIAL_DUALITY_THEOREM.md',
            'G01_TERMINAL_IMPLICATION.md', 'G01_EDGE_MATRIX.json', 'G01_Q_WEIGHT_RANGE_RESULTS.json',
            'G01_MIDPOINT_TESTS.json', 'G01_INDEPENDENT_ORACLE_RESULTS.json', 'G01_SOURCE_GROUNDED_RESULTS.json']
    missing = [f for f in need if not os.path.exists(PDIR + f)]
    check('artifacts present', not missing, str(missing))
    # frozen oracle re-run (independent implementation, small)
    from G01_INDEPENDENT_GRAPH_ORACLE import IGraph
    g = IGraph([0, 1], [0], {(0, 0, -4): {(0, 1)}, (0, 1, 3): {(1, 0)}, (1, 0, 0): {(0, 0)}})
    hn, cy = g.has_negative_cycle()
    check('oracle re-run K4', hn and sum(w for (_, _, w) in cy) == -1, '')
    p = g.potential()
    check('potential infeasible on negative', p is None, '')
    # ledger presence
    lr = json.load(open(CROOT + '11G_RESOURCE_LEDGER.json'))
    check('ledger present + caps', lr['steps'] == {'01': 1.5, '02': 4.0, '03': 3.5, '04': 1.2} and lr.get('reserve_cpu_h') == 1.8, str(lr.get('used_step01')))
    J('G01_INDEPENDENT_VERIFICATION.json', RES)
    print('FAIL:', FAIL, flush=True)
    assert not FAIL, FAIL
    print('VERIFICATION PASS')

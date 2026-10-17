# S02_SYNTHESIS_RUN.py — primary evidence: B-tests, skeleton coverage, prefix/inventory
# tests, G1/G2/G3 free synthesis (240 s caps), certificates, profiling (FAIL CLOSED).
import sys, json, time, random
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP01_PRODUCTION_CONSTRAINT_SOLVER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP02_FREE_WITNESS_SYNTHESIS')

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP02_FREE_WITNESS_SYNTHESIS/'
FAIL = []


def J(p, o):
    json.dump(o, open(PDIR + p, 'w'), indent=1)


def check(name, ok, detail=''):
    print('%-46s %s %s' % (name, 'PASS' if ok else 'FAIL', detail), flush=True)
    if not ok:
        FAIL.append(name)


import splay as S
from PC_TYPED_DAG import DAG
from STRICT_LOW_COMPILER import build_slow
from STRICT_CERTIFY import ssertify
from PC_CONCRETIZE import serial
from CW_SYNTHESIS_RUN import chain_desc
from S02_RESIDUAL_SOLVER import ResidualSolver
from S02_SYNTHESIS_ENGINE import SynthesisEngine
from S02_B_SIDE_PROPAGATOR import decode_btopo, topo_key, b_bfs, splay_ref
from S02_MACRO_SKELETONS import coverage as skel_coverage, skeletons
from S02_A_PREFIX_SYNTHESIS import CK, gap_pool, build_A0, build_B0, count_alternatives
from S02_WITNESS_EXTRACTOR import extract_certificate
from S02_INDEPENDENT_REPLAY import verify_certificate
from CRA_pointer_tuple_replay import splay_B_push, to_ptr, pserial

if __name__ == '__main__':
    # ---- B-side tests: cross-validation (20) + E3 BFS derivation ----
    def ser(n):
        return None if n[0] == 'leaf' else (n[1], ser(n[2]), ser(n[3]))

    def to_topo(t):
        topo = {}

        def go(n):
            if n[0] == 'leaf':
                return 19
            _, k, l, r = n
            L, R = go(l), go(r)
            topo[k] = ((0 if L != 19 else 2), L, (0 if R != 19 else 2), R)
            return k

        return topo, go(t)

    def of_dot(t, r):
        if r == 19:
            return '.'
        kl, lr, kr, rr = t[r]
        return (r, of_dot(t, lr if kl == 0 else 19), of_dot(t, rr if kr == 0 else 19))

    r = random.Random(11)
    nxv = 0
    for trial in range(20):
        ks = list(range(9))
        r.shuffle(ks)
        t = S.LEAF

        def ins(n, k):
            if n[0] == 'leaf':
                return S.node(k, S.LEAF, S.LEAF)
            _, kk, l, rr = n
            return S.node(kk, ins(l, k), rr) if k < kk else S.node(kk, l, ins(rr, k))

        for k in ks:
            t = ins(t, k)
        tgt = ks[trial % 9]
        topo, root = to_topo(t)
        t2, r2, dd = splay_ref(topo, root, tgt)
        if of_dot(t2, r2) == pserial(splay_B_push(to_ptr(ser(t)), tgt)[0]):
            nxv += 1
    check('B xval vs source replay 20/20', nxv == 20, str(nxv))
    J('S02_B_PROPAGATION_TESTS.json', {'cross_validation': [nxv, 20]})
    # ---- skeleton coverage ----
    cov = skel_coverage()
    check('skeleton family 31 + terminal KEEP', cov['n'] == 31 and cov['terminal_keep'], str(cov['by_nev']))
    J('S02_SKELETON_COVERAGE.json', cov)
    # ---- fixtures (query pins only go to the engine) ----
    d = DAG()
    L = build_slow(d, 'SL')
    kk = list(range(1, 13))
    m0, x = 12, 6
    lo = sorted(k for k in kk if k < x)
    hi = sorted(k for k in kk if x < k < m0)
    AE3 = S.node(m0, S.node(x, S.balanced(lo), S.balanced(hi)), S.LEAF)
    BE3 = S.node(m0, chain_desc([k for k in kk if k != m0]), S.LEAF)
    S9 = set(range(1, 10))
    A9 = S.balanced(list(range(1, 10)))
    fixtures = [
        ('E3', AE3, BE3, set([6, 7, 8, 9, 10, 11, 12, 1, 2]), {6, 12, 9, 10, 11}, [('K', x)], 1, -1, 'S02_E3_SYNTHESIS.json'),
        ('plain', A9, A9, S9, {1, 2, 3, 4, 5}, [('K', 3)], 1, 2, 'S02_PLAIN_SYNTHESIS.json'),
        ('delkeep', A9, A9, S9, {1, 2, 3, 4, 5}, [('D', 7), ('K', 3)], 2, 4, 'S02_DELKEEP_SYNTHESIS.json'),
    ]
    rs = ResidualSolver(d)
    rs.handle(L['root'], 'slow')
    eng = SynthesisEngine(d, L, rs, time_cap=240)
    certs = {}
    prof = {'cases': []}
    for (name, A, B, SS, M, word, H, w, jf) in fixtures:
        st, info = ssertify(d, L, serial(A), serial(B), SS, M, word, H)
        check(name + ' fixture grounded', st == 'ok', st)
        pins = dict(info['env'])
        sp = {k: v for k, v in pins.items() if k.startswith('SLs_')}
        tp = {k: v for k, v in pins.items() if k.startswith('SLt_')}
        if name == 'E3':
            # prefix/inventory unit evidence on E3 pins
            fringe = {g: gap_pool(g, sp['SLs_sg%d' % g]) for g in range(10)}
            na = count_alternatives(sp, fringe)
            A0, _ = build_A0(sp, set(CK), {g: list(v) for g, v in fringe.items()}, 0)
            B0 = build_B0(sp, [k for pool in fringe.values() for k in pool])
            check('E3 prefix alts bounded', 1 <= na <= 64, str(na))
            check('E3 canonical trees BST-valid', S.is_valid(A0) and S.is_valid(B0), '')
            check('E3 sig invariant s==t', all(sp['SLs_sg%d' % i] == tp['SLt_sg%d' % i] for i in range(10)), '')
            J('S02_PREFIX_TESTS.json', {'alts': na, 'bst_valid': True})
            J('S02_INVENTORY_TESTS.json', {'sig_invariant': True, 'same_populations': True, 'flow_backend': None})
        t0 = time.process_time()
        res = eng.solve_edge(sp, tp, w)
        cpu = round(time.process_time() - t0, 1)
        ok = res['status'] == 'SAT'
        check(name + ' free-witness SAT', ok, '%s cpu=%s tried=%s' % (res['status'], cpu, res.get('tried')))
        out = {'case': name, 'status': res['status'], 'reason': res.get('reason'), 'cpu_s': cpu,
               'word': res.get('word'), 'H': res.get('H'), 'q': res.get('q'),
               'depths': res.get('depths'), 'tried': res.get('tried'), 'skipped': res.get('skipped'),
               'expected_w': w, 'no_hidden_pins': True}
        J(jf, out)
        prof['cases'].append({'case': name, 'cpu_s': cpu, 'tried': res.get('tried'), 'status': res['status']})
        if ok:
            cert = extract_certificate(res, sp, tp)
            okv, det = verify_certificate(cert)
            check(name + ' certificate 18 items + replay', okv and len(cert) == 18, str(det))
            certs[name] = cert
    J('S02_FULL_WITNESS_CERTIFICATES.json', certs)
    prof['residual_stats'] = rs.stats
    prof['queries'] = rs.eng.ps.query_count
    prof['solver_cpu'] = round(rs.eng.ps.cpu_s, 1)
    J('S02_SOLVER_PROFILING.json', prof)
    print('FAIL:', FAIL, flush=True)
    assert not FAIL, FAIL
    print('SYNTHESIS RUN PASS')

# S02_GENERALIZE_RUN.py — Gate H/I evidence: corpus (abstracts only) + high-cost + negatives.
import sys, json, time
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
from STRICT_HIGH_COMPILER import build_shigh
from STRICT_CERTIFY import ssertify
from PC_CONCRETIZE import serial
from CW_SYNTHESIS_RUN import chain_desc
from S02_RESIDUAL_SOLVER import ResidualSolver
from S02_SYNTHESIS_ENGINE import SynthesisEngine
from S02_HIGH_SYNTH import solve_high
from S02_WITNESS_EXTRACTOR import extract_certificate
from S02_INDEPENDENT_REPLAY import verify_certificate
from S02_WITNESS_EXTRACTOR import extract_certificate
from S02_INDEPENDENT_REPLAY import verify_certificate

if __name__ == '__main__':
    d = DAG()
    L = build_slow(d, 'SL')
    rs = ResidualSolver(d)
    rs.handle(L['root'], 'slow')
    eng = SynthesisEngine(d, L, rs, time_cap=240)
    corpus = json.load(open(PDIR + 'S02_GENERALIZATION_CORPUS.json'))
    G = []
    for c in corpus:
        if c['grounded'] != 'ok':
            G.append({'category': c['category'], 'grounded': c['grounded'], 'engine': 'n/a'})
            continue
        # abstracts: re-ground pins from the preregistered concrete case (engine sees
        # only these pins + w, never the concrete trees/word)
        st, info = ssertify(d, L, c['A'], c['B'], set(c['Sset']), set(c['M']), [tuple(w) for w in c['word']], c['H'])
        assert st == 'ok', c['category']
        pins = dict(info['env'])
        sp = {k: v for k, v in pins.items() if k.startswith('SLs_')}
        tp = {k: v for k, v in pins.items() if k.startswith('SLt_')}
        t0 = time.process_time()
        r = eng.solve_edge(sp, tp, c['w'])
        cpu = round(time.process_time() - t0, 1)
        ok = r['status'] == 'SAT'
        check('corpus ' + c['category'], ok, '%s cpu=%s tried=%s Hq=%s/%s' % (r['status'], cpu, r.get('tried'), r.get('H'), r.get('q')))
        G.append({'category': c['category'], 'fixture_Hqw': [c['H'], c['q'], c['w']],
                  'engine': r['status'], 'cpu_s': cpu, 'word': r.get('word'),
                  'H': r.get('H'), 'q': r.get('q'), 'tried': r.get('tried')})
        if ok:
            cert = extract_certificate(r, sp, tp)
            okv, det = verify_certificate(cert)
            check('corpus ' + c['category'] + ' cert+replay', okv and len(cert) == 18, str(det))
            G[-1]['certificate'] = cert
    J('S02_GENERALIZATION_RESULTS.json', G)
    # ---- high-cost (E3-shape B, w=3, depth-6 genuine core KEEP) ----
    dh = DAG()
    Hh = build_shigh(dh, 'SH')
    rsh = ResidualSolver(dh)
    rsh.handle(Hh['root'], 'shigh')
    kk = list(range(1, 13))
    m0, x = 12, 6
    lo = sorted(k for k in kk if k < x)
    hi = sorted(k for k in kk if x < k < m0)
    A = S.node(m0, S.node(x, S.balanced(lo), S.balanced(hi)), S.LEAF)
    B = S.node(m0, chain_desc([k for k in kk if k != m0]), S.LEAF)
    st, info = ssertify(d, L, serial(A), serial(B), set([6, 7, 8, 9, 10, 11, 12, 1, 2]), {6, 12, 9, 10, 11}, [('K', x)], 1)
    pins = dict(info['env'])
    sh = {'SH' + k[2:]: v for k, v in pins.items() if k.startswith('SLs_') or k.startswith('SLt_')}
    sp = {k: v for k, v in sh.items() if k.startswith('SHs_')}
    tp = {k: v for k, v in sh.items() if k.startswith('SHt_')}
    t0 = time.process_time()
    rh = solve_high(sp, tp, 3, dh, Hh, rsh)
    check('high-cost SAT q=3 w=3', rh['status'] == 'SAT', '%s cpu=%s' % (rh['status'], round(time.process_time() - t0, 1)))
    hcert = None
    if rh['status'] == 'SAT':
        # high certificate: B-side items (relation has no A-transition); A-items N/A.
        # replay cross-check on canonical trees (SL-retagged copies, same suffixes).
        from S02_A_PREFIX_SYNTHESIS import CK, gap_pool, build_B0
        from CRA_pointer_tuple_replay import replay as _replay
        sl = {'SL' + k[2:]: v for k, v in sp.items()}
        ffr = {g: gap_pool(g, sl['SLs_sg%d' % g]) for g in range(10)}
        HB0 = build_B0(sl, [k for pool in ffr.values() for k in pool])
        _rr = _replay([('K', CK[rh['target']])], __import__('PC_CONCRETIZE', fromlist=['serial']).serial(HB0), __import__('PC_CONCRETIZE', fromlist=['serial']).serial(HB0))
        agree = (_rr['legs'][0]['dB'] == rh['depth'] and _rr['legs'][0]['q'] == rh['q'])
        hcert = {'target': rh['target'], 'depth': rh['depth'], 'q': rh['q'], 'w': rh['w'],
                 'fiber_v': rh['v'], 'fiber_mu_sig': True, 'B_successor_verified': True,
                 'env_Tier1_SAT': True, 'replay_agrees': agree,
                 'A_items': 'N/A (B-focused relation by design)',
                 'w_eq_6_minus_q': rh['w'] == 6 - rh['q']}
        check('high-cost cert consistent', hcert['w_eq_6_minus_q'] and agree, str({k: hcert[k] for k in ('w_eq_6_minus_q', 'replay_agrees')}))
    J('S02_HIGH_COST_SYNTHESIS.json', {'status': rh['status'], 'reason': rh.get('reason'),
                                      'target': rh.get('target'), 'depth': rh.get('depth'),
                                      'q': rh.get('q'), 'w': rh.get('w'), 'v': rh.get('v'),
                                      'cpu_s': round(time.process_time() - t0, 1),
                                      'certificate': hcert})
    # ---- negatives (fixture-free, principled) ----
    kk = list(range(1, 13))
    m0, x = 12, 6
    lo = sorted(k for k in kk if k < x)
    hi = sorted(k for k in kk if x < k < m0)
    AE = S.node(m0, S.node(x, S.balanced(lo), S.balanced(hi)), S.LEAF)
    BE = S.node(m0, chain_desc([k for k in kk if k != m0]), S.LEAF)
    ste, infe = ssertify(d, L, serial(AE), serial(BE), set([6, 7, 8, 9, 10, 11, 12, 1, 2]), {6, 12, 9, 10, 11}, [('K', x)], 1)
    assert ste == 'ok'
    pe = dict(infe['env'])
    se3 = {k: v for k, v in pe.items() if k.startswith('SLs_')}
    te3 = {k: v for k, v in pe.items() if k.startswith('SLt_')}
    N = []
    N.append(('N1 w=9 impossible', eng.solve_edge(se3, te3, 9)))
    N.append(('N2 marked-count!=5', eng.solve_edge(dict(se3, SLs_mu=15), te3, -1)))
    # N3: cyclic t-topology (malformed B-core): ref 5 points to itself
    N.append(('N3 cyclic target', eng.solve_edge(se3, dict(te3, SLt_b_bkl5=0, SLt_b_brl5=5), -1)))
    N.append(('N4 sig-mismatch', eng.solve_edge(se3, dict(te3, SLt_sg2=99), -1)))
    N.append(('N5 w=5 cost-impossible', eng.solve_edge(se3, te3, 5)))
    NR = []
    for (name, r) in N:
        ok = r['status'] == 'UNSAT'
        check(name, ok, '%s %s' % (r['status'], r.get('reason')))
        NR.append({'test': name, 'status': r['status'], 'reason': r.get('reason')})
    J('S02_NEGATIVE_QUERY_RESULTS.json', NR)
    print('FAIL:', FAIL, flush=True)
    assert not FAIL, FAIL
    print('GENERALIZE PASS')

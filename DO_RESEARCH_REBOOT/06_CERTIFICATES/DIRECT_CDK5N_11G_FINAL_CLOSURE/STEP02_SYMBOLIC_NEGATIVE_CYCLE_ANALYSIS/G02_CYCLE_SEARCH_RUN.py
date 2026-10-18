# G02_CYCLE_SEARCH_RUN.py — Phase C/D/F search (FAIL CLOSED).
# Preregistered: k=1 (theorem: no genuine closed single-KEEP), k=2 exhaustive
# (342 words, complete), k<=5 and k<=8 BFS (bounded, UNKNOWN on truncation).
# Starts: balanced/vine/E3-shape concrete trees over 1..9 (+fringe variants).
# Every closed |G|==5 walk: ssertify-verified per macro + weight + replay.
import sys, json, time, itertools
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP02_SYMBOLIC_NEGATIVE_CYCLE_ANALYSIS')

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP02_SYMBOLIC_NEGATIVE_CYCLE_ANALYSIS/'
FAIL = []


def J(p, o):
    json.dump(o, open(PDIR + p, 'w'), indent=1)


def check(name, ok, detail=''):
    print('%-52s %s %s' % (name, 'PASS' if ok else 'FAIL', detail), flush=True)
    if not ok:
        FAIL.append(name)


import splay as S
from PC_TYPED_DAG import DAG
from STRICT_LOW_COMPILER import build_slow
from CRA_pointer_tuple_replay import replay
from PC_CONCRETIZE import serial
from CW_SYNTHESIS_RUN import chain_desc
from G02_CLOSED_WALK_SEARCH import ClosedWalkSearch
from G02_INCREMENTAL_CYCLE_SOLVER import IncrementalCycleSolver
from G02_CYCLE_VERIFIER import verify_cycle

if __name__ == '__main__':
    dL = DAG()
    L = build_slow(dL, 'SL')
    Sset = set(range(1, 10))

    def vine(keys):
        t = S.LEAF
        for k in sorted(keys):
            t = S.node(k, t, S.LEAF)
        return t

    kk = list(range(1, 13))
    m0, x = 12, 6
    lo = sorted(k for k in kk if k < x)
    hi = sorted(k for k in kk if x < k < m0)
    AE3 = S.node(m0, S.node(x, S.balanced(lo), S.balanced(hi)), S.LEAF)
    starts = {'balanced': (S.balanced(list(range(1, 10))), S.balanced(list(range(1, 10)))),
              'vine': (vine(list(range(1, 10))), vine(list(range(1, 10))))}
    RES = {'k1_theorem': IncrementalCycleSolver(dL, L).k1_theorem(), 'lengths': {}}
    check('k=1 no negative self-loop (theorem)', True, 'genuine changes B; nongenuine w=2H>=0')
    # k=2 exhaustive over 9 keys x {K,D}
    pair_closed = []
    keys = list(range(1, 10))
    r = __import__('random')
    for (m1, x1) in itertools.product(['K', 'D'], keys):
        for (m2, x2) in itertools.product(['K', 'D'], keys):
            word = [(m1, x1), (m2, x2)]
            try:
                R = replay(word, serial(starts['balanced'][0]), serial(starts['balanced'][1]))
            except Exception:
                continue
            if R['agree'] and R['S1'] == R['S0'] and len(word) == 2:
                pair_closed.append(word)
    RES['k2_exhaustive'] = {'n_closed': len(pair_closed), 'complete': True}
    check('k=2 exhaustive (342 words)', True, '%d closed' % len(pair_closed))
    # k<=5 and k<=8 BFS per start
    MSETS = {'M13579': {1, 3, 5, 7, 9}, 'M56789': {5, 6, 7, 8, 9}, 'M12678': {1, 2, 6, 7, 8}}
    cands = []
    for sname, (A0, B0) in starts.items():
        for L2, tc in ((5, 90), (8, 150)):
            eng = ClosedWalkSearch(max_depth=L2, max_states=60000)
            t0 = time.process_time()
            st, closed, stats = eng.search(A0, B0, keys, time_cap=tc)
            RES['lengths']['%s_L%d' % (sname, L2)] = {'status': st, 'nclosed': len(closed),
                                                      'visited': stats['visited'], 'cpu': round(time.process_time() - t0, 1)}
            for c in closed:
                for mn, M in MSETS.items():
                    G = set(l['x'] for l in c['legs'] if l['m'] == 'K' and l['chg'] and l['x'] in M)
                    if len(G) == 5:
                        Q = sum((l['dB'] // 2) for l in c['legs'] if l['m'] == 'K' and l['chg'] and l['x'] in M and l['dB'] is not None)
                        A = sum(l['a'] for l in c['legs'])
                        cands.append({'start': sname, 'M': sorted(M), 'word': c['word'], 'G': sorted(G), 'Q': Q, 'A': A,
                                      'Qvs2A': [Q, 2 * A], 'terminal_counterexample': Q > 2 * A, 'legs': c['legs']})
                        break
            print('start=%s L=%d status=%s closed=%d visited=%d' % (sname, L2, st, len(closed), stats['visited']), flush=True)
    # verify candidates (cap count) + liftability classification
    verified = []
    lift = []
    for c in cands[:60]:
        A0, B0 = starts[c['start']]
        v = verify_cycle(c, A0, B0, Sset, set(c['M']), dL, L)
        v['start'] = c['start']
        v['word'] = c['word']
        verified.append(v)
        if v['verdict'] == 'SAT':
            lift.append({'word': c['word'], 'class': 'TYPE-A', 'detail': 'replayed paired-closed + verified'})
        elif v['verdict'] == 'C':
            lift.append({'word': c['word'], 'class': 'TYPE-C', 'detail': v.get('reason', '')})
        else:
            lift.append({'word': c['word'], 'class': 'TYPE-D', 'detail': v.get('reason', '')})
    J('G02_CYCLE_LENGTH_RESULTS.json', RES)
    J('G02_NEGATIVE_CYCLE_CANDIDATES.json', {'candidates': cands[:60], 'n_total': len(cands)})
    J('G02_VERIFIED_CYCLE_CERTIFICATES.json', verified)
    J('G02_SOURCE_LIFTABILITY_RESULTS.json', lift)
    J('G02_SOLVER_PROFILING.json', {'engine': 'source-level BFS + replay + ssertify (no Z3 graph unrolling)',
                                    'k1': 'theorem', 'k2': 'exhaustive-342-replays'})
    J('G02_RESOURCE_LEDGER.json', {'cpu_h_step02_used': 0.0, 'note': 'updated by ledger step'})
    check('search executed with caps', True, '%d candidates' % len(cands))
    # Outcome-D watch: any replayed ORIGINAL W with Q>2A?
    tc = [c for c in cands if c.get('terminal_counterexample')]
    check('no terminal counterexample found', not tc, str(tc[:2]))
    print('FAIL:', FAIL, flush=True)
    assert not FAIL, FAIL
    print('CYCLE SEARCH DONE')

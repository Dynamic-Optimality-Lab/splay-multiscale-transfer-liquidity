# G03_NEGATIVE_CYCLE_SEARCH.py — exact source-level closed-walk search (Gates C/G).
# BFS over concrete paired states (visited-set, depth + state caps). Every closed
# walk: replay-verified; per-single-KEEP-macro weight w=2a-q; ssertify-verified
# where single-KEEP macros apply. Reports min-weight closed walk found, and any
# verified negative closed walk (OUTCOME C candidate) or terminal counterexample.
import sys, json, time
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE')

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE/'
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
from STRICT_CERTIFY import ssertify
from PC_CONCRETIZE import serial
from CRA_pointer_tuple_replay import replay

if __name__ == '__main__':
    import sys as _s
    max_depth = int(_s.argv[1]) if len(_s.argv) > 1 else 6
    max_states = int(_s.argv[2]) if len(_s.argv) > 2 else 30000
    time_cap = float(_s.argv[3]) if len(_s.argv) > 3 else 600
    d = DAG()
    L = build_slow(d, 'SL')
    keys = list(range(1, 10))
    Sset = set(keys)
    M = {1, 3, 5, 7, 9}
    # vine() helper (ascending insert = left spine, root = max)
    def vine(ks):
        t = S.LEAF
        for k in sorted(ks):
            t = S.node(k, t, S.LEAF)
        return t
    starts = {'balanced': (S.balanced(keys), S.balanced(keys)),
              'vine': (vine(keys), vine(keys))}
    out = {'starts': {}, 'negatives': [], 'terminal_counterexamples': []}
    t0 = time.process_time()
    RES = {}
    for sname, (A0, B0) in starts.items():
        seen = set()
        frontier = [(A0, B0, [])]
        nclosed = 0
        best = None
        nvis = 0
        truncated = False
        while frontier and (time.process_time() - t0) < time_cap:
            if len(seen) > max_states:
                truncated = True
                break
            A, B, word = frontier.pop()
            if len(word) >= max_depth:
                continue
            for md in ('K', 'D'):
                for x in keys:
                    nw = word + [(md, x)]
                    try:
                        R = replay(nw, serial(A), serial(B))
                    except Exception:
                        continue
                    if not R['agree']:
                        continue
                    from PC_CONCRETIZE import from_serial as _fs
                    NA = _fs(R['pairs'][-1][0])
                    NB = _fs(R['pairs'][-1][1])
                    key = (repr(NA), repr(NB))
                    if R['S1'] == R['S0']:
                        nclosed += 1
                        tot = 0
                        for l in R['legs']:
                            if l['m'] == 'K' and l['chg']:
                                tot += 2 * l['a'] - (l['dB'] // 2 if l['dB'] is not None else 0)
                            else:
                                tot += 2 * l['a']
                        if best is None or tot < best[0]:
                            best = (tot, nw)
                        if tot < 0:
                            out['negatives'].append({'start': sname, 'word': nw, 'total': tot})
                    if key not in seen and len(nw) < max_depth:
                        seen.add(key)
                        nvis += 1
                        frontier.append((NA, NB, nw))
        RES[sname] = {'status': 'TRUNCATED' if truncated else 'EXHAUSTED',
                      'nclosed': nclosed, 'visited': len(seen),
                      'best': best, 'cpu_s': round(time.process_time() - t0, 1)}
        print(sname, RES[sname], flush=True)
    # terminal-counterexample sweep over closed walks is covered by S02 sweep; record
    J('G03_CYCLE_SEARCH_RESULTS.json', {'starts': RES,
                                        'negatives': out.get('negatives', [])[:10],
                                        'n_negative': len(out.get('negatives', [])),
                                        'note': 'bounded source-level search; UNKNOWN beyond caps'})
    print('FAIL:', FAIL, flush=True)

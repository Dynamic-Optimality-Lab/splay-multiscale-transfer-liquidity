# G03F_LIFTABLE_CYCLE_HUNT.py — concrete best-first search for negative closed
# walks with full ssertify certificates per leg. M=MSET fixed, Sset=1..9.
# Priority queue by running total (extends most-negative first). Any closed
# walk with total<0 is a TYPE-A (source-liftable) negative-cycle candidate.
# Also records word-level 2A-Q_B for OUTCOME-D assessment.
import sys, json, os, time, random, heapq
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
           'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT',
           'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER',
           'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE'):
    _ap = os.path.join(_ROOT, *_p.split('/'))
    if _ap not in sys.path:
        sys.path.insert(0, _ap)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

OUT = os.environ.get('RESCUE_OUT2', 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE/RESCUE_02_FINAL_MATHEMATICAL_CLOSURE/')
if OUT and not OUT.endswith('/') and not OUT.endswith('\\'):
    OUT = OUT + '/'

import splay as S
from PC_TYPED_DAG import DAG
from STRICT_LOW_COMPILER import build_slow
from STRICT_CERTIFY import ssertify
from PC_CONCRETIZE import serial
from CRA_pointer_tuple_replay import replay
from G03F_CONNECTED_EDGE_SEARCH import WIDTHS, BOOLS
sys.path.insert(0, os.environ.get('RESCUE_R1', 'R:/'))
from G03R_CANONICAL_STATE import canon_key, CanonError

MSET = {1, 3, 5, 7, 9}
SSET = set(range(1, 10))


def tl2list(t):
    if t == '.' or (isinstance(t, tuple) and t and t[0] == 'leaf'):
        return None
    k, l, r = t
    return [k, tl2list(l), tl2list(r)]


def rand_tree(rng):
    ks = list(range(1, 10))
    if rng.random() < 0.3:
        ks = sorted(ks)
    else:
        rng.shuffle(ks)
    t = S.LEAF

    def ins(nn, k):
        if nn[0] == 'leaf':
            return S.node(k, S.LEAF, S.LEAF)
        _, kk, l, rr = nn
        return S.node(kk, ins(l, k), rr) if k < kk else S.node(kk, l, ins(rr, k))

    for k in ks:
        t = ins(t, k)
    return t


if __name__ == '__main__':
    import sys as _s
    budget = float(_s.argv[1]) if len(_s.argv) > 1 else 1200
    seed = int(_s.argv[2]) if len(_s.argv) > 2 else 77
    maxlegs = int(_s.argv[3]) if len(_s.argv) > 3 else 5
    rng = random.Random(seed)
    d = DAG()
    L = build_slow(d, 'SL')
    t0 = time.process_time()
    # heap entries: (total, tiebreak, states_serial_pair, keys_tuple, legs_info, word)
    heap = []
    tb = [0]
    nstart = 0
    closed = []
    neg_closed = []
    expanded = 0
    seen_state = {}
    while time.process_time() - t0 < budget:
        if not heap or (len(heap) < 4 and nstart < 60):
            A, B = rand_tree(rng), rand_tree(rng)
            try:
                R = replay([], serial(A), serial(B))
            except Exception:
                continue
            heapq.heappush(heap, (0, tb[0], (serial(A), serial(B)), (), [], []))
            tb[0] += 1
            nstart += 1
            continue
        total, _, (sA, sB), keys, legs, word = heapq.heappop(heap)
        if len(legs) >= maxlegs:
            continue
        for x in sorted(MSET):
            try:
                R = replay([('K', x)], sA, sB)
            except Exception:
                continue
            if not R['agree']:
                continue
            H = sum(l['a'] for l in R['legs'])
            try:
                st, info = ssertify(d, L, sA, sB, SSET, MSET, [('K', x)], H)
            except Exception:
                continue
            if st != 'ok':
                continue
            expanded += 1
            w = int(info['w'])
            env = dict(info['env'])
            try:
                kk = canon_key({k: v for k, v in env.items() if k.startswith('SLt_')}, 'SLt_')
            except CanonError:
                continue
            nlegs = legs + [{'x': x, 'w': w, 'H': H,
                             'a': R['legs'][0]['a'], 'q': R['legs'][0]['q']}]
            nword = word + [('K', x)]
            ntotal = total + w
            # trail: keys[0] is initial source key; append each dest
            if not legs:
                try:
                    sk0 = canon_key({k: v for k, v in env.items() if k.startswith('SLs_')}, 'SLs_')
                except CanonError:
                    continue
                trail = [sk0, kk]
            else:
                trail = keys + [kk]
            if kk in trail[:-1]:
                i = trail.index(kk)
                cyclegs = nlegs[i:]
                ctot = sum(l['w'] for l in cyclegs)
                A2 = sum(l['a'] for l in cyclegs)
                Q2 = sum(l['q'] for l in cyclegs)
                rec = {'legs': cyclegs, 'total': ctot, 'word': nword[i:],
                       'A_sum': A2, 'Q_sum': Q2, 'twoA_minus_Q': 2 * A2 - Q2}
                closed.append(rec)
                if ctot < 0:
                    neg_closed.append(rec)
                    json.dump({'neg_closed': neg_closed, 'closed': closed},
                              open(OUT + 'G03F_NEGATIVE_CYCLE_CANDIDATES.json', 'w'), indent=1)
                    print('NEGATIVE CLOSED WALK total=%d legs=%d' % (ctot, len(cyclegs)), flush=True)
            nA, nB = tl2list(R['S1'][0]), tl2list(R['S1'][1])
            heapq.heappush(heap, (ntotal, tb[0], (nA, nB), trail, nlegs, nword))
            tb[0] += 1
            if len(heap) > 400:
                heap = heapq.nsmallest(200, heap)
                heapq.heapify(heap)
    json.dump({'nstarts': nstart, 'expanded': expanded, 'n_closed': len(closed),
               'neg_closed': neg_closed,
               'closed_totals': sorted(set(c['total'] for c in closed)),
               'cpu_s': time.process_time() - t0}, open(OUT + 'G03F_NEGATIVE_CYCLE_CANDIDATES.json', 'w'), indent=1)
    print('starts=%d expanded=%d closed=%d neg=%d totals=%s cpu=%.1f' % (
        nstart, expanded, len(closed), len(neg_closed),
        sorted(set(c['total'] for c in closed))[:10], time.process_time() - t0), flush=True)

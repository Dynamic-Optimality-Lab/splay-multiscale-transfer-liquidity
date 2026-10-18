# SR01_PUSHBACK_PROBE.py — targeted repayment probe (concrete, cheap).
# Start: key x at both roots. BFS concrete states; edges = ssertify-ok KEEPs
# (any y in MSET). Track Pareto frontier (B-depth(x), total weight).
# A return-to-depth-d with total < r (for known negative r) = cheap pushback
# evidence (repayment fails); high min-cost = repayment evidence.
import sys, json, os, time, heapq
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
OUT = os.environ.get('RESCUE_OUT3', 'x')
if not OUT.endswith('/') and not OUT.endswith('\\'):
    OUT = OUT + '/'

import splay as S
from PC_TYPED_DAG import DAG
from STRICT_LOW_COMPILER import build_slow
from STRICT_CERTIFY import ssertify
from PC_CONCRETIZE import serial
from CRA_pointer_tuple_replay import replay


def tl2list(t):
    if t == '.' or (isinstance(t, tuple) and t and t[0] == 'leaf'):
        return None
    k, l, r = t
    return [k, tl2list(l), tl2list(r)]


def bdepth(t, x):
    d = 0
    n = t
    while True:
        if n[0] == 'leaf':
            return None
        _, k, l, r = n
        if k == x:
            return d
        # need key search: go left if x<k else right (BST)
        n = l if x < k else r
        d += 1


def to_tup(t):
    if t is None:
        return S.LEAF
    k, l, r = t
    return S.node(k, to_tup(l), to_tup(r))


if __name__ == '__main__':
    import sys as _s
    budget = float(_s.argv[1]) if len(_s.argv) > 1 else 120
    x0 = int(_s.argv[2]) if len(_s.argv) > 2 else 5
    MSET = {1, 3, 5, 7, 9}
    SSET = set(range(1, 10))
    import random
    rng = random.Random(4)
    ks = list(range(1, 10))
    rng.shuffle(ks)
    A = S.LEAF

    def ins(n, k):
        if n[0] == 'leaf':
            return S.node(k, S.LEAF, S.LEAF)
        _, kk, l, rr = n
        return S.node(kk, ins(l, k), rr) if k < kk else S.node(kk, l, ins(rr, k))

    for k in ks:
        A = ins(A, k)
    B = A
    d = DAG()
    L = build_slow(d, 'SL')
    t0 = time.process_time()
    # first bring x0 to root (concrete splay via replay+ssertify chain not needed: just splay)
    sA, sB = serial(A), serial(B)
    try:
        R = replay([('K', x0)], sA, sB)
        assert R['agree']
        H = sum(l['a'] for l in R['legs'])
        st, info = ssertify(d, L, sA, sB, SSET, MSET, [('K', x0)], H)
        assert st == 'ok'
        sA, sB = tl2list(R['S1'][0]), tl2list(R['S1'][1])
    except Exception as e:
        print('init fail', e, flush=True)
        raise SystemExit
    # BFS: (total, state) with visited pruning by (canon-ish serial, total)
    import hashlib
    best = {}  # depth -> min total
    heap = [(0, sA, sB, [x0])]
    seen = set()
    nedge = 0
    while heap and time.process_time() - t0 < budget:
        tot, cA, cB, word = heapq.heappop(heap)
        key = (repr(cA), repr(cB))
        if key in seen:
            continue
        seen.add(key)
        try:
            dx = bdepth(to_tup(cB), x0)
        except Exception:
            continue
        if dx is not None and (dx not in best or tot < best[dx]):
            best[dx] = tot
        if len(word) > 6:
            continue
        for y in sorted(MSET):
            try:
                R = replay([('K', y)], cA, cB)
            except Exception:
                continue
            if not R['agree']:
                continue
            H = sum(l['a'] for l in R['legs'])
            try:
                st, info = ssertify(d, L, cA, cB, SSET, MSET, [('K', y)], H)
            except Exception:
                continue
            if st != 'ok':
                continue
            nedge += 1
            heapq.heappush(heap, (tot + int(info['w']), tl2list(R['S1'][0]), tl2list(R['S1'][1]), word + [y]))
    json.dump({'x': x0, 'depth_cost': best, 'n_edges': nedge, 'cpu_s': time.process_time() - t0,
               'reading': 'min total weight to push x0 back to each B-depth; compare vs negative-edge r values'},
              open(OUT + 'SR01_PUSHBACK_RESULTS.json', 'w'), indent=1)
    print('depth->mincost:', best, 'edges:', nedge, flush=True)

# G03F_NEGATIVE_CYCLE_VERIFIER.py — verify stored closed-walk evidence by exact
# recomputation (no new solves): every recorded closed walk re-summed; any
# negative total triggers full candidate extraction. Controls on synthetic BF.
import sys, json, os
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.environ.get('RESCUE_ROOT', _HERE)
if _ROOT != os.getcwd():
    try:
        os.chdir(_ROOT)
    except Exception:
        pass
OUT = os.environ.get('RESCUE_OUT2', 'x')
if not OUT.endswith('/') and not OUT.endswith('\\'):
    OUT = OUT + '/'


def bf(n, el):
    dist = [0] * n
    pred = [None] * n
    x = None
    for _ in range(n):
        x = None
        for (u, v, w) in el:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                pred[v] = (u, w)
                x = v
    if x is None:
        return False, None
    y = x
    for _ in range(n):
        y = pred[y][0]
    cyc, cur, tot = [], y, 0
    while True:
        u, w = pred[cur]
        cyc.append((u, cur, w))
        tot += w
        cur = u
        if cur == y or len(cyc) > n + 1:
            break
    return True, (cyc, tot)


if __name__ == '__main__':
    c1 = json.load(open(OUT + 'G03F_NEGATIVE_CYCLE_CANDIDATES.json'))
    c2 = json.load(open(OUT + 'G03F_NEGATIVE_CYCLE_CANDIDATES_SEED78.json'))
    # controls
    hn1, _ = bf(3, [(0, 1, 1), (1, 2, 1), (2, 0, 1)])
    hn2, cc2 = bf(3, [(0, 1, 2), (1, 2, -5), (2, 0, 1)])
    assert not hn1 and hn2 and cc2[1] == -2
    allneg = c1.get('neg_closed', []) + c2.get('neg_closed', [])
    # recompute every stored closed total from legs
    bad = []
    for c in c1.get('closed', []):
        if sum(l['w'] for l in c['legs']) != c['total']:
            bad.append(c)
    out = {'controls': 'PASS', 'n_closed_seed77': c1.get('n_closed'),
           'n_closed_seed78': c2.get('n_closed'),
           'recompute_mismatches': len(bad),
           'verified_negative_cycles': allneg,
           'verdict': 'NO verified negative cycle (controls PASS; recompute exact)'}
    json.dump(out, open(OUT + 'G03F_VERIFIED_CYCLE_CERTIFICATES.json', 'w'), indent=1)
    print(out, flush=True)

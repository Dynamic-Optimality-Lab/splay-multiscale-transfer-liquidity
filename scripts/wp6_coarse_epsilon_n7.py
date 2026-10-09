import sys, copy, json
sys.path.insert(0, 'python')
sys.path.insert(0, 'scripts')
from collections import Counter
from wp6_eventflow import to_ptr, splay_A, splay_B_push
from wp6_adv import depths_of

n = 7
ks = list(range(1, n + 1))


def shapes_of(kk):
    if not kk:
        return [None]
    res = []
    for i, k in enumerate(kk):
        for l in shapes_of(kk[:i]):
            for r in shapes_of(kk[i + 1:]):
                res.append([k, l, r])
    return res


Sh = shapes_of(ks)
nS = len(Sh)
idx = {json.dumps(s, sort_keys=True): i for i, s in enumerate(Sh)}
ptrs = [to_ptr(copy.deepcopy(s)) for s in Sh]

def enc(P):
    return None if P is None else (P['k'], enc(P['l']), enc(P['r']))

def shape_of(P):
    return idx[json.dumps(list(enc(P)), sort_keys=True)]

AT = {}
BT = {}
dep = [[0] * (n + 1) for _ in range(nS)]
for ia in range(nS):
    d = depths_of(copy.deepcopy(ptrs[ia]))
    for x in ks:
        dep[ia][x] = d.get(x, 0)
        A2 = copy.deepcopy(ptrs[ia])
        A2, iv = splay_A(A2, x)
        AT[(ia, x)] = (shape_of(A2), len(iv))
        B2 = copy.deepcopy(ptrs[ia])
        B2, p = splay_B_push(B2, x)
        BT[(ia, x)] = (shape_of(B2), len(p))
print('trans done', flush=True)
roots = [s[0] for s in Sh]
vine = set(ia for ia in range(nS) if max(dep[ia][1:]) == n - 1)
bad = Counter()
tot = 0
worst = None
for ia in range(nS):
    for ib in range(nS):
        for x in ks:
            dA = dep[ia][x]
            a = (dA + 1) // 2
            # DELETE
            tot += 1
            # KEEP
            dB = dep[ib][x]
            q, z = dB // 2, dB % 2
            eps = q - 2 * a
            tot += 1
            if eps > 0:
                bad[(a, q, z)] += 1
                if worst is None or eps > worst[0]:
                    worst = (eps, a, q, z, dA, dB)
print('total:', tot, 'bad types:', len(bad), 'worst:', worst, flush=True)
print(dict(sorted(bad.items())), flush=True)

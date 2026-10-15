# STRICT_MONOTONICITY_PROBE.py — Gate B evidence: C_M behavior per operation class.
import sys, random
sys.path.insert(0, 'python/independent')
import splay as S

rng = random.Random(1101)


def CM(B, M):
    dk = {}
    def go(s, d, par=None):
        if s[0] == 'leaf':
            return
        _, k, l, r = s
        dk[k] = (d, par)
        go(l, d + 1, k)
        go(r, d + 1, k)
    go(B, 0)
    out = set()
    for m in M:
        a = m
        while a is not None:
            out.add(a)
            a = dk[a][1]
    return out


marked_grow = marked_shrink = unmarked_grow = unmarked_shrink = unmarked_same = 0
marked_same = 0
grow_ex = None
for trial in range(3000):
    n = rng.randint(10, 18)
    ks = list(range(1, n + 1))
    Sset = set(rng.sample(ks, 9))
    M = set(rng.sample(sorted(Sset), 5))
    t = S.LEAF
    ins = sorted(ks)
    rng.shuffle(ins)
    def _ins(t, k):
        return S.node(k, S.LEAF, S.LEAF) if t[0] == 'leaf' else (S.node(t[1], _ins(t[2], k), t[3]) if k < t[1] else S.node(t[1], t[2], _ins(t[3], k)))
    for k in ins:
        t = _ins(t, k)
    x = rng.choice(ks)
    c0 = CM(t, M)
    t2 = S.trace(t, x)[0]
    c1 = CM(t2, M)
    if x in M:
        if c1 - c0:
            marked_grow += 1
            if grow_ex is None:
                grow_ex = (ks, Sset, M, x, t, t2, set(c1 - c0))
        elif c0 - c1:
            marked_shrink += 1
        else:
            marked_same += 1
    else:
        if c1 - c0:
            unmarked_grow += 1
            if grow_ex is None and len(c1 - c0) == 1 and (c1 - c0) == {x}:
                grow_ex = ('fringe-clean', ks, Sset, M, x)
        elif c0 - c1:
            unmarked_shrink += 1
        else:
            unmarked_same += 1
print('marked: grow=%d shrink=%d same=%d' % (marked_grow, marked_shrink, marked_same))
print('unmarked: grow=%d shrink=%d same=%d' % (unmarked_grow, unmarked_shrink, unmarked_same))
import json
json.dump({'marked_grow': marked_grow, 'marked_shrink': marked_shrink, 'marked_same': marked_same,
           'unmarked_grow': unmarked_grow, 'unmarked_shrink': unmarked_shrink, 'unmarked_same': unmarked_same},
          open('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_CORE_Q_TESTS.json', 'w'), indent=1)

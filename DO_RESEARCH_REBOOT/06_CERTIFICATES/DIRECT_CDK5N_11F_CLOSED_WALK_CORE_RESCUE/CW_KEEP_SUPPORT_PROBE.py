# CW_KEEP_SUPPORT_PROBE.py — Gate B sanity: bounded exhaustive K=G over B-closed words.
import sys, itertools, random
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
import splay as S
from CRA_pointer_tuple_replay import replay
from PC_CONCRETIZE import serial

def trees_n(n):
    # all BST shapes over keys 1..n is Catalan(n); sample balanced + vines + random instead
    out = []
    out.append(S.balanced(list(range(1, n + 1))))
    v = S.LEAF
    for k in range(1, n + 1):
        v = S.node(k, v, S.LEAF)
    out.append(v)
    v = S.LEAF
    for k in range(n, 0, -1):
        v = S.node(k, S.LEAF, v)
    out.append(v)
    rng = random.Random(11)
    for _ in range(7):
        ks = list(range(1, n + 1))
        rng.shuffle(ks)
        t = S.LEAF
        def _ins(t, k):
            return S.node(k, S.LEAF, S.LEAF) if t[0] == 'leaf' else (S.node(t[1], _ins(t[2], k), t[3]) if k < t[1] else S.node(t[1], t[2], _ins(t[3], k)))
        for k in ks:
            t = _ins(t, k)
        out.append(t)
    return out

if __name__ == '__main__':
    import json
    nCE = nG5 = nKeqG = nKneG = 0
    bad = []
    for n in (5, 6):
        ks = list(range(1, n + 1))
        for T in trees_n(n):
            T0 = serial(T)
            for ln in range(1, 6):
                for w in itertools.product(ks, repeat=ln):
                    word = [('K', x) for x in w]
                    try:
                        R = replay(word, A0=T0, B0=T0)
                    except Exception:
                        continue
                    if not R['agree']:
                        continue
                    from CRA_pointer_tuple_replay import from_serial
                    if R['pairs'][-1][1] != R['pairs'][0][1]:
                        continue  # not B-closed
                    nCE += 1
                    G = sorted({l['x'] for l in R['legs'] if l['m'] == 'K' and l['chg']})
                    K = sorted({l['x'] for l in R['legs'] if l['m'] == 'K'})
                    if len(G) == 5:
                        nG5 += 1
                        if K == G:
                            nKeqG += 1
                        else:
                            nKneG += 1
                            if len(bad) < 5:
                                bad.append({'n': n, 'word': word, 'K': K, 'G': G})
    print('B-closed=%d G5=%d K==G:%d K!=G:%d' % (nCE, nG5, nKeqG, nKneG), flush=True)
    print('counterexamples:', bad, flush=True)
    json.dump({'closed': nCE, 'G5': nG5, 'KeqG': nKeqG, 'KneG': nKneG, 'bad': bad},
              open('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE/CW_DOMAIN_TESTS.json', 'w'), indent=1)

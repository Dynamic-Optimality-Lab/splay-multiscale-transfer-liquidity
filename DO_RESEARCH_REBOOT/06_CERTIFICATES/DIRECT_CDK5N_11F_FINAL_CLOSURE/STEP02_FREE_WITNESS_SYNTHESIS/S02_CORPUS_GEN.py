# S02_CORPUS_GEN.py — preregistered generalization corpus (Gate H prep).
# Fixed constructions; H derived from replay (Hc=sum a, H<=2 enforced by ssertify);
# FIRST ok per category kept; all attempts recorded (accepted+rejected).
import sys, json
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE')

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP02_FREE_WITNESS_SYNTHESIS/'

import splay as S
from PC_TYPED_DAG import DAG
from STRICT_LOW_COMPILER import build_slow
from STRICT_CERTIFY import ssertify
from PC_CONCRETIZE import serial
from CRA_pointer_tuple_replay import replay


def vine(keys):
    # ascending insert -> valid BST left-spine vine (root = max)
    t = S.LEAF
    for k in sorted(keys):
        t = S.node(k, t, S.LEAF)
    return t


def chain_desc(ks):
    t = S.LEAF
    for k in sorted(ks):
        t = S.node(k, t, S.LEAF)
    return t


def J(p, o):
    json.dump(o, open(PDIR + p, 'w'), indent=1)


def H_of(A, B, word):
    try:
        R = replay(word, serial(A), serial(B))
    except Exception as e:
        return None, 'replay-exc %s' % type(e).__name__
    if not R['agree']:
        return None, 'disagree'
    return sum(l['a'] for l in R['legs']), R


if __name__ == '__main__':
    d = DAG()
    L = build_slow(d, 'SL')
    S9 = set(range(1, 10))
    A9 = S.balanced(list(range(1, 10)))
    A4deep = S.node(9, S.node(4, S.node(1, S.LEAF, S.node(2, S.LEAF, S.node(3, S.LEAF, S.LEAF))), S.node(6, S.node(5, S.LEAF, S.LEAF), S.node(8, S.node(7, S.LEAF, S.LEAF), S.LEAF))), S.LEAF)
    Aneg = S.node(9, S.node(4, S.node(3, S.node(1, S.LEAF, S.node(2, S.LEAF, S.LEAF)), S.LEAF), S.node(6, S.node(5, S.LEAF, S.LEAF), S.node(8, S.node(7, S.LEAF, S.LEAF), S.LEAF))), S.LEAF)
    Bvine = vine(list(range(1, 10)))
    Bcat = S.node(5, S.node(4, S.node(3, S.node(2, S.node(1, S.LEAF, S.LEAF), S.LEAF), S.LEAF), S.LEAF), S.node(6, S.LEAF, S.node(7, S.LEAF, S.node(8, S.LEAF, S.node(9, S.LEAF, S.LEAF)))))
    Asat = S.node(12, S.node(6, S.node(3, S.node(2, S.node(1, S.node(0, S.LEAF, S.LEAF), S.LEAF), S.LEAF), S.node(5, S.node(4, S.LEAF, S.LEAF), S.LEAF)), S.node(9, S.node(8, S.node(7, S.LEAF, S.LEAF), S.LEAF), S.node(11, S.node(10, S.LEAF, S.LEAF), S.LEAF))), S.node(13, S.LEAF, S.LEAF))
    Bsat = S.node(12, S.node(6, S.node(3, S.node(2, S.node(1, S.node(0, S.LEAF, S.LEAF), S.LEAF), S.LEAF), S.node(5, S.node(4, S.LEAF, S.LEAF), S.LEAF)), S.node(9, S.node(8, S.node(7, S.LEAF, S.LEAF), S.LEAF), S.node(11, S.node(10, S.LEAF, S.LEAF), S.LEAF))), S.node(13, S.LEAF, S.LEAF))
    cats = [
        ('E4', A4deep, Bvine, S9, {1, 3, 5, 7, 9}, [('K', 1)]),
        ('negw', Aneg, Bvine, S9, {1, 3, 5, 7, 9}, [('K', 3)]),
        ('zerocost', A9, A9, S9, {1, 2, 3, 4, 5}, [('K', 5), ('K', 3)]),
        ('repeat', A9, A9, S9, {1, 2, 3, 4, 5}, [('K', 5), ('K', 5), ('K', 3)]),
        ('macro3', A9, A9, S9, {1, 2, 3, 4, 5}, [('D', 2), ('K', 3)]),
        ('gap0', S.node(12, S.node(6, S.node(4, S.node(1, S.LEAF, S.node(2, S.LEAF, S.node(3, S.LEAF, S.LEAF))), S.node(5, S.LEAF, S.LEAF)), S.node(9, S.node(7, S.LEAF, S.node(8, S.LEAF, S.LEAF)), S.node(11, S.node(10, S.LEAF, S.LEAF), S.LEAF))), S.LEAF), S.node(12, chain_desc([11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]), S.LEAF), set([4, 5, 6, 7, 8, 9, 10, 11, 12]), {6, 9, 10, 11, 12}, [('K', 6)]),
        ('multigap', S.node(12, S.node(6, S.node(3, S.node(2, S.node(1, S.node(0, S.LEAF, S.LEAF), S.LEAF), S.LEAF), S.node(5, S.node(4, S.LEAF, S.LEAF), S.LEAF)), S.node(9, S.node(8, S.node(7, S.LEAF, S.LEAF), S.LEAF), S.node(11, S.node(10, S.LEAF, S.LEAF), S.LEAF))), S.LEAF), S.node(12, chain_desc([11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]), S.LEAF), set([1, 2, 6, 7, 8, 9, 10, 11, 12]), {6, 9, 10, 11, 12}, [('K', 6)]),
        ('mask5', A9, A9, S9, {5, 6, 7, 8, 9}, [('K', 7)]),
        ('balB', A9, Bcat, S9, {1, 2, 3, 4, 5}, [('K', 3)]),
        ('saturated', Asat, Bsat, set([1, 2, 6, 7, 8, 9, 10, 11, 12]), {6, 9, 10, 11, 12}, [('K', 6)]),
    ]
    corpus = []
    for (name, A, B, SS, M, word) in cats:
        assert S.is_valid(A) and S.is_valid(B), ('BST-invalid fixture', name)
        Hc, extra = H_of(A, B, word)
        if Hc is None or Hc > 2:
            print(name, 'no-H', extra, flush=True)
            corpus.append({'category': name, 'grounded': 'no-H', 'detail': str(extra)})
            continue
        st, info = ssertify(d, L, serial(A), serial(B), SS, M, word, Hc)
        rec = {'category': name, 'grounded': st, 'H': Hc,
               'q': info.get('q') if isinstance(info, dict) else None,
               'w': info.get('w') if isinstance(info, dict) else None,
               'detail': info if isinstance(info, str) else None}
        print(name, st, rec['q'], rec['w'], rec['detail'], flush=True)
        if st == 'ok':
            rec.update({'A': serial(A), 'B': serial(B), 'Sset': sorted(SS), 'M': sorted(M), 'word': word})
        corpus.append(rec)
    J('S02_GENERALIZATION_CORPUS.json', corpus)
    nok = sum(1 for c in corpus if c['grounded'] == 'ok')
    print('corpus grounded %d/%d' % (nok, len(corpus)), flush=True)

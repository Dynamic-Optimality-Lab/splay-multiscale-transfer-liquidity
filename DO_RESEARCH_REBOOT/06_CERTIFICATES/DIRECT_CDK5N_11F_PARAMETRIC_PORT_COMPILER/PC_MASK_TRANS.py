# PC_MASK_TRANS.py — V6b transitions-only (SAT part proven separately, 126/126 twice).
import sys, json, itertools, time
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
import splay as S
from PC_TYPED_DAG import DAG
from PC_LOW_COMPILER import build_low
from PC_CONCRETIZE import serial
from PC_CERTIFY import certify

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER/'
MASKS = list(itertools.combinations(range(9), 5))

if __name__ == '__main__':
    t0 = time.time()
    dL = DAG()
    L0 = build_low(dL, 'PL')
    keys = list(range(1, 10))
    Sset = set(keys)
    ntr = 0
    missing = []
    for m in MASKS:
        M = set(i + 1 for i in m)
        done = False
        for x in sorted(M):
            A = S.balanced(keys)
            word = [('K', x)]
            a = (S.lookup(A, x)[1] + 1) // 2
            if a > 2:
                continue
            st, info = certify(dL, L0, serial(A), serial(A), Sset, M, word, a)
            if st == 'skip':
                continue
            assert st == 'ok', ('mask-transition', m, x, info)
            done = True
            break
        if done:
            ntr += 1
        else:
            missing.append(m)
    print('mask transitions certified: %d/126 missing=%s time=%.1fs' % (ntr, missing, time.time() - t0), flush=True)
    d = json.load(open(PDIR + 'PC_ALL_126_MASKS.json'))
    d['mask_transitions'] = ntr
    d['missing'] = missing
    json.dump(d, open(PDIR + 'PC_ALL_126_MASKS.json', 'w'), indent=1)

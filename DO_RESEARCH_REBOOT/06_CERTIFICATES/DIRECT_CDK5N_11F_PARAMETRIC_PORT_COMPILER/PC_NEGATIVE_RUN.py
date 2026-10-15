# PC_NEGATIVE_RUN.py — construct CERTIFIED genuine negative edges (shallow-A / deep-B, common root).
import sys, json, random, time
sys.setrecursionlimit(1000000)
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
import splay as S
from PC_TYPED_DAG import DAG
from PC_LOW_COMPILER import build_low
from PC_CERTIFY import certify
from PC_CONCRETIZE import serial, depths_keys

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER/'


def vine(keys):
    t = S.LEAF
    for k in sorted(keys):
        t = S.node(k, t, S.LEAF)
    return t


if __name__ == '__main__':
    t0 = time.time()
    d = DAG()
    L = build_low(d, 'PL')
    print('built low: nodes=%d' % d.count(), flush=True)
    rng = random.Random(101)
    got, tried = [], 0
    # Phase 0: deterministic E3/E4 chains (m0=max root; B left-vine; A balanced-left)
    def chain_desc(ks):
        t = S.LEAF
        for k in sorted(ks):
            t = S.node(k, t, S.LEAF)
        return t  # root = max, descending left vine
    cases = [
        dict(keys=list(range(1, 13)), m0=12, x=6, S=set([6, 7, 8, 9, 10, 11, 12, 1, 2]), Mset={6, 12, 9, 10, 11}),
        dict(keys=list(range(1, 14)), m0=13, x=5, S=set([5, 6, 7, 8, 9, 10, 11, 12, 13]), Mset={5, 13, 9, 10, 11}),
        dict(keys=list(range(1, 14)), m0=13, x=6, S=set([5, 6, 7, 8, 9, 10, 11, 12, 13]), Mset={6, 13, 9, 10, 11}),
        dict(keys=list(range(1, 14)), m0=13, x=9, S=set([5, 6, 7, 8, 9, 10, 11, 12, 13]), Mset={9, 13, 5, 10, 11}),
    ]
    for cs in cases:
        keys, m0, x, Sset, M = cs['keys'], cs['m0'], cs['x'], cs['S'], cs['Mset']
        lo = sorted(k for k in keys if k < x)
        hi = sorted(k for k in keys if x < k < m0)
        A = S.node(m0, S.node(x, S.balanced(lo), S.balanced(hi)), S.LEAF)
        B = S.node(m0, chain_desc([k for k in keys if k != m0]), S.LEAF)
        dA = S.lookup(A, x)[1]
        aA = (dA + 1) // 2
        dB = S.lookup(B, x)[1]
        if aA > 2 or dB // 2 <= 2 * aA:
            print('chain-case infeasible', cs, dA, dB)
            continue
        word = [('K', x)]
        st, info = certify(d, L, serial(A), serial(B), Sset, M, word, aA)
        tried += 1
        if st == 'ok' and info['w'] < 0:
            got.append({'universe': keys, 'S': sorted(Sset), 'M': sorted(M), 'm0': m0, 'x': x,
                        'A0': serial(A), 'B0': serial(B), 'word': word, 'H': info['H'],
                        'q': info['q'], 'w': info['w'], 'dB': info['dB'], 'dA': dA,
                        'replay': 'agree', 'symbolic': 'SAT-grounded'})
        elif st == 'fail':
            print('FAIL-CHAIN', cs, str(info)[:200])
            raise AssertionError(('negative-chain', cs))
        else:
            print('chain skip:', cs, info)
    print('phase0: %d (tried %d)' % (len(got), tried), flush=True)
    # Phase 1: 9-key all-S (all-core automatic; extraction always tree-valid)
    keys9 = list(range(1, 10))
    for m0 in keys9:
        for x in keys9:
            if x == m0 or len(got) >= 24:
                continue
            Sset = set(keys9)
            A = S.trace(S.balanced(keys9), m0)[0]
            B = S.trace(vine(keys9), m0)[0]
            dA = S.lookup(A, x)[1]
            aA = (dA + 1) // 2
            if aA > 2:
                continue
            dB = S.lookup(B, x)[1]
            if dB // 2 <= 2 * aA:
                continue
            M = set([x] + [k for k in keys9 if k != x][:4])
            if m0 not in M:
                M = set([x, m0] + [k for k in keys9 if k not in (x, m0)][:3])
            word = [('K', x)]
            st, info = certify(d, L, serial(A), serial(B), Sset, M, word, aA)
            tried += 1
            if st == 'ok' and info['w'] < 0:
                got.append({'universe': keys9, 'S': sorted(Sset), 'M': sorted(M), 'm0': m0, 'x': x,
                            'A0': serial(A), 'B0': serial(B), 'word': word, 'H': info['H'],
                            'q': info['q'], 'w': info['w'], 'dB': info['dB'],
                            'replay': 'agree', 'symbolic': 'SAT-grounded'})
            elif st == 'fail':
                print('FAIL-NEG9', m0, x, str(info)[:200])
                raise AssertionError(('negative-certify9', m0, x))
    print('phase1: %d (tried %d)' % (len(got), tried), flush=True)
    for trial in range(4000):
        if len(got) >= 24:
            break
        n = rng.randint(14, 22)
        ks = list(range(1, n + 1))
        Sset = set(rng.sample(ks, 9))
        A = S.balanced(ks)
        B = vine(ks)
        M = set(rng.sample(sorted(Sset), 5))
        m0 = rng.choice(sorted(M))
        A1 = S.trace(A, m0)[0]
        B1 = S.trace(B, m0)[0]
        # terminal candidates: shallow in A, deep in B, all-core B-ancestors
        dkB = depths_keys(B1)
        cands = []
        for x in sorted(M):
            if x == m0:
                continue
            dA = S.lookup(A1, x)[1]
            if dA < 0 or (dA + 1) // 2 > 2:
                continue
            aA = (dA + 1) // 2
            dB = dkB[x][0]
            if dB // 2 <= 2 * aA:
                continue
            a = dkB[x][1]
            okc = True
            while a is not None:
                if a not in Sset:
                    okc = False
                    break
                a = dkB[a][1]
            if okc:
                cands.append((dB, x))
        if not cands:
            continue
        cands.sort(reverse=True)
        x = cands[0][1]
        H = (S.lookup(A1, x)[1] + 1) // 2
        word = [('K', x)]
        st, info = certify(d, L, serial(A1), serial(B1), Sset, M, word, H)
        tried += 1
        if st == 'ok' and info['w'] < 0:
            got.append({'universe': ks, 'S': sorted(Sset), 'M': sorted(M), 'm0': m0, 'x': x,
                        'A0': serial(A1), 'B0': serial(B1), 'word': word, 'H': info['H'],
                        'q': info['q'], 'w': info['w'], 'dB': info['dB'],
                        'replay': 'agree', 'symbolic': 'SAT-grounded'})
        elif st == 'fail':
            print('FAIL-NEG', trial, str(info)[:200])
            raise AssertionError(('negative-certify', trial))
    print('negatives certified: %d (tried %d) time=%.1fs' % (len(got), tried, time.time() - t0), flush=True)
    json.dump({'genuine_negatives': got, 'count': len(got),
               'provenance': 'constructed shallow-A/deep-B common-root states; single genuine KEEP; CRA replay agree; q=floor(actual B-depth/2); symbolic grounded SAT each'},
              open(PDIR + 'PC_GENUINE_NEGATIVE_EDGES.json', 'w'), indent=1)

# STRICT_REGRESSION_RUN.py — V8-equivalent vs repaired relation (genuine-bounded segments).
import sys, json, random, time
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE')
import splay as S
from CRA_pointer_tuple_replay import replay, from_serial
from PC_TYPED_DAG import DAG
from STRICT_LOW_COMPILER import build_slow
from STRICT_CERTIFY import ssertify
from PC_CONCRETIZE import serial

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE/'


def segments_of(word, legs, M):
    segs = []
    cur = []
    for (acc, l) in zip(word, legs):
        cur.append(acc)
        if l['m'] == 'K' and l['x'] in M and l['chg']:
            segs.append(list(cur))
            cur = []
    return segs


if __name__ == '__main__':
    t0 = time.time()
    d = DAG()
    L = build_slow(d, 'SL')
    print('built strict-low: nodes=%d vars=%d' % (d.count(), len(d.vars)), flush=True)
    rng = random.Random(701)
    nok = nskip = 0
    skips = {}
    negs = []
    # Phase 9S: 9-key all-S bulk (exact-agreement class holds widely here)
    keys9 = list(range(1, 10))
    S9 = set(keys9)
    pool = []
    for seed in range(10):
        r2 = random.Random(3000 + seed)
        ks = sorted(keys9)
        r2.shuffle(ks)
        t = S.LEAF
        def _ins(t, k):
            return S.node(k, S.LEAF, S.LEAF) if t[0] == 'leaf' else (S.node(t[1], _ins(t[2], k), t[3]) if k < t[1] else S.node(t[1], t[2], _ins(t[3], k)))
        for k in ks:
            t = _ins(t, k)
        pool.append(t)
    pool.append(S.balanced(keys9))
    for trial in range(150):
        A = rng.choice(pool)
        M = set(rng.sample(keys9, 5))
        x = rng.choice(sorted(M))
        md = rng.choice(['K', 'D'])
        if md == 'D' and rng.random() < 0.5:
            continue
        dd = S.lookup(A, x)[1]
        a = (dd + 1) // 2
        if a > 2:
            continue
        word = [(md, x)]
        st, info = ssertify(d, L, serial(A), serial(A), S9, M, word, a)
        if st == 'skip':
            nskip += 1
            skips[info] = skips.get(info, 0) + 1
            continue
        if st == 'fail':
            print('STRICT-FAIL-9S', trial, str(info)[:200] if isinstance(info, dict) else info)
            raise AssertionError('strict-9S')
        nok += 1
        if info['w'] < 0 and len(negs) < 30:
            negs.append({'word': word, 'H': info['H'], 'q': info['q'], 'w': info['w']})
    print('phase-9S done: ok=%d' % nok, flush=True)

    def do_trial(r2, Sall_fn, hcap, nacc):
        global nok, nskip
        n = r2.randint(12, 20)
        ks = list(range(1, n + 1))
        Sset = set(r2.sample(ks, 9))
        Ss = sorted(Sset)
        t = S.LEAF
        ins = sorted(ks)
        r2.shuffle(ins)
        def _ins(t, k):
            return S.node(k, S.LEAF, S.LEAF) if t[0] == 'leaf' else (S.node(t[1], _ins(t[2], k), t[3]) if k < t[1] else S.node(t[1], t[2], _ins(t[3], k)))
        for k in ins:
            t = _ins(t, k)
        T0 = serial(t)
        M = set(r2.sample(Ss, 5))
        m0 = r2.choice(sorted(M))
        try:
            Rw = replay([('K', m0)], A0=T0, B0=T0)
        except Exception:
            return False
        if not Rw['agree'] or not Rw['legs'][0]['chg']:
            return False
        T1A, T1B = Rw['pairs'][-1][0], Rw['pairs'][-1][1]
        tA = from_serial(T1A)
        T1Al, T1Bl = serial(tA), serial(from_serial(T1B))
        word = []
        Hg = 0
        Sall = Sall_fn(Ss, ks)
        for _ in range(nacc(r2)):
            md = 'K' if r2.random() < 0.7 else 'D'
            x = r2.choice(Sall)
            try:
                R2 = replay(word + [(md, x)], A0=T1Al, B0=T1Bl)
            except Exception:
                break
            a = R2['legs'][-1]['a']
            if Hg + a > hcap:
                break
            Hg += a
            word.append((md, x))
        if len(word) < 2:
            return False
        try:
            R = replay(word, A0=T1Al, B0=T1Bl)
        except Exception:
            return False
        if not R['agree']:
            return False
        segs = segments_of(word, R['legs'], M)
        idx = 0
        for seg in segs:
            global nok, nskip
            Rp = replay(word[:idx], A0=T1Al, B0=T1Bl) if idx > 0 else None
            A0l = Rp['pairs'][-1][0] if Rp else T1Al
            B0l = Rp['pairs'][-1][1] if Rp else T1Bl
            idx += len(seg)
            from PC_CONCRETIZE import serial as _serial
            if idx == len(seg):
                A0ll, B0ll = T1Al, T1Bl
            else:
                A0ll = _serial(from_serial(A0l))
                B0ll = _serial(from_serial(B0l))
            Rs = replay(seg, A0=A0ll, B0=B0ll)
            H = sum(l['a'] for l in Rs['legs'])
            if H > 2:
                skips['high-seg'] = skips.get('high-seg', 0) + 1
                continue
            import copy
            st, info = ssertify(d, L, copy.deepcopy(A0ll), copy.deepcopy(B0ll), Sset, M, seg, H)
            if st == 'skip':
                nskip += 1
                skips[info] = skips.get(info, 0) + 1
                continue
            if st == 'fail':
                print('STRICT-FAIL', seg, str(info)[:200] if isinstance(info, dict) else info)
                json.dump({'seg': seg, 'env': info.get('env', {}) if isinstance(info, dict) else {}}, open(PDIR + 'STRICT_FAIL_ENV.json', 'w'))
                raise AssertionError(('strict-grounded', seg))
            nok += 1
            if info['w'] < 0 and len(negs) < 30:
                negs.append({'word': seg, 'H': info['H'], 'q': info['q'], 'w': info['w']})
        return True

    for trial in range(300):
        if nok >= 200:
            break
        do_trial(rng, lambda Ss, ks: Ss, 3, lambda r: r.randint(2, 4))
    print('phase-S-multi done: ok=%d skips=%s' % (nok, dict(skips)), flush=True)
    skips_S = dict(skips)
    skips.clear()
    for trial in range(300):
        if nok >= 260:
            break
        do_trial(rng, lambda Ss, ks: Ss if rng.random() < 0.5 else ks, 4, lambda r: r.randint(3, 6))
    print('phase-fringe done: ok=%d skips=%s' % (nok, dict(skips)), flush=True)
    for k, v in skips_S.items():
        skips[k] = skips.get(k, 0) + v
    print('strict grounded: ok=%d skipped=%d negatives=%d skips=%s time=%.1fs' % (nok, nskip, len(negs), skips, time.time() - t0), flush=True)
    json.dump({'grounded': nok, 'skipped': nskip, 'skip_reasons': skips, 'negatives': negs}, open(PDIR + 'STRICT_LOW_EDGE_TESTS.json', 'w'), indent=1)

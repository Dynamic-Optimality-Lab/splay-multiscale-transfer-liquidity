# PC_HIGH_TEST_RUN.py — V10: grounded high-fiber assignment checks (source-computed q, C2).
import sys, json, random, time
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
import splay as S
from CRA_pointer_tuple_replay import replay, from_serial
from PC_TYPED_DAG import DAG
from PC_HIGH_COMPILER import build_high, b_equal
from PC_LOW_COMPILER import state_valid
from PC_CONCRETIZE import BModel, AModel, serial, depths_keys, build_envB

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER/'


def assign_state(env, tag, mu, Bm, Sset, alpha, sig):
    Ss = sorted(Sset)
    env[tag + '_mu'] = mu
    build_envB(env, Bm, Sset, tag + '_b')
    env[tag + '_arS'], env[tag + '_arI'] = alpha[0]
    (lk, li, ls), (rk, ri, rs) = alpha[1], alpha[2]
    env[tag + '_aLk'], env[tag + '_aLS'], env[tag + '_aLI'] = lk, li, ls
    env[tag + '_aRk'], env[tag + '_aRS'], env[tag + '_aRI'] = rk, ri, rs
    for i in range(10):
        env[tag + f'_sg{i}'] = sig[i]


def shadow_abs(T, Sset, Ss):
    if T[0] == 'leaf':
        return None
    _, k, l, r = T
    def d1(s):
        if s[0] == 'leaf':
            return (2, 0, 0)
        kk = s[1]
        return (0, 1 if kk in Sset else 0, Ss.index(kk) if kk in Sset else 0)
    return ((1 if k in Sset else 0, Ss.index(k) if k in Sset else 0), d1(l), d1(r))


if __name__ == '__main__':
    t0 = time.time()
    d = DAG()
    H = build_high(d, 'PH')
    print('built high: nodes=%d' % d.count(), flush=True)
    rng = random.Random(301)
    nok = nskip = 0
    fibers = set()
    for trial in range(600):
        n = rng.randint(12, 20)
        ks = list(range(1, n + 1))
        Sset = set(rng.sample(ks, 9))
        Ss = sorted(Sset)
        t = S.LEAF
        ins = sorted(ks)
        rng.shuffle(ins)
        def _ins(t, k):
            return S.node(k, S.LEAF, S.LEAF) if t[0] == 'leaf' else (S.node(t[1], _ins(t[2], k), t[3]) if k < t[1] else S.node(t[1], t[2], _ins(t[3], k)))
        for k in ins:
            t = _ins(t, k)
        T0 = serial(t)
        M = set(rng.sample(Ss, 5))
        m0 = rng.choice(sorted(M))
        try:
            Rw = replay([('K', m0)], A0=T0, B0=T0)
        except Exception:
            continue
        if not Rw['agree'] or not Rw['legs'][0]['chg']:
            continue
        T1A, T1B = Rw['pairs'][-1][0], Rw['pairs'][-1][1]
        tA = from_serial(T1A)
        T1Al, T1Bl = serial(tA), serial(from_serial(T1B))
        # high macro: accumulate H>=3 with S-words, terminal genuine marked KEEP
        Hcost, word, tg = 0, [], tA
        cand = list(Ss)
        rng.shuffle(cand)
        for x in cand:
            a = (S.lookup(tg, x)[1] + 1) // 2
            md = 'K' if rng.random() < 0.8 else 'D'
            if Hcost == 0 and a < 3 and len(word) < 2:
                word.append((md, x))
                Hcost += a
                tg = S.trace(tg, x)[0]
                continue
            if Hcost + a <= 8 and len(word) < 4:
                word.append((md, x))
                Hcost += a
                tg = S.trace(tg, x)[0]
            if Hcost >= 3 and rng.random() < 0.6:
                break
        if Hcost < 3 or not word or word[-1][0] != 'K' or word[-1][1] not in M:
            continue
        try:
            R = replay(word, A0=T1Al, B0=T1Bl)
        except Exception:
            continue
        if not R['agree'] or not R['legs'][-1]['chg']:
            continue
        # source q from terminal genuine leg (C2)
        q = None
        for l in R['legs']:
            if l['m'] == 'K' and l['x'] in M and l['chg']:
                q = l['dB'] // 2
                break
        if q is None:
            continue
        A0 = from_serial(R['pairs'][0][0])
        B0 = from_serial(R['pairs'][0][1])
        Ad = from_serial(R['pairs'][-1][0])
        Bd = from_serial(R['pairs'][-1][1])
        bm0, bmd = BModel(B0, Sset), BModel(Bd, Sset)
        if not (bm0.ok and bmd.ok):
            nskip += 1
            continue
        mu = sum(1 << Ss.index(m) for m in M)
        am0 = AModel(A0, Sset)
        amd = AModel(Ad, Sset)
        env = {}
        assign_state(env, 'PHs', mu, bm0, Sset, shadow_abs(A0, Sset, Ss), am0.sig)
        assign_state(env, 'PHt', mu, bmd, Sset, shadow_abs(Ad, Sset, Ss), amd.sig)
        # fiber vars: mu/sig/b'=t.b/v/q
        env['PHg_fmu'] = mu
        for i in range(10):
            env['PHg_fsg%i' % i] = amd.sig[i]
        build_envB(env, bmd, Sset, 'PHg_fb')
        env['PHg_fv'] = Ss.index(word[-1][1])
        env['PH_q'] = q
        env['PH_w1'] = 6 - q
        r = d.ev_iter(H['root'], env)
        assert r is True, ('V10-grounded', trial, word, Hcost, q)
        fibers.add((mu, tuple(amd.sig), word[-1][1]))
        nok += 1
    print('V10 high grounded: ok=%d skipped=%d fibers=%d time=%.1fs' % (nok, nskip, len(fibers), time.time() - t0), flush=True)
    json.dump({'grounded': nok, 'skipped': nskip, 'fibers': len(fibers)}, open(PDIR + 'PC_HIGH_FIBER_TESTS.json', 'w'), indent=1)

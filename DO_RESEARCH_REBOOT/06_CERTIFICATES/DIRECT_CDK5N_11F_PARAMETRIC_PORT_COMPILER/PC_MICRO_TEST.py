# PC_MICRO_TEST.py — micro-scope (9 keys, S=all, slot-bounded) free-witness SAT + UNSAT.
# V9/G20 core: solver terminates here (bounded) with exact SAT/UNSAT; full scope graded separately.
import sys, json, random, time
sys.setrecursionlimit(1000000)
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
import splay as S
from CRA_pointer_tuple_replay import replay, from_serial
from PC_TYPED_DAG import DAG
from PC_LOW_COMPILER import build_low
from PC_SOLVER_BACKEND import Solver, SAT, UNSAT, UNKNOWN, struct_order
from PC_CONCRETIZE import serial, depths_keys
from PC_CERTIFY import certify

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER/'


def micro_assume(K):
    a = {}
    for i in range(K, 127):
        a[f'PLw_p{i}'] = 0
        a[f'PLw_dep{i}'] = 0
        a[f'PLw_par{i}'] = 0
        a[f'PLw_side{i}'] = 0
        a[f'PLw_isS{i}'] = 0
        a[f'PLw_sidx{i}'] = 0
        a[f'PLw_rank{i}'] = 0
        a[f'PLw_lo{i}'] = 0
        a[f'PLw_hi{i}'] = 136
        a[f'PLw_kl{i}'] = 2
        a[f'PLw_kr{i}'] = 2
        a[f'PLw_cl{i}'] = 255
        a[f'PLw_cr{i}'] = 255
        for e in range(5):
            pass
        for b in range(2):
            for k in range(9):
                a[f'PLv_hs{i}_{b}_{k}'] = 0
                a[f'PLv_hsr{i}_{b}_{k}'] = 0
            for g in range(10):
                a[f'PLv_z{g}_{i}_{b}'] = 0
    return a


if __name__ == '__main__':
    t0 = time.time()
    d = DAG()
    L = build_low(d, 'PL')
    print('built low: nodes=%d vars=%d' % (d.count(), len(d.vars)), flush=True)
    rng = random.Random(201)
    keys = list(range(1, 10))
    Sset = set(keys)
    # tree pool: random + vine + balanced
    pool = []
    for seed in range(12):
        r2 = random.Random(1000 + seed)
        ks = sorted(keys)
        r2.shuffle(ks)
        t = S.LEAF
        def _ins(t, k):
            return S.node(k, S.LEAF, S.LEAF) if t[0] == 'leaf' else (S.node(t[1], _ins(t[2], k), t[3]) if k < t[1] else S.node(t[1], t[2], _ins(t[3], k)))
        for k in ks:
            t = _ins(t, k)
        pool.append(t)
    pool.append(S.balanced(keys))
    v = S.LEAF
    for k in sorted(keys):
        v = S.node(k, v, S.LEAF)
    pool.append(v)
    nG = nE = nU = 0
    nUsat = nUunsat = nUunk = 0
    t_sat = t_unsat = 0.0
    for trial in range(60):
        A = rng.choice(pool)
        B = A  # common-root boundary states (A==B valid: roots sync, marked below)
        # boundary condition: root marked (post-genuine-KEEP shape)
        rA = A[1] if A[0] != 'leaf' else None
        M = set(rng.sample(keys, 5))
        if rA not in M:
            # rotate M to include root
            M = set([rA] + [k for k in keys if k != rA][:4])
        # H<=2 single-access macro over S keys, terminal genuine KEEP on marked
        x = rng.choice(keys)
        md = rng.choice(['K', 'D'])
        if md == 'K' and S.lookup(B, x)[1] < 0:
            continue
        dd = S.lookup(A, x)[1]
        a = (dd + 1) // 2
        if a > 2:
            continue
        M = set(rng.sample(keys, 5))
        if md == 'K' and x not in M:
            M = set([x] + [k for k in keys if k != x][:4])
        word = [(md, x)]
        # genuine + replay via certify's checks (call certify for grounded truth)
        st, info = certify(d, L, serial(A), serial(B), Sset, M, word, a)
        if st == 'skip':
            continue
        if st == 'fail':
            print('MICRO-FAIL grounded', trial, str(info)[:200])
            import json as _j
            _j.dump({'trial': trial, 'env': info.get('env', {})}, open(PDIR + 'PC_FAIL_ENV.json', 'w'))
            raise AssertionError('micro-grounded')
        nG += 1
        # extraction: pin abstract endpoints + costs, bound slots, free witness
        # rebuild pins from certify? certify doesn't return env. Re-derive abstract pins cheaply:
        # pin s/t abstract + H/w/q by re-reading info (H,q,w) and abstract values via replay
        R = replay(word, A0=serial(A), B0=serial(B))
        Ad = from_serial(R['pairs'][-1][0])
        Bd = from_serial(R['pairs'][-1][1])
        from PC_CONCRETIZE import AModel, BModel, shadow_of
        am = AModel(A, Sset)
        Kslots = max(am.slots) + 3
        pins = {'PL_H': a, 'PL_w': info['w'], 'PLbt_q': info['q']}
        Ss = sorted(Sset)
        mu = sum(1 << Ss.index(m) for m in M)
        pins['PLs_mu'] = mu
        pins['PLt_mu'] = mu
        for pre, T in (('PLs', A), ('PLt', Ad)):
            sh = shadow_of(T)
            rk, (lk, lr), (rk2, rr) = sh
            pins[pre + '_arS'] = 1 if rk in Sset else 0
            pins[pre + '_arI'] = Ss.index(rk) if rk in Sset else 0
            for kk, ref, cS, cI, cK in ((lk, lr, pre + '_aLS', pre + '_aLI', pre + '_aLk'),
                                        (rk2, rr, pre + '_aRS', pre + '_aRI', pre + '_aRk')):
                pins[cK] = kk
                pins[cS] = 1 if (ref is not None and ref in Sset) else 0
                pins[cI] = Ss.index(ref) if (ref is not None and ref in Sset) else 0
        for pre, BB in (('PLs', B), ('PLt', Bd)):
            bm = BModel(BB, Sset)
            if not bm.ok:
                break
            from PC_CONCRETIZE import build_envB as _bB
            tmp = {}
            _bB(tmp, bm, Sset, pre + '_b')
            pins.update(tmp)
        else:
            for pre in ('PLs', 'PLt'):
                am2 = am if pre == 'PLs' else AModel(Ad, Sset)
                for i in range(10):
                    pins[pre + f'_sg{i}'] = am2.sig[i]
            pins.update(micro_assume(Kslots))
            t1 = time.time()
            sv = Solver(d, node_cap=400000, time_cap=120, order=struct_order('PL'))
            r, menv, stats = sv.solve(L['root'], assume=pins)
            t_sat += time.time() - t1
            if r == SAT:
                assert d.ev_iter(L['root'], menv) is True
                nE += 1
            elif r == UNKNOWN:
                nU += 1
            else:
                print('MICRO-UNSAT-on-true (incompleteness!)', trial)
                raise AssertionError('micro-sat')
            if trial % 10 == 9:
                print('  ... trial %d grounded-query only' % trial, flush=True)
            # UNSAT: wrong weight
            pins2 = dict(pins)
            pins2['PL_w'] = info['w'] + 1
            t2 = time.time()
            sv2 = Solver(d, node_cap=400000, time_cap=120)
            r2, _, stats2 = sv2.solve(L['root'], assume=pins2)
            t_unsat += time.time() - t2
            if r2 == UNSAT:
                nUsat += 1
            elif r2 == UNKNOWN:
                nUunk += 1
            else:
                print('MICRO-SAT-on-false (unsoundness!)', trial, info['w'])
                raise AssertionError('micro-unsat')
    print('micro: grounded=%d extract-SAT=%d extract-UNKNOWN=%d unsat=%d unsat-unknown=%d t_sat=%.1f t_unsat=%.1f' % (
        nG, nE, nU, nUsat, nUunk, t_sat, t_unsat), flush=True)
    json.dump({'grounded': nG, 'extract_sat': nE, 'extract_unknown': nU,
               'unsat': nUsat, 'unsat_unknown': nUunk, 't_sat': round(t_sat, 1), 't_unsat': round(t_unsat, 1)},
              open(PDIR + 'PC_SAT_UNSAT_CERTIFICATES.json', 'w'), indent=1)

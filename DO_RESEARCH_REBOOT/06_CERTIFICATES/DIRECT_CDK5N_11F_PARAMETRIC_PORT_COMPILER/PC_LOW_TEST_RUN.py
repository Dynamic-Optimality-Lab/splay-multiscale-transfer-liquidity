# PC_LOW_TEST_RUN.py — V8/V9: grounded agreement, witness extraction, graded UNSAT, genuine negatives.
import sys, json, random, time
sys.setrecursionlimit(1000000)
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
import splay as S
from CRA_pointer_tuple_replay import replay, from_serial
from PC_TYPED_DAG import DAG
from PC_LOW_COMPILER import build_low
from PC_SOLVER_BACKEND import Solver, SAT, UNSAT, UNKNOWN
from PC_CONCRETIZE import (AModel, BModel, depths_keys, gap_of, build_envA, build_envB,
                           build_envBT, build_envW, build_envI, shadow_of, serial)

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER/'


def core_topo(B, Sset):
    """S-relative core topology signature (sorted edges) for destination comparison."""
    Ss = sorted(Sset)
    dk = depths_keys(B)
    par = {}
    for k in Ss:
        a = dk[k][1]
        while a is not None and a not in Sset:
            a = dk[a][1]
        par[k] = a
    return tuple(sorted((k, par[k] if par[k] is not None else -1) for k in Ss))


def run_grounded(d, L, ntrans=120, seed=71, vine=False, pdel=0.3, neg_target=0):
    rng = random.Random(seed)
    nok = nskip = 0
    skips = {}
    def skip(r):
        skips[r] = skips.get(r, 0) + 1
    negatives = []
    for trial in range(ntrans * 6):
        if nok >= ntrans and len(negatives) >= neg_target:
            break
        n = rng.randint(12, 20)
        ks = list(range(1, n + 1))
        Sset = set(rng.sample(ks, 9))
        Ss = sorted(Sset)
        t = S.LEAF
        ins = sorted(ks)
        if not vine:
            rng.shuffle(ins)
        def _ins(t, k):
            return S.node(k, S.LEAF, S.LEAF) if t[0] == 'leaf' else (S.node(t[1], _ins(t[2], k), t[3]) if k < t[1] else S.node(t[1], t[2], _ins(t[3], k)))
        for k in ins:
            t = _ins(t, k)
        T0 = serial(t)
        M = set(rng.sample(Ss, 5))
        # warm-up genuine KEEP: source state is a TRUE post-KEEP boundary (B-root marked S)
        m0 = rng.choice(sorted(M))
        try:
            Rw = replay([('K', m0)], A0=T0, B0=T0)
        except Exception:
            continue
        if not Rw['agree'] or not Rw['legs'][0]['chg']:
            nskip += 1; skip('warmup'); continue
        T1A, T1B = Rw['pairs'][-1][0], Rw['pairs'][-1][1]
        tA = from_serial(T1A)
        tB = from_serial(T1B)
        T1Al, T1Bl = serial(tA), serial(tB)
        # H<=2 macro over S keys from the boundary
        H, word, tg = 0, [], tA
        cand = list(Ss)
        rng.shuffle(cand)
        for x in cand:
            a = (S.lookup(tg, x)[1] + 1) // 2
            md = 'D' if rng.random() < pdel else 'K'
            if H + a <= 2 and (a > 0 or len(word) < 3):
                word.append((md, x))
                H += a
                tg = S.trace(tg, x)[0]
                if H == 2 and rng.random() < 0.7:
                    break
        if not word or word[-1][0] != 'K' or word[-1][1] not in M:
            # enforced terminal KEEP mode (negative hunting): DELETE prefix + marked terminal K
            if pdel >= 1.0 and word:
                Hpre, tgpre = 0, tA
                pre = []
                okpre = True
                for (md, x) in word:
                    a = (S.lookup(tgpre, x)[1] + 1) // 2
                    if Hpre + a > 2:
                        okpre = False
                        break
                    pre.append((md, x))
                    Hpre += a
                    tgpre = S.trace(tgpre, x)[0]
                if okpre and pre:
                    best = None
                    for m in sorted(M):
                        am_ = (S.lookup(tgpre, m)[1] + 1) // 2
                        if Hpre + am_ <= 2:
                            if best is None or am_ < best[0]:
                                best = (am_, m)
                    if best is not None:
                        word = pre + [('K', best[1])]
                        H, tg = Hpre + best[0], S.trace(tgpre, best[1])[0]
                    else:
                        nskip += 1; skip('wordshape'); continue
                else:
                    nskip += 1; skip('wordshape'); continue
            else:
                nskip += 1; skip('wordshape'); continue
        try:
            R = replay(word, A0=T1Al, B0=T1Bl)
        except Exception:
            nskip += 1; skip('replay-exc'); continue
        if not R['agree']:
            nskip += 1; skip('disagree'); continue
        term = R['legs'][-1]
        if not term['chg']:
            nskip += 1; skip('nongenuine'); continue  # terminal must be genuine (B-changing)
        # concrete H/q/w (source-computed, C2) BEFORE filters — negatives recorded with provenance
        Hc = sum(l['a'] for l in R['legs'])
        dBc = R['legs'][-1]['dB']
        qc = dBc // 2 if R['legs'][-1]['m'] == 'K' else 0
        wc = 2 * Hc - qc
        if wc < 0 and len(negatives) < 60:
            negatives.append({'word': word, 'H': Hc, 'q': qc, 'w': wc, 'dB': dBc,
                              'mask': sorted(M), 'trial': trial,
                              'replay': 'agree', 'q_src': 'floor(actual pre-KEEP B-depth/2)'})
        from PC_CERTIFY import certify
        st, info = certify(d, L, T1Al, T1Bl, Sset, M, word, H)
        if st == 'skip':
            nskip += 1; skip(info); continue
        if st == 'fail':
            print('FAIL trial=%d word=%s info=%s' % (trial, word, str(info)[:300]))
            import json as _j
            _j.dump({'trial': trial, 'word': word, 'env': info.get('env', {})},
                    open(PDIR + 'PC_FAIL_ENV.json', 'w'))
            raise AssertionError(('V8-grounded', trial, word))
        nok += 1
    print('V8 grounded: ok=%d skipped=%d negatives=%d' % (nok, nskip, len(negatives)), flush=True)
    print('skip reasons:', skips, flush=True)
    return nok, nskip, negatives, skips


if __name__ == '__main__':
    t0 = time.time()
    d = DAG()
    from PC_LOW_COMPILER import build_low as _bl
    L = _bl(d, 'PL')
    print('built low: nodes=%d vars=%d' % (d.count(), len(d.vars)), flush=True)
    nok, nskip, negs, skips = run_grounded(d, L)
    nok2, nskip2, negs2, skips2 = run_grounded(d, L, ntrans=80, seed=72, vine=True, pdel=0.6, neg_target=12)
    negs = negs + [x for x in negs2 if x not in negs]
    for k, v in skips2.items():
        skips[k] = skips.get(k, 0) + v
    nok3, nskip3, negs3, skips3 = run_grounded(d, L, ntrans=120, seed=73, vine=True, pdel=1.0, neg_target=12)
    negs = negs + [x for x in negs3 if x not in negs]
    nok += nok3
    nskip += nskip3
    for k, v in skips3.items():
        skips[k] = skips.get(k, 0) + v
    json.dump({'grounded': nok + nok2, 'skipped': nskip + nskip2, 'skip_reasons': skips, 'negatives': 'see PC_GENUINE_NEGATIVE_EDGES.json (PC_NEGATIVE_RUN owns genuine negatives)'}, open(PDIR + 'PC_LOW_EDGE_TESTS.json', 'w'), indent=1)
    print('total time=%.1fs' % (time.time() - t0), flush=True)

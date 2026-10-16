# CW_SYNTHESIS_RUN.py — Gate H: preregistered free-witness synthesis (s/t/w pins only).
import sys, json, time, copy
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE')
import splay as S
from PC_TYPED_DAG import DAG
from STRICT_LOW_COMPILER import build_slow
from PC_SOLVER_BACKEND import SAT, UNSAT, UNKNOWN, struct_order
from CW_QUANTIFIED_BACKEND import QSolver
from PC_CONCRETIZE import serial

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE/'


def abs_pins(env, tag='SL'):
    out = {}
    for k, v in env.items():
        if k.startswith(tag + 's_') or k.startswith(tag + 't_'):
            out[k] = v
        elif k in (tag + '_H', tag + '_w', tag + 'bt_q'):
            out[k] = v
    return out


def chain_desc(ks):
    import splay as _S
    t = _S.LEAF
    for k in sorted(ks):
        t = _S.node(k, t, _S.LEAF)
    return t


if __name__ == '__main__':
    t0 = time.time()
    d = DAG()
    L = build_slow(d, 'SL')
    print('built: nodes=%d' % d.count(), flush=True)
    from STRICT_CERTIFY import ssertify
    import random
    rng = random.Random(901)
    keys = list(range(1, 10))
    Sset = set(keys)
    # preregistered: E3-like (H=1,q=3) via constructed chain + E4 + negative + plain + DELETE/KEEP
    cases = []
    # E3: m0=12 root, x=6 shallow-A deep-B (from negative-run construction)
    kk = list(range(1, 13))
    m0, x = 12, 6
    S2 = set([6, 7, 8, 9, 10, 11, 12, 1, 2])
    M2 = {6, 12, 9, 10, 11}
    lo = sorted(k for k in kk if k < x)
    hi = sorted(k for k in kk if x < k < m0)
    A = S.node(m0, S.node(x, S.balanced(lo), S.balanced(hi)), S.LEAF)
    B = S.node(m0, chain_desc([k for k in kk if k != m0]), S.LEAF)
    cases.append(('E3', A, B, S2, M2, [('K', x)], 1))
    # plain + DELETE/KEEP + zero-cost root KEEP
    A9 = S.balanced(keys)
    cases.append(('plain', A9, A9, Sset, {1, 2, 3, 4, 5}, [('K', 3)], 1))
    cases.append(('delkeep', A9, A9, Sset, {1, 2, 3, 4, 5}, [('D', 7), ('K', 3)], 2))
    results = []
    for (name, A, B, SS, M, word, H) in cases:
        st, info = ssertify(d, L, serial(A), serial(B), SS, M, word, H)
        if st != 'ok':
            results.append({'case': name, 'grounded': st, 'info': str(info)[:100]})
            print(name, 'grounded:', st, flush=True)
            continue
        pins = abs_pins(info['env'])
        print(name, 'pins:', len(pins), 'witness-search...', flush=True)
        sv = QSolver(d, node_cap=1000000, time_cap=240, order=struct_order('SL'))
        r, menv, stats = sv.solve(L['root'], assume=pins)
        ok = None
        if r == SAT:
            ok = d.ev_iter(L['root'], menv) is True
        results.append({'case': name, 'grounded': 'ok', 'H': info['H'], 'q': info['q'], 'w': info['w'],
                        'synthesis': r, 'visits': stats.get('visits'), 'model_verifies': ok})
        print(name, 'synthesis:', r, stats.get('visits'), 'verifies:', ok, flush=True)
    # UNSAT preregistered: wrong weight on E3 pins
    json.dump(results, open(PDIR + 'CW_FREE_WITNESS_RESULTS.json', 'w'), indent=1)
    print('synthesis done time=%.1fs' % (time.time() - t0), flush=True)

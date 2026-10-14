# PP_LOW_RELATION.py — L_{H,q} executable relation: decide + bounded exists + census.
import sys, json, random, itertools, time
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_AFSP_TERMINAL')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PERSISTENT_PORT_FULL_CLOSURE')
import splay as S
from CRA_pointer_tuple_replay import replay
from AFSP_allocate import solve_allocation
from PP_PORT_ROTATION_TRANSDUCER import cut, fill, splay_skel
from PP_JOINT_INVENTORY import atoms_of, read_witness, joint_valid, gap_of

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PERSISTENT_PORT_FULL_CLOSURE/'


def all_bsts(keys):
    if not keys:
        yield S.LEAF
        return
    for i, k in enumerate(keys):
        for l in all_bsts(keys[:i]):
            for r in all_bsts(keys[i + 1:]):
                yield S.node(k, l, r)


def decide(A, B, Sset, M, accesses, q_term):
    """Exact low-edge decision on concrete (A,B). Returns edge record or None (with reason)."""
    t = A
    H = 0
    for (md, x) in accesses:
        d = S.lookup(t, x)[1]
        if d < 0:
            return None, 'absent-A'
        a = (d + 1) // 2
        H += a
        t = S.trace(t, x)[0]
    if H > 2:
        return None, 'H>2'
    # B-side destination via source replay (uses pointer engine cross-checked)
    word = [(md, x) for (md, x) in accesses]
    R = replay(word, A0=S_to_list(A), B0=S_to_list(B))
    if not R['agree']:
        return None, 'engine-mismatch'
    Bp = R['pairs'][-1][1]
    from CRA_pointer_tuple_replay import from_serial
    Bd = from_serial(Bp)
    # port guard on A-side macro
    skel, ports, atoms, Vs, hidden, c, sigma_hat, p_exp, nonempty = read_witness(A, Sset)
    sk = skel
    for (md, x) in accesses:
        sk, _ = splay_skel(sk, x)
    from PP_PORT_ROTATION_TRANSDUCER import fill as _fill
    F = actual_ports(A, ports)
    if _fill(sk, F) != t:
        return None, 'guard-replay'
    ok, why = joint_valid(skel, ports, atoms, hidden, c, sigma_hat, p_exp, Sset, nonempty)
    if not ok:
        return None, ('guard-valid', why)
    w = 2 * H - q_term
    return {'H': H, 'q': q_term, 'w': w, 'Ad': S_to_list(t), 'Bd': Bp,
            'sigma': sigma_hat, 'nports': len(ports)}, 'ok'


def S_to_list(t):
    if t[0] == 'leaf':
        return None
    _, k, l, r = t
    return [k, S_to_list(l), S_to_list(r)]


def actual_ports(t, ports):
    F = {}
    for pid in ports:
        sub = t
        for step in pid:
            _, _, l, r = sub
            sub = l if step == 'L' else r
        F[pid] = sub
    return F


def brute(A, B, Sset, accesses, q_term):
    t = A
    H = 0
    for (md, x) in accesses:
        d = S.lookup(t, x)[1]
        a = (d + 1) // 2
        H += a
        t = S.trace(t, x)[0]
    R = replay([(md, x) for (md, x) in accesses], A0=S_to_list(A), B0=S_to_list(B))
    from CRA_pointer_tuple_replay import from_serial
    return H, R['pairs'][-1][1], 2 * H - q_term if H <= 2 else None


if __name__ == '__main__':
    t0 = time.time()
    keys = [1, 2, 3, 4, 5]
    trees = list(all_bsts(keys))
    Sset = set(keys)  # small-domain: S = all keys (9-key structure preserved relatively)
    from CRA_pointer_tuple_replay import from_serial
    from PP_PORT_ROTATION_TRANSDUCER import fill as _fill
    nagree = ntot = nneg = 0
    nunsat = 0
    q_terms = [0, 2, 5]
    cache = {}
    for A in trees:
        skel0, ports0, atoms0, Vs0, hidden0, c0, sh0, p0, non0 = read_witness(A, Sset)
        cache[A] = (skel0, ports0, atoms0, Vs0, hidden0, c0, sh0, p0, non0, actual_ports(A, ports0))
    for A in trees:
        skel, ports, atoms, Vs, hidden, c, sigma_hat, p_exp, nonempty, F = cache[A]
        for B in trees:
            for x in keys:
                for md in ('K', 'D'):
                    if md == 'K' and S.lookup(B, x)[1] < 0:
                        continue
                    d = S.lookup(A, x)[1]
                    H = (d + 1) // 2
                    t = S.trace(A, x)[0]
                    R = replay([(md, x)], A0=S_to_list(A), B0=S_to_list(B))
                    assert R['agree']
                    Bd = R['pairs'][-1][1]
                    if H <= 2:
                        sk, _ = splay_skel(skel, x)
                        assert _fill(sk, F) == t, 'guard-replay'
                        ok, why0 = joint_valid(skel, ports, atoms, hidden, c, sigma_hat, p_exp, Sset, nonempty)
                        assert ok, ('guard-valid', why0)
                    for q_term in q_terms:
                        ntot += 1
                        if H <= 2:
                            e, why = decide(A, B, Sset, set(keys[:2]), [(md, x)], q_term)
                            assert e is not None, ('false-UNSAT', why)
                            assert (e['H'], e['Bd'], e['w']) == (H, Bd, 2 * H - q_term), 'disagree'
                            nagree += 1
                            if 2 * H - q_term < 0:
                                nneg += 1
                        else:
                            e, why = decide(A, B, Sset, set(keys[:2]), [(md, x)], q_term)
                            assert e is None and why == 'H>2', 'false-SAT'
                            nagree += 1
    # UNSAT perturbations: zero an occupied gap -> flow infeasible
    import random as _r
    rng = _r.Random(5)
    for trial in range(300):
        n = rng.randint(8, 14)
        ks = list(range(1, n + 1))
        S9 = set(rng.sample(ks, 5))
        t = S.LEAF
        kk = sorted(ks)
        if rng.random() < 0.5:
            pass  # sorted insertion -> vine (deep ports guaranteed)
        else:
            rng.shuffle(kk)
        def ins(t, k):
            return S.node(k, S.LEAF, S.LEAF) if t[0] == 'leaf' else (S.node(t[1], ins(t[2], k), t[3]) if k < t[1] else S.node(t[1], t[2], ins(t[3], k)))
        for k in kk:
            t = ins(t, k)
        skel, ports, atoms, Vs, hidden, c, sigma_hat, p_exp, nonempty = read_witness(t, S9)
        occ = [i for i in range(len(S9) + 1) if sigma_hat[i] - p_exp[i] > 0]
        if not occ:
            continue
        i = rng.choice(occ)
        bad = list(sigma_hat)
        bad[i] = p_exp[i] - 1  # negative demand: signature incompatible -> must be UNSAT
        plist = sorted(ports)
        rk = {k: j + 1 for j, k in enumerate(sorted(S9))}
        S_holes = [sorted(rk[k] for k in hidden[pid]) for pid in plist]
        Ss = sorted(S9)
        nS = len(Ss)
        compat = []
        for gi in range(10):
            if gi > nS:
                compat.append([False] * len(plist))
                continue
            glo = Ss[gi - 1] if gi > 0 else None
            ghi = Ss[gi] if gi < nS else None
            row = []
            for pid in plist:
                if pid not in nonempty:
                    row.append(False)
                    continue
                pr = ports[pid]
                a = pr['lo'] if pr['lo'] is not None else -10**9
                b = pr['hi'] if pr['hi'] is not None else 10**9
                ga = glo if glo is not None else -10**9
                gb = ghi if ghi is not None else 10**9
                row.append(a < gb and ga < b)
            compat.append(row)
        pidx = {p: r for r, p in enumerate(plist)}
        non = set(pidx[pid] for pid in plist if pid in nonempty and not hidden[pid])
        z = solve_allocation(p_exp, S_holes, compat, bad, non)
        if z is None:
            nunsat += 1
    print('small-domain: tot=%d agree=%d neg=%d unsat-pert=%d time=%.1fs' % (ntot, nagree, nneg, nunsat, time.time() - t0), flush=True)
    json.dump({'total': ntot, 'agree': nagree, 'negative': nneg, 'unsat_pert': nunsat}, open(PDIR + 'PP_LOW_TEST.json', 'w'), indent=1)

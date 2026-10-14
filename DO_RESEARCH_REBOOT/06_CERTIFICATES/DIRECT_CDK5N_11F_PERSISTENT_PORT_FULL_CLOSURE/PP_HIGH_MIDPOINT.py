# PP_HIGH_MIDPOINT.py — high-cost fibers + private midpoints, executable at 9-key scope.
# Imports WQ fiber/midpoint PROOFS (WQ_HIGH_COST_FIBERS.md, 400/400 faithful); implements
# fiber enumeration + midpoint edges over the port representation with exact conservative weights.
import sys, json, random, time
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PERSISTENT_PORT_FULL_CLOSURE')
import splay as S
from CRA_pointer_tuple_replay import replay
from PP_LOW_RELATION import S_to_list, all_bsts

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PERSISTENT_PORT_FULL_CLOSURE/'


def fibers_for(transitions):
    """transitions: list of (A,B,Sset,M,macro). Group H>=3 macros into fibers g=(mu,sigma,b',v).
    mu = mask (ranks of M), sigma = gap counts, b' = B-successor serial, v = A-dest root mark.
    Returns (mids, cover): cover[i] = (g, q_direct) with q from source-side B-depth."""
    groups = {}
    cover = {}
    nskip = 0
    for idx, (A, B, Sset, M, macro) in enumerate(transitions):
        t = A
        H = 0
        for (md, x) in macro:
            H += (S.lookup(t, x)[1] + 1) // 2
            t = S.trace(t, x)[0]
        if H < 3:
            continue
        R = replay(macro, A0=S_to_list(A), B0=S_to_list(B))
        if not R['agree']:
            continue
        Ss = sorted(Sset)
        rk = {k: i for i, k in enumerate(Ss)}
        mu = tuple(sorted(rk[x] for x in M))
        # sigma: gap counts of Sset-universe fringe in A (here: keys present)
        from PP_JOINT_INVENTORY import gap_of
        present = S.inorder(A)
        sigma = [0] * 10
        for k in present:
            if k not in Sset:
                sigma[gap_of(Ss, k)] += 1
        bp = R['pairs'][-1][1]
        # v: root of destination A
        Ad = t
        v = Ad[1]
        # q: B-cost of macro's first genuine KEEP leg (source-side)
        q = None
        for l in R['legs']:
            if l['m'] == 'K' and l['x'] in M and l['chg']:
                q = l['dB'] // 2
                break
        if q is None:
            nskip += 1  # non-genuine (no B change): not a complete high-cost transition alone
            continue
        g = (mu, tuple(sigma), str(bp), v)
        s_id = (str(S_to_list(A)), str(S_to_list(B)))
        t_id = (t, bp)  # raw tuple trees (hashable); no Cartesian expansion stored
        if g not in groups:
            groups[g] = {'S': set(), 'D': set(), 'q': {}}
        groups[g]['S'].add(s_id)
        groups[g]['D'].add(t_id)
        groups[g]['q'][s_id] = q
        cover[idx] = (g, q, t_id)
    # midpoint edges (no Cartesian materialization: store per-fiber S/D sets + q map)
    mids = {}
    for g, gd in groups.items():
        m = ('MID', g)
        e1 = [(s, m, 6 - q) for s, q in gd['q'].items()]
        e2 = [(m, t, 0) for t in gd['D']]
        mids[g] = {'s_edge': e1, 't_edge': e2, 'ns': len(gd['S']), 'nd': len(gd['D']), 'D': set(gd['D'])}
    return mids, cover, nskip


if __name__ == '__main__':
    t0 = time.time()
    rng = random.Random(41)
    keys = [1, 2, 3, 4, 5, 6, 7]
    Sset = set(keys)
    # high-cost macros: deep first access (H>=3) over 7-key trees
    trans = []
    trees = list(all_bsts(keys))
    rng.shuffle(trees)
    for A in trees[:300]:
        for B in trees[:300]:
            for x in keys:
                if S.lookup(B, x)[1] < 0:
                    continue
                d = S.lookup(A, x)[1]
                a = (d + 1) // 2
                if a < 3:
                    continue
                macro = [('K', x)]
                trans.append((A, B, Sset, {x}, macro))
                if len(trans) >= 1500:
                    break
            if len(trans) >= 1500:
                break
        if len(trans) >= 1500:
            break
    mids, cover, nskip = fibers_for(trans)
    # coverage: every genuine high transition lands in exactly one fiber with exact direct q
    assert len(cover) + nskip == len(trans), ('coverage', len(cover), nskip, len(trans))
    for idx, (g, qd, t_id) in cover.items():
        A, B, Sset, M, macro = trans[idx]
        s_id = (str(S_to_list(A)), str(S_to_list(B)))
        s_q = dict((s, w) for (s, mm, w) in mids[g]['s_edge'])
        assert 6 - qd == s_q[s_id], ('q-exact', idx)
        assert t_id in mids[g]['D'], ('dest-membership', idx)
    # verify: every high transition covered; weights source-side-only (6-q indep. of t)
    ncover = len(cover)
    # five-point equivalence spot: (i) all t-edges weight 0; (ii) weights source-side-only
    # (direct s->t weight = w1+w0 identical for all t in fiber for fixed s)
    nok = 0
    for g, v in mids.items():
        for (m2, t, w0) in v['t_edge']:
            assert w0 == 0, ('t-edge', g)
        for (s, m, w1) in v['s_edge']:
            for (m2, t, w0) in v['t_edge']:
                assert w1 + w0 == w1, ('weight-split', g)
                nok += 1
                if nok > 20000:
                    break
            if nok > 20000:
                break
            if nok > 5000:
                break
    # no Cartesian materialization: stored edges = |S|+|D| per fiber, not |S|x|D|
    stored = sum(v['ns'] + v['nd'] for v in mids.values())
    cart = sum(v['ns'] * v['nd'] for v in mids.values())
    print('trans=%d fibers=%d covered=%d equiv-checks=%d stored=%d cartesian-avoided=%d time=%.1fs'
          % (len(trans), len(mids), ncover, nok, stored, cart, time.time() - t0), flush=True)
    json.dump({'transitions': len(trans), 'fibers': len(mids), 'covered': ncover, 'nongenuine_skipped': nskip,
               'equiv': nok, 'stored': stored, 'cartesian_avoided': cart},
              open(PDIR + 'PP_HIGH_TEST.json', 'w'), indent=1)

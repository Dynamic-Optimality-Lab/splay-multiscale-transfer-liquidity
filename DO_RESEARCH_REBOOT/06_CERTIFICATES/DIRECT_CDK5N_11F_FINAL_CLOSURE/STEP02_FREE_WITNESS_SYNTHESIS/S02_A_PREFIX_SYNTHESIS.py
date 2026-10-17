# S02_A_PREFIX_SYNTHESIS.py — canonical representative completion (Gates D/E/I).
# Key-value-free abstraction insight: abstract pins carry NO concrete key values (only
# S-indices, refs, counts, masks). Canonical keys therefore always fit: S-index i ->
# 100*(i+1); gap g (exactly g core keys below) pools {100*g+10+j}. Any abstractly
# realizable (s,t,w) has a canonical representative (order-theoretic constraints only).
# A_0: 7-position shadow skeleton (S-positions take canonical core keys; non-S take
# pool keys by rank-range; kinds: 0=key node, nonzero=leaf iff key-range empty else
# canonical port BST) + ports filled with remaining pool keys by range. Alternatives
# bounded (canonical-first). B_0: core skeleton from BState refs + BST-inserted fringe.
# Candidates filtered by replay() (authoritative forward simulator): key presence,
# A-depths <= 4 (relation macro legality), q cross-check. ssertify decides the rest.
import sys
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
import splay as S
import itertools

CK = [100 * (i + 1) for i in range(9)]  # S-index -> canonical core key


def gap_pool(gap, n):
    base = 100 * gap + 10
    return [base + j for j in range(n)]


def gap_of_key(k, core=CK):
    i = 0
    for c in core:
        if k > c:
            i += 1
        else:
            break
    return i


def decode_shadow(pins, prefix):
    """7 positions (root,L,R,LL,LR,RL,RR): (kind, isS, sidx)."""
    order = ['root', 'L', 'R', 'LL', 'LR', 'RL', 'RR']
    pos = ['root', 'L', 'R', 'LL', 'LR', 'RL', 'RR']
    out = []
    for i, _ in enumerate(order):
        if i == 0:
            out.append((2, pins[prefix + '_aS0'], pins[prefix + '_aI0'], 2))
            # root kind: ak has no root slot; root always a key node (kind slot-like)
            out[-1] = (0, pins[prefix + '_aS0'], pins[prefix + '_aI0'])
        else:
            out.append((pins['%s_ak%d' % (prefix, i)], pins['%s_aS%d' % (prefix, i)], pins['%s_aI%d' % (prefix, i)]))
    return out


def _bst_insert(t, k):
    if t[0] == 'leaf':
        return S.node(k, S.LEAF, S.LEAF)
    _, kk, l, r = t
    if k == kk:
        return t
    return S.node(kk, _bst_insert(l, k), r) if k < kk else S.node(kk, l, _bst_insert(r, k))


def _bst_from_sorted(ks):
    t = S.LEAF
    for k in ks:
        t = _bst_insert(t, k)
    return t


def _order_keys(keys, order):
    ks = sorted(keys)
    if order == 'asc':
        return ks
    if order == 'desc':
        return ks[::-1]
    if order == 'balanced':
        out = []

        def rec(q):
            if not q:
                return
            m = len(q) // 2
            out.append(q[m])
            rec(q[:m])
            rec(q[m + 1:])
        rec(ks)
        return out
    raise AssertionError(order)


def build_B0(s_pins, fringe_keys, order='asc'):
    """Core skeleton from BState refs (gap children ignored), then insert fringe."""
    from S02_B_SIDE_PROPAGATOR import decode_btopo
    topo, root = decode_btopo(s_pins, 'SLs')

    def build(ref):
        if ref == 19:
            return S.LEAF
        kl, lr, kr, rr = topo[ref]
        if ref >= 9:
            return S.LEAF  # gap proxy: fringe inserted later by key order
        L = build(lr) if kl == 0 and lr < 9 else S.LEAF
        R = build(rr) if kr == 0 and rr < 9 else S.LEAF
        return S.node(CK[ref], L, R)

    t = build(root)
    for k in _order_keys(fringe_keys, order):
        t = _bst_insert(t, k)
    return t


def _key_range(path_keys):
    """(lo, hi) exclusive bounds from ancestor keys: list of (key, side)."""
    lo, hi = None, None
    for (k, side) in path_keys:
        if side == 0:
            hi = k if hi is None else min(hi, k)
        else:
            lo = k if lo is None else max(lo, k)
    return lo, hi


def count_alternatives(s_pins, fringe_by_gap):
    """Total non-S shadow key choice combos (bounded enumeration budget)."""
    sh = decode_shadow(s_pins, 'SLs')
    paths = {0: [], 1: [(0, 0)], 2: [(0, 1)], 3: [(1, 0)], 4: [(1, 1)],
             5: [(2, 0)], 6: [(2, 1)]}
    key_at = {}
    total = 1
    for i in [0, 1, 2, 3, 4, 5, 6]:
        kind, isS, sidx = sh[i]
        aks = [(key_at[p], s) for (p, s) in paths[i]]
        lo, hi = _key_range(aks)
        if kind == 0 and not isS:
            cands = [k for pool in fringe_by_gap.values() for k in pool
                     if (lo is None or lo < k) and (hi is None or k < hi)]
            total *= max(1, len(cands))
            key_at[i] = CK[sidx] if False else (cands[0] if cands else None)
            if key_at[i] is None:
                return 0
        elif kind == 0:
            key_at[i] = CK[sidx]
        else:
            key_at[i] = None
    return total


def build_A0(s_pins, Sset, fringe_by_gap, alt=0, order='asc'):
    """Canonical A_0: shadow skeleton keys + BST-inserted remainder (deterministic,
    exact-once by construction). alt selects among non-S shadow key choices.
    Returns (tree, n_alternatives) or (None, 0)."""
    sh = decode_shadow(s_pins, 'SLs')
    # tree paths from root: pos -> [(parent_pos, side)]
    paths = {0: [], 1: [(0, 0)], 2: [(0, 1)], 3: [(1, 0)], 4: [(1, 1)],
             5: [(2, 0)], 6: [(2, 1)]}
    key_at = {}
    pools = {g: sorted(v) for g, v in fringe_by_gap.items()}
    skel_keys = []
    for i in [0, 1, 2, 3, 4, 5, 6]:
        kind, isS, sidx = sh[i]
        aks = [(key_at[p], s) for (p, s) in paths[i]]
        lo, hi = _key_range(aks)
        if kind == 0:
            if isS:
                k = CK[sidx]
                if not ((lo is None or lo < k) and (hi is None or k < hi)):
                    return None, 0
                key_at[i] = k
                skel_keys.append(k)
            else:
                cands = sorted(k for pool in pools.values() for k in pool
                               if (lo is None or lo < k) and (hi is None or k < hi))
                if not cands:
                    return None, 0
                k = cands[alt % len(cands)]
                key_at[i] = k
                skel_keys.append(k)
                for pool in pools.values():
                    if k in pool:
                        pool.remove(k)
                if len(cands) > 1:
                    pass  # alternatives counted below
        else:
            key_at[i] = None
    # skeleton tree (None = empty port position, filled by insertion)
    kids = {0: (1, 2), 1: (3, 4), 2: (5, 6)}

    def node(i):
        v = key_at[i]
        if v is None:
            return S.LEAF
        if i in kids:
            l, r = kids[i]
            return S.node(v, node(l), node(r))
        return S.node(v, S.LEAF, S.LEAF)

    t = node(0)
    rest = [k for k in sorted(Sset) if k not in skel_keys]
    for pool in pools.values():
        rest.extend(pool)
    for k in _order_keys(rest, order):
        t = _bst_insert(t, k)
    # alternatives: max non-S choice count (bounded enumeration by caller)
    return t, 1

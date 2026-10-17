# S02_B_SIDE_PROPAGATOR.py — exact source-derived B-side inference (Gate C1/C2).
# Decodes abstract B-topologies from s/t pins (S-index refs, no concrete keys needed:
# splay cases are structural; BST order rides initial inorder labels). Forward BFS over
# abstract B-states (targets = S-indices 0..8; DELETE = identity) finds words whose
# B-trajectory ends at t.B. Derives q = floor(terminal_B_depth/2) and H = (w+q)/2 with
# admissibility checks. Every exclusion is source-justified (splay semantics).
# Nongenuine KEEP (target == current root) is an identity self-loop (Lemma 1, Gate B).
import sys
sys.path.insert(0, 'python/independent')
import splay as S


def decode_btopo(pins, prefix):
    """Abstract B-tree from BState pins: {ref: (lk, lr, rk, rr)}, root. Refs 0..8 core
    (S-index), 9..18 gaps, 19 NULL. Kind 2 = empty."""
    topo = {}
    for i in range(19):
        kl = pins['%s_b_bkl%d' % (prefix, i)]
        lr = pins['%s_b_brl%d' % (prefix, i)]
        kr = pins['%s_b_bkr%d' % (prefix, i)]
        rr = pins['%s_b_brr%d' % (prefix, i)]
        topo[i] = (kl, lr, kr, rr)
    return topo, pins[prefix + '_b_broot']


def children(topo, ref):
    kl, lr, kr, rr = topo[ref]
    out = []
    if kl != 2:
        out.append(('L', lr))
    if kr != 2:
        out.append(('R', rr))
    return out


def topo_key(topo, root):
    """Canonical nested tuple for equality (NULL-safe; cycle-guarded)."""
    seen = set()

    def go(r):
        if r == 19:
            return None
        if r in seen:
            raise AssertionError(('cyclic topology', r))
        seen.add(r)
        kl, lr, kr, rr = topo[r]
        L = go(lr) if kl != 2 else 'E'
        R = go(rr) if kr != 2 else 'E'
        seen.discard(r)
        return (r, L, R)

    return go(root)


def find_path(topo, root, target):
    """Search path (list of refs root->target) or None. Structural (no keys).
    Cycle-guarded (malformed topologies raise instead of hanging)."""
    if root == 19:
        return None
    seen = set()
    stack = [(root, [root])]
    while stack:
        n, p = stack.pop()
        if n in seen:
            continue
        seen.add(n)
        if n == target:
            return p
        kl, lr, kr, rr = topo[n]
        if kr != 2 and rr != 19:
            stack.append((rr, p + [rr]))
        if kl != 2 and lr != 19:
            stack.append((lr, p + [lr]))
    return None


def _side_of(t, par, ch):
    """'L'/'R'/None: which side of par points to ch (kind must be 0=ref)."""
    pkl, plr, pkr, prr = t[par]
    if pkl == 0 and plr == ch:
        return 'L'
    if pkr == 0 and prr == ch:
        return 'R'
    return None


def _set_child(t, par, side, ch):
    pkl, plr, pkr, prr = t[par]
    if side == 'L':
        t[par] = (0, ch, pkr, prr)
    else:
        t[par] = (pkl, plr, 0, ch)


def _rot_up(t, r, x, p, gp):
    """Rotate x above p; relink grandparent gp (None => x becomes root)."""
    sx = _side_of(t, p, x)
    assert sx is not None, ('not a child', x, p)
    xkl, xlr, xkr, xrr = t[x]
    if sx == 'L':
        midk, midr = xkr, xrr
    else:
        midk, midr = xkl, xlr
    pkl, plr, pkr, prr = t[p]
    # p takes middle subtree on x's side
    if sx == 'L':
        t[p] = (midk, midr, pkr, prr)
        t[x] = (xkl, xlr, 0, p)
    else:
        t[p] = (pkl, plr, midk, midr)
        t[x] = (0, p, xkr, xrr)
    # relink grandparent
    if gp is None:
        r = x
    else:
        sp = _side_of(t, gp, p)
        assert sp is not None, ('p not child of gp', p, gp)
        _set_child(t, gp, sp, x)
    return t, r


def splay_ref(topo, root, target):
    """Structural splay of target to root. Returns (new_topo, new_root, depth0)."""
    t = dict(topo)
    r = root
    p0 = find_path(t, r, target)
    if p0 is None:
        raise AssertionError(('target absent', target))
    d0 = len(p0) - 1
    for _step in range(1000):
        path = find_path(t, r, target)
        if path is None:
            raise AssertionError(('lost target', target))
        if len(path) == 1:
            break
        x = path[-1]
        p = path[-2]
        sx = _side_of(t, p, x)
        assert sx is not None
        if len(path) == 2:
            t, r = _rot_up(t, r, x, p, None)
        else:
            g = path[-3]
            sp = _side_of(t, g, p)
            assert sp is not None
            if (sx == 'L') == (sp == 'L'):
                ggp = path[-4] if len(path) > 3 else None
                t, r = _rot_up(t, r, p, g, ggp)
                # p now occupies g's old position; x still p's child on the same side
                t, r = _rot_up(t, r, x, p, ggp)
            else:
                t, r = _rot_up(t, r, x, p, g)
                t, r = _rot_up(t, r, x, g, path[-4] if len(path) > 3 else None)
    else:
        raise AssertionError(('splay non-convergence (malformed topology?)', target))
    return t, r, d0


def b_bfs(s_topo, s_root, t_key, marked, w, max_events=5):
    """BFS words (modes+targets) from s-topology ending at t-topology.
    Returns list of dicts {word, depths, q, H, end_root}. q/H derived, never assumed.
    word ops: ('K', sidx) / ('D', sidx). Terminal op is a genuine KEEP (marked target
    that changes B); DELETE = identity; nongenuine KEEP (target==root) = identity loop.
    H = (w+q)/2 must be integral with 0<=H<=2 (production w=2H-q)."""
    results = []
    # state: (topo_dict, root, word, depths); DELETE is a single B-identity self-loop
    # (delete-key expanded at A-stage); KEEP of current root is a nongenuine identity loop.
    ops = [('D', None)] + [('K', tgt) for tgt in range(9)]
    visited = set()
    frontier = [(s_topo, s_root, [], [])]
    while frontier:
        topo, root, word, depths = frontier.pop()
        if len(word) >= max_events:
            continue
        for (mode, tgt) in ops:
            if mode == 'D' or tgt == root:
                ntopo, nroot, chg = topo, root, False
                d = 0
            else:
                try:
                    ntopo, nroot, d = splay_ref(topo, root, tgt)
                except AssertionError:
                    continue
                chg = True
            nword = word + [(mode, tgt)]
            ndepths = depths + [d]
            if topo_key(ntopo, nroot) == t_key:
                # terminal must be genuine KEEP: marked target that changes B
                if mode == 'K' and tgt in marked and chg:
                    q = d // 2
                    if (w + q) % 2 == 0:
                        H = (w + q) // 2
                        if 0 <= H <= 2 and 2 * q <= d < 2 * q + 2:
                            results.append({'word': nword, 'depths': ndepths,
                                            'q': q, 'H': H, 'end_root': nroot})
                continue
            if len(nword) < max_events:
                sig = (topo_key(ntopo, nroot), tuple(nword))
                if sig not in visited:
                    visited.add(sig)
                    frontier.append((ntopo, nroot, nword, ndepths))
    # Exhaustive over words <= max_events (visited prunes only exact redundant
    # revisits: deterministic transitions make same-word revisits identical).
    return results, len(results)

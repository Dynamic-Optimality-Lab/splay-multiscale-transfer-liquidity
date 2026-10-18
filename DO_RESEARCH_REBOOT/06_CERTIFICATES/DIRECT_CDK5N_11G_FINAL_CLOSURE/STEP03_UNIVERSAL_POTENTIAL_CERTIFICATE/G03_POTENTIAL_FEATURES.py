# G03_POTENTIAL_FEATURES.py — frozen-state feature library (Gate H, Phase 4).
# Every feature is a deterministic function of the ABSTRACT state pins only:
# mu (9-bit mask), b (BState refs+root), alpha (7 shadow positions), sigma (10).
# No witness variables, no new observables. All integer-valued (exact Int).
import sys
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')


def _bint(env, key, default=0):
    v = env.get(key, default)
    try:
        return int(v)
    except (TypeError, ValueError):
        return default


def core_of_env(env, base):
    """Ancestor-closure of marked positions from BState pins (S-indexed).
    base = state tag WITHOUT _b suffix (e.g. 'SLs'); B vars live under base+'_b'."""
    B = base + '_b'
    topo = {}
    for i in range(19):
        kl = _bint(env, B + '_bkl%d' % i, 2)
        lr = _bint(env, B + '_brl%d' % i, 19)
        kr = _bint(env, B + '_bkr%d' % i, 2)
        rr = _bint(env, B + '_brr%d' % i, 19)
        topo[i] = (kl, lr, kr, rr)
    root = _bint(env, B + '_broot', 19)
    if root >= 19:
        return set()
    # BFS parents
    par = {root: None}
    stack = [root]
    while stack:
        n = stack.pop()
        kl, lr, kr, rr = topo[n]
        for nm, ch in (('L', lr if kl != 2 else 19), ('R', rr if kr != 2 else 19)):
            if ch != 19 and ch not in par:
                par[ch] = n
                stack.append(ch)
    mu = _bint(env, base + '_mu', 0)
    marked = [i for i in range(9) if (mu >> i) & 1]
    core = set()
    for m in marked:
        c = m
        while c is not None and c in topo:
            core.add(c)
            c = par.get(c)
    return core


def _bdepth(env, prefix, target):
    """B-depth of S-index target via parent links (None if unreachable)."""
    topo = {}
    for i in range(19):
        kl = _bint(env, prefix + '_bkl%d' % i, 2)
        lr = _bint(env, prefix + '_brl%d' % i, 19)
        kr = _bint(env, prefix + '_bkr%d' % i, 2)
        rr = _bint(env, prefix + '_brr%d' % i, 19)
        topo[i] = (kl, lr, kr, rr)
    root = _bint(env, prefix + '_broot', 19)
    if root == 19:
        return None
    par = {root: None}
    stack = [root]
    while stack:
        n = stack.pop()
        kl, lr, kr, rr = topo[n]
        for ch in (lr if kl != 2 else 19, rr if kr != 2 else 19):
            if ch != 19 and ch not in par:
                par[ch] = n
                stack.append(ch)
    if target not in par:
        return None
    d, c = 0, target
    while par[c] is not None:
        d += 1
        c = par[c]
    return d


FEATURES = {}


def _feat(name):
    def deco(f):
        FEATURES[name] = f
        return f
    return deco


@_feat('b_root')
def f_b_root(env, P):
    return _bint(env, P + '_b_broot', 0)


@_feat('b_depth_sum')
def f_b_depth_sum(env, P):
    tot = 0
    for i in range(9):
        d = _bdepth(env, P + '_b', i)
        if d is None:
            return None
        tot += d
    return tot


@_feat('b_depth_max')
def f_b_depth_max(env, P):
    ds = []
    for i in range(9):
        d = _bdepth(env, P + '_b', i)
        if d is None:
            return None
        ds.append(d)
    return max(ds) if ds else None


@_feat('b_marked_depth_sum')
def f_b_marked_depth_sum(env, P):
    mu = _bint(env, P + '_mu', 0)
    tot = 0
    for i in range(9):
        if (mu >> i) & 1:
            d = _bdepth(env, P + '_b', i)
            if d is None:
                return None
            tot += d
    return tot


@_feat('a_root_sidx')
def f_a_root_sidx(env, P):
    return _bint(env, P + '_aI0', 0)


@_feat('a_nslots')
def f_a_nslots(env, P):
    # number of slot-kind shadow positions (kind==0)
    return sum(1 for i in range(7) if _bint(env, P + '_ak%d' % i, -1) == 0)


@_feat('a_marked_count')
def f_a_marked_count(env, P):
    return sum(1 for i in range(7) if _bint(env, P + '_aS%d' % i, False) not in (0, False))


@_feat('sig_sum')
def f_sig_sum(env, P):
    return sum(_bint(env, P + '_sg%d' % i, 0) for i in range(10))


@_feat('sig_nonempty')
def f_sig_nonempty(env, P):
    return sum(1 for i in range(10) if _bint(env, P + '_sg%d' % i, 0) > 0)


@_feat('core_size')
def f_core_size(env, P):
    return len(core_of_env(env, P))


@_feat('mu_bits')
def f_mu_bits(env, P):
    return bin(_bint(env, P + '_mu', 0)).count('1')


def _blog2(sz):
    if sz <= 1:
        return 0
    if sz <= 3:
        return 1
    if sz <= 7:
        return 2
    return 3


def _bsubtree_sizes(env, prefix):
    """Subtree sizes (node count incl. self) for all 19 B-refs via children links."""
    kids = {}
    for i in range(19):
        kl = _bint(env, prefix + '_bkl%d' % i, 2)
        lr = _bint(env, prefix + '_brl%d' % i, 19)
        kr = _bint(env, prefix + '_bkr%d' % i, 2)
        rr = _bint(env, prefix + '_brr%d' % i, 19)
        kids[i] = ((lr if kl != 2 else None), (rr if kr != 2 else None))
    root = _bint(env, prefix + '_broot', 19)
    sizes = {}

    def sz(n):
        if n is None or n == 19 or n in sizes:
            return sizes.get(n, 0)
        l, r = kids[n]
        sizes[n] = 1 + sz(l) + sz(r)
        return sizes[n]

    if root != 19:
        sz(root)
    return sizes


@_feat('b_rank_sum')
def f_b_rank_sum(env, P):
    sizes = _bsubtree_sizes(env, P + '_b')
    tot = 0
    for i in range(9):
        if i not in sizes:
            return None
        tot += _blog2(sizes[i])
    return tot


@_feat('b_rank_marked')
def f_b_rank_marked(env, P):
    sizes = _bsubtree_sizes(env, P + '_b')
    mu = _bint(env, P + '_mu', 0)
    tot = 0
    for i in range(9):
        if (mu >> i) & 1:
            if i not in sizes:
                return None
            tot += _blog2(sizes[i])
    return tot


@_feat('b_rank_root')
def f_b_rank_root(env, P):
    sizes = _bsubtree_sizes(env, P + '_b')
    root = _bint(env, P + '_b_broot', 19)
    if root not in sizes:
        return None
    return _blog2(sizes[root])


# fixed shadow topology: 0=root, 1=L, 2=R, 3=LL, 4=LR, 5=RL, 6=RR
_SHADOW_KIDS = {0: (1, 2), 1: (3, 4), 2: (5, 6), 3: (None, None), 4: (None, None),
                5: (None, None), 6: (None, None)}


def _ashadow_subsz(env, P):
    occ = [1 if _bint(env, P + '_ak%d' % i, -1) != 0 else 0 for i in range(7)]
    sub = {}

    def sz(n):
        if n is None:
            return 0
        if n in sub:
            return sub[n]
        l, r = _SHADOW_KIDS[n]
        sub[n] = occ[n] + sz(l) + sz(r)
        return sub[n]

    sz(0)
    return sub


@_feat('a_rank_sum')
def f_a_rank_sum(env, P):
    sub = _ashadow_subsz(env, P)
    return sum(_blog2(max(1, sub[i])) for i in range(7))


@_feat('a_rank_root')
def f_a_rank_root(env, P):
    sub = _ashadow_subsz(env, P)
    return _blog2(max(1, sub[0]))


def eval_all(env, prefix):
    out = {}
    for name, f in FEATURES.items():
        try:
            out[name] = f(env, prefix)
        except Exception:
            out[name] = None
    return out

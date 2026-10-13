# UFRL extraction E1-E8 + L1-L8 preservation checker (falsifiable core).
import sys, json
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
import splay as S

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_UFRL_TERMINAL_CLOSURE/'
T_CAP = 266

def depth(t, x):
    d = 0
    cur = t
    while cur[0] != "leaf":
        _, k, l, r = cur
        if x == k:
            return d
        cur = l if x < k else r
        d += 1
    return None

def keys_of(t):
    if t[0] == "leaf":
        return set()
    _, k, l, r = t
    return {k} | keys_of(l) | keys_of(r)

def balanced(ks):
    ks = sorted(ks)
    if not ks:
        return S.LEAF
    m = len(ks) // 2
    return S.node(ks[m], balanced(ks[:m]), balanced(ks[m + 1:]))

def gaps_of(Sset, universe):
    Ss = sorted(Sset)
    gaps = [[] for _ in range(10)]
    for k in sorted(universe):
        if k in Sset:
            continue
        g = sum(1 for s in Ss if s < k)
        gaps[g].append(k)
    return gaps

def extract(A, Sset, universe, words_targets=None):
    # E1: depth-6 prefix (exact nodes) + frontier holes (nonempty subtrees below)
    Ss = set(Sset)
    holes = []  # (path, subtree)
    prefix_nodes = set()
    def walk(t, lv, path):
        if t[0] == "leaf":
            return
        _, k, l, r = t
        if lv <= 6:
            prefix_nodes.add(k)
            walk(l, lv + 1, path + (0,))
            walk(r, lv + 1, path + (1,))
        else:
            holes.append((path, t))
    walk(A, 0, ())
    # frontier = holes that are nonempty (all recorded holes are nonempty by construction)
    K = set(prefix_nodes)
    # E3: S keys per hole + E4 witnesses (min key) for S-less holes
    hole_S = []
    witnesses = {}
    for i, (path, st) in enumerate(holes):
        ks = keys_of(st)
        sh = sorted(ks & Ss)
        hole_S.append(sh)
        if not sh:
            witnesses[i] = min(ks)
    E = set(K) | set(Ss) | set(witnesses.values())
    # E6: per-gap selection
    gaps = gaps_of(Sset, universe)
    V = []
    for g in gaps:
        Eg = [k for k in g if k in E]
        if len(g) <= T_CAP:
            V.append(list(g))
        else:
            extra = [k for k in sorted(g) if k not in Eg][:T_CAP - len(Eg)]
            V.append(sorted(Eg + extra))
    # E7: rebuild: prefix exact; each hole rebuilt over retained keys located in it
    vreps = {}
    for i, (path, st) in enumerate(holes):
        ks = keys_of(st)
        keep = sorted([k for k in ks if k in Ss or k in witnesses.values() or any(k in Vv for Vv in V)])
        # V_i intersect hole: keys of V (any gap) located in this hole = keep-filtered
        vreps[i] = keep
    # rebuild tree: copy prefix, attach balanced retained subtrees at holes
    def rebuild(t, lv, path):
        if t[0] == "leaf":
            return S.LEAF
        _, k, l, r = t
        if lv <= 6:
            return S.node(k, rebuild(l, lv + 1, path + (0,)), rebuild(r, lv + 1, path + (1,)))
        # hole root: find index
        for i, (p, st) in enumerate(holes):
            if p == path:
                return balanced(vreps[i])
        return S.LEAF
    Astar = rebuild(A, 0, ())
    Ustar = set(Ss)
    for Vv in V:
        Ustar |= set(Vv)
    return {"Astar": Astar, "Ustar": Ustar, "V": V, "E": E, "K": K,
            "holes": holes, "witnesses": witnesses, "gaps": gaps}

def shadow(A, Sset):
    # canonical shadow per §6 (rank-canonical S, ordered anonymous, holes w/ S-subsets, root)
    Ss = sorted(Sset)
    rk = {k: i + 1 for i, k in enumerate(Ss)}
    slots = {}
    def walk(t, lv, pos):
        if t[0] == "leaf" or lv > 2:
            return
        _, k, l, r = t
        slots[(lv, pos)] = k
        walk(l, lv + 1, pos * 2)
        walk(r, lv + 1, pos * 2 + 1)
    walk(A, 0, 0)
    # anonymous canonical by inorder
    order = []
    def ino(t, lv):
        if t[0] == "leaf":
            return
        _, k, l, r = t
        ino(l, lv + 1)
        if lv <= 2 and k not in Ss:
            order.append(k)
        ino(r, lv + 1)
    ino(A, 0)
    beta = {k: 'b%d' % (i + 1) for i, k in enumerate(order)}
    vis = tuple(sorted(((p, ('S', rk[k]) if k in Ss else ('F', beta[k]))) for p, k in slots.items()))
    # holes with S-subsets
    holes = []
    def hw(t, lv, lo, hi):
        if t[0] == "leaf":
            if lv == 3:
                holes.append((frozenset(), lo, hi, True))
            return
        _, k, l, r = t
        if lv == 2:
            for ch, (nlo, nhi) in ((l, (lo, k)), (r, (k, hi))):
                sub = set()
                sk = [ch]
                while sk:
                    u = sk.pop()
                    if u[0] == "leaf":
                        continue
                    _, kk, ll, rr = u
                    if kk in Ss:
                        sub.add(rk[kk])
                    sk.append(ll)
                    sk.append(rr)
                holes.append((frozenset(sub), lo if isinstance(lo, int) else lo, hi if isinstance(hi, int) else hi, ch[0] == "leaf"))
            return
        hw(l, lv + 1, lo, k)
        hw(r, lv + 1, k, hi)
    hw(A, 0, 0, 10)
    return {"vis": str(vis), "holes": str(sorted(holes, key=str))}

if __name__ == "__main__":
    # smoke: extract on T0-like tree, check bounds + validity
    def conv(t):
        if t is None:
            return S.LEAF
        k, l, r = t
        return S.node(k, conv(l), conv(r))
    T0 = conv([9, [6, [1, None, [2, None, [5, [4, [3, None, None], None], None]]], [8, [7, None, None], None]], None])
    Sset = set(range(1, 10))
    U = set(range(1, 10))
    R = extract(T0, Sset, U)
    print("Ustar=%d (<=2669), E=%d, holes=%d" % (len(R["Ustar"]), len(R["E"]), len(R["holes"])), flush=True)
    # validity: Astar is BST over Ustar subset, prefix identical
    print("Astar keys <= Ustar:", keys_of(R["Astar"]) <= R["Ustar"], flush=True)
    print("shadow equal:", shadow(T0, Sset) == shadow(R["Astar"], Sset), flush=True)

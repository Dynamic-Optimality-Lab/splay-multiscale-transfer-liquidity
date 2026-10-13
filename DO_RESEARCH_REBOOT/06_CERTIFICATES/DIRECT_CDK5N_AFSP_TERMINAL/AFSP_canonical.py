# AFSP canonical shadow (order-type endpoints; no raw key leakage).
import sys
sys.path.insert(0, 'python/independent')
import splay as S

def canonical_shadow(A, Sset):
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
    beta = {k: i + 1 for i, k in enumerate(order)}
    def desc(k):
        if k in Ss:
            return ('S', rk[k])
        return ('F', beta[k])
    vis = tuple(sorted(((p, desc(k)) for p, k in slots.items()), key=str))
    holes = []
    def hw(t, lv, lo, hi):
        # lo/hi are canonical descriptors (or ('MIN',)/('MAX',) sentinels)
        if t[0] == "leaf":
            if lv == 3:
                holes.append((frozenset(), lo, hi, True))
            return
        _, k, l, r = t
        if lv == 2:
            for ch, (nlo, nhi) in ((l, (lo, desc(k))), (r, (desc(k), hi))):
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
                holes.append((frozenset(sub), nlo, nhi, ch[0] == "leaf"))
            return
        hw(l, lv + 1, lo, desc(k))
        hw(r, lv + 1, desc(k), hi)
    hw(A, 0, ('MIN',), ('MAX',))
    return {"vis": str(vis), "holes": str(sorted(holes, key=str))}

def shadow_equal(A1, A2, Sset):
    return canonical_shadow(A1, Sset) == canonical_shadow(A2, Sset)

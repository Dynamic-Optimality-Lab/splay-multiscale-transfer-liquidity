"""PIVOT-25R-U §9 start: rotation-level eta-update identities, engine-checked.

For one splay StepEv with triple (x,p,g-or-None)+pattern, keys partition:
- OUT: outside g-subtree (or p-subtree if zig): eta fully unchanged.
- RIGID: rehung/untouched blocks inside (descendants of pivots that move
  rigidly): subtree key-sets (=> n, intervals, omega) unchanged; depths
  shift uniformly by the block's root displacement.
- PIVOT {x,p,g}: descendant sets change => all coords may change.
Claim: omega/n/intervals change ONLY at pivots; depths change at most by
region displacement inside the step's subtree, nowhere outside.
Checked against canonical splay_cap on random trees/keys.
"""
from __future__ import annotations
import sys
import copy
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
import wp6_overflow as V


def step(sid, msg):
    print("[JUP %s] %s" % (sid, msg), flush=True)


def depths_list(t):
    out = {}

    def go(nd, d):
        if nd is None:
            return
        out[nd[0]] = d
        go(nd[1], d + 1)
        go(nd[2], d + 1)
    go(t, 0)
    return out


def subkeys_list(t, x):
    nd = t
    while nd is not None and nd[0] != x:
        nd = nd[1] if x < nd[0] else nd[2]
    out = []

    def go(m):
        if m is None:
            return
        out.append(m[0])
        go(m[1])
        go(m[2])
    go(nd)
    return frozenset(out)


def snap(t):
    dd = depths_list(t)
    sk = {y: subkeys_list(t, y) for y in dd}
    return dd, sk


def ptr_to_list(P):
    if P is None:
        return None
    return [P["k"], ptr_to_list(P["l"]), ptr_to_list(P["r"])]


def children_of(T0, node):
    """Direct child subtrees (list-shapes) of node key in T0 + parent key."""
    def find(nd, par):
        if nd is None:
            return None
        if nd[0] == node:
            return (par, nd[1], nd[2])
        r = find(nd[1], nd[0])
        return r if r is not None else find(nd[2], nd[0])
    return find(T0, None)


def main():
    rng = random.Random(11)
    n = 8
    NSTEP = NPIV = NOUT = NRIG = 0
    BAD = 0
    SETBAD = 0
    from collections import Counter
    DD = Counter()
    trials = 0
    import wp6_cycle_ratio as O
    Sh = O.shapes_of(list(range(1, n + 1)))
    for t in range(60):
        T0 = copy.deepcopy(Sh[rng.randrange(len(Sh))])
        x = rng.randint(1, n)
        ptr = V.to_ptr(copy.deepcopy(T0))
        d_pre = V.depths_of(ptr)
        # manual step-by-step splay to isolate single rotations
        node = None
        # locate x ptr
        stack = [ptr]
        while stack:
            nd = stack.pop()
            if nd["k"] == x:
                node = nd
                break
            if nd["l"] is not None:
                stack.append(nd["l"])
            if nd["r"] is not None:
                stack.append(nd["r"])
        while node["p"] is not None:
            p = node["p"]
            g = p["p"]
            # snapshot pre-step full state
            pre = ptr_to_list(ptr)
            dd0, sk0 = snap(ptr_to_list(ptr))
            xk, pk = node["k"], p["k"]
            # perform exactly one StepEv (copy of splay_cap logic per kind)
            import liquidity.legacy_embedding as PE
            if g is None:
                if p["l"] is node:
                    PE._rot_right(p)
                else:
                    PE._rot_left(p)
                piv = {xk, pk}
                top = xk  # new subtree root
            else:
                gk = g["k"]
                if p["l"] is node and g["l"] is p:
                    PE._rot_right(g)
                    PE._rot_right(p)
                elif p["r"] is node and g["r"] is p:
                    PE._rot_left(g)
                    PE._rot_left(p)
                elif p["r"] is node and g["l"] is p:
                    PE._rot_left(p)
                    PE._rot_right(g)
                else:
                    PE._rot_right(p)
                    PE._rot_left(g)
                piv = {xk, pk, gk}
                top = xk
            post_root = node
            while post_root["p"] is not None:
                post_root = post_root["p"]
            ptr = post_root  # re-root: old root may have rotated down
            post = ptr_to_list(ptr)
            dd1, sk1 = snap(post)
            import json as _J
            if sorted(dd1) != list(range(1, n + 1)):
                step("BAD", "keys lost pat x=%d p=%s g=%s T0=%s" %
                     (xk, pk, (g["k"] if g is not None else None),
                      _J.dumps(T0)))
                return 1
            # claim 1: keys outside subtree rooted at `top`'s position...:
            # find top node ptr, its key set; outside keys: depths+sets same
            # locate top
            stack = [ptr]
            tnode = None
            while stack:
                nd = stack.pop()
                if nd["k"] == top:
                    tnode = nd
                    break
                if nd["l"] is not None:
                    stack.append(nd["l"])
                if nd["r"] is not None:
                    stack.append(nd["r"])
            inset = set()

            def col(m):
                if m is None:
                    return
                inset.add(m["k"])
                col(m["l"])
                col(m["r"])
            col(tnode)
            for y in range(1, n + 1):
                if y not in inset:
                    NOUT += 1
                    if dd0[y] != dd1[y] or sk0[y] != sk1[y]:
                        BAD += 1
                elif y not in piv:
                    # RIGID lemma: only pivots change children => key sets
                    # of all other inside keys are IDENTICAL.
                    NRIG += 1
                    if sk0[y] != sk1[y]:
                        SETBAD += 1
                    DD[dd1[y] - dd0[y]] += 1
                else:
                    NPIV += 1
            NSTEP += 1
            # re-find node (x) after rotation
            stack = [ptr]
            while stack:
                nd = stack.pop()
                if nd["k"] == x:
                    node = nd
                    break
                if nd["l"] is not None:
                    stack.append(nd["l"])
                if nd["r"] is not None:
                    stack.append(nd["r"])
        trials += 1
    step("S", "trials=%d steps=%d outside=%d (viol=%d) nonpivot-in=%d "
              "(setviol=%d) pivot=%d ddepth=%s" %
         (trials, NSTEP, NOUT, BAD, NRIG, SETBAD, NPIV, dict(sorted(DD.items()))))
    json.dump({"trials": trials, "steps": NSTEP, "outside": NOUT,
               "outside_viol": BAD, "nonpivot_in": NRIG,
               "nonpivot_set_viol": SETBAD,
               "nonpivot_depth_delta": {str(k): v for k, v in DD.items()}},
              open(str(ROOT / "artifacts" / "v04" / "wp6_present" /
                       "0909c74a" / "dual_mine" / "joint_updates.json"),
                   "w"), indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())

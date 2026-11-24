"""Finite tree identities with opaque, untouched full subtrees as parameters.

This is not a projected source execution. An atom denotes the entire original
subtree, and no pivot/target enters it. Each row is a literal rotation identity
valid for every substitution respecting the displayed key order/extremes.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


class Atom:
    def __init__(self, name, extreme_flags=()):
        self.name = name
        self.flags = frozenset(extreme_flags)


class Node:
    def __init__(self, key, left=None, right=None):
        self.key, self.left, self.right, self.parent = key, left, right, None
        for c in [left, right]:
            if isinstance(c, Node):
                c.parent = self


def expr(t):
    if t is None:
        return None
    if isinstance(t, Atom):
        return ["FULL_SUBTREE", t.name]
    return [t.key, expr(t.left), expr(t.right)]


def perfect(lo, hi):
    if lo > hi:
        return None
    mid = (lo + hi) // 2
    return Node(mid, perfect(lo, mid-1), perfect(mid+1, hi))


def flags(t, maximum=None):
    if t is None:
        return frozenset()
    if isinstance(t, Atom):
        return t.flags
    own = {"MAX"} if maximum is not None and t.key == maximum else set()
    return flags(t.left, maximum) | flags(t.right, maximum) | own


def run(root, targets, maximum=None):
    lookup = {}
    stack = [root]
    while stack:
        t = stack.pop()
        if isinstance(t, Node):
            lookup[t.key] = t
            stack.extend([t.left, t.right])
    rows = []

    def rotate(x):
        nonlocal root
        p = x.parent
        g = p.parent
        if p.left is x:
            middle = x.right
            p.left = middle
            x.right = p
        else:
            assert p.right is x
            middle = x.left
            p.right = middle
            x.left = p
        if isinstance(middle, Node):
            middle.parent = p
        x.parent = g
        p.parent = x
        if g is None:
            root = x
        elif g.left is p:
            g.left = x
        else:
            assert g.right is p
            g.right = x
        new_flags = flags(p, maximum)
        assert len(new_flags) <= 1
        return int(bool(new_flags))

    for target in targets:
        x = lookup[target]
        types, ds, us = [], 0, 0
        while x.parent:
            p = x.parent
            g = p.parent
            if g is None:
                types.append("ZIG")
                ds += rotate(x)
                continue
            old_flags = flags(g, maximum)
            a = "L" if g.left is p else "R"
            b = "L" if p.left is x else "R"
            typ = a+b
            if a == b:
                d0, d1 = rotate(p), rotate(x)
            else:
                d0, d1 = rotate(x), rotate(x)
            us += int(not old_flags and not d0 and not d1)
            ds += d0+d1
            types.append(typ)
        rows.append({"target": target, "types": types, "Q": sum(t != "ZIG" for t in types),
                     "Z": types.count("ZIG"), "U": us, "D": ds})
    return root, rows


def total(rows):
    return {k: sum(r[k] for r in rows) for k in ["Q", "Z", "U", "D"]}


def main():
    if (HERE/'FINAL_MANIFEST.json').exists():
        raise RuntimeError('Sealed run: output generation requires a new versioned directory.')
    P, C, H = Atom("P", {"MIN"}), Atom("C"), Atom("H", {"MAX"})
    initial = Node(2, P, Node("m", Node(18, perfect(3,17), C), H))
    before = expr(initial)
    after, rows = run(initial, range(3,19))
    left = P
    for key in range(2,18):
        left = Node(key, left, None)
    expected = Node(18, left, Node("m", C, H))
    assert expr(after) == expr(expected)
    assert total(rows) == {"Q":13,"Z":12,"U":3,"D":32}
    generic = {"input":before,"output":expr(after),"targets":"a..a+15; explicit keys2..18 are translated by a-3",
               "substitution_contract":"P contains the global minimum; C contains neither extreme; H contains the global maximum. Full subtrees are rigid and never targeted or rotated. 2 < 3..17 <18 <m.",
               "rows":rows,"totals":total(rows),"identity_checked":True}
    P = Atom("P", {"MIN"})
    initial = Node(2, P, Node(10, perfect(3,9), perfect(11,17)))
    before = expr(initial)
    after, rows = run(initial, range(3,18), maximum=17)
    left = P
    for key in range(2,17):
        left = Node(key,left,None)
    assert expr(after) == expr(Node(17,left,None))
    assert total(rows) == {"Q":9,"Z":10,"U":1,"D":26}
    tail={"input":before,"output":expr(after),"substitution_contract":"P is the entire already-processed prefix and contains the global minimum; explicit17 is the global maximum. Translate all explicit keys by16q.",
          "rows":rows,"totals":total(rows),"identity_checked":True}
    out={"meaning":"Algebraic full-subtree rotation identities for the H3q scan, not enumeration of arbitrary BSTs.",
         "A_geometry_required_for_U_D_counts":"At every original post-A snapshot A is the target-rooted two-vine; throughout the entire period every A snapshot is two-vine. In this H source, a new proper B interval is A-common exactly when it contains a global extreme, and every proper interior frame has complete cyclic Pi absence.",
         "generic_block":generic,"terminal_block":tail,
         "initial_KEEP1_KEEP2":{"Q":1,"Z":1,"U":0,"D":3},
         "forward_totals":{"Q":"13q+10","Z":"12q+11","U":"3q+1","D":"32q+29"},
         "full_source_totals":{"A":"64(q+1)","Q_B":"28q+25","Z_B":"28q+27","U_int":"10q+5","D_B":"48q+53","K_B":"32q+37"}}
    (HERE/'SYMBOLIC_BLOCK_CERTIFICATE.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps({'generic':generic['totals'],'tail':tail['totals'],'both_identities':True}))


if __name__=='__main__':
    main()

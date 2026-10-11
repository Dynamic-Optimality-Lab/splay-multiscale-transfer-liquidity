# PROOF independent recursive checker (Gate E): iterative worklist + exhaustive
# path enumeration with minimax-depth canonical choice. Structurally distinct
# from RC Dijkstra and DLSS heap engines. Shared audited primitives only.
# battery-None (badblocks) => INDETERMINATE (never silent uncovered).
import sys
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_DLSS_G0_POST_MSINK')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_MSINK_G0_CYCLIC_RC')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
from RC_recursive_closure_engine import replay_from, canon
from CRA_segment_memberships import full_banked
from DLSS_membership import strict_msink_bank

MEMOP = {}
CALLSP = {"n": 0, "hit": False}
CAPP = 60000
PATHCAP = 20000

def bank21p(legs, pairs, snaps):
    from DLSS_membership import strict_msink_bank
    fb = full_banked(legs, pairs, snaps)
    if fb is None:
        return None
    fb["MSINK"] = strict_msink_bank(legs, pairs)
    return fb

def base21p(legs, pairs, snaps):
    A = sum(l["a"] for l in legs); Q = sum(l["q"] for l in legs)
    if A == 0:
        keys = sorted({l["x"] for l in legs})
        if Q == 0 and len(keys) == 1:
            return True, {"basis": "Z"}
        return False, {"basis": "Z-fail", "indeterminate": True,
                       "note": "A0 anomaly needs review"}
    fb = bank21p(legs, pairs, snaps)
    if fb is None:
        return False, {"basis": "battery-none", "indeterminate": True,
                       "note": "block build failed; must not default uncovered"}
    flags = sorted(k for k, v in fb.items() if v)
    if flags:
        return True, {"basis": "RotB21", "mechanisms": flags}
    return False, {"basis": "no-mechanism"}

def all_simple_paths(edges, n):
    out = []
    stack = [(0, [0])]
    while stack:
        v, path = stack.pop()
        if v == n:
            if len(path) - 1 >= 2:
                out.append(list(zip(path[:-1], path[1:])))
            continue
        if len(out) >= PATHCAP:
            return None
        for j in sorted(edges.get(v, []), reverse=True):
            if j not in path:
                stack.append((j, path + [j]))
    return out

def coverP(start, word):
    key = (start, canon(word))
    if key in MEMOP:
        return MEMOP[key]
    CALLSP["n"] += 1
    if CALLSP["n"] > CAPP:
        CALLSP["hit"] = True
        r = {"covered": False, "indeterminate": "cap"}
        MEMOP[key] = r
        return r
    n = len(word)
    try:
        Fr = replay_from(start, word)
    except Exception as e:
        r = {"covered": False, "indeterminate": "replay-%s" % e}
        MEMOP[key] = r
        return r
    if Fr["pairs"][-1] != start:
        r = {"covered": False, "why": "not-closed"}
        MEMOP[key] = r
        return r
    legs = Fr["legs"]
    ok, cert = base21p(legs, Fr["pairs"], Fr["snaps"])
    if cert.get("indeterminate"):
        CALLSP["hit"] = True
        r = {"covered": False, "indeterminate": cert.get("note", "base"),
             "base": cert}
        MEMOP[key] = r
        return r
    if ok:
        r = {"covered": True, "depth": 0, "cert": cert, "n": n,
             "A": sum(l["a"] for l in legs), "Q": sum(l["q"] for l in legs)}
        MEMOP[key] = r
        return r
    if n <= 1:
        r = {"covered": False, "why": "atomic", "n": n}
        MEMOP[key] = r
        return r
    pairs = Fr["pairs"]
    best = None
    neg = {"rots": []}
    for rr in range(n):
        edges = {}
        einfo = {}
        for i in range(n + 1):
            for j in range(i + 1, n + 1):
                if j - i == n:
                    continue
                a = (rr + i) % n; b = (rr + j) % n
                if pairs[a] != pairs[b]:
                    continue
                sw = [word[(rr + t) % n] for t in range(i, j)]
                ch = coverP(pairs[a], sw)
                einfo[(i, j)] = {"a": a, "b": b,
                                 "covered": ch.get("covered", False),
                                 "depth": ch.get("depth"),
                                 "ind": ch.get("indeterminate")}
                if ch.get("indeterminate"):
                    CALLSP["hit"] = True
                if ch.get("covered"):
                    edges.setdefault(i, []).append(j)
        paths = all_simple_paths(edges, n)
        if paths is None:
            CALLSP["hit"] = True
            fr = {"r": rr, "pathcap": True}
            neg["rots"].append(fr)
            continue
        fr = {"r": rr, "npaths": len(paths),
              "segs": {str(k): {"c": v["covered"], "d": v["depth"]}
                       for k, v in einfo.items()}}
        neg["rots"].append(fr)
        for path in paths:
            kids = []
            for (ii, jj) in path:
                a = (rr + ii) % n; b = (rr + jj) % n
                kids.append(coverP(pairs[a], [word[(rr + t) % n] for t in range(ii, jj)]))
            dd = max(k["depth"] for k in kids) + 1
            cand = (dd, rr, len(path), path, kids)
            if best is None or (cand[0], cand[1], cand[2]) < \
                    (best[0], best[1], best[2]):
                best = cand
    if CALLSP["hit"]:
        r = {"covered": False, "indeterminate": "cap-hit", "neg": neg}
        MEMOP[key] = r
        return r
    if best is not None:
        dd, rr, _, path, kids = best
        totA = sum(l["a"] for l in legs); totQ = sum(l["q"] for l in legs)
        r = {"covered": True, "depth": dd,
             "cert": {"r": rr, "path": path,
                      "bounds": [((rr + a) % n, (rr + b) % n) for (a, b) in path]},
             "A": totA, "Q": totQ,
             "additive": sum(k["A"] for k in kids) == totA
             and sum(k["Q"] for k in kids) == totQ}
        MEMOP[key] = r
        return r
    # canonical choice among equal (depth,r,len): lex-smallest path enforced by
    # sorted-edge DFS order in all_simple_paths (reverse-sorted push + pop).
    r = {"covered": False, "neg": neg,
         "A": sum(l["a"] for l in legs), "Q": sum(l["q"] for l in legs)}
    MEMOP[key] = r
    return r

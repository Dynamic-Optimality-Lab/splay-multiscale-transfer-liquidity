# PROOF independent recursive checker (Gate E): iterative worklist DP with
# exhaustive simple-path enumeration and minimax-depth canonical choice.
# Structurally distinct from the Gate-0 heap-Dijkstra engine. Shared audited
# primitives only (lockstep replay, exact predicates incl. exists-MSINK/DLSS/
# UESINK). battery-None => INDETERMINATE (never silent uncovered).
import sys
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_ZULR_G0_POST_UESINK')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_ZULR_PROOF_POST_UESINK')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_MSINK_G0_CYCLIC_RC')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_DLSS_G0_POST_MSINK')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_UESINK_G0_POST_DLSS')
from RC_recursive_closure_engine import replay_from, canon
from CRA_segment_memberships import full_banked
from DLSS_membership import strict_msink_bank
from UESINK_membership import strict_dlss_bank
from ZULR_membership import strict_uesink_bank

MEMOI = {}
CALLSI = {"n": 0, "hit": False}
CAPI = 60000
PATHCAPI = 20000

def bank23i(legs, pairs, snaps):
    fb = full_banked(legs, pairs, snaps)
    if fb is None:
        return None
    fb["MSINK"] = strict_msink_bank(legs, pairs)
    fb["DLSS"] = strict_dlss_bank(legs, pairs)
    fb["UESINK"] = strict_uesink_bank(legs, pairs)
    return fb

def base23i(legs, pairs, snaps):
    A = sum(l["a"] for l in legs); Q = sum(l["q"] for l in legs)
    if A == 0:
        keys = sorted({l["x"] for l in legs})
        if Q == 0 and len(keys) == 1:
            return True, {"basis": "Z", "A": 0, "Q": 0}
        return False, {"basis": "Z-fail", "indeterminate": True}
    fb = bank23i(legs, pairs, snaps)
    if fb is None:
        return False, {"basis": "battery-none", "indeterminate": True}
    flags = sorted(k for k, v in fb.items() if v)
    if flags:
        return True, {"basis": "RotB23", "mechanisms": flags, "A": A, "Q": Q}
    return False, {"basis": "no-mechanism", "A": A, "Q": Q}

def all_paths(edges, n):
    out = []
    stack = [(0, [0])]
    while stack:
        v, path = stack.pop()
        if v == n:
            if len(path) - 1 >= 2:
                out.append(list(zip(path[:-1], path[1:])))
            continue
        if len(out) >= PATHCAPI:
            return None
        for j in sorted(edges.get(v, []), reverse=True):
            if j not in path:
                stack.append((j, path + [j]))
    return out

def coverI(start, word):
    key = (start, canon(word))
    if key in MEMOI:
        return MEMOI[key]
    CALLSI["n"] += 1
    if CALLSI["n"] > CAPI:
        CALLSI["hit"] = True
        r = {"covered": False, "indeterminate": "cap"}
        MEMOI[key] = r
        return r
    n = len(word)
    try:
        Fr = replay_from(start, word)
    except Exception as e:
        r = {"covered": False, "indeterminate": "replay-%s" % e}
        MEMOI[key] = r
        return r
    if Fr["pairs"][-1] != start:
        r = {"covered": False, "why": "not-closed"}
        MEMOI[key] = r
        return r
    legs = Fr["legs"]
    ok, cert = base23i(legs, Fr["pairs"], Fr["snaps"])
    if cert.get("indeterminate"):
        CALLSI["hit"] = True
        r = {"covered": False, "indeterminate": cert.get("note", "base"),
             "base": cert}
        MEMOI[key] = r
        return r
    if ok:
        r = {"covered": True, "depth": 0, "cert": cert, "n": n,
             "A": sum(l["a"] for l in legs), "Q": sum(l["q"] for l in legs)}
        MEMOI[key] = r
        return r
    if n <= 1:
        r = {"covered": False, "why": "atomic", "n": n}
        MEMOI[key] = r
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
                ch = coverI(pairs[a], sw)
                einfo[(i, j)] = {"a": a, "b": b,
                                 "covered": ch.get("covered", False),
                                 "depth": ch.get("depth"),
                                 "ind": ch.get("indeterminate")}
                if ch.get("indeterminate"):
                    CALLSI["hit"] = True
                if ch.get("covered"):
                    edges.setdefault(i, []).append(j)
        paths = all_paths(edges, n)
        fr = {"r": rr, "npaths": None if paths is None else len(paths),
              "segs": {str(k): {"c": v["covered"], "d": v["depth"]}
                       for k, v in einfo.items()}}
        neg["rots"].append(fr)
        if paths is None:
            CALLSI["hit"] = True
            continue
        for path in paths:
            kids = []
            for (ii, jj) in path:
                a = (rr + ii) % n; b = (rr + jj) % n
                kids.append(coverI(pairs[a], [word[(rr + t) % n] for t in range(ii, jj)]))
            dd = max(k["depth"] for k in kids) + 1
            cand = (dd, rr, len(path), path, kids)
            if best is None or (cand[0], cand[1], cand[2]) < \
                    (best[0], best[1], best[2]):
                best = cand
    if CALLSI["hit"]:
        r = {"covered": False, "indeterminate": "cap-hit", "neg": neg}
        MEMOI[key] = r
        return r
    if best is not None:
        dd, rr, _, path, kids = best
        totA = sum(l["a"] for l in legs); totQ = sum(l["q"] for l in legs)
        r = {"covered": True, "depth": dd,
             "cert": {"r": rr, "cuts": [p[0] for p in path] + [n],
                      "bounds": [((rr + p[0]) % n, (rr + p[1]) % n) for p in path]},
             "A": totA, "Q": totQ,
             "additive": sum(k["A"] for k in kids) == totA
             and sum(k["Q"] for k in kids) == totQ}
        MEMOI[key] = r
        return r
    r = {"covered": False, "neg": neg,
         "A": sum(l["a"] for l in legs), "Q": sum(l["q"] for l in legs)}
    MEMOI[key] = r
    return r

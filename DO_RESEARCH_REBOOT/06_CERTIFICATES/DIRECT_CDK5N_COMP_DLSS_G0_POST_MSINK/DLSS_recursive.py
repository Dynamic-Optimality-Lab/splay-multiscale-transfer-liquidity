# DLSS recursive C21* engine: own memo, Bellman-Ford DP, bank-21 base
# (20 mechanisms + promoted MSINK tested at EVERY recursion level).
import sys
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_DLSS_G0_POST_MSINK')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_MSINK_G0_CYCLIC_RC')
from RC_recursive_closure_engine import replay_from, canon
from CRA_segment_memberships import full_banked, merged_blocks
from DLSS_membership import strict_msink_bank

MEMO21 = {}
CALLS21 = {"n": 0, "hit": False}
CAP21 = 60000

def bank21(legs, pairs, snaps):
    # Frozen 20-mechanism battery + promoted MSINK (tested at every level).
    from CRA_segment_memberships import full_banked
    fb = full_banked(legs, pairs, snaps)
    if fb is None:
        return None
    fb["MSINK"] = strict_msink_bank(legs, pairs)
    return fb

def base21(start, word, legs, pairs, snaps):
    n = len(word)
    A = sum(l["a"] for l in legs); Q = sum(l["q"] for l in legs)
    if A == 0:
        keys = sorted({l["x"] for l in legs})
        if Q == 0 and len(keys) == 1:
            return True, {"basis": "Z", "A": 0, "Q": 0}
        return False, {"basis": "Z-fail"}
    fb = bank21(legs, pairs, snaps)
    if fb is None:
        return False, {"basis": "battery-none"}
    flags = sorted(k for k, v in fb.items() if v)
    if flags:
        return True, {"basis": "RotB21", "mechanisms": flags, "A": A, "Q": Q}
    return False, {"basis": "no-mechanism", "A": A, "Q": Q}

def cover21(start, word):
    key = (start, canon(word))
    if key in MEMO21:
        return MEMO21[key]
    CALLS21["n"] += 1
    if CALLS21["n"] > CAP21:
        CALLS21["hit"] = True
        r = {"covered": False, "indeterminate": "cap"}
        MEMO21[key] = r
        return r
    n = len(word)
    try:
        Fr = replay_from(start, word)
    except Exception as e:
        r = {"covered": False, "indeterminate": "replay-%s" % e}
        MEMO21[key] = r
        return r
    if Fr["pairs"][-1] != start:
        r = {"covered": False, "why": "not-closed"}
        MEMO21[key] = r
        return r
    legs = Fr["legs"]
    ok, cert = base21(start, word, legs, Fr["pairs"], Fr["snaps"])
    if ok:
        r = {"covered": True, "depth": 0, "cert": cert, "n": n,
             "A": sum(l["a"] for l in legs), "Q": sum(l["q"] for l in legs)}
        MEMO21[key] = r
        return r
    if n <= 1:
        r = {"covered": False, "why": "atomic", "base": cert}
        MEMO21[key] = r
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
                ch = cover21(pairs[a], sw)
                einfo[(i, j)] = {"a": a, "b": b,
                                 "covered": ch.get("covered", False),
                                 "depth": ch.get("depth"),
                                 "ind": ch.get("indeterminate")}
                if ch.get("indeterminate"):
                    CALLS21["hit"] = True
                if ch.get("covered"):
                    edges.setdefault(i, []).append((j, ch["depth"]))
        INF = (10 ** 9, 10 ** 9)
        dist = {0: (-1, 0)}
        import heapq as _hq
        heap = [(-1, 0, 0)]
        while heap:
            (dm, np_, ii) = _hq.heappop(heap)
            if (dm, np_) != dist.get(ii):
                continue
            for (jj, dd) in edges.get(ii, []):
                cand = (max(dm, dd), np_ + 1)
                if cand < dist.get(jj, INF):
                    dist[jj] = cand
                    _hq.heappush(heap, (cand[0], cand[1], jj))
        fr = {"r": rr, "nclosed": len(einfo),
              "segs": {str(k): {"c": v["covered"], "d": v["depth"]}
                       for k, v in einfo.items()}}
        neg["rots"].append(fr)
        if n in dist and dist[n][1] >= 2:
            opt = dist
            def dfs(v, _e=edges, _o=opt, _n=n):
                if v == _n:
                    return [v]
                for (jj, dd) in sorted(_e.get(v, [])):
                    if _o.get(jj) is None:
                        continue
                    ed = next(d for (j2, d) in _e[v] if j2 == jj)
                    if max(_o[v][0], ed) == _o[jj][0] and \
                            _o[v][1] + 1 == _o[jj][1]:
                        r2 = dfs(jj)
                        if r2 is not None:
                            return [v] + r2
                return None
            verts = dfs(0)
            if verts is not None:
                path = list(zip(verts[:-1], verts[1:]))
                kids = []
                for (ii, jj) in path:
                    a = (rr + ii) % n; b = (rr + jj) % n
                    kids.append(cover21(pairs[a], [word[(rr + t) % n] for t in range(ii, jj)]))
                dd = max(k["depth"] for k in kids) + 1
                cand = (dd, rr, len(path), path, kids)
                if best is None or (cand[0], cand[1], cand[2]) < \
                        (best[0], best[1], best[2]):
                    best = cand
    if CALLS21["hit"]:
        r = {"covered": False, "indeterminate": "cap-hit", "neg": neg}
        MEMO21[key] = r
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
        MEMO21[key] = r
        return r
    r = {"covered": False, "neg": neg,
         "A": sum(l["a"] for l in legs), "Q": sum(l["q"] for l in legs)}
    MEMO21[key] = r
    return r

# PROOF independent recursive checker: separate decision procedure.
# Bellman-Ford minimax DP (structurally distinct from RC Dijkstra engine),
# own memo, own certificates. Shared audited primitives only
# (replay_from lockstep, full_banked predicates, totals).
import sys
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_MSINK_G0_CYCLIC_RC')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_MSINK_PROOF_RCG0')
from RC_recursive_closure_engine import replay_from, canon, BUDGET as _
from CRA_segment_memberships import full_banked

MEMO2 = {}
CALLS = {"n": 0, "hit": False}
CAP = 60000

def bellman_ford(n, edges):
    """edges: dict i -> list of (j, childdepth). Returns (dist, pred) with
    dist[v] = min (maxdepth, nparts); pred for lex-smallest tight recovery
    handled by caller via tight DFS."""
    INF = (10 ** 9, 10 ** 9)
    dist = {v: INF for v in range(n + 1)}
    dist[0] = (-1, 0)
    for _ in range(n):
        changed = False
        for i in range(n + 1):
            di = dist[i]
            if di == INF:
                continue
            for (j, dd) in edges.get(i, []):
                cand = (max(di[0], dd), di[1] + 1)
                if cand < dist[j]:
                    dist[j] = cand
                    changed = True
        if not changed:
            break
    return dist

def lex_tight_path(n, edges, edepth, dist):
    opt = dist
    def dfs(v):
        if v == n:
            return [v]
        for (jj, dd) in sorted(edges.get(v, [])):
            if opt.get(jj) is None:
                continue
            if max(opt[v][0], edepth[(v, jj)]) == opt[jj][0] and \
                    opt[v][1] + 1 == opt[jj][1]:
                r = dfs(jj)
                if r is not None:
                    return [v] + r
        return None
    return dfs(0)

def cover2(start, word):
    key = (start, canon(word))
    if key in MEMO2:
        return MEMO2[key]
    CALLS["n"] += 1
    if CALLS["n"] > CAP:
        CALLS["hit"] = True
        r = {"covered": False, "indeterminate": "cap"}
        MEMO2[key] = r
        return r
    n = len(word)
    try:
        Fr = replay_from(start, word)
    except Exception as e:
        r = {"covered": False, "indeterminate": "replay-%s" % e}
        MEMO2[key] = r
        return r
    if Fr["pairs"][-1] != start:
        r = {"covered": False, "why": "not-closed"}
        MEMO2[key] = r
        return r
    legs = Fr["legs"]
    A = sum(l["a"] for l in legs); Q = sum(l["q"] for l in legs)
    if A == 0:
        keys = sorted({l["x"] for l in legs})
        if Q == 0 and len(keys) == 1:
            r = {"covered": True, "depth": 0, "via": "Z", "A": 0, "Q": 0}
        else:
            r = {"covered": False, "why": "Z-fail"}
        MEMO2[key] = r
        return r
    from CRA_segment_memberships import merged_blocks
    mb = merged_blocks(legs)
    if not isinstance(mb, list):
        r = {"covered": False, "why": "badblocks"}
        MEMO2[key] = r
        return r
    fb = full_banked(legs, Fr["pairs"], Fr["snaps"])
    if fb is None:
        r = {"covered": False, "why": "battery-none"}
        MEMO2[key] = r
        return r
    flags = sorted(k for k, v in fb.items() if v)
    if flags:
        r = {"covered": True, "depth": 0, "via": flags, "A": A, "Q": Q}
        MEMO2[key] = r
        return r
    if n <= 1:
        r = {"covered": False, "why": "atomic"}
        MEMO2[key] = r
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
                ch = cover2(pairs[a], sw)
                einfo[(i, j)] = {"a": a, "b": b, "covered": ch.get("covered", False),
                                 "depth": ch.get("depth"),
                                 "ind": ch.get("indeterminate")}
                if ch.get("indeterminate"):
                    CALLS["hit"] = True
                if ch.get("covered"):
                    edges.setdefault(i, []).append((j, ch["depth"]))
        dist = bellman_ford(n, edges)
        ed = {(i, j): d for i, js in edges.items() for (j, d) in js}
        ro = {"r": rr, "nclosed": len(einfo),
              "segs": {str(k): {"c": v["covered"], "d": v["depth"], "ind": v["ind"]}
                       for k, v in einfo.items()}}
        neg["rots"].append(ro)
        if n in dist and dist[n][1] >= 2:
            # tight lex-smallest vertex path
            opt = dist
            def dfs(v, _e=edges, _ed=ed, _o=opt, _n=n):
                if v == _n:
                    return [v]
                for (jj, dd) in sorted(_e.get(v, [])):
                    if _o.get(jj) is None:
                        continue
                    if max(_o[v][0], _ed[(v, jj)]) == _o[jj][0] and \
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
                    kids.append(cover2(pairs[a], [word[(rr + t) % n] for t in range(ii, jj)]))
                dd = max(k["depth"] for k in kids) + 1
                cand = (dd, rr, len(path), path, kids)
                if best is None or (cand[0], cand[1], cand[2], cand[3]) < \
                        (best[0], best[1], best[2], best[3]):
                    best = cand
    if CALLS["hit"]:
        r = {"covered": False, "indeterminate": "cap-hit", "neg": neg}
        MEMO2[key] = r
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
        MEMO2[key] = r
        return r
    r = {"covered": False, "neg": neg, "A": sum(l["a"] for l in legs),
         "Q": sum(l["q"] for l in legs)}
    MEMO2[key] = r
    return r

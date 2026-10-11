# RC recursive proof closure C*: memoized cover() over (start-state, word).
# Reuses audited CRA engine modules (hashes pinned in provenance doc).
# cover() returns COVERED (+proof DAG, depth) or UNCOVERED (+negative record)
# or INDETERMINATE (budget). Children strictly shorter: depth <= n.
import sys, json
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_MSINK_G0_CYCLIC_RC')
sys.path.insert(0, 'scripts')
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'python/liquidity')
from wp6_eventflow import to_ptr, splay_A, splay_B_push
from CRA_pointer_tuple_replay import replay, totals, core_of, from_serial, ReplayError
from CRA_segment_memberships import full_banked, merged_blocks, keep_support, genuine_keys
import splay as S
import copy

BUDGET = {"subproblems": 50000, "used_subproblems": 0, "hit": False}

def canon(w):
    return ",".join(m + str(k) for m, k in w)

def _plist(t):
    # serial (. leaves, tuples) -> nested lists (None leaves) for to_ptr
    if t == '.':
        return None
    k, l, r = t
    return [k, _plist(l), _plist(r)]

def idep(t):
    out = {}
    def go(nd, d):
        if nd[0] == "leaf":
            return
        _, k, l, r = nd
        out[k] = d; go(l, d + 1); go(r, d + 1)
    go(t, 0)
    return out
def iser(t):
    if t[0] == "leaf":
        return '.'
    _, k, l, r = t
    return (k, iser(l), iser(r))

def replay_from(start, word):
    """Fresh pointer+tuple lockstep replay of word from start pair-serials.
    Pointer trees rebuilt from serials (parent pointers wired by to_ptr).
    Records push sets + per-access engine agreement. Never restarts at T0."""
    IA = from_serial(start[0]); IB = from_serial(start[1])
    PA = to_ptr(copy.deepcopy(_plist(start[0])))
    PB = to_ptr(copy.deepcopy(_plist(start[1])))
    legs, pairs, snaps = [], [start], {}
    agree = True
    for i, (md, x) in enumerate(word):
        da = idep(IA).get(x, -1)
        if da < 0:
            raise ReplayError("absent-A %r at %d" % (x, i))
        a = (da + 1) // 2
        pda = _pdep(PA).get(x, -1)
        if pda != da:
            raise ReplayError("pointer/tuple dA diverge at %d" % i)
        sA, sB = iser(IA), iser(IB)
        psb = _pser(PB)
        if psb != sB:
            raise ReplayError("pointer/tuple B-tree diverge at %d" % i)
        if md == 'K':
            db = idep(IB).get(x, -1)
            if db < 0:
                raise ReplayError("absent-B %r at %d" % (x, i))
            q = db // 2
        else:
            db = None; q = 0
        IA = S.trace(IA, x)[0]
        if md == 'K':
            IB = S.trace(IB, x)[0]
        PA, _ = splay_A(PA, x)
        push = []
        if md == 'K':
            PB, outB = splay_B_push(PB, x)
            for s in outB:
                push += list(s)
        if iser(IA) != _pser(PA) or iser(IB) != _pser(PB):
            raise ReplayError("pointer/tuple post-tree diverge at %d" % i)
        chg = (iser(IB) != sB) if md == 'K' else False
        snaps[i] = idep(IB)
        legs.append({"m": md, "x": x, "dA": da, "dB": db, "a": a, "q": q,
                     "delta": q - 2 * a, "ra": sA[0] if sA != '.' else None,
                     "rb": sB[0] if sB != '.' else None, "chg": chg,
                     "push": sorted(set(push))})
        pairs.append((iser(IA), iser(IB)))
    return {"legs": legs, "pairs": pairs, "snaps": snaps, "agree": agree}

def _pdep(t):
    out = {}
    def go(nd, d):
        if nd is None:
            return
        out[nd["k"]] = d
        go(nd["l"], d + 1); go(nd["r"], d + 1)
    while t["p"] is not None:
        t = t["p"]
    go(t, 0)
    return out
def _pser(t):
    while t["p"] is not None:
        t = t["p"]
    def go(nd):
        if nd is None:
            return '.'
        return (nd["k"], go(nd["l"]), go(nd["r"]))
    return go(t)

MEMO = {}

def base_cover(start, word, legs, pairs, snaps):
    """C0: Rot(B) via rotation-invariant battery + Z-basis. Returns
    (True, cert) or (False, summary). snaps keyed by frame index (push in legs)."""
    n = len(word)
    A = sum(l["a"] for l in legs); Q = sum(l["q"] for l in legs)
    if A == 0:
        if Q == 0:
            keys = sorted({l["x"] for l in legs})
            if len(keys) == 1:
                return True, {"basis": "Z", "A": 0, "Q": 0, "key": keys[0],
                              "proof": "closed-A0-single-key-noop"}
        return False, {"basis": "Z-fail", "A": A, "Q": Q,
                       "note": "A0-with-Q>0-or-multikey: IMPOSSIBLE-if-closed"}
    mb = merged_blocks(legs)
    if not isinstance(mb, list):
        return False, {"basis": "battery-none"}
    fb = full_banked(legs, pairs, snaps)
    if fb is None:
        return False, {"basis": "battery-none"}
    flags = sorted(k for k, v in fb.items() if v)
    if flags:
        return True, {"basis": "RotB", "mechanisms": flags, "A": A, "Q": Q}
    return False, {"basis": "no-mechanism", "A": A, "Q": Q}

def cover(start, word, depth=0):
    """C* membership for closed cycle (start, word). Memoized."""
    key = (start, canon(word))
    if key in MEMO:
        return MEMO[key]
    BUDGET["used_subproblems"] += 1
    if BUDGET["used_subproblems"] > BUDGET["subproblems"]:
        BUDGET["hit"] = True
        r = {"covered": False, "indeterminate": "subproblem-budget"}
        MEMO[key] = r
        return r
    n = len(word)
    try:
        Fr = replay_from(start, word)
    except ReplayError as e:
        r = {"covered": False, "indeterminate": "replay-%s" % e}
        MEMO[key] = r
        return r
    if Fr["pairs"][-1] != start:
        r = {"covered": False, "why": "not-closed"}
        MEMO[key] = r
        return r
    legs = Fr["legs"]
    ok, cert = base_cover(start, word, legs, Fr["pairs"], Fr["snaps"])
    if ok:
        r = {"covered": True, "depth": 0, "cert": cert, "n": n,
             "A": sum(l["a"] for l in legs), "Q": sum(l["q"] for l in legs)}
        MEMO[key] = r
        return r
    if n <= 1:
        r = {"covered": False, "why": "atomic-uncovered",
             "base": cert, "n": n}
        MEMO[key] = r
        return r
    # recursive: every rotation r, DP over closed segments (children via cover)
    pairs = Fr["pairs"]
    best = None
    neg = {"rotations": n, "frames": []}
    for rr in range(n):
        edges = {}
        frame = {}
        for i in range(n + 1):
            for j in range(i + 1, n + 1):
                if j - i == n:
                    continue
                a = (rr + i) % n; b = (rr + j) % n
                if pairs[a] != pairs[b]:
                    continue
                segword = [word[(rr + t) % n] for t in range(i, j)]
                segstart = pairs[a]
                ch = cover(segstart, segword, depth + 1)
                frame[(i, j)] = {"a": a, "b": b,
                                 "covered": ch.get("covered", False),
                                 "depth": ch.get("depth"),
                                 "ind": ch.get("indeterminate"),
                                 "why": ch.get("why", ch.get("cert"))}
                if ch.get("indeterminate"):
                    BUDGET["hit"] = True
                if ch.get("covered"):
                    edges.setdefault(i, []).append(j)
        # Two-phase canonical path (H5): Dijkstra for min (maxdepth, nparts),
        # then lex-smallest path among tight edges (tight ⇒ nparts rises ⇒ DAG).
        import heapq as _hq
        INF = (10 ** 9, 10 ** 9)
        edepth = {(i, j): frame[(i, j)]["depth"] for (i, j) in frame
                  if frame[(i, j)]["covered"]}
        dist = {0: (-1, 0)}
        heap = [(-1, 0, 0)]
        while heap:
            (dm, np_, ii) = _hq.heappop(heap)
            if (dm, np_) != dist.get(ii):
                continue
            for jj in edges.get(ii, []):
                cand = (max(dm, edepth[(ii, jj)]), np_ + 1)
                if cand < dist.get(jj, INF):
                    dist[jj] = cand
                    _hq.heappush(heap, (cand[0], cand[1], jj))
        fr = {"r": rr, "nclosed": sum(1 for k in frame),
              "ncovered": sum(1 for k in frame if frame[k]["covered"]),
              "segments": {str(k): {"covered": v["covered"],
                                    "depth": v["depth"],
                                    "why": str(v["why"])[:120],
                                    "ind": v["ind"]} for k, v in frame.items()}}
        neg["frames"].append(fr)
        if n in dist and dist[n][1] >= 2:
            opt = dist
            def dfs(v):
                if v == n:
                    return [v]
                for jj in sorted(edges.get(v, [])):
                    if opt.get(jj) is None:
                        continue
                    if max(opt[v][0], edepth[(v, jj)]) == opt[jj][0] and \
                            opt[v][1] + 1 == opt[jj][1]:
                        r2 = dfs(jj)
                        if r2 is not None:
                            return [v] + r2
                return None
            verts = dfs(0)
            if verts is not None:
                path = [(a2, b2) for a2, b2 in zip(verts[:-1], verts[1:])]
                kids = []
                for (ii, jj) in path:
                    a = (rr + ii) % n; b = (rr + jj) % n
                    kids.append(cover(pairs[a],
                                      [word[(rr + t) % n] for t in range(ii, jj)],
                                      depth + 1))
                dmax = max(k["depth"] for k in kids)
                cand = {"r": rr, "cuts": [p[0] for p in path] + [n],
                        "bounds": [((rr + p[0]) % n, (rr + p[1]) % n)
                                   for p in path],
                        "depth": dmax + 1, "kids": kids}
                if best is None or (cand["depth"], cand["r"], len(cand["cuts"]), cand["cuts"]) < \
                        (best["depth"], best["r"], len(best["cuts"]), best["cuts"]):
                    best = cand
    if BUDGET["hit"]:
        r = {"covered": False, "indeterminate": "budget-hit", "neg": neg, "n": n}
        MEMO[key] = r
        return r
    if best is not None:
        totA = sum(l["a"] for l in legs); totQ = sum(l["q"] for l in legs)
        r = {"covered": True, "depth": best["depth"], "cert": best, "n": n,
             "A": totA, "Q": totQ,
             "additive": sum(k["A"] for k in best["kids"]) == totA
             and sum(k["Q"] for k in best["kids"]) == totQ}
        MEMO[key] = r
        return r
    r = {"covered": False, "neg": neg, "n": n,
         "A": sum(l["a"] for l in legs), "Q": sum(l["q"] for l in legs)}
    MEMO[key] = r
    return r

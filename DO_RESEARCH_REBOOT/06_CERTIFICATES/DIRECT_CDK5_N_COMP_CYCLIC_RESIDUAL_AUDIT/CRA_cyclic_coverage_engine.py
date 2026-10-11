# CRA cyclic additive-coverage engine: every rotation, every closed segment,
# fresh from-state replay + cross-check, exact DP, abstract oracle (F6/F8).
import sys, itertools
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
from CRA_pointer_tuple_replay import replay, from_serial, totals, pair_classes, ReplayError
import splay as S
from CRA_segment_memberships import full_banked, merged_blocks

def legs_equal(l1, l2):
    keys = ("m", "x", "dA", "dB", "a", "q", "ra", "rb", "chg")
    return all(a.get(k) == b.get(k) for a, b in zip(l1, l2) for k in keys) \
        and len(l1) == len(l2)

def fresh_segment(word, pairs, a, b):
    """Replay cyclic interval [a,b) (mod n) from rebuilt P_a trees.
    Returns dict with legs + closure + cross-check vs sliced whole-word legs."""
    n = len(word)
    L = (b - a) % n
    if L == 0:
        return None
    idx = [(a + t) % n for t in range(L)]
    seg = [word[t] for t in idx]
    start = pairs[a]
    IA = from_serial(start[0]); IB = from_serial(start[1])
    legs = []
    for (md, x) in seg:
        da = _idep(IA).get(x, -1)
        if da < 0:
            return {"error": "absent-A-%s" % x}
        a2 = (da + 1) // 2
        sA, sB = _iser(IA), _iser(IB)
        ra = sA[0] if sA != '.' else None
        rb = sB[0] if sB != '.' else None
        sb = sB
        if md == 'K':
            db = _idep(IB).get(x, -1)
            if db < 0:
                return {"error": "absent-B-%s" % x}
            q = db // 2
        else:
            db = None; q = 0
        IA = S.trace(IA, x)[0]
        if md == 'K':
            IB = S.trace(IB, x)[0]
        chg = (_iser(IB) != sb) if md == 'K' else False
        legs.append({"m": md, "x": x, "dA": da, "dB": db, "a": a2, "q": q,
                     "delta": q - 2 * a2, "ra": ra, "rb": rb, "chg": chg})
    end = (_iser(IA), _iser(IB))
    return {"legs": legs, "start": start, "end": end,
            "closed": end == pairs[b], "idx": idx}

def _idep(t):
    out = {}
    def go(nd, d):
        if nd[0] == "leaf":
            return
        _, k, l, r = nd
        out[k] = d; go(l, d + 1); go(r, d + 1)
    go(t, 0)
    return out
def _iser(t):
    if t[0] == "leaf":
        return '.'
    _, k, l, r = t
    return (k, _iser(l), _iser(r))

def classify_segment(word, W, a, b):
    """Full certificate for cyclic interval [a,b). W = whole-word replay.
    Returns dict with covered bool + mechanism + cross-checks."""
    n = len(word)
    if pairs_ne(W["pairs"][a], W["pairs"][b]):
        return {"covered": False, "why": "not-closed"}
    fr = fresh_segment(word, W["pairs"], a, b)
    if fr is None or "error" in fr:
        return {"covered": False, "why": fr["error"] if fr else "empty"}
    if not fr["closed"]:
        return {"covered": False, "why": "fresh-replay-not-closed"}
    # cross-check vs sliced whole-word legs (N.28 evidence)
    sliced = [W["legs"][t] for t in fr["idx"]]
    xcheck = legs_equal(fr["legs"], sliced)
    A = sum(l["a"] for l in fr["legs"]); Q = sum(l["q"] for l in fr["legs"])
    if A == 0:
        # closed A0 walk: all accesses one key; closure forces Q==0 (see doc)
        keys = {l["x"] for l in fr["legs"]}
        cov = (Q == 0 and len(keys) == 1)
        return {"covered": cov, "why": "A0-trivial" if cov else "A0-Q>0",
                "A": A, "Q": Q, "xcheck": xcheck, "canon": _canon(
                    [word[t] for t in fr["idx"]])}
    mb = merged_blocks(fr["legs"])
    if not isinstance(mb, list):
        return {"covered": False, "why": "badblocks", "A": A, "Q": Q,
                "xcheck": xcheck}
    # slice-frame snaps: B-depth dicts from whole-word pointer snaps at idx
    snaps = {t: W["snaps"][fr["idx"][t]] for t in range(len(fr["idx"]))
             if fr["idx"][t] in W["snaps"]}
    # remap block l1 to slice frame
    pos_of = {g: t for t, g in enumerate(fr["idx"])}
    for blk in mb:
        blk["l1"] = pos_of.get(blk["l1"] - 1, -1) + 1
        blk["l0"] = pos_of.get(blk["l0"], -1)
    pairs_seg = [W["pairs"][a]] + [W["pairs"][(t + 1) % n] for t in fr["idx"]]
    fb = full_banked(fr["legs"], pairs_seg, snaps)
    if fb is None:
        return {"covered": False, "why": "battery-none", "A": A, "Q": Q,
                "xcheck": xcheck}
    flags = sorted(k for k, v in fb.items() if v)
    return {"covered": bool(flags), "why": "+".join(flags) if flags else "no-mechanism",
            "A": A, "Q": Q, "xcheck": xcheck,
            "canon": _canon([word[t] for t in fr["idx"]])}

def pairs_ne(p, q):
    return p != q

def _canon(w):
    return ",".join(m + str(k) for m, k in w)

def cyclic_covers(word, W):
    """Exact cyclic additive coverage: every rotation r, DP over closed segs.
    Returns dict: covered, certificate(s), rotations_exhausted, primitive."""
    n = len(word)
    pairs = W["pairs"]
    pre = pairs[:-1]
    if len(set(pre)) == n:
        return {"covered": False, "primitive": True, "certificate": None,
                "rotations": n, "note": "F7-pair-state-simple"}
    segcache = {}
    SEG_BUDGET = [400]
    def seg(a, b):
        if (a, b) in segcache:
            return segcache[(a, b)]
        if len(segcache) >= SEG_BUDGET[0]:
            r = {"covered": False, "why": "segment-budget-exceeded"}
        else:
            r = classify_segment(word, W, a, b)
        segcache[(a, b)] = r
        return r
    certs = []
    for r in range(n):
        # edges i->j (0<=i<j<=n) with P[(r+i)%n]==P[(r+j)%n], j-i<n... allow full?
        edges = {}
        for i in range(n + 1):
            for j in range(i + 1, n + 1):
                if j - i == n:
                    continue
                a = (r + i) % n; b = (r + j) % n
                if pairs[a] != pairs[b]:
                    continue
                c = seg(a, b)
                if c["covered"]:
                    edges.setdefault(i, []).append((j, c))
        # shortest path 0->n with >=2 edges (BFS)
        from collections import deque
        prev = {0: None}
        dq = deque([0])
        found = None
        while dq:
            i = dq.popleft()
            for (j, c) in sorted(edges.get(i, [])):
                if j not in prev:
                    prev[j] = (i, c)
                    dq.append(j)
                    if j == n and found is None:
                        found = j
        if found is not None:
            # reconstruct
            path, cert = [], []
            j = n
            while j != 0:
                i, c = prev[j]
                path.append((i, j)); cert.append(c)
                j = i
            path.reverse(); cert.reverse()
            if len(path) >= 2:
                A = sum(x["A"] for x in cert); Q = sum(x["Q"] for x in cert)
                tot = totals(W["legs"])
                bounds = [((r + path[k][0]) % n, (r + path[k][1]) % n)
                          for k in range(len(path))]
                for bb, cc in zip(bounds, cert):
                    cc["bounds"] = bb
                certs.append({"r": r, "cuts": [p[0] for p in path] + [n],
                              "parts": cert, "A": A, "Q": Q,
                              "additive": (A == tot["A"] and Q == tot["Q"])})
    if certs:
        certs.sort(key=lambda c: (c["r"], len(c["cuts"]), c["cuts"]))
        return {"covered": True, "primitive": False, "certificate": certs[0],
                "ncerts": len(certs), "rotations": n}
    budget_hit = any(v.get("why") == "segment-budget-exceeded"
                     for v in segcache.values())
    return {"covered": False, "primitive": False, "certificate": None,
            "rotations": n, "note": "DP-exhausted-no-covered-partition",
            "nsegments_tested": len(segcache), "exhaustive": not budget_hit}

# ---- F8 abstract oracle: DP core on synthetic equality patterns ----
def dp_core(n, closed):
    """closed(a,b) bool for cyclic interval. Returns first (r, path) or None."""
    for r in range(n):
        edges = {}
        for i in range(n + 1):
            for j in range(i + 1, n + 1):
                if j - i == n:
                    continue
                if closed((r + i) % n, (r + j) % n):
                    edges.setdefault(i, []).append(j)
        from collections import deque
        prev = {0: None}
        dq = deque([0])
        while dq:
            i = dq.popleft()
            for j in sorted(edges.get(i, [])):
                if j not in prev:
                    prev[j] = (i,)
                    dq.append(j)
        if n in prev:
            path = []
            j = n
            while j != 0:
                i = prev[j][0]
                path.append((i, j)); j = i
            path.reverse()
            if len(path) >= 2:
                return (r, path)
    return None

def oracle_selftest():
    # Labels are pair-states P_0..P_{n-1} (vertex n IDENTIFIES with vertex 0's
    # state via closure; dp_core queries closed() only on 0..n-1 labels).
    T = []
    def chk(name, got, want):
        T.append((name, got == want, got, want))
    # anchored two-part n=4: P0==P2. r=0 edges 0->2 (P0==P2), 2->4 (P2==P0).
    eq = {(0, 2)}
    cl = lambda a, b: (a, b) in eq or (b, a) in eq or a == b
    r = dp_core(4, cl)
    chk("anchored-2part", r is not None and r[0] == 0 and len(r[1]) == 2, True)
    # non-anchored n=4: P1==P3 only. r=0: edge 1->3 alone, no path. r=1:
    # edges 0->2 (P1==P3), 2->4 (P3==P1): path found.
    eq2 = {(1, 3)}
    cl2 = lambda a, b: (a, b) in eq2 or (b, a) in eq2 or a == b
    r = dp_core(4, cl2)
    chk("nonanchored-needs-rotation", r is not None and r[0] == 1, True)
    # three-part n=5: P0==P2, P2==P4, P4==P0. BFS shortest path is
    # (0,2),(2,5) length 2 (canonical first certificate); r=0.
    eq3 = {(0, 2), (2, 4), (4, 0)}
    cl3 = lambda a, b: (a, b) in eq3 or (b, a) in eq3 or a == b
    r3 = dp_core(5, cl3)
    chk("three-part-shortest", r3 is not None and r3[0] == 0 and len(r3[1]) == 2
        and r3[1] == [(0, 2), (2, 5)], True)
    # primitive: no repeats among P_0..P_3
    cl4 = lambda a, b: a == b
    chk("primitive-none", dp_core(4, cl4) is None, True)
    # whole-only (closure alone, no repeats) => no >=2-part path
    chk("whole-only-none", dp_core(5, cl4) is None, True)
    # same-root-different-tree modeled as unequal labels => no edge
    chk("label-inequality", dp_core(3, lambda a, b: a == b) is None, True)
    # zero-length excluded: n=1 single-state cycle: no edges (j-i<n empty)
    chk("n1-none", dp_core(1, lambda a, b: a == b) is None, True)
    # rotation sensitivity n=6: only repeat P3==P5.
    # r=0: edge 3->5 only (0->3? no; 5->6? P5==P0? no). r=1: edge 2->4 only.
    # r=2: edge 1->3 only. r=3: edges 0->2 (P3==P5), 2->6 (P5==P3): FIRST path.
    eq6 = {(3, 5)}
    cl6 = lambda a, b: ((a, b) in eq6 or (b, a) in eq6 or a == b)
    r6 = dp_core(6, cl6)
    chk("rotation-found", r6 is not None and r6[0] == 3 and len(r6[1]) == 2, True)
    return T

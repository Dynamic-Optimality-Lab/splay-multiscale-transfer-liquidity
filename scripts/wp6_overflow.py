"""PIVOT-13 overflow genealogy + creator matching (StepEv-level charging).

Instrumented replay: every A/B splay step captured with ordered triple
(x=node, p=parent, g=grandparent-or-None) + pattern (LL/RR/LR/RL/Z) +
transferred-subtree keys; every rotation logs its changed (child->parent)
edges with (acc, seq) stamps.

Creator: ORIGIN(e) = latest strictly-prior access establishing ancestor edge e
(transitively through same-splay steps to a strictly-prior access; GENESIS if
never built in-history). creator(D) = latest creator of D's two consumed
edges ((x->p),(p->g)).

Matching: LEFT = B-double StepEvs (the Q objects), RIGHT = 2 credits per
A-StepEv; edges = same-access (local) + creator-access. Kuhn max matching;
on failure, Koenig Hall-violator extraction.
"""
from __future__ import annotations
import sys
import json
import copy
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from liquidity import legacy_embedding as PE

BD = ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "overflow"


def step(sid, msg):
    print("[OVF %s] %s" % (sid, msg), flush=True)


def save(name, obj):
    BD.mkdir(parents=True, exist_ok=True)
    (BD / name).write_text(json.dumps(obj, indent=1, sort_keys=True,
                                      default=str), encoding="utf-8")


def to_ptr(t):
    if t is None:
        return None
    root = PE.mknode(t[0])
    stack = [(t, root)]
    while stack:
        src, dst = stack.pop()
        if src[1] is not None:
            nd = PE.mknode(src[1][0])
            nd["p"] = dst
            dst["l"] = nd
            stack.append((src[1], nd))
        if src[2] is not None:
            nd = PE.mknode(src[2][0])
            nd["p"] = dst
            dst["r"] = nd
            stack.append((src[2], nd))
    return root


def _log3(rotlog, acc, seq, nodes):
    for nd in nodes:
        if nd is None:
            continue
        par = nd["p"]
        rotlog.append({"acc": acc, "seq": seq, "child": nd["k"],
                       "parent": (par["k"] if par is not None else None)})


def splay_cap(root, x, acc, rotlog):
    """Splay with per-step capture + rotation edge log. Returns (root, steps)."""
    d, path = PE._depth_to(root, x)
    if not path or path[-1]["k"] != x:
        return root, []
    steps = []
    node = path[-1]
    seq = 0
    while node["p"] is not None:
        p = node["p"]
        g = p["p"]
        xk, pk = node["k"], p["k"]
        gk = g["k"] if g is not None else None
        if g is None:
            kind, pat = "zig", "Z"
            if p["l"] is node:
                T = node["r"]
                tp = (T["p"]["k"] if T is not None else None)
                PE._rot_right(p)
                _log3(rotlog, acc, seq, [node, p, T])
            else:
                T = node["l"]
                tp = (T["p"]["k"] if T is not None else None)
                PE._rot_left(p)
                _log3(rotlog, acc, seq, [node, p, T])
            steps.append({"seq": seq, "kind": kind, "pat": pat, "x": xk,
                          "p": pk, "g": gk,
                          "T": [T["k"] if T is not None else None]})
        else:
            kind = "double"
            if p["l"] is node and g["l"] is p:
                pat = "LL"
                T1, T2 = node["r"], p["r"]
                PE._rot_right(g)
                _log3(rotlog, acc, seq, [p, g, T1])
                PE._rot_right(p)
                _log3(rotlog, acc, seq, [node, p, T2])
            elif p["r"] is node and g["r"] is p:
                pat = "RR"
                T1, T2 = node["l"], p["l"]
                PE._rot_left(g)
                _log3(rotlog, acc, seq, [p, g, T1])
                PE._rot_left(p)
                _log3(rotlog, acc, seq, [node, p, T2])
            elif p["r"] is node and g["l"] is p:
                pat = "LR"
                T1, T2 = node["l"], node["r"]
                PE._rot_left(p)
                _log3(rotlog, acc, seq, [node, p, T1])
                PE._rot_right(g)
                _log3(rotlog, acc, seq, [node, g, T2])
            else:
                pat = "RL"
                T1, T2 = node["r"], node["l"]
                PE._rot_right(p)
                _log3(rotlog, acc, seq, [node, p, T1])
                PE._rot_left(g)
                _log3(rotlog, acc, seq, [node, g, T2])
            steps.append({"seq": seq, "kind": kind, "pat": pat, "x": xk,
                          "p": pk, "g": gk,
                          "T": [t["k"] if t is not None else None
                                for t in (T1, T2)]})
        seq += 1
    while node["p"] is not None:
        node = node["p"]
    return node, steps


def depths_of(P):
    out = {}
    stack = [(P, 0)] if P is not None else []
    while stack:
        nd, d = stack.pop()
        out[nd["k"]] = d
        if nd["l"] is not None:
            stack.append((nd["l"], d + 1))
        if nd["r"] is not None:
            stack.append((nd["r"], d + 1))
    return out


def replay(T0A, T0B, word):
    """Full instrumented replay. Verifies step counts vs a/q/z formulas."""
    A = to_ptr(copy.deepcopy(T0A))
    B = to_ptr(copy.deepcopy(T0B))
    accesses = []
    arot, brot = [], []
    setup_map = {}  # key -> acc idx that last A-root-arrived it
    for idx, (md, x) in enumerate(word):
        dA = depths_of(copy.deepcopy(A)).get(x, 0)
        a = (dA + 1) // 2
        setup_before = setup_map.get(x)
        A, asteps = splay_cap(A, x, idx, arot)
        assert len(asteps) == a, (idx, len(asteps), a)
        if md == "K":
            dB = depths_of(copy.deepcopy(B)).get(x, 0)
            q, z = dB // 2, dB % 2
            B, bsteps = splay_cap(B, x, idx, brot)
            ndb = sum(1 for s in bsteps if s["kind"] == "double")
            nzg = sum(1 for s in bsteps if s["kind"] == "zig")
            assert ndb == q and nzg == z, (idx, ndb, q, nzg, z)
        else:
            dB, q, z, bsteps = None, 0, 0, []
        accesses.append({"idx": idx, "m": md, "x": x, "dA": dA, "a": a,
                         "asteps": asteps, "dB": dB, "q": q, "z": z,
                         "eps": q - 2 * a, "bsteps": bsteps,
                         "setup": setup_before})
        if dA > 0:
            setup_map[x] = idx

    def enc(P):
        if P is None:
            return None
        return [P["k"], enc(P["l"]), enc(P["r"])]
    return {"accesses": accesses, "arot": arot, "brot": brot,
            "endA": enc(A), "endB": enc(B)}


def build_origin(brot, accesses=None):
    """Index rotation log by edge; changed-edges grouped by (acc,seq).

    v2: consumed pre-step ancestor edges ((x->p),(p->g) read from live
    pointers before each step's rotations) join the recursion set, so
    same-splay descents follow actually-existing material (U1 proof form).
    """
    by_edge = {}
    changed = {}
    for e in brot:
        by_edge.setdefault((e["child"], e["parent"]), []).append(
            (e["acc"], e["seq"]))
        changed.setdefault((e["acc"], e["seq"]), set()).add(
            (e["child"], e["parent"]))
    consumed = {}
    if accesses is not None:
        for a in accesses:
            for s in a["bsteps"]:
                ce = {(s["x"], s["p"])}
                if s["g"] is not None:
                    ce.add((s["p"], s["g"]))
                consumed[(a["idx"], s["seq"])] = ce
    for k in by_edge:
        by_edge[k].sort()
    return by_edge, changed, consumed


def make_origin_fn(by_edge, changed, consumed=None):
    memo = {}
    consumed = consumed or {}

    def origin(edge, bound):
        key = (edge, bound)
        if key in memo:
            return memo[key]
        lst = by_edge.get(edge, [])
        # latest establishment strictly below bound
        best = None
        for (a, s) in lst:
            if (a, s) < bound:
                best = (a, s)
            else:
                break
        if best is None:
            memo[key] = {"G"}
            return {"G"}
        ba, bs = best
        if ba < bound[0]:
            memo[key] = {ba}
            return {ba}
        # same access, earlier step: recurse over that step's changed
        # edges PLUS its consumed pre-step ancestor edges (v2)
        out = set()
        for e2 in (changed.get((ba, bs), ())
                   | consumed.get((ba, bs), ())):
            r = origin(e2, (ba, bs))
            out |= r
            if len(out) > 64:
                break
        memo[key] = out
        return out

    return origin


def creators(rep):
    """creator per B-double: latest strictly-prior builder of (x->p),(p->g)."""
    by_edge, changed, consumed = build_origin(rep["brot"], rep["accesses"])
    origin = make_origin_fn(by_edge, changed, consumed)
    out = []
    for acc in rep["accesses"]:
        t = acc["idx"]
        for s in acc["bsteps"]:
            if s["kind"] != "double":
                continue
            bnd = (t, s["seq"])
            o1 = origin((s["x"], s["p"]), bnd)
            o2 = origin((s["p"], s["g"]), bnd)
            lat = (o1 | o2) - {"G"}
            cr = max(lat) if lat else None
            gen = (o1 | o2) == {"G"}
            out.append({"acc": t, "x": acc["x"], "seq": s["seq"],
                        "pat": s["pat"], "p": s["p"], "g": s["g"],
                        "creator": cr, "genesis": gen,
                        "norig": len(o1 | o2)})
    return out


def kuhn_match(nL, nR, adj):
    mtR = [-1] * nR
    def dfs(u, seen):
        for v in adj[u]:
            if seen[v]:
                continue
            seen[v] = True
            if mtR[v] < 0 or dfs(mtR[v], seen):
                mtR[v] = u
                return True
        return False
    size = 0
    for u in range(nL):
        if dfs(u, [False] * nR):
            size += 1
    mtL = [-1] * nL
    for v, u in enumerate(mtR):
        if u >= 0:
            mtL[u] = v
    return size, mtL, mtR


def hall_violator(nL, nR, adj, mtL, mtR):
    """Konig Z-set from free LEFT vertices; X = LEFT cap Z is deficient."""
    from collections import deque
    free = [u for u in range(nL) if mtL[u] < 0]
    inZL = [False] * nL
    inZR = [False] * nR
    dq = deque()
    for u in free:
        inZL[u] = True
        dq.append(("L", u))
    # matched-pair lookup L->R
    while dq:
        side, i = dq.popleft()
        if side == "L":
            for v in adj[i]:
                if mtL[i] == v:
                    continue  # only UNmatched L->R
                if not inZR[v]:
                    inZR[v] = True
                    dq.append(("R", v))
        else:
            u = mtR[i]
            if u >= 0 and not inZL[u]:
                inZL[u] = True
                dq.append(("L", u))
    X = [u for u in range(nL) if inZL[u]]
    N = [v for v in range(nR) if inZR[v]]
    return X, N


def charge(rep, crlist):
    """Build eligibility (local + creator) and max-match. Returns report."""
    accesses = rep["accesses"]
    # global credit list: 2 credits per A-step
    asteps = []  # credit id -> acc idx
    acc_credits = {}
    for acc in accesses:
        cl = []
        for _ in acc["asteps"]:
            cid0 = len(asteps)
            asteps.append(acc["idx"])
            asteps.append(acc["idx"])
            cl.extend([cid0, cid0 + 1])
        acc_credits[acc["idx"]] = cl
    nR = len(asteps)
    nL = len(crlist)
    # setup map: acc idx -> setup acc idx
    setup_of = {a["idx"]: a.get("setup") for a in accesses}
    adj = []
    for i, d in enumerate(crlist):
        t = d["acc"]
        es = list(acc_credits[t])  # local first (canonical payment order)
        if d["creator"] is not None:
            es += [c for c in acc_credits[d["creator"]] if c not in es]
        st = setup_of.get(t)
        if st is not None:
            es += [c for c in acc_credits[st] if c not in es]
            d["setup_used"] = st
        adj.append(es)
    size, mtL, mtR = kuhn_match(nL, nR, adj)
    rep_out = {"Q": nL, "credits": nR, "matched": size,
               "full": size == nL}
    if size == nL:
        nloc = ncre = nset = 0
        for u in range(nL):
            v = mtL[u]
            t = crlist[u]["acc"]
            inloc = v in acc_credits[t]
            incr = (crlist[u]["creator"] is not None and
                    v in acc_credits[crlist[u]["creator"]])
            inst = ("setup_used" in crlist[u] and
                    v in acc_credits[crlist[u]["setup_used"]])
            if inst and not inloc and not incr:
                nset += 1
            elif incr and not inloc:
                ncre += 1
            else:
                nloc += 1  # local or ambiguous shared pool -> local
        rep_out["n_local"] = nloc
        rep_out["n_creator"] = ncre
        rep_out["n_setup"] = nset
    else:
        X, N = hall_violator(nL, nR, adj, mtL, mtR)
        rep_out["hall_X"] = X
        rep_out["hall_Nsize"] = len(N)
        rep_out["hall_detail"] = [
            {"acc": crlist[u]["acc"], "x": crlist[u]["x"],
             "seq": crlist[u]["seq"], "pat": crlist[u]["pat"],
             "creator": crlist[u]["creator"],
             "genesis": crlist[u]["genesis"]} for u in X]
    return rep_out

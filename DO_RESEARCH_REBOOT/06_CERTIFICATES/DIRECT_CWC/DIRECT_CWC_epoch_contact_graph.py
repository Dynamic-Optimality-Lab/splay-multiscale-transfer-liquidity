"""DIRECT-CWC: frozen ECT graph builder + verifier + deterministic flow.

Implements frozen spec v1.0 EXACTLY. PASS1 (token semantics), PASS2 (contact
correctness), PASS4 (U1 gap regressions). Aborts on any source mismatch."""
import sys, copy, json
sys.path.insert(0, 'scripts')
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'python/liquidity')
from pathlib import Path
RDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CWC')
RDIR.mkdir(parents=True, exist_ok=True)
from wp6_eventflow import to_ptr, splay_A, splay_B_push
import legacy_embedding as PE

def pdepths(t):
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
def pserial(t):
    while t["p"] is not None:
        t = t["p"]
    def go(nd):
        if nd is None:
            return '.'
        return (nd["k"], go(nd["l"]), go(nd["r"]))
    return go(t)
def proot(t):
    while t["p"] is not None:
        t = t["p"]
    return t["k"]
def vine_right(n):
    t = None
    for k in range(n, 0, -1):
        t = [k, None, t]
    return t

def path_to_tup(serial, x):
    """Ancestor chain root->x in a tuple-serial tree; None if absent."""
    path = []
    def go(nd):
        if nd == '.':
            return False
        k, l, r = nd
        path.append(k)
        if k == x:
            return True
        if go(l) or go(r):
            return True
        path.pop()
        return False
    return list(path) if go(serial) else None
def is_anc_tup(serial, u, x):
    p = path_to_tup(serial, x)
    return p is not None and u in p[:-1]

def splay_A_steps(A, x):
    """Mirror of source splay_A; returns (root, [(rotset, post_serial)])."""
    d, path = PE._depth_to(A, x)
    if not path or path[-1]["k"] != x:
        return A, []
    inv = []
    node = path[-1]
    while node["p"] is not None:
        p = node["p"]
        g = p["p"]
        if g is None:
            if p["l"] is node:
                PE._rot_right(p)
            else:
                PE._rot_left(p)
            inv.append(({node["k"], p["k"]}, pserial(node)))
        elif p["l"] is node and g["l"] is p:
            PE._rot_right(g)
            PE._rot_right(p)
            inv.append(({node["k"], p["k"], g["k"]}, pserial(node)))
        elif p["r"] is node and g["r"] is p:
            PE._rot_left(g)
            PE._rot_left(p)
            inv.append(({node["k"], p["k"], g["k"]}, pserial(node)))
        elif p["r"] is node and g["l"] is p:
            PE._rot_left(p)
            PE._rot_right(g)
            inv.append(({node["k"], p["k"], g["k"]}, pserial(node)))
        else:
            PE._rot_right(p)
            PE._rot_left(g)
            inv.append(({node["k"], p["k"], g["k"]}, pserial(node)))
    while node["p"] is not None:
        node = node["p"]
    return node, inv

class Dinic:
    def __init__(self, n):
        self.n = n
        self.adj = [[] for _ in range(n)]
    def add_edge(self, u, v, c):
        self.adj[u].append([v, c, len(self.adj[v])])
        self.adj[v].append([u, 0, len(self.adj[u]) - 1])
    def maxflow(self, s, t):
        import collections
        flow = 0
        INF = 10 ** 9
        while True:
            level = [-1] * self.n
            level[s] = 0
            dq = collections.deque([s])
            while dq:
                u = dq.popleft()
                for v, c, _ in self.adj[u]:
                    if c > 0 and level[v] < 0:
                        level[v] = level[u] + 1
                        dq.append(v)
            if level[t] < 0:
                return flow
            it = [0] * self.n
            def dfs(u, f):
                if u == t:
                    return f
                while it[u] < len(self.adj[u]):
                    v, c, rev = self.adj[u][it[u]]
                    if c > 0 and level[v] == level[u] + 1:
                        ret = dfs(v, min(f, c))
                        if ret:
                            self.adj[u][it[u]][1] -= ret
                            self.adj[v][rev][1] += ret
                            return ret
                    it[u] += 1
                return 0
            while True:
                f = dfs(s, INF)
                if not f:
                    break
                flow += f

def build_ect(prefix, cycle, head=None):
    """Full capture + graph. head (optional) is replayed between prefix and
    cycle (for rotation-invariance checks); cycle-start state follows head."""
    T0 = vine_right(16)
    A = to_ptr(copy.deepcopy(T0)); B = to_ptr(copy.deepcopy(T0))
    for (md, x) in prefix:
        dA = pdepths(A)[x]; A, _ = splay_A(A, x)
        if md == 'K':
            B, _ = splay_B_push(B, x)
    for (md, x) in (head or []):
        dA = pdepths(A)[x]; A, _ = splay_A(A, x)
        if md == 'K':
            B, _ = splay_B_push(B, x)
    m = len(cycle)
    Aser = [pserial(A)]
    Bser = [pserial(B)]
    acc = []  # per cycle access records
    for (md, x) in cycle:
        dA = pdepths(A)[x]
        a = (dA + 1) // 2
        if md == 'K':
            dB = pdepths(B)[x]
            q = dB // 2
            _, Bpath = PE._depth_to(B, x)
            bpath = [nd["k"] for nd in Bpath]
        else:
            dB = None; q = 0; bpath = None
        # authoritative A splay on copy; mirror on live
        Acopy = copy.deepcopy(A)
        Ar, _ = splay_A(Acopy, x)
        Apre_ser = pserial(A)
        A, Asteps = splay_A_steps(A, x)
        assert pserial(A) == pserial(Ar), ("A mirror divergence", md, x)
        assert len(Asteps) == a, ("StepEv count", md, x, len(Asteps), a)
        for rs, _ in Asteps:
            assert len(rs) in (2, 3), ("rotset size", rs)
        if md == 'K':
            B, Bout = splay_B_push(B, x)
            pushed = [set(s) for s in Bout]
            # PASS1 grouping: doubles == consecutive path pairs parent-toward-root.
            # NOTE: _depth_to path lists nodes from ROOT, so x=bpath[-1],
            # p_k=bpath[n-1-k]; pair j = (p_{2j-1}, p_{2j}}.
            npath = len(bpath)
            assert bpath[-1] == x, ("path end", bpath, x)
            exp_pairs = []
            for j in range(1, q + 1):
                exp_pairs.append({bpath[npath - 2 * j], bpath[npath - 2 * j - 1]})
            got_pairs = [s for s in pushed if len(s) == 2]
            assert len(got_pairs) == q, ("ndouble", md, x)
            assert sorted(map(sorted, got_pairs)) == sorted(map(sorted, exp_pairs)), \
                ("pair grouping", md, x, got_pairs, exp_pairs)
            zig_ok = (dB % 2 == 1) == any(len(s) == 1 for s in pushed)
            assert zig_ok, ("zig parity", md, x)
        else:
            pushed = []
        acc.append({"m": md, "x": x, "dA": dA, "dB": dB, "a": a, "q": q,
                    "Asteps": [(sorted(rs), st) for rs, st in Asteps],
                    "Apre": Apre_ser, "push": [sorted(s) for s in pushed],
                    "bpath": bpath})
        Aser.append(pserial(A))
        Bser.append(pserial(B))
    assert Aser[-1] == Aser[0] and Bser[-1] == Bser[0], "cycle not closed"
    # tokens
    toks = []
    for t, lg in enumerate(acc):
        if lg["m"] != 'K':
            continue
        npath = len(lg["bpath"])
        for j in range(1, lg["q"] + 1):
            p = lg["bpath"][npath - 2 * j]
            qq = lg["bpath"][npath - 2 * j - 1]
            toks.append({"t": t, "j": j - 1, "x": lg["x"], "p": p, "q": qq})
    Q = sum(l["q"] for l in acc)
    assert len(toks) == Q, "token count"
    Aev = sum(l["a"] for l in acc)
    assert 2 * sum(len(l["Asteps"]) for l in acc) == 2 * Aev
    # epochs: H from B serials (states B_0..B_m)
    def H(s, u, x):
        return is_anc_tup(Bser[s], u, x)
    epochs = {}
    for b in toks:
        for (u, tag) in ((b["p"], "p"), (b["q"], "q")):
            t = b["t"]
            assert H(t, u, b["x"]), ("pre-death", b, tag)
            # scan back for birth (bounded by m+1 steps; terminates at death
            # state B_{t+1} at the latest since x is root there)
            j = (t - 1) % m
            for _ in range(m + 1):
                if not H(j, u, b["x"]):
                    break
                j = (j - 1) % m
            birth = j
            assert not H(birth, u, b["x"]), ("birth-0", b, tag)
            # verify H(birth+1)==1
            assert H((birth + 1) % m, u, b["x"]), ("birth+1", b, tag)
            win = set()
            s = (birth + 1) % m
            while True:
                win.add(s)
                if s == t:
                    break
                s = (s + 1) % m
            epochs[(b["t"], b["j"], tag)] = {"u": u, "birth": birth, "win": sorted(win)}
    # contacts: RotA + OwnerA per access
    def owner_at(ai, u, v):
        sts = [acc[ai]["Apre"]] + [st for _, st in acc[ai]["Asteps"]]
        Hf = [is_anc_tup(st, u, v) for st in sts]
        if Hf[-1] == Hf[0]:
            return None
        for e in range(len(sts) - 1, 0, -1):
            if Hf[e] == Hf[-1] and Hf[e - 1] != Hf[-1]:
                return e - 1
        return None
    # graph
    ev_index = {}
    ev_list = []
    for s, lg in enumerate(acc):
        for e in range(len(lg["Asteps"])):
            ev_index[(s, e)] = len(ev_list)
            ev_list.append((s, e))
    edges = set()
    for bi, b in enumerate(toks):
        for tag, u in (("p", b["p"]), ("q", b["q"])):
            ep = epochs[(b["t"], b["j"], tag)]
            for s in ep["win"]:
                lg = acc[s]
                for e, (rs, _) in enumerate(lg["Asteps"]):
                    c1 = u in rs
                    c2 = (owner_at(s, u, b["x"]) == e)
                    if c1 or c2:
                        edges.add((bi, ev_index[(s, e)]))
    nB = len(toks); nE = len(ev_list)
    D = Dinic(2 + nB + nE)
    SRC, SNK = 0, 1 + nB + nE
    for bi in range(nB):
        D.add_edge(SRC, 1 + bi, 1)
    for ei in range(nE):
        D.add_edge(1 + nB + ei, SNK, 2)
    for bi, ei in sorted(edges):
        D.add_edge(1 + bi, 1 + nB + ei, 1)
    flow = D.maxflow(SRC, SNK)
    return {"toks": toks, "ev_list": ev_list, "edges": sorted(edges),
            "nB": nB, "nE": nE, "flow": flow, "Q": Q, "A": Aev,
            "epochs": {str(k): v for k, v in epochs.items()},
            "acc": [{"m": l["m"], "x": l["x"], "dA": l["dA"], "dB": l["dB"],
                     "a": l["a"], "q": l["q"]} for l in acc]}

def verify_cut(ev, S):
    """Independent deficient-cut check from raw edge set."""
    N = set()
    for (bi, ei) in ev["edges"]:
        if bi in S:
            N.add(ei)
    return {"S": sorted(S), "N": sorted(N), "|S|": len(S), "2|N|": 2 * len(N),
            "deficient": len(S) > 2 * len(N)}

if __name__ == "__main__":
    import sys
    U1 = json.load(open('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U1/DIRECT_U1_uncovered_closed_witness.json'))
    out = {}
    for c in U1:
        tag = c["seed"] + "-" + c["tag"]
        print("=== PASS4:", tag, "W=", c["W"], flush=True)
        ev = build_ect(c["prefix"], [tuple(w) for w in c["word"]])
        print("tokens=%d (Q=%d) events=%d (A=%d) edges=%d flow=%d" % (
            ev["nB"], ev["Q"], ev["nE"], ev["A"], len(ev["edges"]), ev["flow"]), flush=True)
        # rotation invariance: same cyclic walk from mid-cycle start
        mrot = len(c["word"]) // 3
        wrot = [tuple(w) for w in c["word"][mrot:] + c["word"][:mrot]]
        ev2 = build_ect(c["prefix"], wrot, head=[tuple(w) for w in c["word"][:mrot]])
        assert ev2["flow"] == ev["flow"] and ev2["nB"] == ev["nB"], "rotation variance"
        print("rotation-invariance: PASS (flow=%d)" % ev2["flow"], flush=True)
        res = {"flow": ev["flow"], "nB": ev["nB"], "deficient": ev["flow"] < ev["nB"]}
        if ev["flow"] < ev["nB"]:
            best = None
            for bi in range(ev["nB"]):
                chk = verify_cut(ev, {bi})
                if chk["deficient"] and (best is None or chk["|S|"] > best["|S|"]):
                    best = chk
            res["singleton_cut"] = best
            S = set(range(ev["nB"]))
            res["all_cut"] = verify_cut(ev, S)
        out[tag] = res
    json.dump(out, open(RDIR / 'DIRECT_CWC_U1_gap_flow_or_cut_results.json', 'w'), indent=1,
              default=str)
    print("done", flush=True)

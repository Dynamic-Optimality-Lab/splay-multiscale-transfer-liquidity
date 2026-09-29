"""WP-6 STEP EF-00: nonduplicating event-flow reserve (causal DAG + capacity-3 flow).

NODES: A-StepEvs (source cap 3 if sited else 0) + B-StepEvs (demand 1).
EDGES (structural, past-only, tight-first):
  E1 same-access: all A-StepEvs of access t -> all B-StepEvs of access t
     (A-part precedes B-part intra-access; same splay intent).
  E2 pump-ancestry: A-StepEvs of past KEEPs u that PUSHED z (M1-traced p/g
     sets) with u strictly after z's last KEEP (reset destroys stale depth).
  E4 setup-adoption: A-StepEvs of z's setup access (last A-root-arrival,
     A-tracked) -> z's B-StepEvs (covers genesis-depth via same-shape replay).
NO E3-overlap initially (refine via min-cut only). NO chronological matching.
TEST: max-flow saturates all B-demand on full history + every prefix?
FAIL => min-cut: deficient B-set + saturated A-neighborhood + classify
  (capacity-short vs eligibility-gap; epoch-pooling/nested/same-access/
   merge-split/genuine).
First corpus: psi-anatomy duplication witnesses (tight histories re-seeded).
"""
from __future__ import annotations
import sys
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from liquidity import legacy_embedding as PE
from solver import encode as E


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


class Dinic:
    def __init__(self, n):
        self.n = n
        self.adj = [[] for _ in range(n)]

    def add(self, u, v, c):
        self.adj[u].append([v, c, len(self.adj[v])])
        self.adj[v].append([u, 0, len(self.adj[u]) - 1])

    def flow(self, s, t):
        n = self.n
        F = 0
        INF = 10 ** 18
        while True:
            lv = [-1] * n
            lv[s] = 0
            dq = deque([s])
            while dq:
                u = dq.popleft()
                for v, c, _ in self.adj[u]:
                    if c > 0 and lv[v] < 0:
                        lv[v] = lv[u] + 1
                        dq.append(v)
            if lv[t] < 0:
                break
            it = [0] * n

            def dfs(u, f):
                if u == t:
                    return f
                i = it[u]
                while i < len(self.adj[u]):
                    v, c, rev = self.adj[u][i]
                    if c > 0 and lv[v] == lv[u] + 1:
                        r = dfs(v, min(f, c))
                        if r:
                            self.adj[u][i][1] -= r
                            self.adj[v][rev][1] += r
                            return r
                    i += 1
                    it[u] = i
                return 0

            while True:
                f = dfs(s, INF)
                if not f:
                    break
                F += f
        return F, lv


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


def root_key(t):
    r = t
    while r["p"] is not None:
        r = r["p"]
    return r["k"]


def splay_A(A, x):
    """Replay A-splay capturing rotated sets per StepEv; return (root, [sets])."""
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
            inv.append({node["k"], p["k"]})
        elif p["l"] is node and g["l"] is p:
            PE._rot_right(g)
            PE._rot_right(p)
            inv.append({node["k"], p["k"], g["k"]})
        elif p["r"] is node and g["r"] is p:
            PE._rot_left(g)
            PE._rot_left(p)
            inv.append({node["k"], p["k"], g["k"]})
        elif p["r"] is node and g["l"] is p:
            PE._rot_left(p)
            PE._rot_right(g)
            inv.append({node["k"], p["k"], g["k"]})
        else:
            PE._rot_right(p)
            PE._rot_left(g)
            inv.append({node["k"], p["k"], g["k"]})
    while node["p"] is not None:
        node = node["p"]
    return node, inv


def splay_B_push(B, x):
    """Replay B-splay capturing pushed-key sets per StepEv; return (root, [sets])."""
    d, path = PE._depth_to(B, x)
    if not path or path[-1]["k"] != x:
        return B, []
    out = []
    node = path[-1]
    while node["p"] is not None:
        p = node["p"]
        g = p["p"]
        if g is None:
            if p["l"] is node:
                PE._rot_right(p)
            else:
                PE._rot_left(p)
            out.append({p["k"]})
        elif p["l"] is node and g["l"] is p:
            PE._rot_right(g)
            PE._rot_right(p)
            out.append({p["k"], g["k"]})
        elif p["r"] is node and g["r"] is p:
            PE._rot_left(g)
            PE._rot_left(p)
            out.append({p["k"], g["k"]})
        elif p["r"] is node and g["l"] is p:
            PE._rot_left(p)
            PE._rot_right(g)
            out.append({p["k"], g["k"]})
        else:
            PE._rot_right(p)
            PE._rot_left(g)
            out.append({p["k"], g["k"]})
    while node["p"] is not None:
        node = node["p"]
    return node, out


def build_flow(n, T0, H, upto=None):
    """Build DAG + flow data for prefix H[:upto]. Returns dict."""
    pre = E.precompute(n, T0, H if upto is None else H[:upto])
    A, B = to_ptr(T0), to_ptr(T0)
    Aevs = []  # (acc_idx, sited)
    Bevs = []  # (acc_idx,)
    accA = {}  # acc_idx -> [aev ids]
    accB = {}  # acc_idx -> [bev ids]
    pump_push = {}  # acc_idx(KEEP) -> {pushed key: True} (union over its B-Steps)
    setup = {}  # key -> acc_idx of last root-arrival (non-root-before)
    setups = []  # per-access snapshot AFTER that access (causal E4: no future leak)
    lastkeep = {}  # key -> acc_idx of last KEEP
    for idx, acc in enumerate(pre):
        mode, xx = acc["mode"], acc["x"]
        r_before = root_key(A)
        nonroot_before = (r_before != xx)
        A, _ = splay_A(A, xx)
        ids = []
        for sited in acc["sites"]:
            ids.append(len(Aevs))
            Aevs.append((idx, bool(sited)))
        accA[idx] = ids
        if nonroot_before:
            setup[xx] = idx
        setups.append(dict(setup))
        if mode == "KEEP":
            B, pushes = splay_B_push(B, xx)
            s = set()
            for P in pushes:
                s |= P
            pump_push[idx] = s
            ids = list(range(len(Bevs), len(Bevs) + len(acc["Bev"])))
            Bevs.extend([(idx,)] * len(acc["Bev"]))
            accB[idx] = ids
            lastkeep[xx] = idx
    # pump ancestry per B-event: pump-KEEPs u in (prev KEEP of z, idx) pushing z.
    # prevk snapshot per acc_idx (all Bevs of one KEEP share it).
    prevkeep = {}
    lk2 = {}
    for idx, acc in enumerate(pre):
        if acc["mode"] == "KEEP":
            prevkeep[idx] = lk2.get(acc["x"], -1)
            lk2[acc["x"]] = idx
    b_elig = []  # per bev id: set of aev ids
    for bi, (idx,) in enumerate(Bevs):
        xx = pre[idx]["x"]
        elig = set(accA[idx])  # E1 same-access
        _setup_at = setups[idx]  # causal snapshot (no future leak)
        if xx in _setup_at and _setup_at[xx] != idx:
            elig |= set(accA[_setup_at[xx]])  # E4 (strictly-past setup)
        # E2: pumps after z's previous KEEP (exclusive) strictly before idx
        prevk = prevkeep[idx]
        for u in range(prevk + 1, idx):
            if pre[u]["mode"] == "KEEP" and xx in pump_push.get(u, set()):
                elig |= set(accA[u])
        b_elig.append(elig)
    return {"Aevs": Aevs, "Bevs": Bevs, "elig": b_elig, "pre": pre}


def maxflow_sat(g):
    Aevs, Bevs, elig = g["Aevs"], g["Bevs"], g["elig"]
    na, nb = len(Aevs), len(Bevs)
    N = 2 + na + nb
    S, T = 0, N - 1
    D = Dinic(N)
    for i, (_, sited) in enumerate(Aevs):
        if sited:
            D.add(S, 1 + i, 3)
    for j in range(nb):
        D.add(1 + na + j, T, 1)
    for j, es in enumerate(elig):
        for i in es:
            if Aevs[i][1]:
                D.add(1 + i, 1 + na + j, 1)
    f, _ = D.flow(S, T)
    return f, nb


def main() -> int:
    # WP-6 STEP EF-00: event-flow test, duplication corpses first.
    step("EF-00", "Nonduplicating event-flow reserve test")
    import hashlib
    import json

    class DRBG:
        def __init__(self, s): self.s = s; self.c = 0

        def b(self):
            self.c += 1
            return hashlib.sha256(b"ef|%s|%d" % (self.s, self.c)).digest()

        def below(self, n):
            bound = (1 << 256) - ((1 << 256) % n)
            while True:
                v = int.from_bytes(self.b(), "big")
                if v < bound:
                    return v % n

        def ir(self, a, b): return a + self.below(b - a + 1)

        def ch(self, s): return s[self.below(len(s))]

    def vine(n, left=False):
        t = None
        for k in (range(n, 0, -1) if not left else range(1, n + 1)):
            t = [k, None, t] if not left else [k, t, None]
        return t

    # duplication-corpses: same seeds/shapes as psi-anatomy (ps|t) n<=64
    full_ok = pre_ok = 0
    full_bad = pre_bad = 0
    worst_short = 0
    ex_short = None
    neigh_hist = []
    n_hist = 0
    for t in range(120):
        rng = DRBG(("ps%d" % t).encode())
        n = rng.ch([16, 32, 64])
        T0 = vine(n, rng.below(2) == 0)
        L = rng.ir(4, 18)
        x = rng.ir(1, n)
        H = []
        for i in range(L):
            if i % 4 == 3:
                y = rng.ir(1, n)
                H.append(["DELETE", y if y != x else (1 if x != 1 else n)])
            else:
                H.append([rng.ch(["KEEP", "DELETE", "DELETE", "KEEP"]), x])
            x = min(n, max(1, x + rng.ch([-16, -8, -4, -1, 1, 4, 8, 16])))
        pre = E.precompute(n, T0, H)
        res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
        if res["violations"]:
            step("EF-KILL", "present kill t=%d (refutes MSTL-14P!)" % t)
            return 2
        g = build_flow(n, T0, H)
        f, nb = maxflow_sat(g)
        if nb == 0:
            full_ok += 1
        elif f >= nb:
            full_ok += 1
        else:
            full_bad += 1
            if nb - f > worst_short:
                worst_short, ex_short = nb - f, (t, nb, f)
        # prefix saturation: every KEEP-prefix
        for upto in range(1, len(H) + 1):
            if H[upto - 1][0] != "KEEP":
                continue
            gp = build_flow(n, T0, H, upto=upto)
            fp, nbp = maxflow_sat(gp)
            if nbp == 0 or fp >= nbp:
                pre_ok += 1
            else:
                pre_bad += 1
                if nbp - fp > worst_short:
                    worst_short, ex_short = nbp - fp, (t, upto, nbp, fp)
        # neighborhood sizes (eligible-A per B)
        for es in g["elig"]:
            neigh_hist.append(len(es))
        n_hist += 1
    import statistics
    step("EF-01", "hist=%d full: ok=%d bad=%d; prefix: ok=%d bad=%d; worst shortfall=%d %s"
         % (n_hist, full_ok, full_bad, pre_ok, pre_bad, worst_short, ex_short))
    step("EF-01", "eligible-A per B: min=%d med=%s max=%d"
         % (min(neigh_hist), statistics.median(neigh_hist), max(neigh_hist)))
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "eventflow.json").write_text(
        json.dumps({"histories": n_hist, "full_ok": full_ok, "full_bad": full_bad,
                    "pre_ok": pre_ok, "pre_bad": pre_bad,
                    "worst_shortfall": worst_short, "ex": ex_short,
                    "neigh_min": min(neigh_hist),
                    "neigh_med": statistics.median(neigh_hist),
                    "neigh_max": max(neigh_hist)},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

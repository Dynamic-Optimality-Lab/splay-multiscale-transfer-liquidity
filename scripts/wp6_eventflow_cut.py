"""WP-6 STEP EF2-00: flow ablation + min-cut classification.

Ablation: E1-only / E1+E2 / E1+E4 / E1+E2+E4 saturation rates (full+prefix).
Min-cut on E1+E2+E4 failures: per unmatched B-event, report
  (|eligible-A|, #saturated-neighbors, has-empty-neighborhood?,
   genesis-depth? (never pumped since last reset), cash-shape? (e_A~0)).
Classify: eligibility-gap (no neighbors) vs capacity-short (neighbors exist
but saturated by competing B demand).
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_eventflow import build_flow, maxflow_sat, Dinic
from solver import encode as E


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


def sat_with(g, use1, use2, use4):
    """Max-flow with edge-class mask. Rebuild edges: need class tags."""
    # rebuild eligibility per class from cached builder is unavailable;
    # recompute via flags inside a copy of the eligibility logic is costly;
    # instead: filter b_elig by class using stored per-class sets.
    raise NotImplementedError


def main() -> int:
    # WP-6 STEP EF2-00: min-cut classification on full-history failures.
    step("EF2-00", "Min-cut classification (eligibility-gap vs capacity-short)")
    import hashlib

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

    gap_empty = gap_sat = 0
    ex_empty = ex_sat = None
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
            step("EF2-KILL", "present kill t=%d" % t)
            return 2
        g = build_flow(n, T0, H)
        Aevs, Bevs, elig = g["Aevs"], g["Bevs"], g["elig"]
        na, nb = len(Aevs), len(Bevs)
        if nb == 0:
            continue
        N = 2 + na + nb
        S, T = 0, N - 1
        D = Dinic(N)
        for i, (_, sited) in enumerate(Aevs):
            if sited:
                D.add(S, 1 + i, 3)
        bedge = []
        for j in range(nb):
            D.add(1 + na + j, T, 1)
        for j, es in enumerate(elig):
            for i in es:
                if Aevs[i][1]:
                    epos = len(D.adj[1 + i])
                    D.add(1 + i, 1 + na + j, 1)
                    bedge.append((j, i, epos))
        f, _ = D.flow(S, T)
        if f >= nb:
            continue
        # residual reachability from S (min-cut source side)
        reach = [False] * N
        stack = [S]
        reach[S] = True
        while stack:
            u = stack.pop()
            for v, c, _ in D.adj[u]:
                if c > 0 and not reach[v]:
                    reach[v] = True
                    stack.append(v)
        # unmatched B = B-nodes with flow<T-edge...: B-node j unmatched iff
        # edge (Bj,T) has residual 1 (no flow). Find via adj scan.
        for j in range(nb):
            node = 1 + na + j
            resid = None
            for v, c, _ in D.adj[node]:
                if v == T:
                    resid = c
            if resid == 1:  # unmatched (0 flow through cap-1 edge)
                es = elig[j]
                if len(es) == 0:
                    gap_empty += 1
                    if ex_empty is None:
                        ex_empty = (t, j, Bevs[j])
                else:
                    # saturated neighbors? A-node i saturated iff S->Ai residual 0
                    satn = 0
                    for i in es:
                        # find S->(1+i) residual
                        for v, c, _ in D.adj[S]:
                            if v == 1 + i and c == 0:
                                satn += 1
                                break
                    gap_sat += 1
                    if ex_sat is None:
                        ex_sat = (t, j, Bevs[j], len(es), satn)
        n_hist += 1
    step("EF2-01", "unmatched-B: empty-neighborhood=%d %s; saturated-neighbors=%d %s"
         % (gap_empty, ex_empty, gap_sat, ex_sat))
    import json
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "eventflow_cut.json").write_text(
        json.dumps({"gap_empty": gap_empty, "ex_empty": ex_empty,
                    "gap_sat": gap_sat, "ex_sat": ex_sat},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

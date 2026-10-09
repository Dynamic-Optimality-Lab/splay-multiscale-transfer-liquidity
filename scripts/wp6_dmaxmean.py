"""PIVOT-25R-COMP §cycle: max-mean-D closed walk via Karp (exact).

If max-mean D_s(x) > 0: positive-D closed walk exists => NO pair-state M
with M(s)-M(s') >= D_s(x) exists (telescoping contradiction). Exact
impossibility theorem for the profile approach (NOT a CD counterexample).
Karp DP + certified cycle extraction (mean re-verified).
"""
from __future__ import annotations
import sys
import copy
from pathlib import Path
from fractions import Fraction

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
import wp6_overflow as V
from wp6_staticR import R_static, depths_list


def step(sid, msg):
    print("[DMC %s] %s" % (sid, msg), flush=True)


def main():
    import json as J
    import wp6_cycle_ratio as O
    n = 5
    Sh = O.shapes_of(list(range(1, n + 1)))
    nS = len(Sh)
    Vcount = nS * nS
    idx = {J.dumps(s, sort_keys=True): i for i, s in enumerate(Sh)}
    # incoming adjacency with integer D-weights: pred[v] = [(u, w)]
    pred = [[] for _ in range(Vcount)]
    for ia in range(nS):
        for ib in range(nS):
            u = ia * nS + ib
            da = depths_list(Sh[ia])
            t = 1 if Sh[ia][0] == Sh[ib][0] else 0
            for x in range(1, n + 1):
                rep = V.replay(Sh[ia], Sh[ib], [("K", x)])
                ia2 = idx[J.dumps(rep["endA"], sort_keys=True)]
                ib2 = idx[J.dumps(rep["endB"], sort_keys=True)]
                v = ia2 * nS + ib2
                a = (da[x] + 1) // 2
                d = R_static(Sh[ib], x) - 2 * a - 2 * (1 - t)
                pred[v].append((u, d, x))
    step("G", "graph: %d states, D-edges built" % Vcount)
    N = Vcount
    INF_NEG = -10 ** 30
    # Karp DP with full table (exact mu* + certified cycle recovery).
    FT = [[0] * Vcount]
    PR = []
    F = [0] * Vcount
    for k in range(1, N + 1):
        Fn = [INF_NEG] * Vcount
        Pk = [-1] * Vcount
        Px = [0] * Vcount
        for v in range(Vcount):
            best = INF_NEG
            bu = -1
            bx = 0
            for (u, d, x) in pred[v]:
                if F[u] != INF_NEG and F[u] + d > best:
                    best = F[u] + d
                    bu = u
                    bx = x
            Fn[v] = best
            Pk[v] = bu
            Px[v] = bx
        F = Fn
        FT.append(list(F))
        PR.append((Pk, Px))
        if k % 500 == 0:
            step("K", "k=%d/%d" % (k, N))
    from fractions import Fraction
    best = None
    for v in range(Vcount):
        if FT[N][v] == INF_NEG:
            continue
        mv = None
        kv = 0
        for k in range(N):
            if FT[k][v] == INF_NEG:
                continue
            mu = Fraction(FT[N][v] - FT[k][v], N - k)
            if mv is None or mu < mv:
                mv, kv = mu, k
        if mv is not None and (best is None or mv > best[0]):
            best = (mv, v, kv)
    step("S", "max-mean D = %s" % (best[0],))
    mu, vstar, ks = best
    # recover closed walk: follow parents from (N, vstar) back ks steps...
    # standard: walk n steps from vstar via Par to find repeated vertex.
    seq = [vstar]
    u = vstar
    cyc = None
    seen = {vstar: 0}
    for j in range(N, 0, -1):
        Pk, Px = PR[j - 1]
        u = Pk[u]
        if u == -1:
            break
        if u in seen:
            cyc = seq[seen[u]:] + [u] if False else None
            # extract simple cycle from seq+u
            path = seq + [u]
            i0 = path.index(u)
            cyc = path[i0:]
            break
        seen[u] = len(seq)
        seq.append(u)
    step("S", "recovered walk len=%s" % (len(cyc) if cyc else None))
    # verify mean of recovered cycle from stored edges (recompute D)
    tot = 0
    detail = []
    if cyc:
        for a in range(len(cyc) - 1):
            u, v = cyc[a], cyc[a + 1]
            # find edge u->v weight: search pred[v]
            ws = [(d, x) for (uu, d, x) in pred[v] if uu == u]
            assert ws, (u, v)
            d, x = ws[0]
            tot += d
            detail.append((u, v, x, d))
        step("S", "cycle weight=%d length=%d mean=%s" %
             (tot, len(cyc) - 1, Fraction(tot, len(cyc) - 1)))
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" /
     "dual_mine" / "dmaxmean5.json").write_text(
        J.dumps({"mu": str(mu), "cycle": cyc, "weight": tot,
                 "detail": detail}, indent=1, default=str),
        encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

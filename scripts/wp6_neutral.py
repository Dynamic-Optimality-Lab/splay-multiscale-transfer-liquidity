"""WP-6 STEP NQ-00: neutral quotient + setup-cost law mining.

1. Neutral SCCs: strongly connected components over ZERO-reward edges
   (r==0 transitions) on exact n=6 pair graph. Size distribution, V const
   on components?, states covered.
2. Tight-path profiles: Bellman-optimal paths from diagonals (follow tight
   edges); per path: length, max drawdown (setup depth-­‐min cumulative),
   max single cash, cash vs preceding-drawdown (setup-cost law candidate:
   cash <= drawdown?); never-positive check (tight paths stay <=0?).
3. Edge-type census on tight paths: SETUP (r<=0, V rises?) / NEUTRAL (r=0?)
   / CASH (r>0) fractions + mode transitions (CASH->CASH without SETUP?).
"""
from __future__ import annotations
import sys
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_splaymetric import shapes, splay_cost_events


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


def main() -> int:
    # WP-6 STEP NQ-00.
    step("NQ-00", "Neutral quotient + setup-cost mining")
    import json
    n = 6
    S = shapes(n)
    nxt, cst = {}, {}
    for t in S:
        for x in range(1, n + 1):
            t2, c = splay_cost_events(t, x)
            nxt[(t, x)] = t2
            cst[(t, x)] = c
    seen = set()
    dq = deque()
    for t0 in S:
        seen.add((t0, t0))
        dq.append((t0, t0))
    trans = {}
    while dq:
        A, B = dq.popleft()
        lst = []
        for x in range(1, n + 1):
            A2 = nxt[(A, x)]
            eA = cst[(A, x)]
            s = (A2, B)
            if s not in seen:
                seen.add(s)
                dq.append(s)
            lst.append(("D", x, eA, 0, -3 * eA, s))
            B2 = nxt[(B, x)]
            eB = cst[(B, x)]
            s = (A2, B2)
            if s not in seen:
                seen.add(s)
                dq.append(s)
            lst.append(("K", x, eA, eB, eB - 3 * eA, s))
        trans[(A, B)] = lst
    nodes = list(seen)
    # Bellman V
    V = {v: 0 for v in nodes}
    for _ in range(600):
        changed = False
        Vn = {}
        for v in nodes:
            best = 0
            for (_, _, _, _, r, s) in trans[v]:
                q = r + V[s]
                if q > best:
                    best = q
            Vn[v] = best
            if best != V[v]:
                changed = True
        V = Vn
        if not changed:
            break
    # 1. zero-reward SCCs (Tarjan-lite via Kosaraju on r==0 edges)
    zadj = {v: [] for v in nodes}
    zrev = {v: [] for v in nodes}
    for v in nodes:
        for (_, _, _, _, r, s) in trans[v]:
            if r == 0:
                zadj[v].append(s)
                zrev[s].append(v)
    visited = set()
    order = []

    def dfs1(v):
        visited.add(v)
        for w in zadj[v]:
            if w not in visited:
                dfs1(w)
        order.append(v)

    sys.setrecursionlimit(100000)
    for v in nodes:
        if v not in visited:
            dfs1(v)
    comp = {}
    cid = 0

    def dfs2(v, c):
        comp[v] = c
        for w in zrev[v]:
            if w not in comp:
                dfs2(w, c)

    for v in reversed(order):
        if v not in comp:
            dfs2(v, cid)
            cid += 1
    import statistics as _st
    sizes = {}
    for v, c in comp.items():
        sizes[c] = sizes.get(c, 0) + 1
    sz = list(sizes.values())
    # V const per component?
    vrange = {}
    for v, c in comp.items():
        lo, hi = vrange.get(c, (V[v], V[v]))
        vrange[c] = (min(lo, V[v]), max(hi, V[v]))
    nonconst = sum(1 for (lo, hi) in vrange.values() if hi > lo)
    step("NQ-01", "zero-SCCs=%d sizes max=%d med=%s V-nonconst-comps=%d" %
         (cid, max(sz), _st.median(sz), nonconst))
    # 2-3. tight paths from diagonals: setup-depth vs cash
    dg = [v for v in nodes if v[0] == v[1]]
    npaths = 0
    viol_pos = 0
    cash_vs_draw = []
    type_counts = {"SETUP": 0, "NEUTRAL": 0, "CASH": 0}
    cash_after_cash = 0
    for d in dg:
        if V[d] <= 0:
            continue
        # follow tight edges greedily (lexicographically first)
        cur = d
        cum = 0
        mindraw = 0
        seenp = set()
        prev_cash = False
        while cur not in seenp and len(seenp) < 200:
            seenp.add(cur)
            na = None
            for (m, x, eA, eB, r, s) in trans[cur]:
                if r + V[s] == V[cur] and V[cur] > 0:
                    na = (m, x, eA, eB, r, s)
                    break
            if na is None:
                break
            m, x, eA, eB, r, s = na
            cum += r
            if cum > 0:
                viol_pos += 1
                break
            if cum < mindraw:
                mindraw = cum
            if r > 0:
                type_counts["CASH"] += 1
                cash_vs_draw.append((r, -mindraw))
                if prev_cash:
                    cash_after_cash += 1
                prev_cash = True
            elif r == 0:
                type_counts["NEUTRAL"] += 1
                prev_cash = False
            else:
                type_counts["SETUP"] += 1
                prev_cash = False
            cur = s
        npaths += 1
    step("NQ-02", "tightdiag=%d viol_pos_cum=%d types=%s cash_after_cash=%d" %
         (npaths, viol_pos, type_counts, cash_after_cash))
    worst_ratio = -1.0
    exr = None
    for (c, d) in cash_vs_draw:
        # cash vs preceding drawdown: want c <= d (setup covers cash)?
        if d >= 0:
            rto = float("inf") if c > 0 else 0.0
        else:
            rto = c / (-d)
        if rto > worst_ratio:
            worst_ratio, exr = rto, (c, d)
    step("NQ-03", "cash/drawdown worst=%.3f %s (want<=1); n=%d" %
         (worst_ratio, exr, len(cash_vs_draw)))
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "neutral.json").write_text(
        json.dumps({"n": n, "pairs": len(nodes), "zero_sccs": cid,
                    "scc_max": max(sz), "scc_med": _st.median(sz),
                    "V_nonconst": nonconst, "tightdiag": npaths,
                    "viol_pos": viol_pos, "types": type_counts,
                    "cash_after_cash": cash_after_cash,
                    "cash_drawdown_worst": worst_ratio, "ex": exr},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

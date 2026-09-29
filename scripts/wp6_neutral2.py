"""WP-6 STEP NQ2-00: tight-path grammar from V>0 states (cash adjacency?).

From top-V>0 states (n=6, exact V): follow tight edges; record edge-type
sequences (SETUP r<0 / NEUTRAL r=0 / CASH r>0); cash-after-cash adjacency
(can positives chain adjacently, or must setup/neutral intervene?);
cash vs max-preceding-drawdown (setup-cost law on paths); cumulative<=V0?
Also mixed zero-total cycle anatomy: positives inside zero cycles always
preceded (within cycle) by offsetting negatives?
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
    # WP-6 STEP NQ2-00.
    step("NQ2-00", "Tight-path grammar (cash adjacency?)")
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
    top = sorted([v for v in nodes if V[v] > 0], key=lambda v: -V[v])[:40]
    adj_cash = 0
    tot_cash = 0
    worst_cd = -1.0
    ex_cd = None
    seqs = []
    for d in top:
        cur = d
        cum = 0
        mindraw = 0
        prev = None
        seenp = set()
        seq = []
        while cur not in seenp and len(seenp) < 100:
            seenp.add(cur)
            na = None
            for (m, x, eA, eB, r, s) in trans[cur]:
                if s == cur and r == 0:
                    continue  # no-op self-loop: degenerate stutter, skip
                if r + V[s] == V[cur] and V[cur] > 0:
                    na = (m, x, eA, eB, r, s)
                    break
            if na is None:
                # only self-loop stutter remains: record and stop
                seq.append("n")
                break
            m, x, eA, eB, r, s = na
            seq.append("C" if r > 0 else ("N" if r == 0 else "S"))
            cum += r
            if cum < mindraw:
                mindraw = cum
            if r > 0:
                tot_cash += 1
                if prev == "C":
                    adj_cash += 1
                if mindraw < 0 and r / (-mindraw) > worst_cd:
                    worst_cd, ex_cd = r / (-mindraw), (str(d), r, mindraw)
                prev = "C"
            elif r == 0:
                prev = "N"
            else:
                prev = "S"
            cur = s
        seqs.append("".join(seq))
    import collections
    step("NQ2-01", "paths=%d cash=%d adj_cash_cash=%d worst cash/draw=%.3f %s" %
         (len(top), tot_cash, adj_cash, worst_cd, str(ex_cd)[:120]))
    step("NQ2-02", "seq counter: %s" % collections.Counter(seqs).most_common(8))
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "neutral2.json").write_text(
        json.dumps({"paths": len(top), "cash": tot_cash, "adj_cash": adj_cash,
                    "worst_cd": worst_cd, "ex": ex_cd,
                    "seqs": collections.Counter(seqs).most_common(8)},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

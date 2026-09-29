"""WP-6 STEP RK-00: tight-positive transition anatomy (rank mining).

For EVERY Bellman-tight positive-reward KEEP on exact n=5,6 pair graphs,
record pre/post deltas of candidate rank quantities:
  V, maxAccessReward (max_a r), hazKeys (#y w/ cB-3cA>0), maxHaz (H1),
  divKeys (#v w/ subtree-disagree), maxBdepth, sumBdepth( const check),
  splitSizes (|L|,|R| post common-root), pathLens (B/A depth of x pre),
  V_after, tightness (V_b == q + V_a?).
Find quantities with ALWAYS-<=0 (strict<0?) deltas => rank candidates.
Quantities that ever rise are dead as ranks (record max rise).
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


def depths(t):
    out = {}

    def rec(u, d):
        if u is None:
            return
        out[u[0]] = d
        rec(u[1], d + 1)
        rec(u[2], d + 1)

    rec(t, 0)
    return out


def subtuples(t):
    """Map key -> subtree key-set."""
    out = {}

    def rec(u):
        if u is None:
            return set()
        s = {u[0]} | rec(u[1]) | rec(u[2])
        out[u[0]] = s
        return s

    rec(t)
    return out


def main() -> int:
    # WP-6 STEP RK-00.
    step("RK-00", "Tight-positive anatomy (rank mining)")
    import json
    out = {}
    for n in (5, 6):
        S = shapes(n)
        nxt, cst = {}, {}
        for t in S:
            for x in range(1, n + 1):
                t2, c = splay_cost_events(t, x)
                nxt[(t, x)] = t2
                cst[(t, x)] = c
        # reachable pairs + transitions (reuse pattern)
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
        # Bellman V (value iteration, exact)
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

        def anat(A, B):
            dA, dB = depths(A), depths(B)
            # one-step access rewards
            mx = -10**18
            for x in range(1, n + 1):
                # e for access x from THIS state: need costs (use cst on trees)
                r = cst[(B, x)] - 3 * cst[(A, x)]
                if r > mx:
                    mx = r
            # haz keys + maxHaz
            hk = 0
            mh = 0
            for y in range(1, n + 1):
                # c(A,y): steps to splay y from A: need per-key costs.
                # cst[(T,y)] IS c(T,y) (StepEvs from T!). Reuse table.
                g = cst[(B, y)] - 3 * cst[(A, y)]
                if g > 0:
                    hk += 1
                if g > mh:
                    mh = g
            # div keys (subtree-disagree)
            sA, sB = subtuples(A), subtuples(B)
            dk = sum(1 for k in range(1, n + 1) if sA[k] != sB[k])
            mb = max(dB.values())
            return {"maxAcc": mx, "hazKeys": hk, "maxHaz": mh,
                    "divKeys": dk, "maxBdepth": mb, "V": V[(A, B)]}

        # deltas over tight positive KEEPs
        drops = {}
        rises = {}
        npos = 0
        exmax = {}
        for v in nodes:
            A, B = v
            for (m, x, eA, eB, r, s) in trans[v]:
                if m != "K" or r <= 0:
                    continue
                if r + V[s] != V[v]:
                    continue  # not tight
                npos += 1
                a0 = anat(A, B)
                a1 = anat(s[0], s[1])
                for k in a0:
                    if k == "V":
                        continue
                    d = a1[k] - a0[k] if k in a1 else None
                    if d is None:
                        continue
                    drops.setdefault(k, 0)
                    rises.setdefault(k, 0)
                    if d <= 0:
                        pass
                    else:
                        rises[k] += 1
                        if d > exmax.get(k, -10**18):
                            exmax[k] = d
                # V tightness check
                if V[v] != r + V[s]:
                    step("RK-ERR", "not tight?")
                    return 2
        step("RK-n%d" % n, "tightPos=%d rises=%s exmax=%s" % (npos, rises, exmax))
        out[str(n)] = {"tightPos": npos, "rises": rises, "exmax": exmax}
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "rankmine.json").write_text(
        json.dumps(out, indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

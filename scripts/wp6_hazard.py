"""WP-6 STEP HZ-00: hazard laws + vector LP (exact, n<=7).

H(A,B) = max_y max(0, c(B,y)-3*c(A,y)) [c = StepEv splay cost].
LAW-D (DELETE x): H(S_xA,B)-H(A,B) <= 3*c(A,x).
LAW-K (KEEP x): c(B,x)-3*c(A,x) + H(S_xA,S_xB)-H(A,B) <= 0.
Exhaustive over reachable pairs (all pairs, n<=7 per SM2).
Vector LP (SEC11C): Phi = a*Df + b*Dr (Df=Delta(B,A), Dr=Delta(A,B));
solve exact feasible (a,b) with a,b>=0 over all reachable transitions
(DELETE: a*dDf+b*dDr <= 3*e_A; KEEP: e_B + a*dDf+b*dDr <= 3*e_A).
LP over polygon vertices (intersect half-planes exactly via Fractions).
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_splaymetric import shapes, splay_cost_events


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


def main() -> int:
    # WP-6 STEP HZ-00.
    step("HZ-00", "Hazard laws + vector LP")
    import json
    from fractions import Fraction
    import heapq
    out = {}
    for n in (5, 6, 7):
        S = shapes(n)
        nxt, cst = {}, {}
        for t in S:
            for x in range(1, n + 1):
                t2, c = splay_cost_events(t, x)
                nxt[(t, x)] = t2
                cst[(t, x)] = c
        # Dijkstra Delta (forward star only needed? need all-pairs: reuse)
        INF = 10 ** 18
        Delta = {}
        for s in S:
            dist = {s: 0}
            pq = [(0, s)]
            while pq:
                d, u = heapq.heappop(pq)
                if d > dist[u]:
                    continue
                for x in range(1, n + 1):
                    v = nxt[(u, x)]
                    nd = d + cst[(u, x)]
                    if nd < dist.get(v, INF):
                        dist[v] = nd
                        heapq.heappush(pq, (nd, v))
            for t2, dd in dist.items():
                Delta[(s, t2)] = dd
        # hazard + laws + vector constraints over all pairs
        wD = -10**18
        wK = -10**18
        exD = exK = None
        # vector LP: a,b>=0; constraints p*a+q*b<=r. Feasible polytope.
        # Start box [0,3]x[0,3]; cut by half-planes (Sutherland-Hodgman exact).
        poly = [(Fraction(0), Fraction(0)), (Fraction(3), Fraction(0)),
                (Fraction(3), Fraction(3)), (Fraction(0), Fraction(3))]
        feasible = True

        def cut(poly, P, Q, R):
            # keep P*a+Q*b<=R
            if not poly:
                return poly
            res = []
            m = len(poly)
            for i in range(m):
                A = poly[i]
                B = poly[(i + 1) % m]
                vA = P * A[0] + Q * A[1] - R
                vB = P * B[0] + Q * B[1] - R
                if vA <= 0:
                    res.append(A)
                if (vA <= 0) != (vB <= 0) and vA != vB:
                    t = vA / (vA - vB)
                    res.append((A[0] + t * (B[0] - A[0]), A[1] + t * (B[1] - A[1])))
            return res

        def Hcost(A, B):
            best = 0
            for y in range(1, n + 1):
                # c(B,y): steps to splay y from B; use nxt/cst via temp walk
                # cst keyed by (tree,key): need c(B,y), c(A,y)
                v = cst[(B, y)] - 0  # placeholder, replaced below
                _ = v
                bv = cst[(B, y)]
                av = cst[(A, y)]
                g = bv - 3 * av
                if g > best:
                    best = g
            return best

        for A in S:
            for B in S:
                h0 = Hcost(A, B)
                df0 = Delta.get((B, A), None)
                dr0 = Delta.get((A, B), None)
                for x in range(1, n + 1):
                    Ap = nxt[(A, x)]
                    Bp = nxt[(B, x)]
                    eA, eB = cst[(A, x)], cst[(B, x)]
                    # DELETE laws
                    h1 = Hcost(Ap, B)
                    g = (h1 - h0) - 3 * eA
                    if g > wD:
                        wD, exD = g, (str(A), str(B), x, eA, h0, h1)
                    # KEEP laws
                    h2 = Hcost(Ap, Bp)
                    g = (eB - 3 * eA) + (h2 - h0)
                    if g > wK:
                        wK, exK = g, (str(A), str(B), x, eA, eB, h0, h2)
                    # vector constraints (DELETE + KEEP), if Deltas exist
                    if df0 is not None and (Bp, Ap) in Delta and (Ap, Bp) in Delta:
                        dDf = Delta[(Bp, Ap)] - df0
                        dDr = Delta[(Ap, Bp)] - dr0
                        poly = cut(poly, dDf, dDr, 3 * eA)  # DELETE needs dDf only?
                        # NOTE: DELETE changes only A-side: Dr unchanged? Dr is
                        # Delta(A,B): A->Ap changes Dr too. Use full (dDf,dDr).
                        poly = cut(poly, dDf, dDr, 3 * eA - eB)  # KEEP form
                        # DELETE form: same with eB=0 and Bp=B:
                        dDfD = Delta[(B, Ap)] - df0 if (B, Ap) in Delta else None
                        dDrD = Delta[(Ap, B)] - dr0 if (Ap, B) in Delta else None
                        if dDfD is not None and dDrD is not None:
                            poly = cut(poly, dDfD, dDrD, 3 * eA)
                    if not poly:
                        feasible = False
                        break
                if not feasible:
                    break
            if not feasible:
                break
        step("HZ-n%d" % n, "LAW-D worst=%s LAW-K worst=%s vector feasible=%s poly=%s" %
             (wD, wK, feasible, [(float(a), float(b)) for (a, b) in poly][:6]))
        out[str(n)] = {"lawD": wD, "lawD_ex": exD, "lawK": wK, "lawK_ex": exK,
                       "vec_feasible": feasible,
                       "poly": [[str(a), str(b)] for (a, b) in poly]}
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hazard.json").write_text(
        json.dumps(out, indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

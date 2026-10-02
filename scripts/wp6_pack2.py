"""WP-6 PACK2: constructed root-miss + split killer (C105).

Hillclimb packing stuck at overlap 1 (local optimum?). CONSTRUCT instead:
Phase 1: simulate burst KEEP xc on current (A,B) to read burst-top-triple keys.
Phase 2: run activity restricted to keys whose A-rotated sets avoid those keys
   (verify per-access rotated sets disjoint from burst-top; count violations).
Phase 3: burst KEEP xc; test shortfall>0 => KILL, else record
   (overlap, split, N, eB) to demote-or-crown root-anchor.
Artifact: pack2.json (+hallkill on kill). Sealed files untouched.
"""
from __future__ import annotations
import sys
import copy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_hallcore import build_graph, maxflow_cap3
from wp6_tightest import vine, Rng
from wp6_eventflow import to_ptr, splay_A, splay_B_push


def step(sid, msg):
    print("[WP-6][PACK2 %s] %s" % (sid, msg), flush=True)


def main() -> int:
    import json
    step("P2-00", "constructed root-miss + split killer")
    TP = ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "pack2.json"
    rows = []
    kills = 0
    for s in range(60):
        rng = Rng(("q%d" % s).encode(), b"pack2")
        r = rng(0)
        n = [64, 128][r % 2]
        T0 = vine(n, (r >> 8) % 2 == 0)
        xc = n - (2 + (r >> 16) % 10)
        A, B = to_ptr(T0), to_ptr(T0)
        H = []
        # Phase 0: decouple + deepen B (steer split), tracking rotated sets
        for i in range(40):
            rr = Rng(("q%d" % s).encode(), b"qh%d" % i)
            q = rr(1000 + i)
            best = None
            for c in range(24):
                z = 1 + rr(2000 + c) % (n - 12)
                if abs(z - xc) <= 2:
                    continue
                for mode in ("KEEP", "DELETE"):
                    A2 = copy.deepcopy(A)
                    B2 = copy.deepcopy(B)
                    A2, invs = splay_A(A2, z)
                    if mode == "KEEP":
                        B2, _ = splay_B_push(B2, z)
                    # depth split proxy via precompute-free: use pointer depth
                    def dep(T, x):
                        st = [T]
                        nd = None
                        while st:
                            qq = st.pop()
                            if qq is None:
                                continue
                            if qq["k"] == x:
                                nd = qq
                                break
                            st.append(qq["l"])
                            st.append(qq["r"])
                        d = 0
                        while nd is not None and nd["p"] is not None:
                            nd = nd["p"]
                            d += 1
                        return d
                    sc = dep(B2, xc) - 3 * dep(A2, xc)
                    if best is None or sc > best[0]:
                        best = (sc, mode, z)
            _, mode, z = best
            H.append([mode, z])
            A, _ = splay_A(A, z)
            if mode == "KEEP":
                B, _ = splay_B_push(B, z)
        # Phase 1: read burst-top-triple keys (simulate)
        A3 = copy.deepcopy(A)
        B3 = copy.deepcopy(B)
        A3, _ = splay_A(A3, xc)
        B3, pushes = splay_B_push(B3, xc)
        btop = set(pushes[-1]) | {xc} if pushes else {xc}
        # Phase 2: confined activity (avoid btop in rotated sets), 20 steps
        viol = 0
        for i in range(20):
            rr = Rng(("q%d" % s).encode(), b"qc%d" % i)
            placed = False
            for c in range(40):
                z = 1 + rr(3000 + c) % (n - 12)
                if abs(z - xc) <= 2:
                    continue
                A2 = copy.deepcopy(A)
                A2, invs = splay_A(A2, z)
                keys = set()
                for S in invs:
                    keys |= set(S)
                if keys & btop:
                    continue
                mode = "KEEP" if rr(4000 + c) % 2 else "DELETE"
                H.append([mode, z])
                A, _ = splay_A(A, z)
                if mode == "KEEP":
                    B, _ = splay_B_push(B, z)
                placed = True
                break
            if not placed:
                viol += 1
                z = 1 + rr(5000) % (n - 12)
                H.append(["DELETE", z])
                A, _ = splay_A(A, z)
        # Phase 3: burst
        H.append(["KEEP", xc])
        G = build_graph(n, T0, H)
        if G is None:
            continue
        f, nb, _ = maxflow_cap3(G)
        if nb - f > 0:
            kills += 1
            step("P2-KILL", "HALL seed %d shortfall=%d" % (s, nb - f))
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json").write_text(
                json.dumps({"kill": True, "n": n, "H": H}, indent=1, default=str), encoding="utf-8")
            TP.write_text(json.dumps({"kill": True, "seed": s, "H": H}, indent=1, default=str),
                          encoding="utf-8")
            return 2
        # measure burst overlap/split/N
        from wp6_hallcore import delta_of
        from collections import defaultdict
        Bevs = G["Bevs"]
        last = max(b[0] for b in Bevs)
        Qb = [j for j in range(len(Bevs)) if Bevs[j][0] == last]
        d, N = delta_of(G, Qb)
        rows.append({"s": s, "eB": len(Qb), "N": len(N), "delta": d, "viol": viol,
                     "btop": sorted(btop)})
        if s % 15 == 14:
            step("P2-P", "s=%d eB=%d N=%d delta=%d viol=%d" % (s, len(Qb), len(N), d, viol))
    step("P2-01", "seeds=%d kills=%d mindelta=%s" % (
        len(rows), kills, min((r["delta"] for r in rows), default=None)))
    TP.write_text(json.dumps({"rows": rows, "kills": kills}, indent=1, default=str),
                  encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

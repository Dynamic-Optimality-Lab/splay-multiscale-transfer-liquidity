"""WP-6 STEER2: sealed ride-split scaling run (C65b). Faster greedy (subsampled
candidates, 60 steps, 40 seeds): per seed record (split, Adepth, Bdepth, e_B at
burst, |N| at burst, shortfall). Tests cover-scale-with-chain: |N| ~ e_B even at
split>100 (chain-crossing-touched-zone). Kill => hallkill exit 2.
Artifact: steer.json. Sealed files untouched.
"""
from __future__ import annotations
import sys
import copy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_hallcore import build_graph, maxflow_cap3, delta_of
from wp6_tightest import vine, Rng
from wp6_eventflow import to_ptr, splay_A, splay_B_push


def step(sid, msg):
    print("[WP-6][STEER2 %s] %s" % (sid, msg), flush=True)


from collections import defaultdict


def dep(T, x):
    st = [T]
    nd = None
    while st:
        q = st.pop()
        if q is None:
            continue
        if q["k"] == x:
            nd = q
            break
        st.append(q["l"])
        st.append(q["r"])
    d = 0
    while nd is not None and nd["p"] is not None:
        nd = nd["p"]
        d += 1
    return d


def main() -> int:
    import json
    step("S2-00", "sealed ride-split scaling")
    TP = ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "steer.json"
    rows = []
    kills = 0
    for s in range(40):
        rng = Rng(("t%d" % s).encode(), b"steer2")
        r = rng(0)
        n = [64, 128][r % 2]
        T0 = vine(n, (r >> 8) % 2 == 0)
        xc = n - (2 + (r >> 16) % 10)
        A, B = to_ptr(T0), to_ptr(T0)
        H = []
        for i in range(60):
            best = None
            # subsample 40 candidates far from x
            rr = Rng(("t%d" % s).encode(), b"c%d" % i)
            for c in range(40):
                z = 1 + rr(c) % n
                if abs(z - xc) <= 2:
                    continue
                for mode in ("KEEP", "DELETE"):
                    A2 = copy.deepcopy(A)
                    B2 = copy.deepcopy(B)
                    A2, _ = splay_A(A2, z)
                    if mode == "KEEP":
                        B2, _ = splay_B_push(B2, z)
                    sc = dep(B2, xc) - 3 * dep(A2, xc)
                    if best is None or sc > best[0]:
                        best = (sc, mode, z)
            _, mode, z = best
            H.append([mode, z])
            A, _ = splay_A(A, z)
            if mode == "KEEP":
                B, _ = splay_B_push(B, z)
        da, db = dep(A, xc), dep(B, xc)
        H.append(["KEEP", xc])
        G = build_graph(n, T0, H)
        if G is None:
            continue
        f, nb, _ = maxflow_cap3(G)
        if nb - f > 0:
            kills += 1
            step("S2-KILL", "HALL seed %d shortfall=%d" % (s, nb - f))
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json").write_text(
                json.dumps({"kill": True, "n": n, "H": H}, indent=1, default=str), encoding="utf-8")
            return 2
        # burst access = last; e_B and |N| there
        Bevs = G["Bevs"]
        last = max(b[0] for b in Bevs)
        Qb = [j for j in range(len(Bevs)) if Bevs[j][0] == last]
        d, N = delta_of(G, Qb)
        rows.append({"s": s, "n": n, "x": xc, "split": db - 3 * da, "da": da, "db": db,
                     "eB": len(Qb), "N": len(N), "delta": d})
        if s % 10 == 9:
            step("S2-P", "s=%d split=%d eB=%d N=%d delta=%d" % (s, db - 3 * da, len(Qb), len(N), d))
    mxsplit = max(r["split"] for r in rows) if rows else None
    mindelta = min(r["delta"] for r in rows) if rows else None
    step("S2-01", "seeds=%d maxsplit=%s mindelta=%s kills=%d" % (len(rows), mxsplit, mindelta, kills))
    TP.write_text(json.dumps({"rows": rows, "maxsplit": mxsplit, "mindelta": mindelta,
                              "kills": kills}, indent=1, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

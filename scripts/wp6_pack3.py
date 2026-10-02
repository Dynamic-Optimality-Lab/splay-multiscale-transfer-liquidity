"""WP-6 PACK3: adaptive deep-key packing-miss (decisive root experiment) (C105b).

pack2's recon was stale (trees moved post-read). pack3: at each phase-2 step,
simulate burst NOW -> btop_i; allow only keys with depth >= 10 in BOTH trees
(deep stays deep: 8W drift bound +-2/access keeps them out of top-3-level
triples; re-verified each step). Final burst; shortfall>0 => KILL (root-miss
suffices: GC-STATIC DEAD). Saturate => root-miss insufficient, mid-chain (8Z)
carries: root demoted for good.
Artifact: pack3.json (+hallkill on kill). Sealed files untouched.
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
    print("[WP-6][PACK3 %s] %s" % (sid, msg), flush=True)


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
    step("P3-00", "adaptive deep-key packing-miss (decisive)")
    TP = ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "pack3.json"
    rows = []
    kills = 0
    for s in range(40):
        rng = Rng(("r%d" % s).encode(), b"pack3")
        r = rng(0)
        n = [64, 128][r % 2]
        T0 = vine(n, (r >> 8) % 2 == 0)
        xc = n - (2 + (r >> 16) % 10)
        A, B = to_ptr(T0), to_ptr(T0)
        H = []
        for i in range(30):
            rr = Rng(("r%d" % s).encode(), b"rh%d" % i)
            q = rr(1000 + i)
            z = 1 + (q >> 2) % (n - 12)
            if abs(z - xc) <= 2:
                z = 1
            mode = "KEEP" if q % 3 else "DELETE"
            H.append([mode, z])
            A, _ = splay_A(A, z)
            if mode == "KEEP":
                B, _ = splay_B_push(B, z)
        # adaptive confined phase: 12 steps
        placed = 0
        for i in range(12):
            A3 = copy.deepcopy(A)
            B3 = copy.deepcopy(B)
            A3, _ = splay_A(A3, xc)
            B3, pushes = splay_B_push(B3, xc)
            btop = set(pushes[-1]) | {xc} if pushes else {xc}
            rr = Rng(("r%d" % s).encode(), b"rq%d" % i)
            done = False
            for c in range(30):
                z = 1 + rr(3000 + c) % (n - 12)
                if abs(z - xc) <= 2:
                    continue
                if dep(A, z) < 10 or dep(B, z) < 10:
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
                placed += 1
                done = True
                break
            if not done:
                break
        H.append(["KEEP", xc])
        G = build_graph(n, T0, H)
        if G is None:
            continue
        f, nb, _ = maxflow_cap3(G)
        if nb - f > 0:
            kills += 1
            step("P3-KILL", "HALL seed %d shortfall=%d (ROOT-MISS KILLS)" % (s, nb - f))
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json").write_text(
                json.dumps({"kill": True, "n": n, "H": H}, indent=1, default=str), encoding="utf-8")
            TP.write_text(json.dumps({"kill": True, "seed": s, "H": H}, indent=1, default=str),
                          encoding="utf-8")
            return 2
        Bevs = G["Bevs"]
        last = max(b[0] for b in Bevs)
        Qb = [j for j in range(len(Bevs)) if Bevs[j][0] == last]
        d, N = delta_of(G, Qb)
        rows.append({"s": s, "eB": len(Qb), "N": len(N), "delta": d, "placed": placed})
        if s % 10 == 9:
            step("P3-P", "s=%d eB=%d N=%d delta=%d placed=%d" % (s, len(Qb), len(N), d, placed))
    step("P3-01", "seeds=%d kills=%d mindelta=%s" % (
        len(rows), kills, min((r["delta"] for r in rows), default=None)))
    TP.write_text(json.dumps({"rows": rows, "kills": kills}, indent=1, default=str),
                  encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

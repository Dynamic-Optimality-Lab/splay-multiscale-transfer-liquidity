"""Independent verifier for n=7 dual certificate (no shared code paths
with prover beyond trans tables, which are re-derived from shapes).

Checks: dist[v] <= dist[u] + c(u,v) for ALL edges, c recomputed fresh.
Telescoping then gives every closed cycle W<=0 (Q<=2A at n=7).
"""
from __future__ import annotations
import sys
import copy
import json
import pickle
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))


def main():
    import wp6_overflow as V
    import wp6_cycle_ratio as O
    n = 7
    # re-derive shapes + trans INDEPENDENTLY (fresh ptr + splay_cap)
    Sh = O.build(n)["Sh"]
    nS = len(Sh)
    idx = {json.dumps(s, sort_keys=True): i for i, s in enumerate(Sh)}
    ptrs = [V.to_ptr(copy.deepcopy(s)) for s in Sh]

    def shape_of(P):
        return idx[json.dumps(list(O.enc_ptr(P)), sort_keys=True)]

    # depths + transitions per (shape, key), fresh
    Atrans, Btrans, dA, dB = {}, {}, {}, {}
    for ia in range(nS):
        dd = V.depths_of(ptrs[ia])
        for x in range(1, n + 1):
            A2 = copy.deepcopy(ptrs[ia])
            A2, iv = V.splay_cap(A2, x, 0, [])
            Atrans[(ia, x)] = (shape_of(A2), len(iv))
            B2 = copy.deepcopy(ptrs[ia])
            B2, p = V.splay_cap(B2, x, 0, [])
            Btrans[(ia, x)] = (shape_of(B2), len(p))
            dA[(ia, x)] = dd.get(x, 0)
            dB[(ia, x)] = dd.get(x, 0)
    print("[VFY] trans re-derived: shapes=%d" % nS, flush=True)
    D = pickle.load(open(ROOT / "artifacts" / "v04" / "wp6_present" /
                         "0909c74a" / "bf7.pkl", "rb"))
    dist = D["dist"]
    assert len(dist) == nS * nS
    # check every edge inequality: dist[v] <= dist[u] + c, c=-w=q.. use c=2a-q form
    bad = 0
    checked = 0
    for ia in range(nS):
        for ib in range(nS):
            u = ia * nS + ib
            du = dist[u]
            for x in range(1, n + 1):
                ia2, a = Atrans[(ia, x)]
                v = ia2 * nS + ib
                if dist[v] > du + 2 * a:
                    bad += 1
                checked += 1
                ib2, _ = Btrans[(ib, x)]
                v = ia2 * nS + ib2
                if dist[v] > du + 2 * a - dB[(ib, x)] // 2:
                    bad += 1
                checked += 1
        if (ia + 1) % 60 == 0:
            print("[VFY] %d/%d shapes, bad=%d" % (ia + 1, nS, bad), flush=True)
    print("[VFY] checked=%d bad=%d" % (checked, bad), flush=True)
    print("[VFY] CERTIFICATE: %s" % ("GREEN" if bad == 0 else "RED"))
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

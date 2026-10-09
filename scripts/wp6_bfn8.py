"""PIVOT-22 n=8 exact decision: on-demand Bellman-Ford on c=-w (integers).

2M states, 33M edges/pass on demand. Early exit; pass cap.
Feasible => dual certificate (YES n=8). Negative cycle => NO witness.
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


def step(sid, msg):
    print("[BF8 %s] %s" % (sid, msg), flush=True)


def main():
    import wp6_overflow as V
    D = pickle.load(open(str(ROOT / "artifacts" / "v04" / "wp6_present" /
                             "0909c74a" / "trans8.pkl"), "rb"))
    nS, Atrans, Btrans = D["nS"], D["Atrans"], D["Btrans"]
    n = 8
    Vcount = nS * nS
    # depths for q
    ptrs = [V.to_ptr(copy.deepcopy(s)) for s in D["Sh"]]
    dB = {}
    for ib in range(nS):
        dd = V.depths_of(ptrs[ib])
        for x in range(1, n + 1):
            dB[(ib, x)] = dd.get(x, 0)
    step("B-0", "V=%d E=%d" % (Vcount, Vcount * 2 * n))
    dist = [0] * Vcount
    parent = [-1] * Vcount
    CAP = 12
    for i in range(Vcount):
        if i >= CAP:
            step("B-1", "pass cap reached without convergence: INCONCLUSIVE")
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" /
             "bf8.json").write_text(json.dumps(
                 {"feasible": None, "passes": i, "note": "cap"}),
                encoding="utf-8")
            return 0
        changed = False
        for ia in range(nS):
            base = ia * nS
            for ib in range(nS):
                u = base + ib
                du = dist[u]
                for x in range(1, n + 1):
                    ia2, a = Atrans[(ia, x)]
                    v = ia2 * nS + ib
                    nd = du + 2 * a
                    if nd < dist[v]:
                        dist[v] = nd
                        parent[v] = u
                        changed = True
                    ib2, _ = Btrans[(ib, x)]
                    v = ia2 * nS + ib2
                    nd = du + 2 * a - dB[(ib, x)] // 2
                    if nd < dist[v]:
                        dist[v] = nd
                        parent[v] = u
                        changed = True
            if ia % 200 == 0:
                pass
        step("B-1", "pass %d done" % (i + 1))
        if not changed:
            step("B-2", "FEASIBLE after %d passes" % (i + 1))
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" /
             "bf8.json").write_text(json.dumps(
                 {"feasible": True, "passes": i + 1, "V": Vcount}),
                encoding="utf-8")
            pickle.dump({"dist": dist},
                        open(str(ROOT / "artifacts" / "v04" / "wp6_present" /
                                 "0909c74a" / "bf8.pkl"), "wb"))
            return 0
    # negative cycle: extract from last relaxed node (need tracking; rerun pass)
    step("B-2", "NEGATIVE CYCLE (positive-W exists) -- extracting")
    y = -1
    for ia in range(nS):
        base = ia * nS
        for ib in range(nS):
            u = base + ib
            du = dist[u]
            for x in range(1, n + 1):
                ia2, a = Atrans[(ia, x)]
                v = ia2 * nS + ib
                if du + 2 * a < dist[v]:
                    dist[v] = du + 2 * a
                    parent[v] = u
                    y = v
                ib2, _ = Btrans[(ib, x)]
                v = ia2 * nS + ib2
                if du + 2 * a - dB[(ib, x)] // 2 < dist[v]:
                    dist[v] = du + 2 * a - dB[(ib, x)] // 2
                    parent[v] = u
                    y = v
    for _ in range(Vcount):
        y = parent[y]
    cyc = []
    cur = y
    while True:
        cyc.append(cur)
        cur = parent[cur]
        if cur == y or len(cyc) > Vcount + 5:
            break
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" /
     "bf8.json").write_text(json.dumps(
         {"feasible": False, "cycle": cyc}), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

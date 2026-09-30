"""WP-6 ANCHOR: root-anchor coverage census (C66).

Every access's FINAL A-StepEv triple sits in root-area (node near root at end).
Deep burst chains cross root-area. Measure per KEEP burst with e_B>=4:
  N = neighbor set; F = {final-Aev ids of past accesses} (aid cursor);
  root-hit = |N ∩ F|; plus E1-size, K-size.
If root-hit >= 1 universally-ish (all long bursts), 8AA ROOT-ANCHOR lemma face.
Artifact: anchor.json. Sealed files untouched.
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_hallcore import build_graph, maxflow_cap3
from wp6_tightest import vine, Rng
from wp6_eventflow import to_ptr, splay_A, splay_B_push
from solver import encode as E


def step(sid, msg):
    print("[WP-6][ANCHOR %s] %s" % (sid, msg), flush=True)


from collections import defaultdict, Counter


def main() -> int:
    import json
    step("AN-00", "root-anchor coverage census")
    tot = 0
    rh = Counter()
    nohit_ex = []
    kills = 0
    for t in range(150):
        rng = Rng(("n%d" % t).encode(), b"anchor")
        r = rng(0)
        n = [16, 32, 64, 128][r % 3]
        T0 = vine(n, (r >> 8) % 2 == 0)
        L = 12 + (r >> 16) % 18
        x = 1 + (r >> 24) % n
        H = []
        for i in range(L):
            rr = Rng(("n%d" % t).encode(), b"nh%d" % i)
            q = rr(1000 + i)
            if i % 5 == 4:
                y = min(n, max(1, x + [-32, -16, 16, 32][q % 4]))
                H.append(["DELETE", y if y != x else 1])
                H.append(["KEEP", x])
            else:
                H.append(["KEEP" if q % 3 else "DELETE", x])
            x = min(n, max(1, x + [-16, -8, -4, -1, 1, 4, 8, 16][(q >> 9) % 8]))
        G = build_graph(n, T0, H)
        if G is None:
            continue
        f, nb, _ = maxflow_cap3(G)
        if nb - f > 0:
            kills += 1
            continue
        Aevs, Bevs = G["Aevs"], G["Bevs"]
        pre2 = G["pre"]
        A, B = to_ptr(T0), to_ptr(T0)
        fina = set()
        aid = 0
        acc_final = {}
        for idx, acc in enumerate(pre2):
            A, invs = splay_A(A, acc["x"])
            na = len(invs)
            if na:
                acc_final[idx] = aid + na - 1
                fina.add(aid + na - 1)
            aid += na
            if acc["mode"] == "KEEP":
                B, _ = splay_B_push(B, acc["x"])
        byacc = defaultdict(list)
        for j in range(len(Bevs)):
            byacc[Bevs[j][0]].append(j)
        for acc, js in sorted(byacc.items()):
            if len(js) < 4:
                continue
            N = set()
            for j in js:
                N |= G["adj"][j]
            past_fina = set(i for i in fina if Aevs[i][0] < acc)
            h = len(N & past_fina)
            rh[h] += 1
            tot += 1
            if h == 0 and len(nohit_ex) < 8:
                e = G["elig"][js[0]]
                nohit_ex.append({"t": t, "n": n, "acc": acc, "x": pre2[acc]["x"],
                                 "eB": len(js), "N": len(N),
                                 "e1": sum(1 for i in e["E1"] if Aevs[i][1]),
                                 "e4": sum(1 for i in e["E4"] if Aevs[i][1])})
    step("AN-01", "bursts=%d roothit_dist=%s kills=%d" % (tot, dict(sorted(rh.items())), kills))
    step("AN-02", "nohit_ex=%s" % (nohit_ex[:4],))
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "anchor.json").write_text(
        json.dumps({"bursts": tot, "roothit": dict(sorted(rh.items())), "kills": kills,
                    "nohit_ex": nohit_ex}, indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

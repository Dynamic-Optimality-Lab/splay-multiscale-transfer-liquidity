"""WP-6 DENSITY: per-heavy-block channel decomposition for sharp 8AC-D (C102).

Per B-heavy block (o = |Q|-3f > 0): record o/3 vs |E1|,|E4|,|K|,|E2|,|W|,|E7|,
|N|, plus which single channels suffice alone (ch >= o/3) and min margin per
channel combo. Goal: sharp finite form (e.g., W-sufficiency conditional on
anchored-thin) for the universal 8AC-D statement.
Artifact: density.json (+hallkill on Hall kill). Sealed files untouched.
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


def step(sid, msg):
    print("[WP-6][DENSITY %s] %s" % (sid, msg), flush=True)


from collections import defaultdict, Counter


def main() -> int:
    import json
    step("DN-00", "per-heavy-block channel decomposition")
    nb = 0
    solo = Counter()
    worst = {}
    worst_ex = {}
    cfgs = [(b"dn1", [16, 32, 64], 8, 26, 120), (b"dn2", [64, 128], 10, 30, 80)]
    for tag, nset, Llo, Lhi, NT in cfgs:
        for t in range(NT):
            rng = Rng(("d%d" % t).encode(), tag)
            r = rng(0)
            n = nset[r % len(nset)]
            T0 = vine(n, (r >> 8) % 2 == 0)
            L = Llo + (r >> 16) % (Lhi - Llo + 1)
            x = 1 + (r >> 24) % n
            H = []
            for i in range(L):
                rr = Rng(("d%d" % t).encode(), tag + b"h%d" % i)
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
            f, nbm, _ = maxflow_cap3(G)
            if nbm - f > 0:
                step("DN-KILL", "maxflow shortfall (Hall kill!)")
                (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json").write_text(
                    json.dumps({"kill": True, "n": n, "H": H}, indent=1, default=str), encoding="utf-8")
                return 2
            Aevs, Bevs = G["Aevs"], G["Bevs"]
            pre2 = G["pre"]
            A2, B2 = to_ptr(T0), to_ptr(T0)
            Arot = {}
            acc_of = {}
            aid = 0
            for idx, acc in enumerate(pre2):
                A2, invs = splay_A(A2, acc["x"])
                for (S, sited) in zip(invs, acc["sites"]):
                    Arot[aid] = frozenset(S)
                    acc_of[aid] = idx
                    aid += 1
                if acc["mode"] == "KEEP":
                    B2, _ = splay_B_push(B2, acc["x"])
            byacc = defaultdict(list)
            for j in range(len(Bevs)):
                byacc[Bevs[j][0]].append(j)
            for acc, js in sorted(byacc.items()):
                e = G["elig"][js[0]]
                E1s = set(i for i in e["E1"] if Aevs[i][1])
                E4s = set(i for i in e["E4"] if Aevs[i][1])
                ff = len(E4s) if (acc > 0 and pre2[acc - 1]["x"] == pre2[acc]["x"]) else len(E1s)
                o = len(js) - 3 * ff
                if o <= 0:
                    continue
                nb += 1
                xx = pre2[acc]["x"]
                E3s = set(i for i in e["E3"] if Aevs[i][1])
                K = set(i for i in E3s if xx in Arot.get(i, frozenset()) and acc_of.get(i, acc) < acc)
                W = E3s - K - E1s
                E2s = set(i for i in e["E2"] if Aevs[i][1])
                E7s = set(i for i in e.get("E7", []) if Aevs[i][1])
                N = set()
                for j in js:
                    N |= G["adj"][j]
                need = o / 3.0
                ch = {"E1": len(E1s), "E4": len(E4s), "K": len(K), "E2": len(E2s),
                      "W": len(W), "E7": len(E7s), "N": len(N), "Wall": len(E1s | E4s | K | E2s | W | E7s)}
                for k, v in ch.items():
                    m = v - need
                    if k not in worst or m < worst[k]:
                        worst[k] = m
                        worst_ex[k] = {"t": t, "n": n, "o": o, "v": v}
                for k in ("E1", "E4", "K", "E2", "W", "E7"):
                    if ch[k] >= need:
                        solo[k] += 1
    step("DN-01", "heavyblocks=%d solo-sufficiency=%s" % (nb, dict(solo)))
    step("DN-02", "worst margins=%s" % {k: round(v, 2) for k, v in worst.items()})
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "density.json").write_text(
        json.dumps({"heavyblocks": nb, "solo": dict(solo),
                    "worst": {k: round(v, 2) for k, v in worst.items()},
                    "worst_ex": worst_ex}, indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

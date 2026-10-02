"""WP-6 GREEDY2: order sweep (FWD/REV/minN) x tier sweep at scale (C97b).

C97 found: FWD chronological fails 1/150 (t75: K-hoarding starves later repeats);
REV saturates all tier orders there. Sweep orders x tiers over 500 histories
(random + banked kill witnesses) to crown the constructive rule:
  orders: FWD (chron), REV (reverse), MINN (fewest-neighbors first);
  tiers: E1,E4,K,T permutations (6).
Metric: per (order,tier) combo: #histories with greedy>maxflow (gap), worst gap.
Artifact: greedy2.json. Sealed files untouched.
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
from wp6_greedy import greedy_with


def step(sid, msg):
    print("[WP-6][GREEDY2 %s] %s" % (sid, msg), flush=True)


import itertools
from collections import defaultdict


def gen_histories():
    out = []
    cfgs = [(b"g2a", [16, 32, 64], 8, 26, 200), (b"g2b", [64, 128], 10, 30, 200),
            (b"g2c", [8, 24, 48], 12, 30, 100)]
    for tag, nset, Llo, Lhi, NT in cfgs:
        for t in range(NT):
            rng = Rng(("gg%d" % t).encode(), tag)
            r = rng(0)
            n = nset[r % len(nset)]
            T0 = vine(n, (r >> 8) % 2 == 0)
            L = Llo + (r >> 16) % (Lhi - Llo + 1)
            x = 1 + (r >> 24) % n
            H = []
            for i in range(L):
                rr = Rng(("gg%d" % t).encode(), tag + b"h%d" % i)
                q = rr(1000 + i)
                if i % 5 == 4:
                    y = min(n, max(1, x + [-32, -16, 16, 32][q % 4]))
                    H.append(["DELETE", y if y != x else 1])
                    H.append(["KEEP", x])
                else:
                    H.append(["KEEP" if q % 3 else "DELETE", x])
                x = min(n, max(1, x + [-16, -8, -4, -1, 1, 4, 8, 16][(q >> 9) % 8]))
            out.append((n, T0, H))
    import json
    for fn in ("starve_min.json",):
        try:
            dk = json.load(open(ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / fn))
            out.append((dk["n"], vine(dk["n"], dk["T0left"]), dk["Hmin"]))
        except Exception:
            pass
    return out


def main() -> int:
    import json
    step("G2-00", "order x tier sweep at scale")
    tiers = [list(p) for p in itertools.permutations(["E1", "E4", "K", "T"])]
    stats = {}
    hists = gen_histories()
    step("G2-01", "histories=%d combos=%d" % (len(hists), 3 * len(tiers)))
    prepped = []
    skipped = 0
    for n, T0, H in hists:
        G = build_graph(n, T0, H)
        if G is None:
            skipped += 1
            continue
        f, nb, _ = maxflow_cap3(G)
        if nb - f > 0:
            step("G2-KILL", "maxflow shortfall (Hall kill!)")
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
        seqs = {
            "FWD": sorted(range(len(Bevs)), key=lambda j: (Bevs[j][0], j)),
            "REV": sorted(range(len(Bevs)), key=lambda j: (Bevs[j][0], j), reverse=True),
            "MINN": sorted(range(len(Bevs)), key=lambda j: (len(G["adj"][j]), Bevs[j][0], j)),
        }
        prepped.append((n, T0, H, G, Arot, acc_of, seqs, nb))
    for oname in ("FWD", "REV", "MINN"):
        for tord in tiers:
            key = oname + "|" + "".join(tord)
            gaps = 0
            worst = 0
            for (n, T0, H, G, Arot, acc_of, seqs, nb) in prepped:
                s = greedy_with(n, T0, H, G, Arot, acc_of, seqs[oname], tord)
                if s > 0:
                    gaps += 1
                    worst = max(worst, s)
            stats[key] = {"gaps": gaps, "worst": worst}
            if gaps == 0:
                step("G2-PERFECT", key)
    best = sorted(stats.items(), key=lambda kv: (kv[1]["gaps"], kv[1]["worst"]))[:6]
    step("G2-02", "hists=%d best=%s" % (len(prepped), best))
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "greedy2.json").write_text(
        json.dumps({"hists": len(prepped), "skipped": skipped, "best": best,
                    "rev_E1E4KT": stats.get("REV|E1E4KT"),
                    "fwd_E1E4KT": stats.get("FWD|E1E4KT")},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

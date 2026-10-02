"""WP-6 CODIST: loader key-distance census for cohort-locality (C142).

t75's stuck-loaders are same-x siblings + adjacent-x past cohort (38/39).
If loader key-distance stays bounded at scale, contention localizes to key
neighborhoods and the INTERVAL route (8AC-IL) opens; if it grows with n,
interval aggregation is dead (consistent 8N(d)). Measure over W/K placements
(FWD|T,E1,E4,K, walks n<=512 L70 + pushers): |loader_x - site_acc_x|
distribution (site_acc_x = key of the access that plotted the site),
plus max/med per family, plus stuck-loader distances. Artifact: codist.json.
Sealed files untouched.
"""
from __future__ import annotations
import sys
import json
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_hallcore import build_graph, maxflow_cap3
from wp6_eventflow import to_ptr, splay_A, splay_B_push
from wp6_trap import greedy_M, gen_walk, gen_seed, chan_of


def step(sid, msg):
    print("[WP-6][CODIST %s] %s" % (sid, msg), flush=True)


def analyze(n, T0, H):
    from wp6_hallcore import build_graph as bg
    G = bg(n, T0, H)
    if G is None:
        return None
    f, nb, _ = maxflow_cap3(G)
    if nb - f > 0:
        return ("KILL",)
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
    short, M, loads = greedy_M(n, T0, H, G, Arot, acc_of, ["T", "E1", "E4", "K"], False)
    distsW = []
    distsK = []
    distsE1 = []
    for j, i in M.items():
        aj = Bevs[j][0]
        ai = acc_of.get(i, -1)
        ch = chan_of(j, i, G, Arot, acc_of)
        d = abs(pre2[aj]["x"] - pre2[ai]["x"])
        if "W" in ch:
            distsW.append(d)
        if "K" in ch:
            distsK.append(d)
        if "E1" in ch:
            distsE1.append(d)
    return {"W": distsW, "K": distsK, "E1": distsE1, "stuck": len(short), "n": n}


def main() -> int:
    step("CD-00", "loader key-distance census at scale")
    agg = {"W": [], "K": [], "E1": []}
    stuck = 0
    kills = 0
    done = 0
    for s in range(150):
        for fam in (0, 1):
            n, T0, H = gen_walk(8000 + s) if fam == 0 else gen_seed(8000 + s, b"cd")
            v = analyze(n, T0, H)
            if v is None:
                continue
            if isinstance(v, tuple):
                kills += 1
                continue
            done += 1
            stuck += v["stuck"]
            for k in agg:
                agg[k].extend(v[k])
    import statistics
    out = {"evals": done, "stuck": stuck, "kills": kills}
    for k, ds in agg.items():
        ds.sort()
        out[k] = {"n": len(ds),
                  "med": (ds[len(ds) // 2] if ds else None),
                  "p90": (ds[int(len(ds) * 0.9)] if ds else None),
                  "max": (ds[-1] if ds else None),
                  "mean": (sum(ds) / len(ds) if ds else None)}
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "codist.json").write_text(
        json.dumps(out, indent=1, sort_keys=True, default=str), encoding="utf-8")
    step("CD-01", json.dumps(out, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())

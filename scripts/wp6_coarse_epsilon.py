"""PIVOT-12 epsilon census: epsilon=q-2a per access on exact pair graphs.

n<=6 via oracle adj + depth tables; n=7 streaming transitions.
Saves vine_excursion/epsilon.json (coarse_double reads it too).
"""
from __future__ import annotations
import sys
import json
import copy
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_eventflow import to_ptr, splay_A, splay_B_push
from wp6_adv import depths_of
import wp6_cycle_ratio as O

BD = ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "coarse_double"


def step(sid, msg):
    print("[EPS %s] %s" % (sid, msg), flush=True)


def census_n6():
    G = O.build(6)
    nS, adj = G["nS"], G["adj"]
    ptrs = [to_ptr(copy.deepcopy(s)) for s in G["Sh"]]
    dep = []
    for ia in range(nS):
        d = depths_of(copy.deepcopy(ptrs[ia]))
        dep.append([d.get(x + 1, 0) for x in range(6)])
    bad = Counter()
    tot = 0
    worst = None
    for u in range(nS * nS):
        ia, ib = u // nS, u % nS
        for e in adj[u]:
            md, x = e[1], e[2]
            a = (dep[ia][x - 1] + 1) // 2
            if md == "K":
                dB = dep[ib][x - 1]
                q, z = dB // 2, dB % 2
            else:
                q = z = 0
            eps = q - 2 * a
            tot += 1
            if eps > 0:
                bad[(md, a, q, z)] += 1
                if worst is None or eps > worst[0]:
                    worst = (eps, md, a, q, z)
    return {"n": 6, "total": tot, "bad": [[list(k), v] for k, v in
                                         sorted(bad.items())],
            "worst": worst}


def main():
    out = {"eps6": census_n6()}
    step("E6", "n=6: total=%d badtypes=%d worst=%s" %
         (out["eps6"]["total"], len(out["eps6"]["bad"]), out["eps6"]["worst"]))
    BD.mkdir(parents=True, exist_ok=True)
    (BD / "epsilon.json").write_text(json.dumps(out, indent=1, sort_keys=True,
                                                default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""PIVOT-23 feature discovery (careful): conditional variance of BF potential.

Q: what structural features determine Phi? Exact indistinguishability tests.
Saved artifacts; no inline guessing.
"""
from __future__ import annotations
import sys
import copy
import json
import pickle
from pathlib import Path
from collections import Counter, defaultdict

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
import wp6_overflow as V
import wp6_cycle_ratio as O

BD = ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "dual_mine"


def step(sid, msg):
    print("[MINE %s] %s" % (sid, msg), flush=True)


def save(name, obj):
    BD.mkdir(parents=True, exist_ok=True)
    (BD / name).write_text(json.dumps(obj, indent=1, sort_keys=True,
                                      default=str), encoding="utf-8")


def main():
    n = 7
    G = O.build(n)
    nS, Sh = G["nS"], G["Sh"]
    roots = []
    for s in Sh:
        P = V.to_ptr(copy.deepcopy(s))
        while P["p"] is not None:
            P = P["p"]
        roots.append(P["k"])
    D = pickle.load(open(str(ROOT / "artifacts" / "v04" / "wp6_present" /
                             "0909c74a" / "bf7.pkl"), "rb"))
    dist = D["dist"]
    assert len(dist) == nS * nS
    # F1: root-pair -> set of Phi (CAREFUL: explicit sets)
    rp = defaultdict(set)
    for ia in range(nS):
        for ib in range(nS):
            rp[(roots[ia], roots[ib])].add(dist[ia * nS + ib])
    rp_list = {str(k): sorted(v) for k, v in rp.items()}
    multi = sum(1 for v in rp.values() if len(v) > 1)
    step("F1", "root-pairs=%d multi-valued=%d" % (len(rp), multi))
    save("rootpair_phi.json", {"multi": multi, "table": rp_list})
    # twin-bit split
    tw = Counter()
    for (ra, rb), vs in rp.items():
        for v in vs:
            tw[(ra == rb, v)] += 1
    step("F1", "twin-split distinct (twin,Phi) combos: %s" % dict(tw))
    return 0


if __name__ == "__main__":
    sys.exit(main())

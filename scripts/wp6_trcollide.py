"""PIVOT-25R-T §4/§6/§9: controlled pairs, D0-D4 collisions, shape test.

D0=(pat,sizes); D1=+A-depths of pivots; D2=+A-LCA relations;
D3=+Placement per block; D4=+ordered piece roots.
Ambiguous class = same descriptor, mixed hard/easy labels.
Shape-vs-placement: same D3, same rank-shapes, different pay?
"""
from __future__ import annotations
import sys
import json
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))


def step(sid, msg):
    print("[TRX %s] %s" % (sid, msg), flush=True)


def rankshape(t):
    """Order-invariant shape: inorder-rank relabeling of nested structure."""
    keys = []

    def col(nd):
        if nd is None:
            return
        col(nd[1])
        keys.append(nd[0])
        col(nd[2])
    col(t)
    rk = {k: i for i, k in enumerate(sorted(keys))}

    def go(nd):
        if nd is None:
            return None
        return [rk[nd[0]], go(nd[1]), go(nd[2])]
    return go(t)


def desc(e, level, shapes=None):
    b = e["blocks"]
    sizes = tuple(0 if x["empty"] else len(x["keys"]) for x in b)
    d = (e["pat"], sizes)
    if level >= 1:
        d += (e["piv"]["depths"]["x"], e["piv"]["depths"]["p"],
              e["piv"]["depths"]["g"])
    if level >= 2:
        p = e["piv"]
        d += (p["lca_pg"], p["anc_x_p"], p["anc_p_x"], p["anc_x_g"],
              p["anc_g_x"], p["anc_p_g"], p["anc_g_p"])
    if level >= 3:
        for x in b:
            if x["empty"]:
                d += ((0, -1, 1),)
            else:
                d += ((x["cover"], x["a_lca_d"], 1 if x["is_Asub"] else 0),)
    if level >= 4:
        for x in b:
            d += (tuple(x["pieces"]) if not x["empty"] else (),)
    return d


def main():
    ev = json.loads((ROOT / "artifacts" / "v04" / "wp6_present" /
                     "0909c74a" / "dual_mine" /
                     "transport_bank.json").read_text())
    step("L", "events=%d hard=%d" %
         (len(ev), sum(1 for e in ev if e["hard"])))
    out = {}
    for lv in range(5):
        groups = defaultdict(list)
        for i, e in enumerate(ev):
            groups[desc(e, lv)].append(i)
        amb = {k: v for k, v in groups.items()
               if any(ev[i]["hard"] for i in v)
               and any(not ev[i]["hard"] for i in v)}
        nev = sum(len(v) for v in amb.values())
        step("D%d" % lv, "classes=%d ambiguous=%d events-in-amb=%d" %
             (len(groups), len(amb), nev))
        if amb:
            k0 = min(amb, key=lambda k: (len(amb[k]),
                                        min(amb[k])))
            out["D%d_smallest" % lv] = {
                "desc": str(k0), "members": [
                    {"tag": ev[i]["tag"], "xpg": ev[i]["xpg"],
                     "pay": ev[i]["pay"], "twinDrop": ev[i]["twinDrop"],
                     "DbDrop": ev[i]["DbDrop"]} for i in amb[k0]]}
            step("D%d" % lv, "smallest amb: %s" %
                 (out["D%d_smallest" % lv],))
        out["D%d" % lv] = {"classes": len(groups), "amb": len(amb),
                           "amb_events": nev}
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" /
     "dual_mine" / "transport_collide.json").write_text(
        json.dumps(out, indent=1, default=str), encoding="utf-8")
    step("S", "saved transport_collide.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())

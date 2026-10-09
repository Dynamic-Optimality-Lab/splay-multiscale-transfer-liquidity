"""PIVOT-25R-C §5: L3-8 stitch autopsy. For each adjacent pair of concrete edges
underlying the positive abstract cycle, compare actual destination vs required
source: full pair features + next key's A/B search paths (nodes, turns,
depths, parent/grandparent) in BOTH states + what the previous splay created.
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
import wp6_overflow as V


def step(sid, msg):
    print("[L3S %s] %s" % (sid, msg), flush=True)


def is_vine(t):
    st = [t]
    while st:
        nd = st.pop()
        if nd is None:
            continue
        if nd[1] is not None and nd[2] is not None:
            return False
        st.append(nd[1])
        st.append(nd[2])
    return True


def maxdepth(t):
    mx = 0
    st = [(t, 0)]
    while st:
        nd, d = st.pop()
        if nd is None:
            continue
        mx = max(mx, d)
        st.append((nd[1], d + 1))
        st.append((nd[2], d + 1))
    return mx


def search_path(t, y):
    """Nodes root->y with L/R turns on list-shape."""
    path, turns, nd = [], [], t
    while nd is not None and nd[0] != y:
        path.append(nd[0])
        if y < nd[0]:
            turns.append("L")
            nd = nd[1]
        else:
            turns.append("R")
            nd = nd[2]
    if nd is None:
        return None
    path.append(y)
    return {"nodes": path, "turns": turns, "depth": len(path) - 1,
            "p": path[-2] if len(path) >= 2 else None,
            "g": path[-3] if len(path) >= 3 else None}


def feat(Sh, rt, ia, ib):
    return {"st": (ia, ib), "roots": [rt[ia], rt[ib]],
            "vine": [is_vine(Sh[ia]), is_vine(Sh[ib])],
            "md": [maxdepth(Sh[ia]), maxdepth(Sh[ib])],
            "twin": 1 if rt[ia] == rt[ib] else 0}


def main():
    import sys as _s
    n = 8
    edges = json.loads(_s.argv[1]) if len(_s.argv) > 1 else [
        (457, 429, 8, "K"), (1093, 1003, 7, "K"), (869, 910, 2, "K")]
    edges = [(e[0], e[1], e[2], e[3] if len(e) > 3 else "K") for e in edges]
    out_name = _s.argv[2] if len(_s.argv) > 2 else "l3_stitch.json"
    D = pickle.load(open(str(ROOT / "artifacts" / "v04" / "wp6_present" /
                             "0909c74a" / "trans8.pkl"), "rb"))
    Sh, nS, Atrans, Btrans = D["Sh"], D["nS"], D["Atrans"], D["Btrans"]
    ptrs = [V.to_ptr(copy.deepcopy(s)) for s in Sh]
    rt, dd = {}, {}
    for ia in range(nS):
        r = ptrs[ia]
        while r["p"] is not None:
            r = r["p"]
        rt[ia] = r["k"]
        dd[ia] = V.depths_of(ptrs[ia])
    # cycle edges in following order (each entry: ia, ib, x, mode)
    ends = []
    for (ia, ib, x, mo) in edges:
        ta, _ = Atrans[(ia, x)]
        tb, _ = Btrans[(ib, x)]
        ends.append((ta, tb))
    out = []
    m = len(edges)
    for k in range(m):
        ia, ib, x, mo = edges[k]
        E = ends[k]
        S = (edges[(k + 1) % m][0], edges[(k + 1) % m][1])
        y = edges[(k + 1) % m][2]
        rec = {"stitch": k, "prev_edge": [ia, ib, x],
               "next_edge": [S[0], S[1], y],
               "E": feat(Sh, rt, *E), "S": feat(Sh, rt, *S),
               "stitch_ok": list(E) == list(S)}
        # next key y paths in E-trees vs S-trees
        for tag, (ja, jb) in (("E", E), ("S", S)):
            rec[tag + "_Apath"] = search_path(Sh[ja], y)
            rec[tag + "_Bpath"] = search_path(Sh[jb], y)
        # what did the previous splay create? post-tree root neighborhoods:
        # children of new root (=x) in E_A/E_B + depth profile of y there
        for tag, (ja, jb) in (("E", E),):
            for side, jj in (("A", ja), ("B", jb)):
                t = Sh[jj]
                rec["%s_%s_rootkids" % (tag, side)] = [
                    t[1][0] if t[1] is not None else None,
                    t[2][0] if t[2] is not None else None]
        out.append(rec)
        step("S%d" % k, "E%s S%s ok=%s y=%d" % (E, S, rec["stitch_ok"], y))
        step("S%d" % k, "E feats=%s S feats=%s" %
             (rec["E"], rec["S"]))
        step("S%d" % k, "y=%d E_Apath=%s E_Bpath=%s" %
             (y, rec["E_Apath"], rec["E_Bpath"]))
        step("S%d" % k, "y=%d S_Apath=%s S_Bpath=%s" %
             (y, rec["S_Apath"], rec["S_Bpath"]))
        step("S%d" % k, "E rootkids A=%s B=%s" %
             (rec["E_A_rootkids"], rec["E_B_rootkids"]))
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" /
     "dual_mine" / out_name).write_text(
        json.dumps(out, indent=1, default=str), encoding="utf-8")
    step("S", "wrote dual_mine/%s" % out_name)
    return 0


if __name__ == "__main__":
    sys.exit(main())

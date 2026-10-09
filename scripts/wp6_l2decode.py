"""PIVOT-25R L2 step 1: decode stored L1 root-pair witnesses + stitch states.

Canonical replay: fresh ptr per shape + splay_cap (exact mechanics), cross-checked
against trans7.pkl targets. Vine = degenerate chain (every node <=1 non-null child).
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
import wp6_cycle_ratio as O


def step(sid, msg):
    print("[L2D %s] %s" % (sid, msg), flush=True)


def maxdepth(t):
    mx = 0
    stack = [(t, 0)]
    while stack:
        nd, d = stack.pop()
        if nd is None:
            continue
        mx = max(mx, d)
        stack.append((nd[1], d + 1))
        stack.append((nd[2], d + 1))
    return mx


def is_vine(t):
    stack = [t]
    while stack:
        nd = stack.pop()
        if nd is None:
            continue
        if nd[1] is not None and nd[2] is not None:
            return False
        stack.append(nd[1])
        stack.append(nd[2])
    return True


def main():
    n = 7
    Sh = O.build(n)["Sh"]
    nS = len(Sh)
    idx = {json.dumps(s, sort_keys=True): i for i, s in enumerate(Sh)}
    D = pickle.load(open(str(ROOT / "artifacts" / "v04" / "wp6_present" /
                             "0909c74a" / "trans7.pkl"), "rb"))
    Atrans, Btrans = D["Atrans"], D["Btrans"]

    def shape_of(P):
        return idx[json.dumps(list(O.enc_ptr(P)), sort_keys=True)]

    ptrs = [V.to_ptr(copy.deepcopy(s)) for s in Sh]
    rt, dd, vine, mdep = {}, {}, {}, {}
    for ia in range(nS):
        r = ptrs[ia]
        while r["p"] is not None:
            r = r["p"]
        rt[ia] = r["k"]
        dd[ia] = V.depths_of(ptrs[ia])
        vine[ia] = is_vine(Sh[ia])
        mdep[ia] = maxdepth(Sh[ia])
    step("S", "shapes=%d vines=%d" % (nS, sum(1 for v in vine.values() if v)))

    C = json.load(open(str(ROOT / "artifacts" / "v04" / "wp6_present" /
                           "0909c74a" / "dual_mine" / "cegar.json")))
    wit = C["rootpair_witnesses"]
    # abstract edges: ((U)->(V)) with [maxw, [ia,ib,x,mode]]
    edges = []
    for k, v in wit.items():
        mxw, w2 = v[0], v[1]
        ia, ib, x, mode = w2[0], w2[1], w2[2], w2[3]
        edges.append((k, mxw, ia, ib, x, mode))
    step("S", "stored abstract edges=%d cycle=%s" % (len(edges), C["rootpair_cycle"]))

    out_edges = []
    for (k, mxw, ia, ib, x, mode) in edges:
        dA = dd[ia].get(x, 0)
        a = (dA + 1) // 2
        ta, aa = Atrans[(ia, x)]
        assert aa == a, (ia, x, aa, a)  # trans a == ceil(dA/2)
        if mode == "K":
            dB = dd[ib].get(x, 0)
            q = dB // 2
            tb, bb = Btrans[(ib, x)]
            w = q - 2 * a
        else:
            dB, q, tb = None, 0, ib
            w = -2 * a
        assert w == mxw, (k, w, mxw)
        # canonical replay of this single edge
        A2 = copy.deepcopy(ptrs[ia])
        A2, asteps = V.splay_cap(A2, x, 0, [])
        assert len(asteps) == a, (ia, x, len(asteps), a)
        assert shape_of(A2) == ta, (ia, x, shape_of(A2), ta)
        if mode == "K":
            B2 = copy.deepcopy(ptrs[ib])
            B2, bsteps = V.splay_cap(B2, x, 0, [])
            ndb = sum(1 for s in bsteps if s["kind"] == "double")
            assert ndb == q, (ib, x, ndb, q)
            assert shape_of(B2) == tb, (ib, x, shape_of(B2), tb)
        twn = 1 if rt[ia] == rt[ib] else 0
        twn2 = 1 if rt[ta] == rt[tb] else 0
        rec = {"abstract": k, "maxw": mxw, "ia": ia, "ib": ib, "x": x,
               "mode": mode, "dA": dA, "a": a, "dB": dB, "q": q, "w": w,
               "pre_roots": [rt[ia], rt[ib]], "pre_vine": [vine[ia], vine[ib]],
               "pre_maxdepth": [mdep[ia], mdep[ib]],
               "ta": ta, "tb": tb,
               "post_roots": [rt[ta], rt[tb]],
               "post_vine": [vine[ta], vine[tb]],
               "post_maxdepth": [mdep[ta], mdep[tb]],
               "twin_pre": twn, "twin_post": twn2,
               "c_adj": w - 2 * (twn2 - twn)}
        out_edges.append(rec)
        step("E", "%s pre(r=%s,vine=%s,md=%s) x=%d dA=%d dB=%s a=%d q=%s w=%d "
                  "post[(%d,%d) r=%s vine=%s md=%s] twin %d->%d c=%d" %
             (k, rec["pre_roots"], rec["pre_vine"], rec["pre_maxdepth"], x,
              dA, dB, a, q, w, ta, tb, rec["post_roots"], rec["post_vine"],
              rec["post_maxdepth"], twn, twn2, rec["c_adj"]))

    # stitch analysis: e1: (1,1)->(7,7) is edges[?]; order by cycle
    e1 = next(e for e in out_edges if e["pre_roots"] == [1, 1])
    e2 = next(e for e in out_edges if e["pre_roots"] == [7, 7])
    e1end = (e1["ta"], e1["tb"])
    e2start = (e2["ia"], e2["ib"])
    e2end = (e2["ta"], e2["tb"])
    e1start = (e1["ia"], e1["ib"])
    stitch = {"e1end": list(e1end), "e2start": list(e2start),
              "e2end": list(e2end), "e1start": list(e1start),
              "stitch1_ok": list(e1end) == list(e2start),
              "stitch2_ok": list(e2end) == list(e1start)}

    def feat(s):
        ia, ib = s
        return {"ia": ia, "ib": ib, "roots": [rt[ia], rt[ib]],
                "vineA": vine[ia], "vineB": vine[ib],
                "maxdepth": [mdep[ia], mdep[ib]],
                "twin": 1 if rt[ia] == rt[ib] else 0}

    stitch["feat_e1end"] = feat(e1end)
    stitch["feat_e2start"] = feat(e2start)
    stitch["feat_e2end"] = feat(e2end)
    stitch["feat_e1start"] = feat(e1start)
    # smallest structural distinction at failed stitch-1 (same root-pair class)
    f1, f2 = stitch["feat_e1end"], stitch["feat_e2start"]
    dist = [k for k in ("vineB", "vineA", "twin", "maxdepth", "ia", "ib")
            if f1[k] != f2[k]]
    stitch["distinguish_e1end_vs_e2start"] = dist
    g1, g2 = stitch["feat_e2end"], stitch["feat_e1start"]
    dist2 = [k for k in ("vineB", "vineA", "twin", "maxdepth", "ia", "ib")
             if g1[k] != g2[k]]
    stitch["distinguish_e2end_vs_e1start"] = dist2
    if "vineB" in dist or "vineB" in dist2:
        rec_alpha = "(rootA,rootB,isVineB)"
    elif "vineA" in dist or "vineA" in dist2:
        rec_alpha = "(rootA,rootB,isVineA)"
    else:
        rec_alpha = "NONE_SMALL (shape-index only)"
    stitch["recommended_alpha"] = rec_alpha
    step("ST", "stitch1 %s vs %s ok=%s dist=%s" %
         (e1end, e2start, stitch["stitch1_ok"], dist))
    step("ST", "stitch2 %s vs %s ok=%s dist=%s" %
         (e2end, e1start, stitch["stitch2_ok"], dist2))
    step("ST", "recommended_alpha=%s" % rec_alpha)

    out = {"n": n, "nS": nS, "edges": out_edges, "stitch": stitch}
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" /
     "dual_mine" / "l2_decode.json").write_text(
        json.dumps(out, indent=1, default=str), encoding="utf-8")
    step("S", "wrote dual_mine/l2_decode.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())

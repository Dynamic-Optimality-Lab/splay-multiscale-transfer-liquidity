"""PIVOT-25R-B §5+§9: Bellman horizons + profile-transition determinism.

V_0=0, V_{k+1}=max(0,max_e[D+V_k]) to fixpoint (==V); per-state h(s),
global h_n. Then (P(s),x)->P(s_x') collision test (D-profiles via
target shapes, no replay per edge beyond transitions).
"""
from __future__ import annotations
import sys
import copy
import json
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
import wp6_overflow as V
from wp6_staticR import R_static, depths_list


def step(sid, msg):
    print("[VBH %s] %s" % (sid, msg), flush=True)


def main():
    import sys as _s
    import pickle
    import wp6_cycle_ratio as O
    n = int(_s.argv[1]) if len(_s.argv) > 1 else 5
    Sh = O.shapes_of(list(range(1, n + 1)))
    nS = len(Sh)
    Vcount = nS * nS
    import pickle
    import json as J
    idx = {J.dumps(s, sort_keys=True): i for i, s in enumerate(Sh)}
    try:
        Dp = pickle.load(open(str(ROOT / "artifacts" / "v04" /
                                  "wp6_present" / "0909c74a" /
                                  ("trans%d.pkl" % n)), "rb"))
        Atrans, Btrans = Dp["Atrans"], Dp["Btrans"]
    except FileNotFoundError:
        # build transitions by replay (no stored trans tables at this n)
        Atrans, Btrans = {}, {}
        for ja in range(nS):
            for y in range(1, n + 1):
                rp = V.replay(Sh[ja], Sh[ja], [("K", y)])
                Atrans[(ja, y)] = (
                    idx[J.dumps(rp["endA"], sort_keys=True)],
                    len(rp["accesses"][0]["asteps"]))
                Btrans[(ja, y)] = (
                    idx[J.dumps(rp["endB"], sort_keys=True)],
                    sum(1 for s in rp["accesses"][0]["bsteps"]
                        if s["kind"] == "double"))
        step("T", "trans built by replay")
    ptrs = [V.to_ptr(copy.deepcopy(s)) for s in Sh]
    rt, dd = {}, {}
    for ia in range(nS):
        r = ptrs[ia]
        while r["p"] is not None:
            r = r["p"]
        rt[ia] = r["k"]
        dd[ia] = V.depths_of(ptrs[ia])
    # D-profiles per PAIR state (needed for V_k and determinism)
    Prof = {}
    for ia in range(nS):
        for ib in range(nS):
            A, B = Sh[ia], Sh[ib]
            da = depths_list(A)
            t = 1 if rt[ia] == rt[ib] else 0
            Prof[(ia, ib)] = tuple(
                R_static(B, y) - 2 * ((da[y] + 1) // 2) - 2 * (1 - t)
                for y in range(1, n + 1))
        if (ia + 1) % 60 == 0:
            step("P", "profiles ia=%d/%d" % (ia + 1, nS))
    # transitions (KEEP only for V_k? V covers KEEP+DELETE; horizons on
    # full graph incl DELETE D^DEL)
    adj = {}
    for ia in range(nS):
        for ib in range(nS):
            u = ia * nS + ib
            el = []
            A, B = Sh[ia], Sh[ib]
            da = depths_list(A)
            t = 1 if rt[ia] == rt[ib] else 0
            for x in range(1, n + 1):
                ia2, a = Atrans[(ia, x)]
                ib2, _ = Btrans[(ib, x)]
                t2 = 1 if rt[ia2] == rt[ib2] else 0
                # TRUE residual (shortfall under twin+Db), NOT raw reward:
                from wp6_staticR import R_static as _Rs
                el.append((ia2 * nS + ib2, x, "K",
                           _Rs(Sh[ib], x) - 2 * a - 2 * (1 - t)))
                ja2, _ = Atrans[(ia, x)]
                td = 1 if rt[ja2] == rt[ib] else 0
                el.append((ja2 * nS + ib, x, "D", -2 * a - 2 * (td - t)))
            adj[u] = el
    # V_k monotone relaxation (exact ints)
    Vk = [0] * Vcount
    hs = [0] * Vcount
    for k in range(1, 500):
        ch = 0
        Vn = list(Vk)
        for u in range(Vcount):
            best = 0
            for (to, _, _, w) in adj[u]:
                if w + Vk[to] > best:
                    best = w + Vk[to]
            if best != Vk[u]:
                Vn[u] = best
                hs[u] = k  # last-change iteration = stabilization
                ch += 1
        Vk = Vn
        step("H", "k=%d changed=%d" % (k, ch))
        if ch == 0:
            break
    h_n = max(hs)
    from collections import Counter
    step("H", "h_n=%d hdist=%s" % (h_n, dict(sorted(Counter(hs).items()))))
    # verify against canonical V
    VD = json.loads((ROOT / "artifacts" / "v04" / "wp6_present" /
                     "0909c74a" / "dual_mine" /
                     ("vfull%d.json" % n)).read_text())
    Vf = VD["V"]
    mismatch = sum(1 for u in range(Vcount) if Vk[u] != Vf[u])
    step("H", "V_k-limit vs canonical V mismatches: %d" % mismatch)
    # gateway + C_k (from stored profiles: maxD vs V)
    gw = []
    for ia in range(nS):
        for ib in range(nS):
            u = ia * nS + ib
            if Vf[u] > max([0] + list(Prof[(ia, ib)])):
                gw.append(u)
    step("G", "gateway=%d" % len(gw))
    # determinism: (P(s),x) -> P(s_x') [KEEP only]
    det = defaultdict(set)
    for ia in range(nS):
        for ib in range(nS):
            u = ia * nS + ib
            for x in range(1, n + 1):
                ia2, _ = Atrans[(ia, x)]
                ib2, _ = Btrans[(ib, x)]
                det[(Prof[(ia, ib)], x)].add(Prof[(ia2, ib2)])
    amb = sum(1 for v in det.values() if len(v) > 1)
    step("D", "det-classes=%d amb=%d" % (len(det), amb))
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" /
     "dual_mine" / ("vhor%d.json" % n)).write_text(
        json.dumps({"hn": h_n, "hdist": {str(k): v for k, v in
                                        Counter(hs).items()},
                    "mismatch": mismatch, "det_amb": amb,
                    "det_classes": len(det)}, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

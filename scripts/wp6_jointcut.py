"""PIVOT-25R-U §3: cutting-plane free-g feasibility on COMPLETE graphs.

usage: python wp6_jointcut.py <n> <maxiters> [batchK]
state: dual_mine/joint_cut<n>.json {rows, iters_done, status, log}.

Init rows = 133-edge system (cert + witnesses + battery + grow), all
replay-instantiated via canonical engine. Each iteration: sparse max-slack
LP (margin delta), full-graph scan for top-K violated distinct rows,
append + save. Termination: FEASIBLE-SCAN (no violation within tol) or
LP-INFEASIBLE-FLOAT (exact Farkas attempted separately).
"""
from __future__ import annotations
import sys
import copy
import json
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
import wp6_overflow as V
import wp6_cycle_ratio as O
from wp6_jointlp import edge_row, shift

CERT = Path("C:/Users/SAIFMA~1/AppData/Local/Temp/opencode/jointcert/"
            "joint_depth_template_countercertificate.json")


def step(sid, msg):
    print("[JCT %s] %s" % (sid, msg), flush=True)


def shapes_info(Sh, n):
    nS = len(Sh)
    dd, lo, hi, sz, rt = {}, {}, {}, {}, {}
    ptrs = [V.to_ptr(copy.deepcopy(s)) for s in Sh]
    for ia in range(nS):
        r = ptrs[ia]
        while r["p"] is not None:
            r = r["p"]
        rt[ia] = r["k"]
        dd[ia] = V.depths_of(ptrs[ia])
        for x in range(1, n + 1):
            nd = Sh[ia]
            while nd is not None and nd[0] != x:
                nd = nd[1] if x < nd[0] else nd[2]
            ks = []

            def go(m):
                if m is None:
                    return
                ks.append(m[0])
                go(m[1])
                go(m[2])
            go(nd)
            a, b = min(ks), max(ks)
            assert len(ks) == b - a + 1
            lo[(ia, x)], hi[(ia, x)], sz[(ia, x)] = a, b, len(ks)
    return dd, lo, hi, sz, rt


def omcode(la, ra, lb, rb):
    vals = sorted(set((la, ra, lb, rb)))
    rk = {v: i for i, v in enumerate(vals)}
    return (rk[la], rk[ra], rk[lb], rk[rb])


def init_rows(n):
    rows = []
    SH = {7: O.shapes_of(list(range(1, 8))),
          8: O.shapes_of(list(range(1, 9))),
          9: O.shapes_of(list(range(1, 10)))}
    D = json.loads(CERT.read_text())
    for i, it in enumerate(D["items"]):
        A, B = shift(it["A"]), shift(it["B"])
        x = it["key"] + 1
        mo = "K" if it["mode"] == "KEEP" else "D"
        h, b = edge_row(A, B, x, mo, 8)
        rows.append({"M": {str(k): v for k, v in h.items()}, "b": b,
                     "tag": "cert%d" % i,
                     "wit": {"n": 8, "A": A, "B": B, "x": x, "mo": mo}})
    wit8 = [(457, 429, 8, "K"), (1091, 1003, 7, "K"), (869, 910, 2, "K"),
            (1093, 1003, 7, "K"), (90, 2, 8, "K"), (255, 2, 8, "K"),
            (1001, 1359, 1, "K"), (1003, 1359, 1, "K"), (480, 560, 3, "K"),
            (581, 598, 6, "K"), (786, 785, 8, "K"), (1175, 1429, 1, "K"),
            (160, 358, 2, "K"), (651, 649, 6, "K"), (581, 602, 4, "K"),
            (496, 560, 3, "K"), (0, 89, 3, "K")]
    for (ia, ib, x, mo) in wit8:
        h, b = edge_row(SH[8][ia], SH[8][ib], x, mo, 8)
        rows.append({"M": {str(k): v for k, v in h.items()}, "b": b,
                     "tag": "wit8-%d-%d-%d" % (ia, ib, x),
                     "wit": {"n": 8, "A": SH[8][ia], "B": SH[8][ib],
                             "x": x, "mo": mo}})
    bat7 = [(109, 0, 7, "K", "S4a1"), (0, 0, 7, "K", "S4a3"),
            (110, 0, 7, "K", "S2nv"), (48, 0, 7, "K", "ACTL"),
            (0, 243, 1, "K", "recharge"), (0, 428, 1, "K", "tw03"),
            (0, 41, 3, "K", "tw13")]
    for (ia, ib, x, mo, tag) in bat7:
        h, b = edge_row(SH[7][ia], SH[7][ib], x, mo, 7)
        rows.append({"M": {str(k): v for k, v in h.items()}, "b": b,
                     "tag": tag,
                     "wit": {"n": 7, "A": SH[7][ia], "B": SH[7][ib],
                             "x": x, "mo": mo}})
    h, b = edge_row(SH[9][3432], SH[9][0], 9, "K", 9)
    rows.append({"M": {str(k): v for k, v in h.items()}, "b": b,
                 "tag": "PR904",
                 "wit": {"n": 9, "A": SH[9][3432], "B": SH[9][0],
                         "x": 9, "mo": "K"}})
    G = json.loads((ROOT / "artifacts" / "v04" / "wp6_present" /
                    "0909c74a" / "dual_mine" /
                    "joint_grow.json").read_text())["rows"]
    for r in G:
        h, b = edge_row(r["A"], r["B"], r["x"], r["mo"], r["n"])
        rows.append({"M": {str(k): v for k, v in h.items()}, "b": b,
                     "tag": r["tag"],
                     "wit": {"n": r["n"], "A": r["A"], "B": r["B"],
                             "x": r["x"], "mo": r["mo"]}})
    return rows


def solve_lp(rows):
    # Pure max-slack (NO margin row: the grown system is marginally feasible;
    # a uniform delta overconstrains. Exactness handled at finalization.)
    import numpy as np
    from scipy.optimize import linprog
    from scipy.sparse import csr_matrix
    var = {}
    for r in rows:
        for e in r["M"]:
            if e not in var:
                var[e] = len(var)
    E, Vv = len(rows), len(var)
    # rows: -M g + t <= -b
    rd, cd, vd = [], [], []
    for i, r in enumerate(rows):
        for e, c in r["M"].items():
            rd.append(i)
            cd.append(var[e])
            vd.append(-float(c))
        rd.append(i)
        cd.append(Vv)
        vd.append(1.0)
    Aub = csr_matrix((np.array(vd, dtype=float),
                      (np.array(rd), np.array(cd))),
                     shape=(E, Vv + 1))
    bub = np.array([float(-r["b"]) for r in rows])
    c = np.zeros(Vv + 1)
    c[-1] = -1.0
    res = linprog(c, A_ub=Aub, b_ub=bub,
                  bounds=[(None, None)] * Vv + [(None, 1e6)],
                  method="highs")
    return res, var


def scan(n, Sh, Atrans, Btrans, dd, lo, hi, sz, rt, g, K, active_sigs):
    import heapq
    nS = len(Sh)
    A2t = [[0] * (n + 1) for _ in range(nS)]
    At = [[0] * (n + 1) for _ in range(nS)]
    B2t = [[0] * (n + 1) for _ in range(nS)]
    for ia in range(nS):
        for x in range(1, n + 1):
            ia2, a = Atrans[(ia, x)]
            assert a == (dd[ia].get(x, 0) + 1) // 2
            A2t[ia][x] = ia2
            At[ia][x] = a
            B2t[ia][x] = Btrans[(ia, x)][0]
    heap = []
    checked = 0
    nviol = 0
    maxdef = 0.0
    get = g.get
    for ia in range(nS):
        ra = rt[ia]
        for ib in range(nS):
            rb = rt[ib]
            twu = 1 if ra == rb else 0
            for x in range(1, n + 1):
                a = At[ia][x]
                ia2 = A2t[ia][x]
                # DELETE
                twd = 1 if rt[ia2] == rb else 0
                bd = -2 * a - 2 * (twd - twu)
                d = {}
                for y in range(1, n + 1):
                    oa = omcode(lo[(ia, y)], hi[(ia, y)], lo[(ib, y)],
                                hi[(ib, y)])
                    ob = omcode(lo[(ia2, y)], hi[(ia2, y)], lo[(ib, y)],
                                hi[(ib, y)])
                    e0 = (dd[ia][y], dd[ib][y], sz[(ia, y)], sz[(ib, y)], oa)
                    e1 = (dd[ia2][y], dd[ib][y], sz[(ia2, y)], sz[(ib, y)],
                          ob)
                    if e0 != e1:
                        d[e0] = d.get(e0, 0) + 1
                        d[e1] = d.get(e1, 0) - 1
                sig = (frozenset(d.items()), bd)
                if sig not in active_sigs:
                    lh = 0.0
                    for e, c in d.items():
                        lh += get(e, 0.0) * c
                    if lh < bd - 1e-4:
                        nviol += 1
                        if bd - lh > maxdef:
                            maxdef = bd - lh
                        if len(heap) < K:
                            heapq.heappush(heap, (bd - lh, ia, ib, x, "D",
                                                  d, bd))
                        else:
                            heapq.heappushpop(heap, (bd - lh, ia, ib, x,
                                                     "D", d, bd))
                checked += 1
                # KEEP
                ib2 = B2t[ib][x]
                q = dd[ib][x] // 2
                twk = 1 if rt[ia2] == rt[ib2] else 0
                bk = q - 2 * a - 2 * (twk - twu)
                d = {}
                for y in range(1, n + 1):
                    oa = omcode(lo[(ia, y)], hi[(ia, y)], lo[(ib, y)],
                                hi[(ib, y)])
                    ob = omcode(lo[(ia2, y)], hi[(ia2, y)], lo[(ib2, y)],
                                hi[(ib2, y)])
                    e0 = (dd[ia][y], dd[ib][y], sz[(ia, y)], sz[(ib, y)], oa)
                    e1 = (dd[ia2][y], dd[ib2][y], sz[(ia2, y)],
                          sz[(ib2, y)], ob)
                    if e0 != e1:
                        d[e0] = d.get(e0, 0) + 1
                        d[e1] = d.get(e1, 0) - 1
                sig = (frozenset(d.items()), bk)
                if sig not in active_sigs:
                    lh = 0.0
                    for e, c in d.items():
                        lh += get(e, 0.0) * c
                    if lh < bk - 1e-4:
                        nviol += 1
                        if bk - lh > maxdef:
                            maxdef = bk - lh
                        if len(heap) < K:
                            heapq.heappush(heap, (bk - lh, ia, ib, x, "K",
                                                  d, bk))
                        else:
                            heapq.heappushpop(heap, (bk - lh, ia, ib, x,
                                                     "K", d, bk))
                checked += 1
        if (ia + 1) % 60 == 0:
            step("SC", "n=%d %d/%d heap=%d" % (n, ia + 1, nS, len(heap)))
    # dedupe within batch by signature
    out, seen = [], set()
    for item in sorted(heap, reverse=True):
        _, ia, ib, x, mo, d, b = item
        sig = (frozenset(d.items()), b)
        if sig in seen or sig in active_sigs:
            continue
        seen.add(sig)
        out.append((ia, ib, x, mo, d, b))
    return out, checked, nviol, maxdef


def main():
    import sys as _s
    n = int(_s.argv[1]) if len(_s.argv) > 1 else 7
    maxit = int(_s.argv[2]) if len(_s.argv) > 2 else 3
    K = int(_s.argv[3]) if len(_s.argv) > 3 else 400
    SP = (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" /
          "dual_mine" / ("joint_cut%d.json" % n))
    if SP.exists():
        st = json.loads(SP.read_text())
        rows, done, log = st["rows"], st["iters_done"], st["log"]
        step("L", "resumed n=%d rows=%d iters=%d" % (n, len(rows), done))
    else:
        rows = init_rows(n)
        done, log = 0, []
        step("L", "init n=%d rows=%d" % (n, len(rows)))
    Sh = O.shapes_of(list(range(1, n + 1)))
    nS = len(Sh)
    D = __import__("pickle").load(open(str(ROOT / "artifacts" / "v04" /
                                            "wp6_present" / "0909c74a" /
                                            ("trans%d.pkl" % n)), "rb"))
    Atrans, Btrans = D["Atrans"], D["Btrans"]
    # trans9 has no Sh; shapes_of order validated (200/200 replays + asserts)
    ptrs = [V.to_ptr(copy.deepcopy(s)) for s in Sh]
    rt = {}
    dd = {}
    for ia in range(nS):
        r = ptrs[ia]
        while r["p"] is not None:
            r = r["p"]
        rt[ia] = r["k"]
        dd[ia] = V.depths_of(ptrs[ia])
    _, lo, hi, sz, _ = shapes_info(Sh, n)
    for it in range(maxit):
        res, var = solve_lp(rows)
        if res.status == 2:
            st = {"rows": rows, "iters_done": done, "status":
                  "LP-INFEASIBLE-FLOAT", "log": log + ["infeasible@%d" %
                                                      done]}
            SP.write_text(json.dumps(st, indent=1, default=str),
                          encoding="utf-8")
            step("LP", "INFEASIBLE float (rows=%d). Exact Farkas due." %
                 len(rows))
            return 2
        assert res.status == 0, res.status
        g = {e: res.x[i] for e, i in var.items()}
        tstar = -res.fun
        active_sigs = set()
        for r in rows:
            active_sigs.add((frozenset((eval(k), v)
                                       for k, v in r["M"].items()), r["b"]))
        new, checked, nviol, maxdef = scan(n, Sh, Atrans, Btrans, dd, lo,
                                            hi, sz, rt, g, K, active_sigs)
        step("IT", "iter=%d t*=%.4g checked=%d viol=%d maxdef=%.3g newcuts=%d"
                  " rows=%d->%d" %
             (done, tstar, checked, nviol, maxdef, len(new), len(rows),
              len(rows) + len(new)))
        log.append({"iter": done, "t": float(tstar), "checked": checked,
                    "viol": nviol, "maxdef": maxdef, "new": len(new),
                    "rows": len(rows) + len(new), "vars": len(var)})
        if not new:
            st = {"rows": rows, "iters_done": done + 1, "status":
                  "FEASIBLE-SCAN", "log": log,
                  "checked": checked,
                  "expected": nS * nS * n * 2}
            assert checked == nS * nS * n * 2, checked
            SP.write_text(json.dumps(st, indent=1, default=str),
                          encoding="utf-8")
            step("IT", "NO VIOLATION in complete graph: FEASIBLE-SCAN")
            return 0
        for (ia, ib, x, mo, d, b) in new:
            rows.append({"M": {str(k): v for k, v in d.items()}, "b": b,
                         "tag": "cut%d-%d" % (done, len(rows)),
                         "wit": {"n": n, "ia": ia, "ib": ib, "x": x,
                                 "mo": mo}})
        done += 1
        st = {"rows": rows, "iters_done": done, "status": "PROGRESS",
              "log": log}
        SP.write_text(json.dumps(st, indent=1, default=str), encoding="utf-8")
    step("L", "call budget exhausted: iters=%d rows=%d status=PROGRESS" %
         (done, len(rows)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

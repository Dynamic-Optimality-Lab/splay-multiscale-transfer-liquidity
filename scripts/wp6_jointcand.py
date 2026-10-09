"""PIVOT-25R-U §7 attempt R1: TOTAL majority-list evaluator.

G(eta) = majority LP value on cell (sgn(dB-2dA), omega); unobserved cells
and ties -> 0. Explicit, total (defined on every valid eta), state-based.
Verified EXACTLY on all rows (cert + witnesses + battery + grow).
A failure refutes THIS candidate (not the template).
"""
from __future__ import annotations
import sys
import json
from pathlib import Path
from collections import Counter, defaultdict

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_jointlp import edge_row, shift
import wp6_cycle_ratio as O

CERT = Path("C:/Users/SAIFMA~1/AppData/Local/Temp/opencode/jointcert/"
            "joint_depth_template_countercertificate.json")


def step(sid, msg):
    print("[JCR1 %s] %s" % (sid, msg), flush=True)


def sgn(z):
    return 1 if z > 0 else (-1 if z < 0 else 0)


def main():
    SH = {7: O.shapes_of(list(range(1, 8))),
          8: O.shapes_of(list(range(1, 9))),
          9: O.shapes_of(list(range(1, 10)))}
    G = json.load(open(str(ROOT / "artifacts" / "v04" / "wp6_present" /
                           "0909c74a" / "dual_mine" /
                           "joint_g_minmax.json")))["g"]
    V = {eval(k): v for k, v in G.items()}
    cells = defaultdict(Counter)
    for e, v in V.items():
        cells[(sgn(e[1] - 2 * e[0]), e[4])][v] += 1
    TAB = {}
    for c, ct in cells.items():
        top = ct.most_common()
        TAB[str(c)] = top[0][0] if len(top) == 1 or \
            top[0][1] > top[1][1] else "0"
    step("T", "table cells=%d" % len(TAB))

    def Gfun(eta):
        return TAB.get(str((sgn(eta[1] - 2 * eta[0]), eta[4])), "0")

    def FQ(s):
        from fractions import Fraction
        return Fraction(s)

    edges = []
    D = json.loads(CERT.read_text())
    for it in D["items"]:
        A, B = shift(it["A"]), shift(it["B"])
        x = it["key"] + 1
        mo = "K" if it["mode"] == "KEEP" else "D"
        edges.append((A, B, x, mo, 8, "cert"))
    for (ia, ib, x, mo) in [(457, 429, 8, "K"), (1091, 1003, 7, "K"),
                            (869, 910, 2, "K"), (1093, 1003, 7, "K"),
                            (90, 2, 8, "K"), (255, 2, 8, "K"),
                            (1001, 1359, 1, "K"), (1003, 1359, 1, "K"),
                            (480, 560, 3, "K"), (581, 598, 6, "K"),
                            (786, 785, 8, "K"), (1175, 1429, 1, "K"),
                            (160, 358, 2, "K"), (651, 649, 6, "K"),
                            (581, 602, 4, "K"), (496, 560, 3, "K"),
                            (0, 89, 3, "K")]:
        edges.append((SH[8][ia], SH[8][ib], x, mo, 8, "wit8"))
    for (ia, ib, x, mo, tag) in [(109, 0, 7, "K", "S4a1"),
                                (0, 0, 7, "K", "S4a3"),
                                (110, 0, 7, "K", "S2nv"),
                                (48, 0, 7, "K", "ACTL"),
                                (0, 243, 1, "K", "recharge"),
                                (0, 428, 1, "K", "tw03"),
                                (0, 41, 3, "K", "tw13")]:
        edges.append((SH[7][ia], SH[7][ib], x, mo, 7, tag))
    edges.append((SH[9][3432], SH[9][0], 9, "K", 9, "PR904"))
    Grows = json.loads((ROOT / "artifacts" / "v04" / "wp6_present" /
                        "0909c74a" / "dual_mine" /
                        "joint_grow.json").read_text())["rows"]
    for r in Grows:
        edges.append((r["A"], r["B"], r["x"], r["mo"], r["n"], r["tag"]))
    import wp6_overflow as Vmod
    import copy
    bad = 0
    first = None
    for (A, B, x, mo, n, tag) in edges:
        rep = Vmod.replay(A, B, [(mo, x)])
        acc = rep["accesses"][0]
        w = (acc["q"] - 2 * acc["a"]) if mo == "K" else -2 * acc["a"]
        t0 = 1 if A[0] == B[0] else 0
        t1 = 1 if rep["endA"][0] == rep["endB"][0] else 0
        from wp6_jointlp import eta_of
        p0 = -2 * t0 + sum(FQ(Gfun(eta_of(A, B, y))) for y in range(1, n + 1))
        p1 = -2 * t1 + sum(FQ(Gfun(eta_of(rep["endA"], rep["endB"], y)))
                           for y in range(1, n + 1))
        if p0 - p1 < w:
            bad += 1
            if first is None:
                first = (tag, n, x, mo, acc["a"], acc["q"], w, p0 - p1)
    step("V", "R1 majority-list: %d/%d violated %s" % (bad, len(edges), first))
    Path(str(ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" /
             "dual_mine" / "joint_cand_r1.json")).write_text(
        json.dumps({"fails": bad, "of": len(edges), "first": first,
                    "table_cells": len(TAB)}, indent=1, default=str),
        encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

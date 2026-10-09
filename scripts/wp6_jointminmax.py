"""Min-max magnitude probe for the joint-context template (exploratory float).

minimize U s.t. M g >= b, -U <= g <= U. Small optimum suggests compactness;
huge optimum says even 67 edges force wild coefficients.
"""
from __future__ import annotations
import sys
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_jointlp import edge_row, shift
import wp6_cycle_ratio as O

CERT = Path("C:/Users/SAIFMA~1/AppData/Local/Temp/opencode/jointcert/"
            "joint_depth_template_countercertificate.json")


def main():
    import numpy as np
    from scipy.optimize import linprog
    SH = {7: O.shapes_of(list(range(1, 8))),
          8: O.shapes_of(list(range(1, 9))),
          9: O.shapes_of(list(range(1, 10)))}
    rows = []
    D = json.loads(CERT.read_text())
    for it in D["items"]:
        A, B = shift(it["A"]), shift(it["B"])
        x = it["key"] + 1
        mo = "K" if it["mode"] == "KEEP" else "D"
        h, b = edge_row(A, B, x, mo, 8)
        rows.append((h, b))
    for (ia, ib, x, mo) in [(457, 429, 8, "K"), (1091, 1003, 7, "K"),
                            (869, 910, 2, "K"), (1093, 1003, 7, "K"),
                            (90, 2, 8, "K"), (255, 2, 8, "K"),
                            (1001, 1359, 1, "K"), (1003, 1359, 1, "K"),
                            (480, 560, 3, "K"), (581, 598, 6, "K"),
                            (786, 785, 8, "K"), (1175, 1429, 1, "K"),
                            (160, 358, 2, "K"), (651, 649, 6, "K"),
                            (581, 602, 4, "K"), (496, 560, 3, "K"),
                            (0, 89, 3, "K")]:
        h, b = edge_row(SH[8][ia], SH[8][ib], x, mo, 8)
        rows.append((h, b))
    for (ia, ib, x, mo) in [(109, 0, 7, "K"), (0, 0, 7, "K"),
                            (110, 0, 7, "K"), (48, 0, 7, "K"),
                            (0, 243, 1, "K"), (0, 428, 1, "K"),
                            (0, 41, 3, "K")]:
        h, b = edge_row(SH[7][ia], SH[7][ib], x, mo, 7)
        rows.append((h, b))
    h, b = edge_row(SH[9][3432], SH[9][0], 9, "K", 9)
    rows.append((h, b))
    G = json.loads((ROOT / "artifacts" / "v04" / "wp6_present" /
                    "0909c74a" / "dual_mine" /
                    "joint_grow.json").read_text())["rows"]
    for r in G:
        h, b = edge_row(r["A"], r["B"], r["x"], r["mo"], r["n"])
        rows.append((h, b))
    var = {}
    for h, _ in rows:
        for e in h:
            if e not in var:
                var[e] = len(var)
    Vv, E = len(var), len(rows)
    M = np.zeros((E, Vv))
    bv = np.zeros(E)
    for i, (h, b) in enumerate(rows):
        for e, c in h.items():
            M[i, var[e]] = c
        bv[i] = b
    # minimize U: vars (g, U); -M g <= -b; g-U <= 0; -g-U <= 0
    c = np.zeros(Vv + 1)
    c[-1] = 1.0
    import numpy as _np
    A1 = _np.zeros((E, Vv + 1))
    A1[:, :-1] = -M
    A2 = _np.zeros((Vv, Vv + 1))
    A2[:, :-1] = _np.eye(Vv)
    A2[:, -1] = -1.0
    A3 = _np.zeros((Vv, Vv + 1))
    A3[:, :-1] = -_np.eye(Vv)
    A3[:, -1] = -1.0
    Aub = _np.vstack([A1, A2, A3])
    bub = _np.concatenate([-bv, _np.zeros(2 * Vv)])
    res = linprog(c, A_ub=Aub, b_ub=bub,
                  bounds=[(None, None)] * Vv + [(0, None)], method="highs")
    print("[JMM] status=%s minmax|g|=%s" % (res.status, res.fun
                                           if res.success else None))
    if res.success:
        from fractions import Fraction
        g = [Fraction(x).limit_denominator(36) for x in res.x[:-1]]
        inv = list(var)
        bad = 0
        worst = None
        for i, (h, b) in enumerate(rows):
            lhs = sum(g[var[e]] * c for e, c in h.items())
            if lhs < b:
                bad += 1
                worst = (i, lhs, b)
        print("[JMM] exact (den<=36) violations: %d/%d %s" %
              (bad, len(rows), worst))
        if bad == 0:
            Path(str(ROOT / "artifacts" / "v04" / "wp6_present" /
                     "0909c74a" / "dual_mine" /
                     "joint_g_minmax.json")).write_text(
                json.dumps({"g": {str(inv[v]): str(g[v])
                                  for v in range(Vv)}}, indent=1))
            print("[JMM] saved joint_g_minmax.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())

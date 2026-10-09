"""PIVOT-25R L2 transfer: test compact Phi(s)=-2*twin(s)-[B non-vine] on ALL n=8
concrete edges (32.7M). Reports bad count + violation classes + witnesses."""
from __future__ import annotations
import sys
import copy
import json
import pickle
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
import wp6_overflow as V
import wp6_cycle_ratio as O


def step(sid, msg):
    print("[L2T %s] %s" % (sid, msg), flush=True)


def main():
    n = 8
    D = pickle.load(open(str(ROOT / "artifacts" / "v04" / "wp6_present" /
                             "0909c74a" / "trans8.pkl"), "rb"))
    Sh, nS, Atrans, Btrans = D["Sh"], D["nS"], D["Atrans"], D["Btrans"]
    assert nS == len(Sh) == 1430, nS
    ptrs = [V.to_ptr(copy.deepcopy(s)) for s in Sh]
    rt = [0] * nS
    vb = [0] * nS
    A2 = [[0] * (n + 1) for _ in range(nS)]
    AA = [[0] * (n + 1) for _ in range(nS)]
    B2 = [[0] * (n + 1) for _ in range(nS)]
    QQ = [[0] * (n + 1) for _ in range(nS)]
    for ia in range(nS):
        r = ptrs[ia]
        while r["p"] is not None:
            r = r["p"]
        rt[ia] = r["k"]
        dd = V.depths_of(ptrs[ia])
        # vine test inline
        st = [Sh[ia]]
        vn = True
        while st:
            nd = st.pop()
            if nd is None:
                continue
            if nd[1] is not None and nd[2] is not None:
                vn = False
                break
            st.append(nd[1])
            st.append(nd[2])
        vb[ia] = 1 if vn else 0
        for x in range(1, n + 1):
            ia2, a = Atrans[(ia, x)]
            assert a == (dd.get(x, 0) + 1) // 2, (ia, x)
            A2[ia][x] = ia2
            AA[ia][x] = a
            B2[ia][x] = Btrans[(ia, x)][0]
            QQ[ia][x] = dd.get(x, 0) // 2
    step("T", "shapes=%d vines=%d tables ok" % (nS, sum(vb)))
    rtL, vbL = rt, vb
    bad = 0
    checked = 0
    vc = Counter()
    ex = []
    for ia in range(nS):
        ra = rtL[ia]
        A2ia, AAia = A2[ia], AA[ia]
        for ib in range(nS):
            rb = rtL[ib]
            vbb = vbL[ib]
            phi = (-2 if ra == rb else 0) - (0 if vbb else 1)
            B2ib, QQib = B2[ib], QQ[ib]
            for x in range(1, n + 1):
                a = AAia[x]
                ia2 = A2ia[x]
                ra2 = rtL[ia2]
                phiD = (-2 if ra2 == rb else 0) - (0 if vbb else 1)
                if -2 * a > phi - phiD:
                    bad += 1
                    vc[(a, 0, -2 * a, phi - phiD, "D")] += 1
                    if len(ex) < 5:
                        ex.append({"ia": ia, "ib": ib, "x": x, "mode": "D",
                                   "a": a, "w": -2 * a, "drop": phi - phiD,
                                   "roots": [ra, rb], "proots": [ra2, rb],
                                   "vineB": vbb})
                checked += 1
                ib2 = B2ib[x]
                q = QQib[x]
                phiK = (-2 if ra2 == rtL[ib2] else 0) - \
                    (0 if vbL[ib2] else 1)
                if q - 2 * a > phi - phiK:
                    bad += 1
                    vc[(a, q, q - 2 * a, phi - phiK, "K")] += 1
                    if len(ex) < 5:
                        ex.append({"ia": ia, "ib": ib, "x": x, "mode": "K",
                                   "a": a, "q": q, "w": q - 2 * a,
                                   "drop": phi - phiK,
                                   "roots": [ra, rb],
                                   "proots": [ra2, rtL[ib2]],
                                   "vineB": [vbb, vbL[ib2]]})
                checked += 1
        if (ia + 1) % 130 == 0:
            step("G", "%d/%d bad=%d" % (ia + 1, nS, bad))
    step("G", "checked=%d bad=%d classes=%s" % (checked, bad, dict(vc)))
    out = {"n": n, "formula": "Phi=-2*twin-[B non-vine]", "checked": checked,
           "bad": bad, "classes": {str(k): v for k, v in vc.items()},
           "examples": ex}
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" /
     "dual_mine" / "l2_transfer8.json").write_text(
        json.dumps(out, indent=1, default=str), encoding="utf-8")
    step("S", "wrote dual_mine/l2_transfer8.json CERT=%s" %
         ("GREEN" if bad == 0 else "RED"))
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

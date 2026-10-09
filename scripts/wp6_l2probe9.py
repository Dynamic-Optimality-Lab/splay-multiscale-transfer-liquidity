"""PIVOT-25R n=9 probe: test compact Phi=-2*twin-[B non-vine] ONLY on q>=4
KEEP edges (targeted; full 425M scan infeasible here). Any violation refutes
the bounded-payment family at n=9 with exact witnesses."""
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
    print("[L2P %s] %s" % (sid, msg), flush=True)


def main():
    n = 9
    D = pickle.load(open(str(ROOT / "artifacts" / "v04" / "wp6_present" /
                             "0909c74a" / "trans9.pkl"), "rb"))
    step("K", "keys=%s" % sorted(D.keys()))
    Sh, nS, Atrans, Btrans = O.build(n)["Sh"], None, D["Atrans"], D["Btrans"]
    nS = len(Sh)
    assert nS == 4862, nS
    import json as _J
    _idx = {_J.dumps(s, sort_keys=True): i for i, s in enumerate(Sh)}

    def _shape_of(P):
        return _idx[_J.dumps(list(O.enc_ptr(P)), sort_keys=True)]

    import random as _R
    _rng = _R.Random(25)
    _samp = [(_rng.randrange(nS), _rng.randint(1, n)) for _ in range(200)]
    ptrs = [V.to_ptr(copy.deepcopy(s)) for s in Sh]
    # ordering consistency: 200 sample replays vs trans9 targets
    for (ia, x) in _samp:
        A2 = copy.deepcopy(ptrs[ia])
        A2, _st = V.splay_cap(A2, x, 0, [])
        assert _shape_of(A2) == Atrans[(ia, x)][0], (ia, x)
        B2 = copy.deepcopy(ptrs[ia])
        B2, _st = V.splay_cap(B2, x, 0, [])
        assert _shape_of(B2) == Btrans[(ia, x)][0], (ia, x)
    step("T", "shapes=%d (O.build; 200/200 sample replays match trans9)" % nS)
    rt = [0] * nS
    vb = [0] * nS
    DD = [[0] * (n + 1) for _ in range(nS)]
    for ia in range(nS):
        r = ptrs[ia]
        while r["p"] is not None:
            r = r["p"]
        rt[ia] = r["k"]
        dd = V.depths_of(ptrs[ia])
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
            DD[ia][x] = dd.get(x, 0)
    # qualifying B-moves: q>=4
    qual = []
    for ib in range(nS):
        for x in range(1, n + 1):
            if DD[ib][x] // 2 >= 4:
                ib2, _ = Btrans[(ib, x)]
                qual.append((ib, x, ib2, DD[ib][x] // 2))
    step("Q", "qualifying B-moves (q>=4): %d" % len(qual))
    bad = 0
    checked = 0
    vc = Counter()
    ex = []
    for (ib, x, ib2, q) in qual:
        rb = rt[ib]
        vbb = vb[ib]
        rb2 = rt[ib2]
        vbb2 = vb[ib2]
        for ia in range(nS):
            ra = rt[ia]
            dA = DD[ia][x]
            a = (dA + 1) // 2
            ia2, aa = Atrans[(ia, x)]
            assert aa == a, (ia, x)
            phi = (-2 if ra == rb else 0) - (0 if vbb else 1)
            ra2 = rt[ia2]
            phiK = (-2 if ra2 == rb2 else 0) - (0 if vbb2 else 1)
            if q - 2 * a > phi - phiK:
                bad += 1
                vc[(a, q, q - 2 * a, phi - phiK,
                    1 if ra == rb else 0, 1 if ra2 == rb2 else 0,
                    vbb, vbb2)] += 1
                if len(ex) < 8:
                    ex.append({"ia": ia, "ib": ib, "x": x, "a": a, "q": q,
                               "w": q - 2 * a, "drop": phi - phiK,
                               "roots": [ra, rb], "proots": [ra2, rb2],
                               "vineB": [vbb, vbb2],
                               "dA": dA, "dB": DD[ib][x]})
            checked += 1
    step("G", "checked=%d bad=%d classes=%s" % (checked, bad, dict(vc)))
    out = {"n": n, "formula": "Phi=-2*twin-[B non-vine]",
           "scope": "KEEP edges with q>=4 only", "qualifying": len(qual),
           "checked": checked, "bad": bad,
           "classes": {str(k): v for k, v in vc.items()}, "examples": ex}
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" /
     "dual_mine" / "l2_probe9.json").write_text(
        json.dumps(out, indent=1, default=str), encoding="utf-8")
    step("S", "wrote dual_mine/l2_probe9.json CERT=%s" %
         ("GREEN" if bad == 0 else "RED"))
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

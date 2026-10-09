"""J-side mass slopes from shared-J4 L1 quotient representative (diagnostic).
- c(s) s-dependence; sibling-lambda s-independence per fine class;
- total CJ slopes per row class; sigmaJ(K2)-sigmaJ(K3);
- full-H boundary Gamma at s=0/1 with LP J (width check, finite evidence).
Usage: python scripts/wp6_jslope.py
"""
import sys, copy, json
from pathlib import Path
from collections import defaultdict
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_staticR import depths_list, path_nodes, R_static
from wp6_lambda import R_coeffs
import importlib.util
def load(name):
    spec = importlib.util.spec_from_file_location(name, str(ROOT / 'scripts' / (name + '.py')))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m
j4 = load('wp6_j4shared')
import wp6_cycle_ratio as O
OUT = ROOT / "artifacts/v04/wp6_present/0909c74a/dual_mine"

def shift(T, s):
    if T is None:
        return None
    return [T[0] + s, shift(T[1], s), shift(T[2], s)]

def subsize(T, x):
    nd = T
    while nd is not None and nd[0] != x:
        nd = nd[1] if x < nd[0] else nd[2]
    c = [0]
    def go(m):
        if m is None:
            return
        c[0] += 1; go(m[1]); go(m[2])
    go(nd); return c[0]

def H0(T, y, n, ka=4.0):
    return -R_static(T, y) + ka * (n - subsize(T, y))

def Jy(B, y, J):
    """Total J4 row charge from value dict J (keys str)."""
    _, lam = R_coeffs(B, y)
    dB = depths_list(B)
    tot = 0.0
    for z in dB:
        if z == y:
            continue
        s_ = j4.slot_of(B, y, z)
        key = str(('t', (s_, lam.get(z, 0), dB[z] - dB[y], dB[y])))
        tot += J.get(key, 0.0)
    c, _ = R_coeffs(B, y)
    tot += J.get(str(('r', c)), 0.0)
    return tot

def main():
    rep = {}
    J = dict(json.load(open(OUT / "j4shared_567_l1.json"))["vals"])
    # gauge zeros from solver: which keys are fixed? (NONE,0,-1,1)=0? check
    print("[JS] loaded LP vals:", len(J), flush=True)
    # 1. c(s) dependence for fixed (T,y)
    t = 3
    T = O.shapes_of(list(range(1, t + 1)))[0]
    for y in (1, 2, 3):
        cs = []
        for s in (1, 2, 3, 4):
            S0 = O.shapes_of(list(range(1, s + 1)))[0]
            B = [t + 1, copy.deepcopy(T), shift(copy.deepcopy(S0), t + 1)]
            cs.append(R_coeffs(B, y)[0])
        print(f"[JS] c(s=1..4) y={y}: {cs}", flush=True)
    # 2. sibling lambda by (parity,sx,s)
    sib = defaultdict(set)
    for t in (2, 3, 4):
        for s in (1, 2, 3, 4):
            for T in O.shapes_of(list(range(1, t + 1)))[:20]:
                S0 = O.shapes_of(list(range(1, s + 1)))[0]
                B = [t + 1, copy.deepcopy(T), shift(copy.deepcopy(S0), t + 1)]
                for y in range(1, t + 1):
                    Py = path_nodes(T, y); d = len(Py) - 1
                    sx = None if d == 0 else (0 if Py[0][1] is Py[1] else 1)
                    _, lam = R_coeffs(B, y)
                    for z in range(t + 2, t + 2 + s):
                        sib[(d % 2, sx, s)].add(lam.get(z, 0))
    nonuni = {k: v for k, v in sib.items() if len(v) > 1}
    print(f"[JS] sibling-lambda classes: {len(sib)}, non-singleton: {len(nonuni)}", flush=True)
    for k in sorted(nonuni, key=str)[:10]:
        print(f"    {k}: {sorted(nonuni[k])}", flush=True)
    rep["siblam_nonuni"] = len(nonuni)
    # 3. total CJ slopes per class (sp=0 Ext_L), s=1..4
    slopes = defaultdict(list)
    for t in (2, 3, 4):
        for T in O.shapes_of(list(range(1, t + 1))):
            for y in range(1, t + 1):
                Py = path_nodes(T, y); d = len(Py) - 1
                sx = None if d == 0 else (0 if Py[0][1] is Py[1] else 1)
                vals = []
                for s in (1, 2, 3, 4):
                    S0 = O.shapes_of(list(range(1, s + 1)))[0]
                    B = [t + 1, copy.deepcopy(T), shift(copy.deepcopy(S0), t + 1)]
                    vals.append(Jy(B, y, J))
                sl = [round(vals[i + 1] - vals[i], 6) for i in range(3)]
                # K-class: K2 iff odd and sx matches outer side (sp=0 -> sx=0)
                K = "K2" if (d % 2 == 1 and sx == 0) else "K3"
                slopes[K].append(tuple(sl))
    for K in ("K2", "K3"):
        flat = defaultdict(int)
        for sl in slopes[K]:
            flat[sl] += 1
        print(f"[JS] CJ slopes {K} (n={len(slopes[K])}): {dict(list(flat.items())[:8])}", flush=True)
    # slope difference K2-K3 on matched contexts? report means
    import statistics as st
    for K in ("K2", "K3"):
        allsl = [x for sl in slopes[K] for x in sl]
        print(f"[JS] {K} mean slope={st.mean(allsl):.4f} (n={len(allsl)})", flush=True)
    rep["cj_slope_n"] = {K: len(slopes[K]) for K in slopes}
    # 4. full-H boundary Gamma at s=1 with LP J: width check over corpus t<=4
    viol = totp = 0
    worst = None
    for t in (2, 3, 4):
        for T in O.shapes_of(list(range(1, t + 1))):
            S0 = O.shapes_of(list(range(1, 2)))[0]
            B = [t + 1, copy.deepcopy(T), shift(copy.deepcopy(S0), t + 1)]
            nB = t + 2
            H = {}
            for y in range(1, t + 1):
                H[y] = H0(B, y, nB) + Jy(B, y, J)
            for u in range(1, t + 1):
                for v in range(1, t + 1):
                    if u == v:
                        continue
                    totp += 1
                    dd = H[u] - H[v]
                    if abs(dd) > 2 + 1e-6:
                        viol += 1
                        if worst is None or abs(dd) > abs(worst[0]):
                            worst = (dd, t, u, v)
    print(f"[JS] full-H(s=1,LP-J) same-child |diff|>2: {viol}/{totp} worst={worst}", flush=True)
    rep["width_viol"] = {"viol": viol, "tot": totp, "worst": worst}
    json.dump(rep, open(OUT / "j4_jslope.json", "w"), indent=1, default=str)
    print("[JS] saved", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())

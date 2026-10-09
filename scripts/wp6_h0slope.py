"""H0 slope universality: sigma0/alpha_R by (sp,parity,sx); alpha_R == f_top identity;
extend to total size <=7. Usage: python scripts/wp6_h0slope.py
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

def main():
    rep = {}
    # slope by (sp,parity,sx): use vine S of sizes s,s+1 to measure discrete slope
    tab = defaultdict(set)
    ident_ok = ident_tot = 0
    ident_bad = []
    for t in (1, 2, 3, 4, 5):
        for s in (1, 2, 3):
            if t + 1 + (s + 1) > 7:
                continue
            for T in O.shapes_of(list(range(1, t + 1))):
                S0 = O.shapes_of(list(range(1, s + 1)))[0]
                S1 = O.shapes_of(list(range(1, s + 2)))[0]
                for sp, mk in ((0, lambda T, S: [t + 1, copy.deepcopy(T), shift(copy.deepcopy(S), t + 1)]),
                               (1, lambda T, S: [s + 10, shift(copy.deepcopy(S), 0), shift(copy.deepcopy(T), s + 10)])):
                    # NOTE sp=1 construction below remapped; simpler: Ext_L (sp=0 for T) and Ext_R (sp=1 for T)
                    pass
                for tag, spv in (("L", 0), ("R", 1)):
                    for SS, slab in ((S0, s), (S1, s + 1)):
                        pass
                    B0 = [t + 1, copy.deepcopy(T), shift(copy.deepcopy(S0), t + 1)] if tag == "L" else None
                    B1 = [t + 1, copy.deepcopy(T), shift(copy.deepcopy(S1), t + 1)] if tag == "L" else None
                    if tag == "R":
                        B0 = [s + 1, copy.deepcopy(S0), shift(copy.deepcopy(T), s + 1)]
                        B1 = [s + 2, copy.deepcopy(S1), shift(copy.deepcopy(T), s + 2)]
                    n0 = t + 1 + s; n1 = t + 1 + s + 1
                    for y in range(1, t + 1):
                        y0 = y if tag == "L" else y + s + 1
                        y1 = y if tag == "L" else y + s + 2
                        Py = path_nodes(T, y); d = len(Py) - 1
                        sx = None if d == 0 else (0 if Py[0][1] is Py[1] else 1)
                        r0 = R_static(B0, y0); r1 = R_static(B1, y1)
                        h0 = H0(B0, y0, n0); h1 = H0(B1, y1, n1)
                        aR = r1 - r0; s0 = h1 - h0
                        tab[(spv, d % 2, sx)].add((aR, s0))
                        # identity: alpha_R == sibling lambda f_top in B1
                        _, lam1 = R_coeffs(B1, y1)
                        dB1 = depths_list(B1)
                        sib = set()
                        lo, hi = (t + 2, t + 2 + s) if tag == "L" else (1, s + 1)
                        # sibling key range: Ext_L S keys t+2..; Ext_R S keys 1..s+1 (S1 has s+1 keys)
                        for z in range(lo, hi + 1):
                            if z == y1:
                                continue
                            sib.add(lam1.get(z, 0))
                        ident_tot += 1
                        if len(sib) == 1 and next(iter(sib)) == aR:
                            ident_ok += 1
                        elif ident_bad is not None and len(ident_bad) < 5:
                            ident_bad.append({"t": t, "s": s, "tag": tag, "y": y, "aR": aR, "siblam": sorted(sib)})
    print("[HS] slope table (sp,parity,sx) -> {(alpha_R,sigma0)}:", flush=True)
    for k in sorted(tab, key=str):
        print(f"    sp={k[0]} parity={k[1]} sx={k[2]}: {sorted(tab[k])}", flush=True)
    print(f"[HS] alpha_R==f_top identity: {ident_ok}/{ident_tot}", flush=True)
    for b in ident_bad:
        print(f"    MISMATCH {b}", flush=True)
    rep["slope_table"] = [[list(k), sorted(v)] for k, v in sorted(tab.items(), key=str)]
    rep["identity"] = {"ok": ident_ok, "tot": ident_tot, "bad": ident_bad}
    json.dump(rep, open(OUT / "j4_h0slope.json", "w"), indent=1, default=str)
    print("[HS] saved", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())

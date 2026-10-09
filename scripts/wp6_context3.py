"""Contextual follow-ups: old-claim dlam rule (nonempty S), sibling (j vs d_T,
lambda vs state, delta spread), R-affine slopes per row class.
Usage: python scripts/wp6_context3.py
"""
import sys, json, copy
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

def main():
    rep = {}
    # 1. old-claim dlam by (parity,sx,slot) for Ext_L nonempty S
    cls = defaultdict(lambda: defaultdict(int))
    for t in (2, 3, 4):
        for s in (1, 2, 3):
            for T in O.shapes_of(list(range(1, t + 1))):
                S0 = O.shapes_of(list(range(1, s + 1)))[0]
                B = [t + 1, copy.deepcopy(T), shift(copy.deepcopy(S0), t + 1)]
                for y in range(1, t + 1):
                    Py = path_nodes(T, y); d = len(Py) - 1
                    sx = None if d == 0 else (0 if Py[0][1] is Py[1] else 1)
                    _, lT = R_coeffs(T, y); _, lB = R_coeffs(B, y)
                    for z in range(1, t + 1):
                        if z == y:
                            continue
                        sT = j4.slot_of(T, y, z)
                        if sT[0] == 'F':
                            continue
                        cls[(d % 2, sx, sT[0])][lB.get(z, 0) - lT.get(z, 0)] += 1
    print("[CX3] old-claim Ext_L nonempty-S dlam by (parity,sx,slot):", flush=True)
    for k in sorted(cls, key=str):
        print(f"    parity={k[0]} sx={k[1]} slot={k[2]}: {dict(cls[k])}", flush=True)
    rep["old_dlam"] = [[list(k), dict(v)] for k, v in sorted(cls.items(), key=str)]
    # 2. sibling j vs d_T(y); sibling lambda vs (parity,sx); delta spread
    jmatch = tot = 0
    lam_by = defaultdict(set)
    dspread = defaultdict(set)
    for t in (2, 3, 4):
        for s in (1, 2, 3):
            for T in O.shapes_of(list(range(1, t + 1))):
                dT = depths_list(T)
                for S in O.shapes_of(list(range(1, s + 1))):
                    B = [t + 1, copy.deepcopy(T), shift(copy.deepcopy(S), t + 1)]
                    dB = depths_list(B)
                    for y in range(1, t + 1):
                        _, lam = R_coeffs(B, y)
                        sl0 = None
                        for z in range(t + 2, t + 2 + s):
                            sl = j4.slot_of(B, y, z)
                            if sl0 is None:
                                sl0 = sl
                            lam_by[(dT[y], sl[0], sl[1] if len(sl) > 1 else None)].add(lam.get(z, 0))
                            dspread[(sl[0], sl[1] if len(sl) > 1 else None)].add(dB[z] - dB[y])
                        tot += 1
                        if sl0 is not None and sl0[0] == 'F' and sl0[1] == dT[y]:
                            jmatch += 1
    print(f"[CX3] sibling j == d_T(y): {jmatch}/{tot}", flush=True)
    print("[CX3] sibling lambda by (d_T,slot,j):", flush=True)
    for k in sorted(lam_by, key=str)[:20]:
        print(f"    {k}: {sorted(lam_by[k])}", flush=True)
    print("[CX3] sibling delta-spread by slot:", {str(k): sorted(v) for k, v in dspread.items()}, flush=True)
    rep["sib_jmatch"] = {"match": jmatch, "tot": tot}
    # 3. R-affine slope per (parity,sx) over s=1..4 (fixed T,y, vine S)
    slopes = defaultdict(list)
    for t in (3, 4):
        for T in O.shapes_of(list(range(1, t + 1)))[:12]:
            for y in range(1, t + 1):
                Py = path_nodes(T, y); d = len(Py) - 1
                sx = None if d == 0 else (0 if Py[0][1] is Py[1] else 1)
                Rs = []
                for s in (1, 2, 3, 4):
                    S0 = O.shapes_of(list(range(1, s + 1)))[0]
                    B = [t + 1, copy.deepcopy(T), shift(copy.deepcopy(S0), t + 1)]
                    yB = y
                    Rs.append(R_static(B, yB))
                sl = [Rs[i + 1] - Rs[i] for i in range(3)]
                slopes[(d % 2, sx)].append(sl)
    agg = {}
    for k, v in sorted(slopes.items(), key=str):
        flat = [x for sl in v for x in sl]
        agg[str(k)] = {"n": len(v), "uniq": sorted(set(flat))}
    print("[CX3] R slopes per (parity,sx) s=1..4:", agg, flush=True)
    rep["r_slopes"] = agg
    json.dump(rep, open(OUT / "j4_context3.json", "w"), indent=1, default=str)
    print("[CX3] saved", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())

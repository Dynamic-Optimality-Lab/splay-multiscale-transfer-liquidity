"""Two-level L/R class MAP (for shift operator): per (parity,sx,sx2,slot,lam)
record (postslot, dlam, ddelta). Then shift-validate Dbar(k)->Dbar(k+2).
Usage: python scripts/wp6_shiftmap.py [map|validate]
"""
import sys, copy, json
from pathlib import Path
from collections import defaultdict, Counter
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
OUT = ROOT / "artifacts/v04/wp6_present/0909c74a/dual_mine"
import importlib.util
def load(name):
    spec = importlib.util.spec_from_file_location(name, str(ROOT / 'scripts' / (name + '.py')))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m
j4 = load('wp6_j4shared')
tw = load('wp6_twins')
from wp6_staticR import depths_list, path_nodes
from wp6_lambda import R_coeffs
import wp6_cycle_ratio as O

def cls_of(B, y):
    P = path_nodes(B, y)
    d = len(P) - 1
    sx = None if d == 0 else (0 if P[0][1] is P[1] else 1)
    sx2 = None
    if d >= 2:
        sx2 = 0 if P[1][1] is P[2] else 1
    return (d % 2, sx, sx2)

def mode_map():
    mp = defaultdict(set)
    for T in O.shapes_of(list(range(1, 6)))[:60]:
        for y in range(1, 6):
            Py = path_nodes(T, y)
            if Py is None:
                continue
            d = len(Py) - 1
            if d < 2 or d > 3:
                continue
            T2 = [0, None, [-1, None, copy.deepcopy(T)]]
            _, lam = R_coeffs(T, y)
            _, lam2 = R_coeffs(T2, y)
            dT = depths_list(T)
            c = cls_of(T, y)
            for z in range(1, 6):
                if z == y:
                    continue
                s0 = j4.slot_of(T, y, z)
                if s0[0] not in ('L', 'R'):
                    continue
                s1 = j4.slot_of(T2, y, z)
                dT2 = depths_list(T2)
                mp[(c[0], c[1], c[2], s0[0], lam.get(z, 0))].add(
                    (s1[0], lam2.get(z, 0) - lam.get(z, 0),
                     (dT2[z] - dT2[y]) - (dT[z] - dT[y])))
    out = {}
    for k in sorted(mp, key=str):
        out[str(k)] = sorted([list(x) for x in mp[k]])
    nonuni = {k: v for k, v in mp.items() if len(v) > 1}
    print(f"[SM] classes={len(mp)} non-singleton={len(nonuni)}", flush=True)
    for k in sorted(nonuni, key=str)[:10]:
        print(f"    NONUNI {k}: {sorted(nonuni[k])}", flush=True)
    json.dump(out, open(OUT / "j4_shiftmap.json", "w"), indent=1, default=str)
    print("[SM] saved map", flush=True)

def main():
    modes = sys.argv[1:] or ["map"]
    if "map" in modes:
        mode_map()
    return 0

if __name__ == "__main__":
    sys.exit(main())

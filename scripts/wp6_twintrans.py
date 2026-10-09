"""Twin transport: do (F,1) and (F,2) twins get identical transitions under padding?
Group F dlam by (parity,sx,j,lam); compare lam=1 vs lam=2. Plus type-graph edges.
Usage: python scripts/wp6_twintrans.py
"""
import sys, copy, json
from pathlib import Path
from collections import defaultdict
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_staticR import depths_list, path_nodes
from wp6_lambda import R_coeffs
import importlib.util
def load(name):
    spec = importlib.util.spec_from_file_location(name, str(ROOT / 'scripts' / (name + '.py')))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m
j4 = load('wp6_j4shared')
import wp6_cycle_ratio as O
OUT = ROOT / "artifacts/v04/wp6_present/0909c74a/dual_mine"

def main():
    rep = {}
    # F transitions under Pad_L/R grouped by (parity,sx,j,lam)
    for pk, mkpad in (("L", lambda B: [0, None, copy.deepcopy(B)]),
                      ("R", lambda B: [99, copy.deepcopy(B), None])):
        cls = defaultdict(lambda: defaultdict(int))
        for n in (5, 6):
            for B in O.shapes_of(list(range(1, n + 1))):
                P = mkpad(B)
                for y in range(1, n + 1):
                    yP = y
                    Py = path_nodes(B, y); d = len(Py) - 1
                    sx = None if d == 0 else (0 if Py[0][1] is Py[1] else 1)
                    sx2 = None
                    if d >= 2:
                        sx2 = 0 if Py[1][1] is Py[2] else 1
                    _, lB = R_coeffs(B, y); _, lP = R_coeffs(P, yP)
                    for z in range(1, n + 1):
                        if z == y:
                            continue
                        sB = j4.slot_of(B, y, z)
                        if sB[0] != 'F':
                            continue
                        zP = z
                        sP = j4.slot_of(P, yP, zP)
                        key = (d % 2, sx, sx2, sB[1], lB.get(z, 0))
                        cls[key][(lP.get(zP, 0) - lB.get(z, 0),
                                  sP[1] if sP[0] == 'F' else None)] += 1
        # compare lam=1 vs lam=2 within same (parity,sx,sx2,j)
        fams = defaultdict(dict)
        for (par, sx, sx2, j, lam), dist in cls.items():
            fams[(par, sx, sx2, j)][lam] = dict(dist)
        twin_ok = twin_tot = 0
        for key, m in sorted(fams.items(), key=str):
            if 1 in m and 2 in m:
                twin_tot += 1
                if set(m[1]) == set(m[2]):
                    twin_ok += 1
                else:
                    print(f"[TT] pad={pk} class(par={key[0]},sx={key[1]},j={key[2]}): "
                          f"lam1->{m[1]} lam2->{m[2]}", flush=True)
        print(f"[TT] pad={pk}: twin-support-identical {twin_ok}/{twin_tot} classes", flush=True)
        rep[pk] = {"ok": twin_ok, "tot": twin_tot}
    json.dump(rep, open(OUT / "j4_twintrans.json", "w"), indent=1, default=str)
    print("[TT] saved", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())

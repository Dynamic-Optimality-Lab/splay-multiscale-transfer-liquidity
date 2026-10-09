"""Per-class uniform L/R/NONE transition values under padding."""
import sys
from pathlib import Path
from collections import defaultdict
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_staticR import path_nodes
from wp6_lambda import R_coeffs
import importlib.util
spec = importlib.util.spec_from_file_location('j4', str(ROOT / 'scripts' / 'wp6_j4shared.py'))
j4 = importlib.util.module_from_spec(spec); spec.loader.exec_module(j4)
import wp6_cycle_ratio as O
import copy

def main():
    for n in (5, 6):
        Sh = O.shapes_of(list(range(1, n + 1)))
        for pk, pf in (("L", lambda B: [0, None, copy.deepcopy(B)]),
                       ("R", lambda B: [n + 1, copy.deepcopy(B), None])):
            cls = defaultdict(lambda: defaultdict(int))
            for B in Sh:
                P_ = pf(B)
                for y in range(1, n + 1):
                    Py = path_nodes(B, y)
                    d = len(Py) - 1
                    sx = None
                    if d >= 1:
                        sx = 0 if Py[0][1] is Py[1] else 1
                    _, lB = R_coeffs(B, y)
                    _, lP = R_coeffs(P_, y)
                    for z in range(1, n + 1):
                        if z == y:
                            continue
                        sB = j4.slot_of(B, y, z)
                        if sB[0] == 'F':
                            continue
                        key = (d % 2, sx, sB[0], lB.get(z, 0))
                        cls[key][lP.get(z, 0) - lB.get(z, 0)] += 1
            print(f"=== n={n} pad={pk} L/R/NONE classes ===")
            for k in sorted(cls, key=str):
                print(f"   parity={k[0]} sx={k[1]} slot={k[2]} lam={k[3]}: {dict(cls[k])}")
    return 0

if __name__ == "__main__":
    sys.exit(main())

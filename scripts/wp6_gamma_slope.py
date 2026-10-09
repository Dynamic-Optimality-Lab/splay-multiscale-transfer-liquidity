"""Gamma slope probe: same-class vs cross-class row pairs vs |S|."""
import sys, copy
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_staticR import depths_list, path_nodes, R_static
import importlib.util
def load(name):
    spec = importlib.util.spec_from_file_location(name, str(ROOT / 'scripts' / (name + '.py')))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m
j4 = load('wp6_j4shared')
import wp6_cycle_ratio as O

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
    t = 4
    Sh = O.shapes_of(list(range(1, t + 1)))
    # find a T with two odd-depth rows of sx 0 and sx 1
    for T in Sh:
        cls = {}
        for y in range(1, t + 1):
            Py = path_nodes(T, y); d = len(Py) - 1
            sx = None if d == 0 else (0 if Py[0][1] is Py[1] else 1)
            cls[y] = (d % 2, sx)
        odds0 = [y for y, c in cls.items() if c == (1, 0)]
        odds1 = [y for y, c in cls.items() if c == (1, 1)]
        evens = [y for y, c in cls.items() if c[0] == 0 and c[1] is not None]
        if odds0 and odds1 and evens:
            print(f"[GS] T={T} classes={cls}", flush=True)
            pairs = [(odds0[0], odds1[0], "cross"), (evens[0], odds1[0], "mixed")]
            if len(odds1) >= 2:
                pairs.append((odds1[0], odds1[1], "same"))
            for (u, v, tag) in pairs:
                row = []
                base = H0(T, u, t) - H0(T, v, t)
                for s in (1, 2, 3, 4, 5):
                    S0 = O.shapes_of(list(range(1, s + 1)))[0]
                    B = [t + 1, copy.deepcopy(T), shift(copy.deepcopy(S0), t + 1)]
                    nB = t + 1 + s
                    g = (H0(B, u, nB) - H0(B, v, nB)) - base
                    row.append(g)
                print(f"[GS] pair ({u},{v}) {tag} Gamma vs s=1..5: {row}", flush=True)
            break
    return 0

if __name__ == "__main__":
    sys.exit(main())

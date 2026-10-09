"""Decode worst-violated expansion rows; verify one SELF row by hand."""
import sys, copy, json
from pathlib import Path
import numpy as np
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
vl = load('wp6_validlift')
from wp6_staticR import depths_list, R_static
from wp6_lambda import R_coeffs
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

def main():
    # rebuild trees list identically to nxexpand to index new rows
    trees = []
    for T in O.shapes_of([1, 2, 3]):
        Tr = vl.relabel(copy.deepcopy(T), lambda x: 10 * x)
        p = 100
        for s in (0, 1):
            Sr = None if s == 0 else vl.relabel(O.shapes_of([1])[0], lambda x: 10 * x + 500)
            # replicate lift2_spaced twice
            def lift2(T_):
                mx = max(depths_list(T_).keys())
                return [mx + 6, [mx + 3, copy.deepcopy(T_), None], None]
            T2 = lift2(lift2(Tr))
            B2 = [p, copy.deepcopy(T2), copy.deepcopy(Sr)] if Sr is not None else [0, None, copy.deepcopy(T2)]
            trees.append((B2, T2))
    print(f"[DC] trees: {len(trees)}", flush=True)
    # take first tree, first SELF row x: recompute everything by hand
    B2, T2 = trees[0]
    n = len(depths_list(B2))
    x = sorted(depths_list(B2).keys())[0]
    Bp = j4.V.replay(copy.deepcopy(B2), copy.deepcopy(B2), [("K", x)])["endB"]
    R = R_static(B2, x)
    Rp = R_static(Bp, x)
    G = n - subsize(B2, x)
    Gp = n - subsize(Bp, x)
    b = 1 if B2[0] == x else 0
    D0 = R - 2 * (1 - b)
    s0 = ((-R + j4.KAPPA * G) - (-Rp + j4.KAPPA * Gp)) - D0
    print(f"[DC] n={n} x={x} R={R} Rp={Rp} G={G} Gp={Gp} b={b} D0={D0} s0={s0} rhs={-s0}", flush=True)
    _, l0 = R_coeffs(B2, x)
    _, l1 = R_coeffs(Bp, x)
    d0 = depths_list(B2)
    print(f"[DC] B root={B2[0]} depths(pre)={dict(sorted(d0.items()))}", flush=True)
    print(f"[DC] Bp root={Bp[0]} depths(post)={dict(sorted(depths_list(Bp).items()))}", flush=True)
    print("[DC] done", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())

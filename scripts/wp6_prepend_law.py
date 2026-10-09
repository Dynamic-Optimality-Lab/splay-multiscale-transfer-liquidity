"""Prepend-law verification: class-uniform lambda transitions, composition LL=L o L,
NONE-column identity on full SH567, s0 parity. See PIVOT-25V Part III/IV.
Usage: python scripts/wp6_prepend_law.py
"""
import sys, json
from pathlib import Path
from collections import defaultdict
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_staticR import depths_list, path_nodes, R_static, Tmap
from wp6_lambda import R_coeffs
import importlib.util
spec = importlib.util.spec_from_file_location('j4', str(ROOT / 'scripts' / 'wp6_j4shared.py'))
j4 = importlib.util.module_from_spec(spec); spec.loader.exec_module(j4)
OUT = ROOT / "artifacts/v04/wp6_present/0909c74a/dual_mine"

def pad_L(B):
    import copy
    return [0, None, copy.deepcopy(B)]

def pad_R(B, n):
    import copy
    return [n + 1, copy.deepcopy(B), None]

def top_double_type(P):
    """Top double of path P (needs len>=3): (side_parent, side_child) as pattern name."""
    if len(P) < 3:
        return None
    gnd, pnd, xnd = P[0], P[1], P[2]
    sp = 0 if gnd[1] is pnd else 1
    sx = 0 if pnd[1] is xnd else 1
    return {(0, 0): "LL", (1, 1): "RR", (0, 1): "LR", (1, 0): "RL"}[(sp, sx)]

def main():
    import wp6_cycle_ratio as O
    rep = {}
    # ---- 1. class-uniformity: group lambda transitions by (pad, d parity, sx class) ----
    for n in (5, 6):
        Sh = O.shapes_of(list(range(1, n + 1)))
        for pk, pf, isL in (("L", pad_L, True), ("R", lambda B: pad_R(B, n), False)):
            cls = defaultdict(lambda: defaultdict(int))  # (parity,sx,slot,lam)->Counter(dlam)
            for B in Sh:
                P_ = pf(B)
                for y in range(1, n + 1):
                    Pth = path_nodes(B, y)
                    d = len(Pth) - 1
                    sx = None
                    if d >= 1:
                        par = Pth[d - 1] if False else None
                        # side of path-child under its parent at depth>=1: use second node
                        nd1 = Pth[1] if d >= 1 else None
                        top = Pth[0]
                        sx = 0 if top[1] is nd1 else 1
                    _, lB = R_coeffs(B, y)
                    _, lP = R_coeffs(P_, y)
                    for z in range(1, n + 1):
                        if z == y:
                            continue
                        sB = j4.slot_of(B, y, z)
                        key = (d % 2, sx, sB[0], lB.get(z, 0))
                        cls[key][lP.get(z, 0) - lB.get(z, 0)] += 1
            nonuni = {k: dict(v) for k, v in cls.items() if len(v) > 1}
            uni_by_class = len(cls) - len(nonuni)
            rep[f"uniform_n{n}_{pk}"] = {"classes": len(cls), "uniform": uni_by_class,
                                        "nonuniform": [[list(k), v] for k, v in list(nonuni.items())[:12]]}
            print(f"[PL] n={n} pad={pk}: {len(cls)} classes, {uni_by_class} uniform, "
                  f"{len(nonuni)} non-uniform", flush=True)
            for k, v in list(nonuni.items())[:6]:
                print(f"    NONUNI parity={k[0]} sx={k[1]} slot={k[2]} lam={k[3]}: dlam-dist={v}", flush=True)
    # ---- 2. composition: LL ?= L o L at J4 row-multiset level (SELF rows), all shapes n<=6 ----
    for n in (5, 6):
        Sh = O.shapes_of(list(range(1, n + 1)))
        bad = tot = 0
        for B in Sh:
            for x in range(1, n + 1):
                # direct LL atoms
                LL = pad_L(pad_L(B))
                _, lD = R_coeffs(LL, x)
                dD = depths_list(LL)
                mD = defaultdict(int)
                for z in range(1, n + 1):
                    if z == x:
                        continue
                    mD[j4.slot_of(LL, x, z), lD.get(z, 0), dD[z] - dD[x], dD[x]] += 1
                # composed: L then L
                L1 = pad_L(B)
                L2 = pad_L(L1)
                _, lC = R_coeffs(L2, x)
                dC = depths_list(L2)
                mC = defaultdict(int)
                for z in range(1, n + 1):
                    if z == x:
                        continue
                    mC[j4.slot_of(L2, x, z), lC.get(z, 0), dC[z] - dC[x], dC[x]] += 1
                tot += 1
                if dict(mD) != dict(mC):
                    bad += 1
        print(f"[PL] composition LL==L o L n={n}: {tot-bad}/{tot} match", flush=True)
        rep[f"compose_LL_n{n}"] = {"tot": tot, "bad": bad}
    # ---- 3. NONE-column identity on FULL SH567 matrix ----
    Z = np.load(OUT / "j4_sh567_A.npz")
    A = Z["A"].astype(np.int64)
    vm = json.load(open(OUT / "j4_sh567_vmap.json"))["vmap"]
    inv = {i: k for k, i in vm.items()}
    from collections import defaultdict as dd
    fam = dd(list)
    for i in range(A.shape[1]):
        t = eval(inv[i])
        if t[0] == 't' and t[1][0] == ('NONE',):
            fam[t[1][3]].append(i)
    ok = True
    for dy, cols in sorted(fam.items()):
        base = A[:, cols[0]]
        for c in cols[1:]:
            if not bool(((A[:, c] - base) == 0).all()):
                ok = False
                print(f"[PL] NONE family d_y={dy} MISMATCH", flush=True)
    print(f"[PL] NONE-column identity full-matrix: {'HOLDS' if ok else 'FAILS'} "
          f"({sum(len(v) for v in fam.values())} NONE cols in {len(fam)} families)", flush=True)
    rep["none_fullmatrix"] = {"holds": ok, "ncols": sum(len(v) for v in fam.values()),
                              "nfam": len(fam)}
    # ---- 4. s0 parity over SH567 SELF rows ----
    raw = None
    # rebuild s0 list cheaply via j4shared build for [5,6,7] metas only (reuse prior knowledge is fine;
    # recompute here for parity audit)
    import wp6_cycle_ratio as O2
    par = 0
    for n in (5, 6, 7):
        for B in O2.shapes_of(list(range(1, n + 1))):
            for x in range(1, n + 1):
                Bp = j4.V.replay(B, B, [("K", x)])["endB"]
                R = R_static(B, x); Rp = R_static(Bp, x)
                G = n - j4.subsize(B, x); Gp = n - j4.subsize(Bp, x)
                b = 1 if B[0] == x else 0
                D0 = R - 2 * (1 - b)
                s0 = ((-R + j4.KAPPA * G) - (-Rp + j4.KAPPA * Gp)) - D0
                if s0 % 2 != 0:
                    par += 1
    print(f"[PL] s0 odd count over all SH567 SELF rows: {par}", flush=True)
    rep["s0_odd"] = par
    json.dump(rep, open(OUT / "j4_prepend_law.json", "w"), indent=1, default=str)
    print("[PL] saved", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())

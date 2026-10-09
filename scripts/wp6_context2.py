"""Focused contextual probes: sibling uniformity, old-claim transition vs empty-pad,
R/H0 size dependence, top-pattern classification.
Usage: python scripts/wp6_context2.py
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

def ext_L(T, S):
    t = len(depths_list(T))
    return [t + 1, copy.deepcopy(T), shift(copy.deepcopy(S), t + 1)]

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
    # 1. sibling uniformity: fixed (B,y): single (slot,lambda) for all z in S?
    uni = tot = 0
    slotdist = defaultdict(int)
    for t in (2, 3, 4):
        for s in (1, 2, 3):
            for T in O.shapes_of(list(range(1, t + 1))):
                for S in O.shapes_of(list(range(1, s + 1))):
                    B = ext_L(T, S)
                    dB = depths_list(B)
                    for y in range(1, t + 1):
                        _, lam = R_coeffs(B, y)
                        ss = set()
                        for z in range(t + 2, t + 2 + s):
                            sl = j4.slot_of(B, y, z)
                            ss.add((str(sl), lam.get(z, 0)))
                            slotdist[str(sl)] += 1
                        tot += 1
                        if len(ss) == 1:
                            uni += 1
    print(f"[CX2] sibling uniformity (one slot+lam per (B,y)): {uni}/{tot}", flush=True)
    print("[CX2] sibling slot distribution:", dict(slotdist), flush=True)
    rep["sib_uniform"] = {"uni": uni, "tot": tot}
    # 2. old-claim transition Ext vs empty-pad: same dlam rule?
    # compare lam_B(old)-lam_T(old) distribution vs Pad_L rule classes
    match = tot2 = 0
    for t in (2, 3, 4):
        for s in (1, 2, 3):
            for T in O.shapes_of(list(range(1, t + 1))):
                Svine = None
                # vine S of size s
                Sv = None
                for k in range(t + 2, t + 2 + s):
                    Sv = [k, Sv, None] if Sv is None else [k, Sv, None]
                    # build right vine iteratively: root low keys... simpler: chain
                # use first shape as representative (shape-invariance says any)
                S0 = O.shapes_of(list(range(1, s + 1)))[0]
                B = ext_L(T, S0)
                P0 = [0, None, copy.deepcopy(T)]  # empty Pad_L analog (key 0 root)
                for y in range(1, t + 1):
                    Py = path_nodes(T, y); d = len(Py) - 1
                    sx = None if d == 0 else (0 if Py[0][1] is Py[1] else 1)
                    _, lT = R_coeffs(T, y)
                    _, lB = R_coeffs(B, y)
                    for z in range(1, t + 1):
                        if z == y:
                            continue
                        sB = j4.slot_of(T, y, z)
                        if sB[0] == 'F':
                            continue
                        got = lB.get(z, 0) - lT.get(z, 0)
                        # Pad_L rule
                        if sB[0] == 'R':
                            pred = -1
                        elif sB[0] == 'L':
                            pred = -1 if (d % 2 == 1 and sx == 1) else 0
                        else:
                            pred = 0
                        tot2 += 1
                        if got == pred:
                            match += 1
    print(f"[CX2] old-claim Ext transition == empty-Pad_L rule: {match}/{tot2}", flush=True)
    rep["oldtrans_match"] = {"match": match, "tot": tot2}
    # 3. R and H0-diff vs |S| for fixed (T,y): affine?
    for t in (3,):
        T = O.shapes_of(list(range(1, t + 1)))[0]
        for y in (1, 2):
            row = []
            for s in (0, 1, 2, 3, 4):
                if s == 0:
                    B = [0, None, copy.deepcopy(T)]
                    nB = t + 1
                else:
                    S0 = O.shapes_of(list(range(1, s + 1)))[0]
                    B = ext_L(T, S0)
                    nB = t + 1 + s
                row.append((R_static(B, y), H0(B, y, nB)))
            print(f"[CX2] T#0 y={y} (R,H0) vs s=0..4: {row}", flush=True)
    # 4. top-pattern classification: (side, first-turn, parity) -> prepend Tmap
    pats = defaultdict(int)
    for t in (2, 3, 4):
        for T in O.shapes_of(list(range(1, t + 1))):
            for y in range(1, t + 1):
                Py = path_nodes(T, y); d = len(Py) - 1
                if d == 0:
                    pats[("root",)] += 1
                    continue
                sx = 0 if Py[0][1] is Py[1] else 1
                # Ext_L: new root above old root on right side: sp=1
                pats[("L", d % 2, sx)] += 1
    print("[CX2] (side,parity,sx) classes:", dict(pats), flush=True)
    json.dump(rep, open(OUT / "j4_context2.json", "w"), indent=1, default=str)
    print("[CX2] saved", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())

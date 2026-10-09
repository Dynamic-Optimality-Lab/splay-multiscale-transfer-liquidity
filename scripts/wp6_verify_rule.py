"""Verify hypothesized Pad_L/R rule + composition RR/LR + mirror-symmetrized feasibility."""
import sys
from pathlib import Path
from collections import defaultdict
import numpy as np
import copy
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

def rule_L(d, sx, slot):
    # hypothesized Pad_L: R always -1; L -1 iff (d odd and sx==1); NONE 0
    if slot == 'R':
        return -1
    if slot == 'L':
        if d % 2 == 1 and sx == 1:
            return -1
        return 0
    if slot == 'NONE':
        return 0
    return None

def rule_R(d, sx, slot):
    if slot == 'L':
        return -1
    if slot == 'R':
        if d % 2 == 1 and sx == 0:
            return -1
        return 0
    if slot == 'NONE':
        return 0
    return None

def main():
    badL = badR = totL = totR = 0
    for n in (5, 6):
        Sh = O.shapes_of(list(range(1, n + 1)))
        for B in Sh:
            for pk, pf, rule in (("L", lambda B: [0, None, copy.deepcopy(B)], rule_L),
                                 ("R", lambda B: [n + 1, copy.deepcopy(B), None], rule_R)):
                P = pf(B)
                for y in range(1, n + 1):
                    Py = path_nodes(B, y); d = len(Py) - 1
                    sx = None if d == 0 else (0 if Py[0][1] is Py[1] else 1)
                    _, lB = R_coeffs(B, y); _, lP = R_coeffs(P, y)
                    for z in range(1, n + 1):
                        if z == y:
                            continue
                        sB = j4.slot_of(B, y, z)
                        if sB[0] == 'F':
                            continue
                        pred = rule(d, sx, sB[0])
                        got = lP.get(z, 0) - lB.get(z, 0)
                        if pk == "L":
                            totL += 1
                            if got != pred:
                                badL += 1
                        else:
                            totR += 1
                            if got != pred:
                                badR += 1
    print(f"[VR] Pad_L rule: {totL-badL}/{totL} match", flush=True)
    print(f"[VR] Pad_R rule: {totR-badR}/{totR} match", flush=True)
    # composition RR and LR at multiset level
    for n in (5, 6):
        Sh = O.shapes_of(list(range(1, n + 1)))
        for tag, fdir in (("RR", lambda B, n: [n + 2, [n + 1, copy.deepcopy(B), None], None]),
                          ("LR", lambda B, n: [n + 1, [0, None, copy.deepcopy(B)], None])):
            bad = tot = 0
            for B in Sh:
                D = fdir(B, n)
                # composed stepwise
                if tag == "RR":
                    C = [n + 2, [n + 1, copy.deepcopy(B), None], None]
                else:
                    C = [n + 1, [0, None, copy.deepcopy(B)], None]
                for x in range(1, n + 1):
                    _, lD = R_coeffs(D, x); dD = depths_list(D)
                    mD = defaultdict(int)
                    for z in range(1, n + 1):
                        if z == x:
                            continue
                        mD[j4.slot_of(D, x, z), lD.get(z, 0), dD[z] - dD[x], dD[x]] += 1
                    _, lC = R_coeffs(C, x); dC = depths_list(C)
                    mC = defaultdict(int)
                    for z in range(1, n + 1):
                        if z == x:
                            continue
                        mC[j4.slot_of(C, x, z), lC.get(z, 0), dC[z] - dC[x], dC[x]] += 1
                    tot += 1
                    if dict(mD) != dict(mC):
                        bad += 1
            print(f"[VR] composition {tag} direct==stepwise n={n}: {tot-bad}/{tot}", flush=True)
    print("[VR] done", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())

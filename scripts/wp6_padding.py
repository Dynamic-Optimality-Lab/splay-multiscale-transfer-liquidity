"""Root-padding transition probe: Pad_L/Pad_R/Pad2 on all shapes n<=6.
For every old pointed pair (y,z): compare (slot,lambda,delta,d_y,c) pre/post,
plus new atoms from padding keys. Reports preservation stats per padding kind.
Usage: python scripts/wp6_padding.py
"""
import sys, json
from pathlib import Path
from collections import Counter
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_staticR import depths_list, path_nodes, R_static
from wp6_lambda import R_coeffs
import importlib.util
spec = importlib.util.spec_from_file_location('j4', str(ROOT / 'scripts' / 'wp6_j4shared.py'))
j4 = importlib.util.module_from_spec(spec); spec.loader.exec_module(j4)

def pad_L(B):
    import copy
    return [0, None, copy.deepcopy(B)]

def pad_R(B, n):
    import copy
    return [n + 1, copy.deepcopy(B), None]

def shift_keys(T, s):
    if T is None:
        return None
    return [T[0] + s, shift_keys(T[1], s), shift_keys(T[2], s)]

def main():
    import wp6_cycle_ratio as O
    out = {}
    for n in (5, 6):
        Sh = O.shapes_of(list(range(1, n + 1)))
        pads = {"L": lambda B: pad_L(B), "R": lambda B: pad_R(B, n),
                "LL": lambda B: pad_L(pad_L(B)), "RR": lambda B: pad_R(pad_R(B, n + 1), n),
                "LR": lambda B: pad_R(pad_L(B), n + 1)}
        for pk, pf in pads.items():
            stat = Counter()
            lam_change = Counter()   # (slot, dlam) of changed
            slot_change = Counter()  # (pre,post)
            c_pairs = Counter()
            new_atoms = Counter()
            fshift = Counter()       # (j_pre,j_post) for F
            nchecked = 0
            for B in Sh:
                P = pf(B)
                dB = depths_list(B)
                dP = depths_list(P)
                off = dP[B[0]] - dB[B[0]]
                assert off == (2 if len(pk) == 2 else 1), (pk, off)
                for y in range(1, n + 1):
                    _, lB = R_coeffs(B, y)
                    _, lP = R_coeffs(P, y)
                    cB, _ = R_coeffs(B, y)
                    cP, _ = R_coeffs(P, y)
                    c_pairs[(cB, cP)] += 1
                    for z in range(1, n + 1):
                        if z == y:
                            continue
                        sB = j4.slot_of(B, y, z)
                        sP = j4.slot_of(P, y, z)
                        lamB = lB.get(z, 0); lamP = lP.get(z, 0)
                        dlB = dB[z] - dB[y]; dlP = dP[z] - dP[y]
                        nchecked += 1
                        if sB != sP and not (sB[0] == 'F' and sP[0] == 'F'):
                            slot_change[(str(sB), str(sP))] += 1
                        if sB[0] == 'F' and sP[0] == 'F':
                            fshift[(sB[1], sP[1])] += 1
                        if dlB != dlP:
                            stat["delta_changed"] += 1
                        if lamB != lamP:
                            lam_change[(sB[0], lamB, lamP)] += 1
                    # new atoms: keys in P not in 1..n
                    newk = [kk for kk in dP if kk < 1 or kk > n]
                    for w in newk:
                        sN = j4.slot_of(P, y, w)
                        new_atoms[(str(sN), lP.get(w, 0), dP[w] - dP[y])] += 1
            tot_new = sum(new_atoms.values())
            out[f"n{n}_{pk}"] = {
                "checked": nchecked,
                "slot_changes_nonF": [[list(k) if isinstance(k, tuple) else k, v] for k, v in sorted(slot_change.items(), key=str)],
                "fshift": [[list(k), v] for k, v in sorted(fshift.items(), key=str)],
                "lambda_changes": [[list(k), v] for k, v in sorted(lam_change.items(), key=str)],
                "c_pairs": [[list(k), v] for k, v in sorted(c_pairs.items(), key=str)],
                "new_atoms": [[list(k), v] for k, v in sorted(new_atoms.items(), key=str)],
            }
            print(f"[PAD n={n} {pk}] pairs={nchecked} slotNonF={dict(list(slot_change.items())[:8])} "
                  f"fshift={dict(list(fshift.items())[:10])}", flush=True)
            print(f"   lamCh({len(lam_change)})={dict(list(lam_change.items())[:14])}", flush=True)
            print(f"   cPairs({len(c_pairs)})={dict(list(c_pairs.items())[:14])}", flush=True)
    json.dump(out, open(ROOT / "artifacts/v04/wp6_present/0909c74a/dual_mine/j4_padding.json", "w"), indent=1, default=str)
    print("[PAD] saved", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())

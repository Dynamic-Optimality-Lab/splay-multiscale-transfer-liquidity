"""26R part 1: leveled coupling blocks C0/C1, interfaces S0/S1 (exact RREF),
occurrence transport tau01/tau12, descent gate A ker S subset ker S'.
Usage: python scripts/wp6_levels.py [blocks|descent]
"""
import sys, copy, json
from pathlib import Path
from collections import Counter, defaultdict
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
from wp6_staticR import depths_list, path_nodes, R_static
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

def H0(T, y, n, ka=4.0):
    return -R_static(T, y) + ka * (n - subsize(T, y))

def lift2_spaced(T):
    mx = max(depths_list(T).keys())
    return [mx + 6, [mx + 3, copy.deepcopy(T), None], None]

def Jrow(B, y):
    _, lam = R_coeffs(B, y)
    dB = depths_list(B)
    terms = {}
    for z in dB:
        if z == y:
            continue
        t = (j4.slot_of(B, y, z), lam.get(z, 0), dB[z] - dB[y], dB[y])
        terms[('t', t)] = terms.get(('t', t), 0) + 1.0
    c, _ = R_coeffs(B, y)
    terms[('r', c)] = terms.get(('r', c), 0) + 1.0
    return terms

def chain_levels():
    """Return dict level -> list of trees (level 0,1,2 chain trees, valid)."""
    lv = {0: [], 1: [], 2: []}
    seen = {0: set(), 1: set(), 2: set()}
    for T in O.shapes_of([1, 2, 3]):
        Tr = vl.relabel(copy.deepcopy(T), lambda x: 10 * x)
        p = 100
        for s in (0, 1):
            Sr = None if s == 0 else vl.relabel(O.shapes_of([1])[0], lambda x: 10 * x + 500)
            T0 = copy.deepcopy(Tr)
            T1 = lift2_spaced(T0)
            T2 = lift2_spaced(T1)
            def ext(TT):
                return [p, copy.deepcopy(TT), copy.deepcopy(Sr)] if Sr is not None else [0, None, copy.deepcopy(TT)]
            for TT, B_, lvidx in ((T0, ext(T0), 0), (T1, ext(T1), 1), (T2, ext(T2), 2)):
                for BB in (TT, B_):
                    vl.assert_valid_bst(BB)
                    key = json.dumps(BB, sort_keys=True)
                    if key not in seen[lvidx]:
                        seen[lvidx].add(key)
                        lv[lvidx].append(BB)
    return lv

def rows_for(trees):
    """SELF (replay) + DIAMETER rows for given trees in RAW J4 keys. Returns raw list."""
    raw = []
    for B in trees:
        n = len(depths_list(B))
        for x in depths_list(B):
            Bp = j4.V.replay(copy.deepcopy(B), copy.deepcopy(B), [("K", x)])["endB"]
            R = R_static(B, x)
            Rp = R_static(Bp, x)
            G = n - subsize(B, x)
            Gp = n - subsize(Bp, x)
            b = 1 if B[0] == x else 0
            D0 = R - 2 * (1 - b)
            s0 = ((-R + j4.KAPPA * G) - (-Rp + j4.KAPPA * Gp)) - D0
            tB = Jrow(B, x)
            tP = Jrow(Bp, x)
            terms = dict(tB)
            for kk, cc in tP.items():
                terms[kk] = terms.get(kk, 0) - cc
            raw.append((terms, -s0))
        bB = B[0]
        for rr in depths_list(B):
            for x in depths_list(B):
                if x == rr:
                    continue
                Hr = H0(B, rr, n)
                Hx = H0(B, x, n)
                br = 1 if bB == rr else 0
                bx = 1 if bB == x else 0
                Psi1 = -2 + 2 * (br - bx) - (Hr - Hx)
                tr = Jrow(B, rr)
                tx = Jrow(B, x)
                terms = dict(tr)
                for kk, cc in tx.items():
                    terms[kk] = terms.get(kk, 0) - cc
                raw.append((terms, Psi1))
    return raw

def main():
    modes = sys.argv[1:] or ["blocks"]
    import numpy as np
    if "blocks" in modes:
        lv = chain_levels()
        for i in (0, 1, 2):
            nn = sorted({len(depths_list(T)) for T in lv[i]})
            print(f"[LV] level {i}: {len(lv[i])} trees, sizes {nn}", flush=True)
        # assemble each level's rows in a GLOBAL key space (raw J4 keys, no mapping)
        allraw = {}
        for i in (0, 1, 2):
            allraw[i] = rows_for(lv[i])
            print(f"[LV] level {i} rows: {len(allraw[i])}", flush=True)
        # global vmap
        vmap = {}
        for i in (0, 1, 2):
            for (terms, _) in allraw[i]:
                for k in terms:
                    if k not in vmap:
                        vmap[k] = len(vmap)
        print(f"[LV] global vars: {len(vmap)}", flush=True)
        import scipy.sparse as sp
        out = {}
        for i in (0, 1, 2):
            E = len(allraw[i])
            V = len(vmap)
            rd, cd, vd = [], [], []
            for r, (terms, rh) in enumerate(allraw[i]):
                for k, c in terms.items():
                    rd.append(r); cd.append(vmap[k]); vd.append(float(c))
            Amat = sp.csr_matrix((np.array(vd), (np.array(rd), np.array(cd))), shape=(E, V))
            out[i] = (Amat, [rh for (_, rh) in allraw[i]])
        # interface per level = touched vars; rank; nullity (mod prime)
        for i in (0, 1, 2):
            Amat, _ = out[i]
            touched = sorted({c for r in range(Amat.shape[0]) for c in Amat.getrow(r).indices.tolist()})
            print(f"[LV] level {i}: E={Amat.shape[0]} touched={len(touched)}", flush=True)
        json.dump({"levels": [len(lv[i]) for i in (0, 1, 2)]},
                  open(OUT / "j4_levels2.json", "w"), indent=1)
        # save assembled blocks for descent stage
        np.savez_compressed(OUT / "j4_levelblocks.npz",
                            **{f"A{i}": out[i][0].toarray() for i in (0, 1, 2)})
        # save vmap keys
        inv = {i: k for k, i in vmap.items()}
        json.dump([str(inv[i]) for i in range(len(vmap))], open(OUT / "j4_levelkeys.json", "w"))
        print("[LV] saved blocks", flush=True)
    print("[LV] done", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())

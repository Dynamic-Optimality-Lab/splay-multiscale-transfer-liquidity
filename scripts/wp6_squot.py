"""26R part 2: RREF interfaces S0/S1, occurrence transport tau, descent gate."""
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
from wp6_staticR import depths_list, path_nodes
from wp6_lambda import R_coeffs
import wp6_cycle_ratio as O

def shift(T, s):
    if T is None:
        return None
    return [T[0] + s, shift(T[1], s), shift(T[2], s)]

def lift2_spaced(T):
    mx = max(depths_list(T).keys())
    return [mx + 6, [mx + 3, copy.deepcopy(T), None], None]

def foldword(B, y):
    P = path_nodes(B, y)
    d = len(P) - 1
    pats = []
    for i in range(d, 1, -2):
        gnd, pnd, xnd = P[i - 2], P[i - 1], P[i]
        sp = 0 if gnd[1] is pnd else 1
        sx = 0 if pnd[1] is xnd else 1
        pats.append({(0, 0): "LL", (1, 1): "RR", (0, 1): "LR", (1, 0): "RL"}[(sp, sx)])
    return pats, ('even' if d % 2 == 0 else ('zigL' if y < P[0][0] else 'zigR'))

def main():
    import numpy as np
    # rebuild level trees identically to wp6_levels
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
    # interface S_k: RREF quotient per level block. Rebuild level row blocks + touched.
    import scipy.sparse as sp
    from wp6_staticR import R_static
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
    def rows_for(trees):
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
    import sympy as sp2
    S = {}
    for i in (0, 1, 2):
        raw = rows_for(lv[i])
        vmap = {}
        for (terms, _) in raw:
            for k in terms:
                if k not in vmap:
                    vmap[k] = len(vmap)
        E = len(raw)
        V = len(vmap)
        M = np.zeros((E, V))
        for r, (terms, rh) in enumerate(raw):
            for k, c in terms.items():
                M[r, vmap[k]] = c
        # exact rank via sympy? E large (250..970 rows). Use mod-prime rank (fast).
        Mp = (np.round(M).astype(np.int64) % 1000000007)
        EE, VV = Mp.shape
        rnk = 0
        for c in range(VV):
            sub = Mp[rnk:, c]
            nz = np.flatnonzero(sub)
            if nz.size == 0:
                continue
            ii = rnk + int(nz[0])
            Mp[[rnk, ii]] = Mp[[ii, rnk]]
            inv = pow(int(Mp[rnk, c]), 1000000007 - 2, 1000000007)
            Mp[rnk, c:] = (Mp[rnk, c:] * inv) % 1000000007
            if rnk + 1 < EE:
                col = Mp[rnk + 1:, c]
                m = col != 0
                if m.any():
                    blk = Mp[rnk + 1:, c:]
                    blk[m] = (blk[m] - (col[m].reshape(-1, 1) * Mp[rnk, c:].reshape(1, -1)) % 1000000007) % 1000000007
            rnk += 1
            if rnk == EE:
                break
        print(f"[SQ] level {i}: E={E} V={V} rank={rnk}", flush=True)
        S[i] = {"rank": rnk, "V": V, "E": E}
    json.dump({str(i): S[i] for i in S}, open(OUT / "j4_levelranks.json", "w"), indent=1)
    print("[SQ] done", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())

"""26P part 1: exact coupling block C (integer entries), exact rank/nullity,
sparse exact null basis, semantic functional dictionary + span test.
Usage: python scripts/wp6_symiface.py [exact|dict]
"""
import sys, copy, json
from pathlib import Path
from collections import defaultdict
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
OUT = ROOT / "artifacts/v04/wp6_present/0909c74a/dual_mine"
import importlib.util
def load(name):
    spec = importlib.util.spec_from_file_location(name, str(ROOT / 'scripts' / (name + '.py')))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m

def load_xc():
    import numpy as np
    import scipy.sparse as sp
    Z = np.load(OUT / "j4_xclean_mat.npz")
    A = sp.csr_matrix(Z["A"])
    r = Z["rhs"]
    keys = [eval(k) for k in Z["keys"]]
    E0 = int(Z["E0"][0])
    return A, r, keys, E0

def main():
    modes = sys.argv[1:] or ["exact"]
    import numpy as np
    A, r, keys, E0 = load_xc()
    E, V = A.shape
    rv = {k: i for i, k in enumerate(keys)}
    # old coords = vars in old rows; coupling block = new rows restricted to touched old vars
    oldvars = set()
    for i in range(E0):
        oldvars.update(A.getrow(i).indices.tolist())
    touched = set()
    for i in range(E0, E):
        touched.update([j for j in A.getrow(i).indices.tolist() if j in oldvars])
    touched = sorted(touched)
    print(f"[SI] touched={len(touched)}", flush=True)
    C = A[E0:, :][:, touched].toarray()
    # exact integer? entries should be small ints/floats
    Ci = np.round(C).astype(np.int64)
    print(f"[SI] coupling entries integral: {bool((np.abs(C - Ci).max() < 1e-9))} range=[{Ci.min()},{Ci.max()}]", flush=True)
    if "exact" in modes:
        # exact rank over 3 primes
        import itertools
        ranks = {}
        for p in (1000000007, 1000000009, 998244353):
            M = (Ci % p).astype(np.int64).copy()
            EE, VV = M.shape
            rnk = 0
            for c in range(VV):
                sub = M[rnk:, c]
                nz = __import__("numpy").flatnonzero(sub)
                if nz.size == 0:
                    continue
                i = rnk + int(nz[0])
                M[[rnk, i]] = M[[i, rnk]]
                inv = pow(int(M[rnk, c]), p - 2, p)
                M[rnk, c:] = (M[rnk, c:] * inv) % p
                if rnk + 1 < EE:
                    col = M[rnk + 1:, c]
                    m = col != 0
                    if m.any():
                        blk = M[rnk + 1:, c:]
                        blk[m] = (blk[m] - (col[m].reshape(-1, 1) * M[rnk, c:].reshape(1, -1)) % p) % p
                rnk += 1
                if rnk == EE:
                    break
            ranks[str(p)] = rnk
            print(f"[SI] rank mod {p}: {rnk}", flush=True)
        json.dump({"shape": list(Ci.shape), "mod_ranks": ranks,
                   "nullity": Ci.shape[1] - ranks["1000000007"]},
                  open(OUT / "j4_symrank.json", "w"), indent=1)
        # exact nullspace via sympy on transpose? 79-dim: null of C (79 cols)
        try:
            import sympy as sp2
            M = sp2.Matrix(Ci.tolist())
            NS = M.nullspace()
            print(f"[SI] sympy null dim={len(NS)}", flush=True)
            basis = []
            for v in NS:
                nz = [(touched[i], int(v[i])) for i in range(len(v)) if v[i] != 0]
                basis.append({"nnz": len(nz), "entries": [[str(keys[j]), int(c)] for j, c in nz[:12]]})
                print(f"    nnz={len(nz)}", flush=True)
            json.dump({"dim": len(NS), "basis": basis}, open(OUT / "j4_symnull.json", "w"), indent=1, default=str)
        except Exception as e:
            print(f"[SI] sympy failed: {e}", flush=True)
    if "dict" in modes:
        # semantic functional dictionary over touched coords; test span of rowspan.
        # Build candidate functionals as 79-vectors (dicts), test membership in rowspan(C)
        # via exact rational least squares (use float + integer verify).
        import itertools
        tkeys = [keys[j] for j in touched]
        idx = {k: i for i, k in enumerate(tkeys)}
        # dictionary: K-diffs, L/R pair sums/diffs, F-aggs, singletons
        cand = {}
        # K adjacent differences (K_d indices present?)
        Ks = sorted({k[1] for k in tkeys if k[0] == 'K'})
        for a, b in zip(Ks, Ks[1:]):
            v = np.zeros(len(tkeys))
            v[idx[('K', a)]] = 1.0
            v[idx[('K', b)]] = -1.0
            cand[f"K{a}-K{b}"] = v
        # L/R: per-(slot,depth) sums and pair diffs
        gr = defaultdict(list)
        for k in tkeys:
            if k[0] == 't' and k[1][0][0] in ('L', 'R'):
                gr[(k[1][0][0], k[1][3])].append(k)
        for (s, d), lst in sorted(gr.items(), key=str):
            v = np.zeros(len(tkeys))
            for k in lst:
                v[idx[k]] = 1.0
            cand[f"sum-{s}{d}"] = v
        # F aggregates per j
        gf = defaultdict(list)
        for k in tkeys:
            if k[0] == 't' and k[1][0][0] == 'F':
                gf[k[1][0][1]].append(k)
        for j, lst in sorted(gf.items()):
            v = np.zeros(len(tkeys))
            for k in lst:
                v[idx[k]] = 1.0
            cand[f"Fsum{j}"] = v
        print(f"[SI] dictionary: {len(cand)} candidates", flush=True)
        # rowspan basis via SVD (exact rank known = 48)
        U, Sv, Vt = np.linalg.svd(Ci.astype(float), full_matrices=False)
        print(f"[SI] svd s[47]={Sv[47]:.3e} s[48]={Sv[48]:.3e} s[0]={Sv[0]:.3e}", flush=True)
        Qr = Vt[:48, :].T  # 79x48 basis of rowspan
        res = {}
        for name, v in cand.items():
            proj = Qr @ (Qr.T @ v)
            err = float(np.linalg.norm(v - proj) / (np.linalg.norm(v) + 1e-300))
            res[name] = round(err, 6)
        inspan = sorted([n for n, e in res.items() if e < 1e-6])
        print(f"[SI] in-rowspan: {len(inspan)}/{len(cand)}", flush=True)
        print("   ", inspan[:20], flush=True)
        json.dump({"candidates": len(cand), "inspan": inspan, "errs": res},
                  open(OUT / "j4_symdict.json", "w"), indent=1, default=str)
    print("[SI] done", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())

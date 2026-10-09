"""26O part 1: full 79-var interface audit with metadata + coupling-block rank
+ greedy minimality (pin-sensitivity) + reduced functionals.
Usage: python scripts/wp6_iface.py [audit|rank|pin]
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
    modes = sys.argv[1:] or ["audit"]
    import numpy as np
    import scipy.sparse as sp
    A, r, keys, E0 = load_xc()
    E, V = A.shape
    rv = {k: i for i, k in enumerate(keys)}
    oldvars = set()
    for i in range(E0):
        oldvars.update(A.getrow(i).indices.tolist())
    newvars = [i for i in range(V) if i not in oldvars]
    An = A[E0:, :]
    touched = set()
    touch_rows = defaultdict(list)
    for i in range(An.shape[0]):
        for j in An.getrow(i).indices.tolist():
            if j in oldvars:
                touched.add(j)
                touch_rows[j].append(i)
    if "audit" in modes:
        out = []
        for j in sorted(touched):
            k = keys[j]
            if k[0] == 't':
                s, lam, dl, d = k[1]
                out.append({"var": str(k), "fam": s[0], "slot": str(s), "lam": lam,
                            "delta": dl, "d": d, "nrows": len(touch_rows[j])})
            else:
                out.append({"var": str(k), "fam": str(k[0]), "nrows": len(touch_rows[j])})
        fam = Counter()
        for o in out:
            fam[o["fam"]] += 1
        print(f"[IF] interface touched={len(touched)} fams={dict(fam)}", flush=True)
        # semantic groups: depth distribution
        dd = Counter()
        for o in out:
            dd[o.get("d", "-")] += 1
        print("[IF] by depth:", dict(sorted(dd.items(), key=str)), flush=True)
        json.dump(out, open(OUT / "j4_iface_full.json", "w"), indent=1, default=str)
    if "rank" in modes:
        from scipy.optimize import linprog
        Bm = An[:, sorted(touched)].toarray()
        u, svals, vt = np.linalg.svd(Bm, full_matrices=False)
        tol = max(Bm.shape) * np.finfo(float).eps * (svals[0] if len(svals) else 0.0)
        rnk = int((svals > tol).sum())
        print(f"[IF] coupling block {Bm.shape}: numrank={rnk} (tol={tol:.2e})", flush=True)
        print(f"[IF] top sing vals: {[round(float(x),3) for x in svals[:8]]}", flush=True)
        print(f"[IF] bottom sing vals: {[round(float(x),3) for x in svals[-5:]]}", flush=True)
        json.dump({"shape": list(Bm.shape), "rank": rnk, "top": [float(x) for x in svals[:8]]},
                  open(OUT / "j4_ifacerank.json", "w"), indent=1)
    if "pin" in modes:
        # greedy sensitivity: pin each touched coord to joint-opt value, test extension.
        # First get joint-opt witness over full system.
        from scipy.optimize import linprog
        t0 = [i for i, k in enumerate(keys) if k[0] == 't'][0]
        keep = [i for i in range(V) if i != t0]
        Aub = sp.hstack([-A[:, keep], np.ones((E, 1))]).tocsr()
        cobj = np.zeros(len(keep) + 1); cobj[-1] = -1.0
        res = linprog(cobj, A_ub=Aub, b_ub=-r, bounds=[(None, None)] * len(keep) + [(None, 1e6)], method="highs")
        g = np.zeros(V); g[keep] = res.x[:len(keep)]
        print(f"[IF] joint witness margin={float(-res.fun)}", flush=True)
        # new-layer-only feasibility with ALL old frozen = sanity (must pass: joint witness)
        # then per-coord release test is expensive; instead test pinning each coord to a
        # DIFFERENT value (witness value + delta) and check feasibility change? Cheaper:
        # for each coord, fix it to witness value and check new-layer max-min margin DEGRADATION
        # vs unpinned. Coordinates whose pinning never binds are irrelevant.
        # Implementation: for each j in touched: solve new-layer maxmin with x_j fixed.
        An2 = An
        rn2 = r[E0:]
        import scipy.sparse as _sp
        # baseline: new-layer margin with old TOTALLY free (only new rows) -- unbounded likely;
        # instead measure: max over newvars of row slacks? Use margin with old pinned at witness:
        base_keep = [i for i in range(V) if i != t0]
        # precompute column index map
        results = []
        for j in sorted(touched):
            # fix x_j = g[j]: substitute into new rows (A_ub form with margin var)
            # variables: all except t0; x_j fixed.
            keepj = [i for i in base_keep if i != j]
            # A_ub rows: -Anew[:,keepj], margin col; bub = -(rnew - Anew[:,j]*g[j])
            Anew = An2.tocsc()[:, keepj]
            Aubj = _sp.hstack([-Anew, np.ones((An2.shape[0], 1))]).tocsr()
            colj = np.asarray(An2[:, j].toarray()).ravel()
            bubj = -(rn2 - colj * g[j])
            cj = np.zeros(len(keepj) + 1); cj[-1] = -1.0
            rr = linprog(cj, A_ub=Aubj, b_ub=bubj, bounds=[(None, None)] * len(keepj) + [(None, 1e6)], method="highs")
            m = float(-rr.fun) if rr.status == 0 else None
            results.append({"var": str(keys[j]), "margin": m, "status": rr.status})
        # baseline unpinned margin over new rows alone (free old): likely +inf; use joint margin as ref
        nbind = sum(1 for x in results if x["margin"] is not None and x["margin"] < -1e-7)
        print(f"[IF] pinned-single-coord: {len(results)} tested, {nbind} bind (margin<0)", flush=True)
        worst = sorted([x for x in results if x["margin"] is not None], key=lambda x: x["margin"])[:10]
        for x in worst:
            print(f"    {x['margin']:.3f} {x['var']}", flush=True)
        json.dump(results, open(OUT / "j4_ifacepin.json", "w"), indent=1, default=str)
    print("[IF] done", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())

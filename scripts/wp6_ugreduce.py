"""UG-reduced SH567: substitute 6 gap pairs (x2 -> x1+1), rank/nullity/feasibility,
LP implication tests for newly forced recurrences.
Usage: python scripts/wp6_ugreduce.py [build|implications]
"""
import sys, json
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
OUT = ROOT / "artifacts/v04/wp6_present/0909c74a/dual_mine"

def load_all():
    import scipy.sparse as sp
    import importlib.util
    spec = importlib.util.spec_from_file_location('j4', str(ROOT / 'scripts' / 'wp6_j4shared.py'))
    j4 = importlib.util.module_from_spec(spec); spec.loader.exec_module(j4)
    raw, info = j4.build_shared([5, 6, 7])
    Amat, rhs, metas, vmap = j4.assemble(raw)
    return j4, Amat, rhs, metas, vmap

def ug_pairs(vmap):
    dom = json.load(open(OUT / "j4_gapdomain.json"))
    pairs = []
    for (k, dl, d) in dom["overlap"]:
        key1 = ('t', (('F', k), 1, dl, d)); key2 = ('t', (('F', k), 2, dl, d))
        assert key1 in vmap and key2 in vmap, (k, dl, d)
        pairs.append((vmap[key2], vmap[key1]))  # (elim, keep)
    return pairs

def reduce_system(Amat, rhs, vmap, pairs):
    import scipy.sparse as sp
    A = Amat.tolil()
    r = rhs.copy()
    elim = [e for (e, k) in pairs]
    for (e, k) in pairs:
        col = A[:, e].toarray().ravel()
        A[:, k] = A[:, k].toarray().ravel() + col
        r = r - col  # x_e = x_k + 1
    keep = [i for i in range(A.shape[1]) if i not in set(elim)]
    return A[:, keep].tocsr(), r, keep

def mod_rank(A, p=1000000007):
    M = (A.toarray().astype(np.int64) % p)
    E, V = M.shape
    r = 0
    for c in range(V):
        sub = M[r:, c]
        nz = np.flatnonzero(sub)
        if nz.size == 0:
            continue
        i = r + int(nz[0])
        M[[r, i]] = M[[i, r]]
        inv = pow(int(M[r, c]), p - 2, p)
        M[r, c:] = (M[r, c:] * inv) % p
        if r + 1 < E:
            col = M[r + 1:, c]
            m = col != 0
            if m.any():
                blk = M[r + 1:, c:]
                blk[m] = (blk[m] - (col[m].reshape(-1, 1) * M[r, c:].reshape(1, -1)) % p) % p
        r += 1
        if r == E:
            break
    return r

def main():
    modes = sys.argv[1:] or ["build"]
    j4, Amat, rhs, metas, vmap = load_all()
    E, V = Amat.shape
    pairs = ug_pairs(vmap)
    print(f"[UG] base E={E} V={V} gap-pairs={len(pairs)}", flush=True)
    Ared, rred, keep = reduce_system(Amat, rhs, vmap, pairs)
    inv = {i: k for k, i in vmap.items()}
    kept_keys = [inv[i] for i in keep]
    print(f"[UG] reduced E={Ared.shape[0]} V={Ared.shape[1]}", flush=True)
    rnk = mod_rank(Ared)
    print(f"[UG] reduced rank={rnk} nullity={Ared.shape[1]-rnk}", flush=True)
    # feasibility (gauge: fix 2 globals among kept)
    from scipy.optimize import linprog
    import scipy.sparse as sp
    tkeys = [i for i, k in enumerate(kept_keys) if k[0] == 't']
    rkeys = [i for i, k in enumerate(kept_keys) if k[0] == 'r']
    # find global-ish refs: use first t/r
    gfix = [tkeys[0], rkeys[0]]
    k2 = [i for i in range(len(keep)) if i not in set(gfix)]
    Aub = sp.hstack([-Ared[:, k2], np.ones((E, 1))]).tocsr()
    cobj = np.zeros(len(k2) + 1); cobj[-1] = -1.0
    res = linprog(cobj, A_ub=Aub, b_ub=-rred, bounds=[(None, None)] * len(k2) + [(None, 1e6)], method="highs")
    margin = float(-res.fun) if res.status == 0 else None
    print(f"[UG] reduced feas status={res.status} margin={margin}", flush=True)
    out = {"E": E, "V0": V, "Vred": Ared.shape[1], "rank": rnk,
           "nullity": Ared.shape[1] - rnk, "status": res.status, "margin": margin}
    json.dump(out, open(OUT / "j4_ugreduced.json", "w"), indent=1, default=str)
    if "implications" in modes:
        # gauge-fixed full-space min/max for candidate recurrences
        # fix gauge vars to 0 via equality for bounded LPs
        Vv = len(keep)
        # Build equality: gauge pins (2). NONE ids already quotient? keep raw + pins.
        # For implication ranges use: min/max c^Tx s.t. Ax>=rhs, x[gfix]=0
        from scipy.optimize import linprog as lp
        nEQ = 2
        er = [0, 1]; ec = gfix; ev = [1.0, 1.0]
        Aeq = sp.csr_matrix((np.array(ev), (np.array(er), np.array(ec))), shape=(nEQ, Vv))
        beq = np.zeros(nEQ)
        key2idx = {k: i for i, k in enumerate(kept_keys)}
        tests = {}
        # rho second differences: need rho var keys ('r', c)
        for c0 in (-2, -1, 0):
            a, b, cc = ('r', c0 - 1), ('r', c0), ('r', c0 + 1)
            if a in key2idx and b in key2idx and cc in key2idx:
                c = np.zeros(Vv)
                c[key2idx[a]] = 1.0; c[key2idx[b]] = -2.0; c[key2idx[cc]] = 1.0
                r1 = lp(c, A_ub=-Ared, b_ub=-rred, A_eq=Aeq, b_eq=beq, bounds=[(None, None)] * Vv, method="highs")
                r2 = lp(-c, A_ub=-Ared, b_ub=-rred, A_eq=Aeq, b_eq=beq, bounds=[(None, None)] * Vv, method="highs")
                mn = float(r1.fun) if r1.status == 0 else None
                mx = float(-r2.fun) if r2.status == 0 else None
                tests[f"rho2nd_{c0}"] = [mn, mx]
                print(f"[UG] rho2nd({c0-1},{c0},{c0+1}): [{mn},{mx}]", flush=True)
        # fringe delta-first-differences for lam=1 (base f): j(F1,1,d+1,2)-j(F1,1,d,2)
        for dl in (-1, 0, 1):
            a = ('t', (('F', 1), 1, dl, 2)); b = ('t', (('F', 1), 1, dl + 1, 2))
            if a in key2idx and b in key2idx:
                c = np.zeros(Vv); c[key2idx[b]] = 1.0; c[key2idx[a]] = -1.0
                r1 = lp(c, A_ub=-Ared, b_ub=-rred, A_eq=Aeq, b_eq=beq, bounds=[(None, None)] * Vv, method="highs")
                r2 = lp(-c, A_ub=-Ared, b_ub=-rred, A_eq=Aeq, b_eq=beq, bounds=[(None, None)] * Vv, method="highs")
                mn = float(r1.fun) if r1.status == 0 else None
                mx = float(-r2.fun) if r2.status == 0 else None
                tests[f"f_d1_{dl}"] = [mn, mx]
                print(f"[UG] f-delta({dl}->{dl+1}): [{mn},{mx}]", flush=True)
        # N increments: proxy via NONE vars (NONE,0,-1,d): N_d value; increment (d+1)N_{d+1}-d N_d not linear in vars... use N_d diff
        for d in (1, 2, 3):
            a = ('t', (('NONE',), 0, -1, d)); b = ('t', (('NONE',), 0, -1, d + 1))
            if a in key2idx and b in key2idx:
                c = np.zeros(Vv); c[key2idx[b]] = 1.0; c[key2idx[a]] = -1.0
                r1 = lp(c, A_ub=-Ared, b_ub=-rred, A_eq=Aeq, b_eq=beq, bounds=[(None, None)] * Vv, method="highs")
                r2 = lp(-c, A_ub=-Ared, b_ub=-rred, A_eq=Aeq, b_eq=beq, bounds=[(None, None)] * Vv, method="highs")
                mn = float(r1.fun) if r1.status == 0 else None
                mx = float(-r2.fun) if r2.status == 0 else None
                tests[f"N_{d}"] = [mn, mx]
                print(f"[UG] N({d}->{d+1}): [{mn},{mx}]", flush=True)
        # N increments with FULL quotient (NONE ids + gauge pins)
        from collections import defaultdict as dd
        fams = dd(list)
        for kk, ii in key2idx.items():
            t = kk
            if t[0] == 't' and t[1][0] == ('NONE',):
                fams[t[1][3]].append((t[1][2], ii))
        er2, ec2, ev2, beq2 = [0, 1], gfix, [1.0, 1.0], [0.0, 0.0]
        for dy, lst in sorted(fams.items()):
            base = [ii for (dl, ii) in lst if dl == -1]
            if not base:
                continue
            base = base[0]
            for (dl, ii) in lst:
                if dl != -1:
                    er2 += [len(beq2), len(beq2)]; ec2 += [ii, base]; ev2 += [1.0, -1.0]
                    beq2.append(0.0)
        AeqF = sp.csr_matrix((np.array(ev2), (np.array(er2), np.array(ec2))), shape=(len(beq2), Vv))
        beqF = np.array(beq2)
        for d in (1, 2, 3, 4, 5):
            a = ('t', (('NONE',), 0, -1, d)); b = ('t', (('NONE',), 0, -1, d + 1))
            if a in key2idx and b in key2idx:
                c = np.zeros(Vv); c[key2idx[b]] = (d + 1); c[key2idx[a]] = -d
                r1 = lp(c, A_ub=-Ared, b_ub=-rred, A_eq=AeqF, b_eq=beqF, bounds=[(None, None)] * Vv, method="highs")
                r2 = lp(-c, A_ub=-Ared, b_ub=-rred, A_eq=AeqF, b_eq=beqF, bounds=[(None, None)] * Vv, method="highs")
                mn = float(r1.fun) if r1.status == 0 else None
                mx = float(-r2.fun) if r2.status == 0 else None
                tests[f"Nagg_{d}"] = [mn, mx]
                print(f"[UG] NONE-agg (d+1)N-dN, d={d}: [{mn},{mx}]", flush=True)
        json.dump(tests, open(OUT / "j4_ugimplications.json", "w"), indent=1, default=str)
    print("[UG] done", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())

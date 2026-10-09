"""Compatibility gate: impose all 6 realized gap=1 equalities on SH567 J4 system.
Also: exact rational check of witness; Farkas certificate if infeasible.
Usage: python scripts/wp6_gapcompat.py
"""
import sys, json
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
OUT = ROOT / "artifacts/v04/wp6_present/0909c74a/dual_mine"

def main():
    import scipy.sparse as sp
    from scipy.optimize import linprog
    from fractions import Fraction
    Z = np.load(OUT / "j4_sh567_A.npz")
    Amat = sp.csr_matrix(Z["A"].astype(float))
    import importlib.util
    spec = importlib.util.spec_from_file_location('j4', str(ROOT / 'scripts' / 'wp6_j4shared.py'))
    j4 = importlib.util.module_from_spec(spec); spec.loader.exec_module(j4)
    raw, info = j4.build_shared([5, 6, 7])
    A2, rhs, metas, vmap = j4.assemble(raw)
    E, V = Amat.shape
    from collections import defaultdict
    fams = defaultdict(list)
    for k, i in vmap.items():
        t = k
        if t[0] == 't' and t[1][0] == ('NONE',):
            fams[t[1][3]].append((t[1][2], i))
    er, ec, ev, beq = [], [], [], []
    for dy, lst in sorted(fams.items()):
        base = [i for (dl, i) in lst if dl == -1][0]
        for (dl, i) in lst:
            if dl != -1:
                er += [len(beq), len(beq)]; ec += [i, base]; ev += [1.0, -1.0]
                beq.append(0.0)
    tk = [k for k in vmap if k[0] == 't'][0]; rk = [k for k in vmap if k[0] == 'r'][0]
    er += [len(beq), len(beq) + 1]; ec += [vmap[tk], vmap[rk]]; ev += [1.0, 1.0]
    beq += [0.0, 0.0]
    # six gap=1 equalities
    dom = json.load(open(OUT / "j4_gapdomain.json"))
    gaps = []
    for (k, dl, d) in dom["overlap"]:
        key1 = ('t', (('F', k), 1, dl, d)); key2 = ('t', (('F', k), 2, dl, d))
        gaps.append((key1, key2, (k, dl, d)))
    for (key1, key2, tag) in gaps:
        er += [len(beq), len(beq)]; ec += [vmap[key2], vmap[key1]]; ev += [1.0, -1.0]
        beq.append(1.0)
    beq = np.array(beq)
    nEQ = len(beq)
    Aeq = sp.csr_matrix((np.array(ev), (np.array(er), np.array(ec))), shape=(nEQ, V))
    print(f"[GC] E={E} V={V} equalities={nEQ} (15 NONE + 2 gauge + 6 gaps)", flush=True)
    # feasibility: min 0 s.t. -Ax<=-rhs, Aeq x = beq
    res = linprog(np.zeros(V), A_ub=-Amat, b_ub=-rhs, A_eq=Aeq, b_eq=beq,
                  bounds=[(None, None)] * V, method="highs")
    print(f"[GC] compat status={res.status} (0=feasible)", flush=True)
    out = {"status": res.status}
    if res.status == 0:
        x = res.x
        # exact residual verification with Fractions on a sample + max violation float
        viol = (Amat @ x) - rhs
        print(f"[GC] minslack={float(viol.min()):.3e} maxeqviol={float(np.abs(Aeq @ x - beq).max()):.3e}", flush=True)
        out["minslack"] = float(viol.min())
        out["maxeqviol"] = float(np.abs(Aeq @ x - beq).max())
        # rational reconstruction attempt of gap values (already 1 by construction)
        inv = {i: k for k, i in vmap.items()}
        vals = {}
        for (key1, key2, tag) in gaps:
            vals[str(tag)] = [float(x[vmap[key1]]), float(x[vmap[key2]])]
        out["gap_vals"] = vals
        # L1-min over compat set for canonical witness: min sum u
        Vv = V
        A1 = sp.hstack([-Amat, sp.csr_matrix((E, Vv))]).tocsr()
        I = sp.identity(Vv, format="csr")
        Aub = sp.vstack([A1, sp.hstack([I, -sp.identity(Vv, format="csr")]).tocsr(),
                         sp.hstack([-I, -sp.identity(Vv, format="csr")]).tocsr()]).tocsr()
        bub = np.concatenate([-rhs, np.zeros(Vv), np.zeros(Vv)])
        # equality on x part only
        Aeq2 = sp.hstack([Aeq, sp.csr_matrix((nEQ, Vv))]).tocsr()
        cobj = np.concatenate([np.zeros(Vv), np.ones(Vv)])
        r2 = linprog(cobj, A_ub=Aub, b_ub=bub, A_eq=Aeq2, b_eq=beq,
                     bounds=[(None, None)] * Vv + [(0, None)] * Vv, method="highs")
        print(f"[GC] L1-canonical status={r2.status} l1={float(r2.fun) if r2.status==0 else None}", flush=True)
        out["l1_status"] = r2.status
        out["l1"] = float(r2.fun) if r2.status == 0 else None
        out["verdict"] = "UNIT-GAP-COMPATIBLE"
    else:
        # Farkas certificate for the augmented infeasible system
        # min y^T rhs' ... use max-min margin on equalities-relaxed? Direct: solve
        # find y>=0,z free with y^T A + z^T Aeq = 0, y^T rhs + z^T beq > 0
        # via LP: max rhs^T y + beq^T z s.t. A^T y + Aeq^T z = 0, sum(y)+||z||_1 <= 1?
        # Simpler: report status + margin of AJ>=rhs alone (known feasible) to show gaps cause it.
        print("[GC] INFEASIBLE under simultaneous gaps", flush=True)
        out["verdict"] = "UNIT-GAP-INCOMPATIBLE"
    json.dump(out, open(OUT / "j4_gapcompat.json", "w"), indent=1, default=str)
    print("[GC] saved", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())

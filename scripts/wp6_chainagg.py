"""Chain aggregate gap min/max with correct realizability (d_T=3,k=3 family)."""
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
    er, ec, ev = [], [], []
    beq_list = []
    for dy, lst in sorted(fams.items()):
        base = [i for (dl, i) in lst if dl == -1][0]
        for (dl, i) in lst:
            if dl != -1:
                er += [len(beq_list), len(beq_list)]; ec += [i, base]; ev += [1.0, -1.0]
                beq_list.append(0.0)
    tk = [k for k in vmap if k[0] == 't'][0]; rk = [k for k in vmap if k[0] == 'r'][0]
    er += [len(beq_list), len(beq_list) + 1]; ec += [vmap[tk], vmap[rk]]; ev += [1.0, 1.0]
    beq_list += [0.0, 0.0]
    import numpy as _np
    beq = _np.array(beq_list)
    nEQ = len(beq_list)
    Aeq = sp.csr_matrix((np.array(ev), (np.array(er), np.array(ec))), shape=(nEQ, V))
    # chain C_m in sibling: depths 0..m-1; d_T=3 -> delta=-3+k; d_B(y)=4; k=3
    out = []
    for m in (1, 2, 3, 4, 5):
        c = np.zeros(V); ok = True
        used = []
        for kk in range(m):
            dl = kk - 3
            key1 = ('t', (('F', 3), 1, dl, 4)); key2 = ('t', (('F', 3), 2, dl, 4))
            if key1 not in vmap or key2 not in vmap:
                print(f"[CH] m={m}: missing var dl={dl}", flush=True)
                ok = False; break
            c[vmap[key2]] += 1.0; c[vmap[key1]] -= 1.0
            used.append(dl)
        if not ok:
            out.append({"m": m, "deltas": used, "min": None, "max": None}); continue
        rmin = linprog(c, A_ub=-Amat, b_ub=-rhs, A_eq=Aeq, b_eq=beq,
                       bounds=[(None, None)] * V, method="highs")
        rmax = linprog(-c, A_ub=-Amat, b_ub=-rhs, A_eq=Aeq, b_eq=beq,
                       bounds=[(None, None)] * V, method="highs")
        mn = float(rmin.fun) if rmin.status == 0 else None
        mx = float(-rmax.fun) if rmax.status == 0 else None
        print(f"[CH] chain d=3,k=3 m={m} deltas={used}: min={mn} max={mx}", flush=True)
        out.append({"m": m, "deltas": used, "min": mn, "max": mx})
    json.dump(out, open(OUT / "j4_chainranges.json", "w"), indent=1)
    print("[CH] done", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())

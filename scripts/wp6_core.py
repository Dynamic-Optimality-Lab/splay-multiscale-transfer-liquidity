"""26O part 2: DTQ-augmented system, projection ranges, fixed-point attempt,
old-F firewall check.
Usage: python scripts/wp6_core.py [dtq|proj|fix|firewall]
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
    modes = sys.argv[1:] or ["dtq"]
    import numpy as np
    from scipy.optimize import linprog
    import scipy.sparse as sp
    A, r, keys, E0 = load_xc()
    E, V = A.shape
    rv = {k: i for i, k in enumerate(keys)}
    if "dtq" in modes:
        # DTQ equations: canonical shift forms (quotient-mapped) = 0, on xclean system.
        forms = json.load(open(OUT / "j4_shiftdeep.json"))
        dom = json.load(open(OUT / "j4_gapdomain.json"))
        UGMAP = {}
        for (k, dl, d) in dom["overlap"]:
            UGMAP[(('F', k), 2, dl, d)] = ((('F', k), 1, dl, d))
        eqs = []
        nskip = 0
        for o in forms:
            net = Counter({eval(k): v for k, v in o["terms"]})
            c = np.zeros(V)
            miss = 0
            for kk, cc in net.items():
                if kk[0] == 'K':
                    # expand K_d to member NONE t-vars (exact aggregate definition)
                    for dl in range(-kk[1], 0):
                        t = ('t', (('NONE',), 0, dl, kk[1]))
                        if t in rv:
                            c[rv[t]] += cc
                        else:
                            miss += 1
                else:
                    t = kk[1]
                    if t in UGMAP:
                        t = UGMAP[t]
                    if t[0] == ('NONE',):
                        kk2 = ('K', t[3])
                        if kk2 in rv:
                            c[rv[kk2]] += cc
                        else:
                            miss += 1
                    elif ('t', t) in rv:
                        c[rv[('t', t)]] += cc
                    else:
                        miss += 1
            if miss:
                nskip += 1
                continue
            eqs.append(c)
        print(f"[CO] DTQ equations usable: {len(eqs)}/{len(forms)}", flush=True)
        if eqs:
            nEQ = len(eqs)
            Aeq = sp.vstack([sp.csr_matrix(c).reshape(1, -1) for c in eqs]).tocsr()
            beq = np.zeros(nEQ)
            t0 = [i for i, k in enumerate(keys) if k[0] == 't'][0]
            keep = [i for i in range(V) if i != t0]
            import scipy.sparse as _sp
            AeqK = _sp.hstack([Aeq[:, keep], _sp.csr_matrix((nEQ, 1))]).tocsr()
            Aub = _sp.hstack([-A[:, keep], np.ones((E, 1))]).tocsr()
            cobj = np.zeros(len(keep) + 1); cobj[-1] = -1.0
            res = linprog(cobj, A_ub=Aub, b_ub=-r, A_eq=AeqK, b_eq=beq,
                          bounds=[(None, None)] * len(keep) + [(None, 1e6)], method="highs")
            margin = float(-res.fun) if res.status == 0 else None
            print(f"[CO] DTQ-xclean joint: status={res.status} margin={margin}", flush=True)
            json.dump({"neqs": nEQ, "status": res.status, "margin": margin},
                      open(OUT / "j4_dtqaug.json", "w"), indent=1, default=str)
        else:
            json.dump({"neqs": 0, "status": "no-equations"}, open(OUT / "j4_dtqaug.json", "w"), indent=1)
    if "proj" in modes:
        # projection ranges: min/max per interface coord over JOINT feasible set
        iface = json.load(open(OUT / "j4_iface_full.json"))
        t0 = [i for i, k in enumerate(keys) if k[0] == 't'][0]
        Aeq0 = sp.csr_matrix(([1.0], ([0], [t0])), shape=(1, V))
        beq0 = np.zeros(1)
        out = []
        for o in iface:
            k = eval(o["var"])
            if k not in rv:
                out.append({"var": o["var"], "status": "not-in-system"})
                continue
            c = np.zeros(V)
            c[rv[k]] = 1.0
            r1 = linprog(c, A_ub=-A, b_ub=-r, A_eq=Aeq0, b_eq=beq0, bounds=[(None, None)] * V, method="highs")
            r2 = linprog(-c, A_ub=-A, b_ub=-r, A_eq=Aeq0, b_eq=beq0, bounds=[(None, None)] * V, method="highs")
            mn = float(r1.fun) if r1.status == 0 else None
            mx = float(-r2.fun) if r2.status == 0 else None
            out.append({"var": o["var"], "min": mn, "max": mx,
                        "width": (mx - mn) if (mn is not None and mx is not None) else None})
        nfin = sum(1 for x in out if x.get("width") is not None and x["width"] < 1e6)
        print(f"[CO] projection: {len(out)} coords, finite-width={nfin}", flush=True)
        wide = sorted([x for x in out if x.get("width") is not None], key=lambda x: -x["width"])[:10]
        for x in wide:
            print(f"    width={x['width']:.2f} {x['var']}", flush=True)
        json.dump(out, open(OUT / "j4_proj.json", "w"), indent=1, default=str)
    if "firewall" in modes:
        iface = json.load(open(OUT / "j4_iface_full.json"))
        # old-F j0 presence in interface: F atoms with j0>5? and max j0
        js = []
        for o in iface:
            k = eval(o["var"])
            if k[0] == 't' and isinstance(k[1], tuple) and k[1][0][0] == 'F':
                js.append(k[1][0][1])
        print(f"[CO] interface F j0 values: {sorted(set(js))}", flush=True)
        # NONE depths in interface
        ns = sorted({eval(o["var"])[1] for o in iface if eval(o["var"])[0] == 'K'} | \
                    {eval(o["var"])[1][3] for o in iface if eval(o["var"])[0] == 't' and eval(o["var"])[1][0] == ('NONE',)})
        print(f"[CO] interface NONE/K depths: {ns}", flush=True)
        json.dump({"F_j0": sorted(set(js)), "none_depths": ns}, open(OUT / "j4_firewall.json", "w"), indent=1, default=str)
    print("[CO] done", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())

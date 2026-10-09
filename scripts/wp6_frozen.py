"""26N analysis on xclean expanded matrix: t=3 shift forms + ranges + DTQ gate;
frozen-witness extension (3 diverse base witnesses); interface state.
Usage: python scripts/wp6_frozen2.py [shift|frozen|iface]
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
from wp6_staticR import depths_list
from wp6_lambda import R_coeffs
import wp6_cycle_ratio as O

def shift(T, s):
    if T is None:
        return None
    return [T[0] + s, shift(T[1], s), shift(T[2], s)]

def full_P_row(B, y):
    _, lam = R_coeffs(B, y)
    dB = depths_list(B)
    ms = Counter()
    for z in dB:
        if z == y:
            continue
        ms[('t', (j4.slot_of(B, y, z), lam.get(z, 0), dB[z] - dB[y], dB[y]))] += 1
    if dB[y] != 0:
        ms[('K', dB[y])] += dB[y]
    return ms

def lift2_spaced(T):
    mx = max(depths_list(T).keys())
    return [mx + 6, [mx + 3, copy.deepcopy(T), None], None]

def load_xc():
    import numpy as np
    Z = np.load(OUT / "j4_xclean_mat.npz")
    import scipy.sparse as sp
    A = sp.csr_matrix(Z["A"])
    r = Z["rhs"]
    keys = [eval(k) for k in Z["keys"]]
    E0 = int(Z["E0"][0])
    return A, r, keys, E0

def main():
    modes = sys.argv[1:] or ["shift"]
    import numpy as np
    from scipy.optimize import linprog
    import scipy.sparse as sp
    A, r, keys, E0 = load_xc()
    E, V = A.shape
    rv = {k: i for i, k in enumerate(keys)}
    dom = json.load(open(OUT / "j4_gapdomain.json"))
    UGMAP = {}
    for (k, dl, d) in dom["overlap"]:
        UGMAP[(('F', k), 2, dl, d)] = ((('F', k), 1, dl, d))
    t0 = [i for i, k in enumerate(keys) if k[0] == 't'][0]
    Aeq0 = sp.csr_matrix(([1.0], ([0], [t0])), shape=(1, V))
    beq0 = np.zeros(1)
    def qform(net):
        c = np.zeros(V)
        miss = 0
        for kk, cc in net.items():
            if kk[0] == 'K':
                if kk in rv:
                    c[rv[kk]] += cc
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
        return c, miss
    if "shift" in modes:
        # t=3 shift chains (3 levels, all rows now in-system via expansion)
        recs = []
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
                B0, B1, B2 = ext(T0), ext(T1), ext(T2)
                for BB in (B0, B1, B2, T0, T1, T2):
                    vl.assert_valid_bst(BB)
                if len(depths_list(B2)) > 11:
                    continue
                for u in sorted(depths_list(Tr).keys()):
                    for v in sorted(depths_list(Tr).keys()):
                        if u >= v:
                            continue
                        def dbar(BA, TA, BB, TB):
                            net = Counter()
                            for (X, yy, sgn) in ((BB, u, 1), (BB, v, -1), (TB, u, -1), (TB, v, 1),
                                                (BA, u, -1), (BA, v, 1), (TA, u, 1), (TA, v, -1)):
                                for kk, cc in full_P_row(X, yy).items():
                                    net[kk] += sgn * cc
                            return Counter({k: v2 for k, v2 in net.items() if v2 != 0})
                        lo = dbar(B0, T0, B1, T1)
                        hi = dbar(B1, T1, B2, T2)
                        net = Counter()
                        for kk, cc in hi.items():
                            net[kk] += cc
                        for kk, cc in lo.items():
                            net[kk] -= cc
                        net = Counter({k: v2 for k, v2 in net.items() if v2 != 0})
                        recs.append(((3, s, u, v), net))
        seen = {}
        for meta, net in recs:
            key = tuple(sorted((str(k), v) for k, v in net.items()))
            seen.setdefault(key, []).append(meta)
        print(f"[FZ] raw shift instances={len(recs)} canonical={len(seen)}", flush=True)
        out = []
        for key, ml in seen.items():
            net = Counter({eval(k): v for k, v in key})
            fams = Counter()
            for kk in net:
                fams[kk[0] if kk[0] == 'K' else kk[1][0][0]] += 1
            out.append({"meta": [list(m) for m in ml], "sup": len(net), "fams": dict(fams),
                        "terms": [[k, v] for k, v in key]})
        out.sort(key=lambda x: -len(x["meta"]))
        for o in out[:10]:
            print(f"    count={len(o['meta'])} sup={o['sup']} fams={o['fams']} e.g.{o['meta'][0]}", flush=True)
        json.dump(out, open(OUT / "j4_shiftdeep.json", "w"), indent=1, default=str)
        # ranges + joint DTQ on closed ones (NATIVE xclean coords: raw t incl
        # raw NONE t-vars; UG twins mapped; NO K_d (absent here by design))
        ranges = []
        closed = []
        for o in out:
            net = Counter({eval(k): v for k, v in o["terms"]})
            c = np.zeros(V)
            miss = 0
            for kk, cc in net.items():
                if kk[0] == 'K':
                    # K_d = sum of chain NONE members: expand (exact aggregate definition)
                    d = kk[1]
                    for dl in range(-d, 0):
                        t = ('t', (('NONE',), 0, dl, d))
                        if t in rv:
                            c[rv[t]] += cc
                        else:
                            miss += 1
                else:
                    t = kk[1]
                    if t in UGMAP:
                        t = UGMAP[t]
                    if ('t', t) in rv:
                        c[rv[('t', t)]] += cc
                    else:
                        miss += 1
            if miss:
                ranges.append({"meta": o["meta"], "status": f"missing-{miss}"})
                continue
            r1 = linprog(c, A_ub=-A, b_ub=-r, A_eq=Aeq0, b_eq=beq0, bounds=[(None, None)] * V, method="highs")
            r2 = linprog(-c, A_ub=-A, b_ub=-r, A_eq=Aeq0, b_eq=beq0, bounds=[(None, None)] * V, method="highs")
            mn = float(r1.fun) if r1.status == 0 else None
            mx = float(-r2.fun) if r2.status == 0 else None
            ranges.append({"meta": o["meta"], "min": mn, "max": mx})
            print(f"[FZ] range e.g.{o['meta'][0]}: [{mn},{mx}]", flush=True)
            closed.append(c)
        if closed:
            nEQ = len(closed)
            er, ec, ev = [], [], []
            for i, c in enumerate(closed):
                nz = np.flatnonzero(c)
                for j in nz:
                    er.append(i); ec.append(j); ev.append(float(c[j]))
            Aeq = sp.csr_matrix((np.array(ev), (np.array(er), np.array(ec))), shape=(nEQ, V))
            beq = np.zeros(nEQ)
            keep = [i for i in range(V) if i != t0]
            import scipy.sparse as _sp
            AeqK = _sp.hstack([Aeq[:, keep], _sp.csr_matrix((nEQ, 1))]).tocsr()
            Aub = _sp.hstack([-A[:, keep], np.ones((E, 1))]).tocsr()
            cobj = np.zeros(len(keep) + 1); cobj[-1] = -1.0
            res = linprog(cobj, A_ub=Aub, b_ub=-r, A_eq=AeqK, b_eq=beq,
                          bounds=[(None, None)] * len(keep) + [(None, 1e6)], method="highs")
            margin = float(-res.fun) if res.status == 0 else None
            print(f"[FZ] deep DTQ joint: status={res.status} margin={margin}", flush=True)
            json.dump({"ranges": ranges, "dtq_status": res.status, "dtq_margin": margin},
                      open(OUT / "j4_deepdtq.json", "w"), indent=1, default=str)
    if "frozen" in modes:
        # frozen-witness extension: 3 diverse base witnesses; freeze SH567 coords; solve new.
        E0loc = E0
        basecols = list(range(V))  # all old; new = cols used only by new rows? use E-split instead:
        # old coords = vars appearing in old rows; new coords = rest
        oldvars = set()
        for i in range(E0loc):
            row = A.getrow(i)
            oldvars.update(row.indices.tolist())
        newvars = [i for i in range(V) if i not in oldvars]
        print(f"[FZ] oldvars={len(oldvars)} newvars={len(newvars)}", flush=True)
        import scipy.sparse as _sp
        # base witnesses: solve base-only system 3 ways
        Ab = A[:E0loc, :]
        rb = r[:E0loc]
        t0b = t0
        wit = []
        # w1: max-margin
        keepb = [i for i in range(V) if i != t0b]
        Aub = _sp.hstack([-Ab[:, keepb], np.ones((E0loc, 1))]).tocsr()
        cobj = np.zeros(len(keepb) + 1); cobj[-1] = -1.0
        r1 = linprog(cobj, A_ub=Aub, b_ub=-rb, bounds=[(None, None)] * len(keepb) + [(None, 1e6)], method="highs")
        g1 = np.zeros(V); g1[keepb] = r1.x[:len(keepb)]
        wit.append(("maxmargin", g1))
        # w2: L1-min (need full vars incl new? base-only: min over base cols)
        from scipy.optimize import linprog as _lp
        Vb = V
        A1 = _sp.hstack([-Ab, _sp.csr_matrix((E0loc, Vb))]).tocsr()
        I = _sp.identity(Vb, format="csr")
        Aub2 = _sp.vstack([A1, _sp.hstack([I, -_sp.identity(Vb, format="csr")]).tocsr(),
                           _sp.hstack([-I, -_sp.identity(Vb, format="csr")]).tocsr()]).tocsr()
        bub2 = np.concatenate([-rb, np.zeros(Vb), np.zeros(Vb)])
        cobj2 = np.concatenate([np.zeros(Vb), np.ones(Vb)])
        r2 = _lp(cobj2, A_ub=Aub2, b_ub=bub2, bounds=[(None, None)] * Vb + [(0, None)] * Vb, method="highs")
        g2 = np.zeros(V)
        if r2.status == 0:
            g2 = r2.x[:Vb]
        wit.append(("l1min", g2))
        # w3: joint-optimum old-projection (positive control: extends by construction)
        AubJ = _sp.hstack([-A, np.ones((E, 1))]).tocsr()
        cobjJ = np.zeros(V + 1); cobjJ[-1] = -1.0
        keepJ = [i for i in range(V) if i != t0]
        AubJ = _sp.hstack([-A[:, keepJ], np.ones((E, 1))]).tocsr()
        cobjJ = np.zeros(len(keepJ) + 1); cobjJ[-1] = -1.0
        rJ = _lp(cobjJ, A_ub=AubJ, b_ub=-r, bounds=[(None, None)] * len(keepJ) + [(None, 1e6)], method="highs")
        gJ = np.zeros(V)
        if rJ.status == 0:
            gJ[keepJ] = rJ.x[:len(keepJ)]
            wit.append(("jointopt", gJ))
        # w4/w5: random-box tilts over base polytope for breadth
        for _r, _tag in ((1, "tilt1"), (2, "tilt2")):
            rng = np.random.RandomState(_r)
            d = rng.uniform(-1, 1, V)
            rbt = _lp(-d, A_ub=-Ab, b_ub=-rb, bounds=[(-5, 5)] * V, method="highs")
            if rbt.status == 0:
                wit.append((_tag, rbt.x))
        print(f"[FZ] witnesses: {[ (t, round(float((Ab @ g - rb).min()),3)) for t, g in wit ]}", flush=True)
        # freeze old coords (all V: new vars are those unused by old rows; freezing old = fix oldvars)
        An = A[E0loc:, :]
        rn = r[E0loc:]
        res_out = []
        for tag, g in wit:
            # fix x[oldvars] = g[oldvars]; solve x[newvars]
            # rows: An @ x >= rn -> An_new x_new >= rn - An_old g_old
            An_old = An[:, sorted(oldvars)]
            An_new = An[:, sorted(newvars)]
            rhs_n = rn - np.asarray((An_old @ g[sorted(oldvars)]).ravel() if isinstance(An_old @ g[sorted(oldvars)], np.matrix) else An_old @ g[sorted(oldvars)]).ravel()
            rr = linprog(np.zeros(len(newvars)), A_ub=-An_new, b_ub=-rhs_n,
                         bounds=[(None, None)] * len(newvars), method="highs")
            print(f"[FZ] frozen-{tag}: status={rr.status}", flush=True)
            res_out.append({"tag": tag, "status": rr.status})
        json.dump(res_out, open(OUT / "j4_frozen.json", "w"), indent=1, default=str)
    if "iface" in modes:
        E0loc = E0
        oldvars = set()
        for i in range(E0loc):
            oldvars.update(A.getrow(i).indices.tolist())
        newvars = [i for i in range(V) if i not in oldvars]
        # which old vars appear in new rows?
        An = A[E0loc:, :]
        touched = set()
        for i in range(An.shape[0]):
            touched.update([j for j in An.getrow(i).indices.tolist() if j in oldvars])
        print(f"[FZ] interface: {len(touched)} old vars touched by new rows", flush=True)
        inv = {}
        keys = [eval(k) for k in np.load(OUT / "j4_xclean_mat.npz")["keys"]]
        for j in sorted(touched)[:40]:
            print(f"    {keys[j]}", flush=True)
        json.dump({"ntouched": len(touched),
                   "sample": [str(keys[j]) for j in sorted(touched)[:40]]},
                  open(OUT / "j4_iface.json", "w"), indent=1, default=str)
    print("[FZ] done", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())

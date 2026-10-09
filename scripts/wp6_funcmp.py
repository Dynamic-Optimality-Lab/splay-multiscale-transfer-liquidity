"""Functional compaction probes: (Q) Gamma width-preservation LP over UG-reduced set;
(S) padding-splay commutator structure; (U) Xi vertex diagnostic + transfer sign.
Usage: python scripts/wp6_funcmp.py [width|comm|xi]
"""
import sys, copy, json
from pathlib import Path
import numpy as np
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

UGMAP = {}
def build_ugmap():
    dom = json.load(open(OUT / "j4_gapdomain.json"))
    for (k, dl, d) in dom["overlap"]:
        UGMAP[(('F', k), 2, dl, d)] = ((('F', k), 1, dl, d), 1.0)
    # k=5 new pairs (expanded gate)
    for dl in (-5, -4):
        UGMAP[(('F', 5), 2, dl, 6)] = ((('F', 5), 1, dl, 6), 1.0)

def Jrow_form(B, y):
    """Linear form of J_y(B) in SH567-reduced coords: returns (coefdict, const)."""
    _, lam = R_coeffs(B, y)
    dB = depths_list(B)
    coef = {}
    for z in dB:
        if z == y:
            continue
        t = (j4.slot_of(B, y, z), lam.get(z, 0), dB[z] - dB[y], dB[y])
        if t in UGMAP:
            t2, c = UGMAP[t]
            coef[('t', t2)] = coef.get(('t', t2), 0) + 1.0
        else:
            coef[('t', t)] = coef.get(('t', t), 0) + 1.0
    c, _ = R_coeffs(B, y)
    coef[('r', c)] = coef.get(('r', c), 0) + 1.0
    return coef

def load_reduced():
    import scipy.sparse as sp
    Z = np.load(OUT / "j4_sh567_A.npz")
    A0 = sp.csr_matrix(Z["A"].astype(float))
    spec = importlib.util.spec_from_file_location('j4b', str(ROOT / 'scripts' / 'wp6_j4shared.py'))
    j4b = importlib.util.module_from_spec(spec); spec.loader.exec_module(j4b)
    raw, info = j4b.build_shared([5, 6, 7])
    A2, rhs0, metas0, vmap = j4b.assemble(raw)
    dom = json.load(open(OUT / "j4_gapdomain.json"))
    pairs = []
    for (k, dl, d) in dom["overlap"]:
        pairs.append((vmap[('t', (('F', k), 2, dl, d))], vmap[('t', (('F', k), 1, dl, d))]))
    A = A0.tolil(); r = rhs0.copy()
    elim = [e for (e, k) in pairs]
    for (e, k) in pairs:
        col = A[:, e].toarray().ravel()
        A[:, k] = A[:, k].toarray().ravel() + col
        r = r - col
    keep = [i for i in range(A.shape[1]) if i not in set(elim)]
    inv = {i: kk for kk, i in vmap.items()}
    rvmap = {inv[old]: new for new, old in enumerate(keep)}
    return A[:, keep].tocsr(), r, rvmap

def mode_width():
    from collections import defaultdict
    from scipy.optimize import linprog
    import scipy.sparse as sp
    Ared, rred, rvmap = load_reduced()
    E, Vv = Ared.shape
    allk = list(rvmap.keys())
    tk = [k for k in allk if k[0] == 't'][0]; rk = [k for k in allk if k[0] == 'r'][0]
    gfix = [rvmap[tk], rvmap[rk]]
    out = []
    ntest = npres = 0
    # instances: T sizes 2..4, S sizes 0..2, same-child pairs
    for t in (2, 3, 4):
        for T in O.shapes_of(list(range(1, t + 1))):
            for s in (0, 1, 2):
                Slist = [None] if s == 0 else O.shapes_of(list(range(1, s + 1)))
                for S in Slist:
                    B = [t + 1, copy.deepcopy(T), shift(copy.deepcopy(S), t + 1)] if S is not None else [0, None, copy.deepcopy(T)]
                    nB = t + 1 + s
                    for u in range(1, t + 1):
                        for v in range(u + 1, t + 1):
                            # H diffs as linear forms (H0 const + J coef)
                            fT = Jrow_form(T, u)
                            fTv = Jrow_form(T, v)
                            fB = Jrow_form(B, u)
                            fBv = Jrow_form(B, v)
                            def vec(f):
                                w = np.zeros(Vv)
                                for kk, cc in f.items():
                                    if kk in rvmap:
                                        w[rvmap[kk]] += cc
                                return w
                            wT = vec(fT) - vec(fTv)
                            wB = vec(fB) - vec(fBv)
                            hT = H0(T, u, t) - H0(T, v, t)
                            hB = H0(B, u, nB) - H0(B, v, nB)
                            # max parent diff s.t. |child diff| <= 2:
                            # child: hT + wT.x in [-2,2]; parent obj hB + wB.x max
                            Aub = sp.vstack([-Ared,
                                             wT.reshape(1, -1), -wT.reshape(1, -1)]).tocsr()
                            bub = np.concatenate([-rred, [2 - hT], [2 + hT]])
                            # pin gauge
                            Aeq = sp.csr_matrix((np.ones(2), ([0, 1], gfix)), shape=(2, Vv))
                            beq = np.zeros(2)
                            r1 = linprog(-wB, A_ub=Aub, b_ub=bub, A_eq=Aeq, b_eq=beq,
                                         bounds=[(None, None)] * Vv, method="highs")
                            ntest += 1
                            if r1.status == 0:
                                mx = hB - float(r1.fun)
                                if mx <= 2 + 1e-6:
                                    npres += 1
                                else:
                                    out.append({"t": t, "s": s, "u": u, "v": v, "max": mx})
    from collections import defaultdict as dd
    print(f"[FQ] width preserved: {npres}/{ntest} instances (max parent |diff|<=2 given child<=2)", flush=True)
    for o in out[:10]:
        print(f"    VIOL {o}", flush=True)
    json.dump({"pres": npres, "tot": ntest, "viols": out[:20]}, open(OUT / "j4_fqwidth.json", "w"), indent=1, default=str)
    print("[FQ] saved", flush=True)

def mode_comm():
    # padding-splay commutator: S_{P(x)}(P(B)) vs P(S_x(B)) — tree equality + s0 compare
    tot = same = 0
    s0diffs = {}
    for n in (4, 5):
        for B in O.shapes_of(list(range(1, n + 1))):
            P = [0, None, copy.deepcopy(B)]
            for x in range(1, n + 1):
                # order 1: splay then pad
                Bx = j4.V.replay(copy.deepcopy(B), copy.deepcopy(B), [("K", x)])["endB"]
                P1 = [0, None, copy.deepcopy(Bx)]
                # order 2: pad then splay
                P2 = j4.V.replay(copy.deepcopy(P), copy.deepcopy(P), [("K", x)])["endB"]
                tot += 1
                if json.dumps(P1, sort_keys=True) == json.dumps(P2, sort_keys=True):
                    same += 1
                def s0(T, Tp, xx, N):
                    R = R_static(T, xx); Rp = R_static(Tp, xx)
                    G = N - subsize(T, xx); Gp = N - subsize(Tp, xx)
                    b = 1 if T[0] == xx else 0
                    D0 = R - 2 * (1 - b)
                    return ((-R + j4.KAPPA * G) - (-Rp + j4.KAPPA * Gp)) - D0
                BxB = j4.V.replay(copy.deepcopy(B), copy.deepcopy(B), [("K", x)])["endB"]
                PxP = j4.V.replay(copy.deepcopy(P), copy.deepcopy(P), [("K", x)])["endB"]
                a = s0(B, BxB, x, n); b = s0(P, PxP, x, n + 1)
                s0diffs[round(b - a, 1)] = s0diffs.get(round(b - a, 1), 0) + 1
    print(f"[FQ] commutator tree-equal: {same}/{tot}", flush=True)
    print(f"[FQ] s0(P)-s0(B) distribution: {dict(sorted(s0diffs.items()))}", flush=True)
    json.dump({"same": same, "tot": tot, "s0diff": [[k, v] for k, v in sorted(s0diffs.items())]},
              open(OUT / "j4_fqcomm.json", "w"), indent=1, default=str)

def mode_xi():
    # RAW vertex diagnostic (no UG remap): Xi = Jdrop + s0 over n=5,6 SELF rows.
    # Feasible vertex must satisfy Xi>=-tol in-sample; transfer sign is diagnostic.
    J = dict(json.load(open(OUT / "j4shared_567_l1.json"))["vals"])
    def Jv(B, y):
        _, lam = R_coeffs(B, y)
        dB = depths_list(B)
        tot = 0.0
        for z in dB:
            if z == y:
                continue
            t = ('t', (j4.slot_of(B, y, z), lam.get(z, 0), dB[z] - dB[y], dB[y]))
            tot += J.get(str(t), 0.0)
        c, _ = R_coeffs(B, y)
        return tot + J.get(str(('r', c)), 0.0)
    neg = tot = 0
    trans_neg = trans_tot = 0
    worst = None
    for n in (5, 6):
        for B in O.shapes_of(list(range(1, n + 1))):
            for x in range(1, n + 1):
                Bp = j4.V.replay(copy.deepcopy(B), copy.deepcopy(B), [("K", x)])["endB"]
                R = R_static(B, x); Rp = R_static(Bp, x)
                G = n - subsize(B, x); Gp = n - subsize(Bp, x)
                b = 1 if B[0] == x else 0
                D0 = R - 2 * (1 - b)
                s0 = ((-R + j4.KAPPA * G) - (-Rp + j4.KAPPA * Gp)) - D0
                xi = Jv(B, x) - Jv(Bp, x) + s0
                tot += 1
                if xi < -1e-6:
                    neg += 1
                    if worst is None or xi < worst[0]:
                        worst = (xi, n, x)
                # transfer: padded version
                P = [0, None, copy.deepcopy(B)]
                Pp = j4.V.replay(copy.deepcopy(P), copy.deepcopy(P), [("K", x)])["endB"]
                Rp_ = R_static(P, x); Rpp = R_static(Pp, x)
                Gp_ = (n + 1) - subsize(P, x); Gpp = (n + 1) - subsize(Pp, x)
                bp = 1 if P[0] == x else 0
                D0p = Rp_ - 2 * (1 - bp)
                s0p = ((-Rp_ + j4.KAPPA * Gp_) - (-Rpp + j4.KAPPA * Gpp)) - D0p
                xip = Jv(P, x) - Jv(Pp, x) + s0p
                trans_tot += 1
                if xip < xi - 1e-6:
                    trans_neg += 1
    print(f"[FQ] Xi(vertex+UG) negative: {neg}/{tot} worst={worst}", flush=True)
    print(f"[FQ] Xi decreases under padding: {trans_neg}/{trans_tot}", flush=True)
    json.dump({"neg": neg, "tot": tot, "worst": worst, "trans_neg": trans_neg, "trans_tot": trans_tot},
              open(OUT / "j4_fqxi.json", "w"), indent=1, default=str)

def main():
    modes = sys.argv[1:] or ["width"]
    build_ugmap()
    if "width" in modes:
        mode_width()
    if "comm" in modes:
        mode_comm()
    if "xi" in modes:
        mode_xi()
    return 0

if __name__ == "__main__":
    sys.exit(main())

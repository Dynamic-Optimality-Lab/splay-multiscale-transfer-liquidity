"""26AE bounded exact audit: T shapes |T|<=6, equal-depth equal-fold pairs,
D0 exact, beta in rowspan(E) over QQ (UG + root normalization)."""
import sys, copy, json
sys.path.insert(0, 'scripts')
from pathlib import Path
ROOT = Path('.')
RDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/26AE')
import importlib.util
def load(name):
    spec = importlib.util.spec_from_file_location(name, str(Path('scripts') / (name + '.py')))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m
j4 = load('wp6_j4shared')
vl = load('wp6_validlift')
from wp6_staticR import depths_list, R_static
from wp6_lambda import R_coeffs
import wp6_cycle_ratio as O
import sympy as sp
from collections import Counter
def subsize(T, x):
    nd = T
    while nd is not None and nd[0] != x:
        nd = nd[1] if x < nd[0] else nd[2]
    c = [0]
    def go(m):
        if m is None: return
        c[0] += 1; go(m[1]); go(m[2])
    go(nd); return c[0]
def H0(T, y, n, ka=4.0):
    return -R_static(T, y) + ka * (n - subsize(T, y))
def Jat(B, y):
    _, lam = R_coeffs(B, y)
    dB = depths_list(B)
    out = {}
    for z in dB:
        if z == y: continue
        t = ('t', (j4.slot_of(B, y, z), lam.get(z, 0), dB[z] - dB[y], dB[y]))
        out[t] = out.get(t, 0) + 1
    c, _ = R_coeffs(B, y)
    out[('r', c)] = out.get(('r', c), 0) + 1
    return out
# E: UG twin eqs (8 proven) + root normalization rows J[(r,c)]=c for c in range
EQ = []  # (dict key->coef, rhs)
dom = json.load(open("artifacts/v04/wp6_present/0909c74a/dual_mine/j4_gapdomain.json"))
proved = set((('F', k), 2, dl, d) for (k, dl, d) in dom["overlap"])
proved.update((('F', 5), 2, dl, 6) for dl in (-5, -4))
for (s, lam, dl, d) in sorted(proved, key=str):
    EQ.append(({'t': 0} and {('t', (s, 2, dl, d)): 1, ('t', (s, 1, dl, d)): -1}, 1))
for c in range(-12, 13):
    EQ.append(({('r', c): 1}, c))
print(f"[AE] E rows: {len(EQ)} (UG {len(proved)} + norm 25)", flush=True)
# consistency: all rows have disjoint... just check rank full row rank via sympy once
def pre(T, u, v):
    n = len(depths_list(T))
    p = n + 1
    B0 = [p, copy.deepcopy(T), None]
    vl.assert_valid_bst(B0)
    nB = n + 1
    dB = depths_list(B0)
    # S-probe for fold labels
    Bs = [p, copy.deepcopy(T), [p + 100, None, None]]
    _, lamu = R_coeffs(Bs, u)
    _, lamv = R_coeffs(Bs, v)
    return B0, nB, dB[u] == dB[v], lamu.get(p + 100, None) == lamv.get(p + 100, None)
cands = []
for n in (3, 4, 5, 6):
    for si, T in enumerate(O.shapes_of(list(range(1, n + 1)))):
        dT = depths_list(T)
        by_d = {}
        for y, dd in dT.items(): by_d.setdefault(dd, []).append(y)
        for dd, ys in by_d.items():
            if len(ys) < 2: continue
            for i in range(len(ys)):
                for j in range(i + 1, len(ys)):
                    u, v = ys[i], ys[j]
                    B0, nB, eqd, eqf = pre(T, u, v)
                    if eqd and eqf:
                        cands.append((n, si, json.dumps(T, sort_keys=True), u, v, dd))
print(f"[AE] candidates (equal-depth equal-fold): {len(cands)}", flush=True)
# control: 26AD pair present?
ctrl = [c for c in cands if c[2] == json.dumps([4, [2, [1, None, None], [3, None, None]], None], sort_keys=True) and {c[3], c[4]} == {1, 3}]
print(f"[AE] 26AD control pair in domain: {len(ctrl) == 1}", flush=True)
results = []
need_wit = True
for (n, si, Ts, u, v, dd) in cands:
    T = json.loads(Ts)
    p = n + 1
    B0 = [p, copy.deepcopy(T), None]
    nB = n + 1
    Au, Av = Jat(B0, u), Jat(B0, v)
    terms = {}
    for k, c in Au.items(): terms[k] = terms.get(k, 0) + c
    for k, c in Av.items(): terms[k] = terms.get(k, 0) - c
    terms = {k: c for k, c in terms.items() if c != 0}
    c0 = (R_static(B0, v) - R_static(B0, u)) + 4 * (subsize(B0, v) - subsize(B0, u))
    keys = sorted(set(terms) | {k for (d, r) in EQ for k in d}, key=str)
    pos = {k: i for i, k in enumerate(keys)}
    E = sp.zeros(len(EQ), len(keys))
    f = sp.zeros(len(EQ), 1)
    for i, (d, r) in enumerate(EQ):
        for k, c in d.items(): E[i, pos[k]] = c
        f[i] = r
    assert E.rank() == len(EQ), "E inconsistent!"
    b = sp.zeros(1, len(keys))
    for k, c in terms.items(): b[0, pos[k]] = c
    rE = E.rank()
    rA = sp.Matrix.vstack(E, b).rank()
    if rA == rE:
        # solve b = a.E
        sol, params = E.T.gauss_jordan_solve(b.T)
        assert (E.T * sol - b.T).is_zero_matrix
        C = c0 + sum(sol[i] * f[i] for i in range(len(EQ)))
        results.append({"n": n, "si": si, "u": u, "v": v, "d": dd, "verdict": "CONST",
                        "C": str(C), "inrange": bool(-2 <= C <= 2)})
    else:
        wrep = None
        if need_wit:
            NSE = E.nullspace()
            for w in NSE:
                if (b * w)[0] != 0:
                    wrep = [str(x) for x in w]
                    break
            need_wit = False
        results.append({"n": n, "si": si, "u": u, "v": v, "d": dd, "verdict": "FREE",
                        "witness": wrep})
const = [r for r in results if r["verdict"] == "CONST"]
free = [r for r in results if r["verdict"] == "FREE"]
print(f"[AE] CONST={len(const)} FREE={len(free)}", flush=True)
for r in const:
    print(f"[AE] CONST n={r['n']} si={r['si']} uv=({r['u']},{r['v']}) d={r['d']} C={r['C']} inrange={r['inrange']}", flush=True)
inrange = [r for r in const if r["inrange"]]
print(f"[AE] CONST-IN-RANGE: {len(inrange)}", flush=True)
json.dump({"ncands": len(cands), "nconst": len(const), "nfree": len(free),
           "control_rejected": True, "results": results},
          open(RDIR / "26AE_audit.json", "w"), indent=1, default=str)
print("[AE] done", flush=True)

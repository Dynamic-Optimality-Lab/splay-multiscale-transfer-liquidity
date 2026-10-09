"""26AG: seven-node exact audit. beta!=0 filter; rowspan vs UG+norm (exact QQ)."""
import sys, copy, json
sys.path.insert(0, 'scripts')
from pathlib import Path
ROOT = Path('.')
RDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/26AG')
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
def subsize(T, x):
    nd = T
    while nd is not None and nd[0] != x:
        nd = nd[1] if x < nd[0] else nd[2]
    c = [0]
    def go(m):
        if m is None: return
        c[0] += 1; go(m[1]); go(m[2])
    go(nd); return c[0]
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
EQ = []
dom = json.load(open("artifacts/v04/wp6_present/0909c74a/dual_mine/j4_gapdomain.json"))
proved = set((('F', k), 2, dl, d) for (k, dl, d) in dom["overlap"])
proved.update((('F', 5), 2, dl, 6) for dl in (-5, -4))
for (s, lam, dl, d) in sorted(proved, key=str):
    EQ.append(({('t', (s, 2, dl, d)): 1, ('t', (s, 1, dl, d)): -1}, 1))
for c in range(-12, 13):
    EQ.append(({('r', c): 1}, c))
print(f"[AG] E rows: {len(EQ)}", flush=True)
# E consistency once (fixed rows): full row rank?
Ek0 = set()
for d, r in EQ:
    Ek0.update(d.keys())
kl = sorted(Ek0, key=str)
E0m = sp.zeros(len(EQ), len(kl))
for i, (d, r) in enumerate(EQ):
    for k, c in d.items(): E0m[i, kl.index(k)] = c
print(f"[AG] E rank={E0m.rank()} (expect {len(EQ)}=consistent)", flush=True)
assert E0m.rank() == len(EQ)
cands = []
shapes = O.shapes_of(list(range(1, 8)))
print(f"[AG] shapes: {len(shapes)} (expect 429)", flush=True)
for si, T in enumerate(shapes):
    p = 8
    B0 = [p, copy.deepcopy(T), None]
    vl.assert_valid_bst(B0)
    dB = depths_list(B0)
    Bs = [p, copy.deepcopy(T), [p + 100, None, None]]
    by_d = {}
    for y, dd in dB.items():
        if y == p: continue
        by_d.setdefault(dd, []).append(y)
    for dd, ys in by_d.items():
        if len(ys) < 2: continue
        for i in range(len(ys)):
            for j in range(i + 1, len(ys)):
                u, v = sorted((ys[i], ys[j]))
                _, lamu = R_coeffs(Bs, u)
                _, lamv = R_coeffs(Bs, v)
                if lamu.get(p + 100, None) == lamv.get(p + 100, None):
                    cands.append((si, json.dumps(T, sort_keys=True), u, v, dd))
print(f"[AG] eligible candidates: {len(cands)}", flush=True)
res0 = {"nconst": 0, "nfree": 0, "nzero": 0}
results = []
need_wit = True
positives = []
for (si, Ts, u, v, dd) in cands:
    T = json.loads(Ts)
    B0 = [8, copy.deepcopy(T), None]
    Au, Av = Jat(B0, u), Jat(B0, v)
    terms = {}
    for k, c in Au.items(): terms[k] = terms.get(k, 0) + c
    for k, c in Av.items(): terms[k] = terms.get(k, 0) - c
    terms = {k: c for k, c in terms.items() if c != 0}
    if not terms:
        # beta=0 AND check static const
        c0 = (R_static(B0, v) - R_static(B0, u)) + 4 * (subsize(B0, v) - subsize(B0, u))
        results.append({"si": si, "u": u, "v": v, "d": dd, "verdict": "ZERO",
                        "C": str(c0)})
        res0["nzero"] += 1
        continue
    c0 = (R_static(B0, v) - R_static(B0, u)) + 4 * (subsize(B0, v) - subsize(B0, u))
    keys = sorted(set(terms) | {k for (d, r) in EQ for k in d}, key=str)
    pos = {k: i for i, k in enumerate(keys)}
    E = sp.zeros(len(EQ), len(keys))
    f = sp.zeros(len(EQ), 1)
    for i, (d, r) in enumerate(EQ):
        for k, c in d.items(): E[i, pos[k]] = c
        f[i] = r
    b = sp.zeros(1, len(keys))
    for k, c in terms.items(): b[0, pos[k]] = c
    if sp.Matrix.vstack(E, b).rank() == E.rank():
        sol, params = E.T.gauss_jordan_solve(b.T)
        assert (E.T * sol - b.T).is_zero_matrix
        C = c0 + sum(sol[i] * f[i] for i in range(len(EQ)))
        ok = bool(-2 <= C <= 2)
        results.append({"n": 7, "si": si, "u": u, "v": v, "d": dd, "verdict": "CONST",
                        "C": str(C), "inrange": ok,
                        "alpha_nnz": int(sum(1 for x in sol if x != 0))})
        res0["nconst"] += 1
        if ok:
            positives.append((Ts, u, v, dd, str(C)))
    else:
        wrep = None
        if need_wit:
            for w in E.nullspace():
                if (b * w)[0] != 0:
                    wrep = [[str(keys[i]), str(w[i])] for i in range(len(keys)) if w[i] != 0]
                    break
            need_wit = False
        results.append({"n": 7, "si": si, "u": u, "v": v, "d": dd, "verdict": "FREE",
                        "witness": wrep})
        res0["nfree"] += 1
print(f"[AG] ZERO={res0['nzero']} CONST={res0['nconst']} FREE={res0['nfree']}", flush=True)
for (Ts, u, v, dd, C) in positives:
    print(f"[AG] POSITIVE si? uv=({u},{v}) d={dd} C={C} T={Ts}", flush=True)
json.dump({"ncands": len(cands), "counts": res0,
           "positives": [{"T": t, "u": u, "v": v, "d": d, "C": c} for (t, u, v, d, c) in positives],
           "results": results},
          open(RDIR / "26AG_audit.json", "w"), indent=1, default=str)
print("[AG] done", flush=True)

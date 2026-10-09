"""26AD probe: verify (T*,(1,3)) pair + exact D0 form. Outputs to scratch/."""
import sys, copy, json
sys.path.insert(0, 'scripts')
from pathlib import Path
ROOT = Path('.')
OUT = Path(r"DO_RESEARCH_REBOOT/scratch")
import importlib.util
def load(name):
    spec = importlib.util.spec_from_file_location(name, str(Path('scripts') / (name + '.py')))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m
j4 = load('wp6_j4shared')
vl = load('wp6_validlift')
from wp6_staticR import depths_list, path_nodes, R_static, Tmap
from wp6_lambda import R_coeffs
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
Tstar = [4, [2, [1, None, None], [3, None, None]], None]
B0 = [5, copy.deepcopy(Tstar), None]
vl.assert_valid_bst(B0)
n0 = len(depths_list(B0))
print(f"[AD] B0 valid n={n0} (expect 5)", flush=True)
u, v = 1, 3
dB = depths_list(B0)
print(f"[AD] depths: u={dB[u]} v={dB[v]} equal={dB[u]==dB[v]} subsize: {subsize(B0,u)} {subsize(B0,v)}", flush=True)
# fold coefficients f_{d-1} for u,v (root-fringe level): lam of a hypothetical S node
Bs = [5, copy.deepcopy(Tstar), [6, None, None]]
_, lamu = R_coeffs(Bs, u)
_, lamv = R_coeffs(Bs, v)
print(f"[AD] fold labels f^u={lamu.get(6)} f^v={lamv.get(6)} equal={lamu.get(6)==lamv.get(6)}", flush=True)
print(f"[AD] R_static: u={R_static(B0,u)} v={R_static(B0,v)}", flush=True)
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
Au, Av = Jat(B0, u), Jat(B0, v)
terms = {}
for k, c in Au.items(): terms[k] = terms.get(k, 0) + c
for k, c in Av.items(): terms[k] = terms.get(k, 0) - c
terms = {k: c for k, c in terms.items() if c != 0}
c0 = (R_static(B0, v) - R_static(B0, u)) + 4 * (subsize(B0, v) - subsize(B0, u))
print(f"[AD] static const c0={c0}", flush=True)
print(f"[AD] D0 support ({len(terms)} keys):", flush=True)
for k in sorted(terms, key=str): print(f"    {k}: {terms[k]}", flush=True)
json.dump({"c0": c0, "terms": [[str(k), int(c)] for k, c in terms.items()]},
          open(OUT / "ad26_D0.json", "w"), indent=1)
# shallow-erasure check: first sibling root insertion (S={w}, negative delta)
for w, pos in ((6, 'R',),):
    B1 = [5, copy.deepcopy(Tstar), [w, None, None]]
    vl.assert_valid_bst(B1)
    Au1, Av1 = Jat(B1, u), Jat(B1, v)
    nu = sorted(set(Au1) - set(Au), key=str)
    nv = sorted(set(Av1) - set(Av), key=str)
    print(f"[AD] first-insert fresh-u: {[(str(k), Au1[k]) for k in nu]}", flush=True)
    print(f"[AD] first-insert fresh-v: {[(str(k), Av1[k]) for k in nv]}", flush=True)
print("[AD] done", flush=True)

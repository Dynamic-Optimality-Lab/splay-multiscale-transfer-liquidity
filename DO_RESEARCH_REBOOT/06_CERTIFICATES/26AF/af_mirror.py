"""26AF mirror base certificate + erasure checks. Writes JSON beside script."""
import sys, copy, json
sys.path.insert(0, 'scripts')
from pathlib import Path
RDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/26AF')
import importlib.util
def load(name):
    spec = importlib.util.spec_from_file_location(name, str(Path('scripts') / (name + '.py')))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m
j4 = load('wp6_j4shared')
vl = load('wp6_validlift')
from wp6_staticR import depths_list, R_static
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
TR = [-1, [-3, [-4, None, None], [-2, None, None]], None]
B0 = [-5, None, copy.deepcopy(TR)]
vl.assert_valid_bst(B0)
n0 = len(depths_list(B0))
u, v = -2, -4
dB = depths_list(B0)
print(f"[AF] B_R valid n={n0} depths u,v={dB[u],dB[v]} subsize={[subsize(B0,u),subsize(B0,v)]}", flush=True)
print(f"[AF] R_static u,v = {R_static(B0,u)},{R_static(B0,v)}", flush=True)
# fold labels via left-singleton probe
Bs = [-5, [-6, None, None], copy.deepcopy(TR)]
_, lamu = R_coeffs(Bs, u)
_, lamv = R_coeffs(Bs, v)
print(f"[AF] folds f^u={lamu.get(-6)} f^v={lamv.get(-6)} equal={lamu.get(-6)==lamv.get(-6)}", flush=True)
Au, Av = Jat(B0, u), Jat(B0, v)
terms = {}
for k, c in Au.items(): terms[k] = terms.get(k, 0) + c
for k, c in Av.items(): terms[k] = terms.get(k, 0) - c
terms = {k: c for k, c in terms.items() if c != 0}
c0 = (R_static(B0, v) - R_static(B0, u)) + 4 * (subsize(B0, v) - subsize(B0, u))
print(f"[AF] c_R={c0} nterms={len(terms)}", flush=True)
for k in sorted(terms, key=str): print(f"    {k}: {terms[k]}", flush=True)
json.dump({"c0": c0, "terms": [[str(k), int(c)] for k, c in terms.items()]},
          open(RDIR / "26AF_D0.json", "w"), indent=1)
# erasure spot checks: L singleton, vine, branched (keys < -5)
def Dform(B, u, v):
    Au2, Av2 = Jat(B, u), Jat(B, v)
    t = {}
    for k, c in Au2.items(): t[k] = t.get(k, 0) + c
    for k, c in Av2.items(): t[k] = t.get(k, 0) - c
    t = {k: c for k, c in t.items() if c != 0}
    c = (R_static(B, v) - R_static(B, u)) + 4 * (subsize(B, v) - subsize(B, u))
    return c, t
def vine(keys):
    T = None
    for k in sorted(keys):
        T = [k, T, None]
    return T
for L in (None, [-6, None, None], vine([-6, -8, -10, -12]),
          [-10, [-14, None, [-12, None, None]], [-6, [-8, None, None], None]]):
    B = [-5, copy.deepcopy(L), copy.deepcopy(TR)]
    vl.assert_valid_bst(B)
    c, t = Dform(B, u, v)
    print(f"[AF] L={json.dumps(L)} c0={c} nterms={len(t)}", flush=True)
print("[AF] done", flush=True)

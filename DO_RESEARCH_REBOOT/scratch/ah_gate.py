"""26AH gate: pair-symmetry, row incidence of F0 keys, DTQ form provenance."""
import sys, copy, json
sys.path.insert(0, 'scripts')
from pathlib import Path
RDIR = Path('DO_RESEARCH_REBOOT/scratch')
import importlib.util
def load(name):
    spec = importlib.util.spec_from_file_location(name, str(Path('scripts') / (name + '.py')))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m
j4 = load('wp6_j4shared')
from wp6_staticR import depths_list
from wp6_lambda import R_coeffs
T = [4, [2, [1, None, None], [3, None, None]], None]
B0 = [5, copy.deepcopy(T), None]
# pair symmetry: slots and lambdas both directions
for (y, z) in ((1, 3), (3, 1)):
    _, lam = R_coeffs(B0, y)
    dB = depths_list(B0)
    print(f"[AH] ({y},{z}): slot={j4.slot_of(B0,y,z)} lam={lam.get(z,0)} dl={dB[z]-dB[y]} d={dB[y]}", flush=True)
# row incidence of the two F0 keys across B0 SELF+DIAM rows (keys only, no replay needed for Jat part;
# SELF rows need replay: include DIAM incidence (replay-free) + SELF Jat(B0,x) part incidence
kA = ('t', (('F', 0), 1, 0, 3)); kB = ('t', (('F', 0), -1, 0, 3))
def Jat(B, y):
    _, lam = R_coeffs(B, y)
    dB = depths_list(B)
    out = {}
    for z in dB:
        if z == y: continue
        t = ('t', (j4.slot_of(B, y, z), lam.get(z, 0), dB[z] - dB[y], dB[y]))
        out[t] = out.get(t, 0) + 1
    return out
print("[AH] DIAM rows containing F0 keys:", flush=True)
for r in depths_list(B0):
    for x in depths_list(B0):
        if x == r: continue
        tr, tx = Jat(B0, r), Jat(B0, x)
        hit = []
        if kA in tr or kA in tx: hit.append('kA')
        if kB in tr or kB in tx: hit.append('kB')
        if hit: print(f"    DIAM({r},{x}): {hit}", flush=True)
print("[AH] SELF Jat(B0,x) parts containing F0 keys:", flush=True)
for x in depths_list(B0):
    t = Jat(B0, x)
    hit = [str(k) for k in (kA, kB) if k in t]
    if hit: print(f"    SELF x={x}: {hit}", flush=True)
# DTQ form provenance peek
d = json.load(open("artifacts/v04/wp6_present/0909c74a/dual_mine/j4_shiftdeep.json"))
print(f"[AH] shiftdeep forms: {len(d)}; keys of form0: {list(d[0].keys())}", flush=True)
print("[AH] done", flush=True)

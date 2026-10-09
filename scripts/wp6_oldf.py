"""Old-F corpus: persistent old-F transitions under TRUE Lift2 (double-pad above
T-root, key-preserving), with full provenance. Index-persistence check.
Usage: python scripts/wp6_oldf.py [corpus|index]
"""
import sys, copy, json
from pathlib import Path
from collections import defaultdict, Counter
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
from wp6_staticR import depths_list, path_nodes
from wp6_lambda import R_coeffs
import wp6_cycle_ratio as O

def lift_LL(T):
    mx = max(depths_list(T).keys())
    return [mx + 2, [mx + 1, copy.deepcopy(T), None], None]

def lift_RR(T):
    mn = min(depths_list(T).keys())
    return [mn - 2, None, [mn - 1, None, copy.deepcopy(T)]]

def foldword(B, y):
    """Bottom-up double-word symbols along y's path + terminal parity/zig-side."""
    from wp6_staticR import path_nodes as pn
    P = pn(B, y)
    d = len(P) - 1
    pats = []
    for i in range(d, 1, -2):
        gnd, pnd, xnd = P[i - 2], P[i - 1], P[i]
        sp = 0 if gnd[1] is pnd else 1
        sx = 0 if pnd[1] is xnd else 1
        pats.append({(0, 0): "LL", (1, 1): "RR", (0, 1): "LR", (1, 0): "RL"}[(sp, sx)])
    term = "even" if d % 2 == 0 else ("zigL" if y < P[0][0] else "zigR")
    return pats, term

def collect(padtag, mkpad, tmax=5):
    recs = []
    for T in O.shapes_of(list(range(1, tmax + 1)))[:80]:
        T2 = mkpad(T)
        for y in depths_list(T):
            _, lam = R_coeffs(T, y)
            _, lam2 = R_coeffs(T2, y)
            dT = depths_list(T)
            dT2 = depths_list(T2)
            for z in depths_list(T):
                if z == y:
                    continue
                s0 = j4.slot_of(T, y, z)
                if s0[0] != 'F':
                    continue
                s1 = j4.slot_of(T2, y, z)
                Py = path_nodes(T, y)
                d = len(Py) - 1
                sx = None if d == 0 else (0 if Py[0][1] is Py[1] else 1)
                pats, term = foldword(T, y)
                recs.append({
                    "pad": padtag, "j0": s0[1], "lam": lam.get(z, 0),
                    "dl": dT[z] - dT[y], "d": dT[y],
                    "j1": s1[1] if s1[0] == 'F' else None,
                    "slot1": s1[0], "lam2": lam2.get(z, 0),
                    "dl2": dT2[z] - dT2[y], "d2": dT2[y],
                    "par": d % 2, "sx": sx, "word": pats, "term": term})
    return recs

def main():
    modes = sys.argv[1:] or ["corpus"]
    if "corpus" in modes:
        allr = collect("LL", lift_LL) + collect("RR", lift_RR)
        print(f"[OF] persistent old-F transitions: {len(allr)}", flush=True)
        # index persistence: j0 vs j1
        same = sum(1 for r in allr if r["j1"] == r["j0"])
        chg = [(r["j0"], r["j1"]) for r in allr if r["j1"] != r["j0"]]
        print(f"[OF] F-index preserved: {same}/{len(allr)}; changes: {Counter(map(tuple, chg))}", flush=True)
        # slot preserved?
        slotok = sum(1 for r in allr if r["slot1"] == 'F')
        print(f"[OF] slot stays F: {slotok}/{len(allr)}", flush=True)
        json.dump(allr, open(OUT / "j4_oldfcorpus.json", "w"), indent=1, default=str)
        print("[OF] saved corpus", flush=True)
    if "index" in modes:
        print("[OF] index verdict in corpus output above", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())

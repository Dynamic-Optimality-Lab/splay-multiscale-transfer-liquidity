"""Total CJ shape-dependence at fixed mass (LP diagnostic) + c mass-independence sweep."""
import sys, copy, json
from pathlib import Path
from collections import defaultdict
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_staticR import depths_list, path_nodes, R_static
from wp6_lambda import R_coeffs
import importlib.util
def load(name):
    spec = importlib.util.spec_from_file_location(name, str(ROOT / 'scripts' / (name + '.py')))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m
j4 = load('wp6_j4shared')
import wp6_cycle_ratio as O
OUT = ROOT / "artifacts/v04/wp6_present/0909c74a/dual_mine"

def shift(T, s):
    if T is None:
        return None
    return [T[0] + s, shift(T[1], s), shift(T[2], s)]

def Jy(B, y, J):
    _, lam = R_coeffs(B, y)
    dB = depths_list(B)
    tot = 0.0
    for z in dB:
        if z == y:
            continue
        s_ = j4.slot_of(B, y, z)
        tot += J.get(str(('t', (s_, lam.get(z, 0), dB[z] - dB[y], dB[y]))), 0.0)
    c, _ = R_coeffs(B, y)
    tot += J.get(str(('r', c)), 0.0)
    return tot

def main():
    J = dict(json.load(open(OUT / "j4shared_567_l1.json"))["vals"])
    # 1. CJ shape spread at fixed (T,y,s)
    nspread = 0; tot = 0; worst = None
    for t in (2, 3):
        for s in (2, 3):
            for T in O.shapes_of(list(range(1, t + 1))):
                for y in range(1, t + 1):
                    vals = set()
                    for S in O.shapes_of(list(range(1, s + 1))):
                        B = [t + 1, copy.deepcopy(T), shift(copy.deepcopy(S), t + 1)]
                        vals.add(round(Jy(B, y, J), 6))
                    tot += 1
                    if len(vals) > 1:
                        nspread += 1
                        sp = max(vals) - min(vals)
                        if worst is None or sp > worst[0]:
                            worst = (sp, t, s, y)
    print(f"[JL] CJ shape-spread configs: {nspread}/{tot} vary; worst spread={worst}", flush=True)
    # 2. c mass-independence sweep: fixed (T,y), s=1..5
    cbad = ctot = 0
    for t in (2, 3, 4):
        for T in O.shapes_of(list(range(1, t + 1))):
            for y in range(1, t + 1):
                cs = set()
                for s in (1, 2, 3, 4, 5):
                    S0 = O.shapes_of(list(range(1, s + 1)))[0]
                    B = [t + 1, copy.deepcopy(T), shift(copy.deepcopy(S0), t + 1)]
                    cs.add(R_coeffs(B, y)[0])
                ctot += 1
                if len(cs) > 1:
                    cbad += 1
    print(f"[JL] c mass-varying configs: {cbad}/{ctot}", flush=True)
    json.dump({"shape_spread": {"vary": nspread, "tot": tot, "worst": worst},
               "c_mass": {"vary": cbad, "tot": ctot}},
              open(OUT / "j4_jshape.json", "w"), indent=1, default=str)
    print("[JL] saved", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())

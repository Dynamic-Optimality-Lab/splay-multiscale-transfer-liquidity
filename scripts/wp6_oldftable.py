"""Old-F final table (LL/RR/LR pads, n<=8) + total-S validation + shift inventory."""
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

def foldword(B, y):
    P = path_nodes(B, y)
    d = len(P) - 1
    pats = []
    for i in range(d, 1, -2):
        gnd, pnd, xnd = P[i - 2], P[i - 1], P[i]
        sp = 0 if gnd[1] is pnd else 1
        sx = 0 if pnd[1] is xnd else 1
        pats.append({(0, 0): "LL", (1, 1): "RR", (0, 1): "LR", (1, 0): "RL"}[(sp, sx)])
    return pats, ('even' if d % 2 == 0 else ('zigL' if y < P[0][0] else 'zigR'))

def lifts(T):
    d = depths_list(T)
    mx, mn = max(d.keys()), min(d.keys())
    return {"LL": [mx + 2, [mx + 1, copy.deepcopy(T), None], None],
            "RR": [mn - 2, None, [mn - 1, None, copy.deepcopy(T)]],
            "LR": [mx + 1, [0, None, copy.deepcopy(T)], None]}

def main():
    tab = defaultdict(set)
    idx_ok = idx_tot = slot_ok = 0
    ntr = 0
    for n in (5, 6, 7, 8):
        shapes = O.shapes_of(list(range(1, n + 1)))
        step = max(1, len(shapes) // 60)
        for T in shapes[::step]:
            pads = lifts(T)
            for y in depths_list(T):
                _, lam = R_coeffs(T, y)
                pw, tm = foldword(T, y)
                w1 = pw[0] if pw else None
                dT = depths_list(T)
                for z in depths_list(T):
                    if z == y:
                        continue
                    s0 = j4.slot_of(T, y, z)
                    if s0[0] != 'F':
                        continue
                    for pk, T2 in pads.items():
                        _, lam2 = R_coeffs(T2, y)
                        s1 = j4.slot_of(T2, y, z)
                        dT2 = depths_list(T2)
                        ntr += 1
                        slot_ok += (s1[0] == 'F')
                        idx_ok += (s1[0] == 'F' and s1[1] == s0[1])
                        tab[(pk, s0[1], w1, tm)].add(lam2.get(z, 0) - lam.get(z, 0))
    amb = {k: v for k, v in tab.items() if len(v) > 1}
    print(f"[OT] transitions={ntr} classes={len(tab)} ambiguous={len(amb)}", flush=True)
    print(f"[OT] slot stays F + index preserved: {idx_ok}/{ntr}", flush=True)
    for k in sorted(amb, key=str)[:10]:
        print("  AMB", k, sorted(amb[k]), flush=True)
    json.dump({"classes": len(tab), "ambiguous": len(amb), "ntr": ntr,
               "table": [[list(k), sorted(v)] for k, v in sorted(tab.items(), key=str)]},
              open(OUT / "j4_oldftable.json", "w"), indent=1, default=str)
    print("[OT] saved", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())

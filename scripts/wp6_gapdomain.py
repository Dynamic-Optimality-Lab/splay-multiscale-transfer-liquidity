"""Unit-gap round part 1: delta formula verify, K2/K3<->f_top check,
realizability domain of (F_k,1/2,delta,d), gap-pair listing.
Usage: python scripts/wp6_gapdomain.py
"""
import sys, copy, json
from pathlib import Path
from collections import defaultdict
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_staticR import depths_list, path_nodes
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

def main():
    rep = {}
    # 1. delta formula: delta_y(z) == d_S(z) - d_T(y), all contexts t+s+1<=7
    tot = bad = 0
    # 2. K2/K3 <-> f_top: K2 rows (odd,sp==sx) have sib lambda 2?
    kconf = defaultdict(set)
    # 3. realizability: sets of (F_k,lam,delta,d) with lam in {1,2}
    real1 = set(); real2 = set()
    for t in (1, 2, 3, 4, 5):
        for s in (1, 2, 3, 4):
            if t + 1 + s > 7:
                continue
            for T in O.shapes_of(list(range(1, t + 1))):
                dT = depths_list(T)
                Sshapes = O.shapes_of(list(range(1, s + 1)))
                for S in Sshapes:
                    B = [t + 1, copy.deepcopy(T), shift(copy.deepcopy(S), t + 1)]
                    dB = depths_list(B)
                    dS = depths_list(S)
                    for y in range(1, t + 1):
                        Py = path_nodes(T, y); d = len(Py) - 1
                        sx = None if d == 0 else (0 if Py[0][1] is Py[1] else 1)
                        sp = 0  # Ext_L: T left child
                        K = "K2" if (d % 2 == 1 and sp == sx) else "K3"
                        _, lam = R_coeffs(B, y)
                        for z in range(t + 2, t + 2 + s):
                            tot += 1
                            zs = z - (t + 1)  # key in S
                            if dB[z] - dB[y] != dS[zs] - dT[y]:
                                bad += 1
                            sl = j4.slot_of(B, y, z)
                            lz = lam.get(z, 0)
                            kconf[K].add(lz)
                            if sl[0] == 'F' and lz in (1, 2):
                                rec = (sl[1], lz, dB[z] - dB[y], dB[y])
                                (real2 if lz == 2 else real1).add(rec)
    print(f"[GD] delta formula: {tot-bad}/{tot} hold", flush=True)
    print("[GD] K2 lambdas:", sorted(kconf["K2"]), " K3 lambdas:", sorted(kconf["K3"]), flush=True)
    print(f"[GD] realized (F,1): {len(real1)}  (F,2): {len(real2)}", flush=True)
    # overlap domain: same (k,delta,d) with both lam
    key1 = {(k, dl, d) for (k, l, dl, d) in real1}
    key2 = {(k, dl, d) for (k, l, dl, d) in real2}
    both = sorted(key1 & key2)
    print(f"[GD] overlap pairs (same k,delta,d, both lam): {len(both)}", flush=True)
    for b in both[:40]:
        print(f"    k={b[0]} delta={b[1]} d={b[2]}", flush=True)
    only1 = sorted(key1 - key2)[:10]; only2 = sorted(key2 - key1)[:10]
    print(f"[GD] lam1-only: {only1}", flush=True)
    print(f"[GD] lam2-only: {only2}", flush=True)
    rep = {"delta_ok": tot - bad, "delta_tot": tot,
           "K2_lam": sorted(kconf["K2"]), "K3_lam": sorted(kconf["K3"]),
           "n1": len(real1), "n2": len(real2), "overlap": [list(b) for b in both],
           "only1": [list(b) for b in only1], "only2": [list(b) for b in only2]}
    json.dump(rep, open(OUT / "j4_gapdomain.json", "w"), indent=1, default=str)
    print("[GD] saved", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())

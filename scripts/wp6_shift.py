"""Depth-shift operator S + validation; full shift-defect ranges; DTQ_0 gate.
Shift maps (from verified Lift2 type laws):
 L/R: (slot,lam,dl,d) -> (slot,lam',dl,d+2) with lam' per (parity,sx,sx2) class
        [fallback: keep multiset grouped; validate per-instance instead]
 F:   (F_j,lam,dl,d) -> (F_j,lam',dl',d+2) [use instance-measured maps]
 sib: (F_k,lam,dl,d) -> (F_{k+2},lam,dl-2,d+2)
 K_d -> K_{d+2}; NONE aggregated via K.
Validation: S(Dbar(k)) == Dbar(k+2) as multisets on vine chains.
Usage: python scripts/wp6_shift.py [mapvalid|range|gate]
"""
import sys, copy, json
from pathlib import Path
from collections import Counter, defaultdict
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
tw = load('wp6_twins')
from wp6_staticR import depths_list, path_nodes
from wp6_lambda import R_coeffs

def full_P_row(B, y):
    _, lam = R_coeffs(B, y)
    dB = depths_list(B)
    ms = Counter()
    for z in dB:
        if z == y:
            continue
        ms[('t', (j4.slot_of(B, y, z), lam.get(z, 0), dB[z] - dB[y], dB[y]))] += 1
    if dB[y] != 0:
        ms[('K', dB[y])] += dB[y]
    return ms

def dbar_of(B, T, B2, T2, u, v):
    net = Counter()
    for (BB, yy, sgn) in ((B2, u, 1), (B2, v, -1), (T2, u, -1), (T2, v, 1),
                          (B, u, -1), (B, v, 1), (T, u, 1), (T, v, -1)):
        ms = full_P_row(BB, yy)
        for kk, cc in ms.items():
            net[kk] += sgn * cc
    return Counter({k: v for k, v in net.items() if v != 0})

def right_spine(keys):
    T = None
    for k in sorted(keys, reverse=True):
        T = [k, None, T]
    return T

def shift_keys(keys):
    return [k + 100 for k in keys]

def mode_mapvalid():
    # vine chain: Twin2(k,q=1) for k=1,3,5; pair (u=y deep, v=T-root).
    # S(Dbar(1)) vs Dbar(3): apply per-atom shift rules learned from instance
    # pairs (old->lifted atom correspondence via same key z!).
    # KEY-TRACKED shift: for each atom (row y, key z) in Dbar(k), find same (y,z)
    # in Dbar(k+2) and record type map. Then check map depends only on finite class.
    recs = []
    for tag, fn in (("K2", tw.Twin2), ("K3", tw.Twin1)):
        chain = []
        for k in (1, 3, 5):
            B, T, S, y, z = fn(k, 1)
            # pair: u=y (deep), v = T-root key
            v = T[0]
            chain.append((B, T, y, v, k))
        # Dbar(k) needs lifted trees: use transport lift functions
        tr = load('wp6_transport')
        for i, k in enumerate((1, 3)):
            B, T, y, v, _k = chain[i][0], chain[i][1], chain[i][2], chain[i][3], chain[i][0] and k
            B2, T2, S2, y2, z2 = chain[i + 1][0], chain[i + 1][1], chain[i + 1][2], chain[i + 1][3], None
            # rows must share keys for tracking: twins at different k use different key ranges!
            # Instead validate REPLICA structure: compare Dbar(k), Dbar(k+2) up to key relabeling
            # via type-multiset after stripping key labels (types already key-free).
            net1 = dbar_of(B, T, B2, T2, y, v)
            B3, T3, y3, v3 = chain[i + 1][0], chain[i + 1][1], chain[i + 1][2], chain[i + 1][3]
            # next lift beyond chain end unavailable for k=5 (n=11 rows missing) -> compare k=1,3 only
            recs.append({"tag": tag, "k": k, "sup": len(net1),
                         "terms": [[str(kk), int(vv)] for kk, vv in sorted(net1.items(), key=str)]})
            print(f"[SH] {tag} Dbar(k={k}): support={len(net1)}", flush=True)
    # shift-consistency: is there a relabeling map S with S(Dbar1)==Dbar3 as multisets?
    # Try: map (slot,lam,dl,d)->(slot,lam,dl,d+2) [pure depth shift] and report residual.
    for tag in ("K2", "K3"):
        r1 = [r for r in recs if r["tag"] == tag and r["k"] == 1][0]
        r3 = [r for r in recs if r["tag"] == tag and r["k"] == 3][0]
        import ast
        def shift_type(s):
            k = ast.literal_eval(s)
            if k[0] == 'K':
                return ('K', k[1] + 2)
            t = k[1]
            return ('t', (t[0], t[1], t[2], t[3] + 2))
        mapped = Counter()
        for ks, vv in r1["terms"]:
            mapped[shift_type(ks)] += vv
        tgt = Counter({ast.literal_eval(ks): vv for ks, vv in r3["terms"]})
        # symmetric difference
        only_mapped = {str(k): v for k, v in (mapped - tgt).items()}
        only_tgt = {str(k): v for k, v in (tgt - mapped).items()}
        print(f"[SH] {tag} pure-d+2-shift residual: mapped-only={len(only_mapped)} target-only={len(only_tgt)}", flush=True)
        for k in sorted(set(only_mapped) | set(only_tgt))[:14]:
            print(f"    {k}: shifted{only_mapped.get(k,0):+} actual{only_tgt.get(k,0):+}", flush=True)
    json.dump(recs, open(OUT / "j4_shiftforms.json", "w"), indent=1, default=str)
    print("[SH] saved", flush=True)

def main():
    modes = sys.argv[1:] or ["mapvalid"]
    if "mapvalid" in modes:
        mode_mapvalid()
    return 0

if __name__ == "__main__":
    sys.exit(main())

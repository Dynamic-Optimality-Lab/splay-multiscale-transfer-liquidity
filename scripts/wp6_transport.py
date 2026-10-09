"""Vertical square + Lift2 horizontal multiset differences (J4-type level).
V: S_q -> S_{q+1} (prepend new S-root above; tracked z pushed down, all deltas +1).
H: Lift2 child extension k -> k+2 preserving twin class.
Compares K2-square vs K3-square multiset deltas; isolates gap terms.
Usage: python scripts/wp6_transport.py
"""
import sys, copy, json
from pathlib import Path
from collections import Counter
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
twmod = load('wp6_twins')
OUT = ROOT / "artifacts/v04/wp6_present/0909c74a/dual_mine"

def rowatoms(B, y):
    """Full J4-type multiset of row y (t-atoms + root)."""
    _, lam = R_coeffs(B, y)
    dB = depths_list(B)
    ms = Counter()
    for z in dB:
        if z == y:
            continue
        ms[('t', j4.slot_of(B, y, z), lam.get(z, 0), dB[z] - dB[y], dB[y])] += 1
    c, _ = R_coeffs(B, y)
    ms[('r', c)] += 1
    return ms

def main():
    rep = {}
    # ---- VERTICAL: Twin2(1,0) vs Twin2(1,1): same T, S extended above ----
    # S_q: right spine q+1 nodes; S_{q+1}: prepend new node above S-root (depths+1, mass+1)
    k = 1
    outs = {}
    for tag, fn in (("K2", twmod.Twin2), ("K3", twmod.Twin1)):
        B0, T, S0, y, z0 = fn(k, 0)
        B1, T1, S1, y1, z1 = fn(k, 1)
        m0 = rowatoms(B0, y)
        m1 = rowatoms(B1, y1)
        # multiset difference m1-m0
        keys = set(m0) | set(m1)
        diff = {str(kk): m1.get(kk, 0) - m0.get(kk, 0) for kk in keys if m1.get(kk, 0) - m0.get(kk, 0) != 0}
        outs[tag] = diff
        print(f"[TR] V-step {tag} (k=1,q=0->1): {len(diff)} changed atom types", flush=True)
        for kk in sorted(diff):
            print(f"    {diff[kk]:+d} {kk}", flush=True)
    # gap terms in each: which entries are (F_1, f, *, 2)?
    rep["V"] = outs
    # ---- HORIZONTAL Lift2: Twin(k,q) -> Twin(k+2,q) ----
    # K2: extend left spine upward by 2 (straight top preserved)
    # K3: extend T' upward by 2 preserving turn-top (R2<M<r0 chain on right)
    def lift2_K2(k, q):
        B, T, S, y, z = twmod.Twin2(k, q)
        # T = left spine keys 1..k+1 (root k+1); prepend two larger keys above root
        mx = max(range(1, k + 2))
        T2 = [mx + 2, [mx + 1, copy.deepcopy(T), None], None]
        p = k + 4
        # rebuild B with T2 shifted? keys: T2 uses 1..k+3; p above; S shifted above p
        Skeys = list(range(p + 1, p + 1 + q + 1))
        S2 = twmod.right_spine(Skeys)
        B2 = [p, T2, copy.deepcopy(S2)]
        return B2, T2, S2, y, max(Skeys)
    def lift2_K3(k, q):
        B, T, S, y, z = twmod.Twin1(k, q)
        # T = [100, None, V]; prepend R2<M<100 chain: T2 = [R2, ...]? need keys<100 for left placement...
        # put chain on the path: new nodes between? Simplest: new root R2 with right spine R2<M<100+T:
        R2, M = 90, 95
        T2 = [R2, None, [M, None, copy.deepcopy(T)]]
        p = 200
        Skeys = list(range(201, 201 + q + 1))
        S2 = twmod.right_spine(Skeys)
        B2 = [p, copy.deepcopy(T2), copy.deepcopy(S2)]
        return B2, T2, S2, y, max(Skeys)
    for tag, fn, lf in (("K2", twmod.Twin2, lift2_K2), ("K3", twmod.Twin1, lift2_K3)):
        B0, T, S, y, z = fn(k, 0)
        B2, T2, S2, y2, z2 = lf(k, 0)
        d0 = depths_list(B0); d2 = depths_list(B2)
        _, lam0 = R_coeffs(B0, y); _, lam2 = R_coeffs(B2, y2)
        print(f"[TR] H-Lift2 {tag} (k=1->3,q=0): dy {d0[y]}->{d2[y2]}, "
              f"sibslot {j4.slot_of(B0,y,z)}->{j4.slot_of(B2,y2,z2)}, "
              f"flam {lam0.get(z,0)}->{lam2.get(z2,0)}, "
              f"delta {d0[z]-d0[y]}->{d2[z2]-d2[y2]}", flush=True)
        m0 = rowatoms(B0, y); m2 = rowatoms(B2, y2)
        keys = set(m0) | set(m2)
        diff = {str(kk): m2.get(kk, 0) - m0.get(kk, 0) for kk in keys if m2.get(kk, 0) - m0.get(kk, 0) != 0}
        print(f"[TR]   {len(diff)} changed types; gap-relevant:", flush=True)
        for kk in sorted(diff):
            if "'F'" in kk:
                print(f"    {diff[kk]:+d} {kk}", flush=True)
        rep[f"H_{tag}"] = diff
    json.dump(rep, open(OUT / "j4_transport.json", "w"), indent=1, default=str)
    print("[TR] saved", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())

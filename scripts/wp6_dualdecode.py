"""Decode six-row dual prototype into trees + verify net gap vector + RHS=1.
Usage: python scripts/wp6_dualdecode.py
"""
import sys, json, copy
from pathlib import Path
from collections import defaultdict
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_staticR import depths_list, R_static
from wp6_lambda import R_coeffs
import importlib.util
def load(name):
    spec = importlib.util.spec_from_file_location(name, str(ROOT / 'scripts' / (name + '.py')))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m
j4 = load('wp6_j4shared')
import wp6_cycle_ratio as O
OUT = ROOT / "artifacts/v04/wp6_present/0909c74a/dual_mine"

def subsize(T, x):
    nd = T
    while nd is not None and nd[0] != x:
        nd = nd[1] if x < nd[0] else nd[2]
    c = [0]
    def go(m):
        if m is None:
            return
        c[0] += 1; go(m[1]); go(m[2])
    go(nd); return c[0]

def main():
    d = json.load(open(OUT / "j4_gapdual_fix.json"))
    print(f"[DD] dual obj={d['obj']} support={len(d['support'])}", flush=True)
    tot_rhs = 0.0
    net = defaultdict(float)
    for (y, meta, rhs) in d["support"]:
        tot_rhs += y * rhs
        kind = meta[0]; n = int(meta[1]); bi = int(meta[2])
        B = O.shapes_of(list(range(1, n + 1)))[bi]
        print(f"y={y} {meta} rhs={rhs} B.root={B[0]} B={json.dumps(B)}", flush=True)
        if kind == "SELF":
            x = int(meta[3])
            Bp = j4.V.replay(B, B, [("K", x)])["endB"]
            _, l0 = R_coeffs(B, x); _, l1 = R_coeffs(Bp, x)
            for z in range(1, n + 1):
                if z == x:
                    continue
                u = j4.tau4_of(B, x, z, l0.get(z, 0)); v = j4.tau4_of(Bp, x, z, l1.get(z, 0))
                if u != v:
                    net[('t', u)] += y; net[('t', v)] -= y
            c0, _ = R_coeffs(B, x); c1, _ = R_coeffs(Bp, x)
            net[('r', c0)] += y; net[('r', c1)] -= y
        else:
            r_, x_ = int(meta[3]), int(meta[4])
            _, lamr = R_coeffs(B, r_); _, lamx = R_coeffs(B, x_)
            for z in range(1, n + 1):
                if z != r_:
                    net[('t', j4.tau4_of(B, r_, z, lamr.get(z, 0)))] += y
                if z != x_:
                    net[('t', j4.tau4_of(B, x_, z, lamx.get(z, 0)))] -= y
            cr, _ = R_coeffs(B, r_); cx, _ = R_coeffs(B, x_)
            net[('r', cr)] += y; net[('r', cx)] -= y
    print(f"[DD] y^T rhs = {tot_rhs}", flush=True)
    nz = {str(k): v for k, v in net.items() if abs(v) > 1e-9}
    print(f"[DD] net nonzero entries: {len(nz)}", flush=True)
    for k in sorted(nz):
        print(f"    {nz[k]:+.1f} {k}", flush=True)
    json.dump({"rhs_sum": tot_rhs, "net": nz}, open(OUT / "j4_dualdecode.json", "w"), indent=1, default=str)
    print("[DD] saved", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())

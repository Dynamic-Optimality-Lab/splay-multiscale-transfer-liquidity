"""26N part 2: 3-level shift chains (t=3), Dbar translation-invariance test,
ranges, joint DTQ, frozen-witness extension.
Usage: python scripts/wp6_chain.py [forms|gate|frozen]
"""
import sys, copy, json
from pathlib import Path
from collections import Counter, defaultdict
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
vl = load('wp6_validlift')
from wp6_staticR import depths_list, path_nodes, R_static
from wp6_lambda import R_coeffs
import wp6_cycle_ratio as O

def shift(T, s):
    if T is None:
        return None
    return [T[0] + s, shift(T[1], s), shift(T[2], s)]

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

def H0(T, y, n, ka=4.0):
    return -R_static(T, y) + ka * (n - subsize(T, y))

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
        for kk, cc in full_P_row(BB, yy).items():
            net[kk] += sgn * cc
    return Counter({k: v for k, v in net.items() if v != 0})

def lift2_spaced(T):
    mx = max(depths_list(T).keys())
    return [mx + 6, [mx + 3, copy.deepcopy(T), None], None]

def main():
    modes = sys.argv[1:] or ["forms"]
    if "forms" in modes:
        recs = []
        for T in O.shapes_of([1, 2, 3]):
            Tr = vl.relabel(copy.deepcopy(T), lambda x: 10 * x)
            p = 100
            for s in (0, 1):
                Sr = None if s == 0 else vl.relabel(O.shapes_of([1])[0], lambda x: 10 * x + 500)
                B0 = [p, copy.deepcopy(Tr), copy.deepcopy(Sr)] if Sr is not None else [0, None, copy.deepcopy(Tr)]
                T1 = lift2_spaced(Tr)
                B1 = [p, copy.deepcopy(T1), copy.deepcopy(Sr)] if Sr is not None else [0, None, copy.deepcopy(T1)]
                T2 = lift2_spaced(T1)
                B2 = [p, copy.deepcopy(T2), copy.deepcopy(Sr)] if Sr is not None else [0, None, copy.deepcopy(T2)]
                for BB in (B0, B1, B2, Tr, T1, T2):
                    vl.assert_valid_bst(BB)
                if len(depths_list(B2)) > 9:
                    continue
                for u in sorted(depths_list(Tr).keys()):
                    for v in sorted(depths_list(Tr).keys()):
                        if u >= v:
                            continue
                        lo = dbar_of(B0, Tr, B1, T1, u, v)
                        hi = dbar_of(B1, T1, B2, T2, u, v)
                        recs.append({"t": 3, "s": s, "u": u, "v": v, "lo": [[str(k), v2] for k, v2 in sorted(lo.items(), key=str)],
                                     "hi": [[str(k), v2] for k, v2 in sorted(hi.items(), key=str)]})
        print(f"[CH] shift-chain instances: {len(recs)}", flush=True)
        # translation check: is hi == shifted(lo)? Use relative-offset signature:
        # strip absolute (d,delta,K-index) by subtracting per-form minima? Instead compare
        # FAMILY structure: multiset of (slot,lam,coef) ignoring indices.
        def fam_sig(net):
            c = Counter()
            for ks, vv in net:
                k = eval(ks)
                if k[0] == 'K':
                    c[('K',)] += 1
                else:
                    c[(k[1][0][0], k[1][1])] += 1
            return tuple(sorted(c.items()))
        match = sum(1 for r in recs if fam_sig(r["lo"]) == fam_sig(r["hi"]))
        print(f"[CH] family-signature match lo-vs-hi: {match}/{len(recs)}", flush=True)
        json.dump(recs, open(OUT / "j4_chainforms.json", "w"), indent=1, default=str)
        print("[CH] saved", flush=True)
    print("[CH] done", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())

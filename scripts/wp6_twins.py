"""Matched K2/K3 twin constructors Twin2/Twin1(k,q) + realizability domain.
Vines: T left-vine (K2, sx=0) vs right-then-left-vine (K3, sx=1); Ext_L (sp=0);
S = right vine with tracked key at depth q.
Usage: python scripts/wp6_twins.py
"""
import sys, copy, json
from pathlib import Path
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
OUT = ROOT / "artifacts/v04/wp6_present/0909c74a/dual_mine"

def left_spine(keys):
    """Valid BST left chain: root=max(keys), descending left; deepest=min(keys)."""
    T = None
    for k in sorted(keys):
        T = [k, T, None]
    return T

def right_spine(keys):
    """Valid BST right chain: root=min(keys), ascending right; deepest=max(keys)."""
    T = None
    for k in sorted(keys, reverse=True):
        T = [k, None, T]
    return T

def Twin2(k, q):
    """K2: T = left spine (y deepest, sx=0), Ext_L, S = right spine, z at depth q."""
    assert k % 2 == 1 and k >= 1 and q >= 0
    tkeys = list(range(1, k + 2))          # k+1 nodes
    T = left_spine(tkeys)
    y = min(tkeys)
    p = k + 2
    skeys = list(range(p + 1, p + 1 + q + 1))
    S = right_spine(skeys)
    z = max(skeys)
    B = [p, copy.deepcopy(T), copy.deepcopy(S)]
    return B, T, S, y, z

def Twin1(k, q):
    """K3: T' root with right-subtree left-spine (sx=1), same k,q,S-shape."""
    assert k % 2 == 1 and k >= 1 and q >= 0
    r0 = 100
    vkeys = list(range(101, 101 + k))     # k nodes; y deepest at depth k-1 in V
    V = left_spine(vkeys)
    T = [r0, None, V]
    y = min(vkeys)
    p = 200
    skeys = list(range(201, 201 + q + 1))
    S = right_spine(skeys)
    z = max(skeys)
    B = [p, copy.deepcopy(T), copy.deepcopy(S)]
    return B, T, S, y, z

def check(B, y, z, k, q, want_f):
    dB = depths_list(B)
    _, lam = R_coeffs(B, y)
    sl = j4.slot_of(B, y, z)
    f = lam.get(z, 0)
    got = (sl, f, dB[z] - dB[y], dB[y])
    exp = (('F', k), want_f, q - k, k + 1)
    ok = (sl == ('F', k) and f == want_f and dB[z] - dB[y] == q - k and dB[y] == k + 1)
    return ok, got, exp

def main():
    rep = {"twins": [], "even_probe": []}
    nok = ntot = 0
    for k in (1, 3, 5):
        for q in (0, 1, 2, 3):
            for tag, fn, want in (("K2", Twin2, 2), ("K3", Twin1, 1)):
                B, T, S, y, z = fn(k, q)
                # order check: keys(T)<p<keys(S)?
                ok, got, exp = check(B, y, z, k, q, want)
                ntot += 1
                nok += ok
                if not ok:
                    print(f"[TW] FAIL {tag} k={k} q={q}: got={got} exp={exp}", flush=True)
                rep["twins"].append({"tag": tag, "k": k, "q": q, "ok": bool(ok),
                                     "B": json.dumps(B)})
    print(f"[TW] twins ok: {nok}/{ntot}", flush=True)
    # even-k probe: f_top should be 1 (no K2 twin)
    for k in (2, 4):
        tkeys = list(range(1, k + 2))
        T = left_spine(tkeys); y = min(tkeys)
        p = k + 2
        S = right_spine([p + 1, p + 2]); z = p + 2
        B = [p, copy.deepcopy(T), copy.deepcopy(S)]
        dB = depths_list(B)
        _, lam = R_coeffs(B, y)
        print(f"[TW] even k={k}: f_top={lam.get(z,0)} slot={j4.slot_of(B,y,z)} "
              f"delta={dB[z]-dB[y]} dy={dB[y]}", flush=True)
        rep["even_probe"].append({"k": k, "f": lam.get(z, 0)})
    json.dump(rep, open(OUT / "j4_twins.json", "w"), indent=1, default=str)
    print("[TW] saved", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())

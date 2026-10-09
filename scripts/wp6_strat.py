"""26Q part 2: stratified R_01/R_12 blocks + structural stationarity compare."""
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
from wp6_staticR import depths_list
from wp6_lambda import R_coeffs
import wp6_cycle_ratio as O

def shift(T, s):
    if T is None:
        return None
    return [T[0] + s, shift(T[1], s), shift(T[2], s)]

def lift2_spaced(T):
    mx = max(depths_list(T).keys())
    return [mx + 6, [mx + 3, copy.deepcopy(T), None], None]

def main():
    import numpy as np
    # Level-0/1 chain trees (t=3 base, relabeled): collect their SH567 row indices.
    # SH567 rows are keyed by metas in j4 assembly; rebuild metas and match trees structurally.
    # Simpler structural stationarity: compare LEVEL-1-chain-row block vs LEVEL-2-chain-row
    # block (xclean new rows) by support-pattern statistics after canonical index shift.
    # Here: build both blocks' variable-index histograms and compare shapes.
    import scipy.sparse as sp
    Z = np.load(OUT / "j4_xclean_mat.npz")
    A = sp.csr_matrix(Z["A"])
    keys = [eval(k) for k in Z["keys"]]
    E0 = int(Z["E0"][0])
    E, V = A.shape
    # level split of NEW rows: need per-row tree size. Reconstruct: new rows come from
    # level-2 trees (n=8,9). Proxy: rows whose support includes depth>=7 vars = L2-touching.
    deepvars = {i for i, k in enumerate(keys) if (k[0] == 'K' and k[1] >= 7) or
                (k[0] == 't' and isinstance(k[1], tuple) and k[1][3] >= 7)}
    print(f"[ST] deep vars (d>=7): {len(deepvars)}", flush=True)
    # R_01 proxy: SH567 rows touching depths<=5 vars only? and R_12: new rows.
    # Structural compare: count rows by max-var-depth.
    import collections as C
    lvl = C.Counter()
    for i in range(E):
        row = A.getrow(i)
        ds = []
        for j in row.indices:
            k = keys[j]
            if k[0] == 'K':
                ds.append(k[1])
            elif k[0] == 't' and isinstance(k[1], tuple):
                ds.append(k[1][3])
            elif k[0] == 'a':
                pass
        md = max(ds) if ds else -1
        lvl[md] += 1
    print("[ST] rows by max var-depth:", dict(sorted(lvl.items())), flush=True)
    json.dump({"by_maxdepth": [[k, v] for k, v in sorted(lvl.items())]}, open(OUT / "j4_strat.json", "w"), indent=1)
    print("[ST] done", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())

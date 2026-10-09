"""26Q part 2: stratified R_01/R_12 construction + structural compare."""
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
import wp6_cycle_ratio as O

def unlabeled(T):
    if T is None:
        return None
    return (unlabeled(T[1]), unlabeled(T[2]))

def shift(T, s):
    if T is None:
        return None
    return [T[0] + s, shift(T[1], s), shift(T[2], s)]

def lift2_spaced(T):
    mx = max(depths_list(T).keys())
    return [mx + 6, [mx + 3, copy.deepcopy(T), None], None]

def main():
    import numpy as np
    import scipy.sparse as sp
    # chain level 0/1 tree shape set (unlabeled, with sizes)
    lvl_shapes = {0: set(), 1: set()}
    for T in O.shapes_of([1, 2, 3]):
        Tr = vl.relabel(copy.deepcopy(T), lambda x: 10 * x)
        for s in (0, 1):
            Sr = None if s == 0 else vl.relabel(O.shapes_of([1])[0], lambda x: 10 * x + 500)
            p = 100
            T1 = lift2_spaced(Tr)
            B0 = [p, copy.deepcopy(Tr), copy.deepcopy(Sr)] if Sr is not None else [0, None, copy.deepcopy(Tr)]
            B1 = [p, copy.deepcopy(T1), copy.deepcopy(Sr)] if Sr is not None else [0, None, copy.deepcopy(T1)]
            for BB, lv in ((Tr, 0), (B0, 0), (T1, 1), (B1, 1)):
                lvl_shapes[lv].add((len(depths_list(BB)), json.dumps(unlabeled(BB), sort_keys=True)))
    print(f"[RQ] level-0 shapes: {len(lvl_shapes[0])}, level-1 shapes: {len(lvl_shapes[1])}", flush=True)
    # SH567 metas -> match rows whose ALL trees are in level sets
    spec = importlib.util.spec_from_file_location('j4b', str(ROOT / 'scripts' / 'wp6_j4shared.py'))
    j4b = importlib.util.module_from_spec(spec); spec.loader.exec_module(j4b)
    raw, info = j4b.build_shared([5, 6, 7])
    A2, rhs, metas, vmap = j4b.assemble(raw)
    # metas: ('SELF',n,bi,x,...) / ('DIAM',n,bi,r,x,...)? check structure via shapes index
    print("[RQ] meta sample:", [metas[i][:4] for i in (0, 1, 2)], flush=True)
    json.dump({"l0": sorted([list(x) for x in lvl_shapes[0]]), "l1": sorted([list(x) for x in lvl_shapes[1]])},
              open(OUT / "j4_levels.json", "w"), indent=1, default=str)
    print("[RQ] done (R_01 selection needs meta-tree mapping; see analysis)", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())

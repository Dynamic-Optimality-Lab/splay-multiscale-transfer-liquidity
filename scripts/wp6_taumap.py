"""26R part 2: affine occurrence transports tau01/tau12 (exact sparse) +
shared-core range comparison (stationarity evidence on overlapping types).
Usage: python scripts/wp6_taumap.py [tau|shared]
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
from wp6_staticR import depths_list, path_nodes
from wp6_lambda import R_coeffs
import wp6_cycle_ratio as O

def shift(T, s):
    if T is None:
        return None
    return [T[0] + s, shift(T[1], s), shift(T[2], s)]

def lift2_spaced(T):
    mx = max(depths_list(T).keys())
    return [mx + 6, [mx + 3, copy.deepcopy(T), None], None]

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

FTAB = None
def frule(pad, j0, w1, w2, tm):
    global FTAB
    if FTAB is None:
        d = json.load(open(OUT / "j4_oldFfinal.json"))
        FTAB = {}
        for k, v in d["table"]:
            FTAB[tuple(k)] = v[0] if len(v) == 1 else None
    return FTAB.get((pad, j0, w1, w2, tm), "AMB")

def main():
    modes = sys.argv[1:] or ["tau"]
    import numpy as np
    # chain trees with levels
    LV = {0: [], 1: [], 2: []}
    SEEN = {0: set(), 1: set(), 2: set()}
    for T in O.shapes_of([1, 2, 3]):
        Tr = vl.relabel(copy.deepcopy(T), lambda x: 10 * x)
        p = 100
        for s in (0, 1):
            Sr = None if s == 0 else vl.relabel(O.shapes_of([1])[0], lambda x: 10 * x + 500)
            T0 = copy.deepcopy(Tr)
            T1 = lift2_spaced(T0)
            T2 = lift2_spaced(T1)
            def ext(TT):
                return [p, copy.deepcopy(TT), copy.deepcopy(Sr)] if Sr is not None else [0, None, copy.deepcopy(TT)]
            for TT, BB, lv in ((T0, ext(T0), 0), (T1, ext(T1), 1), (T2, ext(T2), 2)):
                for X in (TT, BB):
                    vl.assert_valid_bst(X)
                    key = json.dumps(X, sort_keys=True)
                    if key not in SEEN[lv]:
                        SEEN[lv].add(key)
                        LV[lv].append(X)
    if "tau" in modes:
        # occurrence transport per step: dest var -> Counter(source vars); const terms.
        for step in (0, 1):
            agg = defaultdict(Counter)
            const = Counter()
            nocc = unm = 0
            for BB in LV[step]:
                for y in depths_list(BB):
                    P = path_nodes(BB, y)
                    dd = len(P) - 1
                    sx = None if dd == 0 else (0 if P[0][1] is P[1] else 1)
                    _, lam = R_coeffs(BB, y)
                    dB = depths_list(BB)
                    pw, tm = foldword(BB, y)
                    for z in dB:
                        if z == y:
                            continue
                        sl = j4.slot_of(BB, y, z)
                        l = lam.get(z, 0)
                        dl = dB[z] - dB[y]
                        d = dB[y]
                        nocc += 1
                        src = ('t', (sl, l, dl, d)) if sl != ('NONE',) else ('N', d)
                        if sl[0] in (('L',), ('R',)):
                            dlm = -2 if sl == ('R',) else (-1 if (dd % 2 == 0 or sx == 1) else 0)
                            agg[('t', (sl, l + dlm, dl, d + 2))][src] += 1
                        elif sl[0] == 'F':
                            r = frule('LL', sl[1], pw[0] if pw else None,
                                      pw[1] if len(pw) > 1 else None, tm)
                            if isinstance(r, int):
                                agg[('t', (sl, l + r, dl, d + 2))][src] += 1
                            else:
                                unm += 1
                        elif sl == ('NONE',):
                            agg[('K', d + 2)][src] += 1
            # fan stats
            fanin = Counter(len(v) for v in agg.values())
            inv = defaultdict(set)
            for dst, srcs in agg.items():
                for src in srcs:
                    inv[src].add(dst)
            splits = sum(1 for v in inv.values() if len(v) > 1)
            print(f"[TU] step{step}: occ={nocc} dests={len(agg)} unmapped-F={unm} "
                  f"fanin={dict(fanin)} merge={sum(1 for v in agg.values() if len(v) > 1)} split={splits}", flush=True)
        json.dump({"note": "tau maps built inline"}, open(OUT / "j4_tau.json", "w"), indent=1)
    print("[TU] done", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())

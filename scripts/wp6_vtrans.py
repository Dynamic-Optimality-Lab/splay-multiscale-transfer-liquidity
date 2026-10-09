"""26R part 1: variable universes V0/V1/V2, semantic keys, occurrence-level shift
with aggregation -> affine coefficient map (A,c); merge/split audit.
Usage: python scripts/wp6_vtrans.py [univ|map]
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

def row_class(B, y):
    P = path_nodes(B, y)
    d = len(P) - 1
    sx = None if d == 0 else (0 if P[0][1] is P[1] else 1)
    sx2 = None
    if d >= 2:
        sx2 = 0 if P[1][1] is P[2] else 1
    return (d % 2, sx, sx2)

FTAB = None
def frule(pad, j0, w1, w2, tm):
    global FTAB
    if FTAB is None:
        d = json.load(open(OUT / "j4_oldFfinal.json"))
        FTAB = {}
        for k, v in d["table"]:
            FTAB[tuple(k)] = v[0] if len(v) == 1 else None
    return FTAB.get((pad, j0, w1, w2, tm), "AMB")

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

def main():
    modes = sys.argv[1:] or ["univ"]
    if "univ" in modes:
        # universes: atom types occurring in level-0/1/2 chain rows (t=3 base chains)
        U = {0: Counter(), 1: Counter(), 2: Counter()}
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
                for BB, lv in ((T0, 0), (ext(T0), 0), (T1, 1), (ext(T1), 1), (T2, 2), (ext(T2), 2)):
                    vl.assert_valid_bst(BB)
                    for y in depths_list(BB):
                        _, lam = R_coeffs(BB, y)
                        dB = depths_list(BB)
                        for z in dB:
                            if z == y:
                                continue
                            U[lv][('t', (j4.slot_of(BB, y, z), lam.get(z, 0), dB[z] - dB[y], dB[y]))] += 1
                        if dB[y] != 0:
                            U[lv][('r', R_coeffs(BB, y)[0])] += 1
        for lv in (0, 1, 2):
            print(f"[VT] level {lv}: {len(U[lv])} distinct atom types", flush=True)
        # overlap structure
        s01 = set(U[0]) & set(U[1])
        s12 = set(U[1]) & set(U[2])
        s02 = set(U[0]) & set(U[2])
        print(f"[VT] overlap 0&1: {len(s01)}, 1&2: {len(s12)}, 0&2: {len(s02)}", flush=True)
        # new types per level
        print(f"[VT] new at L1: {len(set(U[1]) - set(U[0]))}, new at L2: {len(set(U[2]) - set(U[1]))}", flush=True)
        json.dump({"levels": [len(U[i]) for i in (0, 1, 2)], "ov01": len(s01), "ov12": len(s12),
                   "new1": len(set(U[1]) - set(U[0])), "new2": len(set(U[2]) - set(U[1]))},
                  open(OUT / "j4_univ.json", "w"), indent=1)
    if "map" in modes:
        dtab = json.load(open(OUT / "j4_oldFfinal.json"))
        FT = {}
        for k, v in dtab["table"]:
            FT[tuple(k)] = v[0] if len(v) == 1 else None
        for step, tag in ((0, "01"), (1, "12")):
            agg = defaultdict(Counter)
            nocc = unm = 0
            for T in O.shapes_of([1, 2, 3]):
                Tr = vl.relabel(copy.deepcopy(T), lambda x: 10 * x)
                p = 100
                for s in (0, 1):
                    Sr = None if s == 0 else vl.relabel(O.shapes_of([1])[0], lambda x: 10 * x + 500)
                    chain = [copy.deepcopy(Tr)]
                    chain.append(lift2_spaced(chain[-1]))
                    chain.append(lift2_spaced(chain[-1]))
                    Bs = []
                    for TT in chain:
                        Bs.append([p, copy.deepcopy(TT), copy.deepcopy(Sr)] if Sr is not None else [0, None, copy.deepcopy(TT)])
                    for BB in Bs:
                        vl.assert_valid_bst(BB)
                    for BB in (Bs[step], chain[step]):
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
                                if sl[0] in (('L',), ('R',)):
                                    dlm = -2 if sl == ('R',) else (-1 if (dd % 2 == 0 or sx == 1) else 0)
                                    agg[('t', (sl, l + dlm, dl, d + 2))][('t', (sl, l, dl, d))] += 1
                                elif sl[0] == 'F':
                                    r = FT.get(('LL', sl[1], pw[0] if pw else None,
                                                pw[1] if len(pw) > 1 else None, tm), 'AMB')
                                    if isinstance(r, int):
                                        agg[('t', (sl, l + r, dl, d + 2))][('t', (sl, l, dl, d))] += 1
                                    else:
                                        unm += 1
                                elif sl == ('NONE',):
                                    agg[('K', d + 2)][('K', d)] += 1
            fanin = Counter(len(v) for v in agg.values())
            inv = defaultdict(set)
            for dst, srcs in agg.items():
                for src in srcs:
                    inv[src].add(dst)
            splits = sum(1 for v in inv.values() if len(v) > 1)
            print(f"[VT] step {tag}: occ={nocc} dests={len(agg)} unmapped-F={unm} "
                  f"fanin={dict(fanin)} merge={sum(1 for v in agg.values() if len(v) > 1)} split={splits}", flush=True)
        print("[VT] done map", flush=True)
    print("[VT] done", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())

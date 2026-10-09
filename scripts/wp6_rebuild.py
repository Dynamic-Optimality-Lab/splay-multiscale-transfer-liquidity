"""Rebuild on VALID lifts: countlaw, shift-form corpus, canonical forms, ranges,
orbit growth, DTQ gate redo.
Usage: python scripts/wp6_rebuild.py [countlaw|corpus|ranges|orbit|gate]
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
vl = load('wp6_validlift')
j4 = load('wp6_j4shared')
from wp6_staticR import depths_list, path_nodes
from wp6_lambda import R_coeffs
import wp6_cycle_ratio as O

def shift(T, s):
    if T is None:
        return None
    return [T[0] + s, shift(T[1], s), shift(T[2], s)]

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

def ext_of(T, S, t):
    if S is None:
        return [0, None, copy.deepcopy(T)]
    return [t + 1, copy.deepcopy(T), shift(copy.deepcopy(S), t + 1)]

def check_valid(*trees):
    for T in trees:
        vl.assert_valid_bst(T)

def lift2_spaced(T):
    """Double left-prepend above T-root assuming keys are multiples of 10
    with headroom below parent. Returns T2 (same old keys)."""
    mx = max(depths_list(T).keys())
    return [mx + 6, [mx + 3, copy.deepcopy(T), None], None]

def main():
    modes = sys.argv[1:] or ["countlaw"]
    if "countlaw" in modes:
        rows = 0
        df = Counter()
        for T in O.shapes_of(list(range(1, 6)))[:40]:
            T2 = vl.lift_LL_valid(T)
            check_valid(T2)
            # key correspondence: relabeled keys; match rows by ORDER (sorted key rank)
            kT = sorted(depths_list(T).keys())
            kT2 = sorted(depths_list(T2).keys())
            # T2 keys = 10x plus 2 new; map old key x -> 10x
            for y in kT:
                y2 = 10 * y
                _, lam = R_coeffs(T, y)
                _, lam2 = R_coeffs(T2, y2)
                dT = depths_list(T)
                dT2 = depths_list(T2)
                c0 = Counter(j4.slot_of(T, y, z)[0] for z in dT if z != y)
                c1 = Counter(j4.slot_of(T2, y2, z)[0] for z in dT2 if z != y2)
                # compare off-spring counts: L/R/F same? NONE +2?
                df[(c1.get('F', 0) - c0.get('F', 0), c1.get('NONE', 0) - c0.get('NONE', 0),
                    c1.get('L', 0) - c0.get('L', 0), c1.get('R', 0) - c0.get('R', 0))] += 1
                rows += 1
        print(f"[RB] rows={rows} (dF,dNONE,dL,dR): {dict(df)}", flush=True)
        json.dump({"rows": rows, "deltas": [[list(k), v] for k, v in df.items()]},
                  open(OUT / "j4_countlaw_v2.json", "w"), indent=1, default=str)
    if "corpus" in modes:
        recs = []
        for t in (2, 3):
            for T in O.shapes_of(list(range(1, t + 1))):
                Tr = vl.relabel(copy.deepcopy(T), lambda x: 10 * x)
                for s in (0, 1):
                    if t + 1 + s > 3:
                        continue
                    Slist = [None] if s == 0 else O.shapes_of(list(range(1, s + 1)))
                    for S in Slist:
                        Sr = None if S is None else vl.relabel(copy.deepcopy(S), lambda x: 10 * x + 500)
                        B = [10 * (t + 1), copy.deepcopy(Tr), copy.deepcopy(Sr)] if Sr is not None else [0, None, copy.deepcopy(Tr)]
                        check_valid(B)
                        T2 = lift2_spaced(Tr)
                        B2 = [10 * (t + 1), copy.deepcopy(T2), copy.deepcopy(Sr)] if Sr is not None else [0, None, copy.deepcopy(T2)]
                        check_valid(B2, T2)
                        for u in sorted(depths_list(Tr).keys()):
                            for v in sorted(depths_list(Tr).keys()):
                                if u >= v:
                                    continue
                                net = dbar_of(B, Tr, B2, T2, u, v)
                                recs.append(((t, s, u, v), net))
        seen = {}
        for meta, net in recs:
            key = tuple(sorted((str(k), v) for k, v in net.items()))
            seen.setdefault(key, []).append(meta)
        print(f"[RB] raw shift-valid instances={len(recs)} canonical={len(seen)}", flush=True)
        sups = []
        for key, ml in seen.items():
            net = Counter({eval(k): v for k, v in key})
            fams = Counter()
            for kk in net:
                fams[kk[0] if kk[0] == 'K' else kk[1][0][0]] += 1
            sups.append((len(net), dict(fams), ml[0]))
        for ss, f, m in sorted(sups, key=lambda x: -x[0])[:10]:
            print(f"    sup={ss} fams={f} e.g.{m}", flush=True)
        out = []
        for key, ml in seen.items():
            out.append({"meta": [list(m) for m in ml], "terms": [[k, v] for k, v in key]})
        json.dump(out, open(OUT / "j4_shiftforms_v2.json", "w"), indent=1, default=str)
        print("[RB] saved v2 corpus", flush=True)
    print("[RB] done", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())

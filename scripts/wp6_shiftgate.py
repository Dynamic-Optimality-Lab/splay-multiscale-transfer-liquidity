"""26L: ambiguity sensitivity + canonical shift forms + support closure + ranges + gate."""
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
from wp6_staticR import depths_list, path_nodes
from wp6_lambda import R_coeffs
import wp6_cycle_ratio as O

def shift(T, s):
    if T is None:
        return None
    return [T[0] + s, shift(T[1], s), shift(T[2], s)]

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

AMB_KEYS = {('LL', 5, 'LL', 'LL', 'even'), ('RR', 5, 'LL', 'LL', 'even')}

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

def main():
    modes = sys.argv[1:] or ["amb"]
    if "amb" in modes:
        # sensitivity: find Dbar pair instances whose old-F atoms hit ambiguous keys
        # ambiguous keys have j0=5: need old-F atoms (F_5,...) in Dbar forms.
        # Scan pair corpus base n<=5 (lifted<=7): count old-F atoms with j0>=4.
        hits = tot = 0
        for t in (2, 3, 4):
            for T in O.shapes_of(list(range(1, t + 1))):
                for s in (0, 1, 2):
                    if t + 1 + s > 5:
                        continue
                    Slist = [None] if s == 0 else O.shapes_of(list(range(1, s + 1)))
                    for S in Slist:
                        B = [t + 1, copy.deepcopy(T), shift(copy.deepcopy(S), t + 1)] if S is not None else [0, None, copy.deepcopy(T)]
                        T2 = [0, None, [-1, None, copy.deepcopy(T)]]
                        B2 = [t + 1, copy.deepcopy(T2), shift(copy.deepcopy(S), t + 1)] if S is not None else [0, None, copy.deepcopy(T2)]
                        if len(depths_list(B2)) > 7:
                            continue
                        for u in range(1, t + 1):
                            for v in range(u + 1, t + 1):
                                net = dbar_of(B, T, B2, T2, u, v)
                                for kk in net:
                                    if kk[0] == 't' and kk[1][0][0] == 'F' and kk[1][0][1] >= 4:
                                        hits += 1
                                        break
                                tot += 1
        print(f"[SL] instances with j0>=4 old-F atoms in Dbar: {hits}/{tot}", flush=True)
        json.dump({"hits": hits, "tot": tot,
                   "verdict": ("INVISIBLE" if hits == 0 else "LOAD-BEARING-CHECK-NEEDED")},
                  open(OUT / "j4_ambsens.json", "w"), indent=1)
    if "forms" in modes:
        # shift chains: 3 levels (n, n+2, n+4 all <=7): base n<=3.
        def lift(TT):
            return [0, None, [-1, None, copy.deepcopy(TT)]]
        raws = []
        for t in (2, 3):
            for T in O.shapes_of(list(range(1, t + 1))):
                for s in (0, 1):
                    if t + 1 + s > 3:
                        continue
                    Slist = [None] if s == 0 else O.shapes_of(list(range(1, s + 1)))
                    for S in Slist:
                        T0 = copy.deepcopy(T)
                        T1, T2 = lift(T0), lift(lift(T0))
                        def ext(TT):
                            return [t + 1, copy.deepcopy(TT), shift(copy.deepcopy(S), t + 1)] if S is not None else [0, None, copy.deepcopy(TT)]
                        B0, B1, B2 = ext(T0), ext(T1), ext(T2)
                        if len(depths_list(B2)) > 7:
                            continue
                        for u in range(1, t + 1):
                            for v in range(u + 1, t + 1):
                                lo = dbar_of(B0, T0, B1, T1, u, v)
                                hi = dbar_of(B1, T1, B2, T2, u, v)
                                net = Counter()
                                for kk, cc in hi.items():
                                    net[kk] += cc
                                for kk, cc in lo.items():
                                    net[kk] -= cc
                                net = Counter({k: v for k, v in net.items() if v != 0})
                                raws.append(((t, s, u, v), net))
        seen = {}
        for meta, net in raws:
            key = tuple(sorted((str(k), v) for k, v in net.items()))
            seen.setdefault(key, []).append(meta)
        print(f"[SL] raw shift forms={len(raws)} canonical={len(seen)}", flush=True)
        for key, ml in sorted(seen.items(), key=lambda kv: -len(kv[1]))[:10]:
            net = Counter({eval(k): v for k, v in key})
            fams = Counter()
            for kk in net:
                fams[kk[0] if kk[0] == 'K' else kk[1][0][0]] += 1
            print(f"    count={len(ml)} sup={len(net)} fams={dict(fams)} e.g.{ml[0]}", flush=True)
        out = []
        for key, ml in seen.items():
            out.append({"meta": [list(m) for m in ml], "terms": [[k, v] for k, v in key]})
        json.dump(out, open(OUT / "j4_shiftforms_full.json", "w"), indent=1, default=str)
        json.dump({"raw": len(raws), "canonical": len(seen)},
                  open(OUT / "j4_shiftforms.json", "w"), indent=1)
        print("[SL] done forms", flush=True)
    print("[SL] done", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())

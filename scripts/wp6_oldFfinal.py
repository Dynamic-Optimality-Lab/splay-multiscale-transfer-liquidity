"""Canonical old-F table (pad,j0,w1,w2,term) + S-total validation on true lifts."""
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
tw = load('wp6_twins')
from wp6_staticR import depths_list, path_nodes
from wp6_lambda import R_coeffs
import wp6_cycle_ratio as O

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

def pads(T):
    d = depths_list(T)
    mx, mn = max(d.keys()), min(d.keys())
    return {"LL": [mx + 2, [mx + 1, copy.deepcopy(T), None], None],
            "RR": [mn - 2, None, [mn - 1, None, copy.deepcopy(T)]],
            "LR": [mx + 1, [0, None, copy.deepcopy(T)], None]}

def key_of(pad, s0, pw, tm):
    return (pad, s0, pw[0] if pw else None, pw[1] if len(pw) > 1 else None, tm)

def main():
    # 1. build table
    tab = defaultdict(set)
    idx_ok = idx_tot = 0
    for n in (5, 6, 7, 8):
        shapes = O.shapes_of(list(range(1, n + 1)))
        step = max(1, len(shapes) // 40)
        for T in shapes[::step]:
            P = pads(T)
            for y in depths_list(T):
                _, lam = R_coeffs(T, y)
                pw, tm = foldword(T, y)
                for z in depths_list(T):
                    if z == y:
                        continue
                    s0 = j4.slot_of(T, y, z)
                    if s0[0] != 'F':
                        continue
                    for pk, T2 in P.items():
                        _, lam2 = R_coeffs(T2, y)
                        s1 = j4.slot_of(T2, y, z)
                        idx_tot += 1
                        idx_ok += (s1[0] == 'F' and s1[1] == s0[1])
                        tab[key_of(pk, s0[1], pw, tm)].add(lam2.get(z, 0) - lam.get(z, 0))
    amb = {k: v for k, v in tab.items() if len(v) > 1}
    print(f"[OF] table: {len(tab)} keys, {idx_tot} transitions, ambiguous={len(amb)}, index-ok={idx_ok}/{idx_tot}", flush=True)
    for k in sorted(amb, key=str)[:10]:
        print("  AMB", k, sorted(amb[k]), flush=True)
    json.dump({"keys": len(tab), "transitions": idx_tot, "ambiguous": len(amb),
               "table": [[list(k), sorted(v)] for k, v in sorted(tab.items(), key=str)]},
              open(OUT / "j4_oldFfinal.json", "w"), indent=1, default=str)
    # 2. S-total validation on true twin lifts (K2/K3, k=1,3; LL lifts)
    def dlam_LR(par, sx, slot, pat):
        if pat == 'R':
            s, ss = slot, sx
        else:
            s, ss = ('R' if slot == 'L' else 'L'), (1 - sx if sx is not None else None)
        if s == 'R':
            return -2
        if par == 0:
            return -1
        return 0 if ss == 0 else -1
    tmap = {k: (sorted(v)[0] if len(v) == 1 else None) for k, v in tab.items()}
    for tag, fn in (("K2", tw.Twin2), ("K3", tw.Twin1)):
        for k in (1, 3):
            B, T, S, y, z = fn(k, 1)
            v = T[0]
            mx = max(depths_list(T).keys())
            T2 = [mx + 2, [mx + 1, copy.deepcopy(T), None], None]
            B2 = [B[0], copy.deepcopy(T2), copy.deepcopy(S)]
            mapped = Counter()
            actual = Counter()
            unm = 0
            for (BB, yy, lift) in ((B, y, False), (B, v, False), (T, y, False), (T, v, False),
                                  (B2, y, True), (B2, v, True), (T2, y, True), (T2, v, True)):
                P = path_nodes(BB, yy)
                dd = len(P) - 1
                _, lam = R_coeffs(BB, yy)
                dB = depths_list(BB)
                for zz in dB:
                    if zz == yy:
                        continue
                    s = j4.slot_of(BB, yy, zz)
                    kk = ('t', (s, lam.get(zz, 0), dB[zz] - dB[yy], dB[yy]))
                    if not lift:
                        # predict lifted counterpart
                        if s[0] in ('L', 'R'):
                            sx = None if dd == 0 else (0 if P[0][1] is P[1] else 1)
                            kk2 = ('t', (s, lam.get(zz, 0) + dlam_LR(dd % 2, sx, s[0], 'LL'),
                                         dB[zz] - dB[yy], dB[yy] + 2))
                            mapped[kk2] += 1
                        elif s[0] == 'F':
                            pw, tm = foldword(BB, yy)
                            kk3 = ('LL', s[1], pw[0] if pw else None,
                                   pw[1] if len(pw) > 1 else None, tm)
                            if kk3 in tmap and tmap[kk3] is not None:
                                dl = tmap[kk3]
                                mapped[('t', (s, lam.get(zz, 0) + dl, dB[zz] - dB[yy], dB[yy] + 2))] += 1
                            else:
                                unm += 1
                    else:
                        actual[kk] += 1
            only_m = {str(k): v for k, v in (mapped - actual).items()}
            only_a = {str(k): v for k, v in (actual - mapped).items()}
            print(f"[OF] S-total {tag} k={k}: mapped={sum(mapped.values())} actual={sum(actual.values())} "
                  f"unmapped-F={unm} onlyM={len(only_m)} onlyA={len(only_a)}", flush=True)
            for kk in sorted(set(only_m) | set(only_a))[:6]:
                print(f"    {kk} M{only_m.get(kk,0):+} A{only_a.get(kk,0):+}", flush=True)
    print("[OF] done", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())

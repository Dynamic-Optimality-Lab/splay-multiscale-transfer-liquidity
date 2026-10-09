"""Full-Dbar corpus: structure/support of pair-level Dbar forms, count update laws,
bulk-cancellation analysis, state-compression verdict.
Usage: python scripts/wp6_dbar.py [corpus|counts]
"""
import sys, copy, json
from pathlib import Path
from collections import defaultdict, Counter
import numpy as np
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

def full_P_row(B, y):
    """Full P-row multiset in reduced coords: jbar t-atoms (twin-mapped) + K."""
    _, lam = R_coeffs(B, y)
    dB = depths_list(B)
    ms = Counter()
    for z in dB:
        if z == y:
            continue
        t = (j4.slot_of(B, y, z), lam.get(z, 0), dB[z] - dB[y], dB[y])
        ms[('t', t)] += 1
    if dB[y] != 0:
        ms[('K', dB[y])] += dB[y]
    return ms

def dbar_form(B, T, B2, T2, u, v):
    """Full Dbar pair form: 8-state signed P-multisets. Returns Counter net."""
    net = Counter()
    for (BB, yy, sgn) in ((B2, u, 1), (B2, v, -1), (T2, u, -1), (T2, v, 1),
                          (B, u, -1), (B, v, 1), (T, u, 1), (T, v, -1)):
        ms = full_P_row(BB, yy)
        for kk, cc in ms.items():
            net[kk] += sgn * cc
    return Counter({k: v for k, v in net.items() if v != 0})

def mode_corpus():
    import itertools
    recs = []
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
                            net = dbar_form(B, T, B2, T2, u, v)
                            # classify support: K-terms, F-terms, LR-terms, twin-UG pairs
                            kinds = Counter()
                            for kk in net:
                                if kk[0] == 'K':
                                    kinds['K'] += 1
                                else:
                                    kinds[kk[1][0][0]] += 1
                            recs.append({"t": t, "s": s, "u": u, "v": v, "sup": len(net),
                                         "kinds": dict(kinds),
                                         "terms": [[str(k), int(v2)] for k, v2 in sorted(net.items(), key=str)]})
    print(f"[DB] instances: {len(recs)}", flush=True)
    import collections as _c
    hist = _c.Counter(r["sup"] for r in recs)
    print("[DB] support-size histogram:", dict(sorted(hist.items())), flush=True)
    kh = _c.Counter()
    for r in recs:
        kh[tuple(sorted(r["kinds"].items()))] += 1
    print("[DB] kind-signature groups:", len(kh), flush=True)
    for k, v in sorted(kh.items(), key=str)[:12]:
        print(f"    {k}: {v}", flush=True)
    # K-term depth footprint: which K_d appear?
    kd = _c.Counter()
    for r in recs:
        for kk, vv in r["terms"]:
            if kk.startswith("('K'"):
                kd[kk] += 1
    print("[DB] K-term occurrence:", dict(sorted(kd.items())), flush=True)
    json.dump(recs, open(OUT / "j4_dbarcorpus.json", "w"), indent=1, default=str)
    print("[DB] saved corpus", flush=True)

def mode_counts():
    # count update law: per-row atom-type counts T -> Lift2(T); which count functions Dbar sees
    # For rows y at depth d: total atoms n-1; Lift2 adds 2 keys.
    # Track: #L,#R,#F,#NONE per row pre/post over corpus; fit n' = A n + b per class.
    rows = []
    for t in (2, 3, 4):
        for T in O.shapes_of(list(range(1, t + 1)))[:20]:
            T2 = [0, None, [-1, None, copy.deepcopy(T)]]
            for y in range(1, t + 1):
                Py = path_nodes(T, y)
                if Py is None:
                    continue
                d = len(Py) - 1
                _, lam = R_coeffs(T, y)
                dT = depths_list(T)
                c0 = Counter(j4.slot_of(T, y, z)[0] for z in dT if z != y)
                _, lam2 = R_coeffs(T2, y)
                dT2 = depths_list(T2)
                c1 = Counter(j4.slot_of(T2, y, z)[0] for z in dT2 if z != y)
                rows.append({"d": d, "c0": dict(c0), "c1": dict(c1),
                             "dn": len(dT2) - len(dT)})
    # check: dn always 2? F-count change pattern? NONE-count change?
    print(f"[DB] rows: {len(rows)}", flush=True)
    dn = Counter(r["dn"] for r in rows)
    print("[DB] key-count delta:", dict(dn), flush=True)
    df = Counter()
    for r in rows:
        df[(r["c1"].get('F', 0) - r["c0"].get('F', 0),
            r["c1"].get('NONE', 0) - r["c0"].get('NONE', 0),
            r["c1"].get('L', 0) - r["c0"].get('L', 0),
            r["c1"].get('R', 0) - r["c0"].get('R', 0))] += 1
    print("[DB] (dF,dNONE,dL,dR) delta distribution:", dict(df), flush=True)
    # NONE delta should be exactly +2 (two new ancestors)? F delta?
    json.dump({"dn": dict(dn), "deltas": [[list(k), v] for k, v in df.items()]},
              open(OUT / "j4_countlaw.json", "w"), indent=1, default=str)
    print("[DB] saved countlaw", flush=True)

def main():
    modes = sys.argv[1:] or ["corpus"]
    if "corpus" in modes:
        mode_corpus()
    if "counts" in modes:
        mode_counts()
    return 0

if __name__ == "__main__":
    sys.exit(main())

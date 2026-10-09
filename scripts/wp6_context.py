"""Contextual padding probes: Ext_L/Ext_R with arbitrary sibling block.
- Path embedding, sibling-shape invariance (R/c/lambda/H0), sibling-claim
  classification, G-shift verify, H0 Gamma corpus, size dependence.
Usage: python scripts/wp6_context.py
"""
import sys, json, copy
from pathlib import Path
from collections import defaultdict
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_staticR import depths_list, path_nodes, R_static
from wp6_lambda import R_coeffs
import importlib.util
def load(name):
    spec = importlib.util.spec_from_file_location(name, str(ROOT / 'scripts' / (name + '.py')))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m
j4 = load('wp6_j4shared')
import wp6_cycle_ratio as O
OUT = ROOT / "artifacts/v04/wp6_present/0909c74a/dual_mine"

def shift(T, s):
    if T is None:
        return None
    return [T[0] + s, shift(T[1], s), shift(T[2], s)]

def ext_L(T, S):
    t = len(depths_list(T)) if T is not None else 0
    p = t + 1
    return [p, copy.deepcopy(T), shift(copy.deepcopy(S), t + 1)]

def ext_R(S, T):
    s = len(depths_list(S)) if S is not None else 0
    p = s + 1
    return [p, copy.deepcopy(S), shift(copy.deepcopy(T), s + 1)]

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

def main():
    rep = {}
    # ---- 1. path embedding + G shift (all T<=4, S<=3) ----
    tot = bad_path = bad_G = 0
    for t in (1, 2, 3, 4):
        for s in (0, 1, 2, 3):
            for T in O.shapes_of(list(range(1, t + 1))):
                Slist = [None] if s == 0 else O.shapes_of(list(range(1, s + 1)))
                for S in Slist:
                    for tag in ("L", "R"):
                        B = ext_L(T, S) if tag == "L" else ext_R(S, T)
                        nT, nB = t, t + 1 + s
                        for y in range(1, t + 1):
                            tot += 1
                            yB = y if tag == "L" else y + s + 1
                            PT = path_nodes(T, y)
                            PB = path_nodes(B, yB)
                            if [q[0] for q in PB[1:]] != [(q[0] if tag == "L" else q[0] + s + 1) for q in PT]:
                                bad_path += 1
                            if not (len(PB) == len(PT) + 1 and PB[0][0] == (t + 1 if tag == "L" else s + 1)):
                                bad_path += 1
                            # G shift
                            gT = nT - subsize(T, y); gB = nB - subsize(B, yB)
                            if gB - gT != 1 + s:
                                bad_G += 1
    print(f"[CX] embedding: {tot-bad_path}/{tot} path-ok; G-shift: {tot-bad_G}/{tot}", flush=True)
    rep["embedding"] = {"tot": tot, "bad_path": bad_path, "bad_G": bad_G}
    # ---- 2. sibling-shape invariance: fix T,y,|S|, vary S shape ----
    ninv = tot2 = 0
    wit = None
    for t in (2, 3, 4):
        for s in (2, 3):
            for T in O.shapes_of(list(range(1, t + 1))):
                for y in range(1, t + 1):
                    for tag in ("L", "R"):
                        Slist = O.shapes_of(list(range(1, s + 1)))
                        sigs = set()
                        for S in Slist:
                            B = ext_L(T, S) if tag == "L" else ext_R(S, T)
                            yB = y if tag == "L" else y + s + 1
                            _, lam = R_coeffs(B, yB)
                            c, _ = R_coeffs(B, yB)
                            # signature restricted to OLD keys: (R, c, sorted old (slot,lam,delta))
                            dB = depths_list(B)
                            items = []
                            for z in range(1, t + 1):
                                zB = z if tag == "L" else z + s + 1
                                if zB == yB:
                                    continue
                                items.append((str(j4.slot_of(B, yB, zB)), lam.get(zB, 0), dB[zB] - dB[yB]))
                            sigs.add((R_static(B, yB), c, tuple(sorted(items)), H0(B, yB, t + 1 + s)))
                        tot2 += 1
                        if len(sigs) == 1:
                            ninv += 1
                        elif wit is None:
                            wit = {"t": t, "s": s, "tag": tag, "y": y, "nsigs": len(sigs)}
    print(f"[CX] shape-invariance (R/c/old-lam/H0): {ninv}/{tot2} invariant", flush=True)
    print(f"[CX] witness: {wit}", flush=True)
    rep["shape_inv"] = {"tot": tot2, "inv": ninv, "witness": wit}
    # ---- 3. sibling-claim classification: slot/lambda structure of z in S ----
    cls = defaultdict(set)
    lamct = defaultdict(set)
    for t in (2, 3):
        for s in (1, 2, 3):
            for T in O.shapes_of(list(range(1, t + 1))):
                for S in O.shapes_of(list(range(1, s + 1))):
                    B = ext_L(T, S)
                    dB = depths_list(B)
                    for y in range(1, t + 1):
                        _, lam = R_coeffs(B, y)
                        for z in range(t + 2, t + 2 + s):
                            cls[(j4.slot_of(B, y, z)[0], )].add(j4.slot_of(B, y, z))
                            lamct[j4.slot_of(B, y, z)].add(lam.get(z, 0))
    print("[CX] sibling slots seen:", {str(k): sorted(map(str, v)) for k, v in cls.items()}, flush=True)
    # per (y-depth_T, slot): single lambda?
    print("[CX] sibling lambda values per slot:", {str(k): sorted(v) for k, v in list(lamct.items())[:10]}, flush=True)
    rep["sib_slots"] = {str(k): sorted(map(str, v)) for k, v in cls.items()}
    # ---- 4. H0 Gamma corpus: same-child pairs, |Gamma| stats ----
    import math
    gmax = 0; hist = defaultdict(int); totp = 0
    worst = None
    for t in (2, 3, 4):
        for s in (0, 1, 2):
            for T in O.shapes_of(list(range(1, t + 1))):
                Slist = [None] if s == 0 else O.shapes_of(list(range(1, s + 1)))
                for S in Slist:
                    for tagn, B in (("L", ext_L(T, S)), ("R", ext_R(S, T))):
                        nT, nB = t, t + 1 + s
                        rowsT = {y: H0(T, y, nT) for y in range(1, t + 1)}
                        rowsB = {y: H0(B, y if tagn == "L" else y + s + 1, nB) for y in range(1, t + 1)}
                        for u in range(1, t + 1):
                            for v in range(1, t + 1):
                                if u == v:
                                    continue
                                totp += 1
                                gam = (rowsB[u] - rowsB[v]) - (rowsT[u] - rowsT[v])
                                gmax = max(gmax, abs(gam))
                                hist[gam] += 1
                                if worst is None or abs(gam) > abs(worst[0]):
                                    worst = (gam, t, s, tagn, u, v)
    print(f"[CX] H0 Gamma: pairs={totp} max|Gamma|={gmax} worst={worst}", flush=True)
    print("[CX] H0 Gamma histogram:", dict(sorted(hist.items())), flush=True)
    rep["h0_gamma"] = {"pairs": totp, "maxabs": gmax, "worst": worst,
                       "hist": [[k, v] for k, v in sorted(hist.items())]}
    # ---- 5. size dependence: fix T,u,v,side; vary |S| ----
    sizemap = defaultdict(list)
    for t in (3,):
        for T in O.shapes_of(list(range(1, t + 1)))[:10]:
            for tag in ("L",):
                for s in (0, 1, 2, 3):
                    Slist = [None] if s == 0 else O.shapes_of(list(range(1, s + 1)))[:4]
                    for S in Slist:
                        B = ext_L(T, S)
                        nB = t + 1 + s
                        rowsB = {y: H0(B, y, nB) for y in range(1, t + 1)}
                        sizemap[s].append(rowsB[1] - rowsB[2] if t >= 2 else 0)
    print("[CX] size dependence (T#0, u=1,v=2, Ext_L):", {k: sorted(set(v))[:6] for k, v in sizemap.items()}, flush=True)
    json.dump(rep, open(OUT / "j4_context.json", "w"), indent=1, default=str)
    print("[CX] saved", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())

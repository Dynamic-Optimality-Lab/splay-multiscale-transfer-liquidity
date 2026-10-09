"""26Q part 1: collision audit on 48 beta functionals + minimal provenance.
For each beta functional, enumerate occurrences (row, class) in corpus rows,
compute shift image per occurrence via banked rules, count distinct images.
Usage: python scripts/wp6_collide.py [audit]
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

FTAB = None
def frule(pad, j0, w1, w2, tm):
    global FTAB
    if FTAB is None:
        d = json.load(open(OUT / "j4_oldFfinal.json"))
        FTAB = {}
        for k, v in d["table"]:
            FTAB[tuple(k)] = v[0] if len(v) == 1 else None
    return FTAB.get((pad, j0, w1, w2, tm), "AMB")

def shift_image(slot, lam, dl, d, rowcls, pad):
    """Banked shift image of one atom occurrence. rowcls=(par,sx,sp,word,term,j0...).
    Returns mapped type or ('OPEN', reason)."""
    par, sx = rowcls["par"], rowcls["sx"]
    if slot in (('L',), ('R',)):
        # unified rule: R always -2; L: even->-1, odd: sx0->0/sx1->-1 (LL-pad; mirror for RR)
        if pad == 'LL':
            dlm = -2 if slot == ('R',) else (-1 if (par == 0 or sx == 1) else 0)
        else:  # RR mirror
            dlm = -2 if slot == ('L',) else (-1 if (par == 0 or sx == 0) else 0)
        return ('t', (slot, lam + dlm, dl, d + 2))
    if slot[0] == 'F':
        w = rowcls["word"]
        tm = rowcls["term"]
        r = frule(pad, slot[1], w[0] if w else None, w[1] if len(w) > 1 else None, tm)
        if r == "AMB" or r is None:
            return ('OPEN', 'F-amb-or-missing')
        return ('t', ((slot[0], slot[1]), lam + r, dl, d + 2))
    if slot == ('NONE',):
        return ('K-agg', d + 2)
    return ('OPEN', 'unknown-slot')

def main():
    import numpy as np
    beta = json.load(open(OUT / "j4_betaexact.json"))["functionals"]
    print(f"[CL] beta functionals: {len(beta)}", flush=True)
    # occurrence sweep: rows = pointed configs n<=6 (shapes), each atom occurrence
    # gets row class; compute shift image for LL-pad; count distinct per functional.
    results = []
    for bi, bf in enumerate(beta):
        imgs = set()
        noccur = 0
        for terms in [bf["terms"]]:
            pass
        # for each atom in functional, find occurrences in corpus rows
        for ks, cc in bf["terms"]:
            k = eval(ks)
            if k[0] == 't':
                s, lam, dl, d = k[1]
            else:
                continue
            for n in (5, 6):
                for T in O.shapes_of(list(range(1, n + 1)))[:30]:
                    for y in depths_list(T):
                        _, lamr = R_coeffs(T, y)
                        dT = depths_list(T)
                        for z in dT:
                            if z == y:
                                continue
                            if (j4.slot_of(T, y, z), lamr.get(z, 0), dT[z] - dT[y], dT[y]) == (s, lam, dl, d):
                                P = path_nodes(T, y)
                                dd = len(P) - 1
                                sx = None if dd == 0 else (0 if P[0][1] is P[1] else 1)
                                pw, tm = foldword(T, y)
                                rc = {"par": dd % 2, "sx": sx, "word": pw, "term": tm}
                                for pad in ("LL",):
                                    imgs.add(str(shift_image(s, lam, dl, d, rc, pad)))
                                noccur += 1
                                break
                        else:
                            continue
                        break
        results.append({"bi": bi, "nterms": len(bf["terms"]), "images": sorted(imgs)[:6], "nimg": len(imgs)})
    nclosed = sum(1 for r in results if r["nimg"] <= 1 and not any("OPEN" in s for s in r["images"]))
    print(f"[CL] closed functionals: {nclosed}/{len(results)}", flush=True)
    for r in results:
        if r["nimg"] > 1 or any("OPEN" in s for s in r["images"]):
            print(f"    bi={r['bi']} nterms={r['nterms']} images={r['images']}", flush=True)
    json.dump(results, open(OUT / "j4_collide.json", "w"), indent=1, default=str)
    print("[CL] done", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())

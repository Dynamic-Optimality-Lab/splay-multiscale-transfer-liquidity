"""26N part 1: frontier audit, translated copies S(Delta), V_new identification,
coverage by existing expanded rows.
Usage: python scripts/wp6_nextlayer.py [frontier|trans|cover]
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
from wp6_staticR import depths_list
from wp6_lambda import R_coeffs

def main():
    modes = sys.argv[1:] or ["frontier"]
    import numpy as np
    Z = np.load(OUT / "j4_rednorm_mat.npz")
    keys = set(eval(k) for k in Z["keys"])
    Zx = np.load(OUT / "j4_ugar_mat.npz")
    xkeys = set(eval(k) for k in Zx["keys"])
    if "frontier" in modes:
        # max constrained indices per family in reduced system
        fam = defaultdict(lambda: [-1e9, 1e9])
        for k in keys:
            if k[0] == 'K':
                fam[('K',)][0] = max(fam[('K',)][0], k[1])
                fam[('K',)][1] = min(fam[('K',)][1], k[1])
            else:
                s, lam, dl, d = k[1]
                sk = (s[0], lam)
                fam[sk][0] = max(fam[sk][0], d)
                fam[sk][1] = min(fam[sk][1], d)
        print("[NL] frontier (max d per family):", flush=True)
        for k in sorted(fam, key=str):
            print(f"    {k}: maxd={fam[k][0]} mind={fam[k][1]}", flush=True)
        # max delta abs per F family
        fdl = defaultdict(lambda: [0, 0])
        for k in keys:
            if k[0] == 't' and k[1][0][0] == 'F':
                s, lam, dl, d = k[1]
                fdl[(s, lam)][0] = max(fdl[(s, lam)][0], dl)
                fdl[(s, lam)][1] = min(fdl[(s, lam)][1], dl)
        print("[NL] F delta extents:", flush=True)
        for k in sorted(fdl, key=str)[:16]:
            print(f"    {k}: [{fdl[k][1]},{fdl[k][0]}]", flush=True)
        json.dump({"frontier": [[str(k), v] for k, v in sorted(fam.items(), key=str)]},
                  open(OUT / "j4_frontier.json", "w"), indent=1, default=str)
    if "trans" in modes:
        # translated copies of the 2 canonical shift forms via validated S rules.
        # Forms from j4_shiftforms_v2 (raw, pre-quotient). Apply: L/R pattern rule needs
        # row class per atom -- NOT recorded. Instead translate at quotient level using
        # the uniform consequences: L/R atoms keep (slot,delta) with d+2 (lambda shifts
        # unknown per atom without class). REPORT limitation + do K/NONE/F-sib parts.
        forms = json.load(open(OUT / "j4_shiftforms_v2.json"))
        print(f"[NL] canonical forms: {len(forms)}", flush=True)
        # S-map onφορά K terms and sib-F terms deterministically; L/R need classes.
        # Count channel composition per form:
        for f in forms:
            ch = Counter()
            for ks, vv in f["terms"]:
                k = eval(ks)
                if k[0] == 'K':
                    ch['K'] += 1
                elif k[1][0] == ('NONE',):
                    ch['NONE'] += 1
                else:
                    ch[k[1][0][0] + str(k[1][1])] += 1
            print(f"  e.g.{f['meta']}: {dict(ch)}", flush=True)
        json.dump({"note": "L/R need row-class provenance; twin maps in trans2"}, open(OUT / "j4_trans.json", "w"), indent=1)
    print("[NL] done", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())

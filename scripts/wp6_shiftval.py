"""Type-level shift validation with provenance: apply banked S rules per atom
(row class measured in its own tree) to Dbar(k), compare with actual Dbar(k+2).
S rules (banked): L/R via 20-class (parity,sx,sx2)->(post,dl,ddl=0), d+2;
sib F_k->F_{k+2}, dl-2, d+2, lam preserved-class; K_d->K_{d+2}; NONE via K.
F-old: preserved index assumed (flagged separately).
Usage: python scripts/wp6_shiftval.py
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
tw = load('wp6_twins')
from wp6_staticR import depths_list, path_nodes
from wp6_lambda import R_coeffs

SHMAP = {}
def load_shiftmap():
    d = json.load(open(OUT / "j4_shiftmap.json"))
    for k, v in d.items():
        import ast
        SHMAP[ast.literal_eval(k)] = v[0]

def row_atoms_prov(B, y, sp):
    """Atoms with row-class provenance: ((slot,lam,dl,d),(par,sx,sx2,sp))."""
    P = path_nodes(B, y)
    d = len(P) - 1
    sx = None if d == 0 else (0 if P[0][1] is P[1] else 1)
    sx2 = None
    if d >= 2:
        sx2 = 0 if P[1][1] is P[2] else 1
    _, lam = R_coeffs(B, y)
    dB = depths_list(B)
    out = []
    for z in dB:
        if z == y:
            continue
        t = (j4.slot_of(B, y, z), lam.get(z, 0), dB[z] - dB[y], dB[y])
        out.append((t, (d % 2, sx, sx2, sp)))
    return out, d

def apply_S(entries):
    """Map each (type,class) via banked rules. Returns (mapped Counter, unmapped list)."""
    mapped = Counter()
    unmapped = []
    for (t, cls) in entries:
        s, lam, dl, d = t
        par, sx, sx2, sp = cls
        if s[0] in ('L', 'R'):
            key = (par, sx, sx2, s[0], lam)
            if key in SHMAP:
                ps, dlm, ddl = SHMAP[key]
                mapped[('t', (ps, lam + dlm, dl + ddl, d + 2))] += 1
            else:
                unmapped.append(('LR-noclass', str(t), str(cls)))
        elif s[0] == 'F':
            # old-F: index preserved assumed; lam unresolved -> keep lam, flag
            mapped[('t', (s, lam, dl, d + 2))] += 1
            unmapped.append(('F-lam-open', str(t)))
        elif s == ('NONE',):
            # aggregated via K separately; mark
            unmapped.append(('NONE-via-K', str(t)))
        else:
            unmapped.append(('other', str(t)))
    return mapped, unmapped

def main():
    load_shiftmap()
    # Dbar(1) Bacillus: Twin2(1,1) base+lift(Twin2(3,1)); Dbar(3): Twin2(3,1)+Twin2(5,1).
    # Compare S(Dbar(1) non-sib/non-K content) vs Dbar(3) same content.
    # Sibling-F and K handled by their own verified rules; focus: L/R mapping closure.
    rep = {}
    for tag, fn in (("K2", tw.Twin2), ("K3", tw.Twin1)):
        out = {}
        for k in (1, 3):
            B, T, S, y, z = fn(k, 1)
            v = T[0]
            # L/R atoms across the 4 base states (B,y),(B,v),(T,y),(T,v) with classes
            ents = []
            for (BB, yy) in ((B, y), (B, v), (T, y), (T, v)):
                tmp, dd = row_atoms_prov(BB, yy, 0)
                ents.extend([e for e in tmp if e[0][0] in (('L',), ('R',))])
            # apply S
            mapped, unm = apply_S(ents)
            # actual L/R atoms in lifted (k+2) twins' 4 states
            B2, T2, S2, y2, z2 = fn(k + 2, 1)
            v2 = T2[0]
            actual = Counter()
            for (BB, yy) in ((B2, y2), (B2, v2), (T2, y2), (T2, v2)):
                tmp, dd = row_atoms_prov(BB, yy, 0)
                for (t, cls) in tmp:
                    if t[0] in (('L',), ('R',)):
                        actual[('t', t)] += 1
            # compare S-mapped (as multiset over (slot,lam,dl,d)) vs actual
            # normalize: mapped keys are ('t', type); actual same form
            only_map = {str(k): v for k, v in (mapped - Counter({kk: vv for kk, vv in actual.items()})) .items()}
            only_act = {str(k): v for k, v in (Counter({kk: vv for kk, vv in actual.items()}) - mapped).items()}
            print(f"[SV] {tag} k={k}->k+2: mapped={sum(mapped.values())} actual={sum(actual.values())} "
                  f"only-map={len(only_map)} only-actual={len(only_act)}", flush=True)
            for kk in sorted(set(only_map) | set(only_act))[:10]:
                print(f"    {kk}: mapped{only_map.get(kk,0):+} actual{only_act.get(kk,0):+}", flush=True)
            out[f"k{k}"] = {"mapped": sum(mapped.values()), "actual": sum(actual.values()),
                             "only_map": len(only_map), "only_actual": len(only_act)}
        rep[tag] = out
    json.dump(rep, open(OUT / "j4_shiftval.json", "w"), indent=1, default=str)
    print("[SV] saved", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())

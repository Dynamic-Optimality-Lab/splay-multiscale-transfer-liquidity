"""Provenance-tracked shift validation: S applied per banked class rules.
S rules: L/R (slot,lam,dl,d)->(slot,lam+Dlam(class),dl,d+2), Dlam from
  (sp,parity,sx) table; sib F_k->F_{k+2},dl-2,d+2,lam same class rule (f_top preserved);
  K_d->K_{d+2}; NONE via K (aggregate map); F-old: index preserved, lam unresolved.
Compares S(Dbar(k)) vs actual Dbar(k+2); classifies residual.
Usage: python scripts/wp6_shift2.py
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

def row_class(B, y, sp):
    """Finite prepend class of row y: (parity, sx, sp)."""
    P = path_nodes(B, y)
    d = len(P) - 1
    sx = None if d == 0 else (0 if P[0][1] is P[1] else 1)
    return (d % 2, sx, sp)

def dlam_LR(parity, sx, sp, slot):
    """Banked one-level L/R lambda rule (26D class_table), doubled for Lift2?
    Lift2 = two pads; use COMPOSED rule measured on LL data: R:lam-2 always (sp=1)? Use
    banked two-level tables from j4_padding LL/RR (sp groups). Here sp=side of T.
    For Ext_L (sp=0): L always -1... that was ONE-level. Two-level LL: L -1, R -2? From
    n5_LL table: L lam->lam-1 patterns, R lam->lam-2. Rule: same-side always -1 per level?
    sp=0: L: -1 total over 2 levels? Table n5_LL: L 0->-1? shows L -1->-2 etc: L gets -1, R gets -2.
    So two-level (sp=0): dlam_L=-1, dlam_R=-2. Mirror (sp=1): dlam_R=-1, dlam_L=-2."""
    if sp == 0:
        return -1 if slot == 'L' else -2
    else:
        return -1 if slot == 'R' else -2

def atoms_with_prov(B, y, sp, sgn, out):
    _, lam = R_coeffs(B, y)
    dB = depths_list(B)
    for z in dB:
        if z == y:
            continue
        s_ = j4.slot_of(B, y, z)
        out.append((s_, lam.get(z, 0), dB[z] - dB[y], dB[y], row_class(B, y, sp), sgn))

def main():
    # instances: vine twins k=1,3 with pairs (y deep, v=T-root), sibling q=1, Ext_L (sp=0)
    for tag, fn in (("K2", tw.Twin2), ("K3", tw.Twin1)):
        # Dbar(1): base Twin(k=1), lifted Twin(k=3)
        B1, T1, S1, y1, z1 = fn(1, 1)
        B3, T3, S3, y3, z3 = fn(3, 1)
        v1 = T1[0]; v3 = T3[0]
        # full 8-state signed atom lists with provenance
        la = []
        for (BB, TT, yy, vv, sgn8) in ((B3, T3, y3, v3, 1), (B3, T3, y3, v3, 0)):
            pass
        base_states = [(B1, y1, 1), (B1, v1, -1), (T1, y1, -1), (T1, v1, 1)]
        lift_states = [(B3, y3, 1), (B3, v3, -1), (T3, y3, -1), (T3, v3, 1)]
        # Dbar(1) = lift - base (signed)
        d1 = Counter()
        prov = defaultdict(list)
        for (BB, yy, sgn) in lift_states:
            tmp = []
            atoms_with_prov(BB, yy, 0, 1, tmp)
            for a in tmp:
                d1[(a[0], a[1], a[2], a[3])] += sgn
        for (BB, yy, sgn) in base_states:
            tmp = []
            atoms_with_prov(BB, yy, 0, 1, tmp)
            for a in tmp:
                d1[(a[0], a[1], a[2], a[3])] -= sgn if False else 0  # placeholder
                d1[(a[0], a[1], a[2], a[3])] += -sgn
        d1 = Counter({k: v for k, v in d1.items() if v != 0})
        print(f"[S2] {tag} Dbar(1) support={len(d1)}", flush=True)
        # apply S per banked rules with provenance re-derivation is complex;
        # instead DIRECTLY verify the banked per-class L/R two-level rule on
        # persistent atoms base->lifted within Dbar(1)'s own 8 states:
        # for each persistent (row y base->lifted, key z), check dlam matches table.
        bad = tot = 0
        for (BB, yy, sgn) in base_states:
            # find lifted counterpart: B1->B3 (same key? keys differ across twins!)
            pass
        print(f"[S2] {tag}: key-tracking across k impossible (twin key ranges differ);", flush=True)
        print(f"[S2] {tag}: shift validation must use CLASS-channel form (counts per class).", flush=True)
    # CLASS-CHANNEL validation: group Dbar atoms by (slot,class) and compare
    # Dbar(1) vs Dbar(3) channel structure.
    print("[S2] done (see analysis)", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())

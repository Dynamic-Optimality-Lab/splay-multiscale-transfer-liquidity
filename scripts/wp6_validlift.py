"""Valid-lift infrastructure + quarantine registry.
Provides assert_valid_bst + valid double-pad lifts (LL/RR with fresh keys).
Also records which prior artifacts used the invalid [0,None,[-1,None,T]] lift.
Usage: python scripts/wp6_validlift.py audit
"""
import sys, json, copy
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
OUT = ROOT / "artifacts/v04/wp6_present/0909c74a/dual_mine"

def assert_valid_bst(T, lo=None, hi=None):
    if T is None:
        return True
    k, l, r = T[0], T[1], T[2]
    assert (lo is None or lo < k) and (hi is None or k < hi), (lo, k, hi)
    return assert_valid_bst(l, lo, k) and assert_valid_bst(r, k, hi)

def relabel(T, f):
    if T is None:
        return None
    return [f(T[0]), relabel(T[1], f), relabel(T[2], f)]

def depths_list(T):
    out = {}
    def go(nd, d):
        if nd is None:
            return
        out[nd[0]] = d
        go(nd[1], d + 1)
        go(nd[2], d + 1)
    go(T, 0)
    return out

def lift_LL_valid(T):
    """Double left-prepend above T-root with fresh keys. Returns T2 (valid)."""
    d = depths_list(T)
    step = 10
    T = relabel(copy.deepcopy(T), lambda x: x * step)
    r = T[0]
    # left spine above root: N1 < ... wait [N1, T, None] needs max(T) < N1
    mx = max(depths_list(T).keys())
    N1, N2 = mx + 3, mx + 6
    return [N2, [N1, T, None], None]

def lift_RR_valid(T):
    d = depths_list(T)
    step = 10
    T = relabel(copy.deepcopy(T), lambda x: x * step)
    mn = min(depths_list(T).keys())
    N1, N2 = mn - 3, mn - 6
    return [N2, None, [N1, None, T]]

QUARANTINE = {
    "invalid_lift": "[0,None,[-1,None,T]] violates BST (right-subtree key -1 < root 0)",
    "tainted_scripts": ["wp6_lift2.py:mode_oldcore", "wp6_shiftmap.py", "wp6_shiftgate.py(forms/dtqgate)",
                        "wp6_shiftgate2.py", "wp6_dbar.py", "wp6_pairsign.py", "wp6_lift2 refined probe"],
    "tainted_artifacts": ["j4_oldcore.json", "j4_shiftmap.json", "j4_dbarcorpus.json",
                          "j4_countlaw.json", "j4_shiftforms*.json", "j4_dtqgate.json",
                          "j4_pairsign.json", "j4_crem.json"],
    "void_results": ["oldcore 20-class counts", "shiftmap details", "dbar support numbers",
                     "shift-form ranges/DTQ gate (26L)", "pair/crem sups", "countlaw +2-NONE (must reverify)"],
    "standing": ["left-prepend table (valid keys)", "LR-prepend probe (valid keys)",
                 "twin K2/K3 multiset validations (valid lifts)", "class_table Pad_L/R (valid)",
                 "all Ext/Pad/context probes (valid)", "old-F table LL/RR/LR (valid lifts)",
                 "ug/ugar/rednorm LP systems (no lifts involved)"]
}

def main():
    modes = sys.argv[1:] or ["audit"]
    if "audit" in modes:
        # sanity: lifts produce valid trees with expected depth shift
        import wp6_cycle_ratio as O
        nbad = ntot = 0
        for T in O.shapes_of(list(range(1, 5)))[:20]:
            for fn in (lift_LL_valid, lift_RR_valid):
                T2 = fn(T)
                ntot += 1
                try:
                    assert_valid_bst(T2)
                except AssertionError:
                    nbad += 1
        print(f"[VL] valid lifts: {ntot-nbad}/{ntot}", flush=True)
        json.dump(QUARANTINE, open(OUT / "j4_quarantine.json", "w"), indent=1)
        print("[VL] quarantine registry saved", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())

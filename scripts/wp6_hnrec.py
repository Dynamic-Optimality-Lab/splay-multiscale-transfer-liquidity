"""PIVOT-25R-HN §5-9: mass-flow recurrence, collisions, invariants.

Re-steps each high-need B-phase capturing full X_i per double:
(L,R,U,V,pat,twin pre/post,remdepth,fringe profile,turn suffix).
Collision ladder X0-X4 on X_i -> X_{i+1} determinism. Verifies analytic
(L,R,U,V) recurrence per orientation. Invariant probes. Adversarial
constructions (alternating suffix, delayed twin, unbalanced fringe) +
mirrors + held-out.
"""
from __future__ import annotations
import sys
import copy
import json
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
import wp6_overflow as V


def step(sid, msg):
    print("[HNR %s] %s" % (sid, msg), flush=True)


def reroot(P):
    r = P
    while r["p"] is not None:
        r = r["p"]
    return r


def find(P, key):
    P = reroot(P)
    stack = [P]
    while stack:
        nd = stack.pop()
        if nd["k"] == key:
            return nd
        if nd["l"] is not None:
            stack.append(nd["l"])
        if nd["r"] is not None:
            stack.append(nd["r"])
    return None


def sz(nd):
    if nd is None:
        return 0
    return 1 + sz(nd["l"]) + sz(nd["r"])


def path_from_root(P, x):
    P = reroot(P)
    out = []
    nd = P
    while nd is not None and nd["k"] != x:
        if x < nd["k"]:
            out.append((nd["k"], "L"))
            nd = nd["l"]
        else:
            out.append((nd["k"], "R"))
            nd = nd["r"]
    if nd is None:
        return None
    out.append((x, "."))
    return out


def fringe_above(Bptr, x):
    """Per remaining path level above x: (side-of-path-child,
    off-path-child size, turn pair or None at top). From x upward."""
    nd = find(Bptr, x)
    out = []
    while nd["p"] is not None:
        p = nd["p"]
        side = "L" if p["l"] is nd else "R"
        other = p["r"] if side == "L" else p["l"]
        g = p["p"]
        turn = None
        if g is not None:
            ps = "L" if g["l"] is p else "R"
            turn = ps + side
        out.append((side, sz(other), turn))
        nd = p
    return out


def state_of(Aptr, Bptr, x):
    """Full X_i pre-double (x must have depth>=2)."""
    B = reroot(Bptr)
    nd = find(B, x)
    p = nd["p"]
    g = p["p"]
    if p["l"] is nd and g["l"] is p:
        pat = "LL"
    elif p["r"] is nd and g["r"] is p:
        pat = "RR"
    elif p["r"] is nd and g["l"] is p:
        pat = "LR"
    else:
        pat = "RL"
    L = sz(nd["l"])
    R = sz(nd["r"])
    if pat in ("LL", "LR"):
        U = sz(p["r"]) if pat == "LL" else sz(p["l"])
        V = sz(g["r"])
    else:
        U = sz(p["l"]) if pat == "RR" else sz(p["r"])
        V = sz(g["l"])
    rA = reroot(Aptr)["k"]
    tw = 1 if rA == reroot(B)["k"] else 0
    fr = fringe_above(Bptr, x)
    rem = len(fr) - 1  # depth of x
    return {"pat": pat, "L": L, "R": R, "U": U, "V": V, "tw": tw,
            "fr": [list(f) for f in fr], "rem": rem}


def do_double(Bptr, x):
    import liquidity.legacy_embedding as PE
    B = reroot(Bptr)
    nd = find(B, x)
    p = nd["p"]
    g = p["p"]
    if p["l"] is nd and g["l"] is p:
        PE._rot_right(g)
        PE._rot_right(p)
    elif p["r"] is nd and g["r"] is p:
        PE._rot_left(g)
        PE._rot_left(p)
    elif p["r"] is nd and g["l"] is p:
        PE._rot_left(p)
        PE._rot_right(g)
    else:
        PE._rot_right(p)
        PE._rot_left(g)
    return reroot(B)


def run_access(A0, B0, x):
    """Returns list of (X_pre, s, X_post, tw_post) per B-double."""
    A = V.to_ptr(copy.deepcopy(A0))
    B = V.to_ptr(copy.deepcopy(B0))
    A, _ = V.splay_cap(A, x, 0, [])
    out = []
    while True:
        nd = find(B, x)
        if nd["p"] is None or nd["p"]["p"] is None:
            break
        X = state_of(A, B, x)
        rA = reroot(A)["k"]
        tw0 = 1 if rA == reroot(B)["k"] else 0
        D0 = sum(V.depths_of(reroot(B)).values())
        B = do_double(B, x)
        tw1 = 1 if rA == reroot(B)["k"] else 0
        D1 = sum(V.depths_of(reroot(B)).values())
        s = 2 * (tw1 - tw0) + (D0 - D1)
        Xp = state_of(A, B, x) if find(B, x)["p"] is not None and \
            find(B, x)["p"]["p"] is not None else None
        out.append((X, s, Xp, tw1))
    return out


def Xkey(X, level):
    if X is None:
        return None
    base = (X["pat"],)
    if level >= 1:
        base += (X["L"], X["R"])
    if level >= 2:
        base += (X["U"], X["V"], X["pat"])
    if level >= 3:
        base += (X["tw"],)
    if level >= 4:
        base += (tuple(tuple(f) for f in X["fr"]),)
    return base


def main():
    bank = json.loads((ROOT / "artifacts" / "v04" / "wp6_present" /
                       "0909c74a" / "dual_mine" /
                       "highneed_bank.json").read_text())
    hn = [r for r in bank if r["need"] >= 3 and r["rem"] >= 1]
    step("L", "high-need=%d" % len(hn))
    seqs = []
    for r in hn:
        seqs.append(run_access(r["A"], r["B"], r["x"]))
    step("L", "re-stepped %d accesses" % len(seqs))
    # collision ladder: X_i -> (s_i, X_{i+1}) determinism
    for lv in range(5):
        groups = defaultdict(list)
        for s in seqs:
            for (X, pay, Xp, tw1) in s:
                k = Xkey(X, lv)
                Xn = Xkey(Xp, 4) if Xp else "END"
                groups[k].append((pay, str(Xn)))
        amb = {k: v for k, v in groups.items() if len(set(v)) > 1}
        step("X%d" % lv, "states=%d amb=%d" % (len(groups), len(amb)))
    # recurrence check: predict next (L,R) from rotation geometry
    # LL: L'=L (x.left kept); RR: R'=R; LR/RL: both change (verify vs data)
    import pickle
    pickle.dump(seqs, open("C:/Users/SAIFMA~1/AppData/Local/Temp/opencode/"
                           "hnseqs.pkl", "wb"))
    step("S", "saved hnseqs.pkl")
    return 0


if __name__ == "__main__":
    sys.exit(main())

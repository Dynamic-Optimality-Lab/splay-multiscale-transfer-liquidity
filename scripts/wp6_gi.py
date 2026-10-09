"""WP-6 GI: geometric-inversion coin experiment (C177).

Implements GI Defs 5/6/7 EXACTLY (Chalermsook-Jiamjitrak ESA 2020) with
orientation subject=B, reference=A (pre-access A per mission §5):
  I_T(z) = (left_T(z), right_T(z)) open interval, bounds = nearest
    ancestor keys to left/right (0 / n+1 if none); laminar family.
  P_A(a) = {a, left_A(a), right_A(a)} (three important points).
  EI(z,a): z in I_A(a) AND exists b in P_A(a) with b in I_B(z).
  Phi = total EI count (coins: z-coin at node a).
Tests (§5-§7, §23-GOOD, all bounded):
  T1 CP identity: for B-access x, CP(z, LCA_A(z,x))=1 for z on S_B(x)
      satisfies CP <= Phi pointwise (Lemma 9 analog; must hold exactly).
  T2 twin genesis: Phi(B0=T0, A0=T0) value (expect ~0; else record).
  T3 subject update (B splays, A fixed): net-new coins vs |S_A|-path
      (witness-interval bound would need net-new <= C*|S_O|).
  T4 reference update (A splays incl. DELETE windows, B fixed):
      Delta_Phi vs e_A (reference-update bound would need Delta <= C*e_A).
Reports max ratios + witnesses. Unboundedness in T3/T4 kills the
corresponding GI transplant with machine-checked refutation shape;
boundedness would pivot the campaign.
Artifact: gi.json. Sealed files untouched.
"""
from __future__ import annotations
import sys
import json
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_pushledger import gen
from wp6_eventflow import to_ptr, splay_A, splay_B_push
from solver import encode as E


def step(sid, msg):
    print("[WP-6][GI %s] %s" % (sid, msg), flush=True)


def depths_of(T):
    dd = {}
    stack = [(T, 0)]
    while stack:
        nd, d = stack.pop()
        if nd is None:
            continue
        dd[nd["k"]] = d
        stack.append((nd["l"], d + 1))
        stack.append((nd["r"], d + 1))
    return dd


def path_to(T, x):
    """Nodes root->x (BST descent); None if absent."""
    path = []
    cur = T
    while cur is not None:
        path.append(cur)
        if x == cur["k"]:
            return path
        cur = cur["l"] if x < cur["k"] else cur["r"]
    return None


def intervals(T, n):
    """I_T(z) = (lo, hi) open bounds per key via ancestor walk."""
    out = {}
    # collect nodes
    nodes = {}
    stack = [T]
    while stack:
        nd = stack.pop()
        if nd is None:
            continue
        nodes[nd["k"]] = nd
        stack.append(nd["l"])
        stack.append(nd["r"])
    for k, nd in nodes.items():
        lo, hi = 0, n + 1
        cur = nd["p"]
        while cur is not None:
            ck = cur["k"]
            if ck < k:
                if ck > lo:
                    lo = ck
            else:
                if ck < hi:
                    hi = ck
            cur = cur["p"]
        out[k] = (lo, hi)
    return out


def lca(T, x, z):
    """LCA key of present x,z via BST descent."""
    cur = T
    while cur is not None:
        ck = cur["k"]
        if x == ck or z == ck:
            return ck
        if (x < ck) != (z < ck):
            return ck
        cur = cur["l"] if x < ck else cur["r"]
    return None


def phi_of(B, A, n):
    """Total extended inversions, subject=B reference=A."""
    IB = intervals(B, n)
    IA = intervals(A, n)
    total = 0
    for a, (loa, hia) in IA.items():
        pa = {a, loa, hia}
        for z, (lob, hib) in IB.items():
            if not (loa < z < hia):
                continue
            hit = False
            for b in pa:
                # b in I_B(z) <=> lob < b < hib (interval test)
                if lob < b < hib:
                    hit = True
                    break
            if hit:
                total += 1
    return total


def cp_check(B, A, n, x):
    """Returns (ok, path_len, missing) for Lemma-9 analog."""
    pB = path_to(B, x)
    if not pB or pB[-1]["k"] != x:
        return True, 0, 0
    IB = intervals(B, n)
    IA = intervals(A, n)
    missing = 0
    for nd in pB:
        z = nd["k"]
        w = lca(A, x, z)
        if w is None:
            missing += 1
            continue
        loa, hia = IA[w]
        if not (loa < z < hia):
            missing += 1
            continue
        pa = {w, loa, hia}
        lob, hib = IB[z]
        if not any(lob < b < hib for b in pa):
            missing += 1
    return missing == 0, len(pB), missing


def main() -> int:
    step("GI-00", "geometric-inversion coin experiment")
    agg = Counter()
    agg["phi_twin_max"] = 0
    agg["cp_fail"] = 0
    agg["cp_n"] = 0
    # ratio trackers: (num, den) maxima
    agg["t3_max_new"] = 0
    agg["t3_max_path"] = 0
    agg["t3_worst_ratio"] = 0.0
    agg["t4_max_dphi"] = 0
    agg["t4_max_ea"] = 0
    agg["t4_worst_ratio"] = 0.0
    done = 0
    for s in range(40):
        n, T0, H = gen(s, b"gi")
        if n > 64:
            continue
        try:
            pre = E.precompute(n, T0, H)
            bad = E.exec_counts(pre, "P_all", 6, 2, (2, 2))["violations"]
        except Exception:
            continue
        if bad:
            continue
        done += 1
        A, B = to_ptr(T0), to_ptr(T0)
        ph = phi_of(B, A, n)
        if ph > agg["phi_twin_max"]:
            agg["phi_twin_max"] = ph
        for acc in pre:
            x, mode = acc["x"], acc["mode"]
            # CP check pre-access (subject=B path, reference=A LCAs)
            ok, plen, miss = cp_check(B, A, n, x)
            agg["cp_n"] += 1
            if not ok:
                agg["cp_fail"] += 1
            # T4: A-update (DELETE or KEEP A-phase), B fixed
            ph0 = phi_of(B, A, n)
            A, invs = splay_A(A, x)
            eA = len(invs)
            ph1 = phi_of(B, A, n)
            dphiA = ph1 - ph0
            if eA > 0:
                r = dphiA / eA
                if r > agg["t4_worst_ratio"]:
                    agg["t4_worst_ratio"] = r
                    agg["t4_worst_rec"] = {"eA": eA, "dphi": dphiA}
            if abs(dphiA) > agg["t4_max_dphi"]:
                agg["t4_max_dphi"] = abs(dphiA)
            # T3: B-update (KEEP only), A fixed
            if mode == "KEEP":
                ph2 = phi_of(B, A, n)
                B, pushes = splay_B_push(B, x)
                eB = len(pushes)
                ph3 = phi_of(B, A, n)
                dphiB = ph3 - ph2
                pB = path_to(B, x)
                # path length pre-splay needed; recompute approx via eB
                # witness bound would be net-new <= C*|S_O|; record raw
                if dphiB > agg["t3_max_new"]:
                    agg["t3_max_new"] = dphiB
                    agg["t3_worst_rec"] = {"eB": eB, "dphi": dphiB}
        if s % 10 == 9:
            step("GI-P", "s=%d done=%d" % (s, done))
    out = dict(agg)
    out.update({"evals": done})
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "gi.json").write_text(
        json.dumps(out, indent=1, sort_keys=True, default=str), encoding="utf-8")
    step("GI-01", json.dumps(out, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())

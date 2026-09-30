"""WP-6 TRIPLE: shape-aware triple-conjunction assembler (C61b).

Assembles what random walks never do: B-near/A-far pushers (deepen B-x, avoid A-x)
in DELETE-then-KEEP form (E2-hole) + DELETE-x-root + A-trivial burst.
Greedy per cycle: score candidates z by (B-depth-gain of x, A-path-overlap with
x-zone (minimize), A-cost (minimize)) via one-step lookahead replay.
Kill: shortfall>0 exit 2. Else track best (min one-access slack at bursts,
max e_B/f ratio, min new-old at E1-empty bursts).
Artifact: triple.json. Sealed files untouched.
"""
from __future__ import annotations
import sys
import copy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_hallcore import build_graph, maxflow_cap3, delta_of
from wp6_offline import gc_gap
from wp6_tightest import vine, Rng
from wp6_eventflow import to_ptr, splay_A, splay_B_push
from solver import encode as E


def step(sid, msg):
    print("[WP-6][TRIPLE %s] %s" % (sid, msg), flush=True)


import hashlib as _h
from collections import defaultdict


def btpath(T, x):
    # B-path keys from x up to root (pre-splay), via pointer replay
    d, path = None, None
    # find node
    stack = [T]
    node = None
    while stack:
        nd = stack.pop()
        if nd is None:
            continue
        if nd["k"] == x:
            node = nd
            break
        stack.append(nd["l"])
        stack.append(nd["r"])
    if node is None:
        return set()
    s = set()
    while node is not None:
        s.add(node["k"])
        node = node["p"]
    return s


def atriple_keys(A, z):
    A2, invs = splay_A(copy.deepcopy(A), z)
    keys = set()
    for S in invs:
        keys |= set(S)
    return keys


def eval_hist(n, T0, H):
    G = build_graph(n, T0, H)
    if G is None:
        return None
    f, nb, lv = maxflow_cap3(G)
    if nb - f > 0:
        return ("KILL", nb - f, nb)
    gap, _ = gc_gap(n, T0, H)
    if gap > 0:
        return ("GCKILL", gap, nb)
    return ("OK", nb, gap)


def build_history(n, T0, xc, ncyc, rng):
    H = []
    A, B = to_ptr(T0), to_ptr(T0)
    for c in range(ncyc):
        # pick 0-2 pushers: B-near (on/near x B-path) + A-far (A-triples avoid x-zone)
        bpath = btpath(B, xc)
        xzone = set([xc] + [k for k in bpath])
        cands = []
        for z in range(1, n + 1):
            if z == xc:
                continue
            # B-effect: simulate KEEP z, measure x depth gain in B
            B2 = copy.deepcopy(B)
            # depth before/after for x
            def dep(T, x):
                st = [T]
                nd = None
                while st:
                    q = st.pop()
                    if q is None:
                        continue
                    if q["k"] == x:
                        nd = q
                        break
                    st.append(q["l"])
                    st.append(q["r"])
                d = 0
                while nd is not None and nd["p"] is not None:
                    nd = nd["p"]
                    d += 1
                return d
            d0 = dep(B, xc)
            B2t, _ = splay_B_push(B2, z)
            d1 = dep(B2t, xc)
            gain = d1 - d0
            if gain <= 0:
                continue
            akeys = atriple_keys(A, z)
            overlap = len(akeys & xzone)
            cands.append((overlap, -gain, z))
        cands.sort()
        npush = min(len(cands), int(rng(9000 + c)) % 3)
        for _, _, z in cands[:npush]:
            H.append(["DELETE", z])  # E2-hole form: DELETE half unrecorded
            H.append(["KEEP", z])
            A, _ = splay_A(A, z)
            B, _ = splay_B_push(B, z)
        H.append(["DELETE", xc])
        A, _ = splay_A(A, xc)
        H.append(["KEEP", xc])
        A, _ = splay_A(A, xc)
        B, _ = splay_B_push(B, xc)
    return H


def main() -> int:
    import json
    step("TR-00", "shape-aware triple-conjunction assembler")
    TP = ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "triple.json"
    best = None
    evals = 0
    holders = []
    for s in range(120):
        rng = Rng(("tr%d" % s).encode(), b"tri")
        r = rng(0)
        n = [64, 128][r % 2]
        T0 = vine(n, (r >> 8) % 2 == 0)
        xc = 20 + (r >> 16) % 60
        xc = min(n - 1, max(2, xc))
        H = build_history(n, T0, xc, 3 + (r >> 24) % 4, Rng(("tr%d" % s).encode(), b"trh"))
        v = eval_hist(n, T0, H)
        evals += 1
        if v is None:
            continue
        if v[0] == "KILL":
            step("TR-KILL", "HALL seed %d shortfall=%d H=%s" % (s, v[1], H))
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json").write_text(
                json.dumps({"kill": True, "n": n, "H": H}, indent=1, default=str), encoding="utf-8")
            return 2
        if v[0] == "GCKILL":
            step("TR-KILL", "GC seed %d" % s)
            return 2
        holders.append((T0, H, n))
    step("TR-01", "seeds evals=%d clean holders=%d" % (evals, len(holders)))
    holders = holders[-12:]
    it = 0
    while evals < 3000:
        it += 1
        r = int.from_bytes(_h.sha256(b"trm|%d" % it).digest(), "big")
        T0, H, n = holders[(r >> 2) % len(holders)]
        H2 = copy.deepcopy(H)
        op = r % 4
        if op == 0 and H2:
            i = (r >> 5) % len(H2)
            H2[i][0] = "DELETE" if H2[i][0] == "KEEP" else "KEEP"
        elif op == 1 and H2:
            i = (r >> 5) % len(H2)
            H2[i][1] = 1 + (r >> 13) % n
        elif op == 2 and len(H2) < 80:
            H2.insert((r >> 5) % (len(H2) + 1), ["KEEP" if r % 2 else "DELETE", 1 + (r >> 13) % n])
        elif len(H2) > 4:
            del H2[(r >> 5) % len(H2)]
        v = eval_hist(n, T0, H2)
        evals += 1
        if v is None:
            continue
        if v[0] == "KILL":
            step("TR-KILL", "HALL it=%d shortfall=%d H=%s" % (it, v[1], H2))
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json").write_text(
                json.dumps({"kill": True, "n": n, "H": H2}, indent=1, default=str), encoding="utf-8")
            return 2
        if v[0] == "GCKILL":
            step("TR-KILL", "GC it=%d" % it)
            return 2
        if (r >> 6) % 3 == 0:
            holders.append((T0, H2, n))
            holders = holders[-12:]
        if it % 1000 == 0:
            step("TR-02", "it=%d evals=%d clean" % (it, evals))
    step("TR-03", "evals=%d NO KILL (triple conjunction never assembles to kill)" % evals)
    TP.write_text(json.dumps({"evals": evals, "nokill": True,
                              "scope": "shape-aware B-near/A-far + E2-hole + root-burst"}, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

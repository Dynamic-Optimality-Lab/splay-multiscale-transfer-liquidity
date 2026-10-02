"""WP-6 GREEDYMIG: greedy rule under migration pressure (C106).

Triple objective hillclimb: co-location -> 0 AND FWD|E1E4TK-shortfall > 0 AND
maxflow == 0 (rule fails where optimum succeeds, migration-caused).
Found => rule-crown revoked under migration (backstop theory needed).
Not found (5k) => rule migration-proof finite-strong (T-first + historicals).
Artifact: greedymig.json (+hallkill on Hall kill). Sealed files untouched.
"""
from __future__ import annotations
import sys
import copy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_hallcore import build_graph, maxflow_cap3
from wp6_tightest import vine, Rng
from wp6_eventflow import to_ptr, splay_A, splay_B_push
from wp6_greedy import greedy_with
from solver import encode as E


def step(sid, msg):
    print("[WP-6][GREEDYMIG %s] %s" % (sid, msg), flush=True)


import hashlib as _h


def chain_keys(T, x):
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
    s = set()
    while nd is not None:
        s.add(nd["k"])
        nd = nd["p"]
    return s


def eval_hist(n, T0, H):
    G = build_graph(n, T0, H)
    if G is None:
        return None
    f, nb, _ = maxflow_cap3(G)
    if nb - f > 0:
        return ("KILL", nb - f, nb)
    Aevs, Bevs = G["Aevs"], G["Bevs"]
    pre2 = G["pre"]
    A2, B2 = to_ptr(T0), to_ptr(T0)
    Arot = {}
    acc_of = {}
    aid = 0
    for idx, acc in enumerate(pre2):
        A2, invs = splay_A(A2, acc["x"])
        for (S, sited) in zip(invs, acc["sites"]):
            Arot[aid] = frozenset(S)
            acc_of[aid] = idx
            aid += 1
        if acc["mode"] == "KEEP":
            B2, _ = splay_B_push(B2, acc["x"])
    seq = sorted(range(len(Bevs)), key=lambda j: (Bevs[j][0], j))
    g = greedy_with(n, T0, H, G, Arot, acc_of, seq, ["E1", "E4", "T", "K"])
    # co-location at last burst
    A, B = to_ptr(T0), to_ptr(T0)
    impkeys = set()
    coloc = 1.0
    pre = E.precompute(n, T0, H)
    for idx, acc in enumerate(pre):
        A, invs = splay_A(A, acc["x"])
        for S in invs:
            impkeys |= set(S)
        if acc["mode"] == "KEEP":
            B, _ = splay_B_push(B, acc["x"])
    last = max(b[0] for b in Bevs)
    ch = chain_keys(B, pre2[last]["x"])
    # B is post-state; approximate pre-burst chain via depth only: use count proxy
    # (exact pre-chain needs replay split; proxy: coloc over final chain)
    coloc = len(impkeys & ch) / max(1, len(impkeys))
    return ("OK", g, coloc, nb)


def gen_seed(s, tag):
    rng = Rng(("gm%d" % s).encode(), tag)
    r = rng(0)
    n = [64, 128][r % 2]
    T0 = vine(n, (r >> 8) % 2 == 0)
    xc = 2 + (r >> 16) % (n - 2)
    H = []
    L = 16 + (r >> 24) % 16
    for i in range(L):
        rr = Rng(("gm%d" % s).encode(), tag + b"h%d" % i)
        q = rr(1000 + i)
        op = (q >> 2) % 10
        if op < 4:
            H.append(["DELETE", 1 + (q >> 9) % n])
        elif op < 7:
            H.append(["KEEP", 1 + (q >> 5) % n])
        else:
            H.append(["KEEP", xc])
    for _ in range(1 + (r >> 20) % 2):
        H.append(["KEEP", xc])
    return n, T0, H


def main() -> int:
    import json
    step("GM-00", "greedy rule under migration pressure")
    TP = ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "greedymig.json"
    best = None
    ruledead = 0
    evals = 0
    holders = []
    BUDGET = 5000
    for s in range(100):
        n, T0, H = gen_seed(s, b"gm")
        v = eval_hist(n, T0, H)
        evals += 1
        if v is None:
            continue
        if v[0] == "KILL":
            step("GM-KILL", "HALL seed %d (GC-STATIC DEAD)" % s)
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json").write_text(
                json.dumps({"kill": True, "n": n, "H": H}, indent=1, default=str), encoding="utf-8")
            return 2
        _, g, coloc, nb = v
        holders.append((T0, H, n))
        key = (-g if g > 0 else 0, coloc)
        if g > 0:
            ruledead += 1
            if best is None or coloc < best[0]:
                best = (coloc, g, nb)
                step("GM-RULEHIT", "seed %d coloc=%.4f greedy=%d nb=%d" % (s, coloc, g, nb))
                if coloc < 0.05:
                    TP.write_text(json.dumps({"ruledead_mig": True, "seed": s, "H": H},
                                             indent=1, default=str), encoding="utf-8")
                    return 3
    holders = holders[-14:]
    step("GM-01", "seeds evals=%d ruledead=%d" % (evals, ruledead))
    it = 0
    while evals < BUDGET:
        it += 1
        r = int.from_bytes(_h.sha256(b"gmm|%d" % it).digest(), "big")
        T0, H, n = holders[(r >> 2) % len(holders)]
        H2 = copy.deepcopy(H)
        op = r % 4
        if op == 0 and H2:
            i = (r >> 5) % len(H2)
            H2[i][0] = "DELETE" if H2[i][0] == "KEEP" else "KEEP"
        elif op == 1 and H2:
            i = (r >> 5) % len(H2)
            H2[i][1] = 1 + (r >> 13) % n
        elif op == 2 and len(H2) < 70:
            H2.insert((r >> 5) % (len(H2) + 1), ["KEEP" if r % 2 else "DELETE", 1 + (r >> 13) % n])
        elif len(H2) > 4:
            del H2[(r >> 5) % len(H2)]
        v = eval_hist(n, T0, H2)
        evals += 1
        if v is None:
            continue
        if v[0] == "KILL":
            step("GM-KILL", "HALL it=%d (GC-STATIC DEAD)" % it)
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json").write_text(
                json.dumps({"kill": True, "n": n, "H": H2}, indent=1, default=str), encoding="utf-8")
            return 2
        _, g, coloc, nb = v
        if g > 0:
            ruledead += 1
            if best is None or coloc < best[0]:
                best = (coloc, g, nb)
                step("GM-RULEHIT", "it=%d coloc=%.4f greedy=%d nb=%d" % (it, coloc, g, nb))
                holders.append((T0, H2, n))
                holders = holders[-14:]
                if coloc < 0.05:
                    TP.write_text(json.dumps({"ruledead_mig": True, "it": it, "H": H2},
                                             indent=1, default=str), encoding="utf-8")
                    return 3
        elif (r >> 6) % 4 == 0:
            holders.append((T0, H2, n))
            holders = holders[-14:]
        if it % 1200 == 0:
            step("GM-02", "it=%d evals=%d ruledead=%d" % (it, evals, ruledead))
    step("GM-03", "evals=%d ruledead=%d NO KILL" % (evals, ruledead))
    TP.write_text(json.dumps({"evals": evals, "ruledead": ruledead, "nokill": True},
                             indent=1, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

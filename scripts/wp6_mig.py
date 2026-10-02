"""WP-6 MIG: migration-adversary vs co-location rate (C105).

Wall analysis: E3-hits need CURRENT co-location (imprint-key positioned on
burst chain at burst time); keys migrate (rotations). Objective: minimize
co-location rate (imprints currently on chain / all imprints) + maximize split,
then burst. Co-location -> 0 yet saturate => migration-wall confirmed finite
(E1/K/fresh carry). shortfall>0 => KILL (migration starves supply: DEAD).
Artifact: mig.json (+hallkill on kill). Sealed files untouched.
"""
from __future__ import annotations
import sys
import copy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_hallcore import build_graph, maxflow_cap3, delta_of
from wp6_tightest import vine, Rng
from wp6_eventflow import to_ptr, splay_A, splay_B_push
from solver import encode as E


def step(sid, msg):
    print("[WP-6][MIG %s] %s" % (sid, msg), flush=True)


import hashlib as _h


def pos_of(T, x):
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
    return nd


def chain_keys(T, x):
    nd = pos_of(T, x)
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
    # co-location: fraction of sited past A-imprint keys currently on burst chain
    A, B = to_ptr(T0), to_ptr(T0)
    impkeys = set()
    worst = None
    pre = E.precompute(n, T0, H)
    for idx, acc in enumerate(pre):
        A, invs = splay_A(A, acc["x"])
        for S in invs:
            impkeys |= set(S)
        if acc["mode"] == "KEEP":
            B, _ = splay_B_push(B, acc["x"])
        if acc["mode"] == "KEEP" and len(acc["Bev"]) >= 4:
            ch = chain_keys(B, acc["x"])
            # note B already splayed (post-state); use pre-splay chain approx via depth only for rate
            coloc = len(impkeys & ch) / max(1, len(impkeys))
            eB = len(acc["Bev"])
            eA = sum(1 for z in acc["sites"] if z)
            key = (coloc, -(eB - 3 * eA))
            if worst is None or key < (worst[0], -worst[1]):
                worst = (coloc, eB - 3 * eA, eB, idx)
    return ("OK", nb, worst)


def gen_seed(s, tag):
    rng = Rng(("mg%d" % s).encode(), tag)
    r = rng(0)
    n = [64, 128][r % 2]
    T0 = vine(n, (r >> 8) % 2 == 0)
    xc = 2 + (r >> 16) % (n - 2)
    H = []
    L = 16 + (r >> 24) % 16
    for i in range(L):
        rr = Rng(("mg%d" % s).encode(), tag + b"h%d" % i)
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
    step("MG-00", "migration-adversary vs co-location")
    TP = ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "mig.json"
    best = None
    evals = 0
    holders = []
    BUDGET = 5000
    for s in range(100):
        n, T0, H = gen_seed(s, b"mg")
        v = eval_hist(n, T0, H)
        evals += 1
        if v is None:
            continue
        if v[0] == "KILL":
            step("MG-KILL", "HALL seed %d shortfall=%d" % (s, v[1]))
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json").write_text(
                json.dumps({"kill": True, "n": n, "H": H}, indent=1, default=str), encoding="utf-8")
            return 2
        _, nb, worst = v
        holders.append((T0, H, n))
        if worst is not None and (best is None or (worst[0], -worst[1]) < (best[0], -best[1])):
            best = worst
            step("MG-NEW", "seed %d coloc=%.3f split=%d eB=%d acc=%d" % (s, *worst))
    holders = holders[-14:]
    step("MG-01", "seeds evals=%d best=%s" % (evals, best))
    it = 0
    while evals < BUDGET:
        it += 1
        r = int.from_bytes(_h.sha256(b"mgm|%d" % it).digest(), "big")
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
            step("MG-KILL", "HALL it=%d shortfall=%d" % (it, v[1]))
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json").write_text(
                json.dumps({"kill": True, "n": n, "H": H2}, indent=1, default=str), encoding="utf-8")
            return 2
        _, nb, worst = v
        if worst is not None and (best is None or (worst[0], -worst[1]) < (best[0], -best[1])):
            best = worst
            step("MG-NEW", "it=%d coloc=%.3f split=%d eB=%d acc=%d" % (it, *worst))
            holders.append((T0, H2, n))
            holders = holders[-14:]
        elif (r >> 6) % 4 == 0:
            holders.append((T0, H2, n))
            holders = holders[-14:]
        if it % 1200 == 0:
            step("MG-02", "it=%d evals=%d best=%s" % (it, evals, best))
    step("MG-03", "evals=%d best=%s NO KILL" % (evals, best))
    TP.write_text(json.dumps({"evals": evals, "best": best, "nokill": True}, indent=1, default=str),
                  encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

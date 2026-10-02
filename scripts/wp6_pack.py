"""WP-6 PACK: root-packing-miss + split kill assembler (C103).

Novel objective (never directly optimized): minimize root-area triple overlap
(past final-A-triples vs burst-top-B-triple) WHILE maximizing A/B split AND
keeping victim region fresh. If packing-miss + split + sterile assembles yet
saturates => wall = mid-chain-hits (8Z), root-anchor demoted to finite face.
If shortfall>0 => GC-STATIC KILLED (hallkill + exit 2).
Artifact: pack.json (+hallkill on kill). Sealed files untouched.
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
from solver import encode as E


def step(sid, msg):
    print("[WP-6][PACK %s] %s" % (sid, msg), flush=True)


import hashlib as _h
from collections import defaultdict


def pack_metrics(n, T0, H):
    """Per KEEP burst: (split, rootmiss, eB). rootmiss = 1 - |overlap|/|btop|.
    Returns worst (min overlap, max split) + eval or None."""
    pre = E.precompute(n, T0, H)
    res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
    if res["violations"]:
        return None
    A, B = to_ptr(T0), to_ptr(T0)
    # replay tracking final-A-triples (rotated sets of last StepEv per access)
    # and B-top-triples (pushed of last B-StepEv + x). Approximate via splay_A/B
    # invs/pushes last elements.
    from wp6_eventflow import splay_B_push as sbp
    Aroottrips = []
    best = None
    for idx, acc in enumerate(pre):
        A, invs = splay_A(A, acc["x"])
        if invs:
            Aroottrips.append(set(invs[-1]))
        if acc["mode"] == "KEEP":
            B, pushes = sbp(B, acc["x"])
            da = pre[idx]["a"] - 1
            db = pre[idx]["y"] - 1 if pre[idx]["y"] else 0
            # need B-top pushed: pushes[-1] if any
            btop = set(pushes[-1]) | {acc["x"]} if pushes else {acc["x"]}
            ov = 0
            for S in Aroottrips:
                if S & btop:
                    ov += 1
                    break
            # rootmiss proxy: 0 overlap => 1 else 0; score = split - 50*overlap
            eB = len(acc["Bev"])
            eA = sum(1 for z in acc["sites"] if z)
            split = eB - 3 * eA
            score = (split, -ov, eB)
            if best is None or (split > best[0] or (split == best[0] and ov < best[1])):
                best = (split, ov, eB, idx, acc["x"])
    return best


def eval_hist(n, T0, H):
    G = build_graph(n, T0, H)
    if G is None:
        return None
    f, nb, _ = maxflow_cap3(G)
    if nb - f > 0:
        return ("KILL", nb - f, nb)
    pm = pack_metrics(n, T0, H)
    if pm is None:
        return None
    return ("OK", nb, pm)


def gen_seed(s, tag):
    rng = Rng(("pk%d" % s).encode(), tag)
    r = rng(0)
    n = [64, 128][r % 2]
    T0 = vine(n, (r >> 8) % 2 == 0)
    xc = n - (2 + (r >> 16) % 12)
    H = []
    L = 16 + (r >> 24) % 16
    for i in range(L):
        rr = Rng(("pk%d" % s).encode(), tag + b"h%d" % i)
        q = rr(1000 + i)
        op = (q >> 2) % 10
        if op < 4:
            H.append(["DELETE", 1 + (q >> 9) % max(1, n - 20)])
        elif op < 7:
            z = min(n, max(1, xc + [-4, -3, -2, -1, 1, 2, 3, 4][(q >> 9) % 8]))
            H.append(["KEEP", z])
        else:
            H.append(["KEEP", xc])
    for _ in range(2 + (r >> 20) % 2):
        H.append(["KEEP", xc])
    return n, T0, H


def main() -> int:
    import json
    step("PK-00", "root-packing-miss + split assembler")
    TP = ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "pack.json"
    best = None
    evals = 0
    holders = []
    BUDGET = 6000
    for s in range(120):
        n, T0, H = gen_seed(s, b"pk")
        v = eval_hist(n, T0, H)
        evals += 1
        if v is None:
            continue
        if v[0] == "KILL":
            step("PK-KILL", "HALL seed %d shortfall=%d" % (s, v[1]))
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json").write_text(
                json.dumps({"kill": True, "n": n, "H": H}, indent=1, default=str), encoding="utf-8")
            return 2
        _, nb, pm = v
        holders.append((T0, H, n))
        key = (pm[0], -pm[1])
        if best is None or key > (best[0], -best[1]):
            best = pm
            step("PK-NEW", "seed %d split=%d overlap=%d eB=%d acc=%d x=%d" % (s, *pm))
    holders = holders[-14:]
    step("PK-01", "seeds evals=%d best=%s" % (evals, best))
    it = 0
    while evals < BUDGET:
        it += 1
        r = int.from_bytes(_h.sha256(b"pkm|%d" % it).digest(), "big")
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
            step("PK-KILL", "HALL it=%d shortfall=%d H=%s" % (it, v[1], H2))
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json").write_text(
                json.dumps({"kill": True, "n": n, "H": H2}, indent=1, default=str), encoding="utf-8")
            return 2
        _, nb, pm = v
        key = (pm[0], -pm[1])
        if best is None or key > (best[0], -best[1]):
            best = pm
            step("PK-NEW", "it=%d split=%d overlap=%d eB=%d acc=%d x=%d" % (it, *pm))
            holders.append((T0, H2, n))
            holders = holders[-14:]
        elif (r >> 6) % 4 == 0:
            holders.append((T0, H2, n))
            holders = holders[-14:]
        if it % 1500 == 0:
            step("PK-02", "it=%d evals=%d best=%s" % (it, evals, best))
    step("PK-03", "evals=%d best=%s NO KILL" % (evals, best))
    TP.write_text(json.dumps({"evals": evals, "best": best, "nokill": True}, indent=1, default=str),
                  encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""WP-6 YIELD: bystander yield bound + anchored-only assignment test (C60).

8V(a): each KEEP pusher re-deepens bystander x by few levels (claim <=2-3).
  Measure Delta-depth_B(x) per KEEP z!=x over corpus: distribution + max.
8V(b) contention: maxflow restricted to ANCHORED edges (E1+E4+K) vs full
  (E1+E2+E3+E4+E7). anchored-shortfall=0  => transients bonus, contention moot,
  cycle-closure viable. anchored-shortfall>0 => transients load-bearing
  (variation needed); persist worst instances.
Artifact: yield.json. Sealed files untouched.
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_eventflow_abl import build_tagged
from wp6_eventflow import Dinic, to_ptr, splay_A, splay_B_push
from wp6_tightest import vine, Rng
from solver import encode as E


def step(sid, msg):
    print("[WP-6][YIELD %s] %s" % (sid, msg), flush=True)


from collections import Counter


def depth(t, x):
    d = 0
    # to_ptr trees: dict nodes with l/r/p/k
    cur = None
    # find x
    stack = [t]
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
        return None
    while node["p"] is not None:
        node = node["p"]
        d += 1
    return d


def main() -> int:
    import json
    step("YI-00", "bystander yield + anchored-only assignment")
    ydist = Counter()
    ymax = 0
    ymaxex = None
    anch_fail = 0
    anch_worst = None
    evals = 0
    cfgs = [(b"yi1", [16, 32], 10, 24), (b"yi2", [64, 128], 12, 28)]
    for tag, nset, Llo, Lhi in cfgs:
        for t in range(70):
            rng = Rng(("y%d" % t).encode(), tag)
            r = rng(0)
            n = nset[r % len(nset)]
            T0 = vine(n, (r >> 8) % 2 == 0)
            L = Llo + (r >> 16) % (Lhi - Llo + 1)
            x = 1 + (r >> 24) % n
            H = []
            for i in range(L):
                rr = Rng(("y%d" % t).encode(), tag + b"h%d" % i)
                q = rr(1000 + i)
                if i % 5 == 4:
                    y = min(n, max(1, x + [-32, -16, 16, 32][q % 4]))
                    H.append(["DELETE", y if y != x else 1])
                    H.append(["KEEP", x])
                else:
                    H.append(["KEEP" if q % 3 else "DELETE", x])
                x = min(n, max(1, x + [-16, -8, -4, -1, 1, 4, 8, 16][(q >> 9) % 8]))
            pre = E.precompute(n, T0, H)
            res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
            if res["violations"]:
                continue
            evals += 1
            # (a) bystander yields: replay B, per KEEP z measure max depth-gain of other keys
            B = to_ptr(T0)
            A = to_ptr(T0)
            for acc in pre:
                if acc["mode"] == "KEEP":
                    before = {}
                    # sample tracked keys: all keys 1..n is O(n) per access; n<=128 ok
                    for k in range(1, n + 1):
                        before[k] = depth(B, k)
                    A, _ = splay_A(A, acc["x"])
                    B, _ = splay_B_push(B, acc["x"])
                    for k in range(1, n + 1):
                        if k == acc["x"]:
                            continue
                        a, b = before[k], depth(B, k)
                        if a is not None and b is not None and b > a:
                            g = b - a
                            ydist[g] += 1
                            if g > ymax:
                                ymax = g
                                ymaxex = (n, acc["x"], k, a, b)
                else:
                    A, _ = splay_A(A, acc["x"])
            # (b) anchored-only maxflow (E1+E4+K edges only)
            g = build_tagged(n, T0, H)
            Aevs, Bevs, elig = g["Aevs"], g["Bevs"], g["elig"]
            na, nb = len(Aevs), len(Bevs)
            if nb == 0:
                continue
            # need Arot for K: rebuild
            A2 = to_ptr(T0)
            B2 = to_ptr(T0)
            Arot = {}
            acc_of = {}
            aid = 0
            for idx, acc in enumerate(g["pre"]):
                A2, invs = splay_A(A2, acc["x"])
                for (S, sited) in zip(invs, acc["sites"]):
                    Arot[aid] = frozenset(S)
                    acc_of[aid] = idx
                    aid += 1
                if acc["mode"] == "KEEP":
                    B2, _ = splay_B_push(B2, acc["x"])
            N = 2 + na + nb
            S, T = 0, N - 1
            D = Dinic(N)
            for i, (_, sited) in enumerate(Aevs):
                if sited:
                    D.add(S, 1 + i, 3)
            for j in range(nb):
                D.add(1 + na + j, T, 1)
            for j, e in enumerate(elig):
                xx = g["pre"][Bevs[j][0]]["x"]
                accb = Bevs[j][0]
                allow = set(e["E1"]) | set(e["E4"])
                for i in e["E3"]:
                    Sset = Arot.get(i, frozenset())
                    if xx in Sset and acc_of.get(i, accb) < accb and Aevs[i][1]:
                        allow.add(i)
                for i in allow:
                    if Aevs[i][1]:
                        D.add(1 + i, 1 + na + j, 1)
            f, _ = D.flow(S, T)
            if nb - f > 0:
                anch_fail += 1
                if anch_worst is None or (nb - f) > anch_worst[0]:
                    anch_worst = (nb - f, nb, n)
    step("YI-01", "evals=%d yield_dist=%s max=%d %s" % (evals, dict(sorted(ydist.items())), ymax, ymaxex))
    step("YI-02", "anchored-only fail=%d/%d worst=%s" % (anch_fail, evals, anch_worst))
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "yield.json").write_text(
        json.dumps({"evals": evals, "yield": dict(sorted(ydist.items())), "ymax": ymax,
                    "ymaxex": ymaxex, "anch_fail": anch_fail, "anch_worst": anch_worst},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

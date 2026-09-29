"""WP-6 STEP EO-00: E3 ordered-family law (nested/expanding/sliding?).

For each B-splay (KEEP), for B-StepEvs b_1..b_k in execution order with
triples T_1..T_k: E3(b_j) = past A-StepEvs with rotated-set INTERSECT T_j.
Measure per j: |E3|, new members vs b_{j-1} (entered), lost members
(left), nested? (E3_j subset E3_{j+1} or reverse?), savior order (which
member least-loaded picks per j: monotone in aev id?).
Also E3-member reuse counts (loads from E3-claims) + triple-key drift
(keys entering/leaving triples along the path).
Verdict: nested / expanding / sliding / other exact law, or none.
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_eventflow import to_ptr, splay_A, splay_B_push
from liquidity import legacy_embedding as PE
from solver import encode as E


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


def main() -> int:
    # WP-6 STEP EO-00.
    step("EO-00", "E3 ordered-family law")
    import hashlib

    class DRBG:
        def __init__(self, s): self.s = s; self.c = 0

        def b(self):
            self.c += 1
            return hashlib.sha256(b"eo|%s|%d" % (self.s, self.c)).digest()

        def below(self, n):
            bound = (1 << 256) - ((1 << 256) % n)
            while True:
                v = int.from_bytes(self.b(), "big")
                if v < bound:
                    return v % n

        def ir(self, a, b): return a + self.below(b - a + 1)

        def ch(self, s): return s[self.below(len(s))]

    def vine(n, left=False):
        t = None
        for k in (range(n, 0, -1) if not left else range(1, n + 1)):
            t = [k, None, t] if not left else [k, t, None]
        return t

    # per-B-StepEv E3 needs per-StepEv triples: replay B-splay capturing
    # pushed sets + node keys per step.
    def bsteps(B, x):
        d, path = PE._depth_to(B, x)
        if not path or path[-1]["k"] != x:
            return B, []
        out = []
        node = path[-1]
        while node["p"] is not None:
            p = node["p"]
            g = p["p"]
            if g is None:
                if p["l"] is node:
                    PE._rot_right(p)
                else:
                    PE._rot_left(p)
                out.append((frozenset((node["k"], p["k"])), node["k"]))
            elif p["l"] is node and g["l"] is p:
                PE._rot_right(g)
                PE._rot_right(p)
                out.append((frozenset((node["k"], p["k"], g["k"])), node["k"]))
            elif p["r"] is node and g["r"] is p:
                PE._rot_left(g)
                PE._rot_left(p)
                out.append((frozenset((node["k"], p["k"], g["k"])), node["k"]))
            elif p["r"] is node and g["l"] is p:
                PE._rot_left(p)
                PE._rot_right(g)
                out.append((frozenset((node["k"], p["k"], g["k"])), node["k"]))
            else:
                PE._rot_right(p)
                PE._rot_left(g)
                out.append((frozenset((node["k"], p["k"], g["k"])), node["k"]))
        while node["p"] is not None:
            node = node["p"]
        return node, out

    def arot_sets(A, x):
        d, path = PE._depth_to(A, x)
        if not path or path[-1]["k"] != x:
            return A, []
        out = []
        node = path[-1]
        while node["p"] is not None:
            p = node["p"]
            g = p["p"]
            if g is None:
                if p["l"] is node:
                    PE._rot_right(p)
                else:
                    PE._rot_left(p)
                out.append(frozenset((node["k"], p["k"])))
            elif p["l"] is node and g["l"] is p:
                PE._rot_right(g)
                PE._rot_right(p)
                out.append(frozenset((node["k"], p["k"], g["k"])))
            elif p["r"] is node and g["r"] is p:
                PE._rot_left(g)
                PE._rot_left(p)
                out.append(frozenset((node["k"], p["k"], g["k"])))
            elif p["r"] is node and g["l"] is p:
                PE._rot_left(p)
                PE._rot_right(g)
                out.append(frozenset((node["k"], p["k"], g["k"])))
            else:
                PE._rot_right(p)
                PE._rot_left(g)
                out.append(frozenset((node["k"], p["k"], g["k"])))
        while node["p"] is not None:
            node = node["p"]
        return node, out

    nest = {"sub": 0, "super": 0, "incomp": 0, "equal": 0}
    new_tot = 0
    lost_tot = 0
    sav_mono = 0
    sav_tot = 0
    reuse = {}
    n_splay = 0
    for t in range(80):
        rng = DRBG(("eo%d" % t).encode())
        n = rng.ch([32, 64])
        T0 = vine(n, rng.below(2) == 0)
        L = rng.ir(6, 18)
        x = rng.ir(1, n)
        H = []
        for i in range(L):
            if i % 4 == 3:
                y = rng.ir(1, n)
                H.append(["DELETE", y if y != x else 1])
                H.append(["KEEP", x])
            else:
                H.append([rng.ch(["KEEP", "DELETE", "DELETE", "KEEP"]), x])
            x = min(n, max(1, x + rng.ch([-16, -8, -4, -1, 1, 4, 8, 16])))
        pre = E.precompute(n, T0, H)
        res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
        if res["violations"]:
            step("EO-KILL", "present kill t=%d" % t)
            return 2
        A, B = to_ptr(T0), to_ptr(T0)
        alog = []  # (aev global id, frozenset)
        gid = 0
        for acc in pre:
            mode, xx = acc["mode"], acc["x"]
            A, invs = arot_sets(A, xx)
            for S in invs:
                alog.append((gid, S))
                gid += 1
            if mode == "KEEP":
                B, bsteps_list = bsteps(B, xx)
                if len(bsteps_list) >= 2:
                    n_splay += 1
                    prevE = None
                    prevsav = None
                    for (T, _) in bsteps_list:
                        E3 = set(gi for (gi, S) in alog if not S.isdisjoint(T))
                        if prevE is not None:
                            if E3 == prevE:
                                nest["equal"] += 1
                            elif E3 < prevE:
                                nest["sub"] += 1
                            elif E3 > prevE:
                                nest["super"] += 1
                            else:
                                nest["incomp"] += 1
                            new_tot += len(E3 - prevE)
                            lost_tot += len(prevE - E3)
                        # savior order: least-loaded pick among E3 (load tracked
                        # globally would need allocator; use canonical first)
                        prevE = E3
    step("EO-01", "splays=%d nest=%s new/step=%.2f lost/step=%.2f" %
         (n_splay, nest, new_tot / max(1, sum(nest.values())),
          lost_tot / max(1, sum(nest.values()))))
    import json
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "e3order.json").write_text(
        json.dumps({"splays": n_splay, "nest": nest}, indent=1, sort_keys=True,
                   default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

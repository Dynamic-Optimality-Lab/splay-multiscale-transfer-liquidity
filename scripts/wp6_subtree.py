"""WP-6 STEP ST-00: subtree-token presence screen (history-sensitive certificate).

Counters c_v (init 0). A-StepEv (sited) with rotated set S: c_v += 2 for v in S
(<=6 income-exact-ish: |S|<=3 structural). KEEP x: T = pre-splay B-subtree(x);
PRESENCE: sum_{v in T} c_v >= need(x). Then SPEND: c_v := 0 for v in T.
If presence holds at every KEEP: stock follows (created<=6*S_A, spent=needs).
Presence failure kills the LEMMA (sufficient-only), minimized witness kept.
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from liquidity import legacy_embedding as PE
from solver import encode as E


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


def to_ptr(t):
    if t is None:
        return None
    root = PE.mknode(t[0])
    stack = [(t, root)]
    while stack:
        src, dst = stack.pop()
        if src[1] is not None:
            nd = PE.mknode(src[1][0])
            nd["p"] = dst
            dst["l"] = nd
            stack.append((src[1], nd))
        if src[2] is not None:
            nd = PE.mknode(src[2][0])
            nd["p"] = dst
            dst["r"] = nd
            stack.append((src[2], nd))
    return root


def find(t, x):
    cur = t
    while cur is not None and cur["k"] != x:
        cur = cur["l"] if x < cur["k"] else cur["r"]
    return cur


def subtree_keys(u):
    out = []
    stack = [u]
    while stack:
        w = stack.pop()
        if w is None:
            continue
        out.append(w["k"])
        stack.append(w["l"])
        stack.append(w["r"])
    return out


def splay_involve(t, x):
    d, path = PE._depth_to(t, x)
    if not path or path[-1]["k"] != x:
        return t, []
    inv = []
    node = path[-1]
    while node["p"] is not None:
        p = node["p"]
        g = p["p"]
        if g is None:
            if p["l"] is node:
                PE._rot_right(p)
            else:
                PE._rot_left(p)
            inv.append({node["k"], p["k"]})
        elif p["l"] is node and g["l"] is p:
            PE._rot_right(g)
            PE._rot_right(p)
            inv.append({node["k"], p["k"], g["k"]})
        elif p["r"] is node and g["r"] is p:
            PE._rot_left(g)
            PE._rot_left(p)
            inv.append({node["k"], p["k"], g["k"]})
        elif p["r"] is node and g["l"] is p:
            PE._rot_left(p)
            PE._rot_right(g)
            inv.append({node["k"], p["k"], g["k"]})
        else:
            PE._rot_right(p)
            PE._rot_left(g)
            inv.append({node["k"], p["k"], g["k"]})
    while node["p"] is not None:
        node = node["p"]
    return node, inv


def main() -> int:
    # WP-6 STEP ST-00: subtree-token presence screen.
    step("ST-00", "Subtree-token presence screen")
    import hashlib

    class DRBG:
        def __init__(self, s): self.s = s; self.c = 0

        def b(self):
            self.c += 1
            return hashlib.sha256(b"st|%s|%d" % (self.s, self.c)).digest()

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

    worst = -10**18
    ex = None
    n_hist = 0
    n_keeps = 0
    created = 0
    tokSA = 0
    for t in range(500):
        rng = DRBG(("st%d" % t).encode())
        n = rng.ch([16, 32, 64])
        T0 = vine(n, rng.below(2) == 0)
        L = rng.ir(4, 18)
        x = rng.ir(1, n)
        H = []
        for i in range(L):
            if i % 4 == 3:
                y = rng.ir(1, n)
                H.append(["DELETE", y if y != x else (1 if x != 1 else n)])
            else:
                H.append([rng.ch(["KEEP", "DELETE", "DELETE", "KEEP"]), x])
            x = min(n, max(1, x + rng.ch([-16, -8, -4, -1, 1, 4, 8, 16])))
        pre = E.precompute(n, T0, H)
        res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
        if res["violations"]:
            step("ST-KILL", "present kill t=%d (refutes MSTL-14P!)" % t)
            return 2
        kps = list(res["keeps"])
        A, B = to_ptr(T0), to_ptr(T0)
        c = {}
        ki = 0
        for acc in pre:
            mode, xx = acc["mode"], acc["x"]
            if mode == "KEEP":
                nd = kps[ki]["need"]
                ki += 1
                n_keeps += 1
                u = find(B, xx)
                T = subtree_keys(u)
                avail = sum(c.get(v, 0) for v in T)
                gap = nd - avail
                if gap > worst:
                    worst, ex = gap, (t, xx, nd, avail, len(T))
                for v in T:
                    c[v] = 0
            A, invs = splay_involve(A, xx)
            if len(invs) != len(acc["Aev"]):
                step("ST-FAIL", "trace mismatch t=%d" % t)
                return 2
            for S, sited in zip(invs, acc["sites"]):
                if sited:
                    tokSA += 1
                    for v in S:
                        c[v] = c.get(v, 0) + 2
                        created += 2
            if mode == "KEEP":
                B, _ = PE.splay_trace(B, xx)
    step("ST-01", "hist=500 keeps=%d created=%d sited-ev=%d worst presence gap=%s %s (want<=0)"
         % (n_keeps, created, tokSA, worst, ex))
    import json
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "subtree_presence.json").write_text(
        json.dumps({"histories": 500, "keeps": n_keeps, "created": created,
                    "sited_events": tokSA, "worst_gap": worst, "ex": ex},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

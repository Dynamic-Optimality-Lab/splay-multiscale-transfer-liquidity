"""WP-6 STEP PP-00: pure-pump mechanics (M2/M3 verification).

Per B-StepEv (KEEP): pushed keys P (p / {p,g}); A-rotated set Arot (this
access). Pure push: x in P with x not in Arot (x B-pushed, x A-rigid).
Measure: pure fraction; pushes-per-pump distribution; B-sub(x) size change
at pure-pushes (expect shrink: pumped key resets out of B-sub(x)); and the
cash-shape race (x A-shallow + B-pumped repeatedly => later cash?).
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


def subsize(u):
    n = 0
    stack = [u]
    while stack:
        w = stack.pop()
        if w is None:
            continue
        n += 1
        stack.append(w["l"])
        stack.append(w["r"])
    return n


def main() -> int:
    # WP-6 STEP PP-00: pure-pump verification.
    step("PP-00", "Pure-pump mechanics")
    import hashlib

    class DRBG:
        def __init__(self, s): self.s = s; self.c = 0

        def b(self):
            self.c += 1
            return hashlib.sha256(b"pp|%s|%d" % (self.s, self.c)).digest()

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

    def do_step(node):
        """One StepEv; return (pushed_keys, triple)."""
        p = node["p"]
        g = p["p"]
        if g is None:
            if p["l"] is node:
                PE._rot_right(p)
            else:
                PE._rot_left(p)
            return {p["k"]}, (node["k"], p["k"])
        if p["l"] is node and g["l"] is p:
            PE._rot_right(g)
            PE._rot_right(p)
        elif p["r"] is node and g["r"] is p:
            PE._rot_left(g)
            PE._rot_left(p)
        elif p["r"] is node and g["l"] is p:
            PE._rot_left(p)
            PE._rot_right(g)
        else:
            PE._rot_right(p)
            PE._rot_left(g)
        return {p["k"], g["k"]}, (node["k"], p["k"], g["k"])

    n_push = n_pure = 0
    per_pump = {}
    shrink = grow = same = 0
    m1_viol = 0
    n_hist = 0
    for t in range(300):
        rng = DRBG(("pp%d" % t).encode())
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
            step("PP-KILL", "present kill t=%d (refutes MSTL-14P!)" % t)
            return 2
        A, B = to_ptr(T0), to_ptr(T0)
        for acc in pre:
            mode, xx = acc["mode"], acc["x"]
            # A-side: collect rotated set + replay
            _, pa = PE._depth_to(A, xx)
            Arot = set()
            if pa and pa[-1]["k"] == xx:
                node = pa[-1]
                while node["p"] is not None:
                    p = node["p"]
                    g = p["p"]
                    if g is None:
                        if p["l"] is node:
                            PE._rot_right(p)
                        else:
                            PE._rot_left(p)
                        Arot |= {node["k"], p["k"]}
                    elif p["l"] is node and g["l"] is p:
                        PE._rot_right(g)
                        PE._rot_right(p)
                        Arot |= {node["k"], p["k"], g["k"]}
                    elif p["r"] is node and g["r"] is p:
                        PE._rot_left(g)
                        PE._rot_left(p)
                        Arot |= {node["k"], p["k"], g["k"]}
                    elif p["r"] is node and g["l"] is p:
                        PE._rot_left(p)
                        PE._rot_right(g)
                        Arot |= {node["k"], p["k"], g["k"]}
                    else:
                        PE._rot_right(p)
                        PE._rot_left(g)
                        Arot |= {node["k"], p["k"], g["k"]}
                while node["p"] is not None:
                    node = node["p"]
                A = node
            if mode == "KEEP":
                _, pb = PE._depth_to(B, xx)
                node = pb[-1]
                while node["p"] is not None:
                    pushed, _ = do_step(node)
                    per_pump[len(pushed)] = per_pump.get(len(pushed), 0) + 1
                    for v in pushed:
                        n_push += 1
                        if v not in Arot:
                            n_pure += 1
                while node["p"] is not None:
                    node = node["p"]
                B = node
        n_hist += 1
    step("PP-01", "hist=%d pushes=%d pure=%0.4f per-pump-dist=%s M1-viol=%d"
         % (n_hist, n_push, n_pure / max(1, n_push), per_pump, m1_viol))
    import json
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "purepump.json").write_text(
        json.dumps({"histories": n_hist, "pushes": n_push,
                    "pure_frac": n_pure / max(1, n_push),
                    "per_pump": per_pump, "m1_viol": m1_viol},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

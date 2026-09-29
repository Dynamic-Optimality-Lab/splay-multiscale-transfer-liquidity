"""WP-6 STEP LB-00: path-defect exposure measurement (Lemma B candidacy).

Defect candidates per KEEP x (P_B/P_A = root-to-x ancestor chains):
  F2  = |P_B| - |P_B cap P_A|   (non-shared B-path nodes)
  F2b = max(0, |P_B| - 2*|P_A| + 1)
Check need <= F* (exposure) and measure per-rotation global update magnitude
of Sigma_x F2(x) (sum over all keys) to test O(1)-update vs Theta(n)-swing.
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from solver import encode as E
from liquidity import legacy_embedding as PE


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


def path_to(p, x):
    """Ancestor chain root->x (present key) via parent pointers after locating."""
    cur = p
    while cur is not None and cur["k"] != x:
        # find root first if p not root
        break
    r = p
    while r["p"] is not None:
        r = r["p"]
    # descend BST to x collecting path
    chain = []
    cur = r
    while cur is not None:
        chain.append(cur["k"])
        if x == cur["k"]:
            return chain
        cur = cur["l"] if x < cur["k"] else cur["r"]
    raise ValueError("absent in path_to")


def all_keys(p):
    if p is None:
        return set()
    r = p
    while r["p"] is not None:
        r = r["p"]
    out = set()

    def rec(u):
        if u is None:
            return
        out.add(u["k"])
        rec(u["l"])
        rec(u["r"])

    rec(r)
    return out


def F2_of(A, B, x):
    pb, pa = set(path_to(B, x)), set(path_to(A, x))
    return len(pb) - len(pb & pa)


def total_F2(A, B):
    tot = 0
    for x in all_keys(A):
        pb, pa = set(path_to(B, x)), set(path_to(A, x))
        tot += len(pb) - len(pb & pa)
    return tot


def main() -> int:
    # WP-6 STEP LB-00: exposure + update-magnitude measurement.
    step("LB-00", "Path-defect exposure and update magnitude")
    import hashlib

    class DRBG:
        def __init__(self, s): self.s = s; self.c = 0

        def b(self):
            self.c += 1
            return hashlib.sha256(b"lb|%s|%d" % (self.s, self.c)).digest()

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

    viol = totk = 0
    maxswing = 0
    worst = None
    for t in range(300):
        rng = DRBG(("lb%d" % t).encode())
        n = 32
        T0 = vine(n, rng.below(2) == 0)
        L = rng.ir(2, 10)
        x = rng.ir(1, n)
        H = []
        for _ in range(L):
            H.append([rng.ch(["KEEP", "DELETE"]), x])
            x = min(n, max(1, x + [-16, -8, -4, -1, 1, 4, 8, 16][rng.below(8)]))
        # fix H modes (ch missing above on purpose? no: add ch)
        pre = E.precompute(n, T0, H)
        res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
        kps = iter(res["keeps"])
        A, B = to_ptr(T0), to_ptr(T0)
        Fpre = total_F2(A, B)
        for acc in pre:
            if acc["mode"] == "KEEP":
                kp = next(kps)
                # WP-6 STEP LB-00b: defect evaluated PRE-access (need's depths).
                preF2 = F2_of(A, B, acc["x"])
                totk += 1
                if kp["need"] > preF2:
                    viol += 1
                    if viol <= 3:
                        step("LB-KILL", "need exceeds pre-F2 t=%d need=%d F2=%d"
                             % (t, kp["need"], preF2))
            A, _ = PE.splay_trace(A, acc["x"])
            if acc["mode"] == "KEEP":
                B, _ = PE.splay_trace(B, acc["x"])
            Fpost = total_F2(A, B)
            Fpost = total_F2(A, B)
            maxswing = max(maxswing, abs(Fpost - Fpre))
            if abs(Fpost - Fpre) > (worst[0] if worst else -1):
                worst = (abs(Fpost - Fpre), t, acc["mode"], acc["x"])
            Fpre = Fpost
    step("LB-01", "keeps=%d exposure-viol=%d maxswing/access=%d worst=%s"
         % (totk, viol, maxswing, worst))
    import json
    p = ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "lemmaB_pathdefect.json"
    p.write_text(json.dumps({"keeps": totk, "exposure_violations": viol,
                             "max_swing_per_access": maxswing, "worst": worst},
                            indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

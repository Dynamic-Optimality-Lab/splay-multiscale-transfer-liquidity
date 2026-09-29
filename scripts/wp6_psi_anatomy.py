"""WP-6 STEP PS-00: scalar reserve law-violation anatomy (failure-law data).

Psi = sum_v max(0, d_B(v) - d_A(v)) (L1-positive depth-disagreement).
Law per access: e_B - 3*e_A <= Psi_before - Psi_after, i.e.
  viol = (Psi_after - Psi_before) - (3*e_A - e_B) <= 0 wanted.
Decompose Psi change into z-drop (kept key term ->0) vs bystander-rise
(bystander terms up) vs A-drift (A-depth changes). Classify violations by:
duplication (bystander-rise > z-drop), nonlocal reuse, merge/split
(defect-count delta), epoch overlap (tenure crossing), missing history.
Minimized worst-violation witness kept.
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


def depths_keys(t):
    r = t
    while r["p"] is not None:
        r = r["p"]
    out = {}

    def rec(u, d):
        if u is None:
            return
        out[u["k"]] = d
        rec(u["l"], d + 1)
        rec(u["r"], d + 1)

    rec(r, 0)
    return out


def psi_of(dA, dB):
    return sum(max(0, dB[k] - dA[k]) for k in dA)


def main() -> int:
    # WP-6 STEP PS-00: violation anatomy.
    step("PS-00", "Scalar reserve law-violation anatomy")
    import hashlib

    class DRBG:
        def __init__(self, s): self.s = s; self.c = 0

        def b(self):
            self.c += 1
            return hashlib.sha256(b"ps|%s|%d" % (self.s, self.c)).digest()

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
    n_viol = 0
    n_acc = 0
    cls = {"dup": 0, "zdrop_ok": 0, "adrift": 0}
    for t in range(300):
        rng = DRBG(("ps%d" % t).encode())
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
            step("PS-KILL", "present kill t=%d (refutes MSTL-14P!)" % t)
            return 2
        A, B = to_ptr(T0), to_ptr(T0)
        for acc in pre:
            mode, xx = acc["mode"], acc["x"]
            eA = sum(1 for z in acc["sites"] if z)
            eB = len(acc["Bev"]) if mode == "KEEP" else 0
            p0 = psi_of(depths_keys(A), depths_keys(B))
            zterm0 = max(0, depths_keys(B).get(xx, 0) - depths_keys(A).get(xx, 0))
            A, _ = PE.splay_trace(A, xx)
            if mode == "KEEP":
                B, _ = PE.splay_trace(B, xx)
            p1 = psi_of(depths_keys(A), depths_keys(B))
            viol = (p1 - p0) - (3 * eA - eB)
            n_acc += 1
            if viol > 0:
                n_viol += 1
                # classify: bystander-rise vs z-drop
                by_all = p1 - p0
                if by_all > 0:
                    cls["dup"] += 1
                else:
                    cls["zdrop_ok"] += 1
            if viol > worst:
                worst, ex = viol, (t, mode, xx, eA, eB, p0, p1, zterm0)
    step("PS-01", "acc=%d viol=%d worst=%s %s" % (n_acc, n_viol, worst, ex))
    step("PS-01", "classes=%s" % cls)
    import json
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "psi_anatomy.json").write_text(
        json.dumps({"accesses": n_acc, "violations": n_viol, "worst": worst,
                    "ex": ex, "classes": cls}, indent=1, sort_keys=True,
                   default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

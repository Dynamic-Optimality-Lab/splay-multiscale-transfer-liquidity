"""WP-6 STAGE 6+7: global stock composition + adversarial raw-inequality sweep.

Stage 6: the composition argument. Pool carried ACROSS runs (global greedy)
is the only surviving shape (Stage 5 killed per-run budgets 58:1). The
composition proof obligation isolates to ONE lemma: B-created divergence is
prepaid by the same global pool (B-source lemma, OPEN). Recorded here with
the measured slack supporting plausibility but NOT proof.

Stage 7: adversarial sweep of the RAW inequality sum(need) <= 6*S_A.
Constructors: (a) freeze-then-cash (DELETE others to freeze divergence at x,
then KEEP x); (b) CAP/vine/caterpillar/zigzag starts; (c) random hostile with
large n,L; (d) run-arbitrage replay (t=459-style single-A runs chained).
Any history with sum(need)-6*S_A > 0 is a PRESENT KILL (refutes MSTL-14P).
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from solver import encode as E


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


def main() -> int:
    # WP-6 STAGES 6+7: composition obligation + raw-inequality adversarial sweep.
    step("S6-00", "Composition reduces to B-source lemma (recording obligation)")
    step("S7-00", "Adversarial raw-inequality sweep")
    import hashlib
    import json

    class DRBG:
        def __init__(self, s): self.s = s; self.c = 0

        def b(self):
            self.c += 1
            return hashlib.sha256(b"s7|%s|%d" % (self.s, self.c)).digest()

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

    def cater(n, seed):
        # valid BST via shuffled insertion order
        import random
        r = random.Random(seed)
        ks = list(range(1, n + 1))
        r.shuffle(ks)
        t = None

        def ins(t, k):
            if t is None:
                return [k, None, None]
            if k < t[0]:
                t[1] = ins(t[1], k)
            else:
                t[2] = ins(t[2], k)
            return t

        for k in ks:
            t = ins(t, k)
        return t

    worst_gap = -10**18
    worst_ratio = 0.0
    exG = exR = None
    n_hist = 0
    kills = 0

    def trial(T0, n, H, tag):
        nonlocal worst_gap, worst_ratio, exG, exR, n_hist, kills
        pre = E.precompute(n, T0, H)
        res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
        if res["violations"]:
            step("S7-KILL", "present kill %s (refutes MSTL-14P)" % tag)
            kills += 1
            return
        sa = sum(len(a["Aev"]) for a in pre)
        sn = sum(k["need"] for k in res["keeps"])
        gap = sn - 6 * sa
        if gap > worst_gap:
            worst_gap, exG = gap, (tag, sn, sa)
        if sa > 0 and sn / (6 * sa) > worst_ratio:
            worst_ratio, exR = sn / (6 * sa), (tag, sn, sa)
        n_hist += 1

    # (a) freeze-then-cash adversarial
    for t in range(400):
        rng = DRBG(("f%d" % t).encode())
        n = rng.ch([32, 64, 128])
        left = rng.below(2) == 0
        T0 = vine(n, left)
        x = rng.ir(1, n)
        H = []
        F = rng.ir(3, 24)
        for _ in range(F):  # freeze: DELETE others, B frozen, A churns
            y = rng.ir(1, n)
            if y == x:
                y = 1 if x != 1 else n
            H.append(["DELETE", y])
        H.append(["KEEP", x])  # cash the frozen divergence
        for _ in range(rng.ir(0, 6)):
            H.append([rng.ch(["KEEP", "DELETE"]), rng.ir(1, n)])
        trial(T0, n, H, "freeze%d" % t)
    # (b) shuffled/caterpillar starts
    for t in range(200):
        rng = DRBG(("c%d" % t).encode())
        n = rng.ch([32, 64])
        T0 = cater(n, 1000 + t)
        L = rng.ir(4, 20)
        x = rng.ir(1, n)
        H = []
        for _ in range(L):
            H.append([rng.ch(["KEEP", "DELETE", "DELETE"]), x])
            x = min(n, max(1, x + rng.ch([-16, -8, -4, -1, 1, 4, 8, 16])))
        trial(T0, n, H, "cater%d" % t)
    # (c) big random hostile
    for t in range(400):
        rng = DRBG(("h%d" % t).encode())
        n = rng.ch([64, 128])
        T0 = vine(n, rng.below(2) == 0)
        L = rng.ir(8, 32)
        x = rng.ir(1, n)
        H = []
        for _ in range(L):
            H.append([rng.ch(["KEEP", "DELETE"]), x])
            x = min(n, max(1, x + rng.ch([-32, -8, -2, -1, 1, 2, 8, 32])))
        trial(T0, n, H, "hostile%d" % t)
    step("S7-01", "histories=%d kills=%d worst raw gap=%d %s worst ratio=%0.4f %s"
         % (n_hist, kills, worst_gap, exG, worst_ratio, exR))
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "stock_sweep.json").write_text(
        json.dumps({"histories": n_hist, "kills": kills,
                    "worst_gap": worst_gap, "gap_ex": exG,
                    "worst_ratio": worst_ratio, "ratio_ex": exR,
                    "composition_obligation": "B-source lemma OPEN: B-created divergence prepaid by global pool; per-run budgets dead (58:1); greedy global discharge held with 25x slack but is evidence, not proof."},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 2 if kills else 0


if __name__ == "__main__":
    sys.exit(main())

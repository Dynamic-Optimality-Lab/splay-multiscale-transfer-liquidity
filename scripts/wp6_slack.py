"""WP-6 STEP SL-00: slack dynamics (why does slack always suffice?).

slack(t) = 3*S_A(t) - E_B(t). Track: global min slack; at each KEEP with
excess X = e_B - 3*e_A > 0: slack-before vs X (tight or loose?); distribution
of slack; #cashes (e_A=0,e_B>0) and their setups. Determines proof strategy:
loose (crude bounds) vs tight (exact mechanism).
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
    # WP-6 STEP SL-00: slack dynamics.
    step("SL-00", "Slack dynamics measurement")
    import hashlib

    class DRBG:
        def __init__(self, s): self.s = s; self.c = 0

        def b(self):
            self.c += 1
            return hashlib.sha256(b"sl|%s|%d" % (self.s, self.c)).digest()

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

    min_slack = 10**18
    min_ex = None
    worst_tight = -1.0  # max over excess-KEEPs of X/slack_before (<=1 safe)
    tight_ex = None
    n_cash = 0
    max_cash_eb = 0
    cash_ex = None
    n_hist = 0
    for t in range(400):
        rng = DRBG(("sl%d" % t).encode())
        n = rng.ch([16, 32, 64, 128])
        T0 = vine(n, rng.below(2) == 0)
        L = rng.ir(4, 24)
        x = rng.ir(1, n)
        H = []
        for i in range(L):
            if i % 5 == 4:
                y = min(n, max(1, x + rng.ch([-32, -16, 16, 32])))
                H.append(["DELETE", y if y != x else (1 if x != 1 else n)])
                H.append(["KEEP", x])
            else:
                H.append([rng.ch(["KEEP", "DELETE", "DELETE"]), x])
            x = min(n, max(1, x + rng.ch([-16, -8, -4, -1, 1, 4, 8, 16])))
        pre = E.precompute(n, T0, H)
        res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
        if res["violations"]:
            step("SL-KILL", "present kill t=%d (refutes MSTL-14P!)" % t)
            return 2
        eb = sa = 0
        for acc in pre:
            eA = sum(1 for z in acc["sites"] if z)
            if acc["mode"] == "KEEP":
                eB = len(acc["Bev"])
                slack_before = 3 * sa - eb
                X = eB - 3 * eA
                if X > 0 and slack_before > 0:
                    r = X / slack_before
                    if r > worst_tight:
                        worst_tight, tight_ex = r, (t, acc["x"], X, slack_before)
                if eA == 0 and eB > 0:
                    n_cash += 1
                    if eB > max_cash_eb:
                        max_cash_eb, cash_ex = eB, (t, acc["x"])
                eb += eB
            sa += eA
            if 3 * sa - eb < min_slack:
                min_slack, min_ex = 3 * sa - eb, (t, acc["mode"], acc["x"])
        n_hist += 1
    step("SL-01", "hist=%d min-slack=%d %s" % (n_hist, min_slack, min_ex))
    step("SL-01", "worst excess/slack-before=%0.4f %s (<=1 always-safe)" % (worst_tight, tight_ex))
    step("SL-01", "cashes=%d max-cash-eB=%d %s" % (n_cash, max_cash_eb, cash_ex))
    import json
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "slack.json").write_text(
        json.dumps({"histories": n_hist, "min_slack": min_slack, "min_ex": min_ex,
                    "worst_tight": worst_tight, "tight_ex": tight_ex,
                    "n_cash": n_cash, "max_cash_eB": max_cash_eb, "cash_ex": cash_ex},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

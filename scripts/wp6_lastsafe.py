"""WP-6 STEP LS-00: last-safe-time cut (interval payment vs cash demand).

For each high-excess KEEP (q=e_B-3*e_A>0) on hostile histories:
u = last access-index of x* before cash (any mode), or -1 (genesis).
Interval (u,t*]: S_A-interval, E_B-interval (payment inside).
q* vs interval-payment (3*S_A_int - E_B_int): suffices (>=q*)?
Outside funding: S_A-pre-u. Backing split: pump-KEEPs pushing x* in
interval vs pre-u (inside/outside pump-backing for x*'s depth).
Determines: interval-sufficient (N-FIRST local!) vs outside-needed
(sharing/circular).
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_eventflow import to_ptr, root_key, splay_A, splay_B_push
from solver import encode as E


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


def main() -> int:
    # WP-6 STEP LS-00.
    step("LS-00", "Last-safe-time cut measurement")
    import hashlib

    class DRBG:
        def __init__(self, s): self.s = s; self.c = 0

        def b(self):
            self.c += 1
            return hashlib.sha256(b"ls|%s|%d" % (self.s, self.c)).digest()

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

    n_suff = n_out = 0
    worst_ratio = -1.0
    exR = None
    in_pump = []
    out_pump = []
    n_cash = 0
    for t in range(200):
        rng = DRBG(("ls%d" % t).encode())
        n = rng.ch([32, 64, 128])
        T0 = vine(n, rng.below(2) == 0)
        L = rng.ir(8, 24)
        x = rng.ir(1, n)
        H = []
        for i in range(L):
            if i % 4 == 3:
                y = min(n, max(1, x + rng.ch([-32, -16, 16, 32])))
                H.append(["DELETE", y if y != x else 1])
                H.append(["KEEP", x])
            else:
                H.append([rng.ch(["KEEP", "DELETE", "DELETE", "KEEP"]), x])
            x = min(n, max(1, x + rng.ch([-32, -16, -8, -4, -1, 1, 4, 8, 16, 32])))
        pre = E.precompute(n, T0, H)
        res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
        if res["violations"]:
            step("LS-KILL", "present kill t=%d" % t)
            return 2
        # last-access per key + prefix sums
        lastacc = {}
        SA_pre = [0]
        EB_pre = [0]
        sa = eb = 0
        for idx, acc in enumerate(pre):
            eA = sum(1 for z in acc["sites"] if z)
            sa += eA
            if acc["mode"] == "KEEP":
                eb += len(acc["Bev"])
            SA_pre.append(sa)
            EB_pre.append(eb)
        for idx, acc in enumerate(pre):
            if acc["mode"] != "KEEP":
                lastacc[acc["x"]] = idx
                continue
            xx = acc["x"]
            eA = sum(1 for z in acc["sites"] if z)
            eB = len(acc["Bev"])
            q = eB - 3 * eA
            if q <= 0:
                lastacc[xx] = idx
                continue
            n_cash += 1
            u = lastacc.get(xx, -1)
            Sint = SA_pre[idx] - SA_pre[u + 1]
            Eint = EB_pre[idx] - EB_pre[u + 1]
            pay = 3 * Sint - Eint
            if pay >= q:
                n_suff += 1
            else:
                n_out += 1
            if Sint + 1 > 0 and q / (pay if pay > 0 else 1) > worst_ratio:
                worst_ratio, exR = q / (pay if pay > 0 else 1), (t, xx, q, pay, Sint, Eint)
            # pump split: track via replay is costly; approximate pump count
            # by B-depth built: use d_B/q relation instead. Record interval
            # length + outside S_A for context.
            in_pump.append(idx - u - 1)
            out_pump.append(SA_pre[u + 1])
            lastacc[xx] = idx
    import statistics as _st
    step("LS-01", "cashes=%d interval-sufficient=%d outside-needed=%d worst q/pay=%.2f %s" %
         (n_cash, n_suff, n_out, worst_ratio, exR))
    step("LS-01", "interval-len med=%s outside-SA med=%s" %
         (_st.median(in_pump) if in_pump else None,
          _st.median(out_pump) if out_pump else None))
    import json
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "lastsafe.json").write_text(
        json.dumps({"cashes": n_cash, "sufficient": n_suff, "outside": n_out,
                    "worst_ratio": worst_ratio, "ex": exR}, indent=1,
                   sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

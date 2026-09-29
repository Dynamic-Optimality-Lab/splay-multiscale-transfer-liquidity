"""WP-6 STAGE 5: DELETE-started a=1 run attack (tenure-need sharp case).

Per-run arbitrage: for each maximal same-key run, compute run_need
(sum of first-KEEP needs... = the single first-KEEP need, later KEEPs have
need 0... actually sum all KEEP needs in run) vs run_A (A-StepEvs in run).
The tenure-need theorem says need fires at first KEEP of a run with a>=1.
Attack: maximize run_need / max(1,run_A) over hostile histories with
DELETE-heavy starts. A sustained ratio > 6 would break any per-run 6-budget;
record the worst ratio + the constructor.
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
    # WP-6 STAGE 5: DELETE-started a=1 run attack.
    step("S5-00", "Per-run need/A-event arbitrage attack")
    import hashlib

    class DRBG:
        def __init__(self, s): self.s = s; self.c = 0

        def b(self):
            self.c += 1
            return hashlib.sha256(b"s5|%s|%d" % (self.s, self.c)).digest()

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

    worst = 0.0
    exW = None
    n_runs = 0
    del_start_worst = 0.0
    exD = None
    for t in range(600):
        rng = DRBG(("s5%d" % t).encode())
        n = rng.ch([16, 32, 64])
        T0 = vine(n, rng.below(2) == 0)
        L = rng.ir(2, 16)
        x = rng.ir(1, n)
        H = []
        for _ in range(L):
            # bias DELETE starts to sharpen the a=1 case
            m = rng.ch(["KEEP", "DELETE", "DELETE", "KEEP", "DELETE"])
            H.append([m, x])
            x = min(n, max(1, x + rng.ch([-16, -8, -4, -1, 1, 4, 8, 16])))
        pre = E.precompute(n, T0, H)
        res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
        if res["violations"]:
            step("S5-KILL", "present kill t=%d" % t)
            return 2
        kps = list(res["keeps"])
        ki = 0
        cur = None
        rn = ra = 0
        rstart = None
        for idx, acc in enumerate(pre):
            if acc["x"] != cur:
                if cur is not None:
                    n_runs += 1
                    r = rn / max(1, ra)
                    if r > worst:
                        worst, exW = r, (t, cur, rn, ra)
                    if rstart == "DELETE" and r > del_start_worst:
                        del_start_worst, exD = r, (t, cur, rn, ra)
                cur = acc["x"]
                rn, ra = 0, 0
                rstart = acc["mode"]
            ra += len(acc["Aev"])
            if acc["mode"] == "KEEP":
                rn += kps[ki]["need"]
                ki += 1
        n_runs += 1
        r = rn / max(1, ra)
        if r > worst:
            worst, exW = r, (t, cur, rn, ra)
        if rstart == "DELETE" and r > del_start_worst:
            del_start_worst, exD = r, (t, cur, rn, ra)
    step("S5-01", "runs=%d worst per-run need/A=%0.4f %s; worst DELETE-started=%0.4f %s"
         % (n_runs, worst, exW, del_start_worst, exD))
    import json
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "run_arbitrage.json").write_text(
        json.dumps({"n_runs": n_runs, "worst_ratio": worst, "worst_ex": exW,
                    "worst_delete_started": del_start_worst, "del_ex": exD},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

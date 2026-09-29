"""WP-6 STEP ST-00: first-minload-2 saturation frame + load-aware turnover.

For every history: chronological least-loaded (E1+E2+E3+E4 tagged, cap 3,
canonical tiebreak). For EVERY B-event record per-class counts AND loads,
entry/exit with load-at-entry/exit, U(b)=sum max(0,3-load), and FIRST
minload>=2 events with full witness (stronger minload<=1 claim kill).
Deep-trace MA-corpus t=5 acc6 (the draining-neighborhood specimen).
NEW artifact: saturation.json (sealed artifacts untouched).
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_eventflow_abl import build_tagged
from solver import encode as E


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


class DRBG:
    def __init__(self, s, tag):
        self.s = s
        self.tag = tag
        self.c = 0

    def b(self):
        self.c += 1
        import hashlib
        return hashlib.sha256(self.tag + b"|%s|%d" % (self.s, self.c)).digest()

    def below(self, n):
        import hashlib
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


def ma_history(t):
    import hashlib
    rng = DRBG(("ma%d" % t).encode(), b"ma")
    n = rng.ch([32, 64])
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
    return n, T0, H


def replay(n, T0, H):
    """Full load-aware replay. Returns per-B-event records + first m2 list."""
    g = build_tagged(n, T0, H)
    Aevs, Bevs, elig = g["Aevs"], g["Bevs"], g["elig"]
    pre = g["pre"]
    load = {}
    seen = set()  # aev ever eligible
    recs = []
    first_m2 = []
    prevN = None
    for j in range(len(Bevs)):
        acc = Bevs[j][0]
        xx = pre[acc]["x"]
        info = {k: sorted(i for i in elig[j][k] if Aevs[i][1])
                for k in ("E1", "E2", "E3", "E4")}
        N = set().union(*info.values())
        lds = {i: load.get(i, 0) for i in N}
        ml = min(lds.values()) if lds else None
        U = sum(max(0, 3 - v) for v in lds.values())
        # entry/exit vs previous B-event
        if prevN is None:
            entered, exited = set(N), set()
        else:
            entered, exited = set(N) - set(prevN), set(prevN) - set(N)
        ent_loads = sorted(load.get(i, 0) for i in entered)
        ext_loads = sorted(load.get(i, 0) for i in exited)
        cls_new = {k: sorted(i for i in info[k] if i in entered) for k in info}
        if ml is not None and ml >= 2 and not first_m2:
            first_m2.append({"bev": j, "acc": acc, "x": xx, "ml": ml,
                             "nanc": len(N),
                             "cls_n": {k: len(info[k]) for k in info},
                             "cls_loads": {k: sorted(load.get(i, 0) for i in info[k])[:16]
                                           for k in info},
                             "U": U})
        rec = {"bev": j, "acc": acc, "x": xx, "ml": ml, "nanc": len(N),
               "cls_n": {k: len(info[k]) for k in info},
               "U": U, "entered": sorted(entered), "exited": sorted(exited),
               "ent_loads": ent_loads, "ext_loads": ext_loads,
               "cls_new": {k: cls_new[k] for k in info}}
        recs.append(rec)
        prevN = N
        if ml is not None and ml < 3:
            cands = sorted((load.get(i, 0), i) for i in N)
            ld, i = cands[0]
            load[i] = ld + 1
    return recs, first_m2, load, g


def main() -> int:
    step("ST-00", "Saturation frame + load-aware turnover")
    import json
    n_m2_hist = 0
    m2_events = []
    deep = None
    lo_new_tot = [0, 0, 0, 0]
    lo_lost_tot = [0, 0, 0, 0]
    nB = 0
    for t in range(100):
        n, T0, H = ma_history(t)
        pre = E.precompute(n, T0, H)
        res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
        if res["violations"]:
            step("ST-KILL", "present kill t=%d" % t)
            return 2
        recs, first_m2, load, g = replay(n, T0, H)
        nB += len(recs)
        for r in recs:
            for v in r["ent_loads"]:
                lo_new_tot[min(v, 3)] += 1
            for v in r["ext_loads"]:
                lo_lost_tot[min(v, 3)] += 1
        if first_m2:
            n_m2_hist += 1
            m2_events.append({"t": t, "ev": first_m2[0]})
        if t == 5:
            # deep trace of acc6 window
            win = [r for r in recs if r["acc"] == 6]
            deep = {"t": t, "n": n, "H": H,
                    "acc6": [{"bev": r["bev"], "x": r["x"], "ml": r["ml"],
                              "nanc": r["nanc"], "cls_n": r["cls_n"], "U": r["U"],
                              "entered": r["entered"], "exited": r["exited"],
                              "ent_loads": r["ent_loads"],
                              "ext_loads": r["ext_loads"]} for r in win]}
    step("ST-01", "B=%d hist_with_m2=%d m2events=%d" % (nB, n_m2_hist, len(m2_events)))
    step("ST-02", "entered loads low0/1/2/sat=%s lost=%s" % (lo_new_tot, lo_lost_tot))
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "saturation.json").write_text(
        json.dumps({"B": nB, "hist_with_m2": n_m2_hist, "m2_events": m2_events,
                    "entered_loads": lo_new_tot, "lost_loads": lo_lost_tot,
                    "deep_t5_acc6": deep}, indent=1, sort_keys=True, default=str),
        encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

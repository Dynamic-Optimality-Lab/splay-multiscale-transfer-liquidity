"""WP-6 STEP MA-00: minload-1 per-event anatomy (REFRESH discovery).

Chronological least-loaded (E1+E2+E3+E4 tagged, cap 3, canonical tiebreak).
For EVERY B-event with pre-assignment minload == 1, record:
  identity (hist, acc_idx, key, bev ordinal), ancestry size,
  per-class eligible sets + loads (E1/E2/E3/E4: counts, load multiset),
  savior (chosen load-1 member: class, age, how it got to load 1),
  load-0 counts before/after previous B-event (depletion),
  last load-0 disappearance (which B consumed it, when, which class),
  new sources since (which accesses added members, which splay exposed),
  overlap of current N(b) with N(b') of raisers (B-events that moved saviors
  0->1): shared ancestors + structural relation (same-access/path/triple/
  root-zone/pump/setup/interval).
Emit extremal specimens (smallest ancestry, oldest savior, deepest setup...).
Goal: exact REFRESH formulation (what replenishes before 1->2 can occur).
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


def main() -> int:
    # WP-6 STEP MA-00.
    step("MA-00", "Minload-1 per-event anatomy")
    import hashlib
    import json

    class DRBG:
        def __init__(self, s): self.s = s; self.c = 0

        def b(self):
            self.c += 1
            return hashlib.sha256(b"ma|%s|%d" % (self.s, self.c)).digest()

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

    specimens = []
    n_m1 = 0
    nB = 0
    for t in range(100):
        rng = DRBG(("ma%d" % t).encode())
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
        pre = E.precompute(n, T0, H)
        res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
        if res["violations"]:
            step("MA-KILL", "present kill t=%d" % t)
            return 2
        g = build_tagged(n, T0, H)
        Aevs, Bevs, elig = g["Aevs"], g["Bevs"], g["elig"]
        load = {}
        raiser = {}  # aev -> bev idx that raised it 0->1
        prev_l0 = None
        for j in range(len(Bevs)):
            nB += 1
            acc = Bevs[j][0]
            xx = pre[acc]["x"]
            info = {k: sorted(i for i in elig[j][k] if Aevs[i][1]) for k in ("E1", "E2", "E3", "E4")}
            lds = {k: sorted(load.get(i, 0) for i in info[k]) for k in info}
            allc = sorted((load.get(i, 0), i) for k in info for i in info[k])
            if not allc:
                continue
            ml = allc[0][0]
            # load-0 depletion tracking
            l0now = sum(1 for (ld, _) in allc if ld == 0)
            if ml == 1:
                n_m1 += 1
                # savior = chosen (least, canonical)
                sv_ld, sv_i = allc[0]
                sv_cls = next(k for k in info if sv_i in info[k])
                # raiser overlap: B-events that moved neighborhood members 0->1
                overl = {}
                for k in info:
                    for i in info[k]:
                        if i in raiser:
                            rj = raiser[i]
                            overl.setdefault(rj, []).append((k, i))
                if len(specimens) < 25:
                    specimens.append({
                        "t": t, "bev": j, "acc": acc, "x": xx,
                        "nanc": len(allc),
                        "cls_n": {k: len(info[k]) for k in info},
                        "cls_loads": {k: lds[k][:12] for k in lds},
                        "savior": [sv_cls, sv_i, Aevs[sv_i][0]],
                        "l0now": l0now, "l0prev": prev_l0,
                        "n_raiser_overlap": len(overl),
                    })
            prev_l0 = l0now
            if ml < 3 and allc:
                ld, i = allc[0]
                if ld == 0:
                    raiser[i] = j
                load[i] = ld + 1
    step("MA-01", "B=%d minload1=%d specimens=%d" % (nB, n_m1, len(specimens)))
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "minload_anat.json").write_text(
        json.dumps({"B": nB, "m1": n_m1, "specimens": specimens},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

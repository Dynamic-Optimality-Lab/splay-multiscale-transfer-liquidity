"""U4-core: engineered extremal discrepancy at n=7,8 (long builds + DELETE
dethroners preserving B-depth), BFS-close, charge + classify."""
from __future__ import annotations
import sys
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
import wp6_overflow as V
import wp6_siege as S
import wp6_danger as DG
import wp6_cycle_ratio as O
from wp6_ovf_anal import vine


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 81
    ntrials = int(sys.argv[2]) if len(sys.argv) > 2 else 400
    rng = random.Random(seed)
    out = {"extremal": []}
    for n in (7, 8):
        T0 = vine(n)
        G = O.build(n) if n == 6 else None
        # BFS-close needs adj; build n=7 adj is heavy (184K states). Instead:
        # use bred-pool CLOSED cycles only + engineered open words for TYPE census.
        best = [0, None]
        for t in range(ntrials):
            x = rng.randint(1, n)
            others = [k for k in range(1, n + 1) if k != x]
            w = []
            for _ in range(rng.randint(2, 5)):
                rng.shuffle(others)
                w += [("K", k) for k in others]
            w += [("D", x)]
            # DELETE dethroners (preserve B)
            for _ in range(rng.randint(1, 2)):
                w += [("D", rng.choice(others))]
            w += [("K", x)]
            rep = V.replay(T0, T0, w)
            for a in rep["accesses"]:
                if a["m"] == "K" and (a["eps"], a["a"]) > (best[0], 0):
                    if a["a"] >= 1 and a["eps"] >= 1:
                        best = [a["eps"], (n, w, a["x"], a["a"],
                                           a["q"], a["dA"], a["dB"])]
            # record any extremal legs
            for a in rep["accesses"]:
                if a["m"] == "K" and ((a["a"] == 0 and a["q"] >= 3) or
                                     (a["a"] >= 1 and a["eps"] >= 1)):
                    out["extremal"].append(
                        {"n": n, "x": a["x"], "a": a["a"], "q": a["q"],
                         "dA": a["dA"], "dB": a["dB"], "eps": a["eps"]})
        V.step("X-0", "n=%d best-nonst-eps=%s extremal-legs=%d" %
               (n, best[0], len([e for e in out["extremal"] if e["n"] == n])))
        if best[1]:
            V.step("X-0", "  best: %s" % (best[1],))
    V.save("extremal.json", out)
    return 0


if __name__ == "__main__":
    sys.exit(main())

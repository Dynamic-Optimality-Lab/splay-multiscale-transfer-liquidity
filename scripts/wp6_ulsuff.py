"""WP-6 STEP UL-00: old-new sufficiency probe (8K induction-step finite face).

For Q = all B-events (full history), per access L with Q_L nonempty:
  U_L = N(Q_L) \\ N(Q_<L)) (sources first-adjacent at L; E1(L) + first-time
  overlaps + window-new + intervening-young).
  Check at B-heavy accesses (|Q_L| > 3*e_A(L)): |U_L| >= |Q_L|/3 ?
  margin = |U_L| - |Q_L|/3; class split of U_L (E1/Wfirst/E2new/E4/K/interv).
Violations (margin<0) are INDUCTION-FRAME near-misses (NOT Hall kills:
sufficiency-only; record + minimize + analyze zone-novelty).
NEW artifact: ulsuff.json. Sealed files untouched.
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_hallcore import build_graph
from wp6_tightest import vine, Rng, H_walk
from solver import encode as E


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


from collections import defaultdict


def main() -> int:
    step("UL-00", "Old-new sufficiency probe")
    import json
    margins = []
    viols = []
    cls_sum = defaultdict(int)
    nheavy = 0
    nB = 0
    for t in range(250):
        tag = b"ul" if t % 2 == 0 else b"ul2"
        rng = Rng(("s%d" % t).encode(), tag)
        r = rng(0)
        n = [32, 64, 128][r % 3]
        T0 = vine(n, (r >> 8) % 2 == 0)
        rr = Rng(("s%d" % t).encode(), tag + b"h")
        H = H_walk(rr, n, 12 + (r >> 16) % 20, 1 + (r >> 24) % n)
        G = build_graph(n, T0, H)
        if G is None:
            continue
        Aevs, Bevs, elig = G["Aevs"], G["Bevs"], G["elig"]
        pre = G["pre"]
        byacc = defaultdict(list)
        for j in range(len(Bevs)):
            byacc[Bevs[j][0]].append(j)
        accs = sorted(byacc)
        seenN = set()
        for acc in accs:
            js = byacc[acc]
            nB += len(js)
            Nq = set()
            for j in js:
                Nq |= G["adj"][j]
            UL = Nq - seenN
            seenN |= Nq
            eA = sum(1 for z in pre[acc]["sites"] if z)
            if len(js) > 3 * eA and eA > 0:
                nheavy += 1
                need = len(js) / 3.0
                m = len(UL) - need
                margins.append(m)
                # class split of UL
                e = elig[js[0]]
                E1s = set(i for i in e["E1"] if Aevs[i][1]) if js else set()
                for i in UL:
                    if Aevs[i][0] == acc:
                        cls_sum["E1"] += 1
                    else:
                        # which class brings it (first class found at this access)
                        lab = set()
                        for j in js:
                            ee = elig[j]
                            for k in ee:
                                if i in ee[k]:
                                    lab.add(k)
                        k0 = sorted(lab)[0] if lab else "?"
                        cls_sum["old:" + k0] += 1
                if m < 0 and len(viols) < 12:
                    viols.append({"t": t, "acc": acc, "x": pre[acc]["x"],
                                  "Q": len(js), "eA": eA, "UL": len(UL),
                                  "need": round(need, 2), "margin": round(m, 2)})
    margins.sort()
    step("UL-01", "B=%d heavy=%d margin min=%.2f p5=%.2f med=%.2f" % (
        nB, nheavy, margins[0] if margins else float("nan"),
        margins[len(margins) // 20] if margins else float("nan"),
        margins[len(margins) // 2] if margins else float("nan")))
    step("UL-02", "UL class split: %s" % dict(cls_sum))
    step("UL-03", "violations=%d %s" % (len(viols), viols[:6]))
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "ulsuff.json").write_text(
        json.dumps({"B": nB, "nheavy": nheavy,
                    "margin_min": (margins[0] if margins else None),
                    "margin_p5": (margins[len(margins) // 20] if margins else None),
                    "margin_med": (margins[len(margins) // 2] if margins else None),
                    "class_split": dict(cls_sum), "violations": viols},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

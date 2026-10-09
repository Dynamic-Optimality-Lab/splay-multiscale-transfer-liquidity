"""PIVOT-19?: joint E0-gap beam optimization.

Score open words by joint E0-closeness:
  F = max over starved-overflows t of [deficit(t) + best-sharer-residual
      - fat-creator-room + sharing-bonus + order-bonus]
where deficit = q-2a_setup, sharer residual = (q-2a)+ of same-setup nonst,
fat-room = sum 2a over fat creators. Beam-search words, BFS-close/splice
best, charge + Q-2A classify.
"""
from __future__ import annotations
import sys
import copy
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
import wp6_overflow as V
from wp6_ovf_anal import vine


def score_word(T0, w):
    """Joint E0 score: max deficit+residual-fatroom+sharing over starved."""
    rep = V.replay(T0, T0, w)
    accs = {a["idx"]: a for a in rep["accesses"]}
    cr = V.creators(rep)
    crm = {}
    for d in cr:
        crm.setdefault(d["acc"], []).append(d)
    best = (0, None)
    for a in rep["accesses"]:
        if a["m"] != "K" or a["a"] != 0 or a["q"] < 1:
            continue
        st = a.get("setup")
        if st is None:
            continue
        deficit = a["q"] - 2 * accs[st]["a"]
        # sharers: nonst KEEPs with same setup
        sharers = [b for b in rep["accesses"]
                   if b["m"] == "K" and b["a"] >= 1 and b["q"] >= 1
                   and b.get("setup") == st]
        res = max([b["q"] - 2 * b["a"] for b in sharers], default=0)
        # fat creator room over both
        fat = 0
        seen = set()
        for b in [a] + sharers:
            for d in crm.get(b["idx"], []):
                c = d["creator"]
                if c is not None and c not in seen and accs[c]["a"] >= 1:
                    seen.add(c)
                    fat += 2 * accs[c]["a"]
        sharing = 1 if sharers else 0
        F = deficit + max(res, 0) - fat + sharing
        if F > best[0]:
            best = (F, (a["x"], a["q"], accs[st]["a"], deficit,
                        [(b["x"], b["a"], b["q"]) for b in sharers],
                        res, fat))
    return best


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 191
    nbeam = int(sys.argv[2]) if len(sys.argv) > 2 else 40
    nrounds = int(sys.argv[3]) if len(sys.argv) > 3 else 12
    rng = random.Random(seed)
    n = 7
    T0 = vine(n)
    V.step("J-0", "e0-beam seed=%d beam=%d rounds=%d" % (seed, nbeam, nrounds))
    # init beam: random words with starved pairs
    beam = []
    for _ in range(nbeam * 5):
        L = rng.randint(6, 14)
        w = [(rng.choice(["K", "K", "D"]), rng.randint(1, n))
             for _ in range(L)]
        beam.append(w)
    for r in range(nrounds):
        scored = []
        for w in beam:
            try:
                f, _ = score_word(T0, w)
            except Exception:
                continue
            scored.append((f, w))
        scored.sort(key=lambda z: -z[0])
        beam = [w for _, w in scored[:nbeam]]
        V.step("J-1", "round %d best F=%s" % (r, scored[0][0] if scored else None))
        # mutate: splice/extend/mutate top
        new = list(beam)
        for w in beam[:nbeam // 2]:
            # extend
            new.append(w + [(rng.choice(["K", "K", "D"]), rng.randint(1, n))
                            for _ in range(rng.randint(1, 4))])
            # mutate one
            w2 = list(w)
            if w2:
                i = rng.randrange(len(w2))
                w2[i] = (rng.choice(["K", "K", "D"]), rng.randint(1, n))
                new.append(w2)
            # splice two
            w3 = beam[rng.randrange(len(beam))]
            k1, k2 = rng.randrange(len(w) + 1), rng.randrange(len(w3) + 1)
            new.append(w[:k1] + w3[k2:])
        beam = new
    scored = []
    for w in beam:
        try:
            f, info = score_word(T0, w)
        except Exception:
            continue
        scored.append((f, info, w))
    scored.sort(key=lambda z: -z[0])
    V.step("J-2", "top5 F:")
    for f, info, w in scored[:5]:
        V.step("J-2", "  F=%s info=%s len=%d" % (f, info, len(w)))
    V.save("e0beam.json", [{"F": f, "info": info, "w": w}
                           for f, info, w in scored[:10]])
    return 0


if __name__ == "__main__":
    sys.exit(main())

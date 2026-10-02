"""WP-6 HOLEDEMAND: per-site future-claim census for HOLE-IND (C126).

8AC-IND needs residual-sufficiency: site i (plotted acc t) must absorb spill +
future W/K demand within cap 3. Measure the CLAIM POOL per site:
  claim(i) = #{bevs j eligible for i with acc(j) > t} (future demand that could
  ever land on i), by channel (K-claims need rotation; W-claims need grazing).
Stats: max/med claim per history, fraction of sites with claim > 3 (contention
sites), same for K-only. If claims routinely >> 3, HOLE-IND needs assignment
theory (expected per 8N(d) sharing-infinity); if bounded, counting may close.
Artifact: holedemand.json. Sealed files untouched.
"""
from __future__ import annotations
import sys
import json
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_hallcore import build_graph
from wp6_tightest import vine
from wp6_eventflow import to_ptr, splay_A, splay_B_push
from wp6_trap import gen_walk, gen_seed


def step(sid, msg):
    print("[WP-6][HOLEDEMAND %s] %s" % (sid, msg), flush=True)


def analyze(n, T0, H):
    G = build_graph(n, T0, H)
    if G is None:
        return None
    Aevs, Bevs = G["Aevs"], G["Bevs"]
    pre2 = G["pre"]
    A2 = to_ptr(T0)
    B2 = to_ptr(T0)
    Arot = {}
    acc_of = {}
    aid = 0
    for idx, acc in enumerate(pre2):
        A2, invs = splay_A(A2, acc["x"])
        for (S, sited) in zip(invs, acc["sites"]):
            Arot[aid] = frozenset(S)
            acc_of[aid] = idx
            aid += 1
        if acc["mode"] == "KEEP":
            B2, _ = splay_B_push(B2, acc["x"])
    maxclaim = 0
    maxK = 0
    over = 0
    nsites = 0
    claims = []
    for i, (ai, sited) in enumerate(Aevs):
        if not sited:
            continue
        nsites += 1
        c = k = 0
        xi = None
        for j in range(len(Bevs)):
            aj = Bevs[j][0]
            if aj <= ai:
                continue
            e = G["elig"][j]
            if i in e["E1"]:
                continue  # same-access only, never future
            xx = pre2[aj]["x"]
            inK = (i in e["E3"] and xx in Arot.get(i, frozenset()))
            inW = (i in e["E3"] and not inK and i not in e["E1"])
            if inK or inW or i in e["E2"] or i in e.get("E7", []) or i in e["E4"]:
                c += 1
                if inK:
                    k += 1
        claims.append(c)
        maxclaim = max(maxclaim, c)
        maxK = max(maxK, k)
        if c > 3:
            over += 1
    claims.sort()
    return {"nsites": nsites, "maxclaim": maxclaim, "maxK": maxK,
            "over": over, "medclaim": (claims[len(claims) // 2] if claims else 0)}


def main() -> int:
    step("HD-00", "per-site future-claim census (walks + pushers)")
    agg = Counter()
    mx = mxK = 0
    mover = mns = 0
    meds = []
    done = 0
    hists = [gen_walk(9000 + s) for s in range(40)] + [gen_seed(9000 + s, b"hd") for s in range(40)]
    for (n, T0, H) in hists:
        v = analyze(n, T0, H)
        if v is None:
            continue
        done += 1
        mx = max(mx, v["maxclaim"])
        mxK = max(mxK, v["maxK"])
        mover += v["over"]
        mns += v["nsites"]
        meds.append(v["medclaim"])
    meds.sort()
    out = {"evals": done, "sitemax_claim": mx, "sitemax_Kclaim": mxK,
           "sites_over3": mover, "sites_total": mns,
           "over_frac": (mover / max(1, mns)),
           "medclaim_med": (meds[len(meds) // 2] if meds else 0),
           "medclaim_max": max(meds) if meds else 0}
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "holedemand.json").write_text(
        json.dumps(out, indent=1, sort_keys=True, default=str), encoding="utf-8")
    step("HD-01", json.dumps(out, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""WP-6 STEP RD-00: per-run net-drain probe + sustain hunt (C55).

X-run = maximal consecutive same-key accesses. Per run with demanding KEEP(s):
  new-union members (first-ever-adjacent A-StepEvs: E1s + E4-first + W-first +
  E2-new + ...), B-demand (sum e_B over run KEEPs), net = 3*new - demand.
Sustain hunt: repeated B-heavy runs on SAME x/zone (revisit: K/E4-old,
W-shared-old, E2-same-pumpers, sterile-new) maximizing cumulative net-drain
and shortfall (KILL -> hallkill + §24). If net-drain per run stays bounded
(novelty forced), that is the finite face of run-sustainability.
NEW artifact: rundrain.json (+hallkill on kill). Sealed files untouched.
"""
from __future__ import annotations
import sys
import copy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_hallcore import build_graph, maxflow_cap3, delta_of
from wp6_offline import gc_gap
from wp6_tightest import vine, Rng, H_walk
from solver import encode as E


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


import hashlib as _h
from collections import defaultdict


def run_nets(n, T0, H):
    """Per-x-run (net, demand, newN, eB, kind) using union-growth accounting."""
    G = build_graph(n, T0, H)
    if G is None:
        return None
    Aevs, Bevs = G["Aevs"], G["Bevs"]
    pre = G["pre"]
    # x-runs over accesses
    runs = []
    cur = None
    for idx, acc in enumerate(pre):
        if cur is None or acc["x"] != cur[0]:
            if cur is not None:
                runs.append(cur)
            cur = [acc["x"], idx, idx]
        else:
            cur[2] = idx
    if cur is not None:
        runs.append(cur)
    # union growth in access order; attribute new members to runs
    seenN = set()
    out = []
    for (x, a0, a1) in runs:
        # B-demand of run (Bevs in [a0..a1])
        dem = sum(1 for j in range(len(Bevs)) if a0 <= Bevs[j][0] <= a1)
        newN = set()
        for j in range(len(Bevs)):
            if a0 <= Bevs[j][0] <= a1:
                for i in G["adj"][j]:
                    if i not in seenN:
                        newN.add(i)
        seenN |= newN
        eBs = [len(pre[ai]["Bev"]) for ai in range(a0, a1 + 1) if pre[ai]["mode"] == "KEEP"]
        out.append({"x": x, "a0": a0, "a1": a1, "dem": dem, "new": len(newN),
                    "net": 3 * len(newN) - dem, "eBmax": max(eBs) if eBs else 0})
    return out


def eval_hist(n, T0, H):
    for (m, x) in H:
        if not (1 <= x <= n):
            return ("SKIP", None, None)
    G = build_graph(n, T0, H)
    if G is None:
        return None
    f, nb, lv = maxflow_cap3(G)
    if nb - f > 0:
        return ("KILL", nb - f, nb)
    gap, _ = gc_gap(n, T0, H)
    return ("OK", nb, gap)


def main() -> int:
    step("RD-00", "Per-run net-drain probe + sustain hunt")
    import json
    TP = ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "rundrain.json"
    worst_net = 0
    worst_ex = None
    cumdrain = 0
    nrun = 0
    nbheavyrun = 0
    for t in range(250):
        tag = b"rd" if t % 2 == 0 else b"rd2"
        rng = Rng(("s%d" % t).encode(), tag)
        r = rng(0)
        n = [32, 64, 128][r % 3]
        T0 = vine(n, (r >> 8) % 2 == 0)
        rr = Rng(("s%d" % t).encode(), tag + b"h")
        H = H_walk(rr, n, 14 + (r >> 16) % 20, 1 + (r >> 24) % n)
        rn = run_nets(n, T0, H)
        if rn is None:
            continue
        for rec in rn:
            nrun += 1
            if rec["dem"] > 0 and rec["new"] * 3 < rec["dem"]:
                nbheavyrun += 1
            if rec["net"] < worst_net:
                worst_net = rec["net"]
                worst_ex = {"t": t, **rec}
    step("RD-01", "runs=%d Bheavy-drain=%d worst_net=%d %s" % (nrun, nbheavyrun, worst_net, worst_ex))
    # sustain hunt: mutate toward repeated B-heavy same-x runs
    best = worst_net
    evals = 0
    holders = []
    for s in range(60):
        rng = Rng(("s%d" % s).encode(), b"rdh")
        r = rng(0)
        n = [64, 128][r % 2]
        T0 = vine(n, (r >> 8) % 2 == 0)
        x = min(n, max(8, 32 + (r >> 16) % 64))
        H = []
        L = 10 + (r >> 24) % 14
        for i in range(L):
            rr = Rng(("s%d" % s).encode(), ("rdhh%d" % i).encode())
            q = rr(1000 + i)
            # runs: blocks of same-key (DELETE-run + KEEP-repeat pattern included)
            if i % 6 == 5:
                x = min(n, max(8, 32 + (rr(2000 + i) % 64)))
            H.append(["KEEP" if q % 3 else "DELETE", x if (q >> 5) % 3 else 1 + (q >> 7) % n])
        v = eval_hist(n, T0, H)
        evals += 1
        if v is None or v[0] == "SKIP":
            continue
        if v[0] == "KILL":
            step("RD-KILL", "HALL seed %d" % s)
            TP.write_text(json.dumps({"kill": True, "H": H}, indent=1, default=str), encoding="utf-8")
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json").write_text(
                json.dumps({"kill": True, "H": H}, indent=1, default=str), encoding="utf-8")
            return 2
        holders.append((T0, H, n))
    holders = holders[:14]
    it = 0
    cum_best = 0
    while evals < 8000:
        it += 1
        r = int.from_bytes(_h.sha256(b"rdm|%d" % it).digest(), "big")
        T0, H, n = holders[(r >> 2) % len(holders)]
        H2 = copy.deepcopy(H)
        op = r % 5
        if op == 0 and H2:
            i = (r >> 5) % len(H2)
            H2[i][0] = "DELETE" if H2[i][0] == "KEEP" else "KEEP"
        elif op == 1 and H2:
            i = (r >> 5) % len(H2)
            H2[i][1] = 1 + (r >> 13) % n
        elif op == 2 and len(H2) < 70:
            # repeat recent key (run sustain)
            recent = [a[1] for a in H2][-3:]
            k = recent[(r >> 5) % len(recent)] if recent else 1 + (r >> 13) % n
            H2.insert((r >> 5) % (len(H2) + 1), ["KEEP" if r % 2 else "DELETE", k])
        elif op == 3 and H2:
            recent = [a[1] for a in H2 if a[0] == "KEEP"][-3:]
            if recent:
                H2.append(["KEEP", recent[(r >> 5) % len(recent)]])
            else:
                H2.append(["DELETE", 1 + (r >> 13) % n])
        elif len(H2) > 4:
            del H2[(r >> 5) % len(H2)]
        rn = run_nets(n, T0, H2)
        v = eval_hist(n, T0, H2)
        evals += 1
        if v is None or rn is None:
            continue
        if v[0] == "KILL":
            step("RD-KILL", "HALL it=%d" % it)
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json").write_text(
                json.dumps({"kill": True, "H": H2}, indent=1, default=str), encoding="utf-8")
            return 2
        # cumulative net-drain over B-heavy runs (most negative suffix of run nets)
        cum = 0
        mincum = 0
        for rec in rn:
            if rec["dem"] > 0:
                # heavy-run drain contribution (negative net only)
                cum += min(0, rec["net"])
                mincum = min(mincum, cum)
        if mincum < cum_best:
            cum_best = mincum
            holders.append((T0, H2, n))
            holders = holders[-14:]
            if it % 500 == 0:
                step("RD-02", "it=%d evals=%d cumdrain=%d" % (it, evals, cum_best))
        elif (r >> 6) % 4 == 0:
            holders.append((T0, H2, n))
            holders = holders[-14:]
        if it % 2000 == 0:
            step("RD-02", "it=%d evals=%d cumdrain=%d" % (it, evals, cum_best))
    step("RD-03", "evals=%d worst_net=%d cumdrain=%d" % (evals, worst_net, cum_best))
    TP.write_text(json.dumps({"evals": evals, "worst_net": worst_net, "worst_ex": worst_ex,
                              "cumdrain": cum_best},
                             indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

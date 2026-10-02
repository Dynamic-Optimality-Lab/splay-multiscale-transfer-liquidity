"""WP-6 WCHARGE: W-charge-to-rotations census for the FWD pressure law (C124).

FWD greedy is near-total (C123/TB); the only contention on bev j's fresh E1
sites comes from PAST bevs via W (K is impossible for past bevs on
future-plotted sites: K needs acc_of(i) < acc(j')). Per access t measure:
  sites_t, sibling bevs, E1-capacity 3|sites_t|, past-W-load on sites_t,
  headroom_t = 3|sites_t| - pastW_t - siblings_t (expect >= 0; min = margin),
plus per-site max W-load, W time-relation histogram (loader acc vs site acc:
past/same/future), and FWD|T,E1,E4,K placement-channel mix.
Grounding: ML OCC/W-BLOCKS lemmas (rotation occupancy budgets W-load).
Artifact: wcharge.json. Sealed files untouched.
"""
from __future__ import annotations
import sys
import json
from pathlib import Path
from collections import Counter, defaultdict

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_hallcore import build_graph, maxflow_cap3
from wp6_tightest import vine
from wp6_eventflow import to_ptr, splay_A, splay_B_push
from wp6_trap import greedy_M, gen_walk, gen_seed, chan_of


def step(sid, msg):
    print("[WP-6][WCHARGE %s] %s" % (sid, msg), flush=True)


def analyze(n, T0, H, tiers=("T", "E1", "E4", "K")):
    G = build_graph(n, T0, H)
    if G is None:
        return None
    f, nb, _ = maxflow_cap3(G)
    if nb - f > 0:
        return ("KILL", nb - f)
    Aevs, Bevs = G["Aevs"], G["Bevs"]
    pre2 = G["pre"]
    A2, B2 = to_ptr(T0), to_ptr(T0)
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
    short, M, loads = greedy_M(n, T0, H, G, Arot, acc_of, list(tiers), False)
    # placement channels + W time relations + quartile mix
    chanmix = Counter()
    quartmix = defaultdict(Counter)
    wrel = Counter()
    trel = defaultdict(Counter)
    siteload_W = Counter()   # aid -> W placements
    siteload_all = Counter()
    loader_acc = {}
    for j, i in M.items():
        aj = Bevs[j][0]
        loader_acc[(j, i)] = aj
        ai = acc_of.get(i, -1)
        ch = chan_of(j, i, G, Arot, acc_of)
        # tier label by order
        lab = "?"
        for k in tiers:
            if k == "E1" and "E1" in ch:
                lab = "E1"
                break
            if k == "E4" and "E4" in ch:
                lab = "E4"
                break
            if k == "K" and "K" in ch:
                lab = "K"
                break
            if k == "T" and ({"W", "E2", "E7"} & ch):
                lab = ("W" if "W" in ch else ("E2" if "E2" in ch else "E7"))
                break
        chanmix[lab] += 1
        trel[lab]["older" if aj < ai else ("same" if aj == ai else "newer")] += 1
        q = min(3, (4 * aj) // max(1, len(pre2)))
        quartmix[q][lab] += 1
        siteload_all[i] += 1
        if "W" in ch:
            siteload_W[i] += 1
            wrel["older" if aj < ai else ("same" if aj == ai else "newer")] += 1
    # per-access headroom
    sites_of = defaultdict(list)
    for aid2, t in acc_of.items():
        if Aevs[aid2][1]:
            sites_of[t].append(aid2)
    bevs_of = defaultdict(int)
    for j in range(len(Bevs)):
        bevs_of[Bevs[j][0]] += 1
    pastW_of = Counter()
    for (j, i), aj in loader_acc.items():
        ch = chan_of(j, i, G, Arot, acc_of)
        if "W" in ch and aj < acc_of.get(i, -1):
            pastW_of[acc_of[i]] += 1
    heads = []
    neg = 0
    for t in range(len(pre2)):
        cap = 3 * len(sites_of[t])
        h = cap - pastW_of[t] - bevs_of[t]
        heads.append(h)
        if h < 0:
            neg += 1
    return {"stuck": len(short), "chanmix": dict(chanmix), "wrel": dict(wrel),
            "trel": {k: dict(v) for k, v in trel.items()},
            "quartmix": {k: dict(v) for k, v in quartmix.items()},
            "sitemaxW": max(siteload_W.values()) if siteload_W else 0,
            "sitemaxall": max(siteload_all.values()) if siteload_all else 0,
            "head_min": min(heads) if heads else None,
            "head_neg": neg, "nacc": len(pre2)}


def main() -> int:
    import sys as _s
    fam = _s.argv[1] if len(_s.argv) > 1 else "walk"
    step("WC-00", "W-charge census: FWD|T,E1,E4,K family=%s" % fam)
    N = 150
    agg_chan = Counter()
    agg_wrel = Counter()
    agg_quart = defaultdict(Counter)
    agg_trel = defaultdict(Counter)
    sitemaxW = 0
    sitemaxall = 0
    head_mins = []
    head_negs = 0
    stuck = 0
    kills = 0
    done = 0
    for s in range(N):
        n, T0, H = gen_walk(5000 + s) if fam == "walk" else gen_seed(5000 + s, b"wp")
        v = analyze(n, T0, H)
        if v is None:
            continue
        if isinstance(v, tuple):
            kills += 1
            step("WC-KILL", "HALL seed %d" % s)
            continue
        done += 1
        stuck += v["stuck"]
        agg_chan.update(v["chanmix"])
        agg_wrel.update(v["wrel"])
        for q, c in v["quartmix"].items():
            agg_quart[q].update(c)
        for lab, c in v["trel"].items():
            agg_trel[lab].update(c)
        sitemaxW = max(sitemaxW, v["sitemaxW"])
        sitemaxall = max(sitemaxall, v["sitemaxall"])
        head_mins.append(v["head_min"])
        head_negs += v["head_neg"]
        if s % 30 == 29:
            step("WC-P", "s=%d stuck=%d kills=%d" % (s, stuck, kills))
    import statistics
    hm = [h for h in head_mins if h is not None]
    out = {"evals": done, "stuck": stuck, "kills": kills,
           "chanmix": dict(agg_chan), "wrel": dict(agg_wrel),
           "quartmix": {k: dict(v) for k, v in agg_quart.items()},
           "trel": {k: dict(v) for k, v in agg_trel.items()},
           "sitemaxW": sitemaxW, "sitemaxall": sitemaxall,
           "head_min": min(hm) if hm else None,
           "head_med": (sorted(hm)[len(hm) // 2] if hm else None),
           "head_neg_accesses": head_negs}
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / (
        "wcharge.json" if fam == "walk" else ("wcharge_%s.json" % fam))).write_text(
        json.dumps(out, indent=1, sort_keys=True, default=str), encoding="utf-8")
    step("WC-01", json.dumps(out, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())

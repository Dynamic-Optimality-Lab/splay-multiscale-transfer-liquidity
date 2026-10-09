"""PIVOT-13 T4: chains/orientation, nonconsecution, rotation soup, vignettes,
n=7 rho_Q achiever words."""
from __future__ import annotations
import sys
import json
import random
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
import wp6_overflow as V


def vine(n, left=False):
    t = None
    for k in (range(n, 0, -1) if not left else range(1, n + 1)):
        t = [k, None, t] if not left else [k, t, None]
    return t


def shapes_of(ks):
    if not ks:
        return [None]
    res = []
    for i, k in enumerate(ks):
        for l in shapes_of(ks[:i]):
            for r in shapes_of(ks[i + 1:]):
                res.append([k, l, r])
    return res


def chains(rep, cr):
    """Access-level creator chains: C(t) = latest creator among t's doubles
    (fallback: setup). Follow until None/genesis/repeat. Returns stats."""
    dbl_by_acc = {}
    for d in cr:
        dbl_by_acc.setdefault(d["acc"], []).append(d)
    setup_of = {a["idx"]: a.get("setup") for a in rep["accesses"]}
    C = {}
    for t, ds in dbl_by_acc.items():
        cs = [d["creator"] for d in ds if d["creator"] is not None]
        C[t] = max(cs) if cs else None
    lens, terms = [], Counter()
    for t in dbl_by_acc:
        seen = set()
        u, L = t, 0
        while True:
            if u is None:
                terms["none"] += 1
                break
            if u in seen:
                terms["loop"] += 1
                break
            seen.add(u)
            v = C.get(u)
            if v is None:
                # fallback setup of u
                v = setup_of.get(u)
                if v is None:
                    terms["genesis/none"] += 1
                    break
                terms["setup-term"] += 1
                L += 1
                break
            u, L = v, L + 1
            if L > 500:
                terms["long"] += 1
                break
        lens.append(L)
    return {"n": len(lens), "maxlen": max(lens) if lens else 0,
            "meanlen": sum(lens) / max(1, len(lens)), "terms": dict(terms)}


def overflow_blocks_orientation(rep):
    """Compare deep-vs-shallow overflow canonical blocks: for each access
    with eps>0, list overflow seqs under both orientations + their creators."""
    acc_of = {}
    for a in rep["accesses"]:
        acc_of[a["idx"]] = a
    # need creators per (acc,seq): recompute
    cr = V.creators(rep)
    cre = {(d["acc"], d["seq"]): d for d in cr}
    deep_stats, shal_stats = Counter(), Counter()
    for a in rep["accesses"]:
        if a["m"] != "K" or a["eps"] <= 0:
            continue
        dbls = [s["seq"] for s in a["bsteps"] if s["kind"] == "double"]
        k = a["eps"]
        # deep-first-overflow: overflow = shallowest k (largest seq)
        deep_ov = sorted(dbls)[-k:] if k <= len(dbls) else list(dbls)
        # shallow-first-overflow: overflow = deepest k (smallest seq)
        shal_ov = sorted(dbls)[:k] if k <= len(dbls) else list(dbls)
        for sq in deep_ov:
            d = cre.get((a["idx"], sq))
            deep_stats["gen" if (d is None or d["genesis"]) else "built"] += 1
            if d is not None and d["creator"] is not None:
                deep_stats["dist%d" % (a["idx"] - d["creator"])] += 1
        for sq in shal_ov:
            d = cre.get((a["idx"], sq))
            shal_stats["gen" if (d is None or d["genesis"]) else "built"] += 1
            if d is not None and d["creator"] is not None:
                shal_stats["dist%d" % (a["idx"] - d["creator"])] += 1
    return {"deep-first-overflow(shallow-blocks)": dict(deep_stats),
            "shallow-first-overflow(deep-blocks)": dict(shal_stats)}


def main():
    rng = random.Random(99)
    out = {}
    # --- corpus: sample overflow cycles n=6 via walk sampler + fixed words
    import wp6_walk as W
    n = 6
    T0 = vine(n)
    words = []
    tries = 0
    while len(words) < 40 and tries < 3000:
        tries += 1
        cyc = W.sample_cycle(n, T0, T0, rng)
        if not cyc:
            continue
        rep0 = V.replay(T0, T0, cyc)
        if max(a["eps"] for a in rep0["accesses"]) <= 0:
            continue
        words.append(cyc)
    V.step("A-0", "corpus=%d cycles" % len(words))
    # --- chains + orientation aggregate
    agg_ch, agg_or = Counter(), {"d": Counter(), "s": Counter()}
    nonconsec_runs = Counter()
    consec_hits = []
    for w in words:
        rep = V.replay(T0, T0, w + w)
        L = len(w)
        cr = V.creators(rep)
        lap2 = [d for d in cr if d["acc"] >= L]
        ch = chains({"accesses": rep["accesses"]}, lap2)
        agg_ch["n"] += ch["n"]
        agg_ch["maxlen"] = max(agg_ch.get("maxlen", 0), ch["maxlen"])
        # nonconsecution on lap2 legs
        legs = rep["accesses"][L:]
        run = 0
        for a in legs:
            if a["eps"] > 0:
                run += 1
            else:
                if run:
                    nonconsec_runs[run] += 1
                run = 0
        if run:
            nonconsec_runs[run] += 1
        # consecutive overflow pairs?
        for i in range(len(legs) - 1):
            if legs[i]["eps"] > 0 and legs[i + 1]["eps"] > 0:
                consec_hits.append(
                    (legs[i]["x"], legs[i]["eps"], legs[i + 1]["x"],
                     legs[i + 1]["eps"]))
        o = overflow_blocks_orientation(
            {"accesses": legs, "brot": rep["brot"]})
        for k, v in o["deep-first-overflow(shallow-blocks)"].items():
            agg_or["d"][k] += v
        for k, v in o["shallow-first-overflow(deep-blocks)"].items():
            agg_or["s"][k] += v
    out["chains"] = dict(agg_ch)
    out["orientation"] = {k: dict(v) for k, v in agg_or.items()}
    out["overflow_run_lengths"] = dict(nonconsec_runs)
    out["consec_hits"] = consec_hits[:20]
    out["n_consec"] = len(consec_hits)
    V.step("A-1", "chains=%s" % (dict(agg_ch),))
    V.step("A-1", "runs=%s consec=%d" % (dict(nonconsec_runs),
                                         len(consec_hits)))
    V.step("A-1", "orient deep=%s" % (dict(agg_or["d"]),))
    V.step("A-1", "orient shal=%s" % (dict(agg_or["s"]),))
    # --- rotation soup on a big replay (long walk, n=6)
    big = []
    rng2 = random.Random(5)
    for _ in range(300):
        big.append((rng2.choice(["K", "K", "D"]), rng2.randint(1, n)))
    rep = V.replay(T0, T0, big)
    pats = Counter()
    for a in rep["accesses"]:
        for s in a["bsteps"]:
            pats[("B", s["kind"], s["pat"])] += 1
        for s in a["asteps"]:
            pats[("A", s["kind"], s["pat"])] += 1
    out["soup"] = {"%s-%s-%s" % k: v for k, v in pats.items()}
    V.step("A-2", "soup=%s" % (out["soup"],))
    # --- vignettes: find (a=1,q=3) and (a=0,q=1) overflow accesses
    vig = {}
    for w in words:
        rep = V.replay(T0, T0, w + w)
        L = len(w)
        for a in rep["accesses"][L:]:
            if a["m"] != "K" or a["eps"] <= 0:
                continue
            key = "a%dq%d" % (a["a"], a["q"])
            if key in ("a1q3", "a0q1") and key not in vig:
                cr = V.creators(rep)
                ds = [d for d in cr if d["acc"] == a["idx"]]
                vig[key] = {
                    "word": w, "acc": a["idx"], "x": a["x"],
                    "dA": a["dA"], "dB": a["dB"], "setup": a.get("setup"),
                    "bsteps": [(s["seq"], s["pat"], s["p"], s["g"])
                               for s in a["bsteps"]],
                    "dbls": [(d["seq"], d["pat"], d["creator"],
                              d["genesis"]) for d in ds]}
                # setup access detail
                st = a.get("setup")
                if st is not None:
                    sa = rep["accesses"][st]
                    vig[key]["setup_acc"] = {
                        "m": sa["m"], "x": sa["x"], "dA": sa["dA"],
                        "a": sa["a"]}
        if len(vig) == 2:
            break
    out["vignettes"] = vig
    for k, v in vig.items():
        V.step("A-3", "%s: %s" % (k, json.dumps(v)))
    V.save("analysis.json", out)
    # --- n=7 rho_Q achiever words on diagonals
    Sh7 = shapes_of(list(range(1, 8)))
    V.step("A-4", "n=7 shapes=%d" % len(Sh7))
    words7 = {"53": [("K", 3), ("K", 6), ("K", 3), ("K", 4), ("K", 2),
                     ("K", 1)],
              "k2134": [("K", 2), ("K", 1), ("K", 3), ("K", 4)]}
    best = {}
    for wn, w in words7.items():
        for i in (0, 1, 5, 100, 200, 300, 400):
            T = Sh7[i]
            try:
                rep = V.replay(T, T, w)
            except Exception:
                continue
            A = sum(a["a"] for a in rep["accesses"])
            Q = sum(a["q"] for a in rep["accesses"])
            if A > 0 and Q / A > best.get(wn, (0,))[0]:
                best[wn] = (Q / A, i, A, Q)
    out["rhoQ_n7"] = {k: v for k, v in best.items()}
    V.step("A-4", "rhoQ_n7=%s" % (best,))
    V.save("analysis.json", out)
    return 0


if __name__ == "__main__":
    sys.exit(main())

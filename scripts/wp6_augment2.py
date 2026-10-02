"""WP-6 AUGMENT2: stuck-event anatomy + augmenting-path census (C141).
(Named augment2: wp6_augment.py/augment.json belong to C37/C41; preserved.)

Every stuck greedy bev (maxflow-ok) has an augmenting path (Berge). Trace it:
BFS from unmatched b0 over eligible edges (B->A, plotted) + greedy-matched
edges (A->B); first free-A reached gives the augmenting path. Record: path
length (edges), terminal channel (edge into the free node), channel mix along
the path, plus the stuck bev's TIER LEDGER (per-tier: E1/E4/K/T-neighborhood
sizes, full-count, and WHO loads the full ones: siblings vs past, with
past-loader channel mix). Objective: the tier-ledger universal in finite face
(what fills N(j) when greedy sticks: K-hoarding? T-theft? repeat-grounding?)
+ augmenting-path confinement (length/terminal structure: how instances
resolve stuckness). Falsifies-or-guides 8AC-X tier-ledger closure.
Configs: FWD|E1E4KT (known sticker) + REV variants for contrast.
Artifact: augment.json. Sealed files untouched.
"""
from __future__ import annotations
import sys
import json
from pathlib import Path
from collections import Counter, defaultdict, deque

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_hallcore import build_graph, maxflow_cap3
from wp6_eventflow import to_ptr, splay_A, splay_B_push
from wp6_trap import greedy_M, gen_walk, gen_seed, chan_of


def step(sid, msg):
    print("[WP-6][AUGMENT %s] %s" % (sid, msg), flush=True)


def setup(n, T0, H, G):
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
    return Arot, acc_of


def tiers_of(j, G, Arot, acc_of):
    """Tier partition of bev j's plotted eligible neighbors."""
    Aevs, Bevs = G["Aevs"], G["Bevs"]
    pre2 = G["pre"]
    acc = Bevs[j][0]
    e = G["elig"][j]
    xx = pre2[acc]["x"]
    E1s = [i for i in e["E1"] if Aevs[i][1]]
    E4s = [i for i in e["E4"] if Aevs[i][1]]
    E3s = set(i for i in e["E3"] if Aevs[i][1])
    K = [i for i in E3s if xx in Arot.get(i, frozenset()) and acc_of.get(i, acc) < acc]
    E1set = set(E1s)
    W = [i for i in E3s if i not in set(K) and i not in E1set]
    TR = list(set(i for i in e["E2"] if Aevs[i][1]) | set(W) | set(i for i in e.get("E7", []) if Aevs[i][1]))
    return {"E1": E1s, "E4": E4s, "K": K, "T": TR}


def augment_path(G, Arot, acc_of, M, loads, b0):
    """BFS augmenting path from unmatched b0. Returns (length_edges, term_chan, chanmix, open_ok)."""
    Aevs, Bevs = G["Aevs"], G["Bevs"]
    seenB = {b0}
    seenA = {}
    q = deque([("B", b0, 0)])
    Amate = defaultdict(list)
    for j, i in M.items():
        Amate[i].append(j)
    parent = {}
    while q:
        typ, v, d = q.popleft()
        if typ == "B":
            for i in G["adj"][v]:
                if not Aevs[i][1] or i in seenA:
                    continue
                seenA[i] = (v, d + 1)
                parent[("A", i)] = ("B", v)
                if loads.get(i, 0) < 3:
                    # reconstruct channel mix along path
                    chan = Counter()
                    for c in chan_of(v, i, G, Arot, acc_of):
                        chan[c] += 1
                    term = set(chan)
                    cur = ("B", v)
                    length = d + 1
                    while cur != ("B", b0):
                        p = parent[cur]
                        if p[0] == "B":
                            for c in chan_of(p[1], cur[1], G, Arot, acc_of):
                                chan[c] += 1
                        cur = p
                        length += 1
                    return {"len": length, "term": sorted(term), "chan": dict(chan)}
                q.append(("A", i, d + 1))
        else:
            for j in Amate.get(v, []):
                if j not in seenB:
                    seenB.add(j)
                    parent[("B", j)] = ("A", v)
                    q.append(("B", j, d + 1))
    return None


def analyze(n, T0, H, tiers, rev):
    G = build_graph(n, T0, H)
    if G is None:
        return None
    f, nb, _ = maxflow_cap3(G)
    if nb - f > 0:
        return ("KILL", nb - f)
    Aevs, Bevs = G["Aevs"], G["Bevs"]
    Arot, acc_of = setup(n, T0, H, G)
    short, M, loads = greedy_M(n, T0, H, G, Arot, acc_of, tiers, rev)
    if not short:
        return ("OK",)
    invM = {}
    for j, i in M.items():
        invM.setdefault(i, []).append(j)
    out = []
    for b0 in short[:8]:
        ts = tiers_of(b0, G, Arot, acc_of)
        ledger = {}
        futdepth = []
        for k, lst in ts.items():
            full = [i for i in lst if loads.get(i, 0) >= 3]
            past = 0
            sib = 0
            fut = 0
            for i in full:
                for j in invM.get(i, []):
                    if Bevs[j][0] == Bevs[b0][0]:
                        sib += 1
                    elif Bevs[j][0] < Bevs[b0][0]:
                        past += 1
                    else:
                        fut += 1
                        futdepth.append(Bevs[j][0] - Bevs[b0][0])
            ledger[k] = {"deg": len(lst), "full": len(full), "sib": sib,
                         "past": past, "fut": fut}
        ap = augment_path(G, Arot, acc_of, M, loads, b0)
        out.append({"ledger": ledger, "aug": ap, "futdepth": futdepth})
    return ("STUCK", out)


def main() -> int:
    step("AU-00", "stuck anatomy + augmenting-path census")
    configs = [(["E1", "E4", "K", "T"], False), (["E1", "E4", "K", "T"], True),
               (["K", "E1", "E4", "T"], False), (["K", "E1", "E4", "T"], True),
               (["T", "E1", "E4", "K"], True)]
    nstuck = 0
    lens = []
    terms = Counter()
    chmix = Counter()
    led_full = Counter()
    led_past = Counter()
    led_sib = Counter()
    led_fut = Counter()
    led_deg = Counter()
    bygroup = Counter()
    futdepth_all = []
    kills = 0
    done = 0
    for s in range(120):
        for fam in (0, 1):
            n, T0, H = gen_walk(7000 + s) if fam == 0 else gen_seed(7000 + s, b"au")
            for ci, (tiers, rev) in enumerate(configs):
                v = analyze(n, T0, H, tiers, rev)
                if v is None:
                    continue
                done += 1
                if v[0] == "KILL":
                    kills += 1
                    continue
                if v[0] == "OK":
                    continue
                for ev in v[1]:
                    nstuck += 1
                    gk = "cfg%d/fam%d/rev%s" % (ci, fam, rev)
                    bygroup[gk] += 1
                    for d in ev.get("futdepth", []):
                        futdepth_all.append(d)
                    for k, ld in ev["ledger"].items():
                        led_deg[k] += ld["deg"]
                        led_full[k] += ld["full"]
                        led_past[k] += ld["past"]
                        led_sib[k] += ld["sib"]
                        led_fut[k] += ld.get("fut", 0)
                    ap = ev["aug"]
                    if ap is None:
                        terms["NONE(open-fail)"] += 1
                        continue
                    lens.append(ap["len"])
                    for t in ap["term"]:
                        terms[t] += 1
                    chmix.update(ap["chan"])
    lens.sort()
    futdepth_all.sort()
    npd = len(futdepth_all)
    out = {"evals": done, "stuck": nstuck, "kills": kills, "bygroup": dict(bygroup),
           "futdepth_n": npd,
           "futdepth_med": (futdepth_all[npd // 2] if npd else None),
           "futdepth_p90": (futdepth_all[int(npd * 0.9)] if npd else None),
           "futdepth_max": (futdepth_all[-1] if npd else None),
           "aug_len_med": (lens[len(lens) // 2] if lens else None),
           "aug_len_max": (lens[-1] if lens else None),
           "aug_len_hist": {str(k): v for k, v in Counter(lens).most_common(12)},
           "aug_term": dict(terms), "aug_chan": dict(chmix),
           "led_deg": dict(led_deg), "led_full": dict(led_full),
           "led_past": dict(led_past), "led_sib": dict(led_sib),
           "led_fut": dict(led_fut)}
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "augment2.json").write_text(
        json.dumps(out, indent=1, sort_keys=True, default=str), encoding="utf-8")
    step("AU-01", json.dumps(out, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())

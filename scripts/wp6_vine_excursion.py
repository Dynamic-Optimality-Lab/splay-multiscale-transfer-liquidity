"""PIVOT-9-2 vine excursion oracle, phase A (n=6 complete census).

- vine-pair identification + Lean-mapping check (edgeOk under inverted bits)
- open vine law check on all vine-internal edges: B-A <= tau(s)-tau(t)
- exit edges (vine->nonvine) + shortest first-returns: full excursion census
  with W_2, twin bits, DELETE/KEEP counts, max depths, entry/exit taxonomy
- 5/3 achiever search (all starts x word) + vine/excursion anatomy
- artifacts: vine_excursion/
"""
from __future__ import annotations
import sys
import json
import copy
from pathlib import Path
from collections import deque

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_eventflow import to_ptr, splay_A, splay_B_push
from wp6_adv import depths_of
import wp6_cycle_ratio as O

BD = ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "vine_excursion"


def save(name, obj):
    BD.mkdir(parents=True, exist_ok=True)
    (BD / name).write_text(json.dumps(obj, indent=1, sort_keys=True,
                                      default=str), encoding="utf-8")


def step(sid, msg):
    print("[VEX-A %s] %s" % (sid, msg), flush=True)


def main():
    n = 6
    G = O.build(n)
    nS, adj, Sh = G["nS"], G["adj"], G["Sh"]
    ks = list(range(1, n + 1))
    ptrs = [to_ptr(copy.deepcopy(s)) for s in Sh]
    dep = []
    for ia in range(nS):
        d = depths_of(copy.deepcopy(ptrs[ia]))
        dep.append([d.get(x, 0) for x in ks])
    roots = [s[0] for s in Sh]
    vine = set(ia for ia in range(nS) if max(dep[ia]) == n - 1)
    VN = set(ia * nS + ib for ia in vine for ib in vine)
    step("A0", "shapes=%d vines=%d vinepairs=%d" % (nS, len(vine), len(VN)))

    # --- Lean-mapping + open-law check on all vine-internal edges ---
    mapbad = 0
    openbad = 0
    openworst = None
    inedges = 0
    for u in VN:
        ia, ib = u // nS, u % nS
        tu = 1 if roots[ia] != roots[ib] else 0
        for e in adj[u]:
            v = e[0]
            if v not in VN:
                continue
            inedges += 1
            md, x, ea, eb = e[1], e[2], e[3], e[4]
            # inverted-bit mapping: Lean-bit = twin-ness
            ja, jb = v // nS, v % nS
            pre = roots[ia] == roots[ib]
            post = roots[ja] == roots[jb]
            ok = False
            if (ea, eb) == (0, 0) and pre == post:
                ok = True
            elif (ea, eb) == (1, 0):
                ok = True
            elif (ea, eb) == (0, 1) and (not pre) and post:
                ok = True
            elif (ea, eb) == (1, 1) and not (pre and not post):
                ok = True
            if not ok:
                mapbad += 1
            tv = 1 if roots[ja] != roots[jb] else 0
            if (eb - ea) > tu - tv:
                openbad += 1
                g = (eb - ea) - (tu - tv)
                if openworst is None or g > openworst:
                    openworst = g
    step("A1", "vine-internal edges=%d mapping-bad=%d openlaw-bad=%d worst=%s"
         % (inedges, mapbad, openbad, openworst))

    # --- exit edges + shortest first-returns ---
    exits = []  # (u0, edge)
    for u in VN:
        for e in adj[u]:
            if e[0] not in VN:
                exits.append((u, e))
    step("A2", "exit edges=%d" % len(exits))
    rec = []
    poss = []
    for (u0, e0) in exits:
        start = e0[0]
        prev = {start: None}
        pe = {}
        dq = deque([start])
        found = None
        while dq:
            u = dq.popleft()
            if u in VN:
                found = u
                break
            for e in adj[u]:
                w = e[0]
                if w not in prev:
                    prev[w] = u
                    pe[w] = e
                    dq.append(w)
        if found is None:
            rec.append({"u0": u0, "exit": list(e0[1:]), "return": None})
            continue
        tail = []
        nodes = [start]
        u = found
        while u != start:
            tail.append(pe[u])
            u = prev[u]
            nodes.append(u)
        tail.reverse()
        nodes.reverse()
        full = [e0] + tail
        A = sum(e[3] for e in full)
        B = sum(e[4] for e in full)
        ia0, ib0 = u0 // nS, u0 % nS
        ia1, ib1 = found // nS, found % nS
        maxdA = maxdB = 0
        nu = u0
        for e in full:
            ia, ib = nu // nS, nu % nS
            if e[1] == "D":
                maxdA = max(maxdA, dep[ia][e[2] - 1])
            else:
                maxdA = max(maxdA, dep[ia][e[2] - 1])
                maxdB = max(maxdB, dep[ib][e[2] - 1])
            nu = e[0]
        item = {"u0": u0, "u1": found, "len": len(full), "A": A, "B": B,
                "W": B - 2 * A,
                "exit": [e0[1], e0[2], e0[3], e0[4]],
                "word": [[e[1], e[2]] for e in full],
                "t0": roots[ia0] != roots[ib0],
                "t1": roots[ia1] != roots[ib1],
                "nD": sum(1 for e in full if e[1] == "D"),
                "nK": sum(1 for e in full if e[1] == "K"),
                "maxdA": maxdA, "maxdB": maxdB}
        rec.append(item)
        if B - 2 * A > 0:
            poss.append(item)
    import collections
    ws = [r["W"] for r in rec if "W" in r]
    wl = collections.Counter(ws)
    step("A3", "excursions=%d unreachable=%d Wmin=%d Wmax=%d positives=%d" % (
        len(rec), sum(1 for r in rec if "W" not in r),
        min(ws), max(ws), len(poss)))
    save("exc_n6.json", {"n": n, "exits": len(exits),
                         "W_hist": dict(sorted(wl.items())),
                         "excursions": rec, "positives": poss})

    # --- 5/3 achiever search ---
    word = [("K", 3), ("K", 6), ("K", 3), ("K", 4), ("K", 2), ("K", 1)]
    hits = []
    for u0 in range(nS * nS):
        u = u0
        A = B = 0
        ok = True
        seq = [u0]
        for (md, x) in word:
            nxt = None
            for e in adj[u]:
                if e[1] == md and e[2] == x:
                    nxt = e
                    break
            if nxt is None:
                ok = False
                break
            A += nxt[3]
            B += nxt[4]
            u = nxt[0]
            seq.append(u)
        if ok and u == u0 and (A, B) == (6, 10):
            hits.append({"u0": u0, "seq": seq})
    step("A4", "achiever starts closing A6B10: %d" % len(hits))
    ana = []
    for h in hits[:4]:
        states = []
        for i, u in enumerate(h["seq"]):
            ia, ib = u // nS, u % nS
            states.append({"pos": i, "ia": ia, "ib": ib,
                           "vine": [ia in vine, ib in vine]})
        ana.append({"u0": h["u0"], "states": states})
    save("achiever_n6.json", {"word": word, "nhits": len(hits),
                              "anatomy": ana})
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""WP-6 KILLSHOT: medium-small-n + decoupled-pusher burst hunt (C57).

Gap in prior coverage: exhaustive n=3,4,5 (2.28M clean); targeted n=16..512 (70k clean).
Medium-small n=6..24 vines: B-depth up to n (big e_B) with SMALL fresh-far pool
(sterile-rebuild must stall-or-save fast) and SMALL total A-id pool (N bounded).
Generator: decouple (DELETE far: A moves, B frozen) -> push (KEEP nearby-below x:
B-deepens via x, A ideally avoids) -> burst (repeat KEEP x: e_B big, fresh thin).
Hillclimb on (shortfall, gap, -slack, pressure).
Kill: shortfall>0 -> hallkill.json exit 2; gap>0 -> gckill.json exit 2.
Artifact: killshot.json. Sealed files untouched.
"""
from __future__ import annotations
import sys
import copy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_hallcore import build_graph, maxflow_cap3, delta_of, cands_from_cut
from wp6_offline import gc_gap
from wp6_tightest import vine, Rng
from solver import encode as E


def step(sid, msg):
    print("[WP-6][KILLSHOT %s] %s" % (sid, msg), flush=True)


import hashlib as _h


def eval_hist(n, T0, H):
    G = build_graph(n, T0, H)
    if G is None:
        return None
    f, nb, lv = maxflow_cap3(G)
    if nb - f > 0:
        return ("KILL", nb - f, nb, None)
    gap, _ = gc_gap(n, T0, H)
    if gap > 0:
        return ("GCKILL", gap, nb, None)
    best = None
    for name, Q in cands_from_cut(G, lv):
        if not Q:
            continue
        d, N = delta_of(G, set(Q))
        slack = -d
        if best is None or slack < best[0] or (slack == best[0] and len(Q) > best[2]):
            best = (slack, name, len(Q), len(N))
    return ("OK", best, nb, gap)


def gen_seed(s, tag):
    rng = Rng(("ks%d" % s).encode(), tag)
    r = rng(0)
    n = [6, 8, 10, 12, 16, 24, 32][r % 7]
    T0 = vine(n, (r >> 8) % 2 == 0)
    xc = 2 + (r >> 16) % max(1, n - 2)
    H = []
    L = 10 + (r >> 24) % 14
    for i in range(L):
        rr = Rng(("ks%d" % s).encode(), tag + b"h%d" % i)
        q = rr(1000 + i)
        op = (q >> 2) % 10
        if op < 3:
            # decouple far DELETE (A advances, B frozen)
            z = 1 if (q >> 9) % 2 == 0 else n
            if z == xc:
                z = 1 if xc != 1 else n
            H.append(["DELETE", z])
        elif op < 6:
            # nearby-below pusher: DELETE then KEEP adjacent to xc
            z = min(n, max(1, xc - 1 - (q >> 9) % 3))
            if z == xc:
                z = max(1, xc - 1)
            H.append(["DELETE", z])
            H.append(["KEEP", z])
        else:
            # demand burst on xc / neighbors
            H.append(["KEEP", min(n, max(1, xc + [-1, 0, 0, 1][(q >> 5) % 4]))])
    for _ in range(1 + (r >> 20) % 3):
        H.append(["KEEP", xc])
    return n, T0, H


def main() -> int:
    import json
    step("KS-00", "killshot medium-small-n hunt")
    TP = ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "killshot.json"
    bestslack = 10 ** 9
    best = None
    evals = 0
    holders = []
    try:
        dk = json.load(open(ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "starve_min.json"))
        holders.append((vine(dk["n"], dk["T0left"]), dk["Hmin"], dk["n"]))
    except Exception:
        pass
    BUDGET = 12000
    for s in range(400):
        n, T0, H = gen_seed(s, b"ks")
        v = eval_hist(n, T0, H)
        evals += 1
        if v is None:
            continue
        if v[0] == "KILL":
            step("KS-KILL", "HALL seed %d n=%d shortfall=%d nb=%d" % (s, n, v[1], v[2]))
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json").write_text(
                json.dumps({"kill": True, "n": n, "H": H}, indent=1, default=str), encoding="utf-8")
            TP.write_text(json.dumps({"kill": True, "seed": s, "n": n, "H": H}, indent=1, default=str), encoding="utf-8")
            return 2
        if v[0] == "GCKILL":
            step("KS-KILL", "GC seed %d gap=%d" % (s, v[1]))
            return 2
        _, b, nb, gap = v
        slack = b[0] if b else 10 ** 9
        holders.append((T0, H, n))
        if slack < bestslack:
            bestslack = slack
            best = (slack, n, nb, str(b))
            TP.write_text(json.dumps({"evals": evals, "bestslack": bestslack, "best": best}, indent=1, default=str), encoding="utf-8")
            step("KS-NEW", "seed %d n=%d slack=%s nb=%d %s" % (s, n, slack, nb, b[1] if b else ""))
            if slack <= 2:
                step("KS-TIGHT", "near-miss seed %d n=%d %s" % (s, n, b))
    holders = holders[-20:]
    step("KS-01", "seeds evals=%d bestslack=%s" % (evals, bestslack))
    it = 0
    while evals < BUDGET:
        it += 1
        r = int.from_bytes(_h.sha256(b"ksm|%d" % it).digest(), "big")
        T0, H, n = holders[(r >> 2) % len(holders)]
        H2 = copy.deepcopy(H)
        op = r % 6
        if op == 0 and H2:
            i = (r >> 5) % len(H2)
            H2[i][0] = "DELETE" if H2[i][0] == "KEEP" else "KEEP"
        elif op == 1 and H2:
            i = (r >> 5) % len(H2)
            H2[i][1] = 1 + (r >> 13) % n
        elif op == 2 and len(H2) < 60:
            H2.insert((r >> 5) % (len(H2) + 1), ["KEEP" if r % 2 else "DELETE", 1 + (r >> 13) % n])
        elif op == 3 and H2:
            recent = [a[1] for a in H2 if a[0] == "KEEP"][-3:]
            if recent:
                for _ in range(1 + (r >> 7) % 2):
                    H2.append(["KEEP", recent[(r >> 5) % len(recent)]])
            else:
                H2.append(["DELETE", 1 + (r >> 13) % n])
        elif op == 4 and H2:
            # burst duplicate: repeat a KEEP run
            keeps = [i for i, a in enumerate(H2) if a[0] == "KEEP"]
            if keeps:
                i = keeps[(r >> 5) % len(keeps)]
                H2.insert(i + 1, ["KEEP", H2[i][1]])
            else:
                del H2[(r >> 5) % len(H2)]
        elif len(H2) > 4:
            del H2[(r >> 5) % len(H2)]
        v = eval_hist(n, T0, H2)
        evals += 1
        if v is None:
            continue
        if v[0] == "KILL":
            step("KS-KILL", "HALL it=%d n=%d shortfall=%d nb=%d H=%s" % (it, n, v[1], v[2], H2))
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json").write_text(
                json.dumps({"kill": True, "n": n, "H": H2}, indent=1, default=str), encoding="utf-8")
            TP.write_text(json.dumps({"kill": True, "it": it, "n": n, "H": H2}, indent=1, default=str), encoding="utf-8")
            return 2
        if v[0] == "GCKILL":
            step("KS-KILL", "GC it=%d gap=%d" % (it, v[1]))
            return 2
        _, b, nb, gap = v
        slack = b[0] if b else 10 ** 9
        if slack < bestslack:
            bestslack = slack
            best = (slack, n, nb, str(b))
            TP.write_text(json.dumps({"evals": evals, "bestslack": bestslack, "best": best, "H": H2}, indent=1, default=str), encoding="utf-8")
            step("KS-NEW", "it=%d n=%d slack=%s nb=%d %s" % (it, n, slack, nb, b[1] if b else ""))
            holders.append((T0, H2, n))
            holders = holders[-20:]
            if slack <= 2:
                step("KS-TIGHT", "near-miss it=%d n=%d %s" % (it, n, b))
        elif (r >> 6) % 4 == 0:
            holders.append((T0, H2, n))
            holders = holders[-20:]
        if it % 2500 == 0:
            step("KS-02", "it=%d evals=%d bestslack=%s" % (it, evals, bestslack))
    step("KS-03", "evals=%d bestslack=%s best=%s NO KILL" % (evals, bestslack, best))
    try:
        prev = json.loads(TP.read_text(encoding="utf-8"))
    except Exception:
        prev = {}
    prev["evals"] = evals
    prev["bestslack"] = bestslack
    prev["nokill"] = True
    TP.write_text(json.dumps(prev, indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

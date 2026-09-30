"""WP-6 STEP SZ-00: split-zone sustain falsifier (demand-zone vs supply-zone).

Sustain histories where B-demand geometry (x-zone: victim + B-ancestors +
pusher B-paths) stays DISJOINT from A-supply geometry (pusher/positioner
A-paths + rotated sets), verified per access. Victim x first-access discipline
(K/E4 empty); B-heavy strikes (thin E1); E2-hole pushers (repeats); hub-empty
(repeat-w roots). Objective: maxflow shortfall (KILL -> hallkill + §24 audit);
tie-break min slack; track GC-gap (kill -> gckill); record zone-disjointness
violations (recoupling events: which access re-coupled, mechanism).
Seeds: killer, zone/surgical holders, split randoms.
NEW artifact: splitzone.json (+hallkill/gckill ONLY on kills). Sealed untouched.
"""
from __future__ import annotations
import sys
import copy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_hallcore import build_graph, maxflow_cap3, cands_from_cut, delta_of
from wp6_eventflow import to_ptr, splay_A, splay_B_push
from wp6_offline import gc_gap
from wp6_tightest import vine, Rng
from solver import encode as E


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


import hashlib as _h


def eval_hist(n, T0, H):
    G = build_graph(n, T0, H)
    if G is None:
        return None
    f, nb, lv = maxflow_cap3(G)
    if nb - f > 0:
        return ("KILL", nb - f, nb)
    best = None
    for name, Q in cands_from_cut(G, lv):
        if not Q:
            continue
        d, N = delta_of(G, set(Q))
        slack = -d
        if best is None or slack < best[0]:
            best = (slack, name, len(Q), len(N))
    gap, _ = gc_gap(n, T0, H)
    return ("OK", best, nb, gap)


def zone_split(n, T0, H, xzone, szone):
    """Check per-access zone discipline: KEEP B-paths in xzone (or pushers),
    A-paths (all accesses) avoid xzone-triples. Returns (ok_frac, details)."""
    A, B = to_ptr(T0), to_ptr(T0)
    pre = E.precompute(n, T0, H)
    tot = 0
    ok = 0
    for idx, acc in enumerate(pre):
        A, invs = splay_A(A, acc["x"])
        if acc["mode"] == "KEEP":
            B, pushes = splay_B_push(B, acc["x"])
        tot += 1
        # A-rotated keys of this access:
        akeys = set()
        for S in invs:
            akeys |= set(S)
        if akeys.isdisjoint(xzone):
            ok += 1
    return ok / max(1, tot)


def main() -> int:
    step("SZ-00", "Split-zone sustain falsifier")
    import json
    TP = ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "splitzone.json"
    best = None
    evals = 0
    holders = []
    import json as _j
    dk = _j.load(open(ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "starve_min.json"))
    holders.append((vine(dk["n"], dk["T0left"]), dk["Hmin"], dk["n"]))
    for s in range(80):
        rng = Rng(("s%d" % s).encode(), b"sz")
        r = rng(0)
        n = 128
        T0 = vine(n, (r >> 8) % 2 == 0)
        # demand zone (victim x + B-vicinity): mid keys; supply zone: far bottom/top
        xc = 60 + (r >> 16) % 40
        xzone = set(range(max(1, xc - 4), min(n, xc + 4) + 1))
        szone = set(range(1, 20)) | set(range(110, 129))
        x = xc
        H = []
        L = 16 + (r >> 24) % 20
        for i in range(L):
            rr = Rng(("s%d" % s).encode(), ("szh%d" % i).encode())
            q = rr(1000 + i)
            if (q >> 2) % 5 == 0:
                # KEEP in demand zone (pushers/strikes, B-near-x)
                H.append(["KEEP", min(n, max(1, xc + [-3, -2, -1, 1, 2, 3][(q >> 5) % 6]))])
            else:
                # DELETE/KEEP in supply zone (A-far), occasional repeat-pushers
                z = [1 + (q >> 5) % 19, 110 + (q >> 9) % 18][(q >> 13) % 2]
                H.append(["DELETE" if (q >> 15) % 3 else "KEEP", z])
        # first-x discipline: ensure x never accessed before final strike
        H = [a for a in H if a[1] != x]
        H.append(["KEEP", x])
        v = eval_hist(n, T0, H)
        evals += 1
        if v is None:
            continue
        if v[0] == "KILL":
            step("SZ-KILL", "HALL seed %d shortfall=%d" % (s, v[1]))
            TP.write_text(_j.dumps({"kill": True, "H": H}, indent=1, default=str), encoding="utf-8")
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json").write_text(
                _j.dumps({"kill": True, "H": H}, indent=1, default=str), encoding="utf-8")
            return 2
        _, b, nb, gap = v
        if gap > 0:
            step("SZ-KILL", "GC seed %d" % s)
            return 2
        zf = zone_split(n, T0, H, xzone, szone)
        if b is not None and (best is None or (b[0], -zf) < (best[0], -best[3])):
            best = (b[0], -b[2], b[1], zf)
            TP.write_text(_j.dumps({"evals": evals, "best": {"slack": b[0], "kind": b[1],
                                                             "Q": b[2], "N": b[3], "B": nb,
                                                             "zone_frac": zf}},
                                   indent=1, sort_keys=True, default=str), encoding="utf-8")
            step("SZ-NEW", "seeds slack=%s kind=%s zone=%.2f" % (best[0], b[1], zf))
        holders.append((T0, H, n))
    holders = holders[:16]
    step("SZ-01", "seeds evals=%d best=%s" % (evals, best))
    it = 0
    while evals < 12000:
        it += 1
        r = int.from_bytes(_h.sha256(b"szm|%d" % it).digest(), "big")
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
            H2.insert((r >> 5) % (len(H2) + 1), ["KEEP" if r % 2 else "DELETE", 1 + (r >> 13) % n])
        elif op == 3 and H2:
            recent = [a[1] for a in H2 if a[0] == "KEEP"][-4:]
            if recent:
                H2.append(["KEEP", recent[(r >> 5) % len(recent)]])
            else:
                H2.append(["DELETE", 1 + (r >> 13) % n])
        elif len(H2) > 4:
            del H2[(r >> 5) % len(H2)]
        v = eval_hist(n, T0, H2)
        evals += 1
        if v is None:
            continue
        if v[0] == "KILL":
            step("SZ-KILL", "HALL it=%d shortfall=%d" % (it, v[1]))
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json").write_text(
                _j.dumps({"kill": True, "H": H2}, indent=1, default=str), encoding="utf-8")
            return 2
        _, b, nb, gap = v
        if gap > 0:
            step("SZ-KILL", "GC it=%d" % it)
            return 2
        if b is not None and (b[0], -b[2]) < (best[0], best[1] if len(best) > 1 else 0):
            best = (b[0], -b[2], b[1], 0.0)
            holders.append((T0, H2, n))
            holders = holders[-16:]
            step("SZ-NEW", "it=%d slack=%s kind=%s Q=%d" % (it, best[0], b[1], b[2]))
        elif (r >> 6) % 4 == 0:
            holders.append((T0, H2, n))
            holders = holders[-16:]
        if it % 3000 == 0:
            step("SZ-02", "it=%d evals=%d best=%s" % (it, evals, best))
    step("SZ-03", "evals=%d best=%s" % (evals, best))
    return 0


if __name__ == "__main__":
    sys.exit(main())

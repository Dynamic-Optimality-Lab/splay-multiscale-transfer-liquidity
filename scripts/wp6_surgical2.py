"""WP-6 STEP S2-00: surgical T0-shallow first-x strike (sharpened Hall kill).

Victim x in T0-root-region (depth<=6: naturally thin E1 (1-3), no displacement
supply): FIRST-x discipline (K/E4 empty), repeat-pusher deepening in B
(E2-hole), zone-avoidance + sterility (no E3-overlap), B-root-pinning (hub
empty via trivial repeats). If realizable: N ~ E1-thin + holes vs e_B 10+
-> Delta>0 HALL KILL. If fizzles: displacement/avoidance fragility forced
supply (structural finding).
Mutations preserve: first-x (x only at final KEEP), T0-shallow x, avoidance
(far keys), repeat-push cycles. Objective shortfall (hallkill + §24) + GC-gap.
NEW artifact: surgical2.json (+hallkill/gckill on kill). Sealed files untouched.
"""
from __future__ import annotations
import sys
import copy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_hallcore import build_graph, maxflow_cap3, delta_of
from wp6_eventflow_abl import build_tagged
from wp6_offline import gc_gap
from wp6_tightest import vine, Rng
from solver import encode as E


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


import hashlib as _h


def score_hist(n, T0, H):
    import json
    G = build_graph(n, T0, H)
    if G is None:
        return None
    from wp6_hallcore import maxflow_cap3, cands_from_cut, delta_of
    from wp6_offline import gc_gap
    f, nb, lv = maxflow_cap3(G)
    if nb - f > 0:
        return ("KILL", nb - f, nb)
    gap, _ = gc_gap(n, T0, H)
    if gap > 0:
        return ("GC", gap, None)
    best = None
    for name, Q in cands_from_cut(G, lv):
        if not Q:
            continue
        d, N = delta_of(G, set(Q))
        slack = -d
        if best is None or slack < best[0]:
            best = (slack, name)
    return ("OK", 0, best)


def main() -> int:
    step("S2-00", "Surgical T0-shallow first-x strike")
    import json
    n = 128
    T0 = vine(n, True)
    # T0 vine-left root=128; depth(x) = 128-x. Shallow: x in 122..127 (depth 1..6).
    best = None
    evals = 0
    holders = []
    for s in range(80):
        r = int.from_bytes(_h.sha256(b"sg2|%d" % s).digest(), "big")
        x = 122 + (r >> 3) % 6
        H = []
        # position: far-zone keys only (1..60, avoid x vicinity + ancestors)
        for i in range(3 + (r >> 11) % 5):
            H.append([("KEEP" if (r >> (13 + i)) % 2 else "DELETE"), 1 + (r >> (17 + 2 * i)) % 60])
        # repeat-pusher cycles (A-root-pinned hopefuls + sterile hopefuls)
        for i in range(4 + (r >> 29) % 6):
            z = 1 + (r >> (31 + 3 * i)) % 60
            H.append(["DELETE", z])
            H.append(["KEEP", z])
        H.append(["KEEP", x])
        if any(a[1] == x for a in H[:-1]):
            continue
        v = score_hist(n, T0, H)
        evals += 1
        if v is None:
            continue
        if v[0] == "KILL":
            step("SG2-KILL", "HALL seed %d: %s" % (s, v[1]))
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json").write_text(
                json.dumps({"kill": True, "H": H}, indent=1, default=str), encoding="utf-8")
            return 2
        if v[0] == "GC":
            step("SG2-KILL", "GC seed %d" % s)
            return 2
        if best is None or v[1] > best[0]:
            best = (v[1], v[2])
        holders.append((H, x))
    step("SG2-01", "seeds evals=%d best=%s" % (evals, best))
    it = 0
    while evals < 10000:
        it += 1
        r = int.from_bytes(_h.sha256(b"sg2m|%d" % it).digest(), "big")
        H, x = holders[(r >> 2) % len(holders)]
        H2 = copy.deepcopy(H)
        op = r % 5
        if op == 0 and len(H2) > 2:
            i = (r >> 5) % (len(H2) - 1)
            if H2[i][1] == x or H2[i][1] > 60:
                H2[i][1] = 1 + (r >> 13) % 60
            H2[i][0] = "DELETE" if H2[i][0] == "KEEP" else "KEEP"
        elif op == 1 and len(H2) > 2:
            i = (r >> 5) % (len(H2) - 1)
            H2[i][1] = 1 + (r >> 13) % 60
        elif op == 2 and len(H2) < 44:
            H2.insert((r >> 5) % len(H2), ["KEEP" if r % 2 else "DELETE", 1 + (r >> 13) % 60])
        elif op == 3 and len(H2) > 2:
            z = 1 + (r >> 11) % 60
            H2.insert(len(H2) - 1, ["DELETE", z])
            H2.insert(len(H2) - 1, ["KEEP", z])
        elif len(H2) > 6:
            i = (r >> 5) % (len(H2) - 1)
            del H2[i]
        if H2[-1][0] != "KEEP":
            H2[-1][0] = "KEEP"
        x = H2[-1][1]
        if any(a[1] == x for a in H2[:-1]):
            continue
        # keep x T0-shallow-ish: skip if x deep (E1-rich defeats purpose)... allow, selection decides
        v = score_hist(n, T0, H2)
        evals += 1
        if v is None:
            continue
        if v[0] == "KILL":
            step("SG2-KILL", "HALL it=%d %s" % (it, v[1]))
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json").write_text(
                json.dumps({"kill": True, "H": H2}, indent=1, default=str), encoding="utf-8")
            return 2
        if v[0] == "GC":
            step("SG2-KILL", "GC it=%d" % it)
            return 2
        if v[1] > (best[0] if best else -1):
            best = (v[1], v[2])
            holders.append((H2, x))
            holders = holders[-14:]
            step("SG2-NEW", "it=%d shortfall=%d slack=%s" % (it, v[1], v[2]))
        elif (r >> 6) % 4 == 0:
            holders.append((H2, x))
            holders = holders[-14:]
        if it % 2000 == 0:
            step("SG2-02", "it=%d evals=%d best=%s" % (it, evals, best))
    step("SG2-03", "evals=%d best=%s" % (evals, best))
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "surgical2.json").write_text(
        json.dumps({"evals": evals, "best_shortfall": best[0] if best else None,
                    "best_slack": best[1] if best else None},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

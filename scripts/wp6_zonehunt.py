"""WP-6 STEP ZH-00: shared-zone sustain Hall hunt (pool-exhaustion targeting).

Sustained walks confined to a 3-7-key zone (40-70 accesses) with B-heavy bias:
fresh keys through shared geometry drain the zone pool without K-replenish
(C37 mechanism pushed to its limit). Objective: max-flow shortfall (KILL >0 ->
hallkill + §15 path); tie-break min slack. Mutations preserve zone-confinement
(small steps, repeats, mode flips) + occasional zone-shift (new pools).
Seeds: C37 killer (zone walk inside), zone-confined randoms, HH holders.
NEW artifact: zonehunt.json (+hallkill.json on kill). Sealed files untouched.
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
from wp6_tightest import vine, Rng
from wp6_offline import gc_gap
from solver import encode as E


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


import hashlib as _h


def zone_H(rr, n, L, c, w):
    H = []
    x = min(n, max(1, c))
    for i in range(L):
        r = rr(1000 + i)
        if i % 5 == 4:
            y = min(n, max(1, x + [-32, -16, 16, 32][r % 4]))
            H.append(["DELETE", y if y != x else 1])
            H.append(["KEEP", x])
        else:
            H.append(["KEEP" if r % 3 else "DELETE", x])
        x = min(n, max(1, x + [-w, -1, 0, 1, w][(r >> 9) % 5]))
        x = min(n, max(1, c + (x - c) // 2 + [-1, 0, 1][(r >> 13) % 3]))
    return H


def eval_hist(n, T0, H):
    G = build_graph(n, T0, H)
    if G is None:
        return None
    f, nb, lv = maxflow_cap3(G)
    sf = nb - f
    best = None
    if sf > 0:
        return ("KILL", sf, nb)
    # min slack over cut + access slices
    from wp6_hallcore import cands_from_cut
    for name, Q in cands_from_cut(G, lv):
        if not Q:
            continue
        d, N = delta_of(G, set(Q))
        slack = -d
        if best is None or slack < best[0]:
            best = (slack, name, len(Q), len(N))
    gap, _ = gc_gap(n, T0, H)
    return ("OK", best, nb, gap)


def main() -> int:
    step("ZH-00", "Shared-zone sustain Hall hunt")
    import json
    best_sf = 0
    best_slack = None
    evals = 0
    holders = []
    import json as _j
    dk = _j.load(open(ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "starve_min.json"))
    holders.append((vine(dk["n"], dk["T0left"]), dk["Hmin"], dk["n"], 64))
    for s in range(60):
        rng = Rng(("s%d" % s).encode(), b"zh")
        r = rng(0)
        n = 128
        T0 = vine(n, (r >> 8) % 2 == 0)
        c = 8 + (r >> 16) % 112
        w = 2 + (r >> 24) % 3
        rr = Rng(("s%d" % s).encode(), b"zhh")
        H = zone_H(rr, n, 40 + (r >> 28) % 30, c, w)
        v = eval_hist(n, T0, H)
        evals += 1
        if v is None:
            continue
        if v[0] == "KILL":
            step("ZH-KILL", "HALL seed %d shortfall=%d" % (s, v[1]))
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json").write_text(
                _j.dumps({"kill": True, "H": H}, indent=1, default=str), encoding="utf-8")
            return 2
        _, b, nb, gap = v
        if gap > 0:
            step("ZH-KILL", "GC seed %d" % s)
            return 2
        if b is not None and (best_slack is None or b[0] < best_slack[0]):
            best_slack = (b[0], b[1])
        holders.append((T0, H, n, c))
    holders = holders[:16]
    step("ZH-01", "seeds evals=%d slack=%s" % (evals, best_slack))
    it = 0
    while evals < 15000:
        it += 1
        r = int.from_bytes(_h.sha256(b"zhm|%d" % it).digest(), "big")
        T0, H, n, c = holders[(r >> 2) % len(holders)]
        H2 = copy.deepcopy(H)
        op = r % 5
        if op == 0 and H2:
            i = (r >> 5) % len(H2)
            H2[i][0] = "DELETE" if H2[i][0] == "KEEP" else "KEEP"
        elif op == 1 and H2:
            i = (r >> 5) % len(H2)
            # zone-confined key mutation
            H2[i][1] = min(n, max(1, c + ((r >> 13) % 9) - 4))
        elif op == 2 and len(H2) < 80:
            H2.insert((r >> 5) % (len(H2) + 1),
                      ["KEEP" if r % 2 else "DELETE", min(n, max(1, c + ((r >> 13) % 9) - 4))])
        elif op == 3 and H2:
            recent = [a[1] for a in H2][-5:]
            base = recent[(r >> 5) % len(recent)] if recent else c
            H2.append(["KEEP", min(n, max(1, base + [-1, 0, 1][(r >> 9) % 3]))])
        elif len(H2) > 6:
            del H2[(r >> 5) % len(H2)]
        v = eval_hist(n, T0, H2)
        evals += 1
        if v is None:
            continue
        if v[0] == "KILL":
            step("ZH-KILL", "HALL it=%d shortfall=%d" % (it, v[1]))
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json").write_text(
                _j.dumps({"kill": True, "H": H2}, indent=1, default=str), encoding="utf-8")
            return 2
        _, b, nb, gap = v
        if gap > 0:
            step("ZH-KILL", "GC it=%d" % it)
            return 2
        if b is not None and (best_slack is None or b[0] < best_slack[0]):
            best_slack = (b[0], b[1])
            holders.append((T0, H2, n, c))
            holders = holders[-16:]
            step("ZH-NEW", "it=%d slack=%s kind=%s" % (it, best_slack, b[1]))
        elif (r >> 6) % 4 == 0:
            holders.append((T0, H2, n, c))
            holders = holders[-16:]
        if it % 3000 == 0:
            step("ZH-02", "it=%d evals=%d slack=%s" % (it, evals, best_slack))
    step("ZH-03", "evals=%d slack=%s" % (evals, best_slack))
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "zonehunt.json").write_text(
        _j.dumps({"evals": evals, "best_slack": best_slack},
                 indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

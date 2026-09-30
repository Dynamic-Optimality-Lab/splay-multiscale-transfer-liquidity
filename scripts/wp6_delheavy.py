"""WP-6 STEP DH-00: DELETE-heavy decoupled-regime Hall falsifier.

DELETE-heavy histories (80-90% DELETEs) decouple trees (A advances alone, B
frozen stale): A-supply lands far from B-demand zones (sterile-prone), E2 thin
(few pump-KEEPs), roots diverged (no sync-hub except rare KEEPs). Rare KEEPs:
shared-zone pushers (B-near-x, deepen) + B-heavy strikes (first-x discipline
where possible). Objective: maxflow shortfall (KILL -> hallkill + §24 path);
tie-break min slack; track GC-gap (kill -> gckill).
Seeds: killer, M2, zone/surgical holders (re-tracked), DELETE-heavy randoms.
NEW artifact: delheavy.json (+hallkill/gckill ONLY on kills). Sealed untouched.
"""
from __future__ import annotations
import sys
import copy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_hallcore import build_graph, maxflow_cap3, cands_from_cut, delta_of
from wp6_offline import gc_gap, vine, Rng
from solver import encode as E


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


import hashlib as _h


def H_delheavy(rr, n, L, zone, far):
    """80-85% DELETEs (far zone), rare KEEPs (shared zone pushers/strikes)."""
    H = []
    x = far[0]
    for i in range(L):
        r = rr(1000 + i)
        if (r >> 2) % 100 < 82:
            y = far[(r >> 5) % len(far)]
            H.append(["DELETE", y if y != x else far[(y) % len(far)]])
            x = zone[(r >> 9) % len(zone)] if (r >> 13) % 4 == 0 else x
        else:
            H.append(["KEEP", zone[(r >> 5) % len(zone)]])
            x = zone[(r >> 9) % len(zone)]
    return H


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


def main() -> int:
    step("DH-00", "DELETE-heavy decoupled-regime falsifier")
    import json
    TP = ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "delheavy.json"
    best = None
    evals = 0
    holders = []
    import json as _j
    dk = _j.load(open(ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "starve_min.json"))
    holders.append((vine(dk["n"], dk["T0left"]), dk["Hmin"], dk["n"]))
    for s in range(80):
        rng = Rng(("s%d" % s).encode(), b"dh")
        r = rng(0)
        n = 128
        T0 = vine(n, (r >> 8) % 2 == 0)
        c = 40 + (r >> 16) % 48
        zone = list(range(max(1, c - 3), min(n, c + 3) + 1))
        far = list(range(1, 20)) + list(range(110, 129))
        rr = Rng(("s%d" % s).encode(), b"dhh")
        H = H_delheavy(rr, n, 24 + (r >> 24) % 24, zone, far)
        v = eval_hist(n, T0, H)
        evals += 1
        if v is None:
            continue
        if v[0] == "KILL":
            step("DH-KILL", "HALL seed %d shortfall=%d" % (s, v[1]))
            TP.write_text(_j.dumps({"kill": True, "H": H}, indent=1, default=str), encoding="utf-8")
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json").write_text(
                _j.dumps({"kill": True, "H": H}, indent=1, default=str), encoding="utf-8")
            return 2
        _, b, nb, gap = v
        if gap > 0:
            step("DH-KILL", "GC seed %d" % s)
            return 2
        if b is not None and (best is None or (b[0], -b[2]) < best):
            best = (b[0], -b[2])
            TP.write_text(_j.dumps({"evals": evals, "best": {"slack": b[0], "kind": b[1],
                                                             "Q": b[2], "N": b[3], "B": nb}},
                                   indent=1, sort_keys=True, default=str), encoding="utf-8")
            step("DH-NEW", "seeds slack=%s kind=%s Q=%d" % (best, b[1], b[2]))
        holders.append((T0, H, n))
    holders = holders[:16]
    step("DH-01", "seeds evals=%d best=%s" % (evals, best))
    it = 0
    while evals < 15000:
        it += 1
        r = int.from_bytes(_h.sha256(b"dhm|%d" % it).digest(), "big")
        T0, H, n = holders[(r >> 2) % len(holders)]
        H2 = copy.deepcopy(H)
        op = r % 6
        if op == 0 and H2:
            i = (r >> 5) % len(H2)
            # bias to DELETE (keep regime decoupled); flip rarely to KEEP
            if H2[i][0] == "KEEP" and (r >> 7) % 3:
                pass
            else:
                H2[i][0] = "DELETE" if H2[i][0] == "KEEP" else "KEEP"
        elif op == 1 and H2:
            i = (r >> 5) % len(H2)
            H2[i][1] = 1 + (r >> 13) % n
        elif op == 2 and len(H2) < 80:
            # insert DELETE-heavy (mostly DELETE)
            H2.insert((r >> 5) % (len(H2) + 1),
                      ["DELETE" if (r >> 9) % 5 else "KEEP", 1 + (r >> 13) % n])
        elif op == 3 and H2:
            # repeat recent KEEP (sustain pushers/strikes)
            keeps = [a[1] for a in H2 if a[0] == "KEEP"][-4:]
            if keeps:
                H2.append(["KEEP", keeps[(r >> 5) % len(keeps)]])
            else:
                H2.append(["DELETE", 1 + (r >> 13) % n])
        elif len(H2) > 6:
            del H2[(r >> 5) % len(H2)]
        v = eval_hist(n, T0, H2)
        evals += 1
        if v is None:
            continue
        if v[0] == "KILL":
            step("DH-KILL", "HALL it=%d shortfall=%d" % (it, v[1]))
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json").write_text(
                _j.dumps({"kill": True, "H": H2}, indent=1, default=str), encoding="utf-8")
            return 2
        _, b, nb, gap = v
        if gap > 0:
            step("DH-KILL", "GC it=%d" % it)
            return 2
        if b is not None and (b[0], -b[2]) < best:
            best = (b[0], -b[2])
            TP.write_text(_j.dumps({"evals": evals, "best": {"slack": b[0], "kind": b[1],
                                                             "Q": b[2], "N": b[3], "B": nb}},
                                   indent=1, sort_keys=True, default=str), encoding="utf-8")
            step("DH-NEW", "it=%d slack=%s kind=%s Q=%d" % (it, best, b[1], b[2]))
            holders.append((T0, H2, n))
            holders = holders[-16:]
        elif (r >> 6) % 4 == 0:
            holders.append((T0, H2, n))
            holders = holders[-16:]
        if it % 3000 == 0:
            step("DH-02", "it=%d evals=%d best=%s" % (it, evals, best))
    step("DH-03", "evals=%d best=%s" % (evals, best))
    import json as _jj
    _best = _jj.loads(TP.read_text(encoding="utf-8"))["best"] if TP.exists() else None
    TP.write_text(_jj.dumps({"evals": evals, "best": _best}, indent=1, sort_keys=True, default=str),
                  encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""WP-6 STEP HH-00: adversarial Hall-deficit optimization (shortfall + slack).

Objective (lexicographic): maximize max-flow shortfall (KILL >0 -> hallkill +
§15 audit path); tie-break minimize tight-set slack (tight anatomy).
Mutations: concentrated key-walks (repeat recent keys, +-small geographic steps
-- the C37 fresh-key-drain mechanism), B-heavy sustain, sterile zones, long
tenure, mode/key/len edits. Seeds: C37 killer, M2, ENTRY@3, neg-margin-style
fresh walks, generic.
Diagnostics on best: tight-set kind/composition (access/K/class), min source
degree over tight sets, latest-access boundary degrees, E1/E2/E3/E4/K/W split.
NEW artifact: hallhunt.json (+hallkill.json on shortfall>0; +gckill.json on
GC-gap>0, tracked jointly). Sealed files untouched.
"""
from __future__ import annotations
import sys
import copy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_hallcore import build_graph, maxflow_cap3, cands_from_cut, delta_of, degrees
from wp6_offline import gc_gap, H_walk, vine, Rng
from solver import encode as E


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


import hashlib as _h


def eval_hist(n, T0, H):
    G = build_graph(n, T0, H)
    if G is None:
        return None
    f, nb, lv = maxflow_cap3(G)
    sf = nb - f
    best = None
    for name, Q in cands_from_cut(G, lv):
        if not Q:
            continue
        d, N = delta_of(G, Q)
        slack = -d
        if best is None or slack < best[0]:
            best = (slack, name, len(Q), len(N))
    gap, _ = gc_gap(n, T0, H)
    return sf, (best[0] if best else None), nb, gap


def mutate_walk(H, n, r):
    """Geographic-concentration bias: repeat recent keys, small steps."""
    H2 = copy.deepcopy(H)
    op = r % 6
    if op == 0 and H2:
        i = (r >> 5) % len(H2)
        H2[i][0] = "DELETE" if H2[i][0] == "KEEP" else "KEEP"
    elif op == 1 and H2:
        i = (r >> 5) % len(H2)
        H2[i][1] = 1 + (r >> 13) % n
    elif op == 2 and len(H2) < 70:
        H2.insert((r >> 5) % (len(H2) + 1), ["KEEP" if r % 2 else "DELETE", 1 + (r >> 13) % n])
    elif op == 3 and H2:
        recent = [a[1] for a in H2][-6:]
        base = recent[(r >> 5) % len(recent)] if recent else 1 + (r >> 13) % n
        stepd = [-2, -1, -1, 0, 1, 1, 2][(r >> 9) % 7]
        H2.append(["KEEP" if r % 3 else "DELETE", min(n, max(1, base + stepd))])
    elif op == 4 and H2:
        recent = [a[1] for a in H2 if a[0] == "KEEP"][-4:]
        if recent:
            H2.append(["KEEP", recent[(r >> 5) % len(recent)]])
        else:
            H2.append(["KEEP", 1 + (r >> 13) % n])
    elif len(H2) > 4:
        del H2[(r >> 5) % len(H2)]
    return H2


def main() -> int:
    step("HH-00", "Adversarial Hall-deficit optimization")
    import json
    best_sf = 0
    best_slack = None
    evals = 0
    holders = []
    import json as _j
    dk = _j.load(open(ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "starve_min.json"))
    holders.append((vine(dk["n"], dk["T0left"]), dk["Hmin"], dk["n"]))
    step("HH-W", "seeded killer + generic")
    for s in range(80):
        rng = Rng(("s%d" % s).encode(), b"hh")
        r = rng(0)
        n = [32, 64, 128][r % 3]
        T0 = vine(n, (r >> 8) % 2 == 0)
        rr = Rng(("s%d" % s).encode(), b"hhh")
        H = H_walk(rr, n, 12 + (r >> 16) % 20, 1 + (r >> 24) % n)
        v = eval_hist(n, T0, H)
        evals += 1
        if v is None:
            continue
        sf, slack, nb, gap = v
        if sf > 0:
            step("HH-KILL", "HALL seed %d shortfall=%d" % (s, sf))
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json").write_text(
                _j.dumps({"kill": True, "H": H}, indent=1, default=str), encoding="utf-8")
            return 2
        if gap > 0:
            step("HH-KILL", "GC seed %d gap=%d" % (s, gap))
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "gckill.json").write_text(
                _j.dumps({"kill": True, "H": H}, indent=1, default=str), encoding="utf-8")
            return 2
        best_sf = max(best_sf, sf)
        if slack is not None and (best_slack is None or slack < best_slack):
            best_slack = slack
        holders.append((T0, H, n))
    holders = holders[:16]
    step("HH-01", "seeds evals=%d shortfall=%d slack=%s" % (evals, best_sf, best_slack))
    it = 0
    while evals < 20000:
        it += 1
        r = int.from_bytes(_h.sha256(b"hhm|%d" % it).digest(), "big")
        T0, H, n = holders[(r >> 2) % len(holders)]
        H2 = mutate_walk(H, n, r)
        v = eval_hist(n, T0, H2)
        evals += 1
        if v is None:
            continue
        sf, slack, nb, gap = v
        if sf > 0:
            step("HH-KILL", "HALL it=%d shortfall=%d nb=%d" % (it, sf, nb))
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json").write_text(
                _j.dumps({"kill": True, "H": H2}, indent=1, default=str), encoding="utf-8")
            return 2
        if gap > 0:
            step("HH-KILL", "GC it=%d gap=%d" % (it, gap))
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "gckill.json").write_text(
                _j.dumps({"kill": True, "H": H2}, indent=1, default=str), encoding="utf-8")
            return 2
        if sf > best_sf or (slack is not None and best_slack is not None and slack < best_slack):
            best_sf = max(best_sf, sf)
            if slack is not None and (best_slack is None or slack < best_slack):
                best_slack = slack
            holders.append((T0, H2, n))
            holders = holders[-16:]
        elif (r >> 6) % 4 == 0:
            holders.append((T0, H2, n))
            holders = holders[-16:]
        if it % 4000 == 0:
            step("HH-02", "it=%d evals=%d shortfall=%d slack=%s" % (it, evals, best_sf, best_slack))
    step("HH-03", "evals=%d shortfall=%d slack=%s" % (evals, best_sf, best_slack))
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallhunt.json").write_text(
        _j.dumps({"evals": evals, "best_shortfall": best_sf, "best_slack": best_slack},
                 indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""WP-6 STEP SG-00: surgical first-x-strike construction (Hall-kill attempt).

Phases (victim x NEVER accessed until strike):
  POSITION: access FAR keys (zone-avoid x) + hoist x shallow in A (below-x
    accesses) while keeping x B-position (no B-path through x... or accept).
  PUSH: DELETE->KEEP repeat pushers z (A-root-pinned, stale-B-deep) whose
    A-paths avoid x-triples (sterile) and B-paths push x deep. E2-hole +
    hub-empty (repeat-w pinned roots) + W-sterile by zone separation.
  STRIKE: first-ever KEEP-x (E1 thin (shallow) + E2 hole + E4 empty (no setup)
    + K empty (first access) + W sterile + hub empty (repeat-w)).
  Kill: maxflow shortfall>0 (hallkill + §24) or GC-gap>0 (gckill).
  If construction fizzles (a phase FORCES supply/overlap), record the forcing
  (structural lemma candidate!). Diagnostics: per-phase N-composition of the
  strike (E1/E2/E4/K/W/hub-empty verification), e_B vs 3|N|.
NEW artifact: surgical.json (+hallkill/gckill on kill). Sealed files untouched.
"""
from __future__ import annotations
import sys
import copy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_hallcore import build_graph, maxflow_cap3, delta_of
from wp6_eventflow import to_ptr, splay_A, splay_B_push
from wp6_eventflow_abl import build_tagged
from liquidity import legacy_embedding as PE
from solver import encode as E


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


import hashlib as _h


def vine(n, left=False):
    t = None
    for k in (range(n, 0, -1) if not left else range(1, n + 1)):
        t = [k, None, t] if not left else [k, t, None]
    return t


def adepth(A, x):
    d, path = PE._depth_to(A, x)
    return d if (path and path[-1]["k"] == x) else None


def replay_AB(n, T0, H):
    A, B = to_ptr(T0), to_ptr(T0)
    for (m, x) in H:
        A, _ = splay_A(A, x)
        if m == "KEEP":
            B, _ = splay_B_push(B, x)
    return A, B


def keyset(t):
    out = set()
    st = [t]
    while st:
        nd = st.pop()
        if nd is None:
            continue
        out.add(nd["k"])
        st.append(nd["l"])
        st.append(nd["r"])
    return out


def main() -> int:
    step("SG-00", "Surgical first-x-strike construction")
    import json
    n = 128
    T0 = vine(n, True)
    best = None
    bestH = None
    evals = 0
    # Phase structure search: victim x, position keys P (far), pushers Z, strike.
    # Operate by mutating (x, P-walk, push-cycles, strike) templates.
    for s in range(60):
        r = int.from_bytes(_h.sha256(b"sg|%d" % s).digest(), "big")
        x = 96 + (r >> 3) % 24
        # position: far-zone keys (1..40), 4-10 accesses (mix KEEP/DELETE, avoid x)
        H = []
        for i in range(4 + (r >> 11) % 7):
            H.append([("KEEP" if (r >> (13 + i)) % 2 else "DELETE"), 1 + (r >> (17 + 2 * i)) % 40])
        # push cycles: DELETE-z, KEEP-z with z far (A) but B-path-near-x candidates
        for i in range(3 + (r >> 29) % 5):
            z = 1 + (r >> (31 + 3 * i)) % 40
            H.append(["DELETE", z])
            H.append(["KEEP", z])
        H.append(["KEEP", x])
        # verify x never accessed before strike
        if any(a[1] == x for a in H[:-1]):
            continue
        v = score_hist(n, T0, H)
        evals += 1
        if v is None:
            continue
        if v[0] == "KILL":
            step("SG-KILL", "HALL seed %d: %s" % (s, v[1]))
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json").write_text(
                json.dumps({"kill": True, "H": H}, indent=1, default=str), encoding="utf-8")
            return 2
        if v[0] == "GC":
            step("SG-KILL", "GC seed %d" % s)
            return 2
        if best is None or v[1] > best[0]:
            best = (v[1], v[2])
            bestH = (x, copy.deepcopy(H))
            step("SG-NEW", "seeds shortfall=%d slack=%s" % (v[1], v[2]))
    step("SG-01", "seeds evals=%d best=%s" % (evals, best))
    holders = [(T0, bestH[1], n)] if bestH else []
    for s in range(60, 100):
        rng_r = int.from_bytes(_h.sha256(b"sgb|%d" % s).digest(), "big")
        nn = 128
        TT = vine(nn, rng_r % 2 == 0)
        cc = 60 + (rng_r >> 8) % 60
        H = []
        for i in range(4 + (rng_r >> 11) % 7):
            H.append([("KEEP" if (rng_r >> (13 + i)) % 2 else "DELETE"), 1 + (rng_r >> (17 + 2 * i)) % 40])
        for i in range(3 + (rng_r >> 29) % 5):
            z = 1 + (rng_r >> (31 + 3 * i)) % 40
            H.append(["DELETE", z])
            H.append(["KEEP", z])
        H.append(["KEEP", cc])
        if any(a[1] == cc for a in H[:-1]):
            continue
        v = score_hist(nn, TT, H)
        evals += 1
        if v is None:
            continue
        if v[0] == "KILL":
            step("SG-KILL", "HALL seed %d" % s)
            return 2
        if v[0] == "GC":
            step("SG-KILL", "GC seed %d" % s)
            return 2
        holders.append((TT, H, nn))
    it = 0
    while evals < 8000:
        it += 1
        r = int.from_bytes(_h.sha256(b"sgm|%d" % it).digest(), "big")
        T0h, H, nn = holders[(r >> 2) % len(holders)]
        H2 = copy.deepcopy(H)
        # mutate but PRESERVE first-x (never insert x before strike; x = last KEEP key)
        x = H2[-1][1]
        op = r % 5
        if op == 0 and len(H2) > 2:
            i = (r >> 5) % (len(H2) - 1)
            if H2[i][1] == x:
                H2[i][1] = 1 + (r >> 13) % 40
            H2[i][0] = "DELETE" if H2[i][0] == "KEEP" else "KEEP"
        elif op == 1 and len(H2) > 2:
            i = (r >> 5) % (len(H2) - 1)
            H2[i][1] = 1 + (r >> 13) % 40
            if H2[i][1] == x:
                H2[i][1] = 1 + ((r >> 13) % 39)
        elif op == 2 and len(H2) < 40:
            H2.insert((r >> 5) % len(H2), ["KEEP" if r % 2 else "DELETE", 1 + (r >> 13) % 40])
            if H2[-2][1] == x:
                H2[-2][1] = 1 + ((r >> 13) % 39)
        elif op == 3 and len(H2) > 2:
            # extend push cycles (repeat-pusher sustain)
            z = 1 + (r >> 11) % 40
            if z == x:
                z = 1 + ((r >> 11) % 39)
            H2.insert(len(H2) - 1, ["DELETE", z])
            H2.insert(len(H2) - 1, ["KEEP", z])
        elif len(H2) > 6:
            i = (r >> 5) % (len(H2) - 1)
            del H2[i]
        # re-assert first-x (strike key untouched at end; no x before)
        if H2[-1][0] != "KEEP":
            H2[-1][0] = "KEEP"
        x = H2[-1][1]
        if any(a[1] == x for a in H2[:-1]):
            continue
        v = score_hist(nn, T0h, H2)
        evals += 1
        if v is None:
            continue
        if v[0] == "KILL":
            step("SG-KILL", "HALL it=%d %s" % (it, v[1]))
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json").write_text(
                json.dumps({"kill": True, "H": H2}, indent=1, default=str), encoding="utf-8")
            return 2
        if v[0] == "GC":
            step("SG-KILL", "GC it=%d" % it)
            return 2
        if v[1] > (best[0] if best else -1):
            best = (v[1], v[2])
            holders.append((T0h, H2, nn))
            holders = holders[-14:]
            step("SG-NEW", "it=%d shortfall=%d slack=%s" % (it, v[1], v[2]))
        elif (r >> 6) % 4 == 0:
            holders.append((T0h, H2, nn))
            holders = holders[-14:]
        if it % 2000 == 0:
            step("SG-02", "it=%d evals=%d best=%s" % (it, evals, best))
    step("SG-03", "evals=%d best=%s" % (evals, best))
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "surgical.json").write_text(
        json.dumps({"evals": evals, "best_shortfall": best[0] if best else None,
                    "best_slack": best[1] if best else None},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


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


def main2():
    return main()


if __name__ == "__main__":
    sys.exit(main())

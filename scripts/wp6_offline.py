"""WP-6 STEP OF-00: offline fallback test (GC-STATIC + GC-direct).

Stage B (online greedy) is REFUTED (starve_min.json). Fallback: OFFLINE cap-3
causal assignment (past-only E1+E2+E3+E4+E7 edges, sited cap 3) via max-flow.
If offline ALWAYS saturates -> GC-STATIC conjecture (finite) -> GC (counting:
E_B <= 3*S_A) -> ledger chain rebuilds WITHOUT online Stage B.
  1. Killer Hmin offline test (saturate? shortfall? Hall set?).
  2. Adversarial offline falsifier (maximize shortfall; shortfall>0 = Hall
     violator = OFFLINE KILL, bank + exit 2).
  3. GC-direct gap: max over prefixes (E_B - 3*S_A) (GC kill hunt; exit 2).
NEW artifact: offline.json (+hallkill.json on offline kill; +gckill.json on GC
kill). Sealed files untouched.
"""
from __future__ import annotations
import sys
import copy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_eventflow_abl import build_tagged
from wp6_eventflow import Dinic
from solver import encode as E


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


import hashlib as _h


def vine(n, left=False):
    t = None
    for k in (range(n, 0, -1) if not left else range(1, n + 1)):
        t = [k, None, t] if not left else [k, t, None]
    return t


class Rng:
    def __init__(self, s, tag):
        self.s = s
        self.tag = tag

    def __call__(self, c):
        return int.from_bytes(_h.sha256(self.tag + b"|%s|%d" % (self.s, c)).digest(), "big")


def offline_shortfall(n, T0, H):
    """Max-flow cap-3 saturate B-demand. Returns (shortfall, nb) or -2 illegal."""
    pre = E.precompute(n, T0, H)
    res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
    if res["violations"]:
        return -2, None
    g = build_tagged(n, T0, H)
    Aevs, Bevs, elig = g["Aevs"], g["Bevs"], g["elig"]
    na, nb = len(Aevs), len(Bevs)
    if nb == 0:
        return 0, 0
    N = 2 + na + nb
    S, T = 0, N - 1
    D = Dinic(N)
    for i, (_, sited) in enumerate(Aevs):
        if sited:
            D.add(S, 1 + i, 3)
    for j in range(nb):
        D.add(1 + na + j, T, 1)
    for j, e in enumerate(elig):
        for k in e:
            for i in e[k]:
                if Aevs[i][1]:
                    D.add(1 + i, 1 + na + j, 1)
    f, _ = D.flow(S, T)
    return nb - f, nb


def gc_gap(n, T0, H):
    """Max over KEEP-prefixes of (E_B - 3*S_A). Uses exec_counts? No: count
    StepEvs directly via precompute (Bev lens + sites). S_A = sited A count."""
    from wp6_eventflow import to_ptr, splay_A, splay_B_push
    pre = E.precompute(n, T0, H)
    A, B = to_ptr(T0), to_ptr(T0)
    SA = EB = 0
    worst = 0
    worst_at = None
    for idx, acc in enumerate(pre):
        A, _ = splay_A(A, acc["x"])
        SA += sum(1 for z in acc["sites"] if z)
        if acc["mode"] == "KEEP":
            B, pushes = splay_B_push(B, acc["x"])
            EB += len(acc["Bev"])
            if EB - 3 * SA > worst:
                worst, worst_at = EB - 3 * SA, idx
    return worst, worst_at


def H_walk(rr, n, L, x0):
    H = []
    x = x0
    for i in range(L):
        r = rr(1000 + i)
        if i % 4 == 3:
            y = min(n, max(1, x + [-32, -16, 16, 32][r % 4]))
            H.append(["DELETE", y if y != x else 1])
            H.append(["KEEP", x])
        else:
            H.append(["KEEP" if r % 3 else "DELETE", x])
        x = min(n, max(1, x + [-16, -8, -4, -1, 1, 4, 8, 16][(r >> 9) % 8]))
    return H


def main() -> int:
    step("OF-00", "Offline fallback test")
    import json
    # 1. killer offline test
    dk = json.load(open(ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "starve_min.json"))
    n, T0, H = dk["n"], vine(dk["n"], dk["T0left"]), dk["Hmin"]
    sf, nb = offline_shortfall(n, T0, H)
    step("OF-01", "killer offline: shortfall=%s nb=%s (0 = offline survives)" % (sf, nb))
    # 2+3. adversarial: seeds + hillclimb, joint objective (shortfall, gc_gap)
    worst_sf = 0
    worst_sf_ex = None
    worst_gap = 0
    worst_gap_ex = None
    holders = [(T0, H, n)]
    evals = 0
    for s in range(80):
        rng = Rng(("s%d" % s).encode(), b"of")
        r = rng(0)
        nn = [32, 64, 128][r % 3]
        T = vine(nn, (r >> 8) % 2 == 0)
        rr = Rng(("s%d" % s).encode(), b"ofh")
        Hh = H_walk(rr, nn, 12 + (r >> 16) % 22, 1 + (r >> 24) % nn)
        sfh, nbh = offline_shortfall(nn, T, Hh)
        gaph, _ = gc_gap(nn, T, Hh)
        evals += 1
        if sfh == -2:
            continue
        if sfh > 0:
            step("OF-KILL", "OFFLINE HALL KILL seed %d shortfall=%d" % (s, sfh))
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json").write_text(
                json.dumps({"kill": True, "H": Hh}, indent=1, default=str), encoding="utf-8")
            return 2
        if gaph > 0:
            step("OF-KILL", "GC KILL seed %d gap=%d" % (s, gaph))
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "gckill.json").write_text(
                json.dumps({"kill": True, "H": Hh}, indent=1, default=str), encoding="utf-8")
            return 2
        worst_sf = max(worst_sf, sfh)
        worst_gap = max(worst_gap, gaph)
        holders.append((T, Hh, nn))
    holders = holders[:14]
    step("OF-02", "seeds evals=%d worst_shortfall=%d worst_gap=%d" % (evals, worst_sf, worst_gap))
    it = 0
    while evals < 6000:
        it += 1
        r = int.from_bytes(_h.sha256(b"ofm|%d" % it).digest(), "big")
        T, Hh, nn = holders[(r >> 2) % len(holders)]
        H2 = copy.deepcopy(Hh)
        op = r % 4
        if op == 0 and H2:
            i = (r >> 5) % len(H2)
            H2[i][0] = "DELETE" if H2[i][0] == "KEEP" else "KEEP"
        elif op == 1 and H2:
            i = (r >> 5) % len(H2)
            H2[i][1] = 1 + (r >> 13) % nn
        elif op == 2 and len(H2) < 70:
            H2.insert((r >> 5) % (len(H2) + 1), ["KEEP" if r % 2 else "DELETE", 1 + (r >> 13) % nn])
        elif len(H2) > 4:
            del H2[(r >> 5) % len(H2)]
        sfh, nbh = offline_shortfall(nn, T, H2)
        evals += 1
        if sfh == -2:
            continue
        if sfh > 0:
            step("OF-KILL", "OFFLINE HALL KILL it=%d shortfall=%d" % (it, sfh))
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json").write_text(
                json.dumps({"kill": True, "H": H2}, indent=1, default=str), encoding="utf-8")
            return 2
        gaph, _ = gc_gap(nn, T, H2)
        if gaph > 0:
            step("OF-KILL", "GC KILL it=%d gap=%d" % (it, gaph))
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "gckill.json").write_text(
                json.dumps({"kill": True, "H": H2}, indent=1, default=str), encoding="utf-8")
            return 2
        if sfh >= worst_sf or gaph >= worst_gap:
            worst_sf = max(worst_sf, sfh)
            worst_gap = max(worst_gap, gaph)
            holders.append((T, H2, nn))
            holders = holders[-14:]
        if it % 1500 == 0:
            step("OF-03", "it=%d evals=%d worst_sf=%d worst_gap=%d" % (it, evals, worst_sf, worst_gap))
    step("OF-04", "evals=%d worst_shortfall=%d worst_gap=%d" % (evals, worst_sf, worst_gap))
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "offline.json").write_text(
        json.dumps({"evals": evals, "killer_shortfall": sf, "killer_nb": nb,
                    "worst_shortfall": worst_sf, "worst_gap": worst_gap},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

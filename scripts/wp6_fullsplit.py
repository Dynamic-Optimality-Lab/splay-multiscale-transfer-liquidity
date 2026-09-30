"""WP-6 STEP FS-00: full-split sustain falsifier (disjointness 1.0 target).

Sustain histories where A-rotated keys stay DISJOINT from x-zone triples
(disjointness 1.0 = full sterility) while B-heavy strikes hit (first-x
discipline): demand-zone (victim x + B-vicinity) vs supply-zone (everything
A-rotated) with EMPTY intersection, verified per access.
Objective: max sustained-disjoint-length + shortfall (KILL -> hallkill §24);
tie-break min slack; track GC-gap; record recoupling events (which access
broke disjointness 1.0 and how: root-sync? zone-drift? hub transient?).
Seeds: killer, surgical/split holders, split randoms (fresh keys walk).
NEW artifact: fullsplit.json (+hallkill/gckill ONLY on kills). Sealed untouched.
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


def sustain_metrics(n, T0, H, xzone):
    """Longest prefix with per-access A-rotated disjoint from xzone + first break."""
    A, B = to_ptr(T0), to_ptr(T0)
    pre = E.precompute(n, T0, H)
    run = 0
    best = 0
    firstbreak = None
    for idx, acc in enumerate(pre):
        A, invs = splay_A(A, acc["x"])
        akeys = set()
        for S in invs:
            akeys |= set(S)
        if akeys.isdisjoint(xzone):
            run += 1
            best = max(best, run)
        else:
            if firstbreak is None:
                firstbreak = (idx, acc["mode"], acc["x"], sorted(akeys & xzone)[:6])
            run = 0
        if acc["mode"] == "KEEP":
            B, _ = splay_B_push(B, acc["x"])
    return best, firstbreak


def eval_hist(n, T0, H, xzone):
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
    sus, brk = sustain_metrics(n, T0, H, xzone)
    return ("OK", best, nb, gap, sus, brk)


def main() -> int:
    step("FS-00", "Full-split sustain falsifier")
    import json
    TP = ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "fullsplit.json"
    best = None  # (sustain, -shortfall-risk...) primary: kill; else max sustain + min slack
    bestsus = 0
    evals = 0
    holders = []
    import json as _j
    dk = _j.load(open(ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "starve_min.json"))
    holders.append((vine(dk["n"], dk["T0left"]), dk["Hmin"], dk["n"], None))
    for s in range(80):
        rng = Rng(("s%d" % s).encode(), b"fs")
        r = rng(0)
        n = 128
        T0 = vine(n, (r >> 8) % 2 == 0)
        xc = 60 + (r >> 16) % 40
        xzone = set(range(max(1, xc - 5), min(n, xc + 5) + 1))
        x = xc
        H = []
        L = 20 + (r >> 24) % 20
        for i in range(L):
            rr = Rng(("s%d" % s).encode(), ("fsh%d" % i).encode())
            q = rr(1000 + i)
            # supply zone: far bottom/top (away from xzone); demand: xzone KEEPs
            if (q >> 2) % 4 == 0:
                H.append(["KEEP", min(n, max(1, xc + [-4, -3, -2, 2, 3, 4][(q >> 5) % 6]))])
            else:
                z = [1 + (q >> 5) % 25, 103 + (q >> 9) % 25][(q >> 13) % 2]
                H.append(["DELETE" if (q >> 15) % 3 else "KEEP", z])
        H = [a for a in H if a[1] != x]
        H.append(["KEEP", x])
        v = eval_hist(n, T0, H, xzone)
        evals += 1
        if v is None:
            continue
        if v[0] == "KILL":
            step("FS-KILL", "HALL seed %d shortfall=%d" % (s, v[1]))
            TP.write_text(_j.dumps({"kill": True, "H": H}, indent=1, default=str), encoding="utf-8")
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json").write_text(
                _j.dumps({"kill": True, "H": H}, indent=1, default=str), encoding="utf-8")
            return 2
        _, b, nb, gap, sus, brk = v
        if gap > 0:
            step("FS-KILL", "GC seed %d" % s)
            return 2
        if sus > bestsus:
            bestsus = sus
            best = (b[0] if b else None, sus, brk)
            TP.write_text(_j.dumps({"evals": evals, "sustain": sus, "break": brk,
                                    "slack": b[0] if b else None},
                                   indent=1, sort_keys=True, default=str), encoding="utf-8")
            step("FS-NEW", "seeds sustain=%d slack=%s brk=%s" % (sus, b[0] if b else None, brk))
        holders.append((T0, H, n, xzone))
    holders = holders[:16]
    step("FS-01", "seeds evals=%d bestsus=%d" % (evals, bestsus))
    it = 0
    while evals < 12000:
        it += 1
        r = int.from_bytes(_h.sha256(b"fsm|%d" % it).digest(), "big")
        T0, H, n, xz = holders[(r >> 2) % len(holders)]
        if xz is None:
            xz = set(range(55, 106))
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
        v = eval_hist(n, T0, H2, xz)
        evals += 1
        if v is None:
            continue
        if v[0] == "KILL":
            step("FS-KILL", "HALL it=%d shortfall=%d" % (it, v[1]))
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json").write_text(
                _j.dumps({"kill": True, "H": H2}, indent=1, default=str), encoding="utf-8")
            return 2
        _, b, nb, gap, sus, brk = v
        if gap > 0:
            step("FS-KILL", "GC it=%d" % it)
            return 2
        if sus > bestsus:
            bestsus = sus
            best = (b[0] if b else None, sus, brk)
            TP.write_text(_j.dumps({"evals": evals, "sustain": sus, "break": brk,
                                    "slack": b[0] if b else None},
                                   indent=1, sort_keys=True, default=str), encoding="utf-8")
            step("FS-NEW", "it=%d sustain=%d slack=%s brk=%s" % (it, sus, b[0] if b else None, brk))
            holders.append((T0, H2, n, xz))
            holders = holders[-16:]
        elif (r >> 6) % 4 == 0:
            holders.append((T0, H2, n, xz))
            holders = holders[-16:]
        if it % 3000 == 0:
            step("FS-02", "it=%d evals=%d bestsus=%d" % (it, evals, bestsus))
    step("FS-03", "evals=%d bestsus=%d best=%s" % (evals, bestsus, best))
    import json as _jj
    try:
        _prev = _jj.loads(TP.read_text(encoding="utf-8"))
    except Exception:
        _prev = {}
    _prev["evals"] = evals
    TP.write_text(_jj.dumps(_prev, indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""WP-6 STEP BN-00: big-n assault (n=256/512 uncovered territory).

All prior work uses n<=128. Bigger vines allow deeper pushes (e_B to ~256),
more sterile room (far zones), longer B-paths vs A-supply. Regimes: T0-shallow
first-x strikes (E1-thin + pushes + avoidance + repeats + sterile), shared-zone
sustain, B-heavy walks, DELETE-heavy decouplers. Objectives: shortfall (KILL ->
hallkill + §24), GC-gap (kill -> gckill). T0: vine + balanced shapes.
NEW artifact: bign.json (+hallkill/gckill ONLY on kills). Sealed untouched.
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


def balanced(n):
    ks = list(range(1, n + 1))
    def build(ks):
        if not ks:
            return None
        m = len(ks) // 2
        return [ks[m], build(ks[:m]), build(ks[m + 1:])]
    return build(ks)


def H_mix(rr, n, L, x0, shallow=None):
    H = []
    x = x0
    for i in range(L):
        r = rr(1000 + i)
        if i % 5 == 4:
            y = min(n, max(1, x + [-64, -32, 32, 64][r % 4]))
            H.append(["DELETE", y if y != x else 1])
            H.append(["KEEP", x])
        else:
            H.append(["KEEP" if r % 3 else "DELETE", x])
        x = min(n, max(1, x + [-32, -16, -8, -4, -1, 1, 4, 8, 16, 32][(r >> 9) % 10]))
    if shallow is not None:
        H.append(["KEEP", shallow])
    return H


def eval_hist(n, T0, H):
    G = build_graph(n, T0, H)
    if G is None:
        return None
    f, nb, lv = maxflow_cap3(G)
    if nb - f > 0:
        return ("KILL", nb - f, nb)
    gap, _ = gc_gap(n, T0, H)
    return ("OK", nb, gap)


def main() -> int:
    step("BN-00", "Big-n assault")
    import json
    TP = ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "bign.json"
    best = None
    evals = 0
    holders = []
    for s in range(60):
        rng = Rng(("s%d" % s).encode(), b"bn")
        r = rng(0)
        n = [256, 512][r % 2]
        T0 = vine(n, (r >> 8) % 2 == 0) if (r >> 9) % 2 else balanced(n)
        rr = Rng(("s%d" % s).encode(), b"bnh")
        shallow = (n - 1 - (r >> 24) % 6) if (r >> 16) % 2 else None
        H = H_mix(rr, n, 10 + (r >> 16) % 16, 1 + (r >> 24) % n, shallow)
        v = eval_hist(n, T0, H)
        evals += 1
        if v is None:
            continue
        if v[0] == "KILL":
            step("BN-KILL", "HALL seed %d shortfall=%d nb=%d" % (s, v[1], v[2]))
            TP.write_text(json.dumps({"kill": True, "n": n, "H": H}, indent=1, default=str),
                          encoding="utf-8")
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json").write_text(
                json.dumps({"kill": True, "n": n, "H": H}, indent=1, default=str), encoding="utf-8")
            return 2
        _, nb, gap = v
        if gap > 0:
            step("BN-KILL", "GC seed %d" % s)
            return 2
        if best is None or nb > best[0]:
            best = (nb, gap)
            holders.append((T0, H, n))
    holders = holders[:14]
    step("BN-01", "seeds evals=%d bestB=%s" % (evals, best))
    it = 0
    while evals < 5500:
        it += 1
        r = int.from_bytes(_h.sha256(b"bnm|%d" % it).digest(), "big")
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
            step("BN-KILL", "HALL it=%d shortfall=%d nb=%d" % (it, v[1], v[2]))
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json").write_text(
                json.dumps({"kill": True, "n": n, "H": H2}, indent=1, default=str), encoding="utf-8")
            return 2
        _, nb, gap = v
        if gap > 0:
            step("BN-KILL", "GC it=%d" % it)
            return 2
        if nb > best[0]:
            best = (nb, gap)
            holders.append((T0, H2, n))
            holders = holders[-14:]
        elif (r >> 6) % 4 == 0:
            holders.append((T0, H2, n))
            holders = holders[-14:]
        if it % 2000 == 0:
            step("BN-02", "it=%d evals=%d bestB=%s" % (it, evals, best))
    step("BN-03", "evals=%d bestB=%s" % (evals, best))
    TP.write_text(json.dumps({"evals": evals, "bestB": best}, indent=1, sort_keys=True, default=str),
                  encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""WP-6 KILLSHOT3: n=6 exhaustive L<=4 + random-T0 family hunt (C57c).

Uncovered ground: (1) exhaustive stopped at n=5; n=6 L<=4 = 12^4+12^3+12^2+12 = 22,620
histories — feasible exact. (2) EVERY prior run used vine T0; balanced/random BST T0
change E1-depth/push geometry entirely (fresh family).
Kill: shortfall>0 -> hallkill.json exit 2; gap>0 exit 2.
Usage: argv[1] = X (exhaustive) or R (random-T0) or BOTH.
Artifact: killshot3.json. Sealed files untouched.
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_hallcore import build_graph, maxflow_cap3
from wp6_offline import gc_gap
from wp6_tightest import vine, Rng
import itertools


def step(sid, msg):
    print("[WP-6][KILLSHOT3 %s] %s" % (sid, msg), flush=True)


def balanced(n):
    keys = list(range(1, n + 1))
    def build(ks):
        if not ks:
            return None
        m = len(ks) // 2
        return [ks[m], build(ks[:m]), build(ks[m + 1:])]
    return build(keys)


def random_bst(n, rng, c):
    import hashlib as _h
    keys = list(range(1, n + 1))
    # random insertion order -> BST shape
    order = sorted(keys, key=lambda k: int.from_bytes(_h.sha256(b"rbst|%d|%d|%d" % (c, n, k)).digest(), "big"))
    T = None
    def ins(T, k):
        if T is None:
            return [k, None, None]
        if k < T[0]:
            T[1] = ins(T[1], k)
        elif k > T[0]:
            T[2] = ins(T[2], k)
        return T
    for k in order:
        T = ins(T, k)
    return T


def check(n, T0, H):
    G = build_graph(n, T0, H)
    if G is None:
        return None
    f, nb, lv = maxflow_cap3(G)
    if nb - f > 0:
        return ("KILL", nb - f, nb)
    gap, _ = gc_gap(n, T0, H)
    if gap > 0:
        return ("GCKILL", gap, nb)
    return ("OK", nb)


def phase_X():
    import json
    step("K3-X00", "n=6 exhaustive L<=4 (22,620 histories)")
    TP = ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "killshot3X.json"
    n = 6
    T0 = vine(n, True)
    cells = [["KEEP", x] for x in range(1, n + 1)] + [["DELETE", x] for x in range(1, n + 1)]
    evals = 0
    for L in (1, 2, 3, 4):
        step("K3-X%02d" % L, "L=%d: %d histories" % (L, 12 ** L))
        for tup in itertools.product(range(12), repeat=L):
            H = [list(cells[c]) for c in tup]
            v = check(n, T0, H)
            evals += 1
            if v is None:
                continue
            if v[0] == "KILL":
                step("K3-XKILL", "HALL n=6 L=%d shortfall=%d H=%s" % (L, v[1], H))
                (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json").write_text(
                    json.dumps({"kill": True, "n": n, "H": H}, indent=1, default=str), encoding="utf-8")
                TP.write_text(json.dumps({"kill": True, "n": n, "H": H}, indent=1, default=str), encoding="utf-8")
                return 2
            if v[0] == "GCKILL":
                step("K3-XKILL", "GC n=6 L=%d gap=%d" % (L, v[1]))
                return 2
            if evals % 8000 == 0:
                step("K3-XP", "evals=%d" % evals)
    step("K3-X01", "exhaustive n=6 L<=4 clean evals=%d" % evals)
    TP.write_text(json.dumps({"evals": evals, "nokill": True, "scope": "n=6 L<=4 vine-left"}, indent=1), encoding="utf-8")
    return 0


def phase_R(budget=9000):
    import json
    step("K3-R00", "random-T0 family hunt (balanced/random-BST/vine) budget=%d" % budget)
    TP = ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "killshot3R.json"
    evals = 0
    s = 0
    import copy
    while evals < budget:
        rng = Rng(("kr%d" % s).encode(), b"k3r")
        r = rng(0)
        n = [8, 12, 16, 24, 32, 48, 64][r % 7]
        fam = (r >> 5) % 3
        if fam == 0:
            T0 = vine(n, (r >> 8) % 2 == 0)
            fn = "vine"
        elif fam == 1:
            T0 = balanced(n)
            fn = "bal"
        else:
            T0 = random_bst(n, rng, s)
            fn = "rbst"
        L = 12 + (r >> 16) % 24
        x0 = 1 + (r >> 24) % n
        H = []
        x = x0
        rr = Rng(("kr%d" % s).encode(), b"k3rh")
        for i in range(L):
            q = rr(1000 + i)
            op = (q >> 2) % 10
            if op < 3:
                H.append(["DELETE", 1 + (q >> 9) % n])
            elif op < 6:
                z = min(n, max(1, x + [-2, -1, 1, 2][(q >> 5) % 4]))
                H.append(["KEEP", z])
            else:
                H.append(["KEEP", x])
            x = min(n, max(1, x + [-8, -4, -1, 1, 4, 8][(q >> 11) % 6]))
        v = check(n, T0, H)
        evals += 1
        if v is None:
            s += 1
            continue
        if v[0] == "KILL":
            step("K3-RKILL", "HALL s=%d fam=%s n=%d shortfall=%d nb=%d" % (s, fn, n, v[1], v[2]))
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json").write_text(
                json.dumps({"kill": True, "n": n, "fam": fn, "H": H}, indent=1, default=str), encoding="utf-8")
            TP.write_text(json.dumps({"kill": True, "s": s, "fam": fn, "n": n, "H": H}, indent=1, default=str), encoding="utf-8")
            return 2
        if v[0] == "GCKILL":
            step("K3-RKILL", "GC s=%d gap=%d" % (s, v[1]))
            return 2
        s += 1
        if s % 2000 == 0:
            step("K3-RP", "s=%d evals=%d clean" % (s, evals))
    step("K3-R01", "random-T0 clean evals=%d" % evals)
    TP.write_text(json.dumps({"evals": evals, "nokill": True, "scope": "vine/bal/rbst n=8..64"}, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "BOTH"
    rc = 0
    if which in ("X", "BOTH"):
        rc = phase_X()
        if rc == 2:
            sys.exit(2)
    if which in ("R", "BOTH"):
        rc = phase_R()
    sys.exit(rc)

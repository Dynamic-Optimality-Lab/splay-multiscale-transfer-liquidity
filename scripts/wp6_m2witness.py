"""WP-6 STEP MW-00: minload>=2 witness hunt + autopsy (stronger claim kill).

Replicates BR-00 search geometry; SAVES first minload>=2 witness (n,T0,H)
with full load-aware trace; keeps pushing mutations toward minload>=3
(Stage-B starvation kill). NEW artifact: m2witness.json. Sealed files untouched.
"""
from __future__ import annotations
import sys
import copy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_eventflow_abl import build_tagged
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
    def __init__(self, s): self.s = s

    def __call__(self, tag, c):
        if isinstance(tag, str):
            tag = tag.encode()
        return int.from_bytes(_h.sha256(b"br|%s|%s|%d" % (self.s, tag, c)).digest(), "big")


def H_of(rr, n, L, x0, tag):
    H = []
    x = x0
    for i in range(L):
        r = rr(tag, 1000 + i)
        if i % 4 == 3:
            y = min(n, max(1, x + [-32, -16, 16, 32][r % 4]))
            H.append(["DELETE", y if y != x else 1])
            H.append(["KEEP", x])
        else:
            H.append(["KEEP" if r % 3 else "DELETE", x])
        x = min(n, max(1, x + [-16, -8, -4, -1, 1, 4, 8, 16][(r >> 9) % 8]))
    return H


def maxminload(n, T0, H):
    """Max over B-events of min-load-before under least-loaded. -1 if illegal."""
    pre = E.precompute(n, T0, H)
    res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
    if res["violations"]:
        return -2, None
    g = build_tagged(n, T0, H)
    Aevs, Bevs, elig = g["Aevs"], g["Bevs"], g["elig"]
    load = {}
    best = -1
    best_at = None
    for j in range(len(Bevs)):
        e = elig[j]
        cands = sorted((load.get(i, 0), i) for k in e for i in e[k] if Aevs[i][1])
        if not cands:
            continue
        if cands[0][0] > best:
            best, best_at = cands[0][0], j
        if cands[0][0] < 3:
            ld, i = cands[0]
            load[i] = ld + 1
        else:
            return 99, j  # starvation
    return best, best_at


def trace(n, T0, H, upto_bev=None):
    g = build_tagged(n, T0, H)
    Aevs, Bevs, elig = g["Aevs"], g["Bevs"], g["elig"]
    pre = g["pre"]
    load = {}
    out = []
    for j in range(len(Bevs)):
        acc = Bevs[j][0]
        xx = pre[acc]["x"]
        info = {k: sorted(i for i in elig[j][k] if Aevs[i][1])
                for k in ("E1", "E2", "E3", "E4")}
        N = set().union(*info.values())
        ml = min((load.get(i, 0) for i in N), default=None)
        out.append({"bev": j, "acc": acc, "x": xx, "ml": ml, "nanc": len(N),
                    "cls_n": {k: len(info[k]) for k in info},
                    "cls_loads": {k: sorted(load.get(i, 0) for i in info[k]) for k in info},
                    "U": sum(max(0, 3 - load.get(i, 0)) for i in N)})
        if upto_bev is not None and j >= upto_bev:
            break
        if ml is not None and ml < 3:
            cands = sorted((load.get(i, 0), i) for i in N)
            ld, i = cands[0]
            load[i] = ld + 1
    return out, {"Aevs": Aevs, "Bevs": Bevs}


def main() -> int:
    step("MW-00", "minload>=2 witness hunt + autopsy")
    import json
    best = -1
    wit = None
    holders = []
    evals = 0
    # Phase 1: seeds (same geometry as BR-00)
    for s in range(80):
        rng = Rng(("s%d" % s).encode())
        r = rng("s", 0)
        n = [32, 64, 128][r % 3]
        T0 = vine(n, (r >> 8) % 2 == 0)
        rr = Rng(("s%d" % s).encode())
        H = H_of(rr, n, 10 + (r >> 16) % 22, 1 + (r >> 24) % n, "h")
        v, at = maxminload(n, T0, H)
        evals += 1
        if v == -2:
            step("MW-KILL", "present kill s=%d" % s)
            return 2
        if v == 99:
            step("MW-KILL", "STARVATION seed s=%d bev=%s" % (s, at))
            return 2
        if v > best:
            best = v
            if v >= 2 and wit is None:
                wit = {"n": n, "T0": T0, "H": H, "ml": v, "at": at, "phase": "seed",
                       "seed": s}
        holders.append((T0, H, n, v))
    holders.sort(key=lambda z: z[3], reverse=True)
    holders = holders[:10]
    step("MW-01", "seeds evals=%d best=%d" % (evals, best))
    # Phase 2: mutate toward higher minload
    it = 0
    while evals < 4000 and it < 4000:
        it += 1
        r = int.from_bytes(_h.sha256(b"mwm|%d" % it).digest(), "big")
        T0, H, n, _ = holders[(r >> 2) % len(holders)]
        H2 = copy.deepcopy(H)
        op = r % 4
        if op == 0 and H2:
            i = (r >> 5) % len(H2)
            H2[i][0] = "DELETE" if H2[i][0] == "KEEP" else "KEEP"
        elif op == 1 and H2:
            i = (r >> 5) % len(H2)
            H2[i][1] = 1 + (r >> 13) % n
        elif op == 2 and len(H2) < 60:
            H2.insert((r >> 5) % (len(H2) + 1), ["KEEP" if r % 2 else "DELETE", 1 + (r >> 13) % n])
        elif len(H2) > 4:
            del H2[(r >> 5) % len(H2)]
        v, at = maxminload(n, T0, H2)
        evals += 1
        if v == -2:
            step("MW-KILL", "present kill it=%d" % it)
            return 2
        if v == 99:
            step("MW-KILL", "STARVATION it=%d bev=%s" % (it, at))
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "starve.json").write_text(
                json.dumps({"kill": True, "where": at, "H": H2}, indent=1, default=str),
                encoding="utf-8")
            return 2
        if v > best:
            best = v
            holders.append((T0, H2, n, v))
            holders.sort(key=lambda z: z[3], reverse=True)
            holders = holders[:10]
            if v >= 2 and wit is None:
                wit = {"n": n, "T0": copy.deepcopy(T0), "H": copy.deepcopy(H2),
                       "ml": v, "at": at, "phase": "mutate", "it": it}
        if it % 500 == 0:
            step("MW-02", "it=%d evals=%d best=%d wit=%s" % (it, evals, best, wit is not None))
    step("MW-03", "evals=%d best=%d wit=%s" % (evals, best, wit is not None))
    out = {"evals": evals, "best": best, "witness": None}
    if wit is not None:
        tr, _ = trace(wit["n"], wit["T0"], wit["H"], upto_bev=wit["at"])
        # verify by fresh rebuild
        v2, _ = maxminload(wit["n"], wit["T0"], wit["H"])
        wit["reverify"] = v2
        wit["trace"] = tr
        out["witness"] = wit
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "m2witness.json").write_text(
        json.dumps(out, indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

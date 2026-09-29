"""WP-6 STEP HC-00: hillclimb to KILL E_B <= 3*S_A (targeted).

Maximize F = E_B - 3*S_A over (T0-shape, H). F > 0 kills the E_B-route
(NOT stock). Operators: flip mode, rekey access, insert/delete access,
swap two accesses, flip T0 chirality. Present histories only (all keys
in [1,n]); B absent-path cannot occur. Bounded evals, small n for speed.
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from solver import encode as E


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


def F_of(n, T0, H):
    try:
        pre = E.precompute(n, T0, H)
    except ValueError:
        return None
    EB = sum(len(a["Bev"]) for a in pre)
    SA = sum(1 for a in pre for z in a["sites"] if z)
    return EB - 3 * SA, EB, SA


def main() -> int:
    # WP-6 STEP HC-00: kill-hunt for E_B<=3*S_A.
    step("HC-00", "Hillclimb: maximize E_B - 3*S_A")
    import hashlib
    import json

    seed0 = b"hc-seed"

    def rng_stream(tag, c):
        h = hashlib.sha256(b"hc|%s|%d" % (tag, c)).digest()
        return int.from_bytes(h, "big")

    def vine(n, left):
        t = None
        for k in (range(n, 0, -1) if not left else range(1, n + 1)):
            t = [k, None, t] if not left else [k, t, None]
        return t

    best = -10**18
    best_ex = None
    evals = 0
    # seeds: vines + random histories, then local search from the best
    cands = []
    for s in range(300):
        r = rng_stream(("s%d" % s).encode(), 0)
        n = [16, 32, 64][r % 3]
        T0 = vine(n, (r >> 8) % 2 == 0)
        L = 4 + (r >> 16) % 20
        x = 1 + (r >> 24) % n
        H = []
        for i in range(L):
            r = rng_stream(("s%d" % s).encode(), 1000 + i)
            m = "KEEP" if r % 3 else "DELETE"
            H.append([m, x])
            x = min(n, max(1, x + [-16, -8, -4, -1, 1, 4, 8, 16][(r >> 5) % 8]))
        cands.append((n, T0, H))
    for (n, T0, H) in cands:
        v = F_of(n, T0, H)
        evals += 1
        if v is not None and v[0] > best:
            best, best_ex = v[0], (n, len(H), v[1], v[2])
    step("HC-01", "seed phase: evals=%d best F=%d %s" % (evals, best, best_ex))
    # local search: restart from random + mutate best
    import copy
    bn, bT0, bH = None, None, None
    # reconstruct a best holder: keep explicit best triple
    holders = []
    for (n, T0, H) in cands:
        v = F_of(n, T0, H)
        if v is not None and v[0] >= best:
            holders = [(n, T0, H, v[0])]
            break
    n, T0, H, bv = holders[0]
    for it in range(1500):
        r = rng_stream(b"mut", it)
        H2 = copy.deepcopy(H)
        op = r % 5
        if op == 0 and H2:  # flip mode
            i = (r >> 3) % len(H2)
            H2[i][0] = "DELETE" if H2[i][0] == "KEEP" else "KEEP"
        elif op == 1 and H2:  # rekey
            i = (r >> 3) % len(H2)
            H2[i][1] = 1 + (r >> 11) % n
        elif op == 2 and len(H2) < 40:  # insert
            i = (r >> 3) % (len(H2) + 1)
            H2.insert(i, ["KEEP" if r % 2 else "DELETE", 1 + (r >> 11) % n])
        elif op == 3 and len(H2) > 2:  # delete
            i = (r >> 3) % len(H2)
            del H2[i]
        elif op == 4:  # flip T0 chirality
            T0 = vine(n, it % 2 == 0)
        v = F_of(n, T0, H2)
        evals += 1
        if v is not None and v[0] > best:
            best, H, best_ex = v[0], H2, (n, len(H2), v[1], v[2])
            if best > 0:
                break
    step("HC-02", "evals=%d best F=%d %s (F>0 KILLS E_B-route)" % (evals, best, best_ex))
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "eb_hillclimb.json").write_text(
        json.dumps({"evals": evals, "best_F": best, "best_ex": best_ex,
                    "verdict": "E_B-ROUTE DEAD" if best > 0 else "SURVIVES targeted hillclimb"},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

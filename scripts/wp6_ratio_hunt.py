"""WP-6 STEP HC3-00: ratio-fitness kill-hunt (anti-degenerate).

Prior gap-hillclimb parked at degenerate F=0 (doing nothing beats negative).
Fix: fitness = RATIOS (E_B/S_A, R/Q, D/6S_A) with activity constraint
(S_A>=50, E_B>=20); degenerate scores -inf (excluded). Targets:
  J1 = E_B/S_A   (want <3; >=3 kills E_B-route)
  J2 = R/Q       (want <1.5; >=1.5 kills R-link)
  J3 = D/6S_A    (want <1; >=1 REFUTES STOCK (present witness -> RETURN 2))
Cycle-aware + block-repeat + key-permute ops, big budget. Reports argmax.
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from solver import encode as E


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


def eval_hist(n, T0, H):
    try:
        pre = E.precompute(n, T0, H)
    except ValueError:
        return None
    res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
    if res["violations"]:
        return ("KILL",)
    EB = SA = 0
    R = Q = 0
    D = 0
    ki = 0
    kps = list(res["keeps"])
    for acc in pre:
        eA = sum(1 for z in acc["sites"] if z)
        SA += eA
        Q += acc["a"] - 1
        if acc["mode"] == "KEEP":
            EB += len(acc["Bev"])
            R += acc["y"] - 1
            D += kps[ki]["need"]
            ki += 1
    return (EB, SA, R, Q, D)


def main() -> int:
    # WP-6 STEP HC3-00: ratio hunt.
    step("HC3-00", "Ratio-fitness kill-hunt (E_B/S_A, R/Q, D/6S_A)")
    import hashlib
    import json
    import copy

    def R(tag, c):
        return int.from_bytes(hashlib.sha256(b"hc3|%s|%d" % (tag, c)).digest(), "big")

    def vine(n, left):
        t = None
        for k in (range(n, 0, -1) if not left else range(1, n + 1)):
            t = [k, None, t] if not left else [k, t, None]
        return t

    best = {"J1": -1.0, "J2": -1.0, "J3": -1.0}
    ex = {"J1": None, "J2": None, "J3": None}
    evals = 0
    killed_stock = None

    def consider(n, T0, H):
        nonlocal evals, killed_stock
        v = eval_hist(n, T0, H)
        evals += 1
        if v is None:
            return
        if v[0] == "KILL":
            killed_stock = (n, [list(a) for a in H])
            return
        EB, SA, R, Q, D = v
        if SA < 50 or EB < 20:
            return
        j1 = EB / SA
        j2 = (R / Q) if Q > 0 else -1.0
        j3 = D / (6 * SA)
        for key, val in (("J1", j1), ("J2", j2), ("J3", j3)):
            if val > best[key]:
                best[key] = val
                ex[key] = (n, len(H), EB, SA, R, Q, D)

    for s in range(300):
        r = R(("s%d" % s).encode(), 0)
        n = [32, 64, 128][r % 3]
        T0 = vine(n, (r >> 8) % 2 == 0)
        L = 10 + (r >> 16) % 40
        x = 1 + (r >> 24) % n
        H = []
        for i in range(L):
            r = R(("s%d" % s).encode(), 1000 + i)
            if i % 6 == 5:
                y = min(n, max(1, x + [-32, -16, 16, 32][(r >> 5) % 4]))
                H.append(["DELETE", y if y != x else (1 if x != 1 else n)])
                H.append(["KEEP", x])
            else:
                H.append(["KEEP" if r % 3 else "DELETE", x])
            x = min(n, max(1, x + [-16, -8, -4, -1, 1, 4, 8, 16][(r >> 9) % 8]))
        consider(n, T0, H)
        if killed_stock:
            break
    step("HC3-01", "seeds: evals=%d best=%s" % (evals, {k: round(v, 4) for k, v in best.items()}))
    # evolve
    pool = []
    it = 0
    # rebuild small pool from seeds is skipped; mutate best holders via fresh sampling:
    holders = []
    for s in range(300):
        r = R(("h%d" % s).encode(), 0)
        n = [32, 64, 128][r % 3]
        T0 = vine(n, (r >> 8) % 2 == 0)
        L = 10 + (r >> 16) % 40
        x = 1 + (r >> 24) % n
        H = []
        for i in range(L):
            r = R(("h%d" % s).encode(), 1000 + i)
            H.append(["KEEP" if r % 3 else "DELETE", x])
            x = min(n, max(1, x + [-16, -8, -4, -1, 1, 4, 8, 16][(r >> 9) % 8]))
        holders.append((n, T0, H))
    while evals < 12000 and it < 9000 and not killed_stock:
        it += 1
        r = R(b"mut", it)
        n, T0, H = holders[(r >> 2) % len(holders)]
        H2 = copy.deepcopy(H)
        op = r % 6
        if op == 0 and H2:
            i = (r >> 5) % len(H2)
            H2[i][0] = "DELETE" if H2[i][0] == "KEEP" else "KEEP"
        elif op == 1 and H2:
            i = (r >> 5) % len(H2)
            H2[i][1] = 1 + (r >> 13) % n
        elif op == 2 and H2 and len(H2) < 100:
            a = (r >> 5) % len(H2)
            b = a + 1 + (r >> 11) % max(1, len(H2) - a)
            H2[a:a] = copy.deepcopy(H2[a:b])
        elif op == 3 and len(H2) > 4:
            i = (r >> 5) % len(H2)
            del H2[i]
        elif op == 4 and len(H2) < 100:
            i = (r >> 5) % (len(H2) + 1)
            H2.insert(i, ["KEEP" if r % 2 else "DELETE", 1 + (r >> 13) % n])
        else:
            T0 = vine(n, it % 2 == 0)
        b0 = dict(best)
        consider(n, T0, H2)
        if any(best[k] > b0[k] for k in best):
            holders.append((n, T0, H2))
            holders = holders[-16:]
    step("HC3-02", "evals=%d best=%s" % (evals, {k: round(v, 4) for k, v in best.items()}))
    for k in best:
        step("HC3-02", "%s argmax=%s" % (k, ex[k]))
    out = {"evals": evals, "best": best, "ex": ex,
           "verdict": "SEE-BEST"}
    if killed_stock:
        out["STOCK_KILL_WITNESS"] = killed_stock
        out["verdict"] = "STOCK REFUTED (present witness)"
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "ratio_hunt.json").write_text(
        json.dumps(out, indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 2 if killed_stock else 0


if __name__ == "__main__":
    sys.exit(main())

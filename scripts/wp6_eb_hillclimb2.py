"""WP-6 STEP HC2-00: upgraded kill-hunt for E_B<=3*S_A and R<=1.5*Q.

Cycle-aware operators (repeat a pump block to induce recirculation cascades),
longer histories, bigger n, larger budget. Targets: F1 = E_B-3*S_A,
F2 = R-1.5*Q (prefix-max, not just final). F>0 kills that route (NOT stock:
D2-sum has 5x slack, stock may survive). Reports best + argmax shape.
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
    EB = SA = 0
    R = Q = 0
    F1 = F2 = -10**18
    for acc in pre:
        eA = sum(1 for z in acc["sites"] if z)
        dA = acc["a"] - 1
        Q += dA
        SA += eA
        if acc["mode"] == "KEEP":
            eB = len(acc["Bev"])
            EB += eB
            R += acc["y"] - 1
        F1 = max(F1, EB - 3 * SA)
        F2 = max(F2, R - 1.5 * Q)
    return F1, F2, EB, SA, R, Q


def main() -> int:
    # WP-6 STEP HC2-00: upgraded hunt.
    step("HC2-00", "Upgraded kill-hunt (cycle-aware)")
    import hashlib
    import json
    import copy

    def R(tag, c):
        return int.from_bytes(hashlib.sha256(b"hc2|%s|%d" % (tag, c)).digest(), "big")

    def vine(n, left):
        t = None
        for k in (range(n, 0, -1) if not left else range(1, n + 1)):
            t = [k, None, t] if not left else [k, t, None]
        return t

    best1 = best2 = -10**18
    ex1 = ex2 = None
    evals = 0

    def consider(n, T0, H):
        nonlocal best1, best2, ex1, ex2, evals
        v = eval_hist(n, T0, H)
        evals += 1
        if v is None:
            return
        F1, F2, EB, SA, R, Q = v
        if F1 > best1:
            best1, ex1 = F1, (n, len(H), EB, SA)
        if F2 > best2:
            best2, ex2 = F2, (n, len(H), R, Q)

    # seed pool: cash/pump shapes + random
    pool = []
    for s in range(200):
        r = R(("s%d" % s).encode(), 0)
        n = [32, 64, 128][r % 3]
        T0 = vine(n, (r >> 8) % 2 == 0)
        L = 6 + (r >> 16) % 30
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
        pool.append((n, T0, H))
        consider(n, T0, H)
    step("HC2-01", "seeds: evals=%d bestF1=%s bestF2=%s" % (evals, best1, best2))
    # evolve top holders with cycle-aware ops
    scored = []
    for (n, T0, H) in pool:
        v = eval_hist(n, T0, H)
        if v is not None:
            scored.append((max(v[0], v[1]), n, T0, H))
    scored.sort(key=lambda z: -z[0])
    holders = [(n, T0, H) for (_, n, T0, H) in scored[:8]]
    it = 0
    while evals < 8000 and it < 6000:
        it += 1
        r = R(b"mut", it)
        n, T0, H = holders[(r >> 2) % len(holders)]
        H2 = copy.deepcopy(H)
        op = r % 7
        if op == 0 and H2:
            i = (r >> 5) % len(H2)
            H2[i][0] = "DELETE" if H2[i][0] == "KEEP" else "KEEP"
        elif op == 1 and H2:
            i = (r >> 5) % len(H2)
            H2[i][1] = 1 + (r >> 13) % n
        elif op == 2 and len(H2) < 80:
            # repeat a block (recirculation cycle induction)
            a = (r >> 5) % len(H2)
            b = a + 1 + (r >> 11) % max(1, len(H2) - a)
            blk = copy.deepcopy(H2[a:b])
            H2[a:a] = blk
        elif op == 3 and len(H2) > 2:
            i = (r >> 5) % len(H2)
            del H2[i]
        elif op == 4 and len(H2) < 80:
            i = (r >> 5) % (len(H2) + 1)
            H2.insert(i, ["KEEP" if r % 2 else "DELETE", 1 + (r >> 13) % n])
        elif op == 5:
            # key permutation of a block (symdiff churn)
            if len(H2) >= 4:
                a = (r >> 5) % (len(H2) - 3)
                seg = H2[a:a + 4]
                ks = [kv for (_, kv) in seg]
                sh = ks[1:] + ks[:1]
                for j in range(4):
                    seg[j][1] = sh[j]
        else:
            T0 = vine(n, it % 2 == 0)
        before1, before2 = best1, best2
        consider(n, T0, H2)
        if best1 > before1 or best2 > before2:
            holders.append((n, T0, H2))
            holders = holders[-12:]
        if best1 > 0 or best2 > 0:
            break
    step("HC2-02", "evals=%d bestF1=%s %s bestF2=%s %s" % (evals, best1, ex1, best2, ex2))
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "eb_hillclimb2.json").write_text(
        json.dumps({"evals": evals, "best_F1": best1, "ex1": ex1,
                    "best_F2": best2, "ex2": ex2,
                    "verdict": "ROUTE DEAD" if (best1 > 0 or best2 > 0) else "SURVIVES 8k cycle-aware evals"},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""WP-6 STEP SC-00: ratio-vs-n scaling (liftability test).

Max E_B/S_A by n (8/16/32/64/128) via ratio-fitness hillclimb per n
(active-constrained S_A>=50). DECREASING in n => dilution (small-n bounds
lift to large-n via balanced-build dilution). INCREASING => adversary
scales (need large-n direct; unbounded). Decides lifting viability.
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from solver import encode as E


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


def ev(n, T0, H):
    try:
        pre = E.precompute(n, T0, H)
    except ValueError:
        return None
    EB = sum(len(a["Bev"]) for a in pre if a["mode"] == "KEEP")
    SA = sum(1 for a in pre for z in a["sites"] if z)
    return (EB, SA)


def main() -> int:
    # WP-6 STEP SC-00: scaling.
    step("SC-00", "Ratio-vs-n scaling")
    import hashlib
    import copy

    def R(tag, c):
        return int.from_bytes(hashlib.sha256(b"sc|%s|%d" % (tag, c)).digest(), "big")

    def vine(n, left):
        t = None
        for k in (range(n, 0, -1) if not left else range(1, n + 1)):
            t = [k, None, t] if not left else [k, t, None]
        return t

    out = {}
    for n in (8, 16, 32, 64, 128):
        best = -1.0
        ex = None
        evals = 0
        holders = []
        for s in range(120):
            r = R(("n%ds%d" % (n, s)).encode(), 0)
            T0 = vine(n, (r >> 8) % 2 == 0)
            L = 8 + (r >> 16) % 24
            x = 1 + (r >> 24) % n
            H = []
            for i in range(L):
                r = R(("n%ds%d" % (n, s)).encode(), 500 + i)
                if i % 5 == 4:
                    y = min(n, max(1, x + [-16, -8, 8, 16][(r >> 5) % 4]))
                    H.append(["DELETE", y if y != x else (1 if x != 1 else n)])
                    H.append(["KEEP", x])
                else:
                    H.append(["KEEP" if r % 3 else "DELETE", x])
                x = min(n, max(1, x + [-16, -8, -4, -1, 1, 4, 8, 16][(r >> 9) % 8]))
            v = ev(n, T0, H)
            evals += 1
            if v is not None:
                EB, SA = v
                if SA >= 50 and EB >= 20 and EB / SA > best:
                    best, ex = EB / SA, (L, EB, SA)
                    holders.append((T0, H))
                    holders = holders[-8:]
        it = 0
        while evals < 1500 and it < 1200 and holders:
            it += 1
            r = R(("n%dm" % n).encode(), it)
            T0, H = holders[(r >> 2) % len(holders)]
            H2 = copy.deepcopy(H)
            op = r % 5
            if op == 0 and H2:
                i = (r >> 5) % len(H2)
                H2[i][0] = "DELETE" if H2[i][0] == "KEEP" else "KEEP"
            elif op == 1 and H2:
                i = (r >> 5) % len(H2)
                H2[i][1] = 1 + (r >> 13) % n
            elif op == 2 and len(H2) < 70:
                a = (r >> 5) % len(H2)
                b = a + 1 + (r >> 11) % max(1, len(H2) - a)
                H2[a:a] = copy.deepcopy(H2[a:b])
            elif op == 3 and len(H2) > 4:
                del H2[(r >> 5) % len(H2)]
            else:
                T0 = vine(n, it % 2 == 0)
            v = ev(n, T0, H2)
            evals += 1
            if v is not None:
                EB, SA = v
                if SA >= 50 and EB >= 20 and EB / SA > best:
                    best, ex = EB / SA, (len(H2), EB, SA)
                    holders.append((T0, H2))
                    holders = holders[-8:]
        step("SC-n%d" % n, "best E_B/S_A=%.4f %s" % (best, ex))
        out[str(n)] = {"best": best, "ex": ex}
    import json
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "scaling.json").write_text(
        json.dumps(out, indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

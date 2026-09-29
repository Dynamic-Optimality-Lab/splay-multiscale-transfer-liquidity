"""WP-6 STEP GA-00: GC-direct prefix-gap assault (B2 kill hunt).

Objective: maximize over KEEP-prefixes (E_B - 3*S_A). Kill >0 (gckill.json +
exit 2, then §15 audit path). Bias: B-heavy sustain (A-shallow/B-deep keys),
concentrated geographic walks (shared-zone pressure), long histories, vine
starts (deep splays), DELETE-run setups (pristine-E4 aggression).
Seeds: killer, M2, ENTRY@3, neg-margin, generic.
NEW artifact: gcattack.json (+gckill.json ONLY on kill). Sealed files untouched.
"""
from __future__ import annotations
import sys
import copy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_offline import gc_gap, H_walk, vine, Rng
from solver import encode as E


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


import hashlib as _h


def mutate(H, n, r):
    H2 = copy.deepcopy(H)
    op = r % 6
    if op == 0 and H2:
        i = (r >> 5) % len(H2)
        H2[i][0] = "DELETE" if H2[i][0] == "KEEP" else "KEEP"
    elif op == 1 and H2:
        i = (r >> 5) % len(H2)
        H2[i][1] = 1 + (r >> 13) % n
    elif op == 2 and len(H2) < 80:
        H2.insert((r >> 5) % (len(H2) + 1), ["KEEP" if r % 2 else "DELETE", 1 + (r >> 13) % n])
    elif op == 3 and H2:
        recent = [a[1] for a in H2][-6:]
        base = recent[(r >> 5) % len(recent)] if recent else 1 + (r >> 13) % n
        stepd = [-2, -1, -1, 0, 1, 1, 2][(r >> 9) % 7]
        H2.append(["KEEP" if r % 2 else "DELETE", min(n, max(1, base + stepd))])
    elif op == 4 and H2:
        recent = [a[1] for a in H2 if a[0] == "KEEP"][-4:]
        if recent:
            H2.append(["KEEP", recent[(r >> 5) % len(recent)]])
        else:
            H2.append(["KEEP", 1 + (r >> 13) % n])
    elif len(H2) > 4:
        del H2[(r >> 5) % len(H2)]
    return H2


def main() -> int:
    step("GA-00", "GC-direct prefix-gap assault")
    import json
    best = -10 ** 9
    best_ex = None
    evals = 0
    holders = []
    dk = json.load(open(ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "starve_min.json"))
    holders.append((vine(dk["n"], dk["T0left"]), dk["Hmin"], dk["n"]))
    for s in range(100):
        rng = Rng(("s%d" % s).encode(), b"ga")
        r = rng(0)
        n = [64, 128][r % 2]
        T0 = vine(n, (r >> 8) % 2 == 0)
        rr = Rng(("s%d" % s).encode(), b"gah")
        H = H_walk(rr, n, 16 + (r >> 16) % 28, 1 + (r >> 24) % n)
        pre = E.precompute(n, T0, H)
        res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
        evals += 1
        if res["violations"]:
            continue
        gap, at = gc_gap(n, T0, H)
        if gap > 0:
            step("GA-KILL", "GC seed %d gap=%d" % (s, gap))
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "gckill.json").write_text(
                json.dumps({"kill": True, "H": H}, indent=1, default=str), encoding="utf-8")
            return 2
        if gap > best:
            best, best_ex = gap, (s, at)
        holders.append((T0, H, n))
    holders = holders[:18]
    step("GA-01", "seeds evals=%d best_gap=%d %s" % (evals, best, best_ex))
    it = 0
    while evals < 15000:
        it += 1
        r = int.from_bytes(_h.sha256(b"gam|%d" % it).digest(), "big")
        T0, H, n = holders[(r >> 2) % len(holders)]
        H2 = mutate(H, n, r)
        pre = E.precompute(n, T0, H2)
        res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
        if res["violations"]:
            continue
        evals += 1
        gap, at = gc_gap(n, T0, H2)
        if gap > 0:
            step("GA-KILL", "GC it=%d gap=%d" % (it, gap))
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "gckill.json").write_text(
                json.dumps({"kill": True, "H": H2}, indent=1, default=str), encoding="utf-8")
            return 2
        if gap > best:
            best = gap
            holders.append((T0, H2, n))
            holders = holders[-18:]
        elif (r >> 6) % 4 == 0:
            holders.append((T0, H2, n))
            holders = holders[-18:]
        if it % 3000 == 0:
            step("GA-02", "it=%d evals=%d best_gap=%d" % (it, evals, best))
    step("GA-03", "evals=%d best_gap=%d" % (evals, best))
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "gcattack.json").write_text(
        json.dumps({"evals": evals, "best_gap": best}, indent=1, sort_keys=True, default=str),
        encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

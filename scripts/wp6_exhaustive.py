"""WP-6 STEP EX-00: small-n EXHAUSTIVE Stage-B verification.

Enumerate ALL BST shapes T0 (Catalan) x ALL histories H of bounded length L
over ({KEEP,DELETE} x [n]) for n=3,4,5. Every H is present-legal (keys(T0)=[n]).
For each: legality/MSTL check (violations => MSTL-14P COUNTEREXAMPLE, exit 2),
then canonical least-loaded max-minload. Kill: minload>=3 (exit 2 + witness).
Record: max minload over the whole cell, #minload-2 witnesses, max e_B, max drain.
Budgets: n=3 L<=7 (6^7=279936 x 5 T0); n=4 L<=5 (8^5=32768 x 14 T0);
n=5 L<=4 (10^4 x 42 T0). Skip cells by env EX00_CELLS="3,4".
NEW artifact: exhaustive.json. Sealed files untouched.
"""
from __future__ import annotations
import sys
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_eventflow_abl import build_tagged
from solver import encode as E


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


def all_bsts(keys):
    """All BST shapes over sorted keys as nested [k,l,r] lists (None empty)."""
    keys = list(keys)
    if not keys:
        return [None]
    out = []
    for i, k in enumerate(keys):
        for l in all_bsts(keys[:i]):
            for r in all_bsts(keys[i + 1:]):
                out.append([k, l, r])
    return out


def maxminload(n, T0, H):
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
            return 99, j
    return best, best_at


def main() -> int:
    step("EX-00", "Small-n exhaustive Stage-B")
    import json
    cells = os.environ.get("EX00_CELLS", "3,4,5")
    want = set(c.strip() for c in cells.split(","))
    out = {}
    import itertools
    plans = [(3, 7), (4, 5), (5, 4)]
    for (n, L) in plans:
        if str(n) not in want:
            continue
        trees = all_bsts(range(1, n + 1))
        moves = [[m, x] for m in ("KEEP", "DELETE") for x in range(1, n + 1)]
        step("EX-N", "n=%d L=%d trees=%d moves/H=%d" % (n, L, len(trees), len(moves) ** L))
        cell_max = -1
        cell_ex = None
        n_m2 = 0
        total = 0
        for ti, T0 in enumerate(trees):
            seq = [0] * L
            done = False
            while not done:
                H = [list(moves[i]) for i in seq]
                v, at = maxminload(n, T0, H)
                total += 1
                if v == -2:
                    step("EX-KILL", "MSTL-14P COUNTEREXAMPLE n=%d H=%s" % (n, H))
                    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "exkill.json").write_text(
                        json.dumps({"kill": "MSTL", "n": n, "T0": T0, "H": H}, indent=1, default=str),
                        encoding="utf-8")
                    return 2
                if v == 99:
                    step("EX-KILL", "STAGE-B STARVATION n=%d H=%s at=%s" % (n, H, at))
                    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "starve.json").write_text(
                        json.dumps({"kill": True, "n": n, "T0": T0, "where": at, "H": H}, indent=1, default=str),
                        encoding="utf-8")
                    return 2
                if v > cell_max:
                    cell_max = v
                    cell_ex = {"T0": T0, "H": list(H), "at": at}
                    step("EX-NEW", "n=%d newmax=%d" % (n, v))
                if v >= 2:
                    n_m2 += 1
                if total % 200000 == 0:
                    step("EX-PROG", "n=%d total=%d max=%d" % (n, total, cell_max))
                for p in range(L - 1, -1, -1):
                    seq[p] += 1
                    if seq[p] < len(moves):
                        break
                    seq[p] = 0
                    if p == 0:
                        done = True
        out[str(n)] = {"L": L, "trees": len(trees), "total": total,
                       "maxminload": cell_max, "n_m2": n_m2, "ex": cell_ex}
        step("EX-CELL", "n=%d done total=%d max=%d m2=%d" % (n, total, cell_max, n_m2))
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "exhaustive.json").write_text(
        json.dumps(out, indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

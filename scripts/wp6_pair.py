"""WP-6 PAIR: supply-free push pairing check (C167).

For each supply-free KEEP push (e_A==0, e_B>=1) on key z, verify the
pairing structure: a same-key banking arrival (DELETE-z rooting z in A)
with FROZEN B-depth between arrival and push (no B-touching access on
any key in between would unroot z from A, so between-events must be
DELETE-z no-ops; B-depth must be identical at both times), or classify
as GENESIS-ROOT (z never accessed and z == T0 root key). Reports pairing
rate, frozen violations, genesis-root count, arrival banking distribution.
Artifact: pair.json. Sealed files untouched.
"""
from __future__ import annotations
import sys
import json
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_pushledger import gen
from wp6_eventflow import to_ptr, splay_A, splay_B_push
from solver import encode as E


def step(sid, msg):
    print("[WP-6][PAIR %s] %s" % (sid, msg), flush=True)


def depths_of(T):
    dd = {}
    stack = [(T, 0)]
    while stack:
        nd, d = stack.pop()
        if nd is None:
            continue
        dd[nd["k"]] = d
        stack.append((nd["l"], d + 1))
        stack.append((nd["r"], d + 1))
    return dd


def main() -> int:
    step("PR-00", "supply-free push pairing check")
    agg = Counter()
    agg["arr_bank_min"] = None
    done = 0
    for s in range(150):
        n, T0, H = gen(s, b"mc")
        try:
            pre = E.precompute(n, T0, H)
            bad = E.exec_counts(pre, "P_all", 6, 2, (2, 2))["violations"]
        except Exception:
            continue
        if bad:
            continue
        done += 1
        A, B = to_ptr(T0), to_ptr(T0)
        T0root = T0[0]
        # per-access snapshots: (mode, x, eA, eB, dA, dB, dBmap)
        snaps = []
        accessed = set()
        for acc in pre:
            x, mode = acc["x"], acc["mode"]
            da = depths_of(A).get(x)
            dBmap_b = depths_of(B)
            db = dBmap_b.get(x)
            A, invs = splay_A(A, x)
            eA = len(invs)
            if mode == "KEEP":
                B, pushes = splay_B_push(B, x)
                eB = len(pushes)
            else:
                eB = 0
            snaps.append({"mode": mode, "x": x, "eA": eA, "eB": eB,
                          "dA": da, "dB": db, "dBb": dict(dBmap_b),
                          "dBa": depths_of(B)})
            accessed.add(x)
        # check each supply-free push
        for t, r in enumerate(snaps):
            if not (r["mode"] == "KEEP" and r["eA"] == 0 and r["eB"] >= 1):
                continue
            z = r["x"]
            agg["sf_n"] += 1
            # last DELETE-z strictly before t (arrival candidate)
            arr = -1
            for u in range(t - 1, -1, -1):
                if snaps[u]["x"] == z and snaps[u]["mode"] == "DELETE":
                    arr = u
                    break
            if arr < 0:
                # genesis-root? z never KEEP/DELETE before and z == T0 root
                prior = [u for u in range(t) if snaps[u]["x"] == z]
                if not prior and z == T0root:
                    agg["sf_genesis"] += 1
                else:
                    agg["sf_nopair"] += 1
                continue
            agg["sf_pair"] += 1
            # frozen B between arr and t?
            if snaps[arr]["dBa"].get(z) != r["dBb"].get(z):
                agg["sf_unfrozen"] += 1
            # arrival banking
            ab = 3 * snaps[arr]["eA"]
            if agg["arr_bank_min"] is None or ab < agg["arr_bank_min"]:
                agg["arr_bank_min"] = ab
            # pair net
            agg["pair_net_min"] = min(agg.get("pair_net_min", 10 ** 9),
                                      ab - r["eB"])
    out = dict(agg)
    out.update({"evals": done})
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "pair.json").write_text(
        json.dumps(out, indent=1, sort_keys=True, default=str), encoding="utf-8")
    step("PR-01", json.dumps(out, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())

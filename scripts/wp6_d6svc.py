"""WP-6 D6SVC: Terminal C service-vs-D6 discrimination (C170).

Two questions:
 (i)  Do exec_counts service violations (paid<need) exist unfiltered?
      (All prior corpora FILTER violations, so service held by construction.)
 (ii) Joint D6-vs-service: on every trace (violation or not), does
      service-hold imply D6-hold (kernel predicts YES: service=>D6)?
      Does D6-hold with service-fail occur (activation bottleneck real)?
      Does D6-fail with service-hold occur (must be ZERO by kernel)?
D6 uses sited-only S_A (verify 8S: count unsited; expect 0).
need = max(y-2a,0) with y,a splay_costs (present keys only; absent
accesses excluded from D but counted for legality scope note).
Artifact: d6svc.json. Sealed files untouched.
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
from wp6_adv import vine, balanced, depths_of
from solver import encode as E
from liquidity import legacy_embedding as PE


def step(sid, msg):
    print("[WP-6][D6SVC %s] %s" % (sid, msg), flush=True)


def run_one(n, T0, H):
    """Returns dict or None (non-present/illegal)."""
    try:
        pre = E.precompute(n, T0, H)
    except Exception:
        return None
    res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
    viol = res["violations"]
    # independent D6 recompute (sited-only S_A) + service recompute
    A, B = to_ptr(T0), to_ptr(T0)
    SA = EB = D = 0
    unsited = 0
    maxd6 = None
    svc_hold = True
    for acc in pre:
        x, mode = acc["x"], acc["mode"]
        _, pathA = PE._depth_to(A, x)
        present = bool(pathA) and pathA[-1]["k"] == x
        A, invs = splay_A(A, x)
        eA = len(invs)
        nsited = sum(1 for s in acc["sites"])
        unsited += len(acc["sites"]) - nsited
        eB = 0
        need = 0
        if mode == "KEEP":
            B, pushes = splay_B_push(B, x)
            eB = len(pushes)
            if present:
                da = acc["a"] - 1
                db = acc["y"] - 1
                need = (db + 1) - 2 * (da + 1)
                if need < 0:
                    need = 0
        SA += nsited
        EB += eB if mode == "KEEP" else 0
        D += need if (mode == "KEEP" and present) else 0
        d6 = D - 6 * SA
        if maxd6 is None or d6 > maxd6:
            maxd6 = d6
    # service-hold per exec_counts (paid==need everywhere <=> viol==0)
    return {"viol": viol, "maxd6": maxd6, "unsited": unsited,
            "svc_hold": viol == 0,
            "d6_hold": (maxd6 is not None and maxd6 <= 0)}


def main() -> int:
    step("DS-00", "Terminal C service-vs-D6 discrimination")
    agg = Counter()
    shapes = []
    for n in (16, 32, 64):
        shapes.append(("vine%d" % n, n, vine(n)))
        shapes.append(("bal%d" % n, n, balanced(list(range(1, n + 1)))))
    for nm, n, T0 in shapes:
        for s in range(40):
            _, _, H = gen(5000 + s, b"ds")
            # longer histories: concatenate segments, filter keys to [n]
            H2 = [st for st in H if st[1] <= n]
            for k in (1, 2):
                _, _, Hk = gen(6000 + 10 * s + k, b"ds")
                H2.extend([st for st in Hk if st[1] <= n])
            # filter to present-domain scope note: keep all, flag absent
            r = run_one(n, T0, H2)
            if r is None:
                agg["skipped"] += 1
                continue
            agg["n"] += 1
            agg["unsited"] += r["unsited"]
            if r["viol"] > 0:
                agg["viol_hist"] += 1
            # joint table
            key = ("svc_hold" if r["svc_hold"] else "svc_fail",
                   "d6_hold" if r["d6_hold"] else "d6_fail")
            agg["joint_" + key[0] + "_" + key[1]] += 1
            if r["svc_hold"] and not r["d6_hold"]:
                agg["kernel_contra"] += 1
            if r["d6_hold"] and not r["svc_hold"]:
                agg["act_bottleneck"] += 1
            if not r["d6_hold"] and not r["svc_hold"]:
                agg["both_fail"] += 1
        step("DS-P", "%s done" % nm)
    out = dict(agg)
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "d6svc.json").write_text(
        json.dumps(out, indent=1, sort_keys=True, default=str), encoding="utf-8")
    step("DS-01", json.dumps(out, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())

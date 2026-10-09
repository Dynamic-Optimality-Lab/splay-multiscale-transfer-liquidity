"""WP-6 GISTEP: per-StepEv GI coin-creation measurement (C179).

Decisive for the GI bridge: is NET coin creation per A-StepEv bounded by
a UNIVERSAL constant (witness-interval phenomenon: gross flips cancel),
or does it scale with moved-subtree sizes (unbounded => GI dead)?
Instruments stepwise splay (phi after EACH StepEv) on histories + crafted
deep splays, n up to 512. Records max |dphi| per StepEv + distribution +
correlation with moved-subtree sizes. Boundedness => prove reference-move
bound => GI bridge to constant-factor Pair Access. Unbounded => corpse.
Artifact: gistep.json. Sealed files untouched.
"""
from __future__ import annotations
import sys
import json
from pathlib import Path
from collections import Counter

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_pushledger import gen
from wp6_eventflow import to_ptr
from wp6_giscale import bounds, phi_of
from wp6_adv import vine, balanced
from liquidity import legacy_embedding as PE
from solver import encode as E


def step(sid, msg):
    print("[WP-6][GISTEP %s] %s" % (sid, msg), flush=True)


def subtree_size(nd):
    if nd is None:
        return 0
    return 1 + subtree_size(nd["l"]) + subtree_size(nd["r"])


def stepwise_splay_phi(A, B, n, x, loB, hiB, rec):
    """Replay A-splay capturing per-StepEv (dphi, moved_subtree_sizes)."""
    d, path = PE._depth_to(A, x)
    if not path or path[-1]["k"] != x:
        return A
    node = path[-1]
    while node["p"] is not None:
        p = node["p"]
        g = p["p"]
        # moved subtrees ~ sizes of rotated-off parts (approx by p-subtree)
        movesz = subtree_size(p)
        loA0, hiA0 = bounds(A, n)
        ph0 = phi_of(B, A, n, loB, hiB, loA0, hiA0)
        if g is None:
            if p["l"] is node:
                PE._rot_right(p)
            else:
                PE._rot_left(p)
        elif p["l"] is node and g["l"] is p:
            PE._rot_right(g)
            PE._rot_right(p)
        elif p["r"] is node and g["r"] is p:
            PE._rot_left(g)
            PE._rot_left(p)
        elif p["r"] is node and g["l"] is p:
            PE._rot_left(p)
            PE._rot_right(g)
        else:
            PE._rot_right(p)
            PE._rot_left(g)
        loA1, hiA1 = bounds(A, n)
        ph1 = phi_of(B, A, n, loB, hiB, loA1, hiA1)
        dphi = ph1 - ph0
        rec["nsteps"] += 1
        if abs(dphi) > rec["max_abs"]:
            rec["max_abs"] = abs(dphi)
            rec["max_rec"] = {"dphi": dphi, "movesz": movesz}
        rec["hist"].append(dphi)
    while node["p"] is not None:
        node = node["p"]
    return node


def main() -> int:
    step("GS-00", "per-StepEv GI creation measurement")
    out = {"by_n": {}}
    for n in (32, 64, 128, 256, 512):
        nh = {32: 12, 64: 8, 128: 5, 256: 3, 512: 2}[n]
        rec = Counter()
        rec["max_abs"] = 0
        rec["hist"] = []
        done = 0
        for s in range(nh):
            T0 = vine(n) if s % 2 == 0 else balanced(list(range(1, n + 1)))
            _, _, H = gen(8000 + s, b"gs")
            H = [st for st in H if st[1] <= n]
            if not H:
                continue
            try:
                pre = E.precompute(n, T0, H)
                bad = E.exec_counts(pre, "P_all", 6, 2, (2, 2))["violations"]
            except Exception:
                continue
            if bad:
                continue
            done += 1
            A, B = to_ptr(T0), to_ptr(T0)
            loB, hiB = bounds(B, n)
            for acc in pre:
                x = acc["x"]
                A = stepwise_splay_phi(A, B, n, x, loB, hiB, rec)
                if acc["mode"] == "KEEP":
                    from wp6_eventflow import splay_B_push
                    B, _ = splay_B_push(B, x)
                    loB, hiB = bounds(B, n)
        import statistics
        h = rec["hist"]
        out["by_n"][str(n)] = {"evals": done, "nsteps": rec["nsteps"],
                               "max_abs": rec["max_abs"],
                               "max_rec": rec.get("max_rec"),
                               "med_abs": statistics.median([abs(v) for v in h]) if h else 0,
                               "p99_abs": sorted([abs(v) for v in h])[int(0.99 * len(h))] if h else 0}
        step("GS-P", "n=%d done=%d max=%s med=%s" % (
            n, done, rec["max_abs"], out["by_n"][str(n)]["med_abs"]))
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "gistep.json").write_text(
        json.dumps(out, indent=1, sort_keys=True, default=str), encoding="utf-8")
    step("GS-01", json.dumps(out, sort_keys=True, default=str)[:500])
    return 0


if __name__ == "__main__":
    sys.exit(main())

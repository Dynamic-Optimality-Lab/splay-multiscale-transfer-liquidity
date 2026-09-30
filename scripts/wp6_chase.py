"""WP-6 STEP CH-00: chase-pusher conjunction-sustain falsifier (breakdown-point).

Victim x T0-shallow, FIRST-x discipline (K/E4 empty). Greedy sustain loop:
each step picks KEEP-z maximizing B-deepening of x under constraints:
  PUSH: B-depth(x) strictly up (x on z's B-path, descends);
  AVOID: A-depth(x) unchanged (z's A-path avoids displacing x);
  STERILE: new-A-rotated(z) disjoint from x's current B-path-zone triples;
  HOLE: e_A(z-access)==0 (z A-root repeat: E2-hole, creates nothing).
If no candidate satisfies all: record BREAKDOWN (which leg failed: nopush /
displace / overlap / nonhole / shallow-lost) and STRIKE (first-ever KEEP-x).
Score: shortfall (KILL -> hallkill + §24), N-composition at strike
(E1/E2/E4/K/W sizes), e_B vs 3|N|, sustained-push count, breakdown leg.
NEW artifact: chase.json (+hallkill on kill). Sealed files untouched.
"""
from __future__ import annotations
import sys
import copy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_hallcore import build_graph, maxflow_cap3, delta_of
from wp6_eventflow import to_ptr, splay_A, splay_B_push
from wp6_eventflow_abl import build_tagged
from wp6_offline import gc_gap
from wp6_tightest import vine, Rng
from liquidity import legacy_embedding as PE
from solver import encode as E


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


import hashlib as _h


def adepth(A, x):
    d, path = PE._depth_to(A, x)
    return d if (path and path[-1]["k"] == x) else None


def bpath_keys(B, x):
    d, path = PE._depth_to(B, x)
    if not path or path[-1]["k"] != x:
        return set()
    return set(nd["k"] for nd in path)


def bnear_below(B, x, dist=5):
    """Keys in x's B-subtree within `dist` levels below x (push candidates:
    splashing just-below-x pushes x down; far-below splashes LIFT x)."""
    d, path = PE._depth_to(B, x)
    if not path or path[-1]["k"] != x:
        return []
    node = path[-1]
    out = []
    stack = [(node["l"], 1), (node["r"], 1)]
    while stack:
        nd, dd = stack.pop()
        if nd is None or dd > dist:
            continue
        out.append(nd["k"])
        stack.append((nd["l"], dd + 1))
        stack.append((nd["r"], dd + 1))
    return out


def eval_hist(n, T0, H):
    G = build_graph(n, T0, H)
    if G is None:
        return None
    f, nb, lv = maxflow_cap3(G)
    if nb - f > 0:
        return ("KILL", nb - f, nb)
    gap, _ = gc_gap(n, T0, H)
    return ("OK", nb, gap)


def main() -> int:
    step("CH-00", "Chase-pusher conjunction-sustain falsifier")
    import json
    from collections import Counter
    TP = ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "chase.json"
    best = None
    breakdown = Counter()
    tags = Counter()
    evals = 0
    maxpush = 0
    for s in range(400):
        rng = Rng(("s%d" % s).encode(), b"ch")
        r = rng(0)
        n = 128
        T0 = vine(n, True)
        x = 122 + (r >> 3) % 6
        H = []
        A, B = to_ptr(T0), to_ptr(T0)
        # a few far-zone positioners first (avoid x), then chase loop
        for i in range(2 + (r >> 11) % 4):
            z = 1 + (r >> (13 + 3 * i)) % 50
            if z == x:
                z = (z + 7) % n + 1
            m = "DELETE" if (r >> (17 + i)) % 2 else "KEEP"
            H.append([m, z])
            A, _ = splay_A(A, z)
            if m == "KEEP":
                B, _ = splay_B_push(B, z)
        pushes = 0
        leg = None
        impure = False
        for it in range(40):
            da0 = adepth(A, x)
            db0 = adepth(B, x)
            if da0 is None or db0 is None:
                leg = "absent"
                break
            bzone = bpath_keys(B, x)
            cands = []
            # trial order: B-nearby-below first (push x down), then offset scan
            near = [z for z in bnear_below(B, x) if z != x]
            order = near + [z for z in range(1, n + 1) if z != x and z not in set(near)]
            off = (r >> (7 + it)) % max(1, len(order))
            order = order[off:] + order[:off]
            for z in order:
                if z == x:
                    continue
                A2 = copy.deepcopy(A)
                B2 = copy.deepcopy(B)
                A2t, invs = splay_A(A2, z)
                # B-side trial ALWAYS (hole-pushers: trivial-A + real-B-splash)
                B2t, po = splay_B_push(B2, z)
                if not po:
                    continue  # B-no-op: pushes nothing
                db1 = adepth(B2t, x)
                da1 = adepth(A2t, x)
                if db1 is None or da1 is None or db1 <= db0:
                    continue  # no push of x
                disp = 1 if da1 != da0 else 0
                newrot = set()
                for S in invs:
                    newrot |= set(S)
                over = 1 if (newrot & bzone) else 0
                hole = 0 if not invs else 1
                # score: prefer (no-displace, no-overlap, hole); tie-break hash
                cands.append(((disp, over, hole), z, A2t, B2t, invs))
            if not cands:
                leg = "nopush"
                break
            cands.sort(key=lambda c: (c[0], (r >> (11 + it)) % 7))
            tag = cands[0][0]
            if tag != (0, 0, 0):
                impure = True
                leg = "push-but-%s" % ("|".join(n for n, f in
                       (("displace", tag[0]), ("overlap", tag[1]), ("nonhole", tag[2])) if f),)
                # continue deepening anyway with best available (diagnostic)
            tags[tag] += 1
            _, z, A2t, B2t, invs = cands[0]
            H.append(["KEEP", z])
            A, B = A2t, B2t
            pushes += 1
        # STRIKE (first-ever KEEP-x)
        if any(a[1] == x for a in H):
            continue
        H.append(["KEEP", x])
        v = eval_hist(n, T0, H)
        evals += 1
        if v is None:
            continue
        if v[0] == "KILL":
            step("CH-KILL", "HALL s=%d shortfall=%d pushes=%d leg=%s" % (s, v[1], pushes, leg))
            TP.write_text(json.dumps({"kill": True, "H": H}, indent=1, default=str), encoding="utf-8")
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json").write_text(
                json.dumps({"kill": True, "H": H}, indent=1, default=str), encoding="utf-8")
            return 2
        _, nb, gap = v
        if gap > 0:
            step("CH-KILL", "GC s=%d" % s)
            return 2
        maxpush = max(maxpush, pushes)
        if leg is None and not impure and pushes > 0:
            breakdown["pure-sustain"] += 1
        elif leg is not None:
            breakdown[leg + ("|somepush" if pushes > 0 else "|nopush-ever")] += 1
        else:
            breakdown["mixed-impure"] += 1
        if best is None or pushes > best[0]:
            best = (pushes, nb)
            TP.write_text(json.dumps({"evals": evals, "best_pushes": pushes, "B": nb,
                                      "breakdown": dict(breakdown)},
                                     indent=1, sort_keys=True, default=str), encoding="utf-8")
        if s % 100 == 0:
            step("CH-02", "s=%d evals=%d best=%s breakdown=%s" % (s, evals, best, dict(breakdown)))
    step("CH-03", "evals=%d best=%s breakdown=%s maxpush=%d tags=%s" % (
        evals, best, dict(breakdown), maxpush, {str(k): v for k, v in tags.items()}))
    TP.write_text(json.dumps({"evals": evals, "best_pushes": best[0] if best else None,
                              "breakdown": dict(breakdown), "maxpush": maxpush,
                              "tags": {str(k): v for k, v in tags.items()}},
                             indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

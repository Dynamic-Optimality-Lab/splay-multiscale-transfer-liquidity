"""WP-6 RIDES: burst-relative silent-push census (C147).

8V pusher-counting needs bursts built LOUDLY (pushers imprint chain
positions via E3, covering demand). Killer scenario: bursts built by SILENT
pushes (+2 G-outer rides with no triple containing the victim: no E3).
Per heavy burst (e_B >= 8, victim x at access J): walk back over prior KEEP
accesses; each pushing access (gain_t(x) = depth_{t+1}(x) - depth_t(x) > 0)
is classified SILENT (none of its sited Aevs E3-hit burst-J B-events) vs
IMPRINTING (>= 1 hit + hit count). Output: silent-push share of burst depth
(sum silent gains / total positive gains), silent-access fraction, and the
worst bursts (max silent-built depth). Near-zero => 8V closes modulo
counting (all-imprint supply); substantial => ride-sterility is live.
Artifact: rides.json. Sealed files untouched.
"""
from __future__ import annotations
import sys
import json
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_tightest import vine
from wp6_eventflow import to_ptr, splay_A, splay_B_push, root_key
from solver import encode as E


def step(sid, msg):
    print("[WP-6][RIDES %s] %s" % (sid, msg), flush=True)


def depth_of(T, x):
    d, cur = 0, T
    while cur is not None:
        if x == cur["k"]:
            return d
        cur = cur["l"] if x < cur["k"] else cur["r"]
        d += 1
    return None


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


def run_hist(n, T0, H):
    """Replay both trees. B-depths drive demand/gains; A-rot sets supply E3."""
    pre = E.precompute(n, T0, H)
    A = to_ptr(T0)
    B = to_ptr(T0)
    bdepths = []  # per access idx: B key->depth BEFORE splay
    arots = []    # per access idx: list of (rotset, sited)
    btris = []    # per access idx: list of B-push triples (KEEP only)
    eBs = []
    for idx, acc in enumerate(pre):
        bdepths.append(depths_of(B))
        A, invs = splay_A(A, acc["x"])
        ar = []
        for k, (S, sited) in enumerate(zip(invs, acc["sites"])):
            ar.append((frozenset(S), bool(sited)))
        arots.append(ar)
        if acc["mode"] == "KEEP":
            B, pushes = splay_B_push(B, acc["x"])
            tris = []
            for P in pushes:
                tris.append(set(P) | {acc["x"]})
            btris.append(tris)
            eBs.append(len(pushes))
        else:
            btris.append([])
            eBs.append(0)
    return pre, bdepths, arots, btris, eBs


def analyze(n, T0, H):
    pre, depths, arots, btris, eBs = run_hist(n, T0, H)
    depths = depths  # B-depths (demand side)
    out = []
    L = len(pre)
    for J in range(L):
        if pre[J]["mode"] != "KEEP" or eBs[J] < 8:
            continue
        x = pre[J]["x"]
        dJ = depths[J].get(x)
        if dJ is None:
            continue
        tot = 0
        sil = 0
        nsil_acc = 0
        npush_acc = 0
        for t in range(0, J):
            if pre[t]["mode"] != "KEEP":
                continue
            d0 = depths[t].get(x)
            # depth after access t = depth before access t+1 (A-tree evolves every access incl DELETE)
            d1 = depths[t + 1].get(x) if t + 1 < L else None
            if d0 is None or d1 is None:
                continue
            g = d1 - d0
            if g <= 0:
                continue
            tot += g
            npush_acc += 1
            # E3-hits from access-t sited Aevs to burst-J B-events
            hits = 0
            for (S, sited) in arots[t]:
                if not sited:
                    continue
                for tri in btris[J]:
                    if S & tri:
                        hits += 1
                        break
            if hits == 0:
                sil += g
                nsil_acc += 1
        kx = 0
        for t in range(0, J):
            if pre[t]["x"] == x:
                kx += sum(1 for (S, sited) in arots[t] if sited)
        out.append({"J": J, "x": x, "eB": eBs[J], "depth": dJ,
                    "push": tot, "silent": sil,
                    "npush": npush_acc, "nsil": nsil_acc, "kx": kx})
    return out


def gen(s, tag):
    from wp6_tightest import Rng
    rng = Rng(("rd%d" % s).encode(), tag)
    r = rng(0)
    n = [64, 128, 256][r % 3]
    T0 = vine(n, (r >> 8) % 2 == 0)
    H = []
    L = 40 + (r >> 16) % 30
    xc = 2 + (r >> 24) % (n - 2)
    for i in range(L):
        rr = Rng(("rd%d" % s).encode(), tag + b"h%d" % i)
        q = rr(3000 + i)
        op = (q >> 2) % 10
        if op < 3:
            H.append(["DELETE", xc])
        elif op < 6:
            z = min(n, max(1, xc + [-3, -2, -1, 1, 2, 3][(q >> 9) % 6]))
            H.append(["DELETE", z])
            H.append(["KEEP", z])
        else:
            H.append(["KEEP", xc])
        if (q >> 5) % 4 == 0:
            xc = 1 + (q >> 11) % n
    return n, T0, H


def main() -> int:
    step("RD-00", "burst-relative silent-push census")
    bursts = 0
    stot = 0
    ssil = 0
    worst = []
    acc_push = 0
    acc_sil = 0
    kx_cov = []
    for s in range(120):
        n, T0, H = gen(s, b"rd")
        try:
            res = E.precompute(n, T0, H)
            bad = E.exec_counts(res, "P_all", 6, 2, (2, 2))["violations"]
        except Exception:
            continue
        if bad:
            continue
        for b in analyze(n, T0, H):
            bursts += 1
            stot += b["push"]
            ssil += b["silent"]
            acc_push += b["npush"]
            acc_sil += b["nsil"]
            frac = (b["silent"] / b["push"]) if b["push"] else 0.0
            worst.append((frac, b["eB"], b["depth"], b["J"], s))
            if b["eB"] > 0:
                kx_cov.append(3 * b["kx"] / b["eB"])
        if s % 30 == 29:
            step("RD-P", "s=%d bursts=%d" % (s, bursts))
    worst.sort(reverse=True)
    kx_cov.sort()
    out = {"bursts": bursts, "push_events": acc_push, "silent_events": acc_sil,
           "depth_pushed": stot, "depth_silent": ssil,
           "silent_frac": (ssil / stot if stot else None),
           "kx_cover_med": (kx_cov[len(kx_cov) // 2] if kx_cov else None),
           "kx_cover_min": (kx_cov[0] if kx_cov else None),
           "worst": [{"frac": f, "eB": e, "depth": d, "J": j, "s": s}
                     for (f, e, d, j, s) in worst[:15]]}
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "rides.json").write_text(
        json.dumps(out, indent=1, sort_keys=True, default=str), encoding="utf-8")
    step("RD-01", json.dumps({k: v for k, v in out.items() if k != "worst"}, sort_keys=True))
    for w in worst[:8]:
        step("RD-W", "frac=%.2f eB=%d depth=%d J=%d s=%d" % w)
    return 0


if __name__ == "__main__":
    sys.exit(main())

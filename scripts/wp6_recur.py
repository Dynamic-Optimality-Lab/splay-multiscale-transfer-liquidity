"""WP-6 RECUR: chain-key recurrence census (C150).

8AC-WWIT: W-edges are mediated by non-xx witness keys (past-rotated keys
reappearing on current B-paths). The W-residual needs recurrence to be
RELIABLE. Per B-event (triple T = pushed + {xx}): for each key, ever
imprinted before (in a past sited A-rotated set)? recency (t - latest
imprinting access)? Aggregate: recurrence rate overall + by position
(xx vs pushed), recency med/p90/max, per-heavy-burst triple coverage
(fraction imprinted; min over bursts), imprint source mix (same-x access
vs other). Near-1 coverage with recent recency => recurrence reliable
(finite face for 8AC-REC density); gaps => characterize.
Artifact: recur.json. Sealed files untouched.
"""
from __future__ import annotations
import sys
import json
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_tightest import vine, Rng
from wp6_eventflow import to_ptr, splay_A, splay_B_push
from solver import encode as E


def step(sid, msg):
    print("[WP-6][RECUR %s] %s" % (sid, msg), flush=True)


def run_hist(n, T0, H):
    """Replay: per KEEP access, B-triples; per access, sited A-rotated keysets."""
    pre = E.precompute(n, T0, H)
    A, B = to_ptr(T0), to_ptr(T0)
    arots = []   # per access: list of (frozenset(S), sited, acc_x)
    btris = []   # per access: list of triples (KEEP) else []
    for idx, acc in enumerate(pre):
        A, invs = splay_A(A, acc["x"])
        ar = []
        for (S, sited) in zip(invs, acc["sites"]):
            ar.append((frozenset(S), bool(sited), acc["x"]))
        arots.append(ar)
        if acc["mode"] == "KEEP":
            B, pushes = splay_B_push(B, acc["x"])
            btris.append([set(P) | {acc["x"]} for P in pushes])
        else:
            btris.append([])
    return pre, arots, btris


def analyze(n, T0, H):
    pre, arots, btris = run_hist(n, T0, H)
    L = len(pre)
    # imprint time: key -> latest access idx with sited A-rot containing it
    lastimp = {}
    out_ev = Counter()
    rec = Counter()
    out_burst = []
    for J in range(L):
        if pre[J]["mode"] != "KEEP" or not btris[J]:
            # still record imprints below
            pass
        # first answer queries for this access's triples using past only
        if pre[J]["mode"] == "KEEP" and btris[J]:
            xx = pre[J]["x"]
            cov = []
            for tri in btris[J]:
                hit = 0
                for w in tri:
                    out_ev["tri_keys"] += 1
                    if w == xx:
                        out_ev["xx_pos"] += 1
                    if w in lastimp:
                        hit += 1
                        out_ev["recur"] += 1
                        rec[J - lastimp[w]] += 1
                    else:
                        out_ev["fresh"] += 1
                cov.append(hit / len(tri) if tri else 1.0)
            if cov:
                out_burst.append((sum(cov) / len(cov), len(btris[J]), J))
        # then bank this access's imprints
        for (S, sited, ax) in arots[J]:
            if not sited:
                continue
            for w in S:
                lastimp[w] = J
    return out_ev, rec, out_burst


def gen(s, tag):
    rng = Rng(("rc%d" % s).encode(), tag)
    r = rng(0)
    n = [64, 128, 256][r % 3]
    T0 = vine(n, (r >> 8) % 2 == 0)
    H = []
    L = 40 + (r >> 16) % 30
    xc = 2 + (r >> 24) % (n - 2)
    for i in range(L):
        rr = Rng(("rc%d" % s).encode(), tag + b"h%d" % i)
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
    step("RC-00", "chain-key recurrence census")
    tot_ev = Counter()
    tot_rec = Counter()
    covs = []
    worst = []
    min_nz = [None, None]
    done = 0
    for s in range(120):
        n, T0, H = gen(s, b"rc")
        try:
            res = E.precompute(n, T0, H)
            bad = E.exec_counts(res, "P_all", 6, 2, (2, 2))["violations"]
        except Exception:
            continue
        if bad:
            continue
        done += 1
        ev, rec, bursts = analyze(n, T0, H)
        tot_ev.update(ev)
        tot_rec.update(rec)
        for (c, nb, J) in bursts:
            covs.append(c)
            if nb >= 8:
                worst.append((c, nb, J, s))
                if J > 0 and (min_nz[0] is None or c < min_nz[0]):
                    min_nz[0] = c
                    min_nz[1] = (nb, J, s)
        if s % 30 == 29:
            step("RC-P", "s=%d" % s)
    worst.sort()
    covs.sort()
    out = {"evals": done,
           "tri_keys": tot_ev["tri_keys"], "xx_pos": tot_ev["xx_pos"],
           "recur": tot_ev["recur"], "fresh": tot_ev["fresh"],
           "recur_rate": (tot_ev["recur"] / tot_ev["tri_keys"] if tot_ev["tri_keys"] else None),
           "rec_med": None, "rec_p90": None, "rec_max": None,
           "burst_cov_med": (covs[len(covs) // 2] if covs else None),
           "burst_cov_min": (covs[0] if covs else None),
           "heavy_cov_min_nz": min_nz[0],
           "heavy_cov_min_nz_ex": min_nz[1],
           "worst": [{"cov": c, "nb": nb, "J": J, "s": s} for (c, nb, J, s) in worst[:12]]}
    # recency from Counter over depths
    tot = sum(tot_rec.values())
    if tot:
        acc = 0
        med = p90 = mx = None
        for d in sorted(tot_rec):
            acc += tot_rec[d]
            mx = d
            if med is None and acc * 2 >= tot:
                med = d
            if p90 is None and acc * 10 >= 9 * tot:
                p90 = d
        out["rec_med"] = med
        out["rec_p90"] = p90
        out["rec_max"] = mx
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "recur.json").write_text(
        json.dumps(out, indent=1, sort_keys=True, default=str), encoding="utf-8")
    step("RC-01", json.dumps({k: v for k, v in out.items() if k != "worst"}, sort_keys=True))
    for w in worst[:8]:
        step("RC-W", "cov=%.2f nb=%d J=%d s=%d" % w)
    return 0


if __name__ == "__main__":
    sys.exit(main())

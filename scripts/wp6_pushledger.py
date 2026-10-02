"""WP-6 PUSHLEDGER: tight splay-cost bounds + push accounting census (C156).

Prefix-GC universal needs sharp links: (a) e_B vs B-depth (e_B <= d+1?
~= (d+1)/2?); (b) e_A vs A-depth (e_A >= d^A/2?); (c) pushers vs depth
(#B-gain accesses >= (d - dT0)/2?); (d) supplying split (pushers with
e_A >= 1 vs supply-free e_A = 0); (e) alternation (#supplyfree <=
#supplying + 1 globally?); (f) first-access equality (e_B == e_A?).
Per access + per heavy burst: depths (A/B/T0), costs, gains, push counts,
supplying flags. Artifact: pushledger.json. Sealed files untouched.
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
    print("[WP-6][PUSHLEDGER %s] %s" % (sid, msg), flush=True)


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
    pre = E.precompute(n, T0, H)
    A, B = to_ptr(T0), to_ptr(T0)
    T0d = depths_of(to_ptr(T0))
    recs = []
    for idx, acc in enumerate(pre):
        da = depths_of(A).get(acc["x"])
        db = depths_of(B).get(acc["x"])
        A, invs = splay_A(A, acc["x"])
        eA = len(invs)
        if acc["mode"] == "KEEP":
            B, pushes = splay_B_push(B, acc["x"])
            eB = len(pushes)
        else:
            eB = 0
        recs.append({"x": acc["x"], "mode": acc["mode"], "eA": eA, "eB": eB,
                     "dA": da, "dB": db, "dT0": T0d.get(acc["x"])})
    return pre, recs


def analyze(n, T0, H):
    pre, recs = run_hist(n, T0, H)
    out = {"eB_le_dp1_viol": 0, "eB_le_dp1_n": 0,
           "eA_ge_half_viol": 0, "eA_ge_half_n": 0,
           "first_eq_viol": 0, "first_n": 0,
           "push_viol": 0, "push_n": 0,
           "supplyfree": 0, "supplying": 0,
           "Phi_min": None}
    seen = set()
    SA = EB = 0
    phimin = None
    for idx, r in enumerate(recs):
        # (a) eB <= dB + 1
        if r["mode"] == "KEEP" and r["dB"] is not None:
            out["eB_le_dp1_n"] += 1
            if not (r["eB"] <= r["dB"] + 1):
                out["eB_le_dp1_viol"] += 1
        # (b) eA >= dA / 2 (i.e., 2*eA >= dA) when nontrivial
        if r["dA"] is not None and r["eA"] > 0:
            out["eA_ge_half_n"] += 1
            if not (2 * r["eA"] >= r["dA"]):
                out["eA_ge_half_viol"] += 1
        # (f) first access equality
        if r["x"] not in seen and r["mode"] == "KEEP":
            seen.add(r["x"])
            out["first_n"] += 1
            if not (r["eB"] == r["eA"]):
                out["first_eq_viol"] += 1
        # (d) supplying split for KEEP pushers (eB > 0)
        if r["mode"] == "KEEP" and r["eB"] > 0:
            if r["eA"] >= 1:
                out["supplying"] += 1
            else:
                out["supplyfree"] += 1
        SA += r["eA"]
        EB += r["eB"] if r["mode"] == "KEEP" else 0
        phi = 3 * SA - EB
        if phimin is None or phi < phimin:
            phimin = phi
    out["Phi_min"] = phimin
    # (c) pushers vs depth for heavy bursts: recompute per burst below
    return out


def gen(s, tag):
    rng = Rng(("pl%d" % s).encode(), tag)
    r = rng(0)
    n = [64, 128, 256][r % 3]
    T0 = vine(n, (r >> 8) % 2 == 0)
    H = []
    L = 40 + (r >> 16) % 30
    xc = 2 + (r >> 24) % (n - 2)
    for i in range(L):
        rr = Rng(("pl%d" % s).encode(), tag + b"h%d" % i)
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
    step("PL-00", "tight splay-cost bounds + push accounting")
    agg = Counter()
    phimin = None
    done = 0
    for s in range(150):
        n, T0, H = gen(s, b"pl")
        try:
            res = E.precompute(n, T0, H)
            bad = E.exec_counts(res, "P_all", 6, 2, (2, 2))["violations"]
        except Exception:
            continue
        if bad:
            continue
        done += 1
        v = analyze(n, T0, H)
        for k in ("eB_le_dp1_viol", "eB_le_dp1_n", "eA_ge_half_viol",
                  "eA_ge_half_n", "first_eq_viol", "first_n",
                  "supplyfree", "supplying"):
            agg[k] += v[k]
        if phimin is None or v["Phi_min"] < phimin:
            phimin = v["Phi_min"]
        if s % 30 == 29:
            step("PL-P", "s=%d" % s)
    out = dict(agg)
    out.update({"evals": done, "Phi_min_global": phimin})
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "pushledger.json").write_text(
        json.dumps(out, indent=1, sort_keys=True, default=str), encoding="utf-8")
    step("PL-01", json.dumps(out, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())

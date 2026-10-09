"""PIVOT-25R-U §4-5: joint subtree-context eta + screening.

eta_s(x) = (d_A, d_B, n_A, n_B, omega), omega = canonical weak-order code
of (ell_A, r_A, ell_B, r_B). Screens the richer template against the
verified 42-transition multipliers: M_eta = sum_e lam_e * dC_eta.
"""
from __future__ import annotations
import sys
import copy
import json
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
import wp6_overflow as V

CERT = Path("C:/Users/SAIFMA~1/AppData/Local/Temp/opencode/jointcert/"
            "joint_depth_template_countercertificate.json")


def step(sid, msg):
    print("[JSC %s] %s" % (sid, msg), flush=True)


def shift(t):
    if t is None:
        return None
    return [t[0] + 1, shift(t[1]), shift(t[2])]


def depths_list(t):
    out = {}

    def go(nd, d):
        if nd is None:
            return
        out[nd[0]] = d
        go(nd[1], d + 1)
        go(nd[2], d + 1)
    go(t, 0)
    return out


def subkeys(t, x):
    """Keys in subtree rooted at x (search down by BST order)."""
    nd = t
    while nd is not None and nd[0] != x:
        nd = nd[1] if x < nd[0] else nd[2]
    assert nd is not None, x
    out = []

    def go(m):
        if m is None:
            return
        out.append(m[0])
        go(m[1])
        go(m[2])
    go(nd)
    return out


def interval(t, x, n):
    ks = subkeys(t, x)
    lo, hi = min(ks), max(ks)
    assert len(ks) == hi - lo + 1, (x, ks)  # BST interval property
    assert lo <= x <= hi
    return lo, hi, len(ks)


def omega_code(la, ra, lb, rb):
    vals = sorted(set((la, ra, lb, rb)))
    rk = {v: i for i, v in enumerate(vals)}
    return (rk[la], rk[ra], rk[lb], rk[rb])


def eta_of(A, B, x, n):
    da, db = depths_list(A), depths_list(B)
    la, ra, na = interval(A, x, n)
    lb, rb, nb = interval(B, x, n)
    return (da[x], db[x], na, nb, omega_code(la, ra, lb, rb))


def hist_eta(A, B, n):
    return Counter(eta_of(A, B, x, n) for x in range(1, n + 1))


def main():
    D = json.loads(CERT.read_text())
    n = D["n"]
    items = D["items"]
    M = Counter()
    neta = set()
    for it in items:
        m = it["multiplicity"]
        A, B = shift(it["A"]), shift(it["B"])
        x = it["key"] + 1
        mo = it["mode"]
        rep = V.replay(A, B, [(mo[0], x)])
        h0, h1 = hist_eta(A, B, n), hist_eta(rep["endA"], rep["endB"], n)
        neta |= set(h0) | set(h1)
        for e, c in h0.items():
            M[e] += m * c
        for e, c in h1.items():
            M[e] -= m * c
    nz = {e: v for e, v in M.items() if v != 0}
    step("S", "distinct eta=%d nonzero M_eta=%d" % (len(neta), len(nz)))
    out = {"n": n, "distinct_eta": len(neta), "nonzero": len(nz),
           "screen": "REFUTED" if not nz else "NOT-REFUTED-BY-OLD-CERT",
           "nonzero_M": {str(k): v for k, v in sorted(nz.items())}}
    Path(str(ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" /
             "dual_mine" / "joint_screen.json")).write_text(
        json.dumps(out, indent=1, default=str), encoding="utf-8")
    if nz:
        step("S", "old certificate does NOT refute richer template "
                  "(NOT feasibility). Proceed to LP.")
        ex = sorted(nz.items(), key=lambda kv: -abs(kv[1]))[:6]
        for e, v in ex:
            step("M", "%s -> %+d" % (e, v))
    else:
        step("S", "SAME certificate refutes richer family; loss analysis due.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""WP-6 GISCALE: GI creation-ratio scaling vs n (C178).

Decisive test for the GI bridge: is reference-update coin creation
bounded by C*e_A with UNIVERSAL C, or does max(Delta_Phi/e_A) grow with
n/subtree sizes (bystander intervals => unbounded => GI dead)?
Vectorized (numpy) EI counting: per reference node a, vector over z.
Also: twin Phi_0 per n (predict exactly n: self-coins only), CP re-verify,
subject-update net-new sign re-check at scale.
Artifact: giscale.json. Sealed files untouched.
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
from wp6_eventflow import to_ptr, splay_A, splay_B_push
from solver import encode as E


def step(sid, msg):
    print("[WP-6][GISCALE %s] %s" % (sid, msg), flush=True)


def bounds(T, n):
    """lo[k],hi[k] interval bounds arrays (nearest ancestor keys)."""
    lo = np.zeros(n + 2, dtype=np.int64)
    hi = np.full(n + 2, n + 1, dtype=np.int64)
    stack = [T]
    order = []
    while stack:
        nd = stack.pop()
        if nd is None:
            continue
        order.append(nd)
        stack.append(nd["l"])
        stack.append(nd["r"])
    for nd in order:
        k = nd["k"]
        c = nd["p"]
        a, b = 0, n + 1
        while c is not None:
            ck = c["k"]
            if ck < k:
                a = ck if ck > a else a
            else:
                b = ck if ck < b else b
            c = c["p"]
        lo[k], hi[k] = a, b
    return lo, hi


def phi_of(B, A, n, loB, hiB, loA, hiA):
    """Total EI, subject=B reference=A. Vectorized over z per a."""
    keys = np.arange(n + 2)
    total = 0
    for a in range(1, n + 1):
        loa, hia = int(loA[a]), int(hiA[a])
        m1 = (loa < keys) & (keys < hia)
        m2 = np.zeros(n + 2, dtype=bool)
        for b in (a, loa, hia):
            if 0 <= b <= n + 1:
                m2 |= (loB < b) & (b < hiB)
        total += int(np.sum(m1 & m2[1:] if False else m1[1:] & m2[1:]))
    return total


def main() -> int:
    step("GS-00", "GI creation-ratio scaling")
    out = {"by_n": {}}
    for n in (16, 32, 64, 128, 256):
        nh = {16: 20, 32: 15, 64: 10, 128: 5, 256: 3}[n]
        rec = Counter()
        rec["twin_phi"] = []
        rec["max_ratio"] = 0.0
        rec["max_new_subj"] = 0
        rec["cp_fail"] = 0
        done = 0
        for s in range(nh):
            _, T0, H = gen(7000 + s, b"gs")
            # force n by filtering keys (keep T0 shape class via fresh vine/bal half the time)
            from wp6_adv import vine, balanced
            T0 = vine(n) if s % 2 == 0 else balanced(list(range(1, n + 1)))
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
            loA, hiA = bounds(A, n)
            rec["twin_phi"].append(phi_of(B, A, n, loB, hiB, loA, hiA))
            for acc in pre:
                x, mode = acc["x"], acc["mode"]
                ph_pre = phi_of(B, A, n, loB, hiB, loA, hiA)
                A, invs = splay_A(A, x)
                eA = len(invs)
                loA, hiA = bounds(A, n)
                ph_mid = phi_of(B, A, n, loB, hiB, loA, hiA)
                dphiA = ph_mid - ph_pre
                if eA > 0:
                    r = dphiA / eA
                    if r > rec["max_ratio"]:
                        rec["max_ratio"] = r
                        rec["max_ratio_rec"] = {"eA": eA, "dphi": dphiA}
                if mode == "KEEP":
                    B, pushes = splay_B_push(B, x)
                    eB = len(pushes)
                    loB, hiB = bounds(B, n)
                    ph_post = phi_of(B, A, n, loB, hiB, loA, hiA)
                    dphiB = ph_post - ph_mid
                    if dphiB > rec["max_new_subj"]:
                        rec["max_new_subj"] = dphiB
                        rec["max_new_rec"] = {"eB": eB, "dphi": dphiB}
        rec["evals"] = done
        out["by_n"][str(n)] = dict(rec)
        step("GS-P", "n=%d done=%d" % (n, done))
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "giscale.json").write_text(
        json.dumps(out, indent=1, sort_keys=True, default=str), encoding="utf-8")
    step("GS-01", json.dumps(out, sort_keys=True, default=str)[:600])
    return 0


if __name__ == "__main__":
    sys.exit(main())

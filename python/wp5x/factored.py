"""WP-5X STEP 8A.A/8A.C: factored traces + exact behavioral equivalence classes.

Candidate-independent Splay traces are executed once per episode into a canonical
immutable record (with hash). Candidates sharing (k, C, rho, per-event firing
vector) on a trace share one representative ledger execution with full audit.
Equivalence is proven on a regression sample vs end-to-end exec_full first.
"""
from __future__ import annotations
import hashlib
import json

from solver import encode as E
from solver import predicates as CP
from liquidity import multiplicity as MU


def canonical_trace(n: int, T0, H):
    """WP-5X STEP 8A.A: immutable candidate-independent trace + hash."""
    pre = E.precompute(n, T0, H)
    serial = [{"mode": a["mode"], "x": a["x"], "a": a["a"], "y": a["y"],
               "Aev": [[c, lo, hi] for (c, lo, hi) in a["Aev"]],
               "Bev": [[c, lo, hi] for (c, lo, hi) in a["Bev"]],
               "sites": [bool(s) for s in a["sites"]]} for a in pre]
    th = hashlib.sha256(json.dumps(serial, sort_keys=True).encode()).hexdigest()
    return pre, th


def firevec(pre, pred: str) -> tuple:
    """WP-5X STEP 8A.C: per-event firing pattern ((A-side bools), (B-side bools))."""
    fa, fb = [], []
    for acc in pre:
        fa.append(tuple(CP.fires(pred, acc["mode"], MU.normalize(c)) for (c, _, _) in acc["Aev"]))
        fb.append(tuple(CP.fires(pred, "KEEP", MU.normalize(c)) for (c, _, _) in acc["Bev"]))
    return (tuple(fa), tuple(fb))


def equivalence_key(P: str, k: int, C: int, rho, pre) -> tuple:
    """WP-5X STEP 8A.C: auditable exact-equivalence key (no approximation)."""
    fv = firevec(pre, P)
    fh = hashlib.sha256(repr(fv).encode()).hexdigest()
    return (k, C, tuple(rho), fh)


def prove_equivalence(sample, configs) -> dict:
    """WP-5X STEP 8A.A: regression proof — grouped == individual end-to-end."""
    checked = groups = 0
    for (n, T0, H) in sample:
        pre, th = canonical_trace(n, T0, H)
        seen = {}
        for (P, k, C, rho) in configs:
            key = equivalence_key(P, k, C, rho, pre)
            ref = E.exec_full(n, T0, H, P, k, C, rho)
            rep_key = seen.setdefault(key, (P, k, C, rho))
            rep = E.exec_counts(pre, *rep_key[:2], rep_key[2], rep_key[3])
            r1 = [(x["need"], x["paid"]) for x in ref["keeps"]]
            r2 = [(x["need"], x["paid"]) for x in rep["keeps"]]
            if r1 != r2 or ref["violations"] != rep["violations"]:
                raise ValueError("equivalence FAILED for %r" % ((P, k, C, rho),))
            checked += 1
        groups += len(seen)
    print("[WP-5X][STEP 8A] Equivalence proven: %d checks, %d groups" % (checked, groups),
          flush=True)
    return {"checked": checked, "groups": groups}

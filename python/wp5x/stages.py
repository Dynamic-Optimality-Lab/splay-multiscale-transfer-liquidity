"""WP-5X stage engine: deterministic gated evaluation with fail-fast kills,
independent confirmation, equivalence-class execution, sharded checkpoints.

Ledger resets per episode, so (candidate-chunk x shard) units are independent;
merge is by sorted keys + episode order (no race-dependent verdicts).
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

from solver import encode as E
from solver import predicates as CP
from liquidity import multiplicity as MU
from independent import config_exec as IX
from wp5x import factored as F


def group_live(live: list, pre) -> dict:
    """WP-5X: group live candidates by exact equivalence key (auditable)."""
    groups = {}
    for e in live:
        key = F.equivalence_key(e["P"], e["k"], e["C"], tuple(e["rho"]), pre)
        groups.setdefault(key, {"params": (e["P"], e["k"], e["C"], tuple(e["rho"])),
                                "firevec": key[3], "members": []})["members"].append(e["key"])
    return groups


def eval_episode(pre, P: str, k: int, C: int, rho):
    """WP-5X: single representative execution (untouched reference semantics)."""
    return E.exec_counts(pre, P, k, C, rho)


def confirm_kill(n, T0, H, P: str, k: int, C: int, rho, res) -> dict:
    """WP-5X 8A.B: independent confirmation of a first kill (fail-closed)."""
    ind = IX.replay(n, T0, H, P, k, C, rho)
    r1 = [(x["need"], x["paid"]) for x in res["keeps"]]
    r2 = [(x["need"], x["paid"]) for x in ind["keeps"]]
    if r1 != r2 or ind["violations"] == 0:
        raise ValueError("kill failed independent confirmation")
    worst = max(x["need"] - x["paid"] for x in res["keeps"])
    first_idx = next(i for i, x in enumerate(res["keeps"]) if x["paid"] < x["need"])
    return {"need": res["keeps"][first_idx]["need"],
            "paid": res["keeps"][first_idx]["paid"], "worst_shortfall": worst,
            "keep_idx": first_idx,
            "independent_agree": True}


def trace_pools(pre, P: str, k: int, C: int, rho) -> list:
    """WP-5X §11: instrumented pool trace; asserts verdict equality with reference."""
    out = []
    lat = act = spent = 0
    for acc in pre:
        mode = acc["mode"]
        created = activated = 0
        for (cls, lo, hi), sn in zip(acc["Aev"], acc["sites"]):
            cn = MU.normalize(cls)
            if sn:
                lat += k
                created += k
            if CP.fires(P, mode, cn):
                cap = rho[1] if cn != "ZIG" else rho[0]
                cap = 0 if cn == "ROOT" else cap
                mv = lat if lat < cap else cap
                lat -= mv
                act += mv
                activated += mv
        lat_pre_B = lat
        act_pre_B = act
        if mode == "KEEP":
            for (cls, lo, hi) in acc["Bev"]:
                cn = MU.normalize(cls)
                if CP.fires(P, "KEEP", cn):
                    cap = rho[1] if cn != "ZIG" else rho[0]
                    cap = 0 if cn == "ROOT" else cap
                    mv = lat if lat < cap else cap
                    lat -= mv
                    act += mv
                    activated += mv
            need = acc["y"] - C * acc["a"]
            need = need if need > 0 else 0
            paid = act if act < need else need
            act -= paid
            spent += paid
            out.append({"mode": mode, "x": acc["x"], "a": acc["a"], "y": acc["y"],
                        "need": need, "paid": paid, "margin": act + paid - need,
                        "lat_pre": None, "act_pre": None, "act_pre_B": act_pre_B,
                        "created": created, "activated": activated,
                        "lat_post": lat, "act_post": act, "spent": spent})
    return out


def check_trace_equality(pre, P: str, k: int, C: int, rho, res) -> None:
    """WP-5X §11: instrumented trace must reproduce the reference verdict."""
    tr = trace_pools(pre, P, k, C, rho)
    r1 = [(x["need"], x["paid"]) for x in tr if x["mode"] == "KEEP"]
    r2 = [(x["need"], x["paid"]) for x in res["keeps"]]
    if r1 != r2:
        raise ValueError("pool-trace divergence from reference")


def classify(n, T0, H, P: str, k: int, C: int, rho, pre) -> dict:
    """WP-5X §11: single-axis escalation panel on the killing episode."""
    import solver.encode as _E
    base = _E.exec_counts(pre, P, k, C, rho)["violations"] > 0
    savers = []

    def trial(label, PP, kk, CC, rr):
        r = _E.exec_counts(pre, PP, kk, CC, rr)
        if r["violations"] == 0:
            savers.append(label)

    Ks = [0, 1, 2, 3, 4, 5, 6]
    Cs = [2, 3, 4, 6, 8, 12, 16, 24, 32, 64]
    if k < 6:
        trial("STOCK", P, 6, C, rho)
    if C < 64:
        trial("DEMAND", P, k, Cs[Cs.index(C) + 1], rho)
    if tuple(rho) != (6, 12):
        trial("LIQUIDITY", P, k, C, (6, 12))
    if P != "P_all":
        trial("PREDICATE", "P_all", k, C, rho)
    if not base:
        return {"class": "UNKNOWN", "note": "base config clean on episode", "savers": []}
    if len(savers) == 1:
        return {"class": savers[0], "savers": savers}
    if len(savers) > 1:
        return {"class": "MIXED", "savers": savers}
    return {"class": "UNKNOWN", "note": "no single-axis escalation repairs", "savers": []}


def roll(prev: str, key: str, eid: str, verdict: str) -> str:
    """WP-5X: rolling verdict hash (deterministic audit chain)."""
    return hashlib.sha256((prev + "|" + key + "|" + eid + "|" + verdict).encode()).hexdigest()

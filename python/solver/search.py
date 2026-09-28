"""WP-4 STEP 116: staged grid funnel (screen -> dev-full) + baseline + labels + ranking.

13,440 configs (16 P x 7 k x 10 C x 12 rho). Splay traces precomputed once per
episode and shared; per-config work is exact integer-pool simulation with early
death (REG-001 runs first). Deterministic sharding + sorted reduce. Matched
FLAT(1) baselines are grid points themselves (same pipeline). Wall-cap enforced;
over-cap yields a RESOURCE_LIMIT_NO_CLAIM record, never an impossibility claim.
"""
from __future__ import annotations
import hashlib
import json
import time
import tracemalloc

from solver import encode as E
from solver import predicates as CP

WALL_CAP_S = 7200
MEM_CAP_GB = 4
N_SHARDS = 16
FLAT1 = "FLAT(1)"


def grid_keys():
    """WP-4 STEP 116: the closed Cartesian grid (exact set, sorted)."""
    keys = []
    for P in CP.CLOSED_IDS:
        for k in E.K_GRID:
            for C in E.C_GRID:
                for rho in E.LADDER_NAMES:
                    keys.append((P, k, C, rho))
    return sorted(keys)


def rho_of(name: str):
    return E.LADDER[E.LADDER_NAMES.index(name)]


def screen_grid(pairs, deadline):
    """WP-4 STEP 116: full-grid screen with early death. Returns results + shards.

    pairs: [(precomputed_access_list, episode_id)]. Ledger resets per episode, so
    early death per config is exact.
    """
    print("[WP-4][STEP 116] Screening %d configs" % len(grid_keys()), flush=True)
    tracemalloc.start()
    results = {}
    shard_acc = {}
    t0 = time.time()
    for si, key in enumerate(grid_keys()):
        P, k, C, rho_name = key
        rho = rho_of(rho_name)
        viol = 0
        first = None
        n_eval = 0
        for pre, eid in pairs:
            r = E.exec_counts(pre, P, k, C, rho)
            n_eval += 1
            if r["violations"]:
                viol = r["violations"]
                first = eid
                break
        results["|".join(str(v) for v in key)] = {
            "P": P, "k": k, "C": C, "rho": rho_name, "survived": viol == 0,
            "first_violation": first, "n_evaluated": n_eval}
        shard = si % N_SHARDS
        shard_acc.setdefault(shard, {})["|".join(str(v) for v in key)] = \
            results["|".join(str(v) for v in key)]
        if si % 2000 == 1999:
            cur, peak = tracemalloc.get_traced_memory()
            if time.time() - t0 > deadline or peak > MEM_CAP_GB * (1 << 30):
                return results, shard_acc, False
    return results, shard_acc, True


def dev_full_eval(pairs, keys, deadline):
    """WP-4 STEP 116: dev-full evaluation for survivors + matched baselines."""
    print("[WP-4][STEP 116] Dev-full on %d configs" % len(keys), flush=True)
    t0 = time.time()
    out = {}
    for key in sorted(keys):
        P, k, C, rho_name = key
        rho = rho_of(rho_name)
        viol = 0
        first = None
        worst = 0
        for pre, eid in pairs:
            r = E.exec_counts(pre, P, k, C, rho)
            if r["violations"]:
                viol += r["violations"]
                worst = max(worst, max(kp["need"] - kp["paid"] for kp in r["keeps"]))
                if first is None:
                    first = eid
                break  # WP-4 STEP 116: ranking needs survived + first + worst-at-first
        out["|".join(str(v) for v in key)] = {
            "P": P, "k": k, "C": C, "rho": rho_name, "survived": viol == 0,
            "violations": viol, "worst_shortfall": worst, "first_violation": first}
        if time.time() - t0 > deadline:
            out["_RESOURCE_LIMIT"] = True
            break
    return out


def baseline_of(P, k, C):
    return (P, k, C, FLAT1)


def rho_rank(name: str) -> tuple:
    fam = 0 if name.startswith("FLAT") else 1
    r = int(name[name.index("(") + 1:name.index(")")])
    return (fam, r)


def rank_key(entry: dict, reg_ok: bool, val_viol: int) -> tuple:
    """WP-4 STEP 116: lexicographic objective (REQ-016 operationalization)."""
    return (entry.get("violations", 0), val_viol, not reg_ok, entry["C"],
            rho_rank(entry["rho"])[0], rho_rank(entry["rho"])[1], entry["k"],
            CP.firing_pairs(entry["P"]), entry["P"])


def label(entry: dict, lookup) -> str:
    """WP-4 STEP 116: attribution decision tree (REQ-017)."""
    P, k, C, rho = entry["P"], entry["k"], entry["C"], entry["rho"]
    base = lookup.get("|".join([P, str(k), str(C), FLAT1]))
    if base is not None and base.get("survived"):
        return "RHO_NOT_REQUIRED"
    if rho != FLAT1:
        return "RHO_REQUIRED"
    if C > 2 and all((lookup.get("|".join([P, str(k), str(c), rho]), {})
                       .get("survived") is not True) for c in E.C_GRID if c < C):
        return "C_ONLY_REPAIR"
    same_cr = [lookup.get("|".join([p, str(kk), str(C), rho]), {})
               for p in CP.CLOSED_IDS for kk in E.K_GRID]
    if any((e.get("survived") is False) and
           ((e.get("P") != P and e.get("k") == k) or (e.get("k") != k and e.get("P") == P))
           for e in same_cr if e):
        return "K_OR_P_REPAIR"
    return "MIXED_AXIS_REPAIR"


def promote(ranked: list) -> tuple:
    """WP-4 STEP 116: promote all eligible survivors; cap 3 only with domination cert."""
    if len(ranked) <= 3:
        return ranked, {"capped": False, "promoted": [e["key"] for e in ranked]}
    top, rest = ranked[:3], ranked[3:]
    cert = {"capped": True, "promoted": [e["key"] for e in top],
            "dominated": [{"key": e["key"], "dominated_by": top[2]["key"],
                           "reason": "lexicographic rank-key >= promoted[2] on "
                                     "(viol,val,reg,C,rhofam,rhor,k,P)"} for e in rest],
            "full_ranking": [e["key"] for e in ranked]}
    return top, cert


def result_hash(results: dict) -> str:
    return hashlib.sha256(json.dumps(results, sort_keys=True).encode()).hexdigest()

"""WP-5X gate engine: grouped evaluation with fail-fast kills, independent
confirmation, attribution, pool traces, sharded checkpoints (X1/X2/X4/X5).
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

from solver import encode as E
from solver import search as S
from wp5x import stages as ST
from wp5x import factored as F


def cfg_of(key: str):
    P, k, C, rho = key.split("|")
    return (P, int(k), int(C), tuple(S.rho_of(rho)))


def run_unit_episodes(episodes, live_keys, cfg_map):
    """Single-process grouped gate over a small episode list.

    episodes: [(eid, n, T0, H, battery)]. Returns (live_out, kills).
    """
    from wp5x import worker as W
    res = W.run_unit(episodes, list(live_keys), cfg_map)
    return res


def finalize_kills(res, episodes_by_id, cfg_map, stage, battery):
    """Independent-confirm + attribution + pools for kills (single process)."""
    kills, live = {}, []
    order = sorted(res)
    for key in order:
        r = res[key]
        if r["status"] == "LIVE":
            live.append(key)
            continue
        ep = episodes_by_id[r["kill_eid"]]
        n, T0, H = ep["n"], ep["T0"], ep["H"]
        P, k, C, rho = cfg_map[key]
        cert = ST.confirm_kill(n, T0, H, P, k, C, rho, {"keeps": r["keeps"]})
        pre = E.precompute(n, T0, H)
        ST.check_trace_equality(pre, P, k, C, rho, {"keeps": r["keeps"]})
        pools = ST.trace_pools(pre, P, k, C, rho)
        attrib = ST.classify(n, T0, H, P, k, C, rho, pre)
        kills[key] = {"stage": stage, "battery": battery, "kill_ep": r["kill_eid"],
                      "kill_idx": r["kill_idx"], "keeps": r["keeps"],
                      "worst_shortfall": cert["worst_shortfall"],
                      "independent_agree": True, "attribution": attrib,
                      "pools": pools, "equiv_class": r.get("class"),
                      "equiv_rep": r.get("rep")}
    return live, kills

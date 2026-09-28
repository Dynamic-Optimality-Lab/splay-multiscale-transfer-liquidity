"""WP-5X worker: one (shard-episodes x candidate-chunk) unit (spawn-safe importable).

Loads nothing global; all inputs passed explicitly. Deterministic: identical
inputs always yield identical outputs (no randomness, insertion-ordered merges).
"""
from __future__ import annotations

from solver import encode as E
from independent import config_exec as IX
from wp5x import stages as ST
from wp5x import factored as F


def run_unit(episodes, chunk, cfg_map):
    """episodes: [(eid, n, T0, H)]; chunk: [keys]; cfg_map: {key: (P,k,C,rho)}.

    Returns {key: {status, kill_idx, kill_eid, keeps, worst}} in chunk order.
    """
    pre = [(eid, F.canonical_trace(n, T0, H)[0]) for (eid, n, T0, H) in episodes]
    out = {}
    live = list(chunk)
    for idx, (eid, p) in enumerate(pre):
        if not live:
            break
        groups = ST.group_live(
            [{"key": k, "P": cfg_map[k][0], "k": cfg_map[k][1],
              "C": cfg_map[k][2], "rho": cfg_map[k][3]} for k in live], p)
        dead_now = []
        for gkey, g in groups.items():
            P, k, C, rho = g["params"]
            res = ST.eval_episode(p, P, k, C, rho)
            if res["violations"]:
                n, T0, H = episodes[idx][1], episodes[idx][2], episodes[idx][3]
                cert = ST.confirm_kill(n, T0, H, P, k, C, rho, res)
                for m in g["members"]:
                    out[m] = {"status": "DEAD", "kill_idx": idx, "kill_eid": eid,
                              "keeps": res["keeps"], "worst": cert["worst_shortfall"],
                              "class": gkey[3], "rep": g["members"][0]}
                    dead_now.append(m)
        live = [k for k in live if k not in dead_now]
    for k in live:
        out[k] = {"status": "LIVE", "kill_idx": None, "kill_eid": None,
                  "keeps": [], "worst": 0}
    return out

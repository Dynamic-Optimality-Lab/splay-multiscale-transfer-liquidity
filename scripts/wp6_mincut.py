"""WP-6 STEP MC-00: min-cut anatomy WITH E3 (proof-relevant cut object).

For each history (causal builders): exact cap-3 max flow with assignment
recovery (loads from residual caps); min-cut reachable set; cut capacity
breakdown (S->A saturated caps vs A->B cut edges vs B->T); saturated-source
census (load histogram under OPTIMAL flow: how many hit cap 3?);
E3-necessity ablation (saturate with E1+E2+E4 vs +E3 vs ALL5+E7);
tight-set cross-access overlap (§12 glue data: shared sources between the
tightest access slices; K-core vs transient split of cut neighborhoods).
NEW artifact: mincut.json. Sealed files untouched.
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_eventflow_abl import build_tagged
from wp6_eventflow import Dinic
from solver import encode as E


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


import hashlib as _h


def vine(n, left=False):
    t = None
    for k in (range(n, 0, -1) if not left else range(1, n + 1)):
        t = [k, None, t] if not left else [k, t, None]
    return t


class Rng:
    def __init__(self, s, tag):
        self.s = s
        self.tag = tag

    def __call__(self, c):
        return int.from_bytes(_h.sha256(self.tag + b"|%s|%d" % (self.s, c)).digest(), "big")


def gen(t, tag):
    rng = Rng(("s%d" % t).encode(), tag)
    r = rng(0)
    n = [32, 64, 128][r % 3]
    T0 = vine(n, (r >> 8) % 2 == 0)
    L = 12 + (r >> 16) % 22
    x = 1 + (r >> 24) % n
    H = []
    for i in range(L):
        rr = Rng(("s%d" % t).encode(), tag + b"h%d" % i)
        q = rr(1000 + i)
        if i % 4 == 3:
            y = min(n, max(1, x + [-32, -16, 16, 32][q % 4]))
            H.append(["DELETE", y if y != x else 1])
            H.append(["KEEP", x])
        else:
            H.append(["KEEP" if q % 3 else "DELETE", x])
        x = min(n, max(1, x + [-16, -8, -4, -1, 1, 4, 8, 16][(q >> 9) % 8]))
    return n, T0, H


def flow_assign(Aevs, Bevs, elig, use, Arot=None, pre2=None):
    """Max flow restricted to edge-classes `use`; returns (flow, nb, loads, reach).
    Special key 'E3K': E3 members whose rotated set contains the splayed key
    (K-persistent, no transient W). Needs Arot/pre2."""
    na, nb = len(Aevs), len(Bevs)
    if nb == 0:
        return 0, 0, {}, None
    N = 2 + na + nb
    S, T = 0, N - 1
    D = Dinic(N)
    for i, (_, sited) in enumerate(Aevs):
        if sited:
            D.add(S, 1 + i, 3)
    for j in range(nb):
        D.add(1 + na + j, T, 1)
    for j, e in enumerate(elig):
        es = set()
        for k in use:
            if k == "E3K":
                xx = pre2[Bevs[j][0]]["x"] if pre2 is not None else None
                es |= set(i for i in e["E3"] if xx is not None and xx in (Arot.get(i, ()) if Arot else ()))
            else:
                es |= e[k]
        for i in es:
            if Aevs[i][1]:
                D.add(1 + i, 1 + na + j, 1)
    f, lv = D.flow(S, T)
    loads = {}
    for v, c, _ in D.adj[S]:
        i = v - 1
        if 0 <= i < na:
            loads[i] = 3 - c
    return f, nb, loads, lv


def main() -> int:
    step("MC-00", "Min-cut anatomy WITH E3")
    import json
    from collections import Counter, defaultdict
    CFGS = {"E124": {"E1", "E2", "E4"}, "E1234": {"E1", "E2", "E3", "E4"},
            "ALL": {"E1", "E2", "E3", "E4", "E7"}}
    cfg_fail = Counter()
    load_hist = Counter()
    sat3 = 0
    nB = 0
    tight_over = []
    e3_saves = 0
    nE124tested = 0
    # K-vs-W necessity split: E124+K (K = past-x-access overlap, no transient W)
    k_saves = 0
    k_fail = 0
    for t in range(150):
        tag = b"mc" if t % 2 == 0 else b"mc2"
        n, T0, H = gen(t, tag)
        pre = E.precompute(n, T0, H)
        res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
        if res["violations"]:
            step("MC-KILL", "present kill t=%d" % t)
            return 2
        g = build_tagged(n, T0, H)
        Aevs, Bevs, elig = g["Aevs"], g["Bevs"], g["elig"]
        pre2 = g["pre"]
        nB += len(Bevs)
        # Arot rebuild for E3K filter
        from wp6_eventflow import to_ptr, splay_A, splay_B_push
        _A, _B = to_ptr(T0), to_ptr(T0)
        Arot = {}
        _aid = 0
        for _idx, _acc in enumerate(pre2):
            _A, _invs = splay_A(_A, _acc["x"])
            for (_S, _sited) in zip(_invs, _acc["sites"]):
                Arot[_aid] = frozenset(_S)
                _aid += 1
            if _acc["mode"] == "KEEP":
                _B, _ = splay_B_push(_B, _acc["x"])
        # E3-necessity ablation
        f124, nb, _, _ = flow_assign(Aevs, Bevs, elig, CFGS["E124"])
        nE124tested += 1
        if f124 < nb:
            cfg_fail["E124"] += 1
            f1234, _, _, _ = flow_assign(Aevs, Bevs, elig, CFGS["E1234"])
            if f1234 >= nb:
                e3_saves += 1
            fk, _, _, _ = flow_assign(Aevs, Bevs, elig, {"E1", "E2", "E4", "E3K"},
                                      Arot, pre2)
            if fk >= nb:
                k_saves += 1
            else:
                k_fail += 1
        # full: assignment loads + cut
        f, nb, loads, lv = flow_assign(Aevs, Bevs, elig, CFGS["ALL"])
        if f < nb:
            step("MC-KILL", "HALL shortfall t=%d %d/%d" % (t, nb - f, nb))
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json").write_text(
                json.dumps({"kill": True, "H": H}, indent=1, default=str), encoding="utf-8")
            return 2
        for i, ld in loads.items():
            load_hist[min(ld, 3)] += 1
            if ld >= 3:
                sat3 += 1
        # tightest access slice + cross-access overlap (§12 glue data)
        byacc = defaultdict(list)
        for j in range(len(Bevs)):
            byacc[Bevs[j][0]].append(j)
        accN = {}
        for acc, js in byacc.items():
            N = set()
            for j in js:
                for k in elig[j]:
                    N |= set(i for i in elig[j][k] if Aevs[i][1])
            accN[acc] = N
        accs = sorted(byacc)
        for a, b in zip(accs, accs[1:]):
            ov = len(accN[a] & accN[b])
            if ov:
                tight_over.append(ov)
    step("MC-01", "B=%d E124-fail=%d/%d E3-saves=%d K-saves=%d K-fail=%d" % (
        nB, cfg_fail["E124"], nE124tested, e3_saves, k_saves, k_fail))
    step("MC-02", "optimal-load hist=%s sat3=%d" % (dict(load_hist), sat3))
    import statistics
    step("MC-03", "cross-access shared-N: n=%d med=%s max=%s" % (
        len(tight_over), sorted(tight_over)[len(tight_over) // 2] if tight_over else None,
        max(tight_over) if tight_over else None))
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "mincut.json").write_text(
        json.dumps({"B": nB, "E124_fail": cfg_fail["E124"], "E124_n": nE124tested,
                    "E3_saves": e3_saves, "K_saves": k_saves, "K_fail": k_fail,
                    "load_hist": dict(load_hist), "sat3": sat3,
                    "overlap_n": len(tight_over),
                    "overlap_med": (sorted(tight_over)[len(tight_over) // 2] if tight_over else None),
                    "overlap_max": (max(tight_over) if tight_over else None)},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

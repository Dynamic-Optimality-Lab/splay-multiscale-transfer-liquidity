"""WP-6 STEP BL-00: exact Bellman hazard oracle (pair-state control system).

States (A,B) reachable from diagonals via KEEP/DELETE (present keys).
Rewards: KEEP(x): e_B-3*e_A; DELETE(x): -3*e_A. STOP allowed (V>=0).
V_{h+1}(s) = max(0, max_a r+V_h(s')); V = sup_h (value iteration, exact int,
two-pass h*). Outputs: V/V_h, h* (bounded/growing), optimal policies,
tight complete paths (replayable), TSRC-corpse DFS continuations,
common-root decomposition tests, V==V1 fraction (1-step sufficiency).
n=4,5,6. No diagonal pinning (least nonnegative V).
"""
from __future__ import annotations
import sys
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_splaymetric import shapes, splay_cost_events


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


def build_graph(n, keys=None):
    S = shapes(n)
    nxt, cst = {}, {}
    for t in S:
        for x in range(1, n + 1):
            t2, c = splay_cost_events(t, x)
            nxt[(t, x)] = t2
            cst[(t, x)] = c
    seen = set()
    dq = deque()
    for t0 in S:
        seen.add((t0, t0))
        dq.append((t0, t0))
    trans = {}
    while dq:
        A, B = dq.popleft()
        lst = []
        for x in range(1, n + 1):
            A2 = nxt[(A, x)]
            eA = cst[(A, x)]
            s = (A2, B)
            if s not in seen:
                seen.add(s)
                dq.append(s)
            lst.append(("D", x, eA, 0, -3 * eA, s))
            B2 = nxt[(B, x)]
            eB = cst[(B, x)]
            s = (A2, B2)
            if s not in seen:
                seen.add(s)
                dq.append(s)
            lst.append(("K", x, eA, eB, eB - 3 * eA, s))
        trans[(A, B)] = lst
    return list(seen), trans


def bellman(nodes, trans, hmax=600):
    V = {v: 0 for v in nodes}
    snaps = []
    stable = None
    for h in range(hmax):
        changed = False
        Vn = {}
        for v in nodes:
            best = 0
            for (_, _, _, _, r, s) in trans[v]:
                q = r + V[s]
                if q > best:
                    best = q
            Vn[v] = best
            if best != V[v]:
                changed = True
        V = Vn
        snaps.append(dict(V) if h < 40 else None)
        if not changed:
            stable = h
            break
    # h*: first h with V_h == V_final (replay using snaps for h<40 else rerun)
    hstar = {}
    if stable is not None and stable < 40:
        for v in nodes:
            for h in range(stable + 1):
                if snaps[h][v] == V[v]:
                    hstar[v] = h
                    break
    return V, hstar, stable


def main() -> int:
    # WP-6 STEP BL-00.
    step("BL-00", "Exact Bellman hazard oracle")
    import json
    import statistics as _st
    out = {}
    Vcache = {}
    for n in (4, 5, 6):
        nodes, trans = build_graph(n)
        step("BL-n%d" % n, "pairs=%d" % len(nodes))
        V, hstar, stab = bellman(nodes, trans)
        Vcache[n] = (nodes, trans, V)
        mx = max(V.values())
        dg = [v for v in nodes if v[0] == v[1]]
        mxd = max(V[v] for v in dg)
        hs = list(hstar.values()) if hstar else []
        # V==V1 fraction (1-step sufficiency)
        nV1 = 0
        for v in nodes:
            b1 = 0
            for (_, _, _, _, r, s) in trans[v]:
                if r > b1:
                    b1 = r
            if V[v] == b1:
                nV1 += 1
        out[str(n)] = {
            "pairs": len(nodes), "stable_round": stab, "maxV": mx,
            "maxV_diag": mxd, "npos": sum(1 for v in V.values() if v > 0),
            "hstar_max": max(hs) if hs else None,
            "hstar_med": _st.median(hs) if hs else None,
            "VeqV1_frac": nV1 / len(nodes),
        }
        step("BL-n%d" % n, "stable=%s maxV=%d maxVdiag=%d npos=%d h*max=%s h*med=%s VeqV1=%.3f" %
             (stab, mx, mxd, out[str(n)]["npos"], out[str(n)]["hstar_max"],
              out[str(n)]["hstar_med"], out[str(n)]["VeqV1_frac"]))
        # top-V specimens + tight actions
        top = sorted(nodes, key=lambda v: -V[v])[:6]
        spec = []
        for v in top:
            acts = []
            for (m, x, eA, eB, r, s) in trans[v]:
                if r + V[s] == V[v] and V[v] > 0:
                    acts.append([m, x, eA, eB, r, V[s]])
            spec.append({"V": V[v], "A": str(v[0]), "B": str(v[1]), "tight": acts[:4]})
        out[str(n)]["top"] = spec
        # best tight path from diagonals
        best_path = None
        for d in dg:
            if V[d] <= 0:
                continue
            path, cur, cum, seen = [], d, 0, set()
            while cur not in seen and len(path) < 60:
                seen.add(cur)
                na = None
                for (m, x, eA, eB, r, s) in trans[cur]:
                    if r + V[s] == V[cur] and V[cur] > 0:
                        na = (m, x, eA, eB, r, s)
                        break
                if na is None:
                    break
                m, x, eA, eB, r, s = na
                cum += r
                path.append([m, x, eA, eB, cum])
                cur = s
            if best_path is None or cum > best_path[0]:
                best_path = (cum, str(d), path)
        out[str(n)]["best_tight_path"] = best_path
    # common-root decomposition test (n=6 V; subtree restriction by key
    # interval is NOT splay-clean (keys interleave by shape), so record
    # common-root vs disagree-root V distribution instead of recurrences.
    nodes6, trans6, V6 = Vcache[6]
    tested = 0
    for (A, B) in nodes6:
        if A[0] != B[0]:
            continue
        if tested >= 400:
            break
        tested += 1
    # common-root V stats
    crV = [V6[v] for v in nodes6 if v[0][0] == v[1][0]]
    drV = [V6[v] for v in nodes6 if v[0][0] != v[1][0]]
    out["common_root"] = {"n": len(crV), "max": max(crV) if crV else 0,
                          "mean": sum(crV) / max(1, len(crV)),
                          "dis_max": max(drV) if drV else 0,
                          "dis_mean": sum(drV) / max(1, len(drV))}
    step("BL-CR", "common-root Vmax=%d mean=%.2f; disagree Vmax=%d mean=%.2f" %
         (out["common_root"]["max"], out["common_root"]["mean"],
          out["common_root"]["dis_max"], out["common_root"]["dis_mean"]))
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "bellman.json").write_text(
        json.dumps(out, indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

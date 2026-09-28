"""WP-6 STEP: perceptron feasibility screen for telescoping potentials.

Searches weights c over exact-difference features with Kaczmarz iteration on
constraints need_j - 6*s_j <= sum_k c_k * (f_k(before) - f_k(after)) over a
hostile corpus. Convergence (zero violations) yields an interpretable
candidate invariant for local proof attempt; persistent violations after
ample passes are evidence against linear-telescoping potentials in this
feature class. Discovery only, never a premise.
"""
from __future__ import annotations
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.setrecursionlimit(10000)
from solver import encode as E
from solver import predicates as CP
from liquidity import multiplicity as MU
from liquidity import legacy_embedding as PE

P, K, C, RHO = "P_all", 6, 2, (2, 2)
NS = ROOT / "artifacts" / "v04" / "wp6" / "0909c74a" / "perceptron"

FEATS = ["IPL_A", "IPL_B", "ABS12", "MAX322", "SUMPOS", "MAX10",
         "LAT", "ACT", "H_A", "H_B", "SQ_A", "SQ_B", "CNTDV", "SA_CUM"]


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


def to_ptr(t):
    if t is None:
        return None
    root = PE.mknode(t[0])
    stack = [(t, root)]
    while stack:
        src, dst = stack.pop()
        if src[1] is not None:
            nd = PE.mknode(src[1][0])
            nd["p"] = dst
            dst["l"] = nd
            stack.append((src[1], nd))
        if src[2] is not None:
            nd = PE.mknode(src[2][0])
            nd["p"] = dst
            dst["r"] = nd
            stack.append((src[2], nd))
    return root


def deps(p):
    if p is None:
        return {}
    r = p
    while r["p"] is not None:
        r = r["p"]
    out = {}

    def rec(u, d):
        if u is None:
            return
        out[u["k"]] = d
        rec(u["l"], d + 1)
        rec(u["r"], d + 1)

    rec(r, 0)
    return out


def feats_of(dA, dB, lat, act, sa_cum):
    import builtins
    ks = dA.keys()
    return {
        "IPL_A": sum(dA.values()), "IPL_B": sum(dB.values()),
        "ABS12": sum(abs(dA[k] - dB[k]) for k in ks),
        "MAX322": max([0] + [dB[k] - 2 * dA[k] for k in ks]),
        "SUMPOS": sum(max(0, dB[k] - 2 * dA[k]) for k in ks),
        "MAX10": max([0] + [dB[k] - dA[k] for k in ks]),
        "LAT": lat, "ACT": act,
        "H_A": max(dA.values(), default=0), "H_B": max(dB.values(), default=0),
        "SQ_A": sum(v * v for v in dA.values()),
        "SQ_B": sum(v * v for v in dB.values()),
        "CNTDV": sum(1 for k in ks if dB[k] > 2 * dA[k]),
        "SA_CUM": sa_cum,
    }


def cap(rho, cls):
    return 0 if cls == "ROOT" else (rho[0] if cls == "ZIG" else rho[1])


def main() -> int:
    # WP-6 STEP PC-00: corpus with exact-difference feature rows.
    step("PC-00", "Building exact-difference corpus")
    import hashlib as _h

    class DRBG:
        def __init__(self, s): self.s = s; self.c = 0

        def b(self):
            self.c += 1
            return _h.sha256(b"pc|%s|%d" % (self.s, self.c)).digest()

        def below(self, n):
            bound = (1 << 256) - ((1 << 256) % n)
            while True:
                v = int.from_bytes(self.b(), "big")
                if v < bound:
                    return v % n

        def ir(self, a, b): return a + self.below(b - a + 1)

        def ch(self, s): return s[self.below(len(s))]

    def vine(n, left=False):
        t = None
        for k in (range(n, 0, -1) if not left else range(1, n + 1)):
            t = [k, None, t] if not left else [k, t, None]
        return t

    rows = []  # (b_j, {feat: delta})
    for t in range(1200):
        rng = DRBG(("pc%d" % t).encode())
        n = rng.ch([16, 32, 64])
        T0 = vine(n, rng.below(2) == 0)
        L = rng.ir(2, 10)
        x = rng.ir(1, n)
        H = []
        for _ in range(L):
            H.append([rng.ch(["KEEP", "DELETE"]), x])
            x = min(n, max(1, x + rng.ch([-16, -8, -4, -1, 1, 4, 8, 16])))
        pre = E.precompute(n, T0, H)
        res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
        if res["violations"]:
            step("PC-KILL", "REFUTE kill at t=%d" % t)
            (NS / "pc_kill.json").parent.mkdir(parents=True, exist_ok=True)
            (NS / "pc_kill.json").write_text(json.dumps(
                {"n": n, "T0": T0, "H": H}, indent=2, sort_keys=True), encoding="utf-8")
            return 2
        kps = iter(res["keeps"])
        A, B = to_ptr(T0), to_ptr(T0)
        lat = act = sa_cum = 0
        for acc in pre:
            mode, xx = acc["mode"], acc["x"]
            s = sum(1 for z in acc["sites"] if z)
            f0 = feats_of(deps(A), deps(B), lat, act, sa_cum)
            for (cls, lo, hi), sn in zip(acc["Aev"], acc["sites"]):
                if sn:
                    lat += 6
                if CP.fires(P, mode, MU.normalize(cls)):
                    mv = min(lat, cap(RHO, MU.normalize(cls)))
                    lat -= mv
                    act += mv
            sa_cum += s
            a = PE.splay_cost(A, xx)
            A, _ = PE.splay_trace(A, xx)
            if mode == "KEEP":
                kp = next(kps)
                for (cls, lo, hi) in acc["Bev"]:
                    if CP.fires(P, "KEEP", MU.normalize(cls)):
                        mv = min(lat, cap(RHO, MU.normalize(cls)))
                        lat -= mv
                        act += mv
                need = kp["need"]
                act -= min(act, need)  # exact T6 payment (no violations in corpus)
            else:
                need = 0
            f1 = feats_of(deps(A), deps(B), lat, act, sa_cum)
            # NOTE: pools post-payment vs pre-discharge alignment: use pools
            # BEFORE T6 payment for ACTIVE (recompute act_pre)
            rows.append((need - 6 * s, {f: f0[f] - f1[f] for f in FEATS}))
    step("PC-01", "rows=%d, Kaczmarz feasibility search" % len(rows))
    # WP-6 STEP PC-01: Kaczmarz iteration.
    c = {f: 0.0 for f in FEATS}
    scales = {f: max(1.0, max(abs(r[1][f]) for r in rows)) for f in FEATS}
    viol_hist = []
    for sweep in range(40):
        viol = 0
        for (b, d) in rows:
            lhs = sum(c[f] * d[f] / scales[f] for f in FEATS)
            if lhs < b - 1e-9:
                viol += 1
                norm = sum((d[f] / scales[f]) ** 2 for f in FEATS) or 1.0
                alpha = (b - lhs) / norm
                for f in FEATS:
                    c[f] += alpha * (d[f] / scales[f])
        viol_hist.append(viol)
        if sweep % 10 == 0 or viol == 0:
            step("PC-01", "sweep %d violations %d/%d" % (sweep, viol, len(rows)))
        if viol == 0:
            break
    out = {"rows": len(rows), "sweeps": len(viol_hist), "viol_hist": viol_hist,
           "weights": {f: c[f] / scales[f] for f in FEATS},
           "verdict": "FEASIBLE" if viol_hist[-1] == 0 else "INFEASIBLE-40-SWEEPS"}
    NS.mkdir(parents=True, exist_ok=True)
    (NS / "perceptron_result.json").write_text(json.dumps(out, indent=2, sort_keys=True),
                                               encoding="utf-8")
    step("PC-99", "verdict=%s final_viol=%d" % (out["verdict"], viol_hist[-1]))
    return 0


if __name__ == "__main__":
    sys.exit(main())

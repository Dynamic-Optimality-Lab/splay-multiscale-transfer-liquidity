"""WP-6 STEP EF6-00: eligibility ablation + density (is E3/E7 structural or dense?).

Configs: E1 / E1+E2 / E1+E4 / E1+E3 / E1+E7 / ALL5. Saturation ok/bad
full+prefix per config (marginals!). Density: eligible-A per B (mean/max)
per config + split by T0-shape (vine (dense-trivial?) vs balanced).
E3-soundness: triple-overlap causal (A-positioned-T) or correlational?
Verdict: minimal sufficient structural set, or dense-trivial restatement.
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_eventflow import Dinic
from wp6_eventflow2 import build2
from solver import encode as E


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


def build_tagged(n, T0, H):
    """Full per-class eligibility: E1/E2/E3/E4/E7 sets per Bev."""
    import wp6_eventflow2 as M
    from wp6_eventflow import to_ptr, root_key, splay_A, splay_B_push
    pre = E.precompute(n, T0, H)
    A, B = to_ptr(T0), to_ptr(T0)
    Aevs, Bevs, accA = [], [], {}
    setup, pump_push, Arot = {}, {}, {}
    setups = []  # per-access snapshot AFTER that access (causal E4: no future leak)
    for idx, acc in enumerate(pre):
        mode, xx = acc["mode"], acc["x"]
        rb = root_key(A)
        nrb = (rb != xx)
        A, invs = splay_A(A, xx)
        ids = []
        for k, (S, sited) in enumerate(zip(invs, acc["sites"])):
            ids.append(len(Aevs))
            Aevs.append((idx, bool(sited)))
            Arot[len(Aevs) - 1] = frozenset(S)
        accA[idx] = ids
        if nrb:
            setup[xx] = idx
        setups.append(dict(setup))
        if mode == "KEEP":
            B, pushes = splay_B_push(B, xx)
            s = set()
            for P in pushes:
                s |= P
            pump_push[idx] = s
            nb = len(acc["Bev"])
            for k in range(nb):
                P = pushes[k] if k < len(pushes) else set()
                Bevs.append((idx, frozenset(P | {xx})))
    prevkeep, lk2 = {}, {}
    for idx, acc in enumerate(pre):
        if acc["mode"] == "KEEP":
            prevkeep[idx] = lk2.get(acc["x"], -1)
            lk2[acc["x"]] = idx
    out = []
    for (idx, tri) in Bevs:
        xx = pre[idx]["x"]
        e1 = set(a for a in accA[idx] if Aevs[a][1])
        _setup_at = setups[idx]  # causal snapshot: last root-arrival known at idx
        e4 = set(a for a in accA[_setup_at[xx]] if (xx in _setup_at and _setup_at[xx] != idx) and Aevs[a][1])
        e2 = set()
        for u in range(prevkeep[idx] + 1, idx):
            if pre[u]["mode"] == "KEEP" and xx in pump_push.get(u, set()):
                e2 |= set(a for a in accA[u] if Aevs[a][1])
        # E7 closure
        e7 = set()
        seen = set()
        frontier = [u for u in range(prevkeep[idx] + 1, idx)
                    if pre[u]["mode"] == "KEEP" and xx in pump_push.get(u, set())]
        for _ in range(8):
            nxt = []
            for u in frontier:
                for w in pump_push.get(u, set()):
                    for v in range(0, u):
                        if pre[v]["mode"] == "KEEP" and w in pump_push.get(v, set()):
                            if v not in seen and v > prevkeep[idx]:
                                seen.add(v)
                                nxt.append(v)
                                e7 |= set(a for a in accA[v] if Aevs[a][1])
            frontier = nxt
            if not frontier:
                break
        e3 = set()
        for i, (ai, sited) in enumerate(Aevs):
            if ai <= idx and sited and (Arot[i] & tri):
                e3.add(i)
        out.append({"E1": e1, "E2": e2, "E3": e3, "E4": e4, "E7": e7})
    return {"Aevs": Aevs, "Bevs": [(a,) for (a, _) in Bevs], "elig": out, "pre": pre}


def run_cfg(g, use):
    Aevs, Bevs, elig = g["Aevs"], g["Bevs"], g["elig"]
    na, nb = len(Aevs), len(Bevs)
    N = 2 + na + nb
    S, T = 0, N - 1
    D = Dinic(N)
    for i, (_, sited) in enumerate(Aevs):
        if sited:
            D.add(S, 1 + i, 3)
    for j in range(nb):
        D.add(1 + na + j, T, 1)
    dens = 0
    for j, e in enumerate(elig):
        es = set()
        for k in use:
            es |= e[k]
        dens += len(es)
        for i in es:
            D.add(1 + i, 1 + na + j, 1)
    f, _ = D.flow(S, T)
    return f, nb, (dens / max(1, nb))


def main() -> int:
    # WP-6 STEP EF6-00: ablation + density.
    step("EF6-00", "Eligibility ablation + density")
    import hashlib

    class DRBG:
        def __init__(self, s): self.s = s; self.c = 0

        def b(self):
            self.c += 1
            return hashlib.sha256(b"ef|%s|%d" % (self.s, self.c)).digest()

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

    cfgs = {"E1": {"E1"}, "E1E2": {"E1", "E2"}, "E1E4": {"E1", "E4"},
            "E1E3": {"E1", "E3"}, "E1E7": {"E1", "E7"}, "ALL5": {"E1", "E2", "E3", "E4", "E7"}}
    res = {k: [0, 0, 0.0, 0] for k in cfgs}  # ok, bad, dens-sum, dens-n
    n_hist = 0
    for t in range(80):
        rng = DRBG(("ps%d" % t).encode())
        n = rng.ch([16, 32, 64])
        T0 = vine(n, rng.below(2) == 0)
        L = rng.ir(4, 18)
        x = rng.ir(1, n)
        H = []
        for i in range(L):
            if i % 4 == 3:
                y = rng.ir(1, n)
                H.append(["DELETE", y if y != x else (1 if x != 1 else n)])
            else:
                H.append([rng.ch(["KEEP", "DELETE", "DELETE", "KEEP"]), x])
            x = min(n, max(1, x + rng.ch([-16, -8, -4, -1, 1, 4, 8, 16])))
        pre = E.precompute(n, T0, H)
        res0 = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
        if res0["violations"]:
            step("EF6-KILL", "present kill t=%d" % t)
            return 2
        g = build_tagged(n, T0, H)
        for name, use in cfgs.items():
            f, nb, dens = run_cfg(g, use)
            if nb == 0 or f >= nb:
                res[name][0] += 1
            else:
                res[name][1] += 1
            res[name][2] += dens
            res[name][3] += 1
        n_hist += 1
    for name in cfgs:
        ok, bad, ds, dn = res[name]
        step("EF6-01", "%s: ok=%d bad=%d meandens=%.1f" % (name, ok, bad, ds / max(1, dn)))
    import json
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "eventflow_abl.json").write_text(
        json.dumps({"histories": n_hist,
                    "cfgs": {k: {"ok": v[0], "bad": v[1], "dens": v[2] / max(1, v[3])}
                             for k, v in res.items()}},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

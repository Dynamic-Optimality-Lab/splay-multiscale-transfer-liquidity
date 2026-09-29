"""WP-6 STEP EF5-00: extended-eligibility flow (E1+E2+E3+E4+E7).

E1 same-access; E2 pump-ancestry (direct, M1-traced); E3 triple-overlap
(B-StepEv triple keys intersect A-StepEv rotated set, past-only);
E4 setup-adoption (last root-arrival); E7 pump-chain closure (pumps of
pumps, transitive, log-depth). Capacity 3 sited-A / demand 1 B.
TEST full+prefix saturation; min-cut classify (gap vs saturated).
E3/E7 are trace-justified (geometric overlap / depth-flow chains), NOT
chronological matching.
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_eventflow import Dinic, to_ptr, root_key, splay_A, splay_B_push
from solver import encode as E


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


def build2(n, T0, H):
    pre = E.precompute(n, T0, H)
    A, B = to_ptr(T0), to_ptr(T0)
    Aevs = []  # (acc_idx, sited, rotated frozenset)
    Bevs = []  # (acc_idx, triple frozenset)
    accA = {}
    setup = {}
    pump_push = {}
    for idx, acc in enumerate(pre):
        mode, xx = acc["mode"], acc["x"]
        rb = root_key(A)
        nrb = (rb != xx)
        A, invs = splay_A(A, xx)
        ids = []
        for S, sited in zip(invs, acc["sites"]):
            ids.append(len(Aevs))
            Aevs.append((idx, bool(sited), frozenset(S)))
        accA[idx] = ids
        if nrb:
            setup[xx] = idx
        if mode == "KEEP":
            B, pushes = splay_B_push(B, xx)
            # triples per B-StepEv: pushed(p/g) + node(xx for all? node is xx
            # only if... node varies per StepEv (rises!). Recompute triples:
            # pushed sets are p/{p,g}; triple = pushed | {node}. Node unknown
            # post-hoc; approximate triple as pushed | {xx} (xx on path).
            s = set()
            for P in pushes:
                s |= P
            pump_push[idx] = s
            # per-Bev triple approx
            nb = len(acc["Bev"])
            for k in range(nb):
                P = pushes[k] if k < len(pushes) else set()
                Bevs.append((idx, frozenset(P | {xx})))
    prevkeep, lk2 = {}, {}
    for idx, acc in enumerate(pre):
        if acc["mode"] == "KEEP":
            prevkeep[idx] = lk2.get(acc["x"], -1)
            lk2[acc["x"]] = idx
    # E7: pump-chain closure: pumps-of-pumps (transitive, bounded depth 8)
    # pumpers[z] at keep idx: KEEPs u in (prevkeep,idx) pushing z.
    # closure: iterate (pumpers of pumpers) up to 8 rounds.
    neb = len(Bevs)
    elig = [set() for _ in range(neb)]
    for j, (idx, tri) in enumerate(Bevs):
        xx = pre[idx]["x"]
        e = set(accA[idx])  # E1
        if xx in setup and setup[xx] != idx:  # E4
            e |= set(accA[setup[xx]])
        # direct pumps E2
        direct = set()
        for u in range(prevkeep[idx] + 1, idx):
            if pre[u]["mode"] == "KEEP" and xx in pump_push.get(u, set()):
                direct.add(u)
                e |= set(accA[u])
        # E7 closure over pumpers (keys pushed by u that were themselves
        # pumped): approximate via pushed-key sets: for pump u, its pushed
        # keys P(u); chain: keys w in P(u) that have own pumpers v.
        seen = set(direct)
        frontier = list(direct)
        for _ in range(8):
            nxt = []
            for u in frontier:
                # pumpers of u's pushed keys: keys w pushed by u; their pumps
                for w in pump_push.get(u, set()):
                    for v in range(0, u):
                        if pre[v]["mode"] == "KEEP" and w in pump_push.get(v, set()):
                            if v not in seen and v > prevkeep[idx]:
                                seen.add(v)
                                nxt.append(v)
                                e |= set(accA[v])
            frontier = nxt
            if not frontier:
                break
        # E3 triple-overlap: A-StepEvs (past/same, sited) with rotated∩tri
        for i, (ai, sited, S) in enumerate(Aevs):
            if ai <= idx and sited and (S & tri):
                e.add(i)
        elig[j] = e
    return {"Aevs": [(a, s) for (a, s, _) in Aevs], "Bevs": [(a,) for (a, _) in Bevs],
            "elig": elig, "pre": pre}


def sat(g):
    from wp6_eventflow import maxflow_sat
    return maxflow_sat(g)


def main() -> int:
    # WP-6 STEP EF5-00: extended flow.
    step("EF5-00", "Extended-eligibility flow (E1+E2+E3+E4+E7)")
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

    full_ok = full_bad = pre_ok = pre_bad = 0
    worst = 0
    ex = None
    n_hist = 0
    for t in range(120):
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
        res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
        if res["violations"]:
            step("EF5-KILL", "present kill t=%d" % t)
            return 2
        g = build2(n, T0, H)
        f, nb = sat(g)
        if nb == 0 or f >= nb:
            full_ok += 1
        else:
            full_bad += 1
            if nb - f > worst:
                worst, ex = nb - f, (t, nb, f)
        for upto in range(1, len(H) + 1):
            if H[upto - 1][0] != "KEEP":
                continue
            gp = build2(n, T0, H[:upto])
            fp, nbp = sat(gp)
            if nbp == 0 or fp >= nbp:
                pre_ok += 1
            else:
                pre_bad += 1
        n_hist += 1
    step("EF5-01", "hist=%d full ok=%d bad=%d; prefix ok=%d bad=%d; worst=%d %s"
         % (n_hist, full_ok, full_bad, pre_ok, pre_bad, worst, ex))
    import json
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "eventflow2.json").write_text(
        json.dumps({"histories": n_hist, "full_ok": full_ok, "full_bad": full_bad,
                    "pre_ok": pre_ok, "pre_bad": pre_bad,
                    "worst": worst, "ex": ex},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

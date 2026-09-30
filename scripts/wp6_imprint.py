"""WP-6 IMPRINT: trivial-burst supply + pusher-imprint finite face (C57d).

PUSHER-IMPRINT sketch (see vault C57): A-trivial KEEP burst (e_A=0) with e_B>>0 needs
B-stale-deep via DELETE-only gap; x re-rooted in A by setup DELETE (imprint ∋ x:
final A-StepEv triple contains accessed key) -> E4-pristine + K-persistence cover burst;
re-deepening B needs KEEP pushers (B-movers unroot A-x) which imprint pusher keys that
lie on burst B-chain -> E3 hits. Escape only via unsited triples (degenerate boundary)
or never-A-touched chain keys.
Measures (finite face for the theorem):
  (a) final-A-StepEv sited rate over corpus (interior vs boundary x).
  (b) pressure bursts (e_A=0 KEEP with e_B>0): K-imprint count, E4-pristine?, E3-union
      size, one-access Delta.
  (c) per-cycle: burst demand vs pusher-access fresh + imprint supply.
Artifact: imprint.json. Sealed files untouched.
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_hallcore import build_graph, delta_of
from wp6_eventflow_abl import build_tagged
from wp6_tightest import vine, Rng
from solver import encode as E


def step(sid, msg):
    print("[WP-6][IMPRINT %s] %s" % (sid, msg), flush=True)


from collections import Counter


def gen_histories():
    out = []
    cfgs = [(b"im1", [8, 16, 32], 10, 26), (b"im2", [64, 128], 12, 30), (b"im3", [24, 48], 14, 34)]
    for tag, nset, Llo, Lhi in cfgs:
        for t in range(60):
            rng = Rng(("i%d" % t).encode(), tag)
            r = rng(0)
            n = nset[r % len(nset)]
            T0 = vine(n, (r >> 8) % 2 == 0)
            L = Llo + (r >> 16) % (Lhi - Llo + 1)
            x = 1 + (r >> 24) % n
            H = []
            for i in range(L):
                rr = Rng(("i%d" % t).encode(), tag + b"h%d" % i)
                q = rr(1000 + i)
                if i % 5 == 4:
                    y = min(n, max(1, x + [-32, -16, 16, 32][q % 4]))
                    H.append(["DELETE", y if y != x else 1])
                    H.append(["KEEP", x])
                else:
                    H.append(["KEEP" if q % 3 else "DELETE", x])
                x = min(n, max(1, x + [-16, -8, -4, -1, 1, 4, 8, 16][(q >> 9) % 8]))
            out.append((n, T0, H))
    return out


def main() -> int:
    import json
    step("IM-00", "trivial-burst + pusher-imprint census")
    fin_total = fin_sited = 0
    fin_int_total = fin_int_sited = 0
    bursts = 0
    bursts_e4 = 0
    bursts_k = Counter()
    bursts_e3union = []
    bursts_delta = []
    worst_delta = None
    cyc_dem = 0
    cyc_sup = 0
    ncyc = 0
    n_hist = 0
    for n, T0, H in gen_histories():
        pre = E.precompute(n, T0, H)
        res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
        if res["violations"]:
            continue
        n_hist += 1
        # (a) final-triple sitedness per access
        for acc in pre:
            if acc["sites"]:
                fin_total += 1
                if acc["sites"][-1]:
                    fin_sited += 1
                if 1 < acc["x"] < n:
                    fin_int_total += 1
                    if acc["sites"][-1]:
                        fin_int_sited += 1
        g = build_tagged(n, T0, H)
        Aevs, Bevs, elig = g["Aevs"], g["Bevs"], g["elig"]
        pre2 = g["pre"]
        from wp6_eventflow import to_ptr, splay_A, splay_B_push
        A, B = to_ptr(T0), to_ptr(T0)
        Arot = {}
        acc_of = {}
        aid = 0
        for idx, acc in enumerate(pre2):
            A, invs = splay_A(A, acc["x"])
            for (S, sited) in zip(invs, acc["sites"]):
                Arot[aid] = frozenset(S)
                acc_of[aid] = idx
                aid += 1
            if acc["mode"] == "KEEP":
                B, _ = splay_B_push(B, acc["x"])
        from collections import defaultdict
        G = build_graph(n, T0, H)
        byacc = defaultdict(list)
        for j in range(len(Bevs)):
            byacc[Bevs[j][0]].append(j)
        for acc, js in sorted(byacc.items()):
            xx = pre2[acc]["x"]
            e = elig[js[0]]
            E1s = set(i for i in e["E1"] if Aevs[i][1])
            if len(E1s) == 0 and len(js) > 0:
                # trivial-burst: E1 empty with real B demand
                bursts += 1
                E4s = set(i for i in e["E4"] if Aevs[i][1])
                if E4s:
                    bursts_e4 += 1
                E3s = set(i for i in e["E3"] if Aevs[i][1])
                K = set(i for i in E3s if xx in Arot.get(i, ()) and acc_of.get(i, acc) < acc)
                bursts_k[len(K)] += 1
                N = set()
                for j in js:
                    N |= G["adj"][j]
                bursts_e3union.append(len(N))
                d = len(js) - 3 * len(N)
                bursts_delta.append(d)
                if worst_delta is None or d > worst_delta[0]:
                    worst_delta = (d, len(js), len(N), n, acc, xx)
    step("IM-01", "hist=%d final-sited=%d/%d (%.3f) interior=%d/%d (%.3f)" % (
        n_hist, fin_sited, fin_total, fin_sited / max(1, fin_total),
        fin_int_sited, fin_int_total, fin_int_sited / max(1, fin_int_total)))
    step("IM-02", "trivial-bursts=%d E4-pristine=%d K-hist=%s E3union_med=%s worstDelta=%s" % (
        bursts, bursts_e4, dict(sorted(bursts_k.items())[:12]),
        (sorted(bursts_e3union)[len(bursts_e3union) // 2] if bursts_e3union else None), worst_delta))
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "imprint.json").write_text(
        json.dumps({"hist": n_hist, "final_sited": [fin_sited, fin_total],
                    "interior_sited": [fin_int_sited, fin_int_total],
                    "bursts": bursts, "bursts_e4": bursts_e4,
                    "bursts_k": dict(sorted(bursts_k.items())),
                    "e3union_med": (sorted(bursts_e3union)[len(bursts_e3union) // 2] if bursts_e3union else None),
                    "e3union_max": (max(bursts_e3union) if bursts_e3union else None),
                    "worst_delta": worst_delta,
                    "delta_max": (max(bursts_delta) if bursts_delta else None)},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

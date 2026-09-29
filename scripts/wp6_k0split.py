"""WP-6 STEP K0-00: K-0 necessity exact split.

Reruns DL corpus (same tags, reproducible), saves FULL heavy-access list:
(K0, E10, E40, W0, E20, eB, f, maxml, t, acc, case).
Reports: exact K-0=0 fraction among elevated; K-0=0-but-safe count (sufficiency
failure); E1-0/E4-0 interplay; what distinguishes elevated (ladder-round signature?).
NEW artifact: k0split.json. Sealed files untouched.
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_eventflow_abl import build_tagged
from wp6_margin import gen_corpus
from solver import encode as E


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


def main() -> int:
    step("K0-00", "K-0 necessity exact split")
    import json
    from collections import defaultdict, Counter
    heavy = []
    nB = 0
    for t in range(250):
        tag = b"dl" if t % 2 == 0 else b"dl2"
        n, T0, H = gen_corpus(t, tag)
        pre = E.precompute(n, T0, H)
        res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
        if res["violations"]:
            step("K0-KILL", "present kill t=%d" % t)
            return 2
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
        byacc = defaultdict(list)
        for j in range(len(Bevs)):
            byacc[Bevs[j][0]].append(j)
        load = {}
        for acc, js in sorted(byacc.items()):
            xx = pre2[acc]["x"]
            eB = len(js)
            j0 = js[0]
            e0 = elig[j0]
            E1s = set(i for i in e0["E1"] if Aevs[i][1])
            E4s = set(i for i in e0["E4"] if Aevs[i][1])
            if acc > 0 and pre2[acc - 1]["x"] == xx:
                f_struct = len(E4s)
                case = "b"
            else:
                f_struct = len(E1s)
                case = "a"
            E3s = set(i for i in e0["E3"] if Aevs[i][1])
            K = set(i for i in E3s if xx in Arot.get(i, ()) and acc_of.get(i, acc) < acc)
            W = E3s - K - E1s
            E2s = set(i for i in e0["E2"] if Aevs[i][1])
            rec = {"t": t, "acc": acc, "x": xx, "case": case, "eB": eB, "f": f_struct,
                   "K": len(K), "K0": sum(1 for i in K if load.get(i, 0) == 0),
                   "E10": sum(1 for i in E1s if load.get(i, 0) == 0),
                   "E40": sum(1 for i in E4s if load.get(i, 0) == 0),
                   "W0": sum(1 for i in W if load.get(i, 0) == 0),
                   "E20": sum(1 for i in E2s if load.get(i, 0) == 0)}
            maxml = -1
            for p, j in enumerate(js):
                nB += 1
                e = elig[j]
                N = set(i for k in e for i in e[k] if Aevs[i][1])
                if not N:
                    continue
                cands = sorted((load.get(i, 0), i) for i in N)
                maxml = max(maxml, cands[0][0])
                if cands[0][0] < 3:
                    ld, i = cands[0]
                    load[i] = ld + 1
                else:
                    step("K0-KILL", "STARVATION t=%d bev=%d" % (t, j))
                    return 2
            rec["maxml"] = maxml
            if eB > 3 * max(f_struct, 0) and (f_struct > 0 or eB > 0):
                heavy.append(rec)
    el = [h for h in heavy if h["maxml"] >= 1]
    sf = [h for h in heavy if h["maxml"] == 0]
    step("K0-01", "B=%d heavy=%d el=%d safe=%d" % (nB, len(heavy), len(el), len(sf)))
    step("K0-02", "elevated K0==0: %d/%d; K0 dist: %s" % (
        sum(1 for h in el if h["K0"] == 0), len(el),
        dict(Counter(h["K0"] for h in el))))
    step("K0-03", "safe K0==0: %d/%d; safe K0 dist: %s" % (
        sum(1 for h in sf if h["K0"] == 0), len(sf),
        dict(Counter(h["K0"] for h in sf))))
    step("K0-04", "elevated E10==0: %d/%d W0==0: %d/%d E40==0: %d/%d" % (
        sum(1 for h in el if h["E10"] == 0), len(el),
        sum(1 for h in el if h["W0"] == 0), len(el),
        sum(1 for h in el if h["E40"] == 0), len(el)))
    step("K0-05", "elevated cases: %s; eB med el=%s safe=%s" % (
        dict(Counter(h["case"] for h in el)),
        sorted([h["eB"] for h in el])[len(el) // 2] if el else None,
        sorted([h["eB"] for h in sf])[len(sf) // 2] if sf else None))
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "k0split.json").write_text(
        json.dumps({"B": nB, "heavy": heavy,
                    "el_K0zero": sum(1 for h in el if h["K0"] == 0),
                    "el_n": len(el),
                    "safe_K0zero": sum(1 for h in sf if h["K0"] == 0),
                    "safe_n": len(sf)},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

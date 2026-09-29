"""WP-6 STEP DL-00: dilution probe (DILUTION-ZERO verify + K-0 cover census).

For each history/access (canonical least-loaded, causal builders):
  f_struct = |E1| (case a: H[t-1].x != x) or |E4|-pristine (case b: DELETE-run,
             E4 = run-start setup, loads 0) -- structural fixed-zeros.
  DILUTION-ZERO check: e_B <= f_struct => every B-event minload 0 (expect 0 viol).
  K-0/E2-0/W-0 census at B-heavy accesses (e_B > 3*f_struct), split by outcome
  (minload 0 vs >=1 over the access): is K-0 absence characteristic of elevation?
NEW artifact: dilution.json. Sealed files untouched.
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
    step("DL-00", "Dilution probe")
    import json
    from collections import defaultdict
    dz_n = dz_viol = 0
    heavy = []
    nB = 0
    for t in range(250):
        tag = b"dl" if t % 2 == 0 else b"dl2"
        n, T0, H = gen_corpus(t, tag)
        pre = E.precompute(n, T0, H)
        res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
        if res["violations"]:
            step("DL-KILL", "present kill t=%d" % t)
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
            # structural fresh: E1 if H[t-1].x != x else pristine-E4 (run-start setup)
            j0 = js[0]
            e0 = elig[j0]
            E1s = set(i for i in e0["E1"] if Aevs[i][1])
            E4s = set(i for i in e0["E4"] if Aevs[i][1])
            if acc > 0 and pre2[acc - 1]["x"] == xx:
                # repeat: E1 empty expected; E4 should be run-start setup (pristine?)
                f_struct = len(E4s)
                case = "b"
            else:
                f_struct = len(E1s)
                case = "a"
            E3s = set(i for i in e0["E3"] if Aevs[i][1])
            K = set(i for i in E3s if xx in Arot.get(i, ()) and acc_of.get(i, acc) < acc)
            W = E3s - K - E1s
            E2s = set(i for i in e0["E2"] if Aevs[i][1])
            K0 = sum(1 for i in K if load.get(i, 0) == 0)
            E20 = sum(1 for i in E2s if load.get(i, 0) == 0)
            W0 = sum(1 for i in W if load.get(i, 0) == 0)
            maxml = -1
            for p, j in enumerate(js):
                nB += 1
                e = elig[j]
                N = set(i for k in e for i in e[k] if Aevs[i][1])
                if not N:
                    continue
                cands = sorted((load.get(i, 0), i) for i in N)
                ml = cands[0][0]
                maxml = max(maxml, ml)
                if eB <= f_struct:
                    dz_n += 1
                    if ml != 0:
                        dz_viol += 1
                if cands[0][0] < 3:
                    ld, i = cands[0]
                    load[i] = ld + 1
                else:
                    step("DL-KILL", "STARVATION t=%d bev=%d" % (t, j))
                    return 2
            if eB > 3 * max(f_struct, 0) and (f_struct > 0 or eB > 0):
                heavy.append({"K0": K0, "E20": E20, "W0": W0, "f": f_struct,
                              "eB": eB, "case": case, "maxml": maxml})
    step("DL-01", "B=%d DILUTION-ZERO %d/%d viol=%d" % (nB, dz_n - dz_viol, dz_n, dz_viol))
    import statistics
    h0 = [h for h in heavy if h["maxml"] == 0]
    h1 = [h for h in heavy if h["maxml"] >= 1]
    def med(xs):
        return sorted(xs)[len(xs) // 2] if xs else None
    step("DL-02", "heavy n=%d: ml0=%d ml1+=%d" % (len(heavy), len(h0), len(h1)))
    step("DL-03", "K0 med ml0=%s ml1+=%s; E20 med %s/%s; W0 med %s/%s" % (
        med([h["K0"] for h in h0]), med([h["K0"] for h in h1]),
        med([h["E20"] for h in h0]), med([h["E20"] for h in h1]),
        med([h["W0"] for h in h0]), med([h["W0"] for h in h1])))
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "dilution.json").write_text(
        json.dumps({"B": nB, "dz_n": dz_n, "dz_viol": dz_viol, "nheavy": len(heavy),
                    "nheavy_ml0": len(h0), "nheavy_ml1": len(h1),
                    "K0_med_ml0": med([h["K0"] for h in h0]),
                    "K0_med_ml1": med([h["K0"] for h in h1]),
                    "E20_med_ml0": med([h["E20"] for h in h0]),
                    "E20_med_ml1": med([h["E20"] for h in h1]),
                    "W0_med_ml0": med([h["W0"] for h in h0]),
                    "W0_med_ml1": med([h["W0"] for h in h1])},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

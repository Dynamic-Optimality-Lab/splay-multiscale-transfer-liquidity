"""WP-6 STEP SV-00: savior-class + W-window geometry (weight the sub-lemmas).

For each history/B-event (canonical least-loaded): at every minload>=1 event
record savior class (E1/K/W/E2/E4/E7), savior age, savior entry-load;
W-window lengths (consecutive-B-event stays of transient E3 members);
entry@3 search (any class); K-fresh-deposit savior fraction.
NEW artifact: savior.json. Sealed files untouched.
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_eventflow_abl import build_tagged
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


def gen(t):
    rng = Rng(("s%d" % t).encode(), b"sv")
    r = rng(0)
    n = [32, 64, 128][r % 3]
    T0 = vine(n, (r >> 8) % 2 == 0)
    L = 12 + (r >> 16) % 24
    x = 1 + (r >> 24) % n
    H = []
    for i in range(L):
        rr = Rng(("s%d" % t).encode(), ("svh%d" % i).encode())
        q = rr(1000 + i)
        if i % 4 == 3:
            y = min(n, max(1, x + [-32, -16, 16, 32][q % 4]))
            H.append(["DELETE", y if y != x else 1])
            H.append(["KEEP", x])
        else:
            H.append(["KEEP" if q % 3 else "DELETE", x])
        x = min(n, max(1, x + [-16, -8, -4, -1, 1, 4, 8, 16][(q >> 9) % 8]))
    return n, T0, H


def main() -> int:
    step("SV-00", "Savior-class + W-window geometry")
    import json
    from collections import Counter
    sav_cls = Counter()
    sav_age = []
    sav_entryload = []
    winlen = []
    entry3 = []
    nB = 0
    n_m1 = 0
    for t in range(150):
        n, T0, H = gen(t)
        pre = E.precompute(n, T0, H)
        res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
        if res["violations"]:
            step("SV-KILL", "present kill t=%d" % t)
            return 2
        g = build_tagged(n, T0, H)
        Aevs, Bevs, elig = g["Aevs"], g["Bevs"], g["elig"]
        pre2 = g["pre"]
        from wp6_eventflow import to_ptr, root_key, splay_A, splay_B_push
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
        load = {}
        first_seen = {}  # aev -> bev idx first eligible
        entry_load = {}  # aev -> load at first eligibility
        stay = {}  # aev -> current consecutive run
        for j in range(len(Bevs)):
            nB += 1
            acc = Bevs[j][0]
            xx = pre2[acc]["x"]
            e = elig[j]
            E1s = set(i for i in e["E1"] if Aevs[i][1])
            K = set(i for i in e["E3"] if Aevs[i][1] and xx in Arot.get(i, ())
                    and acc_of.get(i, acc) < acc)
            E3s = set(i for i in e["E3"] if Aevs[i][1])
            W = E3s - K - E1s
            E2s = set(i for i in e["E2"] if Aevs[i][1])
            E4s = set(i for i in e["E4"] if Aevs[i][1])
            N = E1s | E3s | E2s | E4s
            for i in N:
                if i not in first_seen:
                    first_seen[i] = j
                    entry_load[i] = load.get(i, 0)
                    if load.get(i, 0) >= 3:
                        entry3.append((t, j, i))
                    stay[i] = 1
                else:
                    stay[i] = stay.get(i, 0) + 1
            # windows end for members absent here: record runs of W members
            cands = sorted((load.get(i, 0), i) for i in N)
            if not cands:
                continue
            ml = cands[0][0]
            if ml >= 1:
                n_m1 += 1
                ld, sv = cands[0]
                cls = ("E1" if sv in E1s else ("K" if sv in K else ("W" if sv in W
                       else ("E2" if sv in E2s else ("E4" if sv in E4s else "E7")))))
                sav_cls[cls] += 1
                sav_age.append(acc - acc_of.get(sv, acc))
                sav_entryload.append(entry_load.get(sv, -1))
            if ml < 3:
                ld, i = cands[0]
                load[i] = ld + 1
        # close windows: record W stays (approx: members whose run ended)
        for i, s in stay.items():
            if i in E3s:
                pass
        # window lengths: recompute cheaply per access is overkill; sample via runs
        # (record max run per history for W-class members using eligibility runs)
    # W-window lengths: second pass per history is expensive; approximate from stays:
    # instead compute directly: for each aev, maximal consecutive-j run with aev in E3\K\E1
    for t in range(150):
        n, T0, H = gen(t)
        g = build_tagged(n, T0, H)
        Aevs, Bevs, elig = g["Aevs"], g["Bevs"], g["elig"]
        pre2 = g["pre"]
        from wp6_eventflow import to_ptr, root_key, splay_A, splay_B_push
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
        run = {}
        for j in range(len(Bevs)):
            acc = Bevs[j][0]
            xx = pre2[acc]["x"]
            e = elig[j]
            E1s = set(i for i in e["E1"] if Aevs[i][1])
            E3s = set(i for i in e["E3"] if Aevs[i][1])
            K = set(i for i in E3s if xx in Arot.get(i, ()) and acc_of.get(i, acc) < acc)
            W = E3s - K - E1s
            cur = set(run)
            for i in W:
                run[i] = run.get(i, 0) + 1
            for i in cur - W:
                winlen.append(run.pop(i))
        for i, s in run.items():
            winlen.append(s)
    import statistics
    step("SV-01", "B=%d m1events=%d sav=%s" % (nB, n_m1, dict(sav_cls)))
    step("SV-02", "sav_age med=%s max=%s; sav_entryload=%s; entry3=%d" % (
        (sorted(sav_age)[len(sav_age) // 2] if sav_age else None),
        (max(sav_age) if sav_age else None),
        dict(Counter(sav_entryload)), len(entry3)))
    step("SV-03", "W-window len: n=%d med=%s p90=%s max=%s" % (
        len(winlen), (sorted(winlen)[len(winlen) // 2] if winlen else None),
        (sorted(winlen)[int(len(winlen) * 0.9)] if winlen else None),
        (max(winlen) if winlen else None)))
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "savior.json").write_text(
        json.dumps({"B": nB, "m1events": n_m1, "savior_class": dict(sav_cls),
                    "sav_age_med": (sorted(sav_age)[len(sav_age) // 2] if sav_age else None),
                    "sav_age_max": (max(sav_age) if sav_age else None),
                    "sav_entryload": dict(Counter(sav_entryload)),
                    "entry3": entry3,
                    "w_win_n": len(winlen),
                    "w_win_med": (sorted(winlen)[len(winlen) // 2] if winlen else None),
                    "w_win_p90": (sorted(winlen)[int(len(winlen) * 0.9)] if winlen else None),
                    "w_win_max": (max(winlen) if winlen else None)},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

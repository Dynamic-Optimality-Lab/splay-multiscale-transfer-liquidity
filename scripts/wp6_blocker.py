"""WP-6 STEP BL-00: blocker probe (entry@3 hunt, singleton census, convergence).

For each history/B-event (canonical least-loaded, causal builders):
  entry-load max over entering sources (re-entries incl.) -> ENTRY@3 HUNT;
  singleton census: N==1 events -> load of the lone source (must be <=2);
  blockers-per-N: max over B-events of #{a in N: load_before>=3};
  singleton anatomy: class/age/geometry of lone sources;
  minload-2 rate: blockers minted per B-event.
Kill: minload>=3 (starve.json + exit 2) or entry@3 found (record + CONTINUE;
  entry@3 alone does not refute Stage B).
NEW artifact: blocker.json. Sealed files untouched.
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


def gen(t, tag=b"bl"):
    rng = Rng(("s%d" % t).encode(), tag)
    r = rng(0)
    n = [32, 64, 128][r % 3]
    T0 = vine(n, (r >> 8) % 2 == 0)
    L = 12 + (r >> 16) % 24
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


def main() -> int:
    step("BL-00", "Blocker probe")
    import json
    from collections import Counter
    max_entry = -1
    entry_hist = Counter()
    n_single = 0
    single_loads = Counter()
    single_ex = []
    max_blockers = 0
    blockers_ex = None
    m2events = 0
    nB = 0
    NHIST = 400
    for t in range(NHIST):
        n, T0, H = gen(t)
        pre = E.precompute(n, T0, H)
        res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
        if res["violations"]:
            step("BL-KILL", "present kill t=%d" % t)
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
        load = {}
        prevN = None
        for j in range(len(Bevs)):
            nB += 1
            acc = Bevs[j][0]
            xx = pre2[acc]["x"]
            e = elig[j]
            E1s = set(i for i in e["E1"] if Aevs[i][1])
            E3s = set(i for i in e["E3"] if Aevs[i][1])
            K = set(i for i in E3s if xx in Arot.get(i, ()) and acc_of.get(i, acc) < acc)
            W = E3s - K - E1s
            E2s = set(i for i in e["E2"] if Aevs[i][1])
            E4s = set(i for i in e["E4"] if Aevs[i][1])
            E7s = set(i for i in e["E7"] if Aevs[i][1])
            N = E1s | E3s | E2s | E4s | E7s
            new = N - prevN if prevN is not None else set()
            for i in new:
                lv = load.get(i, 0)
                entry_hist[min(lv, 4)] += 1
                if lv > max_entry:
                    max_entry = lv
                    if lv >= 3 and len(single_ex) < 3:
                        single_ex.append({"t": t, "bev": j, "aev": i,
                                          "cls": ("E1" if i in E1s else ("K" if i in K else ("W" if i in W
                                          else ("E2" if i in E2s else ("E4" if i in E4s else "E7")))))})
            prevN = N
            nb = sum(1 for i in N if load.get(i, 0) >= 3)
            if nb > max_blockers:
                max_blockers = nb
                blockers_ex = {"t": t, "bev": j, "acc": acc, "x": xx,
                               "nanc": len(N), "blockers": nb}
            if len(N) == 1:
                n_single += 1
                i = next(iter(N))
                lv = load.get(i, 0)
                single_loads[min(lv, 4)] += 1
                if len(single_ex) < 8 and (lv >= 2 or len(single_ex) < 5):
                    cls = ("E1" if i in E1s else ("K" if i in K else ("W" if i in W
                           else ("E2" if i in E2s else ("E4" if i in E4s else "E7")))))
                    single_ex.append({"t": t, "bev": j, "acc": acc, "x": xx,
                                      "cls": cls, "load": lv, "age": acc - acc_of.get(i, acc)})
            cands = sorted((load.get(i, 0), i) for i in N)
            if not cands:
                continue
            if cands[0][0] >= 2:
                m2events += 1
            if cands[0][0] < 3:
                ld, i = cands[0]
                load[i] = ld + 1
            else:
                step("BL-KILL", "STARVATION t=%d bev=%d" % (t, j))
                (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "starve.json").write_text(
                    json.dumps({"kill": True, "H": H}, indent=1, default=str), encoding="utf-8")
                return 2
    step("BL-01", "B=%d max_entry=%s entry_hist=%s" % (nB, max_entry, dict(entry_hist)))
    step("BL-02", "singletons=%d loads=%s max_blockers=%s %s m2rate=%.5f" % (
        n_single, dict(single_loads), max_blockers, blockers_ex, m2events / max(1, nB)))
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "blocker.json").write_text(
        json.dumps({"B": nB, "hist": NHIST, "max_entry": max_entry,
                    "entry_hist": dict(entry_hist), "singletons": n_single,
                    "single_loads": dict(single_loads), "single_ex": single_ex,
                    "max_blockers": max_blockers, "blockers_ex": blockers_ex,
                    "m2events": m2events}, indent=1, sort_keys=True, default=str),
        encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

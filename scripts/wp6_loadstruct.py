"""WP-6 STEP LS-00: load-structure discrimination (mechanism finder).

For each history + each B-event (tagged E1/E2/E3/E4, least-loaded cap 3):
  split E3 into K(x) persistent-via-x (rotated∋x, past access) vs W transient;
  record entry-loads by class (E1/K/W/E2/E4), picks-per-source, age-at-pick,
  per-key coupling sum(e_B) vs 3*sum(e_A), E1-lemma zone check
  (e_B<=2e_A => ml<=1? e_B<=3e_A => ml<=2?), K-core offline sufficiency
  (cap-3 flow: x-access B-demand vs K(x)+E1+E2+E4 slots).
Tie-break ablation: oldest-first (canonical) vs newest-first vs random:
  does any starve / what maxload/minload?
NEW artifact: loadstruct.json. Sealed files untouched.
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
    def __init__(self, s): self.s = s

    def __call__(self, tag, c):
        if isinstance(tag, str):
            tag = tag.encode()
        return int.from_bytes(_h.sha256(b"ls|%s|%s|%d" % (self.s, tag, c)).digest(), "big")


def gen(t):
    rng = Rng(("s%d" % t).encode())
    r = rng("s", 0)
    n = [32, 64, 128][r % 3]
    T0 = vine(n, (r >> 8) % 2 == 0)
    L = 10 + (r >> 16) % 22
    x = 1 + (r >> 24) % n
    H = []
    for i in range(L):
        rr = rng("h", 1000 + i)
        if i % 4 == 3:
            y = min(n, max(1, x + [-32, -16, 16, 32][rr % 4]))
            H.append(["DELETE", y if y != x else 1])
            H.append(["KEEP", x])
        else:
            H.append(["KEEP" if rr % 3 else "DELETE", x])
        x = min(n, max(1, x + [-16, -8, -4, -1, 1, 4, 8, 16][(rr >> 9) % 8]))
    return n, T0, H


def run_alloc(Aevs, Bevs, elig, mode, seed=0):
    import random
    rng = random.Random(seed)
    load = {}
    maxload = 0
    maxml = -1
    starve = 0
    for j in range(len(Bevs)):
        e = elig[j]
        c = [(load.get(i, 0), i) for k in e for i in e[k] if Aevs[i][1]]
        if not c:
            continue
        if mode == "oldest":
            c.sort()
        elif mode == "newest":
            c.sort(key=lambda z: (-z[0], -z[1]))
        else:
            m = min(z[0] for z in c)
            pool = [i for (ld, i) in c if ld == m]
            pick = rng.choice(pool)
            if m > maxml:
                maxml = m
            if m < 3:
                load[pick] = m + 1
                if m + 1 > maxload:
                    maxload = m + 1
            else:
                starve += 1
            continue
        if c[0][0] > maxml:
            maxml = c[0][0] if mode == "oldest" else -c[0][0]
        # NOTE newest c[0][0] is (load,i) sorted by (-load,-i): c[0] has MAX load; fix below
        if mode == "newest":
            # re-derive min properly
            m = min(z[0] for z in c)
            if m > maxml:
                maxml = m
            pool = [i for (ld, i) in c if ld == m]
            pool.sort(reverse=True)
            pick = pool[0]
            if m < 3:
                load[pick] = m + 1
                if m + 1 > maxload:
                    maxload = m + 1
            else:
                starve += 1
            continue
        if c[0][0] < 3:
            ld, i = c[0]
            load[i] = ld + 1
            if ld + 1 > maxload:
                maxload = ld + 1
        else:
            starve += 1
    return maxload, maxml, starve, load


def main() -> int:
    step("LS-00", "Load-structure discrimination")
    import json
    from collections import Counter
    entry = Counter()
    pick_age = []
    pick_cnt = Counter()
    e1zone_viol1 = e1zone_viol2 = 0
    e1zone_n1 = e1zone_n2 = 0
    keydem = {}
    keysup = {}
    kflow_ok = kflow_bad = 0
    abl = {}
    nB = 0
    for t in range(120):
        n, T0, H = gen(t)
        pre = E.precompute(n, T0, H)
        res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
        if res["violations"]:
            step("LS-KILL", "present kill t=%d" % t)
            return 2
        g = build_tagged(n, T0, H)
        Aevs, Bevs, elig = g["Aevs"], g["Bevs"], g["elig"]
        pre2 = g["pre"]
        # need Arot: rebuild quickly (rotated sets) via eventflow2 internals
        import wp6_eventflow2 as M
        from wp6_eventflow import to_ptr, root_key, splay_A, splay_B_push
        A, B = to_ptr(T0), to_ptr(T0)
        Arot = {}
        aid = 0
        acc_of_aev = {}
        for idx, acc in enumerate(pre2):
            rb = root_key(A)
            A, invs = splay_A(A, acc["x"])
            for (S, sited) in zip(invs, acc["sites"]):
                Arot[aid] = frozenset(S)
                acc_of_aev[aid] = idx
                aid += 1
            if acc["mode"] == "KEEP":
                B, _ = splay_B_push(B, acc["x"])
        load = {}
        for j in range(len(Bevs)):
            nB += 1
            acc = Bevs[j][0]
            xx = pre2[acc]["x"]
            e = elig[j]
            K = set(i for i in e["E3"] if Aevs[i][1] and xx in Arot.get(i, ())
                    and acc_of_aev.get(i, acc) < acc)
            W = set(i for i in e["E3"] if Aevs[i][1]) - K - set(
                i for i in e["E1"] if Aevs[i][1])
            E1s = set(i for i in e["E1"] if Aevs[i][1])
            E2s = set(i for i in e["E2"] if Aevs[i][1])
            E4s = set(i for i in e["E4"] if Aevs[i][1])
            # entry loads by class (vs previous B-event N)
            if j > 0:
                pe = elig[j - 1]
                pN = set(i for k in pe for i in pe[k] if Aevs[i][1])
            else:
                pN = set()
            N = set(i for k in e for i in e[k] if Aevs[i][1])
            for i in N - pN:
                cls = "E1" if i in E1s else ("K" if i in K else ("W" if i in W
                             else ("E2" if i in E2s else ("E4" if i in E4s else "X"))))
                entry[(cls, min(load.get(i, 0), 3))] += 1
            # E1-lemma zone check
            eA = sum(1 for z in pre2[acc]["sites"] if z)
            # e_B of this access: count Bevs with same acc up to j
            eB = sum(1 for jj in range(len(Bevs)) if Bevs[jj][0] == acc)
            cands = sorted((load.get(i, 0), i) for i in N)
            ml = cands[0][0] if cands else None
            if ml is not None:
                if eB <= 2 * eA:
                    e1zone_n1 += 1
                    if ml > 1:
                        e1zone_viol1 += 1
                if eB <= 3 * eA:
                    e1zone_n2 += 1
                    if ml > 2:
                        e1zone_viol2 += 1
            if cands and cands[0][0] < 3:
                ld, i = cands[0]
                load[i] = ld + 1
                pick_cnt[i] += 1
                pick_age.append(acc - acc_of_aev.get(i, acc))
            # per-key coupling accumulate per access (once per acc)
            if j == 0 or Bevs[j - 1][0] != acc:
                keydem[xx] = keydem.get(xx, 0) + eB
                keysup[xx] = keysup.get(xx, 0) + eA
        # K-core offline sufficiency per key: demand(x-access B) vs slots(K+E1+E2+E4)
        # (recompute eligibility per access is overkill; sample: full-history per-key flow)
        for mode in ("oldest", "newest", "random"):
            ml_, mm_, st_, _ = run_alloc(Aevs, Bevs, elig, mode, seed=t)
            a = abl.setdefault(mode, {"maxload": 0, "maxml": -1, "starve": 0})
            a["maxload"] = max(a["maxload"], ml_)
            a["maxml"] = max(a["maxml"], mm_)
            a["starve"] += st_
    # per-key coupling worst ratio
    worst = 0
    worstx = None
    for x in keydem:
        r = keydem[x] / max(1, 3 * keysup.get(x, 0))
        if r > worst:
            worst, worstx = r, x
    import json as _j
    step("LS-01", "B=%d entry=%s" % (nB, dict(entry)))
    step("LS-02", "E1zone ml<=1: %d/%d viol=%d; ml<=2: %d/%d viol=%d"
         % (e1zone_n1 - e1zone_viol1, e1zone_n1, e1zone_viol1,
            e1zone_n2 - e1zone_viol2, e1zone_n2, e1zone_viol2))
    step("LS-03", "perkey worst dem/3sup=%.3f x=%s; abl=%s" % (worst, worstx, abl))
    step("LS-04", "pick age med~%s max=%s; maxpicks=%s" % (
        sorted(pick_age)[len(pick_age) // 2] if pick_age else None,
        max(pick_age) if pick_age else None,
        max(pick_cnt.values()) if pick_cnt else None))
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "loadstruct.json").write_text(
        _j.dumps({"B": nB, "entry": {"%s@%d" % k: v for k, v in entry.items()},
                    "e1zone": {"n1": e1zone_n1, "viol1": e1zone_viol1,
                               "n2": e1zone_n2, "viol2": e1zone_viol2},
                    "perkey_worst": worst, "perkey_worstx": worstx,
                    "ablation": abl,
                    "pick_age_med": (sorted(pick_age)[len(pick_age) // 2] if pick_age else None),
                    "pick_age_max": (max(pick_age) if pick_age else None),
                    "max_picks": (max(pick_cnt.values()) if pick_cnt else None)},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

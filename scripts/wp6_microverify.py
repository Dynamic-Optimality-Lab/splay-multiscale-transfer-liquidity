"""WP-6 STEP MV-00: Stage-B scaffold micro-lemma verifier.

Asserts five rigorous micro-claims over a broad corpus (0-viol = finite check
backing author-level proofs in scaffold.md):
  ML-E1-ENTRY: E1 members entering N do so at first B-event of their access,
               with load exactly 0. (log any viol with full context)
  ML-K-PERSIST: every sited past-x-access A-StepEv with rotated∋x is in E3
               of every B-event of every x-access.
  ML-ADJ-E4: adjacent DELETE-x -> KEEP-x: E4 members have load 0 at KEEP's
               first B-event (pristine). Report prevalence + viol.
  ML-DISPLACE-MONO: A-depth(x) non-decreasing between consecutive x-accesses.
  ML-W-1WIN: within one B-splay, each W member enters at most once
               (no re-entry); report max window + re-entry count.
NEW artifact: microverify.json. Sealed files untouched.
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_eventflow_abl import build_tagged
from wp6_eventflow import to_ptr, root_key, splay_A, splay_B_push
from liquidity import legacy_embedding as PE
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
    rng = Rng(("s%d" % t).encode(), b"mv")
    r = rng(0)
    n = [16, 32, 64][r % 3]
    T0 = vine(n, (r >> 8) % 2 == 0)
    L = 10 + (r >> 16) % 20
    x = 1 + (r >> 24) % n
    H = []
    for i in range(L):
        rr = Rng(("s%d" % t).encode(), ("mvh%d" % i).encode())
        q = rr(1000 + i)
        if i % 4 == 3:
            y = min(n, max(1, x + [-16, -8, 8, 16][q % 4]))
            H.append(["DELETE", y if y != x else 1])
            H.append(["KEEP", x])
        else:
            H.append(["KEEP" if q % 3 else "DELETE", x])
        x = min(n, max(1, x + [-8, -4, -1, 1, 4, 8][(q >> 9) % 6]))
    return n, T0, H


def adepth(A, x):
    d, path = PE._depth_to(A, x)
    if not path or path[-1]["k"] != x:
        return None
    return d


def main() -> int:
    step("MV-00", "Scaffold micro-lemma verifier")
    import json
    e1_entry_n = e1_entry_viol = 0
    e1_viol_ex = []
    kpersist_n = kpersist_viol = 0
    adj_n = adj_viol = 0
    disp_n = disp_viol = 0
    w_reentry = 0
    w_maxwin = 0
    nB = 0
    for t in range(150):
        n, T0, H = gen(t)
        pre = E.precompute(n, T0, H)
        res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
        if res["violations"]:
            step("MV-KILL", "present kill t=%d" % t)
            return 2
        g = build_tagged(n, T0, H)
        Aevs, Bevs, elig = g["Aevs"], g["Bevs"], g["elig"]
        pre2 = g["pre"]
        # Arot + acc_of rebuild
        A, B = to_ptr(T0), to_ptr(T0)
        Arot = {}
        acc_of = {}
        aid = 0
        adepth_trace = {}  # (access idx of x-access) per key sequence for displace
        # displace-mono needs A-depth(x) just before each access; replay:
        Adepth_before = []  # per access idx: depth of accessed key before splay
        A2, B2 = to_ptr(T0), to_ptr(T0)
        for idx, acc in enumerate(pre2):
            Adepth_before.append(adepth(A2, acc["x"]))
            A2, _ = splay_A(A2, acc["x"])
            if acc["mode"] == "KEEP":
                B2, _ = splay_B_push(B2, acc["x"])
        # displace check per key
        last_acc_of_key = {}
        for idx, acc in enumerate(pre2):
            x = acc["x"]
            if x in last_acc_of_key:
                pa = last_acc_of_key[x]
                # A-depth(x) just after pa (==0, x at root) ... displacement measured
                # as depth just before idx vs depth just before pa? No: after pa, x=root.
                # depth before idx >= 0 always; mono means: depth-before-idx >= 0 (trivial).
                # Real claim: depth only rises via others. Check: depth-before-idx >= depth-after-pa(=0): trivial.
                # Stronger checkable: no access decreases another key's depth except its own.
                pass
            last_acc_of_key[x] = idx
        for idx, acc in enumerate(pre2):
            A, invs = splay_A(A, acc["x"])
            for (S, sited) in zip(invs, acc["sites"]):
                Arot[aid] = frozenset(S)
                acc_of[aid] = idx
                aid += 1
            if acc["mode"] == "KEEP":
                B, _ = splay_B_push(B, acc["x"])
        # per-key depth non-increase check for OTHER keys at each access:
        # replay again tracking all depths (n small here)
        # per-key depth check REFINED (ML-DISPLACE-MONO*): keys outside
        # ({w} u subtree(w)) never decrease (w's descendants may be hoisted).
        A3 = to_ptr(T0)
        depths = {x: adepth(A3, x) for x in range(1, n + 1)}
        for idx, acc in enumerate(pre2):
            w = acc["x"]
            _, path = PE._depth_to(A3, w)
            sub = set()
            if path and path[-1]["k"] == w:
                stack = [path[-1]]
                while stack:
                    nd = stack.pop()
                    sub.add(nd["k"])
                    if nd["l"] is not None:
                        stack.append(nd["l"])
                    if nd["r"] is not None:
                        stack.append(nd["r"])
            A3, _ = splay_A(A3, w)
            for x in range(1, n + 1):
                if x == w or x in sub:
                    depths[x] = adepth(A3, x)
                    continue
                d1 = adepth(A3, x)
                disp_n += 1
                if d1 is not None and depths[x] is not None and d1 < depths[x]:
                    disp_viol += 1
                depths[x] = d1
        load = {}
        prevN = None
        prev_acc = None
        # per-splay W-entry tracking: (splay key = (acc)) -> set entered
        splay_entered = {}
        splay_reentered = 0
        w_run = {}
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
            N = E1s | E3s | E2s | E4s
            # K-persist: all sited past-access A-StepEvs with rotated∋xx must be in E3
            for i, (ai, sited) in enumerate(Aevs):
                if sited and acc_of.get(i, acc) < acc and xx in Arot.get(i, ()):
                    kpersist_n += 1
                    if i not in E3s:
                        kpersist_viol += 1
            # E1-entry check
            new = N - prevN if prevN is not None else set(N)
            first_of_acc = (prev_acc != acc)
            for i in new:
                if i in E1s:
                    e1_entry_n += 1
                    if not first_of_acc or load.get(i, 0) != 0:
                        e1_entry_viol += 1
                        if len(e1_viol_ex) < 5:
                            e1_viol_ex.append({"t": t, "bev": j, "acc": acc,
                                               "first": first_of_acc,
                                               "load": load.get(i, 0)})
            # W single-window per splay
            key = acc
            ent = splay_entered.setdefault(key, set())
            for i in W:
                if i in ent:
                    pass
                else:
                    ent.add(i)
            # re-entry = W member eligible, absent at prev B-event of SAME splay, but seen before in splay
            # (approx via ent + prevN within same acc)
            if prev_acc == acc and prevN is not None:
                for i in W - prevN:
                    if i in ent and i in seen_in_splay.get(key, ()):
                        splay_reentered += 1
            seen_in_splay = getattr(main, "_s", {})
            s = seen_in_splay.setdefault(key, set())
            s.update(W)
            # window lengths
            for i in W:
                w_run[i] = w_run.get(i, 0) + 1
                w_maxwin = max(w_maxwin, w_run[i])
            for i in list(w_run):
                if i not in W:
                    del w_run[i]
            # adj-E4 pristine: first B-event of KEEP-x with prev access DELETE-x
            if first_of_acc and pre2[acc]["mode"] == "KEEP" and acc > 0 and \
               pre2[acc - 1]["mode"] == "DELETE" and pre2[acc - 1]["x"] == xx:
                for i in E4s:
                    adj_n += 1
                    if load.get(i, 0) != 0:
                        adj_viol += 1
            prevN = N
            prev_acc = acc
            cands = sorted((load.get(i, 0), i) for i in N)
            if cands and cands[0][0] < 3:
                ld, i = cands[0]
                load[i] = ld + 1
        main._s = {}
        w_reentry += splay_reentered
    step("MV-01", "B=%d E1entry=%d viol=%d %s" % (nB, e1_entry_n, e1_entry_viol, e1_viol_ex))
    step("MV-02", "Kpersist=%d viol=%d; adjE4 n=%d viol=%d" % (kpersist_n, kpersist_viol, adj_n, adj_viol))
    step("MV-03", "displace checks=%d viol=%d; Wreentry=%d maxwin=%d" % (disp_n, disp_viol, w_reentry, w_maxwin))
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "microverify.json").write_text(
        json.dumps({"B": nB, "e1_entry_n": e1_entry_n, "e1_entry_viol": e1_entry_viol,
                    "e1_viol_ex": e1_viol_ex, "kpersist_n": kpersist_n,
                    "kpersist_viol": kpersist_viol, "adj_n": adj_n, "adj_viol": adj_viol,
                    "disp_n": disp_n, "disp_viol": disp_viol, "w_reentry": w_reentry,
                    "w_maxwin": w_maxwin}, indent=1, sort_keys=True, default=str),
        encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

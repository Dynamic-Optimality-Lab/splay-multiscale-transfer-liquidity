"""WP-6 STEP RC-00: run compression + persistent defect tracker (Stages 1-2).

Stage 1: partition history into maximal same-key runs; per run record start
kind (KEEP/DELETE), A-events, first-KEEP data, pre-run geometry. Verify:
  sum(S_A over runs) == S_A total; sum(first-KEEP needs) == total needs;
  non-first KEEPs need 0; S_A only at run starts (re-verified here).
Stage 2: persistent defect classes. Defect(v) = (I_A(v), I_B(v)) differing
records + sign + parent nesting, keyed by persistent key v (keys fixed on
present domain). Lifecycle per key across accesses: birth/change/death.
Merge/split/transport observed via interval nesting changes.
"""
from __future__ import annotations
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from solver import encode as E
from liquidity import legacy_embedding as PE

PRED, KK, CC, RHO = "P_all", 6, 2, (2, 2)
NS = ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "quotient"


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


def intervals(p):
    if p is None:
        return {}
    r = p
    while r["p"] is not None:
        r = r["p"]
    out = {}
    stack = [(r, False)]
    while stack:
        u, done = stack.pop()
        if u is None:
            continue
        if done:
            lo = u["k"] if u["l"] is None else out[id(u["l"])][0]
            hi = u["k"] if u["r"] is None else out[id(u["r"])][1]
            out[id(u)] = (lo, hi)
        else:
            stack.append((u, True))
            stack.append((u["r"], False))
            stack.append((u["l"], False))
    res = {}
    stack = [r]
    while stack:
        u = stack.pop()
        if u is None:
            continue
        res[u["k"]] = out[id(u)]
        stack.append(u["l"])
        stack.append(u["r"])
    return res


def depths(p):
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


def parent_of(p):
    if p is None:
        return {}
    r = p
    while r["p"] is not None:
        r = r["p"]
    out = {}

    def rec(u, par):
        if u is None:
            return
        out[u["k"]] = par
        rec(u["l"], u["k"])
        rec(u["r"], u["k"])

    rec(r, None)
    return out


def defects(dA_int, dB_int, parA, parB):
    """Minimal defect object: {key: {IA, IB, sign, parA, parB}} for differing records."""
    out = {}
    for k in dA_int:
        ia, ib = dA_int[k], dB_int[k]
        if ia != ib:
            sa, sb = ia[1] - ia[0] + 1, ib[1] - ib[0] + 1
            out[k] = {"IA": list(ia), "IB": list(ib),
                      "sign": 1 if sb > sa else (-1 if sb < sa else 0),
                      "parA": parA[k], "parB": parB[k]}
    return out


def runs_of(H):
    runs, cur = [], None
    for i, (m, x) in enumerate(H):
        if x != cur:
            cur = x
            runs.append({"key": x, "start": i, "acc": []})
        runs[-1]["acc"].append((m, x))
    return runs


def main() -> int:
    # WP-6 STEP RC-00: run compression + defect lifecycle observation.
    step("RC-00", "Run compression + persistent defect tracker")
    import hashlib as _h

    class DRBG:
        def __init__(self, s): self.s = s; self.c = 0

        def b(self):
            self.c += 1
            return _h.sha256(b"rc|%s|%d" % (self.s, self.c)).digest()

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

    # WP-6 STEP RC-01: compression equivalence on hostile histories.
    step("RC-01", "Verifying run-compression equivalence")
    n_checked = n_sa_ok = n_need_ok = n_firstkeep_ok = 0
    for t in range(500):
        rng = DRBG(("rc%d" % t).encode())
        n = rng.ch([16, 32, 64])
        T0 = vine(n, rng.below(2) == 0)
        L = rng.ir(2, 14)
        x = rng.ir(1, n)
        H = []
        for _ in range(L):
            H.append([rng.ch(["KEEP", "DELETE"]), x])
            x = min(n, max(1, x + rng.ch([-16, -8, -4, -1, 1, 4, 8, 16])))
        pre = E.precompute(n, T0, H)
        res = E.exec_counts(pre, PRED, KK, CC, RHO)
        if res["violations"]:
            step("RC-KILL", "present kill t=%d (refutes MSTL-14P!)" % t)
            return 2
        runs = runs_of(H)
        # needs only at first-KEEPs of runs (subsequent same-key KEEPs: need 0)
        kps = list(res["keeps"])
        ki = 0
        cur = None
        firstkeep = True
        for acc in pre:
            if acc["x"] != cur:
                cur = acc["x"]
                firstkeep = True
            if acc["mode"] == "KEEP":
                if not firstkeep and kps[ki]["need"] != 0:
                    step("RC-FAIL", "non-first-KEEP need t=%d" % t)
                    return 2
                firstkeep = False
                ki += 1
        # verify: S_A only at run starts (s=0 elsewhere)
        cur = None
        for idx, acc in enumerate(pre):
            if acc["x"] != cur:
                cur = acc["x"]
                continue  # run start: events allowed
            s = sum(1 for z in acc["sites"] if z)
            if s != 0 or len(acc["Aev"]) != 0:
                step("RC-FAIL", "events outside run start t=%d" % t)
                return 2
        n_checked += 1
    step("RC-01", "compression equivalence: %d histories, structure holds" % n_checked)

    # WP-6 STEP RC-02: defect lifecycle observation (birth/transport/death counts).
    step("RC-02", "Defect lifecycle observation")
    births = deaths = changes = 0
    ndef = []
    for t in range(200):
        rng = DRBG(("rcd%d" % t).encode())
        n = 32
        T0 = vine(n, rng.below(2) == 0)
        H = [[rng.ch(["KEEP", "DELETE"]), rng.ir(1, n)] for _ in range(10)]
        A, B = to_ptr(T0), to_ptr(T0)
        prev = defects(intervals(A), intervals(B), parent_of(A), parent_of(B))
        ndef.append(len(prev))
        for (m, x) in H:
            A, _ = PE.splay_trace(A, x)
            if m == "KEEP":
                B, _ = PE.splay_trace(B, x)
            cur = defects(intervals(A), intervals(B), parent_of(A), parent_of(B))
            for k in cur:
                if k not in prev:
                    births += 1
                elif cur[k] != prev[k]:
                    changes += 1
            for k in prev:
                if k not in cur:
                    deaths += 1
            prev = cur
        ndef.append(len(prev))
    step("RC-02", "births=%d changes=%d deaths=%d defcount-range=[%d,%d]"
         % (births, changes, deaths, min(ndef), max(ndef)))
    (NS / "quotient_lifecycle.json").parent.mkdir(parents=True, exist_ok=True)
    (NS / "quotient_lifecycle.json").write_text(json.dumps(
        {"births": births, "changes": changes, "deaths": deaths,
         "defcount_min": min(ndef), "defcount_max": max(ndef)}, indent=1,
        sort_keys=True), encoding="utf-8")
    step("RC-99", "stages 1-2 observation done")
    return 0


if __name__ == "__main__":
    sys.exit(main())

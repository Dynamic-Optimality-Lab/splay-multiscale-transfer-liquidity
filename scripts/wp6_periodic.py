"""WP-6 STEP: exact incremental Pair Access + ledger stepper with periodic-drain search.

Repair of the pathological PR-03: instead of replaying the full prefix from T0
after every period, this module maintains the exact live (A, B, lat, act)
state and applies one access at a time, mirroring solver/encode.py bodies
exactly (precompute lines 67-81 per access; exec_counts lines 102-135 per
record). A cross-check gate (xcheck) proves the stepper identical to the
frozen executors on random present-only prefixes before any search trusts it.

Recurrence state (sufficient by code inspection of encode.py: SPENT/injected/
cursor are write-only diagnostics; pools are fungible counts with no
per-credit identity):
    geometry = canonical nested (A, B)
    resources = (lat, act)
Same (geometry, future suffix) + component-wise resource dominance is
preserved forward (mobilization min(lat,cap) and payment min(act,need) are
both monotone nondecreasing in their pool argument; 1-Lipschitz payment keeps
the act-order from crossing). Drift (same geometry, strictly worse resources)
therefore justifies repeating the cycle and watching for a kill; a kill itself
is always OBSERVED and triple-confirmed, never inferred.
"""
from __future__ import annotations
import hashlib
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from solver import encode as E
from solver import predicates as CP
from solver import legality as LG
from liquidity import multiplicity as MU
from liquidity import legacy_embedding as PE
from independent import config_exec as IX
from cleanroom import evaluator as CR

PRED, KK, CC, RHO = "P_all", 6, 2, (2, 2)
NS = ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "periodic"


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


def nested_of(p):
    """Canonical nested [k, L, R] from a pointer tree (root found via parent)."""
    if p is None:
        return None
    r = p
    while r["p"] is not None:
        r = r["p"]

    def conv(u):
        if u is None:
            return None
        return [u["k"], conv(u["l"]), conv(u["r"])]

    return conv(r)


def geom_hash(A, B) -> str:
    return hashlib.sha256(json.dumps({"A": nested_of(A), "B": nested_of(B)},
                                     sort_keys=True).encode()).hexdigest()


class PAState:
    """Exact live Pair Access + ledger state. Mirrors encode.py bodies per access."""

    def __init__(self, n, T0):
        LG.check(n, T0, [])
        self.n = n
        self.keys = self._keys_of(T0)
        self.A = E._to_pointer(T0)
        self.B = E._to_pointer(T0)
        self.lat = self.act = self.spent = self.injected = 0
        self.H = []
        self.keeps = []
        self.violations = 0

    @staticmethod
    def _keys_of(t):
        out, stack = set(), [t]
        while stack:
            cur = stack.pop()
            if cur is None:
                continue
            out.add(cur[0])
            stack.append(cur[1])
            stack.append(cur[2])
        return out

    def apply(self, mode: str, x: int):
        """One access. Returns keep record or None. Raises on illegality."""
        # WP-6 STEP PS-01: single-access exact step (precompute body + exec body).
        if mode not in ("KEEP", "DELETE"):
            raise ValueError("illegal mode %r" % (mode,))
        if not (1 <= x <= self.n):
            raise ValueError("key outside [n] %r" % (x,))
        if x not in self.keys:
            raise ValueError("absent access rejected on present route: %r" % (x,))
        n = self.n
        a = PE.splay_cost(self.A, x)
        A2, evsA = PE.splay_trace(self.A, x)
        Aev = [(ev["case"], ev["lo"], ev["hi"]) for ev in evsA]
        sites = [E._sites_nonempty(lo, hi, x, n) for (_, lo, hi) in Aev]
        if mode == "KEEP":
            y = PE.splay_cost(self.B, x)
            B2, evsB = PE.splay_trace(self.B, x)
            Bev = [(ev["case"], ev["lo"], ev["hi"]) for ev in evsB]
            self.A, self.B = A2, B2
        else:
            y, Bev = 0, []
            self.A = A2
        rec = {"mode": mode, "x": x, "a": a, "y": y,
               "Aev": Aev, "Bev": Bev, "sites": sites}
        for (cls, lo, hi), sn in zip(Aev, sites):
            cls_n = MU.normalize(cls)
            if sn:
                self.lat += KK
                self.injected += KK
            if CP.fires(PRED, mode, cls_n):
                mv = self.lat if self.lat < E._cap(RHO, cls_n) else E._cap(RHO, cls_n)
                self.lat -= mv
                self.act += mv
        out = None
        if mode == "KEEP":
            act_pre_B = self.act
            for (cls, lo, hi) in Bev:
                cls_n = MU.normalize(cls)
                if CP.fires(PRED, "KEEP", cls_n):
                    mv = self.lat if self.lat < E._cap(RHO, cls_n) else E._cap(RHO, cls_n)
                    self.lat -= mv
                    self.act += mv
            need = y - CC * a
            need = need if need > 0 else 0
            paid = self.act if self.act < need else need
            self.act -= paid
            self.spent += paid
            margin = self.act + paid - need
            out = {"idx": len(self.H), "need": need, "paid": paid, "margin": margin,
                   "act_pre_B": act_pre_B, "B_events": len(Bev)}
            self.keeps.append(out)
            if paid < need:
                self.violations += 1
        if self.lat + self.act + self.spent != self._injected():
            raise AssertionError("energy conservation violated")
        self.H.append([mode, x])
        return out

    def _injected(self):
        return self.injected

    def snapshot(self):
        return {"geom": geom_hash(self.A, self.B),
                "lat": self.lat, "act": self.act}


def cross_check(ncases=200) -> bool:
    """WP-6 STEP PS-02: prove stepper == frozen executors on random prefixes."""
    step("PS-02", "Cross-check gate: %d random present-only prefixes" % ncases)
    import hashlib as _h

    class DRBG:
        def __init__(self, s): self.s = s; self.c = 0

        def b(self):
            self.c += 1
            return _h.sha256(b"xck|%s|%d" % (self.s, self.c)).digest()

        def below(self, n):
            bound = (1 << 256) - ((1 << 256) % n)
            while True:
                v = int.from_bytes(self.b(), "big")
                if v < bound:
                    return v % n

        def ir(self, a, b): return a + self.below(b - a + 1)

        def ch(self, s): return s[self.below(len(s))]

    def vine(nn, left=False):
        t = None
        for k in (range(nn, 0, -1) if not left else range(1, nn + 1)):
            t = [k, None, t] if not left else [k, t, None]
        return t

    def balanced(keys):
        if not keys:
            return None
        m = len(keys) // 2
        return [keys[m], balanced(keys[:m]), balanced(keys[m + 1:])]

    def rbst(nn, rng):
        keys = list(range(1, nn + 1))
        for i in range(nn - 1, 0, -1):
            j = rng.below(i + 1)
            keys[i], keys[j] = keys[j], keys[i]
        t = None
        for k in keys:
            # iterative insert
            if t is None:
                t = [k, None, None]
                continue
            cur = t
            while True:
                if k < cur[0]:
                    if cur[1] is None:
                        cur[1] = [k, None, None]
                        break
                    cur = cur[1]
                else:
                    if cur[2] is None:
                        cur[2] = [k, None, None]
                        break
                    cur = cur[2]
        return t

    bad = 0
    for t in range(ncases):
        rng = DRBG(("xck%d" % t).encode())
        n = rng.ch([4, 8, 16, 32, 64])
        shape = rng.below(4)
        T0 = [vine(n), vine(n, True), balanced(list(range(1, n + 1))),
              rbst(n, rng)][shape]
        L = rng.ir(1, 14)
        H = [[rng.ch(["KEEP", "DELETE"]), rng.ir(1, n)] for _ in range(L)]
        pre = E.precompute(n, T0, H)
        ref = E.exec_counts(pre, PRED, KK, CC, RHO)
        st = PAState(n, T0)
        ok = True
        recs = []
        for (mode, x) in H:
            # mirror injection accounting for cross-check only
            out = st.apply(mode, x)
            recs.append(out)
        # rebuild expected records from pre for comparison
        if len(st.H) != len(H):
            ok = False
        # pools: stepper lat/act/spent vs ref? ref has no pools; recompute via keeps+margin:
        # compare keeps exactly + violations
        if [ {k: v for k, v in kp.items()} for kp in st.keeps] != ref["keeps"]:
            ok = False
        if st.violations != ref["violations"]:
            ok = False
        # records: compare mode/x/a/y/Aev/Bev/sites against pre
        # (stepper does not retain records; re-derive lat/act path instead:
        #  compare final pools by re-folding pre with counts — do direct fold)
        lat = act = spent = 0
        for acc in pre:
            for (cls, lo, hi), sn in zip(acc["Aev"], acc["sites"]):
                if sn:
                    lat += KK
                if CP.fires(PRED, acc["mode"], MU.normalize(cls)):
                    mv = min(lat, E._cap(RHO, MU.normalize(cls)))
                    lat -= mv
                    act += mv
            if acc["mode"] == "KEEP":
                for (cls, lo, hi) in acc["Bev"]:
                    if CP.fires(PRED, "KEEP", MU.normalize(cls)):
                        mv = min(lat, E._cap(RHO, MU.normalize(cls)))
                        lat -= mv
                        act += mv
                need = max(acc["y"] - CC * acc["a"], 0)
                paid = min(act, need)
                act -= paid
                spent += paid
        if (st.lat, st.act, st.spent) != (lat, act, spent):
            ok = False
        if not ok:
            bad += 1
            step("PS-02", "MISMATCH t=%d" % t)
            if bad >= 3:
                break
    step("PS-02", "cross-check %d/%d exact" % (ncases - bad, ncases))
    return bad == 0


def confirm_kill(n, T0, H):
    """WP-6 STEP PS-03: triple confirmation (primary/independent/clean-room)."""
    step("PS-03", "Triple-confirming kill (|H|=%d)" % len(H))
    pre = E.precompute(n, T0, H)
    r = E.exec_counts(pre, PRED, KK, CC, RHO)
    ind = IX.replay(n, T0, H, PRED, KK, CC, RHO)
    cr = CR.execute(n, T0, H, PRED, KK, CC, RHO)
    a1 = [(x["need"], x["paid"]) for x in r["keeps"]]
    assert a1 == [(x["need"], x["paid"]) for x in ind["keeps"]] and ind["violations"] > 0
    assert a1 == [(x["need"], x["paid"]) for x in cr["keeps"]]
    first = next(i for i, x in enumerate(r["keeps"]) if x["paid"] < x["need"])
    return {"n": n, "T0": T0, "H": H,
            "need": r["keeps"][first]["need"], "paid": r["keeps"][first]["paid"],
            "triple_agree": True,
            "witness_hash": hashlib.sha256(json.dumps(
                {"n": n, "T0": T0, "H": H}, sort_keys=True).encode()).hexdigest()}


def run_candidate(t, n, T0, W, burn, max_reps, max_H, t_start, t_budget):
    """WP-6 STEP PS-04: one periodic candidate, fully incremental.

    Returns dict with outcome in {KILL, STALLED, CAP, TIME} + instrumentation.
    Drift rule: same canonical geometry with component-wise (lat,act) <= stored
    and strictly less ==> record negative-drift cycle, keep repeating.
    Identical (geometry,lat,act) ==> deterministic loop forever ==> STALLED.
    Greater/incomparable ==> re-baseline, keep repeating (caps backstop).
    """
    import time as _t
    st = PAState(n, T0)
    for (m, x) in burn:
        out = st.apply(m, x)
        if out is not None and out["paid"] < out["need"]:
            return {"outcome": "KILL", "where": "burn-in", "H": [list(h) for h in st.H]}
    seen = {}
    drifts = []
    distinct = 0
    reps = 0
    snap = st.snapshot()
    seen[snap["geom"]] = (reps, snap["lat"], snap["act"])
    distinct = 1
    best_drift = 0
    while reps < max_reps and len(st.H) < max_H:
        reps += 1
        for (m, x) in W:
            out = st.apply(m, x)
            if out is not None and out["paid"] < out["need"]:
                return {"outcome": "KILL", "where": "rep-%d" % reps,
                        "H": [list(h) for h in st.H]}
        snap = st.snapshot()
        if snap["geom"] in seen:
            r0, l0, a0 = seen[snap["geom"]]
            l1, a1 = snap["lat"], snap["act"]
            if (l1, a1) == (l0, a0):
                return {"outcome": "STALLED", "reps": reps, "Hlen": len(st.H),
                        "distinct": distinct, "drifts": drifts,
                        "note": "exact (geometry,lat,act) recurrence: deterministic loop"}
            if l1 <= l0 and a1 <= a0:
                d = (l0 - l1) + (a0 - a1)
                best_drift = max(best_drift, d)
                drifts.append({"rep": reps, "lat": (l0, l1), "act": (a0, a1)})
                # keep repeating: exploitation == continuation (kill or stall decides)
            else:
                seen[snap["geom"]] = (reps, l1, a1)
                distinct += 1
        else:
            seen[snap["geom"]] = (reps, snap["lat"], snap["act"])
            distinct += 1
        if reps % 25 == 0:
            step("PS-04", "t=%d rep=%d/%d |H|=%d elapsed=%.1fs states=%d rec=%d drift=%d"
                 % (t, reps, max_reps, len(st.H), _t.perf_counter() - t_start,
                    distinct, len(drifts), best_drift))
        if _t.perf_counter() - t_start > t_budget:
            return {"outcome": "TIME", "reps": reps, "Hlen": len(st.H),
                    "distinct": distinct, "drifts": drifts}
    return {"outcome": "CAP", "reps": reps, "Hlen": len(st.H),
            "distinct": distinct, "drifts": drifts,
            "best_drift": best_drift}


def all_bsts(keys):
    if not keys:
        yield None
        return
    for i, k in enumerate(keys):
        for L in all_bsts(keys[:i]):
            for R in all_bsts(keys[i + 1:]):
                yield [k, L, R]


def exact_word_search(n_list=(2, 3, 4), max_wl=3, max_reps=2000, max_H=12000):
    """WP-6 STEP PS-05: bounded-exhaustive periodic-word search (honest bounds).

    Enumerates: every BST shape T0 over [1..n] x every word W (length<=max_wl
    over all keys x modes) x repetition to kill/stall/cap. Labels bounds
    explicitly; NOT full-state exhaustive (pools unbounded in principle).
    """
    import itertools
    step("PS-05", "Bounded-exhaustive word search n=%s wl<=%d" % (n_list, max_wl))
    tested = kills = 0
    for n in n_list:
        shapes = list(all_bsts(list(range(1, n + 1))))
        steps = [["KEEP", x] for x in range(1, n + 1)] + \
            [["DELETE", x] for x in range(1, n + 1)]
        for T0 in shapes:
            for wl in range(1, max_wl + 1):
                for Wt in itertools.product(steps, repeat=wl):
                    W = [list(h) for h in Wt]
                    tested += 1
                    st = PAState(n, T0)
                    seen = {}
                    rep = 0
                    dead = False
                    while rep < max_reps and len(st.H) < max_H:
                        rep += 1
                        for (m, x) in W:
                            out = st.apply(m, x)
                            if out is not None and out["paid"] < out["need"]:
                                dead = True
                                break
                        if dead:
                            break
                        snap = st.snapshot()
                        if snap["geom"] in seen and seen[snap["geom"]] == \
                                (snap["lat"], snap["act"]):
                            break  # exact recurrence: stalls forever
                        seen[snap["geom"]] = (snap["lat"], snap["act"])
                    if dead:
                        wit = confirm_kill(n, T0, [list(h) for h in st.H])
                        kills += 1
                        step("PS-05", "EXACT-WORD KILL n=%d" % n)
                        return {"tested": tested, "kills": kills, "witness": wit}
    step("PS-05", "exact-word search done: tested=%d kills=%d" % (tested, kills))
    return {"tested": tested, "kills": kills}


def main() -> int:
    import sys as _s
    cmd = _s.argv[1] if len(_s.argv) > 1 else "help"
    if cmd == "xcheck":
        # WP-6 STEP PS-06: cross-check gate (must pass before any search).
        step("PS-06", "Running cross-check gate")
        return 0 if cross_check(200) else 2
    if cmd == "exact":
        out = exact_word_search()
        (NS / "exact_word_summary.json").parent.mkdir(parents=True, exist_ok=True)
        (NS / "exact_word_summary.json").write_text(
            json.dumps(out, indent=2, sort_keys=True,
                       default=lambda o: None if o is None else o), encoding="utf-8")
        return 0
    if cmd in ("profile1", "profile10", "full"):
        import hashlib as _h

        class DRBG:
            def __init__(self, s): self.s = s; self.c = 0

            def b(self):
                self.c += 1
                return _h.sha256(b"pw|%s|%d" % (self.s, self.c)).digest()

            def below(self, n):
                bound = (1 << 256) - ((1 << 256) % n)
                while True:
                    v = int.from_bytes(self.b(), "big")
                    if v < bound:
                        return v % n

            def ir(self, a, b): return a + self.below(b - a + 1)

            def ch(self, s): return s[self.below(len(s))]

        def vine(nn, left=False):
            t = None
            for k in (range(nn, 0, -1) if not left else range(1, nn + 1)):
                t = [k, None, t] if not left else [k, t, None]
            return t

        def balanced(keys):
            if not keys:
                return None
            m = len(keys) // 2
            return [keys[m], balanced(keys[:m]), balanced(keys[m + 1:])]

        count = {"profile1": 1, "profile10": 10, "full": 300}[cmd]
        results, wit = run_stream(count, DRBG, vine, balanced)
        out = {"mode": cmd, "candidates": len(results),
               "total_s": results[-1].pop("_total_s", 0.0) if results else 0.0,
               "outcomes": [{k: v for k, v in r.items() if k != "H"}
                            for r in results]}
        if wit is not None:
            (NS / "periodic_witness.json").parent.mkdir(parents=True, exist_ok=True)
            (NS / "periodic_witness.json").write_text(
                json.dumps(wit, indent=2, sort_keys=True), encoding="utf-8")
        (NS / ("periodic_%s.json" % cmd)).parent.mkdir(parents=True, exist_ok=True)
        (NS / ("periodic_%s.json" % cmd)).write_text(
            json.dumps(out, indent=2, sort_keys=True,
                       default=lambda o: None if o is None else str(o)),
            encoding="utf-8")
        step("PS-99", "%s done: %d candidates" % (cmd, len(results)))
        return 0
    print("usage: xcheck | exact | profile1 | profile10 | full")
    return 2


def run_stream(count, DRBG, vine, balanced):
    """WP-6 STEP PS-07: instrumented stream of periodic candidates.

    Returns (results, witness_or_None). Present-only by construction
    (vine/balanced T0 over full [1..n]; keys drawn from [1..n]).
    """
    import time as _t
    results = []
    wit = None
    t_all = _t.perf_counter()
    for t in range(count):
        rng = DRBG(("pw%d" % t).encode())
        n = rng.ch([16, 32, 64])
        T0 = vine(n, rng.below(2) == 0)
        wl = rng.ir(1, 4)
        W = [[rng.ch(["KEEP", "DELETE"]), rng.ir(1, n)] for _ in range(wl)]
        burn = [[rng.ch(["KEEP", "DELETE"]), rng.ir(1, n)]
                for _ in range(rng.ir(0, 3))]
        t0 = _t.perf_counter()
        step("PS-07", "candidate t=%d n=%d wl=%d burn=%d" % (t, n, wl, len(burn)))
        r = run_candidate(t, n, T0, W, burn, 1500, 12000, t0, 3600.0)
        r.update({"t": t, "n": n, "wl": wl,
                  "elapsed": _t.perf_counter() - t0})
        step("PS-07", "t=%d outcome=%s reps=%s elapsed=%.1fs" %
             (t, r["outcome"], r.get("reps"), r["elapsed"]))
        results.append(r)
        if r["outcome"] == "KILL":
            wit = confirm_kill(n, T0, r["H"])
            break
    if results:
        results[-1]["_total_s"] = _t.perf_counter() - t_all
    return results, wit


if __name__ == "__main__":
    sys.exit(main())

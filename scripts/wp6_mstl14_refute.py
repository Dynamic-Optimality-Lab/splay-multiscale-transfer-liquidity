"""WP-6 STEP: MSTL-14 REFUTE war for candidate P_all|6|2|FLAT(2) (0909c74a).

Attacks the exact negation (exists legal reachable KEEP with paid<need) over
arbitrary n / unbounded history length using the EXACT frozen candidate
calculus (solver.encode primary; independent.config_exec confirmation).
Families: sanity (REG-001, n192), vine drain-then-diverge, range-walk drains,
DELETE bursts, nested intervals, alternating, high-discharge chains,
deep-node asymmetry, long histories, REG-001/n192 mutations, greedy
negation-driven hill-climb. Deterministic seeds. Any kill is independently
replayed, greedily minimized, hashed, and frozen as a refutation certificate;
the candidate is NEVER mutated. Zero kills => ATTACKED-NOT-REFUTED (not proof).
"""
from __future__ import annotations
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from solver import encode as E
from independent import config_exec as IX

P, K, C, RHO = "P_all", 6, 2, (2, 2)
NS = ROOT / "artifacts" / "v04" / "wp6" / "0909c74a" / "refute"
BIND = {"candidate": "P_all|6|2|FLAT(2)", "P": P, "k": K, "C": C, "rho": "FLAT(2)",
        "identity_hash": "0909c74accb193302d1a9213601567bebcba414de679e362b10ad3007b4fb7fd"}


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


def w(p: Path, obj) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, indent=2, sort_keys=True), encoding="utf-8")
    tmp.replace(p)


def vine_right(n):
    t = None
    for k in range(n, 0, -1):
        t = [k, None, t]
    return t


def vine_left(n):
    t = None
    for k in range(1, n + 1):
        t = [k, t, None]
    return t


def balanced(keys):
    if not keys:
        return None
    m = len(keys) // 2
    return [keys[m], balanced(keys[:m]), balanced(keys[m + 1:])]


class DRBG:
    def __init__(self, stream: bytes):
        self.seed, self.stream, self.ctr = b"wp6-mstl14-refute", stream, 0

    def _block(self) -> bytes:
        self.ctr += 1
        return hashlib.sha256(self.seed + b"|" + self.stream + b"|"
                              + self.ctr.to_bytes(8, "big")).digest()

    def below(self, n: int) -> int:
        bound = (1 << 256) - ((1 << 256) % n)
        while True:
            v = int.from_bytes(self._block(), "big")
            if v < bound:
                return v % n

    def irange(self, lo: int, hi: int) -> int:
        return lo + self.below(hi - lo + 1)

    def choice(self, seq):
        return seq[self.below(len(seq))]


def run_case(eid, n, T0, H, fam):
    pre = E.precompute(n, T0, H)
    r = E.exec_counts(pre, P, K, C, RHO)
    if r["violations"]:
        ind = IX.replay(n, T0, H, P, K, C, RHO)
        r1 = [(x["need"], x["paid"]) for x in r["keeps"]]
        r2 = [(x["need"], x["paid"]) for x in ind["keeps"]]
        assert r1 == r2 and ind["violations"] > 0, "kill failed independent confirm"
        first = next(i for i, x in enumerate(r["keeps"]) if x["paid"] < x["need"])
        return {"eid": eid, "family": fam, "n": n, "T0": T0, "H": H,
                "binding": BIND, "keep_idx": r["keeps"][first]["idx"],
                "need": r["keeps"][first]["need"], "paid": r["keeps"][first]["paid"],
                "margin": r["keeps"][first]["margin"],
                "worst": max(x["need"] - x["paid"] for x in r["keeps"]),
                "independent_agree": True}
    return None


def minimize(kill):
    # WP-6 STEP RF-02: greedy history shrink preserving the exact kill.
    H, n, T0 = list(kill["H"]), kill["n"], kill["T0"]
    improved = True
    while improved:
        improved = False
        for i in range(len(H)):
            trial = H[:i] + H[i + 1:]
            if not trial or not any(m == "KEEP" for m, _ in trial):
                continue
            try:
                r = E.exec_counts(E.precompute(n, T0, trial), P, K, C, RHO)
            except Exception:
                continue
            if r["violations"]:
                H = trial
                improved = True
                break
    kill["H_min"] = H
    kill["min_level"] = "L1-greedy-shrink"
    return kill


def main() -> int:
    step("RF-00", "MSTL-14 REFUTE war: P_all|6|2|FLAT(2), exact frozen calculus")
    kills, tested, worst_margin = [], 0, 0

    def fire(eid, n, T0, H, fam):
        nonlocal tested, worst_margin
        k = run_case(eid, n, T0, H, fam)
        tested += 1
        if k:
            kills.append(minimize(k))
            step("RF-KILL", "%s killed by %s need=%d paid=%d" % (k["eid"], fam, k["need"], k["paid"]))
        return k

    # WP-6 STEP RF-01: sanity — known killers must be survived (calculus check).
    step("RF-01", "Sanity: REG-001 + n192 must be survived")
    fire("REG-001", 28, vine_right(28),
         [["DELETE", 27], ["DELETE", 28], ["KEEP", 28], ["KEEP", 27]], "sanity")
    ce = json.loads((ROOT / "artifacts" / "v04" / "counterexamples" / "ce_0000.json")
                    .read_text(encoding="utf-8"))["episode"]
    fire("n192", ce["n"], ce["T0"], ce["H"], "sanity")
    assert not kills, "sanity failure: frozen calculus drift"

    # WP-6 STEP RF-10: vine drain-then-diverge sweeps (A/B divergence -> big need).
    step("RF-10", "Vine drain-then-diverge sweeps")
    for n in (28, 64, 128, 256, 512, 1024, 2048):
        for div in range(0, min(n, 8)):
            x = n - div
            H = [["DELETE", max(1, n - 2 * div - i)] for i in range(min(div + 1, 6))]
            H += [["KEEP", min(n, x + d)] for d in (6, 2, 0)]
            fire("vine-div-%d-%d" % (n, div), n, vine_right(n), H, "vine-diverge")
            if kills:
                break
        if kills:
            break

    # WP-6 STEP RF-11: long range-walk drains (L 9..64, beyond battery max 8).
    step("RF-11", "Long range-walk drains")
    for (n, L, tag) in ((192, 24, "w24"), (192, 48, "w48"), (384, 32, "w32"),
                        (96, 64, "w64"), (512, 40, "w40")):
        rng = DRBG(("walk|%d|%d" % (n, L)).encode())
        x = rng.irange(1, n)
        H = []
        for _ in range(L):
            H.append([rng.choice(["KEEP", "DELETE"]), x])
            x = min(n, max(1, x + rng.choice([-16, -8, -4, -1, 1, 4, 8, 16])))
        T0 = vine_right(n) if tag != "w32" else vine_left(n)
        fire("walk-%s" % tag, n, T0, H, "range-walk")
        if kills:
            break

    # WP-6 STEP RF-12: DELETE bursts then KEEP (extended lengths).
    step("RF-12", "DELETE bursts before KEEP")
    for n in (64, 192, 512):
        for d in (1, 3, 7, 15, 31):
            rng = DRBG(("burst|%d|%d" % (n, d)).encode())
            H = [["DELETE", rng.irange(1, n)] for _ in range(d)]
            H += [["KEEP", rng.irange(1, n)] for _ in range(4)]
            fire("burst-%d-%d" % (n, d), n, vine_right(n), H, "delete-burst")
            if kills:
                break
        if kills:
            break

    # WP-6 STEP RF-13: nested-interval + alternating long histories.
    step("RF-13", "Nested-interval / alternating long histories")
    for n in (64, 256):
        c = n // 2
        H = []
        for i in range(24):
            H.append([["KEEP", "DELETE"][i % 2], min(n, max(1, c + (i // 2) * (1 if i % 4 < 2 else -1)))])
        fire("nested-%d" % n, n, balanced(list(range(1, n + 1))), H, "nested")
        if kills:
            break

    # WP-6 STEP RF-14: high prior-discharge chains (drain ACTIVE, then big need).
    step("RF-14", "High prior-discharge chains")
    for n in (128, 384):
        rng = DRBG(("drain|%d" % n).encode())
        H = []
        x = rng.irange(1, n)
        for _ in range(20):
            H.append(["KEEP", x])
            x = min(n, max(1, x + rng.choice([-32, -16, 16, 32])))
        H.append(["KEEP", rng.irange(1, n)])
        fire("discharge-%d" % n, n, vine_right(n), H, "discharge-chain")
        if kills:
            break

    # WP-6 STEP RF-15: REG-001 / n192 mutations and generalizations.
    step("RF-15", "REG-001/n192 mutations")
    for n in (28, 29, 56, 112):
        fire("regmut-%d" % n, n, vine_right(n),
             [["DELETE", n - 1], ["DELETE", n], ["KEEP", n], ["KEEP", n - 1]], "reg-mut")
        fire("regmutL-%d" % n, n, vine_left(n),
             [["DELETE", 1], ["DELETE", 2], ["KEEP", 2], ["KEEP", 1]], "reg-mut")
        if kills:
            break
    if not kills:
        for dn in (-64, -32, -16, 16, 32, 64):
            n = 192
            H = [["DELETE", 129], ["KEEP", min(n, max(1, 134 + dn))],
                 ["KEEP", min(n, max(1, 130 + dn))], ["KEEP", 129]]
            fire("n192mut-%d" % dn, n, vine_right(n), H, "n192-mut")
            if kills:
                break

    # WP-6 STEP RF-16: greedy negation-driven hill-climb on margin deficit.
    step("RF-16", "Negation-driven hill-climb (minimize margin)")
    if not kills:
        rng = DRBG(b"hill|192")
        n = 192
        H = [["DELETE", 129], ["KEEP", 134], ["KEEP", 130], ["KEEP", 129]]
        best = min(x["paid"] - x["need"] for x in
                   E.exec_counts(E.precompute(n, vine_right(n), H), P, K, C, RHO)["keeps"])
        for it in range(400):
            i = rng.below(len(H))
            old = H[i]
            H[i] = [rng.choice(["KEEP", "DELETE"]), rng.irange(1, n)]
            try:
                r = E.exec_counts(E.precompute(n, vine_right(n), H), P, K, C, RHO)
            except Exception:
                H[i] = old
                continue
            m = min(x["paid"] - x["need"] for x in r["keeps"]) if r["keeps"] else 0
            if r["violations"]:
                fire("hill-%d" % it, n, vine_right(n), [list(h) for h in H], "hill-climb")
                break
            if m < best:
                best = m
            else:
                H[i] = old
        step("RF-16", "hill-climb best margin=%d (kills=%d)" % (best, len(kills)))

    # WP-6 STEP RF-20: randomized A/B-divergence battery (maximize y-2a).
    step("RF-20", "Randomized A/B-divergence battery (6000 episodes)")
    if not kills:
        for t in range(6000):
            rng = DRBG(("div|%d" % t).encode())
            n = rng.choice([16, 24, 32, 48, 64, 96, 128, 192, 256, 384, 512, 768,
                            1024, 1536, 2048])
            T0 = rng.choice([vine_right(n), vine_left(n),
                             balanced(list(range(1, n + 1)))])
            tgt = rng.irange(1, n)
            H = []
            for _ in range(rng.irange(1, 12)):
                x = rng.irange(1, n)
                if abs(x - tgt) > n // 4:
                    H.append(["DELETE", x])
                else:
                    H.append([rng.choice(["KEEP", "DELETE"]), x])
            for _ in range(rng.irange(1, 4)):
                H.append(["KEEP", tgt])
            fire("div-%d" % t, n, T0, H, "ab-divergence")
            if kills or (t + 1) % 2000 == 0:
                step("RF-20", "progress %d/6000 (kills=%d)" % (t + 1, len(kills)))
            if kills:
                break

    # WP-6 STEP RF-21: extreme-length histories (L up to 256).
    step("RF-21", "Extreme-length histories (2000 episodes)")
    if not kills:
        for t in range(2000):
            rng = DRBG(("long|%d" % t).encode())
            n = rng.choice([64, 128, 192, 384, 768])
            T0 = rng.choice([vine_right(n), vine_left(n)])
            L = rng.irange(64, 256)
            x = rng.irange(1, n)
            H = []
            for _ in range(L):
                H.append([rng.choice(["KEEP", "DELETE"]), x])
                x = min(n, max(1, x + rng.choice([-32, -16, -8, -4, -1, 1, 4, 8, 16, 32])))
            fire("long-%d" % t, n, T0, H, "extreme-length")
            if kills or (t + 1) % 1000 == 0:
                step("RF-21", "progress %d/2000 (kills=%d)" % (t + 1, len(kills)))
            if kills:
                break

    out = {"binding": BIND, "node": "MSTL-14", "negation": "exists legal KEEP with paid<need",
           "tested": tested, "kills": len(kills),
           "verdict": "CANDIDATE_REFUTED_AT_MSTL-14" if kills else "ATTACKED-NOT-REFUTED",
           "note": "Zero kills is not a proof; it only records that this budgeted "
                   "attack found no exact witness." if not kills else
                   "Exact witness frozen; candidate retired without mutation."}
    w(NS / "refute_summary.json", out)
    if kills:
        w(NS / "refutation_witness.json", kills[0])
    step("RF-99", "REFUTE done: tested=%d kills=%d verdict=%s" % (tested, len(kills), out["verdict"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())

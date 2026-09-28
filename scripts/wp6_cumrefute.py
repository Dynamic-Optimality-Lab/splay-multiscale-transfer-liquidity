"""WP-6 STEP: direct cumulative-lemma refuter (P_all|6|2|FLAT(2)).

Maximizes R = sum(need) - 6*S_A over legal histories, where S_A(j) is the
cumulative count of sited A-events through KEEP j's A-phase (inclusive) and
sum(need) is over KEEPs i<=j. R > 0 at any KEEP is a lemma violation.
Tracks: small-n exhaustive (n=2,3,4 over all short histories/T0 shapes),
structured vines/mirrors/alternating/diverge families, and greedy hill-climb
on R. Any R>0 witness is preserved with full content; disposition (lemma-only
vs MSTL-14 refutation) is decided by checking ACTIVE>=need on the same trace.
"""
from __future__ import annotations
import hashlib
import itertools
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from solver import encode as E

P, K, C, RHO = "P_all", 6, 2, (2, 2)
NS = ROOT / "artifacts" / "v04" / "wp6" / "0909c74a" / "cumrefute"
BIND = {"candidate": "P_all|6|2|FLAT(2)", "identity_hash":
        "0909c74accb193302d1a9213601567bebcba414de679e362b10ad3007b4fb7fd"}


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


def R_of(n, T0, H):
    """Max over KEEPs j of (sum_{i<=j} need_i - 6*S_A(j)); plus ACTIVE check.

    S_A(j) counts sited A-events over ALL accesses 1..j inclusive of j's
    A-phase (DELETE accesses inject LATENT too and must be counted).
    """
    pre = E.precompute(n, T0, H)
    r = E.exec_counts(pre, P, K, C, RHO)
    keeps = iter(r["keeps"])
    best, cum_need, cum_sa, detail = -10 ** 18, 0, 0, None
    for acc in pre:
        cum_sa += sum(1 for s in acc["sites"] if s)
        if acc["mode"] != "KEEP":
            continue
        kp = next(keeps)
        cum_need += kp["need"]
        val = cum_need - 6 * cum_sa
        if val > best:
            best = val
            detail = {"x": acc["x"], "a": acc["a"], "y": acc["y"], "need": kp["need"],
                      "paid": kp["paid"], "margin": kp["margin"], "cum_need": cum_need,
                      "cum_SA": cum_sa, "R": val}
    return best, detail, r["violations"]


def all_bsts(keys):
    if not keys:
        yield None
        return
    for i, k in enumerate(keys):
        for L in all_bsts(keys[:i]):
            for R in all_bsts(keys[i + 1:]):
                yield [k, L, R]


def main() -> int:
    # WP-6 STEP CR-00: direct cumulative refutation.
    step("CR-00", "Maximizing R = sum(need) - 6*S_A")
    best, best_case, tested, lemma_kills, mstl_kills = -10 ** 18, None, 0, [], []

    def fire(n, T0, H, fam):
        nonlocal best, best_case, tested
        v, detail, viol = R_of(n, T0, H)
        tested += 1
        if v > best:
            best, best_case = v, {"fam": fam, "n": n, "T0": T0, "H": H, "at": detail}
        if v > 0:
            rec = {"fam": fam, "n": n, "T0": T0, "H": H, "at": detail,
                   "mstl_viol": viol, "binding": BIND}
            lemma_kills.append(rec)
            if viol:
                mstl_kills.append(rec)
                step("CR-KILL", "MSTL-14 violated by %s R=%d" % (fam, v))
            else:
                step("CR-LEMMAKILL", "lemma-only violation by %s R=%d" % (fam, v))
        return v

    # WP-6 STEP CR-01: small-n exhaustive.
    step("CR-01", "Small-n exhaustive (n=2,3,4)")
    for n, Lmax in ((2, 7), (3, 5), (4, 4)):
        shapes = list(all_bsts(list(range(1, n + 1))))
        steps = [["KEEP", x] for x in range(1, n + 1)] + \
            [["DELETE", x] for x in range(1, n + 1)]
        count = 0
        for L in range(1, Lmax + 1):
            for H in itertools.product(steps, repeat=L):
                H = [list(h) for h in H]
                if not any(m == "KEEP" for m, _ in H):
                    continue
                for T0 in shapes:
                    fire(n, T0, H, "exhaustive-n%d" % n)
                    count += 1
                    if mstl_kills:
                        break
                if mstl_kills:
                    break
            if mstl_kills:
                break
        step("CR-01", "n=%d: %d histories x %d shapes tested" % (n, count, len(shapes)))
        if mstl_kills:
            break

    # WP-6 STEP CR-02: structured + mirror + extreme + hill-climb on R.
    step("CR-02", "Structured families maximizing R")
    def vine(n, left=False):
        t = None
        rng = range(n, 0, -1) if not left else range(1, n + 1)
        for k in rng:
            t = [k, None, t] if not left else [k, t, None]
        return t

    import hashlib as _h

    class DRBG:
        def __init__(self, s): self.s = s; self.c = 0
        def b(self):
            self.c += 1
            return _h.sha256(b"cum|%s|%d" % (self.s, self.c)).digest()
        def below(self, n):
            bound = (1 << 256) - ((1 << 256) % n)
            while True:
                v = int.from_bytes(self.b(), "big")
                if v < bound:
                    return v % n
        def ir(self, a, b): return a + self.below(b - a + 1)
        def ch(self, s): return s[self.below(len(s))]

    for t in range(4000):
        rng = DRBG(("s%d" % t).encode())
        n = rng.ch([8, 16, 28, 48, 96, 192, 384])
        T0 = rng.ch([vine(n), vine(n, True)])
        L = rng.ir(2, 24)
        x = rng.ir(1, n)
        H = []
        for _ in range(L):
            H.append([rng.ch(["KEEP", "DELETE"]), x])
            x = min(n, max(1, x + rng.ch([-16, -8, -4, -1, 1, 4, 8, 16])))
        fire(n, T0, H, "struct-walk")
        if mstl_kills:
            break
    # hill-climb on R at n=192 vine.
    step("CR-03", "Hill-climb on R")
    if not mstl_kills:
        rng = DRBG(b"hillR")
        n, T0 = 192, vine(192)
        H = [["DELETE", 129], ["KEEP", 134], ["KEEP", 130], ["KEEP", 129]]
        cur, _, _ = R_of(n, T0, H)
        for it in range(1500):
            op = rng.below(10)
            if op == 0 and len(H) < 16:
                i = rng.below(len(H) + 1)
                H.insert(i, [rng.ch(["KEEP", "DELETE"]), rng.ir(1, n)])
                undo = ("del", i)
            elif op == 1 and len(H) > 2:
                i = rng.below(len(H))
                old = H.pop(i)
                undo = ("ins", i, old)
            else:
                i = rng.below(len(H))
                old = H[i]
                H[i] = [rng.ch(["KEEP", "DELETE"]), rng.ir(1, n)]
                undo = ("set", i, old)
            try:
                v, _, viol = R_of(n, T0, H)
            except Exception:
                v = cur - 1
            if v > cur:
                cur = v
                if v > 0:
                    fire(n, T0, [list(h) for h in H], "hill-R")
                    if mstl_kills:
                        break
            else:
                if undo[0] == "del":
                    H.pop(undo[1])
                elif undo[0] == "ins":
                    H.insert(undo[1], undo[2])
                else:
                    H[undo[1]] = undo[2]
        step("CR-03", "hill-climb best R=%d" % cur)

    out = {"binding": BIND, "tested": tested, "best_R": best,
           "lemma_kills": len(lemma_kills), "mstl_kills": len(mstl_kills),
           "verdict": "MSTL-14-REFUTED" if mstl_kills else
                      ("LEMMA-REFUTED-MSTL-OPEN" if lemma_kills else "LEMMA-HOLDS-TESTED")}
    NS.mkdir(parents=True, exist_ok=True)
    # WP-6 STEP CR-98: stale outputs from prior runs must never contradict current results.
    step("CR-98", "Clearing stale outputs from prior runs")
    if not lemma_kills:
        stale = NS / "lemma_witness.json"
        if stale.exists():
            stale.unlink()
    (NS / "cumrefute_summary.json").write_text(json.dumps(out, indent=2, sort_keys=True),
                                               encoding="utf-8")
    if lemma_kills:
        (NS / "lemma_witness.json").write_text(json.dumps(lemma_kills[0], indent=2,
                                                          sort_keys=True), encoding="utf-8")
    if best_case and best > -10 ** 17:
        (NS / "best_R_case.json").write_text(json.dumps(best_case, indent=2, sort_keys=True),
                                             encoding="utf-8")
    step("CR-99", "done: tested=%d best_R=%d lemma_kills=%d mstl_kills=%d" %
         (tested, best, len(lemma_kills), len(mstl_kills)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

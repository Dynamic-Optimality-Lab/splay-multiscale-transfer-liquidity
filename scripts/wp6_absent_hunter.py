"""WP-6 STEP: targeted absent-kill hunter (fitness = need - ACTIVE_pre).

Hill-climbs (history, absent key) to maximize need(z) - ACTIVE_pre at an
appended absent KEEP. Fitness > 0 IS an exact MSTL-14 kill (paid<need).
Also sweeps post-KEEP absent needs to map the corner's shape.
"""
from __future__ import annotations
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from solver import encode as E
from solver import legality as LG
from independent import config_exec as IX

P, K, C, RHO = "P_all", 6, 2, (2, 2)
NS = ROOT / "artifacts" / "v04" / "wp6" / "0909c74a" / "refute_absent2"
BIND = {"candidate": "P_all|6|2|FLAT(2)", "identity_hash":
        "0909c74accb193302d1a9213601567bebcba414de679e362b10ad3007b4fb7fd"}


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


def bst(keys):
    if not keys:
        return None
    m = len(keys) // 2
    return [keys[m], bst(keys[:m]), bst(keys[m + 1:])]


class DRBG:
    def __init__(self, s): self.s = s; self.c = 0

    def b(self):
        self.c += 1
        return hashlib.sha256(b"ak|%s|%d" % (self.s, self.c)).digest()

    def below(self, n):
        bound = (1 << 256) - ((1 << 256) % n)
        while True:
            v = int.from_bytes(self.b(), "big")
            if v < bound:
                return v % n

    def ir(self, a, b): return a + self.below(b - a + 1)

    def ch(self, s): return s[self.below(len(s))]


def fitness(n, T0, H, z):
    """need(z) - ACTIVE_pre at appended absent KEEP z. >0 kills."""
    H2 = H + [["KEEP", z]]
    LG.check(n, T0, H2)
    pre = E.precompute(n, T0, H2)
    r = E.exec_counts(pre, P, K, C, RHO)
    last = r["keeps"][-1]
    # ACTIVE_pre = paid + leftover; margin = act_post + paid - need
    active_pre = last["paid"] + (last["margin"] + last["need"] - last["paid"])
    return last["need"] - active_pre, (last["need"], last["paid"], r["violations"])


def main() -> int:
    # WP-6 STEP AK-00: fitness hill-climb for absent kills.
    step("AK-00", "Hill-climbing need-ACTIVE_pre at appended absent KEEPs")
    best, best_cfg, kills, tested = -10 ** 18, None, [], 0
    for seed in (b"Q1", b"Q2", b"Q3"):
        rng = DRBG(seed)
        n = rng.ch([32, 64, 128])
        ks = list(range(1, n + 1))
        keep = sorted([k for k in ks if rng.below(2) == 0]) or [1]
        absent = [k for k in ks if k not in keep]
        if not absent:
            continue
        T0 = bst(keep)
        H = [[rng.ch(["KEEP", "DELETE"]), rng.ch(keep)] for _ in range(6)]
        z = rng.ch(absent)
        cur, _ = fitness(n, T0, H, z)
        for it in range(4000):
            op = rng.below(12)
            old_H, old_z = [list(h) for h in H], z
            if op == 0 and len(H) < 20:
                H.insert(rng.below(len(H) + 1),
                         [rng.ch(["KEEP", "DELETE"]), rng.ch(ks)])
            elif op == 1 and len(H) > 2:
                H.pop(rng.below(len(H)))
            elif op == 2:
                z = rng.ch(absent)
            else:
                i = rng.below(len(H))
                H[i] = [rng.ch(["KEEP", "DELETE"]), rng.ch(ks)]
            try:
                v, info = fitness(n, T0, H, z)
            except Exception:
                v = cur - 1
                info = None
            tested += 1
            if info and info[2]:
                ind = IX.replay(n, T0, H + [["KEEP", z]], P, K, C, RHO)
                assert ind["violations"] > 0
                kills.append({"n": n, "T0": T0, "H": H + [["KEEP", z]],
                              "binding": BIND, "need": info[0], "paid": info[1],
                              "independent_agree": True})
                step("AK-KILL", "absent kill seed=%s it=%d need=%d paid=%d"
                     % (seed, it, info[0], info[1]))
                break
            if v > cur:
                cur = v
            else:
                H, z = old_H, old_z
        if cur > best:
            best, best_cfg = cur, (seed, n, len(H))
        step("AK-01", "seed=%s best fitness=%d" % (seed, cur))
        if kills:
            break
    out = {"binding": BIND, "tested": tested, "best_fitness": best,
           "kills": len(kills),
           "verdict": "CANDIDATE_REFUTED_AT_MSTL-14" if kills else "ATTACKED-NOT-REFUTED"}
    NS.mkdir(parents=True, exist_ok=True)
    (NS / "absent2_summary.json").write_text(json.dumps(out, indent=2, sort_keys=True),
                                             encoding="utf-8")
    if kills:
        (NS / "absent2_witness.json").write_text(json.dumps(kills[0], indent=2, sort_keys=True),
                                                 encoding="utf-8")
    step("AK-99", "done: tested=%d best=%d kills=%d" % (tested, best, len(kills)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

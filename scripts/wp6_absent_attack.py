"""WP-6 STEP: absent-key attack (sparse T0 + absent accesses + drain phases).

Legality permits keys(T0) subset [n] and presence NOT required. All frozen
batteries use full key sets, so this corner was never attacked. A kill here
is an exact MSTL-14 refutation (independently confirmed); zero kills extend
REFUTE coverage to the sparse/absent corner.
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
NS = ROOT / "artifacts" / "v04" / "wp6" / "0909c74a" / "refute_absent"
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
        return hashlib.sha256(b"ab|%s|%d" % (self.s, self.c)).digest()

    def below(self, n):
        bound = (1 << 256) - ((1 << 256) % n)
        while True:
            v = int.from_bytes(self.b(), "big")
            if v < bound:
                return v % n

    def ir(self, a, b): return a + self.below(b - a + 1)

    def ch(self, s): return s[self.below(len(s))]


def main() -> int:
    # WP-6 STEP AB-00: sparse-T0 absent-key attack.
    step("AB-00", "Absent-key attack: sparse T0, drain phases, absent KEEPs")
    kills, tested = [], 0
    for t in range(6000):
        rng = DRBG(("ab%d" % t).encode())
        n = rng.ir(8, 64)
        ks = list(range(1, n + 1))
        keep = [k for k in ks if (hashlib.sha256(("s%d|%d" % (t, k)).encode()).digest()[0] % 3) != 0]
        if not keep:
            keep = [1]
        absent = [k for k in ks if k not in keep]
        if not absent:
            continue
        T0 = bst(keep)
        L = rng.ir(2, 12)
        H = []
        for _ in range(L):
            # bias toward absent KEEPs after a drain prefix of present accesses
            if len(H) >= 2 and rng.below(2) == 0:
                H.append([rng.ch(["KEEP", "DELETE"]), rng.ch(absent)])
            else:
                H.append([rng.ch(["KEEP", "DELETE"]), rng.ch(ks)])
        LG.check(n, T0, H)
        pre = E.precompute(n, T0, H)
        r = E.exec_counts(pre, P, K, C, RHO)
        tested += 1
        if r["violations"]:
            ind = IX.replay(n, T0, H, P, K, C, RHO)
            r1 = [(x["need"], x["paid"]) for x in r["keeps"]]
            r2 = [(x["need"], x["paid"]) for x in ind["keeps"]]
            assert r1 == r2 and ind["violations"] > 0
            first = next(i for i, x in enumerate(r["keeps"]) if x["paid"] < x["need"])
            kills.append({"t": t, "n": n, "T0": T0, "H": H, "binding": BIND,
                          "need": r["keeps"][first]["need"],
                          "paid": r["keeps"][first]["paid"],
                          "independent_agree": True})
            step("AB-KILL", "absent-corner kill t=%d need=%d paid=%d"
                 % (t, r["keeps"][first]["need"], r["keeps"][first]["paid"]))
            if len(kills) >= 3:
                break
    out = {"binding": BIND, "tested": tested, "kills": len(kills),
           "verdict": "CANDIDATE_REFUTED_AT_MSTL-14" if kills else "ATTACKED-NOT-REFUTED"}
    NS.mkdir(parents=True, exist_ok=True)
    (NS / "absent_summary.json").write_text(json.dumps(out, indent=2, sort_keys=True),
                                            encoding="utf-8")
    if kills:
        (NS / "absent_witness.json").write_text(json.dumps(kills[0], indent=2, sort_keys=True),
                                                encoding="utf-8")
    step("AB-99", "absent attack done: tested=%d kills=%d" % (tested, len(kills)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

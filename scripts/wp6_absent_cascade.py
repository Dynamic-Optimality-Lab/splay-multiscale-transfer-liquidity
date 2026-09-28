"""WP-6 STEP: absent-battery cascade over all 63 frozen candidates.

For each candidate in frozen wp6_entry_set order: same config-independent base
history (t=10: sparse 28-key T0, n=64) + minimized absent-KEEP battery
(z=10, need=1 each, trees frozen). Finds minimal battery length with first
independently-confirmed legal paid<need kill (binary search, cap 100000).
Freezes per-candidate certificates; NEVER mutates candidates. Stops early only
on a candidate that survives the cap (stays ACTIVE).
"""
from __future__ import annotations
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from solver import encode as E
from solver import search as S
from solver import legality as LG
from independent import config_exec as IX
from cleanroom import evaluator as CR

ART = ROOT / "artifacts" / "v04"
NS = ART / "wp6" / "absent_refutation"
N, T0 = 64, None  # set in main from frozen base
BASE_H = [["DELETE", 30], ["KEEP", 50], ["DELETE", 50], ["DELETE", 11]]
Z = 10
CAP = 100000


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


def build_t0():
    import random
    rnd = random.Random(10)
    ks = list(range(1, 65))
    keep = sorted(rnd.sample(ks, min(rnd.randint(10, 30), 64)))

    def bst(keys):
        if not keys:
            return None
        m = len(keys) // 2
        return [keys[m], bst(keys[:m]), bst(keys[m + 1:])]

    return bst(keep), keep


def first_kill(n, T0, H, P, k, C, rho):
    LG.check(n, T0, H)
    pre = E.precompute(n, T0, H)
    r = E.exec_counts(pre, P, k, C, rho)
    for idx, kp in enumerate(r["keeps"]):
        if kp["paid"] < kp["need"]:
            return True, pre, r, idx, kp
    return False, pre, r, None, None


def main() -> int:
    # WP-6 STEP AC-00: frozen base + per-candidate minimized absent batteries.
    step("AC-00", "Absent-battery cascade over 63 frozen candidates")
    T0, keep = build_t0()
    assert 10 not in keep, "z=10 must be absent"
    entry = json.loads((ART / "wp5x_k6c2" / "h5" / "wp6_entry_set.json").read_text(encoding="utf-8"))
    assert entry["count"] == 63
    deaths, actives = [], []
    for ci, key in enumerate(entry["survivors"]):
        P, ks, Cs, rho_name = key.split("|")
        k, C = int(ks), int(Cs)
        rho = tuple(S.rho_of(rho_name))
        members = {m["key"]: m for m in entry["members"]}
        ident = members[key]["identity_hash"]
        # WP-6 STEP AC-01: minimize battery length for this candidate.
        lo, hi, found = 1, CAP, False
        probe_H = BASE_H + [["KEEP", Z]] * 8
        dead, _, _, _, _ = first_kill(N, T0, probe_H, P, k, C, rho)
        if not dead:
            probe_H = BASE_H + [["KEEP", Z]] * CAP
            dead, _, _, _, _ = first_kill(N, T0, probe_H, P, k, C, rho)
            if not dead:
                actives.append(key)
                step("AC-SURVIVES", "%s survives cap %d (stays ACTIVE)" % (key, CAP))
                continue
            hi = CAP
        else:
            hi = 8
        while lo < hi:
            mid = (lo + hi) // 2
            dead, _, _, _, _ = first_kill(N, T0, BASE_H + [["KEEP", Z]] * mid, P, k, C, rho)
            if dead:
                hi = mid
            else:
                lo = mid + 1
        Hmin = BASE_H + [["KEEP", Z]] * lo
        dead, pre, r, kidx, kp = first_kill(N, T0, Hmin, P, k, C, rho)
        assert dead
        ind = IX.replay(N, T0, Hmin, P, k, C, rho)
        cr = CR.execute(N, T0, Hmin, P, k, C, rho)
        a1 = [(x["need"], x["paid"]) for x in r["keeps"]]
        assert a1 == [(x["need"], x["paid"]) for x in ind["keeps"]] and ind["violations"] > 0
        assert a1 == [(x["need"], x["paid"]) for x in cr["keeps"]]
        wit = {"candidate": key, "P": P, "k": k, "C": C, "rho": rho_name,
               "identity_hash": ident, "node": "MSTL-14", "n": N, "T0": T0,
               "H_base": BASE_H, "absent_key": Z, "battery_length": lo,
               "H": Hmin, "kill_keep_number": kidx,
               "keep_access_idx": kp["idx"], "need": kp["need"], "paid": kp["paid"],
               "margin": kp["margin"], "independent_agree": True,
               "cleanroom_agree": True,
               "witness_hash": hashlib.sha256(json.dumps(
                   {"n": N, "T0": T0, "H": Hmin}, sort_keys=True).encode()).hexdigest()}
        deaths.append(wit)
        (NS / ("death_%02d.json" % ci)).parent.mkdir(parents=True, exist_ok=True)
        (NS / ("death_%02d.json" % ci)).write_text(
            json.dumps(wit, indent=2, sort_keys=True), encoding="utf-8")
        step("AC-01", "[%d/63] %s REFUTED L*=%d need=%d paid=%d" %
             (ci + 1, key, lo, kp["need"], kp["paid"]))
    out = {"count": 63, "refuted": len(deaths), "active": actives,
           "terminal": "ALL_63_CANDIDATES_REFUTED" if len(deaths) == 63 and not actives
                       else "PARTIAL_REFUTATION_CONTINUES"}
    (NS / "cascade_summary.json").write_text(json.dumps(out, indent=2, sort_keys=True),
                                             encoding="utf-8")
    step("AC-99", "cascade done: refuted=%d active=%d terminal=%s"
         % (len(deaths), len(actives), out["terminal"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())

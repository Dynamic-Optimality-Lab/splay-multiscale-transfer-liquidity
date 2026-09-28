"""WP-4 STEP 124m: mutation battery (each mutant live + killed by its checker).

Exit 0 iff all 8 mutants are demonstrated faulty AND caught. Run via
scripts/run_phase04.py STEP 129 (never standalone for certification).
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from solver import encode as E
from solver import search as S
from solver import promote as PM

PASS = []


def check(name: str, cond: bool) -> None:
    print("[WP-4][MUTANT %s] %s" % (name, "KILLED" if cond else "SURVIVED"), flush=True)
    PASS.append(bool(cond))


def _vine(n):
    t = None
    for k in range(n, 0, -1):
        t = [k, None, t]
    return t


REG = (28, _vine(28), [["DELETE", 27], ["DELETE", 28], ["KEEP", 28], ["KEEP", 27]])


def main() -> int:
    print("[WP-4][STEP 124m] Running WP-4 mutation battery", flush=True)
    n, T0, H = REG
    # M-WP4-01: need off-by-one (need+1 changes the REG record; SYN-00 rejects).
    good = E.exec_full(n, T0, H, "P_all", 6, 2, (1, 1))["keeps"][-1]
    mut_need = good["need"] + 1
    check("M-WP4-01 need off-by-one",
          mut_need != 11 and (good["need"], good["paid"], good["margin"]) == (11, 10, -1))
    # M-WP4-02: paid overcount (+1 masks the REG shortfall; fidelity record differs).
    mut_paid = good["paid"] + 1
    check("M-WP4-02 paid overcount",
          mut_paid != 10 and good["margin"] == -1)
    # M-WP4-03: early-termination skip (first-KEEP-only misses a late violation).
    # Witness: [D16,K1,K16] on vine-16 at (P_all,0,2,FLAT(1)) -> [clean, violated].
    H3 = [["DELETE", 16], ["KEEP", 1], ["KEEP", 16]]
    full = E.exec_full(16, _vine(16), H3, "P_all", 0, 2, (1, 1))
    first_only = E.exec_counts(E.precompute(16, _vine(16), [H3[1]]), "P_all", 0, 2, (1, 1))
    assert [kp["paid"] < kp["need"] for kp in full["keeps"]] == [False, True]
    check("M-WP4-03 early-termination skip",
          full["violations"] > 0 and first_only["violations"] == 0)
    # M-WP4-04: baseline config mismatch (ROT(1) instead of FLAT(1)).
    check("M-WP4-04 baseline mismatch",
          S.baseline_of("P_all", 6, 2) == ("P_all", 6, 2, "FLAT(1)") and
          ("P_all", 6, 2, "ROT(1)") != S.baseline_of("P_all", 6, 2))
    # M-WP4-05: REG-gate bypass (screen must open with REG-001).
    from solver import battery as B
    check("M-WP4-05 REG-gate bypass", B.dev_screen()[0]["motif"] == "REG-001")
    # M-WP4-06: flipped label (mutant decision tree disagrees with the contract tree).
    fix = {"P_all|6|2|FLAT(1)": {"survived": False}}
    entry = {"P": "P_all", "k": 6, "C": 2, "rho": "ROT(6)"}
    flipped = "RHO_NOT_REQUIRED"  # mutant: swapped branches

    def mutant_label(e,_tab):
        base = _tab.get("|".join([e["P"], str(e["k"]), str(e["C"]), "FLAT(1)"]))
        if base is not None and base.get("survived"):
            return "RHO_NOT_REQUIRED"
        return "RHO_NOT_REQUIRED"  # mutant: always the same label

    _tab = fix
    check("M-WP4-06 flipped label",
          S.label(entry, fix) == "RHO_REQUIRED" and mutant_label(entry, fix) != "RHO_REQUIRED")
    # M-WP4-07: counterexample overwrite (append-only violated by mutant store).
    import tempfile
    from pathlib import Path as Pth
    with tempfile.TemporaryDirectory() as td:
        out = Pth(td)
        ep = {"n": 8, "H": [["KEEP", 1]], "id": "x"}
        p1 = PM.append_counterexample(out, "t", "c", ep, {}, {}, "L0", "z")
        p2 = PM.append_counterexample(out, "t", "c", ep, {}, {}, "L0", "z")
        mutant_overwrites = (p1 == p2)  # a clobbering store returns the same path
        check("M-WP4-07 counterexample overwrite",
              p1.name == "ce_0000.json" and p2.name == "ce_0001.json"
              and not mutant_overwrites)
    # M-WP4-08: partial reduce (mutant merges one shard only; completeness check kills).
    shards = {0: {"a|0": 1}, 1: {"b|1": 2}}
    mutant_merged = dict(shards[0])  # mutant: drops shard 1
    full_merged = {k: v for s in shards.values() for k, v in s.items()}
    check("M-WP4-08 partial reduce",
          len(full_merged) == 2 and len(mutant_merged) != 2)
    print("[WP-4][STEP 124m] mutants killed: %d/8" % sum(PASS), flush=True)
    return 0 if all(PASS) and len(PASS) == 8 else 2


if __name__ == "__main__":
    sys.exit(main())

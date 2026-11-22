"""Meaningful source, cyclic-credit, failure-continuation and rejection checks."""
from __future__ import annotations

import copy
import json
import random
import sys
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
from core import Tree, compile_source, evaluate, sweep
from sources import H_source, closed_word, mirrored, recurrent_cycles, vine
from verify import accept_unrestricted, check, functional, signature
from vendor import independent_splay as F


def shapes(lo, hi):
    if lo > hi:
        return [F.LEAF]
    return [F.node(k, l, r) for k in range(lo, hi + 1)
            for l in shapes(lo, k - 1) for r in shapes(k + 1, hi)]


class EngineTests(unittest.TestCase):
    def test_every_small_rotation_shape_against_functional_primitive(self):
        cases = set()
        for n in range(1, 6):
            keys = list(range(1, n + 1))
            for t in shapes(1, n):
                s = signature(t)
                for target in keys:
                    fast = Tree(s, keys)
                    steps = list(fast.steps(target))
                    expected, old_steps = F.trace(t, target)
                    self.assertEqual(fast.state(), signature(expected))
                    self.assertEqual([x[0] for x in steps], [x[0] for x in old_steps])
                    cases.update(x[0] for x in steps)
        self.assertEqual(cases, {"ZIG", "LL", "RR", "LR", "RL"})

    def test_large_complete_sources_and_credit_slots(self):
        cases = [H_source(2, 1), H_source(3, 3), mirrored(H_source(3, 3))]
        for source in cases:
            result = check(evaluate(source, detail=True))
            self.assertTrue(result["passed"])
            self.assertGreater(result["support"], 6)
            self.assertLessEqual(result["maximum_A_load"], 45)

    def test_unpaid_steps_do_not_halt_the_physical_word(self):
        source = closed_word(17, [["D", k] for k in range(2, 18)] + [["K", 17]])
        tape = compile_source(source)
        bsteps = [e for e in tape["events"] if e["id"][0] == "B" and e["id"][1] == 17]
        self.assertEqual(sum(e["q"] for e in bsteps), 8)
        # Deliberately forced bank entry: a unit regression, NOT an admissible
        # frozen-policy source certificate or a Universal-CD counterexample.
        final, counts = sweep([0, 0, 0, 5], bsteps, record=True)
        self.assertEqual(counts["paid"], 5)
        self.assertEqual(counts["Omega_5"], 3)
        self.assertEqual(len(counts["rows"]), 8)
        self.assertEqual([r["unpaid"] for r in counts["rows"]][-3:], [1, 1, 1])
        self.assertEqual(sum(final), 0)

    def test_cyclic_cut_and_repetition_with_prefix_excluded(self):
        source = H_source(2, 1)
        cert = evaluate(source, detail=True)
        c = compile_source(source, states=True)
        cut = 19
        from sources import _state
        aa, bb = c["states"][cut]
        shifted = {"name": "cyclic_cut_control", "initial_A": _state(aa, c["keys"]),
                   "initial_B": _state(bb, c["keys"]), "diagonal": source["diagonal"],
                   "prefix": source["operations"][:cut],
                   "operations": source["operations"][cut:] + source["operations"][:cut]}
        shifted_cert = evaluate(shifted, detail=True)
        self.assertTrue(check(shifted_cert)["passed"])
        self.assertEqual(shifted_cert["A"], cert["A"])
        self.assertEqual(shifted_cert["Omega_5"], cert["Omega_5"])
        repeated = dict(source, name="repeated_control",
                        operations=source["operations"] * 3,
                        expected_A=source["expected_A"] * 3)
        rep = evaluate(repeated, detail=True)
        self.assertTrue(check(rep)["passed"])
        self.assertEqual(rep["A"], 3 * cert["A"])
        self.assertEqual(rep["Omega_5"], 3 * cert["Omega_5"])
        self.assertEqual(rep["bank"]["initial_greatest_fixed_point"],
                         cert["bank"]["initial_greatest_fixed_point"])

    def test_arbitrary_physical_key_labels(self):
        source = H_source(2, 1)
        mapping = {k: 101 + 7*k for k in range(1, 18)}
        def tree(t):
            return {"root": mapping[t["root"]], "children": {
                str(mapping[int(k)]): [mapping[v] if v is not None else None for v in children]
                for k, children in t["children"].items()}}
        changed = {**source, "name": "sparse_label_control",
                   "initial_A": tree(source["initial_A"]), "initial_B": tree(source["initial_B"]),
                   "diagonal": tree(source["diagonal"]),
                   "operations": [[mode, mapping[x]] for mode, x in source["operations"]]}
        self.assertTrue(check(evaluate(changed, detail=True))["passed"])

    def test_recurrent_period_is_a_full_original_source(self):
        source = H_source(2, 1)
        cycles = recurrent_cycles(source, limit=3)
        self.assertTrue(cycles)
        for cycle in cycles:
            self.assertTrue(check(evaluate(cycle, detail=True))["passed"])

    def test_pure_circulation_supplies_no_demand(self):
        initial = vine(range(1, 18))
        source = {"name": "no_work", "initial_A": initial, "initial_B": initial,
                  "diagonal": initial, "prefix": [], "operations": []}
        cert = evaluate(source, detail=True)
        self.assertEqual(cert["P_5"], 0)
        self.assertEqual(cert["credit_provenance"]["issuance"], {})
        self.assertTrue(check(cert)["passed"])

    def test_reaching_prefix_is_checked(self):
        bad = H_source(2, 1)
        bad["prefix"] = [["D", 17]]
        with self.assertRaises(AssertionError):
            evaluate(bad, detail=True)

    def test_missing_restoration_is_rejected(self):
        source = H_source(2, 1)
        source["operations"] = source["operations"][:-1]
        with self.assertRaises(AssertionError):
            evaluate(source, detail=True)

    def test_tampered_cyclic_stock_is_rejected(self):
        cert = evaluate(H_source(2, 1), detail=True)
        cert["bank"]["initial_greatest_fixed_point"][0] = (
            cert["bank"]["initial_greatest_fixed_point"][0] + 1) % 6
        with self.assertRaises(AssertionError):
            check(cert)

    def test_tampered_original_event_is_rejected(self):
        cert = evaluate(H_source(2, 1), detail=True)
        next(e for e in cert["events"] if e["q"])["q"] = 0
        with self.assertRaises(AssertionError):
            check(cert)

    def test_duplicate_actual_A_slot_is_rejected(self):
        cert = evaluate(H_source(2, 1), detail=True)
        assignments = cert["credit_provenance"]["paid_original_B_assignments"]
        self.assertGreater(len(assignments), 2)
        assignments[1]["A_unit"] = assignments[0]["A_unit"]
        assignments[1]["A_slot"] = assignments[0]["A_slot"]
        with self.assertRaises(AssertionError):
            check(cert)

    def test_unpaid_label_cannot_be_changed_to_paid(self):
        cert = evaluate(H_source(2, 1), detail=True)
        cert["Omega_5"] += 1
        with self.assertRaises(AssertionError):
            check(cert)

    def test_primary_objective_is_actual_complete_ratio(self):
        from search import score
        low = {"Omega_5_over_A": "1/100", "Q_B_over_A": "100",
               "bank": {"minimum_paid_step_margin": -100}, "A": 1}
        high = {"Omega_5_over_A": "1/99", "Q_B_over_A": "0",
                "bank": {"minimum_paid_step_margin": 100}, "A": 10**6}
        self.assertGreater(score(high), score(low))

    def test_proof_metadata_cannot_bypass_universal_gate(self):
        forged = {"status": "PROVED", "K": 1, "all_original_sources": True,
                  "finite_cases_passed": 10**9}
        self.assertFalse(accept_unrestricted(forged)["accepted"])

    def test_large_support_does_not_disguise_automatic_access_coverage(self):
        from search import score
        automatic = {"Omega_5_over_A": "0", "Q_B_over_A": "3/2",
                     "max_B_doubles_per_access": 2,
                     "bank": {"minimum_paid_step_margin": 2}, "A": 4}
        nontrivial = {"Omega_5_over_A": "0", "Q_B_over_A": "1/4",
                     "max_B_doubles_per_access": 8,
                     "bank": {"minimum_paid_step_margin": 5}, "A": 128}
        self.assertGreater(score(nontrivial), score(automatic))

    def test_actual_positive_residual_fixture_is_not_silently_funded(self):
        from verify import load
        fixture = Path(__file__).resolve().parent / "run_003/complete_00.json.gz"
        cert = load(fixture)
        result = check(cert)
        self.assertEqual((result["A"], result["Q_B"], result["Omega_5"]), (989, 519, 2))
        self.assertEqual(cert["P_5"], 517)
        unpaid = [r["id"] for r in cert["bank"]["rows"] if r["unpaid"]]
        self.assertEqual(unpaid, [["B", 99, 14], ["B", 99, 15]])
        # The next original step is executed and funded; no first-failure stop.
        next_row = next(r for r in cert["bank"]["rows"] if r["id"] == ["B", 99, 16])
        self.assertEqual(next_row["paid"], 1)

    def test_positive_residual_repeats_without_free_prefix_credit(self):
        from verify import load
        cert = load(Path(__file__).resolve().parent / "run_003/complete_00.json.gz")
        source = dict(cert["source"], name="repeat_positive_regression",
                      operations=cert["source"]["operations"] * 2)
        repeated = evaluate(source, detail=True)
        self.assertEqual((repeated["A"], repeated["Q_B"], repeated["Omega_5"]), (1978, 1038, 4))
        self.assertTrue(check(repeated)["passed"])


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(EngineTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print(json.dumps({"passed": result.wasSuccessful(), "tests": result.testsRun,
                      "scope": "Implementation checks, not a universal cost proof."}))
    raise SystemExit(0 if result.wasSuccessful() else 1)

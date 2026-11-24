"""Semantic soundness checks, including cases numerical inequalities miss."""
import json
import unittest
from fractions import Fraction
import certify as C
import composition as M
import gso


class Soundness(unittest.TestCase):
    def test_unlimited_local_A_cannot_repair_the_unreachable_B_state(self):
        z=M.K.load(M.HERE/'COMPONENT_UNREACHABILITY_CERTIFICATE.json');start=C.tupleize(z['component_before']);target=C.tupleize(z['component_after']);reachable,rows=C.local_B_reachable(start)
        self.assertEqual(len(reachable),3);self.assertEqual(len(rows),9);self.assertNotIn(target,reachable)

    def test_zero_original_A_interface_is_not_a_free_local_KEEP(self):
        z=M.K.load(M.HERE/'ZERO_ORIGINAL_A_INTERFACE_CERTIFICATE.json')['witness']['component']
        self.assertEqual(z['attributed_original_A_units'],0);self.assertEqual(z['before_A'],z['after_A']);self.assertEqual(z['before_B'][0],7);self.assertEqual(z['after_B'][0],6)

    def test_open_component_needs_signed_boundary_credit(self):
        z=M.K.load(M.HERE/'TEMPORAL_COMPOSITION_CERTIFICATE.json')['open_piece_counterexample']
        self.assertGreater(Fraction(z['q']),Fraction(3,2)*z['a']);self.assertLessEqual(2*z['q']+z['P_after']-z['P_before'],3*z['a'])

    def test_finite_or_numeric_success_cannot_bypass_the_semantic_gate(self):
        args=dict(source_binding='PROVED_ALL_SOURCES',local_ordinary_histories='PROVED_ALL_SOURCES',coverage='PROVED_ALL_SOURCES',A_reuse='PROVED_ALL_SOURCES',boundary_balance='PROVED_ALL_SOURCES',interaction_budget='PROVED_ALL_SOURCES')
        self.assertEqual(gso.gate(**args)['root_status'],'PROVED_FROM_THE_DECLARED_PREMISES')
        for key in args:
            modified={**args,key:'FINITE_EXACT'};self.assertEqual(gso.gate(**modified)['root_status'],'OPEN')
        modified={**args,'local_ordinary_histories':'REFUTED','interaction_budget':'NUMERICAL_FIT'}
        self.assertEqual(gso.gate(**modified)['first_missing'],'local_ordinary_history_or_costed_interface')

    def test_reference_uses_each_real_A_bit_once(self):
        z=M.K.load(M.HERE/'reference/source_01.json.gz');ids=[tuple(b['original_id']) for part in z['bundles'] for b in part['actual_original_A_rotations']]
        self.assertEqual(len(ids),len(set(ids)));self.assertEqual(len(ids),z['R_A']);self.assertLessEqual(z['reference_cost'],3*z['source_A'])


if __name__=='__main__':unittest.main(verbosity=2)

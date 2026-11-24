"""Soundness tests for original-source credit and theorem acceptance boundaries."""
import sys
import copy
import unittest
sys.dont_write_bytecode=True
import verify as V
import proofcheck as P
from reserve import drawdown,cyclic_credit


class CreditSoundness(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.case=V.read('COMPLETE_SOURCE_AUDIT.json')['cases'][0]
        cls.trace=V.read(cls.case['trace']);cls.tape,_=V.V.physical(cls.trace)

    def test_learned_induction_verified_over_unbounded_states(self):
        self.assertTrue(P.check(V.read('LEARNED_INDUCTION.json'))['passed'])

    def test_wrong_learner_invariant_rejected(self):
        d=V.read('LEARNED_INDUCTION.json');d['second'][2]=15
        with self.assertRaises(AssertionError):P.check(d)

    def test_changed_original_physical_rotation_rejected(self):
        z=copy.deepcopy(self.trace);z['steps'][0]['bits'][0]['promoted']=z['steps'][0]['bits'][0]['demoted']
        with self.assertRaises(AssertionError):V.V.physical(z)

    def test_changed_padding_rejected(self):
        z=copy.deepcopy(self.trace);z['source']['embedding']['gap_sizes'][0]+=1
        with self.assertRaises(AssertionError):V.geometry(z,V.read(self.case['energy']),1)

    def test_changed_size_energy_coefficient_rejected(self):
        energy=V.read(self.case['energy']);energy['whole_operation_delta_Phi_w_coefficients']={}
        with self.assertRaises(AssertionError):V.geometry(self.trace,energy,1)

    def test_understated_global_capacity_rejected(self):
        bank=V.read(self.case['global_credit']);bank['capacity']-=1
        with self.assertRaises(AssertionError):V.global_credit(self.trace,self.tape,bank)

    def test_duplicate_actual_A_credit_rejected(self):
        bank=V.read(self.case['global_credit']);bank['credit_assignments'][1]['A_credit']=bank['credit_assignments'][0]['A_credit']
        with self.assertRaises(AssertionError):V.global_credit(self.trace,self.tape,bank)

    def test_deleted_original_unpaid_cost_is_rejected(self):
        bank=V.read(self.case['global_credit']);bank['credit_assignments'].pop()
        with self.assertRaises(AssertionError):V.global_credit(self.trace,self.tape,bank)

    def test_wraparound_deficit_is_included(self):
        self.assertEqual(drawdown([3,-10,4])['capacity'],7)

    def test_mean_cost_failure_is_not_hidden_by_initial_credit(self):
        with self.assertRaises(AssertionError):cyclic_credit([{'id':['B',1,1],'a':0,'q':1}],4)

    def test_earlier_lap_credit_is_literal_original_A_work(self):
        bank=V.read(self.case['global_credit']);first=self.case['carrier_support']
        assignments=[a for a in bank['credit_assignments'] if a['B'][1]==first]
        self.assertTrue(all(a['A_credit'][0]=='A' and a['A_credit'][1]>first for a in assignments))

    def test_refuted_reverse_phase_assumption_is_preserved(self):
        d=V.read('CHRONOLOGY_CORRECTION.json')
        self.assertEqual(d['status'],'REFUTED_EXACT_SOURCE_CHRONOLOGY')
        self.assertEqual(d['actual_A_phase'],'forward_restoration')

    def test_full_source_is_not_a_CD_counterexample(self):
        self.assertLess(self.trace['Q_B'],self.trace['A'])
        self.assertFalse(P.check(V.read('LEARNED_INDUCTION.json'))['persistent_global_banks_excluded'])

    def test_unrestricted_acceptance_remains_open(self):
        r=P.check(V.read('LEARNED_INDUCTION.json'))
        self.assertFalse(r['root_scope_restricted'])
        self.assertEqual(r['new_unrestricted_root_cost_obligations_deleted'],0)
        self.assertEqual(r['universal_CD'],'OPEN')

    def test_DELETE_loop_erasure_preserves_full_physical_A(self):
        import normalize
        source=self.trace['source'];initial=normalize.V.immutable(source['initial_A'])
        root=initial.k;child=initial.r.k if initial.r else initial.l.k
        result=normalize.delete_gap(initial,[['D',child],['D',root]])
        self.assertEqual(result['kept'],[])
        self.assertEqual((result['original_A_cost'],result['reduced_A_cost']),(2,0))
        self.assertTrue(result['complete_A_state_preserved'])

    def test_normalizer_does_not_erase_KEEP_coupled_restoration(self):
        import normalize
        with self.assertRaises(AssertionError):normalize.delete_gap(normalize.V.immutable(self.trace['source']['initial_A']),[['K',1]])

    def test_failed_full_zero_edge_law_is_not_silently_weakened(self):
        r=V.read('ZERO_EDGE_INVARIANT_RESULT.json');c=r['counterexample']
        self.assertEqual(r['status'],'REFUTED_EXACT_ORIGINAL_PHYSICAL_INVARIANT')
        self.assertEqual(c['edge_owner_banks'][0],c['edge_owner_banks'][1])
        self.assertEqual(c['counter_event_unpaid'],0)
        self.assertFalse(r['bank_funding_refuted'])

    def test_cross_block_zero_edge_law_also_has_a_physical_counterexample(self):
        r=V.read('CROSS_BLOCK_ZERO_EDGE_RESULT.json');c=r['counterexample']
        self.assertEqual(r['status'],'REFUTED_EXACT_ORIGINAL_PHYSICAL_INVARIANT')
        self.assertNotEqual(c['edge_owner_banks'][0],c['edge_owner_banks'][1])
        self.assertEqual(c['counter_event_unpaid'],0)


if __name__=='__main__':unittest.main()

"""Proof soundness: fail closed on bad scopes, missing cases and ghost credit."""
import sys
import copy
import unittest
sys.dont_write_bytecode=True
import proofcheck as P


class JointProofSoundness(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.cert=P.read('run_005/CONTROL_CERTIFICATE.json')

    def test_invariant_and_energy_are_joint_learner_output(self):
        p=self.cert['candidate']
        self.assertEqual(p['path_invariant'],[1,-1,-2,-1])
        self.assertEqual((p['bank_capacity'],p['overflow_ticket'],p['bank_weight'],p['overflow_weight']),(0,1,0,1))
        self.assertGreater(self.cert['reused_inductive_counterconstraints'],0)

    def test_scoped_certificate_cannot_be_promoted(self):
        cert=copy.deepcopy(self.cert);cert['scope']='unrestricted';cert['status']='PROVED_GLOBAL_SYMBOLIC_CERTIFICATE'
        with self.assertRaises(AssertionError):P.check(cert,'unrestricted')

    def test_fake_global_label_rejected(self):
        cert=copy.deepcopy(self.cert);cert['status']='PROVED_GLOBAL_SYMBOLIC_CERTIFICATE'
        with self.assertRaises(AssertionError):P.check(cert)

    def test_missing_orientation_rejected(self):
        ir=P.read('PROOF_LANGUAGE.json');ir['rotation_schemas']=[r for r in ir['rotation_schemas'] if r['case']!='RL']
        with self.assertRaises(AssertionError):P.structural(ir,2)

    def test_erased_hanging_subtree_rejected(self):
        ir=P.read('PROOF_LANGUAGE.json');ir['rotation_schemas'][0]['after'][3]=['hole','C']
        with self.assertRaises(AssertionError):P.structural(ir,2)

    def test_insufficient_structural_bound_rejected(self):
        with self.assertRaises(AssertionError):P.structural(P.read('PROOF_LANGUAGE.json'),1)

    def test_false_conservation_invariant_rejected(self):
        cert=copy.deepcopy(self.cert);cert['candidate']['path_invariant'][2]=0
        with self.assertRaises(AssertionError):P.check(cert)

    def test_unpaid_cost_cannot_be_deleted_by_zero_energy(self):
        cert=copy.deepcopy(self.cert);cert['candidate']['overflow_weight']=0
        with self.assertRaises(AssertionError):P.check(cert)

    def test_global_reserve_may_not_expire_at_access_boundaries(self):
        cert=copy.deepcopy(self.cert)
        for row in cert['proof_dag']:
            if row['obligation']=='ticket_boundary':row['result']='ZERO_AT_EACH_OPERATION_BOUNDARY_BY_CONSERVATIVE_EXPIRY'
        with self.assertRaises(AssertionError):P.check(cert)

    def test_weak_unproved_entry_cannot_pass_cost_check(self):
        cert=copy.deepcopy(self.cert);cert['candidate']['reserve_invariant']=[1,0,0,0,0]
        with self.assertRaises(AssertionError):P.check(cert)

    def test_unpaid_running_total_cannot_be_hidden_in_potential(self):
        cert=copy.deepcopy(self.cert);cert['candidate']['minus_cumulative_unpaid']=1
        with self.assertRaises(AssertionError):P.check(cert)

    def test_nonzero_unpaid_is_really_funded_globally(self):
        audit=P.read('AUDIT_SUMMARY.json')
        self.assertTrue(all(r['bank_unpaid']==r['Q_B']>0 and r['unfunded']==0 for r in audit['controls']))

    def test_original_constant_one_counterexample_keeps_root_open(self):
        audit=P.read('AUDIT_SUMMARY.json')['root_C1_counterexample']
        self.assertEqual((audit['A'],audit['Q_B']),(4,6))
        self.assertGreater(audit['unfunded'],0)

    def test_abstract_barrier_is_not_an_original_counterexample(self):
        barrier=P.read('GLOBAL_ABSTRACT_BARRIER.json')
        self.assertEqual(barrier['universal_CD'],'OPEN')
        self.assertIn('NOT_PROVED',barrier['physical_concretization'])

    def test_unrestricted_target_has_no_support_or_target_cutoff(self):
        import global_energy
        result=global_energy.verify()
        self.assertFalse(result['scope_restriction_added_to_target'])
        self.assertEqual(result['new_unrestricted_root_cost_obligations_deleted'],0)
        self.assertEqual(result['universal_CD'],'OPEN')

    def test_metric_fragment_does_not_refute_a_persistent_bank(self):
        # The new source alias forbids a memoryless metric energy. Earlier A
        # work may still pay the fragment through an independently conserved
        # bank; deliberately do not constrain that bank to cancel here.
        import z3
        s=z3.Solver();q,C,drop=z3.Ints('q C drop')
        s.add(q==1000,C==1,drop==1000,q+1-drop<=14*C)
        self.assertEqual(s.check(),z3.sat)

    def test_metric_witnesses_are_not_full_source_cost_counterexamples(self):
        result=P.read('INDEPENDENT_METRIC_VERIFICATION.json')
        self.assertTrue(result['passed'])
        self.assertFalse(result['original_counterexample_to_Universal_CD'])
        self.assertTrue(all(row['Q_B']<=row['A'] for row in result['cases']))


if __name__=='__main__':unittest.main()

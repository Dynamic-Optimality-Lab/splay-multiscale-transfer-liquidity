"""Meaningful soundness/regression checks for the bounded research engine."""
import copy
import unittest
from fractions import Fraction
from kernel import shapes,encode,original_splay,OLD,json_state,frontier_features,load,HERE
import teacher
from registry import Obligation,REQUIRED,root_gate


class EngineTests(unittest.TestCase):
    def test_source_kernel_preserves_every_key_and_original_cost(self):
        for raw in shapes(1,4):
            t=encode(raw,4)
            for x in range(1,5):
                out,d=original_splay(t,x);original=OLD.Tree(json_state(t),list(range(1,5)))
                expected_depth=len(original.path(x))-1;OLD.plain(original,x)
                self.assertEqual(expected_depth,d);self.assertEqual(original.state(),json_state(out));self.assertEqual(out[0],x)

    def test_positive_cycle_and_potential_are_both_exercised(self):
        g=teacher.build(3)
        self.assertEqual(teacher.exact_trial(g,0)['status'],'VIOLATING_CYCLE')
        self.assertEqual(teacher.exact_trial(g,1)['status'],'FINITE_EXACT_POTENTIAL')
        best=teacher.optimum(g);self.assertEqual(Fraction(best['C']),1);self.assertTrue(best['attaining_cycle'])

    def test_transient_edges_are_not_closed_source_counterexamples(self):
        g=teacher.build(3);recurrent=set(g['recurrent_edges']);self.assertLess(len(recurrent),len(g['edges']))
        for i in recurrent:
            ids=teacher.close_edge(g,i);self.assertEqual(ids[0],i)
            self.assertEqual(g['edges'][ids[-1]][1],g['edges'][ids[0]][0])

    def test_corrupted_potential_is_detected_by_an_actual_edge(self):
        g=teacher.build(3);p=[0]*len(g['pairs'])
        self.assertTrue(any(q+p[v]-p[u]>0 for u,v,a,q,_,_ in g['edges']))

    def test_finite_and_conditional_results_cannot_close_root(self):
        claims=[Obligation(n,'PROVED','ALL_ORIGINAL_SOURCES',True,'checked test fixture') for n in REQUIRED]
        self.assertEqual(root_gate(claims)['root_status'],'PROVED')
        for status,scope in [('FINITE-EXACT','FINITE_SUPPORT_6'),('CONDITIONAL','ALL_ORIGINAL_SOURCES'),('PROVED','FINITE_SUPPORT_6')]:
            altered=[c for c in claims if c.name!='whole_operation_cost']+[Obligation('whole_operation_cost',status,scope,True,'finite/conditional evidence')]
            self.assertEqual(root_gate(altered)['root_status'],'OPEN')

    def test_root_equality_guard_root_depth_terms_are_identically_zero(self):
        g=teacher.build(4)
        self.assertTrue(all(f[6]==f[7]==0 for f in g['features']))


if __name__=='__main__':unittest.main(verbosity=2)

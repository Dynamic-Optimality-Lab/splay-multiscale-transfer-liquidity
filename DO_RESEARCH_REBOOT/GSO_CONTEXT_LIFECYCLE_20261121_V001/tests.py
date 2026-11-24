"""Soundness tests for context lifting, aliasing, and the root gate."""
import copy
import json
import unittest
from fractions import Fraction
import context as C
import path_compiler as P
import gso


class Soundness(unittest.TestCase):
    def test_compression_discharges_every_complete_core3_transition(self):
        direct=C.K.load(C.HERE/'run_001/CONTEXT_GRAPH.json.gz');paths=P.compile_paths(3)
        def rows(g):return {(C.core_key(g['pairs'][u]),C.core_key(g['pairs'][v]),a,q) for u,v,a,q,_,_ in g['edges']}
        compiled=rows(paths)
        for u,v,a,q in rows(direct):
            if u==v=='[[0],[0]]':
                self.assertLessEqual(q,a)
            else:
                self.assertTrue(any((u,v,a-prefix,q-prefix) in compiled for prefix in range(min(a,q)+1)),(u,v,a,q))

    def test_actual_arbitrary_hanging_paths_preserve_the_reduced_pair(self):
        graph=C.K.load(C.HERE/'core5_001/CONTEXT_GRAPH.json.gz')
        core=next(p for p in graph['pairs'] if C.size(p)==5)
        for length in (1,2,7,23):
            path=None
            for key in range(2+length,2,-1):path=(key,None,path)
            a=P.insert_path(tuple(core[0]),2,path,length);b=P.insert_path(tuple(core[1]),2,path,length)
            self.assertEqual(C.reduce_pair(a,b),tuple(map(tuple,core)))

    def test_corrupted_context_certificate_cannot_pass(self):
        g=C.K.load(C.HERE/'core5_001/CONTEXT_GRAPH.json.gz');z=C.K.load(C.HERE/'core5_001/CONTEXT_CERTIFICATE.json');p=z['upper_certificate']['potential_numerators'][:];den=z['upper_certificate']['potential_denominator'];constant=Fraction(z['C'])
        self.assertTrue(all(den*q+p[v]-p[u]<=den*constant*a for u,v,a,q,_,_ in g['edges']))
        u,v,a,q,_,_=next(e for e in g['edges'] if e[0]!=e[1]);p[v]+=1000
        self.assertTrue(any(den*q+p[v]-p[u]>den*constant*a for u,v,a,q,_,_ in g['edges']))

    def test_successful_context_tables_cannot_close_the_unrestricted_root(self):
        s=gso.status();self.assertEqual(s['root_status'],'OPEN');self.assertEqual(s['new_unrestricted_original_residual_classes_paid'],0)

    def test_equal_core_value_rejects_every_scalar_function_at_trial13(self):
        source=C.K.load(C.HERE/'sources_001/source_10.json.gz');n=len(source['source']['initial_A']['children']);r=next(r for r in source['rows'] if r['op']==n+7)
        self.assertEqual((r['kappa_before'],r['kappa_post_A'],r['kappa_after']),(n-3,n-3,n-3));self.assertGreater(r['q'],13*r['a'])


if __name__=='__main__':unittest.main(verbosity=2)

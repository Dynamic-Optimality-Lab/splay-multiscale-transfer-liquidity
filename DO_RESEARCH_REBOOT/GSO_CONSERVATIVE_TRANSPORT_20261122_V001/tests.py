"""Soundness regressions: reject fabricated exact flow/resource certificates."""
import sys
import copy
import unittest
sys.dont_write_bytecode = True
import verify as V


class CertificateSoundness(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.good=V.read(V.HERE/'run_001/legacy_00_H2.json.gz')
        cls.z=V.read(V.ROOT/cls.good['trace']['path'])
        cls.tape,_=V.physical(cls.z)
        cls.edges,_,_,_=V.edges(cls.z,cls.tape,2)

    def test_over_capacity_rejected(self):
        cert=copy.deepcopy(self.good); index=cert['positive_edge_flows'][0][0]
        cert['positive_edge_flows'][0][1]=self.edges[index][2]+1
        with self.assertRaises(AssertionError): V.certificate(self.z,self.tape,cert)

    def test_duplicate_flow_edge_rejected(self):
        cert=copy.deepcopy(self.good); cert['positive_edge_flows'].append(cert['positive_edge_flows'][0])
        with self.assertRaises(AssertionError): V.certificate(self.z,self.tape,cert)

    def test_unfunded_original_demand_rejected(self):
        cert=copy.deepcopy(self.good)
        demand=next(i for i,e in enumerate(self.edges) if e[3]=='demand')
        cert['positive_edge_flows']=[p for p in cert['positive_edge_flows'] if p[0]!=demand]
        with self.assertRaises(AssertionError): V.certificate(self.z,self.tape,cert)

    def test_fabricated_paid_total_rejected(self):
        cert=copy.deepcopy(self.good); cert['paid']+=1
        with self.assertRaises(AssertionError): V.certificate(self.z,self.tape,cert)

    def test_false_cut_rejected(self):
        cert=V.read(V.HERE/'run_001/legacy_00_H1.json.gz'); cert['cut']['source_side_nodes'].append(1)
        with self.assertRaises(AssertionError): V.certificate(self.z,self.tape,cert)

    def test_A_voucher_reuse_rejected(self):
        mapping=V.read(V.HERE/'inputs/legacy_00_vouchers.json.gz'); keys=list(mapping)
        mapping[keys[1]]=mapping[keys[0]]
        with self.assertRaises(AssertionError): V.voucher_check(self.z,mapping)

    def test_entry_obstruction_is_funded_original_U(self):
        record=V.read(V.HERE/'ENTRY_INVARIANT_OBSTRUCTION.json')
        self.assertTrue(record['funded_original_double'])
        self.assertLess(min(record['role_stocks']['external'],record['role_stocks']['grandparent']),1)
        self.assertEqual(record['id'][1:],record['original_U_receipt']['id'])

    def test_finite_candidate_does_not_claim_universal_bound(self):
        choice=V.read(V.HERE/'SELECTED_ROLE_POLICY.json')
        self.assertEqual(choice['status'],'FINITE_SURVIVOR_NOT_UNIVERSAL')
        self.assertEqual(V.read(V.HERE/'PACKET_VERIFICATION.json')['universal_CD'],'OPEN')

    def test_beam_physics_matches_immutable_original_kernel(self):
        import packet_search as search
        import random
        n=17; state=search.initial(n); root=None
        for k in range(n,0,-1):root=V.V.node(k,None,root)
        trees={'A':root,'B':root};rng=random.Random(39121)
        for _ in range(100):
            mode='K' if rng.randrange(3) else 'D';target=rng.randrange(1,n+1)
            state,_,failed=search.move(state,mode,target)
            self.assertFalse(failed)
            for actor in ('A','B') if mode=='K' else ('A',):
                trees[actor],_=V.V.rebuild(trees[actor],target,lambda *x:None,lambda *x:None)
            for actor,children,actual_root in (('A',state[0],state[2]),('B',state[3],state[5])):
                expected=V.raw(trees[actor]);self.assertEqual(actual_root,expected['root'])
                self.assertEqual({str(k):[x or None for x in children[k]] for k in range(1,n+1)},expected['children'])


if __name__=='__main__': unittest.main()

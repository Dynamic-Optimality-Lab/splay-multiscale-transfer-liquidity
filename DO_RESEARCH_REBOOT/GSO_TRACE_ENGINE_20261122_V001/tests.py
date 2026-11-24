"""Soundness regressions for failures that would invalidate the accounting."""
import sys
import copy
import unittest
sys.dont_write_bytecode=True
import trace as X
import trace_teacher as T
import trace_induction as I
import gso as G
import verify as V


class Soundness(unittest.TestCase):
    def test_zero_mask_keeps_original_double(self):
        z=X.K.load(X.HERE/'run_001/trace_17.json.gz');self.assertEqual(sum(s['q'] for s in z['steps']),165)
        self.assertTrue(all(all(not v for v in mask) for s in z['steps'] for mask in s['retained_bit_masks'].values()))
        self.assertTrue(any(s['q'] for s in z['steps']))

    def test_no_free_seam_credit(self):
        z={'blocks':[[1]],'Q_B':1,'A':0,'K_B':0,'source':{'name':'synthetic_ledger_only'},'operations':[{'id':1,'target':1,'k':0,'steps':[0,1]}],'steps':[{'id':['B',1,1],'a':0,'q':1,'k':0,'scope':[0]}]}
        r=T.bank(z,c=100,d=100,capacity=100);self.assertEqual(r['paid'],0)

    def test_one_shared_A_supply(self):
        z=X.K.load(X.HERE/'run_001/trace_01.json.gz');g,ev,_,_=T.bank_network(z,4,0,4)
        self.assertEqual(sum(v['capacity'] for _,_,v in g.out_edges('s',data=True)),4*z['A'])

    def test_corrupt_issuance_rejected_independently(self):
        z=X.K.load(X.HERE/'run_001/trace_00.json.gz');b=X.K.load(X.HERE/'run_001/bank_00.json.gz');bad=copy.deepcopy(b);bad['c']=0
        with self.assertRaises((AssertionError,KeyError)):V.bank_check(z,bad)

    def test_keep_allowance_once_per_access(self):
        z=X.K.load(X.HERE/'run_001/trace_13.json.gz');self.assertEqual(sum(e['k'] for e in T.events(z)),z['K_B']);self.assertTrue(all(s['k']==0 for s in z['steps']))

    def test_ice_requires_successor(self):
        g=X.K.load(X.C.C.PREVIOUS/'run_001/graph_3.json.gz');diag={i for i,(a,b) in enumerate(g['pairs']) if a==b}
        self.assertEqual(I.ice_teacher(g,diag)['status'],'FAILED_SUCCESSOR_IMPLICATION');self.assertEqual(I.ice_teacher(g,range(len(g['pairs'])))['status'],'FINITE_EXACT_INDUCTIVE_SUBSET')

    def test_finite_candidate_does_not_close_root(self):
        p=X.K.load(X.HERE/'run_001/FINITE_RELAXED_CANDIDATE.json');self.assertEqual(G.accept(p,{})['universal_CD'],'OPEN')

    def test_block_view_preserves_pairing_and_cost_id(self):
        z=X.K.load(X.HERE/'run_001/trace_17.json.gz');s=next(s for s in z['steps'] if s['q']);view=X.block_view(s,z['blocks'][0],0)
        self.assertEqual(view['original_id'],s['id']);self.assertEqual(view['original_cost']['q'],1);self.assertTrue(view['original_pairing_retained'])


if __name__=='__main__':unittest.main()

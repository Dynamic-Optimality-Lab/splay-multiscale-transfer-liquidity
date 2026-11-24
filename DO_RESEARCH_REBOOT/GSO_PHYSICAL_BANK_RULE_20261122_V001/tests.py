"""Soundness tests for cyclic closure, monotonicity and exact failure scope."""
import sys
import copy
import unittest
from itertools import product
sys.dont_write_bytecode=True
import bank_rule as B
import coarsening as C


def toy(events):
    return {'source':{'name':'synthetic_bank_algebra_only'},'blocks':[[1],[2],[3]],'A':sum(e['a'] for e in events),'Q_B':sum(e['q'] for e in events),'K_B':sum(e['k'] for e in events)}


E=[{'id':['A',1,1],'a':1,'q':0,'k':0,'target':1,'scope':[0,1],'priority':[0,1]},
   {'id':['B',1,1],'a':0,'q':1,'k':0,'target':3,'scope':[1,2],'priority':[2,1]},
   {'id':['B',1,2],'a':0,'q':1,'k':0,'target':3,'scope':[0,2],'priority':[2,0]},
   {'id':['K',2],'a':0,'q':0,'k':1,'target':2,'scope':[1],'priority':[1]}]


class Soundness(unittest.TestCase):
    def test_monotone_physical_update(self):
        for e in E:
            for state in product(range(3),repeat=3):
                for i in range(3):
                    if state[i]==2:continue
                    low=list(state);high=list(state);high[i]+=1;B.update(low,e,2);B.update(high,e,2)
                    self.assertTrue(all(a<=b for a,b in zip(low,high)))

    def test_greatest_fixed_point_is_maximal(self):
        z=toy(E);r=B.cyclic_events(z,E,2);top=r['initial_greatest_fixed_point']
        for state in product(range(3),repeat=3):
            after,_=B.sweep(state,E,2)
            if after==list(state):self.assertTrue(all(a<=b for a,b in zip(state,top)))

    def test_no_free_cyclic_starting_credit(self):
        e={'id':['B',1,1],'a':0,'q':1,'k':0,'target':1,'scope':[0],'priority':[0]};z=toy([e]);r=B.cyclic_events(z,[e],9)
        self.assertEqual(r['initial_greatest_fixed_point'][0],0);self.assertEqual(r['paid'],0);self.assertEqual(len(r['failures']),1)

    def test_cut_independence(self):
        z=toy(E);r=B.cyclic_events(z,E,2);s=r['initial_greatest_fixed_point'].copy()
        for cut in range(len(E)):
            rotated=E[cut:]+E[:cut];rr=B.cyclic_events(z,rotated,2)
            prefix,_=B.sweep(s,E[:cut],2);self.assertEqual(prefix,rr['initial_greatest_fixed_point'])

    def test_repetition_creates_no_new_balance(self):
        z=toy(E);a=B.cyclic_events(z,E,2);b=B.cyclic_events(toy(E*3),E*3,2)
        self.assertEqual(a['initial_greatest_fixed_point'],b['initial_greatest_fixed_point']);self.assertEqual(b['paid'],3*a['paid'])

    def test_priority_strands_credit(self):
        _,r,_=C.local_fixed(8,8,8)
        self.assertEqual((r['a_new'],r['b_new'],r['retired']),(7,8,8));self.assertLess(2*r['a_new']+r['b_new'],24)

    def test_original_U_counterexamples_verified(self):
        r=B.K.load(B.HERE/'INDEPENDENT_VERIFICATION.json');self.assertTrue(r['passed']);self.assertTrue(all(v['all_unpaid_are_genuine_original_U'] for v in r['witnesses']))
        self.assertEqual(r['witnesses'][0]['policy']['unpaid'],2);self.assertEqual(r['witnesses'][1]['policy']['unpaid'],129)

    def test_more_demand_cannot_help_same_policy(self):
        for state in product(range(3),repeat=3):
            e=E[1];low=list(state);high=list(state);B.update(low,e,2);free=dict(e,q=0);B.update(high,free,2)
            self.assertTrue(all(a<=b for a,b in zip(low,high)))


if __name__=='__main__':unittest.main()

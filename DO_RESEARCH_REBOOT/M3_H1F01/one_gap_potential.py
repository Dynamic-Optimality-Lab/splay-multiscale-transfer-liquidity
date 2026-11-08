"""Verified physical one-gap joint table; old corrected value outside its exact sector/domain."""
import json,sys
from array import array
from pathlib import Path
from build_fragment import BASE,load
from compensated_potential import CompensatedPotential

class OneGapPotential:
    def __init__(self):
        self.old=CompensatedPotential();self.c,self.a=load()
        audit=json.loads((BASE/'edge_audit.json').read_text());assert audit['status']=='FINITE_EXACT_VERIFIED'
        self.p=array('i');self.p.frombytes((BASE/'potential.bin').read_bytes())
        if self.c['byteorder']!=sys.byteorder:self.p.byteswap()
        self.ids={tuple(tuple(r) for r in s):i for i,s in enumerate(self.c['shadows'])}
        self.local={ai:j for r in range(9) for j,ai in enumerate(self.c['shadows_by_root'][str(r)])}
    def inspect(self,s):
        old=self.old.inspect(s);u=None;value=old['compensated_joint']
        chi=s['b']['kr'][8]==0 and s['b']['rr'][8]==19
        if chi and s['mu']==341 and s['sigma']==[1]+[0]*9:
            ai=self.ids.get(tuple(tuple(r) for r in s['alpha']));bi=old['core_tree_id']
            base=self.c['B_bases'][bi]
            if ai is not None and base>=0 and self.c['shadows'][ai][0]==[0,1,s['b']['root']]:
                u=base+self.local[ai];value=self.p[u]
                assert self.a['ordinary_b'][u]==bi and self.a['ordinary_a'][u]==ai
        assert -2<=value<=old['compensated_joint'] and value<=-old['psi']
        return {**old,'table_node':u,'one_gap_joint':value}
    def __call__(self,s):return self.inspect(s)['one_gap_joint']

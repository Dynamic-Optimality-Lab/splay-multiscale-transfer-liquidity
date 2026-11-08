import sys
sys.path.insert(0,'DO_RESEARCH_REBOOT/M3_GAPINT01')
"""All-population single-gap1/8 potential; mirror only mathematical low profiles."""
import json,sys
from array import array
from pathlib import Path
from framework_v2 import rho,reflect_alpha,reflect_tree,V
sys.path.insert(0,'DO_RESEARCH_REBOOT/M3_H2R01')
from terminal_potential import core_tree
BASE=Path('DO_RESEARCH_REBOOT/M3_GAPINT02')
class InteriorPotential:
    def __init__(self):
        self.c=json.loads((BASE/'catalog.json').read_text());self.p=array('i');self.p.frombytes((BASE/'potential.bin').read_bytes())
        if self.c['byteorder']!=sys.byteorder:self.p.byteswap()
        bc=json.loads(Path('DO_RESEARCH_REBOOT/M3_LDR01/negative_run_census.json').read_text());self.trees=[V.from_serial(r['tree']) for r in bc['nodes']];self.bid={t:i for i,t in enumerate(self.trees)}
        self.sid={tuple(tuple(r) for r in s):i for i,s in enumerate(self.c['shadows'])};self.local={ai:j for r in range(9) for j,ai in enumerate(self.c['shadows_by_root'][str(r)])}
    def inspect(self,s):
        support=[i for i,n in enumerate(s['sigma']) if n]
        if not(0<=s['mu']<512 and s['mu'].bit_count()==5 and len(support)<=1 and all(0<=n<=266 for n in s['sigma']) and (not support or support[0] in (self.c['gap'],9-self.c['gap'])) and s['b']['kr'][8]==0 and s['b']['rr'][8]==19):raise ValueError('outside single-gap family')
        a=s['alpha'];b=s['b'];mir=bool(support and support[0]!=self.c['gap'])
        if b['root'] not in range(9) or not a[0][1] or a[0][2]!=b['root']:return {'value':0,'rule':'boundary_zero','table_node':None}
        try:
            core=core_tree(b);core=reflect_tree(core) if mir else core
            image=rho(reflect_alpha(a) if mir else a,self.c['gap']);ai=self.sid[image];bi=self.bid[core];u=self.c['B_bases'][bi]+self.local[ai]
        except (ValueError,KeyError,AssertionError):return {'value':0,'rule':'invalid_low_state_zero','table_node':None}
        v=self.p[u];assert -2<=v<=-self.c['psi'][bi]<=0
        return {'value':v,'rule':'single_gap_profile','reflected':mir,'table_node':u,'core_tree_id':bi,'psi':self.c['psi'][bi],'image_alpha':[list(r) for r in image]}
    def __call__(self,s):return self.inspect(s)['value']

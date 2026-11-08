"""Mask-independent fixed-signature potential; original graph vertices retained."""
import sys,json
from pathlib import Path
from array import array
sys.path[:0]=['DO_RESEARCH_REBOOT/M3_AER01','DO_RESEARCH_REBOOT/M3_H2R01']
from empty_interval_potential import rho,S,V
from terminal_potential import core_tree
BASE=Path('DO_RESEARCH_REBOOT/M3_MSK01/replay_v2')
class UniformPotential:
    def __init__(self):
        self.c=json.loads((BASE/'catalog.json').read_text());self.p=array('i');self.p.frombytes((BASE/'potential.bin').read_bytes())
        if self.c['byteorder']!=sys.byteorder:self.p.byteswap()
        bc=json.loads(Path('DO_RESEARCH_REBOOT/M3_LDR01/negative_run_census.json').read_text())
        self.trees=[V.from_serial(r['tree']) for r in bc['nodes']];self.ids={t:i for i,t in enumerate(self.trees)}
        self.sid={tuple(tuple(r) for r in a):i for i,a in enumerate(self.c['shadows'])}
        self.local={ai:j for r in range(9) for j,ai in enumerate(self.c['shadows_by_root'][str(r)])}
    def inspect(self,s):
        if not(0<=s['mu']<512 and s['mu'].bit_count()==5 and s['sigma']==[1]+[0]*9 and s['b']['kr'][8]==0 and s['b']['rr'][8]==19):raise ValueError('outside sector')
        b=s['b'];a=s['alpha']
        if b['root'] not in range(9) or not a[0][1] or a[0][2]!=b['root']:return {'value':0,'rule':'boundary_zero','table_node':None}
        try:
            image=rho(a);ai=self.sid[image];bi=self.ids[core_tree(b)];u=self.c['B_bases'][bi]+self.local[ai]
        except (ValueError,KeyError,AssertionError):return {'value':0,'rule':'invalid_low_state_zero','table_node':None}
        value=self.p[u];assert -2<=value<=-self.c['psi'][bi]<=0
        return {'value':value,'rule':'uniform_one_gap','table_node':u,'core_tree_id':bi,'psi':self.c['psi'][bi],'image_alpha':[list(r) for r in image]}
    def __call__(self,s):return self.inspect(s)['value']

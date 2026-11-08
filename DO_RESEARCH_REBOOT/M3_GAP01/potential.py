"""Uniform gap0 population potential on the frozen shared state."""
import sys,json
from pathlib import Path
from array import array
sys.path[:0]=['DO_RESEARCH_REBOOT/M3_GAP01','DO_RESEARCH_REBOOT/M3_H2R01']
from core_refinement_v2 import rho,V
from terminal_potential import core_tree
BASE=Path('DO_RESEARCH_REBOOT/M3_GAP01')
class GapPotential:
    def __init__(self):
        self.c=json.loads((BASE/'catalog.json').read_text());self.p=array('i');self.p.frombytes((BASE/'potential.bin').read_bytes())
        if self.c['byteorder']!=sys.byteorder:self.p.byteswap()
        bc=json.loads(Path('DO_RESEARCH_REBOOT/M3_LDR01/negative_run_census.json').read_text());self.trees=[V.from_serial(r['tree']) for r in bc['nodes']];self.bid={t:i for i,t in enumerate(self.trees)}
        self.sid={tuple(tuple(r) for r in s):i for i,s in enumerate(self.c['shadows'])};self.local={ai:j for r in range(9) for j,ai in enumerate(self.c['shadows_by_root'][str(r)])}
    def inspect(self,s):
        if not(0<=s['mu']<512 and s['mu'].bit_count()==5 and 0<=s['sigma'][0]<=266 and not any(s['sigma'][1:]) and s['b']['kr'][8]==0 and s['b']['rr'][8]==19):raise ValueError('outside gap0 sector')
        a=s['alpha'];b=s['b']
        if b['root'] not in range(9) or not a[0][1] or a[0][2]!=b['root']:return {'value':0,'rule':'boundary_zero','table_node':None}
        try:
            im=rho(a);ai=self.sid[im];bi=self.bid[core_tree(b)];u=self.c['B_bases'][bi]+self.local[ai]
        except (ValueError,KeyError,AssertionError):return {'value':0,'rule':'invalid_low_shape_zero','table_node':None}
        value=self.p[u];assert -2<=value<=-self.c['psi'][bi]<=0
        return {'value':value,'rule':'population_opaque','table_node':u,'core_tree_id':bi,'psi':self.c['psi'][bi],'image_alpha':[list(r) for r in im]}
    def __call__(self,s):return self.inspect(s)['value']

"""Existing low tables on every single-gap support, without a chi8 restriction.

Only mathematical core/A profiles are reflected. Raw high states, paths,
sentinel scans and private source witnesses are never reflected here.
Only one finite table is resident at a time.
"""
import importlib.util,sys
from pathlib import Path
sys.path[:0]=['DO_RESEARCH_REBOOT/M3_GAPINT01','DO_RESEARCH_REBOOT/M3_GAP01',
             'DO_RESEARCH_REBOOT/M3_H2R01']
from framework_v2 import reflect_alpha,reflect_tree,rho as rho_interior
from core_refinement_v2 import rho as rho_outer
from terminal_potential import core_tree

class OutsidePotential:
    def __init__(self):
        self.active=None;self.table=None

    def activate(self,g):
        if g==self.active:return
        self.table=None
        folder='M3_GAP01' if g==0 else f'M3_GAPINT0{g}'
        name='potential_v3.py' if g==2 else 'potential.py'
        path=Path('DO_RESEARCH_REBOOT')/folder/name
        spec=importlib.util.spec_from_file_location(f'out01_table_{g}',path)
        mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
        self.table=mod.GapPotential() if g==0 else mod.InteriorPotential()
        self.active=g

    def inspect(self,s):
        sig=s['sigma'];support=[g for g,n in enumerate(sig) if n]
        if not (len(sig)==10 and len(support)<=1 and all(0<=n<=266 for n in sig)
                and 0<=s['mu']<512 and s['mu'].bit_count()==5):
            raise ValueError('outside certified single-gap signature domain')
        g=support[0] if support else 0;mirror=g>=5;canonical=9-g if mirror else g
        a=s['alpha'];b=s['b']
        if b['root'] not in range(9) or not a[0][1] or a[0][2]!=b['root']:
            return {'value':0,'rule':'non_low_boundary_zero'}
        self.activate(canonical);p=self.table
        try:
            core=core_tree(b);core=reflect_tree(core) if mirror else core
            a=reflect_alpha(a) if mirror else a
            image=rho_outer(a) if canonical==0 else rho_interior(a,canonical)
            ai=p.sid[image];bi=p.bid[core];u=p.c['B_bases'][bi]+p.local[ai]
        except (ValueError,KeyError,AssertionError):
            return {'value':0,'rule':'invalid_low_image_zero'}
        value=p.p[u];assert -2<=value<=-p.c['psi'][bi]<=0
        return {'value':value,'rule':'fixed_gap_low_table','gap':g,'reflected':mirror,
                'table_gap':canonical,'table_node':u,'psi':p.c['psi'][bi]}

    def __call__(self,s):return self.inspect(s)['value']

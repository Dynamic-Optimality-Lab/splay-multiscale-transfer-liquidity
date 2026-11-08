"""Explicit range-two joint correction; no potential fitting and no new state."""
import sys,json
from pathlib import Path
sys.path.insert(0,'DO_RESEARCH_REBOOT/M3_H2R01')
from terminal_potential import CappedPotential

class CompensatedPotential:
    def __init__(self):
        self.old=CappedPotential()
        certificate=json.loads(Path('DO_RESEARCH_REBOOT/M3_FRC01/compensation_certificate.json').read_text())
        assert certificate['status']=='COMPLETE'
        self.R=frozenset(certificate['R'])
    def inspect(self,s):
        a=self.old.inspect(s)
        chi=s['b']['kr'][8]==0 and s['b']['rr'][8]==19
        active=chi and s['sigma'][0]>0 and a['core_tree_id'] in self.R
        if active:assert a['psi']==0 and a['old_joint']==a['capped_joint']==0
        value=a['capped_joint']-int(active)
        assert -2<=value<=0
        return {**a,'patch_active':active,'compensated_joint':value}
    def __call__(self,s):return self.inspect(s)['compensated_joint']
    def theta_ordinary(self,s):
        chi=s['b']['kr'][8]==0 and s['b']['rr'][8]==19
        return -3+self(s) if chi else 0

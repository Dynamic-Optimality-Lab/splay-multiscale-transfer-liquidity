"""Deterministic fringe-leaf refinement pullback of H1F01; original state and table unchanged."""
import sys,json
sys.path.insert(0,'DO_RESEARCH_REBOOT/M3_H1F01')
from one_gap_potential import OneGapPotential
from certify_refinement import rho,BASE
class PortPotential:
    def __init__(self):
        self.old=OneGapPotential()
        cert=json.loads((BASE/'refinement_certificate.json').read_text());assert cert['status']=='COMPLETE'
    def inspect(self,s):
        old=self.old.inspect(s);r,rule=rho(s['alpha']);value=old['one_gap_joint'];image=old['table_node'];refined=None
        chi=s['b']['kr'][8]==0 and s['b']['rr'][8]==19
        if chi and s['mu']==341 and s['sigma']==[1]+[0]*9 and r is not None and rule!='identity':
            test={**s,'alpha':[list(row) for row in r]};ri=self.old.inspect(test)
            if ri['table_node'] is not None:
                refined=test['alpha'];value=ri['one_gap_joint'];image=ri['table_node']
        assert -2<=value<=0 and value<=-old['psi']
        return {**old,'refinement_rule':rule,'refined_alpha':refined,
                'image_table_node':image,'port_joint':value}
    def __call__(self,s):return self.inspect(s)['port_joint']

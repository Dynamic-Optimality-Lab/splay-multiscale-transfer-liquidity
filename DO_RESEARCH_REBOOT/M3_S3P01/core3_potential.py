"""State-only singleton S3 refinement composed with the existing fringe refinement."""
import json,sys
sys.path[:0]=['DO_RESEARCH_REBOOT/M3_G0P01','DO_RESEARCH_REBOOT/M3_H1F01']
from port_potential import PortPotential
from certify_core3_v2 import rho,BASE
class Core3Potential:
    def __init__(self):
        self.old=PortPotential();self.physical=self.old.old
        cert=json.loads((BASE/'core3_certificate.json').read_text());assert cert['status']=='COMPLETE'
    def inspect(self,s):
        old=self.old.inspect(s);r,rule=rho(s['alpha']);value=old['port_joint'];image=old['image_table_node'];refined=None
        chi=s['b']['kr'][8]==0 and s['b']['rr'][8]==19
        if chi and s['mu']==341 and s['sigma']==[1]+[0]*9 and r is not None and 'S3_' in rule:
            ss={**s,'alpha':[list(row) for row in r]};ri=self.physical.inspect(ss)
            if ri['table_node'] is not None:
                value=ri['one_gap_joint'];image=ri['table_node'];refined=ss['alpha']
        assert -2<=value<=old['port_joint'] and value<=-old['psi']
        return {**old,'core3_rule':rule,'core3_refined_alpha':refined,
                'core3_image_node':image,'core3_joint':value}
    def __call__(self,s):return self.inspect(s)['core3_joint']

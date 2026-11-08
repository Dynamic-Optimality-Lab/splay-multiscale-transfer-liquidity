"""Capped joint correction: min(CHR01 joint value, complete core debt -psi)."""
import sys,json
from pathlib import Path
sys.path[:0]=['DO_RESEARCH_REBOOT/M3_CHR01','DO_RESEARCH_REBOOT/M3_PHI01','python/independent']
import splay as S
import verify_full_mixed as V
from verify_original_controls import Potential as JointPotential
CATALOG=Path('DO_RESEARCH_REBOOT/M3_LDR01/negative_run_census.json')

def core_tree(b):
    seen=set()
    def go(i):
        assert i<9 and i not in seen;seen.add(i);kids=[]
        for k,r in (('kl','rl'),('kr','rr')):
            kids.append(go(b[r][i]) if b[k][i]==0 and b[r][i]<9 else S.LEAF)
        return S.node(i,*kids)
    t=go(b['root']);assert seen==set(range(9));return t

class CappedPotential:
    def __init__(self):
        self.joint=JointPotential()
        c=json.loads(CATALOG.read_text())
        self.trees=[V.from_serial(n['tree']) for n in c['nodes']]
        self.ids={t:i for i,t in enumerate(self.trees)}
        self.psi=[n['psi'] for n in c['nodes']]
    def inspect(self,state):
        i=self.ids[core_tree(state['b'])];j=self.joint(state);debt=self.psi[i]
        value=min(j,-debt);assert -2<=value<=0 and value<=-debt
        return {'core_tree_id':i,'psi':debt,'old_joint':j,'capped_joint':value}
    def __call__(self,state):return self.inspect(state)['capped_joint']

"""Boundary witness: hidden gap0 population below the canonical depth-six prefix."""
import sys,json,time
from pathlib import Path
sys.path[:0]=['DO_RESEARCH_REBOOT/M3_H1F01','DO_RESEARCH_REBOOT/M3_PHI01','python/independent']
import splay as S
import verify_full_mixed as V
from one_gap_potential import OneGapPotential
from PC_TYPED_DAG import DAG
from STRICT_LOW_COMPILER import build_slow
from build_fragment import BASE
OUT=BASE/'hidden_fringe_control.json'
OriginalAModel=V.AModel
class PhysicalRanks(OriginalAModel):
    def __init__(self,t,Sset):
        super().__init__(t,Sset)
        self.V=S.inorder(t);self.rank={k:i for i,k in enumerate(self.V)}
        self.lo={0:0};self.hi={0:136}
        for sid,v in self.slots.items():
            if sid==0:continue
            p=v['par'];key=self.slots[p]['key']
            self.lo[sid]=self.lo[p] if v['side']==0 else self.rank[key]+1
            self.hi[sid]=self.rank[key] if v['side']==0 else self.hi[p]
def main():
    assert not OUT.exists();start=time.process_time();V.start=start;V.MU=341;P=OneGapPotential()
    A=S.LEAF
    for x in range(-1,9):A=S.node(x,A,S.LEAF)
    assert S.lookup(A,-1)[1]==9
    B=next(t for t in P.old.old.trees if t[1]==8 and S.lookup(t,6)[1]==4)
    B=V.insert(B,-1);d=DAG();L=build_slow(d,'MXL')
    am=PhysicalRanks(A,set(range(9)))
    assert -1 not in {v['key'] for v in am.slots.values()}
    assert am.V==list(range(-1,9)) and am.sig==[1]+[0]*9
    assert sum(z[0] for z in am.pz.values())==1
    # Only the witness constructor is supplied this full physical rank map.
    # The original low DAG object and every compiler predicate remain intact.
    V.AModel=PhysicalRanks
    try:ac,bc,r=V.low(d,L,A,B,[['K',6]],True,'hidden_fringe_physical_rank_prefix')
    finally:V.AModel=OriginalAModel
    a=P.inspect(r['source']);b=P.inspect(r['destination']);red=r['w']-b['one_gap_joint']+a['one_gap_joint']
    assert red>=0 and a['table_node'] is not None and b['table_node'] is not None
    assert r['H']==1 and r['q']==2 and r['w']==0
    r.update(potential_source=a,potential_destination=b,joint_reduced_weight=red,
             full_physical_rank_map=am.rank,fringe_depth=9,fringe_is_hidden=True)
    result={'status':'COMPLETE','original_low_root':True,'low_DAG_nodes':len(d.nodes),
            'fringe_depth':9,'full_physical_ranks_assigned':True,'population_in_port':True,
            'joint_reduced_weight':red,'cpu_seconds':round(time.process_time()-start,3),'record':r}
    assert result['cpu_seconds']<300
    with OUT.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k!='record'},indent=2),flush=True)
if __name__=='__main__':main()

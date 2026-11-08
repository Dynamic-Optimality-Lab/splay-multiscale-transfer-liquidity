"""Full original low roots for the three fringe obstructions and two zero controls."""
import sys,json,time
from pathlib import Path
sys.path[:0]=['DO_RESEARCH_REBOOT/M3_H2R01','DO_RESEARCH_REBOOT/M3_PHI01',
 'DO_RESEARCH_REBOOT/M2_SEP01','python/independent',
 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER',
 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE']
import splay as S
import verify_full_mixed as F
from PC_TYPED_DAG import DAG
from STRICT_LOW_COMPILER import build_slow
from terminal_potential import CappedPotential
OUT=Path('DO_RESEARCH_REBOOT/M3_H2R01/original_fringe_controls.json')

def ashape(r,x):
    z=S.LEAF
    if x<r:
        left=S.node(x,S.balanced(range(x)),S.balanced(range(x+1,r)))
        return S.node(r,S.node(-1,z,left),S.balanced(range(r+1,9)))
    if x>r:
        right=S.node(x,S.balanced(range(r+1,x)),S.balanced(range(x+1,9)))
        return S.node(r,S.node(-1,z,S.balanced(range(r))),right)
    return S.node(r,S.node(-1,z,S.balanced(range(r))),S.balanced(range(r+1,9)))

def main():
    assert not OUT.exists();start=time.process_time();P=CappedPotential();d=DAG();L=build_slow(d,'MXL')
    assert len(d.nodes)<4000000
    kernel=json.loads(Path('DO_RESEARCH_REBOOT/M3_H2R01/fringe_kernel_certificate.json').read_text())
    records=[]
    def add(A,B,word,mu,label,expected):
        assert time.process_time()-start<300,'UNKNOWN: original fringe gate'
        F.MU=mu
        ac,bc,record=F.low(d,L,A,B,word,True,label)
        assert record['H']==2 and record['source']['sigma'][0]==1
        ps=P.inspect(record['source']);pt=P.inspect(record['destination'])
        residual=record['w']-(pt['capped_joint']-ps['capped_joint'])
        assert residual==expected,(label,residual)
        record.update(potential_source=ps,potential_destination=pt,reduced_weight=residual,
                      source_credit_is_actual_preterminal=True)
        records.append(record)
    mu=sum(1<<i for i in (0,1,2,3,5))
    for row in kernel['failures']:
        B=F.insert(P.trees[row['entry_core']],-1);A=ashape(B[1],row['target'])
        add(A,B,[('K',-1),('K',row['target'])],mu,'fringe_plus1_exception_'+str(row['entry_core']),-1)
        rec=records[-1]
        assert rec['q']==3 and rec['w']==1
        assert rec['potential_source']['psi']==2 and rec['potential_destination']['psi']==0
        assert rec['potential_source']['core_tree_id']==row['entry_core']
        assert rec['potential_destination']['core_tree_id']==row['exit_core']
        assert rec['B_event_boundaries'][1]['root']==9
    z=S.LEAF
    A=S.node(8,S.node(-1,z,S.node(0,z,S.balanced(range(1,8)))),z)
    B=P.trees[next(i for i,t in enumerate(P.trees) if S.lookup(t,0)[1]==8)]
    # The terminal depth-eight tree must have root eight, for A/B root synchronization.
    assert B[1]==8
    add(A,F.insert(B,-1),[('D',-1),('K',0)],341,'positive_signature_Gamma0_zero',2)
    row=next(r for r in kernel['rows'] if r['gap0_childless_at_exit'] and r['w']==0
             and P.trees[r['entry_core']][1] in (0,1,2,3,5) and r['target'] in (0,1,2,3,5))
    B=F.insert(P.trees[row['entry_core']],-1)
    add(ashape(B[1],row['target']),B,[('K',-1),('K',row['target'])],mu,
        'positive_signature_Gamma1_zero',row['residual'])
    assert len(records)==5 and sum(r['reduced_weight']<0 for r in records)==3
    result={'status':'COMPLETE','queries':len(records),'low_DAG_nodes':len(d.nodes),
            'refuted_plus1_inequalities':3,'passing_zero_controls':2,
            'cpu_seconds':round(time.process_time()-start,3),'records':records}
    assert result['cpu_seconds']<300
    with OUT.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k!='records'}),flush=True)
if __name__=='__main__':main()

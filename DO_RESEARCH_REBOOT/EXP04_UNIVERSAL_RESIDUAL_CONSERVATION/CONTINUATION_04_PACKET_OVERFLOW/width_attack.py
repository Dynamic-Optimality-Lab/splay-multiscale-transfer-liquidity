from campaign4 import *
from fast_physics import FullTree,physical_replay,skeleton_cost
from packet_payments import test
from packed_states import install,materialize
import gc

def construct(p,left=256,right=256):
    base=both_oscillations(p,left,right,'bitreverse',right_low=2)
    m=len(base['initial_B']['children']);n=m+2
    phi=lambda x:x if x<=4 else x+2;active=[phi(x) for x in range(1,m+1)]
    st={'root':n,'children':{str(k):[k-1 if k>1 else None,None] for k in range(1,n+1)}}
    a=FullTree(st);other=FullTree(st)
    for x in active[-2::-1]:a.splay(x,other,'A')
    diag=a.state();h0=2*m+2*left+3
    word=[[tag,phi(x)] for tag,x in base['operations']]
    assert word[h0-1]==['K',7]
    word=word[:h0-2]+[['D',6]]+word[h0-2:];word[h0]=['K',6]
    word+=ops('K',range(1,n+1))+ops('K',active[-2::-1])
    return {'name':f'C04_sparse_p{p}_l{left}_r{right}','p':p,
        'family':'sparse-private simultaneous-column scaling',
        'initial_A':diag,'initial_B':diag,'diagonal_initial':diag,'reaching_prefix':[],
        'operations':word,'active_keys':active,'target_consumer':h0+1,
        'closure':'Actual full increasing scan makes left vine; actual decreasing active sweep recreates the saved diagonal.'}

if __name__=='__main__':
    meter=Meter('width_attack');sources=[];rows=[]
    pool,restore=install(Tree)
    for p in (8,9):
        s=construct(p);f=physical_replay(s)
        periodic=[skeleton_cost(f,variant=v) for v in ('raw','G','H')]
        s.update(A=f['A'],Q_B=f['Q_B']);sources.append(s)
        row={'source':s['name'],'population':len(s['initial_B']['children']),'operations':len(s['operations']),
            'A':f['A'],'Q_B':f['Q_B'],'original_Pi_classified':False,
            'tested_cut1_periodic':[{k:v for k,v in z.items() if k!='retained_original_operations'} for z in periodic],
            'physical_target_B_parents':f['rows'][s['target_consumer']-1]['B_steps']}
        positive=next((z for z in periodic if z['eligible_periodic']),None)
        row['R_overflow_empty_by_positive_periodic_plus_cheap_quota']=positive is not None
        row['Pi_unrun_is_not_zero']=True
        rows.append(row);write('SOURCE_WITNESSES.json',sources);write('WIDTH_RESULTS.json',rows)
        print('physical',p,'N',row['population'],'A',f['A'],'positive periodic',positive is not None,flush=True)
        if p==8:
            r=Replay(s);star,_,_=original_residual(r);q=test(s,star)
            s.update(trace_hash=digest(r.events),closing_A=materialize(r.a.state()),closing_B=materialize(r.b.state()))
            row.update(original_Pi_classified=True,original_R_star=star,prehybrid_star_quota=q,
                original_U={str(k):v for k,v in r.U.items()},original_pairs=r.pairs,
                original_independent_operation_checks=r.independent_checks)
            print('full Pi',p,'Rstar',len(star),'widths',q['width_by_KEEP'],'overflow',len(q['literal_overflow']),flush=True)
            write('SOURCE_WITNESSES.json',sources);write('WIDTH_RESULTS.json',rows)
            del r;pool.clear();gc.collect()
        del f;pool.clear();gc.collect()
    restore();meter.success=True;meter.details.update(complete_sources=len(sources))

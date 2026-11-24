from campaign3b import *
from fast_physics import FullTree,physical_replay
from accounting import audit
from new_payments import intern_original_states,compact_trace
from packet_payments import test


if __name__=='__main__':
    meter=Meter('sparse_private_width');pool=intern_original_states();p=7
    base=both_oscillations(p,256,256,'bitreverse',right_low=2);m=len(base['initial_B']['children']);n=m+2
    phi=lambda x:x if x<=4 else x+2;active=[phi(x) for x in range(1,m+1)]
    left={'root':n,'children':{str(k):[k-1 if k>1 else None,None] for k in range(1,n+1)}}
    a=FullTree(left);other=FullTree(left)
    for x in active[-2::-1]:a.splay(x,other,'A')
    diag=a.state();assert all(set(Tree(diag).path(x))<=set(active) for x in active)
    h0=2*m+2*256+3;private=6
    word=[[tag,phi(x)] for tag,x in base['operations']]
    assert word[h0-1]==['K',7]
    word=word[:h0-2]+[['D',private]]+word[h0-2:];word[h0]=['K',private]
    word+=ops('K',range(1,n+1))+ops('K',active[-2::-1])
    s={'name':'C3B_sparse_private_p7','family':'unbounded_active_support_with_one_two_key_private_gap',
        'initial_A':diag,'initial_B':diag,'diagonal_initial':diag,'reaching_prefix':[],
        'operations':word,'active_keys':active,'private_keys':[5,6],'p':p,
        'target_consumer':h0+1,'reachability':'common diagonal, empty prefix',
        'parametric_domain':'all p>=4; active size2^(p+2)+1 and physical size2^(p+2)+3; genuine full restoration always included'}
    f=physical_replay(s);r=Replay(s);star,_,_=original_residual(r);a=audit(r,star)
    s.update(A=r.A,Q_B=r.Q,trace_hash=digest(r.events),closing_A=r.a.state(),closing_B=r.b.state())
    quota=test(s,star);row={'source':s['name'],'population':n,'A':r.A,'Q_B':r.Q,
        'original_R_star':star,'original_Pi_classification':True,'ordered_accounting':a,
        'original_R_star_quota':quota,'independent_original_operations':r.independent_checks,
        'primary_R_upper_escape':False}
    write('WIDTH_SOURCE.json',s);write('WIDTH_RESULT.json',row)
    if quota['literal_overflow']:compact_trace(r,star,'WIDTH_FULL_TRACE.json');row['trace_file']='WIDTH_FULL_TRACE.json';write('WIDTH_RESULT.json',row)
    print('N',n,'A',r.A,'Rstar',len(star),'target',s['target_consumer'],
        'widths',[z for z in quota['width_by_KEEP'] if z['h']==s['target_consumer']],
        'quota overflow',len(quota['literal_overflow']),flush=True)
    meter.success=True

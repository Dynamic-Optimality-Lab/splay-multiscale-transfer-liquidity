from campaign3 import *
from source_search import common_dilated
from fast_physics import physical_replay,skeleton_cost
from new_payments import intern_original_states,compact_trace
from epoch_payment import from_replay
import gc


def construct(p,stride=3,left=256,right=256,copies=1):
    base=both_oscillations(p,left,right,'bitreverse',right_low=2)
    m=len(base['initial_B']['children']);diag,active=common_dilated(m,stride)
    n=len(diag['children']);phi=lambda x:1+(x-1)*stride;private=phi(5)-1
    h0=2*m+2*left+3
    assert base['operations'][h0-1]==['K',5] and base['operations'][h0-2]==['K',2]
    body=[[tag,phi(x)] for tag,x in base['operations']]
    body=body[:h0-2]+[['D',private]]+body[h0-2:];body[h0]=['K',private]
    restore=ops('K',range(1,n+1))+ops('K',active[-2::-1]);period=body+restore
    return {'name':f'C03_private_p{p}_d{stride}_c{copies}','family':'parametric_private_upper_parent',
        'p':p,'stride':stride,'copies':copies,'initial_A':diag,'initial_B':diag,
        'diagonal_initial':diag,'reaching_prefix':[],'operations':period*copies,
        'active_keys':active,'private_hit':private,'first_target_consumer':h0+1,
        'one_copy_length':len(period),'reachability':'common diagonal, empty prefix',
        'closure_proof':'Each actual full increasing physical scan produces the left vine; decreasing active sweep restores the saved diagonal. All restoration is inside the measured word.'}


if __name__=='__main__':
    meter=Meter('private_scaling');sources=[];out=[];pool=intern_original_states()
    for p,copies,full in [(4,4,True),(5,1,True),(6,1,True),(7,1,False)]:
        s=construct(p,copies=copies);f=physical_replay(s)
        G=skeleton_cost(f,variant='G');H=skeleton_cost(f,variant='H')
        s.update(A=f['A'],Q_B=f['Q_B']);z={'source':s['name'],'population':len(s['initial_B']['children']),
            'A':f['A'],'Q_B':f['Q_B'],'operations':len(s['operations']),
            'G_periodic':G,'H_periodic':H,'full_physical_paired_closure':True,
            'original_Pi_classification':False,'simultaneous_escape_claimed':False}
        if full:
            r=Replay(s);star,_,_=original_residual(r);pay=from_replay(r,star)
            h=s['first_target_consumer'];gaps=keep_gaps(r)
            upper=[e for e in star if e['original_parent'][1]>2*gaps[e['consumer']]['A'] and
                    r.U[tuple(e['original_parent'])]['g'] not in r.boundaries[e['consumer']-1]['A_path'][:-1]]
            z.update(original_Pi_classification=True,original_R_star=star,upper_original_R_star=upper,
                first_use_payment=pay,independent_original_operations=r.independent_checks,
                target_parent_data=[{'event':e,'U':r.U[tuple(e['original_parent'])],
                    'A_gap':gaps[e['consumer']]['A'],'pre_A_path':r.boundaries[e['consumer']-1]['A_path'],
                    'pre_B_path':r.boundaries[e['consumer']-1]['B_path']} for e in upper])
            s.update(trace_hash=digest(r.events),closing_A=r.a.state(),closing_B=r.b.state())
            if p==6:
                compact_trace(r,star,'LARGE_UPPER_TRACE.json');z['trace_file']='LARGE_UPPER_TRACE.json'
            del r;pool.clear();gc.collect()
        sources.append(s);out.append(z);write('SCALING_SOURCES.json',sources);write('SCALING_RESULTS.json',out)
        print(s['name'],'N',z['population'],'A',z['A'],'R*',len(z.get('original_R_star',[])) if full else 'unrun',
            'upper',len(z.get('upper_original_R_star',[])) if full else 'unrun',
            'G funded',G['eligible_periodic'],flush=True)
        del f;pool.clear();gc.collect()
    meter.success=True;meter.details.update(new_complete_sources=len(sources),full_original_Pi_sources=3)

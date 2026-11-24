from campaign3 import *
from fast_physics import physical_replay
from new_payments import compact_trace,intern_original_states
from accounting import audit
import gc


if __name__=='__main__':
    meter=Meter('far_retarget_packets');sources=[];out=[];pool=intern_original_states()
    base=json.loads((C2/'PRIVATE_ANCESTOR_SOURCES.json').read_text())[0]
    for x in (60,78,96):
        s={k:v for k,v in base.items() if k not in ('A','Q_B','trace_hash','closing_A','closing_B')}
        s.update(name=f'C03_far_retarget_{x}',family='second_upper_parent_across_rigid_A_subtree',
            operations=base['operations'][:646]+[['D',x],['K',12],['K',x]]+base['operations'][646:],extra_private_target=x)
        f=physical_replay(s);s.update(A=f['A'],Q_B=f['Q_B']);r=Replay(s);star,_,_=original_residual(r)
        a=audit(r,star);row={'source':s['name'],'A':r.A,'Q_B':r.Q,'population':len(r.keys),
            'original_R_star':star,'original_Pi_classification':True,'ordered_accounting':a,
            'target_physics':[{'consumer':h,'A_gap':f['rows'][h-1]['A_gap'],
                'g52_upper_neutral_parents':[[h,j] for j,st in enumerate(f['rows'][h-1]['B_steps'],1)
                    if st[2]==52 and st[3]==(0,0) and j>2*f['rows'][h-1]['A_gap']]} for h in (646,649)],
            'independent_original_operations':r.independent_checks,'R_upper_escape_claimed':False}
        s.update(trace_hash=digest(r.events),closing_A=r.a.state(),closing_B=r.b.state())
        if a['first_use_E_C']['repeat_original_gaps']:
            compact_trace(r,star,'FAR_REPEAT_TRACE.json');row['trace_file']='FAR_REPEAT_TRACE.json'
        sources.append(s);out.append(row);write('FAR_RETARGET_SOURCES.json',sources);write('FAR_RETARGET_RESULTS.json',out)
        print(s['name'],'Rstar',len(star),'C',len(a['C_after_frozen_and_prefix']),
            'C repeats',len(a['first_use_E_C']['repeat_original_gaps']),flush=True)
        del r;pool.clear();gc.collect()
        if a['first_use_E_C']['repeat_original_gaps']:break
    meter.success=True;meter.details['new_original_sources']=len(sources)

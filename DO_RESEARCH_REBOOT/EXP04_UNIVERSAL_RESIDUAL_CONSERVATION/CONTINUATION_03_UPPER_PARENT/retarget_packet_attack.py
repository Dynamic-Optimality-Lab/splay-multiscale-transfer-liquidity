from campaign3 import *
from fast_physics import physical_replay
from new_payments import compact_trace,intern_original_states
from accounting import audit
import gc


if __name__=='__main__':
    meter=Meter('retarget_packets');sources=[];out=[];pool=intern_original_states()
    base=json.loads((C2/'PRIVATE_ANCESTOR_SOURCES.json').read_text())[0]
    assert base['operations'][645]==['K',12]
    for xs in ([24],[24,36,48]):
        piece=[];prev=12
        for x in xs:piece += [['D',x],['K',prev],['K',x]];prev=x
        s={k:v for k,v in base.items() if k not in ('A','Q_B','trace_hash','closing_A','closing_B')}
        s.update(name='C03_retarget_'+ '_'.join(map(str,xs)),family='rigid_A_packet_retargeting_with_root_repeat_helpers',
            operations=base['operations'][:646]+piece+base['operations'][646:],extra_private_targets=xs)
        f=physical_replay(s);s.update(A=f['A'],Q_B=f['Q_B'])
        physics=[]
        for h in [646]+[649+3*k for k in range(len(xs))]:
            z=f['rows'][h-1];physics.append({'consumer':h,'A_gap':z['A_gap'],'q':z['q'],'H_guard':z['guard_H'],
                'g52_upper_neutral_parents':[[h,j] for j,st in enumerate(z['B_steps'],1)
                      if st[2]==52 and st[3]==(0,0) and j>2*z['A_gap']]})
        r=Replay(s);star,_,_=original_residual(r);a=audit(r,star)
        row={'source':s['name'],'A':r.A,'Q_B':r.Q,'population':len(r.keys),'target_physics':physics,
             'original_R_star':star,'original_Pi_classification':True,'ordered_accounting':a,
             'independent_original_operations':r.independent_checks,'R_upper_escape_claimed':False}
        s.update(trace_hash=digest(r.events),closing_A=r.a.state(),closing_B=r.b.state())
        if a['first_use_E_C']['repeat_original_gaps']:
            compact_trace(r,star,'RETARGET_REPEAT_TRACE.json');row['trace_file']='RETARGET_REPEAT_TRACE.json'
        sources.append(s);out.append(row);write('RETARGET_SOURCES.json',sources);write('RETARGET_RESULTS.json',out)
        print(s['name'],'Rstar',len(star),'C',len(a['C_after_frozen_and_prefix']),
              'repeats',len(a['first_use_E_C']['repeat_original_gaps']),'no pivot',len(a['first_use_E_C']['A_demotion_free_key_original_gaps']),flush=True)
        del r;pool.clear();gc.collect()
    meter.success=True;meter.details['new_original_sources']=2

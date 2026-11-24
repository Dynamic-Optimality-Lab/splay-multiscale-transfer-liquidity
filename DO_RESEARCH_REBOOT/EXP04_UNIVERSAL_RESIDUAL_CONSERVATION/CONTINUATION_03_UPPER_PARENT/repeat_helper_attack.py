from campaign3 import *
from fast_physics import physical_replay
from epoch_payment import from_replay
from accounting import audit
from new_payments import intern_original_states,compact_trace
import gc


if __name__=='__main__':
    meter=Meter('repeat_aux_helpers');sources=[];out=[];pool=intern_original_states()
    base=next(s for s in json.loads((ROOT/'REPEAT_ATTACK_SOURCES.json').read_text()) if s['offset']==4)
    assert base['operations'][169]==['D',47]
    for helper in (56,66,48,641):
        s={k:v for k,v in base.items() if k not in ('A','Q_B','closing_A','closing_B','trace_hash')}
        s.update(name=f'C03_repeat_aux{helper}',family='repeat_packet_with_real_preceding_helper',
                 operations=base['operations'][:169]+[['D',helper]]+base['operations'][169:],auxiliary_helper=helper,
                 target_operations={k:v+1 for k,v in base['target_operations'].items()})
        f=physical_replay(s);s.update(A=f['A'],Q_B=f['Q_B']);physical=[]
        for h in (173,182):
            z=f['rows'][h-1]
            physical.append({'consumer':h,'A_gap':z['A_gap'],'q':z['q'],'hard_guard':z['guard_H'],
                'g166_neutral_upper':any(step[2]==166 and step[3]==(0,0) and j>2*z['A_gap']
                                        for j,step in enumerate(z['B_steps'],1))})
        row={'source':s['name'],'A':s['A'],'Q_B':s['Q_B'],'target_physics':physical,
             'original_Pi_classification':False,'R_upper_escape_claimed':False}
        if all(p['g166_neutral_upper'] for p in physical):
            r=Replay(s);star,_,_=original_residual(r);a=audit(r,star)
            row.update(original_Pi_classification=True,original_R_star=star,ordered_accounting=a,
                       independent_original_operations=r.independent_checks)
            s.update(trace_hash=digest(r.events),closing_A=r.a.state(),closing_B=r.b.state())
            repeat=a['first_use_E_C']['repeat_original_gaps']
            if repeat:compact_trace(r,star,'AUX_REPEAT_FULL_TRACE.json');row['trace_file']='AUX_REPEAT_FULL_TRACE.json'
            print('helper',helper,'Rstar',len(star),'C',len(a['C_after_frozen_and_prefix']),'C repeats',len(repeat),flush=True)
            del r;pool.clear();gc.collect()
        else:print('helper',helper,'failed targeted physical neutral upper predicate',flush=True)
        sources.append(s);out.append(row);write('REPEAT_HELPER_SOURCES.json',sources);write('REPEAT_HELPER_RESULTS.json',out)
        if row.get('ordered_accounting',{}).get('first_use_E_C',{}).get('repeat_original_gaps'):break
    meter.success=True;meter.details['new_complete_sources']=len(sources)

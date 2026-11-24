from campaign3 import *
from source_search import common_dilated
from fast_physics import physical_replay,skeleton_cost
from epoch_payment import from_replay
from new_payments import intern_original_states,compact_trace
from accounting import audit
import gc


if __name__=='__main__':
    meter=Meter('repeated_upper_attack')
    old=json.loads((REPO/'DO_RESEARCH_REBOOT/EXP01_PHYSICAL_RESIDUAL_DISCOVERY/EXP01_SOURCE_WITNESSES.json').read_text())['sources']
    base=next(s for s in old if s['name']=='DW_5_1_at31')
    diag,active=common_dilated(129,5);n=len(diag['children']);phi=lambda x:1+(x-1)*5
    sources=[];out=[];candidates=[]
    for offset in (1,2,3,4):
        body=[];targets={171:phi(11)-offset,179:phi(19)-offset};indices={}
        for h,(tag,x) in enumerate(base['operations'],1):
            if h+1 in targets:body.append(['D',targets[h+1]])
            body.append([tag,targets.get(h,phi(x))])
            if h in targets:indices[h]=len(body)
        body+=ops('K',range(1,n+1))+ops('K',active[-2::-1])
        s={'name':f'C03_DW5_repeat_private_offset{offset}','family':'private_deepened_W_repeat_packet',
            'initial_A':diag,'initial_B':diag,'diagonal_initial':diag,'reaching_prefix':[],
            'operations':body,'target_operations':indices,'active_keys':active,'offset':offset,
            'reachability':'common diagonal; all original helpers and exact physical restoration measured'}
        f=physical_replay(s);s.update(A=f['A'],Q_B=f['Q_B'])
        rows=[]
        for oldh,h in indices.items():
            r=f['rows'][h-1]
            rows.append({'original_W_consumer':oldh,'consumer':h,'A_gap':r['A_gap'],'q':r['q'],
                'G_guard':r['guard_G'],'H_guard':r['guard_H'],
                'g166_parents':[{'parent':[h,j],'signs':step[3],'j_gt_2A_gap':j>2*r['A_gap']}
                     for j,step in enumerate(r['B_steps'],1) if step[2]==phi(34)]})
        z={'source':s['name'],'A':f['A'],'Q_B':f['Q_B'],'population':n,'target_physics':rows,
            'G_periodic':skeleton_cost(f,variant='G'),'original_Pi_classification':False,
            'simultaneous_escape_claimed':False}
        candidates.append((sum(p['j_gt_2A_gap'] and p['signs']==(0,0) for r in rows for p in r['g166_parents']),offset))
        sources.append(s);out.append(z)
    write('REPEAT_ATTACK_SOURCES.json',sources);write('REPEAT_ATTACK_RESULTS.json',out)
    score,offset=max(candidates);print('best physical offset',offset,'hard neutral upper g166 parents',score,flush=True)
    if score:
        s=next(s for s in sources if s['offset']==offset);row=next(z for z in out if z['source']==s['name'])
        pool=intern_original_states();r=Replay(s);star,_,_=original_residual(r)
        z=from_replay(r,star);a=audit(r,star)
        row.update(original_Pi_classification=True,original_R_star=star,first_use_original_R_star=z,
            ordered_accounting=a,independent_original_operations=r.independent_checks)
        s.update(trace_hash=digest(r.events),closing_A=r.a.state(),closing_B=r.b.state())
        compact_trace(r,star,'REPEAT_ATTACK_FULL_TRACE.json')
        write('REPEAT_ATTACK_SOURCES.json',sources);write('REPEAT_ATTACK_RESULTS.json',out)
        print('original Rstar',len(star),'C',len(a['C_after_frozen_and_prefix']),
              'C repeats',len(a['first_use_E_C']['repeat_original_gaps']),
              'old hybrid funded',a['positive_old_periodic_certificate'] is not None,flush=True)
    meter.success=True;meter.details.update(new_complete_physical_sources=4,full_Pi_sources=int(bool(score)))

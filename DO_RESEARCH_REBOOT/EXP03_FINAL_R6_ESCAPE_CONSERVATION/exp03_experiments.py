"""Deterministic complete-source attacks and causal-episode certificates."""
from exp03_restart import *
from exp03_sources import corpus


def analyze(r,c,details=False):
    eps=actual_mismatch_episodes(r);restart=restart_analysis(r,c['unhandled'],eps)
    paid={digest(e['rho']) for e in restart['paid_original_gaps']}
    parents=parent_sets(c['unhandled']);records=[];lossloads=Counter();undefined=0
    for kind,ps in parents['sets'].items():
        for parent in ps:
            t,j=parent;u=r.U[(t,j)];row=r.boundaries[t-1];g=u['g'];x=row['x']
            hist=ancestry_history(r,g,x);loss=last_A_loss(r,hist,row['post_A_time'])
            if loss:lossloads[tuple(loss['id'])]+=1
            else:undefined+=1
            records.append({'type':kind,'original_parent':parent,'g':g,'target':x,
                'gap_multiplicity':sum(e['original_parent']==parent for e in c['unhandled']),
                'original_parent_certificate':u,'original_A_path':row['A_path'],'original_B_path':row['B_path'],
                'last_A_loss':loss,'ancestry_history':hist,'consumer_A':row['a'],
                'actual_episode':next(ep['id'] for ep in eps if t in ep['operations'])})
    assert sum(len(ep['A_StepEv']) for ep in eps)<=r.A
    byop={t:ep['id'] for ep in eps for t in ep['operations']}
    assert all(e['consumer'] in byop for e in c['unhandled'])
    causal=[];loads=Counter()
    for wi,w in enumerate(c['comparison']['windows']):
        demands=[e for e in c['unhandled'] if e['consumer'] in w['operations']]
        if not demands:continue
        cd=comparison_divergence(r,w)
        for ep in cd['episodes']:
            ep['unhandled_demands']=[e['rho'] for e in demands if e['consumer'] in ep['operations']]
            for step in {tuple(e) for e in ep['A_during_divergence']+ep['incoming_A_gap']}:loads[step]+=1
        causal.append({'window_index':wi,'causal_divergence':cd})
    remaining=[e for e in c['unhandled'] if digest(e['rho']) not in paid]
    out={'source':r.source['name'],'population':len(r.keys),'operations':len(r.ops),'family':r.source.get('family'),
        'A':r.A,'Q_B':r.Q,'R6':r.counts['R6'],'R6_other':len(c['other']),
        'trace_hash':digest(r.events),'complete_paired_closure':r.closed,'independent_operations':r.independent_checks,
        'S':sorted(r.S),'I':sorted(r.I),'orientation':orientation(r),'unhandled_events':c['unhandled'],
        'parent_interface':parents,'original_parents':records,'actual_mismatch_episodes':eps,
        'restart_comparison':restart,'remaining_after_restart':remaining,
        'last_loss_selector':{'undefined_parents':undefined,'maximum_primitive_load':max(lossloads.values(),default=0),
            'loads':{str(list(k)):v for k,v in lossloads.items()},'not_asserted_to_be_a_universal_payment':True},
        'comparison_divergence':causal,'raw_divergence_A_maximum_overlap':max(loads.values(),default=0)}
    if details:
        out['original_residual_inventory']=c['original_rows']
        out['complete_original_boundaries']=r.boundaries
        out['complete_original_events']=r.events
    return out


if __name__=='__main__':
    meter=Meter('experiments')
    archive=json.loads((ROOT/'EXP03_SOURCE_WITNESSES.json').read_text())
    names={s['source'] for s in json.loads((ROOT/'EXP03_UNHANDLED_PARENT_INVENTORY.json').read_text())['sources_with_unhandled_parents']}
    inherited=[];new=[];sources=corpus();checks=0
    for s in archive['inherited_sources']:
        if s['name'] not in names:continue
        r=Replay(s);c=current_classification(r);z=analyze(r,c)
        inherited.append(z);checks+=r.independent_checks
        print('inherited',s['name'],'A',r.A,'unhandled',len(c['unhandled']),'restart',z['restart_comparison']['paid_gap_count'],flush=True)
    for i,s in enumerate(sources):
        r=Replay(s);c=current_classification(r)
        z=analyze(r,c,details=s['name'] in ('Xprobe_p4_L3_hitNone_boundary1','closed_private_p4_L2_hits5_c1','multi_p4_c16_alternate'))
        s.update(trace_hash=digest(r.events),A=r.A,Q_B=r.Q)
        new.append(z);checks+=r.independent_checks
        print(f"new {i+1:02d}/{len(sources)}",s['name'],'A',r.A,'Q',r.Q,'unhandled',dict(Counter(e['type'] for e in c['unhandled'])),
            'restart',z['restart_comparison']['paid_gap_count'],'lossload',z['last_loss_selector']['maximum_primitive_load'],flush=True)
        write('EXP03_EXPERIMENT_CHECKPOINT.json',{'completed_new':i+1,'planned_new':len(sources),'latest':s['name']})
        # Save after every certified source; interruptions leave usable full witnesses.
        archive['new_sources']=sources[:i+1]
        write('EXP03_SOURCE_WITNESSES.json',archive)
        write('EXP03_CAUSAL_EPISODE_RESULTS.json',{'inherited_sources':inherited,'new_sources':new})
    meter.details.update(new_sources=len(new),inherited_sources_reanalyzed=len(inherited),independent_original_operations=checks,
        unhandled_new=sum(len(z['unhandled_events']) for z in new),remaining_new=sum(len(z['remaining_after_restart']) for z in new))
    meter.success=True
    print(json.dumps(meter.details,indent=2),flush=True)

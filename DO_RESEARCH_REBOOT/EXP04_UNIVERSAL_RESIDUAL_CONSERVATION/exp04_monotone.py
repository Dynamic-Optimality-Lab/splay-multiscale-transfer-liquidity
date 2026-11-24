from exp04_core import *


def monotone_windows(r,eps,d,strategy):
    windows=[];slots=set();used=set()
    for ep in eps:
        bs=[]
        for t in ep['operations']:
            tag,x=r.ops[t-1]
            if tag!='K':continue
            if not bs or bs[-1]['x']!=x:bs.append({'x':x,'ts':[]})
            bs[-1]['ts'].append(t)
        ranked={x:i for i,x in enumerate(sorted(r.S,reverse=d<0))};ranks=[ranked[b['x']] for b in bs]
        suffix=[0]*len(bs);best=[0]*len(r.S)
        if strategy=='earliest_feasible':
            for j in range(len(bs)-1,-1,-1):
                q=ranks[j];suffix[j]=1+max(best[q+1:],default=0);best[q]=max(best[q],suffix[j])
        i=0
        while i<len(bs):
            picks=[i];last=ranks[i]
            if strategy=='records':
                for j in range(i+1,len(bs)):
                    if ranks[j]>last:picks.append(j);last=ranks[j]
            elif strategy=='earliest_feasible':
                threshold=(len(r.S)+1)//2+1
                if suffix[i]<threshold:i+=1;continue
                need=threshold-1
                for j in range(i+1,len(bs)):
                    if ranks[j]>last and suffix[j]>=need:
                        picks.append(j);last=ranks[j];need-=1
                        if not need:break
                assert not need
            else:raise ValueError(strategy)
            targets=[bs[j]['x'] for j in picks]
            initial=r.boundaries[bs[i]['ts'][0]-1]['pre_B'];J=sorted(closure(Tree(initial),targets))
            if len(targets)<2 or len(J)>2*(len(targets)-1):i+=1;continue
            retained=[t for j in picks for t in bs[j]['ts']];all_ts=[t for b in bs[i:picks[-1]+1] for t in b['ts']]
            assert not used.intersection(all_ts);used.update(all_ts)
            witnesses=[]
            for u,v in zip(picks,picks[1:]):
                event=A_gap(r,bs[u]['ts'][-1],bs[v]['ts'][0]);slot=tuple(event[1:3])
                assert slot not in slots and event in ep['A_StepEv'];slots.add(slot);witnesses.append(event)
            windows.append({'episode':ep['id'],'direction':d,'strategy':strategy,'operations':all_ts,'retained':retained,
                'omitted':[t for t in all_ts if t not in set(retained)],'targets':targets,'ell':len(targets),'J':J,'domain_size':len(J),
                'initial_B':initial,'original_A_transition_witnesses':witnesses,'block_span':picks[-1]-i+1})
            i=picks[-1]+1
    assert sum(w['domain_size'] for w in windows)<=2*len(slots)<=2*r.A
    return windows


def monotone_analysis(r,events,eps):
    original=restart_module.restart_windows;systems=[];paid={};Aloads=Counter()
    try:
        for strategy in ('records','earliest_feasible'):
            for d in (1,-1):
                restart_module.restart_windows=lambda rr,ee:monotone_windows(rr,ee,d,strategy)
                z=restart_module.restart_analysis(r,events,eps);z.update(comparison_orientation=d,strategy=strategy,
                    bound='R_system <= 3 Q_shadow <=9 C_DF sum |J| <=18 C_DF A; skipped-rank dynamic-finger interface')
                systems.append(z)
                for e in z['paid_original_gaps']:paid.setdefault(digest(e['rho']),{**e,'orientation':d,'strategy':strategy})
                for w in z['windows']:
                    ranks={x:i for i,x in enumerate(w['J'])};travel=sum(abs(ranks[b]-ranks[a]) for a,b in zip(w['targets'],w['targets'][1:]))
                    assert travel<=len(w['J'])-1;w['rank_distance_sum']=travel
                    for event in w['original_A_transition_witnesses']:Aloads[tuple(event)]+=1
    finally:restart_module.restart_windows=original
    assert max(Aloads.values(),default=0)<=4
    return {'systems':systems,'paid':list(paid.values()),'maximum_A_witness_load':max(Aloads.values(),default=0),
        'bound_coefficient_CDF':72,'dependence':'classical dynamic-finger theorem with linear initialization; not a finite fitted constant'}


def rank_travel(r):
    rank={x:i for i,x in enumerate(sorted(r.S))};xs=[x for tag,x in r.ops if tag=='K']
    L=sum(abs(rank[x]-rank[xs[i-1]]).bit_length() for i,x in enumerate(xs)) if r.S else 0
    return {'cyclic_integer_log_rank_travel':L,'A':r.A,'certificate_L_le_2A':L<=2*r.A,
        'ratio':str(Fraction(L,r.A)) if r.A else None,'bound_Q_coefficient_CDF':5,'bound_R_star_coefficient_CDF':15}


def enriched(r,row):
    already={digest(e['rho']) for e in row['new_comparison']['paid']} if 'new_comparison' in row else set()
    after=[e for e in row['events'] if digest(e['rho']) not in already]
    eps,_=psi_episodes(r);m=monotone_analysis(r,after,eps);paid={digest(e['rho']) for e in m['paid']}
    remaining=[e for e in after if digest(e['rho']) not in paid];travel=rank_travel(r)
    cyclepaid=remaining if travel['certificate_L_le_2A'] else []
    return {'source':r.source['name'],'monotone_comparison':m,'after_monotone':remaining,'rank_travel':travel,
        'rank_certificate_paid':cyclepaid,'remaining':[] if cyclepaid else remaining}


if __name__=='__main__':
    meter=Meter('EXP04_monotone_inherited_new42')
    archive=json.loads((ROOT/'EXP04_SOURCE_WITNESSES.json').read_text())
    checkpoint=json.loads((ROOT/'EXP04_NEW_SOURCE_CHECKPOINT.json').read_text())
    inv=json.loads((ROOT/'EXP04_RESIDUAL_INVENTORY.json').read_text())
    rows=inv['inherited_sources']+json.loads((ROOT/'EXP04_NEW_RESULTS.json').read_text());by={s['source']:s for s in rows}
    out=[]
    for s in archive['inherited_sources']+checkpoint['sources']:
        row=by[s['name']]
        if not row['R_star']:continue
        r=Replay(s);z=enriched(r,row);out.append(z)
        print(s['name'],'aftermono',len(z['after_monotone']),'travel',z['rank_travel']['ratio'],'remaining',len(z['remaining']),flush=True)
        write('EXP04_MONOTONE_RESULTS.json',out);del r
    meter.details.update(sources=len(out),after_monotone=sum(len(z['after_monotone']) for z in out),remaining=sum(len(z['remaining']) for z in out));meter.success=True

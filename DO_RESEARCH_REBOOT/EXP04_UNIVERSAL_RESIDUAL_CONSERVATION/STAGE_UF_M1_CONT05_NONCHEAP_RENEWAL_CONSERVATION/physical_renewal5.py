from base5 import *
from catalog5 import entries,data
from physical1 import Edges

def audit(e):
    s=e['source'];p,rows,events,ds,vs,gs,A=data(e)
    ends={z['t']:z['end_time'] for z in rows};starts={z['t']:z['post_A_time'] for z in rows}
    T=rows[-1]['end_time'] if rows else 0
    aa,bb=Edges(s['initial_A']),Edges(s['initial_B']);initial=aa.code(),bb.code()
    reset=Counter();promos=Counter();targetpromos=Counter();oldcols={z['g'] for z in ds.values()}
    previous={};promotime={};completed={};firstafter={};losttargets=defaultdict(set);own={};count=Counter();examples=[];mediators=set()
    positivefirst=negativeA=repeated=0;phi0=0;temporaries={}
    for lap in range(2):
        if lap:phi0=sum(own.values())
        for ev in events():
            actor,h,j,bit=ev['id'];tree=aa if actor=='A' else bb;time_now=ev['time']+lap*T
            if actor=='A':
                g=ev['pivot']
                if lap:negativeA+=bool(own.get(g,False))
                own[g]=False;previous.pop(g,None);losttargets[g].clear()
                if not lap:reset[g]+=1
            elif ev['case']!='ZIG' and bit==0:
                v=(h,j);d=ds[v];g=d['g'];F=bb.m[g];temporaries[v]={'F':F,'promo_old_mask':bb.m[d['p']]}
                assert F&sum(1<<(k-1) for k in p['original_S'])==d['F']
                assert d['target'] not in losttargets[g]
                losttargets[g].add(d['target'])
                if j>2*gs[h]:
                    prior=previous.get(g)
                    if lap:
                        if own.get(g,False):repeated+=1
                        else:positivefirst+=1
                    own[g]=True
                    if prior is not None:
                        assert prior['A_component']==digest(aa.component(g))
                        mediated=promos[g]>prior['promotion_count']
                        if not mediated:
                            assert F&~prior['J_full']==0 and prior['J_full']!=prior['F_full']
                        else:
                            beta=completed[g];assert beta['time']>prior['end'] and beta['time']<starts[h]+lap*T
                            assert F&~beta['P_full']==0 and beta['P_full']!=beta['F_full']
                            w=firstafter.get(g,v);assert vs[w]['type']=='P'
                            if lap:
                                donor=tuple(beta['bit']);assert donor not in mediators;mediators.add(donor)
                        if lap:
                            key='promotion_mediated' if mediated else 'promotion_free';count[key]+=1
                            count['later_'+vs[v]['type']]+=1
                            count['case_'+d['case']]+=1
                            if len(examples)<24:examples.append({'earlier':prior['parent'],'later':v,'old_g':g,'later_type':vs[v]['type'],
                                'transition':key,'A_component_sha256':prior['A_component'],
                                'earlier_full_frame':prior['F_full'],'earlier_completed_J':prior['J_full'],'later_full_frame':F,
                                'original_interval_endpoints':[prior['end']-lap*T,starts[h]],
                                'mediator':beta if mediated else None,'later_double':d})
                    previous[g]={'parent':v,'F_full':F,'J_full':None,'A_component':digest(aa.component(g)),
                        'promotion_count':promos[g],'end':ends[h]+lap*T}
                if g in promotime and g not in firstafter:firstafter[g]=v
            tree.step(ev)
            if actor=='B':
                g=ev['promoted'];promotime[g]=time_now;promos[g]+=1;firstafter.pop(g,None);losttargets[g].clear()
                if not lap and g==ev['target']:targetpromos[g]+=1
                if ev['case']!='ZIG' and bit==1:
                    v=(h,j);d=ds[v]
                    if previous.get(d['g'],{}).get('parent')==v:previous[d['g']]['J_full']=bb.m[d['g']]
                    if d['case'] in ('LL','RR'):
                        g=d['p'];completed[g]={'bit':['B',h,j,0],'time':time_now-1,'P_full':bb.m[g],
                            'F_full':temporaries[v]['F'],'creator':v,
                            'completed_gained_key_count':(bb.m[g]&~temporaries[v]['promo_old_mask']).bit_count()}
        assert (aa.code(),bb.code())==initial
    assert sum(own.values())==phi0 and positivefirst==negativeA
    noreset=sorted(g for g in oldcols if not reset[g])
    for g in noreset:assert promos[g]>0 and targetpromos[g]==0
    assert len(mediators)==count['promotion_mediated']
    assert positivefirst<=sum(reset.values())<=2*A
    return {'source':s['name'],'source_sha256':digest(s),'origin':e['origin'],'A':A,'Q_B':len(ds),
        'noncheap_renewal_counts':dict(count),'promotion_mediators_injective':True,'mediator_bits':sorted(mediators),
        'no_A_reset_old_g_columns':noreset,'no_reset_promotion_necessity_verified':True,
        'ownership_potential':{'cyclic_initial':phi0,'cyclic_final':sum(own.values()),'first_noncheap_B_increments':positivefirst,
            'A_reset_decrements':negativeA,'repeated_noncheap_zero_change_events':repeated,'A_bit_budget':sum(reset.values())},
        'transition_examples':examples,'scope':'All physical index-noncheap renewal transitions, before original F/C_old/H/quota; no posthybrid survivor inferred.'}

if __name__=='__main__':
    m=Meter('exhaustive_physical_renewal_law');out=[]
    for e in entries():
        z=audit(e);out.append(z);write('PHYSICAL_RENEWAL_RESULTS.json',out);gc.collect()
    write('ALL_CONTROL_REFERENCES.json',[{**e,'source_sha256':digest(e['source']),
        'physical_sha256':hfile(e['physical']) if e.get('physical') else None} for e in entries()])
    m.info['complete_sources']=len(out);m.ok=True
    print('PASS exact physical renewal law, mediator injection, no-reset alternative and cyclic ownership potential on',len(out),'complete sources',flush=True)

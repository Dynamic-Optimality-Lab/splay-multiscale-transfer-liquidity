"""New owner/bit inventory from already verified source rows; no replay."""
import collections,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent;OLD=P/'SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01'
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def mp(z):return {tuple(x['demand']):tuple(x['unit']) for x in z}
def main():
    c=json.loads((OLD/'aligned_source_and_owners.json').read_text());rr=c['rows'];tags=c['tags'];a=mp(c['final_full_allocation']);f6=mp(c['f6'])
    units={(r['occurrence'],j,b) for r in rr for j in range(1,r['a']+1) for b in (0,1)}
    demands={(r['occurrence'],j) for r in rr for j in range(1,r['qF']+1)}
    assert set(a)==demands and set(a.values())<=units and len(set(a.values()))==len(a)
    end=[i for i,r in enumerate(rr) if r['genuine_F']];macros=[];source_to_macro={}
    for j,i in enumerate(end):
        prev=end[j-1];rows=rr[prev+1:i+1] if prev<i else rr[prev+1:]+rr[:i+1]
        mm={'macro':j,'occurrences':[r['occurrence'] for r in rows],'target':rows[-1]['target'],'H':sum(r['a'] for r in rows),
            'Q':sum(r['qF'] for r in rows),'units':[(r['occurrence'],k,b) for r in rows for k in range(1,r['a']+1) for b in (0,1)],
            'clean_D_star_K':all(r['mode']=='D' for r in rows[:-1]),'end':rows[-1]['occurrence']}
        macros.append(mm);source_to_macro.update({r['occurrence']:j for r in rows})
    comparisons={'raw_h6':mp(c['f6']),'natural_h6':mp(c['h6_natural']),'full_h0':mp(c['full_h0']),
        'leaf_channels':mp(c['leaf_comparison'])}
    comparisons.update({z['name']:mp(z['comparison']) for z in c['policy_stages']})
    invcomp={name:{u:d for d,u in m.items()} for name,m in comparisons.items()};ainv={u:d for d,u in a.items()};finv={u:d for d,u in f6.items()}
    first={d:'common' for d in mp(c['common_locked'])}
    for d in mp(c['natural_prior']):first.setdefault(d,'common/natural exchange')
    for stage in c['policy_stages']:
        for d in mp(stage['additions']):assert d not in first;first[d]=stage['name']
    extra=c['extra_payment'];first[tuple(extra['demand'])]='C27 later source-gap success (FROZEN)'
    assert set(first)==demands
    births={tuple(z['birth']):z for z in c['selected_transports']};origins={tuple(z['origin']):z for z in c['selected_transports']}
    own=mp(c['own_tail_pairs']);creators=mp(c['creator_pairs']);correction={tuple(u) for u in c['flip']['repair_units']}
    block={tags[k]:'critical_'+k for k in ('j','h','g','s','t','v','p','e')}
    bits=[]
    for r in rr:
        for j in range(1,r['a']+1):
            for b in (0,1):
                u=(r['occurrence'],j,b);bits.append({'unit':u,'A_depth':len(r['A_path']),'StepEv':r['A_events'][j-1],
                    'source_mode':r['mode'],'source_target':r['target'],'macro':source_to_macro[u[0]],
                    'source_block':block.get(u[0],'original_preparation_or_return'),
                    'comparison_preimages':{k:v[u] for k,v in invcomp.items() if u in v},
                    'auxiliary_owner':finv.get(u),'effective_owner':ainv.get(u),'unowned':u not in ainv,
                    'frozen_effective':u in ainv,'eligible_current_residuals':[],
                    'eligibility_note':'Current residual set is empty; no eligible set for a hypothetical new demand is inferred.',
                    'C23_repair_association':u in correction})
    dd=[]
    for d in sorted(demands):
        dd.append({'demand':d,'effective_unit':a[d],'first_effective_stage':first[d],
            'full_natural_comparison_unit':comparisons['full_h0'].get(d),'common':d in mp(c['common_locked']),
            'six_key_unit':f6.get(d),'selected_zero_origin':origins.get(d),'selected_birth':births.get(d),
            'creator_comparison_unit':creators.get(d),'first_own_tail_comparison_unit':own.get(d),
            'frozen':True,'unpaid':False})
    timeline=[]
    for d,u in a.items():timeline.extend([((u[0],0,u[1],u[2]),d),((d[0],1,d[1],0),d)])
    active=set();trace=[];peak=0
    for point,d in sorted(timeline):
        action='close' if d in active else 'open'
        if action=='close':active.remove(d)
        else:active.add(d)
        peak=max(peak,len(active));trace.append({'point':point,'action':action,'demand':d,'active':sorted(active),'records':len(active)})
    assert not active and peak==6 and len(bits)==522 and len(dd)==58
    assert a[(771,4)]==(769,1,1) and a[(661,3)]==(621,2,0)
    # Reusable source ordinal theorem candidate instantiated before and after
    # the already successful direct payment. No owner is removed in C28.
    bands=[];selected_birth_macros={source_to_macro[d[0]] for d in births}
    for m in macros:
        g=sum(1 for z in c['creator_pairs'] if z['creator_macro']==m['macro'])
        if not m['clean_D_star_K'] or m['macro'] in selected_birth_macros:continue
        band=[tuple(u) for u in m['units'][8:max(8,len(m['units'])-g)]]
        if not band:continue
        baseline={u for k,v in comparisons.items() for u in v.values()};old=mp(c['policy_stages'][-1]['after'])
        assert not (set(band)&baseline)
        exception=[u for u in band if u in ainv]
        assert all(u not in set(old.values()) for u in band)
        bands.append({'macro':m['macro'],'H':m['H'],'end':m['end'],'creator_tail_paid':g,
            'band_size':len(band),'units':band,'baseline_comparison_disjoint':True,'effective_exceptions':exception,
            'unowned_now':[u for u in band if u not in ainv]})
    out('w199_inventory.json',{'status':'PRODUCER_EXACT_NEW_INVENTORY_FROM_REUSED_VERIFIED_ROWS','source_replay_calls':0,
        'bit_count':len(bits),'demand_count':len(dd),'A':261,'QF':58,'QE':27,'scalar_margin':522-58,
        'macros':macros,'bits':bits,'demands':dd,'current_full_a':c['final_full_allocation'],'current_residuals':sorted(demands-set(a)),
        'current_unowned':sorted(units-set(a.values())),'static_residual_eligibility':[],
        'Bank25_trace':trace,'Bank25_endpoint_record_peak':peak,'original_raw_bank_peak':10,
        'historical_pre_extra_residuals':sorted(demands-set(mp(c['policy_stages'][-1]['after']))),
        'historical_final_extra_success':extra,'extra_success_is_now_frozen':True,
        'source_safe_middle_bands':bands,'witness_verdict':'W28-FUNDED; P*=empty, g*=empty; complete full map inherited',
        'universal_funding_inferred':False})
    print(json.dumps({'status':'W199_FUNDED_VACUOUS_EXTENSION','bits':len(bits),'demands':len(dd),
        'P':len(demands-set(a)),'free':len(units-set(a.values())),'safe_bands':[(z['end'],z['band_size'],len(z['effective_exceptions'])) for z in bands]}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_inventory_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':0,'source_queries':0})

"""Source-defined full comparison at a NEW, explicitly restricted uniform
class: one hard j..e frame/catchment, <=3 outside natural deficits.
No global desired matching/count is assumed; original source slots rule.
"""
import json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;OLD=B.parent/'SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01'
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def mp(v):return {tuple(z['demand']):tuple(z['unit']) for z in v}
def pack(v):return [{'demand':d,'unit':u} for d,u in sorted(v.items())]
def macros(rows):
    ee=[i for i,r in enumerate(rows) if r['genuine_F']];ans=[]
    for k,i in enumerate(ee):
        p=ee[k-1];ss=rows[p+1:i+1] if p<i else rows[p+1:]+rows[:i+1]
        ans.append({'rows':ss,'end':ss[-1]['occurrence'],'H':sum(r['a'] for r in ss),'Q':sum(r['qF'] for r in ss),
            'units':[(r['occurrence'],j,b) for r in ss for j in range(1,r['a']+1) for b in (0,1)],
            'demands':[(r['occurrence'],j) for r in ss for j in range(1,r['qF']+1)]})
    return ans
def cutprofile(a):
    ee=[]
    for d,u in a.items():ee.extend([((u[0],0,u[1],u[2]),d),((d[0],1,d[1],0),d)])
    seen=set();peak=0;rr=[]
    for t,d in sorted(ee):
        if d in seen:seen.remove(d)
        else:seen.add(d)
        peak=max(peak,len(seen));rr.append((t,len(seen)))
    assert not seen;return peak,rr
def extend(a,h,D):
    inverse={u:d for d,u in a.items()};extra={};paths=[];visited=set()
    for root in sorted(D-set(a)):
        d=root;steps=[]
        while True:
            assert d not in visited;visited.add(d);u=h[d];steps.append((d,u))
            if u not in inverse:extra[root]=u;break
            d=inverse[u]
        paths.append({'root':root,'steps':steps,'terminal':u})
    answer=dict(a);answer.update(extra);assert len(set(answer.values()))==len(answer)
    return answer,paths
def construct(source,tags,prior,current,label):
    mm=macros(source);frame={name:next(m for m in mm if m['end']==tags[name]) for name in ('j','h','g','s','t','v','p','e')}
    assert [frame[k]['Q'] for k in frame]==[1,2,1,3,1,2,1,6]
    assert frame['j']['H']>=3 and all(frame[k]['H']==1 for k in frame if k!='j')
    D={d for m in mm for d in m['demands']};U={u for m in mm for u in m['units']}
    own={d:u for m in mm for d,u in zip(m['demands'],m['units'])};frameD={d for m in frame.values() for d in m['demands']}
    outside=sorted((D-set(own))-frameD);assert len(outside)<=3
    critical=[(tags['s'],3)]+[(tags['e'],k) for k in range(3,7)];jseed=frame['j']['units'][1:6]
    assert len(jseed)==5 and set(critical)==(D-set(own))&frameD
    loop=[frame[k]['units'][1] for k in ('g','t','p')]
    h=dict(own);h.update(zip(critical,jseed));h.update(zip(outside,loop))
    assert set(h)==D and len(set(h.values()))==len(h) and set(h.values())<=U and all(h[d]==u for d,u in own.items())
    answer,paths=extend(prior,h,D);assert set(answer)==D and all(answer[d]==u for d,u in prior.items())
    same,empty=extend(current,h,D);assert same==current and not empty
    hp,ht=cutprofile(h);ap,at=cutprofile(prior);fp,ft=cutprofile(answer)
    # The pointwise bound uses graph paths; no conclusion from just totals.
    endpoints=sorted({t for t,n in ht+at+ft})
    def n_at(trace,t):return next((n for p,n in reversed(trace) if p<=t),0)
    bound=[]
    for t in endpoints:
        hv,av,fv=n_at(ht,t),n_at(at,t),n_at(ft,t);assert fv<=hv+2*av
        bound.append({'cut':t,'H':hv,'a':av,'extended':fv,'upper_bound':hv+2*av})
    assert hp<=10 and ap<=7 and fp<=25
    return {'source_id':label,'frame':{k:{'end':m['end'],'H':m['H'],'Q':m['Q']} for k,m in frame.items()},
        'outside_natural_deficits':outside,'critical_native_deficits':critical,'j_five_units':jseed,'loop_three_units':loop,
        'source_independent_H':pack(h),'own_h0':pack(own),'historical_prefix':pack(prior),
        'counterfactual_extension_of_historical_prefix':pack(answer),'owner_walks':paths,
        'current_full_frozen_a_unchanged':True,'H_cut_peak':hp,'historical_a_cut_peak':ap,'extended_cut_peak':fp,
        'cut_bound_receipts':bound,'actual_frozen_current_extension_is_empty':True,
        'note':'Historical-prefix comparison exercise is NOT replacement of the already successful current full map.'}
def main():
    c=json.loads((OLD/'aligned_source_and_owners.json').read_text());s=json.loads((B/'shortened_source_control.json').read_text());p=json.loads((B/'shortened_control_policy.json').read_text())
    results=[construct(c['rows'],c['tags'],mp(c['policy_stages'][-1]['after']),mp(c['final_full_allocation']),'C27-W199-frozen'),
        construct(s['rows'],s['tags'],mp(p['prior_before_extra']),mp(p['final_full_a']),'C28-shortened-01')]
    out('catchment_comparison_receipts.json',{'status':'EXPLICIT_SOURCE_COMPARISON_AND_FROZEN_PATH_PRODUCER_RECEIPTS',
        'uniform_theorem_scope':'disjoint genuine-macro catchments with one hard j..e frame and <=3 OUTSIDE natural h0 deficits each; proper one-period eligibility; cut-profile storage condition',
        'not_assumed_for_all_guarded_histories':True,'results':results})
    print(json.dumps({'status':'CATCHMENT_COMPARISON_PASS','results':[{'source':z['source_id'],'outside':z['outside_natural_deficits'],
        'H_peak':z['H_cut_peak'],'a_peak':z['historical_a_cut_peak'],'extended_peak':z['extended_cut_peak'],
        'paths':z['owner_walks']} for z in results]}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_catchment_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':0,'source_queries':0})

"""Exact size lower bound from an injectively colored population-free grammar."""
import json,sys,time,hashlib
from pathlib import Path
from functools import lru_cache
from itertools import product
BASE=Path(__file__).resolve().parent;CAP=min(120,float(sys.argv[1]))
sys.path.insert(0,str(BASE.parent/'M3_UNITPAIR01'))
from profiles import specification,PATHS
def read(p):return json.loads(p.read_text())
def write(p,v):
    with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    start=time.process_time();selector=read(BASE.parent/'M3_POP3_RISK01/risk_selector.json')
    assert read(BASE.parent/'M3_POP3_RISK01/representation_audit.json')['status']=='PROVED_COMPLETE_SIGNED_REDUCTION_AND_INDEPENDENT_SELECTOR_AUDIT_PASS'
    plans={(p['helper'],tuple(map(tuple,p['word']))):tuple(p['terminal_source_address']) for p in selector['plans']}
    risk={k:set(map(tuple,v)) for k,v in selector['risk'].items()}
    families=[(None,(p,)) for p in PATHS]+[(g,(p,q)) for g in (0,9) for p,q in product(PATHS,repeat=2)]
    total=0;rows=[];peak=0;status=None
    for helper,word in families:
        obs,need,forced=specification(helper,word);where=plans[helper,word]
        constraints={():('S',None)}
        for p,v in forced.items():constraints[p]=('S',None) if v is None else ('F',helper)
        scores=sorted(risk['H1' if helper is None else str(helper)])
        terms=0;fibers=[];maxF=len(obs)-len({p for p,(k,v) in constraints.items() if k=='S'})
        for root,target in scores:
            fixed={():root,where:target}
            if where==() and root!=target:continue
            @lru_cache(None)
            def count(p,lo,hi):
                if p not in obs:return 1
                ans=(1+int(lo>hi)) if p not in need else 0
                typ,g=constraints.get(p,('ANY',None))
                if typ!='F':
                    values=[fixed[p]] if p in fixed else range(lo,hi+1)
                    for k in values:
                        if lo<=k<=hi:ans+=count(p+(0,),lo,k-1)*count(p+(1,),k+1,hi)
                if typ!='S' and p not in fixed:
                    gap=g if typ=='F' else (lo+hi+1)//2
                    if lo<=gap<=hi+1:ans+=count(p+(0,),lo,gap-1)*count(p+(1,),gap,hi)
                return ans
            n=count((),0,8);info=count.cache_info();peak=max(peak,info.currsize+len(rows)+len(fibers));terms+=n
            if n:fibers.append({'root':root,'target':target,'count':n})
            assert peak<2000000 and time.process_time()-start<CAP,'UNKNOWN preflight record/CPU cap'
        total+=terms
        row={'helper':helper,'word':word,'count_lower_bound':terms,'cumulative_lower_bound':total,'observed':sorted(obs),'required':sorted(need),'forced':[[p,k,v] for p,(k,v) in sorted(constraints.items())],'terminal_source_address':where,'fibers':fibers,'max_anonymous_occurrences_upper_bound':maxF}
        rows.append(row)
        print(json.dumps({'helper':helper,'word':word,'count_lower_bound':terms,'cumulative':total,'CPU':time.process_time()-start}),flush=True)
        if total>2000000:
            status='EXACT_COUNT_FREE_CORPUS_LOWER_BOUND_EXCEEDS_QUERY_CAP';break
    if status is None:status='LOWER_BOUND_FITS_FULL_PREFLIGHT_STILL_REQUIRED'
    result={'status':status,'injective_subgrammar':'one interval-median F choice at each unforced address; forced outer helper retained','canonical_root_lower_bound':total,'limit':2000000,'families_counted':len(rows),'registered_word_families':78,'rows':rows,'peak_counting_records':peak,'source_transition_queries':0,'existing_checks_repeated':0,'CPU_seconds':time.process_time()-start,'CPU_cap':CAP,'uniform_J_constructed':False,'refutes_uniform_J':False,'negative_cycle_certified':False,'old_formula_values_reused_not_refitted':True}
    assert result['CPU_seconds']<CAP;write(BASE/'preflight.json',result);print(json.dumps({k:v for k,v in result.items() if k!='rows'},indent=2),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error={'type':type(e).__name__,'message':str(e)};raise
    finally:write(BASE/'preflight_exit.json',{'whole_process_CPU_seconds':time.process_time(),'CPU_cap':CAP,'error':error})

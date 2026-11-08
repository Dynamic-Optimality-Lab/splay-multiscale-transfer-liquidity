"""Exact max-plus protected-prefix bound for the fixed threshold formula."""
import json,sys,time
from pathlib import Path
from functools import lru_cache
from itertools import product
BASE=Path(__file__).resolve().parent;CAP=min(120,float(sys.argv[1]));NEG=-10000
sys.path.insert(0,str(BASE.parent/'M3_UNITPAIR01'))
from profiles import specification,PATHS
def read(p):return json.loads(p.read_text())
def write(p,v):
    with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    start=time.process_time();selector=read(BASE.parent/'M3_POP3_RISK01/risk_selector.json');plans={(p['helper'],tuple(map(tuple,p['word']))):tuple(p['terminal_source_address']) for p in selector['plans']};risk={k:list(map(tuple,v)) for k,v in selector['risk'].items()}
    families=[(None,(p,)) for p in PATHS]+[(g,(p,q)) for g in (0,9) for p,q in product(PATHS,repeat=2)];rows=[];overall=0;peak=0
    for helper,word in families:
        obs,need,forced=specification(helper,word);terminal=plans[helper,word];types={p:('S',None) if v is None else ('F',helper) for p,v in forced.items()};fibers=[];familymax=NEG;witness=None
        for r,x in risk['H1' if helper is None else str(helper)]:
            if terminal==() and r!=x:continue
            fixed={():r,terminal:x};choices={}
            @lru_cache(None)
            def maximum(p,lo,hi):
                if p not in obs:return 0
                best=0 if p not in need else NEG;chosen=['P'];kind,g=types.get(p,('ANY',None))
                if kind!='F':
                    for k in ([fixed[p]] if p in fixed else range(lo,hi+1)):
                        if not lo<=k<=hi:continue
                        left=maximum(p+(0,),lo,k-1);right=maximum(p+(1,),k+1,hi)
                        if min(left,right)>NEG and left+right>best:best=left+right;chosen=['S',k]
                if kind!='S' and p not in fixed:
                    for gap in ([g] if kind=='F' else range(lo,hi+2)):
                        if not lo<=gap<=hi+1:continue
                        left=maximum(p+(0,),lo,gap-1);right=maximum(p+(1,),gap,hi)
                        if min(left,right)>NEG and 1+left+right>best:best=1+left+right;chosen=['F',gap]
                choices[p,lo,hi]=chosen;return best
            m=maximum((),0,8);peak=max(peak,2*maximum.cache_info().currsize+len(rows)+len(fibers));fibers.append({'root':r,'target':x,'max_retained_F':None if m==NEG else m})
            if m>familymax:
                def term(p,lo,hi):
                    if p not in obs:return ['P']
                    typ,*v=choices[p,lo,hi]
                    if typ=='P':return ['P']
                    k=v[0]
                    if typ=='S':return ['S',k,term(p+(0,),lo,k-1),term(p+(1,),k+1,hi)]
                    return ['F',k,term(p+(0,),lo,k-1),term(p+(1,),k,hi)]
                familymax=m;witness={'root':r,'target':x,'term':term((),0,8)} if m>NEG else None
            assert peak<2000000 and time.process_time()-start<CAP,'UNKNOWN critical-budget max-plus cap'
        overall=max(overall,familymax)
        rows.append({'helper':helper,'word':word,'observed':sorted(obs),'required':sorted(need),'terminal_source_address':terminal,'max_retained_F':None if familymax==NEG else familymax,'attaining_prefix':witness,'fibers':fibers})
    assert 4+overall<266
    result={'status':'EXACT_MAX_PLUS_CRITICAL_PREFIX_BUDGET_CONSTRUCTED_UNAUDITED','word_families':len(rows),'max_retained_F':overall,'total4_threshold_budget':4,'critical_total_population_bound':4+overall,'rows':rows,'peak_max_plus_records':peak,'new_source_transition_queries':0,'CPU_seconds':time.process_time()-start,'CPU_cap':CAP,'universal_predicate_preservation_proved':False,'proof_relation_reduction_only':True}
    assert result['CPU_seconds']<CAP;write(BASE/'critical_budget.json',result);print(json.dumps({k:v for k,v in result.items() if k!='rows'},indent=2),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error={'type':type(e).__name__,'message':str(e)};raise
    finally:write(BASE/'critical_budget_exit.json',{'whole_process_CPU_seconds':time.process_time(),'CPU_cap':CAP,'error':error})

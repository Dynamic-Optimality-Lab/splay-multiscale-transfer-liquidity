"""Independent ordered-list max-plus proof and attaining-prefix checks."""
import json,sys,time,hashlib
from pathlib import Path
from functools import lru_cache
from itertools import product
BASE=Path(__file__).resolve().parent;CAP=min(300,float(sys.argv[1]));NEG=-10000
sys.path.insert(0,str(BASE.parent/'M3_TWOGAP_AUD01'))
import reference as R
def read(p):return json.loads(p.read_text())
def write(p,v):
    with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    start=time.process_time();p=read(BASE/'critical_budget.json');sel=read(BASE.parent/'M3_POP3_RISK01/risk_selector.json');words=[(None,(x,)) for x in R.PATHS]+[(g,(x,y)) for g in (0,9) for x,y in product(R.PATHS,repeat=2)];count=peak=globalmax=0;witnesses=0
    assert len(p['rows'])==len(words)==78
    for row,(helper,word) in zip(p['rows'],words):
        assert row['helper']==helper and row['word']==[list(x) for x in word]
        full=R.universe();need={()};types={():('S',None)}
        for j,path in enumerate(word):
            need.update(R.at(full,path[:i])[0] for i in range(len(path)+1));at=R.at(full,path)[0];types[at]=('F',helper) if j<len(word)-1 else ('S',None);full=R.splay(full,at)
        terminal=full[0];obs=set(R.SHADOW)|{R.at(full,x)[0] for x in R.SHADOW};owner=R.find(full,());obs.update(n[0] for n in owner[1:] if R.real(n));obs|=need
        for a in tuple(obs):obs.update(a[:i] for i in range(len(a)))
        assert sorted(obs)==list(map(tuple,row['observed'])) and sorted(need)==list(map(tuple,row['required'])) and terminal==tuple(row['terminal_source_address'])
        margins=sel['minimum_margins']['H1' if helper is None else str(helper)];computed={};best=NEG
        for root in range(9):
            for target in range(9):
                margin=margins[f'{root},{target}']
                if margin is None or margin>=2 or (terminal==() and root!=target):continue
                fixed={():root,terminal:target}
                @lru_cache(None)
                def score(address,keys,offset):
                    if address not in obs:return 0
                    result=0 if address not in need else NEG;kind,gap=types.get(address,('either',None))
                    if kind!='F':
                        for i,k in enumerate(keys):
                            if address in fixed and k!=fixed[address]:continue
                            left=score(address+(0,),keys[:i],offset);right=score(address+(1,),keys[i+1:],k+1)
                            if min(left,right)>NEG:result=max(result,left+right)
                    if kind!='S' and address not in fixed:
                        for cut in ([gap-offset] if kind=='F' else range(len(keys)+1)):
                            if not 0<=cut<=len(keys):continue
                            left=score(address+(0,),keys[:cut],offset);right=score(address+(1,),keys[cut:],offset+cut)
                            if min(left,right)>NEG:result=max(result,1+left+right)
                    return result
                m=score((),tuple(range(9)),0);computed[root,target]=None if m==NEG else m;best=max(best,m);count+=1;peak=max(peak,score.cache_info().currsize+count)
                assert peak<2000000 and time.process_time()-start<CAP,'UNKNOWN independent critical-budget cap'
        assert computed=={(e['root'],e['target']):e['max_retained_F'] for e in row['fibers']}
        assert (None if best==NEG else best)==row['max_retained_F']
        if row['attaining_prefix'] is not None:
            witness=row['attaining_prefix'];fixed={():witness['root'],terminal:witness['target']};gapcounts=[0]*10
            def check(n,a,lo,hi):
                if n==['P']:
                    assert a not in need;return 0
                assert a in obs and len(n)==4
                typ,k,left,right=n;forced=types.get(a)
                if typ=='S':
                    assert lo<=k<=hi and (forced is None or forced[0]=='S') and (a not in fixed or fixed[a]==k)
                    return check(left,a+(0,),lo,k-1)+check(right,a+(1,),k+1,hi)
                assert typ=='F' and a not in fixed and lo<=k<=hi+1 and (forced is None or forced==('F',k));gapcounts[k]+=1
                return 1+check(left,a+(0,),lo,k-1)+check(right,a+(1,),k,hi)
            assert check(witness['term'],(),0,8)==best==sum(gapcounts);witnesses+=1
        globalmax=max(globalmax,best)
    assert globalmax==p['max_retained_F'] and 4+globalmax==p['critical_total_population_bound']<266
    result={'status':'INDEPENDENT_COMPLETE_CRITICAL_BUDGET_REDUCTION_AUDIT_PASS','word_families':78,'risky_fibers_checked':count,'attaining_prefixes_checked':witnesses,'exact_max_retained_F':globalmax,'critical_total_population_bound':4+globalmax,'construction_imported':False,'independent_method':'ordered Score-list max-plus with parent-map source addresses','complete_grammar_maximum_not_population_fit':True,'source_predicate_unchanged':True,'reduction_domain':'retained signed proof relation; original failure still requires original LOW witness','universal_preservation_test_executed':False,'universal_preservation_proved':False,'new_source_transition_queries':0,'peak_records':peak,'critical_budget_sha256':hashlib.sha256((BASE/'critical_budget.json').read_bytes()).hexdigest(),'CPU_seconds':time.process_time()-start,'CPU_cap':CAP}
    write(BASE/'independent_critical_budget_audit.json',result);print(json.dumps(result,indent=2),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error={'type':type(e).__name__,'message':str(e)};raise
    finally:write(BASE/'audit_critical_exit.json',{'whole_process_CPU_seconds':time.process_time(),'CPU_cap':CAP,'error':error})

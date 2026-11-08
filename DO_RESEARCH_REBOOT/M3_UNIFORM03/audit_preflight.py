"""Independent exact counting using ordered Score lists and address identities."""
import json,sys,time,hashlib
from pathlib import Path
from functools import lru_cache
from itertools import product
BASE=Path(__file__).resolve().parent;CAP=min(300,float(sys.argv[1]))
sys.path.insert(0,str(BASE.parent/'M3_TWOGAP_AUD01'))
import reference as R
def read(p):return json.loads(p.read_text())
def write(p,v):
    with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    start=time.process_time();p=read(BASE/'preflight.json');sel=read(BASE.parent/'M3_POP3_RISK01/risk_selector.json')
    assert p['source_transition_queries']==0
    words=[(None,(x,)) for x in R.PATHS]+[(g,(x,y)) for g in (0,9) for x,y in product(R.PATHS,repeat=2)]
    total=0;checks=0;maxF=0;maxobs=0;peak=0;verified=[]
    for row,(helper,word) in zip(p['rows'],words):
        assert row['helper']==helper and row['word']==[list(x) for x in word]
        # This independently defines the new count subgrammar's address
        # parameters; no source predicate or prior corpus is replayed.
        full=R.universe();need={()};types={():('S',None)}
        for j,path in enumerate(word):
            need.update(R.at(full,path[:i])[0] for i in range(len(path)+1));target=R.at(full,path)[0]
            types[target]=('F',helper) if j<len(word)-1 else ('S',None)
            full=R.splay(full,target)
        obs=set(R.SHADOW)|{R.at(full,x)[0] for x in R.SHADOW};owner=R.find(full,())
        obs.update(n[0] for n in owner[1:] if R.real(n));obs|=need
        for address in tuple(obs):obs.update(address[:i] for i in range(len(address)))
        terminal=full[0]
        assert sorted(obs)==list(map(tuple,row['observed'])) and sorted(need)==list(map(tuple,row['required']))
        assert [[list(a),k,v] for a,(k,v) in sorted(types.items())]==row['forced']
        assert terminal==tuple(row['terminal_source_address'])
        maxobs=max(maxobs,len(obs));maxF=max(maxF,len(obs)-sum(k=='S' for k,v in types.values()))
        margins=sel['minimum_margins']['H1' if helper is None else str(helper)]
        fibers={};subtotal=0
        for r in range(9):
            for x in range(9):
                margin=margins[f'{r},{x}']
                if margin is None or margin>=2:continue
                if terminal==() and r!=x:continue
                pinned={():r,terminal:x}
                @lru_cache(None)
                def ways(address,values,offset):
                    if address not in obs:return 1
                    result=int(address not in need)*(1+int(not values))
                    kind,gap=types.get(address,('either',None))
                    if kind!='F':
                        for i,key in enumerate(values):
                            if address in pinned and key!=pinned[address]:continue
                            result+=ways(address+(0,),values[:i],offset)*ways(address+(1,),values[i+1:],key+1)
                    if kind!='S' and address not in pinned:
                        if kind!='F':cut=len(values)//2
                        else:cut=gap-offset
                        if 0<=cut<=len(values):
                            result+=ways(address+(0,),values[:cut],offset)*ways(address+(1,),values[cut:],offset+cut)
                    return result
                n=ways((),tuple(range(9)),0);checks+=1;peak=max(peak,ways.cache_info().currsize+len(verified)+len(fibers))
                if n:fibers[r,x]=n
                subtotal+=n
                assert time.process_time()-start<CAP and peak<2000000,'UNKNOWN independent count cap'
        assert fibers=={(e['root'],e['target']):e['count'] for e in row['fibers']}
        assert subtotal==row['count_lower_bound'];total+=subtotal;assert total==row['cumulative_lower_bound']
        verified.append({'helper':helper,'word':word,'exact_subgrammar_count':subtotal,'cumulative':total})
    assert len(verified)==p['families_counted'] and total==p['canonical_root_lower_bound']
    over=total>p['limit']
    if over:
        assert p['status']=='EXACT_COUNT_FREE_CORPUS_LOWER_BOUND_EXCEEDS_QUERY_CAP'
        assert total-verified[-1]['exact_subgrammar_count']<=p['limit'],'did not stop on first size obstruction'
    # Saturating every gap at maxF suffices for all selected occurrences
    # of this subgrammar; unused original payload stays in opaque ports.
    assert 10*maxF<=266
    result={'status':'INDEPENDENT_INJECTIVE_SUBGRAMMAR_SIZE_AUDIT_PASS','construction_imported':False,'independent_method':'ordered Score-list recursion with parent-map source-address derivation','families_checked':len(verified),'fiber_counts_checked':checks,'canonical_root_lower_bound':total,'limit':p['limit'],'size_exceeds_cap':over,'strict_injectivity_proof':'SOURCE_COVERAGE.md','max_observed_addresses_in_checked_families':maxobs,'max_selected_F_upper_bound':maxF,'saturating_total_population_upper_bound':10*maxF,'T266_preserved':True,'peak_counting_records':peak,'source_transition_queries':0,'old_source_roots_or_matrix_audits_repeated':0,'preflight_sha256':hashlib.sha256((BASE/'preflight.json').read_bytes()).hexdigest(),'CPU_seconds':time.process_time()-start,'CPU_cap':CAP,'verified_families':verified,'J_formula_proved':False,'M3_status':'OPEN'}
    assert result['CPU_seconds']<CAP;write(BASE/'independent_preflight_audit.json',result);print(json.dumps({k:v for k,v in result.items() if k!='verified_families'},indent=2),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error={'type':type(e).__name__,'message':str(e)};raise
    finally:write(BASE/'audit_preflight_exit.json',{'whole_process_CPU_seconds':time.process_time(),'CPU_cap':CAP,'error':error})

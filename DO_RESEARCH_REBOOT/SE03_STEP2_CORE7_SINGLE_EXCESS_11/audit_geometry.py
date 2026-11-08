"""Source-complete seven-Score Hamiltonian/predecessor certificate.
All eight free gap BSTs remain arbitrary; no bounded population theorem.
"""
import collections,functools,importlib.util,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('source01',B.parent/'SE03_STEP2_COLD_NEG2_01/source_model.py')
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
started=time.process_time();calls=0;CAP=min(25,float(sys.argv[1])-3)
def trace(t,x):
    global calls
    calls+=1;assert calls<500000 and time.process_time()-started<CAP
    return p.trace(t,x)
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
@functools.lru_cache(None)
def trees(lo,hi):
    if lo>hi:return ('F'+str(hi),)
    return tuple(p.N(k,l,r) for k in range(lo,hi+1) for l in trees(lo,k-1) for r in trees(k+1,hi))
def leaves(t):return 0 if not p.node(t) else 1 if not p.node(t[1]) and not p.node(t[2]) else leaves(t[1])+leaves(t[2])
def main():
    ts=trees(1,7);ids={t:i for i,t in enumerate(ts)};assert len(ts)==429
    transitions=[];incoming=collections.defaultdict(list);hamincoming=collections.Counter()
    for t in ts:
        for x in range(1,8):
            dest,path,ev=trace(t,x);q=sum(e['kind']=='DOUBLE' for e in ev)
            assert dest in ids
            if q==3:assert len(path)==6 and leaves(t)==1
            if leaves(dest)==1:assert q<=1;hamincoming[q]+=1
            item={'source':ids[t],'target_key':x,'destination':ids[dest],'depth':len(path),'Q':q}
            transitions.append(item);incoming[ids[dest]].append(item)
    classes=[];critical=[];previous=0
    for u in range(2,7):
        M=set(range(1,8))-{u}
        valid={ids[t] for t in ts if t[0] in M and p.labels(p.core(t,M))==set(range(1,8))}
        admitted=[v for v in transitions if v['source'] in valid and v['destination'] in valid and v['target_key'] in M and v['depth']>0]
        deep=[v for v in admitted if v['Q']==3]
        for v in deep:
            inc=[w for w in incoming[v['source']] if w['source'] in valid and w['target_key'] in M and w['depth']>0]
            assert inc and all(w['Q']<=1 for w in inc)
            previous+=len(inc);critical.append({'unmarked':u,'critical':v,'all_admitted_predecessors':inc})
        classes.append({'unmarked':u,'marks':sorted(M),'core_contexts':len(valid),'admitted_genuine_edges':len(admitted),
            'Q3_sectors':len(deep),'positive_predecessor_condition':'every actual previous genuine Q<=1'})
    result={'status':'COMPLETE_UNIVERSAL_SEVEN_SCORE_GEOMETRY','trees':ts,'transitions':transitions,
        'classes':classes,'critical_sectors':critical,'raw_contexts':len(ts),'all_access_transitions':len(transitions),
        'Hamiltonian_incoming_by_Q':dict(hamincoming),'Q3_sector_count':len(critical),'preceding_sector_incidences':previous,
        'proof_bridge':'all ordered Score trees, all five unmarked positions, exact same-set splay, eight rigid arbitrary BST gaps',
        'source_realization':'necessary coverage ONLY; no claim every admissible sector embeds in an actual closed period',
        'symbolic_lemma':'Hamiltonian destination implies extremal target; second SS double creates a permanent Score fork',
        'source_engine_calls':calls,'new_finite_tests':0}
    out('geometry_certificate.json',result)
    print(json.dumps({k:v for k,v in result.items() if k not in ('trees','transitions','critical_sectors')}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_geometry_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':calls,'new_finite_tests':0})

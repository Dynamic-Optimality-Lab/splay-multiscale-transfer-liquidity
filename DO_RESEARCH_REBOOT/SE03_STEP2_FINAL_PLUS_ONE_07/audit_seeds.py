"""NEW final-H1Q1 terminal seeds, universal ordered-slot A terms."""
import collections,functools,itertools,json,sys,time
from fractions import Fraction as F
from pathlib import Path
B=Path(__file__).resolve().parent;OLD=B.parent/'SE03_STEP2_TERMINAL_PAIR_06'
sys.path.insert(0,str(OLD))
import audit_saturation3 as s
g=s.g;c=s.c;tr=s.tr
started=time.process_time();CAP=min(35,float(sys.argv[1])-3)
counts=collections.Counter()
def guard():
    if time.process_time()-started>CAP or c.account['source_engine_calls']>=400000:raise c.Bound()
c.limit=guard;s.guard=guard
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def serial(v):
    if isinstance(v,g.Hole):return {'gap':[str(v.lo),str(v.hi)]}
    if isinstance(v,F):return str(v)
    if isinstance(v,dict):return {k:serial(q) for k,q in v.items()}
    if isinstance(v,(tuple,list)):return [serial(q) for q in v]
    return v
def main():
    states=list(t for t in g.BF(1,11) if t[0] in c.MM);SS=set(states)
    fwd=collections.defaultdict(list)
    for t in states:
        guard()
        for y in c.M:
            if y==t[0]:continue
            n=c.bm(t,y)
            if n:assert n[0] in SS;fwd[t].append((n[0],y,n[1]))
    perms=list(itertools.permutations(c.M))
    @functools.lru_cache(None)
    def orders(t):return tuple(r for r in perms if r[0]==t[0] and s.heap(t,r))
    @functools.lru_cache(None)
    def Ainitial(word):return tuple(sorted({s.canon(t) for t in tr.starts(word)[0]},key=str))
    groups={};cases=[]
    for b in states:
        root=b[0]
        for end,y,q in fwd[b]:
            if q!=1:continue
            for probe,x,qx in fwd[end]:
                if qx!=4:continue
                # Exact coldness is imposed through all actual recent orders.
                rr=[r for r in orders(b) if c.recent(r,y)[-1]==x]
                if not rr:continue
                assert s.parentmap(end)[x] is not None and x not in set(s.parentmap(end).values())
                aa=Ainitial((root,y,x));ids=[]
                for a in aa:
                    key=(a,b)
                    if key not in groups:groups[key]={'A':a,'BF':b,'recent':set(),'cases':[]}
                    groups[key]['recent'].update(rr);ids.append(key)
                case={'oldroot':root,'plus_target':y,'cold_q4':x,'BF_before':b,'BF_after_plus':end,
                    'A_initial_terms':len(aa),'recent_orders':len(rr),'L_before':c.leaves(b),'L_after':c.leaves(end)}
                ci=len(cases);cases.append(case)
                for key in ids:groups[key]['cases'].append(ci)
                counts[(c.leaves(b),c.leaves(end))]+=1
                if len(groups)>40000:raise c.Bound()
    records=[]
    for d in groups.values():
        d['recent']=sorted(d['recent']);records.append(d)
    leaf=collections.Counter();physical=0
    for d in records:leaf[c.leaves(d['BF'])]+=len(d['recent']);physical+=len(d['recent'])
    result={'status':'COMPLETE_NEW_TERMINAL_SEED_GRAMMAR','groups':serial(records),'terminal_cases':serial(cases),
        'BF_density_contexts':len(states),'BF_source_edges':sum(map(len,fwd.values())),
        'A_word_frame_queries':Ainitial.cache_info().misses,'term_BF_groups':len(records),'term_BF_recent_records':physical,
        'seed_leaf_distribution':dict(leaf),'terminal_case_leaf_changes':[{'from':k[0],'to':k[1],'cases':v} for k,v in sorted(counts.items())],
        'source_engine_calls':c.account['source_engine_calls'],'new_finite_tests':0,
        'coverage':'requires inherited slot-lifting plus new H1Q1 macro proof; no claim from concrete populations'}
    out('terminal_seeds.json',result)
    print(json.dumps({k:v for k,v in result.items() if k not in ('groups','terminal_cases')}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_seeds_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,**c.account})

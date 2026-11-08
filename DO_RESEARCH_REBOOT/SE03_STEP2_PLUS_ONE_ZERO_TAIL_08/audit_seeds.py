"""Campaign08 NEW +1->0 terminal sectors with universally free A slots."""
import collections,functools,itertools,json,sys,time
from fractions import Fraction as F
from pathlib import Path
B=Path(__file__).resolve().parent;OLD=B.parent/'SE03_STEP2_TERMINAL_PAIR_06'
sys.path.insert(0,str(OLD))
import audit_saturation3 as s
g=s.g;c=s.c;tr=s.tr
started=time.process_time();CAP=min(30,float(sys.argv[1])-3)
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
def degree(b):return sum(p==b[0] for p in s.parentmap(b).values())
def main():
    states=[t for t in g.BF(1,11) if t[0] in c.MM];SS=set(states)
    fwd=collections.defaultdict(list);inc=collections.defaultdict(list);q3outputs=0
    for t in states:
        guard()
        for x in c.M:
            if x==t[0]:continue
            n=c.bm(t,x)
            if n:
                end,q=n;assert end in SS
                fwd[t].append((end,x,q));inc[end].append((t,x,q))
                if q==3:assert degree(end)>=3;q3outputs+=1
    perms=list(itertools.permutations(c.M))
    @functools.lru_cache(None)
    def orders(t):return tuple(r for r in perms if r[0]==t[0] and s.heap(t,r))
    @functools.lru_cache(None)
    def initial(word):return tuple(sorted({s.canon(t) for t in tr.starts(word)[0]},key=str))
    sectors=[];cases=[];groups={};P1B=0;sourceleaves=collections.Counter()
    for u in states:
        z=u[0]
        for end,y,q in fwd[u]:
            if q!=2:continue
            for probe,x,qx in fwd[end]:
                if qx!=4:continue
                rU=[r for r in orders(u) if c.recent(r,y)[-1]==x]
                if not rU:continue
                assert c.leaves(u)==c.leaves(end)==2 and degree(end)==2 and degree(u) in (1,2)
                assert x not in set(s.parentmap(end).values())
                three=initial((z,y,x))
                si=len(sectors);sectors.append({'BF_before_zero':u,'BF_after_zero':end,'zero_target':y,'cold_q4':x,
                    'A_before_zero_terms':three,'recent_before_zero':rU,'marked_root_degree_before_zero':degree(u)})
                for old,plus,q0 in inc[u]:
                    if q0==3:
                        P1B+=1
                        raise AssertionError('H2Q3 cannot enter a root of marked degree<=2')
                    if q0!=1:continue
                    rr=[r for r in orders(old) if c.recent(c.recent(r,plus),y)[-1]==x]
                    if not rr:continue
                    word=(old[0],plus,y,x);assert len(set(word))==4
                    for r in rr:assert c.recent(r,plus) in rU
                    aa=initial(word);ci=len(cases)
                    cases.append({'sector':'P1-A','oldroot':old[0],'plus_target':plus,'zero_target':y,'cold_q4':x,
                        'BF_before_plus':old,'BF_after_plus':u,'BF_after_zero':end,'A_initial_terms':len(aa),
                        'recent_orders':len(rr),'final_zero_sector':si,'L_before_plus':c.leaves(old)})
                    sourceleaves[c.leaves(old)]+=1
                    for a in aa:
                        key=(a,old)
                        if key not in groups:groups[key]={'A':a,'BF':old,'recent':set(),'cases':[]}
                        groups[key]['recent'].update(rr);groups[key]['cases'].append(ci)
                    if len(groups)>40000:raise c.Bound()
    records=[];leaf=collections.Counter();physical=0
    for v in groups.values():
        v['recent']=sorted(v['recent']);records.append(v);physical+=len(v['recent']);leaf[c.leaves(v['BF'])]+=len(v['recent'])
    out('final_zero_inverse.json',{'status':'COMPLETE_FINAL_NEUTRAL_ZERO_SOURCE_GRAMMAR','sectors':serial(sectors),
        'sector_count':len(sectors),'universal_H2Q3_output_contexts_degree3plus':q3outputs,
        'H2Q3_composable_sector_count':P1B,'P1B_exclusion':'source root degree<=2 versus Q3 destination degree>=3',
        'source_engine_calls':c.account['source_engine_calls'],'new_finite_tests':0})
    result={'status':'COMPLETE_NEW_P1Z_TERMINAL_SEED_GRAMMAR','groups':serial(records),'terminal_cases':serial(cases),
        'BF_density_contexts':len(states),'BF_source_edges':sum(map(len,fwd.values())),
        'final_zero_sectors':len(sectors),'P1B_composable_cases':P1B,'A_word_frame_queries':initial.cache_info().misses,
        'term_BF_groups':len(records),'term_BF_recent_records':physical,'seed_leaf_distribution':dict(leaf),
        'P1A_BF_case_source_leaves':dict(sourceleaves),'A_infeasible_BF_cases':sum(v['A_initial_terms']==0 for v in cases),
        'source_engine_calls':c.account['source_engine_calls'],'new_finite_tests':0,
        'coverage':'complete new source sectors and lifted g,plus,zero,cold A word; no old terminal set reused'}
    out('terminal_seeds.json',result);print(json.dumps({k:v for k,v in result.items() if k not in ('groups','terminal_cases')}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_seeds_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,**c.account})

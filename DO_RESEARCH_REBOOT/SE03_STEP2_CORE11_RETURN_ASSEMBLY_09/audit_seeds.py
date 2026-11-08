"""NEW genuine q5/q1 destination sectors and budget-consuming +1 seeds.
Both future A events and the actual successor label are retained.
"""
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
def degree(b):return sum(v==b[0] for v in s.parentmap(b).values())
def main():
    states=[t for t in g.BF(1,11) if t[0] in c.MM];SS=set(states);inc=collections.defaultdict(list);fwd=collections.defaultdict(list)
    for t in states:
        guard()
        for x in c.M:
            if x==t[0]:continue
            n=c.bm(t,x)
            if n:
                end,q=n;assert end in SS;fwd[t].append((end,x,q));inc[end].append((t,x,q))
                if q==2:assert c.leaves(end)>=2
                if q==3:assert degree(end)>=3
                if q==4:assert degree(end)>=4
    perms=list(itertools.permutations(c.M))
    @functools.lru_cache(None)
    def orders(t):return tuple(r for r in perms if r[0]==t[0] and s.heap(t,r))
    @functools.lru_cache(None)
    def initial(word):return tuple(sorted({s.canon(t) for t in tr.starts(word)[0]},key=str))
    sectors=[];destination={};combined={};cases=[];aliases=collections.Counter();Q3incoming=0
    for f in states:
        y=f[0]
        for mid,x,q in fwd[f]:
            if q!=5:continue
            assert c.leaves(f)==degree(f)==1 and c.leaves(mid)==degree(mid)==5
            rf=[r for r in orders(f) if r[-1]==x];assert len(rf)==1
            for end,v,qq in fwd[mid]:
                assert qq==1 and v in (1,11) and v!=x and c.leaves(end)==4 and degree(end)==1
                aa=initial((y,x,v));si=len(sectors);rm=c.recent(rf[0],x);re=c.recent(rm,v)
                sectors.append({'BF_before_pair':f,'BF_between_macros':mid,'BF_after_pair':end,
                    'first_target':x,'actual_successor':v,'A_before_pair_terms':aa,'recent_before_pair':rf,
                    'recent_between_macros':rm,'recent_after_pair':re,'successor_is_chart_miss':v not in rm[:5],
                    'costs':{'H_first':1,'H_second':1,'Q_first':5,'Q_second':1,'packet_w':-2}})
                for a in aa:
                    key=(a,f)
                    if key not in destination:destination[key]={'A':a,'BF':f,'recent':set(),'sectors':[]}
                    destination[key]['recent'].update(rf);destination[key]['sectors'].append(si)
                # No genuine zero packet can enter any paired destination L1.
                for before,z,q0 in inc[f]:
                    if q0==3:Q3incoming+=1;raise AssertionError('H2Q3 cannot enter a marked chain of degree1')
                    if q0!=1:continue
                    rp=[r for r in orders(before) if c.recent(r,z)==rf[0]]
                    if not rp:continue
                    assert z==y and c.leaves(before)==degree(before)==2 and before[0] not in (x,y)
                    word=(before[0],y,x,v);terms=initial(word);ci=len(cases)
                    alias='successor_is_old_root' if v==before[0] else 'successor_is_pair_source_root' if v==y else 'four_distinct'
                    aliases[alias]+=1
                    cases.append({'oldroot':before[0],'plus_target':y,'first_target':x,'actual_successor':v,
                        'BF_before_plus':before,'BF_before_pair':f,'BF_between_macros':mid,'BF_after_pair':end,
                        'paired_sector':si,'A_initial_terms':len(terms),'recent_orders':len(rp),'alias':alias})
                    for a in terms:
                        key=(a,before)
                        if key not in combined:combined[key]={'A':a,'BF':before,'recent':set(),'cases':[]}
                        combined[key]['recent'].update(rp);combined[key]['cases'].append(ci)
    def pack(groups):
        data=[]
        for v in groups.values():v['recent']=sorted(v['recent']);data.append(v)
        return data
    dg=pack(destination);cg=pack(combined)
    out('paired_destination_seeds.json',{'status':'COMPLETE_PAIRED_DESTINATION_NECESSARY_GRAMMAR','budget':1,
        'sectors':serial(sectors),'groups':serial(dg),'sector_count':len(sectors),
        'BF_source_contexts':len({v['BF_before_pair'] for v in sectors}),
        'term_BF_groups':len(dg),'term_BF_recent_records':sum(len(v['recent']) for v in dg),
        'incoming_genuine_zero':'NONE: every zero destination has at least2 marked leaves',
        'incoming_H2Q3':Q3incoming,'successor_miss_sectors':sum(v['successor_is_chart_miss'] for v in sectors),
        'both_actual_A_events_required':True,'source_engine_calls':c.account['source_engine_calls'],'new_finite_tests':0})
    result={'status':'COMPLETE_NEW_PAIRED_FINAL_PLUS1_SEEDS','groups':serial(cg),'terminal_cases':serial(cases),
        'budget':0,'BF_contexts':len(states),'BF_edges':sum(map(len,fwd.values())),
        'paired_sectors':len(sectors),'paired_source_BF_contexts':len({v['BF_before_pair'] for v in sectors}),
        'P1B_composable_cases':Q3incoming,'aliases':dict(aliases),'A_word_queries':initial.cache_info().misses,
        'term_BF_groups':len(cg),'term_BF_recent_records':sum(len(v['recent']) for v in cg),
        'A_infeasible_compositions':sum(not v['A_initial_terms'] for v in cases),
        'source_engine_calls':c.account['source_engine_calls'],'new_finite_tests':0,
        'coverage':'all actual future q5/q1 choices, both future H1 events, new incoming +1 sector, private gaps free'}
    out('terminal_seeds.json',result);print(json.dumps({k:v for k,v in result.items() if k not in ('groups','terminal_cases')}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_seeds_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,**c.account})

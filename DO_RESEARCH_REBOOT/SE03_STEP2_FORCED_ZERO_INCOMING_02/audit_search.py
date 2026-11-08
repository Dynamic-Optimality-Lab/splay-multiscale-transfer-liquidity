"""Bounded exact-source return search. No finite failure is a barrier proof."""
import collections,functools,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;OLD=B.parent/'SE03_STEP2_COLD_NEG2_01'
sys.path.insert(0,str(OLD))
from source_model import trace,core,labels
M=(1,3,5,7,9,11);ALL=set(range(1,12));started=time.process_time()
CPU_LIMIT=min(45,float(sys.argv[1])-3);STATE_LIMIT=25000;PROPOSAL_LIMIT=200000;SPLAY_LIMIT=1500000
account={'source_engine_calls':0,'new_finite_tests':0};proposals=0;states_total=0
class Bound(Exception):pass
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def freeze(v):return tuple(freeze(x) for x in v) if isinstance(v,list) else v
def limits():
    if time.process_time()-started>=CPU_LIMIT or states_total>=STATE_LIMIT or proposals>=PROPOSAL_LIMIT or account['source_engine_calls']>=SPLAY_LIMIT:raise Bound()
@functools.lru_cache(maxsize=100000)
def move(t,x):
    account['source_engine_calls']+=1
    if account['source_engine_calls']%128==0:limits()
    n,p,ev=trace(t,x)
    return n,len(ev),sum(e['kind']=='DOUBLE' for e in ev),all(e['kind']=='DOUBLE' and e['case'] in ('LL','RR') and e['G'] in M and e['P'] not in M for e in ev)
def bmove(b,x):
    z,a,q,ss=move(b,x)
    if not ss or labels(core(z,set(M)))!=ALL:return None
    return z,q
def recent(lru,x):return (x,)+tuple(y for y in lru if y!=x)
def epre(e,g,z):
    yield e,[]
    if g!=z:
        n=move(e,g)[0]
        if n!=e:yield n,[('K',g)]
def macro(s,x,H,z):
    a,b,e,lru=s;g=b[0];bb=bmove(b,x)
    if bb is None:return
    nb,q=bb;an,ac,_,_=move(a,x);variants=[]
    if ac==H:variants.append((an,[('K',x)]))
    if H==2 and ac<=2:
        for y in range(1,12):
            ay,hy,_,_=move(a,y)
            if hy!=1:continue
            ax,hx,_,_=move(ay,x)
            if hx==1:variants.append((ax,[('D',y),('K',x)]))
    seen=set()
    for ep,pre in epre(e,g,z):
        ne=move(ep,x)[0] if x!=z else ep
        for na,word in variants:
            ns=(na,nb,ne,recent(lru,x))
            if ns in seen:continue
            seen.add(ns);yield ns,pre+word,q
def forced_trigger(s,z):
    a,b,e,lru=s;x=lru[-1]
    bn=bmove(b,x)
    if bn is None:return None
    an,ac,_,_=move(a,x);nb,q=bn
    if ac!=1:return None
    if q==4:return [('K',x)]
    if q==5:
        g=b[0];ret=bmove(nb,g)
        if ret and ret[1]==1 and move(an,g)[1]==1:return [('K',x),('K',g)]
    return None
def edges(s,z):
    global proposals
    a,b,e,lru=s;g=b[0]
    for x in M:
        if x==g:continue
        bm=bmove(b,x)
        if bm is None:continue
        nb,q=bm
        if q in (1,2):
            for ns,word,_ in macro(s,x,1,z):
                proposals+=1;limits();yield ns,word,2-q,1,q
        if q in (3,4):
            for ns,word,_ in macro(s,x,2,z):
                proposals+=1;limits();yield ns,word,4-q,2,q
        if q==5:
            # A first-H1 source would already have a cold NEG2 trigger.
            # Both genuine macros remain actual, with optional root no-ops.
            for h1,h2 in ((2,1),(1,2)):
                for mid,w1,_ in macro(s,x,h1,z):
                    for y in (1,11):
                        if y==x:continue
                        bm2=bmove(mid[1],y)
                        if bm2 is None or bm2[1]!=1:continue
                        for ns,w2,_ in macro(mid,y,h2,z):
                            proposals+=1;limits();yield ns,w1+w2,0,3,6
def main():
    global states_total
    seeds=json.loads((B/'forced_regions.json').read_text())['records'];reports=[];found=None
    for seed in seeds:
        q=seed['T_state'];s0=(freeze(q['A']),freeze(q['BF']),freeze(q['BE']),tuple(q['recent']));z=q['erased']
        best={s0:0};parent={s0:None};todo=collections.deque([(s0,0)]);popped=0;reason='EXHAUSTED_RESTRICTED_SOURCE_FAMILY'
        states_total+=1
        try:
            while todo:
                limits();s,c=todo.popleft()
                if best.get(s)!=c:continue
                popped+=1;trigger=forced_trigger(s,z)
                if trigger:
                    steps=[];u=s
                    while parent[u] is not None:
                        v,word,w,H,Q=parent[u];steps.append({'word':word,'w':w,'H':H,'Q':Q,'start':v,'end':u});u=v
                    steps.reverse()
                    found={'seed_family':seed['family'],'erased':z,'start_T':s0,'end_candidate_F':s,'return_weight':c,
                        'return_packets':steps,'negative_trigger':trigger,'original_prefix_through_first_T':seed['prefix_through_T'],
                        'status':'REACHABLE_SOURCE_CANDIDATE_REQUIRES_CLOSED_EMBEDDING_AND_AUDIT'}
                    reason='CANDIDATE_FOUND';break
                for ns,word,w,H,Q in edges(s,z):
                    nc=c+w
                    if nc>1 or best.get(ns,2)<=nc:continue
                    if ns not in best:states_total+=1
                    best[ns]=nc;parent[ns]=(s,word,w,H,Q)
                    (todo.appendleft if w==0 else todo.append)((ns,nc))
            reports.append({'family':seed['family'],'reason':reason,'exact_states':len(best),'popped':popped,
                'remaining_queue':len(todo),'includes_erased_B_in_identity':True})
        except Bound:
            reports.append({'family':seed['family'],'reason':'DECLARED_BOUNDED_SEARCH_LIMIT','exact_states':len(best),'popped':popped,
                'remaining_queue':len(todo),'includes_erased_B_in_identity':True});break
        if found:break
    out('search_result.json',{'status':'SOURCE_CANDIDATE_FOUND' if found else 'NO_ARCHITECTURE_CERTIFICATE_FROM_THIS_BOUNDED_SEARCH',
        'reports':reports,'candidate':found,'states_total':states_total,'candidate_packet_proposals':proposals,
        'source_helpers_searched':'actual distinguished keys1..11 only; arbitrary private-fringe helper targets NOT exhausted',
        'full_state_identity':'actual A,BF,BE,recent; fixed M,z,ready phase per seed; all gap terms retained',
        'packet_types':['H1Q2 zero','H2Q4 zero','H3Q6 zero pair','H1Q1 +1','H2Q3 +1'],
        'no_source_graph_or_solver_modified':True,'universal_barrier_proved':False,
        'limits':{'CPU_seconds':CPU_LIMIT,'exact_states':STATE_LIMIT,'packet_proposals':PROPOSAL_LIMIT,'splay_calls':SPLAY_LIMIT},
        'child_CPU':time.process_time()-started,**account})
    print(json.dumps({'status':'SOURCE_CANDIDATE_FOUND' if found else 'BOUNDED_SEARCH_NO_CERTIFICATE','reports':reports,
        'states':states_total,'proposals':proposals,'CPU':time.process_time()-started,**account}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_search_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,**account})

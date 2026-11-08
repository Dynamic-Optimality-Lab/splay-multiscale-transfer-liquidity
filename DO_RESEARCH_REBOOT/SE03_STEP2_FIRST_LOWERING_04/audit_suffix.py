"""Bounded exact full-state suffix search after the two realized first lowerings.
All distinguished-key H2 helpers are included; possible private-helper gaps
are explicitly retained as unresolved rather than silently excluded.
"""
import collections,functools,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;OLD=B.parent/'SE03_STEP2_COLD_NEG2_01'
sys.path.insert(0,str(OLD))
from source_model import trace,core,labels,path
M=(1,3,5,7,9,11);start=time.process_time();CAP=min(30,float(sys.argv[1])-3)
account={'source_engine_calls':0,'new_finite_tests':0};states_total=proposals=0
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def freeze(v):return tuple(freeze(q) for q in v) if isinstance(v,list) else v
def leaves(t):return 0 if t is None else int(t[0] in M) if t[1] is None and t[2] is None else leaves(t[1])+leaves(t[2])
class Bound(Exception):pass
def limit():
    if time.process_time()-start>=CAP or states_total>=15000 or proposals>=150000 or account['source_engine_calls']>=700000:raise Bound()
@functools.lru_cache(maxsize=100000)
def move(t,x):
    account['source_engine_calls']+=1
    if account['source_engine_calls']%128==0:limit()
    return trace(t,x)
def bm(t,x):
    z,p,ev=move(t,x)
    if any(q['kind']!='DOUBLE' or q['case'] not in ('LL','RR') or q['G'] not in M or q['P'] in M for q in ev):return None
    if labels(core(z,set(M)))!=set(range(1,12)):return None
    return z,len(ev)
def lr(v,x):return (x,)+tuple(k for k in v if k!=x)
def holes2(t,depth=0):
    if isinstance(t,str):return [(t,depth)] if 0<depth<=2 else []
    if depth>=2:return []
    return holes2(t[1],depth+1)+holes2(t[2],depth+1)
def macro(s,x,H,z):
    a,b,e,r=s;n= bm(b,x)
    if n is None:return
    nb,q=n;forms=[];na,_,ev=move(a,x)
    if len(ev)==H:forms.append((na,[('K',x)]))
    if H==2:
        for y in range(1,12):
            ay,_,ev1=move(a,y)
            if len(ev1)!=1:continue
            ax,_,ev2=move(ay,x)
            if len(ev2)==1:forms.append((ax,[('D',y),('K',x)]))
    opts=[(e,[])];g=b[0]
    if g!=z:
        ep=move(e,g)[0]
        if ep!=e:opts.append((ep,[('K',g)]))
    seen=set()
    for ep,pre in opts:
        ne=move(ep,x)[0] if x!=z else ep
        for aa,w in forms:
            t=(aa,nb,ne,lr(r,x))
            if t in seen:continue
            seen.add(t);yield t,pre+w,q
def edges(s,z):
    global proposals
    for x in M:
        if x==s[1][0]:continue
        n=bm(s[1],x)
        if n is None:continue
        if n[1]<=4:
            for H in (1,2):
                w=2*H-n[1]
                if w not in (0,1):continue
                for t,word,q in macro(s,x,H,z):
                    proposals+=1;limit();yield t,word,w,H,q
        if n[1]==5:
            for h1,h2 in ((1,2),(2,1)):
                for mid,w1,_ in macro(s,x,h1,z):
                    for y in (1,11):
                        nn=bm(mid[1],y) if x!=y else None
                        if nn is None or nn[1]!=1:continue
                        for t,w2,_ in macro(mid,y,h2,z):
                            proposals+=1;limit();yield t,w1+w2,0,3,6
def trigger(s):
    a,b,e,r=s;x=r[-1];n=bm(b,x)
    if n is None:return None
    aa,_,ev=move(a,x)
    if len(ev)!=1:return None
    if n[1]==4:return [('K',x)]
    if n[1]==5:
        for y in (1,11):
            ret=bm(n[0],y) if y!=x else None
            if ret and ret[1]==1 and len(move(aa,y)[2])==1:return [('K',x),('K',y)]
    return None
def main():
    global states_total
    reports=[];candidate=None
    for filename,budget in [('entry_family.json',1),('e1_family.json',0)]:
        fam=json.loads((B/filename).read_text());q=fam['critical'][0]['post_lowering_state'];z=q['erased']
        s0=tuple(freeze(q[k]) for k in ('A','BF','BE'))+(tuple(q['recent']),)
        todo=collections.deque([(s0,0)]);best={s0:0};parent={s0:None};states_total+=1
        states=[];es=[];unknown=[];cold=None;why='FINITE_DISTINGUISHED_HELPER_FAMILY_EXHAUSTED'
        try:
            while todo:
                limit();s,c=todo.popleft()
                if best.get(s)!=c:continue
                sid=len(states);states.append({'state':s,'cost':c,'marked_leaves':leaves(core(s[1],set(M)))})
                neg=trigger(s)
                if neg:
                    steps=[];u=s
                    while parent[u] is not None:
                        v,w,p,H,Q=parent[u];steps.append({'word':w,'w':p,'H':H,'Q':Q,'source':v,'target':u});u=v
                    candidate={'family':filename,'suffix_weight':c,'source_postlowering':s0,'end_F':s,
                        'suffix_packets':steps[::-1],'negative_trigger':neg,'status':'SOURCE_CANDIDATE_REQUIRES_CLOSED_EXTENSION_AND_AUDIT'}
                    why='CANDIDATE_FOUND';break
                # A private helper inside a Score-free hole is not an ancestor
                # of any Score. One event to it cannot lower a Score's depth.
                # Such an H2 helper can matter only if the target was already
                # at A depth<=2. Cases satisfying this necessary condition are
                # conservatively retained as OPEN, not treated as valid edges.
                hh=holes2(s[0])
                for x in M:
                    if x==s[1][0]:continue
                    b=bm(s[1],x)
                    if b is None:continue
                    w=4-b[1]
                    if b[1] in (3,4) and w<=budget-c and hh and len(path(s[0],x))<=2:
                        unknown.append({'state':sid,'target':x,'Q':b[1],'remaining_budget':budget-c,'near_holes':hh})
                    if b[1]==5:unknown.append({'state':sid,'Q':5,'reason':'paired H2 private helper not universally expanded'})
                for t,w,p,H,Q in edges(s,z):
                    nc=c+p
                    if nc>budget:continue
                    es.append({'source':s,'target':t,'word':w,'w':p,'H':H,'Q':Q,
                        'leaf_change':leaves(core(t[1],set(M)))-leaves(core(s[1],set(M)))})
                    if best.get(t,budget+1)<=nc:continue
                    if t not in best:states_total+=1
                    best[t]=nc;parent[t]=(s,w,p,H,Q)
                    (todo.appendleft if p==0 else todo.append)((t,nc))
        except Bound:why='PREDECLARED_LIMIT'
        reports.append({'family':filename,'remaining_budget':budget,'reason':why,'states':states,'edges':es,
            'unresolved_private_helper_branches':unknown,'complete_source_closure_candidate':why.endswith('EXHAUSTED') and not unknown,
            'zero_queue':not todo,'complete_cheap_return_found':candidate is not None})
        if candidate:break
    out('suffix_analysis.json',{'status':'CANDIDATE_FOUND' if candidate else 'NO_DISTINGUISHED_HELPER_RETURN_FOUND',
        'reports':reports,'candidate':candidate,'states_total':states_total,'candidate_packet_proposals':proposals,
        'global_suffix_barrier_proved':False,'source_completeness':'requires private-helper lemma and all guards/edges independently checked; no finite-to-universal promotion',
        'limits':{'CPU':CAP,'states':15000,'proposals':150000,'source_splays':700000},**account})
    print(json.dumps({'status':'CANDIDATE_FOUND' if candidate else 'NO_DISTINGUISHED_HELPER_RETURN_FOUND',
        'reports':[{'family':r['family'],'states':len(r['states']),'edges':len(r['edges']),
            'private_helper_cases':len(r['unresolved_private_helper_branches']),'closure_candidate':r['complete_source_closure_candidate']} for r in reports],
        'states_total':states_total,'proposals':proposals,**account}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_suffix_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,**account})

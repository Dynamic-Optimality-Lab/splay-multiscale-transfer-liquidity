"""Bounded constructive TP falsification with original A/B/BE histories.
Not a universal weighted graph or a claim from failed finite searches.
"""
import collections,functools,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;OLD=B.parent/'SE03_STEP2_COLD_NEG2_01'
sys.path.insert(0,str(OLD))
from source_model import N,trace,core,labels
M=(1,3,5,7,9,11);MM=set(M);ALL=set(range(1,12));started=time.process_time();CAP=min(40,float(sys.argv[1])-4)
account={'source_engine_calls':0,'new_finite_tests':0};nstates=proposals=0
class Bound(Exception):pass
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def limit():
    if time.process_time()-started>=CAP or account['source_engine_calls']>=1500000 or nstates>=30000 or proposals>=500000:raise Bound()
@functools.lru_cache(maxsize=180000)
def move(t,x):
    account['source_engine_calls']+=1
    if account['source_engine_calls']%128==0:limit()
    z,p,e=trace(t,x)
    return z,len(e),sum(q['kind']=='DOUBLE' for q in e),all(q['kind']=='DOUBLE' and q['case'] in ('LL','RR') and q['G'] in MM and q['P'] not in MM for q in e)
@functools.lru_cache(maxsize=30000)
def bm(t,x):
    z,a,q,ss=move(t,x)
    return (z,q) if ss and labels(core(z,MM))==ALL else None
@functools.lru_cache(maxsize=30000)
def leaves(t):
    def count(v):return 0 if v is None else int(v[0] in MM) if v[1] is None and v[2] is None else count(v[1])+count(v[2])
    return count(core(t,MM))
def recent(r,x):return (x,)+tuple(y for y in r if y!=x)
def canonical():
    t=N(12,'Q12','Q13')
    for x in range(11,1,-1):t=N(x,'Q'+str(x),t)
    return N(1,N(0,'Q0','Q1'),t)
def b_sources(T0):
    warm=[3,5,7,9,11,9,7,5,3,1];b=e=T0;r=()
    for x in warm:
        b=move(b,x)[0]
        if x!=3:e=move(e,x)[0]
        r=recent(r,x)
    assert b==T0 and r==(1,3,5,7,9,11)
    records=[(b,e,r,warm)];seen={(b,r)};todo=collections.deque([0]);found=[]
    while todo and len(records)<1500 and len(found)<32:
        limit();idx=todo.popleft();b,e,r,w=records[idx];x=r[-1];m=bm(b,x)
        if m and m[1] in (4,5):found.append({'BF':b,'BE':e,'recent':r,'KEEP_provenance':w,'cold':x,'q':m[1]})
        for x in M:
            if x==b[0]:continue
            n=bm(b,x)
            if n is None:continue
            rr=recent(r,x);key=(n[0],rr)
            if key in seen:continue
            seen.add(key);ee=move(e,x)[0] if x!=3 else e
            records.append((n[0],ee,rr,w+[x]));todo.append(len(records)-1)
            if len(records)>=1500:break
    return sorted(found,key=lambda q:(q['q']==5,len(q['KEEP_provenance']))),len(records)
def macro(s,x,H):
    a,b,e,r=s;n=bm(b,x)
    if n is None:return
    nb,q=n;forms=[];na,h,_,_=move(a,x)
    if h==H:forms.append((na,[('K',x)]))
    if H==2 and h<=2:
        for y in (0,12,1,3,5,7,9,11,2,4,6,8,10):
            ay,hy,_,_=move(a,y)
            if hy!=1:continue
            ax,hx,_,_=move(ay,x)
            if hx==1:forms.append((ax,[('D',y),('K',x)]))
    opts=[(e,[])];g=b[0]
    if g!=3:
        ee=move(e,g)[0]
        if ee!=e:opts.append((ee,[('K',g)]))
    seen=set()
    for ep,pre in opts:
        ne=move(ep,x)[0] if x!=3 else ep
        for aa,w in forms:
            t=(aa,nb,ne,recent(r,x))
            if t in seen:continue
            seen.add(t);yield t,pre+w,q
def edges(s):
    global proposals
    for x in M:
        if x==s[1][0]:continue
        n=bm(s[1],x)
        if n is None:continue
        if n[1]<=4:
            for H in (1,2):
                w=2*H-n[1]
                if w not in (0,1):continue
                for t,word,Q in macro(s,x,H):
                    proposals+=1;limit();yield t,word,w,H,Q
        if n[1]==5:
            for h1,h2 in ((1,2),(2,1)):
                for mid,w1,_ in macro(s,x,h1):
                    for y in (1,11):
                        nn=bm(mid[1],y) if y!=x else None
                        if nn is None or nn[1]!=1:continue
                        for t,w2,_ in macro(mid,y,h2):
                            proposals+=1;limit();yield t,w1+w2,0,3,6
def cold_shallow(s):
    a,b,e,r=s;x=r[-1];n=bm(b,x)
    return x if n and n[1]==4 and move(a,x)[1]==1 else None
def main():
    global nstates
    T0=canonical();sources,bcnt=b_sources(T0);reports=[];candidate=None;seedcount=0;seedA=set();stopped=None
    order=(0,12,10,6,8,4,2,1,3,5,7,9,11)
    # Spread both preparation indices before repeating the same pattern.
    pairs=[(order[i],order[(i+j)%len(order)]) for j in range(len(order)) for i in range(len(order))]
    try:
        for srcidx,src in enumerate(sources):
            g=src['BF'][0];x=src['cold'];local=0
            for u,v in pairs:
                prep=[u,v,x,g];a=T0
                for k in prep:a=move(a,k)[0]
                if (srcidx,a) in seedA:continue
                seedA.add((srcidx,a));local+=1
                if local>24:break
                ax,h,_,_=move(a,x)
                if h!=1:continue
                b,q=bm(src['BF'],x);e=move(src['BE'],x)[0] if x!=3 else src['BE'];r=recent(src['recent'],x)
                neg=[('K',x)];aa=ax
                if q==5:
                    ret=bm(b,g)
                    if ret is None or ret[1]!=1 or move(aa,g)[1]!=1:continue
                    aa=move(aa,g)[0];b=ret[0];e=move(e,g)[0] if g!=3 else e;r=recent(r,g);neg.append(('K',g))
                seedcount+=1;s0=(aa,b,e,r);key0=(s0,False)
                best={key0:0};parent={key0:None};todo=collections.deque([(key0,0)]);nstates+=1;limited=False
                while todo:
                    limit();key,c=todo.popleft()
                    if best.get(key)!=c:continue
                    s,lastloss=key
                    for t,word,w,H,Q in edges(s):
                        nc=c+w
                        if nc>1:continue
                        L0,L1=leaves(s[1]),leaves(t[1]);isLoss=(w==0 and H==1 and Q==2 and L0==3 and L1==2)
                        if lastloss and w==0 and H==1 and Q==2 and L0==L1==2:
                            target=cold_shallow(t)
                            if target is not None:
                                steps=[{'word':word,'w':w,'H':H,'Q':Q,'source':s,'target':t,'leaves':[L0,L1]}];k=key
                                while parent[k] is not None:
                                    p,ww,pp,hh,qq=parent[k]
                                    steps.append({'word':ww,'w':pp,'H':hh,'Q':qq,'source':p[0],'target':k[0],
                                        'leaves':[leaves(p[0][1]),leaves(k[0][1])]});k=p
                                candidate={'source_B_provenance':src,'A_preparation':prep,'negative_word':neg,
                                    'initial_common_tree':T0,'T_state':s0,'return_packets':steps[::-1],
                                    'return_weight':nc,'cold_q4_target':target,'F_state':t,
                                    'status':'EXACT_CONSECUTIVE_SOURCE_CANDIDATE_NEEDS_CLOSED_EMBEDDING_AND_AUDIT'}
                                break
                        nk=(t,isLoss)
                        if best.get(nk,2)<=nc:continue
                        if nk not in best:nstates+=1
                        best[nk]=nc;parent[nk]=(key,word,w,H,Q)
                        (todo.appendleft if w==0 else todo.append)((nk,nc))
                    if candidate:break
                    if len(best)>=300:limited=True;break
                reports.append({'B_source':srcidx,'prep':prep,'records':len(best),'queue':len(todo),'local_limit':limited})
                if candidate:break
            if candidate:break
    except Bound:stopped='PREDECLARED_GLOBAL_SOURCE_SEARCH_BOUND'
    out('counterattack.json',{'status':'CANONICAL_SOURCE_CANDIDATE_FOUND' if candidate else 'FINITE_NO_COUNTERCERTIFICATE',
        'candidate':candidate,'B_source_construction_records':bcnt,'negative_B_sources':len(sources),
        'actual_A_seeds_tested':seedcount,'reports':reports,'states_total':nstates,'packet_proposals':proposals,
        'stop_reason':stopped or 'DECLARED_SOURCE_FAMILY_EXHAUSTED','source_universe':'physical0..12, M odd1..11; private0/12 never KEEP',
        'last_loss_tag':'temporary word-query metadata, not a new source/frozen controller coordinate',
        'proof_from_negative_search':False,'child_CPU':time.process_time()-started,**account})
    print(json.dumps({'status':'CANONICAL_SOURCE_CANDIDATE_FOUND' if candidate else 'FINITE_NO_COUNTERCERTIFICATE',
        'B_sources':len(sources),'A_seeds':seedcount,'records':nstates,'proposals':proposals,
        'stopped':stopped,'CPU':time.process_time()-started,**account}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_counterattack_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,**account})

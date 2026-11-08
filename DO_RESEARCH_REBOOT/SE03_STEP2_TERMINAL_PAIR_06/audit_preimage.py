"""A different falsification route: all prepared A endpoints on the fixed core.

An exact reachable A preparation replaces the former two-helper seed family.
This is countercertificate discovery only, never finite-to-universal proof.
"""
import collections,json,sys,time
from pathlib import Path
import audit_counterattack as c
B=Path(__file__).resolve().parent
started=time.process_time();CAP=min(48,float(sys.argv[1])-4)
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def guard():
    if time.process_time()-started>CAP or c.account['source_engine_calls']>=1450000 or c.nstates>=100000:raise c.Bound()
def main():
    T0=c.canonical();sources,bcnt=c.b_sources(T0)
    # Each entry is an original DELETE preparation from the common source.
    arr=[T0];pred={T0:None};todo=collections.deque([T0]);Acomplete=False
    while todo:
        guard();a=todo.popleft()
        for x in range(1,12):
            n=c.move(a,x)[0]
            if n in pred:continue
            pred[n]=(a,x);arr.append(n);todo.append(n)
    Acomplete=True
    lookup=collections.defaultdict(list)
    for a in arr:lookup[a[0]].append(a)
    tested=0;candidate=None;localcuts=0
    try:
        # A seed is now the exact PRE-negative source, not a reset x,g suffix.
        for srcidx,src in enumerate(sources):
            g=src['BF'][0];x=src['cold']
            for a in lookup[g]:
                guard();ax,h,_,_=c.move(a,x)
                if h!=1:continue
                b,q=c.bm(src['BF'],x);e=c.move(src['BE'],x)[0] if x!=3 else src['BE'];r=c.recent(src['recent'],x)
                neg=[('K',x)];aa=ax
                if q==5:
                    ret=c.bm(b,g)
                    if ret is None or ret[1]!=1 or c.move(aa,g)[1]!=1:continue
                    aa=c.move(aa,g)[0];b=ret[0];e=c.move(e,g)[0] if g!=3 else e;r=c.recent(r,g);neg.append(('K',g))
                tested+=1;s0=(aa,b,e,r);key0=(s0,False)
                best={key0:0};parent={key0:None};todo=collections.deque([(key0,0)]);c.nstates+=1
                while todo:
                    guard();key,cost=todo.popleft()
                    if best.get(key)!=cost:continue
                    s,lastloss=key
                    for t,word,w,H,Q in c.edges(s):
                        nc=cost+w
                        if nc>1:continue
                        L0,L1=c.leaves(s[1]),c.leaves(t[1]);loss=(w==0 and H==1 and Q==2 and L0==3 and L1==2)
                        if lastloss and w==0 and H==1 and Q==2 and L0==L1==2:
                            target=c.cold_shallow(t)
                            if target is not None:
                                steps=[{'word':word,'w':w,'H':H,'Q':Q,'source':s,'target':t,'leaves':[L0,L1]}];k=key
                                while parent[k] is not None:
                                    p,ww,pp,hh,qq=parent[k]
                                    steps.append({'word':ww,'w':pp,'H':hh,'Q':qq,'source':p[0],'target':k[0],
                                        'leaves':[c.leaves(p[0][1]),c.leaves(k[0][1])]});k=p
                                aw=[];z=a
                                while pred[z] is not None:z,y=pred[z];aw.append(y)
                                candidate={'source_B_provenance':src,'A_preparation':aw[::-1],'negative_word':neg,
                                    'initial_common_tree':T0,'T_state':s0,'return_packets':steps[::-1],
                                    'return_weight':nc,'cold_q4_target':target,'F_state':t,
                                    'status':'EXACT_SOURCE_CANDIDATE_REQUIRES_CLOSED_EMBEDDING'}
                                break
                        nk=(t,loss)
                        if best.get(nk,2)<=nc:continue
                        if nk not in best:c.nstates+=1
                        best[nk]=nc;parent[nk]=(key,word,w,H,Q)
                        (todo.appendleft if w==0 else todo.append)((nk,nc))
                    if candidate:break
                    if len(best)>=600:localcuts+=1;break
                if candidate:break
            if candidate:break
        stop='DECLARED_FAMILY_EXHAUSTED'
    except c.Bound:stop='PREDECLARED_BOUND'
    result={'status':'CANDIDATE_FOUND' if candidate else 'NO_COUNTERCERTIFICATE_IN_DECLARED_FAMILY',
        'candidate':candidate,'all_core_A_preparations_closed':Acomplete,'A_endpoint_count':len(arr),
        'A_seeds_tested':tested,'B_sources':len(sources),'B_provenance_construction_records':bcnt,
        'full_states_in_suffix_queries':c.nstates,'local_query_cuts':localcuts,'stop':stop,
        'source_engine_calls':c.account['source_engine_calls'],'child_CPU':time.process_time()-started,
        'proof_from_negative_search':False,'new_finite_tests':0}
    out('preimage.json',result)
    print(json.dumps({k:v for k,v in result.items() if k!='candidate'}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_preimage_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,**c.account})

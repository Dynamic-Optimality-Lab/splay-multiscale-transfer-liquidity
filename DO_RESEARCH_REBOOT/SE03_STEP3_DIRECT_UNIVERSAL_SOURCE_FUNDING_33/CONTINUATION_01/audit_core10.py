"""Extract an actual LOW deficit path, and embed it in a source-closed word.
No HIGH_ANY_ENDPOINT edge is allowed into this source certificate.
"""
import json,pickle,time,sys,collections,importlib.util
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent.parent;CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);START=time.process_time();queries=0
def fr(v):return tuple(map(fr,v)) if isinstance(v,list) else v
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    global queries
    Z=json.loads((B/'native10_source_actions.json').read_text());T=list(map(fr,Z['trees']));N=len(T);D=Z['destination'];H=Z['H'];Q=Z['Q'];mirror=Z['mirror'];index={t:i for i,t in enumerate(T)}
    with (B/'native10_debt_01.pkl').open('rb') as f:S0=pickle.load(f)
    chosen=None
    for end,val in S0['level'].items():
        if val<3:continue
        v=end;seen=set();chain=[]
        while v in S0['parent'] and v not in seen and len(chain)<500:
            seen.add(v);e=S0['parent'][v]
            if e[0]=='HIGH_ANY_ENDPOINT':break
            chain.append((e[1],v,e));v=e[1]
        if v not in S0['parent'] and sum(e[2][4] for e in chain)<=-3:chosen=(v,list(reversed(chain)));break
    if chosen is None:
        out('native10_width2_path_extraction.json',{'status':'NO_ALL_ACTUAL_LOW_PARENT_PATH_EXTRACTED','source_queries':0,'principal_U33':'OPEN'});print('No all-actual LOW path extracted');return
    start,chain=chosen;a0,b0=divmod(start,N);a,b=a0,b0;window=[];pack=[]
    def canon(a,b):return min(a*N+b,mirror[a]*N+mirror[b])
    for src,dst,e in chain:
        assert canon(a,b)==src;aa,bb=divmod(src,N);_,_,y,x,w=e;options=[]
        for yy,xx in ((y,x),(11-y if y else 0,11-x)):
            at=aa;cost=0
            if yy:cost+=H[at][yy-1];at=D[at][yy-1]
            cost+=H[at][xx-1];at=D[at][xx-1];bt=D[bb][xx-1]
            if canon(at,bt)==dst and 2*cost-Q[bb][xx-1]==w:options.append((yy,xx))
        assert options;yy,xx=options[0]
        if a*N+b!=src:yy=11-yy if yy else 0;xx=11-xx
        before=(a,b);ops=[];cost=0
        if yy:ops.append(('D',yy));cost+=H[a][yy-1];a=D[a][yy-1]
        ops.append(('K',xx));cost+=H[a][xx-1];a=D[a][xx-1];q=Q[b][xx-1];b=D[b][xx-1]
        assert cost in (1,2) and 2*cost-q==w and canon(a,b)==dst
        window+=ops;pack.append({'operations':ops,'H':cost,'Q':q,'weight':w,'before_indices':before,'after_indices':(a,b)})
    assert sum(p['weight'] for p in pack)<=-3
    def bfs(s,t):
        par={s:None};queue=collections.deque([s])
        while queue and t not in par:
            v=queue.popleft()
            for x,u in enumerate(D[v],1):
                if u not in par:par[u]=(v,x);queue.append(u)
        if t not in par:raise ValueError('source reachability bridge failed')
        word=[];v=t
        while v!=s:v,x=par[v];word.append(x)
        return list(reversed(word))
    g=T[b0][0];bpre=next(s for s,t in enumerate(T) if t[0]!=g and D[s][g-1]==b0);prefix=[('D',x) for x in bfs(bpre,a0)]+[('K',g)]
    sp=importlib.util.spec_from_file_location('native10_actual_width_path33',P/'SE03_STEP2_COLD_NEG2_01/source_model.py');S=importlib.util.module_from_spec(sp);sp.loader.exec_module(S);p0=S.path
    def path(t,x):
        global queries
        if queries>=QCAP or time.process_time()-START>CAP-2:raise TimeoutError('SOURCE_REPLAY_CAP')
        queries+=1;return p0(t,x)
    S.path=path;r10=index[S.vine(10)];suffixK=bfs(b,r10)+list(range(2,11))+list(range(9,0,-1))+bfs(r10,bpre)
    acur=a
    for x in suffixK:acur=D[acur][x-1]
    suffix=[('K',x) for x in suffixK]+[('D',x) for x in bfs(acur,bpre)];word=prefix+window+suffix;initial=T[bpre]
    out('native10_width2_source_candidate.json',{'initial_diagonal':initial,'word':word,'window_start_local':len(prefix)+1,'window_end_local':len(prefix)+len(window),'packet_costs':pack,'path_weight':sum(p['weight'] for p in pack),'producer_dependency':'all actual LOW edges only; no HIGH hyperedge','principal_U33':'OPEN'})
    state=(initial,initial,initial);seen={};copies=[];j=0
    def onecopy():
        nonlocal state,j
        rr=[]
        for local,(mode,x) in enumerate(word,1):
            t=j*len(word)+local;before=state;aa,bb,ee=state;aa,pa,ea=S.trace(aa,x);pb=pe='';eb=ev=[]
            if mode=='K':bb,pb,eb=S.trace(bb,x)
            if mode=='K' and x!=10:ee,pe,ev=S.trace(ee,x)
            state=(aa,bb,ee);rr.append({'occurrence':t,'mode':mode,'target':x,'genuine_F':mode=='K' and before[1][0]!=x,'before':before,'after':state,'A_path':pa,'BF_path':pb,'BE_path':pe,'A_events':ea,'BF_events':eb,'BE_events':ev,'a':len(ea),'qF':len(pb)//2,'qE':len(pe)//2})
        assert state[:2]==(initial,initial);copies.append(rr);j+=1
    while state[2] not in seen:
        assert j<30;seen[state[2]]=j;onecopy()
    u0=seen[state[2]];L=j-u0;u=max(u0,1)
    while j<u+L:onecopy()
    rows=sum(copies[u:u+L],[]);assert rows[0]['before']==rows[-1]['after'];base=u*len(word);lo=base+len(prefix)+1;hi=base+len(prefix)+len(window);M={r['target'] for r in rows if r['genuine_F']};assert M==set(range(1,11))
    actual=[];cursor=lo
    for p in pack:
        seg=[r for r in rows if cursor<=r['occurrence']<cursor+len(p['operations'])];h=sum(r['a'] for r in seg);q=sum(r['qF'] for r in seg);assert (h,q)==(p['H'],p['Q']) and seg[-1]['genuine_F'];actual.append({'occurrences':[r['occurrence'] for r in seg],'H':h,'Q':q,'weight':2*h-q});cursor+=len(seg)
    assert cursor==hi+1 and sum(p['weight'] for p in actual)<=-3
    result={'status':'SOURCE_EXACT_NATURAL_WIDTH_TWO_REFUTED_ON_NATIVE10','initial_diagonal':initial,'word':word,'reaching_prefix':word*u,'erased_key':10,'u':u,'L':L,'period':[rows[0]['occurrence'],rows[-1]['occurrence']],'rows':rows,'genuine_KEEP_keys':sorted(M),'window':[lo,hi],'window_packets':actual,'window_weight':sum(p['weight'] for p in actual),'A':sum(r['a'] for r in rows),'QF':sum(r['qF'] for r in rows),'QE':sum(r['qE'] for r in rows),'paired_and_erased_closed':True,'required_debt_range_at_least':3,'only_refuted':'width<=2 on EVERY genuine NATURAL packet, including native10 support; original GateU allows larger range/grouping','CD_refutation':False,'principal_U33':'OPEN','source_queries':queries}
    assert 2*result['A']>=result['QF'];out('native10_width2_source_countercertificate.json',result);print(json.dumps({k:result[k] for k in ('status','window_weight','A','QF','u','L','source_queries')}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_core10_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':queries,'source_engine_calls':queries})

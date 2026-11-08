"""Producer construction in actual full/erased B product; no universal inference."""
import collections,functools,json,sys,time
import audit_construct as C
B=C.B;p=C.p;L=C.L;M=C.M;E=C.E;S=C.S;V=C.V
START=time.process_time();CAP=float(sys.argv[1])
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
@functools.lru_cache(None)
def nxt(t,x):return C.tr(t,x)[0]
@functools.lru_cache(None)
def core(t):return len(p.labels(p.core(t,E)))
@functools.lru_cache(None)
def full_moves(t):return tuple(C.moves(t))
@functools.lru_cache(None)
def goal(t):return C.guard_goal(t)
def main():
    tour=list(sorted(M))+list(sorted(M,reverse=True))[1:]
    ee=V;hist=[];seen={}
    while ee not in seen and len(hist)<15:
        seen[ee]=len(hist);hist.append(ee);bf=V
        for x in tour:
            bf=nxt(bf,x)
            if x!=11:ee=nxt(ee,x)
        assert bf==V
    assert ee in seen
    u=seen[ee];period=len(hist)-u
    assert period==1 and core(ee)>=9
    base=(V,ee);states=[base];ids={base:0};parent=[None];adj=[];rev=[[]];queue=collections.deque([0])
    while queue and len(states)<22000 and time.process_time()-START<min(12,CAP-5):
        i=queue.popleft();bf,be=states[i];edges=[]
        for x,bf2 in full_moves(bf):
            be2=be if x==11 else nxt(be,x)
            if core(be2)<9:continue
            z=(bf2,be2)
            if z not in ids:
                ids[z]=len(states);states.append(z);parent.append((i,x));rev.append([]);queue.append(ids[z])
            j=ids[z];edges.append((x,j));rev[j].append((i,x))
        while len(adj)<=i:adj.append([])
        adj[i]=edges
    while len(adj)<len(states):adj.append([])
    # SCCs in the explored actual graph. No exhaustiveness claim needed for a found cycle.
    visited=set();order=[]
    for i in range(len(states)):
        if i in visited:continue
        visited.add(i);stack=[(i,0)]
        while stack:
            a,k=stack[-1]
            if k<len(adj[a]):
                stack[-1]=(a,k+1);z=adj[a][k][1]
                if z not in visited:visited.add(z);stack.append((z,0))
            else:order.append(a);stack.pop()
    component=[-1]*len(states);sizes=[]
    for i in reversed(order):
        if component[i]>=0:continue
        ci=len(sizes);count=0;stack=[i];component[i]=ci
        while stack:
            a=stack.pop();count+=1
            for z,x in rev[a]:
                if component[z]<0:component[z]=ci;stack.append(z)
        sizes.append(count)
    starts=[i for i,(bf,be) in enumerate(states) if bf==S and sizes[component[i]]>5]
    out('product_graph_receipt.json',{'status':'BOUNDED_ACTUAL_SOURCE_GRAPH_NOT_UNIVERSAL_PROOF','states':len(states),
        'expanded':sum(bool(a) for a in adj),'queue_exhausted':not queue,'Sstar_starts':len(starts),
        'max_SCC':max(sizes),'component_sizes':sorted(sizes,reverse=True)[:20],'common_reaching_tour':tour,'base_u':u,
        'source_engine_calls':C.calls,'source_queries':C.queries})
    print(json.dumps({'states':len(states),'starts':len(starts),'maxSCC':max(sizes),'CPU':time.process_time()-START}),flush=True)
    answer=None;attempts=[]
    def step(i,x):return next((j for y,j in adj[i] if x==y),None)
    for start in starts:
        C.check();ci=component[start];cur=start;ok=True
        for x in (5,7,9):
            cur=step(cur,x)
            if cur is None or component[cur]!=ci:ok=False;break
        if not ok:continue
        pp={cur:None};todo=collections.deque([cur]);target=None
        while todo and len(pp)<8000 and time.process_time()-START<CAP-2:
            a=todo.popleft();bf,be=states[a];x=goal(bf)
            if x:
                z=a;qs=[]
                for k in (13,1,13,11,1,13,1,x):
                    qs.append(len(C.path(states[z][1],k))//2 if k!=11 else 0)
                    z=step(z,k)
                    if z is None or component[z]!=ci:break
                else:
                    if qs[5:]==[1,1,4]:target=(a,z,x,qs);break
            for k,z in adj[a]:
                if component[z]!=ci or z in pp:continue
                ch=C.signature(states[z][0])
                if not ch[7] or not ch[9]:continue
                pp[z]=(a,k);todo.append(z)
        attempts.append({'start':start,'component':ci,'size':sizes[ci],'searched_survivor_states':len(pp),'found':target is not None})
        if target:
            a,z,x,qs=target;route=[]
            while pp[a] is not None:a,k=pp[a];route.append(k)
            route.reverse();back={z:None};todo=collections.deque([z])
            while todo and start not in back:
                a=todo.popleft()
                for k,b in adj[a]:
                    if component[b]==ci and b not in back:back[b]=(a,k);todo.append(b)
            assert start in back;ret=[];a=start
            while back[a] is not None:a,k=back[a];ret.append(k)
            ret.reverse();reach=[];a=start
            while parent[a] is not None:a,k=parent[a];reach.append(k)
            reach.reverse();answer={'start':start,'initial_BF':states[start][0],'initial_BE':states[start][1],
                'route':route,'return':ret,'reach':reach,'x':x,'critical_qE':qs,'tour':tour,'base_u':u};break
    out('product_attempts.json',{'attempts':attempts,'answer':answer,'source_engine_calls':C.calls,'source_queries':C.queries})
    if not answer:
        print('NO_COMPLETE_PRODUCT_CYCLE_IN_BOUNDED_CONSTRUCTION',flush=True);return
    # Turn the actual B cycle into a complete original A/full/erased source.
    tags={};word=[];a=V;bf=S;be=answer['initial_BE']
    prep=list(range(13,0,-1))+[12,1,11,1,13,1,12,1,11,13,1]+[7,5,11,13,1]
    for k in prep:a,_,_=C.tr(a,k)
    initialA=a
    def add(mode,k,label=None):
        nonlocal a,bf,be
        if label:tags[label]=len(word)+1
        a,_,_=C.tr(a,k);word.append((mode,k))
        if mode=='K':
            bf=nxt(bf,k)
            if k!=11:be=nxt(be,k)
    def dels(ks):
        for k in ks:add('D',k)
    def pad():
        root=a[0];child=a[2] if p.node(a[2]) else a[1];y=child[0]
        for _ in range(2):add('D',y);add('D',root)
    for k in (5,7,9):add('K',k,'zero'+str(k))
    for k in answer['route']:pad();add('K',k)
    dels(range(13,0,-1));dels((12,1,11,1,13,1,12,1,11,13,1))
    if answer['x']==3:dels((3,1,13,11,1,12,1,11,13,1))
    for label,k in zip(('j','h','g','s','t','v','p','e'),(13,1,13,11,1,13,1,answer['x'])):add('K',k,label)
    assert answer['return'] and answer['return'][-1]==1
    for k in answer['return'][:-1]:pad();add('K',k)
    dels(prep);add('K',1,'prep_end');assert (a,bf,be)==(initialA,S,answer['initial_BE'])
    rows,end=C.replay(initialA,S,be,word);assert end==(initialA,S,be)
    assert {r['target'] for r in rows if r['genuine_F']}==M
    v,pp,pairs,transport=C.selection(rows)
    arrived=[z for z in transport if z['birth'][0]==tags['e']]
    assert len(arrived)==2 and {z['key'] for z in arrived}=={7,9},arrived
    for label in ('zero5','zero7','zero9','h','g','s','t','v','p','e'):assert rows[tags[label]-1]['a']==1,label
    reachword=[('K',k) for k in tour*u]
    assert answer['reach'] and answer['reach'][-1]==1
    reachword += [('K',k) for k in answer['reach'][:-1]]+[('D',k) for k in prep]+[('K',1)]
    prows,pend=C.replay(V,V,V,reachword);assert pend==(initialA,S,be)
    out('construction_candidate.json',{'status':'GUARDED_SOURCE_CONSTRUCTION_PENDING_BACKEND_AND_INDEPENDENT_AUDIT',
        'original_common_tree':V,'original_reaching_prefix':reachword,'period':word,'initial_A':initialA,'initial_BF':S,
        'initial_BE':be,'rows':rows,'tags':tags,'route':answer['route'],'return':answer['return'],'x':answer['x'],
        'full_marks':sorted(M),'erased':11,'auxiliary_core':core(be),'creator_pairs':pairs,'creator_claims':pp['claims'],
        'selected_transports':transport,'selected_at_e':arrived,'physical_owner_receipt':'PENDING',
        'independent_audit':False,'source_engine_calls':C.calls,'source_queries':C.queries})
    print(json.dumps({'status':'ACTUAL_CLOSED_PRODUCT_SOURCE_FOUND','length':len(word),'x':answer['x'],
        'auxiliary_core':core(be),'arrivals':arrived,'route':answer['route'],'return':answer['return']}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_product_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,
        'source_engine_calls':C.calls,'source_queries':C.queries,'scope':'concrete source construction only'})

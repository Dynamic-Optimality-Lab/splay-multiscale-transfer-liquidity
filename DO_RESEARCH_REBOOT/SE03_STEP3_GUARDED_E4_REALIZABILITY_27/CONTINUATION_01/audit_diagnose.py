"""Reuse saved actual graph to locate a closed B source skeleton; A remains separate."""
import collections,functools,itertools,json,pickle,sys,time
import audit_construct as C
B=C.B;p=C.p;L=C.L;M=C.M;START=time.process_time();CAP=float(sys.argv[1])
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    with (B/'product5_graph_cache.pkl').open('rb') as f:data=pickle.load(f)
    states=data['states'];adj=data['adj'];rev=data['rev'];parent=data['parent'];n=len(states)
    visited=set();order=[]
    for i in range(n):
        if i in visited:continue
        visited.add(i);stack=[(i,0)]
        while stack:
            a,k=stack[-1]
            if k<len(adj[a]):
                stack[-1]=(a,k+1);z=adj[a][k][1]
                if z not in visited:visited.add(z);stack.append((z,0))
            else:order.append(a);stack.pop()
    comp=[-1]*n;sizes=[]
    for i in reversed(order):
        if comp[i]>=0:continue
        ci=len(sizes);stack=[i];count=0;comp[i]=ci
        while stack:
            a=stack.pop();count+=1
            for z,k in rev[a]:
                if comp[z]<0:comp[z]=ci;stack.append(z)
        sizes.append(count)
    @functools.lru_cache(None)
    def children(t):return C.signature(t)
    @functools.lru_cache(None)
    def tree_parents(t):return L.marked_tree(t,M)[0]
    @functools.lru_cache(None)
    def possible_goal(t):
        ch=children(t);root=t[0]
        if root not in {3,5,7,9} or len(ch[root])!=4 or not {1,11,13}<=set(ch[root]) or any(ch[x] for x in (1,11,13)):return None
        chain=[root];v=[x for x in ch[root] if x not in (1,11,13)]
        if len(v)!=1:return None
        a=v[0]
        while True:
            chain.append(a)
            if not ch[a]:break
            if len(ch[a])!=1:return None
            a=ch[a][0]
        if set(chain)!={3,5,7,9}:return None
        z=t
        for x,q in zip((13,1,13,11,1,13,1,a),(1,2,1,3,1,2,1,6)):
            w=C.path(z,x)
            if len(w)!=2*q or any(w[j:j+2] not in ('LL','RR') for j in range(0,len(w),2)):return None
            z,_,_=C.tr(z,x)
        return a
    edges=[dict(e) for e in adj]
    critical=[]
    for i,(bf,be) in enumerate(states):
        if sizes[comp[i]]<=5:continue
        x=possible_goal(bf)
        if not x:continue
        a=i;qs=[]
        for k in (13,1,13,11,1,13,1,x):
            qs.append(len(C.path(states[a][1],k))//2 if k!=11 else 0)
            a=edges[a].get(k)
            if a is None or comp[a]!=comp[i]:break
        else:
            if qs[5:]==[1,1,4]:critical.append({'start':i,'end':a,'x':x,'qE':qs,'component':comp[i]})
    print(json.dumps({'states':n,'critical_closed_skeletons':len(critical),'CPU':time.process_time()-START}),flush=True)
    found=None;tested=[]
    for b,c in itertools.combinations((3,5,7,9),2):
        roots=[q for q in critical if q['x'] not in (b,c)]
        if not roots:continue
        eligible_components={q['component'] for q in roots}
        back={q['start']:None for q in roots};which={q['start']:q for q in roots};queue=collections.deque(back)
        while queue and time.process_time()-START<CAP-3:
            z=queue.popleft()
            for a,k in rev[z]:
                if a in back or comp[a]!=comp[z]:continue
                ch=children(states[a][0])
                if not ch[b] or not ch[c]:continue
                back[a]=(k,z);which[a]=which[z];queue.append(a)
        for i,(bf,be) in enumerate(states):
            if bf[0]!=1 or comp[i] not in eligible_components:continue
            for first in sorted(M-{1,b,c}):
                for second,third in ((b,c),(c,b)):
                    a=i;ok=True
                    for j,k in enumerate((first,second,third)):
                        ch=children(states[a][0]);par=tree_parents(states[a][0]);v=par[k];anc=[]
                        while v is not None:anc.append(v);v=par[v]
                        beta=sum(len(ch[v])>=2 for v in anc)
                        if ch[k] or beta<1 or (j and (len(anc)!=2 or beta!=2)):ok=False;break
                        a=edges[a].get(k)
                        if a is None or comp[a]!=comp[i]:ok=False;break
                    if ok and a in back:
                        q=which[a];route=[];z=a
                        while back[z] is not None:k,z=back[z];route.append(k)
                        ret={q['end']:None};todo=collections.deque([q['end']])
                        while todo and i not in ret:
                            z=todo.popleft()
                            for k,v in adj[z]:
                                if v not in ret and comp[v]==comp[i]:ret[v]=(z,k);todo.append(v)
                        assert i in ret;returnword=[];z=i
                        while ret[z] is not None:z,k=ret[z];returnword.append(k)
                        returnword.reverse();reach=[];z=i
                        while parent[z] is not None:z,k=parent[z];reach.append(k)
                        reach.reverse();found={'initial_BF':bf,'initial_BE':be,'first_three':(first,second,third),
                            'selected_keys':(b,c),'route':route,'critical_x':q['x'],'critical_qE':q['qE'],
                            'return':returnword,'reach':reach,'tour':data['tour'],'base_u':data['u'],
                            'status':'ACTUAL_CLOSED_B_SKELETON_A_COST_SELECTION_AND_OWNERS_NOT_YET_CERTIFIED'};break
                if found:break
            if found:break
        tested.append({'pair':[b,c],'closed_targets':len(roots),'backward_survivor_states':len(back),'found':found is not None})
        if found:break
    out('closed_B_skeleton_diagnosis.json',{'status':'ACTUAL_GRAPH_CONSTRUCTION_DIAGNOSIS_NOT_UNIVERSAL_EXCLUSION',
        'critical':critical,'tested_pairs':tested,'source_engine_calls':C.calls,'source_queries':C.queries})
    if found:out('closed_B_skeleton.json',found)
    with (B/'product5_components.pkl').open('xb') as f:pickle.dump({'components':comp,'sizes':sizes,'critical':critical},f)
    print(json.dumps({'status':'DIAGNOSIS_FINISHED','B_skeleton_found':found is not None,'source_queries':C.queries}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_diagnose_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,
        'source_engine_calls':C.calls,'source_queries':C.queries})

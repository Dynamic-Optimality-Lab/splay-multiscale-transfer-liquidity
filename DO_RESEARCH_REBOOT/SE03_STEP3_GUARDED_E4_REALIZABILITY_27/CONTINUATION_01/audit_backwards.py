"""Source-derived backward lifetime construction in the saved closed component."""
import collections,functools,json,pickle,sys,time
import audit_construct as C
B=C.B;L=C.L;M=C.M;START=time.process_time();CAP=float(sys.argv[1])
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    with (B/'product5_graph_cache.pkl').open('rb') as f:g=pickle.load(f)
    with (B/'product5_components.pkl').open('rb') as f:s=pickle.load(f)
    states=g['states'];adj=g['adj'];rev=g['rev'];comp=s['components'];parent=g['parent']
    @functools.lru_cache(None)
    def shape(t):return L.marked_tree(t,M)
    @functools.lru_cache(None)
    def profile(t,x):
        par,ch=shape(t);anc=[];v=par[x]
        while v is not None:anc.append(v);v=par[v]
        return (len(anc),sum(len(ch[v])>=2 for v in anc),int(not ch[x]))
    reports=[];answers=[]
    for crit in s['critical']:
        available={3,5,7,9}-{crit['x']}
        for aa,bb in __import__('itertools').combinations(sorted(available),2):
            keys=(aa,bb);ci=crit['component'];root=(crit['start'],0,0);seen={root:None};queue=collections.deque([root]);found=None
            while queue and len(seen)<100000 and time.process_time()-START<CAP-3:
                z,mask,pending=cur=queue.popleft()
                if mask==3 and pending==0:found=cur;break
                for a,k in rev[z]:
                    if comp[a]!=ci:continue
                    q,beta,leaf=profile(states[a][0],k);newmask=mask;newpending=0
                    if pending==1:
                        if k in keys or beta+leaf<2:continue
                        newpending=2  # preceding source macro must be a noncritical gap
                    elif pending==2:
                        newpending=0
                    oldch=shape(states[a][0])[1];ok=True
                    for bit,key in enumerate(keys):
                        if mask&(1<<bit):continue
                        if not oldch[key]:
                            if pending or k!=key or (q,beta,leaf)!=(2,2,1):ok=False;break
                            newmask|=1<<bit;newpending=1
                    if not ok:continue
                    nxt=(a,newmask,newpending)
                    if nxt not in seen:seen[nxt]=(cur,k);queue.append(nxt)
            report={'critical':crit,'keys':keys,'states':len(seen),'found':found is not None};reports.append(report)
            if not found:continue
            # The first item preceding the earliest producer is a gap; omit it
            # from the constrained path so it can receive the initial A preparation.
            word=[];records=[];v=found
            while seen[v] is not None:
                n,k=seen[v];word.append(k);records.append({'state':v[0],'after':n[0],'target':k,'mask_before_reverse':v[1],'mask_after_reverse':n[1]});v=n
            start=found[0];ret={crit['end']:None};todo=collections.deque(ret)
            while todo and start not in ret:
                a=todo.popleft()
                for k,z in adj[a]:
                    if comp[z]==ci and z not in ret:ret[z]=(a,k);todo.append(z)
            assert start in ret;rr=[];v=start
            while ret[v] is not None:v,k=ret[v];rr.append(k)
            rr.reverse();reach=[];v=start
            while parent[v] is not None:v,k=parent[v];reach.append(k)
            reach.reverse();ans={'critical':crit,'keys':keys,'initial_BF':states[start][0],'initial_BE':states[start][1],
                'prefix_keep_word':word,'prefix_records':records,'return':rr,'reach':reach,'tour':g['tour'],'base_u':g['u'],
                'status':'CLOSED_B_LIFETIME_AND_ZERO_TAIL_PRODUCER_SKELETON_A_REALIZATION_PENDING'}
            answers.append(ans)
    out('backward_source_skeletons.json',{'status':'ORIGINAL_SOURCE_SKELETON_CONSTRUCTION_NOT_UNIVERSAL_EXCLUSION','reports':reports,'answers':answers})
    print(json.dumps({'reports':reports,'answers':len(answers)}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_backwards_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,
        'source_engine_calls':C.calls,'source_queries':C.queries})

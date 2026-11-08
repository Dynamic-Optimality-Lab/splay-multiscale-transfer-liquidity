"""Filter phantom-support cycles using exact full-support SCCs, then replay
any adverse BF word as an ORIGINAL all-KEEP paired-closed source.
This is a stronger route audit, never a cheap-A/CD countercertificate.
"""
import collections,importlib.util,json,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
s=importlib.util.spec_from_file_location('immutable_scc13',ROOT/'python/independent/splay.py')
I=importlib.util.module_from_spec(s);s.loader.exec_module(I);calls=0
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def tree(t):return ('leaf',t) if isinstance(t,str) else I.node(t[0],tree(t[1]),tree(t[2]))
def plain(t):return t[1] if t[0]=='leaf' else (t[1],plain(t[2]),plain(t[3]))
def move(t,x):
    global calls
    calls+=1;assert calls<2000000 and I.lookup(t,x)[0];return I.trace(t,x)
def qb(e):return sum(x[0]!='ZIG' for x in e)
def core(t,M):
    if t[0]=='leaf':return set()
    a,b=core(t[2],M),core(t[3],M)
    return a|b|{t[1]} if a or b or t[1] in M else set()
def components(n,edges):
    adj=[[] for _ in range(n)];rev=[[] for _ in range(n)]
    for i,(a,b,x,q) in enumerate(edges):adj[a].append(i);rev[b].append(a)
    seen=set();order=[]
    for root in range(n):
        if root in seen:continue
        seen.add(root);stack=[(root,0)]
        while stack:
            a,j=stack[-1]
            if j==len(adj[a]):order.append(a);stack.pop();continue
            stack[-1]=(a,j+1);b=edges[adj[a][j]][1]
            if b not in seen:seen.add(b);stack.append((b,0))
    cc=[-1]*n;groups=[]
    for root in reversed(order):
        if cc[root]>=0:continue
        j=len(groups);group=[];stack=[root];cc[root]=j
        while stack:
            a=stack.pop();group.append(a)
            for b in rev[a]:
                if cc[b]<0:cc[b]=j;stack.append(b)
        groups.append(group)
    return cc,groups,adj
def path(start,end,edges,adj,allowed):
    q=collections.deque([start]);prev={start:None}
    while end not in prev:
        assert q,'no source return path';a=q.popleft()
        for ei in adj[a]:
            b=edges[ei][1]
            if b in allowed and b not in prev:prev[b]=(a,ei);q.append(b)
    result=[];v=end
    while v!=start:a,e=prev[v];result.append(e);v=a
    return list(reversed(result))
def main():
    reports=[]
    for k in (9,10,11):
        supplied=json.loads((B/('bf'+str(k)+'_comparison.json')).read_text());summary=supplied['mask_summaries'][0]
        ts=[tree(t) for t in supplied['trees']];edges=[tuple(e) for e in supplied['edges']];M=set(summary['marks'])
        cc,groups,adj=components(len(ts),edges);good=[];bad=None;totaledges=0
        for j,nodes in enumerate(groups):
            allowed=set(nodes);ee=[i for a in nodes for i in adj[a] if edges[i][1] in allowed]
            marks={edges[i][2] for i in ee}
            if marks!=M:continue
            good.append(j);totaledges+=len(ee);d={a:0 for a in nodes};pred={};length={a:0 for a in nodes};todo=collections.deque(nodes);inside=set(nodes)
            while todo and bad is None:
                a=todo.popleft();inside.remove(a)
                for ei in adj[a]:
                    a,b,x,q=edges[ei]
                    if b not in allowed or d[b]>=d[a]+q-2:continue
                    d[b]=d[a]+q-2;pred[b]=ei;length[b]=length[a]+1
                    if length[b]>=len(nodes):
                        v=b
                        for _ in nodes:v=edges[pred[v]][0]
                        start=v;cycle=[]
                        while True:
                            ei=pred[v];cycle.append(ei);v=edges[ei][0]
                            if v==start:break
                        cycle.reverse();assert sum(2-edges[e][3] for e in cycle)<0
                        bad=(j,cycle);break
                    if b not in inside:todo.append(b);inside.add(b)
            if bad:break
        report={'core':k,'marks':sorted(M),'all_density_states_first_mask':len(ts),'SCC_count':len(groups),
            'full_six_support_SCC_count_scanned':len(good),'full_support_edges_scanned':totaledges,
            'all_masks_complete':False,'status':'NO_NEGATIVE_FULL_SUPPORT_SCC_ON_FIRST_MASK' if bad is None else 'SOURCE_EXACT_BF_ONLY_REPAYMENT_REFUTED'}
        if bad:
            j,cycle=bad;allowed=set(groups[j]);start=edges[cycle[0]][0]
            # Tour ALL six marked access labels and return to the same state.
            tour=[];current=start
            for x in sorted(M):
                ei=next(e for a in groups[j] for e in adj[a] if edges[e][2]==x and edges[e][1] in allowed)
                tour+=path(current,edges[ei][0],edges,adj,allowed);tour.append(ei);current=edges[ei][1]
            tour+=path(current,start,edges,adj,allowed)
            cycprice=sum(2-edges[e][3] for e in cycle);tourprice=sum(2-edges[e][3] for e in tour)
            copies=max(1,tourprice//(-cycprice)+1);word=[('K',edges[e][2]) for e in cycle*copies+tour]
            A=F=R=ts[start];rows=[]
            for t,(m,x) in enumerate(word,1):
                before=A;A,ae=move(A,x);F,be=move(F,x);assert A==F and before[1]!=x
                assert len(core(F,M))==k
                rows.append({'occurrence':t,'mode':m,'target':x,'a':len(ae),'qF':qb(be),
                    'before_A_BF':plain(before),'after_A_BF':plain(A),'actual_A_events':ae,'actual_BF_events':be})
            assert A==F==R and {x for m,x in word}==M
            E=R;seen={};step=0
            z=min(M)
            while E not in seen:
                assert step<50;seen[E]=step;step+=1
                for m,x in word:
                    if x!=z:E=move(E,x)[0]
            L=step-seen[E];E0=E;E=E0
            for _ in range(L):
                for m,x in word:
                    if x!=z:E=move(E,x)[0]
            assert E==E0
            H=sum(v['a'] for v in rows);Q=sum(v['qF'] for v in rows);assert 2*len(rows)-Q<0 and 2*H-Q>=0
            report.update({'negative_cycle':[edges[e] for e in cycle],'negative_cycle_price':cycprice,
                'six_mark_tour':[edges[e] for e in tour],'tour_price':tourprice,'negative_cycle_copies':copies,
                'initial_A_BF':plain(R),'source_word':word,'rows':rows,'all_six_genuine_KEEP_keys':sorted(M),
                'A':H,'QF':Q,'genuine_macros':len(rows),'BF_only_price':2*len(rows)-Q,'actual_signed_margin':2*H-Q,
                'source_reachability':'start from diagonal (R,R); all KEEP, so original A=BF and both close',
                'auxiliary':{'erased':z,'preperiod_word_copies':seen[E0],'period_multiplier':L,'initial_BE':plain(E0),'closed':True},
                'counterexample_scope':'ONLY any B-state-only budget2-per-genuine-access certificate; NOT original CD or physical funding'})
        reports.append(report)
    out('bf_source_refinement.json',{'status':'FULL_SUPPORT_SOURCE_REFINEMENT_AUDITED','reports':reports,'source_engine_calls':calls,
        'source_exclusion_lemma':'every closed six-genuine-support BF walk lies in an SCC whose internal access labels include all six keys',
        'no_AB_cheap_realization_assumed':True})
    print(json.dumps({'status':'PASS_ROUTE_AUDIT','reports':[{k:v for k,v in r.items() if k in ('core','status','A','QF','BF_only_price','actual_signed_margin','full_support_edges_scanned')} for r in reports],'calls':calls}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_refinement_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':calls})

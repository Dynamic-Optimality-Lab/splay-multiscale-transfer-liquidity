"""Exact finite reachable-state teacher. Float LP discovers; integer certificates decide."""
from collections import deque
from fractions import Fraction
import time
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
import networkx as nx
from kernel import shapes,encode,original_splay,json_state,OLD,frontier_features


def build(n):
    start=time.process_time();trees=[encode(t,n) for t in shapes(1,n)];lookup={t:i for i,t in enumerate(trees)};count=len(trees)
    transitions=[]
    for t in trees:
        transitions.append([(lookup[out],d) for out,d in (original_splay(t,x) for x in range(1,n+1))])
    pairs=[(i,i) for i in range(count)];index={p:i for i,p in enumerate(pairs)};parents=[None]*count;edges=[];cursor=0
    while cursor<len(pairs):
        ta,tb=pairs[cursor]
        for x in range(1,n+1):
            na,da=transitions[ta][x-1];nb,db=transitions[tb][x-1]
            for mode,b,q in [('D',tb,0),('K',nb,db//2)]:
                p=(na,b)
                if p not in index:
                    index[p]=len(pairs);pairs.append(p);parents.append([cursor,mode,x])
                edges.append([cursor,index[p],(da+1)//2,q,mode,x])
        cursor+=1
        assert len(pairs)<=20000 and len(edges)<=250000 and time.process_time()-start<=360
    states=[OLD.Tree(json_state(t),list(range(1,n+1))) for t in trees]
    features=[frontier_features(states[a],states[b],True) for a,b in pairs]
    out={'support':n,'trees':trees,'tree_transitions':transitions,'pairs':pairs,'parents':parents,'edges':edges,'features':features,'build_cpu_seconds':time.process_time()-start}
    annotate_recurrence(out);return out


def annotate_recurrence(graph):
    network=nx.DiGraph();network.add_nodes_from(range(len(graph['pairs'])));network.add_edges_from((e[0],e[1]) for e in graph['edges'])
    components=list(nx.strongly_connected_components(network));comp={v:j for j,part in enumerate(components) for v in part}
    graph['SCC']=[comp[i] for i in range(len(graph['pairs']))]
    graph['recurrent_edges']=[i for i,e in enumerate(graph['edges']) if comp[e[0]]==comp[e[1]]]
    graph['SCC_count']=len(components)


def close_edge(graph,eid):
    """Put a selected recurrent edge first in a complete original closed word."""
    edges=graph['edges'];u,v=edges[eid][:2];comp=graph['SCC'];assert comp[u]==comp[v]
    adj=[[] for _ in graph['pairs']]
    for i,e in enumerate(edges):
        if comp[e[0]]==comp[u] and comp[e[1]]==comp[u]:adj[e[0]].append(i)
    queue=deque([v]);seen={v:None}
    while queue and u not in seen:
        at=queue.popleft()
        for i in adj[at]:
            to=edges[i][1]
            if to not in seen:seen[to]=i;queue.append(to)
    assert u in seen;path=[];at=u
    while at!=v:i=seen[at];path.append(i);at=edges[i][0]
    return [eid]+list(reversed(path))


def exact_trial(graph,C):
    """SPFA maximizes walks ending at each state; Phi=-distance/denominator."""
    C=Fraction(C);den,num=C.denominator,C.numerator;edges=graph['edges'];n=len(graph['pairs']);adj=[[] for _ in range(n)]
    for i,e in enumerate(edges):adj[e[0]].append(i)
    distance=[0]*n;pred=[None]*n;length=[0]*n;active=[True]*n;queue=deque(range(n));pops=0;start=time.process_time()
    while queue:
        u=queue.popleft();active[u]=False;pops+=1
        for eid in adj[u]:
            _,v,a,q,_,_=edges[eid];value=distance[u]+den*q-num*a
            if value<=distance[v]:continue
            distance[v]=value;pred[v]=eid;length[v]=length[u]+1
            if length[v]>=n:
                at=v
                for _ in range(n):
                    if pred[at] is None:break
                    at=edges[pred[at]][0]
                else:
                    initial=at;reverse=[]
                    while True:
                        e=pred[at]
                        if e is None:break
                        reverse.append(e);at=edges[e][0]
                        if at==initial:
                            cycle=list(reversed(reverse));gain=sum(den*edges[e][3]-num*edges[e][2] for e in cycle)
                            if gain>0:return {'status':'VIOLATING_CYCLE','C':str(C),'cycle':cycle,'scaled_excess':gain,'pops':pops,'cpu_seconds':time.process_time()-start}
                            break
                        if len(reverse)>n:break
                length[v]=0
            if not active[v]:
                if queue and distance[v]>distance[queue[0]]:queue.appendleft(v)
                else:queue.append(v)
                active[v]=True
        if pops%1000==0:assert time.process_time()-start<=360 and pops<=5000000
    potential=[-z for z in distance]
    assert all(den*q+potential[v]-potential[u]<=num*a for u,v,a,q,_,_ in edges)
    return {'status':'FINITE_EXACT_POTENTIAL','C':str(C),'potential_numerators':potential,'potential_denominator':den,'pops':pops,'cpu_seconds':time.process_time()-start}


def optimum(graph):
    edges=graph['edges'];n=len(graph['pairs']);rows=[];cols=[];values=[]
    for i,(u,v,a,q,_,_) in enumerate(edges):
        rows.extend((i,i,i));cols.extend((u,v,n));values.extend((-1,1,-a))
    matrix=coo_matrix((values,(rows,cols)),shape=(len(edges),n+1)).tocsr();objective=np.zeros(n+1);objective[-1]=1
    result=linprog(objective,A_ub=matrix,b_ub=np.array([-e[3] for e in edges]),bounds=[(None,None)]*n+[(0,None)],method='highs',options={'time_limit':45})
    if result.status!=0:return {'status':'OPEN_NUMERICAL_OPTIMUM','LP_status':int(result.status),'message':result.message}
    C=Fraction(float(result.x[-1])).limit_denominator(max(1,n*((graph['support']+1)//2)))
    upper=exact_trial(graph,C)
    if upper['status']!='FINITE_EXACT_POTENTIAL':return {'status':'OPEN_RATIONAL_RECOVERY','trial':upper,'float_C':float(result.x[-1])}
    p=upper['potential_numerators'];den=upper['potential_denominator'];num=C.numerator
    tight=[i for i,(u,v,a,q,_,_) in enumerate(edges) if den*q+p[v]-p[u]==num*a]
    network=nx.DiGraph();network.add_nodes_from(range(n));network.add_edges_from((edges[i][0],edges[i][1]) for i in tight)
    comp={v:j for j,cc in enumerate(nx.strongly_connected_components(network)) for v in cc};adj=[[] for _ in range(n)]
    for i in tight:adj[edges[i][0]].append(i)
    cycle=None
    if C==0:cycle=[]
    else:
        for eid in tight:
            u,v,a,q,_,_=edges[eid]
            if not a or comp[u]!=comp[v]:continue
            queue=deque([v]);seen={v:None}
            while queue and u not in seen:
                k=queue.popleft()
                for j in adj[k]:
                    to=edges[j][1]
                    if comp[to]==comp[u] and to not in seen:seen[to]=j;queue.append(to)
            assert u in seen
            path=[];at=u
            while at!=v:j=seen[at];path.append(j);at=edges[j][0]
            cycle=[eid]+list(reversed(path));break
    assert cycle is not None
    if cycle:
        aa=sum(edges[i][2] for i in cycle);qq=sum(edges[i][3] for i in cycle);assert aa>0 and Fraction(qq,aa)==C
    return {'status':'FINITE_EXACT_OPTIMUM','C':str(C),'upper_certificate':upper,'attaining_cycle':cycle,'floating_LP_role':'Discovery only; all-edge integer upper certificate plus original tight cycle certify optimum.'}


def graph_rows(graph,columns=12):
    f=graph['features']
    if 'SCC' not in graph:annotate_recurrence(graph)
    return [{'id':['graph',graph['support'],i],'a':e[2],'q':e[3],'delta':[v-u for u,v in zip(f[e[0]][:columns],f[e[1]][:columns])]} for i in graph['recurrent_edges'] for e in [graph['edges'][i]]]

"""Exact SCC/closed-walk extraction from stored original source edges."""
import collections,hashlib,json,pickle,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;B=F.parents[1]/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    p=F/'source13_tight_graph_01.pkl'
    with p.open('rb') as f:z=pickle.load(f)
    assert z['status']=='COMPLETE_RETAINED_EXACT_ZERO_REDUCED_GRAPH'
    keys=z['keys'];rows=z['edges'];records=z['records'];N=len(keys);adj=[[] for _ in keys];rev=[[] for _ in keys]
    for j,e in enumerate(rows):
        u,v,kind,x,h,q=e;assert records[keys[v]][0]-records[keys[u]][0]==q-2*h
        adj[u].append(j);rev[v].append(j)
    seen=set();order=[]
    for root in range(N):
        if root in seen:continue
        seen.add(root);stack=[(root,0)]
        while stack:
            u,k=stack[-1]
            if k==len(adj[u]):order.append(u);stack.pop();continue
            stack[-1]=(u,k+1);v=rows[adj[u][k]][1]
            if v not in seen:seen.add(v);stack.append((v,0))
    comp=[-1]*N;sizes=[]
    for root in reversed(order):
        if comp[root]>=0:continue
        c=len(sizes);stack=[root];comp[root]=c;size=0
        while stack:
            u=stack.pop();size+=1
            for j in rev[u]:
                v=rows[j][0]
                if comp[v]<0:comp[v]=c;stack.append(v)
        sizes.append(size)
    chosen={};labels={};maximum={};internal={}
    for j,e in enumerate(rows):
        u,v,kind,x,h,q=e;c=comp[u]
        if c!=comp[v]:continue
        internal.setdefault(c,[]).append(j);maximum[c]=max(maximum.get(c,0),q)
        if kind=='KEEP' and keys[u][1]!=keys[v][1]:labels.setdefault(c,set()).add(x)
    candidates=[c for c in internal if len(labels.get(c,set()))>=7 and maximum[c]>=3]
    witness=None
    if candidates:
        c=max(candidates,key=lambda c:(len(labels[c]),maximum[c],sizes[c]));select=[];used=set()
        for j in internal[c]:
            u,v,kind,x,h,q=rows[j]
            if kind=='KEEP' and keys[u][1]!=keys[v][1] and x not in used:select.append(j);used.add(x)
        select.append(max(internal[c],key=lambda j:rows[j][5]))
        start=rows[select[0]][0];at=start;walk=[]
        def path(a,b):
            if a==b:return []
            todo=collections.deque([a]);parent={a:None}
            while todo and b not in parent:
                u=todo.popleft()
                for j in adj[u]:
                    v=rows[j][1]
                    if comp[v]==c and v not in parent:parent[v]=(u,j);todo.append(v)
            assert b in parent;out=[];v=b
            while v!=a:u,j=parent[v];out.append(j);v=u
            return out[::-1]
        for j in select:
            u,v,*_=rows[j];walk+=path(at,u);walk.append(j);at=v
        walk+=path(at,start)
        literal=[{'source':keys[rows[j][0]],'destination':keys[rows[j][1]],'kind':rows[j][2],
          'target':rows[j][3],'H':rows[j][4],'Q':rows[j][5]} for j in walk]
        assert sum(e['Q']-2*e['H'] for e in literal)==0 and literal[-1]['destination']==literal[0]['source']
        witness={'edges':literal,'A':sum(e['H'] for e in literal),'Q':sum(e['Q'] for e in literal),
          'genuine_support':sorted(used),'status':'EXACT_FULL_PAIR_CLOSED_PRODUCER_CONTROL; independent replay/closure pending'}
    stats=sorted([{'component':c,'vertices':sizes[c],'edges':len(internal[c]),'genuine_support':sorted(labels.get(c,set())),
      'max_Q':maximum[c]} for c in internal],key=lambda a:(len(a['genuine_support']),a['max_Q'],a['vertices']),reverse=True)[:20]
    out={'status':'TIGHT_SOURCE_CONTROL_FOUND' if witness else 'NO_RELEVANT_ZERO_CYCLE_IN_RETAINED_SUBGRAPH',
      'source_states':N,'source_edges':len(rows),'SCCs':len(sizes),'top_components':stats,'witness':witness,
      'source_queries':0,'source_engine_calls':0,'JR35':'OPEN','passing_finite_result_is_not_universal':True,
      'input_sha256':{str(p):sha(p)}}
    with (F/'source13_tight_cycle_extraction.json').open('x',encoding='utf8') as f:json.dump(out,f,indent=2)
    print(json.dumps({k:v for k,v in out.items() if k not in ('witness','input_sha256')}),flush=True);assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/'audit_proof286_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)

"""Exact closed-source components of the independently checked full B table."""
import collections,hashlib,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1]
B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time()
def main():
    m=json.loads((F/'active_a10_model.json').read_text());n=m['B_count'];edges=m['B_edges']
    out=[[] for _ in range(n)];back=[[] for _ in range(n)]
    for e in edges:out[e['source']].append(e['target']);back[e['target']].append(e['source'])
    seen=set();order=[]
    for s in range(n):
        if s in seen:continue
        seen.add(s);stack=[(s,0)]
        while stack:
            u,i=stack[-1]
            if i<len(out[u]):
                v=out[u][i];stack[-1]=(u,i+1)
                if v not in seen:seen.add(v);stack.append((v,0))
            else:order.append(u);stack.pop()
    labels=[-1]*n;components=[]
    for s in reversed(order):
        if labels[s]>=0:continue
        c=len(components);nodes=[];stack=[s];labels[s]=c
        while stack:
            u=stack.pop();nodes.append(u)
            for v in back[u]:
                if labels[v]<0:labels[v]=c;stack.append(v)
        components.append(nodes)
    masks=[set() for _ in components];counts=[0]*len(components)
    for e in edges:
        if labels[e['source']]==labels[e['target']]:
            c=labels[e['source']];masks[c].add(e['key']);counts[c]+=1
    genuine=[i for i,keys in enumerate(masks) if len(keys)==7]
    rows=[{'id':i,'nodes':len(v),'internal_edges':counts[i],'genuine_target_set':sorted(masks[i]),'all7_closed_scope':i in genuine} for i,v in enumerate(components)]
    r={'status':'EXACT_SCC_SOURCE_COVER','B_states':n,'SCCs':len(components),'component_size_histogram':dict(collections.Counter(map(len,components))),
       'all7_SCCs':genuine,'all7_source_states':sum(len(components[i]) for i in genuine),
       'components':rows,'source_queries':0,'source_engine_calls':0,'JR35':'OPEN',
       'meaning':'a paired-closed all-seven B word stays in one SCC with all seven target labels; conversely such an SCC has a concatenated closed B walk visiting all seven, not a low-cost A lift',
       'input_sha256':{'active_a10_model.json':hashlib.sha256((F/'active_a10_model.json').read_bytes()).hexdigest()}}
    with (F/'closed_B_components.json').open('x',encoding='utf-8') as f:json.dump(r,f,indent=2)
    print(json.dumps({k:v for k,v in r.items() if k not in ('components','input_sha256')}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_proof207_exit.json').open('x',encoding='utf-8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)

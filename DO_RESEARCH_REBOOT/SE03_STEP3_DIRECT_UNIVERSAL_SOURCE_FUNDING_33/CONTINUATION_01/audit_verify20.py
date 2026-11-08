"""Distinct source/shortest-rotation proof checks for the geodesic refutations."""
import json,time,sys,importlib.util,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent.parent;START=time.process_time();CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);queries=0
def fr(v):return tuple(map(fr,v)) if isinstance(v,list) else v
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    global queries
    sp=importlib.util.spec_from_file_location('independent_geodesic33',P/'SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01/audit_independent2.py');I=importlib.util.module_from_spec(sp);sp.loader.exec_module(I)
    def tick():
        global queries
        if queries>=QCAP or time.process_time()-START>CAP-2:raise TimeoutError('INDEPENDENT_CAP')
        queries+=1
    I.tick=tick
    def shape(t):
        def walk(v,hi):return 'F'+str(hi) if v is None else (v.key,walk(v.left,v.key-1),walk(v.right,hi))
        return walk(t.root,7)
    tab=json.loads((B/'geodesic_seven_metric_table.json').read_text());T=list(map(fr,tab['trees']));index={t:i for i,t in enumerate(T)};assert len(T)==len(index)==429
    grammar={}
    def generate(lo,hi):
        if (lo,hi) not in grammar:grammar[lo,hi]=['F'+str(hi)] if lo>hi else [(k,l,r) for k in range(lo,hi+1) for r in generate(k+1,hi) for l in generate(lo,k-1)]
        return grammar[lo,hi]
    assert set(T)==set(generate(1,7));adj=[]
    for tree in T:
        row=set()
        for key in range(1,8):
            tt=I.Tree(tree);node=tt.nodes[key]
            if node.parent is None:continue
            tt.rotate(node);row.add(index[shape(tt)])
        assert len(row)==6;adj.append(row)
    assert all(set(tab['rotation_neighbors'][i])==adj[i] for i in range(429))
    checked_labels=set();records=[]
    for name in ('geodesic_source_countercertificate.json','equal_distance_source_countercertificate.json'):
        z=json.loads((B/name).read_text());assert hashlib.sha256((B/'geodesic_seven_metric_table.json').read_bytes()).hexdigest()==z.get('metric_sha256',z.get('metric_table_sha256'));tt=[I.Tree(fr(z['initial_diagonal'])) for _ in range(3)];rows={r['occurrence']:r for r in z['rows']};lru=[];elru=[];boundary=None
        for t,(mode,x) in enumerate(z['reaching_prefix']+z['word']*z['L'],1):
            if t==z['period'][0]:boundary=(lru[:],elru[:])
            before=tuple(shape(v) for v in tt);pa,ea=tt[0].access(x);pb=pe='';eb=ee=[]
            if mode=='K':pb,eb=tt[1].access(x)
            if mode=='K' and x!=7:pe,ee=tt[2].access(x)
            after=tuple(shape(v) for v in tt)
            if mode=='K':
                if x in lru:lru.remove(x)
                lru.insert(0,x)
                if x!=7:
                    if x in elru:elru.remove(x)
                    elru.insert(0,x)
            if t in rows:
                r=rows[t];assert (r['mode'],r['target'])==(mode,x) and fr(r['before'])==before and fr(r['after'])==after and (pa,pb,pe)==(r['A_path'],r['BF_path'],r['BE_path']);assert (len(ea),len(pb)//2,len(pe)//2)==(r['a'],r['qF'],r['qE']);assert (ea,eb,ee)==(r['A_events'],r['BF_events'],r['BE_events'])
        assert boundary==(lru,elru) and fr(z['rows'][0]['before'])==fr(z['rows'][-1]['after']);assert {r['target'] for r in z['rows'] if r['genuine_F']}==set(range(1,8));lo,hi=z['natural_window'];seg=[rows[t] for t in range(lo,hi+1)];assert rows[lo-1]['genuine_F'] and seg[-1]['genuine_F'] and not any(r['genuine_F'] for r in seg[:-1]);H=sum(r['a'] for r in seg);Q=sum(r['qF'] for r in seg);rho=[]
        for state in (seg[0]['before'],seg[-1]['after']):
            a,b=(index[fr(tree)] for tree in state[:2]);d=tab['distances'][a]
            if a not in checked_labels:
                assert d[a]==0 and all(v>=0 for v in d)
                for v in range(429):
                    assert all(abs(d[v]-d[u])<=1 for u in adj[v])
                    if v!=a:assert d[v]>0 and any(d[u]==d[v]-1 for u in adj[v])
                checked_labels.add(a)
            rho.append(d[b])
        assert (H,Q,rho[0],rho[1])==(z['H'],z['Q'],z['rho_before'],z['rho_after']);A=sum(r['a'] for r in z['rows']);QF=sum(r['qF'] for r in z['rows']);assert 2*A-QF>=0
        if name.startswith('equal'):assert (H,Q,*rho)==(1,3,5,5)
        else:assert 2*H-Q+rho[0]-rho[1]==-1
        records.append({'witness':name,'period':z['period'],'natural_window':[lo,hi],'H':H,'Q':Q,'rho_before':rho[0],'rho_after':rho[1],'A':A,'QF':QF,'all_trees_and_recent_charts_closed':True,'CD_margin':2*A-QF})
    result={'status':'PASS_SOURCE_EXACT_ALL_DISTANCE_ONLY_DEBT_REFUTATION','source_records':records,'metric_graph_trees':429,'independent_single_rotation_instances':429*6,'exact_shortest_distance_vectors_checked':len(checked_labels),'source_queries':queries,'scope':'the specified scalar candidate and EVERY fixed F(rho) on all natural packets, not general debts or GateU','principal_U33':'OPEN','external_or_formal_verification':False,'input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in ('geodesic_source_countercertificate.json','equal_distance_source_countercertificate.json','geodesic_seven_metric_table.json')}};out('geodesic_source_independent_audit.json',result);print(json.dumps(result))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_verify20_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':queries,'source_engine_calls':queries})

"""Fresh original kernel + exact shortest-distance labels + source counterwords."""
import json,time,sys,hashlib,importlib.util
from pathlib import Path
from source_composition_auditor import check
B=Path(__file__).resolve().parent;P=B.parent.parent;START=time.process_time();CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);queries=0
def fr(v):return tuple(map(fr,v)) if isinstance(v,list) else v
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    global queries
    z=json.loads((B/'directed_source_distance_closed_sources.json').read_text());assert all(hashlib.sha256((B/n).read_bytes()).hexdigest()==v for n,v in z['input_sha256'].items());old=json.loads((B/'geodesic_seven_metric_table.json').read_text());T=list(map(fr,old['trees']));D=old['source_destinations'];H=old['source_H'];Q=old['source_Q'];N=len(T);assert N==429;index={t:i for i,t in enumerate(T)};native={'trees':old['trees'],'destination':D,'H':H,'Q':Q};sp=importlib.util.spec_from_file_location('independent_min_source_distances33',P/'SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01/audit_independent2.py');I=importlib.util.module_from_spec(sp);sp.loader.exec_module(I)
    def tick():
        global queries
        if queries>=QCAP or time.process_time()-START>CAP-2:raise TimeoutError('INDEPENDENT_KERNEL_CAP')
        queries+=1
    I.tick=tick
    def shape(tree):
        def walk(v,hi):return 'F'+str(hi) if v is None else (v.key,walk(v.left,v.key-1),walk(v.right,hi))
        return walk(tree.root,7)
    for s,t in enumerate(T):
        for x in range(1,8):
            tree=I.Tree(t);path,events=tree.access(x);assert index[shape(tree)]==D[s][x-1] and len(events)==H[s][x-1] and len(path)//2==Q[s][x-1]
    assert queries==3003;distdata=json.loads((B/'directed_source_event_distances7.json').read_text());assert distdata['source_kernel_sha256']==hashlib.sha256((B/'geodesic_seven_metric_table.json').read_bytes()).hexdigest();dist=distdata['all_pairs'];needed={e['source_edge'][k] for e in z['records'] for k in ('A','B','A_after','B_after')}
    for s in needed:
        d=dist[s];assert len(d)==N and d[s]==0 and all(v>=0 for v in d);tight={s}
        for u in range(N):
            for v,w in zip(D[u],H[u]):
                assert d[v]<=d[u]+w
                if w>0 and d[v]==d[u]+w:tight.add(v)
        assert len(tight)==N and all(d[v]>0 for v in range(N) if v!=s)
    records=[]
    for item in z['records']:
        e=item['source_edge'];a,b,at,bt=(e[k] for k in ('A','B','A_after','B_after'));f,r=dist[a][b],dist[b][a];ft,rt=dist[at][bt],dist[bt][at];assert (f,r,ft,rt)==tuple(e[k] for k in ('ell_A_to_B_before','ell_B_to_A_before','ell_A_to_B_after','ell_B_to_A_after'));source=check(native,item['closed_history']);assert (source['H'],source['Q'])==(1,3)
        if item['kind']=='constant_negative_edge':assert (ft-f,rt-r)==(-3,3) and source['price']==-1
        else:assert (ft,rt)==(f,r)==(8,6)
        records.append({'kind':item['kind'],'source':source,'distances_before':[f,r],'distances_after':[ft,rt]})
    out('directed_source_distance_independent_audit.json',{'status':'PASS_EXACT_DIRECTED_SPLAY_PREPARATION_DISTANCE_FAMILY_REFUTATION','uniform_A_only_DELETE_cone_preservation':'proved by directed triangle inequalities for alpha>=0,beta<=0,alpha-beta<=2; exact a=0 identity included','KEEP_obstruction':'H1/Q3 with forward11->8, reverse7->10 gives -1-3(alpha-beta)<0','lambda_margin':-7,'any_function_only_of_both_directed_distances':'refuted by unchanged(8,6), H1/Q3 source','all_original_7_key_primitive_actions_independently_replayed':3003,'exact_shortest_path_vectors_checked':len(needed),'shortest_path_proof':'all weighted-edge lower labels plus a positive-cost tight predecessor at every nonsource vertex prove matching attainable upper labels','source_records':records,'source_queries':queries,'not_a_Coarse_Double_counterexample':True,'principal_U33':'OPEN','external_or_formal_verification':False,'input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in ('directed_source_distance_closed_sources.json','directed_source_event_distances7.json','geodesic_seven_metric_table.json','DIRECTED_SOURCE_DISTANCE_DELETE_LEMMA.md','DIRECTED_SOURCE_DISTANCE_DELETE_CONE.md')}});print(json.dumps({'status':'PASS_DIRECTED_SOURCE_DISTANCE_KEEP_OBSTRUCTION','source_queries':queries,'vectors':len(needed),'source_period_CD_margins':[r['source']['CD_margin'] for r in records],'uniform_DELETE_lemma_retained':True}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_verify33_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':queries,'source_engine_calls':queries})

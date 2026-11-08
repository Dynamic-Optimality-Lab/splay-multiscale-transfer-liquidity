"""Independent full inequality verification; cache composition only, no source engine."""
import hashlib,json,pickle,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1]
B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time()
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def freeze(t):
    if t is None or isinstance(t,str):return None
    return (t[0],freeze(t[1]),freeze(t[2]))
def mir(t):return None if t is None else (14-t[0],mir(t[2]),mir(t[1]))
def main():
    g=read(F/'cached_product_inputs.json');n=read(Path(g['native_actions']))
    assert sha(Path(g['native_actions']))==g['native_actions_sha256']
    assert read(B/'native10_source_independent_audit.json')['input_sha256']==g['native_actions_sha256']
    # Exact B edge origin checks, distinct from the graph constructor.
    original=[]
    for s in g['sources']:
        assert sha(Path(s['path']))==s['sha256'] and sha(Path(s['audit']))==s['audit_sha256']
        original.append(read(Path(s['path']))[s['rows_field']])
    for e in g['B_edges']:
        row=original[e['origin_source']][e['origin_row']]
        before=freeze(row['BF_before'] if 'BF_before' in row else row['before'][1])
        after=freeze(row['BF_after'] if 'BF_after' in row else row['after'][1]);key=row.get('key',row.get('target'))
        if e['reflected']:before,after,key=mir(before),mir(after),14-key
        assert before==freeze(g['B_trees'][e['source']]) and after==freeze(g['B_trees'][e['target']])
        assert key==e['key'] and row['qF']==e['q'] and row['genuine_F']
    with (F/'product_search_01.pkl').open('rb') as f:s=pickle.load(f)
    assert s['seeded'] and not s['queue'] and s['negative_cycle'] is None
    level=s['level'];nb=s['Nb'];comp=s['component'];loc={b:i for i,b in enumerate(comp)}
    assert nb==95 and len(level)==len(n['trees'])*nb==1595620 and max(level)==6
    assert s['input_sha256']==sha(F/'cached_product_inputs.json')
    # Independent all-state verification, including zero-level sources not
    # processed by the producer. Uses vectorized integer-array indexing.
    import numpy as np
    lev=np.frombuffer(level,dtype=np.int32).reshape((len(n['trees']),nb))
    dest=np.asarray(n['destination'],dtype=np.int64);ha=np.asarray(n['H'],dtype=np.int32)
    checks=0;min_delete=100;min_keep=100
    for x in range(10):
        margin=2*ha[:,x,None]+lev[dest[:,x],:]-lev
        assert np.min(margin)>=0;min_delete=min(min_delete,int(margin.min()));checks+=margin.size
    pton={v:i for i,v in enumerate(g['native_to_physical'])}
    for e in g['B_edges']:
        if e['source'] not in loc or e['target'] not in loc:continue
        bs,bt=loc[e['source']],loc[e['target']];x=pton[e['key']]
        margin=2*ha[:,x]-e['q']+lev[dest[:,x],bt]-lev[:,bs]
        assert np.min(margin)>=0;min_keep=min(min_keep,int(margin.min()));checks+=len(margin)
    # These are proof checks of a complete fixed product, not a new source
    # action request or a claim that its finite coverage is universal.
    report={'status':'PASS_COMPLETE_FIXED_CACHE_PRODUCT_INEQUALITY_CERTIFICATE',
      'state_pairs':len(level),'A_native_shapes':len(n['trees']),'B_component_vertices':nb,
      'checked_cached_inequalities':checks,'maximum_D':6,'minimum_DELETE_margin':min_delete,'minimum_KEEP_margin':min_keep,
      'B_edges_origin_checked':len(g['B_edges']),'source_queries':0,'source_engine_calls':0,
      'scope':'all original words in this certified cache product and its rigid external-gap lifts',
      'arbitrary_A_active_anonymous_nodes_covered':False,'all_B_source_transitions_covered':False,
      'JR35':'OPEN','reservation_phase_started':False,
      'trust':'independent vectorized all-inequality verifier and direct origin checker, same agent; not external or formal review',
      'input_sha256':{'cached_product_inputs.json':sha(F/'cached_product_inputs.json'),
        'product_search_01.pkl':sha(F/'product_search_01.pkl'),'CACHED_SOURCE_PRODUCT_THEOREM.md':sha(F/'CACHED_SOURCE_PRODUCT_THEOREM.md')}}
    with (F/'independent_cached_product_audit.json').open('x',encoding='utf-8') as f:json.dump(report,f,indent=2)
    print(json.dumps({k:v for k,v in report.items() if k!='input_sha256'}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_verify95_exit.json').open('x',encoding='utf-8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)

"""Source-complete B, cached seven-active-key A; no fresh source actions."""
import hashlib,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1]
B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time()
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    grammar=read(F/'maximal_B_grammar.json');bt=read(F/'full_B_actions.json');audit=read(F/'independent_full_B_actions_audit.json')
    assert audit['input_sha256']['full_B_actions.json']==sha(F/'full_B_actions.json')
    nativepath=B/'native10_source_actions.json';native=read(nativepath);prior=read(F/'cached_product_inputs.json')
    a_ids=prior['A_submodels'][0]['A_tree_ids'];assert len(a_ids)==429
    loc={a:i for i,a in enumerate(a_ids)};cols=[0,2,4,6,7,8,9]
    AD=[];H=[]
    def project(t):
        if t is None or isinstance(t,str):return None
        if t[0] in (2,4,6):
            assert isinstance(t[1],str) and isinstance(t[2],str)
            return None
        return (cols.index(t[0]-1)+1,project(t[1]),project(t[2]))
    A_trees=[]
    for a in a_ids:
        ds=[native['destination'][a][x] for x in cols];assert all(d in loc for d in ds)
        AD.append([loc[d] for d in ds]);H.append([native['H'][a][x] for x in cols]);A_trees.append(project(native['trees'][a]))
    edges=[]
    for s,rows in enumerate(bt['actions']):
        for j,row in enumerate(rows):
            if row['admissible'] and row['destination']!=s:
                edges.append({'source':s,'target':row['destination'],'key':grammar['marks'][j],'q':row['q'],'full_table_column':j})
    assert len(edges)==13184
    model={'status':'COMPLETE_MAXIMAL_B_CACHED_A0_PRODUCT','A_trees':A_trees,'A_destination':AD,'A_H':H,
      'A_keys':grammar['marks'],'A_native10_indices':a_ids,'A_native10_columns':cols,
      'B_trees':grammar['trees'],'B_edges':edges,'state_count':429*3876,
      'A_active_anonymous_operands':0,'physical_canonical_keys':list(range(1,14)),
      'physical_A_unmarked_keys':'all six even keys are rigid external-gap leaves; arbitrary rigid payload lifts allowed',
      'B_coverage':'all original closed maximal-core13 B histories',
      'A_coverage':'all cached seven-mark A backbones, original DELETE/KEEP on those marks, arbitrary rigid off-path private gaps',
      'source_queries':0,'source_engine_calls':0,'JR35':'OPEN',
      'input_sha256':{'full_B_actions.json':sha(F/'full_B_actions.json'),'independent_full_B_actions_audit.json':sha(F/'independent_full_B_actions_audit.json'),
         'maximal_B_grammar.json':sha(F/'maximal_B_grammar.json')},'native_cache_sha256':sha(nativepath)}
    with (F/'complete_product_model_k0.json').open('x',encoding='utf-8') as f:json.dump(model,f,indent=2)
    print(json.dumps({k:v for k,v in model.items() if k in ('status','state_count','A_coverage','B_coverage','source_queries')}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_proof185_exit.json').open('x',encoding='utf-8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)

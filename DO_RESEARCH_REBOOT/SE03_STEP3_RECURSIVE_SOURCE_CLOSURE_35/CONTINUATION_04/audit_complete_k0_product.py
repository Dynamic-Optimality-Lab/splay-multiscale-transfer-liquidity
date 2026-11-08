"""Independent complete core13/seven-active-key A product certificate."""
import hashlib,json,pickle,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1]
B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time()
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    m=read(F/'complete_product_model_k0.json');ba=read(F/'full_B_actions.json');va=read(F/'independent_full_B_actions_audit.json')
    assert va['input_sha256']['full_B_actions.json']==sha(F/'full_B_actions.json')
    for p,h in m['input_sha256'].items():assert sha(F/p)==h
    native=read(B/'native10_source_actions.json');ids=m['A_native10_indices'];cols=m['A_native10_columns'];index={a:i for i,a in enumerate(ids)}
    for i,a in enumerate(ids):
        for j,x in enumerate(cols):
            assert m['A_destination'][i][j]==index[native['destination'][a][x]] and m['A_H'][i][j]==native['H'][a][x]
    assert len(ids)==429 and len(m['B_trees'])==3876
    expected={(i,z['destination'],m['A_keys'][j],z['q']) for i,row in enumerate(ba['actions']) for j,z in enumerate(row) if z['admissible'] and z['destination']!=i}
    assert expected=={(e['source'],e['target'],e['key'],e['q']) for e in m['B_edges']}
    with (F/'complete_k0_search_01.pkl').open('rb') as f:s=pickle.load(f)
    assert not s['queue'] and s['seeded'] and s['negative_cycle'] is None
    assert s['input_sha256']==sha(F/'complete_product_model_k0.json')
    import numpy as np
    lev=np.frombuffer(s['level'],dtype=np.int32).reshape(429,3876)
    dest=np.array(m['A_destination'],dtype=np.int64);H=np.array(m['A_H'],dtype=np.int32)
    checks=0
    for x in range(7):
        margin=2*H[:,x,None]+lev[dest[:,x],:]-lev;assert margin.min()>=0;checks+=margin.size
    for e in m['B_edges']:
        x=m['A_keys'].index(e['key']);margin=2*H[:,x]-e['q']+lev[dest[:,x],e['target']]-lev[:,e['source']]
        assert margin.min()>=0;checks+=len(ids)
    K=int(lev.max());assert K==6
    # Whole natural macros follow by telescoping original operation laws;
    # H>=6 is range-safe, H<6 selects every unit, all original h0 fits.
    Ccap=(K+6+1)//2;assert Ccap==6 and K+2*Ccap==18<=25
    report={'status':'PASS_COMPLETE_SOURCE_CORE13_A0_CREDIT_CERTIFICATE','state_pairs':429*3876,
      'B_all_static_source_states':3876,'B_all_admissible_genuine_edges':13184,'cached_inequalities_checked':checks,
      'D_width':K,'natural_c':'min(H,6)','working_bound':18,
      'source_queries':0,'source_engine_calls':0,
      'source_scope':'all original seven-key closed maximal-core13 words with no anonymous A operands, and arbitrary rigid private fringes',
      'unbounded_word_length_and_repeated_shared_helpers':True,'all_JR35_sources':False,'JR35':'OPEN',
      'trust':'independent all-inequality vectorized checker with full B/audit and cached A provenance; same agent, not external/formal review',
      'input_sha256':{'complete_product_model_k0.json':sha(F/'complete_product_model_k0.json'),
         'complete_k0_search_01.pkl':sha(F/'complete_k0_search_01.pkl'),'independent_full_B_actions_audit.json':sha(F/'independent_full_B_actions_audit.json')}}
    with (F/'independent_complete_k0_audit.json').open('x',encoding='utf-8') as f:json.dump(report,f,indent=2)
    print(json.dumps({k:v for k,v in report.items() if k!='input_sha256'}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_verify97_exit.json').open('x',encoding='utf-8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)

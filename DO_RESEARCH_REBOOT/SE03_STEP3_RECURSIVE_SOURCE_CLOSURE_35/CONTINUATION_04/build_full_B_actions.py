"""Source-complete core13 B actions under explicitly amended query cap."""
import hashlib,importlib.util,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1]
B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);START=time.process_time()
sp=importlib.util.spec_from_file_location('accepted_functional_B_core13',B/'audit_core39.py')
S=importlib.util.module_from_spec(sp);sp.loader.exec_module(S);S.CAP=CAP;S.START=START;S.QCAP=QCAP;S.CALLS=0
def fr(t):return None if t is None else (t[0],fr(t[1]),fr(t[2]))
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    grammar=read(F/'maximal_B_grammar.json');trees=list(map(fr,grammar['trees']));index={t:i for i,t in enumerate(trees)}
    old=read(F/'cached_product_inputs.json');known={}
    for e in old['B_edges']:
        before=fr(old['B_trees'][e['source']]);after=fr(old['B_trees'][e['target']])
        assert before in index and after in index
        known[index[before],e['key']]=(index[after],e['q'])
    rows=[];reused=0;marks=grammar['marks'];eligible=0
    for i,t in enumerate(trees):
        row=[]
        for x in marks:
            if x==t[0]:r={'destination':i,'H':0,'q':0,'origin':'ROOT_IDENTITY','admissible':True}
            elif (i,x) in known:
                j,q=known[i,x];r={'destination':j,'H':q,'q':q,'origin':'ACCEPTED_CACHE','admissible':True};reused+=1;eligible+=1
            else:
                assert S.CALLS<QCAP
                after,H,q,ev=S.splay(t,x,False)
                ok=H==q and all(e['pattern'] in ('LL','RR') and e['grandparent']%2 and e['parent'] is not None and not e['parent']%2 for e in ev)
                if ok:assert after in index;eligible+=1
                else:assert after not in index
                r={'destination':index[after] if ok else -1,'H':H,'q':q,'origin':'NEW_ORIGINAL_SPLAY',
                  'admissible':bool(ok),'patterns':[e['pattern'] for e in ev]}
            row.append(r)
        rows.append(row)
    assert S.CALLS==3876*6-reused and len(rows)==3876
    z={'status':'COMPLETE_SOURCE_B_TABLE_PENDING_INDEPENDENT_REPLAY','r':7,'state_count':3876,'marks':marks,
      'actions':rows,'admissible_genuine_edges':eligible,'accepted_genuine_edges_reused':reused,
      'fresh_genuine_actions':S.CALLS,'source_queries':S.CALLS,'source_engine_calls':S.CALLS,
      'all_static_trees_dynamically_recurrent_claimed':False,
      'closed_source_coverage':'all original maximal core13 histories by BG35 and all-SS theorem',
      'input_sha256':{'maximal_B_grammar.json':sha(F/'maximal_B_grammar.json'),
        'cached_product_inputs.json':sha(F/'cached_product_inputs.json')},
      'engine_sha256':sha(B/'audit_core39.py'),'query_authorization_sha256':sha(F/'query_authorization.json'),'JR35':'OPEN'}
    with (F/'full_B_actions.json').open('x',encoding='utf-8') as f:json.dump(z,f,indent=2)
    print(json.dumps({k:v for k,v in z.items() if k not in ('actions','input_sha256')}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_core45_exit.json').open('x',encoding='utf-8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':S.CALLS,'source_engine_calls':S.CALLS},f)

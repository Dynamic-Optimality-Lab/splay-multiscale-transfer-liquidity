"""Independent sparse conversion, part2: retain every old source edge."""
import hashlib,json,pickle,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;START=time.process_time();CAP=float(sys.argv[1])
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    pin=json.loads((B/'sparse_conversion_values_independent_audit.json').read_text());assert pin['status']=='PASS_EXACT_SPARSE_CONVERSION_VALUES_GEOMETRY_CAUSAL_CURSOR'
    for n in ('full_geometry_compressed_work_08.pkl','full_geometry_sparse_work_00.pkl'):assert hashlib.sha256((B/n).read_bytes()).hexdigest()==pin['input_sha256'][n]
    with (B/'full_geometry_compressed_work_08.pkl').open('rb') as f:w=pickle.load(f)
    bypi={pi:a for a,pi in w['projections'].items() if len(pi)>1};N=16796;codes=[bypi[pi]*N+b for b,pi in w['features']]
    actionsets={a:set(w['actions2'].get(a,[]))|{(x,at,1,None) for x,at in w['actions'].get(a,[])} for a in set(w['actions'])|set(w['actions2'])}
    count=0
    for (u,v),e in w['edges'].items():
        a,b=divmod(codes[u],N);at,bt=divmod(codes[v],N)
        assert e['source_A']==w['A'][a] and e['actual_A_target']==w['A'][at]
        assert (e['target_actual_key'],at,e['H'],e.get('DELETE_helper')) in actionsets[a]
        assert (b,bt)==(e['source_B_core_index'],e['B_target_core_index']) and e['price']==2*e['H']-e['Q']
        count+=1
        if count%32768==0 and time.process_time()-START>CAP-2:raise TimeoutError('RETENTION_AUDIT_CAP')
    assert count==2135234 and time.process_time()-START<CAP-1
    files=('sparse_conversion_values_independent_audit.json','audit_verify69.py','SPARSE_SOURCE_REGENERATION.md')
    out('sparse_source_conversion_independent_audit.json',{'status':'PASS_EXACT_SPARSE_SOURCE_PREFIX_CONVERSION','values_geometry_causal_cursor_receipt':'sparse_conversion_values_independent_audit.json','all_old_source_edges_retained_by_grammar':count,'original_H1_legacy_helper_field':'missing means no DELETE helper; checked as such, not discarded','positive_labels':21887,'implicit_zero_profiles':546701-21887,'future_propagation_requirement':'regenerate ALL H1 actions and H2/helper actions on every rise; fixed-source seeds must eventually be completely generated','source_queries':0,'source_engine_calls':0,'complete_funding_certificate':False,'principal_U33':'OPEN','input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in files}})
    print(json.dumps({'status':'PASS_EXACT_SPARSE_CONVERSION','edges_retained':count,'source_queries':0}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_verify69_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})

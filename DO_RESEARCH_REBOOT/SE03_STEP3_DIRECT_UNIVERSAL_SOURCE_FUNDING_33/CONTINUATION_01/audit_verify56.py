"""Independent exact substitution audit, no source solver or construction."""
import json,pickle,time,sys,hashlib,collections
from pathlib import Path
B=Path(__file__).resolve().parent;START=time.process_time();CAP=float(sys.argv[1])
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    with (B/'full_geometry_work_02.pkl').open('rb') as f:old=pickle.load(f)
    with (B/'full_geometry_compressed_work_00.pkl').open('rb') as f:new=pickle.load(f)
    oldids={key:j for j,key in enumerate(old['features'])};M={j:new['feature_index'][key] for key,j in oldids.items() if len(key[1])>1};assert len(M)==125376 and len(oldids)==284213;upper=[None]*len(M);witness=[None]*len(M);counts=collections.Counter();expected_edges=0
    for j,k in M.items():assert new['features'][k]==old['features'][j] and new['lower'][k]==old['lower'][j] and new['pred'][k]==old['pred'][j]
    for e in old['edges'].values():
        s,t=e['source_feature'],e['target_feature'];ss,tt=M.get(s),M.get(t);price=e['price']
        if ss is None and tt is None:assert price+old['lower'][t]-old['lower'][s]>=0;counts['frozen_to_frozen']+=1
        elif ss is None:assert new['lower'][tt]>=old['lower'][s]-price;counts['frozen_to_mutable']+=1
        elif tt is None:
            bound=price+old['lower'][t];assert new['lower'][ss]<=bound;counts['mutable_to_frozen']+=1
            if upper[ss] is None or bound<upper[ss]:upper[ss]=bound;witness[ss]=e
        else:
            expected_edges+=1;counts['mutable_to_mutable']+=1;r=new['edges'][ss,tt];assert (r['source_feature'],r['target_feature'],r['price'])==(ss,tt,price);assert all(r[k]==v for k,v in e.items() if k not in ('source_feature','target_feature'))
    assert new['upper']==upper and len(new['edges'])==expected_edges==415910
    for k,e in enumerate(new['upper_edge']):
        if e is None:assert witness[k] is None;continue
        assert e['target_feature'] is None and e['source_feature']==k and e['price']+e['target_frozen_value']==upper[k];assert all(e[x]==v for x,v in witness[k].items() if x not in ('source_feature','target_feature'))
    assert len(old['updates'])==len(new['updates'])==5381
    for i,(r,u) in enumerate(zip(old['updates'],new['updates'])):
        assert r['parent']==u['parent'] and (r['parent'] is None or r['parent']<i);assert u['source_feature']==M.get(r['source_feature']) and u['target_feature']==M[r['target_feature']];assert u['source_lower']==r['source_lower'] and u['new_lower']==r['new_lower']
    assert dict(counts)==new['compression_counts'];assert time.process_time()-START<CAP-1
    deps=('FROZEN_SINGLETON_ELIMINATION.md','full_geometry_exact_compression.json','unary_boundary_independent_audit.json')
    out('frozen_singleton_elimination_independent_audit.json',{'status':'PASS_EXACT_FROZEN_SINGLETON_CONSTRAINT_ELIMINATION','old_feature_records':284213,'new_mutable_records':125376,'old_edges':1488720,'mutable_edges':415910,'preserved_parent_updates':5381,'constraint_type_counts':dict(counts),'scope':'algebraic equivalence of this saved source model and exact frozen-state substitutions; not completion of its source enumeration','source_queries':0,'source_engine_calls':0,'principal_U33':'OPEN','input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in deps}});print(json.dumps({'status':'PASS_EXACT_SINGLETON_COMPRESSION','old_states':284213,'new_states':125376,'source_queries':0}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_verify56_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})

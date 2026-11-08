"""Exact source-constraint compression; frozen singleton endpoints need no variable."""
import json,pickle,time,sys,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent;START=time.process_time();CAP=float(sys.argv[1])
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    source=B/'full_geometry_work_02.pkl'
    with source.open('rb') as f:w=pickle.load(f)
    oldfeatures=w['features'];oldlower=w['lower'];mapping={j:i for i,j in enumerate(j for j,key in enumerate(oldfeatures) if len(key[1])>1)};features=[oldfeatures[j] for j in mapping];lower=[oldlower[j] for j in mapping];upper=[None]*len(features);upper_edge=[None]*len(features)
    def convert(e):
        r=e.copy();s,t=e['source_feature'],e['target_feature'];r['source_feature']=mapping.get(s);r['target_feature']=mapping.get(t)
        if s not in mapping:r['source_frozen_value']=oldlower[s]
        if t not in mapping:r['target_frozen_value']=oldlower[t]
        return r
    edges={};outgoing={};counts={'frozen_to_frozen':0,'frozen_to_mutable':0,'mutable_to_frozen':0,'mutable_to_mutable':0}
    for e in w['edges'].values():
        s,t=e['source_feature'],e['target_feature'];ss,tt=mapping.get(s),mapping.get(t)
        if ss is None and tt is None:counts['frozen_to_frozen']+=1;continue
        if ss is None:assert lower[tt]>=oldlower[s]-e['price'];counts['frozen_to_mutable']+=1;continue
        if tt is None:
            bound=e['price']+oldlower[t];assert lower[ss]<=bound;counts['mutable_to_frozen']+=1
            if upper[ss] is None or bound<upper[ss]:upper[ss]=bound;upper_edge[ss]=convert(e)
        else:
            r=convert(e);edges[ss,tt]=r;outgoing.setdefault(ss,{})[tt]=r;counts['mutable_to_mutable']+=1
    updates=[]
    for rec in w['updates']:
        assert rec['target_feature'] in mapping;r=rec.copy();r['edge']=convert(rec['edge']);r['source_feature']=mapping.get(rec['source_feature']);r['target_feature']=mapping[rec['target_feature']];updates.append(r)
    ans={k:w[k] for k in ('A','A_index','private','actions','actions2','projections','cursor','source_couplings','initial_H1_complete_A_count')};ans.update(features=features,feature_index={key:i for i,key in enumerate(features)},lower=lower,upper=upper,upper_edge=upper_edge,pred=[w['pred'][j] for j in mapping],depth=[w['depth'][j] for j in mapping],edges=edges,outgoing=outgoing,updates=updates,pending=[mapping[j] for j in w['pending'] if j in mapping],counter=None,causal_edges=[],width3_first_candidate=None,compression_counts=counts)
    assert not w['pending'];assert time.process_time()-START<CAP-5
    with (B/'full_geometry_compressed_work_00.pkl').open('xb') as f:pickle.dump(ans,f,protocol=5)
    out('full_geometry_exact_compression.json',{'status':'EXACT_FROZEN_SINGLETON_ELIMINATION_PRODUCER','old_feature_records':len(oldfeatures),'new_mutable_feature_records':len(features),'old_stored_edges':len(w['edges']),'new_stored_mutable_edges':len(edges),'constraints_by_type':counts,'unary_endpoint_local_lemma_reused':'unary_boundary_independent_audit.json; local sign depends only on the two packet endpoints, not other boundaries','rule':'frozen->mutable seeds already satisfied; mutable->frozen becomes literal source upper bound; mutable->mutable remains edge; fixed source values never change','all_current_causal_parent_updates_retained':len(updates),'discovery_only_not_a_full_certificate':True,'source_queries':0,'source_engine_calls':0,'principal_U33':'OPEN'});print(json.dumps({'status':'EXACT_SINGLETON_ELIMINATION','old_features':len(oldfeatures),'new_features':len(features),'old_edges':len(w['edges']),'new_edges':len(edges),'counts':counts}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof120_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})

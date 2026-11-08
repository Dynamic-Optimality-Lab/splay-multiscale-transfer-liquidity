"""Remove optional HIGH envelopes and widths from the B-sensitive obstruction.
Uses ONLY source inequalities, nonnegative debt, and frozen singleton values.
"""
import json,pickle,time,sys,collections
from pathlib import Path
B=Path(__file__).resolve().parent;START=time.process_time();CAP=float(sys.argv[1])
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    with (B/'B_sensitive_contraction_work_02.pkl').open('rb') as f:w=pickle.load(f)
    edges=w['edges'];features=set(w['labels']);labels={k:(k%16).bit_length()-1 if k%16&((k%16)-1)==0 else 0 for k in features};upper={k:((k%16).bit_length()-1 if k%16&((k%16)-1)==0 else None) for k in features};pred={k:None for k in features};der=[];outgoing=w['outgoing'];q=collections.deque(features);pending=set(features);bad=None
    while q and bad is None:
        u=q.popleft();pending.remove(u)
        for v,e in outgoing.get(u,{}).items():
            need=labels[u]-e['price']
            if need<=labels[v]:continue
            rec={'edge':e,'source_feature':u,'target_feature':v,'source_label':labels[u],'new_label':need,'parent_derivation':pred[u]};der.append(rec);pred[v]=len(der)-1;labels[v]=need
            if upper[v] is not None and need>upper[v]:bad={'type':'FROZEN_SINGLETON_UPPER','end_feature':v,'required':need,'upper':upper[v],'last_derivation':len(der)-1};break
            # Every actual update stores an immutable derivation path; a repeated
            # feature is checked by its literal total price, never an abstract claim.
            if len(der)>4000000:raise RuntimeError('DAG_CAP')
            if v not in pending:q.append(v);pending.add(v)
        if time.process_time()-START>CAP-2:break
    chain=[];start_key=None;start_value=None;total=None
    if bad:
        j=bad['last_derivation']
        while j is not None:chain.append(der[j]['edge']);start_key=der[j]['source_feature'];start_value=der[j]['source_label'];j=der[j]['parent_derivation']
        chain.reverse();assert all(a['target_feature']==b['source_feature'] for a,b in zip(chain,chain[1:]));total=sum(e['price'] for e in chain);assert total+bad['upper']-start_value<0
    result={'status':'B_SENSITIVE_DEBT_SET_SOURCE_ONLY_FORMULA_REFUTATION_CANDIDATE' if bad else 'B_SENSITIVE_SOURCE_ONLY_CHECK_OPEN' if q else 'B_SENSITIVE_SOURCE_ONLY_PREFIX_FEASIBLE','source_inequalities':len(edges),'variables':len(features),'contradiction':bad,'causal_edges':chain,'start_feature':start_key,'start_lower_value':start_value,'end_frozen_value':bad['upper'] if bad else None,'total_price':total,'signed_margin_sum':total+bad['upper']-start_value if bad else None,'optional_B_envelope_bounds_used':False,'width_bound_used':False,'nonnegativity_used':True,'singleton_agreement_used':True,'queue_pending':len(q),'source_queries':0,'source_engine_calls':0,'principal_U33':'OPEN'};out('B_sensitive_source_only_obstruction.json',result);print(json.dumps({k:v for k,v in result.items() if k!='causal_edges'}));print(json.dumps([{'BF':[e['source_B_core_index'],e['B_target_core_index']],'sets':[e['source_value_set'],e['target_value_set']],'price':e['price']} for e in chain]))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof95_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})

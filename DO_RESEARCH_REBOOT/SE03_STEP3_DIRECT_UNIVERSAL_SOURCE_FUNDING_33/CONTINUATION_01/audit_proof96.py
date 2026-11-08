"""Compute exact contraction multiplicities for the source-only B-aware chain."""
import json,time,pickle,hashlib
from pathlib import Path
from interior_projection_source_tools import *
B=Path(__file__).resolve().parent
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    z=json.loads((B/'B_sensitive_source_only_obstruction.json').read_text());assert z['contradiction'];Z=json.loads((B/'native10_source_actions.json').read_text());S=Lift(Z);N=len(S.T);mir=Z['mirror'];raw=(B/'native10_debt_03.pkl').read_bytes();r=json.loads((B/'native10_complete_independent_audit.json').read_text());assert hashlib.sha256(raw).hexdigest()==r['input_sha256'];L=pickle.loads(raw)['level'];debt=lambda a,b:L.get(min(a*N+b,mir[a]*N+mir[b]),0);rows=[]
    for e in z['causal_edges']:
        e=e.copy();p=e['private_key'];ps=[S.idx[a] for a in projections(fr(e['source_A']),p)];pt=[S.idx[a] for a in projections(fr(e['actual_A_target']),p)];e['source_projection_indices']=ps;e['target_projection_indices']=pt;e['source_value_multiset']=sorted(debt(a,e['source_B_core_index']) for a in ps);e['target_value_multiset']=sorted(debt(a,e['B_target_core_index']) for a in pt);rows.append(e)
    matching=all(a['target_value_multiset']==b['source_value_multiset'] and a['B_target_core_index']==b['source_B_core_index'] for a,b in zip(rows,rows[1:]));result={'status':'FULL_B_AND_MULTISET_CAUSAL_CHAIN_FOUND' if matching else 'FULL_B_AND_VALUE_SET_ONLY_CHAIN_MULTIPLICITIES_DIFFER','edges':rows,'all_intermediate_multisets_match':matching,'start':rows[0]['source_value_multiset'],'end':rows[-1]['target_value_multiset'],'total_price':sum(e['price'] for e in rows),'optional_HIGH_bounds_used':False,'width_bound_used':False,'source_queries':0,'source_engine_calls':0,'principal_U33':'OPEN'};out('B_sensitive_full_multiset_chain_candidate.json',result);print(json.dumps({k:v for k,v in result.items() if k!='edges'}));print(json.dumps([{'BF':[e['source_B_core_index'],e['B_target_core_index']],'multisets':[e['source_value_multiset'],e['target_value_multiset']],'price':e['price']} for e in rows]))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof96_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})

"""Extract the causal scalar chain, not an actual source walk, from root-aware run."""
import json,time
from pathlib import Path
B=Path(__file__).resolve().parent
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    z=json.loads((B/'root_aware_contraction_debt_set_candidate.json').read_text());assert z['contradiction'];tr=z['contradiction']['trace'];edges={(e['source_mask'],e['target_mask']):e for e in z['edges']};chain=[];j=len(tr)-1
    while True:
        step=tr[j];key=tuple(step['edge_key']);e=edges[key];assert step['source_label']-e['price']==step['new_target_label'];chain.append(e);source=key[0];value=step['source_label'];earlier=[i for i in range(j) if tr[i]['edge_key'][1]==source and tr[i]['new_target_label']==value]
        if not earlier:
            assert z['bounds']['lower'][str(source)]==value;start_key=source;start_label=value;break
        j=earlier[-1]
    chain=chain[::-1];assert all(a['target_mask']==b['source_mask'] for a,b in zip(chain,chain[1:]));end_key=chain[-1]['target_mask'];end_upper=z['bounds']['upper'][str(end_key)];total=sum(e['price'] for e in chain);assert total+end_upper-start_label<0;assert start_key%16 in (1,2,4,8) and end_key%16 in (1,2,4,8)
    result={'status':'ROOT_AWARE_CAUSAL_SCALAR_CHAIN_EXTRACTED','edges':chain,'start_feature_code':start_key,'start_frozen_value':start_label,'end_feature_code':end_key,'end_frozen_value':end_upper,'total_source_packet_price':total,'sum_of_signed_margins':total+end_upper-start_label,'intermediate_width_bound_used':False,'all_physical_private_keys':[e['private_key'] for e in chain],'source_path_warning':'These representative edges need not concatenate as full source states. The contradiction concerns a common root-aware profile function; each edge must separately receive original-source closed embedding.','source_queries':0,'source_engine_calls':0,'principal_U33':'OPEN'};out('root_aware_contraction_debt_set_chain.json',result);print(json.dumps({k:v for k,v in result.items() if k!='edges'}));print(json.dumps([{'feature': [e['source_mask'],e['target_mask']],'price':e['price'],'source_root':e['source_root_rank'],'target_root':e['target_root_rank'],'private':e['private_key']} for e in chain]))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof89_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})

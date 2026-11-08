"""Exact boundary compatibility of accepted returning templates. No replay
or source query. Unequal whole states cannot be merged by equal core size.
"""
import json,time
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    n=json.loads((B/'nonextremal_source_countercertificate.json').read_text());u=json.loads((B/'forward_recovery_and_period_receipt.json').read_text())
    old=json.loads((P/'SE03_STEP3_MARKED_COMB_SIGNED_REPAYMENT_29/comb_source_fixtures.json').read_text());s=old['reports'][0]['initial'];ans=[]
    for name,z in [('N',n['initial']),('U',u['aligned_initial'])]:
        ans.append({'new_boundary':name,'whole_triple_equal_to_C29':z==s,'equal_components':[z[i]==s[i] for i in range(3)],'new_state':z,'C29_state':s})
    out('mixed_boundary_comparison.json',{'status':'EXACT_SAVED_STATE_BOUNDARY_COMPARISON','comparisons':ans,
        'no_source_bridge_inferred_from_equal_core_size':True,'new_source_queries':0})
    print(json.dumps({'status':'BOUNDARY_COMPARISON','comparisons':[{k:z[k] for k in ('new_boundary','whole_triple_equal_to_C29','equal_components')} for z in ans]}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_geometry2_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':0,'source_queries':0})

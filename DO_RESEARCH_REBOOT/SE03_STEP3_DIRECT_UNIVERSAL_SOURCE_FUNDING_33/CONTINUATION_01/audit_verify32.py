"""Exact root-aware information barrier, no repeated primitive engine audit."""
import json,time,hashlib
from pathlib import Path
from source_composition_auditor import check
B=Path(__file__).resolve().parent
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    z=json.loads((B/'root_clipped2_source_countercertificate.json').read_text());assert all(hashlib.sha256((B/n).read_bytes()).hexdigest()==v for n,v in z['input_sha256'].items());audit=json.loads((B/'native10_source_independent_audit.json').read_text());assert hashlib.sha256((B/'native10_source_actions.json').read_bytes()).hexdigest()==audit['input_sha256'] and audit['status']=='PASS_COMPLETE_NATIVE10_SOURCE_ACTIONS';native=json.loads((B/'native10_source_actions.json').read_text());records=[];sumw=0
    for edge in z['cycle_edges']:
        r=check(native,edge['closed_history']);ps=[max(v,-2) for v in r['delta_before']];pt=[max(v,-2) for v in r['delta_after']];assert ps==edge['capped_profile_before'] and pt==edge['capped_profile_after'] and (r['root_before'],r['root_after'])==(edge['root_before'],edge['root_after']);assert (r['H'],r['Q'])==(edge['source']['H'],edge['source']['Q']);sumw+=r['price'];records.append(r)
    for i,r in enumerate(records):
        nxt=records[(i+1)%len(records)];assert r['root_after']==nxt['root_before'] and [max(v,-2) for v in r['delta_after']]==[max(v,-2) for v in nxt['delta_before']]
    assert sumw==-2 and any(r['full_pair_after']!=records[(i+1)%len(records)]['full_pair_before'] for i,r in enumerate(records));out('root_clipped2_independent_source_audit.json',{'status':'PASS_ANY_ROOT_CAPPED_DEFICIT_K2_FUNCTION_REFUTATION','source_histories':len(records),'exact_profile_cycle_price':sumw,'current_root_retained':True,'any_function_of_root_and_clipped_profile_refuted':True,'all_cutoffs_0_1_2_refuted_by_information_inclusion':True,'any_c_not_exceeding_actual_H_cannot_repair_this_unchanged_packet_rule':True,'all_original_source_operations_and_A_H0_distinction_preserved':True,'all_original_trees_and_recent_key_charts_closed':True,'all_periods_CD_safe':True,'no_actual_negative_full_state_cycle_claimed':True,'new_source_engine_calls':0,'new_source_queries':0,'primitive_identity_instantiations_checked':sum(r['primitive_identity_instantiations_checked'] for r in records),'verification_method':'independent absolute-word/cost/seam checker composing immutable previously independently verified ordinary primitive identities; hypothetical marked depths independently recomputed','source_summary':records,'principal_U33':'OPEN','external_or_formal_verification':False,'input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in ('root_clipped2_source_countercertificate.json','native10_source_actions.json','native10_source_independent_audit.json','source_composition_auditor.py')}});print(json.dumps({'status':'PASS_SOURCE_EXACT_ROOT_CUTOFF_LE2_BARRIER','source_histories':len(records),'cycle_price':sumw,'all_actual_periods_CD_safe':True,'new_source_queries':0}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_verify32_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})

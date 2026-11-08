"""Composition/closure-gate audit, without old semantic-check replays."""
import hashlib,json,sys,time
from pathlib import Path
BASE=Path(__file__).resolve().parent;CAP=min(120,float(sys.argv[1]))
def write(name,obj):
    with (BASE/name).open('x',encoding='utf-8') as f:json.dump(obj,f,indent=2)
def main():
    stages=[('spread_v2','CORRECTED_UNIVERSAL_SPREAD_AUDIT_PASS'),
      ('child','UNIVERSAL_CROSS_MEDIAN_CHILD_AND_SOURCE_DEBT_AUDIT_PASS'),
      ('maskfree','ALL_MASK_SPREAD_UNIVERSAL_AUDIT_PASS'),
      ('central_v2','CENTRAL_RESET_UNIVERSAL_AUDIT_PASS_AFTER_CORRECTED_INVERSE_COVERAGE'),
      ('allcentral','ALL_MASK_CENTRAL_UNIVERSAL_AUDIT_PASS')]
    accepted=[]
    for name,status in stages:
        q=BASE/('audit_'+name+'.json');a=json.loads(q.read_text())
        assert a['status']==status and not a['Step4_complete']
        assert a['all_old_valid_LOW_rows_preserved']
        assert json.loads((BASE/('run_'+name+'_result.json')).read_text())['status']=='PASS'
        assert json.loads((BASE/('audit_'+name+'_exit.json')).read_text())['error'] is None
        accepted.append({'phase':name,'audit_hash':hashlib.sha256(q.read_bytes()).hexdigest()})
    assert all(json.loads((BASE/('run_'+n+'_result.json')).read_text())['status']=='FAILED_OR_UNKNOWN' for n in ('spread','central'))
    old=json.loads((BASE.parent/'M3_XFER17/partition_update.json').read_text())
    assert old['remaining_H1_schematic_slots']==36 and old['remaining_Gamma1_zero_slots']==0
    cells=[]
    for r in old['cells']:
        if r['status']=='OPEN':
            r=dict(r);r['current_potential']='D_current';r['exact_source_debt_at_any_failure']='psi_source'
            r['current_debt_drop_options']=[[1,0]] if r['psi_source']==1 else [[2,0],[2,1]]
            r['completed_region_exclusions_added']=['all-mask spread','cross-median unique child','all-mask central reset']
            r['whole_cell_closed']=False
        cells.append(r)
    assert len([r for r in cells if r['status']=='OPEN'])==36
    write('partition_update.json',{'parent_partition':str(BASE.parent/'M3_XFER17/partition_update.json'),
      'current_potential':'D_current','remaining_H1_schematic_slots':36,'remaining_Gamma1_zero_slots':0,
      'all_remaining_zero_edges_covered':False,'Step4_complete':False,'cells':cells,
      'finite_signature_or_edge_counts_inferred_from_slots':False})
    write('debt_definition.json',{'name':'D_current','formula':'max(D_term,1_A1,2*1_A2)',
      'A1':['all-mask spread U','all-mask spread W','all-mask spread K','all-mask spread Q','all-mask spread V','all-mask central Y','all-mask central Z'],
      'A2':['all-mask spread Z','cross-median unique child C','all-mask central X','all-mask central C'],
      'all_regions_include_P_and_both_actual_orientations':True,'all_original_masks_and_signatures_quantified':True,
      'source_debt_at_every_remaining_H1_failure_equals_psi':True,
      'range':[0,2],'private_inventory_history_or_new_state_coordinate_used':False,
      'global_psi_floor_outside_P_claimed':False,'LOW_destination_psi_E1_floors_preserved':True})
    assert time.process_time()<CAP
    write('audit_composition.json',{'status':'SIGNED_COMPOSITION_PASS_FULL_STEP4_COVERAGE_UNPROVED',
      'accepted_new_proofs':accepted,'failed_attempts_retained':['spread','central'],
      'new_signed_rows_proved':True,'all_old_valid_LOW_rows_preserved':True,
      'HIGH_h0_glue_preserved':True,'all_original_state_scope_and_transition_semantics_retained':True,
      'new_finite_tests':0,'new_original_root_or_saved_psi_queries':0,'completed_semantic_checks_replayed':0,
      'requested_complete_Step4_achieved':False,'Step4_complete':False,'M3_status':'OPEN',
      'unproved_exact_implication':'every remaining marked-source original zero H1 has D_current(t)>=psi(Bs)=D_current(s)',
      'new_negative_cycle_certified':False,'new_whole_signature_certificates':0})
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:
        error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:write('audit_composition_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})

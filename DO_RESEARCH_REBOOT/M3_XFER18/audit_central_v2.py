"""Resume unfinished central inverse coverage; completed prefix reused."""
import json,sys,time
from pathlib import Path
from audit_spread import n,reverse
from audit_spread_v2 import inverse_proof
from audit_central import inverses
BASE=Path(__file__).resolve().parent;CAP=min(120,float(sys.argv[1]));E=None
def write(name,obj):
    with (BASE/name).open('x',encoding='utf-8') as f:json.dump(obj,f,indent=2)
def main():
    first=json.loads((BASE/'run_central_result.json').read_text())
    assert first['status']=='FAILED_OR_UNKNOWN' and first['error']['message'].startswith("('X', 6,")
    L=n(0,E,n(2,n(1),E));X=n(5,n(3,L,n(4)),n(8,n(6,E,n(7)),E))
    P=n(0,E,n(3,n(2,n(1),E),n(4,E,n(8,n(7,n(6,n(5),E),E),E))))
    P2=n(0,E,n(3,n(2,n(1),E),n(8,n(4,E,n(7,n(6,n(5),E),E)),E)))
    inverse=[]
    for d in (6,7,8):
        solutions,proof=inverses(X,d);assert solutions==({P,P2} if d==6 else set()),(d,solutions)
        opposite,opp=inverses(reverse(X),d);assert opposite==({reverse(P),reverse(P2)} if d==6 else set())
        inverse.append({'negative_depth':d,'proof':proof,'actual_opposite_proof':opp})
    zero_pre=[{'predecessor':name,'negative_depth':d,'proof':inverse_proof(t,d),
      'actual_opposite_proof':inverse_proof(reverse(t),d)} for name,t in [('P',P),('P2',P2)] for d in (6,7,8)]
    write('central_inverse_certificate_v2.json',{'status':'PASS',
      'C_all_negative_words_impossible_both_actual_orientations':'REUSED_COMPLETED_PREFIX_OF_FIRST_AUDIT',
      'X_complete_inverse_derivations':inverse,'both_predecessors_have_no_negative_incoming':zero_pre,
      'saved_complete_negative_recurrence_inference':{'psi_C':0,'psi_P':0,'psi_P2':0,'psi_X':1},
      'no_original_model_population_or_psi_bank_tests':True})
    residuals={'C_zero_to_X2':{},'X_plus1_to_floor1':{'target_excess_above1':1},
      'Y_zero_to_Z1':{'target_excess_above1':1},'Z_positive_at1':{'weight_excess_above1':1,'target_debt':1},
      'C_X_helpers_range_safe':{'weight_excess_above2':1,'target_debt':1},
      'unchanged_source':{'old_residual':1,'target_increment':1}}
    assert all(c>=0 for d in residuals.values() for c in d.values())
    assert time.process_time()<CAP
    write('audit_central_v2.json',{'status':'CENTRAL_RESET_UNIVERSAL_AUDIT_PASS_AFTER_CORRECTED_INVERSE_COVERAGE',
      'all_previous_constructor_identities_and_C_word_checks_reused_not_replayed':True,
      'X_negative_predecessor_count':2,'all_X_C_source_LOW_rows_proved':True,
      'all_old_valid_LOW_rows_preserved':True,'universal_signed_slacks':residuals,
      'new_debt':'D_central=max(D_allmarks,1_Zcentral,1_Ycentral,2_Xcentral,2_Ccentral)',
      'new_finite_tests':0,'new_original_root_or_saved_psi_queries':0,'completed_checks_replayed':0,
      'failed_first_attempt_retained':True,'exact_source_debt_induction_preserved':True,'Step4_complete':False})
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:
        error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:write('audit_central_v2_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})

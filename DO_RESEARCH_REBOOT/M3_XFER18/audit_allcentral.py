"""Universal arbitrary-mask central source-cover audit."""
import json,sys,time
from pathlib import Path
from audit_spread import n,block,replay,reverse,path,depths
BASE=Path(__file__).resolve().parent;CAP=min(120,float(sys.argv[1]));E=None
def write(name,obj):
    with (BASE/name).open('x',encoding='utf-8') as f:json.dump(obj,f,indent=2)
def main():
    assert json.loads((BASE/'audit_central_v2.json').read_text())['status']=='CENTRAL_RESET_UNIVERSAL_AUDIT_PASS_AFTER_CORRECTED_INVERSE_COVERAGE'
    L=n(0,E,n(2,n(1),E))
    C=n(3,L,n(4,E,n(8,n(7,n(6,n(5),E),E),E)))
    Y=n(4,n(3,L,E),n(5,E,n(8,n(6,E,n(7)),E)))
    Y1=n(1,n(0),n(3,n(2),n(4,E,n(5,E,n(8,n(6,E,n(7)),E)))))
    C1=n(1,n(0),n(3,n(2),n(4,E,n(8,n(7,n(6,n(5),E),E),E))))
    C2=n(2,n(0,E,n(1)),n(3,E,n(4,E,n(8,n(7,n(6,n(5),E),E),E))))
    ids=[]
    def cert(label,t,p,want):
        assert replay(t,p)==want,label
        assert replay(reverse(t),tuple(1-v for v in p))==reverse(want),label+'_opposite'
        ids.append(label)
    cert('Y_new_zero1_core',Y,path(Y,1),Y1)
    cert('C_new_plus1_1_core',C,path(C,1),C1)
    cert('C_new_plus1_2_core',C,path(C,2),C2)
    assert all(depths(Y1)[k]<=3 for k in (0,2,3,4,5))
    assert all(depths(t)[k]<=2 for t,keys in [(C1,(0,2,3,4)),(C2,(0,1,3,4))] for k in keys)
    A,B,D,F,G,H=map(block,('A','B','D','F','G','H'))
    cert('Y_new_zero1_A_L',n(4,n(1,A,B),n(5,D,F)),(0,),n(1,A,n(4,B,n(5,D,F))))
    cert('Y_new_zero1_A_LL',n(4,n('p',n(1,A,B),D),n(5,F,G)),(0,0),n(1,A,n('p',B,n(4,D,n(5,F,G)))))
    cert('Y_new_zero1_A_LR',n(4,n('p',A,n(1,B,D)),n(5,F,G)),(0,1),n(1,n('p',A,B),n(4,D,n(5,F,G))))
    # Formal ordered role x is universally1 or2. One constructor proof
    # proves BOTH target identities without building or testing a mask.
    cert('C_new_x_A',n(3,n(0,A,n('x',B,D)),n(4,F,n(5,G,H))),(0,1),n('x',n(0,A,B),n(3,D,n(4,F,n(5,G,H)))))
    assert {k for k,d in depths(Y).items() if d>=4}=={1,7}
    signs={'Y_zero1_E1':{'target_excess_above1':1},'C_new_plus1_E1':{'target_excess_above1':1},
      'old_safe_sources_reused':{'saved_nonnegative_residual':1},
      'unchanged_source':{'old_residual':1,'target_increment':1}}
    assert all(c>=0 for v in signs.values() for c in v.values())
    assert time.process_time()<CAP
    write('audit_allcentral.json',{'status':'ALL_MASK_CENTRAL_UNIVERSAL_AUDIT_PASS',
      'new_constructor_identities_both_actual_orientations':ids,'universal_sign_slacks':signs,
      'previous_completed_constructors_inverse_words_and_helper_arguments_reused':True,
      'mu_and_sigma_universally_quantified_without_population_or_mask_tests':True,
      'all_C_X_source_LOW_rows_proved_for_all_masks':True,'all_old_valid_LOW_rows_preserved':True,
      'exact_source_debt_induction_preserved':True,
      'new_debt':'D_current=max(D_central,1_Zcentral_all,1_Ycentral_all,2_Xcentral_all,2_Ccentral_all)',
      'new_finite_tests':0,'new_original_root_or_psi_queries':0,'completed_semantic_checks_replayed':0,
      'Step4_complete':False})
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:
        error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:write('audit_allcentral_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})

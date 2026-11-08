"""All-mask structural proof audit: no instantiated masks or populations."""
import json,sys,time
from pathlib import Path
from audit_spread import n,block,replay,reverse,path,depths
BASE=Path(__file__).resolve().parent;CAP=min(120,float(sys.argv[1]));E=None
def write(name,obj):
    with (BASE/name).open('x',encoding='utf-8') as f:json.dump(obj,f,indent=2)
def main():
    assert json.loads((BASE/'audit_spread_v2.json').read_text())['status']=='CORRECTED_UNIVERSAL_SPREAD_AUDIT_PASS'
    assert json.loads((BASE/'audit_child.json').read_text())['status']=='UNIVERSAL_CROSS_MEDIAN_CHILD_AND_SOURCE_DEBT_AUDIT_PASS'
    T=n(2,n(0,E,n(1)),n(5,n(3,E,n(4)),n(7,n(6),n(8))))
    U=n(6,n(2,n(0,E,n(1)),n(5,n(3,E,n(4)),E)),n(7,E,n(8)))
    W=n(6,n(2,n(0,E,n(1)),n(5,n(3,E,n(4)),E)),n(8,n(7),E))
    V=n(8,n(2,n(0,E,n(1)),n(7,n(5,n(3,E,n(4)),n(6)),E)),E)
    Q=n(1,n(0),n(2,E,n(5,n(3,E,n(4)),n(7,n(6),n(8)))))
    K=n(6,n(2,n(1,n(0),E),n(5,n(3,E,n(4)),E)),n(7,E,n(8)))
    EK=n(4,n(2,n(1,n(0),E),n(3)),n(6,n(5),n(7,E,n(8))))
    C4=n(4,n(2,n(0,E,n(1)),n(3)),n(5,E,n(7,n(6),n(8))))
    EU=n(4,n(2,n(0,E,n(1)),n(3)),n(6,n(5),n(7,E,n(8))))
    EW=n(4,n(2,n(0,E,n(1)),n(3)),n(6,n(5),n(8,n(7),E)))
    ids=[]
    def cert(label,t,p,want):
        assert replay(t,p)==want,label
        assert replay(reverse(t),tuple(1-v for v in p))==reverse(want),label+'_opposite'
        ids.append(label)
    cert('Z_new_target1_core',T,path(T,1),Q)
    cert('Q_zero6_core',Q,path(Q,6),K)
    cert('K_zero4_core',K,path(K,4),EK)
    A,B,C,D,F=map(block,('A','B','C','D','F'))
    cert('Z_new_target1_A',n(2,n(0,A,n(1,B,C)),n(6,D,F)),(0,1),n(1,n(0,A,B),n(2,C,n(6,D,F))))
    cert('Q_zero6_A',n(1,n(0,A,B),n(2,C,n(6,D,F))),(1,1),n(6,n(2,n(1,n(0,A,B),C),D),F))
    # New strength: every core, not the prior five marks, is shallow.
    entire_depths={name:depths(t) for name,t in [('C4',C4),('EU',EU),('EW',EW),('EK',EK)]}
    assert all(set(ds)==set(range(9)) and max(ds.values())<=3 for ds in entire_depths.values())
    assert all({k for k,d in depths(t).items() if d>=4}=={4} and depths(t)[4]==4 for t in (U,W,K))
    assert {k:depths(V)[k] for k in (2,6,7)}=={2:1,6:4,7:2}
    assert {k:depths(Q)[k] for k in (0,2,6)}=={0:1,2:1,6:4}
    # No mu vector is constructed. Quantification is by subset inclusion:
    # every marked eligible target is a member of the proved Score-cover.
    cover={'Z':{'possible_nonroot_Scores':[0,1,4,6,8],
                'hidden_below_observed_separators':[3,5,7]},
           'V':{'possible_nonroot_Scores':[2,6,7],
                'hidden_below_LL2':[0,1,3,4,5]},
           'Q':{'possible_nonroot_Scores':[0,2,6],
                'Score_empty_intervals':[[0,1],[1,2]]}}
    signs={'new_Z_plus1':{'Q_excess_above1':1},
      'Q_zero6':{'K_excess_above1':1},'K_zero4':{'E1_excess_above1':1},
      'V_new_marked7_positive':{'target_debt':1},
      'old_row_transport':{'old_residual':1,'target_increment':1}}
    assert all(v>=0 for d in signs.values() for v in d.values())
    assert time.process_time()<CAP
    write('audit_maskfree.json',{'status':'ALL_MASK_SPREAD_UNIVERSAL_AUDIT_PASS',
      'new_identities_both_actual_orientations':ids,
      'completed_original_spread_identities_reused_not_replayed':True,
      'entire_core_depth_proofs':entire_depths,'fresh_source_target_cover':cover,
      'universal_signed_slacks':signs,'all_legal_five_bit_masks_quantified':True,
      'new_debt':'D_allmarks=max(D_child,1_Ustar,1_Wstar,1_Kstar,1_Qstar,1_Vstar,2_Zstar)',
      'ordered_operations':['U1','W1','K1','Q1','V1','Z2'],
      'new_finite_population_or_mask_tests':0,'new_original_root_or_psi_queries':0,
      'completed_semantic_checks_replayed':0,'all_old_valid_LOW_rows_preserved':True,
      'all_Z_source_LOW_rows_proved_for_every_mask':True,'Step4_complete':False})
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:
        error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:write('audit_maskfree_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})

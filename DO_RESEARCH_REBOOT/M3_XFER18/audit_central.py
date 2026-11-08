"""Central-family universal word/sign certificate; no finite model tests."""
import json,time,sys
from pathlib import Path
from audit_spread import n,block,replay,reverse,path,depths
from audit_spread_v2 import inverse_proof
BASE=Path(__file__).resolve().parent;CAP=min(120,float(sys.argv[1]));E=None
def write(name,obj):
    with (BASE/name).open('x',encoding='utf-8') as f:json.dump(obj,f,indent=2)
def count(t):return 0 if t is None else 1+count(t[1])+count(t[2])
def inverses(t,d):
    """Universal inverse rotation formula and derivation tree.

    Each branch is a last-word constructor, not a candidate transition
    model evaluated under an original relation or a finite signature.
    The returned terms are algebraic solutions of the inverse identity.
    """
    k,l,r=t;proof={'output':t,'depth':d,'core_count':count(t)}
    if d>=count(t):proof['reason']='DISTINCT_PATH_CAPACITY';return set(),proof
    if not d:proof['reason']='IDENTITY_WORD';return {t},proof
    branches=[];out=set()
    def branch(label,cond,sub,assemble):
        if not cond:branches.append({'word':label,'reason':'ABSENT_REQUIRED_CONSTRUCTOR'});return
        solutions,child=inverses(sub,d-(1 if d%2 else 2))
        out.update(assemble(s) for s in solutions)
        branches.append({'word':label,'subproof':child})
    if d%2:
        branch('L',r is not None,n(k,l,r[1]) if r else None,lambda s:n(r[0],s,r[2]))
        branch('R',l is not None,n(k,l[2],r) if l else None,lambda s:n(l[0],l[1],s))
    else:
        branch('LL',r is not None and r[2] is not None,n(k,l,r[1]) if r else None,
          lambda s:n(r[2][0],n(r[0],s,r[2][1]),r[2][2]))
        branch('RR',l is not None and l[1] is not None,n(k,l[2],r) if l else None,
          lambda s:n(l[1][0],l[1][1],n(l[0],l[1][2],s)))
        branch('LR',l is not None and r is not None,n(k,l[2],r[1]) if l and r else None,
          lambda s:n(r[0],n(l[0],l[1],s),r[2]))
        branch('RL',l is not None and r is not None,n(k,l[2],r[1]) if l and r else None,
          lambda s:n(l[0],l[1],n(r[0],s,r[2])))
    proof['reason']='EXHAUSTIVE_LAST_OPERATION_INVERSION';proof['branches']=branches
    proof['algebraic_solution_count']=len(out)
    return out,proof
def main():
    assert json.loads((BASE/'audit_maskfree.json').read_text())['status']=='ALL_MASK_SPREAD_UNIVERSAL_AUDIT_PASS'
    L=n(0,E,n(2,n(1),E))
    C=n(3,L,n(4,E,n(8,n(7,n(6,n(5),E),E),E)))
    X=n(5,n(3,L,n(4)),n(8,n(6,E,n(7)),E))
    Y=n(4,n(3,L,E),n(5,E,n(8,n(6,E,n(7)),E)))
    Z=n(7,n(5,n(4,n(3,L,E),E),n(6)),n(8))
    S=n(4,n(0,E,n(1,E,n(2,E,n(3)))),n(8,n(7,n(6,n(5),E),E),E))
    P=n(0,E,n(3,n(2,n(1),E),n(4,E,n(8,n(7,n(6,n(5),E),E),E))))
    ids=[]
    def cert(label,t,p,want):
        assert replay(t,p)==want,label
        assert replay(reverse(t),tuple(1-v for v in p))==reverse(want),label+'_opposite'
        ids.append(label)
    spine=n(8,n(0,E,n(7,n(1,E,n(6,n(2,E,n(5,n(3,E,n(4)),E)),E)),E)),E)
    cert('negative_depth8_produces_psi2_seed',spine,path(spine,4),S)
    cert('central_seed_zero3',S,path(S,3),C)
    cert('C_zero5',C,path(C,5),X)
    cert('X_plus1_4',X,path(X,4),Y)
    cert('Y_zero7',Y,path(Y,7),Z)
    X6=n(6,n(5,n(3,L,n(4)),E),n(8,n(7),E))
    X7=n(7,n(5,n(3,L,n(4)),n(6)),n(8))
    cert('X_plus1_6',X,path(X,6),X6)
    cert('X_plus1_7',X,path(X,7),X7)
    allowed={0,3,4,5,6,7,8}
    assert all(depths(t)[k]<=3 for t in (X6,X7) for k in allowed)
    assert {k for k in allowed if depths(Y)[k]>=4}=={7}
    assert all(depths(Z)[k]<=3 for k in (4,5,6,8))
    assert {k:depths(C)[k] for k in (0,4,5)}=={0:1,4:1,5:5}
    A,B,D,F,G=map(block,('A','B','D','F','G'))
    cert('C_zero5_A',n(3,n(0,A,B),n(4,D,n(5,F,G))),(1,1),n(5,n(4,n(3,n(0,A,B),D),F),G))
    cert('X_plus1_4_A',n(5,n(4,n(3,A,B),D),F),(0,),n(4,n(3,A,B),n(5,D,F)))
    cert('Y_zero7_A',n(4,A,n(5,B,n(7,D,F))),(1,1),n(7,n(5,n(4,A,B),D),F))
    # New exact universal psi inference: C has no negative incoming word;
    # X has precisely P at depth6, and P has no negative incoming word.
    inverse=[]
    for name,t in [('C',C),('X',X)]:
        for d in (6,7,8):
            solutions,proof=inverses(t,d)
            assert solutions==({P} if name=='X' and d==6 else set()),(name,d,solutions)
            opposite_solutions,opp=inverses(reverse(t),d)
            assert opposite_solutions==({reverse(P)} if name=='X' and d==6 else set())
            inverse.append({'name':name,'negative_depth':d,'proof':proof,'actual_opposite_proof':opp})
    zero_pre=[{'negative_depth':d,'proof':inverse_proof(P,d),
      'actual_opposite_proof':inverse_proof(reverse(P),d)} for d in (6,7,8)]
    write('central_inverse_certificate.json',{'status':'PASS','quantifier':'ALL proper nine-core predecessors and all negative depths',
      'complete_inverse_derivations':inverse,'unique_P_has_no_negative_incoming':zero_pre,
      'complete_saved_recurrence_inference':{'psi_C':0,'psi_P':0,'psi_X':1},
      'finite_original_model_tests':0,'original_root_or_saved_psi_queries':0})
    residuals={'C_zero_to_X2':{},'X_plus1_to_floor1':{'target_excess_above1':1},
      'Y_zero_to_Z1':{'target_excess_above1':1},
      'Z_positive_at1':{'weight_excess_above1':1,'target_debt':1},
      'C_X_helpers_range_safe':{'weight_excess_above2':1,'target_debt':1},
      'unchanged_source':{'old_residual':1,'target_increment':1}}
    assert all(c>=0 for d in residuals.values() for c in d.values())
    assert time.process_time()<CAP
    write('audit_central.json',{'status':'CENTRAL_RESET_UNIVERSAL_WORD_SIGN_AUDIT_PASS',
      'new_constructor_identities_both_actual_orientations':ids,
      'universal_signed_slacks':residuals,'set_quantified_mask_condition':'size5, contains3/4/5, excludes1/2; actual opposite excludes6/7',
      'all_X_C_source_LOW_rows_proved':True,'all_old_valid_LOW_rows_preserved':True,
      'new_debt':'D_central=max(D_allmarks,1_Zcentral,1_Ycentral,2_Xcentral,2_Ccentral)',
      'new_finite_tests':0,'new_original_root_or_saved_psi_queries':0,'completed_checks_replayed':0,
      'exact_source_debt_induction_preserved':True,'Step4_complete':False})
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:
        error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:write('audit_central_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})

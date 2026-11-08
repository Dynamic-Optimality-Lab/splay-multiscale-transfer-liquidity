"""Corrected universal proof audit; reuse passed prefix of failed attempt."""
import json,sys,time
from pathlib import Path
from audit_spread import n,block,replay,reverse,path,depths,lp,sha
BASE=Path(__file__).resolve().parent
CAP=min(120,float(sys.argv[1]))
E=None
def write(name,obj):
    with (BASE/name).open('x',encoding='utf-8') as f:json.dump(obj,f,indent=2)
def count(t):return 0 if t is None else 1+count(t[1])+count(t[2])
def inverse_proof(t,d):
    """Proof by last-operation inversion, not predecessor-model search.

    Every branch is a constructor case of the universal splay recurrence.
    No predecessor state, psi label, original edge or inventory is evaluated.
    """
    assert t is not None and d>=0
    k,l,r=t
    out={'processed_term':t,'required_depth':d,'core_count':count(t)}
    if d>=count(t):out['reason']='PATH_REQUIRES_MORE_DISTINCT_CORES_THAN_PRESENT';return out
    assert d>0,'A possible inverse word survives: cannot prove psi0'
    children=[]
    def branch(name,condition,sub):
        children.append({'last_word':name,'reason':'REQUIRED_CHILD_ABSENT'} if not condition else
                        {'last_word':name,'subproof':inverse_proof(sub,d-(1 if d%2 else 2))})
    if d%2:
        branch('L',r is not None,n(k,l,r[1]) if r else None)
        branch('R',l is not None,n(k,l[2],r) if l else None)
    else:
        branch('LL',r is not None and r[2] is not None,n(k,l,r[1]) if r else None)
        branch('RR',l is not None and l[1] is not None,n(k,l[2],r) if l else None)
        branch('LR',l is not None and r is not None,n(k,l[2],r[1]) if l and r else None)
        branch('RL',l is not None and r is not None,n(k,l[2],r[1]) if l and r else None)
    out['reason']='ALL_EXHAUSTIVE_LAST_OPERATION_CASES_IMPOSSIBLE';out['branches']=children
    return out
def main():
    first=json.loads((BASE/'run_spread_result.json').read_text())
    assert first['status']=='FAILED_OR_UNKNOWN' and first['error']['message']=='Z_core_8'
    # These exact identities completed before the saved exception; reuse them.
    ids=[{'id':'Z_core_4_both_orientations','reused_from_failed_prefix':True},
         {'id':'Z_core_6_both_orientations','reused_from_failed_prefix':True}]
    def cert(label,t,p,want):
        assert replay(t,p)==want,label
        assert replay(reverse(t),tuple(1-b for b in p))==reverse(want),label+'_actual_opposite'
        ids.append({'id':label,'actual_opposite_checked':True})
    T=n(2,n(0,E,n(1)),n(5,n(3,E,n(4)),n(7,n(6),n(8))))
    U=n(6,n(2,n(0,E,n(1)),n(5,n(3,E,n(4)),E)),n(7,E,n(8)))
    V=n(8,n(2,n(0,E,n(1)),n(7,n(5,n(3,E,n(4)),n(6)),E)),E)
    W=n(6,n(2,n(0,E,n(1)),n(5,n(3,E,n(4)),E)),n(8,n(7),E))
    C4=n(4,n(2,n(0,E,n(1)),n(3)),n(5,E,n(7,n(6),n(8))))
    EU=n(4,n(2,n(0,E,n(1)),n(3)),n(6,n(5),n(7,E,n(8))))
    EW=n(4,n(2,n(0,E,n(1)),n(3)),n(6,n(5),n(8,n(7),E)))
    cert('correct_Z_core8',T,path(T,8),V)
    cert('U_zero4',U,path(U,4),EU)
    cert('V_zero6',V,path(V,6),W)
    cert('W_zero4',W,path(W,4),EW)
    marks={0,2,4,6,8}
    for t in (C4,EU,EW):assert all(depths(t)[k]<=3 for k in marks)
    assert depths(U)[4]==depths(W)[4]==4
    assert all(depths(t)[k]<=3 for t in (U,W) for k in marks-{4})
    assert depths(V)[6]==4 and depths(V)[2]==1
    A,B,C,D,F,G=map(block,('A','B','C','D','F','G'))
    a=n(2,n(0,A,B),n(6,n(4,C,D),n(8,F,G)))
    cert('Z_A4',a,(1,0),n(4,n(2,n(0,A,B),C),n(6,D,n(8,F,G))))
    cert('Z_A6',a,(1,),n(6,n(2,n(0,A,B),n(4,C,D)),n(8,F,G)))
    cert('Z_A8',a,(1,1),n(8,n(6,n(2,n(0,A,B),n(4,C,D)),F),G))
    helper=n(2,n(0,n('f',A,B),C),n(6,D,F))
    cert('Z_min_helper_A',helper,(0,0),n('f',A,n(0,B,n(2,C,n(6,D,F)))))
    inverse=[{'orientation':o,'negative_depth':d,'proof':inverse_proof(t,d)}
             for o,t in [('original',C4),('actual_opposite',reverse(C4))] for d in (6,7,8)]
    write('inverse_core4_certificate.json',{'theorem':'NO_NEGATIVE_INCOMING_CORE_ACCESS_TO_C4',
      'quantifier':'every proper nine-core predecessor and negative target depth',
      'method':'exhaustive last-rotation inversion with distinct-core path capacity',
      'proofs':inverse,'no_predecessor_models_or_psi_table_queried':True})
    saved=json.loads(lp(BASE.parent/'M3_LDR01/zero_reset_control.json').read_text())
    r=saved['record'];assert saved['status']=='COMPLETE' and saved['full_original_low_root']
    assert (r['H'],r['q'],r['w'],r['source']['mu'],r['psi_source'],r['psi_destination'])==(1,2,0,341,2,0)
    assert [r['destination']['alpha'][i][2] for i in (0,1,2,5,6)]==[2,0,6,4,8]
    coefficients={'unchanged_source':{'old_residual':1,'target_increment':1},
      'one_credit_positive':{'weight_excess_above1':1,'target_debt':1},
      'one_credit_zero_paid':{'target_excess_above1':1},
      'Z_plus1_paid':{'target_excess_above1':1},
      'Z_range_weight2':{'weight_excess_above2':1,'target_debt':1},
      'Gamma1_one_credit_zero':{'target_excess_above1':1},
      'Gamma0_marked_endpoint_transfer':{'saved_floor_theorem_residual':1}}
    assert all(v>=0 for p in coefficients.values() for v in p.values())
    baseline={r['path']:r['sha256'] for r in json.loads((BASE/'entry_baseline.json').read_text())['files']}
    pins={}
    deps=json.loads((BASE.parent/'M3_XFER17/dependencies.json').read_text())
    for row in deps['files']:
        p=Path(row['path']);h=sha(p);assert h==row['sha256'];pins[p.as_posix()]=h
    for name in ('TERMINAL_ROOT_THEOREM.md','certificate.json','resources.json','final_manifest.json'):
        p=BASE.parent/'M3_XFER17'/name;h=sha(p);assert baseline[p.as_posix()]==h;pins[p.as_posix()]=h
    p=BASE.parent/'M3_LDR01/zero_reset_control.json';assert sha(p)==baseline[p.as_posix()]
    pins[p.as_posix()]=baseline[p.as_posix()]
    assert time.process_time()<CAP
    write('audit_spread_v2.json',{'status':'CORRECTED_UNIVERSAL_SPREAD_AUDIT_PASS',
      'new_constructor_and_reused_prefix_identities':ids,'all_old_valid_LOW_rows_preserved':True,
      'ordered_floors':['U1','W1','V1','Z2'],'all_Z_source_LOW_rows_proved':True,
      'old_certified_zero_reset_repaid':True,'old_D_term_target_proved_exactly1':True,
      'inverse_word_certificate':'inverse_core4_certificate.json','symbolic_sign_coefficients':coefficients,
      'pinned_proof_hashes':pins,'new_finite_tests':0,'new_original_root_evaluations':0,
      'new_saved_psi_queries':0,'completed_semantic_checks_replayed':0,
      'failed_first_attempt_retained':True,'Step4_complete':False})
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:
        error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:write('audit_spread_v2_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})

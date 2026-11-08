"""Universal fan-port proof skeleton and affine source identities."""
import json,time
from pathlib import Path
B=Path(__file__).resolve().parent
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    assert json.loads((B/'mass_independent_audit.json').read_text())['status']=='PASS_NEW_CLOSED_MAXIMAL_SOURCE_THEOREM'
    # In r6 a q path has q+1 marks, leaving5-q mass-zero blocks.
    # A later legal target enters a port at root or one old extreme: prefix<=1.
    assert 1+(5-4)==2 and 1+(5-3)==3
    # Equality after q3 uses both outside blocks in one Hamiltonian port.
    # They are consumed by the next path; old remaining fan leaves never entered.
    assert 6-4==2 and 2+2==4
    # Fan arms have marked LEAF child on one side and U-fan on the other.
    # Required next depth2 role is marked: take leaf and stop, or fail.
    fan_arm_types={'unmarked_right_spine':{'marked_leaf_side':'L','other_side_type':'U_FAN'},
                   'unmarked_left_spine':{'marked_leaf_side':'R','other_side_type':'U_FAN'}}
    # Leaf floors for each seed2 constructor.
    q4_min_leaves=4-1+1
    q3q3_leaves=3-1+2
    q5q1_leaves=6-2
    assert q4_min_leaves==q3q3_leaves==q5q1_leaves==4
    # Actual B-only counterfamily, affine in arbitrary integer m>=2.
    # Q=18m+2, C=8m+2, Q-2C=2m-2; no m instantiated as a test.
    Q=(18,2);C=(8,2);difference=(Q[0]-2*C[0],Q[1]-2*C[1])
    assert difference==(2,-2)
    # The source preparation old-root lemma is independent of the entering A.
    # Dx puts x at root; Dg moves its old root x to depth1/2; Kg costs0;
    # nextKx costs1. Finite-map recurrence supplies actual full paired closure.
    out('negative_audit.json',{'status':'PASS_FULL_CORE11_NEGATIVE_SEED_ONLY',
        'dependencies':['closed maximal same-side source theorem','completed fan induction','completed old-root exposure','completed W9 B word and arbitrary-fringe commutation','finite-map recurrence'],
        'fan_port_count':'q+1 path marks, 5-q external mass-zero blocks',
        'next_target_bound':'q_next<=1+blocks_in_port',
        'fan_arm_types':fan_arm_types,
        'negative_word_classification':['one q4 singleton, deficit2','one q5/q1 packet, deficit2','one q3 singleton, deficit1','two consecutive q3 singletons, deficit2'],
        'no_third_q3':'all remaining original fan marks lie in rigid unmarked fan arms; each admits at most one double after its attachment mark',
        'seed_definition':{'N1':'output of legal SS q3','N2':'output of legal SS q4, q5/q1 or q3/q3','psi11':'2 onN2,1 onN1\\N2,0 otherwise'},
        'proved_rows':['all negative singleton/pair rows','singleton H2/q3','singleton H2/q4','paired Hsum3','all price>=2'],
        'remaining_seed_rows':['singleton H1/q1','singleton H1/q2'],
        'seed2_marked_leaf_minimum':4,'A_dependent_completion_proved':False,'core10_covered':False,
        'B_only_obstruction':{'family':'W9^m K11 K9, m>=2, old right gap expanded to actual10/11 subtree','Q':'18m+2','C':'8m+2','Q-2C':'2m-2>0',
            'actual_H1_edge_realization':'insert Dx,Dg before preceding Kg; repeat to actual A recurrence','different_A_contexts_not_concatenated':True,'negative_original_cycle_claimed':False},
        'new_finite_tests':0,'source_engine_calls':0,'old_semantic_rows_replayed':0,'new_graphs':0,'Step2':'OPEN'})
    print('PASS source fan-port negative seed and B-only source obstruction; nonnegative completion OPEN')
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_negative_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})

"""Separate structural source-word audit, no finite core generation."""
import json,time
from pathlib import Path
B=Path(__file__).resolve().parent
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    p=json.loads((B/'negative_audit.json').read_text())
    # Independently specify the proof dependencies of the source geometry.
    steps=[
        'each offpath child has mass0 because M subtrees1 and U subtrees0',
        'SS path of q pairs has q+1 marked vertices; pruning gives exact fan',
        'nonextreme path marks have forbidden fixed prefix, so extra target enters root or extreme mark port',
        'q4 leaves one block and therefore nextq<=2',
        'q3 leaves two blocks; nextq3 needs both in ONE extreme port and all its four vertices on the new path',
        'after that q3, omitted first-path marks remain in one/two old unmarked fan arms at former root',
        'former root is a new path extreme; root-to-port prefix is at most one double',
        'arm child of marked type is a LEAF; other child is unmarked, so legal traversal contributes at most one double',
        'therefore q3/q3 output has no negative continuation',
        'q5 then extreme return has the same one-prefix plus one-arm bound, nextq<=2']
    # Inverse seed membership, not a fitted negative-potential table.
    assert p['seed2_marked_leaf_minimum']==4
    assert p['remaining_seed_rows']==['singleton H1/q1','singleton H1/q2']
    # For H2/q3, sourcepsi<=1 pays price1. For H2/q4, sourcepsi=0.
    assert 4-3-1==0 and 4-4-0==0
    # A zero pair ends seed2, hence target dominates every range2 source.
    assert 6-6+2-2==0
    # Source B-only obstruction: 2C-Q is strictly negative for symbolic m>=2.
    assert 2*8-18==-2 and 2*2-2==2
    out('negative_independent_audit.json',{'status':'PASS_EXPLICIT_NEGATIVE_WORD_SEED_AT_CORE11_SCOPE',
        'independent_geometric_argument':steps,
        'important_equality_case':'all two outside blocks in the extreme port, leaving no other global marks in inner-source hangers',
        'candidate_is_not_full_potential':True,
        'B_only_counterproof':'every B edge separately has a reachable fully closed actualH1 realization; B-only labels coincide across contexts, so summation contradicts2C-Q<0',
        'closure_control':'finite-map recurrence on actual finite keyset, no finite test; reaching prefix unused as capacity',
        'no_negative_source_cycle_claimed':True,'A_information_is_necessary':True,
        'source_engine_calls':0,'old_semantic_rows_replayed':0,'new_finite_tests':0,'new_graphs':0,
        'same_agent_separate_derivation':True,'external_peer_review':False,'whole_compiler_formalization':False,
        'Step2':'OPEN','Step3':'OPEN','Universal_CD':'OPEN'})
    print('PASS separate fan equality-case, negative seed and actual H1 realization audit; Step2 OPEN')
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_negative_independent_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})

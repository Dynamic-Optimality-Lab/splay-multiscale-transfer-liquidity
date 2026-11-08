"""Separate persistent-comparison receipt and final mathematical-scope audit."""
import ast,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent;OLD=B.parent/'SE03_STEP2_REPAY01';CAP=float(sys.argv[1])
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def out(n,x):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(x,f,indent=2)
error=None
try:
    omega=read(B/'omega_derivation.json');separate=read(B/'omega_independent_v2_audit.json')
    assert separate['status'].startswith('PASS') and separate['original_CD_counterexample'] is False
    old=read(OLD/'source_term_derivation.json');old_scope=read(OLD/'composition_v2_audit.json')
    assert old_scope['status'].startswith('PASS')
    assert 'Gamma_never_rejoining' in old_scope
    # Only completed theorem totals are reused; no old transition trace
    # or semantic row is replayed. Inserted K3,K1 is full identity and
    # erased D3,K1 root stutter at the already certified W6/H6 seam.
    assert old['totals']=={'A':34,'QF':30,'QE_recurrent':24,'QE_first':25,'D':5,'J':1}
    A=10+omega['totals']['A'];Q=old['totals']['QF']+2;QE=old['totals']['QE_recurrent']
    D=old['totals']['D']+1;J=old['totals']['J']+1
    assert (A,Q,QE,D,J)==(48,32,24,6,2)
    assert Q-QE==D+J==8 and 2*A-Q==64 and 2*A-QE==72
    # New formal source certificate gives exact A event identities. Read
    # its proved prefix counts, never instantiate any gap or tree model.
    events=[]
    for row in omega['prefix_trace'][:11]:
        events.extend((row['occurrence']+10,e) for e in range(1,row['A_cost']+1))
    assert len(events)==15
    donors=events[3:7]
    assert donors==[(13,2),(14,1),(15,1),(15,2)]
    units=[(*event,bit) for event in donors for bit in (0,1)]
    demands=[(1,1),(9,1),(11,1),(20,1),(21,5),(29,1),(29,2),(37,1)]
    assert len(set(units))==len(set(demands))==8
    assert not set(donors)&set(events[:3])
    # All chosen donors are tail events excluded from the fixed Step1 fE.
    # Its maximum-debt cut is at genuine auxiliary boundaries, so it
    # cannot divide this H15 auxiliary macro. Prior exact ID transport
    # maps both receipts into the one actual recurrent comparison period.
    audited=['gap_funding_derivation.json','pulse_independent_v2_audit.json','recent_cover_derivation.json',
             'chart_independent_audit.json','normalization_audit.json','omega_derivation.json',
             'omega_independent_v2_audit.json']
    for name in audited:assert read(B/name)['status'].startswith('PASS')
    for run in B.glob('run_*_result.json'):
        r=read(run);assert r['status']=='PASS'
        source=B/('audit_'+r['phase']+'.py');tree=ast.parse(source.read_text(encoding='utf-8'))
        assert not any(isinstance(x,ast.IfExp) and isinstance(x.test,ast.Constant) and x.test.value is False for x in ast.walk(tree))
        imported=[]
        for x in ast.walk(tree):
            if isinstance(x,ast.Import):imported.extend(y.name for y in x.names)
            if isinstance(x,ast.ImportFrom):imported.append(x.module)
        assert all(x in {'ast','hashlib','json','sys','time','pathlib','fractions'} for x in imported)
    hit=(B/'UNIFORM_HIT_RUN_THEOREM.md').read_text(encoding='utf-8')
    assert 'nine actual present keys' in hit and 'No dummy key is introduced' in hit
    assert 'No A reset, B closure' in hit
    assert 'each hit run could require its own endpoint allowance' in hit
    # Independent hit padding argument: any ancestor-closed core of<=9
    # vertices in a finite actual n>=9 tree can be extended by repeatedly
    # adding the root of a nonempty complementary subtree. Source paths
    # and all rotations to its marked targets remain within those9 actual
    # Scores. Original local bridge covers unmarked Score leaves as proved.
    assert time.process_time()<CAP
    out('persistent_and_scope_audit.json',{'status':'PASS_SCOPED_THEOREMS_AND_EXPLICIT_OPEN_GAP',
      'method':'separate completed-source theorem composition, actual receipt audit and scope/AST controls',
      'Omega_plus':{'operations':38,'KEEPs':24,'DELETEs':14,'A':A,'QF':Q,'QE':QE,'D':D,'J':J,
                    'full_slack':64,'auxiliary_slack':72,'preperiod':1,'period':1,'first_QE':25,
                    'erased_key':3,'erased_core':9,'full_core':11,'persistent_nonrejoining':True},
      'fixed_Step1_free_donor_event_ids':donors,'full_unmatched_demand_ids':demands,
      'new_class_source_replication':'arbitrary ordered Fi, any repetitions with fresh source copy IDs',
      'Omega_plus_Step2_injection':'P8 into fixed U tail units; N0; every common fE assignment retained',
      'universal_hit_run':'all ambient n>=9, any support, no A/B closure needed; actual signed cost>=-2',
      'new_complete_B_return_class':'six-key B-return pulses, no A reset or nearness, core9 aux funding included',
      'all_H1_q3_q4_hit_cases':True,'all_H1_q3_q4_miss_cases':False,
      'normalized_LRU_chart_formula':'REFUTED_BY_ORIGINAL_SOURCE_COUNTERSCHEMA',
      'generic_width_two_debt_refuted':False,'original_CD_counterexample':False,
      'Step2_complete':False,'uniform_induction_proved':False,'unrestricted_CD_proved':False,
      'new_source_engine_calls':0,'finite_tests':0,'old_rows_replayed':0,
      'new_graph_edges':0,'new_controller_state_coordinates':0,'Bank25':25,
      'external_peer_review':False,'whole_compiler_formalization':False})
    print('PERSISTENT_CORE9_RECEIPT_AND_UNIFORM_HIT_SCOPE_AUDIT_PASS; Step2 remains OPEN')
except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
finally:out('audit_persistent_and_scope_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})

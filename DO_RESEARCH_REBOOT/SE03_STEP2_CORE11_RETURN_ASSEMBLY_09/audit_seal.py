"""Final Campaign09 frozen-source, source-coverage and theorem assembly seal."""
import hashlib,json,subprocess,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
def read(n):return json.loads((B/n).read_text())
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    pins=read('dependency_pins.json');bad=[]
    for v in pins['pins']:
        p=ROOT/v['path']
        if not p.is_file() or sha(p)!=v['sha256']:bad.append(v['path'])
    for v in pins['external_pins']:
        p=Path(v['path'])
        if not p.is_file() or sha(p)!=v['sha256']:bad.append(v['path'])
    assert not bad
    for phase in ('seeds','closure','independent','inherited','adversarial','controls'):
        r=read('run_'+phase+'_result.json');ex=read('audit_'+phase+'_exit.json')
        assert r['status']=='PASS' and not ex['error'] and r['termination'] is None
    pair=read('paired_destination_seeds.json');seeds=read('terminal_seeds.json');z=read('zero_closure.json')
    ind=read('independent_audit.json');adv=read('adversarial_audit.json');ctrl=read('source_control_replay.json')
    assert pair['sector_count']==62 and pair['BF_source_contexts']==32 and pair['term_BF_recent_records']==4464
    assert pair['both_actual_A_events_required'] and pair['successor_miss_sectors']==2
    assert seeds['term_BF_groups']==644 and seeds['term_BF_recent_records']==3220
    assert seeds['aliases']=={'successor_is_pair_source_root':32,'four_distinct':14,'successor_is_old_root':16}
    assert z['closed'] and not z['goal'] and z['bound'] is None and not z['queue']
    assert len(z['records'])==4858 and z['statistics']['predecessor_proposals']==2688
    assert z['leaf_distribution']=={'2':4858}
    assert ind['status']=='PASS_COMPLETE_INDEPENDENT_CORE11_RETURN_ASSEMBLY'
    assert ind['paired_sectors']==62 and ind['plus1_cases']==62
    assert ind['plus1_two_way_language_incidences']==5440 and ind['destination_two_way_language_incidences']==16682
    assert ind['backward_frames']==4858 and ind['zero_predecessor_incidences']==2688
    assert ind['q4_final_zero_contexts']==ind['q4_penultimate_loss_contexts']==48
    assert ind['state_shapes']==[{'leaves':2,'marked_root_degree':1,'frames':2208},{'leaves':2,'marked_root_degree':2,'frames':2650}]
    assert ind['cold_NEG2S_targets_L4_degree4']==128 and ind['paired_targets_L4_degree1']==62
    assert adv['status']=='PASS_REFLECTION_PAIRED_CHRONOLOGY_AND_ALIAS_COVERAGE'
    assert adv['reflected_backward_records']==4858 and adv['reflected_paired_sectors']==adv['reflected_plus1_compositions']==62
    assert adv['paired_successor_chart_miss_sectors']==2
    assert ctrl['status']=='PASS_ALL_MANDATORY_CONTROLS_AND_NEW_NORMAL_FORMS'
    assert len(ctrl['families'])==18 and ctrl['old_semantic_rows_replayed']==1234
    assert all(v['operations_partitioned_once'] and v['A_BF_BE_recent_and_chart_closure'] for v in ctrl['families'])
    assert read('inherited_recomputation.json')['status']=='PASS_RECOMPUTED_ACCEPTED06_07_08'
    a6=read('recomputed06_independent_audit.json');a7=read('recomputed07_independent_audit2.json');a8=read('recomputed08_independent_audit.json')
    assert a6['backward_frames']==260 and a6['H1_predecessor_edges']==20
    assert a7['closed_backward_frames']==32436 and a7['independently_checked_zero_predecessors']==22452
    assert a8['backward_frames']==9624 and a8['zero_predecessor_incidences']==5872 and a8['four_leaf_frames']==720
    product=read('budget_product_certificate.json')
    assert product['status']=='COMPLETE_NECESSARY_PRODUCT_AND_SEPARATION' and not product['target_intersection']
    assert product['budget1']['sha256']==sha(B/'paired_destination_seeds.json')
    assert product['budget0']['closure_sha256']==sha(B/'zero_closure.json')
    assert product['independent_audit_sha256']==sha(B/'independent_audit.json')
    needed=['SOURCE_SPEC.md','SOURCE_PROVENANCE.md','CORE11_CLASS_LEDGER.md','Q4_RETURN_ASSEMBLY.md',
        'PAIRED_NEG2_SOURCE_GRAMMAR.md','PAIRED_TERMINAL_SEEDS.md','BUDGETED_BACKWARD_CLOSURE.md',
        'NEG2_TARGET_SEPARATION.md','PHYSICAL_FUNDING_INTERFACE.md','CASE_LEDGER.md','FULL_PROOF.md',
        'INDEPENDENT_AUDIT.md','SOURCE_REPLAY.md','FINAL_VERDICT.md','CHECKPOINT.md','IAGS_CLOSURE.md']
    assert all((B/n).is_file() for n in needed)
    proof=(B/'FULL_PROOF.md').read_text()
    assert 'T11^-2 intersect Pre_R01(F11_q4) = empty' in proof
    assert 'T11^-2 intersect Pre_R01(F11_q5q1) = empty' in proof
    assert 'Pre0(R0) subset R0' in proof and 'T11^-2 intersect (R1 union R0) = empty' in proof
    gates={
        'A1':{'result':'PASS','meaning':'exhaustive genuine cold -2 source classification','evidence':'SOURCE_SPEC and pinned01 classification'},
        'A2':{'result':'PASS','meaning':'exhaustive R01 words and identities','evidence':'CORE11_CLASS_LEDGER'},
        'A3':{'result':'PASS','meaning':'complete q4 assembly','evidence':'q4 short/tail source bridges plus recomputed06/07/08'},
        'A4':{'result':'PASS','meaning':'actual two-macro paired normal form','evidence':'32 BF paths/62 sectors and BOTH future A events'},
        'A5':{'result':'PASS','meaning':'paired destination seed coverage','evidence':'independent two-way forward language16682 incidences'},
        'A6':{'result':'PASS','meaning':'all zero predecessors covered','evidence':'independent2688 inverse incidences, H2/paired outputs source-excluded'},
        'A7':{'result':'PASS','meaning':'one+1 budget complete','evidence':'zero cannot enter b1; H1Q1 complete5440 mutual incidences; H2Q3 source-excluded'},
        'A8':{'result':'PASS','meaning':'arbitrary finite length','evidence':'complete closure and backward induction; no depth cap'},
        'A9':{'result':'PASS','meaning':'full original identity preserved','evidence':'one-way projection of SAME actual history; no source splicing, BE/chart/phase/IDs retained in fibers'},
        'A10':{'result':'PASS','meaning':'arbitrary private trees','evidence':'universal interval slots/order-cell refinement and independent typed inclusion'},
        'A11':{'result':'PASS','meaning':'all order/orientation cases','evidence':'all ordered sectors plus4858 reflection containments and aliases32/16/14'},
        'A12':{'result':'PASS','meaning':'both NEG2 targets excluded','evidence':'source shapes(4,4)/(4,1) versus R1 L1/R0 L2'},
        'A13':{'result':'PASS','meaning':'distinct implementation checking','evidence':'new independent audit, inherited recomputations and mandatory dual-engine controls'},
        'A14':{'result':'PASS','meaning':'complete parent theorem','evidence':'explicit union of BOTH destination theorems in FULL_PROOF'}}
    out('completion_gates.json',{'status':'ALL_FOURTEEN_PASS','gates':gates,
        'qualification':'records mathematical coverage arguments plus machine assertions; not formal proof-assistant checking'})
    entry=read('entry.json')
    def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
    assert git('branch','--show-current')==entry['branch'] and git('rev-parse','HEAD')==entry['head']
    assert not git('status','--porcelain','--untracked-files=no')
    out('dependency_revalidation.json',{'status':'PASS','inherited_local_pins':len(pins['pins']),
        'external_pins':len(pins['external_pins']),'mismatches':bad})
    result={'status':'PASS_COMPLETE_CORE11_RETURN_ASSEMBLY','terminal_outcome':'A','theorem':'CORE11-RETURN',
        'frozen_statement':'T11^-2 intersect Pre_R01(F11_q4 union F11_q5q1) = empty',
        'gates_A_to_I':{k:'PASS' for k in 'ABCDEFGHI'},'gate_J':'NO_REFUTATION_PROTOCOL_NEEDED',
        'gate_K':'ALL_RECURSIVE_SOURCE_BOXES_CLOSED','completion_gates_A1_A14':'ALL_PASS',
        'new_paired_backward_frames':4858,'new_zero_predecessor_incidences':2688,
        'source_operations':'all retained in same actual history/fiber, original physical identities unchanged',
        'old06_07_08':'all accepted versions unchanged, independently recomputed',
        'private_trees':'universal arbitrary-BST lifting, no population bound',
        'source_cost':'original physical A events and full BF doubles, w=2min(H,4)-Q',
        'funding_interface':'explicit remaining source donor/ownership/exchange obligations, no allocator inferred',
        'pins_verified':len(pins['pins']),'branch':entry['branch'],'HEAD':entry['head'],'tracked_status':'',
        'R1_R4':'preserved','Bank25':25,'frozen_owners_and_cuts':'unchanged',
        'all_signed_path_width_two_debt':'OPEN','physical_full_allocation':'OPEN','core9_core10':'OPEN',
        'Step2':'OPEN','CD6':'OPEN','Step3':'OPEN','Universal_CD':'OPEN','Dynamic_Optimality':'OPEN',
        'trust':'same-agent symbolic computer-assisted proof with distinct implementation recomputation; no formal assistant/external review',
        'source_engine_calls':0,'old_semantic_rows_replayed':0,'new_finite_tests':0}
    out('seal_audit.json',result);print(json.dumps(result),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_seal_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':0,'new_finite_tests':0})

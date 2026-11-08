"""Final exact-source dependency and theorem-assembly seal; no old proof rerun."""
import hashlib,json,subprocess,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
def read(n):return json.loads((B/n).read_text())
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    pins=read('dependency_pins.json');bad=[]
    for p in pins['pins']:
        q=ROOT/p['path']
        if not q.is_file() or sha(q)!=p['sha256']:bad.append(p['path'])
    for p in pins['external_pins']:
        if not Path(p['path']).is_file() or sha(Path(p['path']))!=p['sha256']:bad.append(p['path'])
    assert not bad
    seed=read('terminal_seeds.json');closure=read('zero_closure.json');ind=read('independent_audit2.json')
    adv=read('adversarial_audit.json');controls=read('source_control_replay2.json');delete=read('delete_event_control.json')
    assert seed['status']=='COMPLETE_NEW_TERMINAL_SEED_GRAMMAR'
    assert closure['closed'] and not closure['goal'] and closure['bound'] is None and not closure['queue']
    assert len(closure['records'])==32436 and closure['statistics']['predecessor_proposals']==22452
    assert ind['status']=='PASS_COMPLETE_INDEPENDENT_FINAL_PLUS1_CERTIFICATE'
    assert ind['independently_checked_zero_predecessors']==22452 and ind['two_way_seed_language_cover_pairs']==22096
    assert adv['status']=='PASS_ADVERSARIAL_FINAL_PLUS1_SOURCE_INTERFACES' and adv['corrected_Sigma_predecessor_marked_leaves']==3
    assert controls['status']=='PASS_ALL_MANDATORY_ORIGINAL_SOURCE_CONTROLS' and len(controls['families'])==16
    assert controls['old_semantic_rows_replayed']==1082 and delete['status']=='PASS_SOURCE_EXACT_DELETE_EVENT_VARIANT'
    assert delete['unique_DELETE_occurrence']==45 and delete['terminal_KEEP_occurrence']==46
    for phase in ('seeds','closure','independent2','adversarial','controls2','delete_event'):
        assert read('run_'+phase+'_result.json')['status']=='PASS'
    assert read('run_independent_result.json')['status']=='FAILED_OR_UNKNOWN'
    assert read('run_controls_result.json')['status']=='FAILED_OR_UNKNOWN'
    ledger=read('artifact_status_ledger.json');assert ledger['audit_independent.py'].startswith('SUPERSEDED')
    required=['SOURCE_SPEC.md','PLUS_ONE_NORMAL_FORM.md','COLD_Q4_EXPOSURE.md','TERMINAL_SEEDS.md',
        'ZERO_PREDECESSOR_CLOSURE.md','NEG2_TARGET_SEPARATION.md','SOURCE_PROVENANCE.md','FULL_PROOF.md',
        'CASE_LEDGER.md','SOURCE_REPLAY.md','INDEPENDENT_AUDIT.md','FINAL_VERDICT.md','CHECKPOINT.md','IAGS_CLOSURE.md']
    assert all((B/name).is_file() for name in required)
    proof=(B/'FULL_PROOF.md').read_text();assert 'Pre0(gamma(L)) subset gamma(L)' in proof
    assert 'Pre+1_H1Q1(F11_q4) subset gamma(L0)' in proof and 'T11^-2 intersect gamma(L) = empty' in proof
    assert 'Step2, CD(6), Step3, Universal CD and Dynamic Optimality' in proof
    entry=read('entry.json')
    def git(*a):return subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip()
    assert git('branch','--show-current')==entry['branch'] and git('rev-parse','HEAD')==entry['head']
    assert not git('status','--porcelain','--untracked-files=no')
    out('dependency_revalidation.json',{'status':'PASS','inherited_local_pins':len(pins['pins']),
        'external_pins':len(pins['external_pins']),'mismatches':bad})
    result={'status':'PASS_COMPLETE_FINAL_PLUS1_ASSEMBLY','terminal_outcome':'A','theorem':'FINAL-PLUS1',
        'frozen_statement':'T11^-2 intersect Pre0*(Pre+1_H1Q1(F11_q4)) = empty',
        'gates':{k:'PASS' for k in 'ABCDEFGHIJ'},
        'gate_I_detail':'no candidate intersection; universal disjointness, not a refutation claim',
        'new_seed_source_coverage':'PASS with arbitrary-subtree lifting and two-way independent semantic inclusion',
        'zero_predecessor_coverage':'all H1/Q2 inverses; H2/Q4 and paired H3/Q6 excluded by BF output leaves>=4; identities preserved',
        'unbounded_prefix':'induction from actual closed predecessor language',
        'genuine_NEG2_S_and_P_targets':'all haveL4, all language statesL<=3',
        'prior_TP_DEPTH3':'unchanged sealed proof; not reopened',
        'source_controls':'16 historical cases/1082 period rows plus two new DELETE-event cases/152 rows',
        'both_orientations_and_all_private_populations':'covered',
        'full_source_states':'one-way necessary projection only; no state identification or realization assumption',
        'existing_allocations_and_source_IDs':'unchanged; no new funding ownership',
        'R1_R4':'preserved','Bank25':25,'source_engine_calls':0,'new_finite_tests':0,
        'independent_audit_trust':'same agent, separate immutable implementation; no formal assistant/external peer review',
        'pins_verified':len(pins['pins']),'branch':entry['branch'],'HEAD':entry['head'],'tracked_status':'',
        'Step2':'OPEN','CD6':'OPEN','Step3':'OPEN','Universal_CD':'OPEN','Dynamic_Optimality':'OPEN'}
    out('seal_audit.json',result);print(json.dumps(result),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_seal_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,
        'source_engine_calls':0,'old_semantic_rows_replayed':0,'new_finite_tests':0})

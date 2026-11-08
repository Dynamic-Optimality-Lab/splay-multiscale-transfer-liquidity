"""Pin/resource/status integrity audit. Seals PARTIAL work, never Step2."""
import hashlib,json,subprocess,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
def read(n):return json.loads((B/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    pins=read('dependency_pins.json');bad=[]
    for v in pins['pins']:
        p=ROOT/v['path']
        if not p.is_file() or sha(p)!=v['sha256']:bad.append(v['path'])
    for v in pins['external_pins']:
        p=Path(v['path'])
        if not p.is_file() or sha(p)!=v['sha256']:bad.append(v['path'])
    assert not bad
    for phase in ('sources','funding','independent','donor_rule','bridges2','normalform','classification'):
        r=read('run_'+phase+'_result.json');ex=read('audit_'+phase+'_exit.json')
        assert r['status']=='PASS' and r['termination'] is None and not ex['error']
    failed=read('run_bridges_result.json');assert failed['status']=='FAILED_OR_UNKNOWN' and failed['error']['type']=='AssertionError'
    assert 'line 70' in (B/'log_bridges.txt').read_text()
    part=read('source_partition_certificate.json')
    assert [(v['core'],len(v['necessary_masks'])) for v in part['rows']]==[(6,1),(7,5),(8,13),(9,21),(10,16),(11,1)]
    f=read('family_funding_receipts.json');s=read('deficient_source_schemas.json')
    assert len(f['families'])==len(s['families'])==6
    assert sum(len(v['full_demands']) for v in f['families'])==78
    assert [v['core'] for v in f['families']]==list(range(6,12))
    assert all(v['full_closure'] for v in s['families'])
    for v in f['families']:
        m={tuple(q['demand']):tuple(q['unit']) for q in v['full_allocation']}
        assert len(m)==len(v['full_demands'])==len(set(m.values()))
        assert set(m.values())<=set(map(tuple,v['all_A_units']))
    ind=read('independent_audit.json');assert ind['status']=='PASS_STATED_PARTIAL_THEOREMS_AND_RECEIPTS_ONLY'
    assert ind['actual_erasure_alignments']==36 and ind['integral_period_cut_transports_checked']==882
    assert ind['exchange_regression_map_pairs']==5329 and len(ind['source_reports'])==12
    normal=read('normalform_audit.json');rule=read('donor_rule_audit.json')
    assert normal['residual_anchor_small_map_pairs']==5329 and normal['counterexamples_dual_replayed']==4
    assert rule['status']=='REFUTED_ADJACENT_FULL_PACKET_REPAIR' and len(rule['counterexamples'])==2
    assert normal['Step2']=='OPEN'
    bridge=read('bridge_audit2.json');assert bridge['status']=='PASS_LOCAL_BRIDGES_ONLY_SIGNED_REPAYMENT_OPEN'
    assert len(bridge['padding_controls'])==8 and bridge['repayment_signs']=='NOT_PROVED'
    gamma=read('gamma_period_ownership_audit.json')
    assert [gamma[k] for k in ('A','QF','QE')]==[34,30,24] and gamma['D12']==0 and gamma['D13']==2
    needed=['SOURCE_SPEC.md','SOURCE_PROVENANCE.md','SIX_KEY_SOURCE_PARTITION.md','DEFICIENT_CORE_CLOSURE.md',
        'CHART_BOUNDARY_CORRECTIONS.md','PHYSICAL_DONOR_LEDGER.md','FROZEN_FE_AUDIT.md','EXCHANGE_THEOREM.md',
        'PERIOD_CUT_VALIDITY.md','GLOBAL_INJECTION.md','UNIFORM_R_INTERFACE.md','CASE_LEDGER.md',
        'INDEPENDENT_AUDIT.md','ADVERSARIAL_AUDIT.md','FINAL_VERDICT.md','CHECKPOINT.md','RESIDUAL_SLOT_THEOREM.md','IAGS_PROGRESS.md']
    assert all((B/n).is_file() for n in needed)
    assert not (B/'FULL_PROOF.md').exists()
    gates=read('completion_gates.json');assert gates['status']=='NOT_ALL_CLOSED_NO_OUTCOME_A'
    assert gates['gates']['J9']['status']=='OPEN'
    assert 'UNRESOLVED' in (B/'FINAL_VERDICT.md').read_text()
    assert 'U-OPEN' in (B/'UNIFORM_R_INTERFACE.md').read_text()
    entry=read('entry.json')
    def git(*a):return subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip()
    assert git('rev-parse','HEAD')==entry['head'] and git('branch','--show-current')==entry['branch']
    assert not git('status','--porcelain','--untracked-files=no')
    out('dependency_revalidation.json',{'status':'PASS','inherited_local_pins':len(pins['pins']),
        'external_pins':len(pins['external_pins']),'mismatches':bad})
    result={'status':'PASS_PARTIAL_RESEARCH_INTEGRITY_NO_STEP2_PROMOTION',
        'terminal_outcome':'UNRESOLVED_PROOF_LIMIT','CPU_exhausted':False,
        'branch':entry['branch'],'HEAD':entry['head'],'tracked_status':'','old_pins_verified':len(pins['pins']),
        'new_universal_results':['full_core6 physical funding','uniform residual-slot/fixed-owner partial exchange',
            'local comparison padding','deficiency-one source peel geometry'],
        'new_restricted_results':'six exact arbitrary-gap source families,78 physical full-demand assignments',
        'refuted_rule':'adjacent-full-packet spare-bit repair, not CD6',
        'global_missing':'source-derived distinct Wstar donors for every Pstar anchored root',
        'incomplete_auxiliary_base_interface':'do not conflate scalar lower-core CD5 with the core9 Step1 bank',
        'independent_checks':'new source/physical components only; no full map falsely audited',
        'failed_draft':'bridge hole/empty bug retained, superseded by2 and fully CPU charged',
        'R1_R4':'preserved','Bank25':25,'fixed_fE':'not modified','original_source_semantics':'unchanged',
        'Step2':'OPEN','CD6_full_scope':'OPEN','Gate_U':'U_OPEN','Step3':'OPEN','Universal_CD':'OPEN','Dynamic_Optimality':'OPEN',
        'source_engine_calls':0,'new_finite_tests':0}
    out('seal_audit.json',result);print(json.dumps(result),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_seal_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':0,'new_finite_tests':0})

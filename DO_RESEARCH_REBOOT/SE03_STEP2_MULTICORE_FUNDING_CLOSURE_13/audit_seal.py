"""Final PARTIAL proof/status, inherited-byte and resource integrity seal.
No formal proof-kernel or full multicore completion claim.
"""
import hashlib,json,subprocess,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
def read(n):return json.loads((B/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def git(*a):return subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip()
def main():
    e=read('entry.json');pins=read('dependency_pins.json')
    assert git('branch','--show-current')==e['branch'] and git('rev-parse','HEAD')==e['head']
    assert not git('status','--porcelain','--untracked-files=no')
    old=set(e['worktree_status'].splitlines());now=set(git('status','--porcelain','--untracked-files=all').splitlines())
    assert old<=now and all(v.startswith('?? DO_RESEARCH_REBOOT/SE03_STEP2_MULTICORE_FUNDING_CLOSURE_13/') for v in now-old)
    for v in pins['pins']:assert sha(ROOT/v['path'])==v['sha256'],v['path']
    for v in pins['external_pins']:assert sha(Path(v['path']))==v['sha256'],v['path']
    assert not list(B.rglob('__pycache__')) and not (B/'FULL_PROOF.md').exists()
    required=['SOURCE_SPEC','MULTICORE_SOURCE_CLASSIFICATION','PREDECESSOR_SUPPLY_THEOREM','MULTISLOT_INJECTIVITY',
        'MULTICORE_OWNER_EXCHANGE','CORE7_FULL_FUNDING','CORE8_FULL_FUNDING','CORE9_FULL_FUNDING','CORE10_FULL_FUNDING',
        'CORE11_FULL_FUNDING','CROSS_CORE_INTERFACE','MULTICORE_INJECTION','UNIFORM_R_TRANSFER','CASE_LEDGER',
        'SOURCE_REPLAY','INDEPENDENT_AUDIT','ADVERSARIAL_AUDIT','FINAL_VERDICT','CHECKPOINT','PARTIAL_PROOF','SOURCE_PROVENANCE']
    assert all((B/(n+'.md')).is_file() for n in required)
    phases=[];CPU=e['prior_uniform_CPU'];groups=dict(e['inherited_group_CPU']);queries=0
    for file in B.glob('run_*_result.json'):
        r=json.loads(file.read_text());c=read('controller_'+r['phase']+'_exit.json')
        assert r['status']=='PASS' and not c['error'] and not read('audit_'+r['phase']+'_exit.json')['error']
        charge=r['child_CPU']+c['whole_process_CPU_seconds'];CPU+=charge;groups[r['group']]+=charge
        assert r['source_engine_calls']<2000000;queries+=r['source_engine_calls'];phases.append(r['phase'])
    assert {'core7','seal7','bf8','core8','bf9','bf10','bf11','refinement','count_witnesses','cheapA','h2_release',
        'A6_independent','A6_source','h2_basis','paired_release','packet_completion','packet_verify','controls'}<=set(phases)
    for name in ('core7_seal.json','core8_seal.json','core9_A6_seal.json'):
        s=read(name)
        for f in s['files']:assert sha(B/f['path'])==f['sha256'],(name,f['path'])
    assert read('core7_seal.json')['status']=='CORE7_PHYSICAL_FUNDING_COMPLETE'
    c8=read('core8_seal.json');assert c8['status']=='CORE8_PHYSICAL_FUNDING_COMPLETE'
    assert [c8['states_independently_generated'],c8['edges_independently_generated'],c8['max_debt']]==[6562,24292,1]
    assert read('core9_A6_source_certificate.json')['reachability_proved_by_explicit_original_prefix']
    count=read('slot_count_witnesses.json');assert len(count['reports'])==6
    for report in count['reports']:
        assert report['exact_physical_slot_count']==1 and len(report['all_six_genuine_keys'])==6
        runs=[r for r in report['erased_runs'] if r['L']==1];assert len(runs)==6
        for r in runs:
            assert len(r['R'])==1
            assert r['rows'][-1]['after']==r['rows'][0]['before']
    expected={9:(78,160,158,-2,162),10:(150,320,302,-2,338),11:(58,120,120,-4,120)}
    for r in read('bf_source_refinement.json')['reports']:
        n,A,Q,w,margin=expected[r['core']]
        assert (r['genuine_macros'],r['A'],r['QF'],r['BF_only_price'],r['actual_signed_margin'])==(n,A,Q,w,margin)
        assert len(r['all_six_genuine_KEEP_keys'])==6 and 2*A-Q==margin and w<0 and margin>=0
        assert r['auxiliary']['closed']
    paired=read('core11_A6_packet_audit.json')
    assert paired['LOW_rows_with_multiplicity']==340002 and paired['HIGH_hyperedges']==4920 and paired['actual_q5_q1_sectors']==62
    assert paired['H2_basis_exactly_identical_across_kernels'] and paired['D_range']==[0,3]
    status=read('research_status_ledger.json');gates=read('completion_gates.json')
    assert status['terminal_outcome']=='UNRESOLVED_MATHEMATICAL_PROOF_LIMIT' and not status['resource_exhaustion']
    assert all(status[k]=='OPEN' for k in ('Step2','CD6','Step3','Universal_CD','Dynamic_Optimality'))
    assert gates['no_Outcome_A_or_E_claim'] and gates['gates']['U13']=='U-B'
    hist=read('historical_replay_summary.json');assert hist['old_period_rows']==1856 and hist['old12_two_slot_source_reports']==48
    gamma=read('historical10_gamma_period_ownership_audit.json');assert [gamma[k] for k in ('A','QF','QE','D12','D13')]==[34,30,24,0,2]
    assert 12 not in gamma['actual_maximum_cut_candidates_not_splitting_blocks']
    assert CPU+time.process_time()<7195 and all(groups[g]+(time.process_time() if g=='independent' else 0)<e['group_caps'][g] for g in groups)
    out('dependency_revalidation.json',{'status':'ALL_PRIOR_BYTES_AND_WORKTREE_PRESERVED','pins':len(pins['pins']),
        'external_directives':len(pins['external_pins']),'branch':e['branch'],'HEAD':e['head'],'tracked_status':'','new_paths_only':'Campaign13'})
    out('seal_audit.json',{'status':'PASS_PARTIAL_SCOPE_AND_SOURCE_INTEGRITY','terminal_outcome':'UNRESOLVED_MATHEMATICAL_PROOF_LIMIT',
        'core7':'SEALED_COMPLETE','core8':'SEALED_COMPLETE','core9':'RESTRICTED_ONLY','core10':'OPEN','core11':'OPEN',
        'Gate_U13':'U-B','complete_count_range':'all nonnegative integers at7..11','cross_full_core_boundaries':'source-excluded',
        'dependencies_verified':len(pins['pins']),'all_accepted_phases':sorted(phases),'queries_before_final_seal':queries,
        'CPU_before_current_seal':CPU,'groups_before_current_seal':groups,
        'remaining_mathematical_gap':'anonymous marked-core A boundary ancestor lifting with signed H1/H2 preservation and original donors',
        'Step2':'OPEN','CD6':'OPEN','Step3':'OPEN','proof_limit_not_resource_exhaustion':True,
        'trust':'same-agent different kernels; integrity/scope seal, not formal or external proof certification'})
    print(json.dumps({'status':'PARTIAL_SEAL_PASS','outcome':'UNRESOLVED','pins':len(pins['pins']),'core7_8':'COMPLETE','queries':queries}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_seal_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':0})

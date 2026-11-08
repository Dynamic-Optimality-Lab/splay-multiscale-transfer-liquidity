import json,subprocess
from pathlib import Path
from entry import BASE,sha

def read(p):return json.loads(p.read_text())
def write(p,v):
    with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    assert not(BASE/'final_manifest.json').exists();run=read(BASE/'run_result.json');done=run['completed_signatures'];N=len(done)
    targets=read(BASE/'targets.json')['canonical_signatures'];assert done==targets[:N]
    assert run['status'] in ('ALL360_TOTAL4_MULTI_FINITE_CERTIFICATES_PASS','STOPPED_ON_FIRST_FAILURE') and N>0
    source=read(BASE/'source_audit.json');assert source['status']=='POPULATION4_ORIGINAL_SOURCE_AND_FULL_CLOSURE_PASS'
    assert source['completed_canonical_signatures']==done and source['CPU_seconds']<300 and source['new_helper_controls']<=8 and source['full_closed_mixed_cycles']<=6
    combined=read(BASE/'combination_check.json');assert combined['status']=='COMBINED_COVERED_DOMAIN_AUDIT_PASS_FULL_M3_OPEN' and combined['production_predicates_replayed']==0
    covered=combined['new_total4_signatures'];new=len(covered);fixed=sum(s==list(reversed(s)) for s in done)
    assert new==2*N-fixed==source['new_original_signatures'] and combined['total4_vectors_remaining']==705-new
    audits=[];builds=[];constructs=[]
    for sig in done:
        folder=BASE/('s'+''.join(map(str,sig)));a=read(folder/'audit.json');d=read(folder/'build_status.json');c=read(folder/'construction.json')
        assert a['status']=='INDEPENDENT_RISK_PREFIX_AND_RESIDUAL_PASS' and d['status']=='COMPLETE_RISK_GUARDED_PREFIX_RELATION_UNAUDITED' and c['status']=='CONSTRUCTED_UNAUDITED'
        assert a['potential_sha256']==sha(folder/'potential.json')==read(folder/'metadata.json')['potential_sha256']
        assert a['canonical_transition_queries']==d['queries']<=1000000 and a['access_options']==d['option_count']<5000000 and a['minimum_residual']>=0
        assert a['cpu_seconds']<a['allocated_CPU_cap']<=120 and d['cpu_seconds']<d['allocated_CPU_cap']<=120 and c['cpu_seconds']<c['allocated_CPU_cap']<=300
        assert d['peak_DP_records']<2000000 and c['peak_conservative_resident_records']<2000000
        audits.append(a);builds.append(d);constructs.append(c)
    resource=read(BASE/'resource_accounting.json');assert resource['status']=='CPU_LEDGER_RECONCILED_PASS'
    effective=resource['conservative_cumulative_CPU_charge'];extra=resource['additional_unreported_failed_process_CPU_seconds']
    assert run['prior_accounted_CPU_seconds']==4495.056 and effective<7200
    deps=[]
    for name in ('M3_POP3_RISK01/certificate.json','M3_POP3_RISK01/final_manifest.json','M3_POP3_RISK01/REPRESENTATION_PROOF.md',
      'M3_POP3_RISK01/SOURCE_LIFT.md','M3_POP3_RISK01/representation_audit.json','M3_POP3_RISK01/risk_selector.json',
      'M3_POP3_01/SOURCE_PROOF.md','M3_POP3_ALL01/SOURCE_PROOF.md','M3_UNITPAIR01/B_bank.json','M3_UNITPAIR_FIN01/certificate.json',
      'M3_TWOGAP_AUD01/final_manifest.json','M3_TWOGAP_AUD01/reference.py','M3_COMB_AUD01/COMBINED_CERTIFICATE.json','M3_OUT01/proof_certificate.json'):
        p=BASE.parent/name;deps.append({'path':p.as_posix(),'sha256':sha(p)})
    write(BASE/'reused_dependencies.json',{'old_original_roots_replayed':0,'old_finite_matrices_regenerated':0,'selector_and_word_proofs_reused':True,'dependencies':deps})
    print(json.dumps({'new_canonical_audit_reports_pass':N,'new_signature_vectors':new,'checking_old_file_integrity':True}),flush=True)
    baseline=read(BASE/'entry_baseline.json');old={r['path'] for r in baseline['files']}
    for i,r in enumerate(baseline['files']):
        assert Path(r['path']).is_file() and sha(Path(r['path']))==r['sha256'],r['path']
        if (i+1)%500==0:print(json.dumps({'old_files_verified':i+1,'total':len(old)}),flush=True)
    assert not[p for p in Path('DO_RESEARCH_REBOOT').rglob('*') if p.is_file() and BASE not in p.parents and p.as_posix() not in old]
    assert not subprocess.check_output(['git','status','--short','--untracked-files=no'],text=True)
    assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==baseline['head']
    integrity={'status':'PASS','old_files_unchanged':len(old),'head':baseline['head'],'tracked_tree_clean':True,'writes_confined_here':True}
    write(BASE/'integrity.json',integrity)
    per=BASE/'certificates';per.mkdir(exist_ok=False)
    for sig,a in zip(done,audits):
        folder=BASE/('s'+''.join(map(str,sig)))
        for s in sorted({tuple(sig),tuple(reversed(sig))}):
            record={'status':'PROVED_RESTRICTED_DOMAIN','sigma':s,'canonical_sigma':sig,'reflected':s!=tuple(sig),'self_reflecting':sig==list(reversed(sig)),
              'independent_full_canonical_audit':(folder/'audit.json').as_posix(),'potential_sha256':a['potential_sha256'],'legal_masks':126,
              'J_range':[-2,0],'finite_walk_lower_bound':-7,'closed_mixed_walk_lower_bound':0,'complete_original_closure':'147 O / same actual127 M',
              'source_lift':'SOURCE_LIFT.md and pinned inherited generic proofs','new_source_audit':'source_audit.json',
              'reflection_rule':'exact low-image/selector/bank transfer only for nonfixed pairs; fixed sigma uses full direct table without J invariance',
              'R1_R4_preserved':True,'h0_correction_preserved':True,'new_observables':0,'full_M3_proved':False}
            write(per/('s'+''.join(map(str,s))+'.json'),record)
    full=new==705
    result={'status':'PROVED_RESTRICTED_DOMAIN_ALL705_TOTAL4_MULTI_SIGNATURES' if full else 'PROVED_RESTRICTED_DOMAIN_PARTIAL_TOTAL4_MULTI_SIGNATURES',
      'campaign_status':run['status'],'new_canonical_certificates':N,'new_original_signatures':new,'self_reflecting_certificates':fixed,
      'new_mask_signature_sectors':126*new,'total4_vectors_covered':10+new,'total4_vectors_remaining':705-new,
      'prior_all_total3_reused':True,'combined_signature_vectors':2916+new,'combined_mask_signature_sectors':126*(2916+new),
      'canonical_transition_queries':sum(a['canonical_transition_queries'] for a in audits),'private_assignment_visits':sum(a['private_assignment_visits'] for a in audits),
      'independent_root_production_visits':sum(a['independent_root_productions'] for a in audits),'analytic_productions_rejected':sum(a['analytic_root_productions_rejected'] for a in audits),
      'finite_access_options':sum(a['access_options'] for a in audits),'independent_explicit_residuals':sum(a['explicit_residuals'] for a in audits),'minimum_residual':min(a['minimum_residual'] for a in audits),
      'maximum_canonical_queries_per_phase':max(a['canonical_transition_queries'] for a in audits),'maximum_live_DP_records':max(d['peak_DP_records'] for d in builds),
      'maximum_construction_records':max(c['peak_conservative_resident_records'] for c in constructs),
      'new_finite_CPU_seconds_including_cap':round(run['new_finite_CPU_seconds']+extra,6),'failed_phase_process_CPU_charged':extra,'prior_accounted_CPU_seconds':4495.056,'cumulative_extension_CPU_seconds':effective,
      'source_CPU_seconds':source['CPU_seconds'],'new_original_roots':source['unique_original_roots'],'new_full_state_mixed_cycles':source['full_closed_mixed_cycles'],
      'middle_of_three_helpers_and_same_actual_zeroKEEP':source['middle_of_three_gap0_and_gap9'] and source['middle_DELETE_zeroKEEP_same_actual_node'],
      'production_DAG_nodes':source['DAG_nodes'],'all_legal_masks':126,'uniform_finite_walk_lower_bound':-7,'closed_mixed_walk_lower_bound':0,
      'completed_source_checks_repeated':0,'completed_finite_matrices_repeated':0,'selector_proof_repeated':False,'R1_R4_preserved':True,'h0_correction_preserved':True,
      'Bank25':25,'T':266,'alpha_depth':2,'caps_increased':False,'failed_phase_split_or_restarted':False,
      'full_M3_proved':False,'Stage04_started':False,'negative_original_cycle_certified':False,'failure':run['failure'],'integrity':integrity}
    result['resource_accounting']=resource
    write(BASE/'certificate.json',result)
    lines=['# Population-four guarded campaign','',
      '**PROVED - RESTRICTED DOMAIN:** '+str(new)+' NEW total-four multi-support signatures, '+str(126*new)+' new mask/signature sectors.',
      str(N)+' independently regenerated canonical tables, including'+str(fixed)+' self-reflecting sectors; all126 masks and both realizable regions.',
      'Every original fully closed mixed walk in this domain has weight>=0; finite walks>=-7.','',
      'The smaller signed representation, B bank, word shapes, high/h0 laws and generic terminal-debt proofs are reused BY HASH.',
      'SOURCE_LIFT.md proves the population4 budget induction. n3 fits are NOT used to infer n4 signs.',
      'No private branch or original vertex is removed; analytic fibers obey w-DeltaJ>=w+psi(Bt)-2>=0.',
      'For fixed reflected sigma the FULL direct relation is audited; no J mirror invariance is imposed.','',
      'Independent audit:'+str(result['canonical_transition_queries'])+' canonical word profiles, '+str(result['finite_access_options'])+' options, '+str(result['independent_explicit_residuals'])+' explicit integer residuals, minimum'+str(result['minimum_residual'])+'.',
      'The independent ordered-key/address-identity checker does not import the DP. Internal private grammar visits are disclosed separately and do not execute words/read endpoints.',
      'Original source:'+str(source['unique_original_roots'])+' new roots, '+str(source['full_closed_mixed_cycles'])+' full147-O/same127-M mixed cycles.',
      'New controls include a helper strictly between two other same-gap keys, reflected gap9 and charged DELETE/zeroKEEP at the SAME actual middle key.',
      'Executed finite versions:run_v2.py,prefix_dp_v2.py,construct_v2.py,audit_v2.py. No old matrix, source-root or selector proof rerun.','',
      'Maximum successful query count:'+str(result['maximum_canonical_queries_per_phase'])+'<=1m; DP records:'+str(result['maximum_live_DP_records'])+'<2m; construction:'+str(result['maximum_construction_records'])+'<2m.',
      'Per-phase CPU caps remain120/300/120; near the carried global ceiling deadlines are only tightened. All DAG/edge/memory/12h caps unchanged.',
      'New finite CPU:'+str(round(run['new_finite_CPU_seconds']+extra,6))+'s; prior:'+str(run['prior_accounted_CPU_seconds'])+'s; total:'+str(effective)+'s<7200. Source:'+str(source['CPU_seconds'])+'s<300.',
      'Integrity:all'+str(len(old))+' old files unchanged; clean tracked tree, unchanged HEAD, all new writes confined here.','',
      '**Proof ledger:** BEFORE10/715 total4 vectors certified (the single-support cases). RESULT '+str(new)+' new multi-support vectors; AFTER '+str(10+new)+'/715, '+str(705-new)+' still open.',
      'All total3 results are reused. Combined bank:'+str(2916+new)+' vectors/'+str(126*(2916+new))+' mask sectors. No new premises or observables.',
      'Campaign status:'+run['status']+'. First failure:'+json.dumps(run['failure'])+'.',
      'Any UNKNOWN/cap is retained without a theorem or negative-cycle promotion. No later signature is tried after that boundary.',
      '**Full M3 remains OPEN.** R1-R4, h0, depth2,T266,Bank25=25, two sorts/actual shared midpoint/full closure preserved. No Stage04 or Dynamic Optimality claim.']
    with (BASE/'RESULT.md').open('x',encoding='utf-8') as f:f.write(chr(10).join(lines)+chr(10))
    result['files']=[{'path':p.as_posix(),'sha256':sha(p)} for p in sorted(BASE.rglob('*')) if p.is_file()]
    write(BASE/'final_manifest.json',result)
    print(json.dumps({k:v for k,v in result.items() if k!='files'},indent=2),flush=True)
if __name__=='__main__':main()

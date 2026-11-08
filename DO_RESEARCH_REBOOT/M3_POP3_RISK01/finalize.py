"""Combine independent new audits with inherited source theorems; no reruns."""
import json,subprocess
from pathlib import Path
from entry import BASE,sha

def read(p):return json.loads(p.read_text())
def write(p,v):
    with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)

def main():
    out=BASE/'final_manifest.json';assert not out.exists()
    run=read(BASE/'run_result.json');targets=read(BASE/'targets.json')['canonical_signatures'];done=run['completed_signatures'];N=len(done)
    assert done==targets[:N] and run['status'] in ('ALL97_REMAINING_TOTAL3_FINITE_CERTIFICATES_PASS','STOPPED_ON_FIRST_FAILURE')
    full=run['status']=='ALL97_REMAINING_TOTAL3_FINITE_CERTIFICATES_PASS';assert not full or N==97
    reduction=read(BASE/'representation_audit.json');assert reduction['status']=='PROVED_COMPLETE_SIGNED_REDUCTION_AND_INDEPENDENT_SELECTOR_AUDIT_PASS' and reduction['cpu_seconds']<120
    source=read(BASE/'source_audit.json');assert source['status']=='RISK_GUARDED_ORIGINAL_SOURCE_AND_FULL_CLOSURE_PASS'
    assert source['completed_canonical_signatures']==done and source['new_original_signatures']==2*N and source['CPU_seconds']<300
    combined=read(BASE/'combination_check.json');assert combined['status']=='COMBINED_COVERED_DOMAIN_AUDIT_PASS_FULL_M3_OPEN'
    assert combined['total3_remaining']==194-2*N and combined['new_signature_count']==2*N and combined['production_predicates_replayed']==0
    assert source['previous_source_checks_repeated']==0 and source['new_helper_controls']<=8 and source['full_closed_mixed_cycles']<=6
    audits=[];builds=[];constructs=[];files=[]
    for sig in done:
        folder=BASE/('s'+''.join(map(str,sig)));a=read(folder/'audit.json');c=read(folder/'construction.json');d=read(folder/'build_status.json')
        assert a['status']=='INDEPENDENT_RISK_PREFIX_AND_RESIDUAL_PASS' and c['status']=='CONSTRUCTED_UNAUDITED' and d['status']=='COMPLETE_RISK_GUARDED_PREFIX_RELATION_UNAUDITED'
        assert a['potential_sha256']==sha(folder/'potential.json') and a['canonical_transition_queries']==d['queries']<=1000000
        assert a['access_options']==d['option_count']<5000000 and a['minimum_residual']>=0
        assert a['cpu_seconds']<120 and d['cpu_seconds']<120 and c['cpu_seconds']<300
        assert d['peak_DP_records']<2000000 and c['peak_conservative_resident_records']<2000000
        assert read(folder/'metadata.json')['potential_sha256']==a['potential_sha256']
        audits.append(a);builds.append(d);constructs.append(c)
    costs=sum(r['cpu_seconds'] for rows in (audits,builds,constructs) for r in rows)
    assert run['accounted_CPU_seconds']<7200 and run['prior_accounted_CPU_seconds']==90.172
    if full:assert abs(costs-run['new_finite_CPU_seconds'])<0.01
    dependencies=[]
    for p in ('M3_POP3_ALL01/final_manifest.json','M3_POP3_ALL01/certificate_partial.json','M3_POP3_ALL01/SOURCE_PROOF.md',
      'M3_POP3_01/certificate.json','M3_POP3_01/SOURCE_PROOF.md','M3_POP3_01/ISOLATED_STATE_EXTENSION.md','M3_UNITPAIR_FIN01/certificate.json',
      'M3_UNITPAIR01/B_bank.json','M3_UNITPAIR01/SOURCE_PROOF.md','M3_TWOGAP_AUD01/final_manifest.json','M3_TWOGAP_AUD01/reference.py',
      'M3_COMB_AUD01/COMBINED_CERTIFICATE.json','M3_OUT01/proof_certificate.json'):
        path=BASE.parent/p;dependencies.append({'path':path.as_posix(),'sha256':sha(path)})
    assert next(v['sha256'] for v in dependencies if v['path'].endswith('B_bank.json'))==reduction['bank_sha256']
    write(BASE/'reused_dependencies.json',{'completed_original_roots_replayed':0,'completed_finite_matrices_regenerated':0,'dependencies':dependencies})
    print(json.dumps({'all_new_audit_reports_and_hashes_pass':N,'checking_old_file_integrity':True}),flush=True)
    baseline=read(BASE/'entry_baseline.json');old={r['path'] for r in baseline['files']}
    for i,r in enumerate(baseline['files']):
        assert Path(r['path']).is_file() and sha(Path(r['path']))==r['sha256'],r['path']
        if (i+1)%500==0:print(json.dumps({'old_files_verified':i+1,'total':len(old)}),flush=True)
    assert not [p for p in Path('DO_RESEARCH_REBOOT').rglob('*') if p.is_file() and BASE not in p.parents and p.as_posix() not in old]
    assert not subprocess.check_output(['git','status','--short','--untracked-files=no'],text=True)
    assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==baseline['head']
    integrity={'status':'PASS','old_files_unchanged':len(old),'head':baseline['head'],'tracked_tree_clean':True,'writes_confined_here':True}
    write(BASE/'integrity.json',integrity)
    per=BASE/'certificates';per.mkdir(exist_ok=False)
    for sig,a in zip(done,audits):
        folder=BASE/('s'+''.join(map(str,sig)))
        for s in (sig,list(reversed(sig))):
            r={'status':'PROVED_RESTRICTED_DOMAIN','sigma':s,'legal_masks':126,'both_regions_where_realizable':True,
              'canonical_sigma':sig,'reflected':s!=sig,'independent_canonical_audit':(folder/'audit.json').as_posix(),
              'potential_sha256':a['potential_sha256'],'canonical_transition_queries':a['canonical_transition_queries'],'explicit_residuals':a['explicit_residuals'],
              'minimum_residual':a['minimum_residual'],'analytic_reduction':'REPRESENTATION_PROOF.md and representation_audit.json',
              'source_coverage':'SOURCE_LIFT.md and inherited pinned source proofs','new_source_audit':'source_audit.json',
              'reflection_if_used':'exact source-image, selector and pinned bank equivariance; no second full matrix replay',
              'J_range':[-2,0],'closed_mixed_walk_lower_bound':0,'finite_walk_lower_bound':-7,'full_original_closure':'147 O / same actual127 M',
              'new_observables':0,'R1_R4_preserved':True,'h0_correction_preserved':True,'full_M3_proved':False}
            write(per/('s'+''.join(map(str,s))+'.json'),r)
    result={'status':'PROVED_RESTRICTED_DOMAIN_ALL194_REMAINING_TOTAL3_SIGNATURES' if full else 'PROVED_RESTRICTED_DOMAIN_PARTIAL_TOTAL3_GUARDED_CAMPAIGN',
      'campaign_status':run['status'],'representation_status':reduction['status'],'new_canonical_certificates':N,'new_original_signatures':2*N,
      'new_mask_signature_sectors':252*N,'remaining_total3_signatures':194-2*N,'all_total3_vectors_covered':full,
      'combined_signature_vectors':2722+2*N,'combined_mask_signature_sectors':(2722+2*N)*126,'total3_vectors_covered':26+2*N,
      'canonical_transition_queries':sum(a['canonical_transition_queries'] for a in audits),'private_assignment_visits':sum(a['private_assignment_visits'] for a in audits),
      'independent_root_production_visits':sum(a['independent_root_productions'] for a in audits),
      'analytic_private_root_productions_rejected':sum(a['analytic_root_productions_rejected'] for a in audits),
      'finite_access_options':sum(a['access_options'] for a in audits),'independent_explicit_residuals':sum(a['explicit_residuals'] for a in audits),
      'minimum_residual':min(a['minimum_residual'] for a in audits),'maximum_canonical_queries_per_phase':max(a['canonical_transition_queries'] for a in audits),
      'maximum_live_DP_records':max(d['peak_DP_records'] for d in builds),'maximum_construction_records':max(c['peak_conservative_resident_records'] for c in constructs),
      'new_finite_CPU_seconds_including_any_cap':run['new_finite_CPU_seconds'],'prior_CPU_seconds_charged':90.172,'combined_extension_finite_CPU_seconds':run['accounted_CPU_seconds'],
      'source_CPU_seconds':source['CPU_seconds'],'representation_CPU_seconds':reduction['cpu_seconds'],'new_original_roots':source['unique_original_roots'],
      'new_full_state_mixed_cycles':source['full_closed_mixed_cycles'],'production_DAG_nodes':source['DAG_nodes'],
      'all_legal_masks':126,'uniform_finite_walk_lower_bound':-7,'closed_mixed_walk_lower_bound':0,'J_range':[-2,0],
      'completed_source_checks_repeated':0,'completed_finite_matrices_repeated':0,'R1_R4_preserved':True,'h0_correction_preserved':True,
      'Bank25':25,'T':266,'alpha_depth':2,'caps_increased':False,'failed_wide_phase_replayed_or_split':False,
      'larger_multi_support_populations_still_open':True,'remaining_hard_branch':('support>=2,total>=4,NH>=1,DL>2NH+PL' if full else 'remaining total3 or total>=4 with support>=2,NH>=1,DL>2NH+PL'),
      'full_M3_proved':False,'Stage04_started':False,'negative_original_cycle_certified':False,'failure':run['failure'],'integrity':integrity}
    write(BASE/'certificate.json',result)
    lines=['# Guarded total-three campaign','',
      '**PROVED - RESTRICTED DOMAIN:** '+str(2*N)+' new total-three signatures, '+str(252*N)+' new mask/signature sectors.',
      'All126 masks and both chi8 regions where realizable; original fully closed mixed walks have weight>=0, finite walks>=-7.','',
      '**Smaller complete signed representation proved first.** For J in[-2,0] below -psi,',
      '`w-J(t)+J(s)>=w+psi(Bt)-2`. A whole root/terminal/helper fiber with minimum margin>=2 is analytic; empty fibers are impossible.',
      'The grammar emits only the remaining fibers before any word-transition query. No private branch, original vertex, state coordinate or closure requirement is discarded.',
      'The independently audited selector retains70 H1 pairs and49 pairs per outer direction and checks78 symbolic source-address word shapes.',
      'Internal grammar-production visits are disclosed separately and do not execute source words or read endpoint shadows.','',
      '**Independent certificate audits:** '+str(N)+' newly regenerated canonical tables plus exact reflected source-image/selector/bank transfer,',
      str(result['canonical_transition_queries'])+' canonical profiles; '+str(result['finite_access_options'])+' options; '+str(result['independent_explicit_residuals'])+' explicit integer residuals, minimum'+str(result['minimum_residual'])+'.',
      'Every retained option and analytic omission is covered. The independent ordered-key/address-identity checker does not import the DP.',
      'Per-signature records in certificates/ disclose all audit hashes and reflection dependencies. SOURCE_LIFT.md supplies universal source coverage; finite samples alone are not its proof.','',
      'New original-source audit: '+str(source['unique_original_roots'])+' roots, '+str(source['full_closed_mixed_cycles'])+' full147-O/same127-M closed mixed cycles; all q/weights and scopes original.',
      'Completed old roots/matrices rerun:0. The h0 correction, universal HIGH law, both outer kernels, repeated-key and Gamma0 normal forms are reused by pinned hashes.','',
      'Each enumeration/audit<120 CPU s and construction<300, <=1m actual canonical transition queries; live states<2m, edges<5m, DAG<4m. Existing12h and7200-extension caps retained.',
      'Maximum query count:'+str(result['maximum_canonical_queries_per_phase'])+'; DP records:'+str(result['maximum_live_DP_records'])+'; construction records:'+str(result['maximum_construction_records'])+'.',
      'New finite CPU:'+str(run['new_finite_CPU_seconds'])+'s; extension including prior capped run:'+str(run['accounted_CPU_seconds'])+'s; source:'+str(source['CPU_seconds'])+'s; representation:'+str(reduction['cpu_seconds'])+'s.',
      'Integrity: all'+str(len(old))+' old files unchanged, clean tracked tree and unchanged HEAD. All new writes confined here.','',
      '**Proof ledger:** BEFORE26/220 total3 vectors certified. RESULT '+str(2*N)+' newly certified; AFTER '+str(26+2*N)+'/220, '+str(194-2*N)+' remain.',
      'Combined bank:'+str(2722+2*N)+' vectors / '+str((2722+2*N)*126)+' mask sectors. No new premises or observables.','',
      '**Full M3 remains OPEN.** Larger multi-support populations remain unresolved. '+('All populations<=3 are now covered.' if full else 'This campaign stopped at the first failure; its exact status is retained below.'),
      'R1-R4, h0, depth2,T266,Bank25=25, original two sorts/actual midpoint/full closure preserved. No Stage04, Dynamic Optimality or negative-cycle promotion.',
      'Campaign status: '+run['status']+'. Failure: '+json.dumps(run['failure'])+'.']
    with (BASE/'RESULT.md').open('x',encoding='utf-8') as f:f.write('\n'.join(lines)+'\n')
    result['files']=[{'path':p.as_posix(),'sha256':sha(p)} for p in sorted(BASE.rglob('*')) if p.is_file()]
    write(out,result)
    print(json.dumps({k:v for k,v in result.items() if k!='files'},indent=2),flush=True)
if __name__=='__main__':main()

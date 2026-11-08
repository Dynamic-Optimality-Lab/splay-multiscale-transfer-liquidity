"""Finalize passed pair and historical cap; no predicate or matrix reruns."""
import json,subprocess
from pathlib import Path
from entry import BASE,sha

def read(p):return json.loads(p.read_text())
def write(name,data):
    with (BASE/name).open('x',encoding='utf-8') as f:json.dump(data,f,indent=2)

def main():
    assert not (BASE/'final_manifest.json').exists()
    run=read(BASE/'run_result.json');assert run['status']=='STOPPED_ON_FIRST_FAILURE' and len(run['completed_signatures'])==1
    sig=run['completed_signatures'][0];folder=BASE/('s'+''.join(map(str,sig)))
    a=read(folder/'audit.json');c=read(folder/'construction.json');build=read(folder/'build_status.json')
    assert a['status']=='INDEPENDENT_POPULATION_PREFIX_AND_RESIDUAL_PASS' and c['status']=='CONSTRUCTED_UNAUDITED'
    assert build['status']=='COMPLETE_POPULATION_PREFIX_RELATION_UNAUDITED'
    assert a['potential_sha256']==sha(folder/'potential.json') and a['canonical_transition_queries']==build['queries']<1000000
    assert a['access_options']==build['option_count']<5000000 and a['minimum_residual']==0
    assert a['cpu_seconds']<120 and build['cpu_seconds']<120 and c['cpu_seconds']<300
    assert build['peak_DP_records']<2000000 and c['peak_conservative_resident_records']<2000000
    cap=read(BASE/'s1100000001/build_status.json');assert cap['status']=='UNKNOWN_CAP' and cap['reason']=='canonical source-query cap'
    assert cap['queries']==943672 and not (BASE/'s1100000001/relation.json').exists()
    assert not (BASE/'s1100000001/construction.json').exists() and not (BASE/'s1100000001/potential.json').exists()
    assert len([p for p in BASE.iterdir() if p.is_dir() and p.name.startswith('s')])==2
    source=read(BASE/'source_audit_partial.json');assert source['status']=='NEW_BOTH_OUTER_TOTAL3_SOURCE_AND_FULL_CLOSURE_PASS'
    assert source['unique_original_roots']==10 and source['full_closed_mixed_cycles']==2 and source['CPU_seconds']<300
    comb=read(BASE/'combination_check_partial.json');assert comb['total3_remaining']==194 and comb['new_signature_count']==2 and comb['production_predicates_replayed']==0
    assert read(BASE/'semantic_attributes_partial.json')['status']=='SAVED_NEW_SOURCE_ATTRIBUTES_PASS'
    # Reuse the saved successful attribute checks from finalize_partial.py.
    dependencies=[]
    for path in ('M3_POP3_01/certificate.json','M3_POP3_01/final_manifest.json','M3_POP3_01/SOURCE_PROOF.md','M3_POP3_01/ISOLATED_STATE_EXTENSION.md',
      'M3_UNITPAIR_FIN01/certificate.json','M3_UNITPAIR01/B_bank.json','M3_UNITPAIR01/SOURCE_PROOF.md','M3_TWOGAP_AUD01/final_manifest.json',
      'M3_TWOGAP_AUD01/reference.py','M3_COMB_AUD01/COMBINED_CERTIFICATE.json','M3_OUT01/proof_certificate.json'):
        p=BASE.parent/path;dependencies.append({'path':p.as_posix(),'sha256':sha(p)})
    write('reused_dependencies.json',{'completed_source_checks_repeated':0,'completed_finite_matrices_regenerated':0,'dependencies':dependencies,
      'scope':'previous results reused at their exact restricted/universal status; no broader promotion'})
    print('New certificate and source attributes passed; checking old-file integrity.',flush=True)
    baseline=read(BASE/'entry_baseline.json');old={r['path'] for r in baseline['files']}
    for i,r in enumerate(baseline['files']):
        assert Path(r['path']).is_file() and sha(Path(r['path']))==r['sha256'],r['path']
        if (i+1)%500==0:print(json.dumps({'old_files_verified':i+1,'total':len(old)}),flush=True)
    assert not [p for p in Path('DO_RESEARCH_REBOOT').rglob('*') if p.is_file() and BASE not in p.parents and p.as_posix() not in old]
    assert not subprocess.check_output(['git','status','--short','--untracked-files=no'],text=True)
    assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==baseline['head']
    integrity={'status':'PASS','old_files_unchanged':len(old),'head':baseline['head'],'tracked_tree_clean':True,'writes_confined_here':True}
    write('integrity.json',integrity)
    per=BASE/'certificates';per.mkdir(exist_ok=False)
    for s in comb['new_certified_signatures']:
        record={'status':'PROVED_RESTRICTED_DOMAIN','sigma':s,'legal_masks':126,'independent_audit':(folder/'audit.json').as_posix(),
          'potential_sha256':a['potential_sha256'],'reflected':s!=sig,'reflection_dependency':'PARTIAL_SOURCE_THEOREM.md and reused independent B-bank/source-image equivariance',
          'new_source_audit':'source_audit_partial.json','full_state_closure':'147 O / same actual127 M','closed_walk_lower_bound':0,'finite_walk_lower_bound':-7,
          'outside_chi8_only':True,'sharper_incident_finite_walk_lower_bound':-2,'new_state_observables':0,'full_M3_proved':False}
        with (per/('s'+''.join(map(str,s))+'.json')).open('x') as f:json.dump(record,f,indent=2)
    result={'status':'PROVED_RESTRICTED_DOMAIN_2_TOTAL3_BOTH_OUTER_SIGNATURES','campaign_status':'OPEN_STOPPED_ON_REGISTERED_QUERY_CAP',
      'requested_new_signatures':196,'new_certified_signatures':comb['new_certified_signatures'],'new_signature_count':2,'new_mask_signature_sectors':252,
      'remaining_requested_signatures':194,'other_unstarted_canonical_tables':96,'capped_canonical_signature':cap['sigma'],'capped_queries_completed':cap['queries'],
      'canonical_transition_queries':a['canonical_transition_queries'],'private_assignment_visits':a['private_assignment_visits'],
      'finite_access_options':a['access_options'],'independent_explicit_residuals':a['explicit_residuals'],'minimum_residual':0,
      'potential_sha256':a['potential_sha256'],'J_range':[-2,0],'closed_mixed_walk_lower_bound':0,'finite_walk_lower_bound':-7,
      'incident_outside_only_finite_walk_lower_bound':-2,'maximum_DP_records':max(build['peak_DP_records'],cap['peak_DP_records']),
      'maximum_construction_records':c['peak_conservative_resident_records'],'finite_CPU_seconds_including_cap':run['accounted_CPU_seconds'],
      'source_CPU_seconds':source['CPU_seconds'],'original_source_roots':10,'new_fully_closed_mixed_cycles':2,'production_DAG_nodes':source['DAG_nodes'],
      'previous_completed_source_checks_repeated':0,'previous_completed_finite_matrices_regenerated':0,
      'combined_signature_vectors':2722,'combined_mask_signature_sectors':342972,'total3_vectors_covered':26,'total3_vectors_remaining':194,
      'larger_multi_support_populations_still_open':True,'R1_R4_preserved':True,'h0_correction_retained':True,'Bank25':25,
      'caps_increased':False,'capped_phase_split_or_restarted':False,'full_M3_proved':False,'negative_original_cycle_certified':False,
      'remaining_branch':'uncovered total3 or total>=4 with support>=2, NH>=1 and DL>2NH+PL','integrity':integrity}
    write('certificate_partial.json',result)
    result['files']=[{'path':p.as_posix(),'sha256':sha(p)} for p in sorted(BASE.rglob('*')) if p.is_file()]
    write('final_manifest.json',result)
    print(json.dumps({k:v for k,v in result.items() if k!='files'},indent=2),flush=True)
if __name__=='__main__':main()

"""Publish only independently complete finite/source total-five certificates."""
import json,subprocess
from pathlib import Path
from entry import BASE,sha
def read(p):return json.loads(p.read_text())
def write(p,v):
    with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    out=BASE/'final_manifest.json';assert not out.exists()
    run=read(BASE/'run_result.json');cert=read(BASE/'certification_run.json');comb=read(BASE/'combination_check.json');plan=read(BASE/'targets.json');targets=plan['canonical_signatures'];done=cert['source_certified_signatures'];N=len(done)
    assert done==targets[:N] and run['completed_signatures']==targets[:len(run['completed_signatures'])]
    assert comb['status']=='TOTAL5_COMBINED_COVERAGE_AUDIT_PASS_FULL_M3_OPEN'
    new=comb['new_signature_count'];assert new==2*N and not any(s==s[::-1] for s in done)
    assert comb['total4_vectors_covered']==715 and comb['total5_multi_vectors_remaining']==1992-new and comb['total5_multi_vectors_covered']==new
    assert run['cumulative_finite_CPU_charged']<=7200 and run['prior_current_finite_CPU_retained']==4055.96875
    assert abs(run['additional_finite_CPU_charged']+4055.96875-run['cumulative_finite_CPU_charged'])<1e-8
    assert run['completed_old_phases_replayed']==run['completed_old_audits_replayed']==0
    caps={'prefix_dp':120,'construct':300,'audit':300}
    for e in run['phase_events']:
        assert e['CPU_cap']<=caps[e['phase']]
        folder=BASE/('s'+''.join(map(str,e['sigma'])));ex=read(folder/(e['phase']+'_exit.json'))
        assert e['CPU_charged']==ex['whole_process_CPU_seconds']
    audits=[];builds=[];constructs=[]
    for sig in done:
        folder=BASE/('s'+''.join(map(str,sig)));a=read(folder/'audit.json');d=read(folder/'build_status.json');c=read(folder/'construction.json')
        assert a['status']=='INDEPENDENT_RISK_PREFIX_AND_RESIDUAL_PASS' and d['status']=='COMPLETE_RISK_GUARDED_PREFIX_RELATION_UNAUDITED' and c['status']=='CONSTRUCTED_UNAUDITED'
        assert a['potential_sha256']==sha(folder/'potential.json')==read(folder/'metadata.json')['potential_sha256']
        assert a['canonical_transition_queries']==d['queries']<=2000000 and a['access_options']==d['option_count']<5000000 and a['minimum_residual']>=0
        assert a['cpu_seconds']<a['allocated_CPU_cap']<=300 and d['cpu_seconds']<d['allocated_CPU_cap']<=120 and c['cpu_seconds']<c['allocated_CPU_cap']<=300
        assert d['peak_DP_records']<2000000 and c['peak_conservative_resident_records']<2000000
        assert read(folder/'audit_exit.json')['error'] is None
        audits.append(a);builds.append(d);constructs.append(c)
    sources=[];rootfiles=[]
    for batch in cert['source_batches']:
        r=read(Path(batch['report']));assert r['status']=='TOTAL5_SOURCE_BATCH_PASS' and r['CPU_seconds']<300
        assert r['new_helper_controls']<=4 and r['full_closed_mixed_cycles']<=4 and r['previous_source_checks_repeated']==0
        assert r['all147_O_coordinates'] and r['same_actual127_M'] and all(n<4000000 for n in r['DAG_nodes'])
        assert read(BASE/('source_batch_'+str(batch['batch_index']).zfill(3)+'_exit.json'))['error'] is None
        i=batch['batch_index'];assert r['completed_canonical_signatures']==plan['source_batches'][i][:len(r['completed_canonical_signatures'])]
        sources.append(r);folder=Path(batch['report']).parent;rootfiles.extend((folder/name).as_posix() for name in r['root_files'])
    assert len(sources)<=20 and sum(len(r['completed_canonical_signatures']) for r in sources)==N
    assert [s for r in sources for s in r['completed_canonical_signatures']]==done
    assert len(rootfiles)==len(set(rootfiles))==sum(r['unique_original_roots'] for r in sources)
    change=read(BASE/'implementation_change_audit.json')
    for r in change['files']:
        old=BASE.parent/'M3_POP4_RISK07'/r['file'];current=BASE/r['file']
        assert sha(old)==r['source_sha256'] and sha(current)==r['new_sha256']
        text=current.read_text()
        for a,b in reversed(r['exact_replacements']):text=text.replace(b,a)
        assert text==old.read_text()
    dependencies=[]
    names=[f'M3_POP4_RISK0{i}/{name}' for i in range(1,8) for name in ('certificate.json','final_manifest.json','combination_check.json','SOURCE_LIFT.md')]
    names+=['M3_POP4_RISK07/TOTAL4_THEOREM.md','M3_POP4_RISK07/GUARD_PRESERVATION.md','M3_POP4_RISK07/AUDIT_CAP_PRESERVATION.md','M3_POP4_RISK01/REPRESENTATION_PROOF.md','M3_POP3_RISK01/REPRESENTATION_PROOF.md','M3_POP3_RISK01/representation_audit.json','M3_POP3_RISK01/risk_selector.json','M3_POP3_RISK01/certificate.json','M3_UNITPAIR01/B_bank.json','M3_UNITPAIR_FIN01/certificate.json','M3_TWOGAP_AUD01/final_manifest.json','M3_COMB_AUD01/COMBINED_CERTIFICATE.json','M3_OUT01/proof_certificate.json']
    for name in names:
        p=BASE.parent/name;dependencies.append({'path':p.as_posix(),'sha256':sha(p)})
    write(BASE/'reused_dependencies.json',{'completed_old_source_queries_replayed':0,'completed_old_finite_matrices_regenerated':0,'complete_old_phases_replayed':0,'query_cap_preserved':2000000,'CPU_caps_preserved':[120,300,300],'source_CPU_cap_preserved':300,'dependencies':dependencies})
    print(json.dumps({'source_complete_new_canonical_tables':N,'new_signature_vectors':new,'checking_old_file_integrity':True}),flush=True)
    baseline=read(BASE/'entry_baseline.json');old={r['path'] for r in baseline['files']}
    for i,r in enumerate(baseline['files']):
        assert Path(r['path']).is_file() and sha(Path(r['path']))==r['sha256'],r['path']
        if (i+1)%500==0:print(json.dumps({'old_files_verified':i+1,'total':len(old)}),flush=True)
    additions=[p for p in Path('DO_RESEARCH_REBOOT').rglob('*') if p.is_file() and BASE not in p.parents and p.as_posix() not in old]
    assert all(p.as_posix().startswith('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/') for p in additions)
    write(BASE/'concurrent_additions.json',{'not_mathematical_dependencies':True,'files':[{'path':p.as_posix(),'sha256':sha(p)} for p in additions]})
    assert not subprocess.check_output(['git','status','--short','--untracked-files=no'],text=True)
    assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==baseline['head']
    integrity={'status':'PASS','old_files_unchanged':len(old),'head':baseline['head'],'tracked_tree_clean':True,'writes_confined_here':True,'write_claim_scope':'this campaign only','concurrent_U4_additions':len(additions)}
    write(BASE/'integrity.json',integrity)
    per=BASE/'certificates';per.mkdir(exist_ok=False)
    for sig,a in zip(done,audits):
        folder=BASE/('s'+''.join(map(str,sig)))
        for actual in (tuple(sig),tuple(sig[::-1])):
            r={'status':'PROVED_RESTRICTED_DOMAIN','sigma':actual,'canonical_sigma':sig,'self_reflecting':False,'reflected':actual!=tuple(sig),'independent_full_canonical_audit':(folder/'audit.json').as_posix(),'potential_sha256':a['potential_sha256'],'source_scope':'SOURCE_LIFT.md and pinned original-source lemmas','new_source_audit_workflow':'certification_run.json','reflection_rule':'nonfixed actual LOW-image/selector/bank transfer','all_legal_masks':126,'J_range':[-2,0],'finite_walk_lower_bound':-7,'closed_mixed_walk_lower_bound':0,'full_original_closure':'147 O / same actual127 M','R1_R4_preserved':True,'h0_correction_preserved':True,'full_M3_proved':False}
            write(per/('s'+''.join(map(str,actual))+'.json'),r)
    bysupport={str(k):sum(sum(n>0 for n in s)==k for s in comb['new_certified_signatures']) for k in (2,3,4,5)}
    result={'status':'PROVED_RESTRICTED_DOMAIN_TOTAL5_PREFIX' if new else 'NO_NEW_TOTAL5_CERTIFICATE_OPEN','finite_campaign_status':run['status'],'source_workflow_status':cert['status'],'new_canonical_certificates':N,'new_original_signatures':new,'new_signature_count_by_support_size':bysupport,'new_mask_signature_sectors':126*new,'total4_vectors_covered':715,'total5_multi_vectors_covered':new,'total5_multi_vectors_remaining':1992-new,'total5_vectors_covered_including_old_singles':10+new,'combined_signature_vectors':3621+new,'combined_mask_signature_sectors':126*(3621+new),'canonical_queries_independently_audited':sum(a['canonical_transition_queries'] for a in audits),'explicit_integer_residuals':sum(a['explicit_residuals'] for a in audits),'minimum_residual':min((a['minimum_residual'] for a in audits),default=None),'maximum_queries_per_phase':max((a['canonical_transition_queries'] for a in audits),default=0),'maximum_DP_records':max((d['peak_DP_records'] for d in builds),default=0),'maximum_construction_records':max((c['peak_conservative_resident_records'] for c in constructs),default=0),'finite_CPU_ceiling':7200,'prior_finite_CPU_retained':4055.96875,'additional_finite_CPU_charged':run['additional_finite_CPU_charged'],'cumulative_whole_process_finite_CPU_charged':run['cumulative_finite_CPU_charged'],'complete_old_phases_repeated':0,'complete_old_audits_replayed':0,'source_batches_passed':len(sources),'new_original_source_roots':sum(r['unique_original_roots'] for r in sources),'new_full_state_mixed_cycles':sum(r['full_closed_mixed_cycles'] for r in sources),'source_CPU_seconds':sum(r['CPU_seconds'] for r in sources),'source_per_phase_CPU_cap':300,'uniform_finite_walk_bound':-7,'closed_mixed_walk_bound':0,'R1_R4_preserved':True,'CPU_caps_preserved':[120,300,300],'query_cap_preserved':2000000,'other_caps_unchanged':True,'h0_correction_preserved':True,'Bank25':25,'T':266,'alpha_depth':2,'new_observables':0,'failure':run['failure'],'source_failure':cert['failure'],'finite_only_unpromoted_signatures':cert['finite_only_signatures'],'full_M3_proved':False,'Stage04_started':False,'negative_original_cycle_certified':False,'integrity':integrity}
    def span(s):
        occupied=[i for i,n in enumerate(s) if n]
        return occupied[-1]-occupied[0]
    result['all_total5_multi_support_span_at_most_two_covered']=not any(span(s)<=2 for s in comb['unresolved_total5_multi_signatures'])
    result['new_certified_signatures_by_span']={str(k):sum(span(s)==k for s in comb['new_certified_signatures']) for k in range(1,10)}
    result['stop_details']=read(BASE/'STOP_NOTE.json')
    write(BASE/'certificate.json',result)
    canonical_left=[s for s in targets if s not in done]
    write(BASE/'remaining_sectors.json',{'total5_multi_covered':new,'total5_multi_unresolved':1992-new,'remaining_reflection_representatives':len(canonical_left),'canonical_signatures':canonical_left,'remaining_original_signatures':comb['unresolved_total5_multi_signatures'],'first_new_failure':run['failure'],'finite_only_unpromoted_signatures':cert['finite_only_signatures'],'full_M3_proved':False,'old_mathematical_checks_or_source_predicates_replayed':0})
    failure=run['failure'];why='none' if failure is None else f"sigma={failure['sigma']}, phase={failure['phase']}, status={failure['status']}, reason={failure.get('reason')}, error={failure.get('error')}"
    lines=['# Total-five multi-support campaign','',f'**{result["status"]}:** {new} new original signatures from {N} complete independent canonical audits plus source lifting. {1992-new}/1992 total-five multi-support signatures remain. The ten total-five singles and all715 total-four sectors were already certified and remain unchanged.','',
      'SOURCE_LIFT.md specializes the generic budget-consuming source induction to total5. This extends coverage; it does not extrapolate feasibility from total4. The DP, independent ordered-key/source-address enumeration, integer residual assertions, original predicates and resource guards are unchanged. Path/scope/label differences are exactly recorded in implementation_change_audit.json.',
      'All promoted vectors are reflection pairs. Odd total5 precludes self-reflecting ten-gap signatures. The reflection lift acts on the actual LOW image and reuses pinned selector/kernel/debt equivariance. Every private count/bill branch, literal-slot0 G read, current-child observation and unfolded F identity remains included. Only finite-audited AND source-complete sectors enter the public decoder.','',
      f'Independent checks: {result["explicit_integer_residuals"]:,} exact residuals, minimum {result["minimum_residual"]}; {result["canonical_queries_independently_audited"]:,} canonical profiles. Maximum successful queries {result["maximum_queries_per_phase"]:,}; DP records {result["maximum_DP_records"]:,}; construction records {result["maximum_construction_records"]:,}.',
      f'New original-source validation: {result["new_original_source_roots"]} roots, {result["new_full_state_mixed_cycles"]} full147-O/same-actual127-M closed mixed cycles, {len(sources)} complete pre-registered source phases, {result["source_CPU_seconds"]} computation CPU seconds. No old source root or completed finite matrix/audit was replayed.','',
      'For each newly certified sector J lies in[-2,0] and J<=-psi. Set W(O)=J-5chi8,W(M)=-5chi8; each original leg has w>=DeltaW. Telescoping gives original fully closed mixed walks>=0 and finite walks>=-7. All126 legal masks and both regions wherever realizable are covered. Sigma is conserved on original edges, so the old and new certificates combine without changing original state identity or shared midpoint.',
      f'New signatures by support size: {json.dumps(bysupport)}. Combined bank: {3621+new} signatures/{126*(3621+new)} mask sectors.','',
      f'CPU ledger: prior4055.96875 retained; additional {run["additional_finite_CPU_charged"]}; cumulative {run["cumulative_finite_CPU_charged"]}/7200. No allowance reset or cap increase. Whole child-process/finally CPU and parent metadata CPU are charged. Source keeps its separate per-phase300-second cap.',
      'Current caps preserved: enumeration120/construction300/independent-audit300 CPU seconds;2m canonical queries;2m live records;4m DAG nodes;5m edges;32GiB; inherited12h ceiling. Source phases of at most50 canonical cases were fixed upfront, each300 seconds/max4 cycles/max4 helpers; no failed phase was split/retried.',
      f'First new finite stop: {why}. Source failure: {json.dumps(cert["failure"])}. A cap/UNKNOWN proves no mathematical contradiction. A range-template obstruction in the superrelation would not certify an original negative cycle. No failed or source-incomplete sector is promoted.',
      f'R1-R4, original q/weights/two sorts/private scopes/full closure and corrected h0 preserved. {len(old)} pinned prior files unchanged; HEAD/tracked tree unchanged. Concurrent U4 additions are recorded separately, not M3 evidence.','',
      f'Proof ledger: BEFORE0/1992 total-five multi-support sectors; RESULT{new} new source-complete sectors; AFTER{new}/1992. New mathematical assumptions/observables:0. Unpromoted finite-only cases:{json.dumps(cert["finite_only_signatures"])}.',
      '**Full M3 remains OPEN.** Unpromoted total-five and larger multi-support totals remain unresolved. No Stage04 or Dynamic Optimality claim. Certificates use exact independent computation and the written source lift, not proof-assistant formalization.']
    lines.insert(-1,'Complete-boundary check: all total-five multi-support signatures with occupied-gap span at most2 covered = '+str(result['all_total5_multi_support_span_at_most_two_covered'])+'. New signatures by span: '+json.dumps(result['new_certified_signatures_by_span'])+'.')
    lines.insert(-1,'Aggregate CPU stop: the next case4e3+e6 had complete enumeration/construction saved (342,348 queries). Its new audit received only3.5625 CPU seconds from the remaining balance, rather than a full300-second allocation. It remains UNKNOWN, with no audit certificate or mathematical refutation. The last persisted completed-family count is67,380; the exact partial count is not invented. No later finite case or failed-phase retry was run. See STOP_NOTE.json and the four saved input hashes for future continuation.')
    with (BASE/'RESULT.md').open('x',encoding='utf-8') as f:f.write('\n'.join(lines)+'\n')
    result['files']=[{'path':p.as_posix(),'sha256':sha(p)} for p in sorted(BASE.rglob('*')) if p.is_file()]
    write(out,result)
    print(json.dumps({k:v for k,v in result.items() if k not in ('files','failure','finite_only_unpromoted_signatures')},indent=2),flush=True)
if __name__=='__main__':main()

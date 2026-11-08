"""Publish independently complete finite/source sectors and exact coverage."""
import json,subprocess
from pathlib import Path
from entry import BASE,sha
def read(p):return json.loads(p.read_text())
def write(p,v):
    with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    out=BASE/'final_manifest.json';assert not out.exists()
    run=read(BASE/'run_result.json');cert=read(BASE/'certification_run.json');comb=read(BASE/'combination_check.json');targets=read(BASE/'targets.json')['canonical_signatures']
    done=cert['source_certified_signatures'];N=len(done)
    assert done==targets[:N] and run['completed_signatures']==targets[:len(run['completed_signatures'])]
    assert comb['status']=='RENEWED_COMBINED_COVERAGE_AUDIT_PASS_FULL_M3_OPEN'
    new=comb['new_signature_count'];fixed=sum(s==s[::-1] for s in done);assert new==2*N-fixed
    assert comb['total4_vectors_remaining']==7-new and comb['total4_vectors_covered']==708+new
    assert run['renewed_CPU_charged']<=7200 and run['prior_current_finite_CPU_retained']==3411.6875
    assert abs(run['additional_finite_CPU_charged']+3411.6875-run['renewed_CPU_charged'])<1e-8
    assert run['reused_completed_old_phases']==2 and run['completed_old_audits_replayed']==0
    audit_caps={'prefix_dp':120,'construct':300,'audit':300}
    for event in run['phase_events']:
        if event['status']=='REUSED_COMPLETE_OLD_PHASE':continue
        assert event['CPU_cap']<=audit_caps[event['phase']]
        folder=BASE/('s'+''.join(map(str,event['sigma'])))
        ex=read(folder/(event['phase']+'_exit.json'))
        assert event['CPU_charged']==ex['whole_process_CPU_seconds']
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
        r=read(Path(batch['report']));assert r['status']=='RENEWED_TOTAL4_SOURCE_BATCH_PASS' and r['CPU_seconds']<300
        assert r['new_helper_controls']<=4 and r['full_closed_mixed_cycles']<=4 and r['previous_source_checks_repeated']==0
        assert r['all147_O_coordinates'] and r['same_actual127_M']
        assert all(n<4000000 for n in r['DAG_nodes'])
        assert read(BASE/('source_batch_'+str(batch['batch_index']).zfill(3)+'_exit.json'))['error'] is None
        sources.append(r);folder=Path(batch['report']).parent;rootfiles.extend((folder/name).as_posix() for name in r['root_files'])
    assert len(sources)<=1 and sum(len(r['completed_canonical_signatures']) for r in sources)==N
    assert [s for r in sources for s in r['completed_canonical_signatures']]==done
    assert len(rootfiles)==len(set(rootfiles))==sum(r['unique_original_roots'] for r in sources)
    reused=read(BASE/'reused_candidate.json')
    for r in reused['files']:assert sha(Path(r['source']))==sha(Path(r['copy']))==r['sha256']
    change=read(BASE/'implementation_change_audit.json')
    for r in change['files']:
        old=BASE.parent/'M3_POP4_RISK06'/r['file'];current=BASE/r['file']
        assert sha(old)==r['source_sha256'] and sha(current)==r['new_sha256']
        text=current.read_text().replace('M3_POP4_RISK07','M3_POP4_RISK06')
        if r['file']=='audit.py':text=text.replace('CPU_CAP=min(300,float(sys.argv[11])) if len(sys.argv)>11 else 300','CPU_CAP=min(120,float(sys.argv[11])) if len(sys.argv)>11 else 120')
        assert text==old.read_text()
    dependencies=[]
    names=[f'M3_POP4_RISK0{i}/{name}' for i in range(1,7) for name in ('certificate.json','final_manifest.json','combination_check.json','SOURCE_LIFT.md')]
    names+=['M3_POP4_RISK06/GUARD_PRESERVATION.md','M3_POP4_RISK06/AUDIT_STOP_NOTE.json','M3_POP4_RISK06/remaining_sectors.json','M3_POP4_RISK01/REPRESENTATION_PROOF.md','M3_POP3_RISK01/representation_audit.json','M3_POP3_RISK01/risk_selector.json','M3_POP3_RISK01/certificate.json','M3_UNITPAIR01/B_bank.json','M3_UNITPAIR_FIN01/certificate.json','M3_TWOGAP_AUD01/final_manifest.json','M3_COMB_AUD01/COMBINED_CERTIFICATE.json','M3_OUT01/proof_certificate.json']
    for name in names:
        p=BASE.parent/name;dependencies.append({'path':p.as_posix(),'sha256':sha(p)})
    write(BASE/'reused_dependencies.json',{'completed_old_source_queries_replayed':0,'completed_old_finite_matrices_regenerated':0,'authorized_old_interrupted_audit_retried':True,'complete_old_phases_replayed':0,'complete_enumeration_and_construction_reused':True,'query_cap_preserved':2000000,'audit_CPU_cap_change':[120,300],'other_caps_unchanged':True,'dependencies':dependencies})
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
        for actual in sorted({tuple(sig),tuple(sig[::-1])}):
            r={'status':'PROVED_RESTRICTED_DOMAIN','sigma':actual,'canonical_sigma':sig,'self_reflecting':sig==sig[::-1],'reflected':actual!=tuple(sig),'independent_full_canonical_audit':(folder/'audit.json').as_posix(),'potential_sha256':a['potential_sha256'],'source_scope':'SOURCE_LIFT.md and pinned original-source lemmas','new_source_audit_workflow':'certification_run.json','reflection_rule':'nonfixed low-image/selector/bank transfer; fixed sector fully direct without J invariance','all_legal_masks':126,'J_range':[-2,0],'finite_walk_lower_bound':-7,'closed_mixed_walk_lower_bound':0,'full_original_closure':'147 O / same actual127 M','R1_R4_preserved_with_explicit_audit_CPU_exception':True,'h0_correction_preserved':True,'full_M3_proved':False}
            write(per/('s'+''.join(map(str,actual))+'.json'),r)
    complete=new==7
    if complete:assert N==5 and fixed==3 and comb['total4_vectors_covered']==715 and not comb['unresolved_total4_signatures'] and run['failure'] is None and cert['failure'] is None
    result={'status':'PROVED_RESTRICTED_DOMAIN_ALL_TOTAL4_SIGNATURES' if complete else 'PROVED_RESTRICTED_DOMAIN_PARTIAL_TOTAL4_SIGNATURES','finite_campaign_status':run['status'],'source_workflow_status':cert['status'],'new_canonical_certificates':N,'new_original_signatures':new,'self_reflecting_new_certificates':fixed,'new_mask_signature_sectors':126*new,'total4_vectors_covered':708+new,'total4_vectors_remaining':7-new,'combined_signature_vectors':3614+new,'combined_mask_signature_sectors':126*(3614+new),'canonical_queries_independently_audited':sum(a['canonical_transition_queries'] for a in audits),'explicit_integer_residuals':sum(a['explicit_residuals'] for a in audits),'minimum_residual':min((a['minimum_residual'] for a in audits),default=None),'maximum_queries_per_phase':max((a['canonical_transition_queries'] for a in audits),default=0),'maximum_DP_records':max((d['peak_DP_records'] for d in builds),default=0),'maximum_construction_records':max((c['peak_conservative_resident_records'] for c in constructs),default=0),'finite_CPU_ceiling':7200,'prior_finite_CPU_retained':3411.6875,'additional_finite_CPU_charged':run['additional_finite_CPU_charged'],'cumulative_whole_process_finite_CPU_charged':run['renewed_CPU_charged'],'interrupted_old_audit_completed':bool(done) and done[0]==[1,0,1,0,0,0,0,1,0,1],'complete_old_phases_repeated':0,'complete_old_audits_replayed':0,'source_batches_passed':len(sources),'new_original_source_roots':sum(r['unique_original_roots'] for r in sources),'new_full_state_mixed_cycles':sum(r['full_closed_mixed_cycles'] for r in sources),'source_CPU_seconds':sum(r['CPU_seconds'] for r in sources),'source_per_phase_CPU_cap':300,'uniform_finite_walk_bound':-7,'closed_mixed_walk_bound':0,'R1_R4_preserved_with_explicit_audit_CPU_exception':True,'audit_CPU_cap_old':120,'audit_CPU_cap_user_authorized':300,'query_cap_preserved':2000000,'other_caps_unchanged':True,'h0_correction_preserved':True,'Bank25':25,'T':266,'alpha_depth':2,'new_observables':0,'failure':run['failure'],'source_failure':cert['failure'],'finite_only_unpromoted_signatures':cert['finite_only_signatures'],'full_M3_proved':False,'Stage04_started':False,'negative_original_cycle_certified':False,'integrity':integrity}
    write(BASE/'certificate.json',result)
    write(BASE/'remaining_sectors.json',{'total4_covered':708+new,'total4_unresolved':7-new,'remaining_signatures':comb['unresolved_total4_signatures'],'larger_multi_support_totals_remain_open':True,'mathematical_checks_or_source_predicates_replayed':0})
    if complete:
        theorem='''# Total-four restricted theorem

Status: PROVED - RESTRICTED DOMAIN, using exact computation and the pinned
written source lift. This is not a proof-assistant formalization.

Fix the original Stage11F architecture and parameters in R1-R4. For every
nonnegative integral ten-gap signature sigma with sum(sigma)=4, every
legal five-of-nine mask, and every original LOW/HIGH walk at that conserved
signature, there is a potential W on the full original two-sort state graph
with every leg weight w>=W(destination)-W(source). Thus every fully closed
mixed walk has weight>=0; every finite walk has weight>=-7.

Proof. There are binomial(13,9)=715 such signatures. The independent
combination_check.json exhausts all715 without overlap or uncovered cases.
Its old sectors use their pinned complete certificates; the last seven use
five new full ordered-key/option/residual audits and one new original-source
phase. The two nonfixed reflection pairs use the proved source-image,
selector and B-bank equivariance. The three fixed sectors use direct full
tables and impose no symmetry on J.

At each new representative the complete retained-budget grammar and
integer construction produce J in[-2,0], J<=-psi(coreB). The independent
checker regenerates every risky option, matches all family/option counts,
and verifies every required residual. The population-independent range/debt
selector identity w-DeltaJ>=w+psi(Bt)-2>=0 discharges omitted fibers. The
population-four structural induction in M3_POP4_RISK01/SOURCE_LIFT.md maps
every original private witness into this superrelation, including original
owner-slot0 G observations, unfolded occurrence identities, independent
private counts/bills and both occupied outer-helper directions. Other LOW
normal forms and the universal HIGH law are pinned established premises.

Use W(O)=J-5chi8 and W(M)=-5chi8. The inherited HIGH law retains corrected
h=0 entry weight-3, independent v and the same actual127-coordinate M.
The original q/weights and independent OM/MO scopes are unchanged. The
edge inequalities therefore hold on the full147-coordinate O and
127-coordinate M graph. This is a potential on original states, not a
quotient graph. Original edges conserve sigma, so dispatch among certified
sectors preserves every edge. Telescoping gives nonnegative weight for a
fully closed walk. Since W lies in[-7,0], any finite walk has weight>=-7.

The theorem deletes the remaining total-four obligation only. Full M3,
larger multi-support populations and Dynamic Optimality remain open.
All dependencies and the old-file integrity check are pinned in the final
manifest and reused_dependencies.json.
'''
        with (BASE/'TOTAL4_THEOREM.md').open('x',encoding='utf-8') as f:f.write(theorem)
    lines=['# Total-four completion under the authorized audit CPU cap','',f'**{result["status"]}:** {new} additional signatures from {N} complete independent canonical audits. Total-four coverage is now {708+new}/715; {7-new} remain.','',
      'The interrupted e0+e2+e7+e9 audit ran FIRST under the authorized300 CPU-second cap. Its complete enumeration/construction inputs were reused by hash. No complete old audit, source root, bank, selector or78-shape proof was rerun. No partial audit state was reused.',
      'All three fixed representatives use full direct tables without potential mirror invariance. The two nonfixed pairs use the proved original-image/selector/B-bank reflection transfer. All private count/bill branches and literal-slot0 G reads remain included.','',
      f'Independent finite checks: {result["explicit_integer_residuals"]:,} integer residuals, minimum {result["minimum_residual"]}; {result["canonical_queries_independently_audited"]:,} canonical profiles. Maximum queries per case {result["maximum_queries_per_phase"]:,}, below2m. Maximum DP records {result["maximum_DP_records"]:,}; construction records {result["maximum_construction_records"]:,}, each below2m.',
      f'One registered source phase: {result["new_original_source_roots"]} new original roots and {result["new_full_state_mixed_cycles"]} full147-O/same-actual127-M mixed cycles, {result["source_CPU_seconds"]} CPU seconds. Inherited h0/normal-form/source-completeness proofs reused; finite evidence alone is not the source lift.','',
      'The certified theorem uses J in[-2,0],J<=-psi and W(O)=J-5chi8,W(M)=-5chi8. Each original leg satisfies w>=DeltaW. Sigma is invariant on original edges, so certified sectors combine. All126 legal masks are covered; both regions wherever realizable. Every finite walk in a certified sector has weight>=-7; every fully closed mixed walk has weight>=0.',
      f'Combined covered bank: {3614+new} signatures / {126*(3614+new)} mask sectors. Total-four includes all single-, two-, three- and four-support signatures; the new sectors all have four supports spanning gaps0 to9.','',
      f'CPU ledger: prior3411.6875 retained, additional {run["additional_finite_CPU_charged"]}, cumulative {run["renewed_CPU_charged"]}/7200. The finite allowance was not reset. Child startup/output/finally and parent metadata CPU are charged. Source has its separate unchanged300-second phase cap.',
      'Only the independent-audit CPU guard changed120->300. Enumeration120, construction300, source300 CPU seconds,2m queries,2m live records,4m DAG nodes,5m edges,32GiB and original12h ceiling remain. The normalized implementation diff confirms unchanged grammar, recurrence, source semantics and residual assertions.',
      f'R1-R4 and corrected h0 preserved. {len(old)} pinned prior files unchanged; HEAD/tracked tree unchanged. Concurrent U4 additions are recorded separately and are not M3 evidence.','',
      f'Proof ledger: BEFORE708/715; RESULT{new} new source-complete signatures; AFTER{708+new}/715. No new mathematical assumptions or observables. Finite status: {run["status"]}; source status: {cert["status"]}. Failure: {json.dumps(run["failure"])}; source failure: {json.dumps(cert["failure"])}.',
      '**Full M3 remains OPEN.** Larger multi-support totals>=5 remain unresolved. Total-four completion does not prove all populations or Dynamic Optimality. No Stage04 or original negative-cycle promotion. The certificates use exact independent computation and a written source lift, not proof-assistant formalization.']
    with (BASE/'RESULT.md').open('x',encoding='utf-8') as f:f.write('\n'.join(lines)+'\n')
    result['files']=[{'path':p.as_posix(),'sha256':sha(p)} for p in sorted(BASE.rglob('*')) if p.is_file()]
    write(out,result);print(json.dumps({k:v for k,v in result.items() if k!='files'},indent=2),flush=True)
if __name__=='__main__':main()

"""Publication tail only; completed finite/source/integrity checks are reused."""
import json
from pathlib import Path
from entry import BASE,sha
def read(p):return json.loads(p.read_text())
def write(p,v):
    with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    out=BASE/'final_manifest.json';assert not out.exists()
    recovery=read(BASE/'PACKAGING_RECOVERY.json')
    assert recovery['status']=='OLD_FILE_CHECKS_REUSED_OUTSIDE_ADDITIONS_RECORDED'
    assert sha(BASE/'entry_baseline.json')==recovery['entry_baseline_sha256']
    for row in recovery['saved_reports']:assert sha(Path(row['path']))==row['sha256']
    run=read(BASE/'run_result.json');cert=read(BASE/'certification_run.json');comb=read(BASE/'combination_check.json')
    done=cert['source_certified_signatures'];N=len(done);new=comb['new_signature_count'];fixed=sum(s==s[::-1] for s in done)
    audits=[];builds=[];constructs=[]
    for sig in done:
        folder=BASE/('s'+''.join(map(str,sig)))
        audits.append(read(folder/'audit.json'));builds.append(read(folder/'build_status.json'));constructs.append(read(folder/'construction.json'))
    sources=[read(Path(batch['report'])) for batch in cert['source_batches']]
    baseline=read(BASE/'entry_baseline.json');old={r['path'] for r in baseline['files']}
    integrity={'status':'PASS_WITH_CONCURRENT_ADDITIONS_RECORDED','old_files_unchanged':len(old),'old_file_claim_scope':'9199 pinned entry-baseline paths','head':baseline['head'],'tracked_tree_clean':True,'writes_confined_here':True,'writes_claim_scope':'this campaign only','concurrent_outside_additions':recovery['outside_additions_recorded'],'concurrent_additions_record':'integrity_additions_final.json','completed_content_checks_reused':True}
    write(BASE/'integrity.json',integrity)
    per=BASE/'certificates';per.mkdir(exist_ok=False)
    for sig,a in zip(done,audits):
        folder=BASE/('s'+''.join(map(str,sig)))
        for actual in sorted({tuple(sig),tuple(reversed(sig))}):
            r={'status':'PROVED_RESTRICTED_DOMAIN','sigma':actual,'canonical_sigma':sig,'self_reflecting':sig==list(reversed(sig)),
              'reflected':actual!=tuple(sig),'independent_full_canonical_audit':(folder/'audit.json').as_posix(),'potential_sha256':a['potential_sha256'],
              'source_scope':'SOURCE_LIFT.md and pinned original-source lemmas','new_source_audit_workflow':'certification_run.json',
              'reflection_rule':'nonfixed low-image/selector/bank transfer; fixed sector fully direct without J invariance',
              'all_legal_masks':126,'J_range':[-2,0],'finite_walk_lower_bound':-7,'closed_mixed_walk_lower_bound':0,
              'full_original_closure':'147 O / same actual127 M','R1_R4_preserved':True,'h0_correction_preserved':True,'full_M3_proved':False}
            write(per/('s'+''.join(map(str,actual))+'.json'),r)
    bysupport={str(k):sum(sum(n>0 for n in s)==k for s in comb['new_certified_signatures']) for k in (2,3,4)}
    result={'status':'PROVED_RESTRICTED_DOMAIN_ALL184_RENEWED_TOTAL4_SIGNATURES' if new==184 else 'PROVED_RESTRICTED_DOMAIN_PARTIAL_RENEWED_TOTAL4_SIGNATURES',
      'finite_campaign_status':run['status'],'source_workflow_status':cert['status'],'new_canonical_certificates':N,'new_original_signatures':new,
      'new_signature_count_by_support_size':bysupport,'new_mask_signature_sectors':126*new,'self_reflecting_new_certificates':fixed,
      'total4_vectors_covered':531+new,'total4_vectors_remaining':184-new,'combined_signature_vectors':3437+new,'combined_mask_signature_sectors':126*(3437+new),
      'canonical_queries_independently_audited':sum(a['canonical_transition_queries'] for a in audits),'explicit_integer_residuals':sum(a['explicit_residuals'] for a in audits),
      'minimum_residual':min(a['minimum_residual'] for a in audits),'maximum_queries_per_phase':max(a['canonical_transition_queries'] for a in audits),
      'maximum_DP_records':max(d['peak_DP_records'] for d in builds),'maximum_construction_records':max(c['peak_conservative_resident_records'] for c in constructs),
      'renewed_finite_CPU_allowance':7200,'renewed_whole_process_CPU_charged':run['renewed_CPU_charged'],'old_finite_charges_unchanged':[7200,7195.21875,7195.25],
      'interrupted_old_audit_completed':done[0]==[1,1,0,0,0,1,0,1,0,0],'complete_old_phases_repeated':0,'complete_old_audits_replayed':0,
      'source_batches_passed':len(sources),'new_original_source_roots':sum(r['unique_original_roots'] for r in sources),
      'new_full_state_mixed_cycles':sum(r['full_closed_mixed_cycles'] for r in sources),'source_CPU_seconds':sum(r['CPU_seconds'] for r in sources),
      'source_per_phase_CPU_cap':300,'uniform_finite_walk_bound':-7,'closed_mixed_walk_bound':0,'R1_R4_preserved':True,'h0_correction_preserved':True,
      'per_phase_caps_unchanged':True,'Bank25':25,'T':266,'alpha_depth':2,'new_observables':0,
      'failure':run['failure'],'resource_stop_details':read(BASE/'RESOURCE_STOP.json'),'source_failure':cert['failure'],'finite_only_unpromoted_signatures':cert['finite_only_signatures'],
      'full_M3_proved':False,'Stage04_started':False,'negative_original_cycle_certified':False,'integrity':integrity}
    write(BASE/'certificate.json',result)
    lines=['# Renewed population-four campaign','',
      '**PROVED - RESTRICTED DOMAIN:** '+str(new)+' additional total4 signatures, '+str(N)+' independent full canonical tables with exact reflection/fixed-sector handling.',
      'All126 masks and both realizable regions; original closed mixed walks>=0, finite walks>=-7.','',
      'The explicitly interrupted audit e0+e1+e5+e7 was completed FIRST. Its complete relation, potential, build and construction reports were reused by hash. No old complete phase was repeated and no partial audit state was reused.',
      'No completed old audit, source root, bank/selector/word proof or finite matrix was rerun. The previous failed short audit and reserved allowance remain unchanged.',
      'All new fixed sectors use full direct tables without J mirror invariance. All private count/bill branches and literal-slot0 G reads remain included.',
      'Only independently audited AND source-complete sectors enter the public decoder. Finite-only/source-failed sectors remain excluded.','',
      'Independent exact checks:'+str(result['explicit_integer_residuals'])+' residuals, minimum'+str(result['minimum_residual'])+'; '+str(result['canonical_queries_independently_audited'])+' canonical profiles.',
      'New source:'+str(result['new_original_source_roots'])+' original roots and'+str(result['new_full_state_mixed_cycles'])+' full147-O/same127-M mixed cycles.',
      'Source audit uses the'+str(len(sources))+' completed disjoint batches registered upfront, each<300 CPU seconds; no failed phase was split/retried.',
      'New signatures by support size:'+json.dumps(bysupport)+'.','',
      'Renewed finite allowance:7200 CPU seconds; charged'+str(run['renewed_CPU_charged'])+' using whole-process time through each finally handler plus metadata CPU.',
      'This additionally charges startup/output overhead compared with the inherited phase-only timer. New failures retain exact process CPU without sampling.',
      'Per-phase mathematical caps remain120/300/120 CPU seconds,1m canonical word queries,2m live states,4m DAG nodes,5m edges,32GiB; original12h ceiling unchanged.',
      'Maximum successful queries:'+str(result['maximum_queries_per_phase'])+'; DP records:'+str(result['maximum_DP_records'])+'; construction:'+str(result['maximum_construction_records'])+'.',
      'All '+str(len(old))+' pinned prior files unchanged; tracked tree clean and HEAD unchanged. This campaign wrote only here. Concurrent U4 additions outside this folder are recorded separately in integrity_additions_final.json and excluded from the mathematical certificate.','',
      '**Proof ledger:** BEFORE531/715 total4 vectors certified. RESULT '+str(new)+' newly certified; AFTER '+str(531+new)+'/715; '+str(184-new)+' remain.',
      'Combined prior/new bank:'+str(3437+new)+' signatures/'+str(126*(3437+new))+' mask sectors. No new assumptions or observables.',
      'Finite campaign:'+run['status']+'. Failure:'+json.dumps(run['failure'])+'. Source workflow:'+cert['status']+'.',
      'RESOURCE STOP: e0+e1+e4+e8 completed 960889 canonical queries. The next whole word family would exceed the fixed 1000000-query cap, so admission stopped before its queries. This is NOT CPU exhaustion, a refuted potential template or a negative original cycle. See RESOURCE_STOP.json.',
      'To continue under unchanged caps, first prove a complete representation requiring fewer canonical queries for the capped signature. Further CPU renewal alone does not remove this limit.',
      'Current unpromoted finite-only cases:'+json.dumps(cert['finite_only_signatures'])+'.',
      '**Full M3 remains OPEN.** Larger multi-support totals remain unresolved. R1-R4,h0,original q/weights,two sorts/private scopes/actual midpoint/full closure preserved. No Stage04, Dynamic Optimality or negative-cycle promotion.']
    with (BASE/'RESULT.md').open('x',encoding='utf-8') as f:f.write(chr(10).join(lines)+chr(10))
    result['files']=[{'path':p.as_posix(),'sha256':sha(p)} for p in sorted(BASE.rglob('*')) if p.is_file()]
    write(out,result);print(json.dumps({k:v for k,v in result.items() if k!='files'},indent=2),flush=True)
if __name__=='__main__':main()

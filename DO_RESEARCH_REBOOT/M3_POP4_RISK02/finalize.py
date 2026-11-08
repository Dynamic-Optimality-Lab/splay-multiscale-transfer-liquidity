"""Publish only complete independent finite/source certificates; reuse prior evidence."""
import json,subprocess
from pathlib import Path
from entry import BASE,sha

def read(p):return json.loads(p.read_text())
def write(p,v):
    with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    out=BASE/'final_manifest.json';assert not out.exists();run=read(BASE/'run_result.json');cert=read(BASE/'certification_run.json');comb=read(BASE/'combination_check.json')
    done=cert['source_certified_signatures'];N=len(done);targets=read(BASE/'targets.json')['canonical_signatures']
    assert done==targets[:N] and run['completed_signatures']==targets[:len(run['completed_signatures'])] and N>0
    assert comb['status']=='RENEWED_COMBINED_COVERAGE_AUDIT_PASS_FULL_M3_OPEN'
    new=comb['new_signature_count'];fixed=sum(s==list(reversed(s)) for s in done);assert new==2*N-fixed
    assert comb['total4_vectors_remaining']==577-new and comb['total4_vectors_covered']==138+new
    assert run['renewed_CPU_charged']<=7200 and run['reused_completed_old_phases']==2 and run['completed_old_audits_replayed']==0
    audits=[];builds=[];constructs=[]
    for sig in done:
        folder=BASE/('s'+''.join(map(str,sig)));a=read(folder/'audit.json');d=read(folder/'build_status.json');c=read(folder/'construction.json')
        assert a['status']=='INDEPENDENT_RISK_PREFIX_AND_RESIDUAL_PASS' and d['status']=='COMPLETE_RISK_GUARDED_PREFIX_RELATION_UNAUDITED' and c['status']=='CONSTRUCTED_UNAUDITED'
        assert a['potential_sha256']==sha(folder/'potential.json')==read(folder/'metadata.json')['potential_sha256']
        assert a['canonical_transition_queries']==d['queries']<=1000000 and a['access_options']==d['option_count']<5000000 and a['minimum_residual']>=0
        assert a['cpu_seconds']<a['allocated_CPU_cap']<=120 and d['cpu_seconds']<d['allocated_CPU_cap']<=120 and c['cpu_seconds']<c['allocated_CPU_cap']<=300
        assert d['peak_DP_records']<2000000 and c['peak_conservative_resident_records']<2000000
        assert read(folder/'audit_exit.json')['error'] is None
        audits.append(a);builds.append(d);constructs.append(c)
    sources=[];rootfiles=[]
    for batch in cert['source_batches']:
        r=read(Path(batch['report']));assert r['status']=='RENEWED_TOTAL4_SOURCE_BATCH_PASS' and r['CPU_seconds']<300
        assert r['new_helper_controls']<=4 and r['full_closed_mixed_cycles']<=4 and r['previous_source_checks_repeated']==0
        assert r['all147_O_coordinates'] and r['same_actual127_M']
        sources.append(r);folder=Path(batch['report']).parent;rootfiles.extend((folder/name).as_posix() for name in r['root_files'])
    assert len(sources)<=6 and sum(len(r['completed_canonical_signatures']) for r in sources)==N
    assert [s for r in sources for s in r['completed_canonical_signatures']]==done
    assert len(rootfiles)==len(set(rootfiles))==sum(r['unique_original_roots'] for r in sources)
    reused=read(BASE/'reused_candidate.json')
    for r in reused['files']:assert sha(Path(r['source']))==sha(Path(r['copy']))==r['sha256']
    dependencies=[]
    for name in ('M3_POP4_RISK01/certificate.json','M3_POP4_RISK01/final_manifest.json','M3_POP4_RISK01/SOURCE_LIFT.md',
      'M3_POP4_RISK01/REPRESENTATION_PROOF.md','M3_POP3_RISK01/representation_audit.json','M3_POP3_RISK01/risk_selector.json',
      'M3_POP3_RISK01/certificate.json','M3_UNITPAIR01/B_bank.json','M3_UNITPAIR_FIN01/certificate.json',
      'M3_TWOGAP_AUD01/final_manifest.json','M3_COMB_AUD01/COMBINED_CERTIFICATE.json','M3_OUT01/proof_certificate.json'):
        p=BASE.parent/name;dependencies.append({'path':p.as_posix(),'sha256':sha(p)})
    write(BASE/'reused_dependencies.json',{'completed_old_source_queries_replayed':0,'completed_old_finite_matrices_regenerated':0,
      'authorized_old_incomplete_audit_retried':True,'old_complete_build_and_construction_reused':True,'dependencies':dependencies})
    print(json.dumps({'source_complete_new_canonical_tables':N,'new_signature_vectors':new,'checking_old_file_integrity':True}),flush=True)
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
        for actual in sorted({tuple(sig),tuple(reversed(sig))}):
            r={'status':'PROVED_RESTRICTED_DOMAIN','sigma':actual,'canonical_sigma':sig,'self_reflecting':sig==list(reversed(sig)),
              'reflected':actual!=tuple(sig),'independent_full_canonical_audit':(folder/'audit.json').as_posix(),'potential_sha256':a['potential_sha256'],
              'source_scope':'SOURCE_LIFT.md and pinned original-source lemmas','new_source_audit_workflow':'certification_run.json',
              'reflection_rule':'nonfixed low-image/selector/bank transfer; fixed sector fully direct without J invariance',
              'all_legal_masks':126,'J_range':[-2,0],'finite_walk_lower_bound':-7,'closed_mixed_walk_lower_bound':0,
              'full_original_closure':'147 O / same actual127 M','R1_R4_preserved':True,'h0_correction_preserved':True,'full_M3_proved':False}
            write(per/('s'+''.join(map(str,actual))+'.json'),r)
    bysupport={str(k):sum(sum(n>0 for n in s)==k for s in comb['new_certified_signatures']) for k in (2,3,4)}
    result={'status':'PROVED_RESTRICTED_DOMAIN_ALL577_RENEWED_TOTAL4_SIGNATURES' if new==577 else 'PROVED_RESTRICTED_DOMAIN_PARTIAL_RENEWED_TOTAL4_SIGNATURES',
      'finite_campaign_status':run['status'],'source_workflow_status':cert['status'],'new_canonical_certificates':N,'new_original_signatures':new,
      'new_signature_count_by_support_size':bysupport,'new_mask_signature_sectors':126*new,'self_reflecting_new_certificates':fixed,
      'total4_vectors_covered':138+new,'total4_vectors_remaining':577-new,'combined_signature_vectors':3044+new,'combined_mask_signature_sectors':126*(3044+new),
      'canonical_queries_independently_audited':sum(a['canonical_transition_queries'] for a in audits),'explicit_integer_residuals':sum(a['explicit_residuals'] for a in audits),
      'minimum_residual':min(a['minimum_residual'] for a in audits),'maximum_queries_per_phase':max(a['canonical_transition_queries'] for a in audits),
      'maximum_DP_records':max(d['peak_DP_records'] for d in builds),'maximum_construction_records':max(c['peak_conservative_resident_records'] for c in constructs),
      'renewed_finite_CPU_allowance':7200,'renewed_whole_process_CPU_charged':run['renewed_CPU_charged'],'prior_finite_allowance_budget_charge_unchanged':7200,
      'interrupted_old_audit_completed':done[0]==[0,0,1,0,2,1,0,0,0,0],'complete_old_phases_repeated':0,'complete_old_audits_replayed':0,
      'source_batches_passed':len(sources),'new_original_source_roots':sum(r['unique_original_roots'] for r in sources),
      'new_full_state_mixed_cycles':sum(r['full_closed_mixed_cycles'] for r in sources),'source_CPU_seconds':sum(r['CPU_seconds'] for r in sources),
      'source_per_phase_CPU_cap':300,'uniform_finite_walk_bound':-7,'closed_mixed_walk_bound':0,'R1_R4_preserved':True,'h0_correction_preserved':True,
      'per_phase_caps_unchanged':True,'Bank25':25,'T':266,'alpha_depth':2,'new_observables':0,
      'failure':run['failure'],'source_failure':cert['failure'],'finite_only_unpromoted_signatures':cert['finite_only_signatures'],
      'full_M3_proved':False,'Stage04_started':False,'negative_original_cycle_certified':False,'integrity':integrity}
    write(BASE/'certificate.json',result)
    lines=['# Renewed population-four campaign','',
      '**PROVED - RESTRICTED DOMAIN:** '+str(new)+' additional total4 signatures, '+str(N)+' independent full canonical tables with exact reflection/fixed-sector handling.',
      'All126 masks and both realizable regions; original closed mixed walks>=0, finite walks>=-7.','',
      'The explicitly interrupted audit e2+2e4+e5 was completed FIRST. Its exact saved relation, potential and complete build/construction reports were reused by hash.',
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
      'All'+str(len(old))+' old files unchanged; tracked tree clean, HEAD unchanged, all new writes confined here.','',
      '**Proof ledger:** BEFORE138/715 total4 vectors certified. RESULT '+str(new)+' newly certified; AFTER '+str(138+new)+'/715; '+str(577-new)+' remain.',
      'Combined prior/new bank:'+str(3044+new)+' signatures/'+str(126*(3044+new))+' mask sectors. No new assumptions or observables.',
      'Finite campaign:'+run['status']+'. Failure:'+json.dumps(run['failure'])+'. Source workflow:'+cert['status']+'.',
      'Current unpromoted finite-only cases:'+json.dumps(cert['finite_only_signatures'])+'.',
      '**Full M3 remains OPEN.** Larger multi-support totals remain unresolved. R1-R4,h0,original q/weights,two sorts/private scopes/actual midpoint/full closure preserved. No Stage04, Dynamic Optimality or negative-cycle promotion.']
    with (BASE/'RESULT.md').open('x',encoding='utf-8') as f:f.write(chr(10).join(lines)+chr(10))
    result['files']=[{'path':p.as_posix(),'sha256':sha(p)} for p in sorted(BASE.rglob('*')) if p.is_file()]
    write(out,result);print(json.dumps({k:v for k,v in result.items() if k!='files'},indent=2),flush=True)
if __name__=='__main__':main()

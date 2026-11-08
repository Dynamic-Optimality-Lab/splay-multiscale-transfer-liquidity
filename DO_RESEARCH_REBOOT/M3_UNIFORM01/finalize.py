"""Integrity/provenance packaging only; no mathematical phase replay."""
import json,math,os,subprocess
from pathlib import Path
from entry import BASE,sha
def read(p):return json.loads(p.read_text())
def write(p,v):
    with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    assert not (BASE/'final_manifest.json').exists();run=read(BASE/'run_result.json');folder=BASE/'case_000'
    c=read(folder/'construction.json');a=read(folder/'audit.json');q=read(folder/'formula_identity_audit.json');r=read(folder/'obstruction.json');v=read(folder/'obstruction_audit.json');source_exit=read(folder/'original_lift_exit.json')
    assert run['counterexample_case']==0 and run['completed_finite_cases']==[]
    assert [e['phase'] for e in run['events']]==['construct_candidate','audit_candidate','audit_obstruction','original_lift']
    assert run['failure']['phase']=='original_lift' and source_exit['error']['message']=='First expansion is not an accepted ORIGINAL root'
    assert q['status']=='EXACT_F_PSI_FORMULA_AUDIT_PASS' and a['status']=='ONE_STEP_CANDIDATE_REFUTED_IN_PROOF_RELATION'
    assert v['status']=='INDEPENDENT_DIRECT_COUNTEREXAMPLE_AUDIT_PASS' and not v['candidate_label_file_read']
    assert c['candidate_sha256']==q['candidate_sha256']==sha(folder/'candidate.json')
    assert (r['D1_source'],r['D1_destination'],r['weight'],r['candidate_residual'])==(1,1,-1,-1)
    assert (r['old_certified_J_source'],r['old_certified_J_destination'],r['old_certified_residual'])==(-1,-2,0)
    assert v['source']['D1']==v['destination']['D1']==1 and v['candidate_residual']==-1
    assert r['source_debt_attainment']==[2074,126,0] and v['source']['attaining_seed']['seed_psi']==2 and v['source']['attaining_seed']['weight']==1
    assert c['saved_canonical_queries_reused']<=2000000 and c['new_source_transition_queries']==a['new_source_transition_queries']==0
    assert c['peak_conservative_live_records']<2000000
    for e in run['events']:assert e['CPU_charged']<e['allocated_cap']<= (120 if e['phase']=='construct_candidate' else 300)
    # Parent bookkeeping was not timed by the controller. Do NOT invent an
    # exact reading: conservatively charge an all-processors/wall upper bound.
    # First exec returned the completed first-child event within10.003043s;
    # controller pre-main time is bounded by that interval. Main wall is saved.
    processors=os.cpu_count();assert processors==12
    parent_wall_bound=math.ceil(run['wall_seconds'])+math.ceil(10.003043)
    parent_CPU_bound=processors*parent_wall_bound
    accounted=run['whole_process_CPU_charged']+parent_CPU_bound;assert accounted<7200-5
    accounting={'status':'CONSERVATIVE_ACCOUNTING_UPPER_BOUND','exact_measured_child_process_CPU':run['whole_process_CPU_charged'],'controller_actual_CPU_not_directly_recorded':True,'saved_main_wall_seconds':run['wall_seconds'],'first_exec_wall_seconds_with_construct_complete':10.003043,'logical_processors':processors,'controller_wall_upper_bound_rounded_seconds':parent_wall_bound,'controller_CPU_conservative_charge':parent_CPU_bound,'accounted_total_CPU_upper_bound':accounted,'fresh_allowance':7200,'guaranteed_remaining_CPU_budget':7200-accounted,'old_ledger_unchanged':7195.203125,'explanation':'A process cannot consume more CPU than all host logical processors busy throughout its lifetime. Controller main wall plus the observed startup interval bounds that lifetime. This deliberately overcharges bookkeeping; it is not an invented exact CPU measurement.'}
    write(BASE/'accounting_addendum.json',accounting)
    dependencies=[]
    names=['M3_POP5_RISK01/certificate.json','M3_POP5_RISK01/final_manifest.json','M3_POP5_RISK01/SOURCE_LIFT.md','M3_POP5_RISK01/DOMAIN_THEOREM.md','M3_POP3_RISK01/REPRESENTATION_PROOF.md','M3_POP3_RISK01/representation_audit.json','M3_POP3_RISK01/risk_selector.json','M3_UNITPAIR01/B_bank.json','M3_CHIB01/RESULT.md','M3_CHIB02/RESULT.md','M3_SIG02/RESULT.md','M3_ACL_AUD02/RESULT.md','M3_H2R01/terminal_potential.py','M3_H2R01/terminal_floor_certificate.json','M3_LDR01/negative_run_census.json']
    source=Path(c['source_folder'])
    paths=[BASE.parent/n for n in names]+[source/n for n in ('relation.json','potential.json','metadata.json','build_status.json','construction.json','audit.json','audit_exit.json')]
    for p in paths:dependencies.append({'path':p.as_posix(),'sha256':sha(p)})
    write(BASE/'dependencies.json',{'prior_mathematical_checks_replayed':0,'files':dependencies})
    old=read(BASE/'entry_baseline.json');pins={p['path'] for p in old['files']}
    for i,p in enumerate(old['files']):
        assert sha(Path(p['path']))==p['sha256'],p['path']
        if (i+1)%500==0:print(json.dumps({'old_files_verified':i+1,'total':len(pins)}),flush=True)
    additions=[p for p in Path('DO_RESEARCH_REBOOT').rglob('*') if p.is_file() and BASE not in p.parents and p.as_posix() not in pins]
    assert all(p.as_posix().startswith('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/') for p in additions)
    write(BASE/'concurrent_additions.json',{'not_mathematical_dependencies':True,'files':[{'path':p.as_posix(),'sha256':sha(p)} for p in additions]})
    assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==old['head']
    assert not subprocess.check_output(['git','status','--short','--untracked-files=no'],text=True)
    integrity={'status':'PASS','old_files_unchanged':len(pins),'head':old['head'],'tracked_tree_clean':True,'writes_confined_here':True,'claim_scope':'this campaign only','concurrent_U4_additions':len(additions)}
    write(BASE/'integrity.json',integrity)
    result={'status':'ONE_STEP_UNIFORM_CLOSURE_REFUTED_IN_SAVED_PROOF_RELATION','candidate':'J1=-F(psi), one cheap incoming LOW edge only','universal_range_lemma':'PROVED_ON_THE_ESTABLISHED_VALID_PROOF_VERTEX_DOMAIN','uniform_original_LOW_closure':'OPEN','uniform_J_proved':False,'independent_formula_identity_audit':True,'independent_direct_obstruction_audit':True,'source_D1':1,'destination_D1':1,'edge_weight':-1,'candidate_residual':-1,'required_destination_debt_from_this_row':2,'existing_certificate_residual':0,'seed_then_test_weights':[1,-1],'seed_psi':2,'new_original_root_attempts':1,'new_original_root_accepted':0,'original_lift_status':'FIRST_COMPLETION_ROOT_FALSE_NO_ALTERNATIVE_SEARCH','original_counterexample_to_candidate_established':False,'original_negative_cycle_certified':False,'M3_status':'OPEN','new_original_signature_theorems':0,'NET_ORIGINAL_PROOF_ADVANCEMENT':0,'strategic_elimination':'The exact one-step debt rule cannot certify the already audited proof relation; further debt transport must be accounted for there. No claim that all uniform formulas or this candidate on the narrower original relation are refuted.','measured_experiment_CPU':run['whole_process_CPU_charged'],'accounted_CPU_upper_bound':accounted,'remaining_budget_guaranteed':7200-accounted,'CPU_caps_preserved':[120,300,300],'source_CPU_cap_preserved':300,'canonical_query_cap_preserved':2000000,'saved_source_profiles_reused':c['saved_canonical_queries_reused'],'new_source_word_regeneration':0,'seed_bounds_audited':q['seed_bounds_checked'],'new_signed_rows_until_first_failure':a['new_signed_checks'],'direct_endpoint_seed_candidates':v['direct_seed_candidates_visited'],'peak_constructor_records':c['peak_conservative_live_records'],'R1_R4_preserved':True,'h0_correction_preserved':True,'old_certificates_unchanged':True,'no_later_corpus_or_horizon_increase':True,'integrity':integrity}
    write(BASE/'certificate.json',result)
    proof='''# Uniform one-step candidate: range proof and exact obstruction

The candidate is explicit: D1(t)=max(psi(Bt), incoming w0 seed debt,
incoming w1 seed debt minus1), with maxima over the complete fixed-sigma
LOW proof relation. Set J1=-D1. This is a single-edge predecessor formula,
not an unbounded shortest-path or unknown-fixed-point definition. It is
not yet an elementary local predicate eliminating the predecessor test.

Universal range lemma, on established valid proof vertices:0<=D1<=2 and
D1>=psi. Each cheap contribution is<=2; empty maxima contribute0 and
psi lies in[0,2]. The negative-core debt theorem bounds negative incoming
seed contributions by psi at the destination. Omitted fibers satisfy
w+psi(Bt)>=2 and seed debt<=2, so cannot increase D1. Other analytically
discharged LOW normal forms retain their inherited source proofs. This
proves the range/seed part, NOT closure under another LOW transition.

The independent complete check proves exact evaluation in the saved
sigma=(4,1,0,...,0) relation: every nondefault label has an attaining
cheap seed row, and23,680,360 seed bounds cover all contributions. A
separate direct incoming-maximum calculation reads no candidate labels
and independently confirms the failed endpoints (142 seed candidates).

The exact debt trace is:

| proof vertex (B,A) | seed psi | relevant D1 | incoming weight |
|---|---:|---:|---:|
|(2074,126)|2|2|seed|
|(83,127)|0|1|+1|
|(2410,1741)|1|1|-1|

The second row retains debt1 from the seed. The next weight-1 row needs
D(destination)>=1-(-1)=2. Instead D1(destination)=1. Therefore
w-J1(t)+J1(s)=-1+1-1=-1. The stored valid certificate has J(s)=-1,
J(t)=-2 and residual0 on this SAME stored row. There is no conflict with
that certificate. The trace has total weight0 and is not a closed cycle.

The first and only registered physical completion was checked against
the unchanged original LOW root and was rejected. That establishes NO
original transition counterexample and NO impossibility of a different
completion. The proof relation is an overapproximation; failure on one
of its rows does not by itself refute the original model. The exact
result eliminates certification of this particular one-step rule through
the present proof relation. Original validity of J1 remains OPEN.

No step2 formula, extra fitted exceptions, later saved corpus or alternate
source completion was tried. The permanent RESEARCH_RULES.md instruction
"Stop on refuted mechanism" applies; the first source attempt also failed
its premise. This is strategic elimination, NET ORIGINAL ADVANCEMENT0.
All prior3761 signature certificates stay unchanged. Full M3 and a
uniform valid J remain OPEN; no Stage04/Dynamic Optimality promotion.

R1-R4, current CPU/query/state/DAG/edge/memory caps, h0 actual0/declared18/
q9/weight-3, private scopes, original q/weights and full-state closure
remain. The proposed candidate was never promoted to an original proof.
'''
    with (BASE/'PROOF_AUDIT.md').open('x',encoding='utf-8') as f:f.write(proof)
    lines=['# Uniform J: first candidate audited','',
      '**A uniform J has not been proved.** The registered one-step debt formula is exactly refuted on the saved proof relation; its validity on the narrower original relation remains OPEN.','',
      'Use D=-J. The candidate starts from psi(B), transports seed debt through one weight0/+1 incoming LOW row, then takes the maximum. The range0<=D<=2 is proved. Closure under further rows fails.',
      'Exact obstruction at sigma=(4,1,0,...,0): seed debt2 crosses a+1 row into debt1 at (B83,A127), then a-1 row to (B2410,A1741). The candidate gives debt1 at both endpoints; residual-1. Independent direct maxima confirm both values. The existing valid certificate gives J=-1 then-2, residual0.','',
      f'Formula audit: {q["seed_bounds_checked"]:,} seed bounds and attaining witnesses. Direct endpoint audit: {v["direct_seed_candidates_visited"]} seed candidates, without reading candidate labels. Saved canonical profiles reused:{c["saved_canonical_queries_reused"]:,}; no grammar/B-bank/source-word audit regenerated.',
      'The one original-root lift attempt was rejected. No original edge counterexample, negative mixed cycle, or refutation of M3 is certified. No alternate completion was searched.','',
      'The next necessary debt-transport obligation in this proof relation is the+1 followed by-1 pattern above. No sufficiency of two-step transport or arbitrary zero-chain closure is claimed.',
      'Stopped at the first candidate obstruction and the registered source-premise failure, as required by RESEARCH_RULES.md. No fitted exception, horizon increase, second/third corpus or automatic retry was run. This rules out one specified mechanism, not the uniform-formula project.',
      f'Current caps retained. Exact measured experimental process CPU:{run["whole_process_CPU_charged"]}; conservative accounted upper bound including controller:{accounted}/7200. Controller CPU was not directly recorded; accounting_addendum.json explicitly charges an all-logical-processors/wall upper bound rather than inventing an exact measurement. Guaranteed remaining allowance:{7200-accounted}. Old ledger7195.203125 unchanged.',
      f'All {len(pins)} pinned prior files unchanged; HEAD/tracked tree unchanged. Concurrent U4 additions are recorded separately. R1-R4 and corrected h0 preserved.','',
      '**NET ORIGINAL PROOF ADVANCEMENT:0.** All prior certified scopes remain valid. Full M3 and a uniform formula remain OPEN. See PROOF_AUDIT.md and exact machine records in case_000/.']
    with (BASE/'RESULT.md').open('x',encoding='utf-8') as f:f.write('\n'.join(lines)+'\n')
    result['files']=[{'path':p.as_posix(),'sha256':sha(p)} for p in sorted(BASE.rglob('*')) if p.is_file()]
    write(BASE/'final_manifest.json',result)
    print(json.dumps({k:v for k,v in result.items() if k!='files'},indent=2),flush=True)
if __name__=='__main__':main()

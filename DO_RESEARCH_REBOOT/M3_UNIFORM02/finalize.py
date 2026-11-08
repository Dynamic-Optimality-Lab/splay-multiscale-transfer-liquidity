"""Provenance, mandatory strategy review and integrity; no experiment replay."""
import json,subprocess
from pathlib import Path
from entry import BASE,sha
def read(p):return json.loads(p.read_text())
def write(p,v):
    with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    assert not (BASE/'final_manifest.json').exists();run=read(BASE/'run_result.json');controller=read(BASE/'controller_exit.json');folder=BASE/'case_000';build=read(folder/'construction.json');identity=read(folder/'formula_identity_audit.json');audit=read(folder/'audit.json');r=read(folder/'obstruction.json');direct=read(folder/'obstruction_audit.json');orig=read(folder/'original_control.json')
    assert run['status']=='STOPPED_ON_FIRST_SIGN_RUN_COUNTEREXAMPLE' and run['counterexample_case']==0 and run['failure'] is None
    assert [e['phase'] for e in run['events']]==['construct','audit','audit_obstruction','original_lift'] and not run['completed_finite_cases']
    assert identity['status']=='INDEPENDENT_SIGN_RUN_FORMULA_IDENTITY_PASS' and audit['status']=='SIGN_RUN_CANDIDATE_REFUTED_IN_PROOF_RELATION'
    assert identity['old_plus1_minus1_regression']=={'source_debt':1,'destination_debt':2,'residual':0,'old_original_lift_repeated':False}
    assert identity['C_sha256']==build['C_sha256']==sha(folder/'C_values.json') and identity['candidate_sha256']==build['candidate_sha256']==sha(folder/'candidate.json')
    assert direct['status']=='INDEPENDENT_PROMOTION_ENDPOINT_AUDIT_PASS' and not direct['final_candidate_labels_read']
    assert (r['D_run_source'],r['D_run_destination'],r['weight'],r['candidate_residual'])==(2,0,1,-1)
    assert (r['old_certified_J_source'],r['old_certified_J_destination'],r['old_certified_residual'])==(-2,-1,0)
    assert r['source_promotion']==[2983,4100,17] and direct['source']['D_run']==2 and direct['destination']['D_run']==0
    assert orig['status']=='FIRST_NEW_COMPLETION_ROOT_FALSE_UNLIFTED' and not orig['original_root'] and not orig['old_rejected_completion_repeated']
    assert read(folder/'original_attempt.json')['root'] is False
    for e in run['events']:assert e['error'] is None and e['CPU_charged']<e['allocated_cap']<= (120 if e['phase']=='construct' else 300)
    assert controller['error'] is None
    newCPU=run['new_child_process_CPU']+controller['whole_process_CPU_seconds'];accounted=622.0625+newCPU;assert accounted<7200-5
    resources={'prior_conservative_uniform_charge_retained':622.0625,'new_exact_child_process_CPU':run['new_child_process_CPU'],'new_controller_CPU_through_finally':controller['whole_process_CPU_seconds'],'new_measured_experimental_CPU':newCPU,'cumulative_accounted_CPU':accounted,'finite_CPU_ceiling':7200,'guaranteed_remaining_CPU':7200-accounted,'old_sigma_campaign_ledger_unchanged':7195.203125,'CPU_caps':[120,300,300],'source_CPU_cap':300,'canonical_query_cap':2000000,'new_source_word_queries':0,'new_original_root_evaluations':1,'new_original_roots_accepted':0,'saved_canonical_profiles_reused':build['saved_canonical_profiles_reused'],'peak_construct_records':build['peak_conservative_live_records'],'peak_independent_audit_records':identity['peak_conservative_live_records'],'metadata_hashing_convention':'entry/final preservation bookkeeping excluded as in prior campaigns; child experimental and controller CPU charged'}
    assert max(resources['peak_construct_records'],resources['peak_independent_audit_records'])<2000000 and resources['saved_canonical_profiles_reused']<=2000000
    write(BASE/'resources.json',resources)
    # Extract the already audited attaining C path. This is proof provenance,
    # not another candidate, transition query, or signed propagation pass.
    source=Path(build['source_folder']);c=read(source/'relation.json');B=read(BASE.parent/'M3_UNITPAIR01/B_bank.json');psi=B['psi'];N=c['classes'];hp=read(folder/'C_attainment.json');hist=hp['history'];latest=hp['latest'];init=read(BASE.parent/'M3_UNIFORM01/case_000/candidate.json');values=read(folder/'candidate.json')['values']
    def row(bs,asrc,oi):
        o=c['options'][asrc][oi];H,x,aa,g,fi,code=o
        bb,w=(B['destinations'][bs][x],2-B['depths'][bs][x]//2) if H==1 else B['kernels'][str(g)][bs][x]
        return {'source_B':bs,'source_A':asrc,'destination_B':bb,'destination_A':aa,'weight':w,'H':H,'target':x,'helper':g,'option_index':oi,'word':c['families'][fi]['word']}
    pb,pa,poi=r['source_promotion'];key=pb*N+pa;idx=latest.get(str(key),-1);back=[]
    while idx>=0:
        u,v,oi,ds,dt,prior=hist[idx];assert v==key
        back.append(row(*divmod(u,N),oi));key=u;idx=prior
    b,a=divmod(key,N);path=[]
    if str(key) in init['values']:
        bs,asrc,oi=init['attainment'][str(key)];path.append(row(bs,asrc,oi));seed=(bs,asrc)
    else:seed=(b,a)
    path+=list(reversed(back));path.append(row(pb,pa,poi));path.append(row(r['source_B'],r['source_A'],r['option_index']))
    current=seed;debt=psi[seed[0]]
    for e in path:
        assert current==(e['source_B'],e['source_A']);current=(e['destination_B'],e['destination_A']);debt-=e['weight'];e['transported_debt_after']=debt
        e['candidate_D_at_destination']=values.get(str(current[0]*N+current[1]),psi[current[0]])
    assert current==(r['destination_B'],r['destination_A']) and debt==1 and r['D_run_destination']==0
    trace={'status':'ATTAINMENT_TRACE_FROM_AUDITED_RECORDS','seed_B':seed[0],'seed_A':seed[1],'seed_psi':psi[seed[0]],'rows':path,'total_weight':sum(e['weight'] for e in path),'required_final_debt':debt,'candidate_final_debt':0,'proof_vertices_close':current==seed,'original_full_state_trace_validated':False,'original_negative_cycle_certified':False,'new_transition_queries':0}
    write(folder/'attainment_trace.json',trace)
    del c,B,hp,hist,latest,init,values
    names=['RESEARCH_RULES.md','M3_UNIFORM01/certificate.json','M3_UNIFORM01/PROOF_AUDIT.md','M3_UNIFORM01/accounting_addendum.json','M3_UNIFORM01/case_000/candidate.json','M3_UNIFORM01/case_000/formula_identity_audit.json','M3_UNIFORM01/case_000/obstruction.json','M3_POP5_RISK01/certificate.json','M3_POP5_RISK01/final_manifest.json','M3_POP5_RISK01/SOURCE_LIFT.md','M3_POP3_RISK01/REPRESENTATION_PROOF.md','M3_POP3_RISK01/representation_audit.json','M3_POP3_RISK01/risk_selector.json','M3_UNITPAIR01/B_bank.json','M3_LDR01/negative_run_census.json']
    deps=[BASE.parent/name for name in names]+[source/name for name in ('relation.json','potential.json','metadata.json','build_status.json','construction.json','audit.json')]
    write(BASE/'dependencies.json',{'old_mathematical_checks_replayed':0,'files':[{'path':p.as_posix(),'sha256':sha(p)} for p in deps]})
    old=read(BASE/'entry_baseline.json');pins={p['path'] for p in old['files']}
    for i,p in enumerate(old['files']):
        assert sha(Path(p['path']))==p['sha256'],p['path']
        if (i+1)%500==0:print(json.dumps({'old_files_verified':i+1,'total':len(pins)}),flush=True)
    additions=[p for p in Path('DO_RESEARCH_REBOOT').rglob('*') if p.is_file() and BASE not in p.parents and p.as_posix() not in pins]
    assert all(p.as_posix().startswith('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/') for p in additions)
    write(BASE/'concurrent_additions.json',{'not_mathematical_dependencies':True,'files':[{'path':p.as_posix(),'sha256':sha(p)} for p in additions]})
    assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==old['head'] and not subprocess.check_output(['git','status','--short','--untracked-files=no'],text=True)
    integrity={'status':'PASS','old_files_unchanged':len(pins),'head':old['head'],'tracked_tree_clean':True,'writes_confined_here':True,'claim_scope':'this campaign only','concurrent_U4_additions':len(additions)}
    write(BASE/'integrity.json',integrity)
    review='''# Mandatory review after two debt-transport pivots

UNIFORM01's one cheap predecessor fails on+1 then-1. UNIFORM02 is a
different, determined sign-run formula: it closes ALL nonnegative paths
first (arbitrarily many zero helpers, at most one positive toll matters)
and then the complete capped negative run. Its algebraic promotion rule
fixes the old obstruction exactly, and its two component functions have
independent attainment/closure certificates. It nevertheless fails when
a+1 row follows a newly promoted negative-run state: debt2 must leave
debt>=1, but the formula returns0. Both pivots yield NET ORIGINAL
ADVANCEMENT0. Treat them conservatively as two consecutive failures of
transport-envelope shortcuts; do not reset that count by renaming phases.

This is NOT evidence that every uniform formula fails. It rejects the
specified truncated sign-language certificates in the present proof
superrelation. The two attempted physical completions were rejected;
neither proves emptiness of the original preimage of the offending row.
All existing signed certificates remain valid, since a stronger proof
relation can certify a valid J even though a simpler proposed J fails.

Do not automatically try C*N*C*, another finite transport horizon, or
arbitrary repeated signed closure. The last is the original open
feasibility burden unless a NEW invariant/construction proves it safe.
A finite fit or a longer history budget is not that theorem.

Two genuinely different research obligations are now explicit:

1. A source-exact feasibility audit for the specific offending row,
   leaving ALL original private counts/bills, legal mu, unused fields,
   slot0 aliases and weak LE freedoms quantified. One rejected completion
   is not an UNSAT proof. Accepted original witnesses must be checked by
   the unchanged root; an impossibility claim needs complete independently
   audited evidence. This may distinguish an artificial proof row from a
   real constraint without modifying the original graph.
2. A structural shared-state invariant that retains newly promoted debt
   through subsequent cheap helpers, with a genuine reason for bounded
   description/closure. It must explain interleaved signs, not assume
   a fixed ordering of sign blocks or omit compatible private branches.

These are directions for a fresh four-rule gate, NOT completed theorems
or automatically authorized post-failure experiments in this campaign.
The source-exactness issue and general invariant must not be silently
combined as two independent open premises of a purported proof.

Current result: uniform J and original closure OPEN. Prior3761 signature
certificates, including all715 total-four and140 total-five multi-support,
stay unchanged. No new original sector, negative cycle, Stage04 or
Dynamic Optimality promotion. The strategy review is complete; the next
mechanism needs a concrete new identity or source-exact construction.
'''
    with (BASE/'STRATEGY_REVIEW.md').open('x',encoding='utf-8') as f:f.write(review)
    proof='''# Sign-run formula: proved components and audited failure

Candidate: C is the least nonnegative-row debt envelope from psi; D is
the capped negative-run envelope from C, and J=-D. The sign language is
0*(1 0*)? followed by a negative-only run. Nonnegative transport is always
range-bounded by2 and has at most2V strict increases. The established
negative core law implies that only psi1 destinations can be promoted:
a w=-1 predecessor with psi0 and C>0 forces D=2. Psi0 destinations have
no negative predecessors; psi2 destinations already have debt2. This
proves the promotion formula and range0<=D<=2,D>=psi universally on the
valid proof-vertex domain. It does not prove every original edge bound.

Independent finite audit proves C exactly by seed-attaining derivation
DAGs and every needed nonnegative row inequality. It reuses UNIFORM01's
completed seed-bound audit rather than rerunning it. It then verifies
every promotion trigger and an attaining incoming row for each change.
The old+1,-1 obstruction now has debts1,2 and residual0. No old original
lift was repeated. Thus the specific transfer requested is handled.

The first NEW counterexample, at sigma=(4,1,0,...,0), is:

| proof vertex (B,A) | psi | C | D | next row weight |
|---|---:|---:|---:|---:|
|(2983,4100)|0|1|1|-1|
|(1647,2073)|1|1|2|+1|
|(2403,2072)|0|0|0|end|

The last row requires D(t)>=D(s)-1=1, but gives0. Therefore
w-J(t)+J(s)=1+0-2=-1. The existing certificate has J(s)=-2,J(t)=-1,
residual0 on the SAME stored row. Separate direct promotion evaluation
reads no final D labels and confirms source2,destination0. Its C inputs
are pinned to the independently proved C identity. Full attaining paths
from psi are recorded in case_000/attainment_trace.json; they are proof
rows, not a claim of full original-state closure.

The new single registered completion was rejected by the unchanged
original LOW root. Its full environment and root=False were saved.
Neither original invalidity of J nor impossibility of another completion
is established. This is an exact refutation of the given certificate on
the existing superrelation, not an original M3 counterexample/negative
cycle. The failing+1 row is different from UNIFORM01's failed row.

All current caps and R1-R4, h0 correction, source q/weights, actual shared
midpoint/private scopes and full-state closure requirements remain.
No later corpus, extra sign block, failed-phase replay or original source
change was run. The mandatory strategy review follows separately.
Uniform J remains OPEN; NET ORIGINAL PROOF ADVANCEMENT0.
'''
    with (BASE/'PROOF_AUDIT.md').open('x',encoding='utf-8') as f:f.write(proof)
    result={'status':'SIGN_RUN_CANDIDATE_REFUTED_ON_SAVED_PROOF_RELATION','candidate':'D=min(2,N*(C*(psi))); J=-D; exact promotion simplification','old_plus1_minus1_transfer_fixed':True,'old_regression_residual':0,'independent_formula_identity_audit':True,'C_attainment_rows':identity['C_attainment_history_rows'],'nonnegative_closure_checks':identity['nonnegative_closure_rows'],'negative_promotion_checks':identity['negative_promotion_triggers'],'new_signed_rows_until_failure':audit['signed_rows_until_stop'],'new_failing_weight':1,'source_D':2,'destination_D':0,'required_destination_D':1,'candidate_residual':-1,'existing_certificate_residual':0,'independent_direct_endpoint_audit':True,'final_candidate_labels_used_by_direct_audit':False,'new_original_root_attempts':1,'new_original_root_accepted':0,'original_validity_of_candidate':'OPEN','original_negative_cycle_certified':False,'uniform_J_proved':False,'M3_status':'OPEN','NET_ORIGINAL_PROOF_ADVANCEMENT':0,'mandatory_strategy_review_completed':True,'further_automatic_sign_alternation_search':False,'R1_R4_preserved':True,'h0_correction_preserved':True,'resources':resources,'integrity':integrity}
    write(BASE/'certificate.json',result)
    lines=['# New uniform J candidate: sign-run audit','',
      '**The requested+1 then-1 transfer is fixed, but a uniform valid J is still OPEN.** The sign-run formula is refuted on the existing proof superrelation; original validity is not decided.','',
      'The formula first computes safe nonnegative closure C*(psi), handling arbitrarily many zero helpers, then applies the entire capped negative-run promotion. The core-debt law reduces the negative phase to one explicit psi1 promotion rule. It is a fixed sign-language function, not arbitrary signed fixed-point optimization.',
      f'Independent audit: {identity["C_attainment_history_rows"]:,} attaining history rows; {identity["nonnegative_closure_rows"]:,} nonnegative closure checks; {identity["negative_promotion_triggers"]:,} promotion triggers. The old+1,-1 example now has residual0. Completed seed/bank/word/source checks were reused.',
      f'The first new signed failure appears after {audit["signed_rows_until_stop"]:,} row checks: a weight+1 row leaves source debt2 and the candidate gives destination debt0, where at least1 is required. Residual-1. The existing certificate gives destination debt1 and residual0. A direct incoming-promotion audit independently confirms both endpoint values without reading final candidate labels.',
      'The new original-root completion was rejected. This supplies no original transition counterexample, no proof that another completion is impossible, and no negative mixed cycle. No alternative completion or later corpus was searched.','',
      'Two consecutive transport-formula pivots have now failed to advance the original theorem. STRATEGY_REVIEW.md records why adding sign phases/horizons automatically would be a treadmill, and distinguishes source-exact realizability from the new structural debt invariant still needed.',
      f'New measured experiment/controller CPU:{newCPU}; prior conservative charge622.0625 retained; cumulative accounted{accounted}/7200; guaranteed remaining{7200-accounted}. Current120/300/300 CPU caps,2m queries,2m live records,4m DAG,5m edges,32GiB/inherited12h unchanged. Source audit cap300. Peak audited records:{identity["peak_conservative_live_records"]:,}.',
      f'R1-R4 and h0 preserved. All {len(pins)} pinned prior files unchanged; HEAD/tracked tree unchanged. Concurrent U4 additions recorded separately.','',
      '**NET ORIGINAL PROOF ADVANCEMENT:0.** All prior certified scopes remain intact. Full M3/uniform J remain OPEN. See PROOF_AUDIT.md, STRATEGY_REVIEW.md and exact case_000/ records.']
    with (BASE/'RESULT.md').open('x',encoding='utf-8') as f:f.write('\n'.join(lines)+'\n')
    result['files']=[{'path':p.as_posix(),'sha256':sha(p)} for p in sorted(BASE.rglob('*')) if p.is_file()]
    write(BASE/'final_manifest.json',result);print(json.dumps({k:v for k,v in result.items() if k!='files'},indent=2),flush=True)
if __name__=='__main__':main()

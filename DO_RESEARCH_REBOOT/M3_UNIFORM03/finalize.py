"""Finalize the exact size obstruction, provenance and immutable-file audit."""
import json,sys,time,subprocess,hashlib
from pathlib import Path
from entry import BASE,sha
def read(p):return json.loads(p.read_text())
def write(p,v):
    with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    assert not (BASE/'final_manifest.json').exists()
    run=read(BASE/'run_result.json');control=read(BASE/'controller_exit.json');p=read(BASE/'preflight.json');a=read(BASE/'independent_preflight_audit.json')
    assert run['status']=='STOPPED_ON_INDEPENDENTLY_VERIFIED_COUNT_FREE_SIZE_OBSTRUCTION' and run['failure'] is None and control['error'] is None
    assert p['status']=='EXACT_COUNT_FREE_CORPUS_LOWER_BOUND_EXCEEDS_QUERY_CAP' and a['status']=='INDEPENDENT_INJECTIVE_SUBGRAMMAR_SIZE_AUDIT_PASS'
    assert p['canonical_root_lower_bound']==a['canonical_root_lower_bound']==2248613 and a['fiber_counts_checked']==420
    assert a['families_checked']==p['families_counted']==6 and a['source_transition_queries']==p['source_transition_queries']==0
    assert a['preflight_sha256']==sha(BASE/'preflight.json') and not a['construction_imported']
    for e in run['events']:assert e['error'] is None and e['CPU_charged']<e['allocated_cap']
    charge=run['new_child_process_CPU']+control['whole_process_CPU_seconds'];total=run['prior_conservative_uniform_charge']+charge
    resources={'prior_conservative_uniform_charge_retained':665.296875,'new_child_process_CPU':run['new_child_process_CPU'],'new_controller_CPU_through_finally':control['whole_process_CPU_seconds'],'new_measured_experimental_CPU':charge,'cumulative_accounted_CPU':total,'finite_CPU_ceiling':7200,'guaranteed_remaining_CPU':7200-total,'old_signature_campaign_ledger_unchanged':7195.203125,'per_phase_caps_preserved':[120,300,300],'canonical_query_limit':2000000,'actual_new_source_transition_queries':0,'projected_lower_bound_not_executed':2248613,'counting_peak_live_records':max(p['peak_counting_records'],a['peak_counting_records']),'old_censuses_or_original_roots_repeated':0,'no_query_cap_exceeded':True,'metadata_hashing_convention':'entry/final immutable-file bookkeeping excluded as previously'}
    assert total<7200-5;write(BASE/'resources.json',resources)
    deps=['RESEARCH_RULES.md','M3_ROW_AUD01/certificate.json','M3_ROW_AUD01/independent_verification.json','M3_ROW_AUD01/witness.json','M3_ROW_AUD01/resources.json','M3_UNIFORM02/STRATEGY_REVIEW.md','M3_UNIFORM02/case_000/obstruction.json','M3_UNIFORM02/case_000/formula_identity_audit.json','M3_POP4_RISK01/SOURCE_LIFT.md','M3_POP5_RISK01/SOURCE_LIFT.md','M3_POP5_RISK01/DOMAIN_THEOREM.md','M3_POP5_RISK01/certificate.json','M3_POP3_RISK01/REPRESENTATION_PROOF.md','M3_POP3_RISK01/representation_audit.json','M3_POP3_RISK01/risk_selector.json','M3_UNITPAIR01/B_bank.json','M3_UNITPAIR01/profiles.py','M3_TWOGAP_AUD01/reference.py','M3_OUT01/RESULT.md','06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER/PC_TYPED_DAG.py','06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_LOW_COMPILER.py','06_CERTIFICATES/DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE/STRICT_HIGH_COMPILER.py']
    write(BASE/'dependencies.json',{'prior_checks_reused_not_rerun':True,'files':[{'path':(BASE.parent/name).as_posix(),'sha256':sha(BASE.parent/name)} for name in deps]})
    prior=read(BASE/'entry_baseline.json');pins={e['path'] for e in prior['files']}
    for i,e in enumerate(prior['files']):
        assert sha(Path(e['path']))==e['sha256'],e['path']
        if (i+1)%1000==0:print(json.dumps({'prior_files_verified':i+1,'total':len(pins)}),flush=True)
    additions=[p for p in BASE.parent.rglob('*') if p.is_file() and BASE not in p.parents and p.as_posix() not in pins]
    assert all('/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/' in p.as_posix() for p in additions),[p.as_posix() for p in additions]
    write(BASE/'concurrent_additions.json',{'not_math_dependencies':True,'files':[{'path':p.as_posix(),'sha256':sha(p)} for p in additions]})
    assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==prior['head']
    assert not subprocess.check_output(['git','status','--short','--untracked-files=no'],text=True)
    integrity={'status':'PASS','old_files_unchanged':len(pins),'HEAD':prior['head'],'tracked_tree_clean':True,'this_campaign_writes_confined_here':True,'unrelated_concurrent_U4_additions':len(additions)};write(BASE/'integrity.json',integrity)
    cert={'status':'FINITE_EXACT_INDEPENDENTLY_VERIFIED_SIZE_OBSTRUCTION_TO_EXPLICIT_COUNT_FREE_ROUTE','count_free_source_coverage':'STRUCTURAL_PROOF_REUSING_FIXED_BUDGET_LIFT','canonical_H1_source_word_case_lower_bound':2248613,'risky_fiber_counts_independently_equal':420,'six_H1_word_families_only':True,'uniform_J_constructed':False,'uniform_J_proved':False,'new_signed_original_sectors':0,'negative_cycle_certified':False,'M3_status':'OPEN','DynamicOptimality_status':'OPEN','NET_ORIGINAL_M3_PROOF_ADVANCEMENT':0,'R1_R4_preserved':True,'h0_correction_preserved':True,'existing_certificates_and_source_audits_reused':True,'no_further_mechanism_or_transport_horizon_tried':True,'resource_obstruction_is_not_uniform_formula_impossibility':True,'resources':resources,'integrity':integrity}
    write(BASE/'certificate.json',cert)
    report=f'''# Uniform03: count-independent structural table route stopped at size gate

**No new uniform J or signed M3 bound was proved.** I tested a different
mechanism from the failed sign-run formulas: one count-independent
J(coreB,alpha7) on a source-complete finite prefix grammar, with every
signed row checked against the same table. That would cover arbitrarily
repeated +/- debt transfers if a complete valid table were obtained.

An exact injective subgrammar already has **2,248,613 distinct source/word
cases in the six H1 families**, exceeding the unchanged2,000,000-query
limit for the registered explicit enumeration. A separate checker,
importing no construction code, independently verifies all420 risky
root/target fiber counts using ordered Score lists and parent-map address
identities. It agrees exactly. Both counting phases finish in<1 CPU second.

The lower bound concerns this explicit canonical-prefix enumeration. It
does NOT bound the minimum possible proof size, the number of distinct
signed endpoint rows, or the complexity of an analytic formula. The
count-free coverage lemma retains every original private branch; no
deterministic hidden-S completion or new shared observable is assumed.
It is a representation result, not a signed feasibility theorem.

I stopped before transition enumeration or table fitting, as registered
in PRE_EXECUTION.md. Actual new transition queries=0; no cap was exceeded.
No H2 family, original root or completed old matrix/debt census was rerun.
The previously verified original +1 edge remains real and still refutes
J_run. It supplies no negative cycle. No new formula assigns values to it.

R1-R4/current caps and h0 correction held. All{len(pins)} pinned prior
files remain byte-identical; HEAD/tracked tree unchanged. New measured
experimental/controller CPU={charge}; cumulative uniform allowance
{total}/7200, guaranteed remaining{7200-total}. No allowance renewal.

BEFORE: repeated signed transfer required a uniform invariant.
RESULT: this explicit count-free route cannot be completed within the
current canonical-query cap; independently verified size obstruction.
AFTER: stop this mechanism; do not split its failed corpus or silently
increase caps. NET ORIGINAL M3 PROOF ADVANCEMENT=0. All3761 prior
signature certificates remain unchanged. M3/Dynamic Optimality stay OPEN.

The remaining research obligation is a structural formula or symbolic
residual reduction that avoids visiting this whole prefix corpus while
preserving all private branches and arbitrary signed alternation. No
such reduction is asserted here. See SOURCE_COVERAGE.md for the exact
coverage/counting proof and independent_preflight_audit.json for evidence.
'''
    with (BASE/'RESULT.md').open('x',encoding='utf-8') as f:f.write(report)
    cert['files']=[{'path':p.as_posix(),'sha256':sha(p)} for p in sorted(BASE.rglob('*')) if p.is_file()]
    write(BASE/'final_manifest.json',cert);print(json.dumps({k:v for k,v in cert.items() if k!='files'},indent=2),flush=True)
if __name__=='__main__':main()

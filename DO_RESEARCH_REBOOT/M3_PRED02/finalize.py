"""Finalize original exact refutation, memory fix and critical-budget proof."""
import json,subprocess
from pathlib import Path
from entry import BASE,sha
def read(p):return json.loads(p.read_text())
def write(p,v):
    with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    assert not (BASE/'final_manifest.json').exists()
    r=read(BASE/'run_result.json');ctrl=read(BASE/'controller_exit.json');cc=read(BASE/'counter_control_result.json');ccx=read(BASE/'counter_controller_exit.json');ep=read(BASE/'endpoint_audit.json');v=read(BASE/'independent_original_verification.json');w=read(BASE/'source_result.json');a=read(BASE/'case_000/audit.json');ident=read(BASE/'case_000/predicate_identity_audit.json');crit=read(BASE/'independent_critical_budget_audit.json')
    assert r['status']=='STOPPED_ON_FIRST_NEW_THRESHOLD_COUNTEREXAMPLE' and r['first_counterexample_case']==0 and r['failure'] is None and ctrl['error'] is None
    assert cc['status']=='ORIGINAL_PREDICATE_REFUTATION_INDEPENDENTLY_CERTIFIED' and cc['failure'] is None and ccx['error'] is None
    assert ident['status']=='INDEPENDENT_STREAMED_THRESHOLD_PREDICATE_IDENTITY_PASS' and ident['all_exceptions_attained'] and ident['all_eligible_basis_contributions_bounded']
    assert ident['candidate_sha256']==sha(BASE.parent/'M3_PRED01/case_001/candidate.json')
    assert a['signed_rows_checked']==10248314 and a['minimum_residual']==-1 and a['peak_conservative_records']==1529558<2000000
    assert ep['candidate_residual']==v['candidate_residual']==v['candidate_full_W_residual']==-1
    assert (v['source_debt'],v['destination_debt'],v['H'],v['q'],v['weight'],v['target'])==(2,0,1,1,1,0)
    assert w['original_root'] and v['original_root'] and not v['factory_called'] and v['namespace_rename_bijective'] and v['all147_source_and_destination_coordinates_match'] and v['independent_A_and_B_parent_map_replays']
    assert v['old_certified_residual']==0 and not v['full_endpoints_close'] and not v['original_negative_cycle_certified']
    assert crit['status']=='INDEPENDENT_COMPLETE_CRITICAL_BUDGET_REDUCTION_AUDIT_PASS' and crit['exact_max_retained_F']==9 and crit['critical_total_population_bound']==13
    assert crit['word_families']==78 and crit['risky_fibers_checked']==3360 and crit['attaining_prefixes_checked']==18 and not crit['universal_preservation_test_executed']
    assert [p.name for p in BASE.glob('case_*') if p.is_dir()]==['case_000']
    for e in r['events']+cc['events']:assert e['error'] is None and e['CPU_charged']<e['allocated_cap']
    charge=r['new_child_process_CPU']+ctrl['whole_process_CPU_seconds']+cc['new_child_process_CPU']+ccx['whole_process_CPU_seconds'];total=713.59375+charge;assert total<7200-5
    res={'prior_conservative_uniform_charge_retained':713.59375,'new_main_child_process_CPU':r['new_child_process_CPU'],'new_main_controller_CPU_through_finally':ctrl['whole_process_CPU_seconds'],'new_counter_child_process_CPU':cc['new_child_process_CPU'],'new_counter_controller_CPU_through_finally':ccx['whole_process_CPU_seconds'],'new_measured_experimental_CPU':charge,'cumulative_accounted_CPU':total,'finite_CPU_ceiling':7200,'guaranteed_remaining_CPU':7200-total,'old_signature_campaign_ledger_unchanged':7195.203125,'CPU_caps_preserved':[120,300,300],'live_record_limit':2000000,'retry_peak_conservative_records':a['peak_conservative_records'],'immutable_bank_container_count':ident['immutable_bank_containers'],'canonical_query_limit':2000000,'new_canonical_source_transition_queries':0,'new_original_root_evaluations':2,'new_independent_direct_endpoint_audits':1,'max_DAG_nodes':v['DAG_nodes'],'original_variables':v['variables'],'old_completed_formula_grammar_debt_or_root_checks_repeated':0,'authorized_old_unknown_retry_completed':True,'candidate_construction_reused':True,'old_candidate_file_unchanged':True,'later_tests_after_first_refutation':False,'no_cap_increase':True,'metadata_hashing_convention':'entry/final immutable-file bookkeeping excluded as previously'}
    write(BASE/'resources.json',res)
    names=['RESEARCH_RULES.md','M3_PRED01/resources.json','M3_PRED01/basis.json','M3_PRED01/case_000/audit.json','M3_PRED01/case_001/construction.json','M3_PRED01/case_001/candidate.json','M3_PRED01/PREDICATES.md','M3_POP5_RISK01/s3110000000/relation.json','M3_POP5_RISK01/s3110000000/audit.json','M3_POP5_RISK01/s3110000000/potential.json','M3_POP5_RISK01/SOURCE_LIFT.md','M3_POP4_RISK01/SOURCE_LIFT.md','M3_POP3_RISK01/REPRESENTATION_PROOF.md','M3_POP3_RISK01/representation_audit.json','M3_POP3_RISK01/risk_selector.json','M3_UNITPAIR01/B_bank.json','M3_UNITPAIR01/profiles.py','M3_UNITPAIR01/proposal_factory_v2.py','M3_POP5_RISK01/source_audit_batch.py','M3_GAPINT01/interior_original.py','M3_TWOGAP_AUD01/reference.py','M3_OUT01/RESULT.md','06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER/PC_TYPED_DAG.py','06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_LOW_COMPILER.py']
    for e in read(BASE.parent/'M3_PRED01/case_001/construction.json')['basis_dependencies']:
        names.extend([str(Path(e['folder'])/n) for n in ('metadata.json','potential.json')]);names.append(e['completion'])
    paths=sorted({(BASE.parent/n).resolve() for n in names});write(BASE/'dependencies.json',{'completed_checks_reused_not_replayed':True,'files':[{'path':p.as_posix(),'sha256':sha(p)} for p in paths]})
    old=read(BASE/'entry_baseline.json');pins={e['path'] for e in old['files']}
    for i,e in enumerate(old['files']):
        assert sha(Path(e['path']))==e['sha256'],e['path']
        if (i+1)%1000==0:print(json.dumps({'old_files_verified':i+1,'total':len(pins)}),flush=True)
    additions=[p for p in BASE.parent.rglob('*') if p.is_file() and BASE not in p.parents and p.as_posix() not in pins]
    assert all('/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/' in p.as_posix() for p in additions),[p.as_posix() for p in additions]
    write(BASE/'concurrent_additions.json',{'not_mathematical_dependencies':True,'files':[{'path':p.as_posix(),'sha256':sha(p)} for p in additions]})
    assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==old['head'] and not subprocess.check_output(['git','status','--short','--untracked-files=no'],text=True)
    integrity={'status':'PASS','old_files_unchanged':len(pins),'HEAD':old['head'],'tracked_tree_clean':True,'this_campaign_writes_confined_here':True,'unrelated_concurrent_U4_additions':len(additions)};write(BASE/'integrity.json',integrity)
    cert={'status':'FOUR_POPULATION_PREDICATE_TEMPLATE_REFUTED_EXACT_ON_ORIGINAL_LOW','memory_efficient_retry':'COMPLETE_WITHIN_CURRENT_CAPS','input_sigma':[3,1,1,0,0,0,0,0,0,0],'mu':341,'source_B':1998,'source_A':7669,'destination_B':7,'destination_A':33361,'target':0,'A_depth':2,'B_depth':2,'H':1,'q':1,'weight':1,'source_debt':2,'destination_debt':0,'source_visible_F':1,'destination_visible_F':5,'P2_source':True,'P1_destination':False,'candidate_residual':-1,'candidate_full_W_residual':-1,'old_certified_J_source':-2,'old_certified_J_destination':-1,'old_certified_residual':0,'both_original_LOW_evaluations_true':True,'independent_fresh_namespace_no_factory':True,'all147_endpoint_coordinates_checked':True,'independent_A_B_rotations':True,'first_possible_counter_total_beyond_complete_four_basis':5,'new_signed_rows_checked_before_failure':10248314,'critical_budget_reduction':'PROVED_FOR_FIXED_CANDIDATE_RETAINED_PROOF_RELATION','exact_max_retained_F':9,'sufficient_critical_population_cutoff':13,'all78_word_shapes_and3360_fibers_independently_audited':True,'universal_cutoff_test_executed':False,'original_negative_cycle_certified':False,'full_endpoints_close':False,'M3_status':'OPEN','same_signature_prior_M3_certificate':'REMAINS_VALID','new_original_signature_certificates':0,'NET_ORIGINAL_M3_SIGNED_PROOF_ADVANCEMENT':0,'mandatory_fixed_pattern_strategy_review':'COMPLETE','R1_R4_preserved':True,'h0_correction_preserved':True,'resources':res,'integrity':integrity};write(BASE/'certificate.json',cert)
    report=f'''# Pred02: memory retry succeeds; uniform predicate extension is false

**The retry completed within current caps and found an ORIGINAL LOW
counterexample to the proposed P1/P2 formula. Independently verified.**

At mu341,sigma=(3,1,1,0,...,0), terminal KEEP Score0 has A depth2,
B depth2,H=q=1,w=+1. Formula debt is2->0, so residual1+0-2=-1.
P2(source) is TRUE and P1(destination) is FALSE. A separate direct
endpoint evaluator confirms all three eligible total-four thresholds
give source2 and destination0. Both complete unchanged original LOW
roots accept the witness, the independent one under fresh P2V with no
factory call. All9544 assignments/widths, all147 fields at each endpoint
and independent parent-map A/B rotations are checked.

This absolutely refutes THIS proposed arbitrary-signature extension. The
signature's prior M3 theorem remains valid: its existing certificate has
debt2->1 and residual0. The positive nonclosed edge is no negative cycle
and does not refute M3. The new formula's failure occurs at total5, the
first possible population beyond its fully certified total-four basis.

The source reveals one anonymous node; the destination reveals five.
Every eligible total-four class bank lacks that destination pattern.
Hence the formula loses carried debt by falling back to psi0. Small
numerical debt does not justify a small population basis. This is the
structural obstruction obtained by examining the actual saved proofs,
not a reason to discard them or automatically raise the basis to5.

The new verifier streams basis values and uses a cleared in-place audit
bit instead of a second candidate-key set. It verifies1,119,626 basis
contributions/411118 attaining states, peaks at1,529,558 records (<2m),
then finds the first violation after10,248,314 explicit signed rows.
The old candidate construction and completed(4,1) audit were reused.
All later registered tests stop at this mathematical refutation.

For an absolute positive test, coverage must be proved. A separate new
structural proof and independent max-plus audit show every failure of
this fixed formula in the retained proof relation descends to population
<=13: rho=max(source-attaining four-unit tau,retained-prefix counts),
and every relevant prefix retains<=9 anonymous occurrences. All78 word
families/3360 risky fibers were audited;18 families are nonempty.
This supplies a complete bounded test specification, not an executed
universal PASS. An original negative needs source validation; the one
here has it. See CRITICAL_BUDGET_PROOF.md and PROOF_AUDIT.md.

R1-R4,h0 and all caps retained. All{len(pins)} prior pinned files remain
byte-identical; HEAD/tracked tree unchanged. New experimental/controller
CPU={charge}; cumulative uniform allowance{total}/7200, remaining
{7200-total}. Old signature-campaign ledger unchanged. No completed old
source/grammar/debt/root check rerun; no new canonical source queries.

BEFORE: resource UNKNOWN for(3,1,1), universal candidate OPEN.
RESULT: authorized bounded-memory retry; candidate REFUTED--EXACT on
the original relation, plus an independently audited critical-budget
reduction. AFTER: stop this formula, complete strategy review, preserve
all3761 old sector certificates. NET ORIGINAL M3 SIGNED PROOF ADVANCEMENT=0.
Full M3/Dynamic Optimality remain OPEN; no Stage04 or negative cycle.
'''
    with (BASE/'RESULT.md').open('x',encoding='utf-8') as f:f.write(report)
    cert['files']=[{'path':p.as_posix(),'sha256':sha(p)} for p in sorted(BASE.rglob('*')) if p.is_file()]
    write(BASE/'final_manifest.json',cert);print(json.dumps({k:v for k,v in cert.items() if k!='files'},indent=2),flush=True)
if __name__=='__main__':main()

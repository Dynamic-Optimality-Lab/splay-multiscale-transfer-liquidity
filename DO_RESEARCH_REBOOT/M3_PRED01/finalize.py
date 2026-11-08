"""Finalize exact restricted predicate theorem and the capped open extension."""
import json,subprocess,hashlib
from pathlib import Path
from entry import BASE,sha
def read(p):return json.loads(p.read_text())
def write(p,v):
    with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    assert not (BASE/'final_manifest.json').exists()
    r=read(BASE/'run_result.json');ctrl=read(BASE/'controller_exit.json');b=read(BASE/'basis.json');c0=read(BASE/'case_000/construction.json');a0=read(BASE/'case_000/audit.json');i0=read(BASE/'case_000/predicate_identity_audit.json');c1=read(BASE/'case_001/construction.json')
    assert r['status']=='STOPPED_ON_FIRST_NEW_CAP_OR_FAILURE' and ctrl['error'] is None
    assert r['passed_case_indices']==[0] and r['first_counterexample_case'] is None
    assert r['failure']['phase']=='audit' and r['failure']['index']==1 and 'record cap' in r['failure']['error']['message']
    assert b['signature_count']==705 and b['canonical_tables']==360
    assert a0['status']=='FINITE_EXACT_THRESHOLD_PREDICATES_SIGNED_PRESERVATION_PASS' and i0['status']=='INDEPENDENT_EXACT_THRESHOLD_PREDICATE_IDENTITY_PASS'
    assert i0['candidate_sha256']==c0['candidate_sha256']==sha(BASE/'case_000/candidate.json')
    assert a0['signed_rows_checked']==21530377 and a0['minimum_residual']==0 and a0['peak_conservative_records']<2000000
    assert a0['original_plus1_regression']['source_debt']==2 and a0['original_plus1_regression']['destination_debt']==1 and a0['original_plus1_regression']['residual']==0
    assert not (BASE/'case_001/predicate_identity_audit.json').exists() and not (BASE/'case_001/audit.json').exists()
    assert not (BASE/'case_002').exists() and not (BASE/'case_003').exists()
    assert c1['eligible_total4_signatures']==3 and c1['changed_pattern_states']==411118
    assert all(e['CPU_charged']<e['allocated_cap'] for e in r['events'])
    charge=r['new_child_process_CPU']+ctrl['whole_process_CPU_seconds'];total=665.75+charge;assert total<7200-5
    res={'prior_conservative_uniform_charge_retained':665.75,'new_child_process_CPU':r['new_child_process_CPU'],'new_controller_CPU_through_finally':ctrl['whole_process_CPU_seconds'],'new_measured_experimental_CPU':charge,'cumulative_accounted_CPU':total,'finite_CPU_ceiling':7200,'guaranteed_remaining_CPU':7200-total,'old_signature_campaign_ledger_unchanged':7195.203125,'CPU_caps_preserved':[120,300,300],'live_record_cap':2000000,'live_record_guard_triggered_in_second_case_independent_identity_audit':True,'failed_phase_peak_estimate_not_persisted':True,'no_record_cap_increase_or_retry':True,'canonical_query_limit':2000000,'actual_new_source_transition_queries':0,'old_grammar_debt_census_original_root_audits_repeated':0,'first_case_peak_conservative_records':a0['peak_conservative_records'],'new_B_product_graph_stored':False,'metadata_hashing_convention':'entry/final immutable-file bookkeeping excluded as previously'}
    write(BASE/'resources.json',res)
    deps=['RESEARCH_RULES.md','M3_UNIFORM03/resources.json','M3_ROW_AUD01/certificate.json','M3_ROW_AUD01/independent_verification.json','M3_ROW_AUD01/witness.json','M3_POP4_RISK07/certificate.json','M3_POP4_RISK01/SOURCE_LIFT.md','M3_POP5_RISK01/SOURCE_LIFT.md','M3_POP5_RISK01/certificate.json','M3_POP5_RISK01/s4100000000/relation.json','M3_POP5_RISK01/s4100000000/audit.json','M3_POP3_RISK01/REPRESENTATION_PROOF.md','M3_POP3_RISK01/representation_audit.json','M3_UNITPAIR01/B_bank.json','M3_TWOGAP_AUD01/reference.py','M3_OUT01/RESULT.md','06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER/PC_TYPED_DAG.py','06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_LOW_COMPILER.py','06_CERTIFICATES/DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE/STRICT_HIGH_COMPILER.py']
    for construction in (c0,c1):
        for e in construction['basis_dependencies']:
            for name in ('metadata.json','potential.json'):deps.append(str(Path(e['folder'])/name))
            deps.append(e['completion'])
    paths=sorted({(BASE.parent/p).resolve() for p in deps})
    write(BASE/'dependencies.json',{'completed_checks_reused_not_replayed':True,'files':[{'path':p.as_posix(),'sha256':sha(p)} for p in paths]})
    old=read(BASE/'entry_baseline.json');pins={p['path'] for p in old['files']}
    for i,p in enumerate(old['files']):
        assert sha(Path(p['path']))==p['sha256'],p['path']
        if (i+1)%1000==0:print(json.dumps({'old_files_verified':i+1,'total':len(pins)}),flush=True)
    additions=[p for p in BASE.parent.rglob('*') if p.is_file() and BASE not in p.parents and p.as_posix() not in pins]
    assert all('/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/' in p.as_posix() for p in additions),[p.as_posix() for p in additions]
    write(BASE/'concurrent_additions.json',{'not_math_dependencies':True,'files':[{'path':p.as_posix(),'sha256':sha(p)} for p in additions]})
    assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==old['head'] and not subprocess.check_output(['git','status','--short','--untracked-files=no'],text=True)
    integrity={'status':'PASS','old_files_unchanged':len(pins),'HEAD':old['head'],'tracked_tree_clean':True,'this_campaign_writes_confined_here':True,'unrelated_concurrent_U4_additions':len(additions)};write(BASE/'integrity.json',integrity)
    cert={'status':'EXPLICIT_POPULATION_THRESHOLD_PREDICATES_WITH_INDEPENDENT_RESTRICTED_PRESERVATION_PROOF','predicate_basis_signatures':705,'canonical_basis_tables':360,'predicate_kind':'shared B/alpha patterns with componentwise sigma thresholds','compact_syntactic_formula_found':False,'unconditionally_nested_P2_subset_P1':True,'unconditional_range_floor':'psi<=D4<=2','original_signed_preservation_proved_sigma':[4,1,0,0,0,0,0,0,0,0],'all_legal_masks_in_proved_sector':True,'arbitrary_signed_repetition_in_proved_sector':True,'new_explicit_signed_residuals':21530377,'minimum_residual':0,'realizable_plus1_obstruction_residual':0,'realizable_plus1_debt_transfer':[2,1],'next_sigma':[3,1,1,0,0,0,0,0,0,0],'next_candidate_status':'UNKNOWN_LIVE_RECORD_GUARD_DURING_INDEPENDENT_IDENTITY_AUDIT','universal_predicate_preservation':'OPEN','M3_status':'OPEN','DynamicOptimality_status':'OPEN','original_negative_cycle_certified':False,'new_original_sector_certificates':0,'NET_ORIGINAL_M3_PROOF_ADVANCEMENT':0,'R1_R4_preserved':True,'h0_correction_preserved':True,'no_old_census_or_original_root_replay':True,'resource_guard_stop_preserved':True,'resources':res,'integrity':integrity};write(BASE/'certificate.json',cert)
    report=f'''# Pred01: structural predicates with a proved restricted transfer

**Explicit sigma-dependent P1/P2 were obtained. Their signed preservation
is proved for sigma=(4,1,0,...,0), independently audited. Universal
preservation remains OPEN.** These are finite current-state pattern
predicates, not a compact closed structural classification.

Let K contain the705 already certified total-four multi-support signatures.
Let d_tau(B,a)=-J_tau(B,a) from their saved tables, including the certified
default/reflection rules. Define

    P_l(B,a,sigma) = [psi(B)>=l] OR
        [EXISTS tau in K: tau<=sigma AND d_tau(B,a)>=l], l=1,2.
    D4=I[P1]+I[P2], J4=-D4.

P2 subset P1 and psi<=D4<=2 hold by construction. In the successful
(4,1) sector only threshold(3,1) is eligible: the old total-four patterns
remain valid after one additional gap0 unit. No total-five labels were
used to fit the predicate. Independent upper-bound/attainment checks fix
all344030 changed patterns; then21,530,377 new signed residuals pass,
minimum0. Zero-debt sources and omitted/range-safe fibers are discharged
by the reused core-debt/source lemmas. The existing complete grammar and
original source audits are reused. This proves every original LOW rule
in that sector for every legal mask, hence arbitrary signed repetition.

On the verified original +1 edge, debt is2->1 and residual0. The old
sign-run formula's2->0 loss is repaired in this sector. Its original
root/witness audit was reused, not replayed. HIGH/h0/full-state glue
then supplies the existing mixed-cycle bound for this same sector.

The next candidate at(3,1,1) has411118 changed patterns and three eligible
thresholds, but its independent identity auditor hit the conservative
2m-live-record guard before completing identity or scanning signed rows.
Its status is UNKNOWN; no formula counterexample or negative cycle was
found. No retry, split, cap increase or later case ran. This stop follows
the registered first-cap rule in PRE_EXECUTION.md/RESEARCH_RULES.md.

The unresolved theorem is preservation across ALL population-compatibility
changes. Taking maxima of certificates for smaller edge relations does
not establish it. PREDICATES.md states the exact proof and its limits.
This already certified sector gains a formula-transfer result, not new
M3 coverage. NET ORIGINAL M3 PROOF ADVANCEMENT=0; all3761 old signature
certificates remain intact. M3/Dynamic Optimality OPEN, no Stage04.

R1-R4,h0,current caps retained. All{len(pins)} prior pinned files remain
byte-identical; Git HEAD/tracked tree unchanged. Experimental/controller
CPU={charge}; cumulative uniform allowance{total}/7200; guaranteed
remaining{7200-total}. Old signature ledger unchanged. No new canonical
source queries or repeated old grammar/debt/root checks.
'''
    with (BASE/'RESULT.md').open('x',encoding='utf-8') as f:f.write(report)
    cert['files']=[{'path':p.as_posix(),'sha256':sha(p)} for p in sorted(BASE.rglob('*')) if p.is_file()]
    write(BASE/'final_manifest.json',cert);print(json.dumps({k:v for k,v in cert.items() if k!='files'},indent=2),flush=True)
if __name__=='__main__':main()

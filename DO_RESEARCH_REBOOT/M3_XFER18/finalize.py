"""Immutable evidence publication and exact resource accounting."""
import json,subprocess
from pathlib import Path
from entry import BASE,lp,normal,sha
def read(name):return json.loads((BASE/name).read_text())
def write(name,obj):
    with (BASE/name).open('x',encoding='utf-8') as f:json.dump(obj,f,indent=2)
def main():
    a=read('audit_composition.json');assert not a['Step4_complete']
    assert a['status']=='SIGNED_COMPOSITION_PASS_FULL_STEP4_COVERAGE_UNPROVED'
    runs=[];total=763.703125
    for p in sorted(BASE.glob('run_*_result.json')):
        r=json.loads(p.read_text());c=read('controller_'+r['phase']+'_exit.json')
        charge=r['child_CPU']+c['whole_process_CPU_seconds'];total+=charge
        assert r['child_CPU']<r['allocated_CPU_cap']<=120
        runs.append({'phase':r['phase'],'status':r['status'],'child_CPU':r['child_CPU'],
          'controller_CPU':c['whole_process_CPU_seconds'],'charge':charge,
          'peak_working_set_bytes':r['peak_working_set_bytes_observed']})
    assert len(runs)==8 and total<7195
    assert sum(r['charge'] for r in runs if r['phase'].startswith('spread'))<120
    assert sum(r['charge'] for r in runs if r['phase'].startswith('central'))<120
    resources={'prior_uniform_CPU_charge':763.703125,'all_attempts_including_failures':runs,
      'new_compute_CPU':total-763.703125,'cumulative_accounted_CPU':total,'finite_CPU_ceiling':7200,
      'remaining_CPU':7200-total,'reserve':5,'old_signature_CPU_ledger_unchanged':7195.203125,
      'per_phase_caps':{'symbolic':120,'construction':300,'source_audit':300},
      'canonical_query_live_record_limit':2000000,'DAG_limit':4000000,'stored_edge_limit':5000000,'RAM_GiB':32,
      'new_finite_tests':0,'new_original_source_root_evaluations':0,'new_saved_psi_queries':0,
      'completed_semantic_checks_replayed':0,'resource_caps_preserved':True,
      'metadata_hashing_convention':'entry/final immutable-file bookkeeping excluded as previously'}
    write('resources.json',resources)
    entry=read('entry_baseline.json');baseline={r['path']:r['sha256'] for r in entry['files']}
    assert entry['extended_path_traversal']
    for i,(p,h) in enumerate(baseline.items()):
        assert sha(Path(p))==h,p
        if (i+1)%3000==0:print(json.dumps({'prior_files_unchanged':i+1}),flush=True)
    inherited=json.loads((BASE.parent/'M3_XFER17/dependencies.json').read_text())
    expected={r['path']:r['sha256'] for r in inherited['files']}
    expected.update(read('audit_spread_v2.json')['pinned_proof_hashes'])
    expected.update(read('audit_child.json')['proof_hashes'])
    for q,h in expected.items():assert sha(Path(q))==h,q
    write('dependencies.json',{'all_old_proofs_reused_not_replayed':True,
      'files':[{'path':p,'sha256':h} for p,h in sorted(expected.items())]})
    additions=[]
    for ext in lp(BASE.parent).rglob('*'):
        if not ext.is_file():continue
        p=normal(ext)
        if BASE in p.parents or p.as_posix() in baseline:continue
        additions.append({'path':p.as_posix(),'sha256':sha(p)})
    write('concurrent_additions.json',{'not_mathematical_dependencies':True,'files':additions})
    assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==entry['head']
    assert not subprocess.check_output(['git','status','--short','--untracked-files=no'],text=True)
    integrity={'status':'PASS','prior_files_unchanged':len(baseline),'extended_path_traversal_used':True,
      'mathematical_dependency_pins_unchanged':len(expected),'HEAD':entry['head'],'tracked_tree_clean':True,
      'our_writes_confined_to_this_new_campaign':True,'unrelated_concurrent_additions':len(additions)}
    write('integrity.json',integrity)
    certificate={'status':'NEW_UNIVERSAL_SIGNED_REGIONS_COMPOSED_FULL_STEP4_OPEN',
      'current_potential':'D_current; see debt_definition.json',
      'new_proved_families':['spread zero reset and returns for all masks',
        'cross-median unique marked child','central three-mark zero reset and returns for all masks'],
      'remaining_failure_exact_source_debt':'psi(core source)',
      'all_previously_proved_signed_LOW_rows_preserved':True,'HIGH_h0_preserved':True,
      'source_private_inventory_sigma_and_raw_fields_universally_quantified':True,
      'independent_symbolic_and_prose_audit':'PASS on the stated new theorems; not external review or full compiler formalization',
      'failed_attempts_corrected_and_preserved':['spread key8 identity','central unique-predecessor assertion'],
      'R1_R4_preserved':True,'corrected_h0':{'actual':0,'declared':18,'q':9,'weight':-3},
      'original147_O_127_M_SAME_midpoint_independent_scopes_HIGH_free_v_weak_LE_G_unused_fields_preserved':True,
      'new_finite_tests':0,'completed_semantic_checks_replayed':0,'new_original_negative_cycle_certified':False,
      'new_whole_signature_certificates':0,'remaining_H1_schematic_slots':36,
      'remaining_Gamma1_zero_slots':0,'all_remaining_marked_zero_edges_covered':False,
      'requested_full_Step4_achieved':False,'Step4_complete':False,'M3_status':'OPEN','DynamicOptimality_status':'OPEN',
      'missing_implication':a['unproved_exact_implication'],
      'old_one_prompt_stop_rule_not_used':True,'no_new_permission_required':True,
      'caps_not_the_reason_the_mathematical_coverage_implication_is_unproved':True,
      'resources':resources,'integrity':integrity}
    write('certificate.json',certificate)
    result=f'''# New uniform zero repayments; complete Step4 still unproved

The campaign continued through multiple necessary proof phases instead
of stopping at the first open sublemma. The new debt D_current preserves
all completed signed LOW rows and HIGH/h0. It repairs the saved spread
reset, proves its returns for EVERY legal marked mask, proves a general
cross-median unique-child rule, and repairs a second central reset with
an all-mask extension. All hold for arbitrary compatible signatures,
private inventories and raw fields. No finite population tests ran.

The exact-source-debt theorem further proves every surviving zero H1
failure starts at psi(source), never a newly raised auxiliary debt.
The new separate constructor/inverse/count/sign audits passed. Two
rejected intermediate assertions were corrected before acceptance;
their failed runs and charges remain. This is not external review or
full compiler formalization.

COMPLETE Step4 has NOT been established. The36 necessary seed/depth/
A-word slots remain parameterized OPEN obligations outside all proved
regions; they are not36 signatures or asserted counterexamples. All
Gamma0/Gamma1 zero rows and all unmarked-source LOW rows stay proved.
What is missing is a universal proof that every remaining marked zero
H1 edge satisfies D_current(target)>=psi(source)=D_current(source).
No theorem here supplies that exhaustive coverage implication. No new
original negative cycle is certified. M3/Dynamic Optimality remain OPEN.

The user requested full closure; the present work does not fulfill that
complete mathematical target. The old one-prompt stop was overridden;
no permission, resource cap or completed finite test is being used to
pretend the remaining implication has been decided. The records retain
the exact open status rather than promote local audit passes to Step4.

R1-R4 and all current caps/h0/full-state semantics remain. All
{len(baseline)} prior entry-listed files and{len(expected)} mathematical
dependency pins are unchanged, using extended Windows paths; HEAD and
tracked tree are unchanged. New CPU including both failed attempts=
{total-763.703125}; cumulative{total}/7200; remaining{7200-total}, with
reserve5. No old semantic checker, source root or saved psi query ran.

Proofs: SPREAD_REPAYMENT.md with SPREAD_CORRECTION.md,
EXACT_SOURCE_DEBT.md,CROSS_MEDIAN_CHILD.md,MASK_FREE_SPREAD.md,
CENTRAL_RESET.md with CENTRAL_AUDIT_CORRECTION.md,ALL_MASK_CENTRAL.md.
Composition and precise coverage limit: PROOF_AUDIT.md. Current formula:
debt_definition.json. Exact statuses: certificate.json/partition_update.json.
'''
    with (BASE/'RESULT.md').open('x',encoding='utf-8') as f:f.write(result)
    write('final_manifest.json',{'certificate':certificate,
      'files':[{'path':p.as_posix(),'sha256':sha(p)} for p in sorted(BASE.iterdir()) if p.is_file()]})
    print(json.dumps({'status':certificate['status'],'CPU':total,'remaining_CPU':7200-total,
      'integrity':integrity,'requested_full_Step4_achieved':False},indent=2),flush=True)
if __name__=='__main__':main()

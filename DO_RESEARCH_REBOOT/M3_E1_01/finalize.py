"""Immutable provenance and honest result publication; no mathematical tests."""
import json, subprocess
from pathlib import Path
from entry import BASE, sha

def read(name):
    return json.loads((BASE/name).read_text())

def write(name, obj):
    with (BASE/name).open('x', encoding='utf-8') as stream:
        json.dump(obj, stream, indent=2)

def main():
    assert not (BASE/'final_manifest.json').exists()
    er, ec = read('e1_run_result.json'), read('e1_controller_exit.json')
    cr, cc = read('capacity_run_result.json'), read('capacity_controller_exit.json')
    ea, ca = read('e1_audit.json'), read('capacity_audit.json')
    assert er['status']==cr['status']=='PASS'
    assert er['error'] is ec['error'] is cr['error'] is cc['error'] is None
    assert ea['status']=='UNIVERSAL_E1_AUGMENTATION_AUDIT_PASS'
    assert ca['status']=='UNIVERSAL_PUBLIC_CAPACITY_AUDIT_PASS'
    assert ca['E1_gate_passed_before_outside_phase']
    for a in (ea,ca):
        assert a['new_finite_population_tests']==a['new_source_transition_queries']==a['new_original_root_evaluations']==0
        assert not a['whole_source_formalization_claimed']
    assert ca['U_source_admissibility_qualification_required'] and not ca['seed_Lambda_globally_proved']
    assert not ca['Score_bearing_H2_normalization_preservation_proved']
    for r in (er,cr):
        assert r['child_CPU']<r['allocated_cap']<=120
    charge=er['child_CPU']+ec['whole_process_CPU_seconds']+cr['child_CPU']+cc['whole_process_CPU_seconds']
    total=755.203125+charge
    assert total<7200-5
    resources={
        'prior_uniform_CPU_charge_retained':755.203125,
        'new_E1_symbolic_checker_CPU':er['child_CPU'],
        'new_E1_controller_CPU_through_finally':ec['whole_process_CPU_seconds'],
        'new_capacity_symbolic_checker_CPU':cr['child_CPU'],
        'new_capacity_controller_CPU_through_finally':cc['whole_process_CPU_seconds'],
        'new_compute_CPU':charge,'cumulative_accounted_CPU':total,
        'finite_CPU_ceiling':7200,'guaranteed_remaining_CPU':7200-total,
        'reserve':5,'old_signature_campaign_ledger_unchanged':7195.203125,
        'new_finite_population_tests':0,'new_source_transition_queries':0,
        'new_original_root_evaluations':0,'new_label_fits':0,
        'old_completed_certification_checks_repeated':0,'new_bank_censuses':0,
        'current_caps_preserved':True,'symbolic_phase_CPU_cap':120,
        'construction_CPU_cap':300,'audit_source_CPU_cap':300,
        'canonical_query_and_live_record_limit':2000000,'DAG_limit':4000000,
        'stored_edge_limit':5000000,'RAM_GiB_limit':32,
        'metadata_hashing_convention':'entry/final immutable-file bookkeeping excluded as previously',
    }
    write('resources.json',resources)
    dependency_names=[
        'RESEARCH_RULES.md','M3_EXPOSURE02/HELPER_REDUCTION.md',
        'M3_EXPOSURE02/ADDENDUM_RANGE_ARGUMENT.md','M3_EXPOSURE02/PUBLIC_DEBT_AUDIT.md',
        'M3_EXPOSURE02/resources.json','M3_AER01/RESULT.md',
        'M3_POP5_RISK01/SOURCE_LIFT.md','M3_POP4_RISK01/SOURCE_LIFT.md',
        'M3_POP3_RISK01/REPRESENTATION_PROOF.md','M3_PRED02/PROOF_AUDIT.md',
        'M3_PRED02/independent_original_verification.json',
        'M3_COMB_AUD01/AUDIT_REPORT.md','M3_UNITPAIR01/B_bank.json',
        '06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE/IAGS_WSIGN02A_ZERO_COST_IMPOSSIBILITY/IAGS_11G_S03_M3_LDR01_LOW_DEFICIT_RUN_REPAYMENT.md',
        '06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_LOW_COMPILER.py',
        '06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_B_CONTROLLER.py',
        '06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_INVENTORY.py',
        '06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER/PC_B_CONTROLLER.py',
        '06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER/PC_ROTATION_INTERPRETER.py',
    ]
    write('dependencies.json',{'completed_proofs_reused_not_replayed':True,'files':[{'path':(BASE.parent/n).as_posix(),'sha256':sha(BASE.parent/n)} for n in dependency_names]})
    old=read('entry_baseline.json');pins={e['path'] for e in old['files']}
    for index,e in enumerate(old['files']):
        assert sha(Path(e['path']))==e['sha256'],e['path']
        if (index+1)%1000==0:
            print(json.dumps({'prior_files_unchanged':index+1,'total':len(pins)}),flush=True)
    additions=[p for p in BASE.parent.rglob('*') if p.is_file() and BASE not in p.parents and p.as_posix() not in pins]
    assert all('/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/' in p.as_posix() for p in additions),[p.as_posix() for p in additions]
    write('concurrent_additions.json',{'not_mathematical_dependencies':True,'files':[{'path':p.as_posix(),'sha256':sha(p)} for p in additions]})
    assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==old['head']
    assert not subprocess.check_output(['git','status','--short','--untracked-files=no'],text=True)
    integrity={'status':'PASS','old_files_unchanged':len(pins),'HEAD':old['head'],'tracked_tree_clean':True,'this_campaign_writes_confined_here':True,'unrelated_concurrent_U4_additions':len(additions)}
    write('integrity.json',integrity)
    certificate={
        'status':'UNIVERSAL_E1_AUGMENTATION_AND_H1_CAPACITY_PROVED_INDEPENDENTLY_AUDITED',
        'E1_theorem_scope':'each original H1 inequality individually, all signatures, public real debt in[0,2]',
        'E1_augmentation':'D_new=max(D,1_E1)',
        'E1_inventory_independent':True,'E1_needs_psi_floor':False,
        'capacity_augmentation':'D_new=max(D,c), c=min(2,min_visible_targets(w+psi(core_splay_target)))',
        'capacity_requires_floor':'D>=psi',
        'upper_U':'min(2,min_visible_targets(w+2))',
        'necessary_U_domain':'original source-admissible states only',
        'integer_H1_normal_form':'max(psi,c)<=D<=U on admissible sources',
        'depth8_visible_marked_target':'every feasible range-two H1 debt is0 at source',
        'depth6_7_visible_marked_target':'every feasible range-two H1 debt is at most1 at source',
        'seed_Lambda_uniform_validity':'OPEN',
        'full_public_debt_constructed':False,
        'Score_bearing_Gamma1_H2_augmentation_preservation':'OPEN',
        'initially_Score_empty_helpers':'completed H1/range reduction reused',
        'M3_status':'OPEN','DynamicOptimality_status':'OPEN',
        'new_signature_certificates':0,'original_negative_cycle_certified':False,
        'new_finite_tests':0,'R1_R4_preserved':True,'h0_correction_preserved':True,
        'whole_compiler_formalization_claimed':False,
        'NET_ADVANCEMENT':'safe public E1/c clauses, H1 integer normalization and forced local debt bounds; coupled transfer and Score-bearing helpers remain',
        'resources':resources,'integrity':integrity,
    }
    write('certificate.json',certificate)
    report=f'''# E1 augmentation proved; outside-E1 capacity bounds proved

E1 augmentation is PROVED--UNIVERSAL for ORIGINAL H1 inequalities and
passed its independent symbolic audit before the outside phase began.
For any public0<=D<=2, D_new=max(D,1_E1) preserves each previously valid
H1 inequality. E1 is the public condition that every observed marked
nonroot target has B depth<=3. Its exits have w>=1. Newly raised source
debt1 is therefore safe, independently of private inventories/signatures.
For integer predicates, P1_new=P1 OR E1 and P2_new=P2.

Outside E1, the separately audited public capacity construction is

    c=min(2,min_visible_targets(w+psi(destination_core))),
    U=min(2,min_visible_targets(w+2)), Lambda=max(psi,c).

For D>=psi, raising D to max(D,c) preserves its valid H1 inequalities.
On source-admissible states U is necessary. A visible target at B depth8
forces debt0; depth6/7 caps debt at1. Feasible H1 debts can be rounded
down and augmented into the integer interval[Lambda,U]. No private
inventory or history is read by these formulas.

The explicit seed Lambda has only the following POSSIBLE failing H1
types: weight0 with source psi1/2, or weight1 with source psi2, always
c(source)<psi(source). No such edge was experimentally tested, and no
universal preservation claim for the seed is made. Fixed source values
still impose destination conditions. A full public debt is NOT built.

The completed initially Score-empty helper theorem is reused. Preservation
of Score-bearing Gamma1 H2 constraints under the augmentations remains
OPEN. Consequently H1 normalization is not claimed safe for all M3 LOW
edges. M3 and Dynamic Optimality remain OPEN; no new sector certificate
or original negative cycle is claimed.

See E1_THEOREM.md for the principal proof, OUTSIDE_E1.md for the subsequent
capacity/normal-form proof, and PROOF_AUDIT.md for quantifiers, source
semantics, dependencies, edge cases and independent audit limits. The
audits use arbitrary symbolic variables and source-AST provenance; they
are not a full compiler formalization. Completed proofs were reused;
finite tests/source-transition queries/original-root evaluations=0.

R1-R4 and current caps preserved, including corrected h0 and full147-O/
127-M closure. All{len(pins)} pinned prior files and Git HEAD/tracked
tree remain unchanged. New charged symbolic/controller CPU={charge}s;
uniform ledger={total}/7200s; remaining={7200-total}s including reserve.
'''
    with (BASE/'RESULT.md').open('x',encoding='utf-8') as stream:
        stream.write(report)
    certificate['files']=[{'path':p.as_posix(),'sha256':sha(p)} for p in sorted(BASE.rglob('*')) if p.is_file()]
    write('final_manifest.json',certificate)
    print(json.dumps({'status':certificate['status'],'M3':'OPEN','new_compute_CPU':charge,'cumulative_CPU':total,'remaining_CPU':7200-total,'integrity':integrity},indent=2),flush=True)

if __name__=='__main__':
    main()

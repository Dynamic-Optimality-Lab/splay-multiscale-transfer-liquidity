"""Append-only SE02 restricted-result, resource and preservation publication."""
import hashlib,json,subprocess,time
from datetime import datetime,timezone
from pathlib import Path
B=Path(__file__).resolve().parent
ROOT=B.parent.parent
def xp(p):return Path('\\\\?\\'+str(p.resolve()))
def read(p):return json.loads(xp(p).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(xp(p).read_bytes()).hexdigest()
def write(n,d):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(d,f,indent=2)
start=time.process_time();entry=read(B/'entry.json');inherited=read(B/'dependency_pins.json');pins=inherited['pins']
for p in pins:assert sha(ROOT/p['path'])==p['sha256'],p['path']
assert sha(Path(inherited['user_directive_path']))==inherited['user_directive_sha256']
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
assert head==entry['head']
assert not subprocess.check_output(['git','status','--short','--untracked-files=no'],cwd=ROOT,text=True).strip()
attempts=[]
for path in sorted(B.glob('run_*_result.json')):
    p=read(path);c=read(B/('controller_'+p['phase']+'_exit.json'))
    assert p['termination'] is None and p['child_CPU']<p['allocated_CPU_cap']
    assert p['peak_working_set_bytes_observed']<entry['memory_cap_bytes']
    attempts.append({'phase':p['phase'],'status':p['status'],'child_CPU':p['child_CPU'],
      'whole_controller_CPU':c['whole_process_CPU_seconds'],
      'charged_CPU':p['child_CPU']+c['whole_process_CPU_seconds'],'child_cap':p['allocated_CPU_cap'],
      'error':p['error'],'peak_working_set_bytes_observed':p['peak_working_set_bytes_observed']})
assert {p['phase'] for p in attempts}=={'derivation','independent','independent_v2'}
by={p['phase']:p for p in attempts}
assert by['derivation']['status']==by['independent_v2']['status']=='PASS'
failed=by['independent'];assert failed['status']=='FAILED_OR_UNKNOWN'
assert failed['error']['type']=='AssertionError' and 'if f-e=-1' in failed['error']['message']
assert read(B/'AUDIT_RETRY_NOTE.json')['failed_result_not_promoted']
audit_CPU=by['independent']['charged_CPU']+by['independent_v2']['charged_CPU']
assert audit_CPU<300 and by['derivation']['charged_CPU']<120
assert by['independent_v2']['child_cap']==297
new=sum(p['charged_CPU'] for p in attempts);total=entry['prior_uniform_CPU']+new
assert total+entry['required_reserve']<7200
p=read(B/'derivation.json');a=read(B/'independent_audit_v2.json')
assert a['status']=='INDEPENDENT_SE02_MATHEMATICAL_AND_SOURCE_AUDIT_PASS'
assert a['protected_compensation']=='PROVED_RESTRICTED_SOURCE_GEOMETRIC_CLASS'
assert a['strictly_outside_CD5_and_core_le7']
assert not a['favorable_key_selection_proved'] and not a['uniform_support_induction_proved']
assert not a['unrestricted_CD_proved'] and not a['original_CD_counterexample_claimed']
assert a['new_finite_tests']==a['new_solver_queries']==a['new_original_root_queries']==a['completed_semantic_checks_replayed']==0
docs=['FOUR_RULE_GATE.md','ERASURE_ALIGNMENT.md','ROTATION_INTERFERENCE.md',
 'PROTECTED_COMPENSATION.md','SIX_KEY_CORE8_FAMILY.md','STRESS_TESTS.md','PROOF_AUDIT.md','BEFORE_RESULT_AFTER.md']
for n in docs:assert (B/n).is_file() and (B/n).stat().st_size>0
resources={'prior_sealed_uniform_CPU':entry['prior_uniform_CPU'],
 'new_CPU_including_failed_attempt_and_whole_controllers':new,'cumulative_uniform_CPU':total,
 'global_allowance':7200,'remaining_CPU_including_reserve':7200-total,'required_reserve':5,
 'attempts':attempts,'phase_groups':[{'name':'symbolic_derivation','cap':120,'charged_CPU':by['derivation']['charged_CPU']},
   {'name':'independent_audit_including_retry','cap':300,'charged_CPU':audit_CPU}],
 'old_signature_ledger_unchanged':7195.203125,'no_cap_increase_or_allowance_renewal':True,
 'canonical_query_cap':2000000,'new_canonical_queries':0,'live_record_cap':2000000,'new_live_graph_records':0,
 'input_DAG_cap':4000000,'new_compiled_input_DAG_nodes':0,'stored_edge_cap':5000000,'new_stored_graph_edges':0,
 'memory_cap_bytes':32*1024**3,'per_phase_wall_cap_hours':12,'proof_object_bytes':a['proof_object_bytes'],
 'new_finite_tests':0,'completed_semantic_checks_replayed':0,
 'metadata_bookkeeping_excluded_by_inherited_convention':True}
write('resources_final.json',resources)
write('SE02_CERTIFICATE.json',{
 'status':'PROVED_RESTRICTED_SOURCE_EXACT_SIGNED_ERASURE_COMPENSATION',
 'general_accounting':'aligned R=R_z-Delta; Delta=direct erased-key sum + signed other-KEEP interference',
 'general_accounting_domain':p['general_domain'],'alignment':p['alignment'],
 'compensation_theorem':p['protected_theorem'],'new_original_family':p['new_family'],
 'principal_six_key_result':'for guarded walks with at most six genuine keys, Q_B<=2A-2m by source contraction and sealed CD(5)',
 'strict_new_entry_domain':'all-m/all-fringe six-genuine-key/core8 family, outside CD(5) and core<=7',
 'global_historical_bank_novelty_claimed':False,
 'proofs':docs,'independent_audit':'independent_audit_v2.json','resources':'resources_final.json',
 'dependency_pins':'dependency_pins.json','new_finite_tests':0,'completed_semantic_checks_replayed':0,
 'R1_R4_preserved':True,'frozen_nine_core_graph_modified':False,'matching_terminal_modified':False,'Bank25':25,
 'uniform_support_induction_proved':False,'unrestricted_CD_proved':False,'Dynamic_Optimality_proved':False,
 'remaining_obligation':'nonresetting/interleaved erasure compensation and a source completeness/key-selection argument for all required walks',
 'audit_scope':'separate symbolic/source/physical-reservation audit; completed premises reused; not external review or whole-compiler formalization',
 'restricted_publication_gates':{'source_compensation':'PASS','new_six_key_core8_family':'PASS',
   'independent_complete_audit_v2':'PASS','failure_record_preserved_and_charged':'PASS',
   'resource_groups':'PASS','inherited_hashes':'PASS','HEAD_tracked_tree':'PASS'},
 'universal_CD_publication_gate':'OPEN_NOT_PROVED'})
write('PRESERVATION_AUDIT.json',{
 'R1_original_global_scope_preserved_and_remaining_open':True,'R2_original_source_weights_and_full_closure':True,
 'R3_no_architecture_observable_graph_solver_or_cap_change':True,'R4_restricted_and_global_claims_distinguished':True,
 'old_CD5_and_all_partial_seals_unchanged':True,'matching_terminal_frozen':True,'Bank25':25,
 'declared_input_hashes_verified':len(pins),'user_directive_pin_verified':True,
 'all_failed_and_successful_CPU_charged':True,'no_finite_tests':True,'no_old_semantic_checks_replayed':True,
 'HEAD':head,'tracked_tree_clean':True})
write('CURRENT_STATE.json',{'SE02':'PROVED_RESTRICTED_SIGNED_ERASURE_TRANSFER',
 'CD5':'SEALED_PROVED_UNCHANGED','new_coverage':'protected erasure class including six genuine keys/core8',
 'general_signed_interference_bound':'OPEN','uniform_support_induction':'OPEN','unrestricted_CD':'OPEN',
 'favorable_key_selection_assumed':False,'matching_terminal':'FROZEN','Bank25':25,
 'cumulative_uniform_CPU':total,'remaining_CPU_including_reserve':7200-total,
 'next_obligation':'source compensation for nonresetting/interleaved erasures and exhaustive residual coverage'})
result=f'''# SE02: a restricted source-exact compensation mechanism proved

**PROVED and separately audited:** protected two-run erasure compensation.
The source guard is geometric/mode-based, with no residual inequality assumed.
Each protected block has direct marginal1 and positive indirect return marginal1.
The two bits of its FIRST real A z-event pay those demands injectively. Deleting
the whole paired-identity block produces a legal smaller-support backbone;
its CD(5) invocation counts none of the reserved block events.

For m protected blocks, exact source identities give

    A=A0+2m, Q_full=Q0+2m, Q_erased=Q0,
    D=J=m, Delta=2m, Q_full<=2A-2m.

The six-genuine-key specialization is unconditional using the sealed CD(5)
backbone. The symbolic family gamma_m=(Dz,Kz,Kb1)^m W has EXACTLY six genuine
keys and fixed core8, arbitrary nine fringe BSTs, and every m>=1. It is outside
both entry domains CD(5) and core<=7. Its totals are A=2m+8,Q=2m+2,Q_E=2 and
R=2m+14. No historical whole-bank novelty or Bank25 promotion is claimed.

The general aligned erasure identity and direct/indirect decomposition were
derived with all charges on the SAME actual closed interval and normalized by
the SAME L. Primitive rotations and integer parity give both interference
signs. For a protected block-boundary cut u=0,L=1. An active-B input cut has
first erased charge Q0+1, then recurrent Q0 (u=1,L=1); that transient is excluded
from compensation. All donors/consumers lie in the selected rotated period.

The inherited RR/LL hanger obstruction passes the payment rule. Arbitrary root
repetitions/DELETEs remain allowed. A missing producer, zigzag A return, or
third-key interleaving fails the stated guard, and is not silently promoted.

**Universal CD remains OPEN.** The rule is uniform in support only under its
explicit source guard and a proved smaller-support backbone. No theorem says
every required walk admits such a key/decomposition. The next obligation is
compensation for nonresetting/interleaved erasures and source-complete coverage.

Independent audit:925 inherited pins plus the directive, eight universal affine
schemas, original source free-term identities, physical unit reservation,
six-key/core8 separation and complete transient review. The initial audit's
case-sensitive prose locator failed; its record is preserved and CPU charged.
The append-only complete v2 passes without a resource reset. This is an audit
within this campaign, not external peer review or full compiler formalization.

No finite tests, solver/source-root queries, old semantic-check replays, source/
graph edits or matching-terminal changes. R1-R4 and Bank25=25 remain intact.

New CPU including the failed audit and all controllers:{new:.6f}s.
Cumulative uniform CPU:{total:.6f}/7200s; remaining{7200-total:.6f}s including
reserve5. Symbolic group and BOTH audit attempts remain inside120/300 CPU caps;
all other current caps pass. Old signature ledger7195.203125 unchanged.

Theorem: PROTECTED_COMPENSATION.md. New family: SIX_KEY_CORE8_FAMILY.md.
Accounting: ERASURE_ALIGNMENT.md, ROTATION_INTERFERENCE.md.
Stress proofs: STRESS_TESTS.md. Audit: PROOF_AUDIT.md, independent_audit_v2.json.
Certificate: SE02_CERTIFICATE.json. Preservation/resources: PRESERVATION_AUDIT.json,
resources_final.json. The publication manifest pins every new artifact.
'''
with (B/'RESULT.md').open('x',encoding='utf-8') as f:f.write(result)
files=[{'file':p.name,'sha256':sha(p)} for p in sorted(B.iterdir()) if p.is_file()]
write('final_manifest.json',{
 'status':'SE02_RESTRICTED_COMPENSATION_PUBLISHED_ALL_GATES_PASS','files':files,
 'certificate':'SE02_CERTIFICATE.json','restricted_signed_compensation_proved':True,
 'six_key_core8_class_proved':True,'uniform_support_induction_proved':False,'unrestricted_CD_proved':False,
 'all_reused_inputs_unchanged':True,'declared_input_pins_verified':len(pins),
 'R1_R4_preserved':True,'matching_terminal_modified':False,'Bank25':25,
 'new_finite_tests':0,'HEAD':head,'tracked_tree_clean':True,'cumulative_uniform_CPU':total,
 'sealed_UTC':datetime.now(timezone.utc).isoformat(),'metadata_CPU_excluded_for_publication':time.process_time()-start,
 'manifest_self_excluded_from_its_file_hash_list':True})
print(json.dumps({'status':'SE02_RESTRICTED_COMPENSATION_PUBLISHED_ALL_GATES_PASS',
 'new_CPU':new,'cumulative_uniform_CPU':total,'remaining_CPU':7200-total,
 'audit_group_CPU_including_retry':audit_CPU,'files_sealed':len(files),'universal_CD':'OPEN'}))

"""Publish only audited partial proofs. Global CD promotion is prohibited here."""
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
start=time.process_time();entry=read(B/'entry.json');pins=read(B/'dependency_pins.json')['pins']
for p in pins:assert sha(ROOT/p['path'])==p['sha256'],p['path']
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
assert head==entry['head']
assert not subprocess.check_output(['git','status','--short','--untracked-files=no'],cwd=ROOT,text=True).strip()
phases=[]
for path in sorted(B.glob('run_*_result.json')):
    p=read(path);c=read(B/('controller_'+p['phase']+'_exit.json'))
    assert p['status']=='PASS' and p['returncode']==0 and p['error'] is None and p['termination'] is None
    assert c['error'] is None and p['child_CPU']<p['allocated_CPU_cap']
    assert p['peak_working_set_bytes_observed']<entry['memory_cap_bytes']
    phases.append({'phase':p['phase'],'child_CPU':p['child_CPU'],
      'whole_controller_CPU':c['whole_process_CPU_seconds'],
      'charged_CPU':p['child_CPU']+c['whole_process_CPU_seconds'],
      'cap':p['allocated_CPU_cap'],'peak_working_set_bytes_observed':p['peak_working_set_bytes_observed']})
assert {p['phase'] for p in phases}=={'proofs','independent'}
assert next(p for p in phases if p['phase']=='proofs')['cap']==120
assert next(p for p in phases if p['phase']=='independent')['cap']==300
new=sum(p['charged_CPU'] for p in phases);total=entry['prior_uniform_CPU']+new
assert total+entry['required_reserve']<7200
a=read(B/'independent_audit.json');p=read(B/'proof_inventory.json')
assert a['status']=='INDEPENDENT_SYMBOLIC_PARTIAL_RESULTS_AUDIT_PASS'
assert not a['unrestricted_CD_proved'] and not p['unrestricted_CD_proved']
assert not a['uniform_support_induction_proved'] and not p['original_CD_counterexample_found']
assert a['signed_erasure_cost_bound']=='OPEN'
assert a['new_finite_tests']==a['new_solver_queries']==a['new_original_root_queries']==a['completed_semantic_checks_replayed']==0
resources={'prior_sealed_uniform_CPU':entry['prior_uniform_CPU'],
  'new_CPU_including_children_and_whole_controllers':new,'cumulative_uniform_CPU':total,
  'global_allowance':7200,'remaining_CPU_including_reserve':7200-total,'required_reserve':5,
  'per_phase':phases,'old_signature_ledger_unchanged':7195.203125,
  'no_old_phase_renewal_or_cap_increase':True,'canonical_query_cap':2000000,'new_canonical_queries':0,
  'live_record_cap':2000000,'new_live_graph_records':0,'input_DAG_cap':4000000,'new_compiled_input_DAG_nodes':0,
  'stored_edge_cap':5000000,'new_stored_graph_edges':0,'memory_cap_bytes':32*1024**3,
  'per_phase_wall_cap_hours':12,'proof_object_bytes':a['input_proof_object_bytes'],
  'new_finite_tests':0,'completed_semantic_checks_replayed':0,
  'metadata_bookkeeping_excluded_by_inherited_convention':True}
write('resources_final.json',resources)
write('PARTIAL_CERTIFICATE.json',{
  'status':'AUDITED_PARTIAL_RESULTS_UNRESTRICTED_CD_OPEN',
  'original_target':p['original_target'],'unrestricted_CD_proved':False,
  'uniform_support_induction_proved':False,'original_CD_counterexample_found':False,
  'proved_restricted_extension':p['positive_extension']['domain'],
  'proved_universal_subbridge':'support-erased histories have reachable fully closed recurrent outputs',
  'refuted_extension_mechanisms':[
    'fixed HIGH cap2C-q with next-genuine-KEEP segmentation and universal closure-preserving coverage',
    'same marked-height-six bit beyond core7',
    'unqualified nondecreasing-B-charge support erasure'],
  'remaining_open':p['first_open_bridge'],
  'documents':['HIGH_TRUNCATION_OBSTRUCTION.md','MARK_SUBSET_LIFT.md','SUPPORT_ERASURE_CLOSURE.md'],
  'independent_audit':'independent_audit.json','audit_explanation':'PROOF_AUDIT.md',
  'dependency_pins':'dependency_pins.json','resources':'resources_final.json',
  'CD5_existing_seal_unchanged':True,'R1_R4_preserved':True,'Bank25':25,
  'new_finite_tests':0,'completed_semantic_checks_replayed':0,'Dynamic_Optimality_proved':False,
  'audit_scope':'separate symbolic/source/quantifier audit reusing completed premises; not external review or whole-compiler formalization',
  'partial_publication_gates':{'named_proofs':'PASS','independent_audit':'PASS','phase_controllers':'PASS',
     'resources':'PASS','declared_input_hashes':'PASS','HEAD_tracked_tree':'PASS'},
  'unrestricted_CD_publication_gate':'FAIL_OPEN_SIGNED_SUPPORT_LIFT'})
write('CURRENT_STATE.json',{
  'CD5':'SEALED_PROVED_UNCHANGED','unrestricted_CD':'OPEN','uniform_support_lift':'OPEN',
  'positive_additional_coverage':p['positive_extension']['domain'],
  'support_erasure_closure':'PROVED','signed_marginal_bound':'OPEN',
  'fixed_HIGH_truncation_uniform_extension':'REFUTED_AT_STATED_SCOPE',
  'original_CD_counterexample_found':False,'frozen_G_AF_negative_cycle_found':False,
  'cumulative_uniform_CPU':total,'remaining_CPU_including_reserve':7200-total,
  'Dynamic_Optimality':'OPEN','Bank25':25})
result=f'''# Uniform support extension: audited progress, global CD OPEN

**Unrestricted CD is not proved or sealed.** The complete CD(5) base remains
unchanged. No negative original-CD cycle was found or claimed.

Three proof results were separately audited without finite tests:

1. **Positive extension:** the existing four-mark certificate extends by a
destination-witness subset argument to every original closed walk whose marked
B-core has at most7 nodes, regardless of its mark count. Together with CD(5),
this adds the six-/seven-genuine-key core<=7 cases. All ambient sizes, lengths,
DELETE support and fringe remain allowed. Larger cores remain outside this leaf.
The same copied bit fails at core8 by an exact two-RR source-term family.

2. **Uniform obstruction to naive M3 enlargement:** every BST with n>=2^14 has
a depth14 node. Repeatedly KEEP a deterministic such node in a diagonal pair;
finite-map recurrence gives a reachable fully closed period. Each access has
a=q=H=7, so true CD weight2a-q=7 while the unchanged HIGH surrogate6-q=-1.
This refutes nonnegative cycles for that hypothetical universally covering
larger-core graph. It does not change or refute the frozen nine-core graph,
and is not an original CD counterexample. The all-cap theorem uses depth4C+2.

3. **Support-erasure closure:** erasing one key's KEEP modes yields smaller-
support reachable closed auxiliary histories after a preperiod. The exact
cost identity is R=R_z-Delta_z. Induction supplies only R_z>=0; the marginal
Delta_z lacks an independent signed bound. The universal RR/LL hanger family
rejects an unqualified charge-monotone erasure rule. It does not reject every
possible r>=6-specific signed lifting theorem.

The remaining principal obligation is a source-exact signed reduction for the
true2A-Q weight on arbitrary support. Neither a fixed truncation nor recurrence
closure supplies it. Naming R_z>=Delta_z without proving it would assert the
original CD conclusion again. The global publication gate remains OPEN.

Audit:898 declared hashes, six universal affine schemas, two free source-term
identity schemas and separate quantifier/source/closure review. No research
engines were imported, no old semantic checks replayed, and no finite tests or
solver/root queries run. R1-R4, frozen source/graph and Bank25=25 remain.
The audit is within this campaign, not external peer review or full compiler
formalization.

Charged CPU:{new:.6f}s new; cumulative{total:.6f}/7200s, remaining{7200-total:.6f}s
including reserve5. All existing caps passed; no allowance was renewed.

Proofs: HIGH_TRUNCATION_OBSTRUCTION.md, MARK_SUBSET_LIFT.md,
SUPPORT_ERASURE_CLOSURE.md. Audit: PROOF_AUDIT.md, independent_audit.json.
Publication record: PARTIAL_CERTIFICATE.json. Resource ledger: resources_final.json.
These artifacts are partial results, not a certificate of unrestricted CD.
'''
with (B/'RESULT.md').open('x',encoding='utf-8') as f:f.write(result)
files=[{'file':f.name,'sha256':sha(f)} for f in sorted(B.iterdir()) if f.is_file()]
write('final_manifest.json',{
  'status':'AUDITED_PARTIAL_RESULTS_PUBLISHED_UNRESTRICTED_CD_OPEN','files':files,
  'unrestricted_CD_complete':False,'original_CD_counterexample_found':False,
  'CD5_existing_seal_unchanged':True,'verified_declared_input_pins':len(pins),
  'all_reused_inputs_unchanged':True,'HEAD':head,'tracked_tree_clean':True,
  'R1_R4_preserved':True,'new_finite_tests':0,'Bank25':25,'cumulative_uniform_CPU':total,
  'Dynamic_Optimality_proved':False,'sealed_UTC':datetime.now(timezone.utc).isoformat(),
  'metadata_CPU_excluded_for_publication':time.process_time()-start,
  'manifest_self_excluded_from_its_file_hash_list':True})
print(json.dumps({'status':'AUDITED_PARTIAL_RESULTS_PUBLISHED_UNRESTRICTED_CD_OPEN',
  'new_CPU':new,'cumulative_uniform_CPU':total,'remaining_CPU':7200-total,'files_sealed':len(files)}))

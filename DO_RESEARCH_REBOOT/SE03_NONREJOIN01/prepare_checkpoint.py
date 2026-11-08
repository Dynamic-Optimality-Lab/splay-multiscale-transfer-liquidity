"""Integrity/resource checkpoint only; no proof checks or source executions."""
import datetime,hashlib,json,subprocess,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
start=time.process_time()
def xp(p):return Path('\\\\?\\'+str(p.resolve()))
def read(p):return json.loads(xp(p).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(xp(p).read_bytes()).hexdigest()
def write(n,d):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(d,f,indent=2)
def prose(n,s):
    with (B/n).open('x',encoding='utf-8') as f:f.write(s)
pins=read(B/'dependency_pins.json')['pins']
for p in pins:assert sha(ROOT/p['path'])==p['sha256'],p['path']
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
assert head==read(B/'entry.json')['head']
assert not subprocess.check_output(['git','status','--short','--untracked-files=no'],cwd=ROOT,text=True).strip()
groups={'symbolic':{'cap':120,'CPU':0},'independent':{'cap':300,'CPU':0}};attempts=[]
for path in sorted(B.glob('run_*_result.json')):
    d=read(path);phase=d['phase'];c=read(B/('controller_'+phase+'_exit.json'))
    assert d['status']=='PASS' and not d['error'] and not c['error']
    charge=d['child_CPU']+c['whole_process_CPU_seconds']
    group='independent' if phase.startswith('independent') else 'symbolic'
    groups[group]['CPU']+=charge
    attempts.append({'phase':phase,'status':d['status'],'child_CPU':d['child_CPU'],
        'whole_controller_CPU':c['whole_process_CPU_seconds'],'charged_CPU':charge,
        'allocated_child_cap':d['allocated_CPU_cap'],'group':group,
        'peak_working_set_bytes_observed':d['peak_working_set_bytes_observed']})
for g in groups.values():assert g['CPU']<g['cap']
new=sum(a['charged_CPU'] for a in attempts);prior=read(B/'entry.json')['prior_uniform_CPU'];total=prior+new
assert total<7195
assert all(a['peak_working_set_bytes_observed']<=32*1024**3 for a in attempts)
for n in ['independent_audit01.json','independent_audit02.json','independent_audit03.json']:
    a=read(B/n);assert a['status'].startswith('PASS')
    assert a['unrestricted_CD'] is False and a['support_induction'] is False
resource={'prior_sealed_uniform_CPU':prior,'new_CPU_including_all_children_and_whole_controllers':new,
    'cumulative_uniform_CPU':total,'global_allowance':7200,'remaining_CPU_including_reserve':7200-total,
    'required_reserve':5,'combined_phase_groups':groups,'attempts':attempts,
    'resource_cap_reached':False,'no_cap_reset_or_renewal':True,'old_signature_ledger_unchanged':7195.203125,
    'canonical_query_cap':2000000,'new_canonical_queries':0,'live_record_cap':2000000,'new_live_records':0,
    'input_DAG_cap':4000000,'new_compiled_input_DAG_nodes':0,'stored_edge_cap':5000000,'new_stored_edges':0,
    'memory_cap_bytes':32*1024**3,'per_phase_wall_cap_hours':12,'new_finite_tests':0,'old_semantic_rows_replayed':0,
    'metadata_bookkeeping_excluded_by_inherited_convention':True}
write('resources_checkpoint.json',resource)
state={'campaign':'SE03_NONREJOIN01','status':'OPEN_UNRESOLVED_NOT_SUCCESSFULLY_COMPLETED',
    'requested_completion_gate_satisfied':False,'CD5':'SEALED_UNCHANGED','uniform_signed_repayment':'OPEN',
    'uniform_key_selection_or_coverage':'OPEN','uniform_support_induction':'OPEN','unrestricted_CD':'OPEN',
    'Dynamic_Optimality':'OPEN','genuinely_new_CD_coverage_established':False,'original_CD_counterexample_found':False,
    'new_six_key_regression':'fullcore9, erasedcore<=8, D0, J>=2m-2; old paired-compositional CD coverage',
    'remaining_auxiliary_funding_case':'six-key fullcore10/11 with erased five-key/core9',
    'checkpoint_reason':'Uniform source compensation/coverage not derived; no resource exhaustion or theorem completion claimed',
    'resource_cap_reached':False,'cumulative_uniform_CPU':total,'Bank25':25,'R1_R4_preserved':True,
    'matching_terminal_modified':False,'frozen_graph_modified':False,'no_finite_tests':True}
write('CURRENT_STATE.json',state)
write('SE03_CHECKPOINT_CERTIFICATE.json',{'status':'AUDITED_INTERMEDIATE_CLAIMS_ONLY_UNIFORM_TARGET_OPEN',
    'current_state':state,'independent_audits':['independent_audit01.json','independent_audit02.json','independent_audit03.json'],
    'corrections':['SE03_SOURCE_CONVENTION_CORRECTION.md','SE03_BLOCK_CLASSIFICATION_CORRECTION.md','SE03_DEPTH_VECTOR_CLARIFICATION.md'],
    'proof_sources':['SE03_EXACT_NONREJOINING_SOURCE_IDENTITIES.md','SE03_EXCURSION_RESERVATION_LEMMA.md',
        'SE03_CORE_DEFICIENCY_AND_LEAF_SELECTION.md','SE03_ROTATION_DISTANCE_OBSTRUCTION.md',
        'SE03_UNIFORM_B_PAIR_PROJECTION.md','SE03_NEGATIVE_SOURCE_BLOCK_PARTITION.md',
        'SE03_ZERO_DIRECT_PERSISTENT_INTERFERENCE.md','SE03_SIX_KEY_PERSISTENT_AMPLIFICATION.md',
        'SE03_INDUCTIVE_STARTUP_AND_SAFE_PIECES.md','SE03_DEEPEST_ACCESS_CORE_GRAMMAR.md','SE03_SUBSET_LIFT_AUDIT.md'],
    'not_a_universal_CD_certificate':True,'not_a_successful_terminal_result':True,'resources':'resources_checkpoint.json'})
prose('SE03_CHECKPOINT.md',f'''# SE03 remains open and has not met its completion gate

The requested uniform implication CD(r-1)=>CD(r) is NOT proved. No original
CD counterexample is found, and no resource cap has been reached. This is
an integrity checkpoint of intermediate results, not successful completion,
a partial-success seal, or a claim that the directive's terminal condition
has been met. The mathematical repayment/coverage obligation remains open.

The strongest new source obstruction is a six-genuine-key/core9 family
with full/erased B disagreement at every later retained boundary, D=0,
and aligned J>=2m-2 as m grows. Only two zero-double K6 occurrences are
erased. Thus a bounded local erasure fee cannot pay the continuing
interference. The original diagonal family is already covered by old
paired-closed components; no genuinely new CD-domain advancement is claimed.

Also established: exact signed cross-key transport; maximal-core even-depth
outer-same-side necessity; leaf-selected erased core<=8 for full six-key
core<=9; an exact negative-source-block partition; removable-excursion and
startup/safe-piece conditional funding; a local deepest-access core grammar;
and source obstructions to rotation-distance, interval-count and simple
maximum-profile potentials. Saved-certificate analysis proves499 guard
implications, with752 not proved by that subsumption rule. It proves no
universal witness-subset padding or larger-core coverage.

The remaining central theorem must independently fund continuing retained
A work (or construct a different valid smaller-support source reduction),
prove signed preservation through repeated nonrejoining transfers, and
provide source-complete key selection or coverage for arbitrary r. Full
six-key cores10/11 with five-key/core9 auxiliaries are still uncovered by
the new compensation arguments. Neither an unsupported marginal inequality
nor the existing bounded-support certificates discharge this obligation.

All997 inherited pins and entry HEAD are intact. R1-R4, source semantics,
frozen graph/h0 correction, matching-terminal and Bank25=25 are unchanged.
No finite tests, semantic source queries, new graphs or old-row replays.
Separate symbolic/source audits are within this campaign, not external
peer review or full compiler formalization. Read the three correction
notes together with the original intermediate proofs.

CPU {total:.6f}/7200 seconds; remaining {7200-total:.6f} including reserve5.
New charged CPU {new:.6f}; original symbolic group {groups['symbolic']['CPU']:.6f}/120,
independent group {groups['independent']['CPU']:.6f}/300. Metadata exclusion
follows the inherited convention. No budget exhaustion is used as an excuse
for the missing proof. Universal CD and Dynamic Optimality remain OPEN.
''')
prose('SE03_INTEGRITY_CHECKPOINT.md',f'''# Integrity checkpoint only

HEAD {head}; tracked tree clean. All{len(pins)} inherited declared pins
rehash exactly. Every new proof process and whole controller is charged;
all statuses are at their exact named scope. Resource caps are preserved.
No CPU cap was reached. The requested uniform proof gate is NOT satisfied.
No SE03 successful final result or Universal CD seal is published.

checkpoint_manifest.json hashes the append-only files present at this
checkpoint, excluding itself. The manifest is an integrity record, not
a proof of any OPEN obligation. No inherited file or status is rewritten.
''')
files=[{'file':p.name,'sha256':sha(p)} for p in sorted(B.iterdir()) if p.is_file()]
write('checkpoint_manifest.json',{'status':'OPEN_CHECKPOINT_NOT_A_SUCCESS_SEAL','files':files,
    'HEAD':head,'tracked_tree_clean':True,'inherited_pins_verified':len(pins),
    'requested_completion_gate_satisfied':False,'unrestricted_CD_proved':False,'support_induction_proved':False,
    'original_CD_counterexample_found':False,'resource_cap_reached':False,'cumulative_uniform_CPU':total,
    'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'metadata_CPU_excluded':time.process_time()-start,'self_excluded':True})
print(json.dumps({'status':'OPEN_CHECKPOINT_WRITTEN_NOT_SUCCESS','files_hashed':len(files),
    'cumulative_uniform_CPU':total,'resource_cap_reached':False,'unrestricted_CD':False}))

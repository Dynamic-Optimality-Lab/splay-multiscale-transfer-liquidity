"""Append-only resource/integrity checkpoint; full Step2 explicitly OPEN."""
import datetime,hashlib,json,subprocess,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent;start=time.process_time()
def xp(p):return Path('\\\\?\\'+str(p.resolve()))
def read(p):return json.loads(xp(p).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(xp(p).read_bytes()).hexdigest()
def out(n,d):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(d,f,indent=2)
def prose(n,s):
    with (B/n).open('x',encoding='utf-8') as f:f.write(s)
e=read(B/'entry.json');pins=read(B/'dependency_pins.json')['pins']
for q in pins:assert sha(ROOT/q['path'])==q['sha256'],q['path']
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
branch=subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()
assert head==e['head'] and branch=='coarse-double-branch'
assert not subprocess.check_output(['git','status','--short','--untracked-files=no'],cwd=ROOT,text=True).strip()
groups={g:{'inherited_CPU':v,'new_CPU':0,'cap':e['group_caps'][g]} for g,v in e['inherited_group_CPU'].items()}
attempts=[]
for path in sorted(B.glob('run_*_result.json')):
    r=read(path);c=read(B/('controller_'+r['phase']+'_exit.json'))
    assert r['status']=='PASS' and not r['error'] and not c['error']
    charge=r['child_CPU']+c['whole_process_CPU_seconds'];groups[r['group']]['new_CPU']+=charge
    attempts.append({'phase':r['phase'],'group':r['group'],'status':r['status'],
      'child_CPU':r['child_CPU'],'controller_CPU':c['whole_process_CPU_seconds'],'charged_CPU':charge,
      'allocated_child_cap':r['allocated_child_cap'],'peak_working_set_bytes_observed':r['peak_working_set_bytes_observed']})
for g in groups.values():
    g['combined_CPU']=g['inherited_CPU']+g['new_CPU'];assert g['combined_CPU']<g['cap']
new=sum(g['new_CPU'] for g in groups.values());total=e['prior_uniform_CPU']+new
assert total<7195 and all(x['peak_working_set_bytes_observed']<32*1024**3 for x in attempts)
scope=read(B/'persistent_and_scope_audit.json')
assert scope['Step2_complete'] is False and scope['original_CD_counterexample'] is False
resources={'prior_uniform_CPU':e['prior_uniform_CPU'],'new_CPU_all_children_and_whole_controllers':new,
 'cumulative_uniform_CPU':total,'global_allowance':7200,'remaining_CPU_including_reserve':7200-total,
 'required_reserve':5,'original_SE03_phase_groups':groups,'attempts':attempts,
 'resource_cap_reached':False,'cap_reset_or_renewal':False,'old_signature_ledger_unchanged':7195.203125,
 'canonical_query_cap':2000000,'new_canonical_queries':0,'live_record_cap':2000000,'new_live_graph_records':0,
 'input_DAG_cap':4000000,'new_compiled_input_DAG_nodes':0,'stored_edge_cap':5000000,'new_stored_graph_edges':0,
 'memory_cap_bytes':32*1024**3,'per_phase_wall_hours':12,'new_finite_tests':0,'source_engine_calls':0,
 'old_semantic_rows_replayed':0,'metadata_exclusion':'inherited provenance, source reads, file preparation and bookkeeping convention'}
out('resources_checkpoint.json',resources)
state={'campaign':'SE03_STEP2_REPAY02','status':'OPEN_NOT_SUCCESSFULLY_COMPLETED','Step2_complete':False,
 'requested_completion_gate_satisfied':False,'all_H1_q3_q4_hit_cases':'COVERED_WITHIN_FIXED_NINE_SCORE_CHART',
 'all_zero_plus1_hit_transfers':'COVERED_WITHIN_FIXED_CHART; future new debt must preserve these inequalities',
 'miss_H1_q3_q4':'OPEN','paired_q5_q1_miss_transfers':'OPEN','zero_plus1_miss_transfers':'OPEN',
 'source_cover':'recent-key windows; core11 cold components<=4 for recent5 replacement; core10 fixed9Score hits',
 'source_miss_identity':'chart residual plus dvirtual-dold-1 for one cold chain; alternative-chart debt difference for separate twigs',
 'normalized_chart_candidate':'REFUTED_ON_FULLY_CLOSED_PERSISTENT_CORE9_COMPARISON',
 'new_complete_scoped_class':'six-key B-return pulses without A reset, including exact-core9 auxiliary funding',
 'uniform_hit_run_theorem':'actual ambient n>=9, any total support, signed original open-run cost>=-2',
 'regression':'Omega_plus A48,QF32,QE24,D6,J2,u1,L1, full original slack64; P8 paid by eight fixed Step1 tail units',
 'original_CD_counterexample_found':False,'generic_width_two_debt_refuted':False,
 'uniform_support_induction':'OPEN','unrestricted_CD':'OPEN','Dynamic_Optimality':'OPEN',
 'novelty_against_all_old_compositions_claimed':False,
 'checkpoint_reason':'Complete signed miss compensation not derived; no cap exhaustion or successful completion claimed',
 'resource_cap_reached':False,'cumulative_uniform_CPU':total,'R1_R4_preserved':True,'Bank25':25,
 'frozen_graph_modified':False,'matching_terminal_modified':False,
 'h0_preserved':{'actual':0,'declared':18,'q':9,'weight':-3},'external_peer_review':False}
out('CURRENT_STATE.json',state)
prose('CHECKPOINT.md',f'''# Step2 remains OPEN

The full signed repayment theorem requested by the user is NOT proved.
No original negative CD cycle was found and no resource cap was reached.
This checkpoint is not a success seal or satisfaction of the completion gate.

The main completed reduction is UNIFORM_HIT_RUN_THEOREM.md. A run of hits
to the five recent KEEP keys has a fixed ancestor-closed tree of nine
ACTUAL Scores and signed source cost>=-2, uniformly in total support and
all ambient populations>=9. The unchanged local M3 predicates allow
unmarked Score leaves, so this covers core10 hits even at true-core9->8.
H1/q3,q4 hit inequalities and every zero/+1 hit transfer reuse the complete
old certificate. No finite test or graph extension proves this reduction.

The actual remaining issue is chart change at a MISS. Core11 recent4 has
core7; its two cold keys form two twigs or one same-side four-node chain.
The latter has exact signed residual d_virtual-d_old-1. The -1 is one
actual B double. No inherited theorem gives the sign of that term or of
the alternative-chart debt difference in the separate-twig case. Core10
miss comparisons and paired q5/1 negative/zero transfers remain too.
See OPEN_MISS_OBLIGATION.md for the complete surviving signed classes.

The accepted M3 D does not compose across charts by itself. Source-row-
preserving Hamiltonian and ray ceilings repair one previous obstruction,
but RAY_NORMALIZATION_AND_OBSTRUCTION.md proves their direct chart formula
still fails. PERSISTENT_OMEGA_EXTENSION.md places that failure inside an
actual permanently nonrejoining core11/core9 comparison. Its original
full source has A48,QF32 and POSITIVE slack64; it is not a CD counterexample.
It has u1,L1,QE24,D6,J2. Four identified tail A events supply eight bits
excluded from the fixed Step1 allocation and pay its eight unmatched
demands, with all common assignments retained. This proves repayment on
the source family, not a universal donor-existence theorem.

RETAINED_GAP_RESERVATION.md and B_RETURN_PULSE_EXTENSION.md close the
old core9 auxiliary funding gap for the complete B-return-pulse class,
without A reset/nearness. The genuine persistent nonreturning class is
not replaced by that control. No claim of novel complete CD coverage
against every inherited composition is made.

All{len(pins)} inherited pins rehash. HEAD {head}; branch {branch}; tracked
tree clean. R1-R4, Bank25=25, original source/graph/two sorts/midpoints,
weights/raw fields/private scopes, matching-terminal and corrected h0
remain intact. No finite populations, source engines, new weighted graph,
solver modifications or old semantic rows were executed. The separate
source/rotation audits are same-agent derivations, not external peer review
or a full compiler formalization. Unrun audit drafts have no PASS status.

CPU {total:.6f}/7200 seconds; remaining {7200-total:.6f} including reserve5.
Original group totals: symbolic {groups['symbolic']['combined_CPU']:.6f}/120,
independent {groups['independent']['combined_CPU']:.6f}/300. No cap reset or
budget exhaustion is invoked for the unresolved mathematical miss bound.
''')
files=[{'file':p.name,'sha256':sha(p)} for p in sorted(B.iterdir()) if p.is_file()]
out('checkpoint_manifest.json',{'status':'OPEN_CHECKPOINT_NOT_A_SUCCESS_SEAL','files':files,'HEAD':head,
 'branch':branch,'tracked_tree_clean':True,'inherited_pins_verified':len(pins),
 'Step2_proved':False,'unrestricted_CD_proved':False,'resource_cap_reached':False,
 'cumulative_uniform_CPU':total,'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'metadata_CPU_excluded':time.process_time()-start,'self_excluded':True})
print(json.dumps({'status':'OPEN_CHECKPOINT_NOT_SUCCESS','files_hashed':len(files),'pins_verified':len(pins),
 'cumulative_uniform_CPU':total,'groups':groups,'Step2_complete':False}))

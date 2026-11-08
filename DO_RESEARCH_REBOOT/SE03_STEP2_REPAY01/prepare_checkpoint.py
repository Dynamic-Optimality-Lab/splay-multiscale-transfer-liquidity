"""Append-only integrity and resource checkpoint; not a success publication."""
import datetime,hashlib,json,subprocess,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
start=time.process_time()
def xp(p):return Path('\\\\?\\'+str(p.resolve()))
def read(p):return json.loads(xp(p).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(xp(p).read_bytes()).hexdigest()
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def prose(n,s):
    with (B/n).open('x',encoding='utf-8') as f:f.write(s)
entry=read(B/'entry.json');pins=read(B/'dependency_pins.json')['pins']
for q in pins:assert sha(ROOT/q['path'])==q['sha256'],q['path']
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
branch=subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()
assert head==entry['head'] and branch=='coarse-double-branch'
assert not subprocess.check_output(['git','status','--short','--untracked-files=no'],cwd=ROOT,text=True).strip()
groups={g:{'inherited_CPU':v,'new_CPU':0,'cap':entry['group_caps'][g]} for g,v in entry['inherited_group_CPU'].items()}
attempts=[]
for path in sorted(B.glob('run_*_result.json')):
    d=read(path);c=read(B/('controller_'+d['phase']+'_exit.json'))
    if d['phase']=='composition':
        assert d['status']=='FAILED_OR_UNKNOWN'
        assert read(B/'run_composition_v2_result.json')['status']=='PASS'
    else:assert d['status']=='PASS' and not d['error'] and not c['error']
    charge=d['child_CPU']+c['whole_process_CPU_seconds']
    groups[d['group']]['new_CPU']+=charge
    attempts.append({'phase':d['phase'],'group':d['group'],'status':d['status'],
       'child_CPU':d['child_CPU'],'controller_CPU':c['whole_process_CPU_seconds'],
       'charged_CPU':charge,'allocated_child_cap':d['allocated_child_cap'],
       'peak_working_set_bytes_observed':d['peak_working_set_bytes_observed']})
manual=read(B/'manual_CPU_charge.json')
groups[manual['phase_group']]['new_CPU']+=manual['charged_CPU_seconds']
for g in groups.values():
    g['combined_CPU']=g['inherited_CPU']+g['new_CPU'];assert g['combined_CPU']<g['cap']
new=sum(g['new_CPU'] for g in groups.values());total=entry['prior_uniform_CPU']+new
assert total<7195
assert all(a['peak_working_set_bytes_observed']<32*1024**3 for a in attempts)
audits=['separate_audit.json','induction_audit.json','safe_levels_audit.json','density_audit.json','successor_audit.json','composition_v2_audit.json']
for name in audits:
    d=read(B/name);assert d['status'].startswith('PASS') and d['Step2_complete'] is False
resource={'prior_uniform_CPU':entry['prior_uniform_CPU'],'new_CPU_all_children_controllers_and_manual_charge':new,
    'cumulative_uniform_CPU':total,'global_allowance':7200,'remaining_CPU_including_reserve':7200-total,
    'required_reserve':5,'original_SE03_phase_groups':groups,'attempts':attempts,
    'manual_conservative_charge':manual,'resource_cap_reached':False,'cap_reset_or_renewal':False,
    'old_signature_ledger_unchanged':7195.203125,'canonical_query_cap':2000000,'new_canonical_queries':0,
    'live_record_cap':2000000,'new_live_records':0,'input_DAG_cap':4000000,'new_compiled_DAG_nodes':0,
    'stored_edge_cap':5000000,'new_stored_edges':0,'memory_cap_bytes':32*1024**3,'per_phase_wall_hours':12,
    'new_finite_tests':0,'new_source_engine_calls':0,'old_semantic_rows_replayed':0,
    'metadata_exclusion':'inherited provenance, file preparation and bookkeeping convention'}
out('resources_checkpoint.json',resource)
state={'campaign':'SE03_STEP2_REPAY01','status':'OPEN_NOT_SUCCESSFULLY_COMPLETED',
    'requested_completion_gate_satisfied':False,'Step1':'SEALED_UNCHANGED','Step2':'OPEN',
    'Step3_uniform_coverage':'OPEN','support_induction':'OPEN','unrestricted_CD':'OPEN','Dynamic_Optimality':'OPEN',
    'new_structural_theorems':['set growth at most2 distinct labels','closed-core subtree density',
      'maximal-core sorted marked/unmarked alternation','max-depth fan and mandatory q1 successor'],
    'new_source_repayment':'disjoint maximum-depth packets with Hsum>=ceil(r/2); all six-core11 H2/q5 negatives paid',
    'new_candidate':'width2 threshold4 on complete singleton/q5-pair source partition; baseline unproved',
    'remaining_core11_negatives':['singleton H1/q3','singleton H1/q4','q5+q1 packet Hsum2'],
    'remaining_core10_negatives':['H1/q3','H1/q4'],
    'remaining_transfers':'all corresponding zero/+1 obligations need one complete state-defined invariant',
    'new_original_CD_coverage':False,'original_CD_counterexample_found':False,
    'checkpoint_reason':'No global signed debt invariant or complete source repayment derived; not cap exhaustion',
    'resource_cap_reached':False,'cumulative_uniform_CPU':total,'R1_R4_preserved':True,'Bank25':25,
    'frozen_graph_modified':False,'matching_terminal_modified':False,
    'h0_preserved':{'actual':0,'declared':18,'q':9,'w':-3},'external_peer_review':False}
out('CURRENT_STATE.json',state)
prose('CHECKPOINT.md',f'''# Step2 is OPEN; this is not successful completion

The requested complete signed source repayment is NOT proved. No original
negative CD cycle was found. No resource cap was reached. This checkpoint
does not satisfy the user's completion gate and is not a Step2 success seal.

The strongest new uniform result is CLOSED_CORE_SUBTREE_DENSITY.md:
c_T<=2m_T-I[root marked] for every actual closed-core subtree. It implies
sorted marked/unmarked alternation for every maximal core2r-1. In the
six-key residual this leaves one necessary core11 mask and at most sixteen
core10 masks, without changing the frozen graph or claiming those masks
are sufficient for source realization.

MAXIMUM_DEPTH_SUCCESSOR_REPAYMENT.md then proves all full-depth source
doubles are LL/RR, gives their canonical fan destination, and forces the
next genuine B charge to1. This repays every negative H2/q5 block at six
keys, and every H1/q5 whose successor A cost is>=2, in disjoint actual
source packets. The H1/H1 pair retains deficit2. H1/q3 and H1/q4 also
remain. The core10 counterparts remain. Positive and zero transfers
cannot be omitted when combining these cases.

PAIRED_RANGE_TWO_TARGET.md gives the improved complete source cost
partition and exact remaining debt rules. The required width-two function
on its actual full-state boundaries is NOT constructed. Existing M3 is
still only a nine-core theorem. The new predicates and source restrictions
do not extend it to ten or eleven nodes by assumption.

The actual universally quantified Gamma source family refutes pointwise
repayment by each auxiliary macro's own reserve. Its two-block repair
identifies excluded DELETE-origin A bits. The separate audits verify full
paired closure, actual auxiliary recurrence, signed D/J, arbitrary gap
validity and persistent nonrejoining at every recurrent original boundary.
Its original CD inequality is already elementary; no novel complete CD
domain is claimed. General Gamma_r supplies only necessary range bounds.

HELPER_INDEPENDENT_SAFE_AUGMENTATION.md proves initial-depth target cover
through every anonymous helper and a safe operation preserving individually
valid inequalities. It supplies no globally feasible seed. Conditional
full-allocation exchange and cyclic ID transport preserve the fixed Step1
common assignments IF all remaining full demands are independently funded.

All{len(pins)} inherited pins rehash; HEAD {head}; branch {branch}; tracked
tree clean. R1-R4, Bank25=25, frozen source/graph, original weights/raw
states/private witnesses, matching-terminal and corrected h0 are intact.
No finite tests, new source engines, graph construction or old-row replay.
Audits are separate same-agent derivations, not external peer review or a
full source-compiler formalization. One capitalization-guard retry is
documented; its failed CPU is charged. An extra unbounded proof-term read
is conservatively charged1 CPU second, not hidden as metadata.

CPU {total:.6f}/7200 seconds; remaining {7200-total:.6f} including reserve5.
Original group totals: symbolic {groups['symbolic']['combined_CPU']:.6f}/120,
independent {groups['independent']['combined_CPU']:.6f}/300. No cap reset.
The unresolved mathematical invariant, not resource exhaustion, is the gap.
''')
files=[{'file':path.name,'sha256':sha(path)} for path in sorted(B.iterdir()) if path.is_file()]
out('checkpoint_manifest.json',{'status':'OPEN_CHECKPOINT_NOT_A_SUCCESS_SEAL','files':files,
   'HEAD':head,'branch':branch,'tracked_tree_clean':True,'inherited_pins_verified':len(pins),
   'requested_completion_gate_satisfied':False,'Step2_proved':False,'unrestricted_CD_proved':False,
   'resource_cap_reached':False,'cumulative_uniform_CPU':total,'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),
   'metadata_CPU_excluded':time.process_time()-start,'self_excluded':True})
print(json.dumps({'status':'OPEN_CHECKPOINT_NOT_SUCCESS','files_hashed':len(files),'inherited_pins_verified':len(pins),
     'cumulative_uniform_CPU':total,'groups':groups,'Step2_proved':False}))

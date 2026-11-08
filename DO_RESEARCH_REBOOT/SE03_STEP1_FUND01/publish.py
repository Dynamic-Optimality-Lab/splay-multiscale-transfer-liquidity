"""Publish the proved Step1 only; final provenance/resource bookkeeping."""
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
entry=read(B/'entry.json');pins=read(B/'dependency_pins.json')['pins']
for p in pins:assert sha(ROOT/p['path'])==p['sha256'],p['path']
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
assert head==entry['head']
assert not subprocess.check_output(['git','status','--short','--untracked-files=no'],cwd=ROOT,text=True).strip()
groups={g:{'inherited_CPU':v,'new_CPU':0,'cap':entry['group_caps'][g]} for g,v in entry['inherited_group_CPU'].items()}
attempts=[]
for p in sorted(B.glob('run_*_result.json')):
    r=read(p);c=read(B/('controller_'+r['phase']+'_exit.json'))
    assert r['status']=='PASS' and not r['error'] and not c['error']
    charge=r['child_CPU']+c['whole_process_CPU_seconds']
    groups[r['group']]['new_CPU']+=charge
    assert r['peak_working_set_bytes_observed']<=32*1024**3
    attempts.append({'phase':r['phase'],'group':r['group'],'status':r['status'],'child_CPU':r['child_CPU'],
       'whole_controller_CPU':c['whole_process_CPU_seconds'],'charged_CPU':charge,
       'allocated_child_cap':r['allocated_child_cap'],'peak_working_set_bytes_observed':r['peak_working_set_bytes_observed']})
for g in groups.values():
    g['combined_CPU']=g['inherited_CPU']+g['new_CPU'];assert g['combined_CPU']<g['cap']
new=sum(a['charged_CPU'] for a in attempts);total=entry['prior_uniform_CPU']+new
assert total<7195
audit=read(B/'independent_audit.json');der=read(B/'derivation.json')
assert audit['status']=='PASS_STEP1_UNIVERSAL_SOURCE_FUNDING_EXTRACTION' and audit['Step1_proved']
assert not audit['original_marginal_repayment_proved'] and not audit['uniform_coverage_proved'] and not audit['unrestricted_CD_proved']
assert der['status']=='PASS_UNIVERSAL_AFFINE_PROOF_SCHEMAS'
resource={'prior_uniform_CPU':entry['prior_uniform_CPU'],'new_CPU_all_children_and_whole_controllers':new,
    'cumulative_uniform_CPU':total,'global_allowance':7200,'remaining_CPU_including_reserve':7200-total,
    'required_reserve':5,'original_SE03_phase_groups':groups,'attempts':attempts,'cap_reset_or_renewal':False,
    'old_signature_ledger_unchanged':7195.203125,'canonical_query_cap':2000000,'new_canonical_queries':0,
    'live_record_cap':2000000,'new_live_records':0,'compiled_DAG_cap':4000000,'new_compiled_DAG_nodes':0,
    'stored_edge_cap':5000000,'new_stored_edges':0,'memory_cap_bytes':32*1024**3,'per_phase_wall_hours':12,
    'new_finite_tests':0,'new_source_engine_calls':0,'old_semantic_rows_replayed':0,
    'metadata_exclusion':'inherited provenance/bookkeeping convention'}
out('resources_final.json',resource)
certificate={'status':'PROVED_STEP1_EXPLICIT_AUXILIARY_FUNDING_AND_SOURCE_RESERVE',
    'domain':'every original reachable fully paired-closed five-genuine-key/core-nine auxiliary history',
    'six_key_application':'all such actual aligned erased histories from full core10/11; no B rejoining assumed',
    'uniform_parameters':['ambient size','walk length','DELETE timing/support','fringe topology/population',
        'all legal original masks','all admissible signatures','zero operations','repetitions'],
    'clipped_budget':'Q_E<=2*sum_i min(H_i,3)',
    'signed_macro_slack':'s_i=2min(H_i,3)-q_i+d_(i+1)-d_i>=0',
    'working_bank':'b_i=max_cycle(D)-d_i; actual units, zero at both selected endpoints',
    'boundary_bank_cap':2,'within_macro_queue_cap':8,
    'auxiliary_assignment':'explicit source-event/bit injection by FIFO in source_allocation.py',
    'tail_exclusion':'both bits after first3 actual A events in every auxiliary macro',
    'retained_A_credit':'both bits of fourth/later A events in each retained request; disjoint subset of tail',
    'reserve_exact':'|U|=2A(I)-Q_E(I); constructed without full B costs',
    'signed_available_pool':'U disjoint_union f_E(auxiliary-only demands)',
    'original_marginal_injection_proved':False,'positive_universal_reserve_claimed':False,
    'Step1_complete':True,'Step2_signed_repayment':'OPEN','Step3_uniform_coverage':'OPEN',
    'uniform_support_induction_proved':False,'unrestricted_CD_proved':False,'Dynamic_Optimality_proved':False,
    'new_original_CD_domain_claimed':False,'essential_OPEN_Step1_dependencies':[],
    'R1_R4_preserved':True,'Bank25':25,'frozen_graph_modified':False,'matching_terminal_modified':False,
    'h0_correction_preserved':{'actual_depth':0,'declared_depth':18,'q':9,'weight':-3},
    'zero_start_timing_scope':'one actual complete source period at a legally realized maximum-debt cyclic cut',
    'arbitrary_fixed_seam_zero_start_claimed':False,
    'proofs':['SOURCE_BRIDGE.md','AUXILIARY_FUNDING_THEOREM.md','SOURCE_IDS_AND_CYCLIC_CUT.md',
        'RETAINED_A_CREDIT.md','SIGNED_CANCELLATION.md'],
    'audit':'INDEPENDENT_PROOF_AUDIT.md','scope_audit':'SCOPE_AND_DEPENDENCY_AUDIT.md',
    'evidence':['derivation.json','independent_audit.json'],'resources':'resources_final.json',
    'audit_scope':'separate mathematical/source derivation and schema checker; not external review or full compiler formalization',
    'publication_gates':{'mathematical_Step1':'PASS','source_bridge':'PASS','separate_audit':'PASS',
        'physical_ID_nonduplication':'PASS','aligned_cyclic_cut':'PASS','scope_honesty':'PASS',
        'all_original_caps':'PASS','inherited_hashes':'PASS','tracked_tree_HEAD':'PASS'}}
out('STEP1_CERTIFICATE.json',certificate)
out('CURRENT_STATE.json',{'Step1':'PROVED_COMPLETE','Step2':'OPEN_SIGNED_REPAYMENT_INTO_EXPLICIT_AVAILABLE_POOL',
    'Step3':'OPEN_UNIFORM_SOURCE_COVERAGE','SE03_principal_induction':'OPEN','unrestricted_CD':'OPEN',
    'CD5':'SEALED_UNCHANGED','Bank25':25,'cumulative_uniform_CPU':total,'certificate':'STEP1_CERTIFICATE.json'})
prose('RESULT.md',f'''# Step1 proved and audited

Every original reachable fully closed five-key/core-nine auxiliary history
has an explicit allocation of all actual auxiliary B doubles to distinct
actual A-event/bit units. This includes every such aligned erased history
arising from full six-key core10/11, with arbitrarily persistent B disagreement.

The sealed11F/M3 proof gives Q_E<=2sum min(H_i,3). On a closed image its
one-way raw chi8 is constant. Cutting the actual source cycle at maximum
ordinary debt makes the initial bank EMPTY. The procedure carries at most
two actual units between macros and releases every surplus unit permanently.
It ends with an empty bank and an explicit disjoint reserve of size2A-Q_E.

Both units of actual A events after the first three of each macro are
protected from auxiliary funding. In particular, the fourth and later
events of every retained A request supply identified ongoing retained
credit. Certified surplus releases identify further source units through
the debt transitions. No full B cost or desired original inequality is
used to select these units.

Step1 is COMPLETE at this scope. The next obligation is Step2: prove that
unmatched original demands fit this reserve plus the actual units released
by negative interference. Its required injection has NOT been proved.
Then Step3 must establish source-complete coverage for arbitrary support.
There is no new original CD-domain or unrestricted-CD claim here.

The allocation starts empty at a legal cyclic source seam, with actual
periodic occurrence reindexing; it is not a zero-start theorem at every
fixed timestamp. All units lie inside ONE aligned rotated period; no
preperiod, invented initial balance or neighboring-copy loan is spent.
Full source closure/reachability, all private inventories, nongenuine
operations and the exact frozen h0 case are preserved. Matching-terminal
is unchanged and no native eligibility/acceptance claim is made.

Separate universal affine/source/ownership audits passed. No finite trace,
new mask/population, source engine, graph or old semantic row was run.
All{len(pins)} inherited pins and entry HEAD match; tracked tree is clean.
R1-R4 and Bank25=25 are preserved. This is mathematical certification
within the inherited framework, not external review or compiler formalization.

Cumulative CPU {total:.6f}/7200 seconds; new charged CPU {new:.6f}.
The SAME SE03 groups now use symbolic {groups['symbolic']['combined_CPU']:.6f}/120
and independent {groups['independent']['combined_CPU']:.6f}/300. No allowance
or cap reset. Remaining {7200-total:.6f} includes reserve5.
''')
prose('FINAL_INTEGRITY.md',f'''# Step1 integrity gate

Step1 alone is proved and complete. The principal SE03 induction and
unrestricted CD remain OPEN. All{len(pins)} inherited pins rehash exactly;
HEAD {head} and tracked tree remain unchanged. The two proof processes
and whole controllers are charged to the original cumulative groups.
All original resource caps pass. No failed or UNKNOWN result is promoted.

final_manifest.json hashes all current append-only files except itself.
No inherited certificate, graph, source or previous OPEN checkpoint is
rewritten. The new current-state record advances auxiliary funding only.
''')
files=[{'file':p.name,'sha256':sha(p)} for p in sorted(B.iterdir()) if p.is_file()]
out('final_manifest.json',{'status':'STEP1_PROVED_AUDITED_AND_PUBLISHED','files':files,
    'head':head,'tracked_tree_clean':True,'inherited_pins_verified':len(pins),'Step1_complete':True,
    'Step2_signed_repayment_proved':False,'Step3_uniform_coverage_proved':False,'unrestricted_CD_proved':False,
    'cumulative_uniform_CPU':total,'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'metadata_CPU_excluded':time.process_time()-start,'self_excluded':True})
print(json.dumps({'status':'STEP1_PROVED_AUDITED_AND_PUBLISHED','files_hashed':len(files),
    'cumulative_uniform_CPU':total,'Step2':'OPEN','Step3':'OPEN'}))

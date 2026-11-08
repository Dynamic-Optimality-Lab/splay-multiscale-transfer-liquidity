"""Final SE02 partial publication; supersedes advancement claims without edits."""
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
start=time.process_time();entry=read(B/'entry.json');inherit=read(B/'dependency_pins.json');pins=inherit['pins']
for p in pins:assert sha(ROOT/p['path'])==p['sha256'],p['path']
for p in read(B/'final_manifest.json')['files']:assert sha(B/p['file'])==p['sha256'],p['file']
assert sha(Path(inherit['user_directive_path']))==inherit['user_directive_sha256']
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
assert head==entry['head']
assert not subprocess.check_output(['git','status','--short','--untracked-files=no'],cwd=ROOT,text=True).strip()
attempts=[]
for path in sorted(B.glob('run_*_result.json')):
    p=read(path);c=read(B/('controller_'+p['phase']+'_exit.json'))
    assert p['termination'] is None and p['child_CPU']<p['allocated_CPU_cap']
    assert p['peak_working_set_bytes_observed']<entry['memory_cap_bytes']
    attempts.append({'phase':p['phase'],'status':p['status'],'child_CPU':p['child_CPU'],
      'whole_controller_CPU':c['whole_process_CPU_seconds'],'charged_CPU':p['child_CPU']+c['whole_process_CPU_seconds'],
      'child_cap':p['allocated_CPU_cap'],'error':p['error'],'peak_working_set_bytes_observed':p['peak_working_set_bytes_observed']})
by={p['phase']:p for p in attempts}
assert set(by)=={'derivation','independent','independent_v2','repeat_gap','repeat_gap_independent','scope'}
for name,p in by.items():
    if name=='independent':
        assert p['status']=='FAILED_OR_UNKNOWN' and p['error']['type']=='AssertionError'
        assert 'if f-e=-1' in p['error']['message']
    else:assert p['status']=='PASS' and p['error'] is None
symbolic=sum(by[n]['charged_CPU'] for n in ('derivation','repeat_gap'))
independent=sum(by[n]['charged_CPU'] for n in ('independent','independent_v2','repeat_gap_independent','scope'))
assert symbolic<120 and independent<300
new=sum(p['charged_CPU'] for p in attempts);total=entry['prior_uniform_CPU']+new
assert total+5<7200
a=read(B/'repeat_gap_independent_audit.json');scope=read(B/'scope_audit.json')
assert a['status']=='INDEPENDENT_SE02_REPEAT_GAP_AUDIT_PASS'
assert scope['status']=='FINAL_SCOPE_AUDIT_PASS_GENUINE_NEW_COVERAGE_NOT_ESTABLISHED'
assert scope['restricted_credit_law_valid'] and scope['return_pulse_class_in_completed_B_only_compositional_closure']
assert not scope['genuinely_new_CD_coverage_established'] and not scope['unrestricted_CD_proved']
resources={'prior_sealed_uniform_CPU':entry['prior_uniform_CPU'],
 'new_CPU_including_all_continuations_failure_and_whole_controllers':new,'cumulative_uniform_CPU':total,
 'global_allowance':7200,'remaining_CPU_including_reserve':7200-total,'required_reserve':5,
 'attempts':attempts,'same_original_phase_groups':[{'name':'all_SE02_symbolic','cap':120,'charged_CPU':symbolic},
    {'name':'all_SE02_independent_and_scope_including_failure','cap':300,'charged_CPU':independent}],
 'old_signature_ledger_unchanged':7195.203125,'no_cap_increase_or_allowance_renewal':True,
 'canonical_query_cap':2000000,'new_canonical_queries':0,'live_record_cap':2000000,'new_live_graph_records':0,
 'input_DAG_cap':4000000,'new_compiled_input_DAG_nodes':0,'stored_edge_cap':5000000,'new_stored_graph_edges':0,
 'memory_cap_bytes':32*1024**3,'per_phase_wall_cap_hours':12,'new_finite_tests':0,
 'old_semantic_checks_replayed':0,'metadata_bookkeeping_excluded_by_inherited_convention':True}
write('resources_final_v2.json',resources)
write('SE02_CERTIFICATE_v2.json',{
 'status':'SE02_PARTIAL_PROVED_RESTRICTED_SIGNED_TRANSFER_NO_GENUINELY_NEW_CD_COVERAGE',
 'general_accounting_proved':'aligned R=R_z-Delta; Delta=direct erased-key + signed retained-key interference',
 'restricted_source_mechanism':'repeat-gap first A event pays direct1 and indirect1; auxiliary work uses disjoint KEEP-change gap pool',
 'restricted_domain':'six genuine KEEP keys/core8 with source-certified same-side-grandchild B-return pulses covering all Kz',
 'A_reset_required':False,'arbitrary_DELETE_interleaving_allowed':True,
 'funding_premise_derived':'erased at-most-five/core<=8 -> completed B-only Q_E<=2C_E',
 'conclusion':'D=J=m, Delta=2m, A>=C_E+2m, Q_full<=2A-2m',
 'new_symbolic_family':{'period_length':23,'G':6,'core':8,'arbitrary_mark_free_hangers':9,
   'proper_repeated_paired_vertices':0,'A':23,'Q':4,'Q_E':2,'C_E':8,'Delta':2,
   'all_repetitions':'costs and distinct unit IDs multiplied by m>=1'},
 'novelty':{'outside_literal_CD5_and_corele7_predicates':True,
   'proper_paired_subwalk_concatenations_excluded':True,
   'contained_in_completed_B_only_compositional_closure':True,
   'genuinely_new_CD_coverage_established':False,
   'first_paired_reset_advancement_claim_superseded':True},
 'current_proofs':['ERASURE_ALIGNMENT.md','ROTATION_INTERFERENCE.md','REPEAT_GAP_COMPENSATION.md',
    'PRIMITIVE_CORE8_FAMILY.md','B_COMPOSITION_AUDIT.md','PROOF_AUDIT_v2.md'],
 'accepted_audits':['independent_audit_v2.json','repeat_gap_independent_audit.json','scope_audit.json'],
 'resources':'resources_final_v2.json','uniform_support_induction_proved':False,'unrestricted_CD_proved':False,
 'original_CD_counterexample_found':False,'remaining_obligation':'nonreturning B interference or uncovered auxiliary funding, with proved source-complete key selection',
 'R1_R4_preserved':True,'matching_terminal_modified':False,'frozen_graph_modified':False,'Bank25':25,
 'new_finite_tests':0,'old_semantic_checks_replayed':0,
 'audit_scope':'separate symbolic/source audits within campaign; not external peer review or whole-compiler formalization',
 'partial_publication_gates':{'restricted_law':'PASS','independent_source_audit':'PASS','novelty_scope_honesty':'PASS',
    'all_original_resource_groups':'PASS','all_inherited_hashes':'PASS','HEAD_tracked_tree':'PASS'},
 'new_global_coverage_gate':'NOT_ESTABLISHED','universal_CD_publication_gate':'OPEN'})
write('CURRENT_STATE_v2.json',{'SE02':'CLOSED_WITH_HONEST_PARTIAL_OUTCOME',
 'restricted_signed_credit_rule':'PROVED','genuinely_new_CD_coverage':'NOT_ESTABLISHED_B_COMPOSITION_ALREADY_COVERS_CLASS',
 'CD5':'SEALED_PROVED_UNCHANGED','uniform_support_induction':'OPEN','unrestricted_CD':'OPEN',
 'next_obligation':'nonresetting full/erased B histories or independently funded residual class; no favorable selection assumed',
 'cumulative_uniform_CPU':total,'remaining_CPU_including_reserve':7200-total,'matching_terminal':'FROZEN','Bank25':25})
result=f'''# SE02 final outcome: restricted compensation proved; new CD coverage not established

The exact aligned signed identity and direct/indirect decomposition are proved.
Positive and negative interference are retained, with explicit transient and
period normalization. No favorable erased key or indirect sign is assumed.

**Restricted source-derived compensation rule proved:** for six-genuine-key/
core8 walks whose Kz occur in the specified B-return pulses, reserve auxiliary
B funding from erased KEEP-CHANGE gaps using the completed stronger B-only
Q_E<=2C_E theorem. A first real event in each relevant KEEP-REPEAT gap then
has two unreserved units, paying the direct z double and indirect y double.
The rule permits arbitrary A changes and DELETE interleaving; no A reset is
required. Distinct source/gap/copy/bit IDs prevent reuse. Exact source counts give

    D=J=m, Delta=2m, A>=C_E+2m, Q_full<=2A-2m.

The23-occurrence symbolic family has G6/core8, nine arbitrary gap BSTs, two
starved marginal consumers, and no proper repeated paired vertex. Its totals
are A23,Q4,Q_E2,C_E8,Delta2, with all-m repetition proved symbolically. It is
outside the literal CD(5)/core<=7 classes and cannot split into proper paired-
closed components from those classes.

**Final novelty limitation:** the B-return pulses ARE closed B-only two-key
components, and their B-only backbone is already covered by completed proofs.
C_full=C_E+2m and Q_full=Q_E+2m give the same bound by existing B-composition.
Thus genuinely new original CD coverage beyond the completed proof closure
was NOT established. The first paired-reset family's advancement claim is also
downgraded. Valid restricted identities/credit maps are retained; they are not
promoted to a new global-domain theorem. Bank25 remains25.

Uniform support induction and unrestricted CD remain OPEN. The next necessary
source leverage is on B histories that do not rejoin through these return
identities, or on an uncovered auxiliary funding class. Scalar CD(5) alone
does not supply Q_E<=2C_E on core9, and no key-selection/completeness theorem
is assumed.

Audit:925 inherited pins plus the directive; original rotation free-term
identities; exact signed, parity, transient and reservation certificates; and
a final compositional novelty rejection. All checks are symbolic universal
proofs, not finite tree/population tests. No solver/root queries, old semantic
replays, source/graph edits or matching-terminal changes. R1-R4 are preserved.
The audits are within this campaign, not external peer review or full compiler
formalization. The failed prose-locator attempt is preserved and charged.

TOTAL SE02 CPU:{new:.6f}s including every continuation, failed attempt and
whole controller. Cumulative uniform CPU:{total:.6f}/7200s; remaining
{7200-total:.6f}s including reserve5. ORIGINAL combined groups: symbolic
{symbolic:.6f}/120s; independent/scope{independent:.6f}/300s. No reset/renewal.

Current certificate: SE02_CERTIFICATE_v2.json. Main mechanism:
REPEAT_GAP_COMPENSATION.md. Source family: PRIMITIVE_CORE8_FAMILY.md.
Novelty boundary: B_COMPOSITION_AUDIT.md. Final audit: PROOF_AUDIT_v2.md.
Resources: resources_final_v2.json. This final version supersedes advancement
interpretations of the first publication; every old artifact stays immutable.
'''
with (B/'RESULT_v2.md').open('x',encoding='utf-8') as f:f.write(result)
files=[{'file':p.name,'sha256':sha(p)} for p in sorted(B.iterdir()) if p.is_file()]
write('final_manifest_v2.json',{
 'status':'SE02_AUDITED_PARTIAL_OUTCOME_PUBLISHED','files':files,'certificate':'SE02_CERTIFICATE_v2.json',
 'restricted_compensation_proved':True,'genuinely_new_CD_coverage_established':False,
 'uniform_support_induction_proved':False,'unrestricted_CD_proved':False,'original_CD_counterexample_found':False,
 'old_inputs_and_first_publication_unchanged':True,'declared_input_pins_verified':len(pins),
 'R1_R4_preserved':True,'matching_terminal_modified':False,'Bank25':25,'new_finite_tests':0,
 'HEAD':head,'tracked_tree_clean':True,'cumulative_uniform_CPU':total,
 'sealed_UTC':datetime.now(timezone.utc).isoformat(),'metadata_CPU_excluded_for_publication':time.process_time()-start,
 'manifest_self_excluded_from_its_file_hash_list':True})
print(json.dumps({'status':'SE02_AUDITED_PARTIAL_OUTCOME_PUBLISHED','SE02_CPU':new,'cumulative_uniform_CPU':total,
 'remaining_CPU':7200-total,'symbolic_group_CPU':symbolic,'independent_group_CPU':independent,
 'files_sealed':len(files),'genuinely_new_CD_coverage':False,'universal_CD':'OPEN'}))

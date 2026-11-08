"""Seal the full M3 proof only after independent audits and resource gates."""
import json,hashlib,subprocess,time
from pathlib import Path
BASE=Path(__file__).resolve().parent;R=BASE.parent;P20=R/'M3_XFER20';P19=R/'M3_XFER19'
def read(p):return json.loads(p.read_text())
def write(n,o):
    with (BASE/n).open('x',encoding='utf-8') as f:json.dump(o,f,indent=2)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def charges(folder):
    out={};runs={}
    for p in folder.glob('run_*_result.json'):
        q=read(p);n=q['phase'];ctrl=read(folder/('controller_'+n+'_exit.json'))
        assert q['child_CPU']<=q['allocated_CPU_cap']
        out[n]=q['child_CPU']+ctrl['whole_process_CPU_seconds'];runs[n]=q
    return out,runs
def main():
    audit=read(BASE/'full_m3_audit.json');contract=read(BASE/'contract_audit.json');low=read(BASE/'audit_extremal.json')
    assert audit['status']=='INDEPENDENT_FULL_ORIGINAL_M3_CERTIFICATE_AUDIT_PASS'
    assert audit['missing_new_signed_obligations']==0 and audit['Gamma1_covered_word_obligations']==4152
    assert contract['status']=='INDEPENDENT_LITERAL_LOW_CONTRACT_AND_GAMMA0_AUDIT_PASS'
    assert low['status']=='COMPLETE_EXTREMAL_HELPER_AND_ALL_LOW_AUDIT_PASS' and low['pending_jobs']==0 and low['unresolved'] is None
    for n in ('extremal','full_m3','contract'):assert read(BASE/('run_'+n+'_result.json'))['status']=='PASS'
    c20,r20=charges(P20);c21,r21=charges(BASE)
    groups=[('positive_source_construction_20',300,sum(c20[n] for n in ('positive','completion','completion_v2','gamma','joint'))),
      ('positive_independent_20',300,c20['independent']),
      ('positive_reductions_and_prefix_20',120,sum(c20[n] for n in ('reductions','visibility','prefix'))),
      ('extremal_source_construction_21',300,c21['extremal']),
      ('full_M3_independent_audit_21',300,c21['full_m3']+c21['contract'])]
    assert set(c20)=={'positive','completion','completion_v2','gamma','joint','independent','reductions','visibility','prefix'}
    assert set(c21)=={'extremal','full_m3','contract'}
    assert all(value<=cap for name,cap,value in groups)
    prior=read(P19/'resources_final.json')['cumulative_uniform_CPU'];total=prior+sum(c20.values())+sum(c21.values())
    assert read(BASE/'entry.json')['prior_uniform_CPU']==prior+sum(c20.values())
    assert total+5<=7200
    head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
    assert head==read(BASE/'entry.json')['head']==read(P20/'entry.json')['head']
    assert not subprocess.check_output(['git','status','--short','--untracked-files=no'],text=True)
    for q in audit['verified_original_dependency_pins']:
        p=Path(q['path']);assert hashlib.sha256(Path('\\\\?\\'+str(p.resolve())).read_bytes()).hexdigest()==q['sha256']
    # Verify the complete previous sealed manifest again as immutable metadata;
    # no prior source/signed check is executed.
    for q in read(P19/'final_manifest.json')['files']:assert sha(P19/q['file'])==q['sha256']
    base=read(P19/'STEP4_CERTIFICATE.json');stats19=read(P19/'step4_audit.json')
    new_total=audit['required_new_signed_clause_word_obligations'];all_signed=stats19['required_clause_word_obligations']+new_total
    allruns=list(r20.values())+list(r21.values())
    resources={'prior_sealed_XFER19_CPU':prior,'new_task_CPU_including_failures_and_controllers':sum(c20.values())+sum(c21.values()),
      'cumulative_uniform_CPU':total,'global_allowance':7200,'remaining_CPU_including_reserve':7200-total,'required_reserve':5,
      'per_phase_groups':[{'name':n,'cap':cap,'charged_CPU':v} for n,cap,v in groups],
      'no_old_phase_renewed':True,'old_signature_ledger_unchanged':7195.203125,
      'canonical_query_cap':2000000,'new_original_root_queries':0,'largest_reported_new_phase_SMT_query_count':max(
        read(P20/'audit_independent.json')['queries'],low['queries']),
      'live_record_cap':2000000,'public_clauses_in_combined_correction':len(base['clauses'])+len(low['clauses']),
      'input_DAG_cap':4000000,'input_DAG_conservative_bound':audit['input_DAG_conservative_bound'],
      'stored_edge_cap':5000000,'signed_clause_word_obligations_inherited_plus_new':all_signed,
      'memory_cap_bytes':32*1024**3,'peak_working_set_bytes_observed':max(q['peak_working_set_bytes_observed'] for q in allruns),
      'per_phase_wall_cap_hours':12,'metadata_bookkeeping_excluded_by_inherited_convention':True,
      'no_finite_population_or_mask_tests':True,'no_completed_accepted_semantic_check_replays':True}
    assert resources['input_DAG_conservative_bound']<=4000000 and resources['peak_working_set_bytes_observed']<32*1024**3
    write('resources_final.json',resources)
    certificate={'name':'Full original two-sort M3 certificate','status':'PROVED_UNIVERSAL_FULL_M3',
      'domain':{'mask':'original9-bit mask with exactly5 marked cores','sigma':'EVERY original admissible ten-component signature',
        'no_new_support_or_population_restriction':True,'ordinary_coordinates':147,'midpoint_coordinates':127,
        'original_R1_R4_frozen_model':True},
      'ordinary_debt_equation':'D=max(F4,1_(P AND N AND C1),2*1_(P AND N AND C2))',
      'ordinary_J_equation':'J=-D','ordinary_potential':'W(O)=-D(O)-5*chi8(O.b)',
      'midpoint_potential':'W(M)=-5*chi8(M.b)',
      'chi8':'original raw b.kr[8]==0 AND b.rr[8]==19','debt_range':[0,2],'J_range':[-2,0],'W_range':[-7,0],
      'parent_Step4_location':'M3_XFER19/STEP4_CERTIFICATE.json','parent_Step4_sha256':sha(P19/'STEP4_CERTIFICATE.json'),
      'parent_Step4_certificate':base,'parent_nested_path_resolution':'relative references inside copied parent resolve from M3_XFER19',
      'completion_anchors':low['anchors'],'completion_clauses':low['clauses'],
      'completion_clause_semantics':{'positive_anchor':'listed marked old-root role at L/LL if role<current root, otherwise R/RR',
        'score_cube':'all listed ScoreAt(position,role), marks true and nonmarks false; omitted coordinates/bits free',
        'outer_guard':'P proper synchronized marked ordinary root, N no nonroot ScoreAt(current root)',
        'ScoreAt':'original nonroot kind0,isS=true,index=role; root.kind UNUSED',
        'Ck':'union of matching exact-core clauses with level>=k'},
      'full_state_and_signature_closure':{'no_vertices_or_edges_identified':True,'SAME_actual_midpoint':True,
        'independent_OM_MO_private_witnesses':True,'HIGH_v_free':True,'weak_LE_and_G_rules_unchanged':True,
        'unused_fields_free':True,'private_inventory_history_new_observable_used':False},
      'weights':{'OO':'original2H-q','OM':'original6-q','MO':0,'MM':'no edge'},
      'corrected_h0':{'actual_depth':0,'declared_depth':18,'q':9,'weight':-3},
      'pointwise_theorem':'EVERY original edge satisfies w(s,t)>=W(t)-W(s)',
      'finite_walk_theorem':'sum(w)>=W(end)-W(start)>=-7','closed_walk_theorem':'EVERY original fully closed walk has sum(w)>=0',
      'constant_chi_region_finite_walk_bound':-2,'M3_complete':True,'Dynamic_Optimality_proved':False,
      'signed_clause_word_obligations_including_Step4':all_signed,
      'critical_helper_word_obligations':4152,'missing_obligations':0,
      'proof':'FULL_M3_PROOF.md','specification':'M3_POTENTIAL_SPEC.md',
      'independent_audit':['full_m3_audit.json','contract_audit.json','FULL_AUDIT_SCOPE.md','ORIGINAL_BUDGET_AND_FLOOR_ADDENDUM.md'],
      'audit_scope':'separate source/coverage/dependency/sign derivation and exact certificate audit; reuses completed UNSAT conclusions; not external review or full compiler formalization'}
    write('M3_CERTIFICATE.json',certificate)
    dependencies=list(audit['verified_original_dependency_pins'])
    for folder,names in [(P19,['STEP4_CERTIFICATE.json','step4_audit.json','step4_scope_audit.json','final_manifest.json']),
      (P20,['audit_prefix.json','audit_reductions.json','audit_visibility.json','positive_inventory.json','audit_completion_v2.json',
        'audit_joint.json','audit_independent.json','completion_v2_checkpoints.jsonl','joint_checkpoints.jsonl','independent_checkpoints.jsonl',
        'gamma_checkpoints.jsonl','joint_gamma_checkpoints.jsonl','independent_gamma_checkpoints.jsonl'])]:
        for n in names:dependencies.append({'path':str((folder/n).resolve()),'sha256':sha(folder/n)})
    write('dependencies_final.json',{'all_reused_original_pins_unchanged':True,'completed_proofs_reused_not_replayed':True,
      'old_finite_sector_potentials_not_used':True,'pins':dependencies})
    write('coverage_final.json',{'status':'COMPLETE_ORIGINAL_M3_COVERAGE',
      'LOW_negative':'inherited global H1 theorem plus signed preservation',
      'LOW_zero':'sealed Step4 plus signed preservation','LOW_H1_plus1':'318 critical rows/275 generic positive anchors plus signed source proof',
      'LOW_Gamma1_plus1':{'critical_word_jobs':4152,'closed_jobs':4152,'proof_kinds':audit['Gamma1_proof_kinds'],
        'other_cases':'depth1 parallel Step4 H1; depth>=3 range; odd terminal impossible; actual psi target floor'},
      'LOW_Gamma0':'original actual-preterminal psi floor and range; independent coefficient audit',
      'LOW_price_at_least2':'range','LOW_genuine_H0_or_Gamma_greater_than1':'excluded by original charge/change injection with literal H<=2',
      'HIGH_OM':'same chi>=2; entering>=-3; leaving impossible','HIGH_MO':'zero price and unchanged chi','MM':'no original edge',
      'all_original_masks_and_signatures':True,'full_state_closure':True,'remaining_M3_cases':0,
      'all_signed_clause_word_obligations_including_Step4':all_signed,
      'new_signed_clause_word_obligations':new_total,'missing_signed_obligations':0})
    result=f'''# M3 closed on the full frozen original graph

M3 is PROVED—UNIVERSAL for every original legal mask and every admissible
signature, including arbitrary multi-support signatures. All remaining
+1 LOW obligations are closed. The combined certificate satisfies

    W(O)=-D(O)-5chi8(O.b),   W(M)=-5chi8(M.b),   0<=D<=2,
    w(s,t)>=W(t)-W(s) on EVERY original edge.

Every original fully closed walk therefore has nonnegative total weight.
Every finite original walk has weight at least-7; within a fixed chi8
region the endpoint bound is-2. There is no bounded transfer horizon,
population/support restriction, selected private completion or unsigned
deficit-count premise.

The full independent audit covers {all_signed} inherited/new signed
source-clause/word obligations and all4152 critical helper word cases,
with ZERO missing. The4359 new completion clauses combine with the3413
Step4 clauses and their fixed explicit baseline. Source-visible capacity
contradictions and the tall extremal ceiling remove only proved-empty
failure domains. Hidden anonymous releases and negative/zero/+1 exits
from every newly raised source were checked universally. Actual maximum
psi coverage was audited separately, without assuming psi symmetry.

R1–R4, original147-O/127-M interfaces, SAME actual midpoint with independent
witnesses, free HIGH v, weak LE/G/unused fields, original prices and
h0(actual0,declared18,q9,w=-3) are preserved. The pointwise proof telescopes
on ORIGINAL FULL states. No finite population/mask tests, new original
root evaluations or completed accepted semantic-check replays were used.

The independent full source/coverage/dependency/sign audit and literal
original LOW-budget/Gamma0 audit passed. All verified original dependency
pins, the sealed prior manifest, HEAD and tracked state are unchanged.
Old capped/rejected attempts and their unproved statuses remain intact;
their trial tails are not proof premises. Source/audit phases remained
within their original caps. Cumulative CPU including all failures and
controllers is {total}/7200; remaining {7200-total}, including reserve5.
All other current limits pass resources_final.json.

Concrete certificate: M3_CERTIFICATE.json. Full proof: FULL_M3_PROOF.md.
Function specification: M3_POTENTIAL_SPEC.md. Separate audit:
full_m3_audit.json and contract_audit.json. Complete coverage:
coverage_final.json. Exact pins/resources: dependencies_final.json and
resources_final.json. This is a separate audit within the campaign,
not external review or formal verification of the whole compiler.

M3 is closed. Dynamic Optimality and unrelated later pipeline gates are
not promoted by this certificate.
'''
    with (BASE/'RESULT.md').open('x',encoding='utf-8') as f:f.write(result)
    write('CURRENT_STATE.json',{'M3':'PROVED_UNIVERSAL_CLOSED','Step4':'CLOSED','remaining_M3_cases':0,
      'certificate':'M3_CERTIFICATE.json','proof':'FULL_M3_PROOF.md','audit':'full_m3_audit.json',
      'all_original_signatures':True,'new_finite_tests':0,'R1_R4_preserved':True,'CPU':total,'CPU_remaining':7200-total,
      'Dynamic_Optimality':'NOT_PROMOTED; separate remaining pipeline obligations'})
    pins=[{'file':p.name,'sha256':sha(p)} for p in sorted(BASE.iterdir()) if p.is_file()]
    write('final_manifest.json',{'status':'FULL_M3_CLOSED_ALL_PUBLICATION_GATES_PASS','files':pins,'HEAD':head,
      'tracked_tree_clean':True,'all_reused_original_dependency_pins_unchanged':True,'M3_complete':True,
      'Dynamic_Optimality_proved':False,'metadata_CPU_excluded_by_inherited_convention':time.process_time()})
    print(json.dumps({'M3_complete':True,'signed_clause_word_obligations':all_signed,'critical_helper_cases':4152,
      'missing_obligations':0,'CPU':total,'remaining_CPU':7200-total,'files_pinned':len(pins),'HEAD':head},indent=2),flush=True)
if __name__=='__main__':main()

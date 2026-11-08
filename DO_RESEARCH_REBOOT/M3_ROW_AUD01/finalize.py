"""Publish the original SAT witness, independent audit and prior-lift correction."""
import json,subprocess,hashlib
from pathlib import Path
from entry import BASE,sha
def read(p):return json.loads(p.read_text())
def write(p,v):
    with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    assert not (BASE/'final_manifest.json').exists();run=read(BASE/'run_result.json');ctrl=read(BASE/'controller_exit.json');binding=read(BASE/'binding_audit.json');w=read(BASE/'witness.json');v=read(BASE/'independent_verification.json');r=read(BASE.parent/'M3_UNIFORM02/case_000/obstruction.json');old_attempt=read(BASE.parent/'M3_UNIFORM02/case_000/original_attempt.json')
    assert run['status']=='ORIGINAL_ROW_REALIZABLE_AND_INDEPENDENTLY_VERIFIED' and run['failure'] is None and ctrl['error'] is None
    assert binding['status']=='EXACT_OLD_ADAPTER_BINDING_MISMATCH_CONFIRMED' and not binding['old_root_replayed']
    assert w['status']=='SAT_ORIGINAL_LOW_WEIGHT_PLUS_ONE_ROW' and v['status']=='INDEPENDENT_ORIGINAL_LOW_REALIZABILITY_VERIFIED'
    assert w['original_root'] and v['original_root'] and v['namespace_rename_bijective'] and not v['factory_called']
    assert (w['H'],w['q'],w['weight'])==(v['H'],v['q'],v['weight'])==(1,1,1)
    assert (v['A_depth'],v['B_depth'])==(1,2) and v['all147_source_and_destination_coordinates_match']
    assert w['source']==old_attempt['source'] and w['destination']==old_attempt['destination']
    assert w['environment_sha256']==hashlib.sha256(json.dumps(w['environment'],sort_keys=True).encode()).hexdigest()
    assert (v['source_D_run'],v['destination_D_run'],v['candidate_residual'])==(2,0,-1)
    assert v['candidate_full_W_residual']==-1 and v['old_certificate_residual']==0 and v['chi8'] and not v['full_endpoints_close']
    assert max(w['DAG_nodes'],v['DAG_nodes'])<4000000 and w['variables']==v['variables']<2000000
    for e in run['events']:assert e['error'] is None and e['CPU_charged']<e['allocated_cap']<= (120 if e['phase']=='binding_audit' else 300)
    newCPU=run['new_child_process_CPU']+ctrl['whole_process_CPU_seconds'];total=654.703125+newCPU;assert total<7200-5
    resources={'prior_conservative_uniform_charge_retained':654.703125,'new_exact_child_process_CPU':run['new_child_process_CPU'],'new_controller_CPU_through_finally':ctrl['whole_process_CPU_seconds'],'new_measured_experimental_CPU':newCPU,'cumulative_accounted_CPU':total,'finite_CPU_ceiling':7200,'guaranteed_remaining_CPU':7200-total,'old_sigma_campaign_ledger_unchanged':7195.203125,'current_CPU_caps_preserved':[120,300,300],'source_and_independent_audit_CPU_cap':300,'canonical_query_cap':2000000,'new_constructive_original_root_evaluations':1,'new_independent_original_root_evaluations':1,'independent_A_rotation_replays':1,'independent_B_rotation_replays':1,'old_matrix_or_debt_censuses_repeated':0,'max_DAG_nodes':max(w['DAG_nodes'],v['DAG_nodes']),'max_variables':max(w['variables'],v['variables']),'no_profile_or_signature_enumeration':True,'metadata_hashing_convention':'entry/final preservation bookkeeping excluded as in prior campaigns'}
    write(BASE/'resources.json',resources)
    names=['RESEARCH_RULES.md','M3_UNIFORM01/original_lift.py','M3_UNIFORM02/original_lift.py','M3_UNIFORM02/RESULT.md','M3_UNIFORM02/PROOF_AUDIT.md','M3_UNIFORM02/STRATEGY_REVIEW.md','M3_UNIFORM02/resources.json','M3_UNIFORM02/case_000/obstruction.json','M3_UNIFORM02/case_000/obstruction_audit.json','M3_UNIFORM02/case_000/formula_identity_audit.json','M3_UNIFORM02/case_000/C_values.json','M3_UNIFORM02/case_000/original_attempt.json','M3_POP5_RISK01/source_audit_batch.py','M3_POP5_RISK01/certificate.json','M3_POP5_RISK01/DOMAIN_THEOREM.md','M3_UNITPAIR01/B_bank.json','M3_UNITPAIR01/proposal_factory_v2.py','M3_TWOGAP_AUD01/reference.py','M3_TWOGAP_AUD01/source_audit.py','M3_GAPINT01/interior_original.py','06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER/PC_TYPED_DAG.py','06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_LOW_COMPILER.py']
    write(BASE/'dependencies.json',{'completed_checks_reused_not_replayed':True,'files':[{'path':(BASE.parent/n).as_posix(),'sha256':sha(BASE.parent/n)} for n in names]})
    old=read(BASE/'entry_baseline.json');pins={p['path'] for p in old['files']}
    for i,p in enumerate(old['files']):
        assert sha(Path(p['path']))==p['sha256'],p['path']
        if (i+1)%500==0:print(json.dumps({'old_files_verified':i+1,'total':len(pins)}),flush=True)
    additions=[p for p in Path('DO_RESEARCH_REBOOT').rglob('*') if p.is_file() and BASE not in p.parents and p.as_posix() not in pins]
    assert all(p.as_posix().startswith('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/') for p in additions)
    write(BASE/'concurrent_additions.json',{'not_mathematical_dependencies':True,'files':[{'path':p.as_posix(),'sha256':sha(p)} for p in additions]})
    assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==old['head'] and not subprocess.check_output(['git','status','--short','--untracked-files=no'],text=True)
    integrity={'status':'PASS','old_files_unchanged':len(pins),'head':old['head'],'tracked_tree_clean':True,'writes_confined_here':True,'claim_scope':'this campaign only','concurrent_U4_additions':len(additions)}
    write(BASE/'integrity.json',integrity)
    correction='''# Correction to the previous uniform-formula lift attempts

This addendum supersedes the interpretation of the source-rejection
statements in M3_UNIFORM02/RESULT.md, PROOF_AUDIT.md and STRATEGY_REVIEW.md.
Old files and their exact recorded evaluations remain unchanged.

The UNIFORM01 and UNIFORM02 adapters called build_slow(dag,'UNIFL'), but
their unmodified witness factory populates names MXLw,MXLv,MXLbt,MXL_H,
MXL_w and MXLsb. State fill() follows the passed state object, so source
and destination interfaces were filled; the intended private witness was
not. In the saved UNIFORM02 environment UNIFLw_p0=False, UNIFLw_nev=0,
UNIFL_H=0. The unchanged original root consequently rejects that wrongly
bound assignment. This was an adapter error, not evidence that the
intended physical completion violated original semantics.

The new audit compiles MXL to match the factory, without changing any
source predicate. It accepts a witness with EXACTLY the same full147
source and destination states as the old attempt's proposed interfaces.
An independent process builds the original root under ROWV, bijectively
renames the complete saved assignment, calls no fixture factory and
again obtains TRUE. Independent parent-map A/B replay confirms the
actual depths1/2, H1,q1 and weight+1.

Therefore the specific UNIFORM02 row IS original-realizable, and its
specified sign-run formula IS refuted on the original LOW relation.
That status upgrades the prior original-validity OPEN result for this
candidate. No original realization of the separate UNIFORM01 row was
tested here; its original validity stays unresolved by this audit.

The earlier exact proof-matrix/debt audits were unaffected. Prior signature
source controls use matching MXL tags and remain unchanged. No existing
valid certificate or M3 model is withdrawn. This audit proves no negative
cycle, no new J formula and no full M3/Dynamic Optimality theorem.
'''
    with (BASE/'PRIOR_LIFT_CORRECTION.md').open('x',encoding='utf-8') as f:f.write(correction)
    proof='''# Exact original LOW realization of the weight+1 obstruction

Status: FINITE-EXACT original witness, independently verified. This proves
existential realizability of the SPECIFIED row. It is REFUTED-EXACT for
the sign-run formula on the original LOW relation, not for M3.

The shared signature is sigma=(4,1,0,...,0), legal mask341={0,2,4,6,8}.
The full original states have core/profile IDs
(1647,2073)->(2403,2072). Their normalized A shadows are root1,L0,R4,
RL2,RR6 followed by root4,L1,R6,LL0,LR2 (other positions opaque/empty).
One terminal KEEP of Score4 is at A depth1 and B depth2. Thus original
H=1,q=floor(2/2)=1,w=2H-q=+1. Both states satisfy chi8; all147 original
coordinates at each endpoint, including unused alpha fields and B lo/hi,
are saved in witness.json along with ALL9544 original input variables.

The complete unchanged original LOW predicate accepts this assignment.
This includes its structural, inventory, weak-LE, beta/shadow, repair,
root-termination, event/path and exact B-controller obligations. A concrete
SAT witness supplies private variables; the chosen completion is not made
into an admissibility rule. No universal uniqueness/completion assumption
or restriction of G/other private cases is introduced.

Independent verification rebuilds the original predicate under ROWV,
checks an exact bijection from saved MXL names, validates every variable's
type/width, evaluates the root TRUE and extracts/computes ALL147 source
and destination coordinates anew. No witness factory is invoked. It
additionally reconstructs this witness's visible prefix and replays the
A splay and the B splay with the separate parent-map implementation.
The A/B depths, target, H,q,w and normalized profiles match exactly.
The full original environment is the authoritative check; opaque/empty
erasure is only an auxiliary view for this concrete independent replay.

Reused independent formula-value audits give D_run(s)=2,D_run(t)=0,
so J_run(s)=-2,J_run(t)=0. Therefore

   w-J_run(t)+J_run(s)=1-0-2=-1.

Since chi8 is unchanged, the full correction W=-D_run-5chi8 has the
same residual. This is an ACTUAL original inequality violation. The
existing valid table instead gives J_old(s)=-2,J_old(t)=-1 and residual0.
Any candidate that assigns J(s)=-2 here must assign J(t)<=-1 to respect
this actual edge. This alone does not force every future candidate to
choose J(s)=-2; no unvalidated predecessor trace is assumed original.

The edge has positive weight and its FULL endpoints do not close. It
is not a negative cycle and does not refute M3. The 3761 existing signature
certificates, including this sector's valid table, remain intact. No
formula or signature enumeration was tried in this audit.
'''
    with (BASE/'PROOF_AUDIT.md').open('x',encoding='utf-8') as f:f.write(proof)
    result={'status':'ORIGINAL_LOW_ROW_REALIZABLE_INDEPENDENTLY_VERIFIED','original_realizability':'PROVED_BY_EXACT_SAT_WITNESS','sign_run_formula_original_LOW_status':'REFUTED_EXACT','mu':341,'sigma':w['source']['sigma'],'source_B_core_id':1647,'source_A_profile_id':2073,'destination_B_core_id':2403,'destination_A_profile_id':2072,'A_depth':1,'B_depth':2,'H':1,'q':1,'weight':1,'terminal_target':4,'candidate_J_source':-2,'candidate_J_destination':0,'candidate_residual':-1,'candidate_full_W_residual':-1,'old_certificate_residual':0,'chi8':True,'both_original_predicate_evaluations_true':True,'fresh_namespace_independent_verification':True,'all147_endpoint_coordinates_verified':True,'independent_A_and_B_parent_map_replay':True,'old_and_new_proposed_shared_endpoints_identical':True,'prior_binding_bug_corrected_in_new_adapter_only':True,'original_predicate_modified':False,'all_private_freedoms_preserved_in_original_definition':True,'unrealizability_claimed':False,'original_negative_cycle_certified':False,'full_endpoints_close':False,'M3_status':'OPEN','new_J_formula_tried':False,'new_M3_signature_certificates':0,'NET_ORIGINAL_M3_PROOF_ADVANCEMENT':0,'source_realizability_obligation_resolved':True,'R1_R4_preserved':True,'h0_correction_preserved':True,'old_matrix_and_debt_checks_reused':True,'environment_sha256':w['environment_sha256'],'resources':resources,'integrity':integrity}
    write(BASE/'certificate.json',result)
    lines=['# Original LOW audit of the weight+1 obstruction','',
      '**REALIZABLE under the unchanged original LOW semantics, independently verified.** The row is not merely an artifact of the proof superrelation. The sign-run formula is now refuted by an actual original LOW edge.','',
      'Witness: mu341; sigma=(4,1,0,...,0); (coreB1647,A2073)->(coreB2403,A2072); terminal KEEP Score4; A depth1,B depth2,H1,q1,w=+1. All147 raw endpoint coordinates and all9544 input variables are saved. Both endpoints lie in chi8.',
      'Original LOW root is TRUE in construction. A separate process with fresh ROWV namespace and bijective rebinding checks the unchanged root TRUE again, all types/widths, all147 endpoint fields and independent parent-map A/B rotations. It calls no witness factory. The prior independently audited debt values are reused.','',
      'Candidate J_run=-2->0 gives residual1-0-2=-1 (also for full W=-D-5chi8). The existing valid certificate gives J_old=-2->-1, residual0. The edge is positive and its full endpoints are distinct: no negative cycle or refutation of M3 is established.',
      'CORRECTION: the earlier lift compiled UNIFL while its factory filled MXL fields. Its actual witness root slot and event count remained zero. The recorded FALSE was a binding error in the adapter, not rejection of the intended completion. This new correctly bound witness has EXACTLY the same full shared endpoints as the old proposal. Prior files are preserved; see PRIOR_LIFT_CORRECTION.md.','',
      'This settles this specific source-realizability obligation. No claim that every mask/completion works is made. Private counts/bills, weak LE, G handling and the original compiler were not restricted or changed. No new formula was tried; the separate UNIFORM01 original-row question was not repeated.',
      f'R1-R4/current caps and corrected h0 preserved. New experiment/controller CPU:{newCPU}; retained prior654.703125; cumulative accounted{total}/7200; guaranteed remaining{7200-total}. Both source audits are below300 CPU seconds; binding audit below120; DAG1,400,081<4m; no profile enumeration or old matrix/debt replay.',
      f'All {len(pins)} pinned prior files unchanged; HEAD/tracked tree unchanged. Concurrent U4 additions recorded separately.','',
      '**M3 remains OPEN.** No new M3 signature certificate or negative cycle was promoted. The exact witness, independent verification and corrected interpretation are in witness.json, independent_verification.json and PROOF_AUDIT.md.']
    with (BASE/'RESULT.md').open('x',encoding='utf-8') as f:f.write('\n'.join(lines)+'\n')
    result['files']=[{'path':p.as_posix(),'sha256':sha(p)} for p in sorted(BASE.rglob('*')) if p.is_file()]
    write(BASE/'final_manifest.json',result);print(json.dumps({k:v for k,v in result.items() if k!='files'},indent=2),flush=True)
if __name__=='__main__':main()
